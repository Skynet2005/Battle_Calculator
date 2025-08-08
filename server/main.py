# server/main.py

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, validator, Field
from typing import List, Dict, Any
import os
from dotenv import load_dotenv, find_dotenv
import json
import httpx
import time

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

load_dotenv(find_dotenv())
app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

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

    # Bonus sources
    # Aggregate permanent bonuses (city buffs, exclusive weapons, etc.) from
    # **all** heroes on each side, including rally joiners.
    atk_bonus = BonusSource(atk_form.all_heroes())
    def_bonus = BonusSource(def_form.all_heroes())

    rpt = BattleReportInput(atk_form, def_form, atk_bonus, def_bonus)

    # Run sim
    if req.sims <= 1:
        return simulate_battle(rpt)
    return monte_carlo_battle(rpt, n_sims=req.sims)


# -----------------------------
# AI-style analysis (rule-based)
# -----------------------------

class AnalysisRequest(BaseModel):
    result: Dict[str, Any]


@app.post("/api/analyze", response_model=Dict[str, str])
def analyze(req: AnalysisRequest):
    # Created Logic for review: lightweight heuristic "AI" analysis without external API
    res = req.result.get("sample_battle") or req.result
    # Read and summarize mechanics context from docs
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

    from pathlib import Path
    root = Path(__file__).resolve().parents[1]  # repo root
    md1 = _read(str(root / "docs" / "Expedition_Battle_Overview.md"))
    md2 = _read(str(root / "docs" / "Expedition_Turn_Based_Logic.md"))
    md3 = _read(str(root / "docs" / "TroopSkills.md"))
    mechanics_summary = "\n".join([
        _summarize(md1, 20),
        _summarize(md2, 16),
        _summarize(md3, 20),
    ]).strip()
    try:
        winner = str(res.get("winner", "unknown")).lower()
        rounds = res.get("rounds", None)
        attacker = res.get("attacker") or {}
        defender = res.get("defender") or {}
        atk_sum = (attacker.get("summary") or {})
        def_sum = (defender.get("summary") or {})
        atk_win_rate = req.result.get("attacker_win_rate")
        def_win_rate = req.result.get("defender_win_rate")

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

        if winner in ("attacker","defender") and atk_sum and def_sum:
            cause = "damage throughput and skill procs"
            if winner == "attacker" and (atk_sum.get("kill_pct",0) > def_sum.get("kill_pct",0)):
                cause = "higher kill share and better proc efficiency"
            if winner == "defender" and (def_sum.get("kill_pct",0) > atk_sum.get("kill_pct",0)):
                cause = "higher kill share and better defensive conversion"
            lines.append(f"Likely primary cause: {cause} favoring the {winner}.")

        # If OpenAI is configured, defer to LLM for analysis
        api_key = os.getenv("OPENAI_API_KEY")
        model = os.getenv("OPENAI_MODEL", "gpt-4o-mini")
        if api_key and not os.getenv("DISABLE_OPENAI"):
            try:
                openai_url = os.getenv("OPENAI_API_URL", "https://api.openai.com/v1/chat/completions")
                system_prompt = (
                    "You are an expert Whiteout Survival Expedition/Rally battle analyst. "
                    "Use the provided mechanics summary as ground truth. Be concise, actionable, and specific. "
                    "Output sections: 1) Why did this side win, 2) Key skill/troop factors, 3) Counter-plan for the loser with recommended ratios and hero focus."
                )
                user_prompt = (
                    "Mechanics summary (for your context only):\n" + mechanics_summary + "\n\n"
                    "Battle result JSON follows. Analyze it strictly under the above mechanics. "
                    "Return clear text, no JSON.\n\n"
                    f"Result: {json.dumps(req.result)[:120000]}"
                )
                headers = {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}
                payload = {
                    "model": model,
                    "messages": [
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": user_prompt},
                    ],
                    "temperature": 0.3,
                }
                max_retries = int(os.getenv("OPENAI_MAX_RETRIES", "3"))
                backoff = float(os.getenv("OPENAI_RETRY_INITIAL", "1.0"))
                last_err = None
                for attempt in range(max_retries):
                    try:
                        with httpx.Client(timeout=60.0) as client:
                            r = client.post(openai_url, headers=headers, json=payload)
                            r.raise_for_status()
                            data = r.json()
                            content = data.get("choices", [{}])[0].get("message", {}).get("content", "")
                            if content:
                                return {"analysis": content}
                            last_err = Exception("Empty OpenAI content")
                            break
                    except httpx.HTTPStatusError as he:
                        last_err = he
                        status = he.response.status_code
                        if status in (429, 500, 502, 503, 504) and attempt < max_retries - 1:
                            retry_after = he.response.headers.get("Retry-After")
                            sleep_s = float(retry_after) if retry_after else backoff
                            time.sleep(sleep_s)
                            backoff *= 2
                            continue
                        break
                    except Exception as e_inner:
                        last_err = e_inner
                        break
                if last_err:
                    raise last_err
            except Exception as e:
                return {"analysis": f"[LLM fallback] {str(e)}\n"}

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

        plan: list[str] = [
            f"Counter-Plan for {loser.capitalize()}",
            f"- Recommended ratios: {fmt_ratio(rec)}.",
            "- Hero focus: use stackable Expedition damage skills on offense (e.g., Jessie/Jasser); on defense, add Patrick/Molly/Sergey for durability.",
            "- Troop notes: keep Infantry frontline healthy; add Lancers if you need more bypass vs. Marksmen; dial Marksmen up only if frontline holds.",
            "- Tuning: run multiple sims; if kill % is still low, move 5–10% from Infantry to Marksmen (attack) or Lancer (defense) and re-run.",
        ]

        lines.extend(["", *plan])
        return {"analysis": "\n".join(lines)}
    except Exception as e:
        raise HTTPException(422, f"Unable to analyze: {e}")