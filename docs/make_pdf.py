#!/usr/bin/env python3
"""Render README.md (and every image it references) to docs/boat-home.pdf

A small markdown renderer on matplotlib: headings, paragraphs, bullets,
pipe tables, code blocks and images. Keeping the PDF generated from the
README means the two cannot drift.

Run: python3 docs/make_pdf.py
"""
import os
import re
import sys
import textwrap

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from matplotlib.backends.backend_pdf import PdfPages

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "docs", "boat-home.pdf")

PW, PH = 8.27, 11.69                 # A4 portrait, inches
ML, MR, MT, MB = 0.78, 0.68, 0.85, 0.75
INK, MUTED, ACCENT = "#1a1a1a", "#5a5a5a", "#b3202b"
RULE = "#c9ced4"

FS_BODY, FS_H1, FS_H2, FS_H3 = 9.2, 20, 14, 11
LEAD = 0.150                          # inch per body line


def strip_md(s):
    s = re.sub(r"!\[[^\]]*\]\([^)]*\)", "", s)
    s = re.sub(r"\[([^\]]*)\]\([^)]*\)", r"\1", s)
    s = s.replace("**", "").replace("`", "")
    s = re.sub(r"(?<!\w)\*(?!\s)(.+?)(?<!\s)\*(?!\w)", r"\1", s)
    return s.strip()


class Doc:
    def __init__(self, pdf):
        self.pdf = pdf
        self.page = None
        self.y = 0
        self.n = 0

    def new_page(self):
        if self.page is not None:
            self.footer()
            self.pdf.savefig(self.page)
            plt.close(self.page)
        self.page = plt.figure(figsize=(PW, PH))
        self.page.patch.set_facecolor("white")
        self.y = PH - MT
        self.n += 1

    def footer(self):
        self.page.text(0.5, MB * 0.55 / PH, f"{self.n}", ha="center",
                       fontsize=8, color=MUTED)
        self.page.text(ML / PW, MB * 0.55 / PH, "Boat-Home — design study",
                       fontsize=7.5, color=MUTED)

    def space(self, inches):
        self.y -= inches
        if self.y < MB:
            self.new_page()

    def need(self, inches):
        if self.y - inches < MB:
            self.new_page()

    def text(self, s, fs=FS_BODY, color=INK, weight="normal", indent=0.0,
             lead=LEAD, wrap=95):
        for line in textwrap.wrap(s, wrap) or [""]:
            self.need(lead)
            self.page.text((ML + indent) / PW, self.y / PH, line, fontsize=fs,
                           color=color, fontweight=weight, va="top",
                           family="DejaVu Sans")
            self.y -= lead

    def heading(self, level, s):
        if level == 1:
            if self.y < PH - MT - 0.01:      # current page already used
                self.new_page()
            self.page.text(ML / PW, self.y / PH, s, fontsize=FS_H1,
                           color=INK, fontweight="bold", va="top")
            self.y -= 0.52
        elif level == 2:
            self.space(0.22)
            self.need(0.6)
            self.page.text(ML / PW, self.y / PH, s, fontsize=FS_H2,
                           color=ACCENT, fontweight="bold", va="top")
            self.y -= 0.26
            self.page.add_artist(plt.Line2D(
                [ML / PW, (PW - MR) / PW], [self.y / PH, self.y / PH],
                transform=self.page.transFigure, color=RULE, lw=0.9))
            self.y -= 0.16
        else:
            self.space(0.14)
            self.need(0.4)
            self.page.text(ML / PW, self.y / PH, s, fontsize=FS_H3,
                           color=INK, fontweight="bold", va="top")
            self.y -= 0.25

    def table(self, rows):
        if not rows:
            return
        ncol = max(len(r) for r in rows)
        rows = [r + [""] * (ncol - len(r)) for r in rows]
        avail = PW - ML - MR
        widths = []
        for c in range(ncol):
            w = max(len(rows[r][c]) for r in range(len(rows)))
            widths.append(max(w, 4))
        tot = sum(widths)
        widths = [avail * w / tot for w in widths]
        MINW = 0.95
        short = [i for i, w in enumerate(widths) if w < MINW]
        if short and len(short) < ncol:
            deficit = sum(MINW - widths[i] for i in short)
            spare = sum(widths[i] - MINW for i in range(ncol)
                        if i not in short)
            for i in range(ncol):
                widths[i] = (MINW if i in short
                             else widths[i] - deficit * (widths[i] - MINW) /
                             max(spare, 1e-6))
        wrapped = []
        for r in rows:
            cells = [textwrap.wrap(r[c],
                                   max(int((widths[c] - 0.16) / 0.053), 6))
                     or [""] for c in range(ncol)]
            wrapped.append((cells, max(len(c) for c in cells)))
        self.space(0.06)
        for i, (cells, hgt) in enumerate(wrapped):
            rh = hgt * 0.135 + 0.055
            self.need(rh + 0.1)
            if i == 0:
                self.page.add_artist(plt.Rectangle(
                    (ML / PW, (self.y - rh + 0.03) / PH), avail / PW, rh / PH,
                    transform=self.page.transFigure, fc="#eef1f4", ec="none"))
            x = ML
            for c in range(ncol):
                for k, ln in enumerate(cells[c]):
                    self.page.text((x + 0.05) / PW,
                                   (self.y - k * 0.135) / PH, ln,
                                   fontsize=8.1, va="top", color=INK,
                                   fontweight="bold" if i == 0 else "normal")
                x += widths[c]
            self.y -= rh
            self.page.add_artist(plt.Line2D(
                [ML / PW, (PW - MR) / PW], [(self.y + 0.02) / PH] * 2,
                transform=self.page.transFigure, color=RULE, lw=0.5))
        self.space(0.12)

    def image(self, path, caption=""):
        full = os.path.join(ROOT, path)
        if not os.path.exists(full):
            return
        img = mpimg.imread(full)
        h, w = img.shape[0], img.shape[1]
        avail_w = PW - ML - MR
        # trim uniform white margins so the drawing fills the page
        disp_w = avail_w
        disp_h = disp_w * h / w
        max_h = PH - MT - MB - 0.5
        if disp_h > max_h:
            disp_h = max_h
            disp_w = disp_h * w / h
        self.need(disp_h + 0.42)
        ax = self.page.add_axes([(ML + (avail_w - disp_w) / 2) / PW,
                                 (self.y - disp_h) / PH,
                                 disp_w / PW, disp_h / PH])
        ax.imshow(img)
        ax.axis("off")
        self.y -= disp_h + 0.06
        if caption:
            self.page.text(0.5, self.y / PH, caption, fontsize=8,
                           color=MUTED, ha="center", va="top", style="italic")
            self.y -= 0.20
        self.space(0.10)

    def close(self):
        self.footer()
        self.pdf.savefig(self.page)
        plt.close(self.page)


