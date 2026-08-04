#!/usr/bin/env python3
"""Interior layout sheet -> docs/images/interior_plan.png

Three views at the same scale: what you see (plan), what is hidden
under and above it (stowage plan), and three cross sections. Numbers
come from params.py.  Run: python3 freecad/interior_plan.py
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import params as P

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, Circle
from matplotlib.lines import Line2D

OUT = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                    "..", "docs", "images",
                                    "interior_plan.png"))
INK = "#1a1a1a"
DIM = "#b3202b"
JOIN = "#e0d2b0"
SOFT = "#93a2b3"
APPL = "#e6e9ec"
HEAVY = "#3f7a5e"
GLASS = "#bcd6e6"
HID = "#7a4fa3"
WET = "#eaf1f4"

S, C, HW = P.SOLE_Z, P.CABIN_CEIL_Z, P.IN_HW
LEN = P.CABIN_X1 - P.CABIN_X0


def rect(ax, x0, x1, y0, y1, fc, hidden=False, z=3, alpha=1.0):
    ax.add_patch(Rectangle((x0, y0), x1 - x0, y1 - y0, fc=fc,
                           ec=HID if hidden else INK,
                           lw=1.6 if hidden else 1.0,
                           ls=(0, (5, 3)) if hidden else "-",
                           alpha=alpha, zorder=z))


def lbl(ax, x, y, text, fs=9, hidden=False, rot=0, bold=False):
    ax.text(x, y, text, ha="center", va="center", fontsize=fs, rotation=rot,
            color=HID if hidden else INK,
            fontweight="bold" if (bold or hidden) else "normal", zorder=6)


def shell(ax, glazing=True):
    ax.add_patch(Rectangle((P.CABIN_X0, -HW), LEN, 2 * HW, fc="white",
                           ec=INK, lw=2.2, zorder=1))
    if not glazing:
        return
    for wx, wl in P.WINDOWS:
        for sy in (-1, 1):
            ax.add_patch(Rectangle((wx, sy * HW - (46 if sy > 0 else 0)),
                                   wl, 46, fc=GLASS, ec="#4b7c99", lw=1.3,
                                   zorder=7))
    px, pz, pd = P.PORTHOLE
    for sy in (-1, 1):
        ax.add_patch(Circle((px, sy * HW), 110, fc=GLASS, ec="#4b7c99",
                            lw=1.2, zorder=7))


def dim_h(ax, x0, x1, y, label, fs=9):
    ax.annotate("", (x0, y), (x1, y),
                arrowprops=dict(arrowstyle="<->", color=DIM, lw=1.1))
    for x in (x0, x1):
        ax.plot([x, x], [y - 60, y + 60], color=DIM, lw=0.8)
    ax.text((x0 + x1) / 2, y + 70, label, ha="center", va="bottom",
            fontsize=fs, color=DIM, fontweight="bold")


fig = plt.figure(figsize=(19.2, 19.0), dpi=100)
fig.patch.set_facecolor("white")
fig.text(0.5, 0.982, "BOAT-HOME  ·  INTERIOR", ha="center", fontsize=23,
         fontweight="bold", color=INK)
fig.text(0.5, 0.963, f"{LEN} × {2 * HW:.0f} mm floor  ·  {C - S} mm "
         f"headroom  ·  berths for 4  ·  all dimensions in mm",
         ha="center", fontsize=12, color="#555")

# ============================================================ 1. PLAN
ax = fig.add_axes([0.04, 0.585, 0.92, 0.35])
ax.set_aspect("equal")
ax.axis("off")
ax.set_title("PLAN  —  what you see,  bow to the right", loc="left",
             fontsize=14, fontweight="bold", color=INK)
shell(ax)

# entry
ax.add_patch(Rectangle((P.CABIN_X0 - 14, -P.DOOR_HW), 28, 2 * P.DOOR_HW,
                       fc="#f2c14e", ec=INK, lw=1.0, zorder=8))
lbl(ax, P.CABIN_X0 - 150, 0, "ENTRY", 9.5, rot=90, bold=True)

# --- service zone
rect(ax, *P.AC_UNIT_X, *P.AC_UNIT_Y, APPL)
lbl(ax, sum(P.AC_UNIT_X) / 2, sum(P.AC_UNIT_Y) / 2, "AC\nunit", 8.5)
rect(ax, P.GALLEY_X[0], P.FRIDGE_X[0], *P.GALLEY_Y, JOIN)
lbl(ax, (P.GALLEY_X[0] + P.FRIDGE_X[0]) / 2, sum(P.GALLEY_Y) / 2,
    "GALLEY\nsink · hob", 9)
rect(ax, *P.FRIDGE_X, *P.GALLEY_Y, APPL)
lbl(ax, sum(P.FRIDGE_X) / 2, sum(P.GALLEY_Y) / 2, "FRIDGE\n+ FREEZER\n"
    f"{P.OH_Z1 - S} tall", 8.5)

hx0, hx1 = P.HEADS_X
hy0, hy1 = P.HEADS_Y
rect(ax, hx0, hx1, hy0, hy1, WET, z=2)
rect(ax, hx0 + 80, hx0 + 560, hy0 + 90, hy0 + 480, APPL)
lbl(ax, hx0 + 320, hy0 + 285, "WC", 8.5)
rect(ax, hx1 - 620, hx1 - 60, hy0 + 40, hy0 + 420, APPL)
lbl(ax, hx1 - 340, hy0 + 230, "basin", 8.5)
ax.add_patch(Rectangle((hx1 - 700, hy0 + 30), 660, (hy1 - hy0) - 60,
                       fc="none", ec="#2f7fbf", lw=1.3, ls=(0, (2, 2)),
                       zorder=5))
lbl(ax, hx1 - 330, hy0 + 640, "shower", 8)
lbl(ax, hx0 + 500, hy1 - 150, "HEADS — wetroom", 9.5, bold=True)
ax.plot(P.HEADS_DOOR_X, [hy1, hy1], color="#f2c14e", lw=5, zorder=8)

ax.annotate("", (P.CABIN_X0 + 60, 150), (P.HEADS_X[1] + 60, 150),
            arrowprops=dict(arrowstyle="<->", color="#2f7fbf", lw=1.3))
lbl(ax, (P.CABIN_X0 + P.HEADS_X[1]) / 2, 300,
    f"corridor {P.CORRIDOR_Y[1] - P.CORRIDOR_Y[0]:.0f} wide", 9)

# --- dinette
bx0, bx1 = P.BERTH_X
for sy in (-1, 1):
    y_out, y_in = sy * HW, sy * (HW - P.SETTEE_D)
    rect(ax, bx0, bx1, min(y_out, y_in), max(y_out, y_in), SOFT)
    lbl(ax, (bx0 + bx1) / 2, (y_out + y_in) / 2,
        f"SETTEE  /  SINGLE BERTH  {bx1 - bx0} × {P.SETTEE_D}", 9)
tx0 = (bx0 + bx1 - P.TABLE_L) / 2
rect(ax, tx0, tx0 + P.TABLE_L, -P.TABLE_W / 2, P.TABLE_W / 2, "#f0e6cd")
lbl(ax, (bx0 + bx1) / 2, 0,
    f"TABLE {P.TABLE_L} × {P.TABLE_W}\nremovable — drops to\nmake a double",
    8.5)

# --- forward
wx0, wx1 = P.WARDROBE_X
for sy in (-1, 1):
    rect(ax, wx0, wx1, min(sy * HW, sy * (HW - P.WARDROBE_W)),
         max(sy * HW, sy * (HW - P.WARDROBE_W)), JOIN)
    lbl(ax, (wx0 + wx1) / 2, sy * (HW - P.WARDROBE_W / 2), "WARDROBE",
        8.5, rot=90)
bdx0, bdx1 = P.BED_X
rect(ax, bdx0 + 40, bdx0 + 40 + P.MATTRESS_W, -P.MATTRESS_L / 2,
     P.MATTRESS_L / 2, SOFT)
lbl(ax, bdx0 + 40 + P.MATTRESS_W / 2, 0,
    f"ELEVATING DOUBLE BED\n{P.MATTRESS_L} across × {P.MATTRESS_W}\n"
    "hoists to the deckhead by day", 9.5)
for rx in (bdx0 + 70, bdx0 + 10 + P.MATTRESS_W):
    for sy in (-1, 1):
        rect(ax, rx - 30, rx + 30, sy * (P.MATTRESS_L / 2 + 60) - 30,
             sy * (P.MATTRESS_L / 2 + 60) + 30, "#5b6570")
lbl(ax, bdx0 + 40 + P.MATTRESS_W / 2, -HW + 260,
    "with the bed up this whole zone is free floor", 8)

for wx, wl in P.WINDOWS:
    lbl(ax, wx + wl / 2, -HW - 190, f"picture window {wl} × {P.WIN_H}", 9)
lbl(ax, P.PORTHOLE[0], -HW - 190, "porthole", 9)

dim_h(ax, P.CABIN_X0, P.HEADS_X[1], HW + 300,
      f"service {P.HEADS_X[1] - P.CABIN_X0}")
dim_h(ax, P.DINETTE_X[0], P.DINETTE_X[1], HW + 300,
      f"dinette {P.DINETTE_X[1] - P.DINETTE_X[0]}")
dim_h(ax, P.WARDROBE_X[0], P.WARDROBE_X[1], HW + 300,
      f"{P.WARDROBE_X[1] - P.WARDROBE_X[0]}")
dim_h(ax, P.BED_X[0], P.BED_X[1], HW + 300,
      f"sleeping {P.BED_X[1] - P.BED_X[0]}")
dim_h(ax, P.CABIN_X0, P.CABIN_X1, HW + 780, f"cabin {LEN}")
ax.annotate("", (P.CABIN_X0 - 300, -HW), (P.CABIN_X0 - 300, HW),
            arrowprops=dict(arrowstyle="<->", color=DIM, lw=1.1))
ax.text(P.CABIN_X0 - 380, 0, f"{2 * HW:.0f}", rotation=90, ha="center",
        va="center", color=DIM, fontsize=9.5, fontweight="bold")
ax.set_xlim(P.CABIN_X0 - 600, P.CABIN_X1 + 300)
ax.set_ylim(-HW - 420, HW + 1000)

# ================================================== 2. STOWAGE PLAN
ax2 = fig.add_axes([0.04, 0.30, 0.92, 0.27])
ax2.set_aspect("equal")
ax2.axis("off")
ax2.set_title("STOWAGE PLAN  —  what is hidden under and above it",
              loc="left", fontsize=14, fontweight="bold", color=HID)
shell(ax2, glazing=False)

hidden_items = [
    (P.BATT_BOX_X[0], P.BATT_BOX_X[1], -HW + 40, -HW + P.SETTEE_D - 40,
     HEAVY),
    (P.BATT_BOX_X[0], P.BATT_BOX_X[1], HW - P.SETTEE_D + 40, HW - 40,
     HEAVY),

    (P.ELEC_X[0], P.ELEC_X[1], -HW + 60, -HW + 500, APPL),
    (P.GALLEY_X[0] + 20, P.GALLEY_X[0] + 20 + P.WASHER_W,
     P.GALLEY_Y[0] + 40, P.GALLEY_Y[1] - 40, APPL),
    (P.GALLEY_X[0], P.FRIDGE_X[0], P.GALLEY_Y[1] - P.GAL_OH_DEPTH,
     P.GALLEY_Y[1], JOIN),
]
rect(ax2, P.TANK_BILGE_X[0], P.TANK_BILGE_X[1], -P.TANK_BILGE_HW,
     P.TANK_BILGE_HW, "#7fb0d0", hidden=True, z=2, alpha=0.35)
for x0, x1, y0, y1, fc in hidden_items:
    rect(ax2, x0, x1, y0, y1, fc, hidden=True, alpha=0.6)
for sy in (-1, 1):
    rect(ax2, P.BERTH_X[0] - 50, P.BERTH_X[1] + 50,
         min(sy * HW, sy * (HW - P.SHELF_DEPTH)),
         max(sy * HW, sy * (HW - P.SHELF_DEPTH)), JOIN, hidden=True,
         alpha=0.5)
    for i in range(3):
        x0 = P.BERTH_X[0] + 60 + i * 620
        ax2.plot([x0, x0 + 560], [sy * (HW - P.SETTEE_D)] * 2, color=INK,
                 lw=3, zorder=5)


def callout(ax, px, py, tx, ty, text, fs=9.5):
    ax.annotate(text, (px, py), (tx, ty), fontsize=fs, color=HID,
                fontweight="bold", ha="center", va="center",
                arrowprops=dict(arrowstyle="->", color=HID, lw=1.2),
                zorder=9)


callout(ax2, 1480, 900, 1250, 1500,
        "washer-dryer\nunder the worktop")
callout(ax2, 1600, 1080, 1900, 2080,
        f"locker band over the worktop\n{P.GAL_OH_Z[0]}–{P.GAL_OH_Z[1]}"
        " (750 tall)")
callout(ax2, 3600, 700, 3700, 1500,
        "BATTERIES — starboard half\n(the bank is split both sides)")
callout(ax2, 4500, -600, 5950, -1850,
        "inverter / charger\n+ MPPT + busbars\n(wardrobe base)")
callout(ax2, 3050, -800, 2450, -1350,
        f"BATTERIES  48 V LiFePO₄\n{P.BATT_KWH} kWh · {P.BATT_MASS:.0f} kg"
        "\nsplit under BOTH settees")
callout(ax2, 2600, -520, 3450, -1850,
        "3 drawers per side\nfacing the aisle")
callout(ax2, 4200, 1010, 5000, -1300,
        f"shelf bands {P.SHELF_Z[0]}–{P.SHELF_Z[1]}\nunder the windows")
callout(ax2, 2700, 200, 1250, -1750,
        f"FRESH WATER {P.WATER_L} L\nshallow BILGE tank under the sole\n"
        "— the lowest weight on board")
callout(ax2, 5300, 900, 5800, 2080,
        "bed hoist: 4 cables on ONE shaft\nunder the deckhead")
ax2.set_xlim(P.CABIN_X0 - 600, P.CABIN_X1 + 300)
ax2.set_ylim(-2300, 2300)

# ===================================================== 3. SECTIONS
def section(ax, title, items, note=None):
    ax.set_aspect("equal")
    ax.axis("off")
    ax.set_title(title, loc="left", fontsize=12, fontweight="bold",
                 color=INK)
    ax.add_patch(Rectangle((-HW, S), 2 * HW, C - S, fc="white", ec=INK,
                           lw=2.0))
    ax.add_patch(Rectangle((-HW, S - 20), 2 * HW, 20, fc="#c9ced4", ec=INK,
                           lw=0.8))
    for (y0, y1, z0, z1, text, fc, hid) in items:
        rect(ax, y0, y1, z0, z1, fc, hidden=hid, alpha=0.5 if hid else 1.0)
        lbl(ax, (y0 + y1) / 2, (z0 + z1) / 2, text, 8, hidden=hid)
    ax.annotate("", (-HW - 230, S), (-HW - 230, C),
                arrowprops=dict(arrowstyle="<->", color=DIM, lw=1.1))
    ax.text(-HW - 300, (S + C) / 2, f"{C - S} clear", rotation=90,
            ha="center", va="center", color=DIM, fontsize=9,
            fontweight="bold")
    if note:
        ax.text(0, S - 220, note, ha="center", fontsize=9, color="#2f7fbf")
    ax.set_xlim(-HW - 620, HW + 260)
    ax.set_ylim(S - 400, C + 160)


axA = fig.add_axes([0.035, 0.055, 0.30, 0.25])
section(axA, "A–A  galley / heads  (looking forward)", [
    (P.GALLEY_Y[0], HW, S, S + P.COUNTER_H, "washer-dryer", APPL, True),
    (P.GALLEY_Y[0] - 20, HW, S + P.COUNTER_H, S + P.COUNTER_H + 40, "", JOIN,
     False),
    (HW - P.GAL_OH_DEPTH, HW, P.GAL_OH_Z[0], P.GAL_OH_Z[1], "locker",
     JOIN, False),
    (-HW, P.HEADS_Y[1], S, C, "", WET, False),
    (-HW + 60, -HW + 560, S + 900, C - 200, "cabinet", JOIN, False),
], note="worktop 900 · 500 clear under the locker")
lbl(axA, (-HW + P.HEADS_Y[1]) / 2, S + 300, "HEADS\nwetroom", 9, bold=True)
axA.add_patch(Circle((HW, P.PORTHOLE[1]), 140, fc=GLASS, ec="#4b7c99",
                     lw=1.2, zorder=2))

axB = fig.add_axes([0.355, 0.055, 0.30, 0.25])
section(axB, "B–B  dinette  (looking forward)", [
    (-HW, -HW + P.SETTEE_D, S, S + P.SEAT_H, "BATTERIES", HEAVY, True),
    (HW - P.SETTEE_D, HW, S, S + P.SEAT_H, "WATER", HEAVY, True),
    (-HW, -HW + P.SETTEE_D, S + P.SEAT_H, S + P.SEAT_H + 110, "berth", SOFT,
     False),
    (HW - P.SETTEE_D, HW, S + P.SEAT_H, S + P.SEAT_H + 110, "berth", SOFT,
     False),
    (-P.TABLE_W / 2, P.TABLE_W / 2, P.TABLE_Z, P.TABLE_Z + 34, "table",
     "#f0e6cd", False),
    (-HW, -HW + P.SHELF_DEPTH, P.SHELF_Z[0], P.SHELF_Z[1], "shelf", JOIN,
     False),
    (HW - P.SHELF_DEPTH, HW, P.SHELF_Z[0], P.SHELF_Z[1], "shelf", JOIN,
     False),
], note="the window band 1500–2100 is kept clear on both sides")
for sy in (-1, 1):
    axB.add_patch(Rectangle((sy * HW - (46 if sy > 0 else 0), P.WIN_Z0), 46,
                            P.WIN_H, fc=GLASS, ec="#4b7c99", lw=1.2,
                            zorder=8))

axC = fig.add_axes([0.675, 0.055, 0.30, 0.25])
section(axC, "C–C  elevating bed  (looking forward)", [
    (-P.MATTRESS_L / 2, P.MATTRESS_L / 2, P.BED_DOWN_Z,
     P.BED_DOWN_Z + P.BED_FRAME_T + P.MATTRESS_T,
     f"bed made up — mattress {P.MATTRESS_L} across", SOFT, False),
    (-HW, -HW + P.SHELF_DEPTH, P.SHELF_Z[0], P.SHELF_Z[1], "", JOIN, False),
    (HW - P.SHELF_DEPTH, HW, P.SHELF_Z[0], P.SHELF_Z[1], "", JOIN, False),
], note=f"{P.CABIN_CEIL_Z - P.BED_DOWN_Z - P.BED_FRAME_T - P.MATTRESS_T} mm "
        f"over the mattress made up  ·  travel {P.BED_UP_Z - P.BED_DOWN_Z}")
# stowed position, dashed
axC.add_patch(Rectangle((-P.MATTRESS_L / 2, P.BED_UP_Z), P.MATTRESS_L,
                        P.BED_FRAME_T + P.MATTRESS_T, fc=SOFT, ec=HID,
                        ls=(0, (5, 3)), lw=1.6, alpha=0.45, zorder=4))
axC.text(0, P.BED_UP_Z + 110, "stowed at the deckhead", ha="center",
         va="center", fontsize=8, color=HID, fontweight="bold", zorder=6)
axC.annotate("", (P.MATTRESS_L / 2 - 200, P.BED_DOWN_Z),
             (P.MATTRESS_L / 2 - 200, P.BED_UP_Z),
             arrowprops=dict(arrowstyle="<->", color=DIM, lw=1.4))
axC.text(P.MATTRESS_L / 2 - 120, (P.BED_UP_Z + P.BED_DOWN_Z) / 2,
         f"lift {P.BED_UP_Z - P.BED_DOWN_Z}", rotation=90, ha="center",
         va="center", color=DIM, fontsize=9, fontweight="bold")
for rx in (-P.MATTRESS_L / 2 - 30, P.MATTRESS_L / 2 + 30):
    axC.add_patch(Rectangle((rx - 22, S), 44, C - S, fc="#5b6570", ec=INK,
                            lw=0.8, zorder=3))
axC.text(0, P.BED_DOWN_Z - 260,
         f"{P.BED_UP_Z - S} clear underneath when stowed", ha="center",
         fontsize=8.5, color=HID, fontweight="bold")
for sy in (-1, 1):
    axC.add_patch(Rectangle((sy * HW - (46 if sy > 0 else 0), P.WIN_Z0), 46,
                            P.WIN_H, fc=GLASS, ec="#4b7c99", lw=1.2,
                            zorder=8))

handles = [
    Line2D([0], [0], marker="s", ls="", ms=13, mfc=JOIN, mec=INK,
           label="joinery"),
    Line2D([0], [0], marker="s", ls="", ms=13, mfc=SOFT, mec=INK,
           label="berths / cushions"),
    Line2D([0], [0], marker="s", ls="", ms=13, mfc=APPL, mec=INK,
           label="appliances"),
    Line2D([0], [0], marker="s", ls="", ms=13, mfc=HEAVY, mec=HID,
           label=f"batteries {P.BATT_KWH} kWh / water — heavy, low"),
    Line2D([0], [0], marker="s", ls="", ms=13, mfc="white", mec=HID,
           label="hidden (dashed purple)"),
    Line2D([0], [0], marker="s", ls="", ms=13, mfc=GLASS, mec="#4b7c99",
           label="glazing"),
]
fig.legend(handles=handles, loc="lower center", ncol=6, frameon=False,
           fontsize=11, bbox_to_anchor=(0.5, 0.006))

fig.savefig(OUT, dpi=100, facecolor="white")
print("wrote", OUT)
