"""Compatibility package to support imports like ``server.main`` when the
repository's ``server`` directory is directly on ``sys.path``.
"""

import sys
import pathlib

_parent = pathlib.Path(__file__).resolve().parent.parent
if str(_parent) not in sys.path:
    sys.path.append(str(_parent))

__all__ = []
