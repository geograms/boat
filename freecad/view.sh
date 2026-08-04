#!/usr/bin/env bash
# Build the boat and open it in FreeCAD with colors applied.
#   ./view.sh                 -> cruise, road, foiling
#   ./view.sh road            -> just road mode
#   ./view.sh anchor harbor   -> any of: road launch harbor cruise anchor foiling
cd "$(dirname "$0")"
exec ~/bin/FreeCAD.AppImage build_boat.py "$@"
# screenshots: ~/bin/FreeCAD.AppImage freecad/capture.py  -> freecad/shots/
