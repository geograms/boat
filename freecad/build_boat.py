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
    wz0, wh = 1500, 450
    for i in range(6):                              # 6 windows per side
        wx = P.CABIN_X0 + 150 + i * 850
        cuts.append(box(600, P.CABIN_W + 200, wh, (wx, -P.CABIN_W / 2 - 100, wz0)))
        panes.append(box(600, P.CABIN_W - 40, wh, (wx, -P.CABIN_W / 2 + 20, wz0)))
    cuts.append(box(200, 1500, wh, (P.CABIN_X1 - 100, -750, wz0)))   # windshield
    panes.append(box(120, 1500, wh, (P.CABIN_X1 - 60, -750, wz0)))
    cuts.append(door_opening())          # companionway
    for c in cuts:
        shell = shell.cut(c)
    return shell, Part.makeCompound(panes)


# ---------------------------------------------------------------
# Pop-top canopy
# ---------------------------------------------------------------
def build_canopy(lift):
    cl = P.CABIN_X1 - P.CABIN_X0 + 2 * P.CANOPY_OVERHANG
    cw = P.CABIN_W + 2 * P.CANOPY_OVERHANG
    cx = (P.CABIN_X0 + P.CABIN_X1) / 2
    z = P.CABIN_ROOF_Z + lift
    slab = box(cl, cw, P.CANOPY_THICK, (cx - cl / 2, -cw / 2, z))
    try:
        slab = slab.makeFillet(40, slab.Edges)
    except Exception:
        pass
    # 3 x 2 standard modules, landscape
    panels = []
    gx = (cl - 3 * P.PANEL_L) / 4
    for i in range(3):
        for j in (-1, 1):
            panels.append(box(
                P.PANEL_L, P.PANEL_W, P.PANEL_T,
                (cx - cl / 2 + gx + i * (P.PANEL_L + gx),
                 j * 20 - (P.PANEL_W if j < 0 else 0),
                 z + P.CANOPY_THICK)))
    acts = []
    if lift > 1:
        for sx in (-1, 1):
            for sy in (-1, 1):
                acts.append(Part.makeCylinder(
                    30, lift, Vector(cx + sx * (cl / 2 - 180),
                                     sy * (cw / 2 - 180), P.CABIN_ROOF_Z)))
    return slab, Part.makeCompound(panels), acts


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
    roll 0 = float flat, wheels lying flat on the deck (water).
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


