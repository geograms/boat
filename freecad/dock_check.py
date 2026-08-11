"""Does the hangar actually FIT under the boat? Solid intersection test.

Renders cannot answer this. The hull stands in front of the hangar in
every beauty shot, and even a stripped orthographic view only shows a
clash if it happens to be on the silhouette. The only honest test is
boolean: intersect the hull with every part of the hangar and measure
the volume that comes back. Zero, or it does not fit.

Run headless and GREP THE LOG - FreeCAD exits 0 even when this throws:
  ~/bin/FreeCAD.AppImage --console dock_check.py < /dev/null
"""
import os
import sys

import FreeCAD as App

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import params as P                                          # noqa: E402
import build_boat as B                                      # noqa: E402

TOL = 1e5            # mm3 = 0.1 litre. Below this is boolean noise on a
                     # 2.4 m3 hull, not a real overlap.


def check(mode):
    cfg = P.MODES[mode]
    hull = B.build_hull()
    pod = P.pod_at(cfg["phi"])
    fx = P.float_x(cfg["phi"])
    fl = B.build_float(pod, 0, P.float_yaw(cfg["phi"]), fx)[0]
    frame, locks, tyres = B.build_hangar(
        cfg["phi"], cfg.get("coupled", True), cfg["tow"],
        drop=P.dock_gap() if cfg.get("drop") else 0.0,
        standoff_x=cfg.get("standoff_x"), deck=cfg.get("deck", True),
        wheels_down=cfg.get("wheels_down"))

    off = None
    if not cfg.get("coupled", True):
        sx = cfg.get("standoff_x") or P.HANGAR_STANDOFF
        off = App.Placement(App.Vector(sx, 0, P.hangar_standoff_z()),
                            App.Rotation())

    def place(shape):
        if off is None or shape is None:
            return shape
        s = shape.copy()
        s.Placement = off.multiply(s.Placement)
        return s

    for nm, sh in (("hull", hull), ("float", fl), ("frame", frame)):
        b = sh.BoundBox
        print(f"  {nm:6s} spans x {b.XMin:7.0f}..{b.XMax:<7.0f} "
              f"y {b.YMin:7.0f}..{b.YMax:<7.0f} z {b.ZMin:7.0f}..{b.ZMax:<7.0f}")
    parts = [("float stbd", place(fl)),
             ("float port", place(B.mirror_y(fl))),
             ("frame", frame), ("tyres", tyres)]

    print("=" * 68)
    print(f"DOES IT FIT - mode '{mode}'")
    print("=" * 68)
    print(f"  frame dropped {P.dock_gap() if cfg.get('drop') else 0:.0f} mm, "
          f"floats at phi {cfg['phi']:.0f}, "
          f"standing off x {cfg.get('standoff_x') or 0:.0f}")
    print(f"  hull volume {hull.Volume / 1e9:.4f} m3")
    worst = 0.0
    for name, shp in parts:
        if shp is None:
            continue
        try:
            common = hull.common(shp)
            v = common.Volume
        except Exception as exc:                            # noqa: BLE001
            print(f"  {name:12s} BOOLEAN FAILED: {exc}")
            worst = max(worst, TOL * 10)
            continue
        worst = max(worst, v)
        if v > TOL:
            bb = common.BoundBox
            print(f"  {name:12s} CLASH {v / 1e9:.5f} m3")
            print(f"               x {bb.XMin:8.0f}..{bb.XMax:<8.0f} "
                  f"y {bb.YMin:7.0f}..{bb.YMax:<7.0f} "
                  f"z {bb.ZMin:7.0f}..{bb.ZMax:<7.0f}")
            # WHICH member? a compound-wide bounding box tells you
            # nothing useful - it is the union of every clash at once.
            sols = shp.Solids or [shp]
            for i, sol in enumerate(sols):
                try:
                    c = hull.common(sol)
                except Exception:                           # noqa: BLE001
                    continue
                if c.Volume > TOL / 10:
                    b, o = sol.BoundBox, c.BoundBox
                    print(f"      solid {i:3d}  {c.Volume / 1e9:.5f} m3")
                    print(f"          member x {b.XMin:7.0f}..{b.XMax:<7.0f} "
                          f"y {b.YMin:6.0f}..{b.YMax:<6.0f} "
                          f"z {b.ZMin:6.0f}..{b.ZMax:<6.0f}")
                    print(f"          OVERLAP x {o.XMin:7.0f}..{o.XMax:<7.0f} "
                          f"y {o.YMin:6.0f}..{o.YMax:<6.0f} "
                          f"z {o.ZMin:6.0f}..{o.ZMax:<6.0f}")
        else:
            print(f"  {name:12s} clear")
    print("-" * 68)
    print("  VERDICT: " + ("FITS" if worst <= TOL else "DOES NOT FIT"))
    return worst <= TOL


# FreeCAD's own argv comes through here too - "--console" is not a mode
ok = True
for m in ([a for a in sys.argv if a in P.MODES] or ["docking"]):
    ok = check(m) and ok
print("\nALL CLEAR" if ok else "\nCLASHES REMAIN")
