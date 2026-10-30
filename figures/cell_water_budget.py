"""Where the water goes in one cell, for docs/theory/overview.md.

One model cell seen from the side, with a lower neighbour cell on the left. Stores are
shapes, fluxes are arrows: blue ribbons for liquid water, grey ribbons for vapour, a
dashed arrow for a routine that exists in the code but is switched off (stemflow).

Facts:
  docs/theory/hydrologic-model.md, sections 1 to 6
  docs/theory/groundwater-model.md, sections 2 to 12
  docs/theory/layered-subsurface.md, Figure 1

Precipitation is split into rain and snow before the canopy: only the rain enters the
canopy store, the snowfall goes to the snowpack, and the melt reaches the surface water
without passing through the canopy (hydrologic-model.md, Sections 5.1 and 5.7). The net
vadose exchange moves the water table every surface step; lateral groundwater flow runs
on the slower scheduler clock.

Run from the repository root:

    python3 figures/cell_water_budget.py [preview-folder]

Output: static/img/theory/cell-water-budget.svg (en), cell-water-budget.pt.svg and
cell-water-budget.es.svg, and a PNG of each in the preview folder, if given.
"""

from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
from matplotlib.patches import Circle, Polygon, Rectangle

sys.dont_write_bytecode = True  # never leave __pycache__ in the docs repo
from site_style import INK, SOFT, STATIC, WATER, Sheet, bezier, color, oklch_hex  # noqa: E402
from layered_column import _tapered  # noqa: E402  (on the path through site_style)
import flow_kit as fk  # noqa: E402
from fig_check import _ARROWS, report, track  # noqa: E402

