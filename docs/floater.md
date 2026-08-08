# The Floater — Specification and Placement

Status: **the contract for the float**. Every feature the float must
contain, what it must do, and where it lives. Geometry in
`build_float()` (`freecad/build_boat.py`), parameters in
`freecad/params.py`. When the float changes, this list is what the
change is checked against — nothing on it may be silently dropped.

## 1. What the floater is

A slim outrigger hull, **6 000 × 400 × 460 mm**, one per side, that
does four jobs:

1. **Stabiliser** — extended 1.65 m out on the pantograph trusses, it
   is the boat's righting moment in waves.
2. **Trailer** — docked in the hull's T-notch, its three wheels carry
   the boat on the road.
3. **Dinghy** — undocked as a pair joined by the bight, it is a powered
   catamaran tender.
4. **Machinery pod** — it carries its own waterjet, battery and solar,
   so it works detached from the boat.

Frame convention below: **float-local**, x along the float (0 aft,
6 000 at the nose), y across (+ outboard), z up (0 at the float's mid
height; bottom −230, deck +230).

## 2. Hull

| Item | Spec | Where |
|---|---|---|
| Body | foam-core GRP sandwich, `float_shell` schedule (PVC80 core) | — |
| Nose | **spoon head**: bottom curves up from x ≈ 4 500 to the tip — no slab face to the water | forward quarter |
| Tail | flat transom carrying the jet nozzle | x 0 |
| Bottom | flat, **flush with the hull keel plane** when docked | z −230 |
| Compartments | **three watertight cells**: aft (jet pump), middle (batteries, under the hatch), forward (buoyancy/stowage) | bulkheads at x ≈ 1 900 and 4 200 |
| Rub strake | half-round, full length of the outer face at the waterline | y +200, z ≈ +40 |
| Drain plugs | one per compartment, bottom aft corner | z −230 |

## 3. Propulsion — the U-intake waterjet

The pump is **enclosed**; nothing rotating ever touches open water.
Water enters through a **U of perforated plates wrapped around the
bottom of the machinery bay** — port cheek, floor, starboard cheek —
so the intake draws from all directions and keeps feeding when heeled
or in weed:

| Item | Spec | Where |
|---|---|---|
| Pump | 2 kW enclosed cartridge | machinery bay, x ≈ 2 675 (bay centre `MOTOR_BAY_DX`) |
| Intake floor plate | perforated, ≈ 560 × 290 | bottom face, directly under the pump |
| Intake cheeks | perforated, ≈ 560 × 130, port and starboard | both side faces, bottom edge, same x as the pump |
| Hole size | 14 mm — weed drifts past, fingers stay out | all three plates |
| Nozzle | cone to ⌀ jet outlet, on the transom, low | tail, z ≈ −120 |
| Steering | differential thrust between the two floats — no rudder | — |

**Rule: the intake and the pump live at the same x.** Water travels
centimetres, not a duct.

## 4. Wheels — manual flip arms

| Item | Spec | Where |
|---|---|---|
| Wheels | 3 × 205/70 R15 AT, hub motors | bays at x 1 800 / 3 550 / 5 300 |
| Bays | **wells, not trenches**: open below, deck bridge on top with a 680 × 230 slot for the wheel to stand through — the profile stays closed. Roughly half the wheel is inside the bay on the road | 730 × 300 below, slot above |
| Flip arm | curved, bulging **outboard**; 180° about a tube spanning the bay | tube on the bay centreline, z +230 |
| Pins | spring pin at each end of the swing — **manual, no electrics** | tube ends |
| Sequence | flip only while **extended** (the T-wing forbids it docked); wheels down before the trusses retract | — |
| Road pose | wheel top sits in the bay, bottom **310 mm proud** of the float — that protrusion IS the ground clearance, and it cannot be tucked away without grounding the hull | ground at −320 |

## 5. Docking and extension

