// params.scad — all master dimensions, mode tables, derived values, checks.
// Units: mm, full scale.
// Frame: x=0 at transom (+x forward), y=0 centerline, z=0 keel baseline.
// Design waterline at z = wl_z.

/* [Mode] */
mode = "cruise";     // [road, launch, harbor, cruise, foiling]
anim = false;        // true: arms/pods driven by $t (View > Animate)
target = "view";     // [view, print]  print: 1:20, no reference planes
canopy_up = false;   // pop-top raised (anchor only)

/* [Hull] */
loa = 7200;
hull_beam = 2200;    // max beam at gunwale
wl_z = 340;          // design waterline above keel (tuned for ~1900 kg)
keel_flat = 40;      // half-width of keel flat
water_rho = 1e-6;    // kg per mm^3, fresh water

// Stations: [x, y_gunwale, y_chine, z_keel, z_chine, z_sheer]
STATIONS = [
  [   0,  950, 820,  80, 260, 1150],
  [ 900, 1050, 920,  20, 250, 1150],
  [1800, 1100, 950,   0, 250, 1150],
  [2700, 1100, 950,   0, 250, 1150],
  [3600, 1100, 940,   0, 255, 1160],
  [4500, 1080, 880,  30, 280, 1190],
  [5400,  980, 720, 120, 360, 1250],
  [6300,  700, 420, 320, 560, 1330],
  [7200,   60,  30, 700, 900, 1420],
];

// Full chined section polygon in (y,z), counterclockwise
function full_section(st) =
  let (yg = st[1], yc = st[2], zk = st[3], zc = st[4], zs = st[5])
  [[keel_flat, zk], [yc, zc], [yg, zs],
   [-yg, zs], [-yc, zc], [-keel_flat, zk]];

/* [Cabin + pop-top canopy] */
cabin_x0 = 1600;
cabin_x1 = 5400;
cabin_w = 2000;
cabin_base_z = 1150;   // sits on deck at sheer
cabin_roof_z = 2150;   // roof deck = terrace floor; 1.8 m headroom inside
canopy_thick = 180;    // panel + frame + solar, stowed
canopy_lift = 1500;    // actuator stroke
canopy_overhang = 80;

/* [Hangar arms + pods] */
arm_hinge_y = 1050;    // longitudinal hinge on gunwale
arm_hinge_z = 1150;
arm_len = 1450;        // hinge to pod pivot
arm_x_front = 4700;
arm_x_rear = 1500;
arm_w = 140;           // arm box section
arm_t = 90;
arm_road_deg = -5;     // from straight down, +outboard
arm_launch_deg = 35;
arm_harbor_deg = 45;
arm_water_deg = 72;
pod_up_off = 360;      // ama center above wheel axle, pod frame (road pose)
pod_water_deg = 157;   // pod world rotation road -> water

/* [Wheels — electric hub motors] */
wheel_dia = 600;
wheel_w = 180;
hub_dia = 250;

/* [Amas] */
ama_len = 3200;
ama_w = 400;
ama_h = 440;
ama_x = (arm_x_front + arm_x_rear) / 2;   // spans both arm tips

/* [Bow hydrofoil] */
foil_x = 6500;         // forward of the V-berth, trunk clear of interior
foil_span = 1800;
foil_chord = 300;
foil_strut_chord = 220;
foil_deploy_z = -900;  // wing below keel, deployed
foil_stow_z = 420;     // wing tucked inside the keel trunk, stowed
                       // (local keel at foil_x is z~404; wing hides in hull)

/* [Drawbar + stern pod] */
drawbar_len = 1600;
coupling_h = 430;      // coupling above ground
sternpod_dia = 300;
sternpod_len = 700;

/* [Mass budget, kg — [name, mass, x_cg]] */
MASSES = [
  ["hull",          550, 3400],
  ["cabin",         330, 3500],
  ["canopy+solar",  170, 3500],
  ["arms+hinges",   160, 3100],
  ["amas",          110, 3100],
  ["wheels+motors", 150, 3100],
  ["battery",       200, 3000],
  ["hydrofoil",      60, 5900],
  ["stern pod",      40,  200],
  ["outfit/misc",   130, 3300],
];

// ---------------------------------------------------------------
// Helpers
// ---------------------------------------------------------------
function lerp(a, b, t) = a + (b - a) * t;
function sumv(v, i = 0) = i >= len(v) ? 0 : v[i] + sumv(v, i + 1);

// ---------------------------------------------------------------
// Arm / pod kinematics (same trig the modules use)
// ---------------------------------------------------------------
function arm_deg_for(m) =
  m == "road"   ? arm_road_deg :
  m == "launch" ? arm_launch_deg :
  m == "harbor" ? arm_harbor_deg :
                  arm_water_deg;          // cruise, foiling

function arm_frac(a) = (a - arm_road_deg) / (arm_water_deg - arm_road_deg);
function pod_deg_for(a) = arm_frac(a) * pod_water_deg;   // pod world roll

// arm tip (wheel axle) position in (y,z), starboard
function arm_tip(a) = [arm_hinge_y + arm_len * sin(a),
                       arm_hinge_z - arm_len * cos(a)];

// ama center offset from axle at pod world roll p
function ama_off(p) = [-pod_up_off * sin(p), pod_up_off * cos(p)];
function ama_center(a) = arm_tip(a) + ama_off(pod_deg_for(a));