def title_page(pdf):
    fig = plt.figure(figsize=(PW, PH))
    fig.patch.set_facecolor("white")
    fig.text(0.5, 0.80, "BOAT-HOME", ha="center", fontsize=40,
             fontweight="bold", color=INK)
    fig.text(0.5, 0.755, "Road-Towable Solar Trimaran", ha="center",
             fontsize=15, color=ACCENT)
    fig.text(0.5, 0.727, "design study  ·  2026", ha="center", fontsize=10,
             color=MUTED)
    hero = os.path.join(ROOT, "freecad/shots/cruise_iso.png")
    if os.path.exists(hero):
        img = mpimg.imread(hero)
        ax = fig.add_axes([0.06, 0.36, 0.88, 0.34])
        ax.imshow(img)
        ax.axis("off")
    lines = ["7.2 m  ·  2.5 m beam  ·  2 535 mm on the road",
             "4.40 kWp solar  ·  50 kWh battery  ·  4.8 kn maximum",
             "5 berths  ·  1 850 mm headroom  ·  12.1 m² floor",
             "its own trailer: six driven wheels inside the floats"]
    for i, ln in enumerate(lines):
        fig.text(0.5, 0.30 - i * 0.033, ln, ha="center", fontsize=10.5,
                 color=INK)
    fig.text(0.5, 0.10, "generated from README.md — python3 docs/make_pdf.py",
             ha="center", fontsize=8, color=MUTED, style="italic")
    pdf.savefig(fig)
    plt.close(fig)


