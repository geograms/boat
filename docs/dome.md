# Front Sky Dome

Status: design study. Geometry in `freecad/params.py` (`DOME_*`,
`dome_section()`, `dome_mesh()`), shapes in `build_front_dome()`,
limits asserted in `checks()`.

## What it is

A glazed conservatory over the foredeck — somewhere to sit with the
view, not just a windscreen. It replaces the old wrap-the-whole-cabin
envelope, which was clunky and double-glazed over the picture windows
that already light the saloon.

**It is half a dome, cut flat by the deck.** That is the whole idea:
the deck is its floor, so the crew walks out of the saloon into it at
the same level.

| | |
|---|---|
| aft edge | the cabin's front opening — full roof height 2 400 at the crown, down the corner posts to the deck |
| foot | sits **on the deck**, following the sheer, all the way round |
| forward | closes down onto the foredeck at x 7 000, leaving 200 mm of solid bow |
| headroom | **1 203 mm** at the saloon end — sitting height, a lounging nook |
| glass | 600 flat triangles, 8 mm laminated, 3.9 m², ≈112 kg with the frame |

## Why hundreds of small triangles

A dome is **doubly curved**, and flat glass cannot tile a doubly curved
surface with quadrilaterals. The best 5-bay quad layout tried here
still twisted **200 mm** out of plane, against the ~12 mm a gasket and
a little cold-bending can absorb. A triangle is planar by definition,
which is why every glass dome ever built is triangulated.

So the shell is 13 arches from the cabin to the bow, each of 26
segments, tessellated into 600 flat panes. The frame shows only every
other arch plus a few longitudinal stringers, so it reads as structure
rather than as a mesh.

## Shape

Each arch springs from the sheer, rises to a crown, and the crown
height falls forward on an elliptical law, `crown = deck + 1204·√(1−t²)`,
so the dome closes tangentially onto the foredeck instead of stopping
in mid air. The section is a superellipse whose exponent runs from 3.6
aft to 2.0 forward — squarish where it meets the cabin's corners,
properly round where it settles onto the bow.

`checks()` asserts the aft arch reaches the cabin roof line, that every
arch foot sits on the deck to within 2 mm, that the forward arch closes
flat, and that there is at least 1 150 mm of head inside.
