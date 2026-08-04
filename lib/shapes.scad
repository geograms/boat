// shapes.scad — small geometry helpers

// box with rounded corners, centered
module rounded_box(size, r = 40) {
  hull()
    for (x = [-size[0]/2 + r, size[0]/2 - r],
         y = [-size[1]/2 + r, size[1]/2 - r],
         z = [-size[2]/2 + r, size[2]/2 - r])
      translate([x, y, z]) sphere(r = r);
}

// rod between two points
module rod(p1, p2, d) {
  hull() {
    translate(p1) sphere(d = d);
    translate(p2) sphere(d = d);
  }
}

// symmetric NACA-4-digit-ish foil section, chord along +x, LE at origin
function naca_half(c, t, n) =
  [ for (i = [0 : n])
      let (u = i / n,
           yt = 5 * t * c * (0.2969 * sqrt(u) - 0.1260 * u
                - 0.3516 * u * u + 0.2843 * u * u * u
                - 0.1015 * u * u * u * u))
      [u * c, yt] ];

function foil_pts(c, t = 0.12, n = 24) =
  concat(naca_half(c, t, n),
         [ for (i = [n - 1 : -1 : 1])
             let (p = naca_half(c, t, n)[i]) [p[0], -p[1]] ]);
