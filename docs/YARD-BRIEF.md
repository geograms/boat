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
| Air draft afloat | 2 267 mm |
| Height on the road | 3 009 mm (limit 4 000) |
| Draft, computed | 349 mm empty, 369 mm loaded |
| Freeboard, loaded | 781 mm |
| Mass, computed | 3 282 kg empty, 3 582 kg loaded |
| Structure | foam-core GRP sandwich, 103 m² of panel, 754 kg |
| Propulsion | 3 × 2 kW flush-intake waterjets, differential thrust, no rudder |
| Power | 4.40 kWp solar, 50 kWh LiFePO₄ at 48 V |
| Speed / range | 4.7 kn maximum; 233 NM at 3 kn; solar-neutral at 4.2 kn |
| Accommodation | 5 berths, 1 850 mm headroom, 12.1 m² floor, wetroom, galley |
| Running gear | 6 × 205/70 R15 on swinging arms inside the floats, ≤ 6 km/h |
| Road status | category O2 trailer — **see the open item below** |

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

## The open item: mass

Stated first because it is the thing a builder will spot in five
minutes, and because it is the one number in this package that does not
yet close.

**Computed: 3 282 kg empty, 3 582 kg with crew and stores** — against a
2 000 kg design figure inherited from the original towing concept. The
model now asserts this and **fails**, deliberately. Consequences:

| | |
|---|---|
| **Road category** | 3 582 kg exceeds the **3 500 kg O2 limit** — above it, overrun brakes are no longer permitted and the towing licence changes |
| **Jack-up stance** | floats give 4 152 kg, **1.16 ×** the loaded mass where 1.40 is wanted; the keel will not ride awash |
| **Flotation** | fine — draft 369 mm, freeboard 781 mm |
| **Speed and range** | almost unaffected: 4.7 kn instead of 4.8, 233 NM instead of 240 at 3 kn |

**There is a package that fixes it without deleting anything** — full
working in [Weight](weight.md). Two moves:

**Make the heavy consumables removable**, so the boat is heavy afloat
and light on the road:

| Removable | kg |
|---|---|
| Fresh water, 200 L — fill at the ramp | −200 |
| 20 kWh of the bank as plug-in modules, 30 kWh stays aboard | −143 |

**Then six measured structural levers**, none of which loses a feature:

| Lever | Saved |
|---|---|
| Roof core 200 → 60 mm on two longitudinal beams | −74 |
| Joinery in foam-core GRP instead of plywood | −70 |
| Walk-on glass 12 mm only over the 6 m² you actually walk on | −62 |
| Dome glass 8 → 6 mm (panes are 0.43 m² and flat) | −20 |
| Float shell 18 → 12 mm with local doublers at the landings | −18 |
| Hull bottom outer skin 1800 → 1400 gsm, after an ISO check | −15 |
| **Total** | **−259** |

Where that lands:

| | Empty | Loaded | On the road |
|---|---|---|---|
| Today | 3 282 | 3 582 | 3 282 |
| With the package | **3 023** | **3 323** | **2 680** |

Road mass inside category O2 with 820 kg of margin, so the overrun
brake set stays a catalogue purchase; afloat draft ≈ 355 mm; same
50 kWh, same sun deck, same interior. A builder's opinion on those six
levers — especially the roof beams and the foam-core joinery — is
exactly what this package is asking for.

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
