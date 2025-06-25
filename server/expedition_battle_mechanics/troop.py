# battle_mechanics/troop.py

from expedition_battle_mechanics.definitions import TroopDefinition

class TroopGroup:
    """
    A group of troops of a single type, with current count.
    """
    def __init__(self, definition: TroopDefinition, count: int):
        self.definition = definition
        self.count = count
