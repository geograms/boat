#!/usr/bin/env python3
"""Spec cards for the pop-top roof -> docs/images/roof_*.png

Every number comes from params.py. Run: python3 freecad/roof_cards.py
"""
import os
import sys
import math

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import params as P

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Rectangle, Circle, Polygon, FancyArrow

IMG = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                    "..", "docs", "images"))
DIM = "#b3202b"
INK = "#1a1a1a"
STEEL = "#8b929b"
ALU = "#c8ccd2"
GASKET = "#3a3a3a"
SOLAR = "#12325c"


def frame(fig, title, sub):
    fig.patch.set_facecolor("white")
    fig.text(0.02, 0.965, title, fontsize=17, fontweight="bold", color=INK)
    fig.text(0.02, 0.928, sub, fontsize=10.5, color="#555", style="italic")


def dim_h(ax, x0, x1, y, label, fs=9):
    ax.annotate("", (x0, y), (x1, y),
                arrowprops=dict(arrowstyle="<->", color=DIM, lw=1.1))
    ax.text((x0 + x1) / 2, y, label, ha="center", va="bottom", fontsize=fs,
            color=DIM, fontweight="bold")


def dim_v(ax, y0, y1, x, label, fs=9):
    ax.annotate("", (x, y0), (x, y1),
                arrowprops=dict(arrowstyle="<->", color=DIM, lw=1.1))
    ax.text(x, (y0 + y1) / 2, label, ha="center", va="center", rotation=90,
            fontsize=fs, color=DIM, fontweight="bold")


# =====================================================  1. scissor unit
def card_scissor():
    fig = plt.figure(figsize=(13.5, 7.6), dpi=100)
    frame(fig, "POP-TOP SCISSOR UNIT  ·  4 off, one per terrace corner",
          "single stage, arms pinned at mid-length — half the joints of a "
          "double scissor, and every joint is a corrosion site")

    ax = fig.add_axes([0.03, 0.07, 0.52, 0.80])
    ax.set_aspect("equal")
    ax.axis("off")
    L = P.SCISSOR_ARM

    for lift, col, lw, lbl in ((P.CANOPY_LIFT, INK, 2.2, "raised"),
                               (0, "#9aa2ab", 1.6, "stowed")):
        th, span, travel, push = P.scissor_geom(lift)
        t = math.radians(th)
        h = L * math.sin(t)
        x0, x1 = -span / 2, span / 2
        ax.plot([x0, x1], [0, h], color=col, lw=lw,
                solid_capstyle="round")
        ax.plot([x1, x0], [0, h], color=col, lw=lw,
                solid_capstyle="round")
        ax.plot([x0 - 150, x1 + 150], [h, h], color=col, lw=lw + 1.6)
        if lift:
            ax.plot(0, h / 2, "o", ms=9, mfc="white", mec=col, mew=2)
            for (px, pz) in ((x0, 0), (x1, 0), (x0, h), (x1, h)):
                ax.plot(px, pz, "o", ms=7, color=col)
            ax.text(0, h / 2 + 90, "centre pin", ha="center", fontsize=8.5)
            dim_v(ax, 0, h, x1 + 420, f"lift {P.CANOPY_LIFT}")
            dim_h(ax, x0, x1, -190, f"span {span:.0f}")
            ax.text(0, h + 130, f"canopy  {P.CANOPY_MASS} kg", ha="center",
                    fontsize=9.5, fontweight="bold")
            ax.annotate(f"{th:.1f}°", (x0 + 210, 60), fontsize=10,
                        color=DIM, fontweight="bold")

    # deck, well and channel
    ax.add_patch(Rectangle((-L / 2 - 260, -P.SCISSOR_WELL), L + 520,
                           P.SCISSOR_WELL, fc="#e6e8ea", ec=INK, lw=1.0))
    ax.text(-L / 2 - 240, -P.SCISSOR_WELL - 480,
            f"recessed well {P.SCISSOR_WELL} + lid cavity {P.CANOPY_THICK} "
            f"= {P.SCISSOR_WELL + P.CANOPY_THICK} mm  ·  stows in 202",
            fontsize=9, color=INK)
    th0, span0, _, _ = P.scissor_geom(0)
    _, span_up, travel, _ = P.scissor_geom(P.CANOPY_LIFT)
    ax.annotate("", (span0 / 2, -290), (span_up / 2, -290),
                arrowprops=dict(arrowstyle="<->", color=DIM, lw=1.2))
    ax.text((span0 + span_up) / 4, -400, f"slider travel {travel:.0f}",
            ha="center", fontsize=9, color=DIM, fontweight="bold")
    ax.set_xlim(-L / 2 - 400, L / 2 + 750)
    ax.set_ylim(-780, P.CANOPY_LIFT + 400)

    # force curve
    ax2 = fig.add_axes([0.62, 0.13, 0.35, 0.68])
    hs = np.linspace(120, P.CANOPY_LIFT, 300)
    fs = [P.scissor_geom(h)[3] for h in hs]
    ax2.plot(hs, fs, color=DIM, lw=2.2)
    ax2.axhline(P.ACT_FORCE_N, color=INK, ls="--", lw=1.2)
    ax2.text(P.CANOPY_LIFT, P.ACT_FORCE_N + 150,
             f"actuator {P.ACT_FORCE_N} N", ha="right", fontsize=9.5,
             fontweight="bold")
    ax2.fill_between(hs, fs, color=DIM, alpha=0.08)
    ax2.set_xlabel("canopy height above the terrace (mm)")
    ax2.set_ylabel("push needed at the slider (N)")
    ax2.set_title("force is set by BREAKOUT, not by weight", fontsize=11,
                  fontweight="bold", loc="left")
    ax2.set_ylim(0, P.ACT_FORCE_N * 1.15)
    ax2.grid(alpha=0.25)
    b = P.scissor_geom(0)[3]
    ax2.annotate(f"{b:.0f} N near flat", (150, b), (500, b * 0.8),
                 arrowprops=dict(arrowstyle="->", color=INK), fontsize=9)
    ax2.annotate(f"{P.scissor_geom(P.CANOPY_LIFT)[3]:.0f} N at full height",
                 (P.CANOPY_LIFT, 90), (900, 900),
                 arrowprops=dict(arrowstyle="->", color=INK), fontsize=9)

    fig.savefig(f"{IMG}/roof_scissor.png", dpi=100, facecolor="white")
    plt.close(fig)


