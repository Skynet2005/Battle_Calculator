# server/main.py

from fastapi import FastAPI, HTTPException, Query, Depends, Header
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, validator, Field
from typing import List, Dict, Any, Optional, Tuple
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
from sqlalchemy.orm import Session

# local auth/db
# Support running as a package (server.main) or as a module in the server dir
try:
    from .db import (
        SessionLocal,
        init_db,
        get_user_by_username,
        get_user_by_id,
        create_user,
        upsert_user_settings,
        get_user_settings,
        create_saved_setting,
        list_saved_settings,
        get_saved_setting,
        delete_saved_setting,
    )
    from .auth import hash_password, verify_password, create_access_token, decode_token
except ImportError:  # fallback when launched as "uvicorn main:app" inside server/
    from db import (  # type: ignore
        SessionLocal,
        init_db,
        get_user_by_username,
        get_user_by_id,
        create_user,
        upsert_user_settings,
        get_user_settings,
        create_saved_setting,
        list_saved_settings,
        get_saved_setting,
        delete_saved_setting,
    )
    from auth import hash_password, verify_password, create_access_token, decode_token  # type: ignore

# raw data
from hero_data.hero_loader import HEROES as RAW_HEROES
from troop_data.troop_definitions import TROOP_DEFINITIONS

# import your updated expedition simulation
from expedition_battle_mechanics.simulation import (
    simulate_battle,
    monte_carlo_battle,
    simulate_battle_weighted,
    monte_carlo_battle_weighted,
)

# expedition engine
from expedition_battle_mechanics.loader       import hero_from_dict
from expedition_battle_mechanics.combat_state import BattleReportInput
from expedition_battle_mechanics.formation    import RallyFormation
from expedition_battle_mechanics.bonus        import BonusSource
# chief gear & charms data
from chief_gear import CHIEF_GEAR_DATA as chief_gear_data
from chief_charms import CHIEF_CHARMS_DATA as chief_charms_data

# research data
from research import (
    get_category_names as research_get_category_names,
    get_tier_labels as research_get_tier_labels,
    get_nodes as research_get_nodes,
    find_stat as research_find_stat,
    flatten as research_flatten,
)

# Legendary/Mythic hero gear calculators
try:
    from .legendary_mythic_hero_gear.infantry_goggles import calc_goggles_infantry_il as _inf_goggles
    from .legendary_mythic_hero_gear.infantry_boot import calc_boot_infantry_il as _inf_boot
    from .legendary_mythic_hero_gear.infantry_glove import calc_glove_infantry_ih as _inf_glove
    from .legendary_mythic_hero_gear.infantry_belt import calc_belt_infantry_ih as _inf_belt
    from .legendary_mythic_hero_gear.lancer_goggles import calc_goggles_lancer_ll as _lan_goggles
    from .legendary_mythic_hero_gear.lancer_boot import calc_boot_lancer_ll as _lan_boot
    from .legendary_mythic_hero_gear.lancer_glove import calc_glove_lancer_lh as _lan_glove
    from .legendary_mythic_hero_gear.lancer_belt import calc_belt_lancer_lh as _lan_belt
    from .legendary_mythic_hero_gear.marksman_goggles import calc_goggles_marksman_ml as _mm_goggles
    from .legendary_mythic_hero_gear.marksman_boot import calc_boot_marksman_ml as _mm_boot
    from .legendary_mythic_hero_gear.marksman_glove import calc_glove_marksman_mh as _mm_glove
    from .legendary_mythic_hero_gear.marksman_belt import calc_belt_marksman_mh as _mm_belt
except ImportError:  # fallback when launched as script
    from legendary_mythic_hero_gear.infantry_goggles import calc_goggles_infantry_il as _inf_goggles  # type: ignore
    from legendary_mythic_hero_gear.infantry_boot import calc_boot_infantry_il as _inf_boot  # type: ignore
    from legendary_mythic_hero_gear.infantry_glove import calc_glove_infantry_ih as _inf_glove  # type: ignore
    from legendary_mythic_hero_gear.infantry_belt import calc_belt_infantry_ih as _inf_belt  # type: ignore
    from legendary_mythic_hero_gear.lancer_goggles import calc_goggles_lancer_ll as _lan_goggles  # type: ignore
    from legendary_mythic_hero_gear.lancer_boot import calc_boot_lancer_ll as _lan_boot  # type: ignore
    from legendary_mythic_hero_gear.lancer_glove import calc_glove_lancer_lh as _lan_glove  # type: ignore
    from legendary_mythic_hero_gear.lancer_belt import calc_belt_lancer_lh as _lan_belt  # type: ignore
    from legendary_mythic_hero_gear.marksman_goggles import calc_goggles_marksman_ml as _mm_goggles  # type: ignore
    from legendary_mythic_hero_gear.marksman_boot import calc_boot_marksman_ml as _mm_boot  # type: ignore
    from legendary_mythic_hero_gear.marksman_glove import calc_glove_marksman_mh as _mm_glove  # type: ignore
    from legendary_mythic_hero_gear.marksman_belt import calc_belt_marksman_mh as _mm_belt  # type: ignore


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
# Startup
# -----------------------------
@app.on_event("startup")
def _on_startup():
    # Created Logic for review: ensure SQLite tables exist on app startup
    init_db()


# -----------------------------
# DB session dependency
# -----------------------------
def get_db_session():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# -----------------------------
# Auth helpers + models
# -----------------------------
class AuthRequest(BaseModel):
    username: str
    password: str


class AuthResponse(BaseModel):
    token: str
    username: str


def _parse_bearer(authorization: Optional[str]) -> Optional[str]:
    if not authorization:
        return None
    parts = authorization.split()
    if len(parts) == 2 and parts[0].lower() == "bearer":
        return parts[1]
    return None


