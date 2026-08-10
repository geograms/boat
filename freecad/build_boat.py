# build_boat.py — Dutch-barge boat-home, FreeCAD documents.
#
# Headless:  ~/bin/FreeCAD.AppImage -c freecad/build_boat.py road foiling
# GUI:       ./freecad/view.sh [modes]   (colors applied, view fitted)
#
# Output: freecad/boat_<mode>.FCStd
import os
import sys
import json
import math
import math as _math

try:
    SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
except NameError:          # FreeCAD console mode may not define __file__
    SCRIPT_DIR = os.path.expanduser("~/code/boat/freecad")
sys.path.insert(0, SCRIPT_DIR)
import params as P

import FreeCAD as App
import Part
from FreeCAD import Vector, Rotation, Placement

WHITE = (0.93, 0.93, 0.90)
HULL_COL = (0.16, 0.25, 0.35)     # barge-style dark blue-gray hull
ORANGE = (0.95, 0.55, 0.05)
GRAY = (0.35, 0.35, 0.38)
DARK = (0.12, 0.12, 0.12)
PANEL = (0.08, 0.09, 0.35)
BLUE = (0.15, 0.45, 0.85)
STEEL = (0.75, 0.75, 0.78)

WALL = 80
DECK_Z = P.CABIN_BASE_Z


def wire(pts3):
    vecs = [Vector(*p) for p in pts3]
    vecs.append(vecs[0])
    return Part.makePolygon(vecs)


def rod(p1, p2, d):
    p1, p2 = Vector(*p1), Vector(*p2)
    axis = p2 - p1
    return Part.makeCylinder(d / 2, axis.Length, p1, axis)


def bar(p1, p2, t, w):
    """Flat bar of section t (in the x-z plane) x w (across y), running
    from p1 to p2. Both points must share the same y."""
    dx, dz = p2[0] - p1[0], p2[2] - p1[2]
    ln = math.hypot(dx, dz)
    s = box(ln, w, t, (0, -w / 2, -t / 2))
    s.rotate(Vector(0, 0, 0), Vector(0, 1, 0), -math.degrees(math.atan2(dz, dx)))
    s.translate(Vector(p1[0], p1[1], p1[2]))
    return s


def bspline_wire(pts3):
    bs = Part.BSplineCurve()
    bs.interpolate([Vector(*p) for p in pts3], PeriodicFlag=True)
    return Part.Wire(bs.toShape())


def plan_prism(plan_pts, z0, z1):
    w = wire([(x, y, z0) for x, y in plan_pts])
    return Part.Face(w).extrude(Vector(0, 0, z1 - z0))


def box(l, w, h, at):
    return Part.makeBox(l, w, h, Vector(*at))


def loft_sections(secs):
    """secs = [(x, [(y, z), ...]), ...]"""
    # RULED: straight lines between stations. A smoothed loft turns the
    # T into a blob; ruled keeps every section exactly as drawn.
    return Part.makeLoft(
        [wire([(x, y, z) for y, z in pts]) for x, pts in secs], True, True)


# ---------------------------------------------------------------
# Hull — hollow barge shell with deck, cabin-size opening
# ---------------------------------------------------------------
def _interp_station(x):
    st = P.STATIONS
    for i in range(len(st) - 1):
        if st[i][0] <= x <= st[i + 1][0]:
            t = (x - st[i][0]) / (st[i + 1][0] - st[i][0])
            return [x] + [a + t * (b - a)
                          for a, b in zip(st[i][1:], st[i + 1][1:])]
    return list(st[-1])


def hull_sections(inner=False):
    """Hull stations. Aft of the bow the section is a T: the underwater
    body narrows to the stem, the deck keeps the full beam, and the two
    notches under the wings are where the floats nest.

    The T holds its FULL depth to the float nose at x 6000, then the
    bow's full-width body closes over it within 280 mm - the shoulders
    that hide the float heads and give the water a clean entry."""
    rows = [st for st in P.STATIONS if not 5980 < st[0] < 6300]
    rows.append(_interp_station(5995))
    rows.append(_interp_station(6280))
    rows.sort(key=lambda r: r[0])
    out = []
    for st in rows:
        x, yg, yc, zk, zc, zs = st
        if inner:
            yg, yc = max(yg - WALL, 15), max(yc - WALL, 10)
            zk, zc, zs = zk + 60, zc + 40, DECK_Z - 30
        # ONE 12-point topology everywhere, and it is a REAL T below
        # the step: flat bottom across the full stem, vertical stem
        # sides, square step, lip, sheer. The bow reuses the same
        # template at full width, so the loft never has to invent
        # geometry between different shapes.
        if x <= 6005:
            w_bot = min(P.STEM_HW - (WALL if inner else 0), yc)
            z_mid = P.T_STEP_Z + (30 if inner else 0)
            z_lip = P.T_LIP_Z + (30 if inner else 0)
        else:
            w_bot = yc
            z_lip = max(P.T_LIP_Z + (30 if inner else 0), zk + 40)
            z_mid = max(P.T_STEP_Z + (30 if inner else 0), z_lip + 30)
        w_in = yg - (45 if inner else 65)         # lip inner face
        w_in = max(w_in, w_bot + 10)
        pts = [(w_bot, zk), (w_bot, z_mid), (w_in, z_mid),
               (w_in, z_lip), (yg, z_lip), (yg, zs),
               (-yg, zs), (-yg, z_lip), (-w_in, z_lip),
               (-w_in, z_mid), (-w_in if False else -w_in, z_mid),
               (-w_bot, z_mid), (-w_bot, zk)]
        # dedupe the accidental repeat, keep symmetric 13-pt ring
        pts = [p for i, p in enumerate(pts) if i == 0 or p != pts[i - 1]]
        out.append((x, pts))
    return out


def build_hull():
    outer = loft_sections(hull_sections())
    shell = outer.cut(loft_sections(hull_sections(inner=True)))
    # deck plate closes the top over the whole length (the sheer rises
    # forward, so the extra height forward becomes a bow bulwark)
    shell = shell.fuse(outer.common(
        box(P.LOA + 400, 3200, 60, (-200, -1600, DECK_Z - 60))))
    # sunken self-draining cockpit: cut the well, drop in a watertight tub
    shell = shell.cut(box(
        P.COCKPIT_X1 - P.COCKPIT_X0, 2 * P.COCKPIT_HW, 800,
        (P.COCKPIT_X0, -P.COCKPIT_HW, P.COCKPIT_FLOOR)))
    tub = box(P.COCKPIT_X1 - P.COCKPIT_X0 + P.COCKPIT_WALL,
              2 * P.COCKPIT_HW + 2 * P.COCKPIT_WALL,
              DECK_Z - P.COCKPIT_FLOOR + P.COCKPIT_WALL,
              (P.COCKPIT_X0 - P.COCKPIT_WALL,
               -P.COCKPIT_HW - P.COCKPIT_WALL,
               P.COCKPIT_FLOOR - P.COCKPIT_WALL))
    tub = tub.cut(box(P.COCKPIT_X1 - P.COCKPIT_X0, 2 * P.COCKPIT_HW,
                      DECK_Z - P.COCKPIT_FLOOR + 100,
                      (P.COCKPIT_X0, -P.COCKPIT_HW, P.COCKPIT_FLOOR)))
    shell = shell.fuse(tub)
    shell = shell.cut(plan_prism(       # cabin-footprint deck opening
        [(P.CABIN_X0 + 50, -P.CABIN_W / 2 + 70),
         (P.CABIN_X1 - 50, -P.CABIN_W / 2 + 70),
         (P.CABIN_X1 - 50, P.CABIN_W / 2 - 70),
         (P.CABIN_X0 + 50, P.CABIN_W / 2 - 70)],
        DECK_Z - 60, DECK_Z + 60))
    # the float notches are built into the T sections themselves
    # ---- WHEEL BOXES. Four of them, and they are cut into the T's
    # WING, not into the keel. Below z 600 the hull is only the 1560 mm
    # stem: at the wheel's y +-910 there is simply no hull to cut, that
    # band is the float's recess. The wing above 600 runs the full beam,
    # so each box opens DOWNWARD through the wing underside and rises
    # 580 mm into the interior. Lined - roof and four walls - so the
    # hull stays closed, and the opening sits 281 mm above the
    # waterline: dry, and out of the flow.
    for wx in P.WHEEL_XS:
        for sy in (-1, 1):
            py = sy * P.WHEEL_Y
            z0, zt = P.POCKET_Z0, P.POCKET_TOP
            cx = wx + P.POCKET_DX
            shell = shell.cut(box(P.POCKET_L, P.POCKET_W, zt - z0 + 40,
                                  (cx - P.POCKET_L / 2, py - P.POCKET_W / 2,
                                   z0 - 20)))
            shell = shell.fuse(box(P.POCKET_L + 40, P.POCKET_W + 40, 22,
                                   (cx - (P.POCKET_L + 40) / 2,
                                    py - (P.POCKET_W + 40) / 2, zt)))
            for dy in (-1, 1):
                shell = shell.fuse(box(
                    P.POCKET_L + 40, 20, zt - z0,
                    (cx - (P.POCKET_L + 40) / 2,
                     py + dy * (P.POCKET_W / 2) - (20 if dy > 0 else 0), z0)))
            for dx in (-1, 1):
                shell = shell.fuse(box(
                    20, P.POCKET_W + 40, zt - z0,
                    (cx + dx * (P.POCKET_L / 2) - (20 if dx > 0 else 0),
                     py - (P.POCKET_W + 40) / 2, z0)))

    # ---- GIRDER CHANNELS. The frame's two girders used to hang under
    # the hull at z 140..380, with the loaded waterline at 319 - half
    # submerged whenever the boat floated. They now run in a lined
    # channel in the WING, z 600..800: out of the water, tucked against
    # the hull, and clear over the docked float instead of fighting it
    # for the same band. Open at the bottom and at the stern so the
    # hangar still slides on from astern.
    gb, gh = P.GIRDER_SECTION[0], P.GIRDER_SECTION[1]
    cw, cz = gb + 40, P.GIRDER_Z0
    for sy in (-1, 1):
        ry = sy * P.GIRDER_Y
        shell = shell.cut(box(P.GIRDER_X1 + 200, cw, gh + 40,
                              (-100, ry - cw / 2, cz - 20)))
        # No lead-in is cut here. One was tried at 334 mm and then at
        # 120, and the hull volume came out IDENTICAL either way - the
        # channel is already open at the transom, so there was nothing
        # for the cut to remove. The 334 mm is taken by the winch.

        shell = shell.fuse(box(P.GIRDER_X1 + 200, cw + 40, 20,
                               (-100, ry - (cw + 40) / 2, cz + gh)))
        for dy in (-1, 1):
            shell = shell.fuse(box(
                P.GIRDER_X1 + 200, 20, gh + 20,
                (-100, ry + dy * (cw / 2) - (20 if dy > 0 else 0), cz)))

    # ---- KEEL CHANNEL for the hangar's cross tie. The tie has to
    # travel the whole length of the hull bottom to dock, so instead of
    # hanging in the flow it runs in a shallow channel cut into the
    # keel and finishes FLUSH: no bar in the water, no drag. The
    # forward end of the channel is ramped so the water closes over it.
    ch_x1 = 3400
    shell = shell.cut(box(ch_x1, P.TIE_CHANNEL_W, P.TIE_CHANNEL_D + 10,
                          (-40, -P.TIE_CHANNEL_W / 2, -10)))
    ramp = Part.makeBox(420, P.TIE_CHANNEL_W, P.TIE_CHANNEL_D,
                        Vector(ch_x1, -P.TIE_CHANNEL_W / 2, 0))
    ramp.rotate(Vector(ch_x1, 0, P.TIE_CHANNEL_D), Vector(0, 1, 0), 15)
    shell = shell.cut(ramp)
    # LINE the channel: cutting it opened the hull shell, so the roof
    # and both walls are added back and the boat stays watertight
    cw, cd = P.TIE_CHANNEL_W, P.TIE_CHANNEL_D
    shell = shell.fuse(box(ch_x1 + 420, cw, 26, (-40, -cw / 2, cd)))
    for sy in (-1, 1):
        shell = shell.fuse(box(ch_x1 + 420, 26, cd + 26,
                               (-40, sy * cw / 2 - (26 if sy > 0 else 0), 0)))
    # guide strips INSIDE the channel, and the stop the tie seats on
    for sy in (-1, 1):
        shell = shell.fuse(box(ch_x1 - 200, 70, 34,
                               (60, sy * 400 - 35, P.TIE_CHANNEL_D - 34)))
    shell = shell.fuse(box(90, P.TIE_CHANNEL_W - 60, P.TIE_CHANNEL_D,
                           (ch_x1 - 120, -(P.TIE_CHANNEL_W - 60) / 2, 0)))

    # the dome is a ROOM, not a bubble on the deck: open the foredeck
    # under it so the saloon sole runs on through, leaving a 130 mm
    # gunwale ledge for the glass to land on
    fx0, fx1 = P.CABIN_X1 - 50, P.DOME_SOLE_X1
    fplan = []
    for i in range(9):
        x = fx0 + (fx1 - fx0) * i / 8
        fplan.append((x, -(P.sheer_at(x)[0] - 180)))
    for i in range(8, -1, -1):
        x = fx0 + (fx1 - fx0) * i / 8
        fplan.append((x, P.sheer_at(x)[0] - 180))
    # only the deck PLATE comes out - the shell below it is untouched
    shell = shell.cut(plan_prism(fplan, DECK_Z - 80, DECK_Z + 80))
    shell = shell.cut(door_opening())   # companionway through the bulkhead
    return shell


