#!/usr/bin/env python3
"""Resistance, speed and range model -> the tables in docs/performance.md

First-order estimate: ITTC friction line plus a residuary factor fitted
to barge data. Run: python3 docs/perf_model.py
"""
import math
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                "..", "freecad"))
import params as P                                          # noqa: E402

# ONE mass figure for the project: the computed budget, loaded. Wired to
# params so the speed and range tables move when the boat gains weight.
DISP = round(P.mass_budget()[1] + P.CREW_STORES)
T = P.draft_for(DISP) / 1000.0     # m, the waterline that follows from it
LWL, B = 6.60, 2.50
S = LWL * (1.7 * T + B * 0.75) + 2 * 6.2 * (1.7 * 0.30 + 0.6 * 0.70)
RHO, NU = 1025, 1.19e-6
ETA = 0.45                         # waterjet propulsive efficiency
P_INSTALLED = 6.0                  # kW
BATT, DOD = P.BATT_KWH, 0.9
HOUSE = 2.5                        # kWh/day


def resistance(V):
    """(total resistance N, Froude number) at V m/s."""
    Cf = 0.075 / (math.log10(V * LWL / NU) - 2) ** 2
    Rf = 0.5 * RHO * V * V * S * Cf
    Fn = V / math.sqrt(9.81 * LWL)
    f = 0.6 + 140 * max(Fn - 0.20, 0) ** 1.7
    return Rf * (1 + f), Fn


def shaft_kw(V):
    Rt, _ = resistance(V)
    return Rt * V / ETA / 1000


def max_speed():
    lo, hi = 1.0, 4.0
    for _ in range(80):
        mid = (lo + hi) / 2
        lo, hi = (mid, hi) if shaft_kw(mid) < P_INSTALLED else (lo, mid)
    return lo / 0.5144


if __name__ == "__main__":
    print(f"wetted surface {S:.1f} m2, displacement {DISP} kg, "
          f"{P_INSTALLED:.0f} kW installed\n")
    print(f"{'kn':>6} {'Fn':>6} {'Rt N':>7} {'kW':>6} {'NM':>6} {'hours':>7}")
    for kn in (2.0, 3.0, 3.5, 4.0, 4.5):
        V = kn * 0.5144
        Rt, Fn = resistance(V)
        kw = shaft_kw(V)
        hrs = BATT * DOD / kw
        print(f"{kn:6.1f} {Fn:6.3f} {Rt:7.0f} {kw:6.2f} {hrs*kn:6.0f} {hrs:7.1f}")
    vmax = max_speed()
    print(f"\nmaximum on {P_INSTALLED:.0f} kW: {vmax:.1f} kn")
    print(f"theoretical hull speed:   "
          f"{1.34 * math.sqrt(LWL * 3.281):.1f} kn (needs "
          f"{shaft_kw(1.34 * math.sqrt(LWL * 3.281) * 0.5144):.0f} kW)\n")
    for solar, label in ((24, "good summer day"), (12, "spring/autumn"),
                         (6, "overcast winter")):
        avail = solar - HOUSE
        lo, hi = 0.5, vmax
        for _ in range(60):
            mid = (lo + hi) / 2
            lo, hi = (mid, hi) if shaft_kw(mid * 0.5144) * 8 < avail else (lo, mid)
        print(f"{label:18} {solar:2.0f} kWh/day -> solar-neutral at "
              f"{lo:.1f} kn for 8 h")