# --- text per language. Math stays the same in every language. ------------------------------
# A word may hold "\n": its lines stack, centred on the anchor of the one-line English label.
LABELS = {
    "en": {
        "atmosphere": "Atmosphere",
        "split": r"$P_{\mathrm{gross}} = P_{\mathrm{rain}} + P_{\mathrm{snow}}$, split by the air temperature",
        "cell": "one model cell",
        "rain": ("rain", r"$P_{\mathrm{rain}}$"),
        "snow": ("snow", r"$P_{\mathrm{snow}}$"),
        "e_can": ("canopy", r"$E_{\mathrm{can}}$"),
        "t_r": ("soil ET", r"$T_{\mathrm{r}}$"),
        "e_surf": ("open water", r"$E_{\mathrm{surf}}$"),
        "e_s": ("sublimation", r"$E_{\mathrm{s}}$"),
        "throughfall": ("throughfall", r"$T_{\mathrm{f}}$"),
        "stemflow": ("stemflow", r"$F_{\mathrm{stem}} = 0$"),
        "melt": ("melt", r"$M_{\mathrm{snow}}$"),
        "infiltration": ("infiltration", r"$i$"),
        "recharge": ("recharge", r"$R_{\mathrm{down}}$"),
        "capillary": ("capillary rise", r"$C_{\mathrm{up}}$"),
        "excess": ("saturation excess", r"$S_{\mathrm{excess}}$"),
        "exfiltration": ("exfiltration", r"$q_{\mathrm{exf}}$"),
        "lateral": r"lateral flow $\mathbf{F}$",
        "surface_flow": ["surface flow"],
        "neighbour": "neighbour cell",
        "notes": {
            "canopy": (r"Canopy store $S_{\mathrm{can}}$",
                       ["takes only the rain and",
                        r"holds up to $S_{\mathrm{can,max}} = C_{\mathrm{can}}\,\mathrm{LAI}$;",
                        "the excess falls as throughfall"]),
            "snow": ("Snowpack SWE",
                     ["gains snow, loses melt and", "sublimation"]),
            "surface": (r"Surface water $d$",
                        [r"receives $P_{\mathrm{eff}} = T_{\mathrm{f}} + F_{\mathrm{stem}}$;",
                         "routed to the neighbour cells;",
                         "while it stands, soil ET pauses"]),
            "vadose": (r"Vadose zone $S_{\mathrm{uz}}$",
                       [r"$i = \min(i_{\mathrm{sup}},\,I_{\mathrm{cap}},\,i_{\mathrm{store}})$",
                        "three stores, detailed in the",
                        "layered-column figure"]),
            "groundwater": (r"Groundwater, head $h$",
                            [r"$S_y\,\partial h/\partial t = -\nabla\cdot\mathbf{F} + R$",
                             r"net exchange $R_{\mathrm{net}} = R_{\mathrm{down}} - C_{\mathrm{up}}$",
                             "is applied every step; lateral",
                             r"flow $\mathbf{F}$ runs on a slower clock"]),
        },
        "key": ["liquid water", "water vapour", "in the code, switched off"],
    },
    "pt": {
        "atmosphere": "Atmosfera",
        "split": r"$P_{\mathrm{gross}} = P_{\mathrm{rain}} + P_{\mathrm{snow}}$, segundo a temperatura do ar",
        "cell": "uma célula do modelo",
        "rain": ("chuva", r"$P_{\mathrm{rain}}$"),
        "snow": ("neve", r"$P_{\mathrm{snow}}$"),
        "e_can": ("dossel", r"$E_{\mathrm{can}}$"),
        "t_r": ("ET do\nsolo", r"$T_{\mathrm{r}}$"),
        "e_surf": ("água livre", r"$E_{\mathrm{surf}}$"),
        "e_s": ("sublimação", r"$E_{\mathrm{s}}$"),
        "throughfall": ("throughfall", r"$T_{\mathrm{f}}$"),
        "stemflow": ("fluxo de tronco", r"$F_{\mathrm{stem}} = 0$"),
        "melt": ("degelo", r"$M_{\mathrm{snow}}$"),
        "infiltration": ("infiltração", r"$i$"),
        "recharge": ("recarga", r"$R_{\mathrm{down}}$"),
        "capillary": ("ascensão\ncapilar", r"$C_{\mathrm{up}}$"),
        "excess": ("excesso de\nsaturação", r"$S_{\mathrm{excess}}$"),
        "exfiltration": ("exfiltração", r"$q_{\mathrm{exf}}$"),
        "lateral": r"fluxo lateral $\mathbf{F}$",
        "surface_flow": ["escoamento", "superficial"],
        "neighbour": "célula vizinha",
        "notes": {
            "canopy": (r"Água interceptada $S_{\mathrm{can}}$",
                       ["o dossel recebe só a chuva e",
                        r"guarda até $S_{\mathrm{can,max}} = C_{\mathrm{can}}\,\mathrm{LAI}$;",
                        "o excesso cai como throughfall"]),
            "snow": ("Manto de neve SWE",
                     ["ganha neve; perde água por", "degelo e sublimação"]),
            "surface": (r"Água superficial $d$",
                        [r"recebe $P_{\mathrm{eff}} = T_{\mathrm{f}} + F_{\mathrm{stem}}$;",
                         "roteada para as células vizinhas;",
                         "sob lâmina, a ET do solo cessa"]),
            "vadose": (r"Zona vadosa $S_{\mathrm{uz}}$",
                       [r"$i = \min(i_{\mathrm{sup}},\,I_{\mathrm{cap}},\,i_{\mathrm{store}})$",
                        "três reservatórios, detalhados na",
                        "figura da coluna em camadas"]),
            "groundwater": (r"Água subterrânea, carga $h$",
                            [r"$S_y\,\partial h/\partial t = -\nabla\cdot\mathbf{F} + R$",
                             r"troca líquida $R_{\mathrm{net}} = R_{\mathrm{down}} - C_{\mathrm{up}}$",
                             "aplicada a cada passo; o fluxo",
                             r"lateral $\mathbf{F}$, num relógio mais lento"]),
        },
        "key": ["água líquida", "vapor d'água", "no código, desativado"],
    },
    "es": {
        "atmosphere": "Atmósfera",
        "split": r"$P_{\mathrm{gross}} = P_{\mathrm{rain}} + P_{\mathrm{snow}}$, según la temperatura del aire",
        "cell": "una celda del modelo",
        "rain": ("lluvia", r"$P_{\mathrm{rain}}$"),
        "snow": ("nieve", r"$P_{\mathrm{snow}}$"),
        "e_can": ("dosel", r"$E_{\mathrm{can}}$"),
        "t_r": ("ET del\nsuelo", r"$T_{\mathrm{r}}$"),
        "e_surf": ("agua libre", r"$E_{\mathrm{surf}}$"),
        "e_s": ("sublimación", r"$E_{\mathrm{s}}$"),
        "throughfall": ("throughfall", r"$T_{\mathrm{f}}$"),
        "stemflow": ("flujo de tallo", r"$F_{\mathrm{stem}} = 0$"),
        "melt": ("fusión", r"$M_{\mathrm{snow}}$"),
        "infiltration": ("infiltración", r"$i$"),
        "recharge": ("recarga", r"$R_{\mathrm{down}}$"),
        "capillary": ("ascenso\ncapilar", r"$C_{\mathrm{up}}$"),
        "excess": ("exceso de\nsaturación", r"$S_{\mathrm{excess}}$"),
        "exfiltration": ("exfiltración", r"$q_{\mathrm{exf}}$"),
        "lateral": r"flujo lateral $\mathbf{F}$",
        "surface_flow": ["flujo", "superficial"],
        "neighbour": "celda vecina",
        "notes": {
            "canopy": (r"Agua interceptada $S_{\mathrm{can}}$",
                       ["el dosel recibe solo la lluvia y",
                        r"retiene hasta $S_{\mathrm{can,max}} = C_{\mathrm{can}}\,\mathrm{LAI}$;",
                        "el exceso cae como throughfall"]),
            "snow": ("Manto de nieve SWE",
                     ["gana nieve; pierde agua por", "fusión y sublimación"]),
            "surface": (r"Agua superficial $d$",
                        [r"recibe $P_{\mathrm{eff}} = T_{\mathrm{f}} + F_{\mathrm{stem}}$;",
                         "enrutada a las celdas vecinas;",
                         "bajo lámina, la ET del suelo cesa"]),
            "vadose": (r"Zona vadosa $S_{\mathrm{uz}}$",
                       [r"$i = \min(i_{\mathrm{sup}},\,I_{\mathrm{cap}},\,i_{\mathrm{store}})$",
                        "tres almacenes, detallados en la",
                        "figura de la columna en capas"]),
            "groundwater": (r"Agua subterránea, carga $h$",
                            [r"$S_y\,\partial h/\partial t = -\nabla\cdot\mathbf{F} + R$",
                             r"intercambio $R_{\mathrm{net}} = R_{\mathrm{down}} - C_{\mathrm{up}}$",
                             "aplicado en cada paso; el flujo",
                             r"lateral $\mathbf{F}$ sigue un reloj más lento"]),
        },
        "key": ["agua líquida", "vapor de agua", "en el código, desactivado"],
    },
}
SYMBOLS = {"can": r"$S_{\mathrm{can}}$", "swe": "SWE", "d": r"$d$", "uz": r"$S_{\mathrm{uz}}$", "h": r"$h$"}

