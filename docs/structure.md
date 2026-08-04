# Exoskeleton & Tow Arch

Status: design study. Geometry in `freecad/params.py` (`FRAME_*`,
`ARCH_*`), shapes in `freecad/build_boat.py` (`build_frame`,
`build_tow`), limits asserted in `checks()`. Terms in
[glossary.md](glossary.md).

## 1. Why an exoskeleton

Every heavy fitting on this boat pulls on one small patch of hull:
each float arm carries ~1 000 kg through a single shoulder pin, the
balconies hang off the gunwale, the tow puts the whole 2 t through the
bow. A GRP/plywood hull skin hates point loads — it wants distributed
pressure.

So the loads never touch the skin. An external steel space frame
carries them, and the hull is left to do only what a hull is good at:
resist water pressure and carry its own distributed weight.

```
                 sheer rail (both sides, full length)
   ┌═══════════════════════════════════════════════┐
   ║   post          post           post           ║   ← bow ring
   ║    │             │              │             ║     (tow pivots)
   ╠════╪═════════════╪══════════════╪═════════════╣
   ║  ══╪══         ══╪══          ══╪══           ║   ← CROSS-BEAMS at
   ║ shoulder      shoulder       shoulder         ║     the shoulder pins
   └═══════════════════════════════════════════════┘
     stern ring                    x 1400 / 3400 / 5400
```

**Members**

| Member | Section | Job |
|---|---|---|
| 2 × sheer rail | ⌀110 tube, full length, 40 mm inside the gunwale | main chassis rails; carry balcony hinges, fenders, deck edge |
| 3 × cross-beam | ⌀130 tube, at z 760 spanning y ±1210 | each passes **straight through both shoulder pins**, so a float's load goes rail-to-rail, not into the hull side |
| 4 × post | ⌀90 tube | tie cross-beam ends up to the rails |
| bow ring | ⌀130 tube | carries the tow-arch pivots at the stem |
| stern ring | ⌀130 tube | transom tie, main waterjet and platform mounts |

**What bolts to it**: float-arm shoulder pins (cross-beams), solar
balcony hinges (rails), tow arch (bow ring), quay fender rails
(rails), jack pads. Nothing structural lands on the hull skin.

**Bonus**: the frame is one weldment that can be built and jigged
before the hull, and the hull can be repaired or even replaced inside
it. It is also the natural earth/bonding path for the 48 V system.

## 2. Tow arch — one part, two jobs

A single A-arch on transverse pivots at the stem, pin-locked in two
positions exactly like the float arms:

| Pose | Leg angle | Where it sits | Function |
|---|---|---|---|
| **SEA** | +55° | apex 495 mm proud of the stem, 318 mm above the sheer | **collision bar** — the first thing to touch a dock, a lock wall or a log; also pulpit rail and anchor gantry |
| **LAND** | −27° | apex swung down-forward, tongue telescoped out | **drawbar** — coupling 457 mm above the ground, 1 687 mm ahead of the transom |

```
SEA (protection)                LAND (tow)
        ╱▔▔╲  ← rub bar
       ╱    ╲                    pivot
      ╱      ╲                     ●╲
  ┌──●────────●──┐             ┌────╲──┐
  │   bow ring   │             │      ╲╲___tongue___● coupling
  │    hull      │             │  hull    (telescopes, pinned)
```

- **Extensible**: the tongue telescopes ~1 000 mm inside the apex yoke
  and pins out; multiple pin holes = adjustable coupling height, the
  standard trailer trick.
- **Pin-locked**, not powered: two lock holes in each pivot boss (sea
  and land), plus the tongue pins. Same discipline as the float arms —
  the load path in each pose is a pinned triangle, not a hydraulic
  cylinder.
- **Geometry check** (asserted): pivots sit 34 mm proud of the hull at
  the stem and the legs pass ~390 mm below the winter-garden glass
  edge, so nothing fouls the glass or the hull in either pose.
- **Why an arch and not a bar**: two legs converging to an apex is a
  triangle in plan — it takes the sideways loads of a collision and
  the yaw loads of towing without needing a big single-shear pivot.

## 3. Foredeck closed

The deck plate now closes the top of the hull over its whole length
(the sheer rises forward, so the extra height forward reads as a bow
**bulwark**). No open cavity at the bow; the foredeck under the winter
garden is a usable, sealed floor.

## 4. Cost sketch (2026, EUR)

| Item | Est. |
|---|---|
| Frame steel (S355 tube, ~180 kg) + laser-cut brackets | 900 |
| Welding/jigging (workshop or DIY) | 800 |
| Hot-dip galvanising | 400 |
| Tow arch tube, telescoping tongue, bosses | 350 |
| Coupling head 2 t + safety cable + pins | 180 |
| **Total** | **≈ 2 600** |
