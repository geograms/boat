#!/usr/bin/env python3
"""Render README.md (and every image it references) to docs/boat-home.pdf

A small markdown renderer on matplotlib: headings, paragraphs, bullets,
pipe tables, code blocks and images. Keeping the PDF generated from the
README means the two cannot drift.

Run: python3 docs/make_pdf.py
"""
import datetime
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

PROJECT = "BOAT-HOME — road-towable solar trimaran"
REV = "Rev. A"
AUTHOR = "Max Brito"
EMAIL = "maxbrito@pm.me"
TODAY = datetime.date.today()
YEAR = TODAY.year
DATE = TODAY.strftime("%d %B %Y")
COPYRIGHT = f"© {YEAR} {AUTHOR}"


def strip_md(s):
    s = re.sub(r"!\[[^\]]*\]\([^)]*\)", "", s)
    s = re.sub(r"\[([^\]]*)\]\([^)]*\)", r"\1", s)
    s = s.replace("**", "").replace("`", "")
    s = re.sub(r"(?<!\w)\*(?!\s)(.+?)(?<!\s)\*(?!\w)", r"\1", s)
    return s.strip()


class Doc:
    def __init__(self, pdf, toc=None, start_page=1):
        self.pdf = pdf
        self.page = None
        self.y = 0
        self.n = start_page - 1
        self.part = ""            # running header, set per document
        self.toc = toc            # [(level, title, page)] collected in pass 1
        self.total = None         # filled in on pass 2 for "x / y"

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
        num = f"{self.n}" if self.total is None else f"{self.n} / {self.total}"
        self.page.text(0.5, MB * 0.55 / PH, num, ha="center",
                       fontsize=8, color=MUTED)
        self.page.text(ML / PW, MB * 0.55 / PH, PROJECT,
                       fontsize=7.5, color=MUTED)
        self.page.text(1 - MR / PW, MB * 0.55 / PH, COPYRIGHT,
                       fontsize=7.5, color=MUTED, ha="right")
        # running header: which part of the package you are in
        if self.part:
            self.page.text(ML / PW, (PH - MT * 0.42) / PH, self.part.upper(),
                           fontsize=7.5, color=MUTED, va="center")
            self.page.text(1 - MR / PW, (PH - MT * 0.42) / PH, REV,
                           fontsize=7.5, color=MUTED, va="center", ha="right")
            self.page.add_artist(plt.Line2D(
                [ML / PW, (PW - MR) / PW],
                [(PH - MT * 0.62) / PH] * 2, transform=self.page.transFigure,
                color=RULE, lw=0.6))

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
        elif level == 2:
            self.need(1.1)                   # never orphan a section head
        if self.toc is not None and level <= 2:
            self.toc.append((level, s, self.n))
        if level == 1:
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
            # clamp: one long prose column must not starve the numbers
            widths.append(min(max(w, 5), 34))
        tot = sum(widths)
        widths = [avail * w / tot for w in widths]
        MINW = min(0.95, avail / ncol * 0.85)
        short = [i for i, w in enumerate(widths) if w < MINW]
        if short and len(short) < ncol:
            deficit = sum(MINW - widths[i] for i in short)
            spare = sum(widths[i] - MINW for i in range(ncol)
                        if i not in short)
            for i in range(ncol):
                widths[i] = (MINW if i in short
                             else widths[i] - deficit * (widths[i] - MINW) /
                             max(spare, 1e-6))
        fs = 8.1 if ncol <= 5 else (7.4 if ncol <= 7 else 6.8)
        cw = 0.061 * fs / 8.1
        wrapped = []
        for r in rows:
            cells = [textwrap.wrap(r[c], max(int((widths[c] - 0.12) / cw), 6))
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
                                   fontsize=fs, va="top", color=INK,
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

    def end_document(self):
        """Flush the current page; the Doc stays alive for the next one."""
        if self.page is not None:
            self.footer()
            self.pdf.savefig(self.page)
            plt.close(self.page)
            self.page = None

    def divider(self, number, title, subtitle=""):
        """Full-page part divider, counted in the page numbering."""
        self.end_document()
        self.page = plt.figure(figsize=(PW, PH))
        self.page.patch.set_facecolor("white")
        self.n += 1
        self.page.text(0.13, 0.60, number, fontsize=64, color="#e4e7ea",
                       fontweight="bold", va="center")
        self.page.text(0.13, 0.50, title.upper(), fontsize=23,
                       fontweight="bold", color=INK, va="center")
        if subtitle:
            self.page.text(0.13, 0.445, subtitle, fontsize=11, color=MUTED,
                           va="center")
        self.page.add_artist(plt.Line2D([0.13, 0.60], [0.415, 0.415],
                                        transform=self.page.transFigure,
                                        color=ACCENT, lw=2.0))
        self.y = 0
        self.end_document()


PR_DIR = "docs/photo-realistic"
PHOTOREAL = [
    ("docs/photo-realistic/ChatGPT Image Aug 5, 2026, 12_10_01 PM (2).png",
     "At anchor",
     "The sky dome forward is a room, not a windscreen: no wall between "
     "it and the saloon, the sole runs straight through, 2 050 mm of "
     "headroom under 4 m² of glass."),
    ("docs/photo-realistic/ChatGPT Image Aug 5, 2026, 12_10_01 PM (3).png",
     "Under way on sunlight",
     "Three flush waterjets, no rudder, no propeller to foul. On a "
     "summer day the roof makes more than the boat spends at 4.2 knots."),
    ("docs/photo-realistic/ChatGPT Image Aug 5, 2026, 12_10_01 PM (1).png",
     "The same boat, Tuesday morning",
     "The floats fold under the hull and carry six driven wheels: "
     "2 535 mm wide behind a Viano-class car. No crane, no yard, no "
     "trailer to store."),
]


def photoreal(pdf, doc=None):
    """Marketing plates at the front — what the thing is, before the
    engineering explains how."""
    plates = [(p, t, s) for p, t, s in PHOTOREAL
              if os.path.exists(os.path.join(ROOT, p))]
    if not plates:
        return
    if doc is not None:
        doc.n += 1 + len(plates)
    fig = plt.figure(figsize=(PW, PH))
    fig.patch.set_facecolor("white")
    fig.text(0.5, 0.62, "A HOUSE THAT SWIMS", ha="center", fontsize=26,
             fontweight="bold", color=INK)
    fig.text(0.5, 0.575, "and drives itself to the water", ha="center",
             fontsize=13, color=ACCENT)
    for i, ln in enumerate([
            "Seven metres of Dutch barge with a glass dome on the bow, a",
            "solar roof you can walk on, and its own trailer folded",
            "underneath. One car tows it; it launches itself.",
            "",
            "The pictures on the next three pages are impressions.",
            "Everything after them is measured."]):
        fig.text(0.5, 0.49 - i * 0.030, ln, ha="center", fontsize=10.5,
                 color=INK if i < 3 else MUTED,
                 style="normal" if i < 3 else "italic")
    fig.text(0.5, 0.08, f"{COPYRIGHT}  ·  {EMAIL}", ha="center", fontsize=8,
             color=MUTED)
    pdf.savefig(fig)
    plt.close(fig)

    for path, title, sub in plates:
        img = mpimg.imread(os.path.join(ROOT, path))
        h, w = img.shape[0], img.shape[1]
        land = w > h
        fw, fh = (PH, PW) if land else (PW, PH)
        fig = plt.figure(figsize=(fw, fh))
        fig.patch.set_facecolor("white")
        ax = fig.add_axes([0.03, 0.135, 0.94, 0.815])
        ax.imshow(img)
        ax.axis("off")
        fig.text(0.5, 0.095, title.upper(), ha="center", fontsize=15,
                 fontweight="bold", color=INK)
        fig.text(0.5, 0.040, "\n".join(textwrap.wrap(sub, 92)), ha="center",
                 fontsize=9.5, color=MUTED, va="bottom")
        fig.text(0.985, 0.012, f"{COPYRIGHT}  ·  {EMAIL}", ha="right",
                 fontsize=7, color=MUTED)
        pdf.savefig(fig)
        plt.close(fig)


def title_page(pdf, doc=None):
    """Cover: what it is, what it weighs, what stage it is at, who to ask."""
    fig = plt.figure(figsize=(PW, PH))
    fig.patch.set_facecolor("white")
    L, R = 0.072, 0.928

    # masthead
    fig.add_artist(plt.Rectangle((0, 0.962), 1, 0.038,
                                 transform=fig.transFigure, fc=INK, ec="none"))
    fig.text(L, 0.9805, "DESIGN PACKAGE FOR DISCUSSION WITH A BUILDER",
             fontsize=8.2, color="white", va="center", fontweight="bold")
    fig.text(R, 0.9805, f"{REV}  ·  {DATE}", fontsize=8.2, color="white",
             va="center", ha="right")

    fig.text(L, 0.935, "BOAT-HOME", fontsize=44, fontweight="bold",
             color=INK, va="top")
    fig.text(L, 0.868, "Road-towable solar trimaran", fontsize=16,
             color=ACCENT, va="top")
    fig.text(L, 0.840,
             "A 7.2 m boat-home that is its own trailer: the floats fold under "
             "the hull and carry six wheels,\nso one car tows it and it drives "
             "itself in and out of the water.",
             fontsize=10, color=MUTED, va="top", linespacing=1.55)

    for cand in (PHOTOREAL[0][0], "freecad/shots/beauty/cruise_bow_quarter.png"):
        hero = os.path.join(ROOT, cand)
        if os.path.exists(hero):
            img = mpimg.imread(hero)
            h, w = img.shape[0], img.shape[1]
            disp_w = R - L
            disp_h = disp_w * (h / w) * (PW / PH)
            if disp_h > 0.335:                       # keep the page breathing
                disp_h = 0.335
                disp_w = disp_h * (w / h) * (PH / PW)
            ax = fig.add_axes([L + (R - L - disp_w) / 2, 0.775 - disp_h,
                               disp_w, disp_h])
            ax.imshow(img)
            ax.axis("off")
            bottom = 0.775 - disp_h
            break
    else:
        bottom = 0.60

    # ---- headline numbers, four across
    stats = [("7.2 m", "length over hull"),
             ("2 535 mm", "beam on the road"),
             ("4.40 kWp", "solar, walk-on glass over it"),
             ("50 kWh", "battery, 48 V LiFePO4"),
             ("4.7 kn", "maximum, 233 NM at 3 kn"),
             ("5", "berths, 12.1 m2 of floor"),
             ("3 582 kg", "computed, loaded"),
             ("369 mm", "draft, 781 mm freeboard")]
    top = bottom - 0.035
    colw = (R - L) / 4
    for i, (big, small) in enumerate(stats):
        col, row = i % 4, i // 4
        x = L + col * colw
        y = top - row * 0.062
        fig.text(x, y, big, fontsize=15, fontweight="bold", color=INK,
                 va="top")
        fig.text(x, y - 0.028, small, fontsize=7.4, color=MUTED, va="top")
    strip_bottom = top - 0.062 - 0.045
    fig.add_artist(plt.Line2D([L, R], [strip_bottom] * 2,
                              transform=fig.transFigure, color=RULE, lw=0.8))

    # ---- what stage this is at, and what the reader is being asked
    rows = [("STAGE", "Detailed concept - geometry complete, scantlings open"),
            ("ASKING FOR", "A split build: yard lays up and assembles the "
                           "shell, owner fits out"),
            ("STRUCTURE", "Foam-core GRP sandwich, 103 m2 of panel, 754 kg"),
            ("MODEL", "Parametric FreeCAD; legal and structural limits "
                      "asserted in code"),
            ("CONTACT", EMAIL)]
    y = strip_bottom - 0.042
    for k, v in rows:
        if k:
            fig.text(L, y, k, fontsize=7.6, color=ACCENT, fontweight="bold",
                     va="top")
        fig.text(L + 0.155, y, v, fontsize=9.0, color=INK, va="top")
        y -= 0.0305

    fig.add_artist(plt.Line2D([L, R], [0.052, 0.052],
                              transform=fig.transFigure, color=RULE, lw=0.8))
    fig.text(L, 0.036, f"{COPYRIGHT}  ·  all rights reserved", fontsize=7.5,
             color=MUTED, va="top")
    fig.text(R, 0.036, "generated from the model - python3 docs/make_pdf.py",
             fontsize=7.5, color=MUTED, va="top", ha="right")
    pdf.savefig(fig)
    plt.close(fig)
    if doc is not None:
        doc.n += 1


def contents_page_count(toc):
    """How many pages the contents will take - same arithmetic as
    contents_page(), so the page numbers it prints are right."""
    pages, y = 1, PH - MT - 0.72
    for level, _title, _page in toc:
        if y < MB + 0.25:
            pages += 1
            y = PH - MT - 0.60
        y -= 0.10 if level == 1 else 0.0
        y -= 0.185 if level == 1 else 0.165
    return pages


def contents_page(pdf, doc, toc):
    """Table of contents, continued over as many pages as it needs."""
    def open_page(first):
        fig = plt.figure(figsize=(PW, PH))
        fig.patch.set_facecolor("white")
        fig.text(ML / PW, 1 - MT / PH,
                 "CONTENTS" if first else "CONTENTS  (continued)",
                 fontsize=20 if first else 14, fontweight="bold", color=INK,
                 va="top")
        fig.add_artist(plt.Line2D([ML / PW, (PW - MR) / PW],
                                  [(PH - MT - 0.34) / PH] * 2,
                                  transform=fig.transFigure, color=ACCENT,
                                  lw=1.6))
        return fig

    def close_page(fig, n):
        fig.text(0.5, MB * 0.55 / PH, str(n), ha="center", fontsize=8,
                 color=MUTED)
        fig.text(ML / PW, MB * 0.55 / PH, PROJECT, fontsize=7.5, color=MUTED)
        fig.text(1 - MR / PW, MB * 0.55 / PH, COPYRIGHT, fontsize=7.5,
                 color=MUTED, ha="right")
        pdf.savefig(fig)
        plt.close(fig)

    first = True
    fig = open_page(True)
    y = PH - MT - 0.72
    for level, title, page in toc:
        if y < MB + 0.25:
            doc.n += 1
            close_page(fig, doc.n)
            first = False
            fig = open_page(False)
            y = PH - MT - 0.60
        if level == 1:
            y -= 0.10
            fig.text(ML / PW, y / PH, title.upper(), fontsize=10.5,
                     fontweight="bold", color=INK, va="top")
        else:
            fig.text((ML + 0.22) / PW, y / PH, title, fontsize=9.2,
                     color=INK, va="top")
        fig.text((PW - MR) / PW, y / PH, str(page), fontsize=9.2,
                 color=MUTED, va="top", ha="right")
        dots_y = (y - 0.045) / PH
        fig.add_artist(plt.Line2D(
            [(ML + (0.10 if level == 1 else 0.32)) / PW, (PW - MR - 0.22) / PW],
            [dots_y, dots_y], transform=fig.transFigure, color="#e2e5e9",
            lw=0.6, ls=(0, (1, 2))))
        y -= 0.185 if level == 1 else 0.165
    doc.n += 1
    close_page(fig, doc.n)


def render(md, doc, part=""):
    """Render one markdown document into an open Doc."""
    doc.part = part
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
            if not part:                     # dividers carry the title
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
    doc.end_document()


def gallery(pdf, doc=None):
    """Every render and drawing, one per page, after the text."""
    shots = []
    for mode, label in (("cruise", "cruise — trimaran, floats out"),
                        ("detached", "detached — hangar stood off, arms splayed"),
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
    shots = [(p, c) for p, c in shots
             if os.path.exists(os.path.join(ROOT, p))]
    if doc is not None:
        doc.divider("12", "Drawings and renders",
                    f"{len(shots)} plates - five configurations, "
                    "then the drawings")

    for path, cap in shots:
        full = os.path.join(ROOT, path)
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
        fig.text(0.985, 0.012, f"{COPYRIGHT}  ·  {EMAIL}", ha="right",
                 fontsize=7, color=MUTED)
        pdf.savefig(fig)
        plt.close(fig)


PARTS = [
    ("1", "The proposal", "what this is, and what I am asking a builder for",
     "docs/YARD-BRIEF.md", "Part 1 — the proposal"),
    ("2", "The boat", "principal dimensions, performance, systems, cost, risks",
     "README.md", "Part 2 — the boat"),
    ("3", "Construction", "laminate schedule, build sequence, shop, suppliers",
     "docs/construction.md", "Part 3 — construction"),
    ("4", "The hangar", "detachable U-frame, electric locks, dinghy mode",
     "docs/hangar.md", "Part 4 — the hangar"),
    ("5", "Weight", "how to take 350 kg out without deleting anything",
     "docs/weight.md", "Part 5 — weight"),
    ("6", "Structure", "exoskeleton, tow arch, steel-to-laminate rules",
     "docs/structure.md", "Part 6 — structure"),
    ("7", "Roof deck", "walk-on glass over the solar array",
     "docs/roof.md", "Part 7 — roof deck"),
    ("8", "Interior", "layout, stowage, services, mass",
     "docs/interior.md", "Part 8 — interior"),
    ("9", "Front dome", "flat glazing on two tube purlins",
     "docs/dome.md", "Part 9 — front dome"),
    ("10", "Performance", "the resistance model behind the speed and range",
     "docs/performance.md", "Part 10 — performance"),
    ("11", "Road approval", "trailer vs amphibian, brakes, DE / PT / NL",
     "docs/homologation.md", "Part 11 — road approval"),
]


def build(pdf, toc_in=None, toc_out=None, total=None):
    """One full pass over the document. Pass 1 collects the TOC, pass 2
    prints it with real page numbers."""
    doc = Doc(pdf, toc=toc_out)
    doc.total = total
    title_page(pdf, doc)
    photoreal(pdf, doc)
    if toc_in is not None:
        contents_page(pdf, doc, toc_in)
    for number, title, subtitle, path, part in PARTS:
        full = os.path.join(ROOT, path)
        if not os.path.exists(full):
            continue
        doc.divider(number, title, subtitle)
        if toc_out is not None:
            toc_out.append((1, f"Part {number} — {title}", doc.n))
        render(open(full).read(), doc, part=part)
    doc.end_document()
    if toc_out is not None:
        toc_out.append((1, "Part 12 — Drawings and renders", doc.n + 1))
    gallery(pdf, doc)
    return doc.n


if __name__ == "__main__":
    import io
    from matplotlib.backends.backend_pdf import PdfPages as _PP

    # pass 1: no contents page, collect headings and the page count
    toc = []
    scratch = io.BytesIO()
    with _PP(scratch) as probe:
        build(probe, toc_in=None, toc_out=toc)
    # the real run has the contents pages themselves in front: estimate
    # how many, then offset every entry by that
    toc_pages = contents_page_count(toc)
    for i, (lvl, title, page) in enumerate(toc):
        toc[i] = (lvl, title, page + toc_pages)

    with PdfPages(OUT) as pdf:
        total = build(pdf, toc_in=toc, toc_out=None)
        with _PP(io.BytesIO()):
            pass
        d = pdf.infodict()
        d["Title"] = "Boat-Home — Road-Towable Solar Trimaran"
        d["Subject"] = "Design package for discussion with a builder"
        d["Author"] = f"{AUTHOR} <{EMAIL}>"
        d["Creator"] = AUTHOR
        d["Keywords"] = (f"{COPYRIGHT}. All rights reserved. "
                         f"Contact {EMAIL}")
    print("wrote", OUT)
