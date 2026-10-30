"""Build-up, wash-off and transport, for docs/theory/water-quality-model.md.

1  Build-up in dry weather sets the starting mass B_0 of every cell (illustrative curve).
2  Wash-off: each face k that water leaves through carries W_out,k = C3 Q_k^C4 B_t. On the
   Voronoi mesh the faces are the edges a cell drains through.
3  Transport: pollutant mass moves between cells through the same faces as the water and
   leaves the domain through the boundary faces (export at the outlet).

Follows the mass-based branch the code runs (flag_wq_model = 0), on the regular grid and
on the Voronoi mesh. A workbook gives ADD and min_Bt, in g/m2, which the model divides
by 1000 to get b_min in kg/m2.

Run from the repository root:

    python3 figures/water_quality.py [preview-folder] [--check]

Output: static/img/theory/water-quality.svg (en), water-quality.pt.svg and
water-quality.es.svg, plus a PNG of each in the preview folder when one is given.
--check prints the text boxes that overlap each other or leave the card.
"""

from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
from matplotlib.backends.backend_agg import FigureCanvasAgg
from matplotlib.patches import Circle, Rectangle

from site_style import INK, SOFT, STATIC, WATER, Sheet, color

# --- text ----------------------------------------------------------------------------------
_P1_EQ = r"$B_0 = C_1\,[\,1 - \exp(-C_2\,\mathrm{ADD})\,]$"
_P2_EQ = r"$W_{\mathrm{out},k} = C_3\, Q_k^{\,C_4}\, B_t$"
_BALANCE = [r"$W_{\mathrm{out,tot}} = \sum_k W_{\mathrm{out},k}$"
            r"$\qquad W_{\mathrm{in}} = \sum_k W_{\mathrm{in},k}$",
            r"$dW = W_{\mathrm{out,tot}} - W_{\mathrm{in}}$"
            r"$\qquad B_t^{\,t+\Delta t} = B_t^{\,t} - dW\,\Delta t$"]
_C_OUT = r"$C_{\mathrm{out}} = \sum W_{\mathrm{out,outlet}}\ /\ \sum Q_{\mathrm{outlet}}$"
_C_CELL = r"$C = W_{\mathrm{out,tot}}\ /\ Q_{\mathrm{tot}}$"
_B_RULE = r"$b = B_t / A_{\mathrm{cell}} < b_{\min}$"
_FLAG = r"$\mathtt{flag\_wq\_model} = 0$"
_MIN_BT = r"$\mathtt{min\_Bt}$"
_B_MIN = r"$b_{\min} = \mathtt{min\_Bt}/1000$"

