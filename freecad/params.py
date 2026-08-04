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
    [6700, 1010,  830, 210, 370, 1240],
    [7000,  770,  580, 350, 470, 1285],
    [7130,  520,  350, 450, 550, 1310],
    [7200,  110,   65, 560, 640, 1330],   # fine rounded stem, no flat face
]

def full_section(st):
    x, yg, yc, zk, zc, zs = st
    return [(KEEL_FLAT, zk), (yc, zc), (yg, zs),
            (-yg, zs), (-yc, zc), (-KEEL_FLAT, zk)]

# ---- cabin (maximized) + pop-top canopy ----
CABIN_X0, CABIN_X1 = 900, 6200
CABIN_W = 2400
CABIN_BASE_Z = 1150
# roof raised 250 over the first design: the 200 mm structural roof was
# eating the interior height. Outside 2400 -> ceiling 2200 -> 1850 clear
# over the sole; road height 3062, still far under the StVZO 4000 limit.
CABIN_ROOF_Z = 2400
ROOF_STRUCT = 200        # sandwich depth of the cabin roof = terrace floor
CABIN_CEIL_Z = CABIN_ROOF_Z - ROOF_STRUCT
# deck build-up over the structural roof: bonded laminate, air box,
# grid and glass. There is no lid and nothing lifts any more.
DECK_BUILDUP = 60 + 55 + 12   # air box (holds the module) + grid + glass
CANOPY_OVERHANG = -20    # kept: the folded balcony clearance references it
WIN_Z0, WIN_H = 1500, 600          # window band (taller with the new roof)
# FEWER, BIGGER windows (Max): two picture windows per side instead of
# six small ones — one over the whole saloon, one over the bed. They
# land where no full-height joinery can ever go, so the interior can be
# rearranged later without touching the glass.
WINDOWS = [(2500, 1800), (4900, 1200)]      # (x0, length)
WIN_PIER = 600                     # solid pillar between the two openings
PORTHOLE = (1500, 1780, 360)       # service zone: light + ventilation

# Real catalogue modules (datasheets checked, not estimated):
#   ROOF  — 500 W mono, Trina Vertex N class: 1961 x 1134 x 30, 27 kg.
#           Its 1961 long side fits the 2100 mm field width lying
#           athwartships, so four cover the roof.
#   SIDES — 400 W BIFACIAL (Max), Photonic Universe / Longi class:
#           1722 x 1134 x 30, 21 kg. 239 mm shorter than the 500 W, and
#           that is exactly what lets THREE fit each balcony instead of
#           two. Bifacial earns its keep here: folded up over the
#           windows in road and harbour trim both faces see daylight,
#           and deployed over the water the back face picks up the
#           surface reflection.
MODULE_500 = (1961, 1134, 30)      # long side, short side, thickness
MODULE_500_W = 500
MODULE_500_KG = 27
MODULE_BIFACIAL = (1722, 1134, 30)
MODULE_BIFACIAL_W = 400
MODULE_BIFACIAL_KG = 21
BIFACIAL_GAIN = 1.05               # rear-face yield, deployed over water

# legacy flexible-laminate footprint, still used for the float strips
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
WHEEL_XS = (-1527, 173, 1873)      # world x 1873/3573/5273, 6 wheels
                                   # (centroid forward of the CG so the
                                   #  STERN coupling gets +100 kg down)
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
BALC_X0, BALC_X1 = 100, 6200   # runs aft to the transom so the
                               # walkway meets the cockpit directly
PASSAGE_W = 540                # aft section is a narrow PASSAGE, not deck:
PASSAGE_X = 900                # it widens to the full balcony only from
                               # the cabin wall forward
BALC_SPAN = 1200
BALC_T = 40                    # ladder-frame depth; modules drop INTO it

