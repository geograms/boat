"""Docking diagnostics -> freecad/shots/dock/<mode>_<view>.png

Beauty shots are useless for this. The hull stands in front of the
hangar in every one of them, so a frame that is 300 mm too high, or a
float driven through the wing, looks perfectly fine. The only way to
see a docking clash is to strip the model to the two things that have
to fit - the HULL and the HANGAR - and look at it square on, in
orthographic, from directly ahead and directly abeam.

Run: xvfb-run -a ~/bin/FreeCAD.AppImage freecad/dock_shots.py
"""
import glob
import json
import os

import FreeCAD as App
import FreeCADGui as Gui

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "shots", "dock")
os.makedirs(OUT, exist_ok=True)
for old in glob.glob(OUT + "/*.png"):
    os.remove(old)

# what has to fit inside what
KEEP = ("Hull", "HangarFrame", "HangarTyres", "HangarLocks",
        "FloatStb", "FloatPort", "WheelForks")

MODES = ["docking", "road", "cruise"]
W, H = 2400, 1500

for mode in MODES:
    path = os.path.join(HERE, f"boat_{mode}.FCStd")
    if not os.path.isfile(path):
        App.Console.PrintWarning(f"dock_shots: no {path}\n")
        continue
    doc = App.openDocument(path)
    look = {}
    lp = os.path.join(HERE, f"boat_{mode}.look.json")
    if os.path.isfile(lp):
        look = json.load(open(lp))

    App.setActiveDocument(doc.Name)
    Gui.ActiveDocument = Gui.getDocument(doc.Name)
    for obj in doc.Objects:
        vp = obj.ViewObject
        if vp is None:
            continue
        vp.Visibility = obj.Name.startswith(KEEP)
        spec = look.get(obj.Name)
        if spec and vp.Visibility:
            try:
                vp.ShapeColor = tuple(spec["color"])
                # the hull half-transparent so a clash INSIDE it shows
                vp.Transparency = 65 if obj.Name == "Hull" else 0
            except Exception:                            # noqa: BLE001
                pass
    Gui.updateGui()
    v = Gui.ActiveDocument.ActiveView
    v.setCameraType("Orthographic")
    # viewFront() on the view object did not take - every image came out
    # axonometric. The message the GUI itself sends does take.
    #   FreeCAD "Front" looks along +Y, so for a boat lying down the x
    #   axis that is the SIDE elevation; "Right" looks along -X and is
    #   the head-on section. The names below are the BOAT's.
    for name, msg in (("side", "ViewFront"), ("headon", "ViewRight"),
                      ("plan", "ViewTop"), ("belly", "ViewBottom"),
                      ("iso", "ViewAxonometric")):
        Gui.SendMsgToActiveView(msg)
        Gui.updateGui()
        Gui.SendMsgToActiveView("ViewFit")
        Gui.updateGui()
        v.saveImage(os.path.join(OUT, f"{mode}_{name}.png"), W, H, "White")
        App.Console.PrintMessage(f"dock_shots: {mode}_{name}\n")
    App.closeDocument(doc.Name)

App.Console.PrintMessage("dock_shots: done\n")
Gui.getMainWindow().close()