| Item | Spec | Where |
|---|---|---|
| Fork guides | two internal guide grooves riding the hull's tapered spike rails — inside the laminate, no external hardware | inboard face, z ±150 |
| Lock | electric bayonet keeper engaging the rail root; limit-switched | forward end of each channel |
| Truss fittings | pinned lugs for the pantograph trusses and the deployed **lock struts** | inboard face, x 2 675 and 4 425 |
| Docked position | outer face recessed 40 mm behind the hull's lip, top 20 mm under it | global y 1 210, top z 450 |
| Extended position | 1.65 m of clear water to the hull | electric, self-locking anywhere |

## 6. Energy and deck

| Item | Spec | Where |
|---|---|---|
| Battery | 2 × 12 V 100 Ah (motorcycle class), **forward compartment** — trims the dinghy against crew aft | x ≈ 4 400, under deck |
| Solar | 2 × 100 W flexible strips, flush | deck, either side of the hatch |
| Charging | from its own panels detached; from the ship's 48 V bus through the dock connector when coupled | — |
| Hatch | gasketed, over the battery/machinery access | deck, x ≈ 2 675 |
| Cleats | pop-up, one forward one aft — dinghy lines, flush when unused | deck ends |
| Nav light socket | plug-in pole for the dinghy role | nose deck |

## 7. What the floater must PERFORM

- **Buoyancy**: ≥ 300 kg net reserve per float after the wheel bays
  (asserted in `checks()`); the pair plus bight floats the dinghy with
  two crew and ≥ 200 mm freeboard.
- **Righting**: at full extension the pair delivers the boat's
  stability margin (SF ≥ 1.7 asserted; the compact stance is a chosen
  trade).
- **Road**: carries the loaded boat on six wheels; bays put the axle
  inside the envelope so the rig rides low.
- **Watertight**: any one compartment flooded, the float still floats
  level enough to limp home.
- **Detachable**: docks and undocks on the water, fork-and-lock, with
  the crew in the cockpit.

## 8. Scantlings — calculated, not guessed

`freecad/structure_calc.py` proves the three members that carry the
boat. 6082-T6 aluminium, 260 MPa proof, **0.60 knockdown for the weld
HAZ** and 1.5 on yield → **104 MPa allowable**. Load cases: ×2.5 road
shock on a trailer axle, ×3.0 wave slam on an outrigger.

| Member | Case | Moment | Stress | SF | Section |
|---|---|---|---|---|---|
| U-girder | 3 599 kg × 2.5 over 3 wheel stations, 1.7 m bay | 2.0 kNm | 7 MPa | **14.8** | 140 × 200 × 8 box |
| Swing arm | one float's full 559 kg buoyancy × 3.0 on **one** arm, 1 918 mm lever | 31.6 kNm | 66 MPa | **1.6** | 165 × 230 × 10 box |
| Flip-arm tube | one wheel's share × 2.5 on the 516 mm arm | 7.0 kNm | 70 MPa | **1.5** | ⌀120 × 12 tube |

Two results changed the design:

- **The ⌀70 flip tube failed at 324 MPa** — three times over. It is now
  ⌀120 × 12.
- **The U-girder was drawn at 190 × 300 × 10 and came out at SF 39** —
  294 kg of aluminium doing a 2 kNm job. Cut to 140 × 200 × 8: still
  SF 15, and 132 kg lighter.

The swing arm at SF 1.6 is the tightest member and the one to watch: it
carries a whole float's buoyancy on a single 1.9 m cantilever, which is
the honest worst case (float pitching on a crest with the other arm
unloaded).

## 9. Open engineering (not yet modelled)

- Compartment bulkheads and the flooded-cell stability case.
- The dock connector (48 V + signals) — wet-mate, location TBD at the
  forward channel end.
- Bay liners: the wheel bays are open to water; the battery and pump
  cells must be sealed boxes within the hull, not just "inside".
- Truss lug local reinforcement (doublers in the laminate).
