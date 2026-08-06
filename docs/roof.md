# Roof Deck — Solar Panels That Rotate Into Guardrails

Status: design study. Geometry in `freecad/params.py` (`RAIL_*`,
`rail_positions()`, `rail_footprint()`), shapes in `build_terrace()`,
limits asserted in `checks()`. Terms in [glossary.md](glossary.md).

## 1. What it is

The roof is a **12.7 m² deck you walk on directly** — the structural
sandwich with a non-slip topcoat — and **ten flexible solar panels
that rotate up into a guardrail** around it.

| Pose | What you get |
|---|---|
| **Flat** (road, passage, everyday) | 2.30 kWp harvesting, panels latched down, no deck |
| **Standing** (deck in use) | the whole 5 300 × 2 400 free to walk on, a **1 234 mm guardrail** both sides, and about a third of the output |

**Two continuous rows, five panels each, mirrored about the
centreline.** Each row is one 5 073 mm band with 12 mm shadow gaps, and
the two rows meet on the centreline with 12 mm to spare — the roof is
covered edge to edge, with no leftover strip and nothing interlaced.
Deployed, each row stands vertical on its outboard edge and latches.
One leaf hinge and one catch per panel: 12.5 kg to lift by hand,
nothing synchronised, nothing hydraulic.

## 1b. Why this replaced the walk-on glass

The glass deck existed for exactly one reason: to let people stand on
the roof without touching the panels. It did that, and it cost:

| | Walk-on glass | Rotating rails |
|---|---|---|
| Mass | 352 kg glass + 108 kg framed modules = **460 kg** | 10 × (6.5 + 6) + surface = **155 kg** |
| Cost | ≈ €5 110 | ≈ €2 900 |
| Roof array | 2.00 kWp nominal, **1.83 effective** (glass ate 9 %, the grid shaded 4.4 %) | **2.30 kWp** nominal, **2.42 effective** |
| Guardrail | **none** — an accepted fall risk, 2.4 m above the water | **1 234 mm** both sides |
| Failure mode | a cracked pane is a crane job | a damaged panel is €100 and four bolts |

**−305 kg, −€2 200, +300 W, and the deck gets the guardrail it never
had.** Nothing was traded away: the array is bigger *and* lighter,
because the glass that used to protect the panels was heavier than the
panels themselves.

## 2. The panel

**Zendure flexible, 230 W per panel**, sold in pairs as "460 W":

| | |
|---|---|
| Size, mass | **1 154 × 1 005 × 28 mm, ≈ 6.5 kg** |
| Output | **230 W** each, 22.6 % — 1.16 m² |
| Face | ETFE, MC4 connectors, no glass and no heavy frame |
| Why this size | laid with the 1 005 side along the boat, **five fill a row** and **two rows cover the roof width exactly** |

6.5 kg is the number that makes this design work. A 500 W framed module
is 27 kg; nobody stands ten of those up by hand twice a weekend.

A flexible laminate **cannot** be a guardrail on its own, so each panel
is bonded into an **aluminium box frame, 34 mm section, ≈ 6 kg**. The
frame carries the 0.5 kN/m top line load, the hinge and the latch; the
panel is cladding on it. That frame is the part that gets engineered.

## 3. Deploying, and the wind

Deployed rail height is **1 234 mm** (1 154 panel + 80 toe rail) —
above the 1 100 mm a building code wants for a balcony, which is a
better barrier than most boats carry. Two **removable webbing lines
close the aft edge**, where the ladder arrives and a panel would only
be a gate in the way.

Standing panels are sail area, and `checks()` prices it:

| Wind | Standing area | Heeling moment | Righting |
|---|---|---|---|
| 15 m/s (F7) | 11.6 m² | 4.8 kNm | 31.3 kNm |
| 20 m/s (F8) | 11.6 m² | 8.6 kNm | 31.3 kNm |
| 25 m/s (F10) | 11.6 m² | **13.4 kNm** | 31.3 kNm |

`checks()` solves for the wind that reaches 40 % of the righting moment
and gets **24 m/s**: **the rule is stow above F8**, and stowing all ten
is a one-minute job. The case the latches are actually sized for is uplift
on the flat-stowed panels in a gale.

## 4. What it weighs and what it makes

