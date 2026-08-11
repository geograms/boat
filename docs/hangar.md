# The T-Hull and the Nesting Floats

Status: design study. Geometry in `freecad/params.py` (`STEM_HW`,
`T_STEP_Z`, `POD_DOCKED`, `POD_SEA`, `arm_points()`), shapes in
`build_boat.py`, limits asserted in `checks()`.

## 1. The T

Aft of the bow the hull's underwater body narrows to a central **stem**
(the stroke of the T); the deck and cabin keep the full 2 500 mm beam
(the bar), and so does the **bow — the head of the ship is full width
to the waterline** for stability forward. The two notches beside the
stem are where the floats live: **same level as the hull, bottoms
flush**, so the docked boat is one clean barge body.

```
FRONT VIEW                DOCKED                    EXTENDED (sea)

 ┌───────────────┐   ┌───────────────┐         ┌───────────────┐
 │     cabin     │   │     cabin     │         │     cabin     │
 ╞═══════════════╡   ╞═══════════════╡         ╞═══════════════╡
 │   ┌───────┐   │   │╔══╗┌────┐╔══╗│  ~WL~   │    ┌────┐     │ ~WL~
 │   │ stem  │   │   │║FL║│stem│║FL║│     ╔══╗│    │stem│    │╔══╗
 └───┴───────┴───┘   └╨──╨┴────┴╨──╨┘     ╚══╝└────┴────┴────┘╚══╝
                      flat bottom flush    sliders push them 0.7 m out
```

| | |
|---|---|
| Stem | **1 560 mm** beam below z 600 — floats the boat alone, and swallows the retracted beams |
| Floats | **5 400 × 460 × 700**; bottom 110 mm below the keel, top under the wing; noses protected by 1 200 mm of solid bow |
| Docked | outer faces flush at 2 500; draft 313 mm loaded |
| Extended | **771 mm** out on the V arms — GM 1.20 → 4.59 m, peak righting 3.8 → 14.8 kNm |
| Dinghy | both floats + bight: 6.1 m beam, 216 mm freeboard with two aboard |

## 2. Docking — screw the frame down, afloat

No slipway, no winching against buoyancy. **A rotating electric screw
sits in each V arm, between the float and the frame.** The floats stay
where the water puts them; the screws drive the **frame** up and down
relative to them.

| Setting | Frame drop | What it is for |
|---|---|---|
| up | 0 | towing, and carrying the boat |
| **dock** | **334 mm** | channel and girders line up exactly |
| under | 700 mm | frame **174 mm below the water** — it passes under a floating boat with nothing to catch |

**Why this and not the two attempts before it.** Afloat the boat's
channel sits **188 mm** above the water and the hangar's girders
**526 mm** above its own, so the frame has to come down **334 mm**.

- *Winch it down:* 1 703 kg of buoyancy on a cable, 851 kg even through
  a 2:1 purchase. Doable, but it fights the boat every time.
- *Slipway:* needs a slipway. There isn't one in the plan.
- *Screws:* the same 334 mm, wound in, repeatable, and it stops
  wherever you leave it.

**4 screws, 700 mm of travel, 887 kg each** with the boat aboard —
the floats carry it through the arms, so the screws are in that load
path. Trapezoidal and self-locking, which makes them the **ride-height
adjustment** as well: set the boat's attitude on the frame and it stays
there with no power and no pin.

**No ramp is cut in the hull**, and two attempts proved why: at the
full 334 mm the channel has to be cut up to z 1 134 at the transom and
takes the stern bottom with it; at 120 mm the hull volume came out
*identical* with the cut and without it, because the channel is already
an open mouth at the transom. There was never anything to flare.

**The wheels stay dry throughout** — retracted, the tyre bottom is
222 mm above the boat's waterline and 555 mm above the hangar's own.

## 3. Extenders

**Two V arms per side** on vertical pins, 900 mm long, opening 59° to
put the float **771 mm out and parallel**. The water opens them; a
rope shuts them. No motor, no screw, no telescope. See
[floater.md](floater.md) §5.

## 4. Wheels — four, on the frame, on swing arms

They are no longer on the floats. See **[wheels.md](wheels.md)** for
the mechanism. In short: four **155/70 R12C** trailer wheels, each on
the end of a **445 mm arm** pivoted off the girder web, swinging 180°
between the road and a lined box in the **T-wing**. Track 1 820,
ground clearance 261, tyre stowed 310 mm above the waterline,
self-locking, workable afloat.

## 5. What it does to certification

The frame, the floats, the running gear and the drawbar unbolt as one
unit: that unit is **the trailer**, the boat is cargo on it. The
wheels never carry through the boat's structure - the load path stops
at the girder.

## 6. Open points