def door_opening():
    return box(220, 2 * P.DOOR_HW, P.DOOR_Z1 - P.DOOR_Z0,
               (P.COCKPIT_X1 - 60, -P.DOOR_HW, P.DOOR_Z0))


# ---------------------------------------------------------------
# Cabin shell — maximized footprint, continuous window band
# ---------------------------------------------------------------
def build_cabin():
    cl = P.CABIN_X1 - P.CABIN_X0
    ch = P.CABIN_ROOF_Z - P.CABIN_BASE_Z
    shell = box(cl, P.CABIN_W, ch, (P.CABIN_X0, -P.CABIN_W / 2, P.CABIN_BASE_Z))
    try:
        shell = shell.makeFillet(50, shell.Edges)
    except Exception:
        pass
    inner = box(cl - 120, P.CABIN_W - 120,
                ch, (P.CABIN_X0 + 60, -P.CABIN_W / 2 + 60, P.CABIN_BASE_Z - 200))
    shell = shell.cut(inner)

    cuts, panes = [], []
    wz0, wh = P.WIN_Z0, P.WIN_H
    # two BIG picture windows per side (saloon and bed) instead of six
    # small ones; the service zone is lit by a porthole each side
    for wx, wl in P.WINDOWS:
        cuts.append(box(wl, P.CABIN_W + 200, wh, (wx, -P.CABIN_W / 2 - 100, wz0)))
        panes.append(box(wl, P.CABIN_W - 40, wh, (wx, -P.CABIN_W / 2 + 20, wz0)))
    px, pz, pd = P.PORTHOLE
    for sy in (-1, 1):
        cuts.append(Part.makeCylinder(
            pd / 2, P.CABIN_W + 200,
            Vector(px, sy * (P.CABIN_W / 2 + 100), pz), Vector(0, -sy, 0)))
        panes.append(Part.makeCylinder(
            pd / 2 - 30, 20, Vector(px, sy * (P.CABIN_W / 2 - 20), pz),
            Vector(0, sy, 0)))
    # NO FORWARD WALL: the saloon opens straight into the dome, so the
    # front of the cabin is a portal - a corner post each side and the
    # roof header over it. The dome's aft rim frames the opening.
    pw = P.CABIN_W - 2 * P.DOME_PORTAL_POST
    cuts.append(box(400, pw, P.CABIN_CEIL_Z - P.SOLE_Z,
                    (P.CABIN_X1 - 200, -pw / 2, P.SOLE_Z)))
    cuts.append(door_opening())          # companionway
    for c in cuts:
        shell = shell.cut(c)
    return shell, Part.makeCompound(panes)


# ---------------------------------------------------------------
# Pop-top canopy
# ---------------------------------------------------------------
def terrace_plan():
    """(length, width, centre x) of the roof terrace."""
    return (P.CABIN_X1 - P.CABIN_X0 + 2 * P.CANOPY_OVERHANG,
            P.CABIN_W + 2 * P.CANOPY_OVERHANG,
            (P.CABIN_X0 + P.CABIN_X1) / 2)


def build_terrace(deploy_deg=None):
    """Roof deck: a bare non-slip walking surface, and eight flexible
    solar panels in alu frames hinged along the deck edges.

    deploy_deg 0   = panels flat on the roof: full solar, no deck
    deploy_deg 90  = panels standing: the deck is clear and they ARE the
                     guardrail, 850 mm high

    Nothing lifts and nothing is synchronised - one leaf hinge and one
    catch per panel. Returns (deck, panels, frame, None, None)."""
    if deploy_deg is None:
        deploy_deg = P.RAIL_STOW_DEG
    tl, tw, cx = terrace_plan()
    z0 = P.CABIN_ROOF_Z
    deck, panels, frame = [], [], []

    # walking surface of the structural roof, non-slip, and its toe rail
    deck.append(box(tl, tw, 12, (cx - tl / 2, -tw / 2, z0)))
    for sy in (-1, 1):
        deck.append(box(tl - 200, 24, P.RAIL_TOE,
                        (cx - (tl - 200) / 2, sy * (tw / 2 - 30) - 12,
                         z0 + 12)))
    for sx in (-1, 1):                       # corner scuppers
        for sy in (-1, 1):
            deck.append(box(P.TERRACE_SCUPPER, 40, 26,
                            (cx + sx * (tl / 2 - 320),
                             sy * (tw / 2 - 30) - 20, z0 + 12)))

    pw, pl, pt = P.MODULE_FLEX      # pl = run along x, pw = rise standing
    fw = P.RAIL_FRAME_W
    ang = math.radians(deploy_deg)

    for (hx, hy, hz, axis, sy) in P.rail_positions():
        # Blank lies flat at the hinge: x 0..pl is the run along the
        # boat, y runs INBOARD from the hinge (+y to port, -y to
        # starboard), z is the frame depth.
        y0 = 0.0 if sy < 0 else -pw
        frame_bar = box(pl, pw, fw, (0, y0, 0)).cut(
            box(pl - 2 * fw, pw - 2 * fw, fw + 2, (fw, y0 + fw, -1)))
        lam = box(pl - 2 * fw - 4, pw - 2 * fw - 4, pt,
                  (fw + 2, y0 + fw + 2, fw - pt))
        # Lifting is ONE rotation about the hinge line, which is the
        # world x axis through (hx, hy, hz): +90 takes +y to +z, so the
        # port row turns +deploy and the starboard row -deploy.
        place = Placement(Vector(hx, hy, hz),
                          Rotation(Vector(1, 0, 0), -sy * deploy_deg))
        for shp in (frame_bar, lam):
            shp.Placement = place.multiply(shp.Placement)
        frame.append(frame_bar)
        panels.append(lam)
        for f in (0.12, 0.88):                  # hinge knuckles
            frame.append(Part.makeCylinder(
                14, 70, Vector(hx + pl * f - 35, hy, hz), Vector(1, 0, 0)))

    # removable webbing line closing the aft edge at rail height
    if P.RAIL_AFT_LINE and deploy_deg > 45:
        yh = P.CABIN_W / 2 - P.RAIL_INSET
        for f in (0.45, 0.95):
            zl = z0 + P.RAIL_TOE + pw * f
            frame.append(rod((P.CABIN_X0 + 60, -yh, zl),
                             (P.CABIN_X0 + 60, yh, zl), 10))

    return (Part.makeCompound(deck), Part.makeCompound(panels),
            Part.makeCompound(frame), None, None)


# ---------------------------------------------------------------
# Solar wings (from the STL sketch): panel wing hinged on the deck
# edge, pontoon float capsule along the outer edge
# ---------------------------------------------------------------
def mirror_y(shape):
    return shape.mirror(Vector(0, 0, 0), Vector(0, 1, 0))


# Float mini-hull stations, local frame: z up = hull face DOWN (roll 0),
# flat deck at z = +FLOAT_H/2. [u, y_gunw, y_chine, z_keel, z_chine]
FLOAT_STATIONS = [
    [-0.50, 130, 100, 120, 240],
    [-0.35, 190, 155,  40, 170],
    [-0.15, 200, 165,  15, 160],
    [0.05,  200, 165,  15, 160],
    [0.25,  200, 165,  15, 160],
    [0.42,  198, 163,  18, 162],   # FULL width past the last wheel bay:
    [0.46,  190, 157,  30, 170],   # the taper used to start at 0.25 and
    [0.50,   45,  36, 210, 250],   # ate the forward bay's own walls
]