LABELS = {
    "en": {
        "p1_title": "1  Build-up in dry weather",
        "p1_lines": [r"$C_1$: maximum build-up (kg/ha); $C_2$: rate (per day),",
                     "both per land cover; ADD: antecedent dry days"],
        "p1_y": "mass on the surface",
        "p1_dry": "dry days",
        "p1_run": "the run",
        "p1_storm": "storm",
        "p1_wash": "wash-off",
        "p1_illus": "illustration",
        "p1_notes": [r"a map of initial mass can replace $B_0$;",
                     "no build-up is added during the run"],
        "p2_title": "2  Wash-off from a cell",
        "p2_eq_note": [r"for each face $k$ with outflow $Q_k$: the four faces",
                       "of a grid cell, or every edge of a Voronoi cell"],
        "p2_lines": [r"$B_t$: mass in the cell (kg)",
                     r"$C_3$, $C_4$: wash-off",
                     "coefficient and exponent",
                     "of the land cover",
                     "no wash-off while",
                     _B_RULE],
        "p3_title": "3  Transport between cells and export at the outlet",
        "p3_outlet": "outlet",
        "p3_export": "export",
        "p3_key_flux": r"pollutant flux $W$ through a face",
        "p3_key_mass": r"mass $B_t$ in the cell, low to high",
        "p3_key_illus": "illustration",
        "p3_balance_title": "Mass balance of every cell, every time step",
        "p3_substeps": ["the step is split into sub-steps when a cell would",
                        "lose more mass than it holds, so no mass turns negative"],
        "p3_outlet_title": "At the outlet",
        "p3_outlet_lines": [_C_OUT + ", in mg/L",
                            "and in each cell " + _C_CELL + ", in mg/L"],
        "footer": ["mass-based formulation, " + _FLAG,
                   "workbook: ADD, " + _MIN_BT + r" in g/m$^2$; " + _B_MIN],
    },
    "pt": {
        "p1_title": "1  Acúmulo em tempo seco",
        "p1_lines": [r"$C_1$, $C_2$: acúmulo máximo (kg/ha) e taxa (por dia),",
                     "por cobertura do solo; ADD: dias secos antecedentes"],
        "p1_y": "massa na superfície",
        "p1_dry": "dias secos",
        "p1_run": "a simulação",
        "p1_storm": "chuva",
        "p1_wash": "lavagem",
        "p1_illus": "ilustração",
        "p1_notes": [r"um mapa de massa inicial pode substituir $B_0$;",
                     "nenhum acúmulo é somado durante a simulação"],
        "p2_title": "2  Lavagem de uma célula",
        "p2_eq_note": [r"para cada face $k$ com vazão de saída $Q_k$: as quatro",
                       "faces da célula da grade ou cada aresta da malha"],
        "p2_lines": [r"$B_t$: massa na célula (kg)",
                     r"$C_3$, $C_4$: coeficiente",
                     "e expoente de lavagem",
                     "da cobertura do solo",
                     "sem lavagem enquanto",
                     _B_RULE],
        "p3_title": "3  Transporte entre células e exportação no exutório",
        "p3_outlet": "exutório",
        "p3_export": "exportação",
        "p3_key_flux": r"fluxo de poluente $W$ por uma face",
        "p3_key_mass": r"massa $B_t$ na célula, de baixa a alta",
        "p3_key_illus": "ilustração",
        "p3_balance_title": "Balanço de massa de cada célula, a cada passo",
        "p3_substeps": ["o passo é dividido em subpassos quando uma célula",
                        "perderia mais massa do que tem; nenhuma fica negativa"],
        "p3_outlet_title": "No exutório",
        "p3_outlet_lines": [_C_OUT + ", em mg/L",
                            "e em cada célula " + _C_CELL + ", em mg/L"],
        "footer": ["formulação baseada em massa, " + _FLAG,
                   "planilha: ADD, " + _MIN_BT + r" em g/m$^2$; " + _B_MIN],
    },
    "es": {
        "p1_title": "1  Acumulación en tiempo seco",
        "p1_lines": [r"$C_1$, $C_2$: acumulación máxima (kg/ha) y tasa (por día),",
                     "por cobertura del suelo; ADD: días secos antecedentes"],
        "p1_y": "masa en la superficie",
        "p1_dry": "días secos",
        "p1_run": "la simulación",
        "p1_storm": "tormenta",
        "p1_wash": "lavado",
        "p1_illus": "ilustración",
        "p1_notes": [r"un mapa de masa inicial puede reemplazar $B_0$;",
                     "no se añade acumulación durante la simulación"],
        "p2_title": "2  Lavado de una celda",
        "p2_eq_note": [r"para cada cara $k$ con caudal de salida $Q_k$: las cuatro",
                       "caras de una celda regular o cada arista de Voronoi"],
        "p2_lines": [r"$B_t$: masa en la celda (kg)",
                     r"$C_3$, $C_4$: coeficiente",
                     "y exponente de lavado",
                     "según la cobertura",
                     "sin lavado mientras",
                     _B_RULE],
        "p3_title": "3  Transporte entre celdas y exportación en la salida",
        "p3_outlet": "salida",
        "p3_export": "exportación",
        "p3_key_flux": r"flujo de contaminante $W$ a través de una cara",
        "p3_key_mass": r"masa $B_t$ en la celda, de baja a alta",
        "p3_key_illus": "ilustración",
        "p3_balance_title": "Balance de masa de cada celda, en cada paso",
        "p3_substeps": ["el paso se divide en subpasos cuando una celda",
                        "perdería más masa de la que tiene; ninguna queda negativa"],
        "p3_outlet_title": "En la salida",
        "p3_outlet_lines": [_C_OUT + ", en mg/L",
                            "y en cada celda " + _C_CELL + ", en mg/L"],
        "footer": ["formulación basada en masa, " + _FLAG,
                   "Excel: ADD, " + _MIN_BT + r" en g/m$^2$; " + _B_MIN],
    },
}