| | |
|---|---|
| 10 panels | 65 kg |
| 10 alu frames, hinges, latches | 60 kg |
| Non-slip surface, toe rail, scuppers, fixings | 30 kg |
| **Roof deck total** | **155 kg** |
| Build-up over the structural roof | **120 mm** (toe rail 80 + panel 28 + latch 12) |
| Air draft | 2 260 mm (was 2 267) |
| Road height | 3 002 mm (was 3 009, limit 4 000) |

**Output.** 2.30 kWp nominal on the roof. Nothing shades it and nothing
absorbs 9 % on the way in, so the effective figure is **2.42 kWp** —
against 1.83 for the 2.00 kWp array under glass. Deployed vertical the
panels make roughly a third of that and shade each other fore and aft:
**you deploy to sit on the deck, not to charge.**

Boat total: 2.30 roof + 2.40 balcony = **4.70 kWp** nominal,
**4.94 kWp** effective — up from 4.40 nominal with the glass deck.

## 5. Open points

- The sandwich now takes foot traffic directly. The distributed 2 kN/m²
  is easy; the 2 kN point load on a 50 × 50 patch needs the top skin to
  spread it before the core sees it. Check it when the roof core drops
  from 200 mm to 60 mm on beams
  ([weight.md](weight.md)).
- Hinge corrosion. Stainless leaf hinges into aluminium frames on a
  salt deck: isolate, and specify a hinge that can be driven out and
  replaced with the panel in place.
- Cable routing through the hinge line, in a drip loop, so rotating a
  panel does not flex a conductor.

## 6. The solar balconies — full-width standard panels

The balconies carry **400 W BIFACIAL modules**, 1 722 × 1 134,
recessed into an aluminium ladder frame, **3 per side**.

Two datasheet facts decided this. A 400 W panel is the 54-cell format
at **1 722 × 1 134 × 30, ~21 kg**; a 500 W is **1 961 × 1 134 × 30,
~27 kg**. Those 239 mm are exactly what lets **three** fit the 5 300 mm
balcony run (3 × 1 722 + gaps = 5 246) where only two 500 W would go —
so the smaller panel gives *more* power per side: 1.2 kW against 1.0.

**Bifacial on the sides**: the rear face earns its keep here in a
way it never could on the roof. Folded up over the windows in road and
harbour trim both faces see daylight, and deployed flat over the water
the back face picks up the surface reflection — reckon +5 %.

The roof no longer uses framed modules at all — see §1. The balconies
keep them because a balcony panel is structure that folds over a window,
not something anyone lifts by hand.

A side walkway was the first requirement here, and the geometry gave
a hard answer: a 500 W module is 1 134 mm wide, the balcony span is
1 200, and the fold height caps that span at 1 431 — so a walkway
(480 mm) and a full-size module cannot share the deck. Offered the
trade, he **dropped the walkway**: the balconies went from 0.99 to
**2.00 kWp**, which is worth more than side decks nobody needs when the
cockpit and the aft passage already give access.

```
   PLAN of one balcony                SECTION (folded 48 mm)
   +--------------------------+        |<------ 1160 ------>|
   |  module   |   module     |       ...........................
   |  1934x1134|   1934x1134  |       |  module 35 recessed     |
   +--------------------------+       +--- 40 mm alu ladder ----+
    passage 540 aft, tread only
```

| | |
|---|---|
| frame | aluminium box 25 × 40 × 3 ladder, cross rails at 740 |
| modules | **3 × 400 W bifacial per side**, 1 722 × 1 134, recessed |
| walked on | the **540 mm aft passage only** — the panels are not a deck |
| folded thickness | **48 mm** of the 75 available |
| mass | ≈ 149 kg per side |

The folded assembly is what the road limit sees, which is why the
modules still drop **into** the frame rather than onto it.

## 7. Cost sketch (2026, EUR)

| Item | Est. |
|---|---|
| 10 × 230 W flexible panels (5 pairs) | 1 250 |
| Alu frames, 34 mm box, 10 off | 800 |
| Stainless hinges, latches, gate webbing | 380 |
| Non-slip topcoat, toe rail, scuppers | 320 |
| Wiring, MC4, drip loops, junction boxes | 160 |
| **Roof deck total** | **≈ 2 900** |

| Balconies (both sides) | Est. |
|---|---|
| 6 × 400 W bifacial framed modules | 660 |
| Alu ladder frames, hinges, brackets | 900 |
| Anti-slip tread on the aft passages | 140 |
| **Balcony total** | **≈ 1 700** |
