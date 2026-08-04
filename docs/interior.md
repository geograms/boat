# Interior — Layout, Stowage, Services

Status: design study. Geometry in `freecad/params.py` (the `---- interior
----` block), shapes in `build_interior()`, limits asserted in
`checks()`. Drawing: [interior_plan.png](images/interior_plan.png)
(plan, stowage plan, three sections). Terms in
[glossary.md](glossary.md).

## 1. What there is to work with

**5 300 × 2 280 mm of floor, 1 850 mm of headroom.** That is a small
one-bedroom flat's footprint minus the corridor, so every decision is a
trade against another. Two rules shaped the plan:

1. **The beam is the long dimension where it matters.** A body is
   1 900 mm long and the cabin is 2 280 mm wide, so the double bed goes
   **athwartships** — it then eats only 1 400 mm of the boat's length
   instead of 1 900.
2. **Heavy things go low and amidships.** The 50 kWh battery bank fills
   both settee bases at sole level and the water tank sits in the bilge
   *under* the sole — the two heaviest items aboard are also the two
   lowest, and both are on the keel line.

## 2. Zones, aft to forward

```
 aft ← entry                                                    bow →
 ┌────────────┬───────────────────────┬──────┬────────────────┐
 │ AC │galley │  settee / berth       │ ward │                │
 │ ── corridor├─── table ─────────────┤ robe │  DOUBLE BED    │
 │ heads      │  settee / berth       │ ward │  athwartships  │
 └────────────┴───────────────────────┴──────┴────────────────┘
   1 450          2 000                 300      1 500
```

| Zone | Contents |
|---|---|
| **Service 1 450** | heads to port, galley to starboard, **780 mm corridor** straight in from the door |
| **Dinette 2 000** | two settees 1 900 × 620 that are also **single berths**, removable table between them |
| **Wardrobes 300** | one full-height wardrobe each side, 880 mm passage between |
| **Sleeping 1 500** | **elevating** athwartships double, **1 900 × 1 400** |

**Berths for four**: the two settees as singles, the double forward.
The table drops onto its own bearers between the settees and the filler
cushions make the dinette a second double — so six can sleep if they
are friendly.

## 3. Galley

600 mm deep along the starboard side:

- **worktop 900 high** with a sink and a two-zone induction hob
- **washer-dryer** (460 mm compact) under the worktop
- **fridge + freezer tower**, 600 × 600, **1 850 mm tall** — a proper
  vertical fridge, not a coolbox under a seat
- **locker band over the worktop, 1 450–2 200** — 750 mm of full-depth
  lockers, possible only because this side has no picture window

## 4. Heads

A **1 400 × 900 wetroom** (1.26 m²) to port: WC aft, basin on a shelf,
shower riser forward, the whole floor drains to a sump. Sliding door
into the corridor, wall cabinet above the WC to the ceiling. It is a
wetroom rather than a separate shower box because at this size a
separate cubicle would cost the corridor.

## 4b. The elevating bed

The forward zone is 1 500 mm long and the bed is 1 400 of it, so a
fixed bed would spend 22 hours a day being a wasted room. Instead the
platform **hoists to the deckhead**:

| | |
|---|---|
| made up | platform underside **650**, mattress top 870 — normal bed height, **1 330 mm** of air over it |
| stowed | platform underside **1 980**, hard under the deckhead |
| travel | **1 330 mm**, stops anywhere in between |
| clear underneath, stowed | **1 630 mm** over the sole |

**Mechanism.** Four stainless cables, one at each corner, all wound on
**one shaft** running under the deckhead — a single shaft is what
guarantees the corners stay level. The shaft turns through a **worm gearbox**, which is
self-locking: the bed holds wherever it is stopped, with no power and
no brake to fail. A crank/lever socket on the gearbox drives it by hand
if the electrics are dead.

The platform runs on **four corner guide rails** (45 mm section, sole
to deckhead) with UHMW shoes, so it cannot swing when the boat rolls,
and it pins at the stowed height for road and passage-making.

With the bed up, the forward zone is a **1 500 × 2 280 empty floor**
with the big window at the end of it — that is the whole point of the
arrangement.

## 5. AC

The indoor air handler stands in the **aft-starboard corner, right
beside the door**, directly inboard of the ventilator box already
fitted on the outside of that wall — so the duct crosses the wall on
the shortest possible run and no cold air has to be pushed the length
of the boat. Below the handler the same column is a full-height
utility/broom locker. Return air comes off the corridor; supply blows
forward down the centreline.

## 6. Stowage — including what you cannot see

| Where | What |
|---|---|
| under **both settees** | battery bank, 48 V LiFePO₄, **50 kWh**, ≈ 357 kg, split symmetrically |
| under the **sole** | fresh water 200 L in a shallow bilge tank — the lowest weight on board |
| wardrobe base | inverter/charger + MPPT + busbars |
| facing the aisle | **3 drawers per side** |
| **shelf bands 1 150–1 480** | full length of the dinette and the bed, under the windows, both sides |
| over the worktop | 750 mm locker band |
| wardrobes | full height, hanging + shelves |
| fridge tower | full height |

## 7. Windows and vertical space — the trade

Full-height lockers along the sides and big windows want the same wall.
The resolution:

- **Two big picture windows per side** — 1 800 × 600 over the saloon,
  1 200 × 600 over the bed — instead of six small ones. Fewer, larger
  openings look better from outside and give the living zones the view.
- **All full-height joinery is in the service zone**, which has no
  picture window; it is lit and vented by a **360 mm porthole** each
  side.
- In the living zones the storage goes in the **band under the glass**
  (1 150–1 480) rather than blinding the saloon.

`checks()` asserts that no full-height unit ever stands in front of a
window opening, so the interior can be rearranged later without moving
the glass.

## 8. Mass — and the problem with 50 kWh

| | kg |
|---|---|
| joinery | 180 |
| **batteries (50 kWh)** | **357** |
| water (200 L) | 200 |
| appliances | 95 |
| **total** | **832** |

That is ≈ 63 mm of extra draft, which the hull can take. The real
issue is the **mass budget**: the whole boat is costed at 2 000 kg for
towing, and the fit-out alone is now **42 % of it**, with the battery
bank taking 18 % on its own. Hull, frame, floats, wheels, arms, jets
and the glass sun deck have to live in the remaining 1 170 kg, and they
will not.

Three honest options, in order of how much they cost you:

1. **Travel light.** Empty the water tank (−200 kg) and accept that the
   bank is aboard. Cheapest, and it is what most owners actually do.
2. **Split the bank.** Keep ~25 kWh permanently and carry the second
   half as removable modules that come out for road trips (−180 kg).
   The settee bases are already sized for the full 50 kWh.
3. **Re-budget the boat** at ~2 500 kg and tow with a heavier car; a
   Viano is rated for it but the trailer approval changes.

50 kWh is the right *capacity* for the mission — with 6.9 kWp of solar
it is about a day and a half of autonomy, or eight hours at cruise on
all three jets. It is the *mass* that has to be managed, and it is
better to know that now than after the structure is welded.

## 9. Open points

- Heating: the AC is a heat pump, fine to about 0 °C; a diesel air
  heater would need a locker and a flue — not yet placed.
- Holding tank and grey water are not yet modelled; the obvious volume
  is under the heads sole.
- The interior is drawn as volumes, not as joinery details (no door
  swings, fiddles, or fastenings yet).
