#!/usr/bin/env python3
"""Stability: the righting-arm curve, and what it says about the floats.

Before this file, stability in this model was three scalars at zero
heel - a buoyancy moment about the centreline compared with a wind
moment - and it could not answer the only question that matters:
what happens as the boat heels.

It also could not be trusted. The stability block ran at a FROZEN
waterline (WL_Z 260) while the mass budget put the boat 60-115 mm
deeper; the float-immersion assert was a tautology that no weight
change could trip; the reserve driving the righting moment used a
different block coefficient from the float's own buoyancy function,
making it 12 % larger than the whole float; and the wind lever was
1.5 m where the model's own rail_heel_moment() used the true 3.2 m.

What is computed here instead:

  * KG from the mass budget and a per-item height table (params.vcg())
  * the real waterline, from draft_for(), which follows the mass
  * a GZ curve, 0 to 90 degrees, for BOTH stances - floats docked and
    floats extended - so the value of extending them is a table this
    repo prints rather than a claim someone made once
  * the angles that end the curve: deck edge in, downflooding

Run: python3 freecad/stability.py
"""
import math
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import params as P                                            # noqa: E402

G = 9.81
RHO = 1.025e-6          # kg/mm3, salt water

# ---- ISO 12217 design category C, coastal ----
# Winds to Beaufort 6 and a significant wave height to 2 m. The
# thresholds below are engineering checks in the spirit of 12217, not
# a certification: a real category assessment needs the full STIX
# apparatus and a measured boat. They are here so the model states an
# envelope instead of implying one.
CAT_C_WIND = 13.8       # m/s, top of Beaufort 6
CAT_C_GUST = 1.4        # gust over the steady wind
CAT_C_HS = 2.0          # m, significant wave height
AIR_RHO = 1.2
CD_BOX = 1.1


def loaded_mass():
    _items, empty = P.mass_budget()
    return empty + P.CREW_STORES


def waterline():
    """The REAL waterline: it follows the mass. WL_Z is for drawings."""
    return P.draft_for(loaded_mass())


def float_immersion(wl=None):
    """Fraction of the float that is under water sitting upright."""
    wl = waterline() if wl is None else wl
    bot = P.POD_DOCKED[1] - P.FLOAT_H / 2
    return (wl - bot) / P.FLOAT_H


def windage():
    """(area m2, centroid height above the waterline m) of the boat
    seen from the beam, rails stowed. Built from the model's own
    dimensions rather than a literal."""
    wl = waterline()
    cabin_h = P.CABIN_ROOF_Z - P.CABIN_BASE_Z
    cabin_a = cabin_h * 5300 / 1e6
    cabin_z = (P.CABIN_BASE_Z + cabin_h / 2 - wl) / 1000
    top_h = P.CABIN_BASE_Z - wl                     # topsides above water
    top_a = top_h * P.LOA / 1e6
    top_z = (wl + top_h / 2 - wl) / 1000
    a = cabin_a + top_a
    return a, (cabin_a * cabin_z + top_a * top_z) / a


def wind_moment(v, with_rails=False):
    """kNm of heeling moment at v m/s, beam on."""
    a, lever = windage()
    m = 0.5 * AIR_RHO * CD_BOX * a * v * v * lever / 1000
    if with_rails:
        m += P.rail_heel_moment(v)
    return m


def gz_curve(y_float, steps=91):
    """[(heel deg, righting kNm, GZ m)] for a float pair at offset y.

    The float term is exact for a prism: each float's immersion is
    clipped to [0, FLOAT_H] as the boat heels, so the curve saturates
    when the lee float goes under and again when the windward one comes
    clear - which is what actually shapes a multihull's curve.

    The hull term is the linear metacentric one. Past the deck edge it
    understates the truth, so the curve is only quoted to that angle.
    """
    wl = waterline()
    W = loaded_mass()
    d0 = wl - (P.POD_DOCKED[1] - P.FLOAT_H / 2)         # upright immersion
    fl, fb, fh = P.FLOAT_LEN, P.FLOAT_W, P.FLOAT_H
    gm_hull = hull_gm()
    out = []
    for deg in range(steps):
        t = math.tan(math.radians(deg))
        c = math.cos(math.radians(deg))
        d_lee = min(fh, d0 + y_float * t)
        d_win = max(0.0, d0 - y_float * t)
        b = RHO * P.FLOAT_CB * fl * fb * (d_lee - d_win)      # kg of couple
        m = b * G * y_float * c / 1e6                         # kNm
        # W*G is newtons, gm_hull is metres -> N.m, so ONE /1000 to kNm
        m += W * G * gm_hull * math.sin(math.radians(deg)) / 1000
        out.append((deg, m, m * 1000 / (W * G)))
    return out