def build_float(pod, roll, flip=0.0, fx=None):
    """Stabilizer float with CASTER wheels (stub axles perpendicular to
    the deck): roll 90 = float on its side, wheels vertical (road);
    roll 0 = float flat, wheels flat on the deck (water).
    Starboard, posed."""
    ty, tz = pod
    dx = 0.0 if fx is None else fx - P.FLOAT_X
    # -roll about x maps the local deck normal (+z) outboard (+y).
    # YAW: the float pivots on its bow pin, so it is not just moved
    # outboard, it is turned. flip carries the yaw in from the caller.
    place = Placement(Vector(dx, ty, tz),
                      Rotation(Vector(0, 0, 1), -flip).multiply(
                          Rotation(Vector(1, 0, 0), -roll)))

    secs = []
    ky = P.FLOAT_W / 400.0            # loft table is 400 wide, 900 tall
    kz = P.FLOAT_H / 900.0
    for u, yg, yc, zk, zc in FLOAT_STATIONS:
        # the HEAD curves up FROM THE BOTTOM over the last half-metre
        # only - a spoon TIP. The body keeps full depth past the last
        # wheel bay; the earlier version started the rise at 25% of the
        # length and left the whole forward quarter without a hull.
        if u >= 0.46:
            f = (u - 0.46) / 0.04
            zk = zk + (430 - zk) * min(1.0, f)
            zc = max(zc, zk + 40)
        x = P.FLOAT_X + u * P.FLOAT_LEN
        h2 = P.FLOAT_H / 2
        pts = [(10, (zk - 450) * kz + 0), (yc * ky, (zc - 450) * kz),
               (yg * ky, h2), (-yg * ky, h2),
               (-yc * ky, (zc - 450) * kz), (-10, (zk - 450) * kz)]
        pts = [(py, max(pz, -h2)) for (py, pz) in pts]
        secs.append((x, pts))
    hull_f = loft_sections(secs)

    # OPEN WHEEL BAYS: at each station the float body is cut through -
    # only the flip tube spans the bay, so the wheel nests inside the
    # envelope in either pose (local frame: x along, y across, z up)
    hull_f.Placement = place.multiply(hull_f.Placement)

    # THE WHEEL NOTCH. Docked on the road, the float and the wheel-down
    # tyre want the same space: the tyre's inner flank runs through the
    # float's inner-lower corner. So the corner is cut away at each
    # wheel station - the "eats half the floater" of the road stance,
    # cut for real. Only the DOWN position has to clear, because the
    # floats swing OUT before the wheels come up; that costs 118 kg of
    # buoyancy across both floats instead of 328 for the full travel.
    for _wx in P.WHEEL_XS:
        hull_f = hull_f.cut(box(
            P.WELL_L, P.WELL_W + 30, P.WELL_H,
            (_wx - P.WELL_L / 2, ty - P.FLOAT_W / 2 - 30,
             tz - P.FLOAT_H / 2 - 10)))
        # groove for the docked V arm to lie in - the float's inner
        # face is against the stem, so the arm needs somewhere to go
        pass
    for _ax in P.ARM_XS:
        hull_f = hull_f.cut(box(
            P.ARM_L + 120, P.ARM_GROOVE_D, P.ARM_GROOVE_W,
            (_ax - P.ARM_L - 60, ty - P.FLOAT_W / 2 - 10,
             P.BEAM_Z0 - P.ARM_GROOVE_W / 2 + 30)))

    # solar strips on the deck, in the gaps between the wheels
    strips = []
    for x0 in (P.FLOAT_X - 1900, P.FLOAT_X + 700):
        s = box(P.DINGHY_PANEL[0], P.FLOAT_W - 90, 12,
                (x0, -(P.FLOAT_W - 90) / 2, P.FLOAT_H / 2))
        s.Placement = place.multiply(s.Placement)
        strips.append(s)

    # the float has NO running gear: no legs, no wheels, no motors for
    # the road. It is a buoyancy body that swings for stability, notched
    # at two stations to let the wheels down past it
    forks, tires, rims = [], [], []



    # in-float hydraulic drive (docs/wheels.md): gasketed deck hatch
    # over the machinery bay, pump unit inside, hoses to each hub,
    # goldenrod hub-motor caps
    bx = P.FLOAT_X + P.MOTOR_BAY_DX
    hatch = box(P.MOTOR_BAY_L + 20, P.FLOAT_W - 110, 22,
                (bx - (P.MOTOR_BAY_L + 20) / 2, -(P.FLOAT_W - 110) / 2,
                 P.FLOAT_H / 2 + 12))
    hatch.Placement = place.multiply(hatch.Placement)

    # The wheel drive is NOT here any more - it moved to the girder
    # with the wheels. What is left in the float is the waterjet's own
    # pump and motor, dry in the same bay, under the hatch.
    hyd = []
    bx0 = P.FLOAT_X + P.MOTOR_BAY_DX
    hyd.append(Part.makeCylinder(78, 260, Vector(bx0 - 320, 0, 0),
                                 Vector(1, 0, 0)))
    hyd.append(Part.makeCylinder(92, 190, Vector(bx0 - 60, 0, 0),
                                 Vector(1, 0, 0)))
    hydraulics = Part.makeCompound(hyd)
    hydraulics.Placement = place.multiply(hydraulics.Placement)

    # U-INTAKE waterjet (docs/floater.md). The grid is on the BOTTOM of
    # the float, directly under the pump: a perforated floor plate with
    # a narrow return up each side, so water is drawn from all
    # directions and travels centimetres to the impeller. Nothing sits
    # on the topsides - an intake up there would suck air.
    gx = P.FLOAT_X + P.MOTOR_BAY_DX
    gl, gw = 620, P.FLOAT_W - 90
    bot = -P.FLOAT_H / 2
    thr = []
    thr.append(box(gl + 60, gw + 40, 16,
                   (gx - gl / 2 - 30, -(gw + 40) / 2, bot - 6)))
    for ix in range(12):
        for iy in range(7):
            thr.append(Part.makeCylinder(
                P.JET_HOLE_D / 2 + 2, 10,
                Vector(gx - gl / 2 + 26 + ix * 52, -gw / 2 + 30 + iy * 52,
                       bot - 10), Vector(0, 0, 1)))
    for sgn in (-1, 1):                     # the U's short returns
        gy = sgn * (P.FLOAT_W / 2)
        thr.append(box(gl, 14, 90,
                       (gx - gl / 2, gy - (14 if sgn > 0 else 0), bot + 4)))
        for ix in range(11):
            thr.append(Part.makeCylinder(
                P.JET_HOLE_D / 2 + 2, 9,
                Vector(gx - gl / 2 + 30 + ix * 52, gy + sgn * 7, bot + 48),
                Vector(0, sgn, 0)))
    # jet nozzle: low on the transom, in line with the pump
    tail = P.FLOAT_X - P.FLOAT_LEN / 2
    thr.append(Part.makeCone(85, P.JET_NOZZLE_D / 2, 190,
                             Vector(tail + 40, 0, bot + 150),
                             Vector(-1, 0, 0)))
    thr.append(Part.makeCylinder(P.JET_NOZZLE_D / 2 - 12, 30,
                                 Vector(tail - 155, 0, bot + 150),
                                 Vector(-1, 0, 0)))
    # rub strake along the outer face at the waterline
    thr.append(rod((P.FLOAT_X - P.FLOAT_LEN / 2 + 260, P.FLOAT_W / 2 + 8, 40),
                   (P.FLOAT_X + P.FLOAT_LEN / 2 - 500, P.FLOAT_W / 2 + 8, 40),
                   30))
    thruster = Part.makeCompound(thr)
    thruster.Placement = place.multiply(thruster.Placement)

    # low-profile boxes over the flat wheels: water pose only
    boxes = []                        # gone: the open bays replaced the
                                      # wheel covers
    return hull_f, Part.makeCompound(strips), Part.makeCompound(forks), \
        tires, rims, (Part.makeCompound(boxes) if boxes else None), \
        hatch, hydraulics, thruster


def build_curtains(deg):
    """Solar curtains: the SAME flexible panel as the roof rails, five a
    side in a light aluminium frame, hinged on the corner where the
    cabin roof meets the side wall.

    deg 0  = closed, hanging flat down the side: windows covered, boat
             slim - the road pose
    deg 40 = swung out as an awning: shade over the glass, cells tilted

    Returns (frames, panels, hinges) for BOTH sides, already placed."""
    rise, run_l, pt = P.MODULE_FLEX
    fw = P.CURT_FRAME_W
    frames, panels, hinges = [], [], []
    for (hx, hy, hz, sy) in P.curtain_positions():
        # blank hangs from the hinge: x along the boat, y outboard, z DOWN
        y0 = 0.0 if sy > 0 else -fw
        frame_bar = box(run_l, fw, rise, (0, y0, -rise)).cut(
            box(run_l - 2 * fw, fw + 2, rise - 2 * fw,
                (fw, y0 - 1, -rise + fw)))
        lam = box(run_l - 2 * fw - 4, pt, rise - 2 * fw - 4,
                  (fw + 2, y0 + (fw - pt if sy > 0 else 0), -rise + fw + 2))
        # swinging out is ONE rotation about the hinge line (the world x
        # axis through the corner)
        place = Placement(Vector(hx, hy, hz),
                          Rotation(Vector(1, 0, 0), sy * deg))
        for shp in (frame_bar, lam):
            shp.Placement = place.multiply(shp.Placement)
        frames.append(frame_bar)
        panels.append(lam)
        for f in (0.12, 0.88):
            hinges.append(Part.makeCylinder(
                10, 60, Vector(hx + run_l * f - 30, hy, hz), Vector(1, 0, 0)))
        if deg > 5:                          # stay holding the awning out
            import math as _m
            r = _m.radians(deg)
            hinges.append(rod(
                (hx + run_l / 2, hy, hz - 60),
                (hx + run_l / 2, hy + sy * rise * 0.55 * _m.sin(r),
                 hz - rise * 0.55 * _m.cos(r)), 12))
    return (Part.makeCompound(frames), Part.makeCompound(panels),
            Part.makeCompound(hinges))


