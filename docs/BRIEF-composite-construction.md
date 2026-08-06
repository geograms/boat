# BRIEF — switch primary structure to foam-core GRP, and force the mass budget to close

Hand this to Claude Code in the `boat-home` repo. It describes a construction-method
change plus the model/doc work needed to carry it through `params.py`, `checks()`,
the README and the PDF.

Read `README.md`, `docs/structure.md`, `docs/interior.md` and `freecad/params.py`
before starting. Nothing here should be applied blindly — where a number below
conflicts with something already computed in the model, the model wins and the
conflict gets reported back, not silently overwritten.

---

## 0. The two changes

**A. Construction method.** Primary structure moves to foam-core GRP sandwich:
PVC/PET foam core, biaxial E-glass skins, epoxy resin, vacuum bagged. This replaces
whatever the current hull/float construction assumption is in `structure.md`.

Rationale, in priority order:

1. **Mass.** It is the lightest structure buildable by one person without a yard.
2. **Skills and tools.** No welding qualification, no 400 V three-phase, no
   EN 1090 conversation, no galvanic-corrosion design in the hull. Panels can be
   laid up on a flat table with hand tools and a vacuum pump.
3. **Cost.** Materials are higher per kg than steel, but there is no fabrication
   labour to buy and no shop rate to pay.

**B. Mass budget.** `checks()` currently lets `DESIGN_ALL_UP = 2000 kg` coexist with
a performance model run at 2 600 kg and a §7 risk note saying the structure does not
fit in what's left. That inconsistency has to become a hard failure.

**What does not change:** the steel exoskeleton, the wheels/hangar kinematics, the
waterjets, the walk-on glass deck, the interior layout, the road-approval strategy.
See §9.

---

## 1. Laminate schedule — new module

Create `freecad/laminate.py`. It owns areal masses so that structural mass is
*computed* from geometry rather than estimated in prose.

```python
"""Laminate schedule. Areal masses include resin at the stated fibre fraction."""

FIBRE_FRACTION = 0.45          # hand layup + vacuum bag; 0.55 only if infused
RESIN_DENSITY  = 1150          # kg/m3, epoxy
GLASS_DENSITY  = 2560          # kg/m3, E-glass

CORES = {
    "PVC80":  {"rho":  80, "note": "Divinycell H80 class - bottom, slam, hardware"},
    "PET60":  {"rho":  60, "note": "ArmaFORM/Airex PET - topsides, cabin, deck"},
    "PET100": {"rho": 100, "note": "float deck under wheel stub axles"},
    "PLY18":  {"rho": 650, "note": "local inserts at every through-bolt"},
}

# zone: (core, core_mm, outer_skin_gsm, inner_skin_gsm)
ZONES = {
    "hull_bottom":   ("PVC80",  20, 1800,  900),
    "hull_topsides": ("PET60",  20,  900,  600),
    "hull_deck":     ("PET60",  25,  900,  600),
    "float_shell":   ("PVC80",  18, 1200,  800),
    "float_deck":    ("PET100", 20, 1200,  800),
    "cabin_walls":   ("PET60",  20,  600,  600),
    "roof_sandwich": ("PET60", 200,  900,  900),   # per roof.md, carries glass deck
    "bulkheads":     ("PET60",  15,  600,  600),
}

def skin_areal(gsm):
    """kg/m2 of one cured skin at FIBRE_FRACTION."""
    return (gsm / 1000.0) / FIBRE_FRACTION

def panel_areal(zone):
    core, mm, outer, inner = ZONES[zone]
    core_kg = CORES[core]["rho"] * mm / 1000.0
    return core_kg + skin_areal(outer) + skin_areal(inner)
```

Add a `LAMINATE_MARGIN = 1.12` factor applied to every computed structural mass —
covers fillets, tapes, overlaps, bog and the resin you will actually use rather
than the resin the arithmetic says you need. Do not omit this; it is the single
most commonly underestimated item in a composite build.

**Do not stack two cores.** If `structure.md` anywhere describes wood *and* foam
in the same panel, remove it — one core per panel.

---

## 2. `params.py` additions

