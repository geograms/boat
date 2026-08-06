# build_boat.py — Dutch-barge boat-home, FreeCAD documents.
#
# Headless:  ~/bin/FreeCAD.AppImage -c freecad/build_boat.py road foiling
# GUI:       ./freecad/view.sh [modes]   (colors applied, view fitted)
#
# Output: freecad/boat_<mode>.FCStd
import os
import sys
import math

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
    return Part.makeLoft(
        [wire([(x, y, z) for y, z in pts]) for x, pts in secs], True, False)


# ---------------------------------------------------------------
# Hull — hollow barge shell with deck, cabin-size opening
# ---------------------------------------------------------------
def hull_sections(inner=False):
    out = []
    for st in P.STATIONS:
        x, yg, yc, zk, zc, zs = st
        if inner:
            yg, yc = max(yg - WALL, 15), max(yc - WALL, 10)
            zk, zc, zs = zk + 60, zc + 40, DECK_Z - 30
        out.append((x, [(P.KEEL_FLAT, zk), (yc, zc), (yg, zs),
                        (-yg, zs), (-yc, zc), (-P.KEEL_FLAT, zk)]))
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
    [0.25,  180, 148,  40, 170],
    [0.42,  110,  85, 150, 250],
    [0.50,   12,  10, 320, 360],
]


