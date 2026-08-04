// wheel.scad — pneumatic wheel with electric hub motor, axle along y
include <../params.scad>

module wheel() {
  rotate([90, 0, 0]) {
    color([0.15, 0.15, 0.15])             // tire
      cylinder(h = wheel_w, d = wheel_dia, center = true);
    color("silver")                       // rim + hub motor cartridge
      cylinder(h = wheel_w + 50, d = hub_dia, center = true);
    color("darkorange")                   // clamshell hub cap (sealed, Solaris)
      for (s = [-1, 1])
        translate([0, 0, s * (wheel_w / 2 + 25)])
          cylinder(h = 14, d = hub_dia + 30, center = true);
  }
}

wheel();   // demo
