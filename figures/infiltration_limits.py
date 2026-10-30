"""Three limits on infiltration, for docs/theory/hydrologic-model.md, Sections 4.5 and 4.6.

The infiltration of a time step is the smallest of three rates (Section 4.6):
the supply i_sup (the water on the surface), the Darcy capacity I_cap (Section 4.5) and the
storage room i_store left above the water table (Section 4.1). Three soil columns, one cell
each, show a case where each limit is the smallest. Under each column: the verdict, the
definition of that limit and where its terms come from. A band at the bottom says what
happens to the water that does not infiltrate and to the water that does.

Soil and water colours follow the layered-column figure (figures/layered_column.py) and
figures/cell_water_budget.py. The cases are schematic: no numbers, layers not to scale.

Where the docs and the code differ, the figure draws the code (see FACTS below):
  - the matric head comes from the near-surface layer, not from the whole vadose store
    of Section 4.2;
  - d_eff is the surface water plus the rain of the step (the throughfall, with the canopy
    on) plus the snowmelt;
  - the near-surface layer is L_top thick (0.05 m by default), not the 0.10 m target of the
    docs' layer list.

Run from the repository root:

    python3 figures/infiltration_limits.py [preview-folder]

Output: static/img/theory/infiltration-limits.svg (en), infiltration-limits.pt.svg and
infiltration-limits.es.svg, and a PNG of each in the preview folder, if given.
"""

from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
from matplotlib.backends.backend_agg import RendererAgg
from matplotlib.patches import Polygon, Rectangle

sys.dont_write_bytecode = True  # never leave __pycache__ in the docs repo
from site_style import INK, SOFT, STATIC, WATER, Sheet, color, oklch_hex  # noqa: E402
import flow_kit as fk  # noqa: E402
from fig_check import _ARROWS, report, track  # noqa: E402

# --- text per language. Math stays the same in every language. ------------------------------
EQ_TERMS = [r"$i = \min($", r"$i_{\mathrm{sup}}$", None, r"$I_{\mathrm{cap}}$", None,
            r"$i_{\mathrm{store}}$", r"$)$"]  # None: the separator of the language