def build_float(pod, roll):
    """Stabilizer float with CASTER wheels (stub axles perpendicular to
    the deck): roll 90 = float on its side, wheels vertical (road);
    roll 0 = float flat, wheels flat on the deck (water).
    Starboard, posed."""
    ty, tz = pod
    # -roll about x maps the local deck normal (+z) outboard (+y)
    place = Placement(Vector(0, ty, tz), Rotation(Vector(1, 0, 0), -roll))

    secs = []
    for u, yg, yc, zk, zc in FLOAT_STATIONS:
        x = P.FLOAT_X + u * P.FLOAT_LEN
        h2 = P.FLOAT_H / 2
        pts = [(10, zk - h2), (yc, zc - h2), (yg, h2),
               (-yg, h2), (-yc, zc - h2), (-10, zk - h2)]
        secs.append((x, pts))
    hull_f = loft_sections(secs)

    # bevel the mating face so it sits FLUSH on the hull bottom in road
    # pose: cut with the hull-bottom plane transformed to float-local
    slope = P.BOTTOM_SLOPE
    off = (P.POD_ROAD[1] + 40 * slope - slope * P.POD_ROAD[0])
    theta = math.degrees(math.atan(slope))
    bev = box(P.FLOAT_LEN + 800, 1600, 3200,
              (P.FLOAT_X - P.FLOAT_LEN / 2 - 400, -1600, -1600))
    bev.rotate(Vector(P.FLOAT_X, 0, 0), Vector(1, 0, 0), theta)
    bev.translate(Vector(0, off, 0))
    hull_f = hull_f.cut(bev)

    # wheel wells: the discs sit half-recessed in the deck
    for dx in P.WHEEL_XS:
        hull_f = hull_f.cut(Part.makeCylinder(
            350, P.FLOAT_H / 2, Vector(P.FLOAT_X + dx, P.WHEEL_DROP,
                                       P.FLOAT_H / 2 - 130),
            Vector(0, 0, 1)))
    hull_f.Placement = place.multiply(hull_f.Placement)

    # solar strips on the deck, in the gaps between the wheels
    strips = []
    for x0 in (P.FLOAT_X - 1480, P.FLOAT_X + 200):
        s = box(580, 260, 14, (x0, -130, P.FLOAT_H / 2))
        s.Placement = place.multiply(s.Placement)
        strips.append(s)

    # caster wheels: stub axle along the deck normal, disc half-recessed
    # in the deck well, axle dropped so wheels (not float) touch ground
    forks, tires, rims = [], [], []
    h2 = P.FLOAT_H / 2
    for dx in P.WHEEL_XS:
        wx = P.FLOAT_X + dx
        wz = h2 + P.AXLE_STANDOFF
        ax = Part.makeCylinder(60, 170, Vector(wx, P.WHEEL_DROP, wz - 150),
                               Vector(0, 0, 1))
        ax.Placement = place.multiply(ax.Placement)
        forks.append(ax)
        t = Part.makeTorus((P.WHEEL_DIA - P.WHEEL_W) / 2, P.WHEEL_W / 2,
                           Vector(wx, P.WHEEL_DROP, wz), Vector(0, 0, 1))
        t.Placement = place.multiply(t.Placement)
        tires.append(t)
        r = Part.makeCylinder(P.HUB_DIA / 2, P.WHEEL_W + 40,
                              Vector(wx, P.WHEEL_DROP,
                                     wz - (P.WHEEL_W + 40) / 2),
                              Vector(0, 0, 1))
        r.Placement = place.multiply(r.Placement)
        rims.append(r)

    # in-float hydraulic drive (docs/wheels.md): gasketed deck hatch
    # over the machinery bay, pump unit inside, hoses to each hub,
    # goldenrod hub-motor caps
    bx = P.FLOAT_X + P.MOTOR_BAY_DX
    hatch = box(P.MOTOR_BAY_L + 20, P.MOTOR_BAY_W + 20, 25,
                (bx - (P.MOTOR_BAY_L + 20) / 2,
                 -(P.MOTOR_BAY_W + 20) / 2, h2))
    for sx in (-1, 1):
        for sy in (-1, 1):
            hatch = hatch.fuse(box(60, 30, 35,
                (bx + sx * (P.MOTOR_BAY_L / 2 - 40) - 30,
                 sy * (P.MOTOR_BAY_W / 2 + 5) - 15, h2)))
    hatch.Placement = place.multiply(hatch.Placement)

    hyd = []
    unit = Part.makeCylinder(85, 320, Vector(bx - 260, 0, h2 - 320),
                             Vector(1, 0, 0))          # 48V motor
    hyd.append(unit.fuse(box(240, 220, 200,
                             (bx + 80, -110, h2 - 300))))  # pump+manifold
    for dx in P.WHEEL_XS:                              # hoses to the hubs
        wx = P.FLOAT_X + dx
        hyd.append(rod((bx, 0, h2 + 12), (wx, P.WHEEL_DROP, h2 + 12), 25))
        hyd.append(Part.makeCylinder(                  # hub motor cap
            62, 45, Vector(wx, P.WHEEL_DROP,
                           h2 + P.AXLE_STANDOFF + (P.WHEEL_W + 40) / 2),
            Vector(0, 0, 1)))
    hydraulics = Part.makeCompound(hyd)
    hydraulics.Placement = place.multiply(hydraulics.Placement)

    # flush-intake WATERJET (docs/propulsion.md): perforated grids on
    # BOTH sides -> plenum -> internal duct -> enclosed pump -> tail jet
    gx = P.FLOAT_X + P.JET_GRID_X_LOCAL
    gz = P.JET_Z_LOCAL
    thr = []
    for sgn in (-1, 1):
        gy = sgn * 170                       # flat midbody side face
        # recessed dark panel + frame, flush with the side
        thr.append(box(P.JET_GRID_L + 60, 16, P.JET_GRID_H + 60,
                       (gx - P.JET_GRID_L / 2 - 30, gy - 8 * sgn - 8,
                        gz - P.JET_GRID_H / 2 - 30)))
        # hole pattern: light discs proud of the panel
        for ix in range(28):
            for iz in range(5):
                hx = gx - P.JET_GRID_L / 2 + 45 + ix * 45
                hz = gz - P.JET_GRID_H / 2 + 30 + iz * 45
                d = Part.makeCylinder(
                    P.JET_HOLE_D / 2 + 3, 6,
                    Vector(hx, gy + 9 * sgn, hz), Vector(0, sgn, 0))
                thr.append(d)
    # jet nozzle out the tail cone
    tail = P.FLOAT_X - P.FLOAT_LEN / 2
    noz = Part.makeCone(110, P.JET_NOZZLE_D / 2, 200,
                        Vector(tail + 40, 0, gz), Vector(-1, 0, 0))
    thr.append(noz)
    thr.append(Part.makeCylinder(P.JET_NOZZLE_D / 2 - 12, 30,
                                 Vector(tail - 165, 0, gz),
                                 Vector(-1, 0, 0)))
    thruster = Part.makeCompound(thr)
    thruster.Placement = place.multiply(thruster.Placement)

    # low-profile boxes over the flat wheels: water pose only
    boxes = []
    if abs(roll) < 45:
        for dx in P.WHEEL_XS:
            wx = P.FLOAT_X + dx
            bw = P.WHEELBOX_Y1 - P.WHEELBOX_Y0
            outer = box(P.WHEELBOX_L, bw, P.WHEELBOX_H,
                        (wx - P.WHEELBOX_L / 2, P.WHEELBOX_Y0, h2))
            inner = box(P.WHEELBOX_L - 50, bw + 100, P.WHEELBOX_H - 25,
                        (wx - (P.WHEELBOX_L - 50) / 2, P.WHEELBOX_Y0 + 25,
                         h2 - 20))
            b = outer.cut(inner)
            b.Placement = place.multiply(b.Placement)
            boxes.append(b)
    return hull_f, Part.makeCompound(strips), Part.makeCompound(forks), \
        tires, rims, (Part.makeCompound(boxes) if boxes else None), \
        hatch, hydraulics, thruster


