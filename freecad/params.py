# params.py — master dimensions (mm), Dutch-barge hull at max road width.
# Frame: x=0 transom (+x forward), y=0 centerline, z=0 keel baseline.
import math

# ---- hull: Dutch barge, widened to the German road limit ----
LOA = 7200
HULL_BEAM = 2500         # road limit 2550; hangar tucks fully underneath
WL_Z = 260               # wide hull floats shallow (~2000 kg here)
KEEL_FLAT = 40

# [x, y_gunwale, y_chine, z_keel, z_chine, z_sheer]
STATIONS = [
    [0,    1136, 1023,  60, 240, 1150],
    [600,  1227, 1125,  10, 230, 1150],
    [1800, 1250, 1136,   0, 230, 1150],
    [3000, 1250, 1136,   0, 230, 1150],
    [4200, 1250, 1136,   0, 230, 1150],
    [5400, 1227, 1102,  20, 240, 1160],
    [6300, 1125,  977, 120, 300, 1200],
    [6900,  886,  704, 300, 420, 1260],
    [7200,  398,  250, 520, 600, 1320],
]

def full_section(st):
    x, yg, yc, zk, zc, zs = st
    return [(KEEL_FLAT, zk), (yc, zc), (yg, zs),
            (-yg, zs), (-yc, zc), (-KEEL_FLAT, zk)]

# ---- cabin (maximized) + pop-top canopy ----
CABIN_X0, CABIN_X1 = 900, 6200
CABIN_W = 2400
CABIN_BASE_Z = 1150
CABIN_ROOF_Z = 2150
CANOPY_THICK = 180
CANOPY_LIFT = 1500
CANOPY_OVERHANG = -20    # canopy 2360: fits 2 rows of panels, clears shutters

# ONE panel footprint everywhere: FLEXIBLE laminates (~430 W, ~6 kg,
# bifacial on the balconies)
PANEL_L = 1700
PANEL_W = 1130
PANEL_T = 4

# ---- movable stabilizers = the hangar, fully under the hull on road ----
# ONE FULLY RIGID welded arm per station (Max: no rotating parts in the
# middle or at the float — straight segments cut at angles, welded with
# gussets; the float attachment is static). The ONLY pivot is the
# shoulder pin at the top, on the upper hull side. Because the float is
# rigid on the arm, float roll is locked 1:1 to arm swing — so the
# swing is EXACTLY 90 degrees:
#   road (phi 0):    float on its SIDE flush under the hull, wheels
#                    vertical and rolling (also the launch/harbor pose)
#   water (phi 90):  float swung out and flat on the water, wheels
#                    lying flat on the deck, dry
# Launching happens IN the road configuration: drive in until the boat
# floats off the wheels, then swing the arms out in deeper water.
ARM_X = (1400, 5400)
SH_Y, SH_Z = 1210, 760             # shoulder pin, upper hull side
# arm polyline in ROAD pose, shoulder first, wrist (= float center) last
ARM_POLY_ROAD = [(1210, 760), (1170, 420), (1150, 150), (700, -88)]
ARM_T = 100                        # segment tube section

POD_ROAD = ARM_POLY_ROAD[-1]       # (700, -88): beveled float face sits FLUSH
BOTTOM_SLOPE = 230 / 1096          # hull deadrise: z = (y-40)*slope
_V0 = (POD_ROAD[0] - SH_Y, POD_ROAD[1] - SH_Z)
ARM_R = math.hypot(*_V0)           # rigid chord shoulder->wrist ~1572


def pod_at(phi_deg):
    """Wrist/float center after swinging the rigid arm by phi (deg,
    positive outboard) from the road pose."""
    c, s = math.cos(math.radians(phi_deg)), math.sin(math.radians(phi_deg))
    vy, vz = _V0
    return (SH_Y + vy * c - vz * s, SH_Z + vy * s + vz * c)


PHI_WATER = 90.0                   # exact, by rigid-arm construction
POD_WATER = pod_at(PHI_WATER)      # (2058, 250)

FLOAT_LEN = 6200
FLOAT_W = 600                      # vertical extent when on its side
FLOAT_H = 900                      # deep ama; sized so the bevel keeps 80% reserve
FLOAT_X = sum(ARM_X) / 2

