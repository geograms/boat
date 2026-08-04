// assembly.scad — top level. Select configuration via mode / anim / target
// (all defined in params.scad, overridable with -D on the CLI).
include <params.scad>
use <modules/hull.scad>
use <modules/cabin.scad>
use <modules/canopy.scad>
use <modules/arm.scad>
use <modules/hydrofoil.scad>
use <modules/drawbar.scad>
use <modules/stern_pod.scad>

// coarse facets: hull() forces CGAL evaluation, fine spheres are slow
$fa = 8;
$fs = 20;

// mode -> pose
arm_a = anim ? lerp(arm_road_deg, arm_water_deg, $t) : arm_deg_for(mode);
pod_p = pod_deg_for(arm_a);
foil_e = (mode == "foiling") ? 1 : 0;
lift = (canopy_up && (mode == "harbor" || mode == "cruise")) ? canopy_lift : 0;
in_water = (mode == "harbor" || mode == "cruise" || mode == "foiling");

module boat() {
  hull_body();
  cabin();
  canopy(lift);
  side_assembly(arm_a, pod_p);
  mirror([0, 1, 0]) side_assembly(arm_a, pod_p);
  hydrofoil(foil_e);
  drawbar(mode == "road");
  stern_pod();
}

// reference planes (view target only)
module refs() {
  if (in_water)
    color("lightblue", 0.35)
      translate([loa / 2, 0, wl_z - 15])
        cube([13000, 9000, 30], center = true);
  if (mode == "road")
    color("gray", 0.5)
      translate([loa / 2, 0, ground_z - 15])
        cube([13000, 9000, 30], center = true);
  if (mode == "launch") {
    lg = arm_tip(arm_launch_deg)[1] - wheel_dia / 2;
    color("gray", 0.5)                              // slipway
      translate([loa / 2, 0, lg - 15])
        cube([13000, 9000, 30], center = true);
    color("lightblue", 0.35)                        // water lapping the ramp
      translate([-4500, 0, lg + 100])
        cube([6000, 9000, 30], center = true);
  }
}

if (target == "print")
  scale(1 / 20) boat();     // 360 mm model
else {
  boat();
  refs();
}