def _require_user(authorization: Optional[str], db: Session) -> dict:
    token = _parse_bearer(authorization)
    if not token:
        raise HTTPException(401, "Missing bearer token")
    payload = decode_token(token)
    if not payload:
        raise HTTPException(401, "Invalid or expired token")
    try:
        uid = int(str(payload.get("sub")))
    except Exception:
        raise HTTPException(401, "Malformed token")
    user = get_user_by_id(db, uid)
    if not user:
        raise HTTPException(401, "User not found")
    return {"id": user.id, "username": user.username}



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
    attackerEwLevels:      List[int] = Field(default_factory=list)
    defenderEwLevels:      List[int] = Field(default_factory=list)
    attackerRatios:        Dict[str, float]
    defenderRatios:        Dict[str, float]
    attackerCapacity:      int
    defenderCapacity:      int
    sims:                  int
    attackerTroops:        Dict[str, str]
    defenderTroops:        Dict[str, str]
    attackerSupportHeroes: List[str] = Field(default_factory=list)
    defenderSupportHeroes: List[str] = Field(default_factory=list)
    # Chief Gear & Charms (percent values in percent units, e.g., 12.5 means +12.5%)
    attackerGear:          Optional[Dict[str, float]] = None  # { attackPct?, defensePct? }
    defenderGear:          Optional[Dict[str, float]] = None
    attackerCharms:        Optional[Dict[str, float]] = None  # { lethalityPct?, healthPct? }
    defenderCharms:        Optional[Dict[str, float]] = None
    # Research buffs (percent values) aggregated per class/stat
    attackerResearch:      Optional[Dict[str, float]] = None
    defenderResearch:      Optional[Dict[str, float]] = None
    # Chief Skin bonuses (percent values, applies to all troop types)
    attackerChiefSkinBonuses: Optional[Dict[str, float]] = None  # { troops_lethality_pct?, troops_health_pct?, troops_defense_pct?, troops_attack_pct? }
    defenderChiefSkinBonuses: Optional[Dict[str, float]] = None
    # NEW: Legendary/Mythic Hero Gear (class-specific totals)
    attackerHeroGear: Optional[Dict[str, float]] = None  # { infantry_lethality_pct?, infantry_health_pct?, infantry_attack_pct?, infantry_defense_pct?, ... per class }
    defenderHeroGear: Optional[Dict[str, float]] = None
    # NEW: Daybreak Island bonuses (percent values)
    attackerDaybreakBonuses: Optional[Dict[str, float]] = None
    defenderDaybreakBonuses: Optional[Dict[str, float]] = None

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
    openai_api_key: Optional[str] = None


class ChiefGearItem(BaseModel):
    item: str  # "Cap" | "Coat" | "Ring" | "Watch" | "Pants" | "Weapon"
    tier: str  # exact label as in chief_gear_data e.g., "Red (Legendary) T2 Step 3"
    stars: int

class ChiefGearRequest(BaseModel):
    items: List[ChiefGearItem]

class ChiefGearTotals(BaseModel):
    total_attack_pct: float
    total_defense_pct: float
    total_power: int
    set_bonus_attack_pct: float
    set_bonus_defense_pct: float
    breakdown: Dict[str, Dict[str, float]]
    # Created Logic for review: class-specific base stats (EXCLUDES set bonuses)
    infantry_attack_pct: float = 0.0
    infantry_defense_pct: float = 0.0
    lancer_attack_pct: float = 0.0
    lancer_defense_pct: float = 0.0
    marksman_attack_pct: float = 0.0
    marksman_defense_pct: float = 0.0
    infantry_power: int = 0
    lancer_power: int = 0
    marksman_power: int = 0

class ChiefCharmsRequest(BaseModel):
    # 3 charms per gear slot item; user provides levels for each of the 3 charms
    # Example payload per slot: { "Cap": [1, 16, 4], ... }
    levels_by_slot: Dict[str, List[int]]

class ChiefCharmsTotals(BaseModel):
    total_lethality_pct: float
    total_health_pct: float
    total_power: int
    breakdown: Dict[str, Dict[str, float]]
    # Created Logic for review: class-specific totals from slot mapping
    infantry_lethality_pct: float = 0.0
    infantry_health_pct: float = 0.0
    lancer_lethality_pct: float = 0.0
    lancer_health_pct: float = 0.0
    marksman_lethality_pct: float = 0.0
    marksman_health_pct: float = 0.0
    infantry_power: int = 0
    lancer_power: int = 0
    marksman_power: int = 0


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
# Shared helpers
# -----------------------------
def _mk_city_buffs(
    gear: Optional[Dict[str, float]] | None,
    charms: Optional[Dict[str, float]] | None,
    research: Optional[Dict[str, float]] | None,
    chief_skin_bonuses: Optional[Dict[str, float]] = None,
    hero_gear: Optional[Dict[str, float]] = None,
    daybreak: Optional[Dict[str, float]] = None,
) -> Dict[str, float]:
    """
    Created Logic for review: Merge class-specific city buffs from gear, charms, and research.
    Input values are percent units (e.g., 12.5) and converted to decimals (0.125).
    """
    city: Dict[str, float] = {}
    if gear:
        # Only use class-specific mapping to avoid double-counting
        for cls in ("infantry", "lancer", "marksman"):
            ca = float(gear.get(f"{cls}_attack_pct", 0.0)) / 100.0
            cd = float(gear.get(f"{cls}_defense_pct", 0.0)) / 100.0
            if ca:
                city[f"{cls}_attack"] = city.get(f"{cls}_attack", 0.0) + ca
            if cd:
                city[f"{cls}_defense"] = city.get(f"{cls}_defense", 0.0) + cd
    if charms:
        # Only use class-specific mapping
        for cls in ("infantry", "lancer", "marksman"):
            le = float(charms.get(f"{cls}_lethality_pct", 0.0)) / 100.0
            hp = float(charms.get(f"{cls}_health_pct", 0.0)) / 100.0
            if le:
                city[f"{cls}_lethality"] = city.get(f"{cls}_lethality", 0.0) + le
            if hp:
                city[f"{cls}_health"] = city.get(f"{cls}_health", 0.0) + hp
    if research:
        # research map contains cumulative percent values; convert to decimals and add
        # Supports both troop-wide keys and class-specific keys
        troop_map = {
            "troop_attack_pct": ("infantry_attack", "lancer_attack", "marksman_attack"),
            "troops_attack_pct": ("infantry_attack", "lancer_attack", "marksman_attack"),
            "troop_defense_pct": ("infantry_defense", "lancer_defense", "marksman_defense"),
            "troops_defense_pct": ("infantry_defense", "lancer_defense", "marksman_defense"),
            "troop_health_pct": ("infantry_health", "lancer_health", "marksman_health"),
            "troops_health_pct": ("infantry_health", "lancer_health", "marksman_health"),
            "troop_lethality_pct": ("infantry_lethality", "lancer_lethality", "marksman_lethality"),
            "troops_lethality_pct": ("infantry_lethality", "lancer_lethality", "marksman_lethality"),
        }
        # troop-wide fields
        for k, targets in troop_map.items():
            v = float(research.get(k, 0.0)) / 100.0
            if not v:
                continue
            for t in targets:
                city[t] = city.get(t, 0.0) + v
        # class-specific fields
        for cls in ("infantry", "lancer", "marksman"):
            for stat in ("attack", "defense", "lethality", "health"):
                pct = float(research.get(f"{cls}_{stat}_pct", 0.0)) / 100.0
                if pct:
                    city[f"{cls}_{stat}"] = city.get(f"{cls}_{stat}", 0.0) + pct
        
    # Chief Skin bonuses (apply to all troop types)
    if chief_skin_bonuses:
        # Created Logic for review: Chief Skin bonuses apply to all troop types (Infantry, Lancer, Marksman)
        for cls in ("infantry", "lancer", "marksman"):
            # Lethality bonus
            le = float(chief_skin_bonuses.get("troops_lethality_pct", 0.0)) / 100.0
            if le:
                city[f"{cls}_lethality"] = city.get(f"{cls}_lethality", 0.0) + le
            # Health bonus
            hp = float(chief_skin_bonuses.get("troops_health_pct", 0.0)) / 100.0
            if hp:
                city[f"{cls}_health"] = city.get(f"{cls}_health", 0.0) + hp
            # Defense bonus
            df = float(chief_skin_bonuses.get("troops_defense_pct", 0.0)) / 100.0
            if df:
                city[f"{cls}_defense"] = city.get(f"{cls}_defense", 0.0) + df
            # Attack bonus
            atk = float(chief_skin_bonuses.get("troops_attack_pct", 0.0)) / 100.0
            if atk:
                city[f"{cls}_attack"] = city.get(f"{cls}_attack", 0.0) + atk

    # Daybreak Island bonuses
    if daybreak:
        ia = float(daybreak.get("infantry_attack_pct", 0.0)) / 100.0
        if ia:
            city["infantry_attack"] = city.get("infantry_attack", 0.0) + ia
        idf = float(daybreak.get("infantry_defense_pct", 0.0)) / 100.0
        if idf:
            city["infantry_defense"] = city.get("infantry_defense", 0.0) + idf
        ma = float(daybreak.get("marksman_attack_pct", 0.0)) / 100.0
        if ma:
            city["marksman_attack"] = city.get("marksman_attack", 0.0) + ma
        for stat_key, targets in (
            ("troops_attack_pct", ("infantry_attack","lancer_attack","marksman_attack")),
            ("troops_defense_pct", ("infantry_defense","lancer_defense","marksman_defense")),
            ("troops_lethality_pct", ("infantry_lethality","lancer_lethality","marksman_lethality")),
            ("troops_health_pct", ("infantry_health","lancer_health","marksman_health")),
        ):
            v = float(daybreak.get(stat_key, 0.0)) / 100.0
            if v:
                for t in targets:
                    city[t] = city.get(t, 0.0) + v
    return city


