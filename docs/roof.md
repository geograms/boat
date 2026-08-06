# Walkable Decks — Roof Sun Deck and Solar Balconies

Status: design study. Geometry in `freecad/params.py` (the `---- roof
terrace ----` block), shapes in `build_terrace()`, limits asserted in
`checks()`. Spec cards: [roof_deck](images/roof_deck.png),
[roof_glass](images/roof_glass.png), [roof_loads](images/roof_loads.png).
Terms in [glossary.md](glossary.md).

## 1. What it is

The cabin roof at z 2 400 is a 200 mm structural sandwich. On top of it:

```
   ▓▓▓▓▓▓  6+6 laminated heat-strengthened glass, anti-slip frit
   ──┬───  alu grid, 8 panes of 1200 × 1050, bolted to deck inserts
     │ 60  VENTILATED AIR BOX — holds a 30 mm framed module,
   ░░┴░░░  4 × STANDARD 500 W modules 1934 × 1134, laid across
   ██████  200 mm roof sandwich  ← carries every load
   ██████  cabin ceiling 2 200
```

**Nothing moves.** People walk on the glass; the panels underneath can
never be touched, stepped on, or scuffed. The air box ventilates the
cells, so they run cooler than laminates bonded straight to a deck.

Total build-up **127 mm**, so the deck surface sits at 2 531, the air
draft is **2 267** and the road height **3 009** against the 4 000 limit.

The roof panels are **standard 500 W framed modules** (1 934 × 1 134 ×
30, ≈24 kg) rather than bonded laminates — the right
one: they are the cheapest watt on the market, replaceable at any solar
shop, and the 60 mm air box swallows their 30 mm frame with room to
spare. They cost ≈72 kg more than flexible laminates would.

Four of them fit the 4 800 × 2 100 field laid **across** the boat
(1 134 along, 1 934 athwartships). `deck_panel_xy()` in params.py
computes those positions and `checks()` asserts every module lies
inside the field — after an earlier version drew five laminates at
1 700 pitch and put the last two off the bow.

## 2. Why the pop-top was deleted

The earlier design lifted a 12 m² canopy 1 900 mm on four scissor units.
It was judged weak for rough sea and wind. Rechecking the mechanics
agreed with him, and the first analysis had been wrong:

- The force at a scissor foot is **F = W/tan θ** (virtual work), not
  **W/(2·tan θ)** as first specced. The true breakout force was
  **11.4 kN per corner, not 3.6 kN** — the actuators were half the size
  they needed to be.
- Because F → ∞ as θ → 0, a scissor that folds into a thin lid is
  always brutal to start. Fixes existed (park at 7–8°, a 220 mm lid,
  spring assist) but all of them traded thickness or fatigue parts.
- Worse, four salt-exposed mechanisms still had to hold a **7.7 kN**
  uplift at 50 kn, and be trusted after months of neglect.

A fixed glass deck has none of those failure modes. The trade was
**weight-neutral** (see §5), so the whole gain is robustness.

## 3. Sizing the glass

Two load cases, and they scale completely differently:

| | law | t needed at 1 050 mm |
|---|---|---|
| UDL 2 kN/m² | σ = 0.287·q·a²/t² → **t ∝ a** | 4.9 mm |
| 2 kN point on 50 × 50 | σ ≈ (3P/2πt²)·[(1+ν)·ln(2a/πr₀)+0.5] → **t ∝ √ln a** | **11.2 mm** ← governs |

That log term is the whole story: **halving the pane barely thins the
glass.** A 1 000 mm pane needs 10.9 mm, a 400 mm pane 9.4, a 200 mm
pane 8.0 — while the extra grid metal and the shading grow fast. Total
deck weight is nearly flat (300–340 kg) across every pane size, with a
shallow minimum near 400–500 mm.

Chosen: **8 panes of 1 200 × 1 050 in 6+6 heat-strengthened laminated
glass** (12 mm, SGP interlayer). Fewest seals, least shading (4.4 %),
38 kg per pane — two people or a suction lifter to lift one out.
Deflection under the distributed load is 0.9 mm against a span/300
limit of 3.5 mm.

**Two plies, not the three a building floor would use**: the air box is
only 60 mm over a solid deck, so a cracked pane cannot drop anyone. The
residual-capacity case that drives 3-ply floor glazing does not exist
here.

Design loads are the full building-code figures — 2 kN/m² plus a 2 kN
point load — so there are no use restrictions: stilettos, a stepladder,
a dropped anchor are all inside the envelope.

## 4. Detail

- **Panes** drop into a gasketed rebate in the grid with captive
  fasteners; any pane lifts out to clean the inside face or service the
  laminate beneath it.
- **Air box** vented fore and aft through insect mesh. Cross-flow keeps
  the cells cool and clears condensation; the floor of the box falls to
  the corner scuppers.
- **Cabling and junction boxes** live in the perimeter channel, never
  under a walked pane.
- **Anti-slip**: ceramic frit, R11, on the top face.
- **No guardrail** — stanchions and lifelines spoil the line.
  The edge carries the 80 mm toe rail and nothing else. This is a sun
  deck to sit on rather than a working deck, and the fall risk from
  2.4 m is accepted deliberately — worth knowing before anyone brings
  children aboard.
- **Stability**: four people hard to one side is 3.7 kNm of heeling
  against ≈31 kNm of float righting — asserted in `checks()`.

## 5. What it weighs, and what it generates

| removed | kg | added | kg |
|---|---|---|---|
| canopy slab + frame | 145 | glass, 10.1 m² × 30 kg/m² | 302 |
| | | 4 × 500 W framed modules | 108 |
| scissors (4 units) | 88 | alu grid + kerb | 35 |
| drives + controller | 36 | seals, adhesive, fixings | 15 |
| latches, gaskets, coaming | 12 | | |
| solar side walls | 60 | | |
| **total** | **341** | **total** | **460** |

**Net ≈ +107 kg**, of which 96 is the choice of standard framed modules
over bonded laminates. Not a weight saving — mass bought as fixed
structure and replaceable parts instead of mechanism.

Solar: **4.40 kWp nominal** — roof 4 × 500 W = 2.00, balconies
6 × 400 W bifacial = 2.40. After glass transmission (91 %), frame shading
(4.4 %) and the ventilation gain (+5 %), **≈ 4.35 kWp effective** (the bifacial rear gain roughly cancels the glass and frame losses).

Two limits worth stating plainly:

1. **People shade the panels.** The deck generates best when nobody is
   on it. It is a sun deck first and a solar array second.
2. **Dark glass gets hot** — 60–70 °C in strong sun. Light-toned cells
   and the ventilated box help; barefoot at midday will still be
   unpleasant.

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

The roof keeps the 500 W panel, because there the constraint is the
2 100 mm field width and a 1 961 mm module lies across it happily.

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
| 8 × walk-on laminated panes 1200 × 1050, 6+6 HS, frit | 3 200 |
| Alu grid, kerb, standoffs, inserts | 700 |
| Gaskets, structural adhesive, fixings | 350 |
| 4 standard 500 W framed modules (under the glass) | 520 |
| Stanchions, lifelines, sockets | 340 |
| **Roof deck total** | **≈ 5 110** |

| Balconies (both sides) | Est. |
|---|---|
| 6 × 400 W bifacial framed modules | 660 |
| Alu ladder frames, hinges, brackets | 900 |
| Anti-slip tread on the aft passages | 140 |
| **Balcony total** | **≈ 1 700** |
