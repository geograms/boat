"""Interior renders -> freecad/shots/interior_*.png

Builds the cruise document, hides everything except the fit-out, and
frames it with fitAll (same proven path as capture.py).
Run: ~/bin/FreeCAD.AppImage freecad/interior_shots.py
"""
import os
import sys
import glob
import time

sys.path.insert(0, "/home/brito/code/boat/freecad")
import FreeCAD as App
import FreeCADGui as Gui

OUT = "/home/brito/code/boat/freecad/shots"
for old in glob.glob(OUT + "/interior_*.png"):
    os.remove(old)

sys.argv = ["interior", "cruise"]
exec(open("/home/brito/code/boat/freecad/build_boat.py").read())

KEEP = ("Joinery", "Cushions", "Appliances", "BatteriesTanks", "Fittings")


def frame(doc, tag, view_name, keep_hull=False):
    App.setActiveDocument(doc.Name)
    Gui.ActiveDocument = Gui.getDocument(doc.Name)
    Gui.updateGui()
    for o in doc.Objects:
        vis = any(o.Name.startswith(k) for k in KEEP)
        if keep_hull and o.Name.startswith("Hull"):
            vis = True
        try:
            o.ViewObject.Visibility = vis
        except Exception:
            pass
    Gui.updateGui()
    v = Gui.ActiveDocument.ActiveView
    getattr(v, view_name)()
    v.fitAll()
    Gui.updateGui()
    time.sleep(1.0)
    Gui.updateGui()
    v.saveImage(f"{OUT}/{tag}.png", 2200, 1400, "White")


doc = App.getDocument("boat_cruise")
frame(doc, "interior_top", "viewTop")
frame(doc, "interior_iso", "viewIsometric")
frame(doc, "interior_side", "viewFront")
frame(doc, "interior_iso_hull", "viewIsometric", keep_hull=True)
print("done")
os._exit(0)
