#!/usr/bin/env bash
# Build the boat and open it in FreeCAD with colours applied.
#   ./view.sh                  -> all modes
#   ./view.sh cruise           -> just cruise
#   ./view.sh road detached    -> any of: road launch harbor cruise
#                                         anchor deck detached
#
# It returns immediately. FreeCAD runs DETACHED and NICED, so building
# seven modes does not lock the desktop up on a 16 GB machine: it used
# to run in the foreground at normal priority, hold the terminal, and
# starve everything else while OCC chewed through the lofts.
#
#   -f / --fg   run in the foreground instead (for debugging)
#   -q          just build, no GUI (uses --console, much faster)
set -u
cd "$(dirname "$0")"

FG=0
CONSOLE=0
ARGS=()
for a in "$@"; do
    case "$a" in
        -f|--fg) FG=1 ;;
        -q|--quiet|--console) CONSOLE=1 ;;
        *) ARGS+=("$a") ;;
    esac
done

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
    echo "view.sh: clearing a stale /tmp/FreeCAD socket"
    rm -f /tmp/FreeCAD
fi

LOG="${TMPDIR:-/tmp}/boat-view.log"
BIN=~/bin/FreeCAD.AppImage

# nice + ionice keep the desktop responsive while OCC works. The build
# is CPU-bound for minutes; without this the machine is unusable.
RUN=(nice -n 12 "$BIN")
command -v ionice > /dev/null && RUN=(ionice -c2 -n6 "${RUN[@]}")

if [ "$CONSOLE" = 1 ]; then
    # headless: no GUI, and stdin closed so --console cannot drop into
    # its interactive prompt and hang
    "${RUN[@]}" --console build_boat.py "${ARGS[@]:-}" < /dev/null
    rc=$?
    exit $rc
fi

if [ "$FG" = 1 ]; then
    exec "${RUN[@]}" build_boat.py "${ARGS[@]:-}"
fi

# Detached: its own session, so closing the terminal does not kill it
# and it never holds the shell.
setsid "${RUN[@]}" build_boat.py "${ARGS[@]:-}" > "$LOG" 2>&1 < /dev/null &
PID=$!
disown 2>/dev/null || true
echo "view.sh: FreeCAD started detached, pid $PID (nice 12)"
echo "         building ${#ARGS[@]} mode(s); the window appears when it is done"
echo "         log: $LOG"
echo "         a build of all seven modes takes a few minutes"

# screenshots: ~/bin/FreeCAD.AppImage beauty_shots.py -> shots/beauty/
