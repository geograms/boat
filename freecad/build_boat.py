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
    shell = loft_sections(hull_sections()).cut(
        loft_sections(hull_sections(inner=True)))
    shell = shell.cut(plan_prism(       # cabin-footprint deck opening
        [(P.CABIN_X0 + 50, -P.CABIN_W / 2 + 70),
         (P.CABIN_X1 - 50, -P.CABIN_W / 2 + 70),
         (P.CABIN_X1 - 50, P.CABIN_W / 2 - 70),
         (P.CABIN_X0 + 50, P.CABIN_W / 2 - 70)],
        DECK_Z - 60, DECK_Z + 60))
    return shell


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
    cuts.append(box(200, 650, 900, (P.CABIN_X0 - 100, -325, P.CABIN_BASE_Z)))
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
def build_drawbar(deployed):
    tip = ((P.LOA + P.DRAWBAR_LEN, 0, P.GROUND_Z + P.COUPLING_H)
           if deployed else (7050, 0, 1900))
    parts = [rod((6500, s * 430, 900), tip, 90) for s in (-1, 1)]
    parts.append(Part.makeSphere(80, Vector(*tip)))
    return Part.makeCompound(parts)


def build_wintergarden():
    """Full curved plexiglass envelope: sheer line -> cabin sides ->
    raked bow bubble. Lofted from consistently-ordered sections (the
    plexiglass is bent in multiple planes, panel by panel)."""
    def gunw(x):
        st = P.STATIONS
        for i in range(len(st) - 1):
            if st[i][0] <= x <= st[i + 1][0]:
                t = (x - st[i][0]) / (st[i + 1][0] - st[i][0])
                return (st[i][1] + t * (st[i + 1][1] - st[i][1]),
                        st[i][5] + t * (st[i + 1][5] - st[i][5]))
        return st[-1][1], st[-1][5]

    def section(x, apex, thw):
        gw, sz = gunw(x)
        gw -= P.WG_EDGE_INSET
        shoulder = sz + (apex - sz) * 0.86
        mid = (sz + apex) / 2
        return wire([(x, 0, sz - 20), (x, -gw, sz), (x, -gw - 14, mid),
                     (x, -thw, shoulder), (x, 0, apex),
                     (x, thw, shoulder), (x, gw + 14, mid), (x, gw, sz)])

    wires = []
    for x in (P.CABIN_X0, 2000, 3200, 4400, 5400, 6200):
        wires.append(section(x, P.WG_APEX_CABIN, P.WG_TOP_HW))
    for x, apex, f in ((6550, 1950, 0.80), (6850, 1700, 0.66),
                       (7060, 1480, 0.5), (7180, 1360, 0.38)):
        gw, _ = gunw(x)
        wires.append(section(x, apex, max((gw - P.WG_EDGE_INSET) * f, 110)))
    return Part.makeLoft(wires, True, True)   # ruled: bent-panel look


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

    add("Drawbar", build_drawbar(cfg["drawbar"]), GRAY)
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
