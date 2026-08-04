# Boat-Home — Road-Towable Solar Trimaran (Design Study)

A 7.2 m Dutch-barge style boat-home that is **its own trailer**: the
stabilizer floats fold underneath the hull and carry six driven wheels,
so one Mercedes-Viano-class car tows it on German roads, and it drives
itself in and out of the water on slipways. Solar-electric, weed-proof
waterjets, and a walk-on glass sun deck on the roof — you stand on the
glass, the solar panels live safely underneath it.

Parametric CAD in FreeCAD (Python-scripted); every legal and
hydrostatic constraint is asserted in code.

## Key numbers

| | |
|---|---|
| Hull | 7.20 × 2.50 m Dutch barge, WL draft 260 mm, ~2.0 t |
| Road envelope | 2 535 mm wide × 3.01 m tall (limits 2 550 / 4 000) |
| Wheels | 6 × 205/70 R15 all-terrain, in-float hydraulic drive |
| Floats | 6.2 m, ~1.55 t reserve each (82 %), righting SF ≈ 4.5 |
| Water beam | 4.72 m (trimaran), floats fold flush under hull on road |
| Solar | roof: 5 flexible laminates under walk-on glass; balconies: 6 standard framed 165 W modules — 3.14 kWp nominal / ~3.0 effective |
| Structure | external steel frame (ladder loop) carries all arm/balcony/tow loads — nothing crosses the cabin |
| Tow | stern-first; A-arch pin-locked: sea gantry / extensible drawbar, +100 kg tongue |
| Stern gear | 2 t electric self-recovery winch + anchor on a transom roller |
| Propulsion | 3 × 2 kW flush-intake waterjets (weed-proof), differential steering |
| Aft entry | self-draining cockpit, gasketed storm door, rain porch, ladder to the terrace |
| Cabin | 5.3 × 2.28 m inside, 1.85 m clear headroom |
| Interior | heads with shower, galley (fridge/freezer tower, washer), dinette that sleeps 2, athwartships double; batteries + water under the settees |
| Roof deck | walk-on glass over a ventilated air box: 8 laminated panes on an alu grid, panels bonded underneath — no moving parts |
| Side balconies | walkable too: 480 mm anti-slip walkway beside standard framed modules recessed into an alu ladder frame, 48 mm folded |

## The five configurations

`road` (towed, shutters closed) · `launch` (self-driving on slipway) ·
`harbor` (jack-up: floats under hull carry the boat, keel awash, tires as rolling quay fenders) ·
`cruise` (trimaran, panels out) · `anchor` (lying to the stern anchor,
guardrail up on the sun deck).
Renders: `freecad/shots/`.

## Repository layout

```
freecad/            primary model
  params.py         ALL dimensions, kinematics, checks() asserts
  build_boat.py     geometry builders -> boat_<mode>.FCStd
  view.sh           build + open in FreeCAD GUI (./view.sh [modes])
  capture.py        wipes shots/, re-renders every configuration
  ga_drawing.py     dimensioned general-arrangement sheet
  roof_cards.py     roof-deck spec cards
  interior_plan.py  interior sheet: plan + stowage plan + sections
  shots/            current renders (always regenerated, never stale)
docs/
  glossary.md       shared vocabulary for every part and term
  wheels.md         wheel system: kinematics, drive, BOM + 2026 costs
  propulsion.md     waterjet system: weed strategy, BOM
  structure.md      exoskeleton frame + two-pose tow arch
  aft_entry.md      companionway, porch, ladder, AC, lockers, gates
  roof.md           roof deck: glass sizing, air box, loads, yield
  interior.md       layout, stowage (incl. hidden), services, mass
  images/           dimensioned spec cards for purchasable parts
drafts/             original concept PDF + STL sketch
*.scad, Makefile    legacy OpenSCAD sketch (superseded by freecad/)
```

## Working on it

```sh
./freecad/view.sh                 # open cruise+road+foiling in the GUI
./freecad/view.sh anchor          # any mode by name
~/bin/FreeCAD.AppImage freecad/capture.py    # regenerate all renders
python3 -c "import sys; sys.path.insert(0,'freecad'); import params; params.checks()"
```

`params.py` is the single source of truth; `checks()` recomputes road
legality (StVZO), submergence margins, stability and displacement from
the same numbers the geometry uses — change a dimension and the asserts
tell you what broke.

## Status / open engineering risks

Design study — not build drawings. Known open items: TÜV approval of
the integrated running gear as a trailer; 1.9 t all-in mass budget is
ambitious; arm/shoulder fatigue loads; wheel-arch recesses for
suspension travel not yet modeled; jet hydrodynamics are
first-order estimates; the waterjet intake grids' final position needs
Max's sign-off (moved to float midbody sides + transom, 2026-08-04).
See docs/ for per-system detail.
