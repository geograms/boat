// hydrofoil.scad — retractable bow T-foil. ext 0 (stowed) .. 1 (deployed)
include <../params.scad>
use <../lib/shapes.scad>

module hydrofoil(ext = 0) {
  wing_z = lerp(foil_stow_z, foil_deploy_z, ext);
  color("dodgerblue") {
    // strut: vertical foil section, chord along x, from hull into water
    translate([foil_x + foil_strut_chord / 2, 0, wing_z])
      rotate([0, 0, 180])                       // LE forward
        linear_extrude(600 - wing_z)
          polygon(foil_pts(foil_strut_chord, 0.15));
    // main wing: span along y, slight dihedral
    for (s = [-1, 1])
      scale([1, s, 1])
        translate([foil_x + foil_chord / 2, 0, wing_z])
          rotate([4, 0, 0])                     // dihedral, tips up
            rotate([90, 0, 180])                // span +y, LE forward
              linear_extrude(foil_span / 2)
                polygon(foil_pts(foil_chord, 0.12));
  }
}

hydrofoil(1);   // demo: deployed
