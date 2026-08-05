"""Photo-reference renders -> freecad/shots/beauty/<mode>_<view>.png

The standard captures are orthographic and let the interior show
through the glass, which reads like a cutaway. These are what an
observer outside actually sees: PERSPECTIVE camera at natural eye
heights, interior hidden, glazing closed up, a big water/ground plane
so the horizon never ends inside the frame, rendered large for use as
photo-realistic references.

Run: ~/bin/FreeCAD.AppImage freecad/beauty_shots.py
"""
import os
import sys
import math
import glob
import time

sys.path.insert(0, "/home/brito/code/boat/freecad")
import FreeCAD as App
import FreeCADGui as Gui
import Part
from FreeCAD import Vector, Rotation

OUT = "/home/brito/code/boat/freecad/shots/beauty"
os.makedirs(OUT, exist_ok=True)
for old in glob.glob(OUT + "/*.png"):
    os.remove(old)

MODES = ["cruise", "road", "harbor", "launch", "anchor"]
sys.argv = ["beauty"] + MODES
exec(open("/home/brito/code/boat/freecad/build_boat.py").read())

W, H = 2800, 1750

# anything that lives inside the cabin must not show through the glass
INSIDE = ("Joinery", "Cushions", "Appliances", "BatteriesTanks", "Fittings")
GLASSY = ("Glazing", "FrontDome", "DoorGlass", "WalkOnGlass")

CX = P.LOA / 2                      # boat centre, for aiming the camera


def look_at(view, eye, target):
    """Point a perspective camera at target with world +Z up.

    Uses the Inventor camera STRING api: view.getCameraNode() needs the
    pivy SWIG bindings, which are not loaded in this headless-GUI run."""
    eye_v, tgt_v = Vector(*eye), Vector(*target)
    fwd = tgt_v - eye_v
    dist = fwd.Length
    fwd.normalize()
    rot = Rotation(Vector(0, 0, -1), fwd)          # camera looks down -Z
    up_now = rot.multVec(Vector(0, 1, 0))
    world_up = Vector(0, 0, 1)
    up_want = world_up - fwd * world_up.dot(fwd)   # up, perpendicular to fwd
    if up_want.Length > 1e-6:
        up_want.normalize()
        ang = math.atan2(fwd.dot(up_now.cross(up_want)), up_now.dot(up_want))
        rot = Rotation(fwd, math.degrees(ang)).multiply(rot)
    ax = rot.Axis
    view.setCamera(
        "#Inventor V2.1 ascii\n\n"
        "PerspectiveCamera {\n"
        f"  position {eye[0]:.1f} {eye[1]:.1f} {eye[2]:.1f}\n"
        f"  orientation {ax.x:.6f} {ax.y:.6f} {ax.z:.6f} {rot.Angle:.6f}\n"
        "  nearDistance 400\n  farDistance 500000\n"
        f"  focalDistance {dist:.1f}\n  heightAngle 0.82\n}}\n")


def view_points(sea):
    """(name, eye, target) — natural viewpoints for an outside observer."""
    z0 = P.WL_Z if sea else P.GROUND_Z
    aim = (CX, 0, z0 + 1200)
    return [
        ("bow_quarter", (CX + 7600, -5400, z0 + 1700), aim),
        ("stern_quarter", (CX - 7200, 5600, z0 + 1750), aim),
        ("beam", (CX + 600, -9200, z0 + 1600), (CX, 0, z0 + 1250)),
        ("drone", (CX + 6200, -6200, z0 + 6200), (CX, 0, z0 + 800)),
        ("low", (CX + 5200, -3800, z0 + 420), (CX, 0, z0 + 1400)),
    ]


for mode in MODES:
    doc = App.getDocument("boat_" + mode)
    App.setActiveDocument(doc.Name)
    Gui.ActiveDocument = Gui.getDocument(doc.Name)
    Gui.updateGui()
    sea = mode not in ("road", "launch")

    for o in doc.Objects:
        try:
            if o.Name.startswith(INSIDE):
                o.ViewObject.Visibility = False       # no cutaway look
            elif o.Name.startswith(GLASSY):
                o.ViewObject.Transparency = 30        # real glass, not open
                if o.Name.startswith("FrontDome"):
                    # shaded, no facet wireframe: the dome must read as
                    # a smooth glass cap, not as a mesh
                    o.ViewObject.DisplayMode = "Shaded"
                    o.ViewObject.Transparency = 42
                if o.Name.startswith("WalkOnGlass"):
                    o.ViewObject.Transparency = 45
            elif o.Name in ("Water", "Ground", "Slipway"):
                o.ViewObject.Visibility = False       # replaced, see below
        except Exception:
            pass

    # one big plane so the surface never ends inside the frame
    plane = doc.addObject("Part::Feature", "Seascape")
    z = P.WL_Z if sea else P.GROUND_Z
    plane.Shape = Part.makeBox(90000, 90000, 30,
                               Vector(CX - 45000, -45000, z - 30))
    plane.ViewObject.ShapeColor = ((0.42, 0.60, 0.74) if sea
                                   else (0.55, 0.55, 0.55))
    plane.ViewObject.Transparency = 15 if sea else 0
    doc.recompute()

    view = Gui.ActiveDocument.ActiveView
    Gui.updateGui()

    for name, eye, target in view_points(sea):
        look_at(view, eye, target)
        Gui.updateGui()
        time.sleep(0.6)
        Gui.updateGui()
        view.saveImage(f"{OUT}/{mode}_{name}.png", W, H, "White")
        print("wrote", mode, name)

print("done")
os._exit(0)