# =====================================================  2. sealing
def card_seal():
    fig = plt.figure(figsize=(13.5, 6.8), dpi=100)
    frame(fig, "CANOPY SEAL  ·  roof down = the mechanism is in a closed box",
          "coaming, bulb gasket and over-centre latches; the scissors only "
          "meet weather at anchor")

    # ---- left: section through the coaming, roof stowed (zoomed detail)
    ax = fig.add_axes([0.03, 0.06, 0.50, 0.79])
    ax.set_aspect("equal")
    ax.axis("off")
    ax.set_title("SECTION AT THE CANOPY EDGE  —  roof down and latched",
                 fontsize=12, fontweight="bold", loc="left", color=INK)
    zc = P.COAMING_H + P.GASKET_D            # canopy underside when shut

    ax.add_patch(Rectangle((-260, -P.ROOF_STRUCT), 680, P.ROOF_STRUCT,
                           fc="#e6e8ea", ec=INK, lw=1.1))
    ax.add_patch(Rectangle((-260, 0), 680, 12, fc="#c9ced4", ec=INK, lw=0.8))
    ax.add_patch(Rectangle((300, 0), 90, P.COAMING_H, fc=ALU, ec=INK, lw=1.1))
    ax.add_patch(Circle((345, P.COAMING_H + P.GASKET_D / 2), P.GASKET_D / 2,
                        fc=GASKET, ec=INK, lw=1.0))
    ax.add_patch(Rectangle((-260, zc), 700, P.CANOPY_THICK, fc="#f2f3f4",
                           ec=INK, lw=1.2))
    ax.add_patch(Rectangle((-250, zc + P.CANOPY_THICK), 660, 8, fc=SOLAR,
                           ec="none"))
    ax.add_patch(Rectangle((410, zc - P.CANOPY_SKIRT), 30,
                           P.CANOPY_SKIRT + P.CANOPY_THICK, fc="#f2f3f4",
                           ec=INK, lw=1.2))
    ax.add_patch(Rectangle((452, zc - 120), 24, 120, fc=STEEL, ec=INK))
    ax.add_patch(Rectangle((444, -8), 40, 40, fc=STEEL, ec=INK))

    lead = [
        (zc + P.CANOPY_THICK + 4, (60, zc + P.CANOPY_THICK + 4),
         "flexible laminate bonded to the canopy sandwich"),
        (zc + 60, (0, zc + 60), "canopy: crowned sandwich slab"),
        (P.COAMING_H + P.GASKET_D / 2, (352, P.COAMING_H + P.GASKET_D / 2),
         f"EPDM bulb gasket ⌀{P.GASKET_D} — the seal"),
        (P.COAMING_H / 2, (345, P.COAMING_H / 2),
         f"coaming {P.COAMING_H} high: the gasket line sits above "
         "any standing water"),
        (zc - 60, (428, zc - 60),
         f"skirt {P.CANOPY_SKIRT} drops 50 mm past the coaming — "
         "a labyrinth, not a butt joint"),
        (-70, (464, -70),
         f"{P.LATCH_N} over-centre draw latches clamp the gasket: "
         "THEY hold the roof down at sea, never the motors"),
        (-P.ROOF_STRUCT / 2, (100, -P.ROOF_STRUCT / 2),
         f"cabin roof — {P.ROOF_STRUCT} structural sandwich, "
         "the terrace floor; the living space is never opened"),
    ]
    tx = 620
    ys = [1050, 830, 610, 400, 190, -30, -250]
    for (yv, (px, py), txt), ty in zip(lead, ys):
        ax.annotate("", (px, py), (tx - 18, ty),
                    arrowprops=dict(arrowstyle="->", color=INK, lw=0.9))
        ax.text(tx, ty, txt, fontsize=9, va="center", wrap=True)
    ax.annotate("", (120, 14), (120, -250),
                arrowprops=dict(arrowstyle="->", color="#2f7fbf", lw=1.8))
    ax.text(120, -300, "scupper", fontsize=9, color="#2f7fbf", ha="center")
    ax.set_xlim(-320, 1780)
    ax.set_ylim(-380, 1180)

    # ---- right: plug-in bar and socket
    ax3 = fig.add_axes([0.58, 0.06, 0.40, 0.79])
    ax3.set_aspect("equal")
    ax3.axis("off")
    ax3.set_title("PLUG-IN BAR + SOCKET  —  roof up", fontsize=12,
                  fontweight="bold", loc="left", color=INK)
    ax3.add_patch(Rectangle((-300, -140), 900, 150, fc="#e6e8ea", ec=INK))
    ax3.text(-280, -65, "terrace deck", fontsize=9)
    ax3.add_patch(Rectangle((-60, -130), 120, 200, fc=ALU, ec=INK, lw=1.1))
    ax3.add_patch(Rectangle((-P.BAR_D / 2, -100), P.BAR_D, 1900, fc=STEEL,
                            ec=INK, lw=1.1))
    ax3.plot([-P.BAR_D / 2 - 24, P.BAR_D / 2 + 24], [50, 50], color=INK,
             lw=2.5)
    ax3.add_patch(Rectangle((-320, 1800), 920, 70, fc="#f2f3f4", ec=INK,
                            lw=1.2))
    ax3.text(-300, 1900, "canopy", fontsize=9)
    # framed solar wall in the bay
    ax3.add_patch(Rectangle((120, 260), 420, P.PANEL_W, fc=SOLAR,
                            alpha=0.22, ec=SOLAR, lw=1.6))
    ax3.text(330, 260 + P.PANEL_W / 2, "flexible laminate\non a 25 mm\n"
             "tube frame", ha="center", va="center", fontsize=9.5,
             color=SOLAR, fontweight="bold")
    ax3.annotate("spring ball lock:\ndrop in, twist, done", (0, 50),
                 (150, -40), fontsize=9,
                 arrowprops=dict(arrowstyle="->", color=INK))
    ax3.text(-300, 2050,
             f"⌀{P.BAR_D} × {P.BAR_T} anodized alu, {P.CANOPY_LIFT} long\n"
             f"{len(P.BAR_XS)} sockets per side → {P.SIDEPANEL_BAYS} bays\n"
             "the bars take uplift and racking and carry the lifelines;\n"
             "2 diagonal tie-rods per side brace the forward bays",
             fontsize=9.5, va="bottom")
    ax3.set_xlim(-360, 700)
    ax3.set_ylim(-260, 2400)

    fig.savefig(f"{IMG}/roof_seal.png", dpi=100, facecolor="white")
    plt.close(fig)