# ---- caster wheels (electric hub motors, sealed) ----
# 205/70 R15 ALL-TERRAIN (General Grabber AT3 class): sand/mud traction
# plus normal road use; still a standard 15-inch size, any tire shop
WHEEL_DIA = 668
WHEEL_W = 205
HUB_DIA = 390
WHEEL_XS = (-2100, -400, 1300)     # world x 1300/3000/4700, 6 wheels
AXLE_STANDOFF = -15                # disc recessed; rim stays inside 2550
WHEEL_DROP = 60                    # axle dropped so wheels, not floats, touch ground

GROUND_Z = POD_ROAD[1] - WHEEL_DROP - WHEEL_DIA / 2   # -448

# ---- jack-up stance (folded arms afloat) ----
# Floats hold ~3.1 t of max buoyancy vs a 2.0 t boat: folding the arms
# in deep water lifts the HULL until the floats alone carry the boat.
# Equilibrium: floats ~65% submerged; the hull keel ends up AT the
# water surface (unloaded, awash) — float top is welded flush to the
# hull bottom, so true dry clearance is ~zero by construction.
BOAT_MASS = 2000
_wedge = 0.5 * (BOTTOM_SLOPE * FLOAT_H) * FLOAT_H * FLOAT_LEN
_reserve = (FLOAT_LEN * FLOAT_W * FLOAT_H * 0.62 - _wedge) * 1e-6
JACK_DEPTH = FLOAT_W * BOAT_MASS / (2 * _reserve)        # ~387 mm
HARBOR_WL_Z = (POD_ROAD[1] - FLOAT_W / 2) + JACK_DEPTH   # ~-1: keel awash

# in-float electric-hydraulic drive bay (see docs/wheels.md):
# 48V motor + pump + valve manifold in a watertight compartment;
# hydraulic orbital motors in the wheel hubs, hoses internal to the
# float — nothing hydraulic ever crosses the arm articulation
MOTOR_BAY_DX = 650       # bay center, float-local x
MOTOR_BAY_L = 800
MOTOR_BAY_W = 400

# ---- solar balcony: bifacial shutters / walkable water deck ----
BALC_X0, BALC_X1 = 900, 6200
BALC_SPAN = 1200
BALC_T = 40
BALC_HINGE_Y = 1200                # folded outer face 1256 <= 1275
BALC_HINGE_Z = 1150

# low-profile boxes over the flat-lying wheels (water pose only);
# balcony stays horizontal and stands on legs down to the box lids
WHEELBOX_L = 780
WHEELBOX_W = 780
WHEELBOX_H = 120   # low lids over the recessed flat wheels
WHEELBOX_Y0, WHEELBOX_Y1 = -350, 250   # OPEN outboard: tire edge exposed
                                       # as a rolling harbor fender
WHEELBOX_TOP_Z = POD_WATER[1] + FLOAT_H / 2 + WHEELBOX_H

# ---- propulsion: 3x flush-intake WATERJETS (docs/propulsion.md) ----
# Max's architecture: large flush perforated grids on BOTH SIDES of
# each float (low face velocity ~0.5 m/s -> weed drifts past, 14 mm
# holes pass no strands) -> internal plenum -> D200 duct -> enclosed
# 2 kW rim-driven inline pump -> jet nozzle out the tail. Same
# cartridge in the main hull with grids on the aft hull sides and the
# nozzle through the transom. Nothing rotating is reachable by weed.
JET_GRID_L = 1300        # grid panel, along float axis (midbody)
JET_GRID_H = 240   # fits the SIDE face between chine and WL
JET_GRID_X_LOCAL = -300  # panel center: parallel midbody, flat side
JET_Z_LOCAL = -170       # grid centerline: fully below WL, above the chine
JET_DUCT_D = 200
JET_NOZZLE_D = 140
JET_HOLE_D = 14
JET_POWER_W = 2000
MAIN_GRID_L = 850        # main intakes: VERTICAL panels on the transom
MAIN_GRID_H = 180
MAIN_GRID_Y = 420        # +- from centerline, flanking the nozzle
MAIN_GRID_Z = 130
MAIN_NOZZLE = (0, 0, 150)  # exits through the transom



