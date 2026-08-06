# Construction — Foam-Core GRP Sandwich

Status: method decision, August 2026. Schedule in `freecad/laminate.py`,
areas measured off the solids by `freecad/areas.py` into
`freecad/areas.json`, mass asserted in `params.checks()`.

Primary structure is **PVC/PET foam core with biaxial E-glass skins in
epoxy, vacuum bagged**. The steel exoskeleton stays steel — see
[structure.md](structure.md).

Why, in priority order:

1. **Mass.** It is the lightest structure one person can build without a
   yard.
2. **Skills and tools.** No welding qualification, no 400 V three-phase,
   no EN 1090 conversation, no galvanic design inside the hull. Panels
   are laid up on a flat table with hand tools and a vacuum pump.
3. **Cost.** Materials cost more per kg than steel; there is no
   fabrication labour to buy and no trade to learn first.

## 1. Panel schedule

The governing principle: **panel stiffness goes as the square of core
thickness, so thicker core with thinner skins beats more glass, every
time.** Skins here are set by impact, abrasion and print-through — not
by a bending calculation.

| Zone | Core | mm | Outer | Inner | kg/m² | Panel | Purpose |
|---|---|---|---|---|---|---|---|
| Hull bottom | PVC80 | 20 | 1800 | 900 | 7.60 | 23 | slam, grounding, trailer |
| Hull topsides | PET60 | 20 | 900 | 600 | 4.53 | 22 | stiffness, not strength |
| Hull deck | PET60 | 25 | 900 | 600 | 4.83 | 27 | walked on; dome, hardware |
| Float shell | PVC80 | 18 | 1200 | 800 | 5.88 | 20 | grounding, wheel loads |
| Float deck | PET100 | 20 | 1200 | 800 | 6.44 | 22 | axle landings, denser core |
| Cabin walls | PET60 | 20 | 600 | 600 | 3.87 | 21 | distributed loads only |
| Roof sandwich | PET60 | 200 | 900 | 900 | 16.00 | 202 | carries the glass deck, 2.4 m span |
| Bulkheads | PET60 | 15 | 600 | 600 | 3.57 | 16 | shear webs, tank boundaries |

Fibre fraction **0.45** — hand layup under a bag. Only claim 0.55 if the
panels are actually infused.

**One core per panel.** No wood-and-foam sandwiches: the two move
differently with moisture and temperature and the joint between them
becomes the failure plane. Plywood appears only as **local inserts**,
routed in at every through-bolt.

**Fabric: stitched non-crimp biaxial, not woven roving.** Woven fibres
crimp over each other at every crossing and lose real stiffness for the
same weight. Skip triaxial — biax plus separate unidirectional where
axial stiffness is wanted gives better control at lower cost.

**Margin ×1.12** on every computed mass, for fillets, tapes, overlaps,
bog, and the resin you actually use rather than the resin the arithmetic
says you need. This is the single most commonly underestimated item in a
composite build.

## 2. Measured areas and structural mass

Areas are **measured off the FreeCAD solids**, not estimated:

| Zone | m² measured | kg |
|---|---|---|
| Float shell (both) | 24.18 | 159 |
| Hull topsides | 15.90 | 81 |
| Hull bottom | 15.28 | 130 |
| Cabin walls | 17.92 | 78 |
| Roof sandwich | 12.41 | 222 |
| Bulkheads | 9.94 | 40 |
| Hull deck | 4.32 | 23 |
| Float deck (both) | 2.85 | 21 |
| **Total** | **102.8 m²** | **754 kg** (margin included) |

Two things fall out of that table:

- **The floats carry more laminate area than the hull does** — 27 m²
  against 35 m² for the whole hull including deck. They are the first
  place to look when mass has to come out.
- **The roof sandwich is 222 kg for 12 m²** — 200 mm of core, because it
  spans 2.4 m carrying a walk-on glass deck. It is the heaviest square
  metre on the boat and it sits 2.4 m up, where mass hurts stability
  about three times as much as mass in the bilge.

Against the brief's hand estimates the model is lighter almost
everywhere — 103 m² measured against ~130 m² estimated, and 754 kg
against ~1 008 kg. The differences over 15 %: hull deck (4.3 vs 8 m² —
most of the deck is cabin footprint and dome opening, both cut away),
float deck (2.9 vs 8 — the float's flat top is narrow), bulkheads (9.9
vs 15) and float shell (24.2 vs 32).

## 3. Build sequence — flat panel, and the answer to "is it developable?"

**Measured, on the model:** the hull's panel strips are ruled quads
between chined stations, and their out-of-plane twist is:

| Region | Worst twist |
|---|---|
| Parallel midbody, x 1 800 – 5 400 | **0.0 mm** — exactly developable |
| Aft, x 0 – 1 800 | 21 mm |
| Bow, x 5 400 – 7 200 | **35 mm** (topsides at x 6 300) |

