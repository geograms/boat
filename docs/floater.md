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
| Body | foam-core GRP sandwich, `float_shell` schedule (PET60 15 mm, 800/600) | — |
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

## 4. The float has no running gear

Nothing rolls, folds or drives on the float any more. **The wheels are
on the frame** and jack straight up into pockets in the hull; the float
is a closed buoyancy body whose only job is to swing out for stability.

That is worth stating because it undoes three earlier problems at once:

- **Almost no slots.** The float keeps a notch at each wheel station
  so the wheel can go DOWN past it, but nothing passes through any
  more: **564 kg** each, against 559 when the wheels lived inside it.
- **The load path is direct.** Hull → girder → leg → wheel, instead of
  hull → girder → swing arm → float → wheel. The boat's weight no
  longer passes through the part that moves.
- **Nothing that carries the boat is on a hinge.**

### The wheels, on the frame

| | |
|---|---|
| Wheel | **155/70 R12C** trailer tyre, 522 × 155, rated 900 kg against 753 carried |
| Stations | x 1 900 and 5 200 — wheelbase **3 300**, CG 3 300 inside it, 91 kg on the coupling |
| Track | **1 820 mm**: each pocket eats the float's **inner half** (y 810 → 1 010) and the wheel centres on y ±910 |
| Leg | fixed ⌀170 outer on the girder, sliding ⌀130 inner, Tr45 leadscrew, self-locking, **890 mm of stroke**, tube offset 380 mm so the wheel passes it |
| Retracted | tyre bottom at **z 629 — 310 mm above the 319 mm loaded waterline**, wholly inside an 800 × 200 × 580 box in the **T-wing**, which opens at z 600 into the float recess. The keel is never cut. Out of the water, out of the flow, out of sight |

**Why the pocket takes half the float.** Keeping the wheels wholly
inboard of the girders would give a 1 300 mm track — 24.9° of tip and a
**0.46 g** rollover threshold, marginal under a boat 2.8 m tall. Moving
them out to y ±910 gives:

| Wheel at | Track | Tip | Rollover |
|---|---|---|---|
| inboard of the girders | 1 300 | 24.9° | 0.46 g |
| **half into the float** | **1 820** | **33.0°** | **0.65 g** |
| full float depth | 2 280 | 39.2° | 0.81 g |

**+8.1° and +41 % of rollover margin** for half a float's width — a tall
van is ≈0.5 g and a loaded truck 0.35–0.40 g, so this sits in normal
trailer territory. The float keeps its **outboard** half solid, so the
skin that meets the water is untouched.

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

## 7b. Mass — the 300 kg target and why it does not close

Asked for a hangar under 300 kg. Every lever was pulled and the honest
floor is **609 kg**:

| Item | kg | What was done |
|---|---|---|
| Float shells | 129 | PVC80 18 mm → **PET60 15 mm, 800/600 skins** |
| Screw legs | 76 | four, on the frame |
| Wheels + hubs | 60 | 4 x 155/70 R12C on steel |
| 4 wheels | 66 | 185 R14 C trailer tyres, two per float |
| U-girder | 73 | **110 × 240 × 6** — with only two wheel stations the 3.1 m span makes **stiffness** the governing case, not stress |
| Swing arms | 57 | 340 mm deep trusses, 70 × 70 × 4 chords |
| Drive | 86 | **one** 6 kW motor in the hull, cross shaft, 2 driven wheels |
| Bight | 25 | |
| Dock locks | 30 | |

| Cross tie, knees, dinghy fit-out | **0** | **deleted** |
| **Total** | **531** | was 1 003 |

**The arms were the honest mistake.** 127 kg for four beams came from
two errors compounding: putting **100 % of a float's buoyancy on one
arm** when the float is a stiff beam pinned at two of them (immersion
centroid midway; 70/30 even pitched hard bow-down), and then carrying
that moment in a **box wall in bending**. A truss carries the same
moment **axially in its chords**: 22.1 kNm over a 300 mm depth is
73.6 kN per chord, 82 MPa in a 60 × 60 × 4 — **155 kg → 48 kg**.