LABELS = {
    "en": {
        "eq_sep": r"$,\ \ $",
        "eq_terms": ["supply", "capacity", "storage"],
        "panels": [
            {
                "title": "Supply limits",
                "case": "light rain on a dry soil",
                "verdict": (r"$i = i_{\mathrm{sup}}$", "all the water enters"),
                "lines": [
                    (r"$i_{\mathrm{sup}} = d_{\mathrm{eff}}\,/\,\Delta t_{\mathrm{h}}$", 0),
                    (r"$d_{\mathrm{eff}}$  water on the surface,", 21),
                    ("with the rain of this step,", 17),
                    ("or the canopy throughfall,", 17),
                    ("and the snowmelt", 17),
                    (r"$\Delta t_{\mathrm{h}}$  time step in hours", 19),
                ],
            },
            {
                "title": "Capacity limits",
                "case": "deep pond on a soil of low conductivity",
                "verdict": (r"$i = I_{\mathrm{cap}}$", "what the soil can pass"),
                "lines": [
                    (r"$I_{\mathrm{cap}} = K_{\mathrm{soil}}\,[\min(h_{\mathrm{pond}} - \psi_{\mathrm{m}},"
                     r"\Delta h_{\mathrm{max}})/L_{\mathrm{top}} + 1]$", 0),
                    (r"$K_{\mathrm{soil}} = w_K\,K_{\mathrm{sat}} + (1 - w_K)\,K(\theta_{\mathrm{top}})$", 21),
                    (r"$K_{\mathrm{sat}}$  near-surface layer, from the soil table", 20),
                    (r"$K(\theta_{\mathrm{top}})$  conductivity once the top is wetted", 19),
                    (r"$\psi_{\mathrm{m}}$  matric head of the near-surface layer", 19),
                    (r"defaults $L_{\mathrm{top}} = 0.05$ m, $\Delta h_{\mathrm{max}} = 1$ m, $w_K = 0.5$", 19),
                ],
            },
            {
                "title": "Storage limits",
                "case": "shallow water table",
                "verdict": (r"$i = i_{\mathrm{store}}$", "what still fits"),
                "lines": [
                    (r"$i_{\mathrm{store}} = S_{\mathrm{uz,rem}}\,/\,\Delta t_{\mathrm{h}}$", 0),
                    (r"$S_{\mathrm{uz,rem}} = \max(S_{\mathrm{uz,max}} - S_{\mathrm{uz}},0)$", 21),
                    (r"$S_{\mathrm{uz,max}} = z_{\mathrm{wt}}\,(\theta_{\mathrm{sat}} - \theta_{\mathrm{r}})$", 20),
                    (r"$z_{\mathrm{wt}}$  depth to the water table:", 19),
                    ("less room as the table rises;", 17),
                    (r"with none left, $i = 0$", 18),
                ],
            },
        ],
        "layers": ["near surface", "root zone", "transmission", "saturated"],
        "rain": "light rain",
        "low_k": r"low $K_{\mathrm{sat}}$",
        "routed": "routed",
        "notes": [
            ("What does not infiltrate",
             [r"$d_{\mathrm{eff}} - i\,\Delta t_{\mathrm{h}}$ stays on the",
              r"surface as $d$ and is routed to",
              "the neighbour cells"]),
            ("What infiltrates",
             ["fills the near-surface layer first, then the",
              "root zone, then the transmission layer"]),
            ("No infiltration",
             ["on impervious cells, and",
              "when the water table is at",
              r"the surface, $z_{\mathrm{wt}} \leq 0$"]),
        ],
    },
    "pt": {
        "eq_sep": r"$,\ \ \qquad$",
        "eq_terms": ["fornecimento", "capacidade", "armazenamento"],
        "panels": [
            {
                "title": "O fornecimento limita",
                "case": "chuva fraca sobre solo seco",
                "verdict": (r"$i = i_{\mathrm{sup}}$", "toda a água entra"),
                "lines": [
                    (r"$i_{\mathrm{sup}} = d_{\mathrm{eff}}\,/\,\Delta t_{\mathrm{h}}$", 0),
                    (r"$d_{\mathrm{eff}}$  água na superfície,", 21),
                    ("com a chuva deste passo,", 17),
                    ("ou o throughfall do dossel,", 17),
                    ("e o degelo", 17),
                    (r"$\Delta t_{\mathrm{h}}$  passo de tempo (h)", 19),
                ],
            },
            {
                "title": "A capacidade limita",
                "case": "lâmina alta sobre solo de baixa condutividade",
                "verdict": (r"$i = I_{\mathrm{cap}}$", "o que o solo deixa passar"),
                "lines": [
                    (r"$I_{\mathrm{cap}} = K_{\mathrm{soil}}\,[\min(h_{\mathrm{pond}} - \psi_{\mathrm{m}},"
                     r"\Delta h_{\mathrm{max}})/L_{\mathrm{top}} + 1]$", 0),
                    (r"$K_{\mathrm{soil}} = w_K\,K_{\mathrm{sat}} + (1 - w_K)\,K(\theta_{\mathrm{top}})$", 21),
                    (r"$K_{\mathrm{sat}}$  camada superficial, da tabela de solos", 20),
                    (r"$K(\theta_{\mathrm{top}})$  condutividade com o topo umedecido", 19),
                    (r"$\psi_{\mathrm{m}}$  carga matricial da camada superficial", 19),
                    (r"padrão: $L_{\mathrm{top}} = 0.05$ m, $\Delta h_{\mathrm{max}} = 1$ m, $w_K = 0.5$", 19),
                ],
            },
            {
                "title": "O armazenamento limita",
                "case": "lençol freático raso",
                "verdict": (r"$i = i_{\mathrm{store}}$", "o que ainda cabe"),
                "lines": [
                    (r"$i_{\mathrm{store}} = S_{\mathrm{uz,rem}}\,/\,\Delta t_{\mathrm{h}}$", 0),
                    (r"$S_{\mathrm{uz,rem}} = \max(S_{\mathrm{uz,max}} - S_{\mathrm{uz}},0)$", 21),
                    (r"$S_{\mathrm{uz,max}} = z_{\mathrm{wt}}\,(\theta_{\mathrm{sat}} - \theta_{\mathrm{r}})$", 20),
                    (r"$z_{\mathrm{wt}}$  profundidade do lençol", 19),
                    ("freático; menos espaço se", 17),
                    (r"ele sobe; sem espaço, $i = 0$", 18),
                ],
            },
        ],
        "layers": ["superficial", "zona radicular", "transmissão", "saturado"],
        "rain": "chuva fraca",
        "low_k": r"$K_{\mathrm{sat}}$ baixo",
        "routed": "roteada",
        "notes": [
            ("O que não infiltra",
             [r"$d_{\mathrm{eff}} - i\,\Delta t_{\mathrm{h}}$ fica na superfície",
              r"como $d$ e é roteado para as",
              "células vizinhas"]),
            ("O que infiltra",
             ["enche primeiro a camada superficial, depois a",
              "zona radicular, por fim a camada de transmissão"]),
            ("Sem infiltração",
             ["em células impermeáveis e",
              "com o lençol freático na",
              r"superfície, $z_{\mathrm{wt}} \leq 0$"]),
        ],
    },
    "es": {
        "eq_sep": r"$,\ \ \qquad$",
        "eq_terms": ["suministro", "capacidad", "almacenamiento"],
        "panels": [
            {
                "title": "El suministro limita",
                "case": "lluvia débil sobre suelo seco",
                "verdict": (r"$i = i_{\mathrm{sup}}$", "toda el agua entra"),
                "lines": [
                    (r"$i_{\mathrm{sup}} = d_{\mathrm{eff}}\,/\,\Delta t_{\mathrm{h}}$", 0),
                    (r"$d_{\mathrm{eff}}$  agua en la superficie,", 21),
                    ("con la lluvia de este paso,", 17),
                    ("o el throughfall del dosel,", 17),
                    ("y la fusión de la nieve", 17),
                    (r"$\Delta t_{\mathrm{h}}$  paso de tiempo (h)", 19),
                ],
            },
            {
                "title": "La capacidad limita",
                "case": "lámina alta sobre suelo de baja conductividad",
                "verdict": (r"$i = I_{\mathrm{cap}}$", "lo que el suelo deja pasar"),
                "lines": [
                    (r"$I_{\mathrm{cap}} = K_{\mathrm{soil}}\,[\min(h_{\mathrm{pond}} - \psi_{\mathrm{m}},"
                     r"\Delta h_{\mathrm{max}})/L_{\mathrm{top}} + 1]$", 0),
                    (r"$K_{\mathrm{soil}} = w_K\,K_{\mathrm{sat}} + (1 - w_K)\,K(\theta_{\mathrm{top}})$", 21),
                    (r"$K_{\mathrm{sat}}$  capa superficial, de la tabla de suelos", 20),
                    (r"$K(\theta_{\mathrm{top}})$  conductividad de la capa humedecida", 19),
                    (r"$\psi_{\mathrm{m}}$  carga matricial de la capa superficial", 19),
                    (r"por defecto $L_{\mathrm{top}} = 0.05$ m, $\Delta h_{\mathrm{max}} = 1$ m, $w_K = 0.5$", 19),
                ],
            },
            {
                "title": "El almacenamiento limita",
                "case": "nivel freático somero",
                "verdict": (r"$i = i_{\mathrm{store}}$", "lo que aún cabe"),
                "lines": [
                    (r"$i_{\mathrm{store}} = S_{\mathrm{uz,rem}}\,/\,\Delta t_{\mathrm{h}}$", 0),
                    (r"$S_{\mathrm{uz,rem}} = \max(S_{\mathrm{uz,max}} - S_{\mathrm{uz}},0)$", 21),
                    (r"$S_{\mathrm{uz,max}} = z_{\mathrm{wt}}\,(\theta_{\mathrm{sat}} - \theta_{\mathrm{r}})$", 20),
                    (r"$z_{\mathrm{wt}}$  profundidad del nivel", 19),
                    ("freático: menos espacio si", 17),
                    (r"sube; sin espacio, $i = 0$", 18),
                ],
            },
        ],
        "layers": ["superficial", "zona de raíces", "transmisión", "saturado"],
        "rain": "lluvia débil",
        "low_k": r"$K_{\mathrm{sat}}$ bajo",
        "routed": "enrutada",
        "notes": [
            ("Lo que no se infiltra",
             [r"$d_{\mathrm{eff}} - i\,\Delta t_{\mathrm{h}}$ queda en",
              r"la superficie como $d$ y se",
              "enruta a las celdas vecinas"]),
            ("Lo que se infiltra",
             ["llena primero la capa superficial, después la",
              "zona de raíces y luego la capa de transmisión"]),
            ("Sin infiltración",
             ["en celdas impermeables y",
              "con el nivel freático en la",
              r"superficie, $z_{\mathrm{wt}} \leq 0$"]),
        ],
    },
}
MATH = {
    "d_eff": r"$d_{\mathrm{eff}}$",
    "i": r"$i$",
    "h_pond": r"$h_{\mathrm{pond}}$",
    "l_top": r"$L_{\mathrm{top}}$",
    "psi": r"$\psi_{\mathrm{m}}$",
    "z_wt": r"$z_{\mathrm{wt}}$",
}

