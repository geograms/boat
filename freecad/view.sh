#!/usr/bin/env bash
# Build the boat and open it in FreeCAD with colors applied.
#   ./view.sh                  -> all modes
#   ./view.sh cruise           -> just cruise
#   ./view.sh road detached    -> any of: road launch harbor cruise anchor
#                                         deck detached alongside
cd "$(dirname "$0")"

# A FreeCAD killed mid-run leaves its single-instance socket behind, and
# every later launch blocks forever trying to hand off to a dead
# process - the document appears not to load at all. Clear it, but only
# when no FreeCAD is actually running.
#
# Match the BINARY, not the command line: `pgrep -f FreeCAD.AppImage`
# also matches any shell whose command line merely mentions it, which
# made this guard silently decide FreeCAD was running when it was not.
if [ -S /tmp/FreeCAD ] && ! pgrep -x FreeCAD > /dev/null \
   && ! ps -eo cmd | grep -qE "^[^ ]*bin/FreeCAD"; then
    rm -f /tmp/FreeCAD
fi

exec ~/bin/FreeCAD.AppImage build_boat.py "$@"
# screenshots: ~/bin/FreeCAD.AppImage beauty_shots.py -> shots/beauty/
