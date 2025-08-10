"""
Research package exposing battle research data and helpers.

This module mirrors the working draft in `research(Working)/battle_research_tree.py`
but provides an import-safe package path for the FastAPI server.
"""

from .battle_research_tree import (
    BATTLE_RESEARCH,
    get_category_names,
    get_tier_labels,
    get_nodes,
    find_stat,
    flatten,
)

__all__ = [
    "BATTLE_RESEARCH",
    "get_category_names",
    "get_tier_labels",
    "get_nodes",
    "find_stat",
    "flatten",
]