```python
# --- construction -------------------------------------------------------
CONSTRUCTION       = "foam_core_grp"
BUILD_METHOD       = "flat_panel"      # or "male_jig"; see open question Q1
VACUUM_METHOD      = "wet_layup_bagged"  # not infusion; see docs/construction.md
POST_CURE_C        = 55                # deck panels see 60-70 C under the glass
LAMINATE_TOL_MM    = 3                 # per side, as-built thickness tolerance
```

Then **compute** these from the FreeCAD geometry rather than hard-coding them —
that is the whole point of the exercise:

- `AREA_HULL_BOTTOM`, `AREA_HULL_TOPSIDES`, `AREA_HULL_DECK`
- `AREA_FLOAT_SHELL`, `AREA_FLOAT_DECK` (both floats combined)
- `AREA_CABIN_WALLS` (net of glazing openings)
- `AREA_ROOF_SANDWICH`
- `AREA_BULKHEADS`

My rough hand estimates, **for sanity-checking the computed values only** — if the
model disagrees by more than ~15%, report it rather than adopting my numbers:

| Zone | Est. area | Est. areal | Est. mass |
|---|---|---|---|
| Hull bottom | 18 m² | 11.6 kg/m² | 209 kg |
| Hull topsides | 13 m² | 4.5 kg/m² | 59 kg |
| Hull deck | 8 m² | 4.8 kg/m² | 38 kg |
| Float shell (both) | 32 m² | 5.9 kg/m² | 189 kg |
| Float deck (both) | 8 m² | 6.4 kg/m² | 51 kg |
| Cabin walls | 22 m² | 3.9 kg/m² | 86 kg |
| Roof sandwich | 14 m² | 15.3 kg/m² | 214 kg |
| Bulkheads | 15 m² | 3.6 kg/m² | 54 kg |
| **Subtotal** | | | **~900 kg** |
| × 1.12 margin | | | **~1 008 kg** |

The float shell is the surprise: two 6.2 m floats carry more skin area than the
hull does. Flag that in `structure.md` — it is the first place to look if mass
needs to come out.

---

## 3. `checks()` — new asserts

### 3.1 Mass closure (this one is expected to FAIL on first run — that is the point)

```python
structural = sum(panel_areal(z) * AREAS[z] for z in ZONES) * LAMINATE_MARGIN
known      = (structural + MASS_EXOSKELETON + MASS_WHEELS_HUBS
              + MASS_ARMS + MASS_JETS + MASS_BATTERY + MASS_INTERIOR
              + MASS_GLASS_DECK + MASS_SOLAR + MASS_ELECTRICS)
assert known <= DESIGN_ALL_UP, (
    f"mass budget does not close: {known:.0f} kg computed "
    f"vs {DESIGN_ALL_UP} kg design figure")
```

Do **not** raise `DESIGN_ALL_UP` to make this pass. Report the computed figure and
stop. Resolving it is my decision — see Q2 in §10.

### 3.2 Single mass figure

`DESIGN_ALL_UP` (§1) and the mass used in `performance.md` must be the same
variable. Right now §1 says 2 000 kg and §2 computes at 2 600 kg. Wire the
performance model to `DESIGN_ALL_UP` and let the speed/range table move.

### 3.3 Waterline follows mass

Stop asserting `draft == 260 mm`. Compute the waterline from `DESIGN_ALL_UP` and
the hull's hydrostatics, and assert instead:

- freeboard at the computed waterline ≥ some minimum
- the jack-up stance still works: float buoyancy ≥ 1.4 × all-up mass
- ground clearance in road mode unaffected (it is set by geometry, not draft)

### 3.4 Road width tolerance — new, and tight

`BEAM_ROAD = 2535 mm` against a 2 550 mm StVZO limit is **15 mm of total margin,
7.5 mm per side.** In welded metal that is fine. In hand-laid composite it is not
automatically fine: skin thickness varies with layup technique, and a bog-and-fair
coat adds 1–3 mm per side on its own.

```python
assert BEAM_ROAD + 2 * (LAMINATE_TOL_MM + FAIR_COAT_MM) <= 2550, (
    "as-built road beam can exceed the StVZO limit")
```

If that fails, the fix is to take the nominal beam down to ~2 500 mm and spend the
margin on build tolerance. **This is the single most likely way the boat becomes
road-illegal after it is built**, and it is much cheaper to fix in `params.py` than
in a mould.

