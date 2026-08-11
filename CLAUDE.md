# Working on this repo

`freecad/params.py` is the single source of truth. `checks()` asserts
every legal, structural and hydrostatic limit. Geometry lives in
`build_boat.py`, scantlings in `structure_calc.py`. Change a number in
params, never in the builder.

---

## Producing FreeCAD drawings — the procedure that works

Learned the hard way, repeatedly. Follow it in order.

### 1. FreeCAD exits 0 even when the script throws

This is the single most expensive trap in this repo. A Python exception
inside a script run by `--console` is caught by FreeCAD, printed to
stdout as one line, and **the process still exits 0**:

```
Exception while processing file: build_boat.py [module 'params' has no attribute 'BEAM_H']
```

A silent run is *not* a good run. The saved `.FCStd` files are simply
left at their previous contents, so every later render is of stale
geometry and looks perfectly fine while being two rewrites out of date.

**Always capture and grep:**

```bash
timeout 590 ~/bin/FreeCAD.AppImage --console build_boat.py < /dev/null > /tmp/b.log 2>&1
grep -iE "exception|traceback|error" /tmp/b.log   # must be empty
```

### 2. After renaming or deleting anything in params, sweep for orphans

Deleting a params block while builders still reference it is what
causes §1. Sweep before building:

```bash
python3 - <<'PY'
import re, sys; sys.path.insert(0,'freecad'); import params as P
for f in ('freecad/build_boat.py','freecad/structure_calc.py',
          'freecad/areas.py','freecad/ga_drawing.py'):
    for n in set(re.findall(r"\bP\.([A-Za-z_]\w*)", open(f).read())):
        if not hasattr(P, n): print(f, n)
PY
```

Also watch for **name collisions**: `RAIL_GAP` already meant the solar
rail shadow gap, and a second definition later in the file silently
overwrote the new one. Grep before naming.

### 3. Never run FreeCAD in the user's session

FreeCAD is single-instance through a socket in the system temp dir. If
Max has the GUI open, a headless run **hands the script off into his
session** — his tabs fill with my documents and my process hangs
forever. Isolate with a private temp dir:

```bash
export TMPDIR=$CLAUDE_JOB_DIR/tmp/fctmp   # mkdir -p first
```

**A stale socket is the "the file will not open" symptom.** A FreeCAD
that exits badly leaves `/tmp/FreeCAD` behind; every later launch then
tries to hand the document to a process that no longer exists and
appears to do nothing at all. The document is fine — check it headless
before suspecting it:

```bash
ps -eo cmd | grep -E "^[^ ]*bin/FreeCAD"      # is one really running?
rm -f /tmp/FreeCAD                            # only if not
```

Do **not** test with `pgrep -f FreeCAD.AppImage`: it matches any shell
whose command line merely mentions the string — including our own
polling loops — so it reports "running" when nothing is. `view.sh` had
this bug and it is why the guard never fired.

`--console` also drops to an interactive prompt and hangs unless stdin
is redirected: always `< /dev/null`.

**A headless-built file has NO GUI DOCUMENT AT ALL.** This is the root
cause of every "boat_detached will not load" report, and it took three
rounds to find because the symptom points at the file:

```bash
python3 -c "import zipfile; print(zipfile.ZipFile('boat_detached.FCStd').namelist())"
# ['Document.xml']          <- headless build: no GuiDocument.xml
# ['Document.xml', 'GuiDocument.xml']   <- was saved by a GUI run
```

`--console` has no GUI, so there are no view providers to save. Open
such a file afterwards and FreeCAD invents the view state: **every
object hidden, every colour default grey, no camera**. The tree is
fully populated the whole time, which is exactly what makes it look
like a broken file.

The fix is in two halves and both must stay:

1. `build_boat.py` records every object's colour and transparency as
   it builds and writes `boat_<mode>.look.json` beside the `.FCStd`.
2. `open_modes.py` opens the document, forces **every** object
   visible, re-applies that colour map, hides the interior groups so
   they do not read as a cutaway through the glazing, then
   `viewAxonometric` + `ViewFit`.

`view.sh` runs `open_modes.py`. **Never hand the filenames to FreeCAD
directly** — you will get the hidden, grey, unfittable version.

**Never build with the GUI up.** FreeCAD makes a view provider for
every shape, so a GUI build is roughly ten times slower than
`--console` — seven modes will not finish inside ten minutes, and it
starves the desktop while it tries. Build headless, then open.

**MEMORY is what freezes this machine, not CPU.** One open mode is
about **750 MB** with its view providers; all seven is ~5 GB, and the
desktop already sits at 11 of 15 GB with swap full. `nice` does
nothing about that. `view.sh` therefore:

- defaults to **one** mode (`./view.sh all` if you really want seven)
- runs FreeCAD inside a `systemd-run --user --scope` with
  `MemoryHigh`/`MemoryMax` sized from `MemAvailable`, so it gets
  throttled and reclaimed instead of dragging the session into swap
- warns when less than 1.5 GB is available

Check it is actually applied:

```bash
systemctl --user list-units --type=scope | grep boat-view
systemctl --user show boat-view-<pid>.scope -p MemoryCurrent -p MemoryMax
```

### 4. Beauty shots hide defects — render the parts alone

`beauty_shots.py` renders the whole boat from outside. The hull and the
floats sit in front of the hangar, so **missing, floating and
interpenetrating parts are invisible in every one of them**. Real
defects found only by isolating parts:

- lining plates for the wheel boxes hanging in open air, cut where no
  hull existed
- the girders stopping 1.9 m short of the forward wheel station, so
  that pair of wheels hung on nothing
- the bight and the drawbar deleted entirely — no hitch on the trailer
- the extender arms passing straight through the docked float

The diagnostic scripts live in the job's tmp dir and are worth
recreating: build a mode, hide everything except the group under test,
`setCameraType("Orthographic")`, then `viewTop/viewFront/viewRight/
viewAxonometric` + `SendMsgToActiveView("ViewFit")`, save at 2400×1500.

**Always render, and always LOOK at, before saying anything is fixed:**

| Set | Shows |
|---|---|
| `Hull` alone, iso + bottom | are the boxes and channels cut into hull that exists |
| `HangarFrame` + `HangarTyres` alone | is the frame closed, do the girders reach the wheels, is there a drawbar |
| frame + floats, top + bottom, **both poses** | do parts interpenetrate, does the mechanism have room to move |

Plan views from below are the most informative single view of the
hangar.

### 4b. A render CANNOT prove two parts fit - intersect them

Renders are how you find a part that is missing or obviously wrong.
They are useless for interference, because the hull stands in front of
the hangar in every view: the frame was buried in the wing by 21 litres
in `cruise` and 11 in `road`, and 12 litres of float was inside the
hull on each side, and NONE of it showed in any picture.

`freecad/dock_check.py` does it properly - it intersects the hull solid
with each part of the hangar and prints the volume:

```bash
cd freecad && ~/bin/FreeCAD.AppImage --console dock_check.py < /dev/null \
    | sed -n '/DOES IT FIT/,$p'
# every mode must say FITS, and the last line must be ALL CLEAR
```

Run it after ANY geometry change. Two things it taught that are worth
keeping in mind while drawing:

- **Tangency is not a fit.** Two surfaces at the same coordinate give
  litres of boolean sliver and will not build. Give real clearance -
  `FLOAT_DOCK_GAP_Y` exists because the float sat on the stem face at
  exactly zero.
- **The cap under the wing is `T_LIP_Z` (590), not `T_STEP_Z` (600).**
  The wing's outer lip hangs lower than its step, and it is the lip
  that everything passing underneath has to clear. Probe the hull if in
  doubt: `hull.isInside(Vector(x, y, z), 1e-6, True)`.

### 5. Delete stale `.FCStd` for modes that no longer exist

`MODES` in params is the list. Anything else in `freecad/*.FCStd` is a
saved document from an older architecture; opening one shows screw
jacks and scissors that were removed months ago, indistinguishable
from the current model being wrong. Delete them. `.FCBak` too.

### 6. Report only what a picture shows

Say "verified in the render" only after actually reading the image in
this conversation. Numbers from `checks()` and `structure_calc.py` are
evidence of arithmetic, not of geometry.

---

## Design rules that keep being re-learned

- **Cut into hull that exists.** Below the T step the hull is only the
  1 560 mm stem; at the wheel's y ±910 there is nothing there to cut.
- **A mechanism needs a plane clear of everything at EVERY angle**, not
  just at the two ends of its travel.
- **Size from the budget, not the wish.** Pick the mass or the section
  first and let the stroke, angle or reach fall out of it — an arm pays
  for reach twice, in load and in length.
- **Righting is reserve × lever.** Lever is expensive, reserve is
  cheap: buy stability with float length before arm length.
- **Nothing structural in the water.** Frame and gear live in the
  z 380…800 band, above the loaded waterline, under the wing.
- The floats must stay **parallel** to the hull at every angle.

## Commits

Author is Max Brito alone. No Claude/Anthropic co-author trailers, no
"Generated with" lines. Commit messages explain *why*, in prose.