def keel_z_at(x):
    for i in range(len(STATIONS) - 1):
        x0, x1 = STATIONS[i][0], STATIONS[i + 1][0]
        if x0 <= x <= x1:
            t = (x - x0) / (x1 - x0)
            return STATIONS[i][3] + t * (STATIONS[i + 1][3] - STATIONS[i][3])
    return STATIONS[-1][3]

# ---- winter garden: full curved plexiglass envelope ----
# One molded piece covering the WHOLE habitation area: bottom edge at
# the sheer line (where the hull starts), rising over the cabin sides
# to just under the roof-lid edge, wrapping the raked bow bubble down
# to the foredeck. The solar roof lid caps the top opening, so the
# pop-top still lifts through it.
WG_APEX_CABIN = 2210     # glass crown over the cabin (roof lid above)
WG_TOP_HW = 1195         # glass meets the roof-lid edge here
WG_EDGE_INSET = 30       # bottom edge inset from the gunwale line

# ---- exoskeleton: external steel space frame ----
# Everything mounts on the frame, not the hull skin: float-arm shoulder
# pins, balcony hinges, tow arch, fenders. The hull then only carries
# hydrostatic pressure and its own distributed loads.
#   - 2 sheer rails (chassis rails) running the full length at the
#     gunwale, tube 110
#   - transverse CROSS-BEAMS at the arm stations at exactly SH_Z, so
#     each float's load passes rail-to-rail through one beam instead of
#     into the hull side
#   - posts tying cross-beam ends up to the rails
#   - bow ring (carries the tow arch pivots) + stern ring (jet, platform)
FRAME_TUBE = 110
FRAME_BEAM = 130
FRAME_RAIL_INSET = 40         # rails sit just inside the gunwale line
FRAME_BEAM_X = (1400, 3400, 5400)

# ---- tow arch: bow protection bar <-> extensible drawbar ----
# One A-arch on transverse pivots at the bow ring, pin-locked in two
# positions (same principle as the float arms):
#   SEA  +55 deg: arch stands up and forward of the stem — takes the
#                 hit in a collision, doubles as pulpit/anchor gantry
#   LAND -25 deg: arch swings down-forward, telescoping tongue extends
#                 and pins out to the car coupling
ARCH_PIVOT_X = 7150   # at the stem: clear of the hull and the glass
ARCH_PIVOT_Y = 420    # ~85 mm proud of the hull surface there
ARCH_PIVOT_Z = 860
ARCH_LEG = 950
ARCH_SEA_DEG = 55
ARCH_LAND_DEG = -27
ARCH_EXT = 1000               # telescoping tongue stroke
ARCH_TUBE = 95
COUPLING_H = 430              # target coupling height above ground

# ---- stern pod ----
STERNPOD_DIA = 300
STERNPOD_LEN = 700

# phi: arm swing (0 = road, PHI_WATER = floats on the water)
# roll: float roll (90 = on its side / wheels vertical, 0 = flat)
# balc: 90 folded up over the windows, 0 horizontal over the water
# roll is NOT independent: rigid arm -> roll = 90 - phi
MODES = {
    "road":    dict(phi=0,         balc=90, tow="land", lift=0),
    "launch":  dict(phi=0,         balc=90, tow="land", lift=0),
    "harbor":  dict(phi=0,         balc=90, tow="sea",  lift=0),
    "cruise":  dict(phi=PHI_WATER, balc=0,  tow="sea",  lift=0),
    "anchor":  dict(phi=PHI_WATER, balc=0,  tow="sea",  lift=CANOPY_LIFT),
}


def arch_apex(deg):
    """Tow-arch apex (x, z) at a given leg angle from horizontal."""
    r = math.radians(deg)
    return (ARCH_PIVOT_X + ARCH_LEG * math.cos(r),
            ARCH_PIVOT_Z + ARCH_LEG * math.sin(r))


def arch_coupling():
    """Coupling ball (x, z) with the tongue fully extended, land pose."""
    ax, az = arch_apex(ARCH_LAND_DEG)
    r = math.radians(ARCH_LAND_DEG)
    return (ax + ARCH_EXT * math.cos(r), az + ARCH_EXT * math.sin(r))


