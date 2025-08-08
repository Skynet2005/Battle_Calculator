# server/main.py

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, validator, Field
from typing import List, Dict, Any, Optional
import os
from dotenv import load_dotenv, find_dotenv
import json
import httpx
import time
import random
import threading
import hashlib
from pathlib import Path
import re  # for markdown -> plaintext sanitation

# raw data
from hero_data.hero_loader import HEROES as RAW_HEROES
from troop_data.troop_definitions import TROOP_DEFINITIONS

# import your updated expedition simulation
from expedition_battle_mechanics.simulation import simulate_battle, monte_carlo_battle

# expedition engine
from expedition_battle_mechanics.loader       import hero_from_dict
from expedition_battle_mechanics.combat_state import BattleReportInput
from expedition_battle_mechanics.formation    import RallyFormation
from expedition_battle_mechanics.bonus        import BonusSource


# -----------------------------
# App + CORS
# -----------------------------
load_dotenv(find_dotenv())
app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


# -----------------------------
# Globals for throttling/circuit breaker/cache
# -----------------------------
ANALYZE_LAST_CALL_TS: float = 0.0  # throttle OpenAI calls
ANALYZE_SEM = threading.Semaphore(int(os.getenv("OPENAI_CONCURRENCY", "1")))
ANALYZE_COOLDOWN_UNTIL: float = 0.0  # 429 circuit-breaker pause end timestamp

ANALYZE_CACHE_TTL = int(os.getenv("ANALYZE_CACHE_TTL", "60"))  # seconds
_ANALYZE_CACHE: Dict[str, tuple[float, str]] = {}  # key: hash -> (ts, text)


# -----------------------------
# Models
# -----------------------------
class SimRequest(BaseModel):
    attackerHeroes:        List[str]
    defenderHeroes:        List[str]
    attackerRatios:        Dict[str, float]
    defenderRatios:        Dict[str, float]
    attackerCapacity:      int
    defenderCapacity:      int
    sims:                  int
    attackerTroops:        Dict[str, str]
    defenderTroops:        Dict[str, str]
    attackerSupportHeroes: List[str] = Field(default_factory=list)
    defenderSupportHeroes: List[str] = Field(default_factory=list)

    @validator("attackerRatios", "defenderRatios")
    def check_ratios_sum(cls, v):
        total = sum(v.get(c, 0) for c in ("Infantry","Lancer","Marksman"))
        if abs(total - 1.0) > 1e-6:
            raise ValueError(f"ratios must sum to 1.0 (got {total})")
        return v

    @validator("attackerTroops", "defenderTroops")
    def check_all_classes_present(cls, v):
        missing = [c for c in ("Infantry","Lancer","Marksman") if c not in v or not v[c]]
        if missing:
            raise ValueError(f"Must specify a FC for each class ({missing})")
        return v


class AnalysisRequest(BaseModel):
    result: Dict[str, Any]


# -----------------------------
# Helpers (cache, cooldown, hashing, prompt compaction, RL logging, markdown→text)
# -----------------------------
def _hash_payload(s: str) -> str:
    return hashlib.sha256(s.encode("utf-8")).hexdigest()


def _cache_get(h: str) -> Optional[str]:
    v = _ANALYZE_CACHE.get(h)
    if not v:
        return None
    ts, text = v
    if time.time() - ts <= ANALYZE_CACHE_TTL:
        return text
    _ANALYZE_CACHE.pop(h, None)
    return None


def _cache_put(h: str, text: str) -> None:
    # prune oldest ~10 entries if too big
    if len(_ANALYZE_CACHE) > 50:
        for k in list(_ANALYZE_CACHE.keys())[:10]:
            _ANALYZE_CACHE.pop(k, None)
    _ANALYZE_CACHE[h] = (time.time(), text)


def _respect_cooldown() -> bool:
    return time.time() < ANALYZE_COOLDOWN_UNTIL


def _set_cooldown(seconds: float) -> None:
    global ANALYZE_COOLDOWN_UNTIL
    ANALYZE_COOLDOWN_UNTIL = time.time() + max(seconds, 1.0)