- **Dinghy freeboard is 216 mm** with two aboard — thin. Options: bigger
  floats stern-only, or accept it as a calm-water tender.
- The T-step at z 600 narrows the interior below that height: the sole
  band from z 350 to 600 is **1 560 mm** wide, not 2 280. The berths sit
  above z 600, but the heads floor and the tank bays need a layout pass.
- The stem quarters near the transom want fairing into the jets' inflow.
- Spike rail wear pads and the bayonet preload need detailing.


## 7. The floor, and why it is two parts

Asked for an aluminium bottom on the hangar that would both protect the
hull underneath and be a platform to walk on when undocked. It has to
be **two parts**, because one part cannot be in two places — and the
reason is worth writing down.

**The frame has no structure below the hull.** The girders sit at
y ±835, z 600 … 800 — *above* the stem and *outboard* of it. Every
route from there down to the keel is blocked:

| Route | Blocked by |
|---|---|
| straight down at y ±835 | the docked float, z −110…590, x 600 … 6 000 |
| inboard of that | the stem: 1 560 mm wide below z 600, and its face is at y 780 — the same y as the float's inner face, so there is **zero gap** to thread through |
| forward, past the float's bow | the hull goes full width from x 5 600 (half-width 1 081 at z 300) |

That leaves 720 mm of a 5 700 mm frame, at the stern, as the only place
a leg could reach the water. A 5 m cantilever off that is not
structure. And hanging the plate off the **floats** is out — they move.

So:

- **The deck** — **5.70 × 1.78 m**, the whole frame, in 3 mm 5083 tread
  plate on two panels with a centreline stringer and bearers, so
  neither panel cantilevers off its girder. **10.1 m²**, which roughly
  doubles the boat's own 12.7 m² of roof deck: detached and lying
  alongside, the hangar is a pontoon to work on, swim off, or park a
  boat's worth of gear on while the cabin stays a cabin. 760 mm above
  its own waterline. Docked it lifts out, because at z 800 between the
  girders is the inside of the boat. **134 kg** — plate is the whole
  cost of a deck, and this is the biggest single item on the hangar
  after the float shells.
- **The keel shoe** — 3 mm 5083 bolted flat on the stem's 1 560 mm
  bottom, transom to x 6 000. Sacrificial: it takes slipway rash,
  gravel and the odd rock. **81 kg**, and it belongs to the *boat*, not
  the hangar, which is the point — the hangar comes off and the
  protection stays.


## 8. Six wheels, a bow ramp, and what it can actually carry

**Six wheels.** A middle pair on the axle centroid at x 3 510. It halves
the girder spans — the longest bay goes 3 300 → 1 650 — and bending
goes as the span *squared*, so the girder that was right for two axles
came out at SF 8 with three. It drops to **60 × 120 × 4, 41 kg the
pair against 92**: the middle wheels pay for most of themselves. Each
wheel now carries **576 kg against a 900 kg tyre**.

It is not free. A third notch pair in each float costs **93 kg of
buoyancy** (185 → 278 kg a side), and buoyancy is what the hangar
floats and carries cargo on.

**The bow ramp.** 1 600 mm hinged on the frame's forward end,
projecting forward, lowering 25° to reach from the deck at z 800 down
to **z 124**. The forward tie is its hinge beam. *(First drawn hinged
1 600 mm back from there, which swung the ramp straight through that
tie — the bar was structural, and visible the moment the hangar was
rendered on its own.)*

### Could a car go up it?

**No.** Two independent limits, and buoyancy is the decisive one.

Stated as float freeboard, which is something you can look at, rather
than as a percentage of a buoyancy nobody can picture. Computed by
`params.payload_afloat()` and `params.float_freeboard()` — it used to
be this table alone, typed by hand against a hangar mass that had since
changed twice.

| Payload | Float freeboard |
|---|---|
| 300 kg | 207 mm |
| **400 kg** | **175 mm** |
| 500 kg | 144 mm |

The float pair displaces **1 600 kg** fully immersed. The hangar that
actually floats away is **781 kg** of that — not the 675 kg road
figure, because two of the three waterjets are built into the floats
and the arm jacks live in the V arms, so **106 kg was booked to the
boat that leaves with the hangar**. A car is 900–1 500 kg: it would put
the floats under before it was aboard.

And it would not fit anyway. Clear width between the girders is
**1 580 mm** and the deck overhangs to 1 760 — a Kei car's *track*
fits, its body does not — and the deck is 3 mm plate on ribs at
1 200 mm centres: right for people and cargo, not for 300 kg wheel
loads on a 200 mm contact patch.

**Afloat it will carry a quad, two motorbikes, or about 350 kg of
cargo** with sensible freeboard.

