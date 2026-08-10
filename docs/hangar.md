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

- **The deck** — 3.2 × 1.78 m of 3 mm 5083 tread plate in two panels,
  on the frame between the girders at z 800, with a centreline
  stringer so neither panel cantilevers off its girder. Undocked it is
  what people stand on, 760 mm above the dinghy's waterline. Docked it
  lifts out, because at z 800 between the girders is the inside of the
  boat. **76 kg.** Full frame length would be 134 — plate is the whole
  cost of a deck, and 3.2 m is already more standing room than a tender
  needs.
- **The keel shoe** — 3 mm 5083 bolted flat on the stem's 1 560 mm
  bottom, transom to x 6 000. Sacrificial: it takes slipway rash,
  gravel and the odd rock. **81 kg**, and it belongs to the *boat*, not
  the hangar, which is the point — the hangar comes off and the
  protection stays.