# -----------------------------
# Routes
# -----------------------------
@app.post("/api/auth/register", response_model=AuthResponse)
def register(req: AuthRequest, db: Session = Depends(get_db_session)):
    if not req.username or not req.password:
        raise HTTPException(422, "Username and password are required")
    existing = get_user_by_username(db, req.username)
    if existing:
        raise HTTPException(409, "Username already exists")
    ph = hash_password(req.password)
    user = create_user(db, req.username, ph)
    token = create_access_token(user.id, user.username)
    return AuthResponse(token=token, username=user.username)


@app.post("/api/auth/login", response_model=AuthResponse)
def login(req: AuthRequest, db: Session = Depends(get_db_session)):
    user = get_user_by_username(db, req.username)
    if not user or not verify_password(req.password, user.password_hash):
        raise HTTPException(401, "Invalid credentials")
    token = create_access_token(user.id, user.username)
    return AuthResponse(token=token, username=user.username)


class SettingsUpsertRequest(BaseModel):
    data: Dict[str, Any]


class SettingsResponse(BaseModel):
    data: Dict[str, Any]


@app.get("/api/settings", response_model=SettingsResponse)
def get_settings(Authorization: Optional[str] = Header(default=None), db: Session = Depends(get_db_session)):
    user = _require_user(Authorization, db)
    raw = get_user_settings(db, user_id=user["id"]) or "{}"
    try:
        parsed = json.loads(raw)
    except Exception:
        parsed = {}
    return SettingsResponse(data=parsed)


@app.post("/api/settings", response_model=SettingsResponse)
def save_settings(req: SettingsUpsertRequest, Authorization: Optional[str] = Header(default=None), db: Session = Depends(get_db_session)):
    user = _require_user(Authorization, db)
    try:
        # Validate is JSON-serializable
        raw = json.dumps(req.data, separators=(",", ":"))
    except Exception:
        raise HTTPException(422, "Settings must be JSON-serializable")
    upsert_user_settings(db, user_id=user["id"], json_text=raw)
    return SettingsResponse(data=req.data)


# --------------- Multiple saved settings (named presets) ---------------
class SavedSettingsCreateRequest(BaseModel):
    name: str
    data: Dict[str, Any]


class SavedSettingsItem(BaseModel):
    id: int
    name: str
    updated_at: str


class SavedSettingsListResponse(BaseModel):
    items: List[SavedSettingsItem]


@app.get("/api/settings/saved", response_model=SavedSettingsListResponse)
def list_saved(Authorization: Optional[str] = Header(default=None), db: Session = Depends(get_db_session)):
    user = _require_user(Authorization, db)
    rows = list_saved_settings(db, user_id=user["id"])  # type: ignore
    items = [SavedSettingsItem(id=r.id, name=r.name, updated_at=r.updated_at.isoformat()) for r in rows]
    return SavedSettingsListResponse(items=items)


@app.post("/api/settings/saved", response_model=SavedSettingsItem)
def create_saved(req: SavedSettingsCreateRequest, Authorization: Optional[str] = Header(default=None), db: Session = Depends(get_db_session)):
    user = _require_user(Authorization, db)
    try:
        raw = json.dumps(req.data, separators=(",", ":"))
    except Exception:
        raise HTTPException(422, "Settings must be JSON-serializable")
    row = create_saved_setting(db, user_id=user["id"], name=req.name.strip()[:200], json_text=raw)  # type: ignore
    return SavedSettingsItem(id=row.id, name=row.name, updated_at=row.updated_at.isoformat())


@app.get("/api/settings/saved/{setting_id}", response_model=SettingsResponse)
def get_saved(setting_id: int, Authorization: Optional[str] = Header(default=None), db: Session = Depends(get_db_session)):
    user = _require_user(Authorization, db)
    row = get_saved_setting(db, user_id=user["id"], setting_id=setting_id)  # type: ignore
    if not row:
        raise HTTPException(404, "Not found")
    try:
        data = json.loads(row.data)
    except Exception:
        data = {}
    return SettingsResponse(data=data)


@app.delete("/api/settings/saved/{setting_id}", response_model=Dict[str, str])
def remove_saved(setting_id: int, Authorization: Optional[str] = Header(default=None), db: Session = Depends(get_db_session)):
    user = _require_user(Authorization, db)
    ok = delete_saved_setting(db, user_id=user["id"], setting_id=setting_id)  # type: ignore
    if not ok:
        raise HTTPException(404, "Not found")
    return {"status": "deleted"}
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

