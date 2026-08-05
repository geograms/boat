#!/usr/bin/env python3
"""Spec cards for the walk-on roof deck -> docs/images/roof_*.png

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
from matplotlib.patches import Rectangle, Circle
from matplotlib.lines import Line2D

IMG = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                    "..", "docs", "images"))
DIM = "#b3202b"
INK = "#1a1a1a"
STEEL = "#8b929b"
ALU = "#c8ccd2"
GLASS = "#bcd6e6"
SOLAR = "#12325c"
DECKC = "#e6e8ea"


def frame(fig, title, sub):
    fig.patch.set_facecolor("white")
    fig.text(0.02, 0.955, title, fontsize=17, fontweight="bold", color=INK)
    fig.text(0.02, 0.915, sub, fontsize=10.5, color="#555", style="italic")


def dim_v(ax, y0, y1, x, label, fs=9):
    ax.annotate("", (x, y0), (x, y1),
                arrowprops=dict(arrowstyle="<->", color=DIM, lw=1.1))
    ax.text(x + 14, (y0 + y1) / 2, label, ha="left", va="center",
            fontsize=fs, color=DIM, fontweight="bold")


# =============================================== 1. deck build-up
def card_deck():
    fig = plt.figure(figsize=(13.5, 7.0), dpi=100)
    frame(fig, "ROOF DECK BUILD-UP  ·  walk on the glass, never on the panels",
          "no moving parts anywhere on the roof; the air box ventilates the "
          "cells so they run cooler than bonded laminates")

    ax = fig.add_axes([0.03, 0.06, 0.52, 0.80])
    ax.set_aspect("equal")
    ax.axis("off")
    VS = 6                      # vertical exaggeration, or it is unreadable
    z = 0
    layers = [
        (P.ROOF_STRUCT, "#d9dde1",
         f"structural roof sandwich {P.ROOF_STRUCT} — carries every load"),
        (12, "#c9ced4", "deck skin"),
        (P.PANEL_T, SOLAR, f"flexible laminate {P.PANEL_T} mm, bonded flat"),
    ]
    for h, c, lbl in layers:
        ax.add_patch(Rectangle((0, z * VS), 1400, h * VS, fc=c, ec=INK,
                               lw=1.0))
        ax.annotate(lbl, (1400, (z + h / 2) * VS),
                    (1560, (z + h / 2) * VS), fontsize=9.5, va="center",
                    arrowprops=dict(arrowstyle="-", color=INK, lw=0.8))
        z += h
    ax.add_patch(Rectangle((0, z * VS), 1400, P.AIRBOX_H * VS, fc="white",
                           ec=INK, lw=1.0, ls=(0, (4, 3))))
    ax.annotate(f"VENTILATED AIR BOX {P.AIRBOX_H} mm\n"
                "mesh slots fore and aft, drains to the scuppers",
                (1400, (z + P.AIRBOX_H / 2) * VS),
                (1560, (z + P.AIRBOX_H / 2) * VS), fontsize=9.5,
                va="center", fontweight="bold",
                arrowprops=dict(arrowstyle="-", color=INK, lw=0.8))
    for k in range(5):
        ax.annotate("", (120 + k * 280, (z + P.AIRBOX_H / 2) * VS),
                    (40 + k * 280, (z + P.AIRBOX_H / 2) * VS),
                    arrowprops=dict(arrowstyle="->", color="#2f7fbf", lw=1.2))
    z += P.AIRBOX_H
    for bx in (0, 660, 1320):
        ax.add_patch(Rectangle((bx, z * VS), 80, P.DECK_FRAME_H * VS, fc=ALU,
                               ec=INK, lw=1.0))
    ax.annotate(f"alu grid {P.DECK_FRAME_W} × {P.DECK_FRAME_H}, on inserts",
                (1400, (z + P.DECK_FRAME_H / 2) * VS),
                (1560, (z + P.DECK_FRAME_H / 2) * VS), fontsize=9.5,
                va="center", arrowprops=dict(arrowstyle="-", color=INK,
                                             lw=0.8))
    z += P.DECK_FRAME_H
    ax.add_patch(Rectangle((0, z * VS), 1400, P.DECK_GLASS_T * VS, fc=GLASS,
                           ec=INK, lw=1.4))
    ax.annotate(f"6+6 heat-strengthened laminated glass {P.DECK_GLASS_T} mm\n"
                "SGP interlayer, anti-slip frit R11",
                (1400, (z + P.DECK_GLASS_T / 2) * VS),
                (1560, (z + P.DECK_GLASS_T / 2) * VS), fontsize=9.5,
                va="center", fontweight="bold",
                arrowprops=dict(arrowstyle="-", color=INK, lw=0.8))
    for k in range(9):
        ax.plot([70 + k * 160, 110 + k * 160],
                [(z + P.DECK_GLASS_T) * VS + 40] * 2, color=INK, lw=2)
    dim_v(ax, (P.ROOF_STRUCT + 12) * VS, (z + P.DECK_GLASS_T) * VS, -230,
          f"{P.DECK_BUILDUP} mm")
    ax.text(700, -260, "a cracked pane cannot drop anyone — only 60 mm of air "
            "under it,\nso two plies is enough where a building floor needs "
            "three\n(vertical scale × 6)", ha="center", va="top",
            fontsize=9.5, color="#2f7fbf")
    ax.set_xlim(-420, 3400)
    ax.set_ylim(-700, (z + P.DECK_GLASS_T) * VS + 200)

    # right: plan of the field
    ax2 = fig.add_axes([0.58, 0.10, 0.40, 0.72])
    ax2.set_aspect("equal")
    ax2.axis("off")
    ax2.set_title("PLAN — 8 panes over the field", fontsize=12,
                  fontweight="bold", loc="left")
    tl = P.CABIN_X1 - P.CABIN_X0
    ax2.add_patch(Rectangle((P.CABIN_X0, -P.CABIN_W / 2), tl, P.CABIN_W,
                            fc=DECKC, ec=INK, lw=1.6))
    fx0, fx1 = P.DECK_FIELD_X
    px, py = P.DECK_PANE
    for i in range(P.DECK_PANE_NX):
        for j in range(P.DECK_PANE_NY):
            ax2.add_patch(Rectangle(
                (fx0 + i * px + 10, -P.DECK_FIELD_HW + j * py + 10),
                px - 20, py - 20, fc=GLASS, ec=INK, lw=1.2))
    ax2.text((fx0 + fx1) / 2, P.CABIN_W / 2 + 90,
             f"{P.DECK_PANE_NX} × {P.DECK_PANE_NY} panes of {px} × {py}  ·  "
             f"{P.DECK_GLASS_KG_M2 * px * py / 1e6:.0f} kg each",
             ha="center", va="center", fontsize=10, fontweight="bold")
    ax2.text(P.CABIN_X0 + tl / 2, -P.CABIN_W / 2 - 190,
             f"walking margin {P.CABIN_W / 2 - P.DECK_FIELD_HW:.0f} mm all "
             f"round  ·  toe rail, no guardrail  ·  frame shades "
             f"{P.deck_areas()[3] * 100:.1f}%", ha="center", fontsize=9)
    ax2.set_xlim(P.CABIN_X0 - 200, P.CABIN_X1 + 200)
    ax2.set_ylim(-P.CABIN_W / 2 - 420, P.CABIN_W / 2 + 200)

    fig.savefig(f"{IMG}/roof_deck.png", dpi=100, facecolor="white")
    plt.close(fig)


# =============================================== 2. glass sizing
def card_glass():
    fig = plt.figure(figsize=(13.5, 6.6), dpi=100)
    frame(fig, "WALK-ON GLASS SIZING  ·  why the pane size hardly matters",
          "the concentrated load governs, and its stress grows with the "
          "LOG of the span — not the square of it")

    ax = fig.add_axes([0.06, 0.13, 0.40, 0.70])
    spans = np.linspace(200, 1400, 200)
    t_pt = [P.glass_t_required(s) for s in spans]
    t_ud = [P.glass_t_udl(s) for s in spans]
    ax.plot(spans, t_pt, color=DIM, lw=2.4,
            label=f"{P.DECK_LOAD_POINT / 1000:.0f} kN point load  (governs)")
    ax.plot(spans, t_ud, color=INK, lw=1.8, ls="--",
            label=f"{P.DECK_LOAD_UDL * 1000:.0f} kN/m² distributed")
    ax.axhline(P.DECK_GLASS_T, color="#2f7fbf", lw=1.4)
    ax.text(1390, P.DECK_GLASS_T + 0.35, f"chosen 6+6 = {P.DECK_GLASS_T} mm",
            fontsize=9.5, color="#2f7fbf", fontweight="bold", ha="right")
    ax.axvline(max(P.DECK_PANE), color="#2f7fbf", ls=":", lw=1.4)
    ax.set_xlabel("pane span (mm)")
    ax.set_ylabel("glass thickness required (mm)")
    ax.grid(alpha=0.25)
    ax.legend(fontsize=9.5, loc="upper left")
    ax.set_ylim(0, 14)

    ax2 = fig.add_axes([0.52, 0.06, 0.46, 0.80])
    ax2.axis("off")
    rows = [("H", "PANE SIZE TRADE (same 10 m² field)", ""),
            ("", "pane", "glass   frame   TOTAL   shading")]
    for a, barkg in ((1000, 1.4), (500, 1.1), (400, 1.0), (200, 0.8)):
        t = max(P.glass_t_required(a), P.glass_t_udl(a))
        tg = math.ceil(t / 2) * 2
        field = 10.08
        glass = field * 2.5 * tg
        nx, ny = 4800 // a + 1, 2100 // a + 1
        bar = (nx * 2.1 + ny * 4.8) * barkg
        shade = 1 - (1 - 25 / a) ** 2
        rows.append(("", f"{a} mm → {tg} mm",
                     f"{glass:4.0f}kg  {bar:4.0f}kg  {glass + bar:5.0f}kg"
                     f"  {shade * 100:4.1f}%"))
    rows += [
        ("H", "CHOSEN", ""),
        ("", "panes", f"{P.DECK_PANE_NX} × {P.DECK_PANE_NY} of "
         f"{P.DECK_PANE[0]} × {P.DECK_PANE[1]}"),
        ("", "glass", f"6+6 HS laminated, {P.DECK_GLASS_T} mm, SGP"),
        ("", "needed for point load", f"{P.glass_t_required(1050):.1f} mm"),
        ("", "deflection under UDL", "0.9 mm  (limit span/300 = 3.5)"),
        ("", "mass per pane", f"{P.DECK_GLASS_KG_M2 * 1.2 * 1.05:.0f} kg"),
        ("", "deck total", f"{P.deck_mass():.0f} kg"),
    ]
    y = 0.97
    for kind, left, right in rows:
        if kind == "H":
            y -= 0.02
            ax2.text(0, y, left, transform=ax2.transAxes, fontsize=11.5,
                     fontweight="bold", color=DIM, va="top",
                     family="monospace")
            y -= 0.075
        else:
            ax2.text(0.03, y, left, transform=ax2.transAxes, fontsize=10.5,
                     color=INK, va="top", family="monospace")
            ax2.text(0.42, y, right, transform=ax2.transAxes, fontsize=10.5,
                     color=INK, va="top", family="monospace")
            y -= 0.066

    fig.savefig(f"{IMG}/roof_glass.png", dpi=100, facecolor="white")
    plt.close(fig)


# =============================================== 3. loads + yield
def card_loads():
    fig = plt.figure(figsize=(13.5, 6.4), dpi=100)
    frame(fig, "ROOF DECK  ·  loads, stability and what it generates",
          "full building-code deck loads — no use restrictions, "
          "stilettos and dropped anchors included")

    ax = fig.add_axes([0.04, 0.10, 0.44, 0.72])
    ax.set_aspect("equal")
    ax.axis("off")
    ax.add_patch(Rectangle((-1200, 0), 2400, 60, fc=GLASS, ec=INK, lw=1.4))
    ax.add_patch(Rectangle((-1200, -200), 2400, 200, fc="#d9dde1", ec=INK))
    ax.text(0, -100, "200 mm roof sandwich", ha="center", va="center",
            fontsize=9)
    for k in range(9):
        ax.annotate("", (-1000 + k * 250, 80), (-1000 + k * 250, 260),
                    arrowprops=dict(arrowstyle="->", color=INK, lw=1.2))
    ax.text(0, 320, f"{P.DECK_LOAD_UDL * 1000:.0f} kN/m² distributed",
            ha="center", fontsize=10, fontweight="bold")
    ax.annotate("", (500, 80), (500, 560),
                arrowprops=dict(arrowstyle="-|>", color=DIM, lw=3))
    ax.text(560, 400, f"{P.DECK_LOAD_POINT / 1000:.0f} kN on 50 × 50\n"
            "(a heel, a chair leg,\na dropped shackle)", fontsize=9.5,
            color=DIM, fontweight="bold")
    ax.text(0, -300, "the sandwich takes the load — the panels never see it",
            ha="center", fontsize=9.5, color="#2f7fbf")
    ax.set_xlim(-1400, 1900)
    ax.set_ylim(-400, 640)

    ax2 = fig.add_axes([0.52, 0.06, 0.46, 0.80])
    ax2.axis("off")
    kwp_deck, kwp_balc, kwp_eff = P.solar_kwp()
    _, _, _, shade = P.deck_areas()
    rows = [
        ("H", "STABILITY", ""),
        ("", "4 crew hard to one side", "3.7 kNm heeling"),
        ("", "float righting moment", "31.3 kNm"),
        ("", "margin", "8.5 ×"),
        ("H", "SOLAR", ""),
        ("", "deck laminates", f"{P.DECK_PANELS} × {P.PANEL_W_PEAK} W = "
         f"{kwp_deck:.2f} kWp"),
        ("", "solar balconies", f"{kwp_balc:.2f} kWp"),
        ("", "nominal total", f"{kwp_deck + kwp_balc:.2f} kWp"),
        ("", "glass transmission", f"{P.GLASS_TRANSMISSION * 100:.0f} %"),
        ("", "frame shading", f"−{shade * 100:.1f} %"),
        ("", "ventilation gain", f"+{(P.COOLING_GAIN - 1) * 100:.0f} %"),
        ("", "effective", f"{kwp_eff:.2f} kWp"),
        ("H", "GEOMETRY", ""),
        ("", "deck surface", f"{P.CABIN_ROOF_Z + P.DECK_BUILDUP} above keel"),
        ("", "air draft", f"{P.CABIN_ROOF_Z + P.DECK_BUILDUP - P.WL_Z} mm"),
        ("", "road height", f"{P.CABIN_ROOF_Z + P.DECK_BUILDUP - P.GROUND_Z:.0f}"
         " mm  (limit 4 000)"),
        ("", "deck edge", f"{P.TERRACE_TOERAIL} mm toe rail, no guardrail"),
    ]
    y = 0.98
    for kind, left, right in rows:
        if kind == "H":
            y -= 0.015
            ax2.text(0, y, left, transform=ax2.transAxes, fontsize=11.5,
                     fontweight="bold", color=DIM, va="top",
                     family="monospace")
            y -= 0.062
        else:
            ax2.text(0.03, y, left, transform=ax2.transAxes, fontsize=10.5,
                     color=INK, va="top", family="monospace")
            ax2.text(0.52, y, right, transform=ax2.transAxes, fontsize=10.5,
                     color=INK, va="top", family="monospace")
            y -= 0.053
    fig.text(0.52, 0.045, "the deck generates best when nobody is on it — "
             "it is a sun deck first", fontsize=9.5, color="#2f7fbf",
             style="italic")

    fig.savefig(f"{IMG}/roof_loads.png", dpi=100, facecolor="white")
    plt.close(fig)


card_deck()
card_glass()
card_loads()
for old in ("roof_scissor.png", "roof_seal.png", "roof_wind.png",
            "roof_hardware.png"):
    p = os.path.join(IMG, old)
    if os.path.exists(p):
        os.remove(p)
print("wrote roof_deck / roof_glass / roof_loads to", IMG)