def build_arms(phi):
    """Rigid welded arm per station: straight segments cut at angles that
    follow the hull section in road pose. The whole polyline swings
    outboard by phi about the shoulder pin. Starboard, posed."""
    c = math.cos(math.radians(phi))
    s = math.sin(math.radians(phi))

    def rot(p):
        vy, vz = p[0] - P.SH_Y, p[1] - P.SH_Z
        return (P.SH_Y + vy * c - vz * s, P.SH_Z + vy * s + vz * c)

    pts = [rot(p) for p in P.ARM_POLY_ROAD]
    parts = []
    for ax in P.ARM_X:
        # shoulder pin lug — the ONLY rotating joint
        parts.append(Part.makeCylinder(
            P.ARM_T / 2 + 30, P.ARM_T + 100,
            Vector(ax - (P.ARM_T + 100) / 2, P.SH_Y, P.SH_Z),
            Vector(1, 0, 0)))
        # fully welded segments; angle-cut joints with gusset plates
        for a, b in zip(pts, pts[1:]):
            parts.append(rod((ax, a[0], a[1]), (ax, b[0], b[1]), P.ARM_T))
        for j in pts[1:-1]:
            parts.append(box(P.ARM_T + 40, 130, 130,
                             (ax - (P.ARM_T + 40) / 2, j[0] - 65,
                              j[1] - 65)))
        # static welded foot plate at the float (no pivot)
        parts.append(box(P.ARM_T + 80, 170, 60,
                         (ax - (P.ARM_T + 80) / 2, pts[-1][0] - 85,
                          pts[-1][1] - 30)))
    # hydraulic actuator: hull side to the mid-arm joint
    acts = []
    mid = pts[len(pts) // 2]
    for ax in P.ARM_X:
        acts.append(rod((ax + 180, P.SH_Y - 60, P.SH_Z - 300),
                        (ax + 180, mid[0], mid[1]), 70))
    return parts, acts


def build_balcony(fold_deg):
    """Solar balcony: horizontal deck on gunwale hinge, 2 big panels,
    edge rail, diagonal brackets. fold_deg 0 = horizontal (water),
    90 = folded up against the cabin (road). Starboard, posed."""
    place = Placement(Vector(0, P.BALC_HINGE_Y, P.BALC_HINGE_Z),
                      Rotation(Vector(1, 0, 0), fold_deg))
    L = P.BALC_X1 - P.BALC_X0

    def posed(s):
        s.Placement = place.multiply(s.Placement)
        return s

    plate = posed(box(L, P.BALC_SPAN, P.BALC_T, (P.BALC_X0, 0, 0)))
    # 3 BIFACIAL modules: active laminate on both faces of the plate
    panels = []
    gx = (L - 3 * P.PANEL_L) / 4
    for i in range(3):
        px = P.BALC_X0 + gx + i * (P.PANEL_L + gx)
        py = (P.BALC_SPAN - P.PANEL_W) / 2
        panels.append(posed(box(P.PANEL_L, P.PANEL_W, P.PANEL_T,
                                (px, py, P.BALC_T))))           # front face
        panels.append(posed(box(P.PANEL_L, P.PANEL_W, P.PANEL_T,
                                (px, py, -P.PANEL_T))))         # rear face
    # outboard edge rail
    rail = posed(box(L, 40, 90, (P.BALC_X0, P.BALC_SPAN - 40, P.BALC_T)))
    # diagonal brackets under the deck, back to the hull side
    braces = []
    for bx in (P.BALC_X0 + 250, (P.BALC_X0 + P.BALC_X1) / 2,
               P.BALC_X1 - 250):
        braces.append(posed(rod((bx, 60, -20),
                                (bx, P.BALC_SPAN - 120, -20), 55)))
    # support legs down onto the wheel-box lids (open pose only)
    if abs(fold_deg) < 10:
        leg_len = P.BALC_HINGE_Z - P.WHEELBOX_TOP_Z
        for dx in P.WHEEL_XS:
            bx = P.FLOAT_X + dx
            if P.BALC_X0 + 200 < bx < P.BALC_X1 - 200:
                braces.append(posed(Part.makeCylinder(
                    35, leg_len, Vector(bx, P.BALC_SPAN - 90, 0),
                    Vector(0, 0, -1))))
    hinges = []
    for hx in (P.BALC_X0 + 200, P.BALC_X1 - 200):
        hinges.append(Part.makeCylinder(
            40, 240, Vector(hx - 120, P.BALC_HINGE_Y, P.BALC_HINGE_Z),
            Vector(1, 0, 0)))
    return plate, Part.makeCompound(panels), \
        rail.fuse(Part.makeCompound(braces)), Part.makeCompound(hinges)


# ---------------------------------------------------------------
# Bow hydrofoil, drawbar, stern pod
# ---------------------------------------------------------------
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
    parts.append(box(P.PORCH_X1 - P.PORCH_X0, 2 * P.PORCH_HW, P.PORCH_T,
                     (P.PORCH_X0, -P.PORCH_HW,
                      P.CABIN_ROOF_Z - P.PORCH_T)))
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

    # ONE folding handrail, outboard side only: up only when the roof
    # terrace is in use, folded flat on the stringer otherwise.
    ry = P.STAIR_Y0 + 45
    if rail_up:
        parts.append(rod((sx0, ry, z0), (sx0, ry, z0 + 950), 60))
        parts.append(rod((sx1, ry, z1), (sx1, ry, z1 + 950), 60))
        parts.append(rod((sx0, ry, z0 + 950), (sx1, ry, z1 + 950), 55))
        parts.append(rod((sx1, ry, z1 + 950), (sx1 + 420, ry, z1 + 950), 55))
        parts.append(rod((sx1 + 420, ry, z1 + 950), (sx1 + 420, ry, z1), 55))
    else:
        parts.append(rod((sx0 - 40, ry, z0 + 90), (sx1 + 30, ry, z1 + 90), 55))
        for px in (sx0, sx1):
            pz = z0 + (px - sx0) / (sx1 - sx0) * (z1 - z0)
            parts.append(rod((px, ry, pz), (px, ry, pz + 110), 60))

    # --- AC ventilator box (upper right) and lockers (rest of the wall)
    dark.append(box(P.AC_DEPTH, P.AC_Y1 - P.AC_Y0, P.AC_Z1 - P.AC_Z0,
                    (x1 - P.AC_DEPTH, P.AC_Y0, P.AC_Z0)))
    for i in range(5):
        parts.append(box(30, P.AC_Y1 - P.AC_Y0 - 80, 26,
                         (x1 - P.AC_DEPTH - 15, P.AC_Y0 + 40,
                          P.AC_Z0 + 50 + i * 58)))
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
        tri = Part.Face(wire([(620, sgn * 380, P.LANDING_Z),
                              (x1, sgn * 380, P.LANDING_Z),
                              (x1, sgn * 1180, P.LANDING_Z),
                              (620, sgn * 700, P.LANDING_Z)]))
        parts.append(tri.extrude(Vector(0, 0, 55)))
        parts.append(box(200, 480, 55,
                         (x1 - 220, sgn * 700 - (480 if sgn < 0 else 0),
                          (P.LANDING_Z + DECK_Z) / 2)))       # half step
        parts.append(box(P.GATE_X1 - P.GATE_X0, 220, 50,
                         (P.GATE_X0, sgn * 1090 - 110, DECK_Z)))
        # grab post on the balcony frame + tie back into the cabin wall
        parts.append(rod((P.GRAB_POST_X, sgn * P.GRAB_POST_Y, DECK_Z),
                         (P.GRAB_POST_X, sgn * P.GRAB_POST_Y,
                          DECK_Z + P.GRAB_POST_H), 65))
        parts.append(rod((P.GRAB_POST_X, sgn * P.GRAB_POST_Y,
                          DECK_Z + P.GRAB_POST_H),
                         (P.CABIN_X0 - 30, sgn * (P.CABIN_W / 2 - 40),
                          DECK_Z + P.GRAB_POST_H - 120), 55))
        parts.append(rod((P.GRAB_POST_X, sgn * P.GRAB_POST_Y,
                          DECK_Z + P.GRAB_POST_H),
                         (P.GATE_X1, sgn * P.GRAB_POST_Y,
                          DECK_Z + P.GRAB_POST_H), 55))
    return (Part.makeCompound(parts), Part.makeCompound(dark),
            Part.makeCompound(glass))


def build_stern_gear():
    """Electric self-recovery winch + stern anchor on its roller."""
    wx, wy, wz = P.WINCH_POS
    parts = [box(420, 260, 230, (wx - 210, wy - 130, wz - 115))]   # housing
    parts.append(Part.makeCylinder(85, 300, Vector(wx, wy - 150, wz),
                                   Vector(0, 1, 0)))               # drum
    parts.append(box(60, 300, 190, (wx - 260, wy - 150, wz - 95)))  # fairlead
    parts.append(Part.makeCylinder(55, 120, Vector(wx - 300, wy - 60, wz),
                                   Vector(0, 1, 0)))               # roller
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


def build_wintergarden():
    """Full curved plexiglass envelope, fuller/rounder profile:
    elliptical side curve with a gentle outward bulge (5 bends per
    side), open top under the roof lid over the cabin, closed crown
    around the raked bow bubble. Ruled loft = bent-panel build."""
    def gunw(x):
        st = P.STATIONS
        for i in range(len(st) - 1):
            if st[i][0] <= x <= st[i + 1][0]:
                t = (x - st[i][0]) / (st[i + 1][0] - st[i][0])
                return (st[i][1] + t * (st[i + 1][1] - st[i][1]),
                        st[i][5] + t * (st[i + 1][5] - st[i][5]))
        return st[-1][1], st[-1][5]

    def section(x, top_z, top_hw):
        gw, sz = gunw(x)
        gw -= P.WG_EDGE_INSET
        a = gw + 95                     # elliptical half-width w/ bulge
        b_ = top_z - sz
        side = []
        for th in (20, 40, 60, 80):
            yy = min(a * math.cos(math.radians(th)), gw + 60)
            zz = sz + b_ * math.sin(math.radians(th))
            side.append((yy, zz))
        pts = [(x, 0, sz - 20), (x, -gw, sz)]
        pts += [(x, -yy, zz) for yy, zz in side]
        pts += [(x, -top_hw, top_z), (x, top_hw, top_z)]
        pts += [(x, yy, zz) for yy, zz in reversed(side)]
        pts += [(x, gw, sz)]
        return wire(pts)

    wires = []
    for x in (P.CABIN_X0, 1800, 2800, 3800, 4800, 5600, 6200):
        wires.append(section(x, 2145, P.WG_TOP_HW))
    for x, apex in ((6550, 1980), (6800, 1760), (7000, 1560),
                    (7130, 1430), (7190, 1360)):
        gw, _ = gunw(x)
        wires.append(section(x, apex, max((gw - P.WG_EDGE_INSET) * 0.12, 50)))
    return Part.makeLoft(wires, True, True)


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

    slab, panels, acts = build_canopy(cfg["lift"])
    add("Canopy", slab, WHITE)
    add("SolarPanels", panels, PANEL)
    for i, ac in enumerate(acts):
        add(f"Actuator{i}", ac, GRAY)

    pod = P.pod_at(cfg["phi"])
    roll = 90 - cfg["phi"]          # rigid arm: roll locked to swing
    (fl, strips, forks, tires, rims, wboxes,
     hatch, hydraulics, thruster) = build_float(pod, roll)
    arms, acts = build_arms(cfg["phi"])
    bplate, bpanels, brail, bhinges = build_balcony(cfg["balc"])
    for side, mir in (("Stb", False), ("Port", True)):
        m = mirror_y if mir else (lambda s: s)
        add(f"Float{side}", m(fl), ORANGE, group=g_gear)
        add(f"FloatSolar{side}", m(strips), PANEL, group=g_gear)
        add(f"WheelForks{side}", m(forks), GRAY, group=g_gear)
        add(f"DriveHatch{side}", m(hatch), WHITE, group=g_gear)
        add(f"Jet{side}", m(thruster), (0.8, 0.65, 0.2), group=g_gear)
        add(f"Hydraulics{side}", m(hydraulics), (0.8, 0.65, 0.2),
            group=g_gear)
        if wboxes:
            add(f"WheelBoxes{side}", m(wboxes), WHITE, group=g_gear)
        add(f"Balcony{side}", m(bplate), WHITE, group=g_gear)
        add(f"BalconyPanels{side}", m(bpanels), PANEL, group=g_gear)
        add(f"BalconyRail{side}", m(brail), STEEL, group=g_gear)
        add(f"BalconyHinges{side}", m(bhinges), GRAY, group=g_gear)
        for i, a in enumerate(arms):
            add(f"Arm{side}{i}", m(a), GRAY, group=g_gear)
        for i, a in enumerate(acts):
            add(f"Actuator{side}{i}", m(a), STEEL, group=g_gear)
        for i, t in enumerate(tires):
            add(f"Tire{side}{i}", m(t), DARK, group=g_gear)
        for i, r in enumerate(rims):
            add(f"Rim{side}{i}", m(r), STEEL, group=g_gear)

    add("Frame", build_frame(), (0.42, 0.44, 0.47))
    add("SternArch", build_tow(cfg["tow"]), (0.42, 0.44, 0.47))
    add("SternGear", build_stern_gear(), (0.55, 0.57, 0.6))
    aft_s, aft_d, aft_g = build_aft_entry(cfg["lift"] > 0,
                                          cfg["balc"] == 0)
    add("AftEntry", aft_s, WHITE)
    add("AftFittings", aft_d, (0.30, 0.32, 0.35))
    add("DoorGlass", aft_g, (0.5, 0.7, 0.8), 70)
    add("MainJet", build_main_jet(), (0.8, 0.65, 0.2))
    add("WinterGarden", build_wintergarden(), (0.75, 0.88, 0.92), 70)

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


P.checks()
modes = [a for a in sys.argv if a in P.MODES] or ["cruise", "road", "foiling"]
for m in modes:
    build_mode(m)

if App.GuiUp:
    import FreeCADGui as Gui
    Gui.activeDocument().activeView().viewIsometric()
    Gui.SendMsgToActiveView("ViewFit")
