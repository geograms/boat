# Stability — what the floats are actually for

Status: computed, not asserted from memory. Everything here comes out
of `freecad/stability.py`, which runs off `params.py` and the mass
budget. Run it: `python3 freecad/stability.py`.

## 1. The finding that reframes the boat

**The stem alone has GM −0.42 m.**

The underwater body is 1 560 mm wide and carries a 2 820 mm
superstructure with a 200 mm roof sandwich on top of it. Its own
metacentric height is *negative*. Without the floats the boat does not
float upright — it lies on its side.

So the question "do the extended floats make a difference to stability"
has a sharper answer than expected: **the floats are not a stability
aid, they are the stability.** Even docked they are doing the work; the
extension is about how much margin there is on top.

## 2. What extending them buys

| | docked | **extended** | |
|---|---|---|---|
| Float centre from CL | 1 010 mm | **1 781 mm** | |
| Overall beam | 2.48 m | **4.02 m** | |
| GM | 1.26 m | **4.76 m** | 3.8 × |
| Peak righting | 7.9 kNm @ 21° | **14.5 kNm @ 13°** | **1.8 ×** |
| Peak GZ | 0.26 m | **0.47 m** | |
| Capsize energy to the deck edge | 3.1 kJ | **6.3 kJ** | **2.1 ×** |

**Yes, dramatic — 1.8 × the peak righting moment and 2.1 × the energy
needed to roll it.** And in the small-angle range where the boat
actually lives, the difference is nearer 3 ×: at 5° of heel the docked
stance gives 2.8 kNm and the extended stance 8.5.

## 3. But the curve saturates at 13°, and that is the real limit

The float is **71 % immersed sitting upright** — the pair already
carries 39 % of the boat. There are only **155 mm of float freeboard**.

```
   5°   the lee float goes under      no more buoyancy from it, ever
  13°   the windward float comes clear  PEAK - 14.5 kNm
  32°   the hull's deck edge immerses
  49°   the windows downflood
```

Past 13° nothing more arrives. The curve does not collapse — the
submerged lee float keeps its buoyancy and the arm only loses `cos φ` —
but it never grows again either. This is a **stiff, short-range**
stability: exactly the multihull character, and the opposite of a
ballasted monohull that keeps building righting arm to 60° and beyond.

Two consequences worth being honest about:

- Most of the stability is spent in the first 13°. A knockdown that
  gets past that has nothing new to fight it.
- Like any multihull, if it goes over it will float inverted. There is
  no ballast to bring it back.

## 4. The governing risk is windage, not the floats

| Case | Heeling | vs 14.5 kNm righting | |
|---|---|---|---|
| F6 steady, rails stowed | 2.1 kNm | SF 7.0 | fine |
| F6 gust, rails stowed | 4.0 kNm | SF 3.6 | fine |
| **F6 gust, rails standing** | **13.2 kNm** | **SF 1.10** | **fails** |

The boat presents 14.4 m² to the beam with the rails down. Stand the
solar rails up and it adds 11.6 m² at 3.2 m above the water, which
almost triples the heeling moment. **`checks()` now reports this as an
open item.** The rule is: stow the rails by Beaufort 6. It is the
rails, not the floats, that set the wind limit on this boat.

The breaking-wave heuristic is kinder: a breaker taller than the beam
will roll a small craft, so the extended stance moves that threshold
from **2.5 m to 4.0 m** — against a category C significant wave height
of 2 m. That is the single most valuable thing the extension does for
coastal work.

## 5. Where the levers are

Peak righting, extended, against each variable on its own:

| Float depth | | Extension | | KG | |
|---|---|---|---|---|---|
| 540 mm | 17.2 kNm | 0 mm | 7.5 kNm | 900 mm | 18.2 kNm |
| 600 | 19.2 | 400 | 12.7 | 1 061 | 17.2 |
| **700** | **22.7** | **771** | **17.2** | 1 200 | 16.2 |
| 800 | 26.0 | 1 200 | 22.2 | 1 400 | 14.9 |

*(computed at the earlier KG of 1 061; the ranking is what matters)*

- **Float depth is the cheap lever.** 160 mm more depth buys as much as
  400 mm more extension, costs no beam, and loads the arms no harder —
  because the float's 155 mm of freeboard is what ends the curve at
  13°, not the lever.
- **Extension is the strong lever** but it costs beam, arm load and
  weight; that is why the arms are 900 mm and open 59°.
- **KG is the weak lever.** ±500 mm of KG is worth ±3 kNm. The floats
  dominate everything.

## 6. What this file replaced, and why it was wrong

The old check was three scalars at zero heel, and each had a defect:

| Was | Wrong because |
|---|---|
| stability computed at `WL_Z = 260` | the mass budget floats the boat at **375 mm**. Every hydrostatic number was taken at a waterline the boat never sits at |
| `assert 0.30 < immersion < 0.70` | `POD_WATER[1]` equals `WL_Z` by construction, so immersion was pinned at 0.50. **No weight change could trip it.** The real figure is 71 % |
| `reserve_kg` at Cb 0.80 | `float_buoyancy()` used 0.62 on the same prism, so the reserve driving the righting moment was **12 % larger than the whole float** |
| wind lever 1.5 m | the model's own `rail_heel_moment()` used the true 3.2 m on the same area. Against a correct lever the old margin was **1.06, not 2.16** |
| no KG anywhere | the "righting moment" was a buoyancy moment about the centreline, which is not a righting arm about anything. The only vertical CG in the repo was a literal `1400` in the road tip assert |

`params.vcg()` now computes KG from the mass budget and a per-item
height table, and the laminate's own contribution from the zone areas —
which put it at **1 674 mm**, because the 200 mm roof sandwich is
222 kg sitting at z 2 860. Boat KG is **1 239 mm**.

That also corrects the road figure: the tip angle was computed off the
literal 1 400 and published as 33.0° / 0.65 g. On the computed KG it is
**36.3° / 0.73 g**.

## 7. Limits of this model

- The hull term is the linear metacentric one, so the curve is only
  quoted to the deck edge (32°). Past that the cabin box starts adding
  reserve and the real curve is better than this one shows.
- No free-surface correction — the water tanks should be baffled and
  are assumed so.
- The flooded-cell case is still open (see floater.md).
- These are engineering checks in the spirit of ISO 12217 category C,
  **not a certification**. A real category assessment needs the full
  STIX apparatus and a measured boat.
