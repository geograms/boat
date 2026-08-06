# The Detachable Hangar — a trailer that is also a dinghy

Status: design study. Geometry in `freecad/params.py`
(`HANGAR_*`, `LOCK_*`, `rail_positions()` neighbours `lock_points()`),
shapes in `build_hangar()`, limits asserted in `checks()`.

## 1. Why detach it at all

Two reasons, and the first one is worth more than the second.

**Certification.** With the running gear welded into the hull, the
*boat* is the vehicle: an amphibious one, with a drive on its wheels and
brakes that no catalogue axle can supply. Detached, the hangar is a
**complete trailer** — chassis, axles, brakes, lights, drawbar — and the
boat is **cargo**. A boat trailer carrying a boat is the most ordinary
vehicle in Europe. Everything difficult in
[homologation.md](homologation.md) stops applying to the boat and
applies instead to a trailer that a manufacturer can supply parts for.

**A dinghy.** The floats already carry the motors. Add two
motorcycle-class batteries and a small panel on each float deck and the
detached U runs itself: **4.72 m beam, 504 mm of freeboard with two
people aboard** — a stable working catamaran for a shore run.

## 2. What the hangar is

The drawbar is now modelled too: an **A-frame off the bight** dropping
to a 445 mm coupling height, 50 mm ball head, safety-chain eyes and a
jockey wheel — the parts a technical service expects to see.

```
PLAN — the U                          SECTION at a lock

        bow                              spine 55 x 200
   +-----------+  open end             (rides at the LOCK height,
   |           |                        where the hull is 1 202 half-
 spine       spine  y +/-1 237          beam, not 1 250 at the sheer)
   |           |                                 |
  [float]   [float]                    hull      |  cone
   |           |                     +-------+   |   ___
   +===========+  bight, aft of      |       |<==|==(___)== gearmotor
        |         the transom        |       |   |
     drawbar                         +-------+   |
```

| | |
|---|---|
| Spines | 55 × 200 alu box, y ±1 237, x 900 → 5 900 |
| U opening | **2 419 mm** against a hull 2 403 mm wide at that height |
| Bight | 140 × 180 cross beam, **320 mm aft of the transom**, carrying the drawbar |
| Road width | **2 529 mm** with the spines included — inside 2 550 |
| Mass | **957 kg** complete: floats, wheels, arms, outrigger beams, drives, spines, bight, drawbar, locks |

The spines ride at the **lock height, not the sheer**. The hull is
1 202 mm half-beam down there against 1 250 at the gunwale, and those
48 mm a side are the only reason the U fits inside the road limit at
all.

## 2b. The arms — the original fixed arm on a sliding outrigger

A rigid one-pivot arm cannot give both the wide stance and the
under-hull stow: the pivot would have to sit equidistant from both
float positions, and inside the road envelope that caps the standoff at
**~580 mm**. Articulating the arm fixes the geometry and ruins the
machine. The resolution keeps the arm **exactly as originally designed**
— rigid, welded, radius 990 mm, one 90° swing — and moves its
**shoulder** instead:

```
SEA                          STOW 1 - slide in          STOW 2 - rotate
sleeve                        (on the water)             (the original fold)
  ╠══════beam══════o pivot      ╠══o                       ╠══o
  ║          fixed  \           ║  |fixed arm              ║ / arm swings 90
[spine]        arm  [float]     ║ [float] at the hull      [float] flush
         2 000 mm out           ║  side (ALONGSIDE pose)    UNDER the hull
                              beam tail crosses under
                              the keel - stations are
                              staggered, so the two
                              sides' beams pass
```

Each station carries a **crane-style outrigger beam** sliding through a
sleeve on the spine, driven by a **24 V leadscrew** (worm — self-locking
at any extension). The arm's shoulder pivot and its rotation drive ride
on the beam's outer end.