# --- colours ---------------------------------------------------------------------------------
SOIL = [color("slot_near_surface"), color("slot_root_zone"), color("slot_transmission")]
SATURATED = color("slot_wet_even")
SURFACE_WATER = oklch_hex(0.72, 0.090, 245)  # ponded water d, as in cell_water_budget and snow
VERDICT_FILL = color("deep_fill")

# --- layout (px, y downward) -----------------------------------------------------------------
W, H = 760, 576
PANELS = [(14, 215), (225, 535), (545, 746)]   # x0, x1 of the three case panels
PANEL_Y0 = 74
PAD = 10
BW = 110                                       # soil block width, the same cell in every case
BLOCK_X0 = [58, 290, 582]                      # left edge of each soil block
G = 184                                        # ground surface
LAYER_Y = [G, G + 16, G + 54, G + 90]          # tops of near surface, root zone, transmission; deep table
BASE = G + 114                                 # soil base (bedrock below)
POND = [3, 36, 22]                             # surface water depth drawn in each case, px
TABLE = [G + 90, G + 90, G + 24]               # water table in each case
TABLE_SYMBOL_DX = [80, 80, 40]                 # water-table symbol, from the block's left edge
ARROW_DX = 88                                  # infiltration arrow, from the block's left edge
VERDICT_Y = BASE + 36
LINES_Y = VERDICT_Y + 36
PANEL_Y1 = LINES_Y + 98 + 14                   # the longest panel text is 98 px of steps
NOTES_Y = PANEL_Y1 + 22
EQ_SIZE, EQ_Y = 15, 32

