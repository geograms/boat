# The T-Hull and the Nesting Floats

Status: design study. Geometry in `freecad/params.py` (`STEM_HW`,
`T_STEP_Z`, `POD_DOCKED`, `POD_SEA`, `flip_points()`), shapes in
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

## 4. Wheels — manual 180° flip in open bays

Three per float. Each wheel hangs on a curved arm from a **tube that
spans an open bay cut through the float**. A spring pin at each end of
the swing:

| Pose | What |
|---|---|
| **Sea** | wheel points **straight up** through the bay, clear of the water; rides out with the float |
| **Road** | pull the pin, flip 180° by hand, re-pin: the wheel hangs **through the bay**, nested in the float envelope, protruding 250 mm to roll |

**Manual — a pin and a tube, no electrics.** The bays cost 353 kg of
buoyancy across both floats and it is accounted for in `checks()`.

Road stance: ground at **−250**, keel 250 mm over the road — the rig
sits lower than every previous iteration, and the centre of gravity
with it. Road width 2 535 mm unchanged.

## 5. What it does to certification

Unchanged in principle from the detachable hangar: the float pair with
its wheels, bight and drawbar is **the trailer**; the boat is cargo on
it. The wheels never touch the boat.

## 6. Open points

- **Dinghy freeboard is 216 mm** with two aboard — thin. Options: bigger
  floats stern-only, or accept it as a calm-water tender.
- The T-step at z 600 narrows the interior below that height: the sole
  band from z 350 to 600 is **1 800 mm** wide, not 2 280. The berths sit
  above z 600, but the heads floor and the tank bays need a layout pass.
- The stem quarters near the transom want fairing into the jets' inflow.
- Spike rail wear pads and the bayonet preload need detailing.
