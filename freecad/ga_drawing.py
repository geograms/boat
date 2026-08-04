#!/usr/bin/env python3
"""General-arrangement drawing (dimensioned) -> docs/images/general_arrangement.png

Pure matplotlib; every number is read from params.py, so the drawing can
never drift from the model.  Run:  python3 freecad/ga_drawing.py
"""
import os
import sys
import math

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import params as P

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon, Rectangle, Circle, FancyBboxPatch

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                   "..", "docs", "images", "general_arrangement.png")

HULL = "#2b3a52"
GLASS = "#d7e3ea"
CABIN = "#dcdcd6"
ROOF = "#1f2a44"
FLOATC = "#e08a17"
DIM = "#b3202b"
INK = "#1a1a1a"

# ---------------------------------------------------------------- helpers
def keel(x):
    return P.keel_z_at(x)


def sheer(x):
    S = P.STATIONS
    for i in range(len(S) - 1):
        x0, x1 = S[i][0], S[i + 1][0]
        if x0 <= x <= x1:
            t = (x - x0) / (x1 - x0)
            return S[i][5] + t * (S[i + 1][5] - S[i][5])
    return S[-1][5]


def hull_profile():
    """Closed side-view outline of the hull, transom at x=0."""
    S = P.STATIONS
    bot = [(s[0], s[3]) for s in S]
    top = [(s[0], s[5]) for s in S]
    return bot + top[::-1]


def dim_h(ax, x0, x1, y, label, off=0, tick=60, fs=10, colour=DIM):
    """Horizontal dimension with arrow heads and witness ticks."""
    ax.annotate("", (x0, y), (x1, y),
                arrowprops=dict(arrowstyle="<->", color=colour, lw=1.2))
    for x in (x0, x1):
        ax.plot([x, x], [y - tick, y + tick], color=colour, lw=0.8)
    ax.text((x0 + x1) / 2, y + off + 40, label, ha="center", va="bottom",
            color=colour, fontsize=fs, fontweight="bold")


def dim_v(ax, y0, y1, x, label, tick=60, fs=10, colour=DIM, side="left"):
    ax.annotate("", (x, y0), (x, y1),
                arrowprops=dict(arrowstyle="<->", color=colour, lw=1.2))
    for y in (y0, y1):
        ax.plot([x - tick, x + tick], [y, y], color=colour, lw=0.8)
    ax.text(x + (-90 if side == "left" else 90), (y0 + y1) / 2, label,
            ha="center", va="center", rotation=90, color=colour,
            fontsize=fs, fontweight="bold")


def witness(ax, x0, y0, x1, y1):
    ax.plot([x0, x1], [y0, y1], color=DIM, lw=0.6, ls=(0, (3, 3)), alpha=0.75)


def clean(ax):
    ax.set_aspect("equal")
    ax.axis("off")


# ---------------------------------------------------------------- numbers
D = dict(
    LOA=P.LOA,
    beam=P.HULL_BEAM,
    WL=P.WL_Z,
    cabin_L=P.CABIN_X1 - P.CABIN_X0,
    cabin_W=P.CABIN_W,
    cabin_W_in=P.CABIN_W - 120,
    sole=350,
    head=P.CABIN_CEIL_Z - 350,
    roof=P.CABIN_ROOF_Z,
    canopy_top=P.CABIN_ROOF_Z + P.DECK_BUILDUP,
    ground=P.GROUND_Z,
    road_h=P.CABIN_ROOF_Z + P.DECK_BUILDUP - P.GROUND_Z,
    water_beam=2 * (P.POD_WATER[0] + P.FLOAT_W / 2),
    disp=P.displacement_kg(),
    door=1700,
    balc=P.BALC_SPAN,
    passage=P.PASSAGE_W,
    float_L=P.FLOAT_LEN,
    tongue=P.tongue_load_kg(),
    track=2 * P.POD_ROAD[0] + 2 * 435,
)
D["air_draft"] = D["canopy_top"] - P.WL_Z
D["cpl_x"], D["cpl_z"] = P.arch_coupling()
D["cpl_h"] = D["cpl_z"] - P.GROUND_Z
D["overhang"] = -D["cpl_x"]
wx = [P.FLOAT_X + d for d in P.WHEEL_XS]
D["wheelbase"] = max(wx) - min(wx)