def _log_rl(resp: httpx.Response) -> None:
    try:
        h = resp.headers
        print(
            "[openai-rl]",
            "rem-req=", h.get("x-ratelimit-remaining-requests"),
            "rem-tok=", h.get("x-ratelimit-remaining-tokens"),
            "reset-req=", h.get("x-ratelimit-reset-requests"),
            "reset-tok=", h.get("x-ratelimit-reset-tokens"),
        )
    except Exception:
        pass


def _to_plaintext(s: str) -> str:
    """
    Remove Markdown headings/formatting and normalize whitespace so UI renders clean text.
    """
    # Strip heading markers at line start
    s = re.sub(r'^\s*#{1,6}\s*', '', s, flags=re.M)
    # Remove bold/italics markers
    s = s.replace('**', '').replace('__', '')
    # Optional: convert list markers "* " to "- " for consistency
    s = re.sub(r'^\s*\*\s+', '- ', s, flags=re.M)
    # Trim trailing spaces per line & overall
    s = re.sub(r'[ \t]+$', '', s, flags=re.M).strip()
    return s


def compact_result(full: dict, max_chars: int = int(os.getenv("OPENAI_MAX_CHARS", "20000"))) -> str:
    """
    Keep only essential parts of the result to manage token usage.
    """
    keep = {
        "winner": full.get("winner"),
        "rounds": full.get("rounds"),
        "attackerRatios": full.get("attackerRatios") or full.get("attacker_ratios"),
        "defenderRatios": full.get("defenderRatios") or full.get("defender_ratios"),
        "attacker": (full.get("attacker") or {}).get("summary"),
        "defender": (full.get("defender") or {}).get("summary"),
        "proc_stats": full.get("proc_stats"),
        "power": full.get("power"),
        "attacker_win_rate": full.get("attacker_win_rate"),
        "defender_win_rate": full.get("defender_win_rate"),
    }
    s = json.dumps(keep, separators=(",", ":"))
    if len(s) <= max_chars:
        return s
    # prune proc_stats sides to top ~6 skills if present
    try:
        keep2 = keep.copy()
        ps = keep2.get("proc_stats") or {}
        for side in ("attacker", "defender"):
            side_ps = ps.get(side) or {}
            pruned = dict(list(side_ps.items())[:6])
            ps[side] = pruned
        keep2["proc_stats"] = ps
        s2 = json.dumps(keep2, separators=(",", ":"))
        if len(s2) <= max_chars:
            return s2
        # final hard trim
        return s2[:max_chars]
    except Exception:
        return s[:max_chars]


# -----------------------------
# Routes
# -----------------------------
@app.get("/api/heroes", response_model=List[Dict[str, Any]])
def get_heroes():
    out = []
    for key, raw in RAW_HEROES.items():
        hero = raw[0] if isinstance(raw, list) else raw
        out.append({
            "name":       hero.get("hero-name", key),
            "charClass":  hero.get("hero-class","").capitalize(),
            "generation": hero.get("generation",0),
        })
    return out


@app.get("/api/troops", response_model=List[str])
def get_troops():
    return list(TROOP_DEFINITIONS.keys())


@app.post("/api/simulate", response_model=Dict[str, Any])
def run_simulation(req: SimRequest):
    # Resolve heroes
    try:
        atk_heroes = [hero_from_dict(RAW_HEROES[n]) for n in req.attackerHeroes]
        def_heroes = [hero_from_dict(RAW_HEROES[n]) for n in req.defenderHeroes]
        atk_support = [hero_from_dict(RAW_HEROES[n]) for n in req.attackerSupportHeroes]
        def_support = [hero_from_dict(RAW_HEROES[n]) for n in req.defenderSupportHeroes]
    except KeyError as e:
        raise HTTPException(422, f"Unknown hero: {e.args[0]}")

    # Resolve troop definitions
    try:
        atk_defs = {
            req.attackerTroops[c]: TROOP_DEFINITIONS[req.attackerTroops[c]]
            for c in ("Infantry","Lancer","Marksman")
        }
        def_defs = {
            req.defenderTroops[c]: TROOP_DEFINITIONS[req.defenderTroops[c]]
            for c in ("Infantry","Lancer","Marksman")
        }
    except KeyError as e:
        raise HTTPException(422, f"Unknown troop definition: {e.args[0]}")

    # Build formations
    atk_form = RallyFormation(
        atk_heroes,
        req.attackerRatios,
        req.attackerCapacity,
        atk_defs,
        support_heroes=atk_support,
    )
    def_form = RallyFormation(
        def_heroes,
        req.defenderRatios,
        req.defenderCapacity,
        def_defs,
        support_heroes=def_support,
    )

    # Bonus sources (aggregate from all heroes, including rally joiners)
    atk_bonus = BonusSource(atk_form.all_heroes())
    def_bonus = BonusSource(def_form.all_heroes())

    rpt = BattleReportInput(atk_form, def_form, atk_bonus, def_bonus)

    # Run sim
    if req.sims <= 1:
        return simulate_battle(rpt)
    return monte_carlo_battle(rpt, n_sims=req.sims)


