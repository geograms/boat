# The Wheels — Mechanism and Drive

Status: design study. Geometry lives in `freecad/params.py` (single
source of truth, asserted by `checks()`); shapes in
`freecad/build_boat.py`; scantlings in `freecad/structure_calc.py`.

## 1. Concept

**Four wheels, on the frame, on screw jacks.** Each one winds straight
down for the road and straight up into a box in the hull bottom for the
water — high enough that the retracted tyre sits **above the
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
| Box, at equal duty | 940 × 250 × 1310 | **800 × 200 × 1160** | **−40 % of volume** |
| Four boxes | 1 232 L | **742 L** | out of the hull |
| Proud of the sole | 690 mm | **540 mm** | −150 mm of furniture |
| Lift needed | 733 mm | **660 mm** | radius + 319 draft + 80 |
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

## 3. The screw leg

A vertical tube bolted to the girder web with a trapezoidal leadscrew
inside it. The screw turns, the inner tube slides, the wheel goes up
or down. That is the whole mechanism.

| | |
|---|---|
| Outer tube | ⌀170 × 10, 6082-T6, bolted to the girder web, z 240 → 1160 |
| Inner tube | ⌀130 × 12, sliding — the slender member, and the one that governs |
| Screw | Tr45, self-locking — it holds at any height with no power and no pin |
| Stroke | **660 mm** |
| Down | axle at z 0, ground at **−261**, keel 261 mm clear |
| Up | axle at z 660 — tyre bottom at **z 399, 80 mm above the 319 mm loaded waterline** |
| Stress | 59.5 MPa against a 104 MPa allowable, **SF 1.75** |

### The tube stands beside the wheel, not over it

The stroke is set by one requirement: **the retracted wheel has to be
out of the water.** 319 mm of loaded draft + 80 mm of clearance + the
261 mm tyre radius = **660 mm of lift**, and that number breaks a
coaxial telescope. Coaxial, the outer tube has to begin above the
retracted tyre (z 921) and still hold 250 mm of the inner when the leg
is fully out — which puts its top at **z 1570**, a 950 mm column
standing in the saloon, four times over.

Offset the tube **380 mm along the boat** and the problem disappears:
the wheel and the tube pass each other instead of colliding. The axle
rides on a short bracket **100 mm** up from the inner tube's foot —
short on purpose. Carry the axle high on a long bracket and the tube's
foot reaches below the tyre's contact patch and drags on the tarmac; at
100 mm the foot stops at z −100, still **161 mm clear of the road**.

```
        ROAD (down)                 WATER (up)

 z1160 ┌───┐                       ┌───┐  inner swallowed whole
       │ ▓ │ outer, fixed          │ ▓▓│
       │ ▓ │                       │ ▓▓│
       │ ▓ │                  z660 │ ▓▓│      ● axle
  z500 │ ▓ │ inner top             │ ▓▓│  ┌───────┐
       │ ▓ │                  z560 └─┬─┘  │ (  o  )│ tyre bottom 399
  z240 └─┬─┘                    ~~~~~~~~~~~~~~~~~~~~~ WL 319
         │ inner
    z0 ──●───(  o  )──  axle           80 mm of air under the tyre
  z-100  └── foot, 161 clear
  -261 ══════════════ road
       ├── 380 ──┤
```

The price is paid in bending, not height: the wheel sits 380 mm out
from the tube axis, so the inner tube carries 7.17 kNm instead of
2.36. ⌀130 × 12 takes it at 59.5 MPa — **SF 1.75**, down from 6.4 but
still ample, and the outer tube lands the load straight into the
girder web it passes through.

Self-locking matters more than it sounds. A leadscrew at this lead
angle cannot be back-driven, so the boat's weight cannot wind the
wheel up, and there is no lock pin to forget on a slipway with the
tide coming in.

It can be worked **afloat**, which the old flip arm never comfortably
could: the leg is happy submerged, there is nothing electrical below
the girder, and the screw does not care about the water.

## 4. The wheel boxes, and what the track buys

Each box is cut through the hull bottom and **lined** — roof plate and
four walls — so the shell stays closed. The opening is flush with the
keel: retracted, nothing stands in the flow and nothing shows.

**The boxes stand 540 mm proud of the sole**, and that is the honest
cost of a dry wheel. 800 long × 200 wide × 1160 tall from the keel,
against a sole at z 620. They sit at the hull sides, at seat height:
the two aft boxes carry the settee bases, the two forward ones are
steps at the dome threshold. There is no way to lift a wheel 660 mm
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
inner half left solid.

It only has to clear the wheel **down**, which is what keeps the cut
small. That imposes one rule on the order of operations:

| | |
|---|---|
| **Launching** | drive in on the wheels with the floats **docked** (road width), float free, **swing the floats out**, *then* wind the wheels up |
| **Recovering** | wheels down first, *then* swing the floats in, then drive out |

Get it backwards and the wheel tries to travel up through a solid
float. The interlock is trivial — the leg controller reads the swing
position and will not run up below 60° of swing.

Cost: **99 kg of buoyancy** across both floats — 616 kg of reserve a
side instead of 715 — against 328 kg if the notch had to clear the
full 660 mm of travel. The lighter float also eases the swing arm,
which drops from 101 MPa to 68 (SF 1.0 → **1.5**).

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
| 4 | Screw leg: ⌀150 tube, Tr40 screw + bronze nut, thrust bearings | 4 | 210 | 840 | local machine shop + <https://www.norelem.de> |
| 5 | 24 V leg gearmotor + limit switches | 4 | 130 | 520 | <https://www.framo-morat.com> |
| 6 | 48 V BLDC motor 3 kW + controller | 2 | 550 | 1 100 | <https://www.goldenmotor.com> · <https://www.kellycontroller.com> |
| 7 | 100:1 planetary reduction | 2 | 320 | 640 | <https://www.apex-dynamics.de> |
| 8 | Marine face seal + housing, ⌀90 shaft | 2 | 140 | 280 | <https://www.volvopenta.com> class · SKF/CR catalogue |
| 9 | Anodes, flush ports, cabling, glands | — | — | 260 | chandlery |
|   | **Total wheels + legs + drive** | | | **≈ 4 400** | |

Down from ≈ €5 600 for the six-wheel hydraulic scheme, mostly because
trailer tyres are a quarter the price of AT car tyres and two orbital
hub motors dropped out.

## 7. Model objects (FreeCAD tree)

`HangarFrame` — girders, legs, drive boxes, drawbar. `HangarTyres` —
the four wheels, dark. `HangarLocks` — bayonet spikes, gold.
`DriveHatchStb/Port` and `HydraulicsStb/Port` — the float's own bay,
which now holds only the **waterjet** pump and motor. Hide `HullShell`
to see the wheels inside their pockets.