@app.get("/api/heroes/{class_type}", response_model=List[Dict[str, Any]])
def get_heroes_by_class(class_type: str):
    """Get heroes filtered by class type (Infantry, Lancer, Marksman) and sorted by generation"""
    out = []
    for key, raw in RAW_HEROES.items():
        hero = raw[0] if isinstance(raw, list) else raw
        hero_class = hero.get("hero-class","").capitalize()
        if hero_class.lower() == class_type.lower():
            out.append({
                "name":       hero.get("hero-name", key),
                "charClass":  hero.get("hero-class","").capitalize(),
                "generation": hero.get("generation",0),
            })
    
    # Sort by generation order: Rare (0), Epic (1), SSR Gen 1-8 (2-9)
    def sort_key(hero):
        gen = hero.get("generation", 0)
        # Ensure proper ordering: Rare (0) < Epic (1) < SSR Gen 1-8 (2-9)
        return gen
    
    out.sort(key=sort_key)
    return out

@app.get("/api/troops", response_model=List[str])
def get_troops():
    return list(TROOP_DEFINITIONS.keys())

@app.get("/api/troops/{class_type}", response_model=List[str])
def get_troops_by_class(class_type: str):
    """Get troops filtered by class type (Infantry, Lancer, Marksman) including Helios variants"""
    all_troops = list(TROOP_DEFINITIONS.keys())
    filtered_troops = []
    
    for troop in all_troops:
        # Check if troop name starts with the class type OR starts with "Helios" + class type
        if (troop.lower().startswith(class_type.lower()) or 
            troop.lower().startswith(f"helios {class_type.lower()}")):
            filtered_troops.append(troop)
    
    # Sort by FC level (extract number from "FC10", "FC9", etc.) and prioritize Helios troops
    def sort_key(troop):
        # Extract FC number from troop name like "Infantry (FC10)" -> 10
        import re
        match = re.search(r'FC(\d+)', troop)
        fc_level = int(match.group(1)) if match else 0
        
        # Helios troops should come before regular troops at the same FC level
        # Use negative priority for Helios (so they sort first) and positive for regular
        is_helios = troop.lower().startswith("helios")
        priority = -1 if is_helios else 1
        
        # Return tuple for sorting: (FC level, priority)
        # Higher FC levels first, then Helios before regular
        return (-fc_level, priority)  # Negative FC level for reverse sort, positive priority for Helios first

    filtered_troops.sort(key=sort_key)  # Higher FC levels first, Helios before regular
    return filtered_troops

