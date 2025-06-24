# Rally Calc Laptop

This project is a toolkit for simulating and analyzing battle and rally mechanics, hero data, and troop data for a strategy game. The codebase is organized into modules for battle mechanics, hero and troop data, and supporting documentation.

## File Organization

Below is a Mermaid diagram visualizing the file and folder structure of the project in a left-to-right outline format (excluding the Archive and Docs folders):

```mermaid
flowchart LR
  A["rally_calc_laptop/"]
  A1["battle_mechanics.py"]
  A2["hero_data/"]
  A3["troop_data/"]

  A --> A1
  A --> A2
  A --> A3

  A2 --> A2a["__init__.py"]
  A2 --> A2b["epic_heroes/"]
  A2 --> A2c["rare_heroes/"]
  A2 --> A2d["ssr_gen_eight_heroes/"]
  A2 --> A2e["ssr_gen_five_heroes/"]
  A2 --> A2f["ssr_gen_four_heroes/"]
  A2 --> A2g["ssr_gen_one_heroes/"]
  A2 --> A2h["ssr_gen_seven_heroes/"]
  A2 --> A2i["ssr_gen_six_heroes/"]
  A2 --> A2j["ssr_gen_three_heroes/"]
  A2 --> A2k["ssr_gen_two_heroes/"]

  A2b --> A2b1["bahiti.py"]
  A2b --> A2b2["gina.py"]
  A2b --> A2b3["jassar.py"]
  A2b --> A2b4["jessie.py"]
  A2b --> A2b5["patrick.py"]
  A2b --> A2b6["seo_yoon.py"]
  A2b --> A2b7["sergey.py"]
  A2b --> A2b8["walis_bokan.py"]

  A2c --> A2c1["charlie.py"]
  A2c --> A2c2["cloris.py"]
  A2c --> A2c3["eugene.py"]
  A2c --> A2c4["smith.py"]

  A2d --> A2d1["gatot.py"]
  A2d --> A2d2["hendrik.py"]
  A2d --> A2d3["sonya.py"]

  A2e --> A2e1["gwen.py"]
  A2e --> A2e2["hector.py"]
  A2e --> A2e3["norah.py"]

  A2f --> A2f1["ahmose.py"]
  A2f --> A2f2["lynn.py"]
  A2f --> A2f3["reina.py"]

  A2g --> A2g1["jeronimo.py"]
  A2g --> A2g2["molly.py"]
  A2g --> A2g3["natalia.py"]
  A2g --> A2g4["zinman.py"]

  A2h --> A2h1["bradley.py"]
  A2h --> A2h2["edith.py"]
  A2h --> A2h3["gordon.py"]

  A2i --> A2i1["renee.py"]
  A2i --> A2i2["wayne.py"]
  A2i --> A2i3["wu_ming.py"]

  A2j --> A2j1["greg.py"]
  A2j --> A2j2["logan.py"]
  A2j --> A2j3["mia.py"]

  A2k --> A2k1["alonso.py"]
  A2k --> A2k2["flint.py"]
  A2k --> A2k3["philly.py"]

  A3 --> A3a["troop_definiions.py"]
```

---

This diagram provides a high-level overview of the folder and file organization for easy navigation and understanding of the codebase.