# FULL-WIDTH balcony panels (Max, after seeing what a walkway costs):
# the side decks give up walking so that a 1134 mm 500 W module fits
# across the whole 1200 mm span. The aft PASSAGE_W strip stays as the
# route out of the cockpit; forward of the cabin wall the balcony is a
# panel surface you do not stand on.
#
# The folded balcony stands vertically against the cabin on the road,
# so the assembly may be at most 75 mm thick before the 2550 mm road
# limit bites — which is why the modules still drop INTO the ladder
# frame rather than onto it.
MODULE_STD = MODULE_BIFACIAL   # 400 W bifacial: three fit each side
MODULE_W_PEAK_STD = MODULE_BIFACIAL_W
MODULE_KG = MODULE_BIFACIAL_KG
BALC_WALK_W = 0                # no side walkway any more
BALC_PANEL_W = 1160            # the full span carries the module
BALC_TREAD_T = 3               # tread remains on the aft passage only
BALC_MODULE_X0 = 920
BALC_MODULES = 3               # per side: 3 x 1722 + gaps = 5246
BALC_MODULE_GAP = 40
BALC_FRAME_RAIL = (25, 40, 3)  # alu box: b, h, wall
BALC_FRAME_PITCH = 740         # cross rails: module ends + mid support
BALC_FOLDED_T = BALC_T + 8     # frame depth + module lip + tread proud
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
# STRICTLY EXTERNAL — nothing crosses the living volume. Two hard
# constraints make this the only possible layout:
#   * only ~73 mm of width is left outboard of the hull at shoulder
#     height before the 2550 mm road limit
#   * the folded floats fill the whole underside from x 300 to 6500
# so transverse ties are possible ONLY at the ends. The frame is a
# LADDER LOOP IN PLAN:
#   - 2 chassis rails at shoulder height, half-recessed into the
#     topsides (they read as a heavy rubbing wale) — carry the float
#     arm pins
#   - 2 sheer rails on the side-deck strip outside the cabin wall —
#     carry the solar balcony hinges
#   - external straps tying chassis to sheer rail at each arm station
#   - bow tie (tow-arch pivots) and stern tie (waterjet) close the loop
# Torsion is carried by the loop plus the hull shell acting as a shear
# box, which a monocoque hull does well — unlike point loads.
FRAME_TUBE = 100              # chassis rail
FRAME_SHEER_TUBE = 90
FRAME_BEAM = 130              # end ties
FRAME_RAIL_BURY = 25          # chassis rail half-buried in the topside
FRAME_SHEER_INSET = 60        # sheer rail inset from the gunwale line
FRAME_STRAP_X = (1400, 3400, 5400)

# ---- STERN arch: sea gantry <-> extensible drawbar ----
# The boat tows STERN-FIRST, so the arch lives on the transom. One
# A-arch on transverse pivots on the stern tie, pin-locked in two
# positions (same principle as the float arms):
#   SEA  +65 deg: wide gantry standing above the transom — carries the
#                 anchor roller, winch fairlead, nav lights, davits
#   LAND -23.5 deg: swings down-aft, telescoping tongue pins out to
#                 the car coupling
# The bow keeps a FIXED rub bar (the frame's bow tie) — no moving part
# at the pretty end, and the rounded stem stays clean.
BOAT_LCG = 3300               # longitudinal centre of gravity estimate
ARCH_PIVOT_X = -60            # just aft of the transom, on the stern tie
ARCH_PIVOT_Y = 950
ARCH_PIVOT_Z = 760
ARCH_LEG = 1200
ARCH_SEA_DEG = 65
ARCH_LAND_DEG = -23.5
ARCH_EXT = 800                # telescoping tongue stroke
ARCH_TUBE = 130               # heavier section: reads as structure, not wire
COUPLING_H = 430              # target coupling height above ground

# ---- aft entry: sunken cockpit, storm door, porch, stairs ----
# The cabin is only 1000 mm above deck, so the entry is a proper
# COMPANIONWAY: a self-draining footwell (floor 360 mm above the
# waterline, scuppers through the transom), a storm sill, and a
# 1300 mm door header — you step over the sill and duck, then stand
# up in the 1800 mm saloon. Every barge works this way; the geometry
# leaves no alternative (a 1900 mm door would need the cockpit floor
# 20 mm above the keel).
# Side decks are only 50 mm wide, so the cockpit is also the hub for
# reaching the solar balconies: they start at x 900, level with the
# deck, and are entered through boarding gates in the sheer rail.
COCKPIT_X0, COCKPIT_X1 = 150, 900
COCKPIT_HW = 700              # footwell half width
COCKPIT_FLOOR = 400           # deep well: 1700 mm clear at the door, no
                              # ducking; 750 mm bulwark all round as the
                              # fall barrier; still 140 mm above WL so it
                              # gravity-drains through the transom
COCKPIT_WALL = 40
BENCH_Z = 850                 # side benches: seat, and the step up to deck
BENCH_DEPTH = 400
DOOR_HW = 350
DOOR_SLIDE = 760              # leaf slides to PORT into a pocket under
                              # the ladder (i.e. to the right seen from
                              # inside), so it never swings into the well
DOOR_Z0, DOOR_Z1 = 550, 2100  # 150 sill; 1700 mm clear above the floor
PORCH_X0, PORCH_X1 = 120, 820 # cantilevered, flashing seals it to the wall
PORCH_HW = 700                # narrow: covers the well, clears the ladder
PORCH_T = 120                 # thin slab + fascia lip: a deliberate lower roof
PORCH_STRUT_Y = 620           # diagonal tubes to the wall — no deck posts
# alternating-tread ladder, hard against the aft wall to save floor space
STAIR_Y0, STAIR_Y1 = -1200, -740   # port strip, to the LEFT of the door
STAIR_X0, STAIR_X1 = 350, 880      # 530 run for the 1250 rise -> 67 deg
STAIR_STEPS = 8
GATE_X0, GATE_X1 = 200, 800    # sheer-rail gap right beside the
                               # cockpit: step straight out of the
                               # door onto the balcony walkway