def naca_pts(chord, t=0.12, n=20):
    top = []
    for i in range(n + 1):
        u = i / n
        yt = 5 * t * chord * (0.2969 * math.sqrt(u) - 0.1260 * u
                              - 0.3516 * u**2 + 0.2843 * u**3 - 0.1015 * u**4)
        top.append((u * chord, yt))
    bot = [(x, -y) for x, y in reversed(top[1:-1])]
    return top + bot


# ---------------------------------------------------------------
# Checks
# ---------------------------------------------------------------
def _sub_area(st, wl):
    pts = full_section(st)
    clipped = []
    n = len(pts)
    for i in range(n):
        a, b = pts[i], pts[(i + 1) % n]
        if a[1] <= wl:
            clipped.append(a)
        if (a[1] <= wl) != (b[1] <= wl):
            t = (wl - a[1]) / (b[1] - a[1])
            clipped.append((a[0] + (b[0] - a[0]) * t, wl))
    if len(clipped) < 3:
        return 0.0
    s = 0.0
    for i in range(len(clipped)):
        a, b = clipped[i], clipped[(i + 1) % len(clipped)]
        s += a[0] * b[1] - a[1] * b[0]
    return abs(s) / 2


def displacement_kg(wl=WL_Z):
    vol = 0.0
    for i in range(len(STATIONS) - 1):
        a0 = _sub_area(STATIONS[i], wl)
        a1 = _sub_area(STATIONS[i + 1], wl)
        vol += (a0 + a1) / 2 * (STATIONS[i + 1][0] - STATIONS[i][0])
    return vol * 1e-6