# --- colours ---------------------------------------------------------------------------------
VAPOUR = SOFT
SOIL = color("slot_near_surface")
SATURATED = color("slot_wet_even")
SKY = color("deep_fill")
# New colours (OKLCH), near the lightness and chroma of the water tokens:
SURFACE_WATER = oklch_hex(0.72, 0.090, 245)  # ponded water d: between "water" (0.50) and "wet_a" (0.86)
SNOW = oklch_hex(0.975, 0.012, 240)          # snowpack: near white, a trace of the water hue

# --- geometry (px, y downward) ---------------------------------------------------------------
W, H = 760, 560
NX0, CX0, CX1 = 24, 80, 520          # neighbour from NX0 to CX0, the cell from CX0 to CX1
BAND = (80, 18, 520, 50)             # atmosphere band x0, y0, x1, y1
GY, FY = 290, 276                    # cell ground and top of its surface water
NGY, NFY = 318, 310                  # neighbour ground and water
TY, NTY = 400, 412                   # water table, cell and neighbour
BY = 468                             # aquifer base
RD = 345                             # root depth
TX, CROWN_Y = 290, 150               # tree trunk x, crown centre y
SNOW_X0, SNOW_TOP = 400, 250         # snowpack left edge and top
NOTE_X = 548
NOTE_ROOM = W - 6 - NOTE_X           # the note column ends 6 px inside the card


def main(preview: Path | None = None) -> None:
    for lang in LABELS:
        draw(lang, preview)


