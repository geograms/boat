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

A killed run leaves a stale socket that blocks every later launch:
`rm -f /tmp/FreeCAD` when no FreeCAD is running.

`--console` also drops to an interactive prompt and hangs unless stdin
is redirected: always `< /dev/null`.

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
