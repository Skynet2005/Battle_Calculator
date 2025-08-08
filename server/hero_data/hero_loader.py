# server/hero_data/hero_loader.py

import os
import importlib.util

# final map: hero-name → hero dict
HEROES = {}

def load_heroes():
    hero_dir = os.path.dirname(__file__)
    for root, _, files in os.walk(hero_dir):
        for file in files:
            # skip ourselves
            if not file.endswith(".py") or file in ("__init__.py", "hero_loader.py"):
                continue

            path = os.path.join(root, file)
            # module name relative to hero_data
            rel = os.path.relpath(path, hero_dir)
            mod_name = os.path.splitext(rel.replace(os.sep, "."))[0]

            spec = importlib.util.spec_from_file_location(mod_name, path)
            if spec and spec.loader:
                mod = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(mod)

                # scan all module globals for hero data
                for val in vars(mod).values():
                    # a single dict with hero-name
                    if isinstance(val, dict) and "hero-name" in val:
                        HEROES[val["hero-name"]] = val
                    # or a list of dicts containing hero-name
                    elif isinstance(val, list):
                        for entry in val:
                            if isinstance(entry, dict) and "hero-name" in entry:
                                HEROES[entry["hero-name"]] = entry

# load on import
load_heroes()
