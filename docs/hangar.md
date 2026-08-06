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
| Mass | **901 kg** complete: floats, wheels, arms, drives, spines, bight, locks |

The spines ride at the **lock height, not the sheer**. The hull is
1 202 mm half-beam down there against 1 250 at the gunwale, and those
48 mm a side are the only reason the U fits inside the road limit at
all.

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
4. **Arms close** under power, taking the floats from y 2 058 alongside
   the hull, and on to the road pose.

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
| **Hangar**, the whole trailer | **901** |
| Combination with crew and stores | **3 429** — still category O2 |

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