def draw(lang: str, preview: Path | None = None) -> None:
    T = LABELS[lang]
    _ARROWS.clear()  # fig_check keeps the arrows of every sheet; check this one only
    s = Sheet(W, H, "cell-water-budget")
    ax = s.ax

    def two_line(x, y, pair, ha="left", c=INK):
        """Word lines, then the symbol 16 px below; a multi-line word is centred on y."""
        words, sym = pair[0].split("\n"), pair[1]
        y0 = y - 8 * (len(words) - 1)
        for k, word in enumerate(words):
            s.text(x, y0 + 16 * k, word, ha=ha, c=c)
        s.text(x, y0 + 16 * len(words), sym, ha=ha, c=c, size=10)

    def flux(points, kind="water", **kw):
        """Liquid (blue) or vapour (grey) ribbon; points as for Sheet.arrow."""
        c = WATER if kind == "water" else VAPOUR
        kw.setdefault("width", (1.2, 3.8) if kind == "water" else (1.0, 3.2))
        kw.setdefault("head", (12, 11) if kind == "water" else (11, 10))
        with track(ax):
            s.arrow(points, c=c, **kw)

    # --- atmosphere ----------------------------------------------------------------------------
    x0, y0, x1, y1 = BAND
    s.box(x0, y0, x1 - x0, y1 - y0, fill=SKY, edge=color("guide"), radius=8, lw=0.8, z=1)
    s.text(x0 + 12, (y0 + y1) / 2, T["atmosphere"], bold=True, size=10.5)
    fk.text(s, x0 + 112, (y0 + y1) / 2, T["split"], room=x1 - 10 - (x0 + 112))

    # --- neighbour cell (lower, faded) --------------------------------------------------------
    FADE = 0.45
    ax.add_patch(Rectangle((NX0, NGY), CX0 - NX0, NTY - NGY, facecolor=SOIL, alpha=FADE, lw=0, zorder=1))
    ax.add_patch(Rectangle((NX0, NTY), CX0 - NX0, BY - NTY, facecolor=SATURATED, alpha=FADE, lw=0, zorder=1))
    ax.add_patch(Rectangle((NX0, NFY), CX0 - NX0, NGY - NFY, facecolor=SURFACE_WATER, alpha=FADE, lw=0, zorder=1))
    s.line([NX0, CX0], [NGY, NGY], c=color("ground"), lw=2.0, z=3)
    s.line([NX0, CX0], [NTY, NTY], c=WATER, lw=1.6, z=3)
    s.text((NX0 + CX0) / 2, (NGY + NTY) / 2, T["neighbour"], c=SOFT, size=9, rotation=90, ha="center")

    # --- the cell: soil, groundwater, surface water, bedrock -----------------------------------
    ax.add_patch(Rectangle((CX0, GY), CX1 - CX0, TY - GY, facecolor=SOIL, lw=0, zorder=1))
    ax.add_patch(Rectangle((CX0, TY), CX1 - CX0, BY - TY, facecolor=SATURATED, lw=0, zorder=1))
    ax.add_patch(Rectangle((CX0, FY), CX1 - CX0, GY - FY, facecolor=SURFACE_WATER, lw=0, zorder=2))
    ax.add_patch(Rectangle((NX0, BY), CX1 - NX0, 22, facecolor=color("card"),
                           edgecolor=color("bedrock_hatch"), hatch="////", lw=0, zorder=1))
    ax.add_patch(Rectangle((CX0, FY), CX1 - CX0, BY - FY, fill=False, edgecolor=color("guide"),
                           lw=0.8, zorder=3))
    s.line([CX0, CX1], [GY, GY], c=color("ground"), lw=2.4, z=4)
    s.line([CX0, CX1], [TY, TY], c=WATER, lw=2.0, z=4)
    s.line([NX0, CX1], [BY, BY], c=INK, lw=2.0, z=4)

    # Water-table symbol and the head label.
    ax.add_patch(Polygon([(442, TY - 11), (458, TY - 11), (450, TY - 1)], closed=True,
                         facecolor=WATER, edgecolor="none", zorder=6))
    s.line([443, 457], [TY + 5, TY + 5], c=WATER, lw=1.2, z=6)
    s.line([446, 454], [TY + 9, TY + 9], c=WATER, lw=1.2, z=6)
    s.text(466, TY - 7, SYMBOLS["h"], size=11)

    # Snowpack: a drift resting on the surface water.
    drift = bezier([(SNOW_X0, FY), (SNOW_X0 + 4, SNOW_TOP - 2), (SNOW_X0 + 40, SNOW_TOP),
                    (CX1, SNOW_TOP + 2)], 40)
    ax.add_patch(Polygon(np.vstack([drift, [(CX1, FY)]]), closed=True, facecolor=SNOW,
                         edgecolor=color("guide"), lw=0.9, zorder=5))
    s.text(468, 266, SYMBOLS["swe"], size=10, ha="center")

    # Store symbols.
    s.text(338, (FY + GY) / 2, SYMBOLS["d"], size=10, ha="center", z=11)
    s.text(446, 356, SYMBOLS["uz"], size=11, ha="center")

    # --- tree (scaled from layered_column.tree, with a taller trunk) ---------------------------
    def tall_tree(x, ground, crown_y, root_depth, k=1.3):
        bark, roots = color("trunk"), color("roots")
        shade, light = color("canopy_shade"), color("canopy_light")
        reach = root_depth - ground
        root_paths = [
            ([(x, ground), (x + 2, ground + 0.45 * reach), (x - 3, ground + reach - 1)], (3.4, 0.8)),
            ([(x - 2, ground + 2), (x - 24, ground + 0.35 * reach), (x - 34, ground + 0.95 * reach)], (2.6, 0.6)),
            ([(x + 2, ground + 2), (x + 26, ground + 0.30 * reach), (x + 36, ground + 0.90 * reach)], (2.6, 0.6)),
            ([(x - 3, ground + 1), (x - 32, ground + 0.10 * reach), (x - 48, ground + 0.40 * reach)], (1.8, 0.5)),
            ([(x + 3, ground + 1), (x + 34, ground + 0.08 * reach), (x + 50, ground + 0.36 * reach)], (1.8, 0.5)),
            ([(x - 13, ground + 0.40 * reach), (x - 8, ground + 0.70 * reach), (x - 17, ground + reach - 2)], (1.2, 0.4)),
            ([(x + 14, ground + 0.36 * reach), (x + 10, ground + 0.66 * reach), (x + 20, ground + reach - 3)], (1.2, 0.4)),
        ]
        for pts, (w0, w1) in root_paths:
            ax.add_patch(Polygon(_tapered(bezier(pts, 40), w0, w1), closed=True, facecolor=roots,
                                 edgecolor="none", zorder=4))
        top = crown_y + 16
        trunk = [(x - 6.5, ground + 1), (x - 3.6, ground - 18), (x - 3.0, top),
                 (x + 3.0, top), (x + 3.6, ground - 18), (x + 6.5, ground + 1)]
        ax.add_patch(Polygon(trunk, closed=True, facecolor=bark, edgecolor="none", zorder=6))
        for (xa, ya), (xb, yb) in (((x - 1, top + 18), (x - 16, top + 2)), ((x + 1, top + 10), (x + 17, top - 6))):
            ax.plot([xa, xb], [ya, yb], color=bark, linewidth=2.4, solid_capstyle="round", zorder=6)
        for dx, dy, r in ((-22, 8, 17), (22, 8, 17), (0, 12, 19)):
            ax.add_patch(Circle((x + k * dx, crown_y + k * dy), k * r, facecolor=shade, edgecolor="none", zorder=7))
        for dx, dy, r in ((-12, -6, 17), (13, -4, 16), (0, -16, 16), (-26, -2, 11), (27, 0, 11)):
            ax.add_patch(Circle((x + k * dx, crown_y + k * dy), k * r, facecolor=light, edgecolor="none", zorder=8))

    tall_tree(TX, GY, CROWN_Y, RD)
    s.text(TX, CROWN_Y + 2, SYMBOLS["can"], size=11, ha="center", z=12)

    # --- precipitation --------------------------------------------------------------------------
    def raindrop(x, y, r=2.6):
        """Teardrop: pointed top at y - 2.6 r, round bottom centred on y."""
        a = np.linspace(-0.25 * np.pi, 1.25 * np.pi, 24)
        arc = np.column_stack([x + r * np.cos(a), y + r * np.sin(a)])[::-1]
        ax.add_patch(Polygon(np.vstack([[(x, y - 2.6 * r)], arc]), closed=True, facecolor=WATER,
                             edgecolor="none", zorder=6))

    def snowflake(x, y, r=4.2):
        for a in (0, 60, 120):
            t = np.deg2rad(a)
            ax.plot([x - r * np.cos(t), x + r * np.cos(t)], [y - r * np.sin(t), y + r * np.sin(t)],
                    color=WATER, linewidth=1.0, solid_capstyle="round", zorder=6)

    flux([(352, 52), (348, 88), (330, 116)])                      # rain onto the crown
    two_line(358, 72, T["rain"])
    for x, y in ((338, 64), (321, 99)):
        raindrop(x, y)
    flux([(495, 52), (495, 248)])                                 # snow onto the snowpack
    two_line(488, 130, T["snow"], ha="right")
    for x, y in ((506, 92), (484, 178), (507, 214)):
        snowflake(x, y)

    # --- vapour -----------------------------------------------------------------------------------
    flux([(445, SNOW_TOP + 1), (445, 52)], kind="vapour")         # sublimation
    two_line(437, 112, T["e_s"], ha="right")
    flux([(282, 110), (276, 80), (270, 52)], kind="vapour")       # soil ET (transpiration)
    two_line(284, 72, T["t_r"])
    flux([(244, 140), (222, 104), (205, 52)], kind="vapour")      # canopy evaporation
    two_line(214, 112, T["e_can"], ha="right")
    flux([(125, FY - 1), (125, 52)], kind="vapour")               # open-water evaporation
    two_line(133, 185, T["e_surf"])

    # --- canopy to ground; melt straight to the surface water ----------------------------------
    flux([(262, 192), (262, FY - 1)])                             # throughfall
    two_line(254, 228, T["throughfall"], ha="right")
    with track(ax):
        s.dashed([(301, 196), (301, FY - 1)], c=WATER)            # stemflow, off in the code
    two_line(309, 200, T["stemflow"])
    flux([(SNOW_X0 + 2, 262), (SNOW_X0 - 24, 261), (SNOW_X0 - 42, FY + 3)])
    s.text(SNOW_X0 - 4, 242, " ".join(T["melt"]), ha="right")

    # --- surface to soil to groundwater --------------------------------------------------------
    flux([(150, GY + 1), (150, 342)])                             # infiltration
    two_line(158, 305, T["infiltration"])
    flux([(185, 352), (185, TY - 1)])                             # recharge
    two_line(177, 365, T["recharge"], ha="right")
    flux([(210, TY + 2), (210, 352)])                             # capillary rise
    two_line(218, 365, T["capillary"])
    flux([(378, 446), (378, FY + 4)])                             # exfiltration
    two_line(370, 370, T["exfiltration"], ha="right")
    flux([(500, 345), (500, FY + 4)])                             # saturation excess
    two_line(492, 310, T["excess"], ha="right")

    # --- to the neighbour -----------------------------------------------------------------------
    flux([(330, 440), (200, 438), (90, 444), (34, 446)], width=(2.5, 10), head=(18, 20))
    s.text(236, 420, T["lateral"])
    flux([(100, FY + 4), (70, FY + 8), (44, NFY + 3)])
    lines = T["surface_flow"]
    for k, line in enumerate(lines):                              # bottom line at y = 266
        s.text(30, 266 - 16 * (len(lines) - 1 - k), line)

    # --- notes: one per store, with a swatch of its fill ---------------------------------------
    NOTES = T["notes"]
    for key, y, fill in (("canopy", 96, color("canopy_light")), ("snow", 178, SNOW),
                         ("surface", 244, SURFACE_WATER), ("vadose", 328, SOIL),
                         ("groundwater", 412, SATURATED)):
        s.box(NOTE_X - 18, y - 6, 12, 12, fill=fill, edge=color("guide"), radius=2.5, lw=0.8)
        heading, rows = NOTES[key]
        fk.text(s, NOTE_X, y, heading, bold=True, size=10, room=NOTE_ROOM)
        for i, row in enumerate(rows):
            fk.text(s, NOTE_X, y + 20 + 17 * i, row, room=NOTE_ROOM)

    # --- key ------------------------------------------------------------------------------------
    # One-cell bracket under the bedrock.
    s.line([CX0, CX0, CX1, CX1], [BY + 28, BY + 33, BY + 33, BY + 28], c=SOFT, lw=1.0)
    s.text((CX0 + CX1) / 2, BY + 45, T["cell"], c=SOFT, ha="center")

    ky = 538
    kx = 40
    for label, kind in zip(T["key"], ("water", "vapour", "dashed")):
        if kind == "dashed":
            with track(ax):
                s.dashed([(kx, ky), (kx + 34, ky)], c=WATER)
        else:
            flux([(kx, ky), (kx + 34, ky)], kind=kind)
        s.text(kx + 44, ky, label)
        kx += 44 + fk.width(s, label) + 26

    print(lang, end=": ")
    report(s)
    print(s.save(STATIC / "theory", lang, preview))


if __name__ == "__main__":
    main(Path(sys.argv[1]) if len(sys.argv) > 1 else None)