def build_hangar(phi, coupled=True, tow="sea"):
    """The docking gear: spike rails in the hull recesses, the electric
    extenders, and the bight + drawbar joining the float tails.
    phi 0 = docked, 90 = extended to the sea stance.
    Returns (frame, locks, rubber)."""
    parts, locks, rubber = [], [], []
    pod = P.pod_at(phi)

    # ---- THE U: a SOLID box girder each side, tied by the bight.
    # This is what the boat's 3 t sits on, so it is a real beam, not
    # tubes. The girders run the length of the notch inside the stem
    # face; the float's fork grooves ride their outer web, and the
    # tapered nose closes the fit as the float slides in from astern.
    gb, gh = P.GIRDER_SECTION[0], P.GIRDER_SECTION[1]
    gz = P.GIRDER_Z              # z 600..800: in the wing channel,
                                 # 281 mm clear of the waterline and
                                 # above the docked float
    for sy in (-1, 1):
        ry = sy * P.GIRDER_Y
        # the girder runs from the BIGHT to the cross tie, so the O is
        # closed at both ends - it used to stop 220 mm short of the
        # bight and the frame was open there
        g0 = P.GIRDER_X0
        glen = P.GIRDER_LEN
        gir = box(glen, gb, gh,
                  (g0, ry - gb / 2, gz - gh / 2))
        gir = gir.cut(box(glen - 240, gb - 16, gh - 16,
                          (g0 + 120, ry - (gb - 16) / 2,
                           gz - (gh - 16) / 2)))
        parts.append(gir)
        # the docking nose: a tapered lead-in at the aft end
        locks.append(Part.makeCone(
            gh / 2 - 20, 30, P.SPIKE_TAPER,
            Vector(g0, ry, gz), Vector(-1, 0, 0)))
        # bayonet lock gearmotor on the girder web
        locks.append(Part.makeCylinder(
            45, 110, Vector(700, ry + sy * (gb / 2), gz),
            Vector(0, sy, 0)))
        # web stiffeners every 1.2 m - the girder is the load path
        for lx in range(500, int(P.GIRDER_X1) - 300, 1200):
            parts.append(box(90, gb + 70, gh + 60,
                             (lx, ry - (gb + 70) / 2,
                              gz - (gh + 60) / 2)))

    # ---- SWING ARMS AND WHEELS, on the FRAME. The wheel sits on the
    # END of a 445 mm arm pivoted at z 445 off the girder. Hanging
    # straight down the axle is at z 0 and the tyre is on the road;
    # swung 180 deg it is at z 890 with the tyre stowed inside the
    # wing. 890 mm of travel out of a 445 mm mechanism, and nothing
    # stands above the girder - which a straight jack of the same
    # stroke could not do, it needed a 1.14 m column.
    #
    # OVER-CENTRE: straight down, the load line runs through the pivot
    # into a hard stop, so the screw actuator carries almost none of
    # the boat. It only swings the arm.
    for wx in P.WHEEL_XS:
        for sy in (-1, 1):
            pivot, axle = P.arm_points(sy, down=(phi <= 5))
            py = pivot[0]
            # the arm itself, pivot to axle
            arm = Part.makeCylinder(
                P.ARM_D / 2, P.ARM_R,
                Vector(wx, py, pivot[1]),
                Vector(0, 0, -1 if axle[1] < pivot[1] else 1))
            parts.append(arm)
            # pivot boss and its bracket down onto the girder web
            parts.append(Part.makeCylinder(
                95, P.POCKET_W + 60, Vector(wx, py - (P.POCKET_W + 60) / 2,
                                            pivot[1]), Vector(0, 1, 0)))
            # bracket dropping from the girder down to the pivot
            parts.append(box(200, 170, P.GIRDER_Z - pivot[1] + 100,
                             (wx - 100, py - 85, pivot[1] - 100)))
            # the leadscrew actuator: frame lug to a lug at 0.6 R along
            # the arm. Self-locking, so the arm parks anywhere.
            lug = (wx, py, pivot[1] + (axle[1] - pivot[1]) * 0.6)
            anc = (wx + 330, py, P.GIRDER_Z - P.GIRDER_SECTION[1] / 2)
            # the anchor LUG on the girder's underside - the actuator
            # used to start at a point in space with nothing to react
            # against, which is what made it read as a loose rod
            parts.append(box(150, 120, 90, (anc[0] - 75, py - 60, anc[2])))
            d = Vector(lug[0] - anc[0], 0, lug[2] - anc[2])
            parts.append(Part.makeCylinder(
                P.ACT_D / 2, d.Length, Vector(*anc), d))
            parts.append(Part.makeCylinder(
                P.ACT_D / 2 + 14, d.Length * 0.45, Vector(*anc), d))
            # stub axle, tyre and rim on the END of the arm
            parts.append(Part.makeCylinder(
                46, P.WHEEL_W + 90,
                Vector(wx, axle[0] - (P.WHEEL_W + 90) / 2, axle[1]),
                Vector(0, 1, 0)))
            rubber.append(Part.makeTorus(
                (P.WHEEL_DIA - P.WHEEL_W) / 2, P.WHEEL_W / 2,
                Vector(wx, axle[0], axle[1]), Vector(0, 1, 0)))
            rubber.append(Part.makeCylinder(
                P.HUB_DIA / 2, P.WHEEL_W - 40,
                Vector(wx, axle[0] - (P.WHEEL_W - 40) / 2, axle[1]),
                Vector(0, 1, 0)))
            # ONE driven wheel per side: motor and 100:1 reduction dry
            # in a box on the girder web, one short shaft out through a
            # marine face seal to the forward wheel.
            if wx == min(P.WHEEL_XS):
                parts.append(box(380, 220, 220,
                                 (wx - 480, py + sy * 60 - 110,
                                  P.GIRDER_Z - 110)))
                parts.append(Part.makeCylinder(
                    P.SEAL_DIA / 2, 60,
                    Vector(wx, axle[0] - sy * (P.WHEEL_W / 2 + 60), axle[1]),
                    Vector(0, sy, 0)))

    # ---- THE V ARMS. Two per side on vertical pins, equal length and
    # parallel: a parallelogram, so the float TRANSLATES and never
    # yaws. Seen from above the two sides mirror and the four arms read
    # as a V. They sweep AFT as they open, so the water's push on the
    # float drives them further open against the stop; a rope pulls the
    # float forward to shut the V and a latch holds it for the road.
    ang = _math.radians(P.arm_angle(phi))
    ab, ah, at_ = P.ARM_SECTION
    fcx, fcy, _yaw = P.float_pose(phi)
    for sy in (-1, 1):
        for ax in P.ARM_XS:
            # hull pin on the girder, float pin on the float's inner face
            px, py = ax, sy * P.STEM_HW
            tx = ax - P.ARM_L * _math.cos(ang) * 0 - P.ARM_L * (1 - _math.cos(ang))
            ty = sy * (P.STEM_HW + P.ARM_L * _math.sin(ang))
            L = _math.hypot(tx - px, abs(ty) - abs(py))
            yawd = _math.degrees(_math.atan2(abs(ty) - abs(py), tx - px))
            arm = box(max(L, 1.0), ab, ah, (0, -ab / 2, P.BEAM_Z0))
            arm.Placement = Placement(
                Vector(px, py, 0), Rotation(Vector(0, 0, 1), sy * yawd))
            parts.append(arm)
            for (qx, qy) in ((px, py), (tx, ty)):     # the two pins
                parts.append(Part.makeCylinder(
                    P.HINGE_PIN_D / 2, P.BEAM_H + 200,
                    Vector(qx, qy, P.BEAM_Z0 - 100), Vector(0, 0, 1)))
                parts.append(box(200, 220, 90,
                                 (qx - 100, qy - 110, P.BEAM_Z0 - 100)))
            # the open stop: a hard lug on the girder the arm lands on
            parts.append(box(140, 110, P.BEAM_H,
                             (px - 70 - 190, py - sy * 55, P.BEAM_Z0)))
        # haul-in line: float's forward end back to a block on the frame
        locks.append(rod((fcx + P.FLOAT_LEN / 2 - 300, sy * (fcy - P.FLOAT_W / 2),
                          P.BEAM_Z0 + P.BEAM_H / 2),
                         (P.GIRDER_X1 - 300, sy * P.GIRDER_Y,
                          P.BEAM_Z0 + P.BEAM_H / 2), 12))
        parts.append(Part.makeCylinder(
            55, 90, Vector(P.GIRDER_X1 - 300, sy * P.GIRDER_Y, P.BEAM_Z0),
            Vector(0, 0, 1)))
        # road latch, holding the V shut against the stem face
        parts.append(box(160, 120, 140,
                         (P.FLOAT_X_DOCKED - P.FLOAT_LEN / 2 + 500,
                          sy * P.STEM_HW - 60, P.BEAM_Z0 + 40)))

    # ---- THE FLOOR. Aluminium deck panels between the girders, on
    # the frame and only on the frame: the floats move, so nothing here
    # touches them. Undocked this is what people stand on; docked it
    # lifts out, because at z 800 between the girders is the inside of
    # the boat.
    #
    # It is NOT the hull's bottom protection - the frame has nothing
    # below the keel to hang a plate from. That job belongs to the keel
    # shoe on the boat. See the note in params.
    dw, dl = P.deck_panels()
    sb, sh, _st = P.DECK_STRINGER
    parts.append(box(dl, sb, sh, (P.GIRDER_X0, -sb / 2, P.DECK_Z - sh)))
    for _k in range(1, int(dl / 1400)):        # deck bearers on the stringer
        parts.append(box(80, 2 * dw, 60,
                         (P.GIRDER_X0 + _k * 1400, -dw, P.DECK_Z - 60)))
    if phi > 0:                     # laid only when the boat is off
        for sy in (-1, 1):
            parts.append(box(dl, dw, P.DECK_T,
                             (P.GIRDER_X0, 0 if sy > 0 else -dw, P.DECK_Z)))
            rb, rh, _rt = P.DECK_RIB
            for k in range(int(dl / P.DECK_RIB_PITCH) + 1):
                parts.append(box(rb, dw, rh,
                                 (P.GIRDER_X0 + k * P.DECK_RIB_PITCH,
                                  0 if sy > 0 else -dw, P.DECK_Z - rh)))
        # TRACTION BOARDS stowed flat on the deck: two plastic
        # recovery boards, 4 kg each, that lay off the deck edge to
        # walk a quad or a bike aboard. They replaced a 35 kg hinged
        # ramp that had to swing clear of the forward tie.
        bl, bw_, bt = P.BOARD
        for k in range(P.BOARD_N):
            parts.append(box(bl, bw_, bt,
                             (P.GIRDER_X1 - bl - 200,
                              -bw_ - 60 + k * (bw_ + 120),
                              P.DECK_Z + P.DECK_T)))

    # ---- THE BIGHT AND THE FORWARD TIE. Two girders on their own are
    # two rails; what makes them a frame is a transverse tie at each
    # end. Both sit at girder level in the wing channel, so neither is
    # in the water and neither fouls the docked float (top z 530).
    bb, bh = P.HANGAR_BIGHT
    by = P.GIRDER_Y + gb / 2
    for tx, tag in ((P.GIRDER_X0, "bight"), (P.GIRDER_X1 - bb, "forward")):
        parts.append(box(bb, 2 * by, bh,
                         (tx, -by, gz - bh / 2)))
        for s_ in (-1, 1):                      # gussets into the girders
            parts.append(box(bb + 260, 90, bh - 30,
                             (tx - 130, s_ * P.GIRDER_Y - 45, gz - bh / 2 + 15)))

    # ---- THE DRAWBAR. Demountable: on the road it pins into two
    # sockets on the bight and drops to the car ball 445 mm over the
    # tarmac; at sea it comes off and stows flat on a float deck, so
    # nothing stands in the water or rears over the transom.
    if tow == "land":
        nose_x = P.GIRDER_X0 - P.DRAWBAR_LEN
        nose_z = P.GROUND_Z + P.COUPLING_H
        for s_ in (-1, 1):                      # the A
            parts.append(rod((P.GIRDER_X0 + bb / 2, s_ * (by - 90), gz),
                             (nose_x + 300, 0, nose_z + 60), P.DRAWBAR_TUBE))
        parts.append(rod((nose_x + 330, 0, nose_z + 60),
                         (nose_x, 0, nose_z), P.DRAWBAR_TUBE))
        # coupling head, ball, safety-chain eyes
        parts.append(box(240, 160, 140, (nose_x - 40, -80, nose_z - 55)))
        locks.append(Part.makeSphere(P.COUPLING_BALL / 2,
                                     Vector(nose_x + 30, 0, nose_z - 60)))
        for s_ in (-1, 1):
            parts.append(Part.makeTorus(
                30, 8, Vector(nose_x + 140, s_ * 95, nose_z - 20),
                Vector(0, 1, 0)))
        # jockey wheel, clamped to the drawbar
        parts.append(Part.makeCylinder(
            55, 420, Vector(nose_x + 470, 150, nose_z - 340), Vector(0, 0, 1)))
        parts.append(Part.makeCylinder(
            P.JOCKEY_D / 2, 80, Vector(nose_x + 470, 110, nose_z - 340),
            Vector(0, 1, 0)))
    else:
        # the sockets the A-frame pins into - lugs on the bight's face
        for s_ in (-1, 1):
            parts.append(box(110, 160, 160,
                             (P.GIRDER_X0 - 110, s_ * (by - 90) - 80,
                              gz - 80)))

    if not coupled:
        off = Placement(Vector(P.HANGAR_STANDOFF, 0,
                               P.hangar_standoff_z()), Rotation())
        for grp in (parts, locks, rubber):
            for shp in grp:
                shp.Placement = off.multiply(shp.Placement)
    return (Part.makeCompound(parts), Part.makeCompound(locks),
            Part.makeCompound(rubber))


