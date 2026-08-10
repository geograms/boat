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

## 2. Docking — the fork

Two tapered **spike rails** per side on the stem faces: the float
slides on from astern, the taper closes the fit over the last 300 mm,
and the electric bayonet lock pins it. The bow fairing takes the water
first; the float noses never see slam.

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
came out at SF 8 with three. It drops to **90 × 140 × 4, 55 kg the
pair against 92**: the middle wheels pay for most of themselves. Each
wheel now carries **517 kg against a 900 kg tyre**.

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

| Reserve freeboard | Payload afloat |
|---|---|
| 20 % | 508 kg |
| 30 % | **348 kg** |
| 40 % | 188 kg |

The float pair displaces **1 600 kg** fully immersed and the hangar is
**793 kg** of that. A car is 900–1 500 kg: it would put the floats
under before it was aboard.

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