fig = plt.figure(figsize=(19.2, 15.6), dpi=100)
fig.patch.set_facecolor("white")
gs = fig.add_gridspec(3, 2, height_ratios=[1.0, 0.78, 1.06],
                      hspace=0.06, wspace=0.02,
                      left=0.03, right=0.985, top=0.925, bottom=0.015)

fig.text(0.5, 0.988, "BOAT-HOME  ·  GENERAL ARRANGEMENT  ·  "
         "all dimensions in mm", ha="center", va="center",
         fontsize=21, fontweight="bold", color=INK)

# ================================================== 1. profile afloat
ax = fig.add_subplot(gs[0, :])
clean(ax)
ax.set_title("PROFILE  —  afloat (cruise),  bow to the right", loc="left",
             fontsize=14, fontweight="bold", color=INK, pad=10)

ax.add_patch(Polygon(hull_profile(), closed=True, fc=HULL, ec=INK, lw=1.2))

# cockpit tub (open well aft)
ax.add_patch(Rectangle((P.COCKPIT_X0, P.COCKPIT_FLOOR),
                       P.COCKPIT_X1 - P.COCKPIT_X0,
                       P.CABIN_BASE_Z - P.COCKPIT_FLOOR,
                       fc="white", ec=INK, lw=1.0))
ax.text((P.COCKPIT_X0 + P.COCKPIT_X1) / 2, P.COCKPIT_FLOOR + 230,
        "cockpit\nwell", ha="center", va="center", fontsize=8.5, color=INK)

# cabin + winter garden envelope
ax.add_patch(Rectangle((P.CABIN_X0, P.CABIN_BASE_Z),
                       P.CABIN_X1 - P.CABIN_X0,
                       P.CABIN_ROOF_Z - P.CABIN_BASE_Z,
                       fc=CABIN, ec=INK, lw=1.0))
glass = [(P.CABIN_X0, P.CABIN_BASE_Z), (P.CABIN_X0, P.CABIN_ROOF_Z - 40),
         (P.CABIN_X1, P.CABIN_ROOF_Z - 40), (6700, 1950), (6980, 1500),
         (7050, sheer(7050)), (P.CABIN_X1, sheer(P.CABIN_X1) + 10)]
ax.add_patch(Polygon(glass, closed=True, fc=GLASS, ec=INK, lw=1.0,
                     alpha=0.85))
ax.text(6560, 1640, "winter\ngarden", ha="center", va="center",
        fontsize=8.5, style="italic", color=INK)

# walk-on glass deck over the structural roof
ax.add_patch(Rectangle((P.CABIN_X0 - 20, P.CABIN_ROOF_Z),
                       P.CABIN_X1 - P.CABIN_X0 + 40, P.DECK_BUILDUP,
                       fc=ROOF, ec=INK, lw=1.0))
ax.text(P.CABIN_X0 + 300, P.CABIN_ROOF_Z + P.DECK_BUILDUP + 120,
        f"walk-on glass sun deck  ·  build-up {P.DECK_BUILDUP} mm  ·  "
        "no moving parts", ha="left", va="bottom", fontsize=9.5,
        color=DIM, fontweight="bold")

# solar balcony (folded-down walkway, seen edge-on behind the hull)
ax.plot([P.BALC_X0, P.BALC_X1], [P.CABIN_BASE_Z + 30, P.CABIN_BASE_Z + 30],
        color="#12325c", lw=4, solid_capstyle="butt", zorder=0)

# waterline + sole
ax.plot([-1500, 8600], [P.WL_Z, P.WL_Z], color="#2f7fbf", lw=1.4)
ax.text(8620, P.WL_Z, "WL", ha="left", va="center", color="#2f7fbf",
        fontsize=10, fontweight="bold")
ax.plot([P.CABIN_X0, P.CABIN_X1], [350, 350], color=INK, lw=0.9,
        ls=(0, (5, 3)))
ax.text(P.CABIN_X0 + 200, 240,
        f"cabin sole 350 above keel  ·  displacement ≈ "
        f"{D['disp']:.0f} kg", ha="left", va="top", fontsize=9,
        style="italic", color=INK)

# ---- dimensions
top = P.CABIN_ROOF_Z + P.DECK_BUILDUP + 1100
dim_h(ax, 0, P.LOA, top, f"LOA  {P.LOA}")
witness(ax, 0, P.STATIONS[0][5], 0, top)
witness(ax, P.LOA, P.STATIONS[-1][5], P.LOA, top)

