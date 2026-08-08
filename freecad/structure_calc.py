#!/usr/bin/env python3
"""Scantling calculations for the load paths that carry the boat.

Three members were drawn by judgement and have to be proved:

  1. the U-girder      - carries the whole boat on the road
  2. the swing arm     - carries the float's buoyancy at sea
  3. the flip-arm tube - carries one wheel's share on the road

Everything below is first-principles beam theory with stated load
cases and stated allowables. Run: python3 freecad/structure_calc.py
"""
import math
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import params as P                                            # noqa: E402

G = 9.81

# ---- materials -----------------------------------------------------
# 6082-T6 extruded aluminium: the usual structural alloy for trailer
# and beam work, weldable, available in box section.
ALU_FY = 260.0          # MPa, 0.2% proof of the parent metal
ALU_E = 70000.0         # MPa
ALU_RHO = 2700.0        # kg/m3
WELD_KNOCKDOWN = 0.60   # HAZ within ~25 mm of a weld (EN 1999-1-1)
SF_STATIC = 1.5         # on yield, static
DYN_ROAD = 2.5          # road shock factor on a trailer axle
DYN_SLAM = 3.0          # wave slam on an outrigger


def box_section(b, h, t):
    """(A mm2, I mm4 about the strong axis, Z mm3) of a box b x h,
    wall t, bending about the h axis."""
    A = b * h - (b - 2 * t) * (h - 2 * t)
    I = (b * h ** 3 - (b - 2 * t) * (h - 2 * t) ** 3) / 12.0
    return A, I, I / (h / 2)


def tube_section(d, t):
    di = d - 2 * t
    A = math.pi / 4 * (d ** 2 - di ** 2)
    I = math.pi / 64 * (d ** 4 - di ** 4)
    return A, I, I / (d / 2)


def report(name, M_Nmm, V_N, Z, A, I, span_mm, welded=True,
           note="", defl_limit=250):
    """Print stress, shear and deflection against the allowable."""
    fy = ALU_FY * (WELD_KNOCKDOWN if welded else 1.0)
    allow = fy / SF_STATIC
    sigma = M_Nmm / Z
    tau = V_N / (A * 0.5)                      # webs take the shear
    d = 5 * (V_N * 2) * span_mm ** 3 / (384 * ALU_E * I) if span_mm else 0.0
    print(f"\n{name}")
    if note:
        print(f"  {note}")
    print(f"  section  A {A:8.0f} mm2   I {I / 1e6:8.2f} x10^6 mm4   "
          f"Z {Z / 1e3:7.1f} x10^3 mm3")
    print(f"  bending  M {M_Nmm / 1e6:7.2f} kNm  -> sigma {sigma:6.1f} MPa   "
          f"allow {allow:5.1f} MPa   {'OK' if sigma <= allow else 'FAIL'}"
          f"   (SF {allow / max(sigma, 1e-9):.2f})")
    print(f"  shear    V {V_N / 1e3:7.2f} kN   -> tau   {tau:6.1f} MPa   "
          f"allow {allow * 0.58:5.1f} MPa   "
          f"{'OK' if tau <= allow * 0.58 else 'FAIL'}")
    if span_mm:
        print(f"  midspan deflection {d:5.1f} mm, limit span/{defl_limit} = "
              f"{span_mm / defl_limit:5.1f} mm   "
              f"{'OK' if d <= span_mm / defl_limit else 'FAIL'}")
    return sigma <= allow


