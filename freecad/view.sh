#!/usr/bin/env bash
# OPEN the boat in FreeCAD.
#   ./view.sh                  -> every mode
#   ./view.sh detached         -> just that one
#   ./view.sh road detached    -> any of: road launch harbor cruise
#                                         anchor deck detached
#
# It OPENS the saved .FCStd files. It does not rebuild them, and that
# is the point: building a mode with the GUI up means FreeCAD makes a
# view provider for every shape, which is minutes per mode - all seven
# would not finish inside ten. Opening the same file takes seconds.
# The old default rebuilt everything before showing anything, so a
# single mode looked like it was "not loading" when it was queued
# behind six others.
#
# Rebuild explicitly when the model has changed:
#   -b / --build   rebuild HEADLESS first (fast), then open
#   -q / --console rebuild headless, no window
#   -f / --fg      run in the foreground (for debugging)
#
# FreeCAD runs DETACHED and NICED either way, so it never holds the
# terminal or starves the desktop on a 16 GB machine.
set -u
cd "$(dirname "$0")"

FG=0
CONSOLE=0
BUILD=0
ARGS=()
for a in "$@"; do
    case "$a" in
        -f|--fg) FG=1 ;;
        -q|--quiet|--console) CONSOLE=1; BUILD=1 ;;
        -b|--build) BUILD=1 ;;
        *) ARGS+=("$a") ;;
    esac
done
ALL=(road launch harbor cruise anchor deck detached)
# Default to ONE mode. Opening all seven means seven copies of the
# model in memory - about 1.5 GB each with view providers - and on a
# 16 GB desktop that is what pushes the machine into swap and freezes
# everything, terminal included. Ask for `all` if you really want them.
if [ ${#ARGS[@]} -eq 0 ]; then
    ARGS=(detached)
elif [ "${ARGS[0]}" = "all" ]; then
    ARGS=("${ALL[@]}")
fi

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

# MEMORY, not CPU, is what freezes this machine. nice only bounds the
# processor; FreeCAD loading the model wants a couple of gigabytes, and
# with the desktop already at 11 of 15 GB that goes straight into swap
# and takes the whole session down with it.
#
# So run it in its own cgroup scope with a memory ceiling: it gets
# throttled and reclaimed instead of dragging everything else into
# swap. MemoryHigh throttles, MemoryMax is the hard stop.
AVAIL=$(awk '/MemAvailable/{printf "%d", $2/1024}' /proc/meminfo)
SWAPUSED=$(awk '/SwapTotal/{t=$2} /SwapFree/{f=$2} END{printf "%d", (t-f)/1024}' /proc/meminfo)
HIGH=$(( AVAIL > 3000 ? 2500 : AVAIL * 2 / 3 ))
[ "$HIGH" -lt 700 ] && HIGH=700
MAXM=$(( HIGH + 800 ))
if [ "$AVAIL" -lt 1500 ]; then
    echo "view.sh: WARNING only ${AVAIL} MB of RAM available and ${SWAPUSED} MB"
    echo "         of swap already in use. FreeCAD will be capped at"
    echo "         ${MAXM} MB so it cannot freeze the desktop, but it may"
    echo "         be slow or get killed. Close something first."
fi
LIMIT=()
if command -v systemd-run > /dev/null; then
    LIMIT=(systemd-run --user --scope --quiet
           --unit="boat-view-$$"
           -p MemoryHigh=${HIGH}M -p MemoryMax=${MAXM}M
           -p CPUWeight=20 --)
fi

# nice + ionice keep the desktop responsive while OCC works. The build
# is CPU-bound for minutes; without this the machine is unusable.
RUN=(nice -n 12 "$BIN")
command -v ionice > /dev/null && RUN=(ionice -c2 -n6 "${RUN[@]}")
RUN=("${LIMIT[@]}" "${RUN[@]}")

if [ "$BUILD" = 1 ]; then
    # headless build: no view providers, so it is ~10x faster. stdin
    # closed so --console cannot drop into its prompt and hang.
    echo "view.sh: rebuilding ${ARGS[*]} headless..."
    if ! "${RUN[@]}" --console build_boat.py "${ARGS[@]}" < /dev/null \
            > "$LOG" 2>&1; then
        echo "view.sh: BUILD FAILED - see $LOG" >&2
        exit 1
    fi
    # FreeCAD exits 0 even when the script throws, so check the log
    if grep -qiE "exception|traceback" "$LOG"; then
        echo "view.sh: the build threw - NOT opening a stale model:" >&2
        grep -iE "exception|traceback" "$LOG" | head -3 >&2
        exit 1
    fi
    echo "view.sh: built."
fi

[ "$CONSOLE" = 1 ] && exit 0

FOUND=()
for m in "${ARGS[@]}"; do
    if [ -f "$PWD/boat_$m.FCStd" ]; then
        FOUND+=("$m")
    else
        echo "view.sh: no boat_$m.FCStd - run './view.sh -b $m' first" >&2
    fi
done
[ ${#FOUND[@]} -eq 0 ] && { echo "view.sh: nothing to open" >&2; exit 1; }

# Do NOT hand the filenames to FreeCAD directly. These files come from a
# headless build, so they carry no camera: FreeCAD opens them and shows
# an empty grey window zoomed to a few millimetres, which looks exactly
# like the file failed to load. open_modes.py opens them and fits the
# view.
export BOAT_MODES="${FOUND[*]}"

if [ "$FG" = 1 ]; then
    exec "${RUN[@]}" open_modes.py
fi

# Detached: its own session, so closing the terminal does not kill it
# and it never holds the shell.
setsid "${RUN[@]}" open_modes.py > "$LOG" 2>&1 < /dev/null &
PID=$!
disown 2>/dev/null || true
echo "view.sh: opening ${#FOUND[@]} document(s), pid $PID"
echo "         ${FOUND[*]}"
echo "         nice 12, memory capped at ${MAXM} MB (${AVAIL} MB free now)"
echo "         log: $LOG"

# screenshots: ~/bin/FreeCAD.AppImage beauty_shots.py -> shots/beauty/
