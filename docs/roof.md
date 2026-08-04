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
     │ 60  VENTILATED AIR BOX — mesh slots fore and aft, drains
   ░░┴░░░  flexible laminates, bonded flat
   ██████  200 mm roof sandwich  ← carries every load
   ██████  cabin ceiling 2 200
```

**Nothing moves.** People walk on the glass; the panels underneath can
never be touched, stepped on, or scuffed. The air box ventilates the
cells, so they run cooler than laminates bonded straight to a deck.

Total build-up **131 mm**, so the deck surface sits at 2 531, the air
draft is **2 271** and the road height **3 013** against the 4 000 limit.

## 2. Why the pop-top was deleted

The earlier design lifted a 12 m² canopy 1 900 mm on four scissor units.
Max judged it weak for rough sea and wind. Rechecking the mechanics
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
- **Guardrail**: the plug-in bar sockets remain, but the bars are now
  **1 000 mm stanchions with two lifelines**, removable so they cost
  nothing on the road.
- **Stability**: four people hard to one side is 3.7 kNm of heeling
  against ≈31 kNm of float righting — asserted in `checks()`.

## 5. What it weighs, and what it generates

| removed | kg | added | kg |
|---|---|---|---|
| canopy slab + frame | 145 | glass, 10.1 m² × 30 kg/m² | 302 |
| scissors (4 units) | 88 | alu grid + kerb | 35 |
| drives + controller | 36 | seals, adhesive, fixings | 15 |
| latches, gaskets, coaming | 12 | | |
| solar side walls | 60 | | |
| **total** | **341** | **total** | **352** |

**Net ≈ +11 kg.** This is not a weight saving — it is the same mass
bought as fixed structure instead of mechanism.

Solar: **4.73 kWp nominal** (deck 5 laminates = 2.15, balconies 2.58)
against 6.88 before; the four side-wall panels went with the raised
roof that carried them. After glass transmission (91 %), frame shading
(4.4 %) and the ventilation gain (+5 %), reckon **≈ 4.5 kWp effective**.

Two limits worth stating plainly:

1. **People shade the panels.** The deck generates best when nobody is
   on it. It is a sun deck first and a solar array second.
2. **Dark glass gets hot** — 60–70 °C in strong sun. Light-toned cells
   and the ventilated box help; barefoot at midday will still be
   unpleasant.

## 6. The solar balconies — same problem, different answer

The side balconies must be walkable too, and Max wants **standard
framed modules** there: standardised, cheap, and replaceable at any
solar shop in ten years' time.

**The roof's trick does not transfer.** Folded up against the cabin for
the road, the balcony assembly may be at most **75 mm thick** before
the 2 550 mm width limit bites. A walking surface *over* the panels
needs module 35 + air gap 40 + tread 30 = **105 mm**. It does not fit.

So on the balcony the walkway goes **beside** the panels, in the same
plane, and the modules drop **into** the frame instead of onto it:

```
   PLAN of one balcony              SECTION (folded thickness 48 mm)
   +-------------------------+       |<-- 480 -->|<--- 690 --->|
   | ///// walkway 480 ///// |      .............................
   +---+-----+-----+-----+---+      | tread 3   | module 35 in  |
   |   | mod | mod | mod |   |      +----- 40 mm alu ladder ----+
   +---+-----+-----+-----+---+
     3 x 1480 x 670 standard panels    hinge <- 1200 -> outer edge
```

| | |
|---|---|
| frame | aluminium box 25 × 40 × 3 ladder, cross rails at 740 |
| walkway | 480 mm of perforated anti-slip alu tread, full length |
| modules | **3 standard 1 480 × 670 framed panels per side, 165 W** |
| folded thickness | **48 mm** of the 75 available |
| mass | ≈ 141 kg per side |

**What it costs.** Giving 480 mm of the 1 200 mm width to a walkway,
and using small standard modules rather than full-size laminates, takes
the balconies from 2.58 kWp to **0.99 kWp**. System total is now
**3.14 kWp nominal / 2.95 effective** — roughly 15–18 kWh on a good
summer day against the 50 kWh bank.

If the walkways are ever judged not worth it, the swap is
straightforward: full-width 1 130 mm modules restore **+1.6 kWp** and
the balconies become panel surfaces you do not stand on, with only the
540 mm aft passage walkable.

## 7. Cost sketch (2026, EUR)

| Item | Est. |
|---|---|
| 8 × walk-on laminated panes 1200 × 1050, 6+6 HS, frit | 3 200 |
| Alu grid, kerb, standoffs, inserts | 700 |
| Gaskets, structural adhesive, fixings | 350 |
| 5 flexible laminates (bonded, under the glass) | 1 750 |
| Stanchions, lifelines, sockets | 340 |
| **Roof deck total** | **≈ 6 340** |

| Balconies (both sides) | Est. |
|---|---|
| 6 × standard 165 W framed modules | 480 |
| Alu ladder frames, hinges, brackets | 900 |
| Perforated anti-slip tread, 6 m² | 420 |
| **Balcony total** | **≈ 1 800** |