# =====================================================  3. wind
def card_wind():
    fig = plt.figure(figsize=(13.5, 6.4), dpi=100)
    frame(fig, "POP-TOP WIND LOADS  ·  what holds the roof, and when it "
          "comes down",
          "EN 1991-1-4 free-standing canopy, cp,net ±%.1f, canopy %.1f m²"
          % (P.CP_NET, (P.CABIN_X1 - P.CABIN_X0) * P.CABIN_W / 1e6))

    ax = fig.add_axes([0.06, 0.14, 0.42, 0.68])
    kn = np.linspace(0, 60, 200)
    tot = np.array([P.canopy_uplift_N(k) / 1000 for k in kn])
    ax.plot(kn, tot, color=DIM, lw=2.4, label="net uplift, whole canopy")
    ax.plot(kn, tot / 4, color=INK, lw=1.6, ls="--",
            label="per corner (4 units)")
    for v, txt, col, ty in ((P.WIND_PANEL_KN, "side walls off", "#2f7fbf",
                             0.95),
                            (P.WIND_DESIGN_KN, "roof down", "#e08a17", 0.76),
                            (P.WIND_SURVIVE_KN, "survival", DIM, 0.95)):
        ax.axvline(v, color=col, ls=":", lw=1.6)
        ax.text(v - 0.8, tot.max() * ty, f"{v} kn\n{txt}", fontsize=9,
                color=col, fontweight="bold", va="top", ha="right")
    ax.set_xlabel("wind speed (kn)")
    ax.set_ylabel("force (kN)")
    ax.grid(alpha=0.25)
    ax.legend(fontsize=9, loc="upper left")

    ax2 = fig.add_axes([0.53, 0.04, 0.45, 0.84])
    ax2.axis("off")
    rows = [
        ("H", "LOAD PATH", ""),
        ("", "canopy mass", f"{P.CANOPY_MASS} kg → "
         f"{P.CANOPY_MASS * 9.81 / 4:.0f} N per unit"),
        ("", f"uplift @ {P.WIND_DESIGN_KN} kn",
         f"{P.canopy_uplift_N(P.WIND_DESIGN_KN) / 1000:.1f} kN  "
         f"({P.canopy_uplift_N(P.WIND_DESIGN_KN) / 4:.0f} N/corner)"),
        ("", f"uplift @ {P.WIND_SURVIVE_KN} kn",
         f"{P.canopy_uplift_N(P.WIND_SURVIVE_KN) / 1000:.1f} kN  "
         f"({P.canopy_uplift_N(P.WIND_SURVIVE_KN) / 4:.0f} N/corner)"),
        ("", "carried by", "lock pins (up) / draw latches (down)"),
        ("", "NOT carried by", "the actuators — ever"),
        ("H", "OPERATING LIMITS", ""),
        ("", "raise the roof", "at anchor or alongside only"),
        ("", "never", "underway, or on the road"),
        ("", f"above {P.WIND_PANEL_KN} kn", "take the side walls off"),
        ("", f"above {P.WIND_DESIGN_KN} kn", "roof down and latched"),
        ("H", "RAISED GEOMETRY", ""),
        ("", "terrace headroom", f"{P.CANOPY_LIFT} mm"),
        ("", "air draft", f"{P.CABIN_ROOF_Z + P.CANOPY_LIFT + P.CANOPY_THICK - P.WL_Z} mm above WL"),
        ("", "raise time", f"{P.scissor_geom(P.CANOPY_LIFT)[2] / P.ACT_SPEED / 60:.1f} min"),
    ]
    y = 0.96
    for kind, left, right in rows:
        if kind == "H":
            y -= 0.02
            ax2.text(0, y, left, transform=ax2.transAxes, fontsize=11.5,
                     fontweight="bold", color=DIM, va="top",
                     family="monospace")
            y -= 0.070
        else:
            ax2.text(0.03, y, left, transform=ax2.transAxes, fontsize=10.5,
                     color=INK, va="top", family="monospace")
            ax2.text(0.42, y, right, transform=ax2.transAxes, fontsize=10.5,
                     color=INK, va="top", family="monospace")
            y -= 0.058

    fig.savefig(f"{IMG}/roof_wind.png", dpi=100, facecolor="white")
    plt.close(fig)


