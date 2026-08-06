#!/usr/bin/env python3
"""Measure the laminated surface areas off the FreeCAD solids.

Structural mass has to come from geometry, not from prose. This builds
the cruise model, measures the faces that are actually laminated, and
writes freecad/areas.json, which params.py reads.

Run: ~/bin/FreeCAD.AppImage freecad/areas.py
"""
import json
import os
import sys

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, SCRIPT_DIR)

import params as P                                   # noqa: E402
import build_boat as B                               # noqa: E402
import FreeCAD as App                                # noqa: E402
import Part                                          # noqa: E402


def area_m2(shape):
    return shape.Area / 1e6


def below(shape, z):
    """Area of the faces whose centre of mass sits below z."""
    return sum(f.Area for f in shape.Faces
               if f.CenterOfMass.z < z) / 1e6


def main():
    out = {}

    # ---- hull: split at the chine, and take the deck plate separately
    hull = B.build_hull()
    z_chine = sum(s[4] for s in P.STATIONS[:6]) / 6        # ~233 mm
    z_deck = P.CABIN_BASE_Z - 60
    bottom = topsides = deck = 0.0
    for f in hull.Faces:
        c = f.CenterOfMass
        if c.z >= z_deck:
            deck += f.Area
        elif c.z < z_chine:
            bottom += f.Area
        else:
            topsides += f.Area
    # the hull solid is a shell: outer and inner faces both counted, and
    # only the outer one is a laminate surface
    out["hull_bottom"] = bottom / 2e6
    out["hull_topsides"] = topsides / 2e6
    out["hull_deck"] = deck / 2e6

    # ---- floats: shell versus the flat top the hardware lands on
    fl = B.build_float(P.pod_at(P.PHI_WATER), 0)[0]      # hull shell only
    top_z = max(v.Point.z for v in fl.Vertexes) - 1
    ftop = sum(f.Area for f in fl.Faces if f.CenterOfMass.z > top_z) / 1e6
    out["float_deck"] = 2 * ftop
    out["float_shell"] = 2 * (area_m2(fl) - ftop)

    # ---- cabin: walls net of the openings the model already cuts
    cabin, _panes = B.build_cabin()
    walls = 0.0
    roof_z = P.CABIN_ROOF_Z - 5
    for f in cabin.Faces:
        if f.CenterOfMass.z < roof_z:
            walls += f.Area
    out["cabin_walls"] = walls / 2e6         # shell again: two faces per wall

    # ---- roof sandwich: the structural roof under the glass deck
    tl, tw, _cx = B.terrace_plan()
    out["roof_sandwich"] = tl * tw / 1e6

    # ---- bulkheads: transverse webs at the frame stations
    bh = 0.0
    for x in P.BULKHEAD_X:
        hw, zs = P.sheer_at(x)
        for st in P.STATIONS:
            if abs(st[0] - x) < 700:
                bh += (2 * hw) * (zs - st[3]) * 0.72      # net of limber/access
                break
    out["bulkheads"] = bh / 1e6

    path = os.path.join(SCRIPT_DIR, "areas.json")
    with open(path, "w") as fh:
        json.dump({k: round(v, 3) for k, v in sorted(out.items())}, fh, indent=2)
    print("wrote", path)
    for k, v in sorted(out.items()):
        print(f"  {k:16s} {v:7.2f} m2")
    print(f"  {'TOTAL':16s} {sum(out.values()):7.2f} m2")


main()
