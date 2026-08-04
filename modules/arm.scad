// arm.scad — one side of the hangar: two hinged arms, wheel pods, ama.
// arm_a: main hinge angle from straight-down (+ = outboard)
// pod_p: pod world roll (road 0 -> water pod_water_deg)
// Starboard geometry; assembly mirrors for port.
include <../params.scad>
use <wheel.scad>
use <ama.scad>

module arm_beam() {
  // box arm from hinge to pod pivot, along -z in hinge frame
  color("dimgray") {
    translate([0, 0, -arm_len / 2])
      cube([arm_w, arm_t, arm_len + arm_w], center = true);
    // hinge knuckle + lock-pin boss
    rotate([0, 90, 0])
      cylinder(h = arm_w + 60, d = arm_t + 40, center = true);
  }
}

module side_assembly(arm_a, pod_p) {
  for (ax = [arm_x_rear, arm_x_front])
    translate([ax, arm_hinge_y, arm_hinge_z])
      rotate([arm_a, 0, 0]) {
        arm_beam();
        translate([0, 0, -arm_len])
          rotate([pod_p - arm_a, 0, 0]) {
            wheel();
            // ama rides on both pods; draw once, off the rear arm
            if (ax == arm_x_rear)
              translate([ama_x - arm_x_rear, 0, pod_up_off])
                ama();
          }
      }
}

side_assembly(arm_road_deg, 0);   // demo: road pose
