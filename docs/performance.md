# Performance — Speed, Range and How They Were Estimated

Status: first-order estimate. Numbers reproduced by
`docs/perf_model.py`; the summary table lives in the
[README](../README.md) §2.

## 1. The model

No tank test exists, so this is a resistance estimate with every
assumption stated. Treat the speeds as ±10 % and the ranges as ±20 %.

| Input | Value | Why |
|---|---|---|
| Waterline length | 6.60 m | 7.20 LOA less the tapered stem |
| Beam / draft | 2.50 m / **0.37 m** | the draft now FOLLOWS the mass, `params.draft_for()` |
| Displacement | **3 582 kg** | the computed mass budget, loaded — `params.mass_budget()` |
| Wetted surface | **28.0 m²** | hull + two floats, at the computed draft |
| Installed power | **6 kW** | 3 × 2 kW waterjets |
| Propulsive efficiency | **0.45** | small waterjets are poor at low speed |
| Usable battery | 45 kWh | 50 kWh × 90 % depth of discharge |

**Friction** from the ITTC-57 line, Cf = 0.075 / (log₁₀Re − 2)².

**Residuary resistance** is where a barge hurts. A block coefficient
near 0.75 on an L/B of 2.6 makes waves early, so the friction is scaled
by (1 + f) with f rising steeply once the Froude number passes 0.20:

```
f = 0.6 + 140 · max(Fn − 0.20, 0)^1.7        Fn = V / √(g·LWL)
```

That is a shape fitted to published barge and canal-boat data rather
than a first-principles calculation — it is the weakest link here and
the reason for the ±10 %.

## 2. Results

| Speed | Fn | Resistance | Shaft power | Range (45 kWh) | Endurance |
|---|---|---|---|---|---|
| 2.0 kn | 0.13 | 81 N | 0.18 kW | 488 NM | 244 h |
| 3.0 kn | 0.19 | 169 N | 0.58 kW | 233 NM | 78 h |
| 3.5 kn | 0.22 | 258 N | 1.03 kW | 153 NM | 44 h |
| 4.0 kn | 0.26 | 470 N | 2.15 kW | 84 NM | 21 h |
| 4.5 kn | 0.29 | 849 N | 4.37 kW | 46 NM | 10 h |
| **4.7 kn** | 0.30 | — | **6.0 kW** | 32 NM | 7 h |

**Maximum ≈ 4.7 kn.** The boat is *power*-limited, not hull-speed
limited: theoretical hull speed is 6.2 kn, and reaching it would take
about 30 kW. The curve is brutal past 4.5 kn — the last 0.3 kn costs
as much as the first 4.0.

The design conclusion: **cruise at 3–4 knots.** At 3.5 kn the boat has
153 NM of range on the battery alone, which covers a day's canal
passage or a coastal hop with reserve.

## 3. Solar-neutral cruising

This is the number that matters for a liveaboard.

| Condition | Solar/day | House load | Left for propulsion | Neutral speed |
|---|---|---|---|---|
| Good summer day | 24 kWh | 2.5 | 21.5 | **4.2 kn for 8 h** |
| Average spring/autumn | 12 kWh | 2.5 | 9.5 | 3.6 kn for 8 h |
| Overcast winter | 6 kWh | 2.5 | 3.5 | 2.7 kn for 8 h |

In summer the boat can move all day at 4.2 knots and still finish with
a fuller battery than it started. That, not the top speed, is the point
of a 4.4 kWp array on a 2.6 t boat.

**The mass rise costs almost nothing.** Going from the old 2 600 kg
assumption to the computed **3 582 kg** takes the maximum from 4.8 to
**4.7 kn** and the range at 3 kn from 240 to **233 NM**. At these
Froude numbers resistance is friction-dominated, and friction follows
*wetted surface*, which barely moved. Mass is a road and stability
problem on this boat, not a speed problem.

## 4. What is not modelled

- **Wind and sea.** Head wind and chop matter more than anything here
  for a 2.5 m-beam box with a 2.3 m air draft. Expect to lose a knot in
  a fresh breeze on the nose.
- **Appendage and interference drag** between the hull and the floats.
  The floats are close-coupled; their wave systems will interact, and
  it could go either way by a few percent.
- **Waterjet efficiency below 3 kn** is probably worse than the flat
  0.45 assumed. At displacement speeds a propeller would beat a jet
  comfortably — the jet is chosen for weed immunity and shallow draft,
  and it costs real efficiency.
- **Fouling.** A month on a mooring can add 30 % to friction.

## 5. Reproducing it

```sh
python3 docs/perf_model.py            # prints the tables above
```