def build_arms(phi, dx=0.0):
    """Elbowed arm per station - the inverted V. Two tube segments,
    shoulder and elbow both 24 V worm slew drives; phi 90 = sea stance,
    phi 0 = folded under the hull. `dx` staggers the stations so the
    folded elbows of the two sides pass each other. Starboard, posed."""
    J, Pod = P.arm_joints(phi)
    parts, drives = [], []
    for ax0 in P.ARM_X:
        ax = ax0 + dx
        # shoulder slew drive on the spine
        drives.append(Part.makeCylinder(
            P.ARM_DRIVE_D / 2, P.ARM_T + 120,
            Vector(ax - (P.ARM_T + 120) / 2, P.SH_Y, P.SH_Z),
            Vector(1, 0, 0)))
        # upper segment, shoulder -> elbow
        parts.append(rod((ax, P.SH_Y, P.SH_Z), (ax, J[0], J[1]), P.ARM_T))
        # elbow slew drive
        drives.append(Part.makeCylinder(
            P.ARM_DRIVE_D / 2 - 20, P.ARM_T + 90,
            Vector(ax - (P.ARM_T + 90) / 2, J[0], J[1]), Vector(1, 0, 0)))
        # lower segment, elbow -> float
        parts.append(rod((ax, J[0], J[1]), (ax, Pod[0], Pod[1]), P.ARM_T))
        # welded foot at the float
        parts.append(box(P.ARM_T + 80, 170, 60,
                         (ax - (P.ARM_T + 80) / 2, Pod[0] - 85, Pod[1] - 30)))
    return parts, drives


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