@app.post("/api/simulate", response_model=Dict[str, Any])
def run_simulation(req: SimRequest):
    # Resolve heroes
    try:
        # Created Logic for review: apply Exclusive Weapon level per hero in order (1-10)
        def _ew_for(idx: int, arr: List[int]) -> int | None:
            try:
                lvl = int(arr[idx]) if idx < len(arr) else None
            except Exception:
                lvl = None
            if lvl is None:
                return None
            return max(1, min(10, int(lvl)))

        atk_heroes = [hero_from_dict(RAW_HEROES[n], ew_level=_ew_for(i, req.attackerEwLevels)) for i, n in enumerate(req.attackerHeroes)]
        def_heroes = [hero_from_dict(RAW_HEROES[n], ew_level=_ew_for(i, req.defenderEwLevels)) for i, n in enumerate(req.defenderHeroes)]
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

    # Merge external buffs from Gear/Charms (convert percent → decimal)
    def _mk_city_buffs(
        gear: Optional[Dict[str, float]],
        charms: Optional[Dict[str, float]],
        research: Optional[Dict[str, float]],
        chief_skin_bonuses: Optional[Dict[str, float]] = None,
        hero_gear: Optional[Dict[str, float]] = None,
        daybreak: Optional[Dict[str, float]] = None,
    ) -> Dict[str, float]:
        city: Dict[str, float] = {}
        if gear:
            # Only use class-specific mapping to avoid double-counting
            for cls in ("infantry", "lancer", "marksman"):
                ca = float(gear.get(f"{cls}_attack_pct", 0.0)) / 100.0
                cd = float(gear.get(f"{cls}_defense_pct", 0.0)) / 100.0
                if ca:
                    city[f"{cls}_attack"] = city.get(f"{cls}_attack", 0.0) + ca
                if cd:
                    city[f"{cls}_defense"] = city.get(f"{cls}_defense", 0.0) + cd
        if charms:
            # Only use class-specific mapping
            for cls in ("infantry", "lancer", "marksman"):
                le = float(charms.get(f"{cls}_lethality_pct", 0.0)) / 100.0
                hp = float(charms.get(f"{cls}_health_pct", 0.0)) / 100.0
                if le:
                    city[f"{cls}_lethality"] = city.get(f"{cls}_lethality", 0.0) + le
                if hp:
                    city[f"{cls}_health"] = city.get(f"{cls}_health", 0.0) + hp
        # Legendary/Mythic Hero Gear contributions (class-specific), convert percent to decimals
        if hero_gear:
            for cls in ("infantry", "lancer", "marksman"):
                for stat in ("attack", "defense", "lethality", "health"):
                    pct = float(hero_gear.get(f"{cls}_{stat}_pct", 0.0)) / 100.0
                    if pct:
                        city[f"{cls}_{stat}"] = city.get(f"{cls}_{stat}", 0.0) + pct

        if research:
            # Created Logic for review: research map contains cumulative percent values; convert to decimals and add
            # Supports both troop-wide keys and class-specific keys
            troop_map = {
                "troop_attack_pct": ("infantry_attack", "lancer_attack", "marksman_attack"),
                "troops_attack_pct": ("infantry_attack", "lancer_attack", "marksman_attack"),
                "troop_defense_pct": ("infantry_defense", "lancer_defense", "marksman_defense"),
                "troops_defense_pct": ("infantry_defense", "lancer_defense", "marksman_defense"),
                "troop_health_pct": ("infantry_health", "lancer_health", "marksman_health"),
                "troops_health_pct": ("infantry_health", "lancer_health", "marksman_health"),
                "troop_lethality_pct": ("infantry_lethality", "lancer_lethality", "marksman_lethality"),
                "troops_lethality_pct": ("infantry_lethality", "lancer_lethality", "marksman_lethality"),
            }
            # troop-wide fields
            for k, targets in troop_map.items():
                v = float(research.get(k, 0.0)) / 100.0
                if not v:
                    continue
                for t in targets:
                    city[t] = city.get(t, 0.0) + v
            # class-specific fields
            for cls in ("infantry", "lancer", "marksman"):
                for stat in ("attack", "defense", "lethality", "health"):
                    pct = float(research.get(f"{cls}_{stat}_pct", 0.0)) / 100.0
                    if pct:
                        city[f"{cls}_{stat}"] = city.get(f"{cls}_{stat}", 0.0) + pct
        
        # Chief Skin bonuses (apply to all troop types)
        if chief_skin_bonuses:
            # Created Logic for review: Chief Skin bonuses apply to all troop types (Infantry, Lancer, Marksman)
            for cls in ("infantry", "lancer", "marksman"):
                # Lethality bonus
                le = float(chief_skin_bonuses.get("troops_lethality_pct", 0.0)) / 100.0
                if le:
                    city[f"{cls}_lethality"] = city.get(f"{cls}_lethality", 0.0) + le
                # Health bonus
                hp = float(chief_skin_bonuses.get("troops_health_pct", 0.0)) / 100.0
                if hp:
                    city[f"{cls}_health"] = city.get(f"{cls}_health", 0.0) + hp
                # Defense bonus
                df = float(chief_skin_bonuses.get("troops_defense_pct", 0.0)) / 100.0
                if df:
                    city[f"{cls}_defense"] = city.get(f"{cls}_defense", 0.0) + df
                # Attack bonus
                atk = float(chief_skin_bonuses.get("troops_attack_pct", 0.0)) / 100.0
                if atk:
                    city[f"{cls}_attack"] = city.get(f"{cls}_attack", 0.0) + atk
        
        # Daybreak Island bonuses
        if daybreak:
            # class-specific
            ia = float(daybreak.get("infantry_attack_pct", 0.0)) / 100.0
            if ia:
                city["infantry_attack"] = city.get("infantry_attack", 0.0) + ia
            idf = float(daybreak.get("infantry_defense_pct", 0.0)) / 100.0
            if idf:
                city["infantry_defense"] = city.get("infantry_defense", 0.0) + idf
            ma = float(daybreak.get("marksman_attack_pct", 0.0)) / 100.0
            if ma:
                city["marksman_attack"] = city.get("marksman_attack", 0.0) + ma
            # troop-wide
            for stat_key, targets in (
                ("troops_attack_pct", ("infantry_attack","lancer_attack","marksman_attack")),
                ("troops_defense_pct", ("infantry_defense","lancer_defense","marksman_defense")),
                ("troops_lethality_pct", ("infantry_lethality","lancer_lethality","marksman_lethality")),
                ("troops_health_pct", ("infantry_health","lancer_health","marksman_health")),
            ):
                v = float(daybreak.get(stat_key, 0.0)) / 100.0
                if v:
                    for t in targets:
                        city[t] = city.get(t, 0.0) + v
        return city

    atk_city_buffs = _mk_city_buffs(req.attackerGear, req.attackerCharms, req.attackerResearch, req.attackerChiefSkinBonuses, req.attackerHeroGear, req.attackerDaybreakBonuses)
    def_city_buffs = _mk_city_buffs(req.defenderGear, req.defenderCharms, req.defenderResearch, req.defenderChiefSkinBonuses, req.defenderHeroGear, req.defenderDaybreakBonuses)

    # Bonus sources (aggregate from all heroes, including rally joiners)
    atk_bonus = BonusSource(atk_form.all_heroes(), city_buffs=atk_city_buffs)
    def_bonus = BonusSource(def_form.all_heroes(), city_buffs=def_city_buffs)

    rpt = BattleReportInput(atk_form, def_form, atk_bonus, def_bonus)

    # Run sim
    if req.sims <= 1:
        out = simulate_battle(rpt, use_power_weighting=False)
    else:
        out = monte_carlo_battle(rpt, n_sims=req.sims, use_power_weighting=False)

    # Include gear percentages in result JSON for UI display/copy
    try:
        base = out.get("sample_battle") or out
        base["attackerGear"] = req.attackerGear or {}
        base["defenderGear"] = req.defenderGear or {}
        base["attackerCharms"] = req.attackerCharms or {}
        base["defenderCharms"] = req.defenderCharms or {}
        base["attackerHeroGear"] = req.attackerHeroGear or {}
        base["defenderHeroGear"] = req.defenderHeroGear or {}
    except Exception:
        pass

    return out


@app.post("/api/simulate/weighted", response_model=Dict[str, Any])
def run_simulation_weighted(req: SimRequest):
    # Same payload model; uses power weighting in damage
    # Resolve heroes
    try:
        def _ew_for(idx: int, arr: List[int]) -> int | None:
            try:
                lvl = int(arr[idx]) if idx < len(arr) else None
            except Exception:
                lvl = None
            if lvl is None:
                return None
            return max(1, min(10, int(lvl)))

        atk_heroes = [hero_from_dict(RAW_HEROES[n], ew_level=_ew_for(i, req.attackerEwLevels)) for i, n in enumerate(req.attackerHeroes)]
        def_heroes = [hero_from_dict(RAW_HEROES[n], ew_level=_ew_for(i, req.defenderEwLevels)) for i, n in enumerate(req.defenderHeroes)]
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

    atk_city_buffs = _mk_city_buffs(req.attackerGear, req.attackerCharms, req.attackerResearch, req.attackerChiefSkinBonuses, req.attackerHeroGear)
    def_city_buffs = _mk_city_buffs(req.defenderGear, req.defenderCharms, req.defenderResearch, req.defenderChiefSkinBonuses, req.defenderHeroGear)

    atk_bonus = BonusSource(atk_form.all_heroes(), city_buffs=atk_city_buffs)
    def_bonus = BonusSource(def_form.all_heroes(), city_buffs=def_city_buffs)

    rpt = BattleReportInput(atk_form, def_form, atk_bonus, def_bonus)

    if req.sims <= 1:
        out = simulate_battle_weighted(rpt)
    else:
        out = monte_carlo_battle_weighted(rpt, n_sims=req.sims)

    try:
        base = out.get("sample_battle") or out
        base["attackerGear"] = req.attackerGear or {}
        base["defenderGear"] = req.defenderGear or {}
        base["attackerCharms"] = req.attackerCharms or {}
        base["defenderCharms"] = req.defenderCharms or {}
        base["attackerHeroGear"] = req.attackerHeroGear or {}
        base["defenderHeroGear"] = req.defenderHeroGear or {}
    except Exception:
        pass

    return out


# -----------------------------
# Chief Gear helpers + routes
# -----------------------------

_GEAR_SLOTS: Tuple[str, ...] = ("Cap", "Coat", "Ring", "Watch", "Pants", "Weapon")

def _parse_pct(s: str) -> float:
    try:
        return float(str(s).replace("%", ""))
    except Exception:
        return 0.0