def checks(verbose=True):
    # road: everything inside the hull footprint, shallow stack
    wheel_disc_y = POD_ROAD[0] + FLOAT_H / 2 + AXLE_STANDOFF   # 1170
    wheel_outer = wheel_disc_y + (WHEEL_W + 60) / 2
    float_outer_road = POD_ROAD[0] + FLOAT_H / 2               # sideways
    road_width = 2 * max(HULL_BEAM / 2, wheel_outer, float_outer_road,
                         BALC_HINGE_Y + BALC_T + 2 * PANEL_T + 12)
    road_height = CABIN_ROOF_Z + CANOPY_THICK - GROUND_Z
    track = 2 * wheel_disc_y
    # water: floats flat, wheels flat on deck
    water_beam = 2 * (POD_WATER[0] + FLOAT_W / 2)
    float_bot = POD_WATER[1] - FLOAT_H / 2
    immersion = (WL_Z - float_bot) / FLOAT_H
    wheel_low_water = POD_WATER[1] + FLOAT_H / 2 + 30          # flat discs
    disp = displacement_kg()
    # reserve minus the bevel wedge shaved to sit flush on the hull bottom
    wedge = 0.5 * (BOTTOM_SLOPE * FLOAT_H) * FLOAT_H * FLOAT_LEN
    reserve_kg = (FLOAT_LEN * FLOAT_W * FLOAT_H * 0.62 - wedge) * 1e-6
    m_right = reserve_kg * 9.81 * POD_WATER[0] / 1e6
    m_heel = 0.5 * 1.2 * 1.1 * 11.5 * 25.7**2 * 1.5 / 1000
    box_gap = BALC_HINGE_Z - BALC_T - WHEELBOX_TOP_Z           # leg length

    assert road_width <= 2550, f"road width {road_width}"
    assert road_height <= 4000, f"road height {road_height}"
    assert -GROUND_Z >= 250, f"ground clearance {-GROUND_Z}"
    assert wheel_outer <= HULL_BEAM / 2 + 20, \
        f"wheels outside the hull footprint: {wheel_outer}"
    assert wheel_low_water >= WL_Z + 25, f"wheels wet: {wheel_low_water}"
    assert 0.30 < immersion < 0.70, f"float immersion {immersion}"
    assert 4500 <= water_beam <= 5700, f"water beam {water_beam}"
    assert 1700 < disp < 2400, f"displacement {disp}"
    assert reserve_kg >= 0.80 * 1900, f"ama reserve {reserve_kg:.0f}"
    assert m_right / m_heel >= 3, f"righting SF {m_right / m_heel:.1f}"
    assert BALC_HINGE_Y >= CABIN_W / 2 + CANOPY_OVERHANG + 15, \
        "folded balcony hits the canopy"
    assert BALC_HINGE_Z + BALC_SPAN <= CABIN_ROOF_Z + CANOPY_THICK + 50, \
        "folded balcony sticks above the canopy"
    assert 100 <= box_gap <= 450, f"balcony leg length odd: {box_gap}"
    # tow arch: coupling height on the road, protection reach at sea
    cpl_x, cpl_z = arch_coupling()
    cpl_h = cpl_z - GROUND_Z
    sea_x, sea_z = arch_apex(ARCH_SEA_DEG)
    assert 380 <= cpl_h <= 480, f"coupling height {cpl_h:.0f} mm off-spec"
    assert cpl_x - LOA <= 2000, f"drawbar overhang {cpl_x - LOA:.0f} too long"
    assert sea_x > LOA + 250, "protection arch not proud of the stem"
    assert 2 * ARCH_PIVOT_Y + ARCH_TUBE <= 2550, "tow arch wider than road"
    # jack-up stance equilibrium
    jack_d = FLOAT_W * BOAT_MASS / (2 * reserve_kg)      # submerged depth
    harbor_wl = (POD_ROAD[1] - FLOAT_W / 2) + jack_d     # ~0 = keel awash
    jack_frac = jack_d / FLOAT_W
    L_m, w_m, d_m = FLOAT_LEN / 1000, FLOAT_H / 1000, 0.700
    gm_est = 2 * (L_m * w_m**3 / 12 + L_m * w_m * d_m**2) / (BOAT_MASS / 1000)
    assert jack_frac <= 0.85, f"floats too small to jack up: {jack_frac:.2f}"
    assert -60 <= harbor_wl <= 40, \
        f"jack-up equilibrium off keel-awash regime: {harbor_wl:.0f}"
    grid_top = POD_WATER[1] + JET_Z_LOCAL + JET_GRID_H / 2
    assert grid_top <= WL_Z - 40, \
        f"intake grids not submerged enough: top {grid_top}"
    face_v = 0.13 / (2 * JET_GRID_L * JET_GRID_H * 0.40 * 1e-6)
    grid_bot_local = JET_Z_LOCAL - JET_GRID_H / 2
    assert grid_bot_local >= -292, \
        f"float grid crosses the chine onto the bottom: {grid_bot_local}"
    if verbose:
        print(f"road width      {road_width:.0f} mm (limit 2550)")
        print(f"road height     {road_height:.0f} mm (limit 4000)")
        print(f"ground clear    {-GROUND_Z:.0f} mm  (stack under keel)")
        print(f"track           {track:.0f} mm")
        print(f"arm swing       {PHI_WATER:.1f} deg, chord {ARM_R:.0f} mm")
        print(f"water beam      {water_beam:.0f} mm")
        print(f"wheel dry marg  {wheel_low_water - WL_Z:.0f} mm above WL")
        print(f"float immersion {immersion * 100:.0f} %")
        print(f"displacement    {disp:.0f} kg @ WL {WL_Z}")
        print(f"ama reserve     {reserve_kg:.0f} kg/side "
              f"({100 * reserve_kg / 1900:.0f}%)")
        print(f"righting SF     {m_right / m_heel:.1f}")
        print(f"balcony legs    {box_gap:.0f} mm down to the wheel boxes")
        print(f"waterjets       3 x {JET_POWER_W} W, grid top "
              f"{WL_Z - grid_top:.0f} mm under WL, face v {face_v:.2f} m/s")
        print(f"tow arch       sea apex {sea_x - LOA:.0f} mm proud of stem, "
              f"land coupling {cpl_h:.0f} mm high, overhang {cpl_x - LOA:.0f}")
        print(f"jack-up stance  floats {jack_frac * 100:.0f}% deep, "
              f"keel {-harbor_wl:.0f} mm above water (awash), "
              f"pontoon GM ~{gm_est:.1f} m")
    return True
