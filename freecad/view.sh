#!/usr/bin/env bash
# Build the boat and open it in FreeCAD with colors applied.
#   ./view.sh                  -> all modes
#   ./view.sh cruise           -> just cruise
#   ./view.sh road detached    -> any of: road launch harbor cruise anchor
#                                         deck detached alongside
cd "$(dirname "$0")"

# A FreeCAD killed mid-run leaves its single-instance socket behind, and
# every later launch blocks forever trying to hand off to a dead
# process. Clear it, but only when no FreeCAD is actually running.
if [ -S /tmp/FreeCAD ] && ! pgrep -f FreeCAD.AppImage > /dev/null; then
    rm -f /tmp/FreeCAD
fi

exec ~/bin/FreeCAD.AppImage build_boat.py "$@"
# screenshots: ~/bin/FreeCAD.AppImage beauty_shots.py -> shots/beauty/