# --- colours (all from figures/palette.py) -----------------------------------------------
POLLUTANT = color("roots")              # brown token, used here for pollutant mass and flux
MASS_RAMP = [color("slot_rock_even"), color("slot_near_surface"), color("slot_root_zone"),
             color("slot_transmission")]  # the soil ramp, low to high mass
STORM = color("deep_fill")
WATER_ALPHA = 0.14

W, H = 760, 580
PAD = 14


def lerp_hex(stops, f):
    rgb = np.array([[int(c[i:i + 2], 16) for i in (1, 3, 5)] for c in stops]) / 255
    f = min(max(f, 0.0), 1.0) * (len(rgb) - 1)
    i = min(int(f), len(rgb) - 2)
    return tuple(rgb[i] + (rgb[i + 1] - rgb[i]) * (f - i))


def text_width(sh: Sheet, s: str, *, bold=False, size=9.5) -> float:
    """Width in px of a label, measured with the figure's renderer."""
    renderer = FigureCanvasAgg(sh.fig).get_renderer()
    t = sh.text(0, 0, s, bold=bold, size=size)
    width = t.get_window_extent(renderer).width
    t.remove()
    return width


def draw(lang: str, preview: Path | None = None, check: bool = False) -> Path:
    t = LABELS[lang]
    sh = Sheet(W, H, "water-quality")
    ax = sh.ax
    edge = color("card_edge")

    # ---------------- panel 1: build-up ----------------
    x0, y0, w1, h1 = 22, 22, 352, 278
    sh.box(x0, y0, w1, h1, fill="#ffffff", edge=edge)
    sh.text(x0 + PAD, y0 + 18, t["p1_title"], bold=True, size=10.5)
    sh.text(x0 + PAD, y0 + 44, _P1_EQ, size=10.5)
    for i, line in enumerate(t["p1_lines"]):
        sh.text(x0 + PAD, y0 + 66 + 17 * i, line)

    # Plot frame (px): dry days from xa to xb, the run from xb to xc.
    xa, xb, xc = 84, 232, 352
    yb0, yc1 = 236, 132                     # B = 0 and B = C1
    def ypix(frac):
        return yb0 - frac * (yb0 - yc1)
    ax.add_patch(Rectangle((xb, yc1 - 12), xc - xb, yb0 - yc1 + 12, facecolor=STORM,
                           edgecolor="none", zorder=2))
    sh.text((xb + xc) / 2, yc1 - 3, t["p1_storm"], ha="center", size=9, c=SOFT)
    # Axes.
    ax.plot([xa, xa, xc], [yc1 - 14, yb0, yb0], color=SOFT, linewidth=1.0, zorder=4)
    ax.plot([xa, xb], [yc1, yc1], color=SOFT, linewidth=0.9, linestyle=(0, (4, 3)), zorder=4)
    ax.plot([xb, xb], [yb0, yc1 - 12], color=SOFT, linewidth=0.9, linestyle=(0, (1.2, 2.4)), zorder=4)
    # Curves: B/C1 = 1 - exp(-C2 t) over 5 dry days (C2 = 0.6 per day), then an exponential
    # wash-off decay in the storm (shape only).
    td = np.linspace(0, 5, 80)
    bd = 1 - np.exp(-0.6 * td)
    ax.plot(xa + td / 5 * (xb - xa), ypix(bd), color=POLLUTANT, linewidth=2.0, zorder=6,
            solid_capstyle="butt")
    b0 = bd[-1]
    tr = np.linspace(0, 1, 60)
    br = b0 * np.exp(-1.3 * tr)
    ax.plot(xb + tr * (xc - 6 - xb), ypix(br), color=POLLUTANT, linewidth=2.0, zorder=6,
            solid_capstyle="butt")
    ax.add_patch(Circle((xb, ypix(b0)), 3.2, facecolor=POLLUTANT, edgecolor="none", zorder=7))
    sh.text(xa - 7, yc1, r"$C_1$", ha="right", size=10)
    sh.text(xb - 8, ypix(b0) + 14, r"$B_0$", ha="right", size=10)
    sh.text(xa - 7, yb0, "0", ha="right")
    sh.text(xa - 30, (yb0 + yc1) / 2, t["p1_y"], rotation=90, ha="center", size=9, c=SOFT)
    sh.text(xb, yb0 + 13, "ADD", ha="center")
    sh.text((xa + xb) / 2, yb0 + 13, t["p1_dry"], ha="center", c=SOFT)
    sh.text((xb + xc) / 2 + 8, yb0 + 13, t["p1_run"], ha="center", c=SOFT)
    sh.text(xb + 56, ypix(br[24]) - 12, t["p1_wash"], size=9.5)
    sh.text(xc - 2, ypix(0.12), t["p1_illus"], ha="right", size=9, c=SOFT)
    for i, line in enumerate(t["p1_notes"]):
        sh.text(x0 + PAD, yb0 + 36 + 17 * i, line)

    # ---------------- panel 2: wash-off from one cell ----------------
    x2, w2 = 386, 352
    sh.box(x2, y0, w2, h1, fill="#ffffff", edge=edge)
    sh.text(x2 + PAD, y0 + 18, t["p2_title"], bold=True, size=10.5)
    sh.text(x2 + PAD, y0 + 44, _P2_EQ, size=10.5)
    for i, line in enumerate(t["p2_eq_note"]):
        sh.text(x2 + PAD, y0 + 64 + 17 * i, line)

    cs = 66                                     # cell size (px)
    cx0, cy0 = x2 + 44, y0 + 126                # top-left corner of the centre cell
    stub = 28
    # Neighbourhood: dashed grid lines around the centre cell.
    for gx in (cx0, cx0 + cs):
        ax.plot([gx, gx], [cy0 - stub, cy0 + cs + stub], color=color("guide"), linewidth=0.8,
                linestyle=(0, (3, 2.5)), zorder=3)
    for gy in (cy0, cy0 + cs):
        ax.plot([cx0 - stub, cx0 + cs + stub], [gy, gy], color=color("guide"), linewidth=0.8,
                linestyle=(0, (3, 2.5)), zorder=3)
    ax.add_patch(Rectangle((cx0 - stub, cy0 - stub), cs + 2 * stub, cs + 2 * stub,
                           facecolor=WATER, alpha=WATER_ALPHA, edgecolor="none", zorder=2))
    ax.add_patch(Rectangle((cx0, cy0), cs, cs, facecolor=MASS_RAMP[2], edgecolor=INK,
                           linewidth=1.2, zorder=3))
    rng = np.random.default_rng(7)
    for px, py in rng.uniform(0.12, 0.88, size=(20, 2)):
        ax.add_patch(Circle((cx0 + px * cs, cy0 + py * cs), 1.9, facecolor=POLLUTANT,
                            edgecolor="none", zorder=4))
    sh.text(cx0 + cs / 2, cy0 + cs / 2, r"$B_t$", size=11, ha="center", z=11)
    ax.add_patch(Rectangle((cx0 + cs / 2 - 11, cy0 + cs / 2 - 9), 22, 18, facecolor=MASS_RAMP[2],
                           edgecolor="none", zorder=5))

    # Water (blue) and pollutant (brown) arrows: in from the left, out right and down.
    aw = dict(width=(1.1, 3.0), head=(10, 9))
    yq, yw = cy0 + 22, cy0 + 40
    sh.arrow([(cx0 - stub + 2, yq), (cx0 + 14, yq)], c=WATER, **aw, z=8)
    sh.arrow([(cx0 - stub + 2, yw), (cx0 + 14, yw)], c=POLLUTANT, **aw, z=8)
    sh.text(cx0 - stub / 2, cy0 - 13, r"$W_{\mathrm{in}}$", ha="center", size=10)
    sh.arrow([(cx0 + cs - 14, yq), (cx0 + cs + stub - 2, yq)], c=WATER, **aw, z=8)
    sh.arrow([(cx0 + cs - 14, yw), (cx0 + cs + stub - 2, yw)], c=POLLUTANT, **aw, z=8)
    sh.text(cx0 + cs + stub + 4, yq, r"$Q_k$", size=10, c=WATER)
    sh.text(cx0 + cs + stub + 4, yw + 2, r"$W_{\mathrm{out},k}$", size=10, c=POLLUTANT)
    xq, xw = cx0 + 24, cx0 + 42
    sh.arrow([(xq, cy0 + cs - 14), (xq, cy0 + cs + stub - 2)], c=WATER, **aw, z=8)
    sh.arrow([(xw, cy0 + cs - 14), (xw, cy0 + cs + stub - 2)], c=POLLUTANT, **aw, z=8)

    # Text beside the cell; it moves left when a long line would reach the panel edge.
    tx = x2 + min(196.0, w2 - 12 - max(text_width(sh, line) for line in t["p2_lines"]))
    for i, line in enumerate(t["p2_lines"]):
        sh.text(tx, cy0 - 16 + 18 * i + (8 if i >= 4 else 0), line)
    for i, line in enumerate(t["footer"]):
        sh.text(x2 + PAD, y0 + h1 - 16 - 17 * (len(t["footer"]) - 1 - i), line, c=SOFT)

    # ---------------- panel 3: transport and export ----------------
    y3, h3 = y0 + h1 + 12, H - (y0 + h1 + 12) - 22
    sh.box(x0, y3, W - 2 * x0, h3, fill="#ffffff", edge=edge)
    sh.text(x0 + PAD, y3 + 18, t["p3_title"], bold=True, size=10.5)

    ncol, nrow, g = 5, 3, 48
    gx0, gy0 = x0 + 26, y3 + 42
    mass = np.array([[0.20, 0.30, 0.40, 0.48, 0.55],
                     [0.32, 0.48, 0.64, 0.80, 0.95],
                     [0.18, 0.28, 0.38, 0.46, 0.52]])
    for r in range(nrow):
        for cidx in range(ncol):
            ax.add_patch(Rectangle((gx0 + cidx * g, gy0 + r * g), g, g,
                                   facecolor=lerp_hex(MASS_RAMP, mass[r, cidx]),
                                   edgecolor="#ffffff", linewidth=1.0, zorder=2))
    # Domain boundary, open at the outlet face (right face of the middle row).
    gx1, gy1 = gx0 + ncol * g, gy0 + nrow * g
    ax.plot([gx1, gx1, gx0, gx0, gx1, gx1], [gy0 + g, gy0, gy0, gy1, gy1, gy0 + 2 * g],
            color=INK, linewidth=1.6, solid_joinstyle="miter", zorder=5)
    fa = dict(width=(1.0, 2.8), head=(9, 8), c=POLLUTANT, z=8)
    for r in range(nrow):
        for cidx in range(ncol):
            xc_, yc_ = gx0 + (cidx + 0.5) * g, gy0 + (r + 0.5) * g
            if r == 1 and cidx < ncol - 1:
                sh.arrow([(xc_ + 6, yc_), (xc_ + g - 6, yc_)], **fa)
            if r == 0:
                sh.arrow([(xc_, yc_ + 6), (xc_, yc_ + g - 13)], **fa)
            if r == 2:
                sh.arrow([(xc_, yc_ - 6), (xc_, yc_ - g + 13)], **fa)
    # Export through the outlet face.
    yo = gy0 + 1.5 * g
    sh.arrow([(gx1 - g / 2 + 6, yo), (gx1 + 40, yo)], width=(1.6, 4.4), head=(12, 11),
             c=POLLUTANT, z=8)
    sh.text(gx1 + 6, yo - 15, t["p3_export"])
    sh.text(gx1 + 6, gy0 + 2 * g + 12, t["p3_outlet"], c=SOFT)

    # Key under the grid.
    ky = gy1 + 22
    sh.arrow([(gx0, ky), (gx0 + 26, ky)], **fa)
    sh.text(gx0 + 34, ky, t["p3_key_flux"])
    ky2 = ky + 20
    for k in range(30):
        ax.add_patch(Rectangle((gx0 + k * 26 / 30, ky2 - 5), 26 / 30 + 0.3, 10,
                               facecolor=lerp_hex(MASS_RAMP, k / 29), edgecolor="none", zorder=3))
    sh.text(gx0 + 34, ky2, t["p3_key_mass"])
    sh.text(gx1 + 6, gy0 + 8, t["p3_key_illus"], size=9, c=SOFT)

    # Equations column.
    ex = x0 + 352
    ey = gy0 + 4
    sh.text(ex, ey, t["p3_balance_title"], bold=True, size=10)
    ey += 25
    for line in _BALANCE:
        sh.text(ex, ey, line, size=10)
        ey += 26
    for line in t["p3_substeps"]:
        sh.text(ex, ey - 4, line)
        ey += 17
    ey += 16
    sh.text(ex, ey, t["p3_outlet_title"], bold=True, size=10)
    ey += 23
    for line in t["p3_outlet_lines"]:
        sh.text(ex, ey, line, size=10)
        ey += 23

    if check:
        report(sh)
    svg = sh.save(STATIC / "theory", lang, preview)
    print("wrote", svg)
    return svg