### 3.5 Post-cure vs deck temperature

The roof sandwich sits under dark solar laminates behind glass. Assert
`POST_CURE_C >= 55` and note in `roof.md` that room-temperature-cured epoxy
(Tg ≈ 50–60 °C) will creep and print through under that deck. Panels must be
post-cured while flat on the table — it is effectively impossible to retrofit
once assembled.

---

## 4. New document: `docs/construction.md`

Written to the same standard as the other `docs/*.md`. Cover:

**Panel schedule** — the `ZONES` table above, in human-readable form, with the
reasoning for each core density. Key principle to state explicitly: *panel
stiffness goes as the square of core thickness, so thicker core and thinner skins
beats more glass every time.* Skins are set by impact, abrasion and print-through,
not by bending calculation.

**Build sequence** — the flat-panel route, assuming it survives Q1:

1. Infuse or bag flat sandwich panels on a table (repeatable, near-perfect, one
   person, no jig fairing).
2. CNC-cut panels from the FreeCAD surfaces — the model already has the geometry,
   so no lofting.
3. Assemble hull and floats from cut panels; tape internal joints with biax,
   fillet with thickened epoxy, tape externally.
4. Fair, coat, paint.

**Consumables and shop requirements** — this changes the workshop hunt materially
and needs saying plainly:

- Epoxy needs 18–25 °C and stable humidity. Below ~15 °C cure stalls and you get
  amine blush and undercured laminate. An unheated tent will not do; the build
  needs an enclosed, heated, ventilated space through two German winters.
- Grinding cured glass is a serious respiratory exposure, not a nuisance. Extraction
  and P3 protection are equipment, not optional extras.
- Vacuum consumables run ~€10–20/m² per shot and are discarded.

**Fairing** — state the honest number. Full exterior fairing on hull plus two floats
is several hundred hours of filler and longboard. It is the largest single labour
item and the one that stalls owner builds in year two. It belongs in the build-time
table (§6) as its own line, not buried in "hull shell, bulkheads, fairing".

**Suppliers, German market** — R&G Faserverbundwerkstoffe, HP-Textiles,
Lange+Ritter (roll quantities), Diab or Gurit for PVC, Armacell/Airex for PET.
Note that buying full rolls is typically 25–40 % cheaper than cut lengths, and at
this surface area full rolls will be consumed anyway.

**Fabric note** — specify stitched non-crimp biaxial, not woven roving. Woven fibres
crimp over each other at every crossing and lose real stiffness for the same weight.
Skip triaxial: biax plus separate unidirectional where axial stiffness is wanted
gives better control at lower cost.

---

## 5. Where carbon is and is not worth it

Add to `structure.md`. Short version:

- **Not** in hull or float skins. Paying 5–8× for stiffness the sandwich already
  gets from core thickness, and losing impact tolerance to do it.
- **Yes**, consider it for the roof/glass-deck substructure. That mass sits 2.5 m
  up and works directly against righting moment. Mass aloft is worth roughly three
  times mass in the bilge.
- **Isolate carbon from aluminium** with a glass barrier ply wherever they meet —
  the galvanic couple is aggressive and it eats the aluminium, not the carbon.
  Relevant at the alu roof grid.
- Carbon fails without warning where glass cracks first. Do not use it anywhere a
  warning matters.

---

## 6. README edits

**§4 Key systems** — add a `Construction` bullet before `Roof deck`, one paragraph,
pointing to `docs/construction.md`.

**§5 Cost table** — replace the `Hull shell, structure, fairing` and `Floats` lines
with a computed breakdown. Drive it from areas × areal mass × unit price so it
updates with the model:

| Item | Low | High | Source |
|---|---|---|---|
| Foam core, PVC + PET, by zone | 3 800 | 5 200 | construction.md |
| Glass fabric, biax NCF, roll qty | 2 200 | 3 000 | construction.md |
| Epoxy resin + hardener + fillers | 4 500 | 6 500 | construction.md |
| Vacuum consumables | 1 200 | 2 000 | construction.md |
| Fairing compound, primer | 900 | 1 500 | construction.md |
| Tooling: pump, table, extraction, PPE | 1 500 | 2 500 | construction.md |

