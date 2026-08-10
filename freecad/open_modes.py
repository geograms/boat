"""Open saved boat_*.FCStd files so you can actually SEE them.

Opening a document is not the same as being able to see it, and this
model is built HEADLESS - `--console`, no GUI, because a GUI build is
about ten times slower. A headless save writes Document.xml and no
GuiDocument.xml at all: there are no view providers to save.

Open such a file afterwards and FreeCAD invents the view state from
nothing:

  * every object comes up HIDDEN
  * every colour is default grey
  * there is no camera, so ViewFit has nothing to fit and you get an
    empty window zoomed to a few millimetres

The tree is fully populated the whole time, which is what makes it look
like the file is broken when it is perfectly fine. It cost three
rounds of "boat_detached will not load" before the cause was found in
the zip: no GuiDocument.xml.

So this script does not trust the file's view state. It opens each
document, makes everything visible, re-applies the colours that
build_boat.py recorded in boat_<mode>.look.json, and fits the view.

Modes come from the BOAT_MODES environment variable, space separated.
"""
import json
import os

import FreeCAD as App

HERE = os.path.dirname(os.path.abspath(__file__))
INSIDE = ("Joinery", "Cushions", "Appliances", "BatteriesTanks", "Fittings")

modes = os.environ.get("BOAT_MODES", "").split()
opened = []

for m in modes:
    path = os.path.join(HERE, f"boat_{m}.FCStd")
    if not os.path.isfile(path):
        App.Console.PrintWarning(f"open_modes: no {path}\n")
        continue
    opened.append((m, App.openDocument(path)))

if not opened:
    App.Console.PrintError("open_modes: nothing opened\n")

if App.GuiUp:
    import FreeCADGui as Gui

    for m, doc in opened:
        look = {}
        lp = os.path.join(HERE, f"boat_{m}.look.json")
        if os.path.isfile(lp):
            with open(lp) as fh:
                look = json.load(fh)

        shown = 0
        for obj in doc.Objects:
            vp = obj.ViewObject
            if vp is None:
                continue
            # EVERYTHING visible. A headless save left no view data, so
            # the default is hidden and the whole model is invisible.
            vp.Visibility = True
            shown += 1
            spec = look.get(obj.Name)
            if spec:
                try:
                    vp.ShapeColor = tuple(spec["color"])
                    vp.Transparency = int(spec["transparency"])
                except Exception:                        # noqa: BLE001
                    pass
        # the interior would otherwise show through the glazing and read
        # as a cutaway
        for obj in doc.Objects:
            if obj.Name.startswith(INSIDE) and obj.ViewObject:
                obj.ViewObject.Visibility = False

        App.setActiveDocument(doc.Name)
        Gui.ActiveDocument = Gui.getDocument(doc.Name)
        Gui.updateGui()
        try:
            Gui.ActiveDocument.ActiveView.viewAxonometric()
            Gui.SendMsgToActiveView("ViewFit")
        except Exception as exc:                         # noqa: BLE001
            App.Console.PrintWarning(f"open_modes: no view for {m}: {exc}\n")
        Gui.updateGui()
        App.Console.PrintMessage(
            f"open_modes: boat_{m} - {shown} objects shown, "
            f"{len(look)} colours applied\n")

    # leave the FIRST mode asked for in front, not the last one loaded
    App.setActiveDocument(opened[0][1].Name)
    Gui.ActiveDocument = Gui.getDocument(opened[0][1].Name)
    Gui.SendMsgToActiveView("ViewFit")
