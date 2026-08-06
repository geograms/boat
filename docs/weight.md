# Weight — Where the Kilos Are and How to Take Them Out

Status: study, August 2026. Every figure recomputed against the model
(`freecad/laminate.py` × `freecad/areas.json`); nothing here is a guess
about what "should" be lighter.

**Update, August 2026: the biggest lever in this study has been taken.**
The walk-on glass deck is gone, replaced by solar panels that rotate up
into guardrails ([roof.md](roof.md)) — **−305 kg**, while the array grew from 2.00 to 2.30 kWp — and the dome
glass went 8 → 6 mm — **−20 kg**. The boat is now **2 957 kg empty,
3 257 kg loaded**, inside the 3 500 kg category O2 limit with 243 kg,
where it was 3 582 kg and illegal. The rest of this study is what is
left on the table.

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

This alone takes the road mass from 2 957 to **2 614 kg** — while the boat still floats with 50 kWh and
full tanks. The battery has to be designed for it: **five 10 kWh
modules on rails with wet-mate connectors**, not one bonded bank. That
is a decision to take now, because it is impossible to retrofit.

## 2. Structural levers — all measured, none cosmetic

Ranked by kilos per unit of regret.

| Lever | Now | After | Saved | What it costs |
|---|---|---|---|---|
| **Roof core 200 → 60 mm on two beams** | 222 | 148 | **−74** | two alu top-hat beams under the deck; span drops from 2.4 m to 0.8 m, so the core no longer has to do the work alone |
| **Joinery in foam-core GRP, not ply** | 180 | 110 | **−70** | same interior, built from the same panels as the boat; more layup hours |
| **Float shell 18 → 12 mm + local doublers** | 159 | 141 | **−18** | doublers at the six axle landings and six arm roots; needs a load case each |
| **Hull bottom outer skin 1800 → 1400 gsm** | 130 | 115 | **−15** | only after an ISO 12215 check — this is the slam zone |
| **Roof core again**, now that no glass deck sits on it | 148 | 100 | **−48** | the sandwich only has to be a floor now, not a floor carrying a glass lid |
| **Structural total still open** | | | **−225** | no feature lost |

Then one that is a real trade:

| Lever | Now | After | Saved | What it costs |
|---|---|---|---|---|
| **Exoskeleton in 6082 aluminium, not steel** | 260 | 170 | **−90** | −90 kg is the biggest single item left, but: alu fatigues where steel does not, welds lose ~40 % of parent strength, and it needs isolating from every stainless fastener. Worth pricing, not worth assuming. |

## 3. Where the package lands

| | Empty | Loaded (crew + stores) | On the road |
|---|---|---|---|
| Before the rails | 3 282 | 3 582 | 3 282 |
| **Today** (rails + 6 mm dome) | **2 957** | **3 257** | 2 957 |
| + removables (§1) | 2 957 | 3 257 | **2 614** |
| + the remaining levers | **2 685** | 2 985 | **2 342** |
| + aluminium exoskeleton | 2 595 | 2 895 | 2 252 |

Consequences as the boat stands today:

- **Road 2 957 kg**, or 2 614 with the removables: inside category O2
  either way, so the overrun brake set stays a catalogue purchase.
- **Afloat 3 257 kg**: draft 348 mm, freeboard 802 mm.
- **Jack-up 1.27 ×** — still short of the 1.40 wanted. §4.
- **Speed and range unchanged** to within the model's precision.
- **Nothing is deleted.** Same 50 kWh afloat, same sun deck, same dome,
  same interior.

## 4. The jack-up stance is a separate problem

Float buoyancy is **4 152 kg**. At 3 257 kg loaded that is 1.27 ×,
against 1.40 wanted, so the keel will not ride fully awash. Fixing it
means buoyancy, not weight:

| Option | Effect |
|---|---|
| Float depth 900 → 1 050 mm | +690 kg of buoyancy → **1.51 ×**; costs 150 mm of road height (2 977 → 3 127, limit 4 000) |
| Float length 6.2 → 6.6 m | +270 kg → 1.38 ×; the floats already run most of the hull |
| Accept partial jack-up | the keel floats ~80 mm deep instead of awash — the stance still works for boarding and quay fending |

**Deeper floats are the clean answer** and the road height has room for
it. It is a parameter change, not a redesign.

## 5. What is deliberately not on the list

- **Battery capacity.** Cutting 50 → 30 kWh saves 143 kg and costs 40 %
  of the range. The removable-module trick gets the same road benefit
  for none of that.
- **The sun deck.** Kept in full — and it now costs 155 kg instead of
  460, because the panels became the guardrail.
  → [roof.md](roof.md)
- **Wheels and running gear** (270 kg). Six 205/70 R15 on a slipway is
  the reason the boat can launch itself; smaller wheels dig in.
- **Interior comfort.** The 70 kg in lever 2 comes from *how* the
  joinery is built, not from having less of it.
- **Carbon in the hull skins.** 5–8× the cost for stiffness the core
  already provides, and worse impact tolerance.
  → [construction.md §7](construction.md)

## 6. Taken already

| Change | Saved | Where |
|---|---|---|
| **Walk-on glass deck → rotating solar guardrails** | **−305** | [roof.md](roof.md) |
| Dome glass 8 → 6 mm | −20 | [dome.md](dome.md) |

The first one is the model for the rest of this list: it did not delete
a feature, it deleted a *part* by making another part do two jobs.

## 7. What to decide now, because it cannot be retrofitted

1. **Modular battery** — five 10 kWh modules on rails, wet-mate
   connectors, one man can lift a module. Everything else in §1 follows
   from this.
2. **Roof beams before the roof panel is laid up** — the 60 mm core
   only works if the beams exist.
3. **Foam-core joinery** — decided at panel-ordering time, not at
   fit-out time.
4. **Float depth**, if the jack-up stance is to be kept as drawn.