def _find_gear_entry(slot: str, tier: str, stars: int) -> Optional[dict]:
    rows = chief_gear_data.get(slot)
    if not rows:
        return None
    for row in rows:
        if str(row.get("Tier")) == tier and int(row.get("Stars", 0)) == int(stars):
            return row
    return None


@app.get("/api/gear/chief/slots", response_model=List[str])
def get_chief_gear_slots():
    return list(_GEAR_SLOTS)


@app.get("/api/gear/chief/options", response_model=Dict[str, List[Dict[str, Any]]])
def get_chief_gear_options():
    """
    Returns for each slot the list of { tier, stars, attackPct, defensePct, power } options.
    """
    out: Dict[str, List[Dict[str, Any]]] = {}
    for slot in _GEAR_SLOTS:
        rows = chief_gear_data.get(slot, [])
        out[slot] = [
            {
                "tier": r.get("Tier"),
                "stars": r.get("Stars"),
                "attackPct": _parse_pct(r.get("Attack", 0)),
                "defensePct": _parse_pct(r.get("Defense", 0)),
                "power": int(r.get("Power Total", 0)),
            }
            for r in rows
        ]
    return out


@app.post("/api/gear/chief/calc", response_model=ChiefGearTotals)
def calc_chief_gear(req: ChiefGearRequest):
    # Sum base stats
    total_attack_pct = 0.0
    total_defense_pct = 0.0
    total_power = 0
    breakdown: Dict[str, Dict[str, float]] = {}

    chosen_tiers: Dict[str, str] = {}
    chosen_stars: Dict[str, int] = {}

    # class-specific buckets (base only)
    infantry_attack_pct = infantry_defense_pct = 0.0
    lancer_attack_pct = lancer_defense_pct = 0.0
    marksman_attack_pct = marksman_defense_pct = 0.0
    infantry_power = lancer_power = marksman_power = 0

    for it in req.items:
        if it.item not in _GEAR_SLOTS:
            raise HTTPException(422, f"Unknown gear slot: {it.item}")
        row = _find_gear_entry(it.item, it.tier, it.stars)
        if not row:
            raise HTTPException(422, f"No data for {it.item} {it.tier} ★{it.stars}")
        a = _parse_pct(row.get("Attack", 0))
        d = _parse_pct(row.get("Defense", 0))
        p = int(row.get("Power Total", 0))
        breakdown[it.item] = {"attackPct": a, "defensePct": d, "power": float(p)}
        total_attack_pct += a
        total_defense_pct += d
        total_power += p
        chosen_tiers[it.item] = it.tier
        chosen_stars[it.item] = int(it.stars)

        # Map slot → class for base stats
        if it.item in ("Coat", "Pants"):
            infantry_attack_pct += a
            infantry_defense_pct += d
        elif it.item in ("Cap", "Watch"):
            lancer_attack_pct += a
            lancer_defense_pct += d
            lancer_power += p
        elif it.item in ("Ring", "Weapon"):
            marksman_attack_pct += a
            marksman_defense_pct += d
            marksman_power += p

    # Set bonuses – use authoritative mapping from chief_gear.SET_BONUSES
    set_bonus_attack_pct = 0.0
    set_bonus_defense_pct = 0.0

    from chief_gear import SET_BONUSES

    def _normalize_set_key(raw_tier: str, stars: int) -> str:
        tier = str(raw_tier)
        # Uncommon
        if "Uncommon" in tier:
            # Uncommon has a special T1 only for 1-star
            return "Uncommon T1" if stars == 1 or "T1" in tier else "Uncommon"
        # Rare with star-dependent variants
        if "Rare" in tier:
            if stars == 0:
                return "Rare"
            return f"Rare ({stars}-star)"
        # Epic (Purple)
        if "Epic" in tier:
            return "Epic T1" if "T1" in tier else "Epic"
        # Mythic (Gold)
        if "Mythic" in tier:
            if "T2" in tier:
                return "Mythic T2"
            if "T1" in tier:
                return "Mythic T1"
            return "Mythic"
        # Legendary (Red) has Step N and T1/T2/T3 Step N → ignore step when mapping
        if "Legendary" in tier:
            if "T3" in tier:
                return "Legendary T3"
            if "T2" in tier:
                return "Legendary T2"
            if "T1" in tier:
                return "Legendary T1"
            return "Legendary"
        # Fallback to the raw tier (may yield 0 bonus if missing in map)
        return tier

    # For defense: head set (Cap, Coat, Ring)
    cap_tier = chosen_tiers.get("Cap")
    coat_tier = chosen_tiers.get("Coat")
    ring_tier = chosen_tiers.get("Ring")
    if cap_tier and coat_tier and ring_tier:
        cap_key = _normalize_set_key(cap_tier, chosen_stars.get("Cap", 0))
        coat_key = _normalize_set_key(coat_tier, chosen_stars.get("Coat", 0))
        ring_key = _normalize_set_key(ring_tier, chosen_stars.get("Ring", 0))
        if cap_key == coat_key == ring_key:
            set_def = SET_BONUSES.get(cap_key)
        if set_def is not None:
            set_bonus_defense_pct += float(set_def)

    # For attack: weapon set (Watch, Pants, Weapon)
    watch_tier = chosen_tiers.get("Watch")
    pants_tier = chosen_tiers.get("Pants")
    weapon_tier = chosen_tiers.get("Weapon")
    if watch_tier and pants_tier and weapon_tier:
        watch_key = _normalize_set_key(watch_tier, chosen_stars.get("Watch", 0))
        pants_key = _normalize_set_key(pants_tier, chosen_stars.get("Pants", 0))
        weapon_key = _normalize_set_key(weapon_tier, chosen_stars.get("Weapon", 0))
        if watch_key == pants_key == weapon_key:
            set_atk = SET_BONUSES.get(watch_key)
        if set_atk is not None:
            set_bonus_attack_pct += float(set_atk)

    # Totals include set bonuses
    total_attack_pct_with_bonus = total_attack_pct + set_bonus_attack_pct
    total_defense_pct_with_bonus = total_defense_pct + set_bonus_defense_pct

    # Also allocate set bonuses to each troop class bucket (applies to all classes)
    infantry_attack_pct += set_bonus_attack_pct
    lancer_attack_pct += set_bonus_attack_pct
    marksman_attack_pct += set_bonus_attack_pct
    infantry_defense_pct += set_bonus_defense_pct
    lancer_defense_pct += set_bonus_defense_pct
    marksman_defense_pct += set_bonus_defense_pct

    return ChiefGearTotals(
        total_attack_pct=round(total_attack_pct_with_bonus, 2),
        total_defense_pct=round(total_defense_pct_with_bonus, 2),
        total_power=int(total_power),
        set_bonus_attack_pct=round(set_bonus_attack_pct, 2),
        set_bonus_defense_pct=round(set_bonus_defense_pct, 2),
        breakdown=breakdown,
        infantry_attack_pct=round(infantry_attack_pct, 2),
        infantry_defense_pct=round(infantry_defense_pct, 2),
        lancer_attack_pct=round(lancer_attack_pct, 2),
        lancer_defense_pct=round(lancer_defense_pct, 2),
        marksman_attack_pct=round(marksman_attack_pct, 2),
        marksman_defense_pct=round(marksman_defense_pct, 2),
        infantry_power=int(infantry_power),
        lancer_power=int(lancer_power),
        marksman_power=int(marksman_power),
    )