// rotated ama bounding half-extents in y and z
function ama_yext(p) = ama_w / 2 * abs(cos(p)) + ama_h / 2 * abs(sin(p));
function ama_zext(p) = ama_w / 2 * abs(sin(p)) + ama_h / 2 * abs(cos(p));

// ---------------------------------------------------------------
// Derived: road mode
// ---------------------------------------------------------------
road_tip = arm_tip(arm_road_deg);
ground_z = road_tip[1] - wheel_dia / 2;      // road surface under keel datum
road_width = max(hull_beam,
                 2 * (road_tip[0] + ama_yext(pod_deg_for(arm_road_deg))),
                 2 * (road_tip[0] + wheel_w / 2));
canopy_top_z = cabin_roof_z + canopy_thick;
road_height = canopy_top_z - ground_z;
ground_clearance = -ground_z;                 // keel above road

// ---------------------------------------------------------------
// Derived: water mode
// ---------------------------------------------------------------
water_tip = arm_tip(arm_water_deg);
wheel_bottom_water = water_tip[1] - wheel_dia / 2;
ama_c_water = ama_center(arm_water_deg);
ama_zx = ama_zext(pod_water_deg);
ama_bottom_water = ama_c_water[1] - ama_zx;
ama_immersion = (wl_z - ama_bottom_water) / (2 * ama_zx);
water_beam = 2 * (ama_c_water[0] + ama_yext(pod_water_deg));

// ---------------------------------------------------------------
// Displacement at wl_z: clip each section at waterline, shoelace
// area, trapezoid integration along x
// ---------------------------------------------------------------
function clip_below(pts, zc) =
  [ for (i = [0 : len(pts) - 1])
      let (a = pts[i], b = pts[(i + 1) % len(pts)])
      each concat(
        a[1] <= zc ? [a] : [],
        ((a[1] <= zc) != (b[1] <= zc))
          ? [[a[0] + (b[0] - a[0]) * (zc - a[1]) / (b[1] - a[1]), zc]]
          : []) ];

function poly_area(pts) =
  len(pts) < 3 ? 0 :
  abs(sumv([ for (i = [0 : len(pts) - 1])
      let (a = pts[i], b = pts[(i + 1) % len(pts)])
      a[0] * b[1] - a[1] * b[0] ])) / 2;

function sub_area(st) = poly_area(clip_below(full_section(st), wl_z));

displacement_kg = sumv([ for (i = [0 : len(STATIONS) - 2])
    (sub_area(STATIONS[i]) + sub_area(STATIONS[i + 1])) / 2
    * (STATIONS[i + 1][0] - STATIONS[i][0]) ]) * water_rho;

// ---------------------------------------------------------------
// Mass / trim
// ---------------------------------------------------------------
total_mass = sumv([for (m = MASSES) m[1]]);
lcg = sumv([for (m = MASSES) m[1] * m[2]]) / total_mass;
axle_center_x = (arm_x_front + arm_x_rear) / 2;
coupling_x = loa + drawbar_len;
tongue_load = total_mass * (lcg - axle_center_x) / (coupling_x - axle_center_x);

// ---------------------------------------------------------------
// Checks — run once when params.scad is include<>d or opened
// ---------------------------------------------------------------
run_checks = true;

if (run_checks) {
  assert(road_width <= 2550,
    str("ROAD WIDTH ", road_width, " > 2550 mm (StVZO)"));
  assert(road_height <= 4000,
    str("ROAD HEIGHT ", road_height, " > 4000 mm (StVZO)"));
  assert(ground_clearance >= 250,
    str("GROUND CLEARANCE ", ground_clearance, " < 250 mm"));
  assert(wheel_bottom_water >= wl_z + 25,
    str("WHEELS WET in water mode: bottom ", wheel_bottom_water,
        " vs WL ", wl_z));
  assert(ama_immersion > 0.30 && ama_immersion < 0.70,
    str("AMA IMMERSION ", ama_immersion, " outside 30-70 %"));
  assert(water_beam >= 4500 && water_beam <= 5200,
    str("WATER BEAM ", water_beam, " outside 4500-5200 mm"));
  assert(foil_stow_z >= 0,
    str("STOWED FOIL below keel: ", foil_stow_z));
  assert(displacement_kg > 1600 && displacement_kg < 2300,
    str("DISPLACEMENT ", displacement_kg, " kg implausible at WL ", wl_z));

  echo(str("=== boat check ==="));
  echo(str("road width      ", road_width, " mm (limit 2550)"));
  echo(str("road height     ", road_height, " mm (limit 4000)"));
  echo(str("ground clear    ", ground_clearance, " mm"));
  echo(str("water beam      ", water_beam, " mm"));
  echo(str("wheel dry marg  ", wheel_bottom_water - wl_z, " mm above WL"));
  echo(str("ama immersion   ", round(ama_immersion * 100), " %"));
  echo(str("displacement    ", round(displacement_kg), " kg @ WL ", wl_z,
           "  (target ", total_mass, ")"));
  echo(str("mass total      ", total_mass, " kg, LCG x=", round(lcg)));
  echo(str("tongue load     ", round(tongue_load), " kg"));
  echo(str("air draft stowed ", canopy_top_z - wl_z, " mm above WL"));
}
