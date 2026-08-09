# For the Builder

## What this is

A **7.2 m solar-electric boat-home that is its own road trailer**. The
stabiliser floats fold under the hull and carry six wheels, so one car
tows it and it drives itself in and out of the water on a slipway.
Designed to be built, not admired: every dimension lives in a
parametric FreeCAD model where the legal, structural and hydrostatic
limits are asserted in code, so nothing drifts silently.

The design is at **detailed-concept** stage. Geometry is complete and
consistent; scantlings, brake engineering and the mass resolution are
the work still open, and they are stated plainly rather than hidden.

## What I am asking a yard for

Not a turnkey boat. A **split build**, where the yard does the part that
needs a shop, a flat table and hands that have done it before, and the
owner does the part that only needs time:

| Scope | Who | Hours |
|---|---|---|
| Flat sandwich panels, laid up, bagged, post-cured | **yard** | 250 |
| Hull and float assembly: cutting, taping, filleting | **yard** | 350 |
| Fairing and coating | **yard or owner** | 400 |
| Steel exoskeleton, tow arch, arms | **subcontract** | — |
| Running gear, hydraulics, jets | owner | 500 |
| Interior joinery and fit-out | owner | 500 |
| Electrics, plumbing, systems | owner | 250 |
| Commissioning, trials, approvals | owner + yard sign-off | 150 |

**The specific questions for the yard:**