# =====================================================  4. hardware
def card_hardware():
    fig = plt.figure(figsize=(13.5, 6.2), dpi=100)
    frame(fig, "ROOF HARDWARE  ·  actuator and pin joint",
          "washdown-grade actuator; every pin runs in a composite bush — "
          "no metal on metal, no grease to wash out")

    ax = fig.add_axes([0.03, 0.10, 0.46, 0.72])
    ax.set_aspect("equal")
    ax.axis("off")
    ax.set_title("ELECTRIC LINEAR ACTUATOR  (4 off, encoder-synced)",
                 fontsize=12, fontweight="bold", loc="left")
    ax.add_patch(Rectangle((0, -38), 520, 76, fc=STEEL, ec=INK, lw=1.2))
    ax.add_patch(Rectangle((520, -20), 430, 40, fc=ALU, ec=INK, lw=1.2))
    ax.add_patch(Rectangle((500, -46), 46, 92, fc="#4a4f55", ec=INK))
    ax.add_patch(Circle((-40, 0), 40, fc=ALU, ec=INK, lw=1.2))
    ax.add_patch(Circle((-40, 0), 16, fc="white", ec=INK))
    ax.add_patch(Circle((990, 0), 40, fc=ALU, ec=INK, lw=1.2))
    ax.add_patch(Circle((990, 0), 16, fc="white", ec=INK))
    ax.text(260, 0, "IP69K, 24 V", ha="center", va="center", fontsize=10,
            color="white", fontweight="bold")
    ax.text(523, 70, "neoprene boot over the rod seal", fontsize=8.5)
    dim_h(ax, 546, 950, -110, f"stroke {P.ACT_STROKE}")
    ax.text(0, -230, f"force {P.ACT_FORCE_N} N  ·  speed {P.ACT_SPEED} mm/s  "
            f"·  stainless tube  ·  Hall encoder\n"
            f"mounted rod-down-aft so the seal never sits in a puddle  ·  "
            f"breakout demand {P.scissor_geom(0)[3]:.0f} N",
            fontsize=9.5, va="top")
    ax.set_xlim(-140, 1120)
    ax.set_ylim(-330, 200)

    ax2 = fig.add_axes([0.55, 0.10, 0.42, 0.72])
    ax2.set_aspect("equal")
    ax2.axis("off")
    ax2.set_title("PIN JOINT  (14 per unit)", fontsize=12,
                  fontweight="bold", loc="left")
    ax2.add_patch(Rectangle((-260, -22), 240, 44, fc=ALU, ec=INK, lw=1.2))
    ax2.add_patch(Rectangle((20, -22), 240, 44, fc=ALU, ec=INK, lw=1.2))
    ax2.add_patch(Circle((0, 0), 62, fc="#f0c674", ec=INK, lw=1.2))
    ax2.add_patch(Circle((0, 0), 40, fc=STEEL, ec=INK, lw=1.2))
    ax2.annotate("316 shoulder bolt", (0, 0), (150, 170),
                 arrowprops=dict(arrowstyle="->", color=INK), fontsize=9.5)
    ax2.annotate("PTFE-lined composite bush\n(igus / Vesconite)", (52, 32),
                 (110, -190), arrowprops=dict(arrowstyle="->", color=INK),
                 fontsize=9.5)
    ax2.annotate("hard-anodized 6082-T6 arm", (-180, 22), (-330, 150),
                 arrowprops=dict(arrowstyle="->", color=INK), fontsize=9.5)
    ax2.text(-340, -250, "Tef-Gel at every stainless-in-aluminium "
             "interface.\nSingle-stage scissors on purpose: half the joints\n"
             "of a double scissor to inspect and rinse.", fontsize=9.5,
             va="top")
    ax2.set_xlim(-380, 420)
    ax2.set_ylim(-330, 240)

    fig.savefig(f"{IMG}/roof_hardware.png", dpi=100, facecolor="white")
    plt.close(fig)


card_scissor()
card_seal()
card_wind()
card_hardware()
print("wrote roof_scissor / roof_seal / roof_wind / roof_hardware to", IMG)
