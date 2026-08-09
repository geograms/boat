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
                      flat bottom flush    scissors push them 1.8 m out
```

| | |
|---|---|
| Stem | **1 800 mm** beam below z 600 — floats the boat alone |
| Floats | **6 000 × 350 × 600**, slim; noses protected by 1 200 mm of solid full-width bow |
| Docked | outer faces flush at 2 500; draft 313 mm loaded |
| Extended | **1 800 mm** out on the scissors — righting 21 kNm from the slim floats plus the full-width T wings |
| Dinghy | both floats + bight: 6.1 m beam, 216 mm freeboard with two aboard |

## 2. Docking — the fork

Two tapered **spike rails** per side on the stem faces: the float
slides on from astern, the taper closes the fit over the last 300 mm,
and the electric bayonet lock pins it. The bow fairing takes the water
first; the float noses never see slam.

## 3. Extenders

**Campervan-lift scissors**, two per side at x 900 and 4 500, 24 V
leadscrew, self-locking anywhere in the **0 → 1 800 mm** stroke. Purely
horizontal: the float's draft never changes. Docked, they fold into the
notch.

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
  band from z 350 to 600 is **1 800 mm** wide, not 2 280. The berths sit
  above z 600, but the heads floor and the tank bays need a layout pass.
- The stem quarters near the transom want fairing into the jets' inflow.
- Spike rail wear pads and the bayonet preload need detailing.