dim_h(ax, P.CABIN_X0, P.CABIN_X1, top - 560, f"cabin {D['cabin_L']}")
witness(ax, P.CABIN_X0, P.CABIN_ROOF_Z + P.DECK_BUILDUP,
        P.CABIN_X0, top - 560)
witness(ax, P.CABIN_X1, P.CABIN_ROOF_Z + P.DECK_BUILDUP,
        P.CABIN_X1, top - 560)

dim_v(ax, P.WL_Z, D["canopy_top"], 8300, f"air draft {D['air_draft']}")
witness(ax, P.CABIN_X1, D["canopy_top"], 8300, D["canopy_top"])

dim_v(ax, 0, P.WL_Z, -1150, f"draft {P.WL_Z}", side="right")
witness(ax, 0, 0, -1150, 0)
witness(ax, 0, P.WL_Z, -1150, P.WL_Z)

dim_v(ax, 350, P.CABIN_CEIL_Z, 5900, f"headroom {D['head']}")
dim_v(ax, P.COCKPIT_FLOOR, P.COCKPIT_FLOOR + D["door"], 1560,
      f"door {D['door']}")

ax.set_xlim(-1900, 9400)
ax.set_ylim(-450, top + 700)

# ================================================== 2. profile on road
ax = fig.add_subplot(gs[1, :])
clean(ax)
ax.set_title("PROFILE  —  on the road  (floats folded flat under the hull, "
             "towed stern-first)", loc="left", fontsize=14,
             fontweight="bold", color=INK, pad=10)

g = P.GROUND_Z
# folded float band
fl_x0 = P.FLOAT_X - P.FLOAT_LEN / 2
ax.add_patch(Rectangle((fl_x0, P.POD_ROAD[1] - P.FLOAT_W / 2), P.FLOAT_LEN,
                       P.FLOAT_W / 2 + 80, fc=FLOATC, ec=INK, lw=1.0))
ax.text(fl_x0 + 250, P.POD_ROAD[1] - 470,
        "float folded on its side = road chassis", ha="left", va="top",
        fontsize=9, color=INK)

ax.add_patch(Polygon(hull_profile(), closed=True, fc=HULL, ec=INK, lw=1.2))
ax.add_patch(Rectangle((P.CABIN_X0, P.CABIN_BASE_Z),
                       P.CABIN_X1 - P.CABIN_X0,
                       P.CABIN_ROOF_Z - P.CABIN_BASE_Z,
                       fc=CABIN, ec=INK, lw=1.0))
ax.add_patch(Rectangle((P.CABIN_X0 - 20, P.CABIN_ROOF_Z),
                       P.CABIN_X1 - P.CABIN_X0 + 40, P.DECK_BUILDUP,
                       fc=ROOF, ec=INK, lw=1.0))
# folded solar shutters standing over the windows
for x0 in (P.CABIN_X0 + 150, P.CABIN_X0 + 1900, P.CABIN_X0 + 3650):
    ax.add_patch(Rectangle((x0, P.CABIN_BASE_Z + 60), 1700, 40,
                           fc="#12325c", ec="none"))

for dx in P.WHEEL_XS:
    ax.add_patch(Circle((P.FLOAT_X + dx, g + P.WHEEL_DIA / 2),
                        P.WHEEL_DIA / 2, fc="#232323", ec=INK, lw=1.0))
    ax.add_patch(Circle((P.FLOAT_X + dx, g + P.WHEEL_DIA / 2), 130,
                        fc="#9aa2ab", ec=INK, lw=0.8))
ax.plot([-2600, 8000], [g, g], color="#555", lw=2.0)

# drawbar
ax.plot([P.ARCH_PIVOT_X, D["cpl_x"]], [P.ARCH_PIVOT_Z, D["cpl_z"]],
        color="#3c3c3c", lw=5, solid_capstyle="round")
ax.add_patch(Circle((D["cpl_x"], D["cpl_z"]), 90, fc="#3c3c3c", ec=INK))
ax.text(D["cpl_x"] + 60, D["cpl_z"] + 300, "coupling", ha="center",
        va="bottom", fontsize=9, color=INK)

dim_v(ax, g, D["canopy_top"], 8400, f"road height {D['road_h']:.0f}",
      side="right")
witness(ax, P.CABIN_X1, D["canopy_top"], 8400, D["canopy_top"])
witness(ax, 3000, g, 8400, g)