| Pose | Beam | Arm |
|---|---|---|
| **Sea** | out 1 492 mm | down — float 2 000 mm off the hull |
| **Alongside** | in | down — float at the hull side; lockable anywhere between, so narrow canals get a free intermediate stance |
| **Under / road** | in | rotated 90° — the original fold, flush under the hull, wheels down |

- Righting moment at sea: 31 → **54 kNm**, righting SF 4.2 → **7.2**.
- Water beam 7.7 m at sea; nothing protrudes on the road — retracted,
  the beam tails cross the centreline under the keel, and the port
  stations sit 350 mm aft of the starboard ones so they pass.
- Two powered motions, both self-locking, **no articulation in the arm**
  and still no wrist at the float: the 90° roll comes from the original
  single rotation.

## 3. Coupling — guide with a cone, lock with a motor

**Guide first, lock second.** Each spine carries a **tapered cone,
60 → 120 mm over 180 mm**, that finds a socket bonded into the
exoskeleton frame at the arm stations. The cone swallows the approach
error — roughly ±40 mm and 3° is what a boat on jets can hold — so the
lock never has to do alignment work.

**The lock is a motorised bayonet.** Inside each cone sits a T-head on a
short shaft. A **24 V worm gearmotor** turns it 90° behind a keeper
plate in the hull socket, exactly like a container twist-lock:

- **Self-locking.** A worm drive cannot be back-driven, so no power, no
  hydraulic pressure and no spring is needed to *hold* the lock — only
  to change it.
- **It reports the truth.** Limit switches at both ends of the turn give
  a real locked/unlocked signal, not an inferred one.
- **Interlock.** All four green or the arm drives will not move. That
  rule is an assert in `checks()`, not a note in a manual.
- **Manual override.** A square drive on each gearmotor shaft, turned
  with the winch handle already aboard.
- Preload comes from the cone taper, so the joint is tight rather than
  rattling — which is what kills bolted joints on trailers.

**Sequence, on the water:**

1. Hangar lies to a line with the **arms splayed** — 4.7 m beam, stable
   enough to stand on.
2. The boat **reverses in**: the stern approaches the bight, the spines
   slide alongside the hull. The crew is in the cockpit, watching.
3. Cones enter their sockets; **four locks turn** on one button.
4. **Beams slide in, arms fold** — the two-step stow, all under power.

Uncoupling is the same list backwards, and the boat is never without
either its own flotation or the hangar's.

## 4. Arm drive

Each of the four shoulders gets a **24 V worm slew drive**, not a
hydraulic ram:

- self-locking at any angle, so the float parks splayed, alongside or
  fully under without holding pressure;
- no fluid crossing the articulation — the old hydraulic hoses through
  a 90° swing were the least convincing part of the design;
- the same interlock logic and the same manual override as the locks.

## 5. What it does to the mass

| | kg |
|---|---|
| **Boat alone**, empty | **2 228** |
| **Hangar**, the whole trailer | **957** |
| Combination with crew and stores | **3 485** — inside category O2 |

Detachability costs about **180 kg** (spines, bight, cones, gearmotors,
slew drives) against welding it in. What it buys is a boat that is not a
vehicle, a trailer that a technical service has seen before, and a
dinghy that was already aboard.

The hull now floats on **279 mm** empty and 299 mm loaded, because the
hangar's 901 kg is carried by its own floats rather than by the hull.

## 6. Open points

- **Brakes.** The trailer still needs a service brake over 750 kg. On a
  detachable hangar this is now a normal problem: the wheels are on the
  hangar, so a catalogue overrun set can be specified against the
  hangar's own axle loads.
- **The bight and the drawbar** carry the whole towing load into two
  spine beams. Those two joints want a proper calculation, not a
  section guess.
- **Dinghy trim.** 901 kg of hangar with two people aft will trim by the
  stern; the battery bays should go forward in the floats to balance it.
- **Corrosion at the lock.** Aluminium spine, stainless cone, salt
  water, and a motor. Isolate, and make the cone the sacrificial,
  replaceable part.