Materials total goes **up** slightly against the current 12 000–18 000 + 3 500–4 500
for hull and floats. The saving is not in the material line — it is that there is
no fabricator invoice and no equipment purchase for a trade you would have to learn.
Say that explicitly rather than claiming composites are cheaper, because on the
materials line they are not.

**§6 Build time** — split `Hull shell, bulkheads, fairing` into:

| Phase | Hours |
|---|---|
| Panel layup and post-cure | 250 |
| Hull and float assembly, taping, filleting | 350 |
| Fairing and coating | 400 |

That pushes the total to roughly 3 100 h, i.e. ~4 years at 15 h/week or ~2.4 years
at 25 h/week. Update the bullets under the table. This is a real increase and it
should not be smoothed over — composite is lighter and needs no trade skills, but
it is not faster than welding.

**§7 Open risks** — rewrite. Remove any risk relating to welding or metal
fabrication. Add:

1. **Mass budget — still the binding constraint.** State the computed figure from
   §3.1 and the chosen resolution.
2. **Road beam tolerance.** 15 mm of margin against StVZO on a hand-built
   laminate. See §3.4.
3. **Fairing labour.** 400 h is the estimate; it is the item most likely to
   overrun and the one that stalls projects.
4. **Workshop conditioning.** Two heated winters, not a tent.
5. Keep the existing brake/homologation, jet hydrodynamics and shoulder-pin
   fatigue risks unchanged — none are affected by this decision.

---

## 7. Things to leave alone

Explicitly do **not** touch these while implementing the above:

- **The steel exoskeleton stays steel.** An external frame taking every point load
  so nothing structural crosses the living volume is a good decision and it works
  even better with composite panels — the panels then carry only distributed loads,
  which is exactly what sandwich is good at. Isolate steel from laminate with a
  glass barrier and bed fittings in ply or high-density inserts.
- Wheels, hangar kinematics, hub stack, hydraulics.
- Waterjets, intake grilles, weed strategy.
- Walk-on glass deck sizing and the 8-pane layout.
- Interior layout and the sky dome geometry.
- The road-approval strategy: O2 trailer, ≤ 6 km/h land drive, catalogue overrun
  brake set. **Note:** if the mass resolution in Q2 lands above 3 500 kg, the O2
  category is exceeded and the whole homologation route changes. Check this and
  flag it loudly if so.

---

## 8. Deliverables

1. `freecad/laminate.py` — new
2. `freecad/params.py` — construction block, computed areas, updated `checks()`
3. `docs/construction.md` — new
4. `docs/structure.md` — revised for composite + carbon guidance
5. `README.md` — §4, §5, §6, §7 as above
6. `docs/make_pdf.py` run to regenerate `docs/boat-home.pdf`
7. A short report of what `checks()` now fails on, with the numbers

---

## 9. Questions to come back to me with — do not guess

**Q1 — Are the hull and float surfaces developable?** Check Gaussian curvature on
the hull and float surfaces in the FreeCAD model. If they are developable or near
enough, flat-panel construction works and the build gets dramatically simpler: no
jig, no batten fairing, panels cut flat and folded up. If they are not, we need a
male frame-and-batten jig and the build sequence in `construction.md` changes.
This single answer determines roughly a year of schedule. Answer it first.

**Q2 — Mass resolution.** Once §3.1 gives a real number, present the options with
consequences rather than picking one:
(a) accept ~3 000 kg, tow with a 3 500 kg-rated vehicle, resize the brake set,
    confirm still inside category O2;
(b) delete or reduce the walk-on glass deck (460 kg — the largest discretionary
    item on the boat);
(c) reduce battery to 30 kWh (−140 kg) and accept the range hit;
(d) some combination.
Include what each does to the §2 speed/range table.

**Q3 — Float shell schedule.** The floats carry more laminate area than the hull.
Is there a lighter schedule that still takes slipway grounding loads and the wheel
stub-axle reactions, with local reinforcement only where the arms and axles land?

**Q4 — Do the floats need to be watertight-compartmented?** They contain the drive
motors, pumps and hydraulics and they are the boat's reserve buoyancy in jack-up
stance. If one is holed on a slipway, what does the stability picture look like?
This is not in the current documents and it should be.
