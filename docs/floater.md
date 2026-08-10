# The Floater — Specification and Placement

Status: **the contract for the float**. Every feature the float must
contain, what it must do, and where it lives. Geometry in
`build_float()` (`freecad/build_boat.py`), parameters in
`freecad/params.py`. When the float changes, this list is what the
change is checked against — nothing on it may be silently dropped.

## 1. What the floater is

A slim outrigger hull, **5 400 × 460 × 700 mm**, one per side, that
does four jobs:

1. **Stabiliser** — extended 0.7 m out on the sliders, it
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
| Leg | **swing arm**: ⌀150 × 12, 445 mm, pivot at z 445 on the girder web, 180° = **890 mm of lift**, Tr45 leadscrew actuator, self-locking. Nothing stands above the girder |
| Retracted | tyre bottom at **z 629 — 310 mm above the 319 mm loaded waterline**, wholly inside a 1 000 × 200 × 580 box in the **T-wing**, which opens at z 600 into the float recess. The keel is never cut. Out of the water, out of the flow, out of sight |

**Why the pocket takes half the float.** Keeping the wheels wholly
inboard of the girders would give a 1 300 mm track — 24.9° of tip and a
**0.46 g** rollover threshold, marginal under a boat 2.8 m tall. Moving
them out to y ±910 gives:

| Wheel at | Track | Tip | Rollover |
|---|---|---|---|
| inboard of the girders | 1 300 | 27.7° | 0.52 g |
| **half into the float** | **1 820** | **36.3°** | **0.73 g** |
| full float depth | 2 280 | 42.6° | 0.92 g |

**+11.4° and +59 % of rollover margin** for half a float's width — a tall
van is ≈0.5 g and a loaded truck 0.35–0.40 g, so this sits in normal
trailer territory. The float keeps its **outboard** half solid, so the
skin that meets the water is untouched.

## 5. Extension — the V arms

**Two arms per side**, each on a vertical pin at the frame and a
vertical pin at the float, **equal length and parallel to each other**:
a parallelogram. So the float **translates** — it never yaws, it stays
parallel to the hull at every angle. That is the whole point. A float
that toes in or out fights the boat.

Seen from above, the port and starboard sets mirror and the four arms
read as a **V**. That is not decoration — the arms sweep **aft** as
they open, so the water's push on the float drives them **further
open** and holds them against the stop. A rope pulls the float forward
to shut the V, and a latch holds it under the hull for the road.

**Nothing screws, nothing jacks, nothing telescopes.**

| Item | Spec |
|---|---|
| Arms | **2 per side**, pins at x 2 700 and 4 600 |
| Length | **900 mm** pin to pin |
| Section | **160 × 220 × 5** box, 6082-T6 |
| Open | **59°** → float **771 mm out**, 436 mm aft, parallel |
| Band | z **380 … 600** — 57 mm over the loaded waterline, top flush under the wing |
| Docked | each arm lies in a **120 × 160 groove** in the float's inner face |
| Opening | the water does it |
| Closing | a rope to a block on the frame's forward tie |
| Holding | a hard stop on the girder, and a latch for the road |
| Load | 70 % of the float's 893 kg displacement × 3.0 slam on the arm's own length → 16.6 kNm, 70 MPa, **SF 1.50** |
| Mass | **10.3 kg the arm, 55 kg the whole system** both sides |

### Why the arm is short

The arm's own length is the lever, so mass climbs with length twice
over — once in the section it needs, once in the span it spans. 900 mm
is what a 10 kg arm buys; the open angle then does the rest of the
work, because 900 × sin 59° = 771 mm of stance out of a 900 mm part.

Righting **SF 2.2** against the 1.9 required.

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

- **Buoyancy**: ≥ 500 kg of float displacement per side after the wheel
  notches (asserted in `checks()`); the pair plus bight floats the
  dinghy with two crew and ≥ 200 mm freeboard.
- **Righting**: the float pair *is* the boat's stability — the stem
  alone has GM −0.42 m. Extended, peak righting is **14.5 kNm at 13°**
  against a Beaufort 6 gust of 4.0, SF 3.6 asserted ≥ 1.9. The curve
  saturates at 13° because the float has 155 mm of freeboard.
  See [stability.md](stability.md).
- **Road**: carries the loaded boat on six wheels; bays put the axle
  inside the envelope so the rig rides low.
- **Watertight**: any one compartment flooded, the float still floats
  level enough to limp home.
- **Detachable**: docks and undocks on the water, fork-and-lock, with
  the crew in the cockpit.

## 7b. Mass — the 300 kg target, and where the 589 actually goes

Asked for a hangar under 300 kg. Every line below is **computed** —
from measured areas times a laminate schedule, or from a section times
a length — not estimated:

| Item | kg | Note |
|---|---|---|
| Float shells (GRP) | 121 | 5 400 × 460 × 700 each, PET60 15 mm core, 800/600 skins |
| U-girders | 93 | 110 × 200 × 5 alu, 5 740 long — they have to reach both wheel stations |
| Wheel swing arms | 88 | four ⌀150 × 12 arms, pivots, actuators |
| Drive + seals | 80 | 2 × 3 kW, 100:1, one face seal a side |
| Wheels + hubs | 60 | 4 × 155/70 R12C on steel |
| **V arms + ropes** | **55** | **was 209 as a telescope** |
| Bight, forward tie, drawbar | 63 | two transverse ties + the demountable A-frame |
| Locks and sundry | 30 | |
| **Total** | **589** | was 1 003 |

**300 kg is below the floor, and it is worth being precise about why.**
A braked commercial boat trailer for 3 t weighs 400–600 kg empty, and
it has no floats, no extenders, no retracting wheels and no dinghy
duty. Of the 589 here, **129 kg is the two float hulls** — those are
boat, not trailer. The metalwork is 281 kg and the drive 80.

The remaining levers, in order of size: the girders (93 kg) are sized
by road deflection over a 5.7 m span and would come down if the
wheelbase shortened; the wheel swing arms (88 kg) are sized by a kerb
strike at SF 3.4 and have margin to give.

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
| V arm | 70 % of one float's **893 kg** × 3.0, on the arm's own 900 mm | 16.6 kNm | 70 MPa | **1.5** | 160 × 220 × 5 box, two a side |
| Swing arm (gear) | kerb strike, 0.6 g at the contact patch on the 445 mm arm | 5.1 kNm | 31 MPa | **3.4** | ⌀150 × 12 arm |

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
