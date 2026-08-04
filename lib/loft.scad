// loft.scad — station lofting.
// hull()-chain over convex sections now; polyhedron skin can replace
// loft_stations() later with the same call signature.

// one thin slab of a section polygon (points in (y,z)) at station x
module station_slab(x, pts) {
  translate([x, 0, 0])
    rotate([90, 0, 90])       // polygon (y,z) -> Y-Z plane, extrude +x
      linear_extrude(1)
        polygon(pts);
}

// stations = [[x, [[y,z], ...]], ...] ordered by x, same winding
module loft_stations(stations) {
  for (i = [0 : len(stations) - 2])
    hull() {
      station_slab(stations[i][0], stations[i][1]);
      station_slab(stations[i + 1][0], stations[i + 1][1]);
    }
}
