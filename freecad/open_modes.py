"""Open saved boat_*.FCStd files and FIT THE VIEW.

Opening a document is not the same as being able to see it. These files
are written by a HEADLESS build, so their GuiDocument.xml carries no
useful camera - open one directly and FreeCAD shows you an empty grey
window zoomed to a few millimetres, with the whole model somewhere off
screen. It looks exactly like the file failed to load.

So view.sh runs this instead of passing the filenames to FreeCAD: it
opens each one, points the camera isometrically and fits it.

Modes come from the BOAT_MODES environment variable, space separated.
"""
import os
import sys

import FreeCAD as App

HERE = os.path.dirname(os.path.abspath(__file__))
modes = os.environ.get("BOAT_MODES", "").split()

opened = []
for m in modes:
    path = os.path.join(HERE, f"boat_{m}.FCStd")
    if not os.path.isfile(path):
        App.Console.PrintWarning(f"open_modes: no {path}\n")
        continue
    opened.append((m, App.openDocument(path)))
    App.Console.PrintMessage(f"open_modes: opened boat_{m}\n")

if App.GuiUp and opened:
    import FreeCADGui as Gui
    for m, doc in opened:
        App.setActiveDocument(doc.Name)
        Gui.ActiveDocument = Gui.getDocument(doc.Name)
        Gui.updateGui()
        try:
            view = Gui.ActiveDocument.ActiveView
            view.viewAxonometric()
            Gui.SendMsgToActiveView("ViewFit")
        except Exception as exc:                     # noqa: BLE001
            App.Console.PrintWarning(f"open_modes: no view for {m}: {exc}\n")
        Gui.updateGui()
    # leave the FIRST mode asked for in front, not the last one loaded
    App.setActiveDocument(opened[0][1].Name)
    Gui.ActiveDocument = Gui.getDocument(opened[0][1].Name)
    Gui.SendMsgToActiveView("ViewFit")
