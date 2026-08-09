# The Wheels — Mechanism and Drive

Status: design study. Geometry lives in `freecad/params.py` (single
source of truth, asserted by `checks()`); shapes in
`freecad/build_boat.py`; scantlings in `freecad/structure_calc.py`.

## 1. Concept

**Four wheels, on the frame, on swing arms.** Each one hangs straight
down for the road and swings 180° up into a box in the **T-wing** for
the water — high enough that the retracted tyre sits **310 mm above the
waterline**, dry, out of the flow. Nothing folds, nothing swings, and
nothing that carries the boat is on a hinge.

The wheels belong to the **hangar** — the frame, the two floats, the
drawbar and the running gear, which unbolt from the boat as one unit.
That is what makes the paperwork work: the hangar is the trailer, the
boat is cargo on it. It is also why the drive has to live on the
hangar and not in the boat — detached, the hangar has to run as a
catamaran dinghy under its own power.

```
SECTION AT AN AXLE                      PLAN

  +---------------------------+          stern           bow
  |          cabin            |            |  o        o  |   x 1900
  |    ,---.         ,---.    |  pockets   |              |   x 5200
  |====| o |=========| o |====|            |  o        o  |
  |  girder         girder    |            +--------------+
  +--[FLOAT]---------[FLOAT]--+             track 1820
```

## 2. The wheel

| Item | Value | Why |
|---|---|---|
| Tyre | **155/70 R12C** (⌀522 × 155 mm) | A *trailer* tyre, not a car tyre. C-type casing, built for a load that never comes off it. LI 104 = **900 kg** against the **753 kg** each one carries. Speed rating N = 140 km/h |
| Rim | 12 × 4J, 4 × 100 or 5 × 112 | The commonest braked-trailer fitment in Europe; every trailer dealer stocks it |
| Count | **4**, at x 1 900 and 5 200 | Wheelbase **3 300**, the CG at 3 300 inside it, **91 kg** on the coupling |
| Track | **1 820 mm** | Each box eats the float's inner half; see §4 |
| Mass | 15 kg a wheel, 60 kg the set | Against 88 kg for four 15" car wheels |

### Why it shrank from a 205/70 R15

The car tyre worked, but the **hole** it needed did not. Every
millimetre of tyre diameter is a millimetre of hull cut away twice
over — once to swallow the tyre, once again in lift, because the
retracted wheel has to clear the waterline by its own radius.

| | 205/70 R15 | **155/70 R12C** | |
|---|---|---|---|
| Tyre | 668 × 205 | **522 × 155** | |
| Box, at equal duty | 1 180 × 250 × 700 | **1 000 × 200 × 580** | **−44 % of volume** |
| Four boxes | 826 L | **464 L** | out of the interior |
| Proud of the sole | 707 mm | **560 mm** | −147 mm of furniture |
| Lift needed | 954 mm | **890 mm** | 600 wing + 20 + radius |
| Arm | 477 mm | **445 mm** | half the lift |
| Wheel set | 88 kg | **60 kg** | −28 kg |
| Rated | 950 kg | 900 kg | vs 753 carried |
| Drive torque | 812 Nm | **635 Nm** | −22 %, torque = force × radius |

Less hole, less lining, less structure to work round, less lift, less
weight, and a smaller motor for the same pull. The one thing given up
is load margin — 1.20 against 1.26 — still comfortable, and a C-casing
is designed for exactly this duty where a passenger casing is not.

**It costs ground clearance unless you pay for it, and the design
pays.** The axle winds 74 mm further down than the 15" wheel needed
(`AXLE_DOWN_Z` 74 → 0), which keeps the keel **261 mm** off the road,
as before.

## 3. The swing arm

The wheel is on the **end of a 445 mm arm**, pivoted at z 445 off the
girder web. Hanging straight down the axle is at z 0 and the tyre is on
the road; swung 180° it is at z 890 with the tyre stowed in the wing.

**890 mm of travel out of a mechanism 445 mm long, and nothing stands
above the girder.**

| | |
|---|---|
| Arm | ⌀150 × 12, 6082-T6, 445 mm pivot to axle |
| Pivot | z 445, on a bracket off the girder web, ⌀190 boss |
| Sweep | 180° |
| Down | axle z 0, ground at **−261**, keel 261 mm clear |
| Up | axle z 890 — tyre bottom at **z 629**, in the wing, 310 mm above the loaded waterline |
| Actuator | Tr45 leadscrew, frame lug to a lug at 0.6 R along the arm, self-locking |
| Stress | 30.6 MPa against a 104 MPa allowable, **SF 3.4** |
| Mass | 22 kg a station — arm, pivot, bearings, actuator |

### Why not a straight jack

A straight jack needs a **column at least as long as its stroke**.
890 mm of lift therefore means a 1 140 mm tube standing off each
girder — four of them, ~960 mm proud, with the wheel dangling off a
380 mm bracket beside the tube because a coaxial telescope of that
stroke would reach z 1 800. That was drawn, rendered, and it looked
like what it was: a forest of poles with the wheels not even on them.

