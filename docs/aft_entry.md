# Aft Entry — Cockpit, Door, Porch, Stairs

Status: design study. Geometry in `freecad/params.py` (`COCKPIT_*`,
`DOOR_*`, `PORCH_*`, `STAIR_*`, `AC_*`, `LOCKER_*`), shapes in
`build_aft_entry()`. Terms in [glossary.md](glossary.md).

## 1. The constraint that shapes everything

The cabin is only **1 000 mm tall above the deck**, so the door height
is bought entirely by how deep the footwell goes. Dropping the floor to
**400 mm** buys three things at once:

| floor | freeboard | clear at the door | bulwark |
|---|---|---|---|
| 620 | 360 | 1 480 — you duck | 530 |
| **400** | **140** | **1 700 — you walk in** | **750** |
| 350 | 90 | 1 750 | 800 (won't gravity-drain) |

400 mm is the sweet spot: **1 700 mm clear at the threshold** (no
ducking), a **750 mm bulwark** all round the well that stops anyone
stepping off into the water, and still 140 mm of freeboard so the
cockpit gravity-drains through the transom.

```
                     porch roof (top flush with the terrace)
        ▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄
        │      ╱ ladder        │▒▒▒ cabin roof 2150
        │    ╱                 ├──────────────
   ═════╡  ╱   ┌───door────┐   │   AC box  ▲ upper right
        │╱     │  1300 mm  │   │  lockers  │ rest of the wall
   deck 1150   │           │   │           │
        ┌──────┤ sill 180  ├───┴───────────┘
        │ footwell 620 ────┴── sole 350 (step down inside)
   ~~~~~~~~~~~ WL 260 ~~~~~~~~~~~
```

## 2. Water-tightness (storm case)

The living quarters stay sealed from every direction:

- **Self-draining footwell** — floor at 620, i.e. **360 mm above the
  waterline**, with scuppers through the transom. Any water that gets
  aboard runs straight out; it can never pond against the door.
- **Storm sill 180 mm** above that floor. Water has to rise 180 mm in
  an already-draining cockpit before it can even reach the threshold.
- **Sliding gasketed door.** The leaf runs to port into a pocket
  **under the ladder** (to the right as you look out from inside), so
  it never swings into the well and never has to be held against the
  wind. A slider only seals if it also clamps, so two **cam levers**
  pull the leaf onto its gaskets when shut — the standard marine
  sliding-door detail.
- **Porch roof** over the whole cockpit, so rain never falls on the
  door while it is open. It is **cantilevered off the cabin wall on two
  diagonal tubes** — no posts standing on the deck, because nobody
  walks on this roof and posts would only clutter the entry. A flashing
  plate seals it to the wall.
- **The AC unit does not breach the envelope**: only its ventilator
  box sits outside, bolted to the aft wall through a gasketed flange.
- **Lockers open outward**, into the cockpit — they are separate
  compartments, so a flooded locker cannot reach the saloon.

## 3. The aft wall, seen from the entrance

Standing in the cockpit facing forward:

| Position | Item |
|---|---|
| **Left (port)** of the door | ship's ladder to the roof terrace |
| Centre | companionway door, 700 mm wide, 1 300 mm high over the sill |
| **Upper right (starboard)** | AC ventilator box, 540 × 340 mm, louvred — heat pump: cools in summer, heats in winter |
| Right, below the AC | locker bank, two doors, 720 × 800 mm — tools, lines, fenders, shore cables |

## 4. Stairs to the roof terrace

The ladder is pushed **hard against the aft wall** — 530 mm of run for
1 250 mm of rise, i.e. **67°** — so it takes almost no deck. (The rise
grew when the cabin roof went up 250 mm for interior headroom; the run
grew with it to hold the angle.) That angle
is only walkable with **alternating treads** (the loft/engine-room
stair): eight half-width treads that swap sides, so each foot gets a
250 mm-deep step in half the going a normal stair would need. Two
stringers on edge carry them.

**One folding handrail, outboard only.** The rail is needed solely
when the roof terrace is in use, so it does not stand permanently in
the way: a single rail on the **outboard (port) side** raises when the
pop-top is up — posts at both ends, and a return that carries on as a
grab rail along the terrace edge — and folds flat onto the stringer
the rest of the time, taking no space in road, harbour or cruise
trim. The inboard side needs no rail: it faces the cabin wall, and the
footwell drop beside it is only 530 mm.

If a gentler stair is ever wanted, the only way is to hang it along
the cabin side over a solar balcony (1 300 mm of run → 37°) — at the
cost of blocking that balcony's aft walkway.

## 5. Reaching the solar balconies

The side decks are only 50 mm wide — the cabin nearly fills the beam —
so the balconies are **not** reached by walking along the sides. They
are reached from the cockpit: both balconies start at x 900, level
with the deck, right where the crew stands.

The balcony panel itself now runs **aft to the transom**, but only as a
**540 mm passage** — it flares to the full 1 200 mm deck at the cabin
wall. A passage is all that is needed back there; widening it would
only add weight, windage and folded height for no use.

On **both sides**, the route out of the door is made walkable by three
pieces:

1. **Triangular corner landing** at bench height (850), filling the
   forward corner of the well. It turns one awkward 750 mm climb into
   two easy steps — floor 400 → landing 850 → deck 1150 — and gives
   room to turn while carrying something.
2. **Half step** at the outboard edge of the landing, then the
   **boarding gate** (x 950–1450): a gap deliberately left in the sheer
   rail with a threshold plate.
3. **Flush threshold plate** at the gate, kept inside the deck edge.
   No stanchions or grab posts: they stood in the middle of the
   passage and would have pushed the road width over the limit.

You then walk the 1 200 mm-wide balcony over the float for the whole
length of the boat. In road trim the balconies fold up over the
windows and the gates are simply unused.