**300 kg is below the physical floor for this boat.** The reason is that
almost every item scales with what it carries: a 3 153 kg combination
needs six wheels, and the beams that spread that load over them are
what they are. For scale, a **commercial braked boat trailer for 3 t
weighs 400–600 kg empty** — and it has no floats and no swing gear.
At 448 kg this one is already inside that band while doing more.

The hangar reaches 300 kg only if the **boat** does its share: at
roughly 1 800 kg loaded it needs four wheels instead of six and
proportionally lighter beams, which lands near the target. The lever is
in [weight.md](weight.md), not here.

## 7c. The drive — one motor, and where it lives

**One 6 kW motor drives the whole machine**, and it never gets wet.

```
SECTION AT THE DRIVE STATION (x 2000, the pair nearest the coupling)

        motor + 100:1 reduction, DRY in the stem
                    ┌────────┐
                    │  6 kW  │
        ════════════╧═══╤════╧════════════   cross shaft, in the
    dog clutch ══╗      │      ╔══ dog clutch   keel channel
                 ║  hull stem  ║
      ┌──────────╨──┐       ┌──╨──────────┐
      │ stub shaft  │       │ stub shaft  │   one face seal each
      │   chain ↓   │       │   ↓ chain   │
      │  [ WHEEL ]  │       │  [ WHEEL ]  │
      └── float ────┘       └──── float ──┘
```

| | |
|---|---|
| Motor | **one**, 6 kW, 48 V, mounted **dry in the hull's stem** above the keel channel — the driest, most accessible place on the boat |
| Transmission | 100:1 reduction → a **transverse shaft in the keel channel** → a **dog clutch at each stem face** |
| Coupling | the clutches engage the floats' stub shafts **as the floats dock**; undocked, the floats are purely mechanical |
| In the float | a stub shaft through **one marine face seal** and a chain case up to the driven wheel. **No electrics in the float at all** |
| Driven | the pair **nearest the coupling** (x 2 000). The forward pair free-wheels |
| Output | **1 623 Nm** at the two driven wheels — a **15 %** ramp at 3 km/h |
| Mass | 86 kg: motor and reduction 38, cross shaft and clutches 18, two chain drives 18, controls 12 |

**Why the motor is not in the wheel.** IP68 is a *static* test — the unit
is dipped, not run. A rotating seal under load can fail within minutes
on an IP68-rated motor, which is the standard warning from marine motor
suppliers. Putting the motor in the hull leaves **one rotating seal per
driven wheel**, on a stub shaft, serviceable from outside without
opening anything. It is the saildrive pattern, and it is why one motor
is possible at all: a motor per wheel has to live where the wheel is.

**Why only two wheels are driven.** Traction is needed on a ramp, and on
a ramp the pull is at the coupling. The pair nearest it does the work;
the other pair rolls. That halves the transmission and costs nothing —
1 623 Nm on two wheels still climbs 15 %.

**What does not work: lifting a pair on the road.** A coupling carries
about 100 kg of nose load, so if the front pair lifted, each remaining
wheel would carry **1 596 kg** — above the heaviest 15-inch commercial
tyre (≈1 250 kg). **All four stay down on the road.** The flip arms can
still lift a pair for manoeuvring or maintenance, just not under tow.

## 8. Scantlings — calculated, not guessed

`freecad/structure_calc.py` proves the three members that carry the
boat. 6082-T6 aluminium, 260 MPa proof, **0.60 knockdown for the weld
HAZ** and 1.5 on yield → **104 MPa allowable**. Load cases: ×2.5 road
shock on a trailer axle, ×3.0 wave slam on an outrigger.

| Member | Case | Moment | Stress | SF | Section |
|---|---|---|---|---|---|
| U-girder | 3 292 kg × 2.5 over a 3.1 m simple span | 11.0 kNm | 47 MPa | **2.2** (deflection 8.1 of 12.4 mm governs) | 110 × 240 × 6 box |
| Swing arm | 70 % of one float's **564 kg** × 3.0, 1 918 mm lever | 22.3 kNm | 62 MPa | **1.7** | 340 deep truss, 70 × 70 × 4 chords |
| Screw leg | a quarter of the boat × 2.5, 380 mm forward of the tube axis | 7.2 kNm | 60 MPa | **1.8** | ⌀130 × 12 sliding inner tube |

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
