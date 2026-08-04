# Aft Entry — Cockpit, Door, Porch, Stairs

Status: design study. Geometry in `freecad/params.py` (`COCKPIT_*`,
`DOOR_*`, `PORCH_*`, `STAIR_*`, `AC_*`, `LOCKER_*`), shapes in
`build_aft_entry()`. Terms in [glossary.md](glossary.md).

## 1. The constraint that shapes everything

The cabin is only **1 000 mm tall above the deck** — the other 800 mm
of the 1 800 mm headroom comes from the hull below. So a full-height
door is not geometrically possible: a 1 900 mm door would need the
cockpit floor 20 mm above the keel, i.e. underwater.

The answer is the one every barge and sailboat uses: a **companionway**
— a sunken footwell, a storm sill, a header you duck under, then you
stand up inside.

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
- **Gasketed door** with four dogs (two per side), sealing against a
  continuous frame — the same detail used on wheelhouse doors.
- **Porch roof** over the whole cockpit, so rain never falls on the
  door while it is open, and the crew can stand dry while unlocking.
  A flashing plate closes the 80 mm gap between porch and cabin wall
  and sheds that water to the sides.
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

720 mm of run for 1 000 mm of rise is a **ship's ladder (54°)**, not a
staircase — the aft deck simply has no more length. It is detailed as
a proper ladder rather than pretending otherwise: two stringers on
edge, seven nosed treads let into them. The ladder rises through a
cut-out in the porch roof and lands flush on the terrace.

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

- A **boarding gate** (x 950–1450) is left open in the sheer rail on
  each side, with a threshold step plate.
- Step out of the cockpit onto the side strip, through the gate, and
  you are on the 1 200 mm-wide balcony walkway that runs the length of
  the boat over the float.
- In road mode the balconies fold up over the windows, so the gates
  are simply unused.