def build_frame():
    """EXTERNAL space frame (docs/structure.md). Nothing crosses the
    living volume: two chassis rails half-buried in the topsides at
    shoulder height, two sheer rails on the side-deck strip, external
    straps between them at the arm stations, and transverse ties only
    at bow and stern — the only places the folded floats leave free."""
    def gunw(x):
        st = P.STATIONS
        for i in range(len(st) - 1):
            if st[i][0] <= x <= st[i + 1][0]:
                t = (x - st[i][0]) / (st[i + 1][0] - st[i][0])
                return st[i][1] + t * (st[i + 1][1] - st[i][1])
        return st[-1][1]

    def hw(x, z):
        st = P.STATIONS
        for i in range(len(st) - 1):
            if st[i][0] <= x <= st[i + 1][0]:
                t = (x - st[i][0]) / (st[i + 1][0] - st[i][0])
                yc = st[i][2] + t * (st[i + 1][2] - st[i][2])
                yg = st[i][1] + t * (st[i + 1][1] - st[i][1])
                zc = st[i][4] + t * (st[i + 1][4] - st[i][4])
                zs = st[i][5] + t * (st[i + 1][5] - st[i][5])
                return yc + (z - zc) / (zs - zc) * (yg - yc)
        return st[-1][2]

    parts = []
    xs = [250, 900, 1400, 2400, 3400, 4400, 5400, 6200, 6700, 7000]
    for sgn in (-1, 1):
        chassis = [(x, sgn * (hw(x, P.SH_Z) - P.FRAME_RAIL_BURY), P.SH_Z)
                   for x in xs]
        sheer = [(x, sgn * (gunw(x) - P.FRAME_SHEER_INSET), P.CABIN_BASE_Z)
                 for x in xs]
        for a, c in zip(chassis, chassis[1:]):
            parts.append(rod(a, c, P.FRAME_TUBE))
        for a, c in zip(sheer, sheer[1:]):
            if a[0] >= P.GATE_X0 - 60 and c[0] <= P.GATE_X1 + 60:
                continue                  # boarding gate to the balcony
            parts.append(rod(a, c, P.FRAME_SHEER_TUBE))
        # external straps tying the two rails, on the outside of the skin
        for sx in P.FRAME_STRAP_X:
            parts.append(rod(
                (sx, sgn * (hw(sx, P.SH_Z) - P.FRAME_RAIL_BURY), P.SH_Z),
                (sx, sgn * (gunw(sx) - P.FRAME_SHEER_INSET), P.CABIN_BASE_Z),
                P.FRAME_TUBE - 25))
            parts.append(Part.makeCylinder(     # shoulder-pin boss
                P.FRAME_TUBE / 2 + 30, 190,
                Vector(sx - 95, sgn * P.SH_Y - 95, P.SH_Z), Vector(0, 1, 0)))
    # transverse ties: only where the folded floats leave the underside free
    r250 = hw(250, P.SH_Z) - P.FRAME_RAIL_BURY
    parts.append(rod((250, -r250, P.SH_Z), (250, r250, P.SH_Z), P.FRAME_BEAM))
    # stern: pivot brackets for the tow/gantry arch, aft of the transom
    parts.append(rod((P.ARCH_PIVOT_X, -P.ARCH_PIVOT_Y, P.ARCH_PIVOT_Z),
                     (P.ARCH_PIVOT_X, P.ARCH_PIVOT_Y, P.ARCH_PIVOT_Z),
                     P.FRAME_BEAM))
    for sgn in (-1, 1):
        parts.append(rod((250, sgn * r250, P.SH_Z),
                         (P.ARCH_PIVOT_X, sgn * P.ARCH_PIVOT_Y,
                          P.ARCH_PIVOT_Z), P.FRAME_TUBE))
    # bow: fixed external stem band — the collision protection now that
    # the arch has moved aft. No moving parts at the pretty end.
    r7000 = hw(7000, P.SH_Z) - P.FRAME_RAIL_BURY
    for sgn in (-1, 1):
        parts.append(rod((7000, sgn * r7000, P.SH_Z),
                         (7150, sgn * 330, 800), P.FRAME_TUBE))
        parts.append(rod((7150, sgn * 330, 800), (7215, 0, 840),
                         P.FRAME_TUBE))
    return Part.makeCompound(parts)