The arm has none of that. It is shorter than its own travel, the
wheel is *on* it, and it disappears into the wing with the tyre.

```
   ROAD                        WATER

  ──┐ pivot z 445             ──┐ pivot z 445
    │                            └───● axle z 890
    │ 445 arm                    ( o ) tyre 629..1151, in the WING
    ● axle z 0             ═══════════ wing underside z 600
  ( o )                    ~~~~~~~~~~~ WL 319
 ══════════ road z −261     nothing above the girder
```

### Over-centre — the screw does not hold the boat up

Hanging straight down, the wheel's load line runs **through the
pivot** into a hard stop. The road load goes tyre → arm → pivot →
girder as pure compression; the actuator carries almost none of it and
only has to swing the arm. That is why the arm is a strut in the
scantlings and not a cantilever: what sizes it is a **kerb strike** —
0.6 g sideways at the contact patch on the full 445 mm — not the
boat's weight.

Self-locking still matters for the stowed position, and the leadscrew
gives it: the arm parks anywhere with no power and no pin. The whole
mechanism is happy submerged; there is nothing electrical below the
girder.

## 4. The wheel boxes, and what the track buys

Each box is cut through the **wing underside at z 600** — not through
the keel — and **lined**, roof plate and four walls, so the shell
stays closed. The keel is left an unbroken bottom, and the opening
sits **281 mm above the waterline** inside the float recess: nothing
in the flow, nothing visible, nothing wet.

That is forced, not chosen. At y ±910 the hull below z 600 does not
exist — the T narrows to a 1 560 mm stem there and the rest is the
float's recess. An earlier cut of this was made at the keel and
produced exactly what it should have: four lining plates floating in
open air with no hull to join.

**The boxes stand 560 mm proud of the sole**, and that is the honest
cost. 1 000 long × 200 wide, from the wing underside at z 600 up
to z 1180 — long because the tyre comes in on an **arc**: crossing
z 600 the axle is 417 mm out from the pivot and the tyre reaches 678,
while stowed it sits back at ±261, against a sole at z 620. They sit at the hull sides, at seat height:
the two aft boxes carry the settee bases, the two forward ones are
steps at the dome threshold. There is no way to lift a wheel 890 mm
and leave the interior untouched — the alternative was to leave the
tyre 280 mm under water in an open well for the life of the boat.

