# Boat-Home — Road-Towable Solar Trimaran (Design Study)

A 7.2 m Dutch-barge style boat-home that is **its own trailer**: the
stabilizer floats fold underneath the hull and carry six driven wheels,
so one Mercedes-Viano-class car tows it on German roads, and it drives
itself in and out of the water on slipways. Solar-electric, weed-proof
waterjets, retractable bow hydrofoil, pop-top roof deck.

Parametric CAD in FreeCAD (Python-scripted); every legal and
hydrostatic constraint is asserted in code.

## Key numbers

| | |
|---|---|
| Hull | 7.20 × 2.50 m Dutch barge, WL draft 260 mm, ~2.0 t |
| Road envelope | 2 525 mm wide × 2.80 m tall (limits 2 550 / 4 000) |
| Wheels | 6 × 205/70 R15 all-terrain, in-float hydraulic drive |
| Floats | 6.2 m, ~1.55 t reserve each (82 %), righting SF ≈ 4.5 |
| Water beam | 5.06 m (trimaran), floats fold flush under hull on road |
| Solar | 12 flexible laminates (1700×1130), ~5.2 kWp; balcony panels bifacial |
| Structure | external steel exoskeleton carries all arm/balcony/tow loads |
| Tow | A-arch, pin-locked: bow collision bar (sea) / extensible drawbar (land) |
| Propulsion | 3 × 2 kW flush-intake waterjets (weed-proof), differential steering |
| Cabin | 5.3 × 2.4 m, 1.8 m headroom; pop-top roof = chillout deck at anchor |

## The five configurations

`road` (towed, shutters closed) · `launch` (self-driving on slipway) ·
`harbor` (jack-up: floats under hull carry the boat, keel awash, tires as rolling quay fenders) ·
`cruise` (trimaran, panels out) · `anchor` (roof raised).
Renders: `freecad/shots/configs.png`.

## Repository layout

```
freecad/            primary model
  params.py         ALL dimensions, kinematics, checks() asserts
  build_boat.py     geometry builders -> boat_<mode>.FCStd
  view.sh           build + open in FreeCAD GUI (./view.sh [modes])
  capture.py        wipes shots/, re-renders every configuration
  shots/            current renders (always regenerated, never stale)
docs/
  glossary.md       shared vocabulary for every part and term
  wheels.md         wheel system: kinematics, drive, BOM + 2026 costs
  propulsion.md     waterjet system: weed strategy, BOM
  structure.md      exoskeleton frame + two-pose tow arch
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
