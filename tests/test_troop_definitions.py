import importlib
import pathlib
import sys

# Add the server directory to the module search path
ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.append(str(ROOT / 'server'))

# ensure reload to pick up changes
TROOP_DEFS = importlib.import_module('troop_data.troop_definitions').TROOP_DEFINITIONS

def test_infantry_fc8_and_helios_present():
    assert 'Infantry (FC8)' in TROOP_DEFS
    assert 'Helios Infantry (FC8)' in TROOP_DEFS
    base = TROOP_DEFS['Infantry (FC8)']['Power']
    helios = TROOP_DEFS['Helios Infantry (FC8)']['Power']
    assert helios > base