def render(md, pdf):
    doc = Doc(pdf)
    doc.new_page()
    lines = md.split("\n")
    i, in_code, code, table = 0, False, [], []

    def flush_table():
        nonlocal table
        if table:
            doc.table(table)
            table = []

    while i < len(lines):
        ln = lines[i]
        raw = ln.rstrip()

        if raw.startswith("```"):
            if in_code:
                doc.space(0.05)
                for c in code:
                    doc.need(0.135)
                    doc.page.text((ML + 0.12) / PW, doc.y / PH, c,
                                  fontsize=7.8, family="DejaVu Sans Mono",
                                  color="#24404f", va="top")
                    doc.y -= 0.135
                doc.space(0.12)
                code, in_code = [], False
            else:
                flush_table()
                in_code = True
            i += 1
            continue
        if in_code:
            code.append(raw)
            i += 1
            continue

        m = re.match(r"^!\[([^\]]*)\]\(([^)]+)\)", raw)
        if m:
            flush_table()
            doc.image(m.group(2), m.group(1))
            i += 1
            continue

        if raw.startswith("|"):
            cells = [strip_md(c) for c in raw.strip("|").split("|")]
            if not all(set(c) <= set("-: ") for c in cells):
                table.append(cells)
            i += 1
            continue
        flush_table()

        if raw.startswith("### "):
            doc.heading(3, strip_md(raw[4:]))
        elif raw.startswith("## "):
            doc.heading(2, strip_md(raw[3:]))
        elif raw.startswith("# "):
            doc.heading(1, strip_md(raw[2:]))
        elif raw.strip() in ("---", "***"):
            doc.space(0.08)
        elif re.match(r"^\s*[-*]\s+", raw):
            doc.text("•  " + strip_md(re.sub(r"^\s*[-*]\s+", "", raw)),
                     indent=0.16, wrap=88)
        elif re.match(r"^\s*\d+\.\s+", raw):
            doc.text(strip_md(raw.strip()), indent=0.16, wrap=88)
        elif raw.strip() == "":
            doc.space(0.09)
        else:
            doc.text(strip_md(raw))
        i += 1

    flush_table()
    doc.close()


def gallery(pdf):
    """Every render and drawing, one per page, after the text."""
    shots = []
    for mode, label in (("cruise", "cruise — trimaran, floats out"),
                        ("road", "road — folded, towed stern-first"),
                        ("harbor", "harbour — jack-up stance"),
                        ("launch", "launch — on the slipway"),
                        ("anchor", "anchor")):
        for v, vlabel in (("bow_quarter", "bow quarter"),
                          ("stern_quarter", "stern quarter"),
                          ("beam", "beam on"),
                          ("drone", "from above"),
                          ("low", "low, from the water")):
            shots.append((f"freecad/shots/beauty/{mode}_{v}.png",
                          f"{label} — {vlabel}"))
    # drawings only after them: no orthographic renders, they read as
    # cutaways rather than as a boat seen from outside
    shots += [
        ("docs/images/general_arrangement.png", "general arrangement"),
        ("docs/images/interior_plan.png", "interior layout sheet"),
        ("docs/images/roof_deck.png", "roof deck build-up"),
        ("docs/images/roof_glass.png", "walk-on glass sizing"),
        ("docs/images/roof_loads.png", "roof deck loads and yield"),
        ("docs/images/tire_205_70_r15_at.png", "wheel spec card"),
        ("docs/images/orbital_motor_omr200.png", "hub motor spec card"),
        ("docs/images/bldc_48v_3kw.png", "drive motor spec card"),
        ("docs/images/gear_pump_group2.png", "gear pump spec card"),
        ("docs/images/hub_assembly_section.png", "hub assembly"),
        ("docs/images/wetmate_connector.png", "wet-mate connector"),
        ("docs/images/rim_thruster.png", "rim thruster"),
        ("docs/images/weed_grille.png", "weed grille"),
    ]
    fig = plt.figure(figsize=(PW, PH))
    fig.patch.set_facecolor("white")
    fig.text(0.5, 0.55, "DRAWINGS AND RENDERS", ha="center", fontsize=22,
             fontweight="bold", color=INK)
    fig.text(0.5, 0.50, f"{len(shots)} plates", ha="center", fontsize=11,
             color=MUTED)
    pdf.savefig(fig)
    plt.close(fig)

    for path, cap in shots:
        full = os.path.join(ROOT, path)
        if not os.path.exists(full):
            continue
        img = mpimg.imread(full)
        h, w = img.shape[0], img.shape[1]
        land = w > h
        fig = plt.figure(figsize=(PH, PW) if land else (PW, PH))
        fig.patch.set_facecolor("white")
        fw, fh = (PH, PW) if land else (PW, PH)
        ax = fig.add_axes([0.04, 0.075, 0.92, 0.86])
        ax.imshow(img)
        ax.axis("off")
        fig.text(0.5, 0.035, cap, ha="center", fontsize=10, color=INK)
        pdf.savefig(fig)
        plt.close(fig)


if __name__ == "__main__":
    md = open(os.path.join(ROOT, "README.md")).read()
    with PdfPages(OUT) as pdf:
        title_page(pdf)
        render(md, pdf)
        gallery(pdf)
        d = pdf.infodict()
        d["Title"] = "Boat-Home — Road-Towable Solar Trimaran"
        d["Subject"] = "Design study"
    print("wrote", OUT)
