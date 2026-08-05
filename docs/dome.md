# Front Sky Dome

Status: design study. Geometry in `freecad/params.py` (`DOME_*`,
`dome_section()`, `dome_mesh()`, `dome_panel_edges()`), shapes in
`build_front_dome()`, limits asserted in `checks()`.

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
| aft edge | **exactly the cabin's front rectangle** — the glass corners land on the living-quarters box corners, ±1 200 at z 2 400 |
| foot | sits **on the deck**, following the sheer, all the way round |
| forward | closes down onto the foredeck at x 7 000, leaving 200 mm of solid bow |
| headroom | **1 204 mm** at the saloon end — sitting height, a lounging nook |
| glass | **8 big panes**, 9 seams, 8 mm laminated, 4.07 m², ≈115 kg with the frame |

## Why 8 big panes and not hundreds of small ones

Small panes are cheap to make and a nightmare to keep dry: every seam
is a joint that has to be sealed, and a dome's seams all point uphill
into the weather. Fewer seams beats thinner glass here.

Flat glass cannot do it — a dome is doubly curved, and the best flat
quad layout tried still twisted **205 mm** out of plane, against the
~12 mm a gasket plus a little cold-bend can absorb. Flat *triangles*
work (a triangle is planar by definition) but need ~600 of them.

So the glass is **hot-bent**, in one band of 8 panels round the arch:

| panels | layout | out-of-flat if flat | bend radius |
|---|---|---|---|
| 6 | 6 × 1 | 214 mm | 2.4 m |
| **8** | **8 × 1** | 205 mm | **3.1 m** ← chosen |
| 16 | 8 × 2 | 82 mm | 1.4 m |

The tightest radius anywhere on the shell is **1.6 m**, at the forward
end where the dome closes onto the bow. That is ordinary hot-bent
laminated glass — a car windscreen is bent tighter than that, and every
bus shelter and shop front in Europe is made this way.

One band means the seams run **fore-and-aft only**: no horizontal joint
anywhere on the dome, so nothing collects water and every seam sheds
downhill to the deck.

## Shape

Each arch springs from the sheer, rises to a crown, and the crown
height falls forward on an elliptical law, `crown = deck + 1204·√(1−t²)`,
so the dome closes tangentially onto the foredeck instead of stopping
in mid air.

The section blends from an **exact rectangle** at the cabin face to an
**ellipse** at the bow (`box = (1−t)^1.6` over a square/Chebyshev
mapping). That is what makes the aft arch match the living-quarters box
corner for corner while the forward end is properly round.

`checks()` asserts the aft arch reaches the cabin roof line **and its
top corners land on y ±1 200**, that every arch foot sits on the deck to
within 2 mm, that the forward arch closes flat, that there is at least
1 150 mm of head inside, and echoes the worst bend radius so the
"ordinary hot-bent glass" claim stays honest.