# transition from the door out to the balcony walkway: a landing at
# bench height, a half step, and a flush threshold plate at the gate
LANDING_Z = 850
GATE_PLATE_Y = 1180           # threshold plate stays inside the hull
# aft wall fit-out, seen from the cockpit: AC upper right, lockers below
AC_Y0, AC_Y1 = 600, 1140
AC_Z0, AC_Z1 = 1760, 2100
AC_DEPTH = 170                # shallow and faired, not a bolted-on slab
LOCKER_Y0, LOCKER_Y1 = 430, 1140
LOCKER_Z0, LOCKER_Z1 = 950, 1720
LOCKER_DEPTH = 300

# ---- roof terrace: WALK-ON GLASS DECK over a ventilated air box ----
# The pop-top lift is gone (see docs/roof.md for why: the scissor
# breakout force is W/tan(theta), which blows up as the arms go flat,
# and four salt-exposed mechanisms had to carry a 7.7 kN gale uplift).
# Max's replacement has NO MOVING PARTS: flexible laminates bonded flat
# on the roof sandwich, and a framed walk-on glass lid 60 mm above them.
# People walk on the glass; the panels can never be touched, and the
# air box ventilates the cells so they run cooler than bonded ones.
DECK_FIELD_X = (1000, 5800)        # PV field on the terrace, 4800 long
DECK_FIELD_HW = 1050               # +/- : 2100 wide
DECK_PANE = (1200, 1050)           # 8 panes, 4 x 2 — fewest seals
DECK_PANE_NX, DECK_PANE_NY = 4, 2
DECK_GLASS_T = 12                  # 6+6 heat-strengthened laminated, SGP
DECK_GLASS_KG_M2 = 2.5 * DECK_GLASS_T
DECK_GLASS_SIGMA = 35.0            # N/mm2 design stress, heat-strengthened
DECK_LOAD_UDL = 0.002              # N/mm2 = 2 kN/m2, building code
DECK_LOAD_POINT = 2000             # N on a 50x50 patch, building code
DECK_LOAD_PATCH_R = 28             # mm, equivalent radius of the patch
AIRBOX_H = 60                      # ventilated gap, laminate to glass
DECK_FRAME_W = 25                  # grid bar seen in plan -> shading
DECK_FRAME_H = 55
DECK_FRAME_KG_M = 1.4
DECK_VENT_H = 25                   # mesh slots fore and aft of the box
TERRACE_TOERAIL = 80
TERRACE_SCUPPER = 60               # corner drains

# NO guardrail on the roof deck (Max: the stanchions and lifelines
# looked awful). The edge carries the toe rail and nothing else — a sun
# deck to sit on, not a working deck; the fall risk is accepted.

DECK_PANELS = 4                    # what actually fits — see deck_panel_xy()
PANEL_W_PEAK = MODULE_500_W        # W per roof module
GLASS_TRANSMISSION = 0.91          # low-iron laminated
COOLING_GAIN = 1.05                # ventilated cells vs bonded


def glass_t_required(span, P=None, sigma=None):
    """Thickness a walk-on pane needs for the concentrated load — the
    case that governs. Stress spreads locally, so it depends on the LOG
    of the span: halving the pane barely thins the glass."""
    P = DECK_LOAD_POINT if P is None else P
    sigma = DECK_GLASS_SIGMA if sigma is None else sigma
    nu, r0 = 0.23, DECK_LOAD_PATCH_R
    k = (3 * P / (2 * math.pi)) * ((1 + nu) * math.log(2 * span /
                                                       (math.pi * r0)) + 0.5)
    return math.sqrt(k / sigma)


def glass_t_udl(span, q=None, sigma=None):
    """Thickness for the distributed load — quadratic in the span."""
    q = DECK_LOAD_UDL if q is None else q
    sigma = DECK_GLASS_SIGMA if sigma is None else sigma
    return math.sqrt(0.287 * q * span * span / sigma)


