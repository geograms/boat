// drawbar.scad — fold-up A-frame at the bow with ball coupling
include <../params.scad>
use <../lib/shapes.scad>

module drawbar(deployed = true) {
  attach = [for (s = [-1, 1]) [6500, s * 430, 900]];
  tip = deployed
    ? [coupling_x, 0, ground_z + coupling_h]   // to car hitch
    : [7050, 0, 1900];                         // folded up over bow
  color("dimgray") {
    for (a = attach) rod(a, tip, 90);
    translate(tip) sphere(d = 140);            // coupling head
  }
}

drawbar(true);   // demo: deployed
