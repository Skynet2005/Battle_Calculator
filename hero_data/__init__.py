# Index for all hero files by generation and rarity

# Rare Heroes
from .rare_heroes.charlie import charlie_hero
from .rare_heroes.cloris import cloris_hero
from .rare_heroes.eugene import eugene_hero
from .rare_heroes.smith import smith_hero

# Epic Heroes
from .epic_heroes.bahiti import bahiti_hero
from .epic_heroes.gina import gina_hero
from .epic_heroes.jassar import jassar_hero
from .epic_heroes.jessie import jessie_hero
from .epic_heroes.patrick import patrick_hero
from .epic_heroes.seo_yoon import seo_yoon_hero
from .epic_heroes.sergey import sergey_hero
from .epic_heroes.walis_bokan import walis_bokan_hero

# SSR Gen 1
from .ssr_gen_one_heroes.jeronimo import jeronimo_hero
from .ssr_gen_one_heroes.molly import molly_hero
from .ssr_gen_one_heroes.natalia import natalia_hero
from .ssr_gen_one_heroes.zinman import zinman_hero

# SSR Gen 2
from .ssr_gen_two_heroes.alonso import alonso_hero
from .ssr_gen_two_heroes.flint import flint_hero
from .ssr_gen_two_heroes.philly import philly_hero

# SSR Gen 3
from .ssr_gen_three_heroes.greg import greg_hero
from .ssr_gen_three_heroes.logan import logan_hero
from .ssr_gen_three_heroes.mia import mia_hero

# SSR Gen 4
from .ssr_gen_four_heroes.ahmose import ahmose_hero
from .ssr_gen_four_heroes.lynn import lynn_hero
from .ssr_gen_four_heroes.reina import reina_hero

# SSR Gen 5
from .ssr_gen_five_heroes.gwen import gwen_hero
from .ssr_gen_five_heroes.hector import hector_hero
from .ssr_gen_five_heroes.norah import norah_hero

# SSR Gen 6
from .ssr_gen_six_heroes.renee import renee_hero
from .ssr_gen_six_heroes.wayne import wayne_hero
from .ssr_gen_six_heroes.wu_ming import wu_ming_hero

# SSR Gen 7
from .ssr_gen_seven_heroes.bradley import bradley_hero
from .ssr_gen_seven_heroes.edith import edith_hero
from .ssr_gen_seven_heroes.gordon import gordon_hero

# SSR Gen 8
from .ssr_gen_eight_heroes.gatot import gatot_hero
from .ssr_gen_eight_heroes.hendrik import hendrik_hero
from .ssr_gen_eight_heroes.sonya import sonya_hero

# Indexes for programmatic access
RARE_HEROES = [charlie_hero, cloris_hero, eugene_hero, smith_hero]
EPIC_HEROES = [bahiti_hero, gina_hero, jassar_hero, jessie_hero, patrick_hero, seo_yoon_hero, sergey_hero, walis_bokan_hero]
SSR_GEN_ONE_HEROES = [jeronimo_hero, molly_hero, natalia_hero, zinman_hero]
SSR_GEN_TWO_HEROES = [alonso_hero, flint_hero, philly_hero]
SSR_GEN_THREE_HEROES = [greg_hero, logan_hero, mia_hero]
SSR_GEN_FOUR_HEROES = [ahmose_hero, lynn_hero, reina_hero]
SSR_GEN_FIVE_HEROES = [gwen_hero, hector_hero, norah_hero]
SSR_GEN_SIX_HEROES = [renee_hero, wayne_hero, wu_ming_hero]
SSR_GEN_SEVEN_HEROES = [bradley_hero, edith_hero, gordon_hero]
SSR_GEN_EIGHT_HEROES = [gatot_hero, hendrik_hero, sonya_hero]

# All heroes by generation and rarity for easy lookup
ALL_HEROES = {
    'rare': RARE_HEROES,
    'epic': EPIC_HEROES,
    'ssr_gen_1': SSR_GEN_ONE_HEROES,
    'ssr_gen_2': SSR_GEN_TWO_HEROES,
    'ssr_gen_3': SSR_GEN_THREE_HEROES,
    'ssr_gen_4': SSR_GEN_FOUR_HEROES,
    'ssr_gen_5': SSR_GEN_FIVE_HEROES,
    'ssr_gen_6': SSR_GEN_SIX_HEROES,
    'ssr_gen_7': SSR_GEN_SEVEN_HEROES,
    'ssr_gen_8': SSR_GEN_EIGHT_HEROES,
}