def deck_panel_xy():
    """Positions of the roof modules, laid ACROSS the field (short side
    along the boat, long side athwartships). ONE source of truth for
    the geometry and for checks(), so a panel can never again be drawn
    hanging off the end of the boat."""
    mod_l, mod_w, _ = MODULE_500
    fx0, fx1 = DECK_FIELD_X
    pitch = mod_w + 40
    n = min(DECK_PANELS, int((fx1 - fx0 - 40) // pitch))
    run = n * pitch - 40
    x0 = fx0 + (fx1 - fx0 - run) / 2
    return [(x0 + i * pitch, -mod_l / 2) for i in range(n)]


def deck_areas():
    """(field m2, glass m2, frame bar metres, frame shading fraction)."""
    fx = DECK_FIELD_X[1] - DECK_FIELD_X[0]
    fy = 2 * DECK_FIELD_HW
    field = fx * fy / 1e6
    bars = (DECK_PANE_NX + 1) * fy + (DECK_PANE_NY + 1) * fx
    shade = 1 - (1 - DECK_FRAME_W / DECK_PANE[0]) * \
        (1 - DECK_FRAME_W / DECK_PANE[1])
    return field, field, bars / 1000, shade


def deck_mass():
    """kg of the whole walk-on deck: glass, frame, seals and fixings."""
    field, glass, bars, _ = deck_areas()
    return glass * DECK_GLASS_KG_M2 + bars * DECK_FRAME_KG_M + 15


def solar_kwp():
    """(deck kWp, balcony kWp, effective kWp after glass and shading)."""
    deck = DECK_PANELS * PANEL_W_PEAK / 1000
    balc = 2 * BALC_MODULES * MODULE_W_PEAK_STD / 1000
    _, _, _, shade = deck_areas()
    eff = deck * GLASS_TRANSMISSION * (1 - shade) * COOLING_GAIN + \
        balc * BIFACIAL_GAIN
    return deck, balc, eff


# ---- interior ----
# 5300 x 2280 of floor and 1850 of height. Four zones, aft to forward:
#   services (heads to port, galley to starboard, corridor between)
#   dinette  (two settees that are also single berths, table between)
#   wardrobes (flanking the passage)
#   sleeping (double bed ATHWARTSHIPS — a 2000 mm body fits across the
#             2280 mm beam, so the bed eats only 1400 mm of length)
# Everything heavy (batteries, water) lives under the settees and the
# bed: low, amidships, and out of the way.
SOLE_Z = 350
IN_HW = CABIN_W / 2 - 60           # 1140: inside half beam
SEAT_H = 450                       # above the sole
COUNTER_H = 900
OH_Z0, OH_Z1 = 1750, 2200          # overhead lockers, hard to the ceiling
OH_DEPTH = 320

# AC: the indoor air handler stands in the aft-STARBOARD corner, right
# beside the door and directly inboard of the ventilator box already on
# the outside of that wall — the duct crosses the wall on the shortest
# possible run. Below the handler the same column is a full-height
# broom/utility locker.
AC_UNIT_X = (950, 1250)
AC_UNIT_Y = (640, IN_HW)
AC_HANDLER_Z = (1450, 2200)

HEADS_X = (950, 2350)              # wetroom: toilet, shower, basin
HEADS_Y = (-IN_HW, -240)           # 900 deep to port
HEADS_DOOR_X = (1850, 2300)        # sliding, opens into the corridor
GALLEY_X = (1250, 2350)
GALLEY_Y = (540, IN_HW)            # 600 deep to starboard
FRIDGE_X = (1750, 2350)            # full-height fridge + freezer tower
WASHER_W = 460                     # compact washer-dryer under the counter
CORRIDOR_Y = (-240, 540)           # 780 clear between heads and galley
# vertical space: in the SERVICE zone both sides are solid joinery to
# the ceiling and daylight comes from two portholes, so the galley gets
# a 750 mm locker band over the worktop. In the living zones the
# glazing (1500-2100) wins, and storage goes in the band UNDER it.
GAL_OH_Z = (1450, 2200)
GAL_OH_DEPTH = 300
SHELF_Z = (1150, 1480)             # side shelf band under the windows
SHELF_DEPTH = 260

DINETTE_X = (2400, 4400)
SETTEE_D = 620                     # seat depth = berth width
BERTH_X = (2450, 4350)             # 1900 single berth each side
TABLE_L, TABLE_W = 900, 700        # removable, drops to make a double
TABLE_Z = 1050
ELEC_X = (4350, 4700)              # inverter/charger/MPPT, wardrobe base

WARDROBE_X = (4400, 4700)
WARDROBE_W = 700                   # one each side, passage between

# ELEVATING DOUBLE BED at the forward end, right at the big window.
# The 1900 side lies ACROSS the boat (fits the 2280 inside beam); the
# 1400 side runs fore-and-aft. The platform rides on four corner rails
# and is hoisted to the ceiling when it is not being slept in, which
# gives the whole forward zone back as living space by day.
BED_X = (4700, 6200)
MATTRESS_L = 1900                  # across the boat
MATTRESS_W = 1400                  # fore-and-aft
BED_FRAME_T = 70                   # platform thickness
MATTRESS_T = 150
BED_UP_Z = 1980                    # platform underside, stowed at the deckhead
BED_DOWN_Z = 650                   # platform underside, made up for sleeping
BED_RAIL = 45                      # corner guide rail section
BED_CABLE = 6                      # stainless hoist cable
BED_SHAFT = 25                     # common drive shaft = mechanical sync

# ---- 48 V house bank: 50 kWh (Max) ----
# Split symmetrically under BOTH settees: low, amidships, and no list.
# 50 kWh of LiFePO4 is ~360 kg — 18% of the whole mass budget, so it is
# also the single biggest threat to staying road legal (see checks()).
BATT_KWH = 50
BATT_WH_PER_KG = 140               # pack level, incl. cases and busbars
BATT_WH_PER_L = 180                # pack level, incl. spacing and vents
BATT_MASS = BATT_KWH * 1000 / BATT_WH_PER_KG
BATT_VOL_NEED = BATT_KWH * 1000 / BATT_WH_PER_L / 1000      # m3
BATT_BOX_X = (2450, 4350)          # full length of both settee bases
BATT_BOX_H = 400
# water lives in a shallow BILGE tank under the dinette sole: lower than
# any locker, on the centreline, and it frees both settee bases for cells
TANK_BILGE_X = (2500, 4300)
TANK_BILGE_HW = 900
TANK_BILGE_H = 250
WATER_L = 200

# mass budget for the fit-out (kg) — it comes straight off the payload
INT_MASS = dict(joinery=180, batteries=round(BATT_MASS), water=WATER_L,
                appliances=95)

# ---- stern gear: electric winch + anchor ----
# Winch: self-recovery on slippery ramps — pull to a ramp-top anchor
# point and the boat hauls itself out even with no wheel grip.
# Anchor: stern roller on the gantry leg, rode to the same drum family.
WINCH_PULL_KG = 2000          # 4500 lb class, 12/24 V
# BOTH ON THE CENTERLINE (Max): an off-centre winch pulls the boat
# with a yaw bias — on a slipway that fights the wheels and makes the
# recovery harder. Drum athwartships on a stern-tie bracket, rode
# leading aft and down over the anchor roller directly beneath it, so
# the pull line is dead on the keel line.
WINCH_POS = (-70, 0, 1310)
ANCHOR_ROLLER = (-140, 0, 1150)
WINCH_BODY = (300, 420, 230)  # x, y, z: fits between the gantry legs

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
    "anchor":  dict(phi=PHI_WATER, balc=0,  tow="sea",  lift=0),
}


def arch_apex(deg):
    """Stern-arch apex (x, z); the arch extends AFT (-x)."""
    r = math.radians(deg)
    return (ARCH_PIVOT_X - ARCH_LEG * math.cos(r),
            ARCH_PIVOT_Z + ARCH_LEG * math.sin(r))


def arch_coupling():
    """Coupling ball (x, z) with the tongue fully extended, land pose."""
    ax, az = arch_apex(ARCH_LAND_DEG)
    r = math.radians(ARCH_LAND_DEG)
    return (ax - ARCH_EXT * math.cos(r), az + ARCH_EXT * math.sin(r))


def tongue_load_kg():
    """Download on the car's coupling (positive = pressing down)."""
    axle = sum(FLOAT_X + d for d in WHEEL_XS) / len(WHEEL_XS)
    cx, _ = arch_coupling()
    return BOAT_MASS * (BOAT_LCG - axle) / (cx - axle)


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
                         BALC_HINGE_Y + BALC_FOLDED_T,
                         GATE_PLATE_Y)            # gate threshold plate
    road_height = CABIN_ROOF_Z + DECK_BUILDUP - GROUND_Z
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
    assert BALC_HINGE_Z + BALC_SPAN <= CABIN_ROOF_Z + DECK_BUILDUP + 50, \
        "folded balcony sticks above the roof deck"
    assert 100 <= box_gap <= 450, f"balcony leg length odd: {box_gap}"
    # walkable balcony: the folded thickness is what the road limit sees
    ml, mw, mt = MODULE_STD
    balc_free = 1275 - BALC_HINGE_Y
    balc_mass = (2 * (BALC_X1 - PASSAGE_X) / 1000 * 3 * BALC_FRAME_RAIL[0]
                 * BALC_FRAME_RAIL[1] * 2.7e-6 * 1000) + \
        BALC_MODULES * MODULE_KG + \
        (BALC_X1 - PASSAGE_X) * BALC_WALK_W / 1e6 * 8
    assert BALC_FOLDED_T <= balc_free, \
        f"folded balcony {BALC_FOLDED_T} mm thick, only {balc_free:.0f} free"
    assert mt < BALC_T, \
        f"module {mt} mm must recess into the {BALC_T} mm frame, not sit on it"
    assert BALC_WALK_W == 0 or BALC_WALK_W >= 450, \
        f"balcony walkway {BALC_WALK_W} mm is neither absent nor usable"
    assert mw + 20 <= BALC_PANEL_W, \
        f"module {mw} does not fit the {BALC_PANEL_W} panel strip"
    assert BALC_WALK_W + BALC_PANEL_W + BALC_FRAME_RAIL[0] <= BALC_SPAN, \
        "walkway + panel strip wider than the balcony"
    assert BALC_MODULE_X0 >= PASSAGE_X - 50, \
        "balcony modules must start at the wide deck, not in the passage"
    assert BALC_MODULE_X0 + BALC_MODULES * ml + \
        (BALC_MODULES - 1) * BALC_MODULE_GAP <= BALC_X1, \
        f"{BALC_MODULES} modules do not fit the deck length"
    # tow arch: coupling height on the road, protection reach at sea
    cpl_x, cpl_z = arch_coupling()
    cpl_h = cpl_z - GROUND_Z
    sea_x, sea_z = arch_apex(ARCH_SEA_DEG)
    tongue = tongue_load_kg()
    assert 380 <= cpl_h <= 480, f"coupling height {cpl_h:.0f} mm off-spec"
    assert -cpl_x <= 2100, f"drawbar overhang aft {-cpl_x:.0f} too long"
    assert 60 <= tongue <= 130, f"tongue load {tongue:.0f} kg off-spec"
    assert sea_x < -300, "sea gantry not clear aft of the transom"
    # winch + anchor on the keel line: an off-centre pull yaws the boat
    # on a slipway and fights the wheels
    assert abs(WINCH_POS[1]) <= 30, \
        f"winch {WINCH_POS[1]} mm off centreline — biased ramp pull"
    assert abs(ANCHOR_ROLLER[1]) <= 30, \
        f"anchor roller {ANCHOR_ROLLER[1]} mm off centreline"
    assert WINCH_POS[0] > ANCHOR_ROLLER[0], \
        "rode must lead aft from the drum onto the roller"
    assert WINCH_BODY[1] / 2 + 60 <= ARCH_PIVOT_Y, \
        "winch body fouls the gantry legs"
    assert sea_z > WL_Z + 1200, "gantry too low to hang an anchor"
    assert 2 * ARCH_PIVOT_Y + ARCH_TUBE <= 2550, "stern arch wider than road"
    # aft entry
    stair_ang = math.degrees(math.atan2(CABIN_ROOF_Z - CABIN_BASE_Z,
                                        STAIR_X1 - STAIR_X0))
    assert COCKPIT_FLOOR >= WL_Z + 120, \
        f"cockpit floor only {COCKPIT_FLOOR - WL_Z} mm above WL"
    assert DOOR_Z0 - COCKPIT_FLOOR >= 140, "storm sill too low"
    assert DOOR_Z1 - COCKPIT_FLOOR >= 1650, \
        f"only {DOOR_Z1 - COCKPIT_FLOOR} mm clear at the door — you would duck"
    assert CABIN_BASE_Z - COCKPIT_FLOOR >= 600, "bulwark too low to stop a fall"
    assert stair_ang <= 70, f"ladder {stair_ang:.0f} deg too steep"
    assert PORCH_X1 < CABIN_X0, "porch must clear the cabin wall for flashing"
    # jack-up stance equilibrium
    jack_d = FLOAT_W * BOAT_MASS / (2 * reserve_kg)      # submerged depth
    harbor_wl = (POD_ROAD[1] - FLOAT_W / 2) + jack_d     # ~0 = keel awash
    jack_frac = jack_d / FLOAT_W
    L_m, w_m, d_m = FLOAT_LEN / 1000, FLOAT_H / 1000, 0.700
    gm_est = 2 * (L_m * w_m**3 / 12 + L_m * w_m * d_m**2) / (BOAT_MASS / 1000)
    assert jack_frac <= 0.85, f"floats too small to jack up: {jack_frac:.2f}"
    assert -60 <= harbor_wl <= 40, \
        f"jack-up equilibrium off keel-awash regime: {harbor_wl:.0f}"
    # interior: circulation, berths, stowage, and what it costs in draft
    corridor_w = CORRIDOR_Y[1] - CORRIDOR_Y[0]
    berth_l = BERTH_X[1] - BERTH_X[0]
    aisle_w = 2 * IN_HW - 2 * SETTEE_D
    passage_w = 2 * (IN_HW - WARDROBE_W)
    head_clear = CABIN_CEIL_Z - SOLE_Z
    counter_gap = OH_Z0 - (SOLE_Z + COUNTER_H)
    heads_area = (HEADS_X[1] - HEADS_X[0]) * (HEADS_Y[1] - HEADS_Y[0]) / 1e6
    batt_vol = 2 * (BATT_BOX_X[1] - BATT_BOX_X[0]) * (SETTEE_D - 80) * \
        BATT_BOX_H / 1e9
    water_vol = (TANK_BILGE_X[1] - TANK_BILGE_X[0]) * 2 * TANK_BILGE_HW * \
        TANK_BILGE_H / 1e6                                   # litres
    bed_stow_clear = BED_UP_Z - SOLE_Z
    bed_travel = BED_UP_Z - BED_DOWN_Z
    bed_head = CABIN_CEIL_Z - (BED_DOWN_Z + BED_FRAME_T + MATTRESS_T)
    int_mass = sum(INT_MASS.values())
    waterplane = 5.5 * 2.4                                   # m2, near WL
    int_sinkage = int_mass / (waterplane * 1000) * 1000       # mm

    assert corridor_w >= 600, f"corridor only {corridor_w} mm"
    assert berth_l >= 1850, f"settee berth {berth_l} mm too short"
    assert aisle_w >= 900, f"dinette aisle {aisle_w} mm"
    assert passage_w >= 700, f"passage past the wardrobes {passage_w} mm"
    assert head_clear >= 1800, f"cabin headroom {head_clear} mm"
    assert counter_gap >= 450, f"only {counter_gap} mm over the worktop"
    assert heads_area >= 1.2, f"heads {heads_area:.2f} m2 — too tight"
    assert MATTRESS_L <= 2 * IN_HW - 200, \
        f"athwartships bed {MATTRESS_L} does not fit the {2 * IN_HW} beam"
    assert batt_vol >= BATT_VOL_NEED, \
        f"{BATT_KWH} kWh needs {BATT_VOL_NEED:.2f} m3, bays give {batt_vol:.2f}"
    assert water_vol >= WATER_L, \
        f"bilge tank {water_vol:.0f} L < {WATER_L} L"
    assert MATTRESS_L <= 2 * IN_HW - 100, "bed too long for the beam"
    assert bed_travel >= 1200, f"bed lift travel only {bed_travel}"
    assert bed_head >= 900, f"only {bed_head} mm over the mattress in bed"
    assert BED_UP_Z + BED_FRAME_T + MATTRESS_T <= CABIN_CEIL_Z, \
        "stowed bed hits the deckhead"
    assert bed_stow_clear >= 1550, \
        f"only {bed_stow_clear} mm under the stowed bed"
    assert BED_X[1] <= CABIN_X1 and WARDROBE_X[1] <= BED_X[0], \
        "forward zones overlap"
    # the big windows must never be blocked by full-height joinery
    tall = [(AC_UNIT_X, "AC column"), (FRIDGE_X, "fridge tower"),
            (HEADS_X, "heads"), (WARDROBE_X, "wardrobes")]
    for wx, wl in WINDOWS:
        for (tx0, tx1), name in tall:
            assert tx1 <= wx or tx0 >= wx + wl, \
                f"{name} stands in front of the window at x {wx}"
    assert min(wl for _, wl in WINDOWS) >= 1200, "windows got small again"
    assert DINETTE_X[1] <= WARDROBE_X[0] and HEADS_X[1] <= DINETTE_X[0], \
        "interior zones overlap"

    # roof terrace: walk-on glass deck, no moving parts
    interior_clear = CABIN_CEIL_Z - 350                    # sole at 350
    field, glass_area, bar_m, shade = deck_areas()
    pane_x, pane_y = DECK_PANE
    t_point = glass_t_required(max(pane_x, pane_y))
    t_udl = glass_t_udl(max(pane_x, pane_y))
    # deflection of the pane under the distributed load, alpha for a
    # simply supported square plate; limit span/300
    defl = 0.0443 * DECK_LOAD_UDL * pane_y ** 4 / (70000 * DECK_GLASS_T ** 3)
    deck_kg = deck_mass() + DECK_PANELS * MODULE_500_KG
    air_draft = CABIN_ROOF_Z + DECK_BUILDUP - WL_Z
    kwp_deck, kwp_balc, kwp_eff = solar_kwp()
    # four people hard to one side of the terrace vs the float righting
    m_heel_crew = 4 * 85 * 9.81 * (CABIN_W / 2 - 100) / 1e6      # kNm

    mod_l, mod_w, mod_t = MODULE_500
    lam = deck_panel_xy()
    assert len(lam) == DECK_PANELS, \
        f"only {len(lam)} of {DECK_PANELS} roof laminates fit the field"
    for (lx, ly) in lam:
        assert DECK_FIELD_X[0] <= lx and lx + mod_w <= DECK_FIELD_X[1], \
            f"roof module at x {lx:.0f} runs off the field"
        assert ly >= -DECK_FIELD_HW and ly + mod_l <= DECK_FIELD_HW, \
            f"roof module spans y {ly:.0f}..{ly + mod_l:.0f} of " \
            f"+/-{DECK_FIELD_HW}"
    assert DECK_PANE_NX * pane_x <= DECK_FIELD_X[1] - DECK_FIELD_X[0], \
        "glass panes do not fit the field lengthwise"
    assert DECK_PANE_NY * pane_y <= 2 * DECK_FIELD_HW, \
        "glass panes do not fit the field across"
    assert DECK_FIELD_HW + 150 <= CABIN_W / 2, \
        "no walking margin outboard of the glass"
    assert DECK_GLASS_T >= t_point, \
        f"glass {DECK_GLASS_T} mm under the {DECK_LOAD_POINT} N point load " \
        f"({t_point:.1f} needed)"
    assert defl <= pane_y / 300, \
        f"pane deflects {defl:.1f} mm, limit {pane_y / 300:.1f}"
    assert AIRBOX_H >= mod_t + 20, \
        f"air box {AIRBOX_H} too shallow for a {mod_t} mm framed module"
    assert DECK_BUILDUP == AIRBOX_H + DECK_FRAME_H + DECK_GLASS_T, \
        "deck build-up does not add up"
    assert "RAIL_H" not in globals(), "a guardrail crept back onto the deck"
    assert interior_clear >= 1800, f"interior clear only {interior_clear}"
    assert m_heel_crew <= 0.3 * m_right, \
        f"crew on one side heels {m_heel_crew:.1f} vs righting {m_right:.1f}"
    assert shade <= 0.08, f"frame shades {shade * 100:.0f}% of the field"
    # the roof must stay a fixed structure — nothing to seize in a gale
    assert not any(k in globals() for k in
                   ("SCISSOR_ARM", "CANOPY_LIFT", "ACT_FORCE_N")), \
        "a lifting roof crept back in"
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
        print(f"balcony deck    walkway {BALC_WALK_W} + panels "
              f"{BALC_PANEL_W} = {BALC_SPAN}; {BALC_MODULES} std modules "
              f"{ml}x{mw} per side; folded {BALC_FOLDED_T} mm of "
              f"{balc_free:.0f} free;  ~{balc_mass:.0f} kg/side")
        print(f"waterjets       3 x {JET_POWER_W} W, grid top "
              f"{WL_Z - grid_top:.0f} mm under WL, face v {face_v:.2f} m/s")
        print(f"stern arch      gantry {-sea_x:.0f} mm aft of transom, "
              f"{sea_z - WL_Z:.0f} above WL")
        print(f"stern tow       coupling {cpl_h:.0f} mm high, overhang aft "
              f"{-cpl_x:.0f} mm, tongue load {tongue:+.0f} kg")
        print(f"aft entry       {DOOR_Z1 - COCKPIT_FLOOR} mm clear at the door, "
              f"bulwark {CABIN_BASE_Z - COCKPIT_FLOOR}, "
              f"floor {COCKPIT_FLOOR - WL_Z} above WL, ladder {stair_ang:.0f} deg")
        print(f"interior        corridor {corridor_w:.0f}, aisle "
              f"{aisle_w:.0f}, passage {passage_w:.0f}, heads "
              f"{heads_area:.2f} m2, berths 2 x {berth_l:.0f} + "
              f"{MATTRESS_L}x{MATTRESS_W} double")
        print(f"bed lift        {MATTRESS_L}x{MATTRESS_W} athwartships, "
              f"travel {bed_travel} mm, {bed_stow_clear} clear under it "
              f"stowed, {bed_head} over the mattress made up")
        print(f"house bank      {BATT_KWH} kWh, {BATT_MASS:.0f} kg, "
              f"{BATT_VOL_NEED:.2f} m3 in {batt_vol:.2f} m3 of settee base; "
              f"water {water_vol:.0f} L bilge tank")
        print(f"interior mass   {int_mass} kg "
              f"({', '.join(f'{k} {v}' for k, v in INT_MASS.items())})"
              f" -> +{int_sinkage:.0f} mm draft")
        print(f"cabin inside    {interior_clear:.0f} mm clear "
              f"({CABIN_ROOF_Z} outside, {ROOF_STRUCT} roof structure)")
        print(f"roof deck       {field:.1f} m2 field, {DECK_PANE_NX}x"
              f"{DECK_PANE_NY} panes {pane_x}x{pane_y}, glass "
              f"{DECK_GLASS_T} mm (point load needs {t_point:.1f}, "
              f"UDL {t_udl:.1f}), deflection {defl:.1f} mm")
        print(f"deck build-up   {DECK_BUILDUP} mm = air box {AIRBOX_H} "
              f"(holds a {mod_t} mm module) + grid {DECK_FRAME_H} + glass "
              f"{DECK_GLASS_T};  mass {deck_kg:.0f} kg incl. modules, "
              f"shading {shade * 100:.1f}%")
        print(f"roof modules    {DECK_PANELS} x standard {mod_l}x{mod_w} "
              f"{MODULE_500_W} W framed, laid across, "
              f"{DECK_PANELS * MODULE_500_KG} kg")
        print(f"deck edge       toe rail {TERRACE_TOERAIL} mm, no guardrail")
        print(f"deck loads      {DECK_LOAD_UDL * 1000:.1f} kN/m2 + "
              f"{DECK_LOAD_POINT / 1000:.1f} kN point; crew one side "
              f"{m_heel_crew:.1f} vs righting {m_right:.1f} kNm")
        print(f"solar           deck {kwp_deck:.2f} + balcony {kwp_balc:.2f} "
              f"= {kwp_deck + kwp_balc:.2f} kWp nominal, {kwp_eff:.2f} "
              f"effective;  air draft {air_draft:.0f} mm")
        print(f"jack-up stance  floats {jack_frac * 100:.0f}% deep, "
              f"keel {-harbor_wl:.0f} mm above water (awash), "
              f"pontoon GM ~{gm_est:.1f} m")
    return True
