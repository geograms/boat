# Exoskeleton & Tow Arch

Status: design study. Geometry in `freecad/params.py` (`FRAME_*`,
`ARCH_*`), shapes in `freecad/build_boat.py` (`build_frame`,
`build_tow`), limits asserted in `checks()`. Terms in
[glossary.md](glossary.md).

## 1. Why an exoskeleton

Every heavy fitting on this boat pulls on one small patch of hull:
each float arm carries ~1 000 kg through a single shoulder pin, the
balconies hang off the gunwale, the tow puts the whole 2 t through the
bow. A GRP/plywood hull skin hates point loads — it wants distributed
pressure.

So the loads never touch the skin. An external steel frame carries
them, and the hull is left to do only what a hull is good at: resist
water pressure and carry its own distributed weight.

**The frame is strictly outside — nothing crosses the living volume.**
Two hard constraints force the layout, and it is worth stating them
because they rule out the obvious answer (transverse cross-beams
through the boat at shoulder height):

1. At shoulder height the hull is already 1 202 mm half-width, so only
   **73 mm** is left outboard before the 2 550 mm road limit.
2. The folded floats fill the **entire underside from x 300 to 6 500**.

So a transverse member amidships can go neither through the boat (it
would eat the cabin), nor outboard (too wide), nor underneath (floats).
Transverse ties are therefore possible **only at the two ends**, and
the frame becomes a **ladder loop in plan**:

```
   PLAN VIEW                              SECTION (amidships)
   ┌──────────────────────────────┐        ▁▁▁▁▁▁▁▁▁▁▁
   │ ◄── sheer rail (side deck)   │       │  cabin    │  ← nothing
 ══╪══════════════════════════════╪══     │  (clear)  │    crosses
   │ ◄── chassis rail (topside)   │       ├───────────┤
   └──────────────────────────────┘     ══╡hull      ╞══ ← rails half
   stern tie              bow tie         │           │    buried in
   (transom)              (tow pivots)    └───┬───┬───┘    the topsides
                                            float float
```

**Members**

| Member | Section | Job |
|---|---|---|
| 2 × chassis rail | ⌀100 tube at z 760, half-buried in the topsides (reads as a heavy rubbing wale) | carries the float-arm shoulder pins; outer edge 1 227 mm |
| 2 × sheer rail | ⌀90 tube on the side-deck strip outside the cabin wall | carries the solar balcony hinges, fenders; outer edge 1 235 mm |
| 6 × strap | ⌀75 tube, external, at the arm stations | ties chassis rail to sheer rail on the outside of the skin |
| bow tie | ⌀130 tube at the stem | closes the loop, carries the tow-arch pivots |
| stern tie | ⌀130 tube at the transom | closes the loop, carries the main waterjet |

**Torsion**: taken by the plan-view loop plus the hull shell acting as
a shear box — which a monocoque hull does very well. What a hull skin
does *badly* is exactly what the frame now absorbs: concentrated point
loads.

**What bolts to it**: float-arm shoulder pins (cross-beams), solar
balcony hinges (rails), tow arch (bow ring), quay fender rails
(rails), jack pads. Nothing structural lands on the hull skin.

**Bonus**: the frame is one weldment that can be built and jigged
before the hull, and the hull can be repaired or even replaced inside
it. It is also the natural earth/bonding path for the 48 V system.

## 2. Stern arch — the boat tows stern-first

The tow moved to the **transom**, and that one decision made three
other things fall into place. A single wide A-arch pivots on the stern
tie, pin-locked in two positions like the float arms:

| Pose | Leg angle | Where it sits | Function |
|---|---|---|---|
| **SEA** | +65° | apex 567 mm aft of the transom, 1 588 mm above the waterline | **gantry** — anchor sheave, winch fairlead, nav-light post, davit points |
| **LAND** | −23.5° | swung down-aft, tongue telescoped out | **drawbar** — coupling 445 mm above the ground, 1 894 mm aft of the transom |

```
SEA (gantry)                      LAND (tow, stern-first)
    ╔═══════╗ ← anchor sheave
    ║       ║                     pivot
     ╲     ╱                       ╱●
  ┌───●───●───┐              ┌────╱──┐
  │   hull    │        ●____╱╱ hull  │   ← car this side
  │           │      coupling (telescopes, pinned)
```

**Why the stern is the right end**

- **Ramp logic becomes consistent.** The winch (below) pulls toward a
  ramp-top anchor point, so the boat comes out **stern-first** — and
  the car then hooks to the same end. No turning around, no
  reconfiguration between winching out and hitching up.
- **The bow stays clean.** The rounded stem and the winter-garden dome
  are the hydrodynamic and the pretty end; no drawbar, no coupling, no
  brackets. Bow protection is now a **fixed external stem band** —
  part of the frame, no moving parts.
- **At sea the arch finally earns its keep.** A bow bumper was doing
  little (the tyres already fender the sides); a stern gantry carries
  the anchor, the winch lead, lights and davits — real daily use.

**The catch, and the fix.** Towing from the stern reverses the balance:
with the wheels where they were, the coupling load went **−123 kg**
(lifting the hitch — dangerous). The wheel group therefore moved
**573 mm forward** to world x 1 873 / 3 573 / 5 273, putting the CG
between coupling and axle again: **+100 kg down** on the ball,
asserted in `checks()` at 60–130 kg.

- **Extensible**: the tongue telescopes 800 mm inside the apex yoke and
  pins out; extra pin holes give adjustable coupling height.
- **Pin-locked**, not powered: two lock holes per pivot boss plus the
  tongue pins — a pinned triangle in each pose.

## 2b. Stern gear: winch and anchor

- **Electric winch**, 2 t (4 500 lb) class, 12/24 V, mounted on the
  stern tie with a fairlead through the transom. Purpose: **self-
  recovery on slippery ramps**. Algae-covered concrete can drop tyre
  friction to ~0.2, below the 0.18 needed for a 15 % ramp with no
  margin; the winch takes a line to a ramp-top eye or the car and the
  boat hauls itself out regardless of grip. Same drum also serves as a
  kedge winch.
- **Anchor** on a roller at the transom under the gantry sheave: shank
  and plough stow against the roller, rode runs to the drum. Anchoring
  from the stern suits this boat — the winter garden and the terrace
  face forward, so lying stern-to the wind keeps the view and the
  breeze where people sit.

## 3. Bow: closed and faired

Two fixes, one cause. The hull used to end at a **flat 800 mm-wide
stem face** — it read as a hole in renders and it was a bluff plate
being pushed through the water for no reason. The bow now tapers over
four extra stations to a **220 mm rounded stem bar**: a proper
spoon-shaped barge entry, full above the waterline for interior volume,
fine at the waterline for wave-making. Displacement is unchanged
(1 970 kg at WL 260).

The deck plate also closes the top of the hull over its whole length
(the sheer rises forward, so the extra height forward reads as a bow
**bulwark**). The only things now breaking the bow surface are the two
tow-arch pivot brackets, which must be outside by definition — they
stand ~30 mm proud of the shell at the stem.

## 4. Cost sketch (2026, EUR)

| Item | Est. |
|---|---|
| Frame steel (S355 tube, ~180 kg) + laser-cut brackets | 900 |
| Welding/jigging (workshop or DIY) | 800 |
| Hot-dip galvanising | 400 |
| Tow arch tube, telescoping tongue, bosses | 350 |
| Coupling head 2 t + safety cable + pins | 180 |
| **Total** | **≈ 2 600** |
