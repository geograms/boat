import os, sys
sys.path.insert(0, "/home/brito/code/boat/freecad")
import FreeCAD as App
import FreeCADGui as Gui

OUT = "/home/brito/code/boat/freecad/shots"
os.makedirs(OUT, exist_ok=True)
# fresh captures only — stale screenshots cause confusion
import glob
for old in glob.glob(OUT + "/*.png"):
    os.remove(old)
sys.argv = ["capture", "road", "launch", "harbor", "cruise", "anchor"]
exec(open("/home/brito/code/boat/freecad/build_boat.py").read())

PLANES = ("Ground", "Water", "Slipway")

for mode in ("road", "launch", "harbor", "cruise", "anchor"):
    doc = App.getDocument("boat_" + mode)
    App.setActiveDocument(doc.Name)
    Gui.ActiveDocument = Gui.getDocument(doc.Name)
    Gui.updateGui()
    view = Gui.ActiveDocument.ActiveView
    planes = [doc.getObject(n) for n in PLANES if doc.getObject(n)]
    for vp, name in ((view.viewIsometric, "iso"), (view.viewFront, "side"),
                     (view.viewRight, "bow")):
        for p in planes:
            p.ViewObject.Visibility = False
        vp()
        view.fitAll()          # frame the boat, not the 13 m plane
        for p in planes:
            p.ViewObject.Visibility = True
        Gui.updateGui()
        view.saveImage(f"{OUT}/{mode}_{name}.png", 2000, 1250, "White")
print("shots done")
os._exit(0)
