"""Laminate schedule — areal masses include resin at the stated fibre fraction.

The point of this module: structural mass is COMPUTED from wetted areas
(`areas.json`, measured off the FreeCAD solids) times a laminate schedule,
instead of being estimated in prose. Change a schedule here and the mass
budget in `params.checks()` moves with it.

Plain python3, no FreeCAD import — `params.py` uses it directly.
"""

FIBRE_FRACTION = 0.45          # hand layup + vacuum bag; 0.55 only if infused
RESIN_DENSITY = 1150           # kg/m3, epoxy
GLASS_DENSITY = 2560           # kg/m3, E-glass

# Fillets, tapes, overlaps, bog, and the resin you actually use rather
# than the resin the arithmetic says you need. The single most commonly
# underestimated item in a composite build - do not drop it.
LAMINATE_MARGIN = 1.12

CORES = {
    "PVC80":  {"rho":  80, "note": "Divinycell H80 class - bottom, slam, hardware"},
    "PET60":  {"rho":  60, "note": "ArmaFORM/Airex PET - topsides, cabin, deck"},
    "PET100": {"rho": 100, "note": "float deck under wheel stub axles"},
    "PLY18":  {"rho": 650, "note": "local inserts at every through-bolt"},
}

# zone: (core, core_mm, outer_skin_gsm, inner_skin_gsm)
ZONES = {
    "hull_bottom":   ("PVC80",  20, 1800,  900),
    "hull_topsides": ("PET60",  20,  900,  600),
    "hull_deck":     ("PET60",  25,  900,  600),
    "float_shell":   ("PVC80",  18, 1200,  800),
    "float_deck":    ("PET100", 20, 1200,  800),
    "cabin_walls":   ("PET60",  20,  600,  600),
    "roof_sandwich": ("PET60", 200,  900,  900),   # per roof.md, carries the glass deck
    "bulkheads":     ("PET60",  15,  600,  600),
}

# what each zone is for, in words - used by docs and the PDF
ZONE_NOTE = {
    "hull_bottom":   "slam, grounding, trailer support - the only zone that sees impact",
    "hull_topsides": "above the chine; stiffness, not strength",
    "hull_deck":     "walked on, carries the dome and deck hardware",
    "float_shell":   "grounding on slipways, wheel and arm reactions",
    "float_deck":    "stub-axle and arm landings; denser core under hardware",
    "cabin_walls":   "distributed loads only - the exoskeleton takes point loads",
    "roof_sandwich": "200 mm core: carries the walk-on glass deck over a 2.4 m span",
    "bulkheads":     "shear webs and tank/berth boundaries",
}


def skin_areal(gsm):
    """kg/m2 of one cured skin at FIBRE_FRACTION."""
    return (gsm / 1000.0) / FIBRE_FRACTION


def core_areal(zone):
    core, mm, _o, _i = ZONES[zone]
    return CORES[core]["rho"] * mm / 1000.0


def panel_areal(zone):
    """kg/m2 of the finished panel, core + both skins, before margin."""
    core, mm, outer, inner = ZONES[zone]
    return core_areal(zone) + skin_areal(outer) + skin_areal(inner)


def panel_thickness(zone):
    """mm, nominal: core + both skins at ~1.9 kg/m2 per mm of laminate."""
    core, mm, outer, inner = ZONES[zone]
    return mm + (skin_areal(outer) + skin_areal(inner)) / 1.9


def zone_mass(zone, area_m2):
    """kg for a zone, margin included."""
    return panel_areal(zone) * area_m2 * LAMINATE_MARGIN


def structural_mass(areas):
    """kg of primary structure for {zone: m2}, margin included."""
    return sum(zone_mass(z, areas.get(z, 0.0)) for z in ZONES)


def glass_kg(areas):
    """kg of dry fabric to buy, before the margin - for the shopping list."""
    total = 0.0
    for z, a in areas.items():
        if z not in ZONES:
            continue
        _c, _mm, outer, inner = ZONES[z]
        total += (outer + inner) / 1000.0 * a
    return total * LAMINATE_MARGIN


def resin_kg(areas):
    """kg of mixed epoxy, including the margin and consumable waste."""
    return glass_kg(areas) * (1 - FIBRE_FRACTION) / FIBRE_FRACTION


def core_m2(areas):
    """{core: m2} of core board to buy."""
    out = {}
    for z, a in areas.items():
        if z not in ZONES:
            continue
        out.setdefault(ZONES[z][0], 0.0)
        out[ZONES[z][0]] += a
    return out
