// stern_pod.scad — placeholder electric pod drive under the transom
include <../params.scad>

module stern_pod() {
  color("dimgray") {
    // strut from hull
    translate([250, 0, 150])
      cube([120, 60, 500], center = false);
    // pod body along x
    translate([550, 0, 150])
      rotate([0, -90, 0])
        cylinder(h = sternpod_len, d = sternpod_dia);
    // prop disc at aft end
    color("goldenrod")
      translate([550 - sternpod_len - 15, 0, 150])
        rotate([0, 90, 0])
          cylinder(h = 25, d = sternpod_dia + 90, center = true);
  }
}

stern_pod();   // demo