def build_hangar(phi, coupled=True):
    """The U-frame hangar as its own vehicle: two spine beams along the
    hull sides carrying the four arm shoulders, joined aft of the
    transom by the bight, which carries the drawbar.

    phi     arm swing, 0 = floats under the hull (road),
            90 = splayed (dinghy / approach pose)
    coupled False shifts the whole frame aft and out, the way it sits
            while the boat is being driven in

    Returns (frame, locks) — the arms, floats and wheels stay with
    build_float()/build_arms(), which the hangar carries."""
    sy = P.hangar_spine_y()
    sb, sh = P.HANGAR_SPINE
    x0, x1 = P.HANGAR_SPINE_X
    parts, locks = [], []

    for s_ in (-1, 1):
        # spine beam, hollow alu box
        beam = box(x1 - x0, sb, sh, (x0, s_ * sy - sb / 2, P.LOCK_Z - sh / 2))
        beam = beam.cut(box(x1 - x0 - 2 * 8, sb - 16, sh - 16,
                            (x0 + 8, s_ * sy - sb / 2 + 8,
                             P.LOCK_Z - sh / 2 + 8)))
        parts.append(beam)
        # the spine runs aft to the bight
        parts.append(box(x0 - P.HANGAR_BIGHT_X, sb, sh,
                         (P.HANGAR_BIGHT_X, s_ * sy - sb / 2,
                          P.LOCK_Z - sh / 2)))
        # the shoulder drives live on build_arms(); the spine only
        # carries their mounting bosses
        for ax in P.ARM_X:
            parts.append(Part.makeCylinder(
                60, sb + 40, Vector(ax - (sb + 40) / 2, s_ * sy, P.SH_Z),
                Vector(1, 0, 0)))

    # the bight: cross beam aft of the transom, carrying the drawbar
    bb, bh = P.HANGAR_BIGHT
    parts.append(box(bb, 2 * sy + sb, bh,
                     (P.HANGAR_BIGHT_X - bb, -sy - sb / 2, P.LOCK_Z - bh / 2)))
    # ---- the coupler to the car: an A-frame off the bight ----
    nose_x = P.HANGAR_BIGHT_X - P.DRAWBAR_LEN
    nose_z = P.GROUND_Z + P.COUPLING_H
    for s_ in (-1, 1):                       # the two legs of the A
        parts.append(rod((P.HANGAR_BIGHT_X - bb / 2, s_ * (sy - 200),
                          P.LOCK_Z),
                         (nose_x + 260, 0, nose_z + 40), P.DRAWBAR_TUBE))
    parts.append(rod((nose_x + 300, 0, nose_z + 40),
                     (nose_x, 0, nose_z), P.DRAWBAR_TUBE))
    # coupling head and the ball socket
    parts.append(box(220, 150, 130, (nose_x - 40, -75, nose_z - 50)))
    parts.append(Part.makeSphere(P.COUPLING_BALL / 2,
                                 Vector(nose_x + 30, 0, nose_z - 55)))
    # safety chain eyes
    for s_ in (-1, 1):
        parts.append(Part.makeTorus(28, 7, Vector(nose_x + 120, s_ * 90,
                                                  nose_z - 20),
                                    Vector(0, 1, 0)))
    # jockey wheel, stowed up
    parts.append(rod((nose_x + 420, 150, nose_z + 60),
                     (nose_x + 420, 150, nose_z - 300), 60))
    parts.append(Part.makeCylinder(
        P.JOCKEY_D / 2, 70, Vector(nose_x + 420, 115, nose_z - 300),
        Vector(0, 1, 0)))

    # four cone-and-bayonet locks, pointing INBOARD off the spines
    for (lx, ly, lz) in P.lock_points():
        s_ = 1 if ly > 0 else -1
        root = s_ * (sy - sb / 2)
        cone = Part.makeCone(P.LOCK_CONE_D1 / 2, P.LOCK_CONE_D0 / 2,
                             P.LOCK_CONE_L, Vector(lx, root, lz),
                             Vector(0, -s_, 0))
        locks.append(cone)
        # the T-head that turns 90 deg behind the keeper in the hull
        tip = root - s_ * P.LOCK_CONE_L
        locks.append(Part.makeCylinder(P.LOCK_TWIST_D / 2, 90,
                                       Vector(lx, tip, lz), Vector(0, -s_, 0)))
        locks.append(box(30, 120, 26, (lx - 15, tip - s_ * 90 - 60, lz - 13)))
        # 24 V worm gearmotor on the outboard face
        md, ml = P.LOCK_MOTOR
        locks.append(Part.makeCylinder(
            md / 2, ml, Vector(lx, s_ * (sy + sb / 2), lz), Vector(0, s_, 0)))

    if not coupled:                      # stood off, ready to take the boat
        off = Placement(Vector(P.HANGAR_STANDOFF, 0, P.hangar_standoff_z()),
                           Rotation())
        for grp in (parts, locks):
            for shp in grp:
                shp.Placement = off.multiply(shp.Placement)

    return Part.makeCompound(parts), Part.makeCompound(locks)


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