Each box straddles the stem face and eats the float's **inner
half** (y 810 → 1 010, stopping exactly at the float's midline). That
is what puts the wheel centreline at y ±910:

| Wheel at | Track | Tip | Rollover |
|---|---|---|---|
| inboard of the girders | 1 300 | 24.9° | 0.46 g |
| **half into the float** | **1 820** | **33.0°** | **0.65 g** |
| full float depth | 2 280 | 39.2° | 0.81 g |

**+8.1° and +41 % of margin** for half a float's width. A tall van is
≈0.5 g and a loaded truck 0.35–0.40 g, so this sits in normal trailer
territory under a boat 2.8 m tall. The float keeps its **outboard**
half solid — the skin that meets the water is untouched — and the
narrow 200 mm box is what allowed the extra 25 mm a side without
crossing the midline.

## 4b. The notch in the float, and the launch sequence

Docked on the road, the float and the wheel-down tyre want the same
space: the tyre's inner flank runs through the float's inner-lower
corner. So the corner is **cut away** at each wheel station — 800 long
× 230 wide × 320 deep from the float bottom, the top 220 mm of the
inner half left solid — plus a **240 mm full-height slot** at the wheel
station itself, because the arm and its pivot live in the recess up to
z 445 and the float has to dock past them.

It only has to clear the wheel **down**, which is what keeps the cut
small. That imposes one rule on the order of operations:

| | |
|---|---|
| **Launching** | drive in on the wheels with the floats **docked** (road width), float free, **swing the floats out**, *then* wind the wheels up |
| **Recovering** | wheels down first, *then* swing the floats in, then drive out |

Get it backwards and the wheel tries to travel up through a solid
float. The interlock is trivial — the leg controller reads the swing
position and will not run up below 60° of swing.

Cost: **144 kg of buoyancy per float** — 564 kg of reserve a side
instead of 708 — against roughly double that if the notch had to clear
the whole 890 mm of travel. The lighter float also eases the swing
arm, which drops from 101 MPa to 68 (SF 1.0 → **1.5**).

## 4c. The frame is out of the water

The girders ran at **z 140…380** with the loaded waterline at **319** —
the structure that carries the whole boat spent every floating hour
half submerged, in salt, in a weldment that cannot be slipped for
inspection. There was room above it the whole time.

| | was | **now** |
|---|---|---|
| Girders | z 140…380, hanging under the hull | **z 600…800, in a lined channel in the wing** |
| Clearance | −179 mm (submerged) | **+281 mm above the waterline** |
| Versus the docked float | overlapped it, unmodelled | **clears it** — float top is 530 |
| Extender sliders | z 90…430, centred on the waterline | **z 380…600** |
| Clearance | −229 mm (submerged) | **+57 mm** |

The girder channel is cut into the wing underside and lined, open at
the bottom and at the stern, so the hangar still slides on from
astern. Nothing about the wheels moved: the arm pivot stays at z 445
on a bracket dropping off the girder, the axle still travels 0 → 890,
and the wing box is unchanged.

**And the swing wing had to go entirely.** See
[floater.md](floater.md) §5: a horizontal swing needs a plane clear of
the float at every angle, and this boat has 70 mm of it. The float now
slides straight out on telescopic beams that live inside the stem.

## 5. Drive

Requirement: electric, ≤ 6 km/h (the German rule that keeps the rig
out of full type approval on the slipway), and it must survive being
submerged for long periods.

**One driven wheel per side — the forward one.** Traction on four
wheels is not needed at walking pace; two driven wheels with most of
the weight over them is enough to climb a 15 % slipway.

```
48 V house bank ──► dry box bolted to the girder web, forward station:
      3 kW BLDC motor ─► 100:1 planetary ─► ONE stub shaft
        ─► marine face seal ─► forward wheel        635 Nm
```

**Why not a submerged hub motor.** IP68 is a *static* test. A rotating
seal under load, in salt, with grit, is a different problem, and hub
motors fail at exactly that interface. This design has **one
serviceable face seal per side** and nothing else rotating in the
water. The seal changes from outside without opening the box.

**Why on the girder and not in the float.** The float swings. Putting
the drive there meant a shaft or a hose crossing a moving joint, and
the wheels are no longer on the float anyway. On the girder the motor
sits a few hundred millimetres from the wheel it drives, on the same
rigid weldment, and it detaches with the hangar.

- **Torque check**: 3 100 kg on a 15 % slipway with rolling resistance
  ≈ 5.5 kN of tractive force → ~1 435 Nm total, 718 Nm per driven
  wheel at the tyre. 635 Nm at 3 kW / 100:1 covers a 6 km/h climb with
  the load transfer aft on the ramp; on a 10 % ramp it is comfortable.
- **Power check**: ~1.2 kW to hold 6 km/h on the flat, ~2.6 kW peak on
  the ramp, per side.
- **Control**: one controller per side gives forward, reverse and a
  speed differential — skid steering at walking pace. No steered axle
  is needed below 6 km/h.
- **Corrosion**: zinc anode at each hub, a freshwater flush port, and
  the box drains downward.

## 6. Main pieces, 2026 cost estimate

Prices are 2026 street-price estimates (EUR, excl. VAT variation);
URLs are representative product pages to see the item class.

| # | Item | Qty | Est. € each | Est. € total | Where to see it |
|---|---|---|---|---|---|
| 1 | Tyre 155/70 R12C 104/102N (Kenda K399, Security TR603) | 4 + 1 spare | 45 | 225 | <https://www.kendatire.com> · <https://www.reifen.com> |
| 2 | Steel rim 12×4J, 4×100 | 5 | 35 | 175 | <https://www.anhaengerteile.de> |
| 3 | Braked trailer hub + stub axle, 900 kg | 4 | 90 | 360 | <https://www.knott.de> · <https://www.alko-tech.com> |
| 4 | Swing arm: ⌀150 tube, pivot boss, bearings, hard stop | 4 | 190 | 760 | local machine shop + <https://www.skf.com> |
| 5 | Tr45 leadscrew actuator, 24 V, self-locking, with limit switches | 4 | 240 | 960 | <https://www.framo-morat.com> |
| 6 | 48 V BLDC motor 3 kW + controller | 2 | 550 | 1 100 | <https://www.goldenmotor.com> · <https://www.kellycontroller.com> |
| 7 | 100:1 planetary reduction | 2 | 320 | 640 | <https://www.apex-dynamics.de> |
| 8 | Marine face seal + housing, ⌀90 shaft | 2 | 140 | 280 | <https://www.volvopenta.com> class · SKF/CR catalogue |
| 9 | Anodes, flush ports, cabling, glands | — | — | 260 | chandlery |
|   | **Total wheels + legs + drive** | | | **≈ 4 400** | |

Down from ≈ €5 600 for the six-wheel hydraulic scheme, mostly because
trailer tyres are a quarter the price of AT car tyres and two orbital
hub motors dropped out.

## 7. Model objects (FreeCAD tree)

`HangarFrame` — girders, swing arms, actuators, drive boxes, drawbar. `HangarTyres` —
the four wheels, dark. `HangarLocks` — bayonet spikes, gold.
`DriveHatchStb/Port` and `HydraulicsStb/Port` — the float's own bay,
which now holds only the **waterjet** pump and motor. Hide `HullShell`
to see the wheels inside their pockets.