# Sources of every element. DOCS = docs/theory/hydrologic-model.md. "Code" names what the
# model code does where the docs say less or differ.
FACTS = {
    "shared equation i = min(i_sup, I_cap, i_store); three simultaneous limits": "DOCS 4, 4.6",
    "names under the terms: supply, capacity, storage": "DOCS 4.6 (supply-, capacity- and storage-limited)",
    "i_sup = d_eff / dt_h; dt_h the time step in hours": "DOCS 4.6",
    "d_eff = surface water plus this step's rain (or the throughfall with the canopy on) plus melt":
        "DOCS 2.5, 5.1, 5.7; code: the melt joins the throughfall before infiltration",
    "a supply-limited step takes all of d_eff ('all the water enters')": "code",
    "I_cap = K_soil [min(h_pond - psi_m, dh_max)/L_top + 1]": "DOCS 4.5; code: times the pervious fraction",
    "K_soil = w_K K_sat + (1 - w_K) K(theta_top); theta_top after a trial wetting": "DOCS 4.5",
    "K(theta) = K_sat K_r (van Genuchten-Mualem)": "DOCS 4.4",
    "K_sat of the near-surface layer, from the soil table (base K_sat times its multiplier)":
        "DOCS 4 (layer multipliers); docs/inputs/parameter-tables.md",
    "psi_m matric head of the near-surface layer; 0 near saturation":
        "DOCS 4.3; code: from the near-surface store, not all of S_uz",
    "defaults L_top = 0.05 m, dh_max = 1 m, w_K = 0.5": "DOCS 4.5 (w_K default not given); code defaults",
    "L_top bracket spans the near-surface layer": "code: the near-surface thickness is L_top",
    "h_pond bracket on the ponded depth": "DOCS 4.5",
    "i_store = S_uz,rem / dt_h": "DOCS 4.6",
    "S_uz,rem = max(S_uz,max - S_uz, 0); S_uz,max = z_wt (theta_sat - theta_r)":
        "DOCS 4.1; code: times the pervious fraction, z_wt capped at the soil depth",
    "z_wt depth to the water table; a rising table leaves less room": "DOCS 4.1",
    "with no room left, i = 0": "DOCS 4.1, 4.6; docs/theory/layered-subsurface.md",
    "soil column: near surface, root zone, transmission above the table, saturated below":
        "DOCS 4 (layered vadose structure); figures/layered_column.py (colours, symbol)",
    "shallow table truncates the root zone (case 3)": "DOCS 4 (fallback rules)",
    "what does not infiltrate stays on the surface as d and is routed to the neighbour cells":
        "DOCS 1, 2.5",
    "what infiltrates fills the near-surface layer, then root zone, then transmission": "DOCS 4.7",
    "no infiltration on impervious cells or where z_wt <= 0": "DOCS 4.6",
    "colours: soil roles slot_near_surface/root_zone/transmission, slot_wet_even, water, ground":
        "figures/palette.py; SURFACE_WATER = oklch(0.72, 0.090, 245) from cell_water_budget.py",
}