# -----------------------------
# Legendary/Mythic Hero Gear routes
# -----------------------------

from typing import Literal as _Literal

class HeroGearPiece(BaseModel):
    level: int
    essence_level: int
    mastery_forged: bool = True
    mastery_level: int = 0
    stacking: _Literal["additive","multiplicative"] = "additive"

class HeroGearClass(BaseModel):
    goggles: HeroGearPiece
    boot: HeroGearPiece
    glove: HeroGearPiece
    belt: HeroGearPiece

class HeroGearCalcRequest(BaseModel):
    infantry: HeroGearClass
    lancer: HeroGearClass
    marksman: HeroGearClass

class HeroGearTotals(BaseModel):
    infantry_lethality_pct: float
    infantry_health_pct: float
    infantry_attack_pct: float
    infantry_defense_pct: float
    lancer_lethality_pct: float
    lancer_health_pct: float
    lancer_attack_pct: float
    lancer_defense_pct: float
    marksman_lethality_pct: float
    marksman_health_pct: float
    marksman_attack_pct: float
    marksman_defense_pct: float


def _calc_infantry(p: HeroGearClass) -> tuple[float,float,float,float]:
    # returns (leth, health, atk, def)
    g1 = _inf_goggles(p.goggles.level, p.goggles.mastery_forged, p.goggles.mastery_level, p.goggles.essence_level, p.goggles.stacking)
    b1 = _inf_boot(p.boot.level, p.boot.mastery_forged, p.boot.mastery_level, p.boot.essence_level, p.boot.stacking)
    g2 = _inf_glove(p.glove.level, p.glove.mastery_forged, p.glove.mastery_level, p.glove.essence_level, p.glove.stacking)
    b2 = _inf_belt(p.belt.level, p.belt.mastery_forged, p.belt.mastery_level, p.belt.essence_level, p.belt.stacking)
    leth = float(g1.get("infantry_lethality_pct",0.0)) + float(b1.get("infantry_lethality_pct",0.0))
    hp   = float(g2.get("infantry_health_pct",0.0)) + float(b2.get("infantry_health_pct",0.0))
    atk  = float(g1.get("infantry_attack_pct",0.0)) + float(b2.get("infantry_attack_pct",0.0))
    df   = float(g2.get("infantry_defense_pct",0.0)) + float(b1.get("infantry_defense_pct",0.0))
    return leth, hp, atk, df

def _calc_lancer(p: HeroGearClass) -> tuple[float,float,float,float]:
    g1 = _lan_goggles(p.goggles.level, p.goggles.mastery_forged, p.goggles.mastery_level, p.goggles.essence_level, p.goggles.stacking)
    b1 = _lan_boot(p.boot.level, p.boot.mastery_forged, p.boot.mastery_level, p.boot.essence_level, p.boot.stacking)
    g2 = _lan_glove(p.glove.level, p.glove.mastery_forged, p.glove.mastery_level, p.glove.essence_level, p.glove.stacking)
    b2 = _lan_belt(p.belt.level, p.belt.mastery_forged, p.belt.mastery_level, p.belt.essence_level, p.belt.stacking)
    leth = float(g1.get("lancer_lethality_pct",0.0)) + float(b1.get("lancer_lethality_pct",0.0))
    hp   = float(g2.get("lancer_health_pct",0.0)) + float(b2.get("lancer_health_pct",0.0))
    atk  = float(g1.get("lancer_attack_pct",0.0)) + float(b2.get("lancer_attack_pct",0.0))
    df   = float(g2.get("lancer_defense_pct",0.0)) + float(b1.get("lancer_defense_pct",0.0))
    return leth, hp, atk, df

def _calc_marksman(p: HeroGearClass) -> tuple[float,float,float,float]:
    g1 = _mm_goggles(p.goggles.level, p.goggles.mastery_forged, p.goggles.mastery_level, p.goggles.essence_level, p.goggles.stacking)
    b1 = _mm_boot(p.boot.level, p.boot.mastery_forged, p.boot.mastery_level, p.boot.essence_level, p.boot.stacking)
    g2 = _mm_glove(p.glove.level, p.glove.mastery_forged, p.glove.mastery_level, p.glove.essence_level, p.glove.stacking)
    b2 = _mm_belt(p.belt.level, p.belt.mastery_forged, p.belt.mastery_level, p.belt.essence_level, p.belt.stacking)
    leth = float(g1.get("marksman_lethality_pct",0.0)) + float(b1.get("marksman_lethality_pct",0.0))
    hp   = float(g2.get("marksman_health_pct",0.0)) + float(b2.get("marksman_health_pct",0.0))
    atk  = float(g1.get("marksman_attack_pct",0.0)) + float(b2.get("marksman_attack_pct",0.0))
    df   = float(g2.get("marksman_defense_pct",0.0)) + float(b1.get("marksman_defense_pct",0.0))
    return leth, hp, atk, df


@app.post("/api/hero-gear/calc", response_model=HeroGearTotals)
def calc_hero_gear(req: HeroGearCalcRequest):
    # Created Logic for review: sum four pieces per class, mapping lethality/health and empowerment bonuses appropriately
    i_leth, i_hp, i_atk, i_def = _calc_infantry(req.infantry)
    l_leth, l_hp, l_atk, l_def = _calc_lancer(req.lancer)
    m_leth, m_hp, m_atk, m_def = _calc_marksman(req.marksman)
    return HeroGearTotals(
        infantry_lethality_pct=round(i_leth, 2),
        infantry_health_pct=round(i_hp, 2),
        infantry_attack_pct=round(i_atk, 2),
        infantry_defense_pct=round(i_def, 2),
        lancer_lethality_pct=round(l_leth, 2),
        lancer_health_pct=round(l_hp, 2),
        lancer_attack_pct=round(l_atk, 2),
        lancer_defense_pct=round(l_def, 2),
        marksman_lethality_pct=round(m_leth, 2),
        marksman_health_pct=round(m_hp, 2),
        marksman_attack_pct=round(m_atk, 2),
        marksman_defense_pct=round(m_def, 2),
    )

