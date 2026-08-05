# Front Sky Dome

Status: design study. Geometry in `freecad/params.py` (`DOME_*`,
`dome_section()`, `dome_rings()`, `dome_panes()`), shapes in
`build_front_dome()` and `build_dome_sole()`, limits asserted in
`checks()`.

## What it is

A glazed room over the foredeck — somewhere to sit with the view, not a
windscreen. **It is half a dome, cut flat by the deck**, and it is part
of the living quarters: there is **no wall** between the saloon and the
dome, only a 2 040 mm portal between two corner posts, and **the sole
runs straight through** at z 350. You walk forward out of the saloon
into the glass without a step.

| | |
|---|---|
| aft rim | **exactly the cabin's front rectangle** — the glass corners land on the living-quarters box corners, ±1 200 at z 2 400 |
| opening into it | **2 040 mm wide**, sole to deckhead; posts 180 mm each side carry the roof |
| headroom | **2 050 mm** at the saloon end — standing height, not a sitting nook |
| foot | on the gunwale, following the sheer, all the way round |
| forward | glass ends at **x 6 880** with a flat bow pane, leaving a **320 mm** bow platform |
| glass | **51 FLAT panes**, 8 mm laminated, 4.03 m², ≈115 kg with the frame; biggest pane 0.43 m² |

## All the glass is flat — and why that means triangles

Flat glass is the brief: any pane can be re-cut by any glazier, no
moulds, no lead time, no bent-glass premium. That decides the geometry,
because **a dome is doubly curved and flat quadrilaterals cannot tile
it**. Measured on this shell:

| layout | worst out-of-plane twist |
|---|---|
| 8 panes, one band | 147 mm |
| 8 × 2 with one tube | 153 mm |
| **8 × 3 with two tubes** | **124 mm** |
| 8 × 5 with four tubes | 76 mm |

Splitting barely helps — the twist does not come from pane size, it
comes from the surface changing shape between the rectangular aft rim
and the round bow. A planar-quad optimiser run over the mesh only got
it to 43 mm, and to do that it dragged the shape 214 mm off station.
Against the ~12 mm a gasket plus a little cold-bend can absorb, none of
that works.

**A triangle is planar by definition.** So each cell is split on its
diagonal, and every pane is flat to **0.00 mm** — asserted in
`checks()`, not asserted by hand.

## The frame

```
     aft rim            tube 1            tube 2         bow rim
     x 6200             x 6496            x 6728         x 6880
   (cabin corners)   ┌──── 8 meridians, one diagonal per cell ────┐
        ║════════════╪═════════════════╪══════════════════╣  flat
        ║  ╲  ╱  ╲   │   ╲  ╱  ╲  ╱    │    ╲  ╱  ╲  ╱    ║  bow
        ║════════════╪═════════════════╪══════════════════╣  pane
```

- **8 meridian seams** — the lines that were there before, unchanged.
- **2 tube purlins**, ⌀48 aluminium, across the dome at x 6 496 and
  x 6 728 — these are what keep the panes small.
- **one diagonal per cell**, mirrored about the centreline so the
  pattern reads as a herringbone and not as a random web.
- **flat bow pane** in 3 strips: the bow rim is a plain section at
  constant x, so its closing face is already planar.

## Why the nose is cut off at x 6 880

With flat glass the meridians are straight between rings, so the
silhouette is faceted and sits *inside* the true dome. The last 15 % of
the length is where the dome plunges onto the deck, and that plunge is
what a facet cannot follow:

| glass ends at | facet error |
|---|---|
| x 7 000 (full) | 256 mm |
| **x 6 880 (0.85)** | **20 mm** |

Cutting the plunge and closing with a flat bow pane costs nothing —
that last stretch was 300 mm of headroom over the anchor — and it buys
back a 320 mm bow platform to fend off with. `checks()` asserts the
facet error stays under 40 mm.

## Shape

Each arch springs from the sheer, rises to a crown, and the crown falls
forward on an elliptical law, `crown = deck + 1204·√(1−t²)`. The
section blends from an **exact rectangle** at the cabin face to an
**ellipse** at the bow (`box = (1−t)^1.6` over a square/Chebyshev
mapping) — that is what makes the aft rim match the living-quarters box
corner for corner while the forward end is properly round.

`checks()` asserts the aft arch reaches the cabin roof line and its top
corners land on y ±1 200, that every arch foot sits on the deck to
within 2 mm, that no pane is more than 0.5 mm out of flat, that the
biggest pane stays under 1.2 m² (one person can carry it), that the
portal is at least 1 800 mm wide and that there is 1 900 mm of head.

## Open points

- The foredeck plate is cut away over the dome footprint, leaving a
  130 mm gunwale ledge. That ledge is now a **structural rim** carrying
  the dome — it needs a proper section, not a plate edge.
- Ventilation: a glass room facing south needs opening lights. None are
  drawn yet; the obvious place is the two cells either side of the
  crown at the aft rim.
- Shading. 4 m² of glass over a lounge will cook it in July. An
  internal roller on the meridians is the cheap answer.