def build_tow(pose):
    """STERN arch: sea gantry (anchor roller, winch fairlead, lights) /
    extensible drawbar for stern-first towing. Pin-locked both ways."""
    deg = P.ARCH_SEA_DEG if pose == "sea" else P.ARCH_LAND_DEG
    ax, az = P.arch_apex(deg)
    parts = []
    for sgn in (-1, 1):                       # legs, pivot -> apex yoke
        parts.append(rod((P.ARCH_PIVOT_X, sgn * P.ARCH_PIVOT_Y,
                          P.ARCH_PIVOT_Z), (ax, sgn * 170, az), P.ARCH_TUBE))
        parts.append(Part.makeCylinder(       # pivot boss + lock-pin ear
            P.ARCH_TUBE / 2 + 26, 160,
            Vector(P.ARCH_PIVOT_X, sgn * P.ARCH_PIVOT_Y - 80,
                   P.ARCH_PIVOT_Z), Vector(0, 1, 0)))
        parts.append(box(130, 40, 230,
                         (P.ARCH_PIVOT_X - 65, sgn * P.ARCH_PIVOT_Y - 140,
                          P.ARCH_PIVOT_Z - 115)))
    parts.append(rod((ax, -170, az), (ax, 170, az), P.ARCH_TUBE))
    for sgn in (-1, 1):                       # root gussets
        parts.append(Part.Face(wire([
            (P.ARCH_PIVOT_X, sgn * P.ARCH_PIVOT_Y, P.ARCH_PIVOT_Z - 150),
            (P.ARCH_PIVOT_X, sgn * P.ARCH_PIVOT_Y, P.ARCH_PIVOT_Z + 150),
            (P.ARCH_PIVOT_X + (ax - P.ARCH_PIVOT_X) * 0.32,
             sgn * (P.ARCH_PIVOT_Y + (170 - P.ARCH_PIVOT_Y) * 0.32),
             P.ARCH_PIVOT_Z + (az - P.ARCH_PIVOT_Z) * 0.32)])).extrude(
                 Vector(0, sgn * 22, 0)))
    if pose == "sea":
        # gantry fit-out: hanging beam, anchor sheave, nav-light post
        parts.append(rod((ax - 40, -520, az - 90), (ax - 40, 520, az - 90),
                         P.ARCH_TUBE - 15))
        for sgn in (-1, 1):
            parts.append(rod((ax, sgn * 170, az), (ax - 40, sgn * 520,
                                                   az - 90), 60))
        parts.append(Part.makeCylinder(70, 90, Vector(ax - 40, -45, az - 90),
                                       Vector(0, 1, 0)))     # anchor sheave
        parts.append(rod((ax, 0, az), (ax, 0, az + 260), 55))  # light post
    else:
        cx, cz = P.arch_coupling()
        parts.append(rod((ax, 0, az), (cx, 0, cz), P.ARCH_TUBE - 10))
        for sgn in (-1, 1):                   # A-frame triangulation
            parts.append(rod((ax, sgn * 170, az),
                             ((ax + cx) / 2, 0, (az + cz) / 2),
                             P.ARCH_TUBE - 35))
        parts.append(Part.makeSphere(80, Vector(cx, 0, cz)))
        parts.append(box(70, 150, 150, (cx + 150, -75, cz - 40)))
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
    # bracket down to the stern tie, and the chain stripper aft
    for sy in (-1, 1):
        parts.append(box(40, 30, 300,
                         (wx - 20, sy * (bw / 2 - 30), wz - bh / 2 - 290)))
    parts.append(box(50, 240, 150, (wx - bl / 2 - 50, wy - 120,
                                    wz - bh / 2)))                 # stripper
    ax_, ay, az_ = P.ANCHOR_ROLLER
    parts.append(Part.makeCylinder(60, 200, Vector(ax_, ay - 100, az_),
                                   Vector(0, 1, 0)))               # bow roller
    parts.append(rod((ax_, ay, az_), (ax_ - 220, ay, az_ - 620), 55))  # shank
    for sgn in (-1, 1):                                            # flukes
        parts.append(rod((ax_ - 220, ay, az_ - 620),
                         (ax_ - 120, sgn * 240, az_ - 780), 45))
        parts.append(rod((ax_ - 220, ay, az_ - 620),
                         (ax_ - 350, sgn * 150, az_ - 700), 40))
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

    def add(name, shape, color=None, transparency=0, group=None):
        obj = doc.addObject("Part::Feature", name)
        obj.Shape = shape
        if group:
            group.addObject(obj)
        if App.GuiUp and color:
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
    roll = 90 - cfg["phi"]          # rigid arm: roll locked to swing
    (fl, strips, forks, tires, rims, wboxes,
     hatch, hydraulics, thruster) = build_float(pod, roll)
    arms_s, drv_s = build_arms(cfg["phi"])
    arms_p, drv_p = build_arms(cfg["phi"], P.ARM_STAGGER)
    hframe, hlocks = build_hangar(cfg["phi"], cfg.get("coupled", True))
    add("HangarFrame", hframe, (0.55, 0.57, 0.60), group=g_gear)
    add("HangarLocks", hlocks, (0.80, 0.65, 0.20), group=g_gear)
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
        arms_side = arms_p if mir else arms_s
        drv_side = drv_p if mir else drv_s
        for i, a in enumerate(arms_side):
            add(f"Arm{side}{i}", m(a), GRAY, group=g_gear)
        for i, a in enumerate(drv_side):
            add(f"ArmDrive{side}{i}", m(a), STEEL, group=g_gear)
        for i, t in enumerate(tires):
            add(f"Tire{side}{i}", m(t), DARK, group=g_gear)
        for i, r in enumerate(rims):
            add(f"Rim{side}{i}", m(r), STEEL, group=g_gear)

    add("Frame", build_frame(), (0.42, 0.44, 0.47))
    add("SternArch", build_tow(cfg["tow"]), (0.42, 0.44, 0.47))
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


# importable: areas.py and beauty_shots.py pull the builders in without
# rebuilding every mode
if __name__ == "__main__":
    main()