def hull_gm():
    """GM of the STEM alone, m. Negative: the narrow underwater body
    cannot hold a 2.8 m superstructure up on its own. This is the
    single most important number about this boat, and the model has
    never had it."""
    W = loaded_mass()
    V = W / 1025.0                                    # m3
    wl = waterline()
    i_wp = (2 * P.STEM_HW / 1000) ** 3 / 12 * 6.0     # m4, stem waterplane
    kb = 0.53 * wl / 1000
    return kb + i_wp / V - P.vcg() / 1000


def stance_gm(y_float):
    """GM with the float pair in, m."""
    W = loaded_mass()
    V = W / 1025.0
    wl = waterline()
    fl, fb = P.FLOAT_LEN / 1000, P.FLOAT_W / 1000
    y = y_float / 1000
    i_wp = (2 * P.STEM_HW / 1000) ** 3 / 12 * 6.0
    i_wp += 2 * (fb ** 3 / 12 * fl + fb * fl * y * y)
    return 0.53 * wl / 1000 + i_wp / V - P.vcg() / 1000


def deck_edge_angle():
    """Heel at which the hull's deck edge goes under, degrees."""
    fb = P.CABIN_BASE_Z - waterline()
    return math.degrees(math.atan2(fb, P.HULL_BEAM / 2))


def downflood_angle():
    """Heel at which the lowest opening immerses. The window sills are
    the first thing that lets water in."""
    return math.degrees(math.atan2(P.WIN_Z0 - waterline(), P.CABIN_W / 2))


def summarise(y_float, tag):
    curve = gz_curve(y_float)
    de = deck_edge_angle()
    peak = max(curve, key=lambda r: r[1])
    # area under GZ to the deck edge, in metre-radians
    area = 0.0
    for (d0_, _m0, g0), (d1, _m1, g1) in zip(curve, curve[1:]):
        if d1 > de:
            break
        area += 0.5 * (g0 + g1) * math.radians(1)
    W = loaded_mass()
    print(f"\n{tag}")
    print(f"  float centre y {y_float:.0f} mm, overall beam "
          f"{2 * (y_float + P.FLOAT_W / 2) / 1000:.2f} m")
    print(f"  GM {stance_gm(y_float):5.2f} m")
    print(f"  peak righting {peak[1]:5.1f} kNm  (GZ {peak[2]:.2f} m) "
          f"at {peak[0]:.0f} deg")
    print(f"  area under GZ to the deck edge {area:.3f} m.rad "
          f"= {W * G * area / 1000:.1f} kJ of capsize energy")
    print("   heel   righting     GZ")
    for d, m, gz in curve:
        if d in (0, 2, 5, 10, 15, 20, 30, 40):
            print(f"   {d:3d}   {m:6.1f} kNm  {gz:5.2f} m")
    return peak, area


