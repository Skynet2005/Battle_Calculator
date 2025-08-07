# server/main.py

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, validator, Field
from typing import List, Dict, Any

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