# -----------------------------
# AI-style analysis (rule-based + LLM with guardrails)
# -----------------------------
@app.post("/api/analyze", response_model=Dict[str, str])
def analyze(req: AnalysisRequest):
    # Lightweight heuristic "AI" analysis without external API; LLM used if available & not rate limited.
    res = req.result.get("sample_battle") or req.result

    # Read mechanics docs and summarize relevant lines
    def _read(p: str) -> str:
        try:
            with open(p, "r", encoding="utf-8") as f:
                return f.read()
        except Exception:
            return ""

    def _summarize(text: str, max_lines: int = 24) -> str:
        if not text:
            return ""
        lines = text.splitlines()
        picked = []
        for ln in lines:
            s = ln.strip()
            if s.startswith("###") or s.startswith("- ") or s[:2].isdigit() or ("%" in s and ("Infantry" in s or "Lancer" in s or "Marksmen" in s)):
                picked.append(s.lstrip("# "))
            if len(picked) >= max_lines:
                break
        return "\n".join(picked)

    try:
        root = Path(__file__).resolve().parents[1]  # repo root
        md1 = _read(str(root / "docs" / "Expedition_Battle_Overview.md"))
        md2 = _read(str(root / "docs" / "Expedition_Turn_Based_Logic.md"))
        md3 = _read(str(root / "docs" / "TroopSkills.md"))

        # Env-tunable summary sizes
        ov_lines = int(os.getenv("MECH_OVERVIEW_MAX_LINES", "20"))
        tl_lines = int(os.getenv("MECH_TURN_LOGIC_MAX_LINES", "16"))
        ts_lines = int(os.getenv("MECH_TROOP_SKILLS_MAX_LINES", "20"))

        mechanics_summary = "\n".join([
            _summarize(md1, ov_lines),
            _summarize(md2, tl_lines),
            _summarize(md3, ts_lines),
        ]).strip()

        # Extract headline fields
        winner = str(res.get("winner", "unknown")).lower()
        rounds = res.get("rounds", None)
        attacker = res.get("attacker") or {}
        defender = res.get("defender") or {}
        atk_sum = (attacker.get("summary") or {})
        def_sum = (defender.get("summary") or {})
        atk_win_rate = req.result.get("attacker_win_rate")
        def_win_rate = req.result.get("defender_win_rate")

        # Heuristic narrative lines
        lines: List[str] = []
        if rounds is not None:
            lines.append(f"Battle concluded in {rounds} rounds. Winner: {winner.upper()}.")
        else:
            lines.append(f"Winner: {winner.upper()}.")

        if atk_win_rate is not None and def_win_rate is not None:
            lines.append(
                f"Simulated win rates — Attacker: {atk_win_rate*100:.1f}%, Defender: {def_win_rate*100:.1f}%."
            )

        if atk_sum and def_sum:
            lines.append("Survivorship and losses suggest the momentum:")
            lines.append(
                f"- Attacker lost {atk_sum.get('losses', 0)} ({(atk_sum.get('loss_pct', 0)*100):.1f}%) and killed {atk_sum.get('kills', 0)} ({(atk_sum.get('kill_pct', 0)*100):.1f}%)."
            )
            lines.append(
                f"- Defender lost {def_sum.get('losses', 0)} ({(def_sum.get('loss_pct', 0)*100):.1f}%) and killed {def_sum.get('kills', 0)} ({(def_sum.get('kill_pct', 0)*100):.1f}%)."
            )

        # Top skill procs
        proc_stats = (res.get("proc_stats") or {})

        def top_procs(side_key: str):
            side = (proc_stats.get(side_key) or {})
            counts: Dict[str, int] = {}
            for skill, cls_map in side.items():
                total = sum(int(n) for n in (cls_map or {}).values())
                counts[skill] = counts.get(skill, 0) + total
            top = sorted(counts.items(), key=lambda kv: kv[1], reverse=True)[:3]
            return [f"{skill} ({cnt} procs)" for skill, cnt in top if cnt > 0]

        atk_top = top_procs("attacker")
        def_top = top_procs("defender")
        if atk_top:
            lines.append("Attacker skill highlights: " + ", ".join(atk_top) + ".")
        if def_top:
            lines.append("Defender skill highlights: " + ", ".join(def_top) + ".")

        # Ratios
        atk_ratios = (req.result.get("attackerRatios") or req.result.get("attacker_ratios") or {})
        def_ratios = (req.result.get("defenderRatios") or req.result.get("defender_ratios") or {})

        def fmt_rs(rs):
            parts = []
            for k in ("Infantry","Lancer","Marksman"):
                v = rs.get(k)
                if v is not None:
                    parts.append(f"{k}: {v*100:.0f}%")
            return ", ".join(parts)

        if atk_ratios:
            lines.append("Attacker ratios — " + fmt_rs(atk_ratios) + ".")
        if def_ratios:
            lines.append("Defender ratios — " + fmt_rs(def_ratios) + ".")

        # Heuristic cause
        if winner in ("attacker","defender") and atk_sum and def_sum:
            cause = "damage throughput and skill procs"
            if winner == "attacker" and (atk_sum.get("kill_pct",0) > def_sum.get("kill_pct",0)):
                cause = "higher kill share and better proc efficiency"
            if winner == "defender" and (def_sum.get("kill_pct",0) > atk_sum.get("kill_pct",0)):
                cause = "higher kill share and better defensive conversion"
            lines.append(f"Likely primary cause: {cause} favoring the {winner}.")

        # Build a heuristic counter-plan early so we can use it if we must skip LLM
        loser = "defender" if winner == "attacker" else "attacker"
        loser_details = attacker if loser == "attacker" else defender
        loser_sum = atk_sum if loser == "attacker" else def_sum

        rec_atk = {"Infantry": 0.50, "Lancer": 0.20, "Marksman": 0.30}
        rec_def = {"Infantry": 0.60, "Lancer": 0.40, "Marksman": 0.00}
        rec = rec_def if loser == "defender" else rec_atk

        if loser_sum and loser_sum.get("kill_pct", 0) < 0.45:
            if loser == "defender":
                rec = {"Infantry": 0.55, "Lancer": 0.35, "Marksman": 0.10}
            else:
                rec = {"Infantry": 0.30, "Lancer": 0.30, "Marksman": 0.40}

        try:
            inf_surv = (loser_details.get("survivors") or {}).get("Infantry", 0)
            if isinstance(inf_surv, (int, float)) and inf_surv <= 0:
                rec["Infantry"] = min(0.7, rec.get("Infantry", 0.5) + 0.1)
                if rec.get("Marksman", 0) > 0:
                    rec["Marksman"] = max(0, rec["Marksman"] - 0.05)
                rec["Lancer"] = max(0, 1 - rec.get("Infantry", 0) - rec.get("Marksman", 0))
        except Exception:
            pass

        tot = sum(rec.values()) or 1.0
        rec = {k: v / tot for k, v in rec.items()}

        def fmt_ratio(r):
            return ", ".join([f"{k}: {int(v*100)}%" for k, v in r.items()])

        plan: List[str] = [
            f"Counter-Plan for {loser.capitalize()}",
            f"- Recommended ratios: {fmt_ratio(rec)}.",
            "- Hero focus: use stackable Expedition damage skills on offense (e.g., Jessie/Jasser); on defense, add Patrick/Molly/Sergey for durability.",
            "- Troop notes: keep Infantry frontline healthy; add Lancers if you need more bypass vs. Marksmen; dial Marksmen up only if frontline holds.",
            "- Tuning: run multiple sims; if kill % is still low, move 5–10% from Infantry to Marksmen (attack) or Lancer (defense) and re-run.",
        ]

        # Prepare compact JSON for LLM and cache key
        compact_json = compact_result(req.result)
        payload_hash = _hash_payload(compact_json)

        # Cache hit?
        cached = _cache_get(payload_hash)
        if cached:
            return {"analysis": cached}

        # If OpenAI is disabled or we are in cooldown, return heuristic immediately
        api_key = os.getenv("OPENAI_API_KEY")
        model = os.getenv("OPENAI_MODEL", "gpt-4o-mini")

        if os.getenv("DISABLE_OPENAI") or not api_key or _respect_cooldown():
            text = "\n".join(lines + [""] + ["(LLM temporarily unavailable; using heuristic analysis.)"] + plan)
            _cache_put(payload_hash, text)
            return {"analysis": text}

        # ---------- Prompts with explicit Facts block & plain-text constraint ----------
        def _fmt_ratio_for_facts(rs: dict | None) -> str:
            if not rs:
                return "not provided"
            parts = []
            for k in ("Infantry", "Lancer", "Marksman"):
                v = rs.get(k)
                if v is None:
                    continue
                try:
                    parts.append(f"{k} {v*100:.0f}%")
                except Exception:
                    pass
            return ", ".join(parts) if parts else "not provided"

        system_prompt = (
            "You are an expert Whiteout Survival Expedition/Rally battle analyst.\n"
            "Rules:\n"
            "1) You MUST use the provided Facts verbatim (winner, rounds, ratios, win rates). Do not infer or guess.\n"
            "2) If a value is missing, say 'not provided' rather than guessing.\n"
            "3) Output must be PLAIN TEXT only. Do NOT use Markdown headings or formatting (no ###, no **bold**, no code blocks).\n"
            "4) Be concise, actionable, and specific.\n"
            "5) Structure exactly:\n"
            "   1) Why did this side win\n"
            "   2) Key skill/troop factors\n"
            "   3) Counter-plan for the loser with recommended ratios and hero focus\n"
            "6) Use the exact ratios from Facts when referencing what was used.\n"
            "7) If you recommend new ratios, clearly mark them as 'Recommended ratios'."
        )

        facts_block = (
            "Facts:\n"
            f"- Winner: {winner or 'not provided'}\n"
            f"- Rounds: {rounds if rounds is not None else 'not provided'}\n"
            f"- Attacker ratios used: {_fmt_ratio_for_facts(atk_ratios)}\n"
            f"- Defender ratios used: {_fmt_ratio_for_facts(def_ratios)}\n"
            f"- Attacker win rate: {f'{atk_win_rate*100:.1f}%' if isinstance(atk_win_rate,(int,float)) else 'not provided'}\n"
            f"- Defender win rate: {f'{def_win_rate*100:.1f}%' if isinstance(def_win_rate,(int,float)) else 'not provided'}\n"
        )

        user_prompt = (
            facts_block + "\n"
            "Mechanics summary (for your context only):\n" + mechanics_summary + "\n\n"
            "Battle result JSON (already compacted). Analyze strictly under the above mechanics and Facts.\n"
            "Return plain text only, no Markdown.\n\n"
            f"Result: {compact_json}"
        )

        # Throttle to avoid bursts
        min_interval = float(os.getenv("OPENAI_MIN_INTERVAL_SEC", "0"))
        global ANALYZE_LAST_CALL_TS
        if min_interval > 0:
            now = time.time()
            elapsed = now - ANALYZE_LAST_CALL_TS
            if elapsed < min_interval:
                time.sleep(min_interval - elapsed)
            ANALYZE_LAST_CALL_TS = time.time()

        # Serialize calls in-process to reduce concurrency pressure
        with ANALYZE_SEM:
            max_retries = int(os.getenv("OPENAI_MAX_RETRIES", "4"))
            backoff = float(os.getenv("OPENAI_RETRY_INITIAL", "1.5"))

            # Prefer SDK Responses API
            last_err: Optional[Exception] = None
            used_sdk = False
            try:
                from openai import OpenAI as OpenAIClient
                base_url_env = os.getenv("OPENAI_API_BASE") or os.getenv("OPENAI_BASE_URL")
                if not base_url_env:
                    url_env = os.getenv("OPENAI_API_URL")
                    if url_env and "/v1/" in url_env:
                        base_url_env = url_env.split("/v1/")[0] + "/v1"

                client_kwargs = {"api_key": api_key}
                org_id = os.getenv("OPENAI_ORG_ID") or os.getenv("OPENAI_ORGANIZATION")
                if org_id:
                    client_kwargs["organization"] = org_id
                if base_url_env:
                    client_kwargs["base_url"] = base_url_env

                sdk_client = OpenAIClient(**client_kwargs)

                for attempt in range(max_retries):
                    try:
                        sdk_resp = sdk_client.responses.create(
                            model=model,
                            input="System:\n" + system_prompt + "\n\n" + user_prompt,
                            temperature=0.3,
                        )
                        content = getattr(sdk_resp, "output_text", None)
                        if not content:
                            try:
                                content = sdk_resp.to_dict().get("output_text")
                            except Exception:
                                content = str(sdk_resp)
                        if content:
                            text = _to_plaintext(content.strip())
                            _cache_put(payload_hash, text)
                            return {"analysis": text}
                        last_err = Exception("Empty OpenAI SDK content")
                        break
                    except Exception as oe:
                        last_err = oe
                        msg = str(oe)
                        # backoff on rate/5xx
                        if any(code in msg for code in ["429", "500", "502", "503", "504"]) and attempt < max_retries - 1:
                            time.sleep(backoff)
                            backoff = min(backoff * 2, 16.0)
                            continue
                        break
                used_sdk = True  # we attempted SDK path, even if failed
            except Exception as import_err:
                last_err = import_err
                used_sdk = False  # SDK unavailable

            # Fallback: HTTP chat/completions (legacy). Respect Retry-After and RL headers.
            if not used_sdk:
                openai_url = os.getenv("OPENAI_API_URL", "https://api.openai.com/v1/chat/completions")
                headers = {
                    "Authorization": f"Bearer {api_key}",
                    "Content-Type": "application/json",
                }
                payload = {
                    "model": model,
                    "messages": [
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": user_prompt},
                    ],
                    "temperature": 0.3,
                }
                for attempt in range(max_retries):
                    try:
                        with httpx.Client(timeout=60.0) as client:
                            r = client.post(openai_url, headers=headers, json=payload)
                            _log_rl(r)
                            if r.status_code == 429:
                                # Adaptive cooldown based on headers, then heuristic
                                ra = r.headers.get("Retry-After")
                                reset_r = r.headers.get("x-ratelimit-reset-requests")
                                reset_t = r.headers.get("x-ratelimit-reset-tokens")
                                cooldown = None
                                for val in (ra, reset_r, reset_t):
                                    try:
                                        if val:
                                            cooldown = max(float(val), 2.0)
                                            break
                                    except Exception:
                                        pass
                                if cooldown is None:
                                    cooldown = 8.0  # sane default
                                _set_cooldown(cooldown)
                                text = "\n".join(lines + [""] + [f"(LLM paused ~{int(cooldown)}s due to rate limits; using heuristic.)"] + plan)
                                _cache_put(payload_hash, text)
                                return {"analysis": text}
                            r.raise_for_status()
                            data = r.json()
                            content = data.get("choices", [{}])[0].get("message", {}).get("content", "")
                            if content:
                                text = _to_plaintext(content.strip())
                                _cache_put(payload_hash, text)
                                return {"analysis": text}
                            last_err = Exception("Empty OpenAI content")
                            break
                    except httpx.HTTPStatusError as he:
                        last_err = he
                        status = he.response.status_code
                        if status in (429, 500, 502, 503, 504) and attempt < max_retries - 1:
                            ra = he.response.headers.get("Retry-After")
                            reset_r = he.response.headers.get("x-ratelimit-reset-requests")
                            reset_t = he.response.headers.get("x-ratelimit-reset-tokens")
                            sleep_s = None
                            for val in (ra, reset_r, reset_t):
                                try:
                                    if val:
                                        sleep_s = max(float(val), 0.5)
                                        break
                                except Exception:
                                    pass
                            if sleep_s is None:
                                sleep_s = backoff
                            time.sleep(sleep_s)
                            backoff = min(backoff * 2, 16.0)
                            continue
                        break
                    except Exception as e_inner:
                        last_err = e_inner
                        break

            # If we got here, LLM failed for other reasons: return heuristic but include error banner
            err_msg = f"[LLM fallback] {str(last_err)}" if last_err else "[LLM fallback] Unknown LLM error"
            text = "\n".join(lines + ["", err_msg, ""] + plan)
            _cache_put(payload_hash, text)
            return {"analysis": text}

    except Exception as e:
        raise HTTPException(422, f"Unable to analyze: {e}")
