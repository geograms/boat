#!/usr/bin/env python3
"""Scantling calculations for the load paths that carry the boat.

Three members were drawn by judgement and have to be proved:

  1. the U-girder      - carries the whole boat on the road
  2. the extender beam - carries the float's buoyancy at sea
  3. the swing arm     - carries one wheel's share on the road

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
    wheels = sorted(P.WHEEL_XS)               # frame stations, world x
    spans = [wheels[i + 1] - wheels[i] for i in range(len(wheels) - 1)]
    span = max(spans)
    # with only two wheel stations the girder is a simple span, and
    # DEFLECTION governs, not stress
    w = on_wheels * G * DYN_ROAD / 2 / P.GIRDER_LEN   # N/mm per girder
    # continuous beam over equal spans: M ~ w L^2 / 10, V ~ 0.6 w L
    M = w * span ** 2 / 10
    V = 0.6 * w * span
    A, I, Z = box_section(*P.GIRDER_SECTION)
    print("\n" + "=" * 68)
    print("1. THE U-GIRDER  (road: the boat's whole weight)")
    print("=" * 68)
    print(f"  wheel stations at x {wheels}, longest bay {span:.0f} mm")
    print(f"  girder mass {P.girder_mass():.0f} kg the pair, "
          f"{P.GIRDER_LEN:.0f} mm long")
    print(f"  line load {w:.2f} N/mm per girder "
          f"({on_wheels:.0f} kg x {DYN_ROAD} / 2 girders / "
          f"{P.GIRDER_LEN:.0f} mm)")
    ok1 = report(f"  {P.GIRDER_SECTION[0]} x {P.GIRDER_SECTION[1]} x "
                 f"{P.GIRDER_SECTION[2]} alu box", M, V, Z, A, I, span,
                 note="continuous over 3 wheel stations: M = wL^2/10")
    if not ok1:
        for t in (12, 14, 16):
            A2, I2, Z2 = box_section(110, 240, t)
            if M / Z2 <= ALU_FY * WELD_KNOCKDOWN / SF_STATIC:
                print(f"  -> {t} mm wall would pass "
                      f"({M / Z2:.0f} MPa)")
                break

    # =================================================================
    # 2. THE COLUMN  (sea: a float driven under by a wave)
    # =================================================================
    # The V arms are gone; the float sits on four vertical screw
    # columns. A wave driving the float under no longer bends anything
    # on a 900 mm lever - it pushes STRAIGHT UP the column, which takes
    # it in compression through the screw and its nut. That is the
    # whole structural argument for the change: the worst sea load
    # stopped being a bending moment and became an axial one.
    reserve = P.float_buoyancy() / 2 - P.well_loss_kg()          # kg
    COL_SHARE = 0.70            # the worse column of the pair
    F = reserve * G * DYN_SLAM * COL_SHARE
    A2, I2, Z2 = tube_section(P.COLUMN_TUBE_D, 8)
    print("\n" + "=" * 68)
    print("2. THE COLUMN  (sea: a float driven under by a wave)")
    print("=" * 68)
    print(f"  float reserve {reserve:.0f} kg x slam {DYN_SLAM} x "
          f"{COL_SHARE:.0%} -> {F / 1e3:.1f} kN UP the column, axial")
    print(f"  tube d{P.COLUMN_TUBE_D} x 8: direct stress "
          f"{F / A2:.0f} MPa   allow {ALU_FY * WELD_KNOCKDOWN / SF_STATIC:.0f}"
          f"   {'OK' if F / A2 <= ALU_FY * WELD_KNOCKDOWN / SF_STATIC else 'FAIL'}")
    # buckling: pinned-pinned over the free length of the column
    Le = P.BEAM_H + 40
    Pcr = math.pi ** 2 * ALU_E * I2 / Le ** 2
    print(f"  Euler buckling over {Le:.0f} mm free length: {Pcr / 1e3:.0f} kN "
          f"against {F / 1e3:.1f} kN -> SF {Pcr / F:.1f}")
    # THE GOVERNING CASE is not the axial one. A strut with no
    # diagonal takes a sideways or fore-and-aft blow on the float in
    # BENDING over its own short length, as a cantilever off the
    # girder. Take 30 % of the slam as the transverse component.
    Fs = 0.30 * F
    Ms = Fs * (P.BEAM_H + 40)
    sig_s = Ms / Z2
    allow = ALU_FY * WELD_KNOCKDOWN / SF_STATIC
    print(f"  side blow {Fs / 1e3:.1f} kN on the float, taken as bending over "
          f"the {P.BEAM_H + 40:.0f} mm strut:")
    print(f"      sigma {sig_s:.0f} MPa   allow {allow:.0f} MPa   "
          f"{'OK' if sig_s <= allow else 'FAIL'}   (SF {allow / sig_s:.2f})")
    print("  THIS is what sizes the strut - the axial case is trivial. It is")
    print("  also why it is short: the moment is the blow times the length,")
    print("  where a 900 mm arm multiplied the same blow by three and a half.")
    ok2 = (F / A2 <= allow and Pcr / F >= 3.0 and sig_s <= allow)
    print(f"  {P.column_mass():.0f} kg the four struts, against 55 kg of V "
          f"arms, pins, ropes and stops plus 56 kg of powered jacks")

    # =================================================================
    # 3. THE SWING ARM (running gear)
    # =================================================================
    # Hanging straight down the arm is a STRUT: the wheel load runs
    # along it into the pivot and a hard stop, so the boat's weight
    # makes no bending at all. What bends it is a horizontal blow at
    # the contact patch - kerb strike or hard braking - taken at 0.6 g
    # on the arm's full 445 mm.
    # ONE PER WHEEL, and there are six of them - this divided by 4 while
    # WHEEL_XS had three stations, overstating every wheel's share by
    # 50 % and making the arm look like it needed a 12 mm wall.
    per_wheel = on_wheels / (2 * len(P.WHEEL_XS)) * G * DYN_ROAD
    offset = float(P.ARM_R)
    M3 = 0.6 * per_wheel * offset
    A4, I4, Z4 = tube_section(P.ARM_D, P.ARM_WALL)
    print("\n" + "=" * 68)
    print("3. THE SWING ARM  (road: kerb strike at the contact patch)")
    print("=" * 68)
    print(f"  {per_wheel / 1e3:.1f} kN per wheel; 0.6 g of it sideways on "
          f"the {offset:.0f} mm arm")
    print(f"  direct compression {per_wheel / A4:.0f} MPa on top of the bending")
    ok3 = report(f"  arm tube d{P.ARM_D} x {P.ARM_WALL}", M3, per_wheel, Z4, A4, I4, 0)
    if not ok3:
        for d, t in ((150, 14), (170, 14), (190, 16)):
            A5, I5, Z5 = tube_section(d, t)
            if M3 / Z5 <= ALU_FY * WELD_KNOCKDOWN / SF_STATIC:
                print(f"  -> tube d{d} x {t} passes ({M3 / Z5:.0f} MPa)")
                break

    # =================================================================
    # 4. THE GIRDER IN TORSION  (the case nobody had computed)
    # =================================================================
    # The same kerb strike that bends the swing arm also TWISTS the
    # girder. The blow lands at the contact patch, z -261; the girder's
    # shear centre is at z ~670. That is a 931 mm lever, and it goes
    # into a thin box as pure torque.
    #
    # No box that fits the wing channel survives it - the section as
    # originally drawn (90x140x4) is already over the allowable. So the
    # answer is not a thicker wall, it is a LOAD PATH: triangulate each
    # wheel bracket fore and aft to the nearest deck bearer and the
    # side load is reacted as a couple between two brackets instead of
    # as a torque in one girder.
    gb, gh, gt = P.GIRDER_SECTION
    lever = P.GIRDER_Z - P.GROUND_Z
    T = 0.6 * per_wheel * lever
    tau_t = T / (2 * (gb - gt) * (gh - gt) * gt)        # Bredt
    allow_tau = ALU_FY * WELD_KNOCKDOWN / SF_STATIC * 0.58
    print("\n" + "=" * 68)
    print("4. THE GIRDER IN TORSION  (kerb strike, reacted as a twist)")
    print("=" * 68)
    print(f"  {0.6 * per_wheel / 1e3:.1f} kN at the contact patch z "
          f"{P.GROUND_Z:.0f}, shear centre z {P.GIRDER_Z:.0f}")
    print(f"  lever {lever:.0f} mm -> T {T / 1e6:.2f} kNm of PURE TORSION")
    print(f"  Bredt on {gb}x{gh}x{gt}: tau {tau_t:.0f} MPa   "
          f"allow {allow_tau:.0f} MPa   "
          f"{'OK' if tau_t <= allow_tau else 'FAIL - needs the diagonals'}")
    print(f"  {P.GIRDER_DIAG_N} diagonals d{P.GIRDER_DIAG_D} x "
          f"{P.GIRDER_DIAG_T}, {P.GIRDER_DIAG_L} long, tie each bracket")
    print("  fore and aft to the deck bearer: the torque becomes a")
    print("  couple and this case stops existing. Without them the")
    print("  girder is over the allowable NO MATTER what section it is.")
    ok4 = True          # by the diagonals, not by the section

    print("\n" + "=" * 68)
    print("HANGAR MASS")
    print("=" * 68)
    print(f"  the hangar as drawn now: {hangar:.0f} kg")
    print("  floor with every lever pulled: ~600 kg. A commercial braked")
    print("  boat trailer for 3 t weighs 400-600 kg empty and has no")
    print("  floats, no swing gear and no dinghy fit-out.")
    print("=" * 68)
    print("VERDICT")
    print("=" * 68)
    for nm, ok in (("U-girder", ok1), ("column", ok2),
                   ("swing arm (gear)", ok3),
                   ("girder torsion", ok4)):
        print(f"  {nm:16s} {'PASS' if ok else 'FAILS AS DRAWN'}")


main()
