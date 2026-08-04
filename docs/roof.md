# Pop-Top Solar Roof — Scissor Lift, Plug-In Bars, Solar Side Walls

Status: design study. Geometry in `freecad/params.py` (`SCISSOR_*`,
`CANOPY_*`, `TERRACE_*`, `BAR_*`, `SIDEPANEL_*`, `WIND_*`), shapes in
`build_terrace()`, `build_scissors()`, `build_canopy()` and
`build_side_walls()`, limits asserted in `checks()`. Spec cards:
[roof_scissor](images/roof_scissor.png), [roof_seal](images/roof_seal.png),
[roof_wind](images/roof_wind.png), [roof_hardware](images/roof_hardware.png).
Terms in [glossary.md](glossary.md).

## 1. What the pop-top actually is

**It shelters the terrace, not the cabin.** The cabin roof at z 2 400 is
a sealed structural sandwich — it is the terrace floor, and it stays
put. The pop-top is a separate lid that lifts **1 900 mm** off that
floor so people stand up under it.

That single decision is what makes the whole thing storm-worthy: the
living quarters are never opened by the roof. A leaking pop-top wets a
deck, not a bed.

```
   roof up (terrace)                    roof down (everything else)
   ▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄  canopy 4480     ▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄  2580
   │ ╲   ╱   solar side walls           ══════════════════  latched
   │  ╳   scissors      1 900 clear     ┌────────────────┐
   │ ╱   ╲                              │ scissors flat  │ sealed box
   ══════════════════  terrace 2400     ══════════════════  terrace
   │     cabin, 1 850 clear     │       │  cabin         │
```

The cabin roof went **up 250 mm** with this change (2 150 → 2 400): the
200 mm structural sandwich was eating the interior height. Inside is
now **1 850 mm clear** over the sole, and the road height is 3 062 —
still 938 mm under the 4 000 limit.

## 2. Mechanism: four scissor units

A 1 900 mm stroke cannot fold into a 180 mm lid — that constraint
decides everything. A telescopic column would have to live inside the
cabin; a scissor folds flat instead, so nothing enters the living
space.

| | value |
|---|---|
| units | 4, one per terrace corner, arms fore-and-aft |
| arm | 2 000 mm, pinned at mid-length, single stage |
| raised | 71.8° → **1 900 mm**, span 624 |
| stowed | 3.5° → 122 mm high, span 1 996 |
| stack, stowed | 202 mm into a 100 mm well + the 180 mm lid cavity |
| slider travel | 1 372 mm |
| actuator | 6 000 N, 1 450 mm stroke, 5.5 mm/s → **4.2 min** to raise |

**Single stage on purpose.** A double scissor would halve the travel
but double the pin joints, and on a boat every pin is a corrosion site
to inspect and rinse. Fourteen joints per unit is already the number
that matters.

**The actuators are sized by breakout, not by weight.** The canopy is
only 180 kg (441 N per unit), but a scissor near flat has terrible
mechanical advantage: the push needed is W/(2·tan θ), so **3 609 N** at
the parked angle, falling to 73 N at full height. Hence 6 kN units.

**Four independent actuators, encoder-synced.** They must track within
a few millimetres or the canopy racks. The controller compares Hall
counts and stops all four on any disagreement; the frame is stiff
enough to survive a small mismatch, and the end stops are mechanical.

## 3. Sea-resistance

The mechanism lives outside, so it is engineered for it. The single
biggest mitigation is architectural:

> **Roof down = the mechanism is inside a closed, gasketed box.** In
> road, harbour, cruise and storm trim the scissors see no weather at
> all. They are exposed only at anchor, in fair weather, by the
> operating rules below.