def main():
    W = loaded_mass()
    wl = waterline()
    print("=" * 68)
    print("STABILITY")
    print("=" * 68)
    print(f"  loaded {W:.0f} kg, waterline {wl:.0f} mm "
          f"(the DRAWING waterline WL_Z is {P.WL_Z} - not used here)")
    print(f"  KG {P.vcg():.0f} mm, of which the laminate sits at "
          f"{P.structure_vcg():.0f}")
    print(f"  float immersed {100 * float_immersion():.0f} % upright, so "
          f"the pair already carries "
          f"{2 * RHO * P.FLOAT_CB * P.FLOAT_LEN * P.FLOAT_W * (wl - (P.POD_DOCKED[1] - P.FLOAT_H / 2)):.0f} kg "
          f"= {100 * 2 * RHO * P.FLOAT_CB * P.FLOAT_LEN * P.FLOAT_W * (wl - (P.POD_DOCKED[1] - P.FLOAT_H / 2)) / W:.0f} % of the boat")
    print()
    print(f"  THE STEM ALONE: GM {hull_gm():+.2f} m")
    if hull_gm() < 0:
        print("  -> negative. The floats are not a stability aid, they ARE")
        print("     the stability. Without them the boat lies on its side.")

    docked = summarise(P.POD_DOCKED[0], "DOCKED  (road, harbour, canal)")
    ext = summarise(P.float_pose(90)[1], "EXTENDED  (the sea stance)")

    print("\n" + "=" * 68)
    print("WHAT EXTENDING THE FLOATS BUYS")
    print("=" * 68)
    print(f"  peak righting  {docked[0][1]:5.1f} -> {ext[0][1]:5.1f} kNm "
          f"({ext[0][1] / docked[0][1]:.1f} x)")
    print(f"  capsize energy {W * G * docked[1] / 1000:5.1f} -> "
          f"{W * G * ext[1] / 1000:5.1f} kJ "
          f"({ext[1] / docked[1]:.1f} x)")
    print(f"  GM             {stance_gm(P.POD_DOCKED[0]):5.2f} -> "
          f"{stance_gm(P.float_pose(90)[1]):5.2f} m")
    print(f"  beam           {2 * (P.POD_DOCKED[0] + P.FLOAT_W / 2) / 1000:5.2f} -> "
          f"{2 * (P.float_pose(90)[1] + P.FLOAT_W / 2) / 1000:5.2f} m")

    print("\n" + "=" * 68)
    print("ANGLES THAT END THE CURVE")
    print("=" * 68)
    print(f"  lee float awash        "
          f"{math.degrees(math.atan2(P.POD_DOCKED[1] + P.FLOAT_H / 2 - wl, P.float_pose(90)[1])):5.1f} deg "
          f"- only {P.POD_DOCKED[1] + P.FLOAT_H / 2 - wl:.0f} mm of float freeboard")
    print(f"  deck edge immerses     {deck_edge_angle():5.1f} deg")
    print(f"  downflooding (windows) {downflood_angle():5.1f} deg")

    print("\n" + "=" * 68)
    print(f"CATEGORY C (coastal): wind to {CAT_C_WIND} m/s (F6), "
          f"Hs {CAT_C_HS} m")
    print("=" * 68)
    a, lev = windage()
    print(f"  windage {a:.1f} m2 at {lev:.2f} m above the waterline, "
          f"rails stowed")
    checks = []
    for name, v, rails in (("F6 steady", CAT_C_WIND, False),
                           ("F6 gust", CAT_C_WIND * CAT_C_GUST, False),
                           ("F6 gust, rails standing",
                            CAT_C_WIND * CAT_C_GUST, True)):
        h = wind_moment(v, rails)
        sf = ext[0][1] / h
        ok = sf >= 1.5
        checks.append((name, ok))
        print(f"  {name:24s} {h:5.1f} kNm  vs {ext[0][1]:5.1f} righting  "
              f"SF {sf:4.2f}  {'OK' if ok else 'FAIL'}")
    # the breaking-wave heuristic: a breaker taller than the beam rolls it
    beam = 2 * (P.float_pose(90)[1] + P.FLOAT_W / 2) / 1000
    print(f"  breaking wave that rolls it: about {beam:.1f} m "
          f"(beam), against Hs {CAT_C_HS} m for the category")
    checks.append(("breaking wave vs beam", beam >= 1.8 * CAT_C_HS))
    print("\n" + "=" * 68)
    print("VERDICT")
    print("=" * 68)
    for n, ok in checks:
        print(f"  {n:28s} {'PASS' if ok else 'FAILS AS DRAWN'}")
    return all(ok for _n, ok in checks)


if __name__ == "__main__":
    main()