dim_v(ax, g, D["cpl_z"], D["cpl_x"] - 700, f"coupling {D['cpl_h']:.0f}")
dim_h(ax, fl_x0, fl_x0 + P.FLOAT_LEN, g - 700, f"float {P.FLOAT_LEN}")
dim_h(ax, min(wx), max(wx), g - 1150, f"wheelbase {D['wheelbase']:.0f}")
dim_h(ax, D["cpl_x"], P.LOA, g - 1600,
      f"length with drawbar {P.LOA + D['overhang']:.0f}")
dim_v(ax, g, 0, 7500, f"clearance {-g:.0f}", side="right")
witness(ax, 6300, 0, 7500, 0)
witness(ax, 6300, g, 7500, g)

ax.text(P.LOA / 2, g - 2150,
        f"6 × 205/70 R15 all-terrain  ·  track {D['track']:.0f}  ·  "
        f"tongue load +{D['tongue']:.0f} kg  ·  "
        f"road width {P.HULL_BEAM + 35}  (limit 2 550)",
        ha="center", va="top", fontsize=10, style="italic", color=INK)

ax.set_xlim(-3400, 9700)
ax.set_ylim(g - 2600, D["canopy_top"] + 500)

# ================================================== 3. midship section
ax = fig.add_subplot(gs[2, 0])
clean(ax)
ax.set_title("MIDSHIP SECTION  —  afloat  (looking forward)", loc="left",
             fontsize=14, fontweight="bold", color=INK, pad=10)

sec = P.full_section(P.STATIONS[3])
ax.add_patch(Polygon([(y, z) for y, z in sec], closed=True, fc=HULL,
                     ec=INK, lw=1.2))
ax.add_patch(Rectangle((-P.CABIN_W / 2, P.CABIN_BASE_Z), P.CABIN_W,
                       P.CABIN_ROOF_Z - P.CABIN_BASE_Z, fc=CABIN, ec=INK,
                       lw=1.0))
ax.add_patch(Rectangle((-P.CABIN_W / 2 - 20, P.CABIN_ROOF_Z),
                       P.CABIN_W + 40, P.DECK_BUILDUP, fc=ROOF, ec=INK,
                       lw=1.0))
ax.plot([-1250, 1250], [P.CABIN_BASE_Z, P.CABIN_BASE_Z], color=INK, lw=2.5)

for s in (1, -1):
    py, pz = P.POD_WATER
    ax.add_patch(Rectangle((s * py - P.FLOAT_W / 2, pz - P.FLOAT_H / 2),
                           P.FLOAT_W, P.FLOAT_H, fc=FLOATC, ec=INK, lw=1.0))
    # arm + balcony deck
    ax.plot([s * P.SH_Y, s * py], [P.SH_Z, pz + P.FLOAT_H / 2],
            color="#3c3c3c", lw=3)
    ax.plot([s * P.BALC_HINGE_Y, s * (P.BALC_HINGE_Y + P.BALC_SPAN)],
            [P.CABIN_BASE_Z + 20, P.CABIN_BASE_Z + 20],
            color="#12325c", lw=5, solid_capstyle="butt")

ax.plot([-3400, 3400], [P.WL_Z, P.WL_Z], color="#2f7fbf", lw=1.4)

dim_h(ax, -P.HULL_BEAM / 2, P.HULL_BEAM / 2, 620,
      f"hull beam {P.HULL_BEAM}")
dim_h(ax, -P.CABIN_W / 2 + 60, P.CABIN_W / 2 - 60, P.CABIN_ROOF_Z + 620,
      f"interior {D['cabin_W_in']}")
witness(ax, -P.CABIN_W / 2 + 60, P.CABIN_ROOF_Z + P.DECK_BUILDUP,
        -P.CABIN_W / 2 + 60, P.CABIN_ROOF_Z + 620)
witness(ax, P.CABIN_W / 2 - 60, P.CABIN_ROOF_Z + P.DECK_BUILDUP,
        P.CABIN_W / 2 - 60, P.CABIN_ROOF_Z + 620)
dim_h(ax, P.BALC_HINGE_Y, P.BALC_HINGE_Y + P.BALC_SPAN,
      P.CABIN_BASE_Z + 430, f"solar balcony {P.BALC_SPAN}", fs=9)
