# Weight — How to Take 350 kg Out Without Losing Anything

Status: study, August 2026. Every figure recomputed against the model
(`freecad/laminate.py` × `freecad/areas.json`); nothing here is a guess
about what "should" be lighter.

The problem, from [construction.md](construction.md): **3 282 kg empty,
3 582 kg loaded**, against a 2 000 kg figure inherited from the original
towing idea. Loaded, that breaks the **3 500 kg category O2 trailer
limit** and takes the jack-up reserve down to 1.16 × instead of 1.40 ×.

## 1. The insight that changes the problem

**Road mass and afloat mass are two different numbers, and only one of
them is legally binding.**

Afloat, 300 extra kilos cost 30 mm of draft on a hull with 781 mm of
freeboard — nothing. On the road, the same 300 kg decide whether the
vehicle is a category O2 trailer or a different legal animal.

So the cheapest weight saving is not to delete features. It is to
**make the heaviest consumables removable**, so they are aboard when
the boat is a boat and out of it when the boat is a trailer:

| Removable | kg | Cost of removing it |
|---|---|---|
| Fresh water, 200 L | **−200** | fill at the ramp; 20 minutes |
| 20 kWh of the battery as plug-in modules | **−143** | 30 kWh still aboard for the trip; the modules live in the car |
| **Road-only total** | **−343** | **nothing permanent** |

This alone takes the road mass from 3 282 to **2 939 kg** — inside O2
with 561 kg of headroom — while the boat still floats with 50 kWh and
full tanks. The battery has to be designed for it: **five 10 kWh
modules on rails with wet-mate connectors**, not one bonded bank. That
is a decision to take now, because it is impossible to retrofit.

## 2. Structural levers — all measured, none cosmetic

Ranked by kilos per unit of regret.

| Lever | Now | After | Saved | What it costs |
|---|---|---|---|---|
| **Roof core 200 → 60 mm on two beams** | 222 | 148 | **−74** | two alu top-hat beams under the deck; span drops from 2.4 m to 0.8 m, so the core no longer has to do the work alone |
| **Joinery in foam-core GRP, not ply** | 180 | 110 | **−70** | same interior, built from the same panels as the boat; more layup hours |
| **Walk-on glass only where you walk** | 303 | 242 | **−62** | 6 m² of 12 mm walkable lounge, the remaining 4 m² in 6 mm non-walk glass over the panels |
| **Dome glass 8 → 6 mm** | 115 | 95 | **−20** | panes are already small (0.43 m² biggest) and flat, so 6 mm is ample |
| **Float shell 18 → 12 mm + local doublers** | 159 | 141 | **−18** | doublers at the six axle landings and six arm roots; needs a load case each |
| **Hull bottom outer skin 1800 → 1400 gsm** | 130 | 115 | **−15** | only after an ISO 12215 check — this is the slam zone |
| **Structural total** | | | **−259** | no feature lost |

Then one that is a real trade:

| Lever | Now | After | Saved | What it costs |
|---|---|---|---|---|
| **Exoskeleton in 6082 aluminium, not steel** | 260 | 170 | **−90** | −90 kg is the biggest single item left, but: alu fatigues where steel does not, welds lose ~40 % of parent strength, and it needs isolating from every stainless fastener. Worth pricing, not worth assuming. |

## 3. Where the package lands

| | Empty | Loaded (crew + stores) | On the road |
|---|---|---|---|
| Today | 3 282 | 3 582 | 3 282 |
| **+ removables (§1)** | 3 282 | 3 582 | **2 939** |
| **+ the six structural levers** | **3 023** | 3 323 | **2 680** |
| + aluminium exoskeleton | 2 933 | 3 233 | 2 590 |

Consequences of the middle row — the recommended package:

- **Road 2 680 kg**: inside category O2 with 820 kg of margin, so the
  overrun brake set stays a catalogue purchase.
- **Afloat 3 323 kg**: draft ≈ 355 mm, freeboard ≈ 795 mm. Fine.
- **Jack-up 1.25 ×** — still short of the 1.40 wanted. §4.
- **Speed and range unchanged** to within the model's precision.
- **Nothing is deleted.** Same 50 kWh afloat, same sun deck, same dome,
  same interior.

## 4. The jack-up stance is a separate problem

Float buoyancy is **4 152 kg**. Even at 3 323 kg loaded that is 1.25 ×,
against 1.40 wanted, so the keel will not ride fully awash. Fixing it
means buoyancy, not weight:

| Option | Effect |
|---|---|
| Float depth 900 → 1 050 mm | +690 kg of buoyancy → 1.44 ×; costs 150 mm of road height (3 009 → 3 159, limit 4 000) |
| Float length 6.2 → 6.6 m | +270 kg → 1.33 ×; the floats already run most of the hull |
| Accept partial jack-up | the keel floats ~80 mm deep instead of awash — the stance still works for boarding and quay fending |

**Deeper floats are the clean answer** and the road height has room for
it. It is a parameter change, not a redesign.

## 5. What is deliberately not on the list

- **Battery capacity.** Cutting 50 → 30 kWh saves 143 kg and costs 40 %
  of the range. The removable-module trick gets the same road benefit
  for none of that.
- **The sun deck.** It is 352 kg with its frame and it is the boat's
  best feature. Lever 3 keeps it and takes a fifth of the mass out.
- **Wheels and running gear** (270 kg). Six 205/70 R15 on a slipway is
  the reason the boat can launch itself; smaller wheels dig in.
- **Interior comfort.** The 70 kg in lever 2 comes from *how* the
  joinery is built, not from having less of it.
- **Carbon in the hull skins.** 5–8× the cost for stiffness the core
  already provides, and worse impact tolerance.
  → [construction.md §7](construction.md)

## 6. What to decide now, because it cannot be retrofitted

1. **Modular battery** — five 10 kWh modules on rails, wet-mate
   connectors, one man can lift a module. Everything else in §1 follows
   from this.
2. **Roof beams before the roof panel is laid up** — the 60 mm core
   only works if the beams exist.
3. **Foam-core joinery** — decided at panel-ordering time, not at
   fit-out time.
4. **Float depth**, if the jack-up stance is to be kept as drawn.