**On the road** it is a different question — as a trailer on its own
the O2 limit leaves 2 707 kg and the six tyres are good for 5 400 —
but the deck would need thicker plate and proper wheel tracks first.

### To actually carry a car

Float displacement would have to roughly double: **1 500 kg a side**
against 800 now. At 5.4 m long and 460 mm wide that means about
**1 200 mm of depth** instead of 700, which the wing underside will not
allow, so the float would have to grow in length and beam — and the
road width is already 2 500 of a 2 550 limit. It is a different boat,
not an option on this one.

## 10. The simplification pass — 766 → 675 kg

The hangar had grown a mechanism per problem and nobody could say what
it could carry. The reason was in the code, not in the concept:
**394 kg of its 766 kg came from hand-guessed constants** —
`MASS_HYDRAULICS` a flat 80, `ARM_KG` a flat 22, and a bare unnamed
`+ 20` on the end of the sum. Half the trailer's mass was an estimate
nobody had revisited, so the payload could only ever be a guess too.

### What actually came off

| | was | now | |
|---|---:|---:|---|
| Deck | 140.9 | **87.8** | plank instead of plate — see below |
| Drive | 80.0 | **54.0** | sized for sand, not for a ramp it cannot climb |
| Girders + diagonals | 54.7 | **48.9** | 60 × 120 × 4, plus the torsion fix |
| Wheels | 90.0 | **78.0** | 13 kg each; the hub is on the arm, not counted twice |
| Float decks | 33.9 | **23.9** | PET60: the stub axles it was specified for moved to the arm |
| Ties | 35.9 | **25.8** | real box sections instead of a solid × 0.15 "fill" |
| Locks | 10.4 | **5.2** | two are drawn; the other two were per a dead spike |
| **Brakes** | **0** | **34.0** | a bill that was never presented — over 750 kg an O2 trailer must have them |
| **Total** | **766.1** | **675.0** | |

Loaded road mass **3 457 kg — 42 kg under the 3 500 limit**, where it
was 49 kg over.

### The deck was the answer to "unrealistic to move"

It was two plates of 880 × 5 700 × 3 mm tread — **66 kg each** — and
because z 800 between the girders is the inside of the boat, they had
to be **lifted out by hand, afloat, over the boat, every time it
docked**. Nobody moves 66 kg off a pontoon.

It is now extruded interlocking pontoon plank, which self-spans
1 425 mm between three bearers, so the ribs *and* the centreline
stringer both disappear. **Fifty-eight boards of 1.1 kg.** You take the
deck up one plank at a time.

It also has a **stated load rating for the first time: 2.5 kPa.** The
old deck was never checked against any load at all, and failed that one
by 2.9× read as a one-way strip.

### Three things that were wrong, not just heavy

- **The girder fails in torsion.** A kerb strike lands at the contact
  patch, z −261, while the girder's shear centre is at z 660 — a
  921 mm lever, **7.8 kNm of pure torque** into a thin box. No section
  that fits the wing channel survives it. The fix is a load path, not a
  thicker wall: twelve diagonals tying each wheel bracket fore and aft
  to a deck bearer, 7.9 kg, and the torque becomes a couple. It is now
  `structure_calc` case 4.
- **The swing arms were sized against four wheels when there are six.**
  `structure_calc` divided by 4 with three stations, overstating every
  wheel's share by 50 %. Corrected, the arm passes at SF 3.3 on an 8 mm
  wall instead of 12.
- **The deck bearers were drawn outside the docked guard**, so with the
  boat aboard a beam stood at z 660–800 between the girders — inside
  the stem, which the comment directly above it says cannot happen.

### And the drive could never do its job

3 kW a side was sized to climb a 1:8 slipway: 4 979 N. Two driven
wheels carrying a third of the boat can only put **4 579 N** through
wet concrete before they spin. **It was sized for a job traction
forbids** — which is what the winch is for, and always was. Re-sized
for what it really does, soft ground at walking pace (sand at 12 %
rolling resistance, 4 120 N against 5 723 N of traction, 3 km/h), it is
2 kW a side.

## 11. Docking: the sequence, and proof that it fits

The hangar could never be shown to go under the boat, because nothing
in the repo ever tested it. Beauty shots cannot: the hull stands in
front of the hangar in every one, so a frame buried in the wing looks
perfectly fine. `freecad/dock_check.py` intersects the hull solid with
every part of the hangar and measures the volume that comes back.

**It found that the hangar overlapped the hull in every pose already** -
21 litres in cruise, 11 in road, 12 litres per float - none of it
visible in any render. The docking pose was not the problem; the model
had simply never been checked.

### The sequence