def build_aft_entry(rail_up=False, door_open=False):
    """Deep self-draining cockpit with side benches, storm door with
    1700 mm clear height, cantilevered rain porch (no deck posts —
    diagonal tubes to the wall), alternating-tread ladder hard against
    the aft wall, AC box and lockers. One folding outboard handrail."""
    parts, glass, dark = [], [], []
    x0, x1 = P.COCKPIT_X0, P.COCKPIT_X1

    # --- side benches: seats, and the step from the well up to the deck
    for sgn in (-1, 1):
        parts.append(box(x1 - x0 - 120, P.BENCH_DEPTH, 60,
                         (x0 + 60, sgn * P.COCKPIT_HW - (P.BENCH_DEPTH
                                                         if sgn > 0 else 0),
                          P.BENCH_Z - 60)))
        parts.append(box(x1 - x0 - 120, 50, P.BENCH_Z - P.COCKPIT_FLOOR,
                         (x0 + 60,
                          sgn * (P.COCKPIT_HW - P.BENCH_DEPTH) - (50 if sgn > 0
                                                                  else 0),
                          P.COCKPIT_FLOOR)))

    # --- cantilevered porch: no posts, two diagonal tubes to the wall
    pz = P.CABIN_ROOF_Z - P.PORCH_T
    parts.append(box(P.PORCH_X1 - P.PORCH_X0, 2 * P.PORCH_HW, P.PORCH_T,
                     (P.PORCH_X0, -P.PORCH_HW, pz)))
    parts.append(box(70, 2 * P.PORCH_HW, 90, (P.PORCH_X0, -P.PORCH_HW,
                                              pz - 90)))        # aft fascia
    for sgn in (-1, 1):                                          # side fascia
        parts.append(box(P.PORCH_X1 - P.PORCH_X0, 70,  90,
                         (P.PORCH_X0, sgn * P.PORCH_HW - (70 if sgn > 0
                                                          else 0),
                          pz - 90)))
    for sgn in (-1, 1):
        parts.append(rod((P.PORCH_X0 + 90, sgn * P.PORCH_STRUT_Y,
                          P.CABIN_ROOF_Z - P.PORCH_T),
                         (P.CABIN_X0 - 20, sgn * P.PORCH_STRUT_Y, 1430), 85))
    parts.append(box(P.CABIN_X0 - P.PORCH_X1 + 60, 2 * P.PORCH_HW, 60,
                     (P.PORCH_X1 - 30, -P.PORCH_HW,
                      P.CABIN_ROOF_Z - P.PORCH_T - 30)))        # flashing

    # --- companionway: storm sill, frame, gasketed door leaf
    parts.append(box(180, 2 * P.DOOR_HW + 160, P.DOOR_Z0 - P.COCKPIT_FLOOR,
                     (x1 - 90, -P.DOOR_HW - 80, P.COCKPIT_FLOOR)))
    for sgn in (-1, 1):
        parts.append(box(150, 70, P.DOOR_Z1 - P.DOOR_Z0,
                         (x1 - 75, sgn * P.DOOR_HW - 35, P.DOOR_Z0)))
    parts.append(box(150, 2 * P.DOOR_HW + 70, 70,
                     (x1 - 75, -P.DOOR_HW - 35, P.DOOR_Z1 - 35)))
    # sliding leaf: runs to PORT into a pocket under the ladder, so it
    # never swings into the well. Closed it is pulled onto its gaskets
    # by two cam levers (a slider seals as well as a hinged door only if
    # it clamps — hence the cams, not just a track).
    slide = -P.DOOR_SLIDE if door_open else 0
    dark.append(box(50, 2 * P.DOOR_HW - 40, P.DOOR_Z1 - P.DOOR_Z0 - 60,
                    (x1 - 25, -P.DOOR_HW + 20 + slide, P.DOOR_Z0 + 30)))
    glass.append(box(20, 2 * P.DOOR_HW - 300, 800,
                     (x1 - 40, -P.DOOR_HW + 150 + slide, P.DOOR_Z0 + 620)))
    parts.append(rod((x1 - 40, -P.DOOR_HW - P.DOOR_SLIDE - 40, P.DOOR_Z1 + 45),
                     (x1 - 40, P.DOOR_HW + 40, P.DOOR_Z1 + 45), 55))  # track
    parts.append(box(70, P.DOOR_SLIDE + 60, P.DOOR_Z1 - P.DOOR_Z0 + 40,
                     (x1 - 95, -P.DOOR_HW - P.DOOR_SLIDE - 40,
                      P.DOOR_Z0 - 20)))                             # pocket
    for sgn in (-1, 1):                                             # cam levers
        parts.append(Part.makeCylinder(
            26, 110, Vector(x1 - 40, sgn * (P.DOOR_HW - 70) + slide,
                            P.DOOR_Z0 + 620), Vector(-1, 0, 0)))

    # --- alternating-tread ladder, hard against the aft wall (67 deg).
    # Alternating treads are what make this angle walkable in 420 mm of
    # run; a normal stair would need three times the floor space.
    n, sx0, sx1 = P.STAIR_STEPS, P.STAIR_X0, P.STAIR_X1
    z0, z1 = DECK_Z, P.CABIN_ROOF_Z
    rise, going = (z1 - z0) / n, (sx1 - sx0) / n
    ymid = (P.STAIR_Y0 + P.STAIR_Y1) / 2
    for sy in (P.STAIR_Y0 + 50, P.STAIR_Y1 - 50):                # stringers
        parts.append(rod((sx0 - 70, sy, z0 - 30), (sx1 + 50, sy, z1 - 30),
                         140))
    for i in range(n):
        tz = z0 + (i + 1) * rise
        tx = sx0 + i * going
        y_lo = P.STAIR_Y0 + 40 if i % 2 else ymid
        parts.append(box(250, (P.STAIR_Y1 - P.STAIR_Y0) / 2 - 40, 40,
                         (tx - 95, y_lo, tz - 40)))
        parts.append(rod((tx - 95, y_lo, tz - 20),
                         (tx - 95, y_lo + (P.STAIR_Y1 - P.STAIR_Y0) / 2 - 40,
                          tz - 20), 40))

    # Handrail that FOLLOWS THE LADDER: a
    # second side rail parallel to the stringer, offset 220 mm on short
    # standoffs, terminating exactly AT deck level — nothing sticks up
    # above the roof deck.
    ry = P.STAIR_Y0 + 55
    run, rise = sx1 - sx0, z1 - z0
    ln = math.hypot(run, rise)
    ux, uz = run / ln, rise / ln
    off = 220
    rx0, rz0 = sx0 - uz * off, z0 + ux * off
    rx1, rz1 = sx1 - uz * off, z1 + ux * off
    t = (P.CABIN_ROOF_Z - rz0) / (rz1 - rz0)      # clip at the deck
    rx1, rz1 = rx0 + t * (rx1 - rx0), P.CABIN_ROOF_Z
    parts.append(rod((rx0, ry, rz0), (rx1, ry, rz1), 42))
    for f in (0.08, 0.5, 0.92):                   # standoffs to the stringer
        parts.append(rod((sx0 + f * run, ry, z0 + f * rise),
                         (rx0 + f * (rx1 - rx0), ry, rz0 + f * (rz1 - rz0)),
                         30))

    # --- AC ventilator box (upper right) and lockers (rest of the wall)
    ac = box(P.AC_DEPTH, P.AC_Y1 - P.AC_Y0, P.AC_Z1 - P.AC_Z0,
             (x1 - P.AC_DEPTH, P.AC_Y0, P.AC_Z0))
    try:
        ac = ac.makeFillet(55, ac.Edges)          # faired into the wall
    except Exception:
        pass
    parts.append(ac)
    for i in range(6):                            # flush louvre blades
        dark.append(box(16, P.AC_Y1 - P.AC_Y0 - 130, 30,
                        (x1 - P.AC_DEPTH - 6, P.AC_Y0 + 65,
                         P.AC_Z0 + 45 + i * 48)))
    parts.append(box(P.LOCKER_DEPTH, P.LOCKER_Y1 - P.LOCKER_Y0,
                     P.LOCKER_Z1 - P.LOCKER_Z0,
                     (x1 - P.LOCKER_DEPTH, P.LOCKER_Y0, P.LOCKER_Z0)))
    for i in range(2):
        dark.append(box(24, (P.LOCKER_Y1 - P.LOCKER_Y0) / 2 - 30,
                        P.LOCKER_Z1 - P.LOCKER_Z0 - 60,
                        (x1 - P.LOCKER_DEPTH - 20,
                         P.LOCKER_Y0 + 15 + i * (P.LOCKER_Y1 - P.LOCKER_Y0) / 2,
                         P.LOCKER_Z0 + 30)))

    # --- comfortable route from the door out to the balcony walkways:
    # a triangular corner landing at bench height turns the awkward
    # climb into two easy steps, and a grab post bolted to the balcony
    # frame gives a handhold right at the gate.
    for sgn in (-1, 1):
        # wedge landing at bench height along the outboard edge of the
        # well, then a half step up to deck level and straight out
        # through the gate onto the balcony — no detour.
        tri = Part.Face(wire([(P.GATE_X0, sgn * 380, P.LANDING_Z),
                              (P.GATE_X1, sgn * 380, P.LANDING_Z),
                              (P.GATE_X1, sgn * 1180, P.LANDING_Z),
                              (P.GATE_X0, sgn * 1180, P.LANDING_Z)]))
        parts.append(tri.extrude(Vector(0, 0, 55)))
        parts.append(box(P.GATE_X1 - P.GATE_X0, 300, 55,
                         (P.GATE_X0, sgn * 880 - (300 if sgn < 0 else 0),
                          (P.LANDING_Z + DECK_Z) / 2)))       # half step
        parts.append(box(P.GATE_X1 - P.GATE_X0, 240, 50,
                         (P.GATE_X0, sgn * P.GATE_PLATE_Y
                          - (240 if sgn > 0 else 0), DECK_Z)))
    return (Part.makeCompound(parts), Part.makeCompound(dark),
            Part.makeCompound(glass))


def build_stern_gear():
    """Electric self-recovery winch + stern anchor on its roller."""
    # winch and anchor share the centerline: the rode leaves the drum,
    # runs aft and down over the anchor roller right beneath it, so a
    # ramp recovery pulls straight along the keel line with no yaw
    wx, wy, wz = P.WINCH_POS
    bl, bw, bh = P.WINCH_BODY
    parts = [box(bl, bw, bh, (wx - bl / 2, wy - bw / 2, wz - bh / 2))]
    parts.append(Part.makeCylinder(85, bw - 120,
                                   Vector(wx, wy - (bw - 120) / 2, wz),
                                   Vector(0, 1, 0)))               # drum
    # low plinth onto the deck - nothing hangs over the water
    parts.append(box(bl + 60, bw - 80, 90,
                     (wx - (bl + 60) / 2, wy - (bw - 80) / 2,
                      wz - bh / 2 - 90)))
    parts.append(box(50, 240, 150, (wx - bl / 2 - 50, wy - 120,
                                    wz - bh / 2)))                 # stripper
    ax_, ay, az_ = P.ANCHOR_ROLLER
    parts.append(Part.makeCylinder(60, 200, Vector(ax_, ay - 100, az_),
                                   Vector(0, 1, 0)))               # bow roller
    # anchor stowed short and tight against the transom, well above WL
    parts.append(rod((ax_, ay, az_), (ax_ - 90, ay, az_ - 380), 50))
    for sgn in (-1, 1):
        parts.append(rod((ax_ - 90, ay, az_ - 380),
                         (ax_ - 30, sgn * 170, az_ - 500), 40))
    return Part.makeCompound(parts)


BED_DOWN = True          # module flag so a render script can hoist the bed
BUNK_DOWN = True         # upper bunk deployed (False = folded to the deckhead)


