// canopy.scad — pop-top solar canopy, 4 actuators, lift 0..canopy_lift
include <../params.scad>
use <../lib/shapes.scad>

module canopy(lift = 0) {
  cl = cabin_x1 - cabin_x0 + 2 * canopy_overhang;
  cw = cabin_w + 2 * canopy_overhang;
  cx = (cabin_x0 + cabin_x1) / 2;
  // canopy slab
  translate([cx, 0, cabin_roof_z + lift + canopy_thick / 2]) {
    color("whitesmoke")
      rounded_box([cl, cw, canopy_thick], r = 50);
    // solar panels, 2 x 3 grid
    color("midnightblue")
      for (i = [0 : 2], j = [-1, 1])
        translate([(i - 1) * cl * 0.32, j * cw * 0.26,
                   canopy_thick / 2 + 6])
          cube([cl * 0.29, cw * 0.44, 14], center = true);
  }
  // 4 actuators from roof corners
  if (lift > 1)
    color("silver")
      for (sx = [-1, 1], sy = [-1, 1])
        translate([cx + sx * (cl / 2 - 180), sy * (cw / 2 - 180),
                   cabin_roof_z])
          cylinder(h = lift, d = 60);
  // guardrail when raised (terrace mode)
  if (lift > canopy_lift * 0.9)
    color("silver")
      for (sy = [-1, 1])
        translate([cx, sy * (cw / 2 - 40),
                   cabin_roof_z + lift + canopy_thick])
          rotate([0, 90, 0])
            cylinder(h = cl - 200, d = 35, center = true);
}

canopy(canopy_lift);   // demo: raised
