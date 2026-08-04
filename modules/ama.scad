// ama.scad — foam-cored float, long axis along x, centered at origin
include <../params.scad>
use <../lib/shapes.scad>

module ama() {
  color("darkorange")
    hull() {
      rounded_box([ama_len * 0.72, ama_w, ama_h], r = 90);
      // tapered bow/stern tips
      for (s = [-1, 1])
        translate([s * (ama_len / 2 - 80), 0, ama_h * 0.1])
          rotate([0, 90, 0])
            cylinder(h = 40, d = ama_h * 0.4, center = true);
    }
}

ama();   // demo