def build_interior(bed_down=None, bunk_down=None):
    """Fit-out of the 5300 x 2280 cabin. Returns
    (joinery, soft, appliances, tanks_and_batteries, glass)."""
    S, C = P.SOLE_Z, P.CABIN_CEIL_Z
    HW = P.IN_HW
    joinery, soft, appl, heavy, glass = [], [], [], [], []

    def blk(x0, x1, y0, y1, z0, z1):
        return box(x1 - x0, y1 - y0, z1 - z0, (x0, y0, z0))

    # ---------------- sole + services zone -------------------------
    joinery.append(blk(P.CABIN_X0 + 50, P.CABIN_X1 - 50, -HW, HW, S - 18, S))

    # heads: a wetroom to port — bulkheads, sliding door, fittings
    hx0, hx1 = P.HEADS_X
    hy0, hy1 = P.HEADS_Y
    for (x0, x1) in ((hx0 - 40, hx0), (hx1, hx1 + 40)):     # end bulkheads
        joinery.append(blk(x0, x1, hy0, hy1, S, C))
    door_x0, door_x1 = P.HEADS_DOOR_X
    joinery.append(blk(hx0, door_x0, hy1, hy1 + 40, S, C))  # inboard wall
    joinery.append(blk(door_x1, hx1, hy1, hy1 + 40, S, C))
    joinery.append(blk(door_x0, door_x1, hy1 + 40, hy1 + 62, S + 40, C - 100))
    # toilet, basin on a shelf, shower tray and riser
    appl.append(blk(hx0 + 80, hx0 + 560, hy0 + 90, hy0 + 480, S, S + 420))
    appl.append(Part.makeCylinder(160, 130, Vector(hx0 + 320, hy0 + 285,
                                                   S + 420)))
    joinery.append(blk(hx0 + 60, hx0 + 620, hy0, hy0 + 120, S + 900, C - 200))
    appl.append(blk(hx1 - 620, hx1 - 60, hy0 + 40, hy0 + 420, S + 820,
                    S + 900))                                # basin shelf
    appl.append(Part.makeCylinder(190, 110, Vector(hx1 - 340, hy0 + 230,
                                                   S + 900)))
    joinery.append(blk(hx1 - 700, hx1 - 40, hy0 + 30, hy1 - 30, S, S + 30))
    joinery.append(blk(hx1 - 60, hx1 - 40, hy0 + 200, hy0 + 240,
                       S + 1400, S + 1560))                  # shower riser

    # AC column beside the door: air handler high, utility locker below,
    # duct straight through the aft wall into the external vent box
    ax0, ax1 = P.AC_UNIT_X
    ay0, ay1 = P.AC_UNIT_Y
    joinery.append(blk(ax0, ax1, ay0, ay1, S, P.AC_HANDLER_Z[0]))
    appl.append(blk(ax0, ax1, ay0, ay1, *P.AC_HANDLER_Z))
    for i in range(7):                                       # louvres
        glass.append(blk(ax0 - 14, ax0, ay0 + 40, ay1 - 40,
                         P.AC_HANDLER_Z[0] + 90 + i * 70,
                         P.AC_HANDLER_Z[0] + 130 + i * 70))
    glass.append(blk(P.CABIN_X0 - 20, ax0, P.AC_Y0, P.AC_Y1,
                     P.AC_Z0, P.AC_Z1))                      # duct to the box

    # galley to starboard: counter, washer under it, fridge tower
    gx0, gx1 = P.GALLEY_X
    gy0, gy1 = P.GALLEY_Y
    fx0, fx1 = P.FRIDGE_X
    joinery.append(blk(gx0, fx0, gy0, gy1, S, S + P.COUNTER_H))
    joinery.append(blk(gx0 - 20, fx0 + 20, gy0 - 20, gy1, S + P.COUNTER_H,
                       S + P.COUNTER_H + 40))                # worktop
    appl.append(blk(gx0 + 20, gx0 + 20 + P.WASHER_W, gy0 + 40, gy1 - 40,
                    S + 120, S + P.COUNTER_H - 60))          # washer-dryer
    glass.append(blk(fx0 - 470, fx0 - 60, gy0 + 90, gy1 - 90,
                     S + P.COUNTER_H + 30, S + P.COUNTER_H + 44))  # hob
    appl.append(blk(gx0 + 40, gx0 + 440, gy0 + 120, gy1 - 120,
                    S + P.COUNTER_H - 160, S + P.COUNTER_H + 20))  # sink
    joinery.append(blk(fx0, fx1, gy0, gy1, S, P.OH_Z1))      # fridge tower
    glass.append(blk(fx0 - 16, fx0, gy0 + 60, gy1 - 60, S + 180, S + 1250))
    glass.append(blk(fx0 - 16, fx0, gy0 + 60, gy1 - 60, S + 1330, P.OH_Z1 - 120))
    # locker band over the worktop — this side has no picture window
    joinery.append(blk(gx0, fx0, gy1 - P.GAL_OH_DEPTH, gy1, *P.GAL_OH_Z))

    # ---------------- dinette --------------------------------------
    bx0, bx1 = P.BERTH_X
    for sy in (-1, 1):
        y_out = sy * HW
        y_in = sy * (HW - P.SETTEE_D)
        y0, y1 = min(y_out, y_in), max(y_out, y_in)
        joinery.append(blk(bx0, bx1, y0, y1, S, S + P.SEAT_H))   # base
        soft.append(blk(bx0, bx1, y0, y1, S + P.SEAT_H, S + P.SEAT_H + 110))
        soft.append(blk(bx0, bx1, min(y_out, y_out - sy * 130),
                        max(y_out, y_out - sy * 130),
                        S + P.SEAT_H + 110, S + 800))            # backrest
        # drawers facing the aisle
        for i in range(3):
            joinery.append(blk(bx0 + 60 + i * 620, bx0 + 620 + i * 620,
                               min(y_in, y_in - sy * 18),
                               max(y_in, y_in - sy * 18),
                               S + 60, S + P.SEAT_H - 60))
        # shelf band UNDER the window: the glazing owns 1500-2100 here,
        # so the storage goes below it rather than blinding the saloon
        joinery.append(blk(bx0 - 50, bx1 + 50,
                           min(y_out, y_out - sy * P.SHELF_DEPTH),
                           max(y_out, y_out - sy * P.SHELF_DEPTH),
                           *P.SHELF_Z))
    # ---- UPPER BUNK over the starboard settee (folds to the deckhead)
    sy = P.BUNK_SIDE
    y_out = sy * HW
    y_in = sy * (HW - P.SETTEE_D)
    by0, by1 = min(y_out, y_in), max(y_out, y_in)
    bz = P.BUNK_BASE_Z if bunk_down else P.BUNK_STOW_Z
    joinery.append(blk(bx0, bx1, by0, by1, bz, bz + P.BUNK_FRAME_T))
    soft.append(blk(bx0 + 20, bx1 - 20, by0 + 20, by1 - 20,
                    bz + P.BUNK_FRAME_T,
                    bz + P.BUNK_FRAME_T + P.BUNK_MATTRESS_T))
    # hinge line on the hull side, and the two struts that hold it level
    glass.append(rod((bx0, y_out - sy * 30, bz + P.BUNK_FRAME_T / 2),
                     (bx1, y_out - sy * 30, bz + P.BUNK_FRAME_T / 2), 40))
    if bunk_down:
        for fx in (bx0 + 200, bx1 - 200):
            glass.append(rod((fx, y_in, bz + P.BUNK_FRAME_T),
                             (fx, y_out - sy * 60, C - 40), 26))
        # lee cloth along the inboard edge
        soft.append(blk(bx0 + 60, bx1 - 60, y_in - sy * 18, y_in,
                        bz + P.BUNK_FRAME_T,
                        bz + P.BUNK_FRAME_T + P.BUNK_LEE_H))
        # two fold-out treads to climb up at the aft end
        for k, sz in enumerate(P.BUNK_STEP_Z):
            joinery.append(blk(P.BUNK_STEP_X[0], P.BUNK_STEP_X[1],
                               min(y_in, y_in - sy * 260),
                               max(y_in, y_in - sy * 260), sz, sz + 40))

    # removable table on a floor socket
    joinery.append(blk((bx0 + bx1 - P.TABLE_L) / 2,
                       (bx0 + bx1 + P.TABLE_L) / 2,
                       -P.TABLE_W / 2, P.TABLE_W / 2,
                       P.TABLE_Z, P.TABLE_Z + 34))
    joinery.append(Part.makeCylinder(45, P.TABLE_Z - S,
                                     Vector((bx0 + bx1) / 2, 0, S)))
    # 50 kWh of cells fill BOTH settee bases, symmetrically: lowest
    # possible, amidships, and no list. Water goes under the sole.
    for sy in (-1, 1):
        heavy.append(blk(*P.BATT_BOX_X,
                         min(sy * HW + sy * 40, sy * (HW - P.SETTEE_D + 40)),
                         max(sy * HW + sy * 40, sy * (HW - P.SETTEE_D + 40)),
                         S + 40, S + 40 + P.BATT_BOX_H))
    heavy.append(blk(*P.TANK_BILGE_X, -P.TANK_BILGE_HW, P.TANK_BILGE_HW,
                     S - 18 - P.TANK_BILGE_H, S - 18))     # bilge water tank

    # ---------------- wardrobes + bed ------------------------------
    wx0, wx1 = P.WARDROBE_X
    for sy in (-1, 1):
        y_out = sy * HW
        joinery.append(blk(wx0, wx1, min(y_out, y_out - sy * P.WARDROBE_W),
                           max(y_out, y_out - sy * P.WARDROBE_W), S, C))
    bdx0, bdx1 = P.BED_X
    appl.append(blk(*P.ELEC_X, -HW + 60, -HW + 500,
                    S + 40, S + 700))                    # inverter cabinet

    # ELEVATING BED: platform on four corner rails, hoisted by four
    # cables off ONE shaft under the deckhead — one shaft means the
    # corners cannot go out of sync. Worm gearbox holds it anywhere;
    # a lever/crank socket drives it by hand if the power is off.
    if bed_down is None:
        bed_down = BED_DOWN
    if bunk_down is None:
        bunk_down = BUNK_DOWN
    bz = P.BED_DOWN_Z if bed_down else P.BED_UP_Z
    joinery.append(blk(bdx0 + 40, bdx0 + 40 + P.MATTRESS_W,
                       -P.MATTRESS_L / 2 - 60, P.MATTRESS_L / 2 + 60,
                       bz, bz + P.BED_FRAME_T))
    soft.append(blk(bdx0 + 60, bdx0 + 60 + P.MATTRESS_W - 40,
                    -P.MATTRESS_L / 2, P.MATTRESS_L / 2,
                    bz + P.BED_FRAME_T, bz + P.BED_FRAME_T + P.MATTRESS_T))
    rails_x = (bdx0 + 70, bdx0 + 10 + P.MATTRESS_W)
    for rx in rails_x:
        for sy in (-1, 1):
            ry = sy * (P.MATTRESS_L / 2 + 30)
            joinery.append(blk(rx - P.BED_RAIL / 2, rx + P.BED_RAIL / 2,
                               ry - P.BED_RAIL / 2, ry + P.BED_RAIL / 2,
                               S, C))                      # guide rail
            glass.append(rod((rx, ry, bz + P.BED_FRAME_T),
                             (rx, ry, C - 60), P.BED_CABLE))   # hoist cable
    # common drive shaft + gearmotor under the deckhead
    glass.append(rod((rails_x[0], -P.MATTRESS_L / 2 - 30, C - 60),
                     (rails_x[0], P.MATTRESS_L / 2 + 30, C - 60),
                     P.BED_SHAFT))
    glass.append(rod((rails_x[1], -P.MATTRESS_L / 2 - 30, C - 60),
                     (rails_x[1], P.MATTRESS_L / 2 + 30, C - 60),
                     P.BED_SHAFT))
    glass.append(rod((rails_x[0], 0, C - 60), (rails_x[1], 0, C - 60),
                     P.BED_SHAFT))
    appl.append(blk(rails_x[0] + 80, rails_x[0] + 380, -120, 180,
                    C - 200, C - 40))                      # gearmotor
    # no fixed seat here on purpose: with the bed hoisted the whole
    # 1500 x 2280 forward zone is free floor, which is the point of it
    # over the bed: shelves in the solid piers between the windows, and
    # a shelf across the forward bulkhead under the windshield
    for sy in (-1, 1):
        joinery.append(blk(bdx0 + 40, bdx1 - 40,
                           min(sy * HW, sy * (HW - P.SHELF_DEPTH)),
                           max(sy * HW, sy * (HW - P.SHELF_DEPTH)),
                           *P.SHELF_Z))
    joinery.append(blk(P.CABIN_X1 - 300, P.CABIN_X1 - 60, -HW + 60, HW - 60,
                       *P.SHELF_Z))
    return (Part.makeCompound(joinery), Part.makeCompound(soft),
            Part.makeCompound(appl), Part.makeCompound(heavy),
            Part.makeCompound(glass))


def build_front_dome():
    """The SKY DOME over the foredeck: a glazed conservatory the crew
    sits in. Half a dome, cut flat by the deck - the deck is its floor.
    Its aft arch IS the cabin's front opening, so the top of the glass
    lands on the box's own upper corners; forward it rounds off and
    closes onto the bow.

    EVERY PANE IS FLAT - no bent glass anywhere, so any pane can be
    re-cut by a local glazier. Flat quads cannot tile a dome (they twist
    124 mm), so each cell is split on its diagonal into two triangles,
    which are planar by definition. Two tube purlins run across the
    middle to keep the panes small, and the nose closes with a flat bow
    pane. Returns (glass, frame)."""
    rings = P.dome_rings()
    glass, frame = [], []

    for pts in P.dome_panes():
        try:
            face = Part.Face(wire([tuple(q) for q in pts]))
            glass.append(face.extrude(
                Vector(*[c * P.DOME_GLASS_T for c in face.normalAt(0, 0)])))
        except Exception:
            pass

    fh, fw = P.DOME_FRAME_H, P.DOME_FRAME_W
    for p in range(len(rings[0])):             # the eight meridian seams
        for b in range(len(rings) - 1):
            if rings[b][p] != rings[b + 1][p]:
                frame.append(rod(rings[b][p], rings[b + 1][p], fh))
    for b, ring in enumerate(rings):           # rims and the TWO TUBES
        d = P.DOME_TUBE_D if 0 < b < len(rings) - 1 else fw
        for i in range(len(ring) - 1):
            if ring[i] != ring[i + 1]:
                frame.append(rod(ring[i], ring[i + 1], d))
    for b in range(len(rings) - 1):            # the diagonal in each cell
        a, c = rings[b], rings[b + 1]
        for p in range(len(a) - 1):
            if p < P.DOME_PANELS / 2:          # mirrored about the
                q0, q1 = a[p], c[p + 1]        # centreline
            else:
                q0, q1 = a[p + 1], c[p]
            if q0 != q1:
                frame.append(rod(q0, q1, fh - 6))
    bow = rings[-1]                            # sill under the bow pane
    z0 = min(q[2] for q in bow)
    for i in range(len(bow) - 1):
        frame.append(rod((bow[i][0], bow[i][1], z0),
                         (bow[i + 1][0], bow[i + 1][1], z0), fw))
    return Part.makeCompound(glass), Part.makeCompound(frame)