def main():
    items, empty = P.mass_budget()
    loaded = empty + P.CREW_STORES
    hangar = items["HANGAR, complete vehicle"]
    on_wheels = loaded                      # the road case carries it all
    print("=" * 68)
    print("LOAD CASES")
    print("=" * 68)
    print(f"  boat + hangar, loaded            {loaded:7.0f} kg")
    print(f"  of which the hangar itself       {hangar:7.0f} kg")
    print(f"  road dynamic factor              {DYN_ROAD:7.1f}")
    print(f"  wave slam factor                 {DYN_SLAM:7.1f}")
    print(f"  allowable = {ALU_FY:.0f} MPa x {WELD_KNOCKDOWN} (HAZ) "
          f"/ {SF_STATIC} = {ALU_FY * WELD_KNOCKDOWN / SF_STATIC:.0f} MPa")

    # =================================================================
    # 1. THE U-GIRDER
    # =================================================================
    # The boat sits on two girders, one each side. Between the wheels
    # the girder is a beam on three supports (three wheel stations);
    # the governing span is the longest bay, loaded by the boat's
    # weight as a distributed line load, times the road factor.
    wheels = sorted(P.FLOAT_X_DOCKED + d for d in P.WHEEL_XS)
    spans = [wheels[i + 1] - wheels[i] for i in range(len(wheels) - 1)]
    span = max(spans)
    w = on_wheels * G * DYN_ROAD / 2 / (P.SPIKE_L)    # N/mm per girder
    # continuous beam over equal spans: M ~ w L^2 / 10, V ~ 0.6 w L
    M = w * span ** 2 / 10
    V = 0.6 * w * span
    A, I, Z = box_section(140, 200, 8)
    print("\n" + "=" * 68)
    print("1. THE U-GIRDER  (road: the boat's whole weight)")
    print("=" * 68)
    print(f"  wheel stations at x {wheels}, longest bay {span:.0f} mm")
    print(f"  girder mass {A * P.SPIKE_L * ALU_RHO / 1e9 * 2:.0f} kg the pair")
    print(f"  line load {w:.2f} N/mm per girder "
          f"({on_wheels:.0f} kg x {DYN_ROAD} / 2 girders / {P.SPIKE_L} mm)")
    ok1 = report("  140 x 200 x 8 alu box", M, V, Z, A, I, span,
                 note="continuous over 3 wheel stations: M = wL^2/10")
    if not ok1:
        for t in (12, 14, 16):
            A2, I2, Z2 = box_section(140, 200, t)
            if M / Z2 <= ALU_FY * WELD_KNOCKDOWN / SF_STATIC:
                print(f"  -> {t} mm wall would pass "
                      f"({M / Z2:.0f} MPa)")
                break

    # =================================================================
    # 2. THE SWING ARM
    # =================================================================
    # At sea each float can be pressed down by a wave to its full
    # buoyancy. That force reaches the hull through two arms per side;
    # the worst case puts it on ONE arm (the float pitching on a crest)
    # with the slam factor on top.
    reserve = (P.FLOAT_LEN * P.FLOAT_W * P.FLOAT_H * 0.80
               - 3 * P.WELL_L * P.WELL_W * P.FLOAT_H) / 1e6   # kg
    F = reserve * G * DYN_SLAM
    lever = P.SWING_ARM_R
    M2 = F * lever
    V2 = F
    A2, I2, Z2 = box_section(230, 165, 10)
    print("\n" + "=" * 68)
    print("2. THE SWING ARM  (sea: a float driven under by a wave)")
    print("=" * 68)
    print(f"  float reserve buoyancy {reserve:.0f} kg, slam factor "
          f"{DYN_SLAM} -> {F / 1e3:.1f} kN on ONE arm")
    print(f"  cantilever {lever:.0f} mm from the pin")
    ok2 = report("  230 x 165 x 10 alu box (bending about 230)",
                 M2, V2, box_section(165, 230, 10)[2],
                 box_section(165, 230, 10)[0],
                 box_section(165, 230, 10)[1], 0,
                 note="worst case: all of one float on a single arm")
    if not ok2:
        print("  -> the arm must be deeper in the vertical plane:")
        for h in (260, 300, 340, 380):
            A3, I3, Z3 = box_section(165, h, 12)
            s = M2 / Z3
            print(f"     165 x {h} x 12 -> {s:5.0f} MPa "
                  f"{'OK' if s <= ALU_FY * WELD_KNOCKDOWN / SF_STATIC else ''}")

    # =================================================================
    # 3. THE FLIP-ARM TUBE
    # =================================================================
    # On the road each wheel carries its share of the boat, times the
    # road factor, on the arm's offset from the tube.
    per_wheel = on_wheels / (2 * len(P.WHEEL_XS)) * G * DYN_ROAD
    M3 = per_wheel * P.FLIP_ARM_LEN
    A4, I4, Z4 = tube_section(P.FLIP_TUBE_D, 12)
    print("\n" + "=" * 68)
    print("3. THE WHEEL FLIP ARM  (road: one wheel's share)")
    print("=" * 68)
    print(f"  {per_wheel / 1e3:.1f} kN per wheel on a "
          f"{P.FLIP_ARM_LEN} mm arm")
    ok3 = report(f"  tube d{P.FLIP_TUBE_D} x 12", M3, per_wheel, Z4, A4, I4, 0)
    if not ok3:
        for d, t in ((100, 10), (120, 12), (140, 12), (160, 14)):
            A5, I5, Z5 = tube_section(d, t)
            s = M3 / Z5
            if s <= ALU_FY * WELD_KNOCKDOWN / SF_STATIC:
                print(f"  -> tube d{d} x {t} passes ({s:.0f} MPa)")
                break

    print("\n" + "=" * 68)
    print("VERDICT")
    print("=" * 68)
    for nm, ok in (("U-girder", ok1), ("swing arm", ok2),
                   ("flip-arm tube", ok3)):
        print(f"  {nm:16s} {'PASS' if ok else 'FAILS AS DRAWN'}")


main()