So: **the middle 3.6 m of the boat is flat-panel work with no jig at
all**, and the ends need either cold-forming or a light frame. 35 mm of
twist across a ~1.2 m panel is more than a 20 mm sandwich will take
cold. Options for the ends, cheapest first:

1. **Kerf the core** on the inside face and let the panel twist, then
   laminate the inner skin over the kerfs. Standard practice.
2. **A light frame-and-batten jig for the bow only** — three or four
   station moulds, not a full male plug.
3. **Re-fair the bow chine to zero twist.** The chine line is a free
   parameter; moving it can make the bow panels developable too. This is
   a hull-shape change and needs sign-off — say the word and it is an
   afternoon of numerical work in `params.py`.

Sequence:

1. **Lay up flat panels on a table**, bag them, **post-cure them flat**.
2. **CNC-cut from the FreeCAD surfaces** — the model already carries the
   geometry, so there is no lofting step.
3. **Assemble** hull and floats from cut panels: tape internal joints
   with biax, fillet with thickened epoxy, tape externally.
4. **Fair, coat, paint.**

**Post-cure is not optional.** The roof panels sit under dark solar
laminates behind glass and will see 60–70 °C. Room-temperature-cured
epoxy has a Tg of 50–60 °C: it will creep and print through. Post-cure
at ≥ 55 °C **while the panel is flat on the table** — it cannot be
retrofitted once the boat is assembled. `checks()` asserts this.

## 4. Shop requirements — this changes the workshop hunt

- **Heat.** Epoxy needs 18–25 °C and stable humidity. Below ~15 °C the
  cure stalls and you get amine blush and undercured laminate. An
  unheated tent will not do: the build needs an enclosed, heated,
  ventilated space through **two German winters**.
- **Extraction and respiratory protection.** Grinding cured glass is a
  serious exposure, not a nuisance. Extraction and P3 are equipment, not
  optional extras.
- **Vacuum consumables** run €10–20/m² per shot and are thrown away. At
  103 m² of panel that is a real line item, not a rounding error.
- **Flat table**, 6 m minimum, dead flat, plus a vacuum pump and enough
  bagging film to cover the biggest panel in one shot.

## 5. Fairing — the honest number

Full exterior fairing on the hull plus two floats is **≈ 400 hours** of
filler and longboard. It is the largest single labour item on the boat
and the one that stalls owner builds in year two. It has its own line in
the build-time table for that reason — burying it inside "hull shell"
is how a schedule stops being honest.

## 6. Materials and suppliers, German market

| Item | Quantity | Note |
|---|---|---|
| Biaxial E-glass NCF | **203 kg** dry fabric | roll quantities; 600/900/1200/1800 gsm |
| Epoxy resin + hardener | **248 kg** mixed | laminating grade, slow hardener |
| PVC foam (Divinycell H80 class) | **39.5 m²** | 18–20 mm, hull bottom and floats |
| PET foam (ArmaFORM/Airex) | **63.4 m²** | 15–200 mm, topsides, cabin, roof, bulkheads |
| Plywood inserts | as needed | 18 mm, every through-bolt |

Suppliers: **R&G Faserverbundwerkstoffe**, **HP-Textiles**,
**Lange+Ritter** (roll quantities), **Diab** or **Gurit** for PVC,
**Armacell/Airex** for PET. Buying full rolls is typically **25–40 %
cheaper** than cut lengths, and at this surface area full rolls are
consumed anyway.

## 7. Where carbon is worth it

- **Not** in the hull or float skins. You would pay 5–8× for stiffness
  the sandwich already gets from core thickness, and lose impact
  tolerance doing it.
- **Yes**, consider it for the roof and glass-deck substructure. That
  mass sits 2.4 m up and works directly against righting moment; **mass
  aloft costs roughly three times what mass in the bilge costs.**
- **Isolate carbon from aluminium** with a glass barrier ply wherever
  they meet. The galvanic couple is aggressive and it eats the
  aluminium, not the carbon. Relevant at the alu roof grid.
- Carbon fails without warning where glass cracks first. Do not use it
  anywhere a warning matters.

## 8. Open questions back to the owner

**Q3 — float schedule.** The floats are 159 kg of laminate for 24 m².
A lighter schedule (12 mm PVC80, 900/600 skins → 4.29 kg/m²) saves
**≈ 38 kg** but the floats take slipway grounding and the wheel
stub-axle reactions. Proposal: lighter base schedule with **local
doublers** at the six axle landings and the six arm roots, rather than
carrying heavy skins over the whole 24 m². Needs a load case per
landing before it is more than a proposal.

**Q4 — float compartmentation.** Not currently modelled, and it should
be. The floats hold the drive motors, pumps and hydraulics *and* they
are the reserve buoyancy in the jack-up stance. Holing one on a slipway
today loses the whole float. Recommendation: **three watertight
compartments per float** — machinery bay amidships, buoyancy cells fore
and aft — so a holed cell costs a third of one float, not half the
boat's reserve. Cheap in composite (three bulkheads per float, already
in the schedule), impossible to retrofit.