| | | |
|---|---|---|
| 1 | floats **splayed**, frame jacked **down 358 mm** | girders come to the boat's channel; the floats pass **outside** the hull instead of driving into the wing |
| 2 | winch forward | the girders enter the channels from astern; wheels are **down**, because stowed they stand up into a wing that has no pocket over them yet |
| 3 | jack the frame **up** | the boat's weight transfers to the floats, which sink ~356 mm **on their own** - the jack never has to push them down |
| 4 | close the V arms | the floats swing into their recesses, now at the right height |

Step 3 is why the stroke works. The float bottom goes from −166 mm
(hangar floating light) to −522 mm (fully docked); the recess floor it
has to reach is at −515. **It matches to 7 mm, and it is load transfer
that does it, not the screw.** The jack only travels the 358 mm of
step 1, leaving 342 mm of its 700 mm spare.

### What had to change to make it true

- **The wing's outer lip, `T_LIP_Z`, was the most expensive 40 mm in the
  model.** It is a *shadow line* - its only job is to let the docked
  float sit recessed behind the hull face. But everything that passes
  under the wing is capped by the **lip**, not by the step at 600: the
  float's top and the V arms were both drawn to 600 and were cutting
  through it along their whole length. Raising it 550 → 590 keeps a
  10 mm shadow line and gives back the float's full 700 mm of depth,
  its road clearance and its reserve.
- **The V-arm pins sat exactly on the stem face.** `py = sy * STEM_HW`
  put the pin, its lug, the open stop and the road latch half inside
  the hull. They belong on the groove's centreline - which is also the
  only line where the parallelogram closes without the float yawing.
- **The girder's web stiffeners were drawn 70 mm proud all round**, so
  eight of them stood outside a girder running in a 100 mm channel.
  A web stiffener in a box girder is an internal diaphragm.
- **The wheel pockets and the girder channel are one merged void**, and
  whichever was lined last left its wall standing in the other. The
  pocket's end walls were putting a plate through the girder twice per
  wheel.
- **There is no forward tie any more** and there cannot be one: at
  girder level it crosses the cabin (`SOLE_Z` 620 is 20 mm above the
  wing), and under the keel it cannot clear during the approach. Its
  job is done by the deck bearers when detached and by the boat itself
  when docked.
- **The float sat on the stem face with zero gap.** That is not a fit,
  it is a tangency; the check read 12 litres a side, which is 3 mm of
  numerical sliver over 3.8 m² of touching face. Nothing is built to
  zero.

Run it after any geometry change:

```bash
~/bin/FreeCAD.AppImage --console dock_check.py < /dev/null | tail -20
```

All eight poses now report **FITS**, zero interference.

## 12. The floats are fixed now, and what that decided

The V arms are gone. Each float bolts to the girder on **four welded
struts** - no pins, no stops, no haul ropes, no latch, no groove in the
float, no parallelogram to keep true, and no powered jacks either.
**Nothing on the hangar moves any more except the six wheels.**

| | was | now |
|---|---|---|
| Float connection | 4 swinging V arms on 8 vertical pins + 4 powered screw jacks | **4 welded struts** |
| Mass | 55 kg of arm gear + 56 kg of jacks | **36 kg** |
| Governing load | 16.4 kN of slam on a 900 mm lever, in bending | the same blow on a **260 mm** strut |

The strut is sized by a *side* blow, not the vertical one - 4.9 kN taken
as bending over its own short length, 12 MPa against 104. The axial
case is trivial. That is the structural argument for the change in one
line: **the arm multiplied the worst sea load by 3.5; the strut divides
it by the same.**

### What it cost, stated plainly

Righting is reserve × **lever**, and a fixed float can only sit where
the road lets it. Beam is 2.50 m in every condition instead of 4.05.

| | with arms | **fixed** |
|---|---|---|
| Peak righting | 14.7 kNm | **3.8 kNm** |
| F6 gust (4.0 kNm) | SF 3.7 | **SF 0.95** |
| Stability vanishes | beyond 40° | **~38°** |

**An F6 gust alone exceeds the peak righting moment.** The crew's own
weight on one rail is most of it. This is a **sheltered-water boat** as
drawn - canals, harbours, rivers - not ISO category C, and not the
coastal boat the floats were sized for. `checks()` reports it as the
first open item, every run.

### And it cannot be docked afloat any more

A fixed float cannot move out of the hull's way, so the frame cannot be
slid under a floating boat: the solid check reads **105 litres** of
float driven into the wing. Splaying the arms was the only thing that
made the afloat slide-in possible, and the screw jacks went with them.

So the boat is picked up **off a slipway**, the way every trailered boat
is: back the rig down until it floats over, then pull out. That is a
deliberate reversal of the earlier decision to dock afloat, and it is
the price of having nothing that moves.
