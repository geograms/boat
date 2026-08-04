// cabin.scad — boat-home cabin on deck: berth, galley, wet head inside
include <../params.scad>
use <../lib/shapes.scad>

module cabin() {
  cl = cabin_x1 - cabin_x0;
  ch = cabin_roof_z - cabin_base_z;
  difference() {
    color("whitesmoke")
      translate([(cabin_x0 + cabin_x1) / 2, 0, cabin_base_z + ch / 2])
        rounded_box([cl, cabin_w, ch], r = 60);
    // side windows, 3 per side
    for (i = [0 : 2])
      translate([cabin_x0 + cl * (0.22 + 0.28 * i), 0,
                 cabin_base_z + ch * 0.62])
        cube([cl * 0.20, cabin_w + 200, ch * 0.42], center = true);
    // windshield (forward face)
    translate([cabin_x1, 0, cabin_base_z + ch * 0.62])
      cube([200, cabin_w * 0.7, ch * 0.42], center = true);
    // aft door
    translate([cabin_x0, 0, cabin_base_z + ch * 0.45])
      cube([200, 650, ch * 0.9], center = true);
  }
}

cabin();   // demo