def build_dome_sole():
    """The saloon sole runs straight on under the dome, so you walk out
    of the living quarters into the glass without a step. The foredeck
    is opened over the dome footprint (build_hull) and this is the floor
    at the bottom of it, with one step up where the hull rises."""
    parts = []
    x0, x1 = P.CABIN_X1 - 200, P.DOME_SOLE_X1
    plan = []
    n = 8
    for i in range(n + 1):
        x = x0 + (x1 - x0) * i / n
        plan.append((x, -(P.sheer_at(x)[0] - 130)))
    for i in range(n, -1, -1):
        x = x0 + (x1 - x0) * i / n
        plan.append((x, P.sheer_at(x)[0] - 130))
    inside = loft_sections(hull_sections(inner=True))
    parts.append(plan_prism(plan, P.SOLE_Z - 30, P.SOLE_Z).common(inside))
    # step up onto the bow locker top, forward of the sole
    hw = P.sheer_at(P.DOME_SOLE_X1)[0] - 130
    parts.append(box(240, 2 * hw, 30,
                     (P.DOME_SOLE_X1, -hw, P.SOLE_Z + 220)).common(inside))
    return Part.makeCompound(parts)

def build_main_jet():
    """Main-hull waterjet: VERTICAL flush grids on the submerged part
    of the transom, flanking the jet nozzle. No bottom openings — no
    down-suction, no added drag. Same 2 kW cartridge inside."""
    parts = []
    for sgn in (-1, 1):
        cy = sgn * P.MAIN_GRID_Y
        parts.append(box(16, P.MAIN_GRID_L + 60, P.MAIN_GRID_H + 60,
                         (-16, cy - P.MAIN_GRID_L / 2 - 30,
                          P.MAIN_GRID_Z - P.MAIN_GRID_H / 2 - 30)))
        for iy in range(18):
            for iz in range(4):
                parts.append(Part.makeCylinder(
                    P.JET_HOLE_D / 2 + 3, 6,
                    Vector(-22, cy - P.MAIN_GRID_L / 2 + 45 + iy * 45,
                           P.MAIN_GRID_Z - P.MAIN_GRID_H / 2 + 30 + iz * 45),
                    Vector(-1, 0, 0)))
    mx, my, mz = P.MAIN_NOZZLE
    parts.append(Part.makeCone(110, P.JET_NOZZLE_D / 2, 180,
                               Vector(mx + 30, my, mz), Vector(-1, 0, 0)))
    parts.append(Part.makeCylinder(P.JET_NOZZLE_D / 2 - 12, 30,
                                   Vector(mx - 155, my, mz),
                                   Vector(-1, 0, 0)))
    return Part.makeCompound(parts)


# ---------------------------------------------------------------
# Document assembly
# ---------------------------------------------------------------
def build_mode(mode):
    cfg = P.MODES[mode]
    doc = App.newDocument("boat_" + mode)

    # A HEADLESS build writes no GuiDocument.xml - there is no GUI, so
    # there are no view providers to save. Open such a file later and
    # FreeCAD invents defaults: every object hidden, every colour grey,
    # and nothing for ViewFit to fit. That is why a freshly built model
    # looked like it "would not load".
    #
    # So record the appearance as we go and write it beside the .FCStd.
    # open_modes.py applies it when the document is opened.
    look = {}

    def add(name, shape, color=None, transparency=0, group=None):
        obj = doc.addObject("Part::Feature", name)
        obj.Shape = shape
        if group:
            group.addObject(obj)
        if color:
            look[name] = {"color": list(color), "transparency": transparency}
            if App.GuiUp:
                obj.ViewObject.ShapeColor = color
                obj.ViewObject.Transparency = transparency
        return obj

    g_gear = doc.addObject("App::DocumentObjectGroup", "Hangar")

    add("Hull", build_hull(), HULL_COL)
    cabin, panes = build_cabin()
    add("Cabin", cabin, WHITE)
    add("Glazing", panes, (0.5, 0.7, 0.8), 70)

    g_int = doc.addObject("App::DocumentObjectGroup", "Interior")
    ijoin, isoft, iappl, iheavy, iglass = build_interior()
    add("Joinery", ijoin, (0.80, 0.71, 0.55), group=g_int)
    add("Cushions", isoft, (0.45, 0.50, 0.55), group=g_int)
    add("Appliances", iappl, (0.88, 0.89, 0.91), group=g_int)
    add("BatteriesTanks", iheavy, (0.25, 0.42, 0.35), group=g_int)
    add("Fittings", iglass, (0.20, 0.22, 0.24), group=g_int)

    g_roof = doc.addObject("App::DocumentObjectGroup", "RoofDeck")
    tdeck, tlam, tframe, _g, _r = build_terrace(cfg.get("rails", 0))
    add("Terrace", tdeck, WHITE, group=g_roof)
    add("DeckLaminates", tlam, PANEL, group=g_roof)
    add("DeckFrame", tframe, (0.62, 0.64, 0.67), group=g_roof)

    pod = P.pod_at(cfg["phi"])
    fx_now = P.float_x(cfg["phi"])
    # the float NEVER rotates: it rides upright in every pose. The only
    # rotation anywhere is each wheel's 180-deg flip arm.
    (fl, strips, forks, tires, rims, wboxes,
     hatch, hydraulics, thruster) = build_float(pod, 0,
                                                P.float_yaw(cfg["phi"]),
                                                fx_now)
    hframe, hlocks, htyres = build_hangar(cfg["phi"], cfg.get("coupled", True),
                                  cfg["tow"])
    add("HangarFrame", hframe, (0.55, 0.57, 0.60), group=g_gear)
    add("HangarLocks", hlocks, (0.80, 0.65, 0.20), group=g_gear)
    add("HangarTyres", htyres, (0.12, 0.12, 0.13), group=g_gear)
    cframe, cpanels, chinges = build_curtains(cfg["curt"])
    add("CurtainFrames", cframe, (0.62, 0.64, 0.67), group=g_gear)
    add("CurtainPanels", cpanels, PANEL, group=g_gear)
    add("CurtainHinges", chinges, GRAY, group=g_gear)
    stand_off = (None if cfg.get("coupled", True) else
                 Placement(Vector(P.HANGAR_STANDOFF, 0, P.hangar_standoff_z()),
                           Rotation()))

    def _off(shape):
        if stand_off is not None and shape is not None:
            shape = shape.copy()
            shape.Placement = stand_off.multiply(shape.Placement)
        return shape

    for side, mir in (("Stb", False), ("Port", True)):
        m = (lambda s: _off(mirror_y(s))) if mir else _off
        add(f"Float{side}", m(fl), ORANGE, group=g_gear)
        add(f"FloatSolar{side}", m(strips), PANEL, group=g_gear)
        add(f"WheelForks{side}", m(forks), GRAY, group=g_gear)
        add(f"DriveHatch{side}", m(hatch), WHITE, group=g_gear)
        add(f"Jet{side}", m(thruster), (0.8, 0.65, 0.2), group=g_gear)
        add(f"Hydraulics{side}", m(hydraulics), (0.8, 0.65, 0.2),
            group=g_gear)
        if wboxes:
            add(f"WheelBoxes{side}", m(wboxes), WHITE, group=g_gear)
        for i, t in enumerate(tires):
            add(f"Tire{side}{i}", m(t), DARK, group=g_gear)
        for i, r in enumerate(rims):
            add(f"Rim{side}{i}", m(r), STEEL, group=g_gear)

    add("Frame", build_frame(), (0.42, 0.44, 0.47))
    add("SternGear", build_stern_gear(), (0.55, 0.57, 0.6))
    aft_s, aft_d, aft_g = build_aft_entry(cfg["tow"] == "sea",
                                          cfg["curt"] > 5)
    add("AftEntry", aft_s, WHITE)
    add("AftFittings", aft_d, (0.30, 0.32, 0.35))
    add("DoorGlass", aft_g, (0.5, 0.7, 0.8), 70)
    add("MainJet", build_main_jet(), (0.8, 0.65, 0.2))
    dglass, dframe = build_front_dome()
    add("FrontDome", dglass, (0.72, 0.86, 0.92), 62)
    add("FrontDomeFrame", dframe, (0.62, 0.64, 0.67))
    add("DomeSole", build_dome_sole(), (0.78, 0.72, 0.60))

    if mode == "road":
        add("Ground", box(13000, 9000, 20,
            (P.LOA / 2 - 6500, -4500, P.GROUND_Z - 20)), (0.5, 0.5, 0.5), 40)
    elif mode == "harbor":
        # jack-up stance: floats carry the boat, keel awash
        add("Water", box(13000, 9000, 20,
            (P.LOA / 2 - 6500, -4500, P.HARBOR_WL_Z - 20)),
            (0.55, 0.75, 0.9), 50)
    elif mode == "launch":
        add("Slipway", box(13000, 9000, 20,
            (P.LOA / 2 - 6500, -4500, P.GROUND_Z - 20)), (0.5, 0.5, 0.5), 40)
        add("Water", box(5000, 9000, 20,
            (P.LOA / 2 - 6500, -4500, P.GROUND_Z + 150)), (0.55, 0.75, 0.9), 50)
    else:
        add("Water", box(13000, 9000, 20,
            (P.LOA / 2 - 6500, -4500, P.WL_Z - 20)), (0.55, 0.75, 0.9), 50)

    doc.recompute()
    out = os.path.join(SCRIPT_DIR, f"boat_{mode}.FCStd")
    doc.saveAs(out)
    with open(os.path.join(SCRIPT_DIR, f"boat_{mode}.look.json"), "w") as fh:
        json.dump(look, fh, indent=1, sort_keys=True)
    print("saved", out)
    return doc


def main():
    P.checks(strict=False)
    modes = [a for a in sys.argv if a in P.MODES] or list(P.MODES)
    for m in modes:
        build_mode(m)

    if App.GuiUp:
        import FreeCADGui as Gui
        Gui.activeDocument().activeView().viewIsometric()
        Gui.SendMsgToActiveView("ViewFit")


# Importable: areas.py and beauty_shots.py pull the builders in without
# rebuilding every mode. FreeCAD does NOT set __name__ to "__main__" for
# CLI scripts (it uses the filename), so detect direct launch from argv.
if any(a.endswith("build_boat.py") for a in sys.argv):
    main()