dim_h(ax, -D["water_beam"] / 2, D["water_beam"] / 2, -1150,
      f"beam afloat {D['water_beam']:.0f}")
witness(ax, -D["water_beam"] / 2, P.POD_WATER[1] - P.FLOAT_H / 2,
        -D["water_beam"] / 2, -1150)
witness(ax, D["water_beam"] / 2, P.POD_WATER[1] - P.FLOAT_H / 2,
        D["water_beam"] / 2, -1150)
dim_v(ax, P.CABIN_BASE_Z, P.CABIN_ROOF_Z, -2050, f"cabin {P.CABIN_ROOF_Z - P.CABIN_BASE_Z:,}".replace(",", " "),
      fs=9, side="right")

ax.set_xlim(-3600, 3600)
ax.set_ylim(-1750, P.CABIN_ROOF_Z + 1000)

# ================================================== 4. table
ax = fig.add_subplot(gs[2, 1])
ax.axis("off")
ax.set_title("KEY DIMENSIONS", loc="left", fontsize=14,
             fontweight="bold", color=INK, pad=10)

rows = [
    ("H", "OVERALL", ""),
    ("", "length, hull", f"{P.LOA:,} mm".replace(",", " ")),
    ("", "length with drawbar", f"{P.LOA + D['overhang']:,.0f} mm"
        .replace(",", " ")),
    ("", "beam — road / afloat",
     f"2 535 / {D['water_beam']:,.0f} mm".replace(",", " ")),
    ("", "height on the road",
     f"{D['road_h']:,.0f} mm  (StVZO limit 4 000)".replace(",", " ")),
    ("", "air draft afloat", f"{D['air_draft']:,.0f} mm".replace(",", " ")),
    ("", "draft / displacement",
     f"{P.WL_Z} mm / ≈{D['disp']:,.0f} kg".replace(",", " ")),
    ("H", "LIVING QUARTERS", ""),
    ("", "cabin length", f"{D['cabin_L']:,} mm".replace(",", " ")),
    ("", "cabin width, inside", f"{D['cabin_W_in']:,} mm".replace(",", " ")),
    ("", "standing headroom", f"{D['head']:,} mm".replace(",", " ")),
    ("", "roof sun deck", "walk-on glass, 8 panes"),
    ("", "floor area", "≈ 12.1 m²"),
    ("", "entry door, clear", f"700 × {D['door']:,} mm".replace(",", " ")),
    ("", "cockpit floor / bulwark", "400 / 750 mm"),
    ("H", "DECKS & SOLAR", ""),
    ("", "solar balcony", f"{P.BALC_SPAN:,} wide: {P.BALC_WALK_W} walkway"
     f" + {P.BALC_PANEL_W} panels".replace(",", " ")),
    ("", "aft passage width", f"{P.PASSAGE_W} mm  (part of the folding deck)"),
    ("", "roof terrace", f"{P.CABIN_X1 - P.CABIN_X0:,} × 2 360 mm"
     .replace(",", " ")),
    ("", "panels", f"5 laminates + 6 std modules (≈ 3.1 kWp)"
     .replace(",", " ")),
    ("H", "ROAD GEAR", ""),
    ("", "wheels", "6 × 205/70 R15 all-terrain"),
    ("", "track / wheelbase",
     f"{D['track']:,.0f} / {D['wheelbase']:,.0f} mm".replace(",", " ")),
    ("", "ground clearance", f"{-P.GROUND_Z:.0f} mm"),
    ("", "coupling height / tongue",
     f"{D['cpl_h']:.0f} mm / +{D['tongue']:.0f} kg"),
    ("", "float, each", f"{P.FLOAT_LEN:,} × {P.FLOAT_W} × {P.FLOAT_H} mm".replace(",", " ")),
]

y = 0.985
for kind, left, right in rows:
    if kind == "H":
        y -= 0.008
        ax.text(0.0, y, left, transform=ax.transAxes, fontsize=11.5,
                fontweight="bold", color=DIM, va="top", family="monospace")
        y -= 0.040
    else:
        ax.text(0.035, y, left, transform=ax.transAxes, fontsize=11,
                color=INK, va="top", family="monospace")
        ax.text(0.60, y, right, transform=ax.transAxes, fontsize=11,
                color=INK, va="top", family="monospace")
        y -= 0.0335

fig.savefig(OUT, dpi=100, facecolor="white")
print("wrote", os.path.normpath(OUT))