def report(sh: Sheet) -> None:
    """List text boxes that overlap each other or leave the card."""
    renderer = FigureCanvasAgg(sh.fig).get_renderer()
    boxes = []
    for txt in sh.ax.texts:
        bb = txt.get_window_extent(renderer)
        x0, x1, y0, y1 = bb.x0, bb.x1, sh.H - bb.y1, sh.H - bb.y0
        boxes.append((txt.get_text(), x0, y0, x1, y1))
        if x0 < 10 or x1 > sh.W - 10 or y0 < 10 or y1 > sh.H - 10:
            print("OUTSIDE", txt.get_text()[:50], round(x0), round(y0), round(x1), round(y1))
        if x0 < 374 - 6 < x1 and y1 < 300 or 386 <= x0 and x1 > 738 - 8:
            print("PANEL", txt.get_text()[:50], round(x0), round(x1))
    for i, a in enumerate(boxes):
        for b in boxes[i + 1:]:
            if a[1] < b[3] and b[1] < a[3] and a[2] < b[4] and b[2] < a[4]:
                print("OVERLAP", repr(a[0][:40]), "|", repr(b[0][:40]))


def main(preview: Path | None = None, check: bool = False) -> None:
    for lang in LABELS:
        draw(lang, preview, check)


if __name__ == "__main__":
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    main(Path(args[0]) if args else None, check="--check" in sys.argv)