def main(preview: Path | None = None) -> None:
    for lang in LABELS:
        draw(lang, preview)


def draw(lang: str, preview: Path | None = None) -> None:
    T = LABELS[lang]
    _ARROWS.clear()  # fig_check keeps the arrows of every sheet; check this one only
    s = Sheet(W, H, "infiltration-limits")
    ax = s.ax
    R = RendererAgg(W, H, 100)

    def flow(points, **kw):
        """Liquid-water ribbon, as in cell_water_budget."""
        kw.setdefault("width", (1.2, 3.8))
        kw.setdefault("head", (12, 11))
        with track(ax):
            s.arrow(points, c=WATER, **kw)

    def bracket_right(x, y0, y1, label, tick=5):
        """Right-hand bracket, ticks pointing back to the block, label to its right."""
        s.line([x - tick, x, x, x - tick], [y0 + 1, y0 + 1, y1 - 1, y1 - 1], c=SOFT, lw=1.0, z=5)
        return s.text(x + 6, (y0 + y1) / 2, label, size=10)

    def raindrop(x, y, r=2.6):
        """Teardrop: pointed top at y - 2.6 r, round bottom centred on y."""
        a = np.linspace(-0.25 * np.pi, 1.25 * np.pi, 24)
        arc = np.column_stack([x + r * np.cos(a), y + r * np.sin(a)])[::-1]
        ax.add_patch(Polygon(np.vstack([[(x, y - 2.6 * r)], arc]), closed=True, facecolor=WATER,
                             edgecolor="none", zorder=6))

    def water_table_symbol(x, y):
        ax.add_patch(Polygon([(x - 8, y - 11), (x + 8, y - 11), (x, y - 1)], closed=True,
                             facecolor=WATER, edgecolor="none", zorder=6))
        s.line([x - 7, x + 7], [y + 5, y + 5], c=WATER, lw=1.2, z=6)
        s.line([x - 4, x + 4], [y + 9, y + 9], c=WATER, lw=1.2, z=6)

    def soil_column(k):
        """One cell: surface water, the vadose layers above the table, saturated soil below."""
        x0, x1 = BLOCK_X0[k], BLOCK_X0[k] + BW
        table = TABLE[k]
        tops = LAYER_Y[:3] + [BASE]
        for j in range(3):
            top, bot = tops[j], min(tops[j + 1], table)
            if bot > top:
                ax.add_patch(Rectangle((x0, top), BW, bot - top, facecolor=SOIL[j], lw=0, zorder=2))
        ax.add_patch(Rectangle((x0, table), BW, BASE - table, facecolor=SATURATED, lw=0, zorder=2))
        ax.add_patch(Rectangle((x0, G - POND[k]), BW, POND[k], facecolor=SURFACE_WATER, lw=0, zorder=2))
        ax.add_patch(Rectangle((x0, BASE), BW, 10, facecolor=color("card"),
                               edgecolor=color("bedrock_hatch"), hatch="////", lw=0, zorder=2))
        ax.add_patch(Rectangle((x0, G), BW, BASE - G, fill=False, edgecolor=color("guide"), lw=0.8, zorder=3))
        s.line([x0, x1], [G, G], c=color("ground"), lw=2.4, z=4)
        s.line([x0, x1], [table, table], c=WATER, lw=2.0, z=4)
        s.line([x0, x1], [BASE, BASE], c=INK, lw=2.0, z=4)
        water_table_symbol(x0 + TABLE_SYMBOL_DX[k], table)
        return x0, x1

    # --- the shared equation, the name of each limit under its term --------------------------
    eq_parts = [T["eq_sep"] if p is None else p for p in EQ_TERMS]
    widths = [fk.width(s, p, size=EQ_SIZE) for p in eq_parts]
    x = W / 2 - sum(widths) / 2
    term_x = []
    for k, (part, w) in enumerate(zip(eq_parts, widths)):
        piece = s.text(x, EQ_Y + fk.baseline_offset(EQ_SIZE), part, size=EQ_SIZE, va="baseline")
        if k in (1, 3, 5):
            bb = piece.get_window_extent(R)
            term_x.append((bb.x0 + bb.x1) / 2)
        x += w
    for tx, word in zip(term_x, T["eq_terms"]):
        s.text(tx, 57, word, c=SOFT, ha="center")

    # --- the three cases ----------------------------------------------------------------------
    for k, ((px0, px1), panel) in enumerate(zip(PANELS, T["panels"])):
        s.box(px0, PANEL_Y0, px1 - px0, PANEL_Y1 - PANEL_Y0, fill=color("card"), edge=color("card_edge"),
              radius=7, lw=1.0, z=1)
        tx0 = px0 + PAD + 2
        fk.text(s, tx0, PANEL_Y0 + 20, panel["title"], bold=True, size=10.5, room=px1 - PAD - tx0)
        fk.text(s, tx0, PANEL_Y0 + 38, panel["case"], c=SOFT, room=px1 - PAD - tx0)

        x0, x1 = soil_column(k)
        ax_x = x0 + ARROW_DX
        flow([(ax_x, G - POND[k] + 1), (ax_x, min(G + 30, TABLE[k] - 4))])
        s.text(ax_x + 9, G + 10, MATH["i"], size=10)

        # verdict
        sym, words = panel["verdict"]
        w_sym = fk.width(s, sym, size=11)
        w_words = fk.width(s, words)
        vw = w_sym + w_words + 30
        if vw > px1 - px0 - 12:
            print(f"verdict {words!r}: {vw:.0f} px in a panel of {px1 - px0} px")
        vx = (px0 + px1) / 2 - vw / 2
        s.box(vx, VERDICT_Y - 12, vw, 24, fill=VERDICT_FILL, edge=WATER, radius=12, lw=1.0, z=3)
        s.text(vx + 11, VERDICT_Y + fk.baseline_offset(11), sym, size=11, va="baseline")
        s.text(vx + 19 + w_sym, VERDICT_Y, words)

        # definition and sources
        y = LINES_Y
        for line, step in panel["lines"]:
            y += step
            fk.text(s, px0 + PAD, y, line, room=px1 - px0 - 2 * PAD)
        if y - LINES_Y > 98:
            print(f"panel {k + 1} text runs {y - LINES_Y} px, more than the 98 px of the panel")

    # Case 1: light rain on a thin film, every layer named.
    x0 = BLOCK_X0[0]
    for xd, yd in ((x0 + 12, G - 36), (x0 + 28, G - 18), (x0 + 42, G - 40)):
        raindrop(xd, yd)
    fk.text(s, x0 + 54, G - 30, T["rain"], room=PANELS[0][1] - PAD - (x0 + 54))
    s.text(x0 + BW + 8, G - 3, MATH["d_eff"], size=10)
    for j, label in enumerate(T["layers"]):
        yy = [G + 8, G + 40, G + 70, G + 103][j]
        room = ARROW_DX - 6 - 6 if j == 0 else BW - 12   # the arrow crosses the near-surface layer
        fk.text(s, x0 + 6, yy, label, size=9, c=SOFT if j == 3 else INK, room=room)

    # Case 2: a deep pond; the terms of I_cap on the drawing; the rest is routed.
    x0 = BLOCK_X0[1]
    bracket_right(x0 + BW + 10, G - POND[1], G, MATH["h_pond"])
    bracket_right(x0 + BW + 10, G, LAYER_Y[1], MATH["l_top"])
    s.text(x0 + 6, G + 8, MATH["psi"], size=10)
    s.text(x0 + 6, G + 35, T["low_k"])
    flow([(x0 + 64, G - 13), (x0 + 20, G - 13), (x0 - 40, G - 13)])
    s.text(x0 - 40, G - POND[1] - 11, T["routed"])

    # Case 3: the water table near the surface leaves a thin unsaturated zone.
    x0 = BLOCK_X0[2]
    bracket_right(x0 + BW + 10, G, TABLE[2], MATH["z_wt"])
    s.text(x0 + 6, G + 70, T["layers"][3], size=9, c=SOFT)
    flow([(x0 + 64, G - 10), (x0 + 20, G - 10), (x0 - 26, G - 10)])
    s.text(x0 - 26, G - POND[2] - 11, T["routed"])

    # Pieces of the shared equation touch by design.
    quiet = {(a[:28], b[:28]) for a, b in zip(eq_parts, eq_parts[1:])}

    # --- bottom notes -------------------------------------------------------------------------
    for (px0, px1), (heading, lines) in zip(PANELS, T["notes"]):
        fk.text(s, px0 + PAD, NOTES_Y, heading, bold=True, size=10, room=px1 - px0 - 2 * PAD)
        for i, line in enumerate(lines):
            fk.text(s, px0 + PAD, NOTES_Y + 20 + 17 * i, line, room=px1 - px0 - 2 * PAD)

    print(lang, end=": ")
    report(s, quiet_pairs=quiet)
    print(s.save(STATIC / "theory", lang, preview))


if __name__ == "__main__":
    main(Path(sys.argv[1]) if len(sys.argv) > 1 else None)
