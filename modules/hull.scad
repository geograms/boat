// hull.scad — chined main hull lofted from STATIONS
include <../params.scad>
use <../lib/loft.scad>

module hull_body() {
  color("whitesmoke")
    loft_stations([for (st = STATIONS) [st[0], full_section(st)]]);
}

hull_body();   // demo when opened standalone (assembly use<>s this file)