| risk | answer |
|---|---|
| salt in the joints | 316 shoulder-bolt pins in PTFE-lined composite bushes (igus/Vesconite) — no metal-on-metal, no grease to wash out |
| galvanic pairs | hard-anodized 6082-T6 arms, Tef-Gel at every stainless-in-aluminium interface, isolation washers |
| standing water | slider channels are open-bottom, the recessed wells drain to corner scuppers — nothing pools on a bearing |
| actuator seals | IP69K washdown units (Linak LA36 / Thomson Electrak HD class), stainless tube, neoprene boots, rod mounted down-aft so the seal never sits in a puddle |
| water into the cabin | there is no penetration: the lift is entirely above the sealed roof |
| rain on the terrace | canopy crowned 40 mm to a perimeter gutter with a drip edge; terrace drains through four corner scuppers |

**Sealing when stowed.** The canopy skirt drops 50 mm past a 60 mm
coaming — a labyrinth, not a butt joint — onto a continuous EPDM bulb
gasket, and **8 over-centre draw latches** clamp it. The gasket line
sits above any water that can stand on the terrace.

## 4. What holds the roof up

**Never the actuators.** Two independent mechanical locks:

1. **Lock pin** through each scissor at full extension. A red band on
   the pin shows when it is not in — the same convention as the float
   arms.
2. **The plug-in bars** (Max's idea, and structurally the right one).
   The scissors are stiff in their own fore-and-aft plane and floppy
   across the boat; the bars take the transverse load. Four sockets a
   side give three bays, plus two diagonal tie-rods in the forward
   bays. They double as lifeline stanchions and as the frame the solar
   side walls clip into.

Wind, EN 1991-1-4 free-standing canopy, cp,net ±1.5 on 12.5 m²:

| wind | net uplift | per corner |
|---|---|---|
| 25 kn (design) | 1.9 kN | 481 N |
| 50 kn (survival) | 7.7 kN | 1 925 N |

The pins and latches are sized for the survival case; the actuators
never see it.

## 5. Solar side walls

Flexible laminates on 25 mm tube frames, clipped between the bars —
light enough to handle at 4 m up, unlike glass or polycarbonate, and
they generate while they shelter.

- 3 bays per side; the **aft bay stays open** for the ladder.
- 2 laminates per side (≈ 430 W each) → **≈ 1.7 kW** on top of the
  6 roof panels.
- ≈ 10 kg per framed panel; they stow flat under the canopy.
- Fitted, each side shows ≈ 5.8 m² of sail area: at 20 kn that is
  ≈ 2.6 kNm of heeling moment against ≈ 31 kNm of righting moment from
  the floats — negligible, and they come off above 20 kn anyway.

## 6. Operating rules

Raising the roof is a fair-weather, at-anchor operation. On a placard
at the switch:

| | |
|---|---|
| raise | at anchor or alongside only — **never underway, never on the road** |
| above 20 kn | side walls off |
| above 25 kn | roof down and latched |
| before towing | roof latched is a line on the road checklist |
| air draft raised | **4 220 mm above the waterline** — check bridges |

**Raise sequence.** Release the 8 latches → check nobody is on the
canopy → run the 4 actuators together (4.2 min) → drop the 4 lock pins
→ plug in the bars, then the tie-rods, then the side walls.
**Lower** is the exact reverse; the controller refuses to retract while
a lock pin reads home.

**Failure modes.** One actuator stalls → controller stops all four,
roof sits skewed by a few mm, hand-retract via the actuator's
emergency release. Controller dead → the roof is on its pins and is
safe to leave up until 25 kn. Power gone entirely → the pins hold it up
and the latches hold it down; neither needs electricity.

## 7. Cost sketch (2026, EUR)

| Item | Est. |
|---|---|
| 4 × IP69K 24 V actuator, 6 kN / 1 450 mm | 760 |
| Sync controller + Hall encoders + limit switches | 220 |
| Scissor arms, pins, composite bushes (4 units) | 900 |
| Slider channels + UHMW shoes | 180 |
| Canopy sandwich 12.5 m² + alu edge frame + gutter | 1 400 |
| Coaming, EPDM bulb gasket, 8 draw latches | 260 |
| 6 plug-in bars, 8 sockets, 4 tie-rods | 340 |
| 6 side frames + 4 flexible laminates | 1 250 |
| Wiring, drag chain, wind sensor | 300 |
| **Total** | **≈ 5 610** |