1. Can you quote **panel layup and shell assembly** as a package —
   103 m² of foam-core panel, hull plus two floats — to the schedule in
   [Construction](#) ?
2. Would you take the boat on **your table but my labour**: I lay up
   under your supervision, you take the structural sign-off?
3. What do you think of the **flat-panel route**? The middle 3.6 m of
   the hull is exactly developable; the ends twist up to 35 mm and I
   have three options costed for them.
4. **Fairing** — 400 h is my estimate for hull plus two floats. Is that
   the number you would use?
5. The **mass package** below takes 259 kg out of the structure and
   makes another 343 kg removable for the road. Which of those six
   levers would you actually do, and what have I missed?

## Principal particulars

| | |
|---|---|
| Length over hull | 7 200 mm |
| Beam, hull | 2 500 mm |
| Beam on the road, folded | 2 535 mm (StVZO limit 2 550) |
| Beam afloat, floats out | 4 716 mm |
| Air draft afloat | 2 260 mm |
| Height on the road | 3 002 mm (limit 4 000) |
| Draft, computed | 328 mm empty, 348 mm loaded |
| Freeboard, loaded | 802 mm |
| Mass, computed | **2 948 kg empty, 3 248 kg loaded** — inside category O2 |
| Structure | foam-core GRP sandwich, 103 m² of panel, 754 kg |
| Propulsion | 3 × 2 kW flush-intake waterjets, differential thrust, no rudder |
| Power | 4.60 kWp solar (one panel type, 20 panels), 50 kWh LiFePO₄ at 48 V |
| Speed / range | 4.7 kn maximum; 233 NM at 3 kn; solar-neutral at 4.2 kn |
| Accommodation | 5 berths, 1 850 mm headroom, 12.1 m² floor, wetroom, galley |
| Running gear | 4 × 155/70 R12C on 445 mm swing arms off the frame, 180° into boxes in the T-wing, ≤ 6 km/h |
| Road status | category O2 trailer, 243 kg inside the 3 500 kg limit |

## Construction, in one page

**Foam-core GRP sandwich**: PVC and PET core, stitched biaxial E-glass
skins, epoxy, vacuum bagged, panels laid up flat and CNC-cut from the
model. Principle throughout: **panel stiffness goes as the square of
core thickness**, so the schedule is thick core and thin skins, and the
skins are set by impact and print-through rather than by bending.

| Zone | Core | mm | Outer | Inner | kg/m² | m² | kg |
|---|---|---|---|---|---|---|---|
| Hull bottom | PVC80 | 20 | 1800 | 900 | 7.60 | 15.3 | 130 |
| Hull topsides | PET60 | 20 | 900 | 600 | 4.53 | 15.9 | 81 |
| Hull deck | PET60 | 25 | 900 | 600 | 4.83 | 4.3 | 23 |
| Float shell (both) | PVC80 | 18 | 1200 | 800 | 5.88 | 24.2 | 159 |
| Float deck (both) | PET100 | 20 | 1200 | 800 | 6.44 | 2.9 | 21 |
| Cabin walls | PET60 | 20 | 600 | 600 | 3.87 | 17.9 | 78 |
| Roof sandwich | PET60 | 200 | 900 | 900 | 16.00 | 12.4 | 222 |
| Bulkheads | PET60 | 15 | 600 | 600 | 3.57 | 9.9 | 40 |
| **Total** | | | | | | **102.8** | **754** |

Areas are measured off the 3D solids, not estimated; masses include a
1.12 margin for tapes, fillets and real resin use. Shopping list that
falls out of it: **203 kg** of dry biaxial fabric, **248 kg** of mixed
epoxy, **39.5 m²** of PVC foam and **63.4 m²** of PET foam.

Two structural decisions worth flagging to a builder:

- **The steel exoskeleton stays steel.** Every point load — six arm
  shoulder pins at ~1 000 kg each, the balconies, the tow — goes into an
  external galvanised frame, so the sandwich carries only distributed
  pressure, which is what sandwich is good at. Glass barrier ply
  wherever steel meets laminate; hard inserts under every through-bolt.
- **Post-cure the roof panels flat at ≥ 55 °C.** They sit under dark
  solar laminates behind glass and will see 60–70 °C. Room-temperature
  epoxy has a Tg of 50–60 °C and will creep. It cannot be retrofitted
  after assembly.

## The mass story, and what is still open

A builder will ask what it weighs, so: **2 948 kg empty, 3 248 kg with
crew and stores**, computed from measured areas × the laminate schedule
plus every known fitting — not estimated. That is inside the 3 500 kg
category O2 trailer limit with 243 kg to spare.

It was 3 582 kg and illegal three changes ago. What fixed it:

| Change | kg |
|---|---|
| Walk-on glass deck → **solar panels that rotate up into guardrails** | **−305** |
| Dome glass 8 → 6 mm | −20 |

The first one is the pattern worth showing a builder: it did not delete
a feature, it deleted a *part* by making another part do two jobs. The
glass existed only to protect the panels underfoot; now the panels
stand up out of the way instead, the deck is bare non-slip sandwich,
the array grew from 2.00 to **2.30 kWp**, and the deck gained the
**1 234 mm guardrail** it never had.

Still open, and worth a builder's opinion:

| | |
|---|---|
| **Jack-up stance** | floats give 4 152 kg, **1.27 ×** the loaded mass where 1.40 is wanted. That wants float *depth*, not weight: 150 mm deeper gives 1.51 × inside the road-height limit |
| **Design figure** | `checks()` still fails against an inherited 2 000 kg target that predates the computed budget. It wants re-baselining |
| **Another 225 kg** | roof core on beams, foam-core joinery, lighter float shell, lighter bottom skin — all costed in [Weight](weight.md) |

## What is already settled

- Hull form, float form, arm kinematics and the 90° swing.
- Walk-on glass roof deck sized for full building-code deck loads
  (2 kN/m² plus 2 kN on a 50 × 50 patch), solar under the glass.
- Interior layout: 5 berths, wetroom, galley, elevating double,
  batteries and water low and amidships.
- Front sky dome: 51 flat panes on 8 meridians and 2 tube purlins, no
  bent glass anywhere.
- Road-approval strategy: category O2 trailer, land drive capped at
  6 km/h, catalogue overrun brake set.

## What is not

- Scantling verification against a class rule (nothing here has been
  checked against ISO 12215 — the schedule is engineering judgement plus
  measured areas).
- Brake engineering for a swinging-arm axle.
- Float compartmentation.
- CFD or tank testing of the waterjet intakes.

Every one of those is named again, with numbers, in the open-risks
section of the main document.