@app.get("/api/gear/chief/charms/options", response_model=List[Dict[str, Any]])
def get_chief_charms_options():
    """
    Returns a flat list of charm level options with fields { level, lethalityPct, healthPct, power }.
    """
    return [
        {
            "level": r.get("Level"),
            "lethalityPct": float(r.get("Lethality", 0)) * 100.0,
            "healthPct": float(r.get("Health", 0)) * 100.0,
            "power": int(r.get("Power_Total", 0)),
        }
        for r in chief_charms_data
    ]


@app.post("/api/gear/chief/charms/calc", response_model=ChiefCharmsTotals)
def calc_chief_charms(req: ChiefCharmsRequest):
    # Created Logic for review: charms are per slot; each slot has 3 charms; sum their stats
    # Acceptable slots reuse the same chief gear slots
    total_lethality_pct = 0.0
    total_health_pct = 0.0
    total_power = 0
    breakdown: Dict[str, Dict[str, float]] = {}

    levels_to_row: Dict[int, Dict[str, Any]] = {int(r["Level"]): r for r in chief_charms_data}

    # class-specific buckets based on slot mapping like gear
    infantry_lethality_pct = infantry_health_pct = 0.0
    lancer_lethality_pct = lancer_health_pct = 0.0
    marksman_lethality_pct = marksman_health_pct = 0.0
    infantry_power = lancer_power = marksman_power = 0

    for slot, levels in req.levels_by_slot.items():
        if slot not in ("Cap", "Coat", "Ring", "Watch", "Pants", "Weapon"):
            raise HTTPException(422, f"Unknown slot for charms: {slot}")
        if not isinstance(levels, list) or len(levels) != 3:
            raise HTTPException(422, f"Slot {slot} must provide exactly 3 charm levels")

        slot_leth = 0.0
        slot_hp = 0.0
        slot_pow = 0
        for lv in levels:
            row = levels_to_row.get(int(lv))
            if not row:
                raise HTTPException(422, f"Invalid charm level {lv} for {slot}")
            slot_leth += float(row.get("Lethality", 0)) * 100.0
            slot_hp += float(row.get("Health", 0)) * 100.0
            slot_pow += int(row.get("Power_Total", 0))

        breakdown[slot] = {"lethalityPct": slot_leth, "healthPct": slot_hp, "power": float(slot_pow)}
        total_lethality_pct += slot_leth
        total_health_pct += slot_hp
        total_power += slot_pow

        # distribute to classes by slot
        if slot in ("Coat", "Pants"):
            infantry_lethality_pct += slot_leth
            infantry_health_pct += slot_hp
            infantry_power += slot_pow
        elif slot in ("Cap", "Watch"):
            lancer_lethality_pct += slot_leth
            lancer_health_pct += slot_hp
            lancer_power += slot_pow
        elif slot in ("Ring", "Weapon"):
            marksman_lethality_pct += slot_leth
            marksman_health_pct += slot_hp
            marksman_power += slot_pow

    return ChiefCharmsTotals(
        total_lethality_pct=round(total_lethality_pct, 2),
        total_health_pct=round(total_health_pct, 2),
        total_power=int(total_power),
        breakdown=breakdown,
        infantry_lethality_pct=round(infantry_lethality_pct, 2),
        infantry_health_pct=round(infantry_health_pct, 2),
        lancer_lethality_pct=round(lancer_lethality_pct, 2),
        lancer_health_pct=round(lancer_health_pct, 2),
        marksman_lethality_pct=round(marksman_lethality_pct, 2),
        marksman_health_pct=round(marksman_health_pct, 2),
        infantry_power=int(infantry_power),
        lancer_power=int(lancer_power),
        marksman_power=int(marksman_power),
    )


# -----------------------------
# Research tree routes
# -----------------------------

class ResearchNode(BaseModel):
    category: str
    tier_label: str
    level: int
    power: int
    stat_name: str
    value: float


class ResearchFindResponse(BaseModel):
    value: Optional[float]


@app.get("/api/research/categories", response_model=List[str])
def research_categories():
    return research_get_category_names()


@app.get("/api/research/tiers", response_model=List[str])
def research_tiers(category: str = Query(..., description="Research category name")):
    try:
        return research_get_tier_labels(category)
    except Exception:
        raise HTTPException(422, f"Unknown category: {category}")


@app.get("/api/research/nodes", response_model=List[ResearchNode])
def research_nodes(
    category: str = Query(..., description="Research category name"),
    tier: str = Query(..., description="Tier label, e.g., 'Level 3'"),
):
    # Created Logic for review: normalize node dicts into a single {level, power, stat_name, value}
    try:
        raw_nodes = research_get_nodes(category, tier)
    except Exception:
        raise HTTPException(422, f"Unknown category/tier: {category} / {tier}")

    def stat_keys_for_node(node: dict) -> List[str]:
        meta = {"level", "power", category}
        return [k for k in node.keys() if k not in meta]

    out: List[ResearchNode] = []
    for node in raw_nodes:
        level = int(node.get("level", 0))
        power = int(node.get("power", 0))
        keys = stat_keys_for_node(node)
        if not keys:
            continue
        # most nodes have exactly one stat key; if multiple, return one item per key
        for k in keys:
            try:
                val = float(node.get(k, 0))
            except Exception:
                val = 0.0
            out.append(
                ResearchNode(
                    category=category,
                    tier_label=tier,
                    level=level,
                    power=power,
                    stat_name=k,
                    value=val,
                )
            )
    return out


@app.get("/api/research/find", response_model=ResearchFindResponse)
def research_find(
    category: str = Query(...),
    tier: str = Query(..., alias="tier"),
    level: int = Query(...),
    stat: str = Query(..., description="Stat name, e.g., 'Troop Attack'"),
):
    try:
        v = research_find_stat(category, tier, int(level), stat)
    except Exception:
        raise HTTPException(422, f"Invalid lookup for {category} / {tier} / {level} / {stat}")
    return ResearchFindResponse(value=v)


@app.get("/api/research/flatten", response_model=List[ResearchNode])
def research_flatten_all():
    # Map flattened rows into ResearchNode model
    rows = research_flatten()
    out: List[ResearchNode] = []
    for r in rows:
        try:
            out.append(
                ResearchNode(
                    category=str(r.get("category")),
                    tier_label=str(r.get("tier_label")),
                    level=int(r.get("level", 0)),
                    power=int(r.get("power", 0)),
                    stat_name=str(r.get("stat_name")),
                    value=float(r.get("value", 0)),
                )
            )
        except Exception:
            # skip malformed rows
            continue
    return out

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
        api_key = req.openai_api_key or os.getenv("OPENAI_API_KEY")
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
