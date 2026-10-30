"""The shared V-tilted catchment, for docs/validation/overview.md (Shared V-tilted catchment).

The canonical 20 m V-tilted raster drawn as an oblique (orthographic) block, its common
setting, and the validation cases that run on it.

Geometry comes from the canonical V-tilted static rasters of the MATLAB model (DEM, LULC,
SOIL, LAI, GW_table and DTB: 50 rows by 81 columns of 20 m). The lowest row of the DEM is
its north row (row 0), so the outlet is on the north edge: the two channel cells of row 0
(columns 40 and 41), with a normal-flow boundary of slope 0.02. The block is seen from in
front of that edge, 14 degrees to the right and 32 degrees above. The surface is drawn from
the DEM's own rule, z = 0.05 d + 0.02 y (d: distance from the channel edge, y: distance
from the north edge), with the relief exaggerated 8 times; the soil band on the front and
side faces is not to scale.

The grey tags on the right say which grid each case runs on. Several run on smaller grids
with the same three zones (left plane, channel, right plane), not on this raster.

Run from the repository root:

    python3 figures/vtilted_catchment.py [preview-folder]

Output: static/img/validation/vtilted-catchment.svg (en), vtilted-catchment.pt.svg and
vtilted-catchment.es.svg, and a PNG of each in the preview folder, if given.
"""

from __future__ import annotations

import sys
import warnings
from pathlib import Path

import numpy as np
from matplotlib import patheffects
from matplotlib.backends.backend_agg import RendererAgg
from matplotlib.patches import Polygon, Rectangle

sys.dont_write_bytecode = True
sys.path.insert(0, str(Path(__file__).resolve().parent))
import fig_check  # noqa: E402
import flow_kit as fk  # noqa: E402
from fig_check import report, track  # noqa: E402
from site_style import INK, SOFT, STATIC, WATER, Sheet, color, hex_of, oklch_hex  # noqa: E402

W, H = 760, 620
NAME = "vtilted-catchment"
B, L = True, False

# --- labels ------------------------------------------------------------------------------------
LABELS = {
    "en": {
        "title": "The shared V-tilted catchment",
        "subtitle": "a synthetic 20 m test domain used by many validation cases",
        # drawing
        "left_plane": "left plane",
        "right_plane": "right plane",
        "channel": "channel",
        "cross_slope": "0.05",
        "along_slope": "0.02",
        "w_left": "800 m, 40 cells",
        "w_channel": "40 m, 2 cells",
        "w_right": "780 m, 39 cells",
        "length": "1000 m, 50 cells",
        "outlet": [[("Outlet", B), (", north edge", L)], "normal flow,", "slope 0.02"],
        "closed": "closed edges",
        "notes_under": ["20 m cells; relief exaggerated 8 times; contours every 10 m;",
                        "planes and channel fall 0.02 north, toward the outlet"],
        # setting card
        "setting": "Common setting",
        "zone_heads": ("left", "channel", "right"),
        "rows": [
            ("soil and land-cover class", ("1", "2", "3")),
            ("leaf area index, LAI", ("0.5", "0", "2.0")),
            (r"Manning $n$, benchmark", ("0.015", "0.15", "0.015")),
        ],
        "column": [("0.5 m", "water table, below the surface"), ("1 m", "bedrock, below the surface")],
        "notes": [
            [("Soil  ", B), ("properties set by each case", L)],
            [("Benchmark storm  ", B), ("10.8 mm/h for 90 min,", L)],
            [("", L), ("then dry to 180 min; losses off", L)],
        ],
        # case list
        "cases": "Cases that use it",
        "blocks": [
            ("Hydrologic modules", [
                {"name": "Canopy interception", "ids": "VAL-CANOPY-001", "more": [],
                 "tag": None, "status": "ok",
                 "line": ["store, throughfall and evaporation in one cell per zone,",
                          "against an independent bucket"]},
                {"name": "Snow", "ids": "VAL-SNOW-001", "more": [], "tag": None, "status": "ok",
                 "line": "a coupled snow and runoff event closes its ledger"},
                {"name": "Infiltration", "ids": "VAL-INFIL-VT-000 to 006", "more": [],
                 "tag": "81 × 50", "status": "ok",
                 "line": "seven regimes, against an independent reference"},
                {"name": "Evapotranspiration", "ids": "VAL-ET-VT-000 to 006", "more": [],
                 "tag": "3 × 3", "status": "ok",
                 "line": "potential and actual ET, against independent references"},
            ]),
            ("Groundwater and recharge", [
                {"name": "Local groundwater", "ids": None,
                 "more": ["VAL-GW-ASYNC-001, VAL-GW-ASYNC-002,", "VAL-GW-CAP-001, VAL-GW-MOUND-001"],
                 "tag": "3 × 3, 7 × 7", "status": "ok",
                 "line": r"rise $\Delta h = R\,\Delta t/S_y$, scheduler, capillary rise, mound"},
                {"name": "Layered subsurface", "ids": "no case ID", "more": [],
                 "tag": "2 × 2, step", "status": "ctl",
                 "line": "full-model runs close mass; Python and MATLAB agree"},
            ]),
            ("Hydrodynamics and routing", [
                {"name": "Symmetry and conservation", "ids": None,
                 "more": [("VAL-HYDRO-FM-VTILT-001", "VAL-ROUTE-KIN-001"),
                          ("VAL-HYDRO-LI-VTILT-001", "VAL-ROUTE-DIFF-001"),
                          ("VAL-HYDRO-CA-VTILT-001", "")],
                 "tag": "31 × 41", "status": "ok",
                 "line": "five routing families: equal halves, volume conserved"},
                {"name": "Benchmark hydrograph", "ids": "no case ID", "more": [],
                 "tag": "81 × 50", "status": None,
                 "line": "five families: outlet hydrograph against the benchmark"},
                {"name": "Gauges, case workbook", "ids": "MATLAB checks", "more": [],
                 "tag": None, "status": "ctl",
                 "line": "cross-section discharge; same results from both layouts"},
            ]),
        ],
        "key": [("ok", "validated"), ("ctl", "controlled tests"), ("tag", "grid it runs on")],
    },
    "pt": {
        "title": "A bacia sintética em V",
        "subtitle": "um domínio de teste sintético de 20 m, usado por muitos casos de validação",
        "left_plane": "encosta esquerda",
        "right_plane": "encosta direita",
        "channel": "canal",
        "cross_slope": "0,05",
        "along_slope": "0,02",
        "w_left": "800 m, 40 células",
        "w_channel": "40 m, 2 células",
        "w_right": "780 m, 39 células",
        "length": "1000 m, 50 células",
        "outlet": [[("Exutório", B), (", borda norte", L)], "fluxo normal,", "declividade 0,02"],
        "closed": "bordas fechadas",
        "notes_under": ["relevo exagerado 8 vezes; curvas de nível a cada 10 m;",
                        "encostas e canal descem 0,02 rumo ao exutório, ao norte"],
        "setting": "Configuração comum",
        "zone_heads": ("esquerda", "canal", "direita"),
        "rows": [
            ("classe de solo e cobertura", ("1", "2", "3")),
            ("índice de área foliar, IAF", ("0,5", "0", "2,0")),
            (r"Manning $n$, benchmark", ("0,015", "0,15", "0,015")),
        ],
        "column": [("0,5 m", "lençol freático, abaixo da superfície"),
                   ("1 m", "leito rochoso, abaixo da superfície")],
        "notes": [
            [("Solo  ", B), ("propriedades definidas por cada caso", L)],
            [("Chuva do benchmark  ", B), ("10,8 mm/h por 90 min,", L)],
            [("", L), ("seco até 180 min; sem perdas", L)],
        ],
        "cases": "Casos que a usam",
        "blocks": [
            ("Módulos hidrológicos", [
                {"name": "Interceptação pelo dossel", "ids": "VAL-CANOPY-001", "more": [],
                 "tag": None, "status": "ok",
                 "line": ["armazenamento, precipitação interna e evaporação",
                          "em uma célula por zona, contra um balde independente"]},
                {"name": "Neve", "ids": "VAL-SNOW-001", "more": [], "tag": None, "status": "ok",
                 "line": "um evento de neve e escoamento fecha o seu balanço"},
                {"name": "Infiltração", "ids": "VAL-INFIL-VT-000 a 006", "more": [],
                 "tag": "81 × 50", "status": "ok",
                 "line": "sete regimes, contra uma referência independente"},
                {"name": "Evapotranspiração", "ids": "VAL-ET-VT-000 a 006", "more": [],
                 "tag": "3 × 3", "status": "ok",
                 "line": "ET potencial e real, contra referências independentes"},
            ]),
            ("Águas subterrâneas e recarga", [
                {"name": "Águas subterrâneas locais", "ids": None,
                 "more": ["VAL-GW-ASYNC-001, VAL-GW-ASYNC-002,", "VAL-GW-CAP-001, VAL-GW-MOUND-001"],
                 "tag": "3 × 3, 7 × 7", "status": "ok",
                 "line": r"$\Delta h = R\,\Delta t/S_y$, agendamento, ascensão capilar, domo"},
                {"name": "Subsuperfície em camadas", "ids": "sem ID", "more": [],
                 "tag": "2 × 2, passo", "status": "ctl",
                 "line": "o modelo fecha a massa; Python e MATLAB concordam"},
            ]),
            ("Hidrodinâmica e roteamento", [
                {"name": "Simetria e conservação", "ids": None,
                 "more": [("VAL-HYDRO-FM-VTILT-001", "VAL-ROUTE-KIN-001"),
                          ("VAL-HYDRO-LI-VTILT-001", "VAL-ROUTE-DIFF-001"),
                          ("VAL-HYDRO-CA-VTILT-001", "")],
                 "tag": "31 × 41", "status": "ok",
                 "line": "cinco famílias: metades iguais, volume conservado"},
                {"name": "Hidrograma de referência", "ids": "sem ID", "more": [],
                 "tag": "81 × 50", "status": None,
                 "line": "cinco famílias contra o hidrograma de referência"},
                {"name": "Postos, planilha do caso", "ids": "verificações MATLAB", "more": [],
                 "tag": None, "status": "ctl",
                 "line": "vazão na seção; mesmos resultados nos dois formatos"},
            ]),
        ],
        "key": [("ok", "validado"), ("ctl", "testes controlados"), ("tag", "grade do caso")],
    },
    "es": {
        "title": "La cuenca sintética en V",
        "subtitle": "un dominio de prueba sintético de 20 m, usado por muchos casos de validación",
        "left_plane": "ladera izquierda",
        "right_plane": "ladera derecha",
        "channel": "canal",
        "cross_slope": "0,05",
        "along_slope": "0,02",
        "w_left": "800 m, 40 celdas",
        "w_channel": "40 m, 2 celdas",
        "w_right": "780 m, 39 celdas",
        "length": "1000 m, 50 celdas",
        "outlet": [[("Salida", B), (", borde norte", L)], "flujo normal,", "pendiente 0,02"],
        "closed": "bordes cerrados",
        "notes_under": ["relieve exagerado 8 veces; curvas de nivel cada 10 m;",
                        "laderas y canal bajan 0,02 al norte, hacia la salida"],
        "setting": "Configuración común",
        "zone_heads": ("izquierda", "canal", "derecha"),
        "rows": [
            ("clase de suelo y cobertura", ("1", "2", "3")),
            ("índice de área foliar, IAF", ("0,5", "0", "2,0")),
            (r"Manning $n$, benchmark", ("0,015", "0,15", "0,015")),
        ],
        "column": [("0,5 m", "nivel freático, bajo la superficie"),
                   ("1 m", "lecho rocoso, bajo la superficie")],
        "notes": [
            [("Suelo  ", B), ("propiedades fijadas por cada caso", L)],
            [("Lluvia de prueba  ", B), ("10,8 mm/h durante 90 min,", L)],
            [("", L), ("seco hasta 180 min; sin pérdidas", L)],
        ],
        "cases": "Casos que la usan",
        "blocks": [
            ("Módulos hidrológicos", [
                {"name": "Intercepción del dosel", "ids": "VAL-CANOPY-001", "more": [],
                 "tag": None, "status": "ok",
                 "line": ["almacenamiento, trascolación y evaporación en una",
                          "celda por zona, frente a un depósito independiente"]},
                {"name": "Nieve", "ids": "VAL-SNOW-001", "more": [], "tag": None, "status": "ok",
                 "line": "un evento de nieve y escorrentía cierra su balance"},
                {"name": "Infiltración", "ids": "VAL-INFIL-VT-000 a 006", "more": [],
                 "tag": "81 × 50", "status": "ok",
                 "line": "siete regímenes, frente a una referencia independiente"},
                {"name": "Evapotranspiración", "ids": "VAL-ET-VT-000 a 006", "more": [],
                 "tag": "3 × 3", "status": "ok",
                 "line": "ET potencial y real, frente a referencias independientes"},
            ]),
            ("Aguas subterráneas y recarga", [
                {"name": "Agua subterránea local", "ids": None,
                 "more": ["VAL-GW-ASYNC-001, VAL-GW-ASYNC-002,", "VAL-GW-CAP-001, VAL-GW-MOUND-001"],
                 "tag": "3 × 3, 7 × 7", "status": "ok",
                 "line": r"$\Delta h = R\,\Delta t/S_y$, programación, ascenso capilar, domo"},
                {"name": "Subsuelo en capas", "ids": "sin ID de caso", "more": [],
                 "tag": "2 × 2, paso", "status": "ctl",
                 "line": "el modelo cierra la masa; Python y MATLAB coinciden"},
            ]),
            ("Hidrodinámica y enrutamiento", [
                {"name": "Simetría y conservación", "ids": None,
                 "more": [("VAL-HYDRO-FM-VTILT-001", "VAL-ROUTE-KIN-001"),
                          ("VAL-HYDRO-LI-VTILT-001", "VAL-ROUTE-DIFF-001"),
                          ("VAL-HYDRO-CA-VTILT-001", "")],
                 "tag": "31 × 41", "status": "ok",
                 "line": "cinco familias: mitades iguales, volumen conservado"},
                {"name": "Hidrograma de referencia", "ids": "sin ID de caso", "more": [],
                 "tag": "81 × 50", "status": None,
                 "line": "cinco familias frente al hidrograma de referencia"},
                {"name": "Estaciones, libro del caso", "ids": "pruebas MATLAB", "more": [],
                 "tag": None, "status": "ctl",
                 "line": "caudal en la sección; ambos formatos coinciden"},
            ]),
        ],
        "key": [("ok", "validado"), ("ctl", "pruebas controladas"), ("tag", "malla del caso")],
    },
}

# --- colours ---------------------------------------------------------------------------------
SURFACE_WATER = oklch_hex(0.72, 0.090, 245)          # shared with other figures
ACCEPT_EDGE = color("ground")                       # status bar of a validated module
LEFT_FILL = color("slot_near_surface")              # zone 1
RIGHT_FILL = oklch_hex(0.870, 0.055, 118)            # new: zone 3, the plane with LAI 2.0
CHANNEL_FILL = SURFACE_WATER                         # zone 2
ZONE_FILLS = (LEFT_FILL, CHANNEL_FILL, RIGHT_FILL)
SOIL_FACE = color("slot_root_zone")
SOIL_SIDE = color("slot_transmission")
WET_FACE = color("slot_wet_even")
WET_SIDE = color("slot_wet_odd")
CONTOUR = color("text_soft")
TAG_FILL = hex_of("rock_b")
EDGE = color("card_edge")

# --- the catchment (metres), from the canonical DEM ------------------------------------------
X_LEFT, X_CH0, X_CH1, X_RIGHT = 0.0, 800.0, 840.0, 1620.0
Y_FRONT, Y_BACK = 0.0, 1000.0
CROSS, ALONG = 0.05, 0.02
EXAG = 8.0                    # vertical exaggeration of the relief
PHI, THETA = np.radians(14.0), np.radians(32.0)
BAND = 16.0                   # px: drawn thickness of the 1 m soil band (not to scale)

# --- layout (px) -----------------------------------------------------------------------------
DRAW_BOX = (42, 70, 370, 246)       # where the block (with its soil band) is fitted
CARD = (20, 386, 380, 606)          # x0, y0, x1, y1 of the setting card
LIST_X0, LIST_X1 = 396, 740         # case list column: status bar at x0, text from x0 + 10


def z_surface(x, y):
    d = np.where(x < X_CH0, X_CH0 - x, np.where(x > X_CH1, x - X_CH1, 0.0))
    return CROSS * d + ALONG * y


class Projection:
    """Orthographic view from in front of the outlet, 14 degrees to the right, 32 above."""

    def __init__(self, box):
        self.S, self.cx, self.cy = 1.0, 0.0, 0.0
        pts = np.array([self._raw(x, y, float(z_surface(np.array(x), np.array(y))))
                        for x in (X_LEFT, X_CH0, X_RIGHT) for y in (Y_FRONT, Y_BACK)])
        x0, y0, x1, y1 = box
        lo, hi = pts.min(axis=0), pts.max(axis=0)
        self.S = min((x1 - x0) / (hi[0] - lo[0]), (y1 - y0 - BAND) / (hi[1] - lo[1]))
        self.cx = x0 - self.S * lo[0] + ((x1 - x0) - self.S * (hi[0] - lo[0])) / 2
        self.cy = y0 + self.S * hi[1]

    @staticmethod
    def _raw(x, y, z):
        xs, ys, zs = x - 810.0, y - 500.0, EXAG * z
        sx = np.cos(PHI) * xs + np.sin(PHI) * ys
        su = -np.sin(PHI) * np.sin(THETA) * xs + np.cos(PHI) * np.sin(THETA) * ys + np.cos(THETA) * zs
        return float(sx), float(su)

    def __call__(self, x, y, z=None):
        if z is None:
            z = float(z_surface(np.array(x), np.array(y)))
        sx, su = self._raw(x, y, z)
        return np.array([self.cx + self.S * sx, self.cy - self.S * su])


def head(s, tip, direction, *, c=INK, size=(9.0, 7.5), z=8):
    """The site's notched head at tip, pointing along direction (screen px)."""
    d = np.asarray(direction, float)
    d /= np.linalg.norm(d)
    n = np.array([-d[1], d[0]])
    t = np.asarray(tip, float)
    ln, wd = size
    pts = [t, t - ln * d + wd / 2 * n, t - 0.62 * ln * d, t - ln * d - wd / 2 * n]
    s.ax.add_patch(Polygon(pts, closed=True, facecolor=c, edgecolor="none", zorder=z))


def slope_arrow(s, p0, p1, *, c=INK, lw=1.1, z=8):
    d = np.subtract(p1, p0)
    d = d / np.linalg.norm(d)
    end = np.asarray(p1) - 5.6 * d
    s.ax.plot([p0[0], end[0]], [p0[1], end[1]], color=c, linewidth=lw, solid_capstyle="butt", zorder=z)
    head(s, p1, d, c=c, z=z)


def dim_line(s, a, b, *, ticks=(), c=SOFT, z=7, tick=4.0):
    """Dimension line a-b with end and intermediate ticks perpendicular to it."""
    a, b = np.asarray(a, float), np.asarray(b, float)
    d = (b - a) / np.linalg.norm(b - a)
    n = np.array([-d[1], d[0]])
    s.ax.plot([a[0], b[0]], [a[1], b[1]], color=c, linewidth=0.8, zorder=z)
    for p in [a, b, *[np.asarray(t, float) for t in ticks]]:
        s.ax.plot([p[0] - tick * n[0], p[0] + tick * n[0]], [p[1] - tick * n[1], p[1] + tick * n[1]],
                  color=c, linewidth=0.8, zorder=z)


def grid_tag(s, x, y, label):
    """Grey tag, right-aligned at x: the grid a case runs on."""
    w = fk.width(s, label) + 12
    s.box(x - w, y - 8, w, 16, fill=TAG_FILL, edge=TAG_FILL, radius=4, lw=0.6, z=4)
    s.text(x - w + 6, y + 0.3, label, z=5)
    return x - w


def water_table_symbol(ax, x, y, *, z=6):
    """Inverted triangle sitting on the water-table line at height y."""
    ax.add_patch(Polygon([(x - 4.5, y - 6.5), (x + 4.5, y - 6.5), (x, y - 0.8)], closed=True,
                         facecolor=WATER, edgecolor="none", zorder=z))


def draw_block(s, t):
    ax = s.ax
    P = Projection(DRAW_BOX)

    def zone(xa, xb, fill):
        pts = [P(xa, Y_FRONT), P(xb, Y_FRONT), P(xb, Y_BACK), P(xa, Y_BACK)]
        ax.add_patch(Polygon(pts, closed=True, facecolor=fill, edgecolor="none", zorder=2))

    zone(X_LEFT, X_CH0, LEFT_FILL)
    zone(X_CH1, X_RIGHT, RIGHT_FILL)
    zone(X_CH0, X_CH1, CHANNEL_FILL)

    # Contours every 10 m from the DEM rule: chevrons that point upstream.
    for c in (10, 20, 30, 40, 50):
        ys = np.linspace(Y_FRONT, Y_BACK, 400)
        for xs, ok in ((X_CH0 - (c - ALONG * ys) / CROSS, None), (X_CH1 + (c - ALONG * ys) / CROSS, None)):
            ok = (xs >= X_LEFT) & (xs <= X_RIGHT) & ((xs <= X_CH0 + 1e-9) | (xs >= X_CH1 - 1e-9))
            if ok.sum() > 1:
                pts = np.array([P(x, y) for x, y in zip(xs[ok], ys[ok])])
                ax.plot(pts[:, 0], pts[:, 1], color=CONTOUR, linewidth=0.55, alpha=0.5, zorder=3)
        yc = c / ALONG
        if yc < Y_BACK:
            pts = np.array([P(X_CH0, yc), P(X_CH1, yc)])
            ax.plot(pts[:, 0], pts[:, 1], color=CONTOUR, linewidth=0.55, alpha=0.5, zorder=3)

    # Front face (y = 0) and right face (x = 1620): soil band, saturated below the table.
    front_top = np.array([P(X_LEFT, 0), P(X_CH0, 0), P(X_CH1, 0), P(X_RIGHT, 0)])
    side_top = np.array([P(X_RIGHT, 0), P(X_RIGHT, Y_BACK)])

    def band(top, fill_dry, fill_wet):
        mid, bot = top + [0, BAND / 2], top + [0, BAND]
        ax.add_patch(Polygon(np.vstack([top, mid[::-1]]), closed=True, facecolor=fill_dry,
                             edgecolor="none", zorder=2))
        ax.add_patch(Polygon(np.vstack([mid, bot[::-1]]), closed=True, facecolor=fill_wet,
                             edgecolor="none", zorder=2))
        ax.plot(mid[:, 0], mid[:, 1], color=WATER, linewidth=1.0, solid_capstyle="butt", zorder=4)
        ax.plot(bot[:, 0], bot[:, 1], color=INK, linewidth=1.6, solid_capstyle="butt", zorder=4)
        return bot

    f_bot = band(front_top, SOIL_FACE, WET_FACE)
    band(side_top, SOIL_SIDE, WET_SIDE)
    for p in (front_top[0], front_top[-1], side_top[-1]):
        ax.plot([p[0], p[0]], [p[1], p[1] + BAND], color=INK, linewidth=0.8, zorder=4)
    p = P(1230, 0)
    water_table_symbol(ax, p[0], p[1] + BAND / 2)

    # Closed edges: the rim of the surface, except the outlet (the channel's front edge).
    rim = np.array([P(X_CH0, 0), P(X_LEFT, 0), P(X_LEFT, Y_BACK), P(X_CH0, Y_BACK), P(X_CH1, Y_BACK),
                    P(X_RIGHT, Y_BACK), P(X_RIGHT, 0), P(X_CH1, 0)])
    with track(ax):
        ax.plot(rim[:, 0], rim[:, 1], color=INK, linewidth=1.6, solid_joinstyle="round", zorder=5)
    for xe in (X_CH0, X_CH1):
        pts = np.array([P(xe, 0), P(xe, Y_BACK)])
        ax.plot(pts[:, 0], pts[:, 1], color=INK, linewidth=0.5, alpha=0.6, zorder=4)

    # Downhill arrows: across each plane, and along the channel to the outlet.
    with track(ax):
        a0, a1 = P(250, 380), P(640, 380)
        slope_arrow(s, a0, a1)
        b0, b1 = P(1400, 380), P(1020, 380)
        slope_arrow(s, b0, b1)
        c0, c1 = P(820, 960), P(820, 150)
        d = (c1 - c0) / np.linalg.norm(c1 - c0)
        ax.plot([c0[0], c1[0] - 5.6 * d[0]], [c0[1], c1[1] - 5.6 * d[1]], color=WATER, linewidth=1.6,
                solid_capstyle="butt", zorder=8)
        head(s, c1, d, c=WATER)
    # Labels on the surface get a halo in the zone's fill, so the contours stop short of them.
    def on_surface(xy, label, fill, **kw):
        artist = s.text(xy[0], xy[1], label, **kw)
        artist.set_path_effects([patheffects.withStroke(linewidth=3.4, foreground=fill)])
        return artist

    m = (a0 + a1) / 2
    on_surface((m[0], m[1] - 16), t["cross_slope"], LEFT_FILL, ha="center")
    m = (b0 + b1) / 2
    on_surface((m[0], m[1] - 16), t["cross_slope"], RIGHT_FILL, ha="center")
    m = P(820, 640)
    on_surface((m[0] - 7, m[1]), t["along_slope"], LEFT_FILL, c=WATER, ha="right")

    # Zone names on the surface; the channel name sits in the notch at the back.
    on_surface(P(400, 700), t["left_plane"], LEFT_FILL, ha="center")
    on_surface(P(1250, 760), t["right_plane"], RIGHT_FILL, ha="center")
    m = P(820, Y_BACK)
    s.text(m[0], m[1] - 21, t["channel"], ha="center", c=WATER)
    # "closed edges" along the back rim of the right plane, rotated with it.
    ra, rb = P(X_CH1, Y_BACK), P(X_RIGHT, Y_BACK)
    dr = (rb - ra) / np.linalg.norm(rb - ra)
    nr = np.array([dr[1], -dr[0]])
    m = ra + 0.62 * (rb - ra) + 9 * nr
    s.text(m[0], m[1], t["closed"], c=SOFT, ha="center", rotation=np.degrees(np.arctan2(-dr[1], dr[0])),
           rotation_mode="anchor")

    # Outlet: a ribbon out of the channel's front (north) edge, toward the viewer; label
    # to its left.
    o0 = P(820, 0)
    toward = P(820, -1) - o0
    toward = toward / np.linalg.norm(toward)
    tip = o0 + 36 * toward
    with track(ax):
        s.arrow([tuple(o0 + 2 * toward), tuple(tip)], width=(3.0, 3.0), head=(11, 10), c=WATER)
    ox, oy = tip[0] - 10, tip[1] - 16
    fk.rich(s, ox, oy, t["outlet"][0], ha="right")
    for k, line in enumerate(t["outlet"][1:]):
        fk.text(s, ox, oy + 15 * (k + 1), line, ha="right")

    # Widths along the front, on a line parallel to the projected x axis.
    drop = (f_bot[:, 1].max() + 56) - P(820, 0, 0)[1]

    def on_dim(xw):
        return P(xw, 0, 0) + [0, drop]

    da, db, t0, t1 = on_dim(X_LEFT), on_dim(X_RIGHT), on_dim(X_CH0), on_dim(X_CH1)
    with track(ax):
        dim_line(s, da, db, ticks=(t0, t1))
    for xw, top in ((X_LEFT, front_top[0]), (X_RIGHT, front_top[-1])):
        q = on_dim(xw)
        ax.plot([top[0], q[0]], [top[1] + BAND + 3, q[1] + 4], color=SOFT, linewidth=0.6, zorder=6)
    for (pa, pb), key in (((da, t0), "w_left"), ((t1, db), "w_right")):
        m = (pa + pb) / 2
        s.text(m[0], m[1] + 14, t[key], ha="center")
    # The channel's width sits above the line, just right of its two ticks.
    s.text(t1[0] + 7, t1[1] - 11, t["w_channel"])
    mc = (t0 + t1) / 2

    # Length along the left edge, offset outward.
    la, lb = P(X_LEFT, 0), P(X_LEFT, Y_BACK)
    dl = (lb - la) / np.linalg.norm(lb - la)
    nl = np.array([dl[1], -dl[0]])
    la2, lb2 = la + 16 * nl, lb + 16 * nl
    with track(ax):
        dim_line(s, la2, lb2)
    for p0, p1 in ((la, la2), (lb, lb2)):
        ax.plot([p0[0] + 3 * nl[0], p1[0] + 4 * nl[0]], [p0[1] + 3 * nl[1], p1[1] + 4 * nl[1]],
                color=SOFT, linewidth=0.6, zorder=6)
    m = (la2 + lb2) / 2 + 9 * nl
    ang = np.degrees(np.arctan2(-dl[1], dl[0]))
    s.text(m[0], m[1], t["length"], ha="center", rotation=ang, rotation_mode="anchor")
    return on_dim(X_RIGHT)[1] + 14


def draw_card(s, t):
    x0, y0, x1, y1 = CARD
    fk.panel(s, x0, y0, x1 - x0, y1 - y0)
    fk.text(s, x0 + 14, y0 + 19, t["setting"], bold=True, size=10.5)

    # Zone table: chips in the drawing's fills key the three zones.
    ty = y0 + 44
    cx = [x0 + 192, x0 + 258, x0 + 320]     # room for the longer pt and es zone names
    for xc, name, fill in zip(cx, t["zone_heads"], ZONE_FILLS):
        w = fk.width(s, name)
        s.ax.add_patch(Rectangle((xc + 7 - w / 2 - 15, ty - 5), 10, 10, facecolor=fill, edgecolor=INK,
                                 linewidth=0.6, zorder=4))
        fk.text(s, xc + 7, ty, name, ha="center")
    fk.line(s, [(x0 + 14, ty + 11), (x1 - 14, ty + 11)], c=EDGE, lw=0.8)
    for i, (label, vals) in enumerate(t["rows"]):
        yy = ty + 27 + 17 * i
        fk.text(s, x0 + 14, yy, label, room=cx[0] - x0 - 26)   # values are short and centred
        for xc, v in zip(cx, vals):
            fk.text(s, xc + 7, yy, v, ha="center")

    # Groundwater: a small column in the colours of the drawing's soil band.
    gy = ty + 27 + 17 * (len(t["rows"]) - 1) + 18
    colx, colw, colh = x0 + 16, 22, 32
    s.ax.add_patch(Rectangle((colx, gy), colw, colh / 2, facecolor=SOIL_FACE, edgecolor="none", zorder=3))
    s.ax.add_patch(Rectangle((colx, gy + colh / 2), colw, colh / 2, facecolor=WET_FACE, edgecolor="none",
                             zorder=3))
    fk.line(s, [(colx, gy), (colx + colw, gy)], c=INK, lw=0.8)
    fk.line(s, [(colx, gy + colh / 2), (colx + colw, gy + colh / 2)], c=WATER, lw=1.0)
    fk.line(s, [(colx, gy + colh), (colx + colw, gy + colh)], c=INK, lw=1.6)
    water_table_symbol(s.ax, colx + colw / 2, gy + colh / 2)
    for k, (depth, what) in enumerate(t["column"]):
        fk.rich(s, colx + colw + 10, gy + colh / 2 + k * colh / 2 - 1, [(depth + "  ", B), (what, L)],
                room=x1 - colx - colw - 24)

    # Soil and the benchmark storm.
    ny = gy + colh + 20
    lead = ""
    for k, row in enumerate(t["notes"]):
        yy = ny + 16 * k
        if row[0][0]:
            lead = row[0][0]
            fk.rich(s, x0 + 14, yy, row, room=x1 - x0 - 28)
        else:
            fk.text(s, x0 + 14 + fk.width(s, lead, bold=True), yy, row[1][0], room=x1 - x0 - 28)
    return ny + 16 * (len(t["notes"]) - 1)


def status_bar(s, x, ya, yb, kind):
    fill = ACCEPT_EDGE if kind == "ok" else color("guide")
    s.box(x - 1.5, ya, 3, yb - ya, fill=fill, edge=fill, radius=1.5, lw=0.1, z=4)


def draw_list(s, t):
    x0, x1 = LIST_X0, LIST_X1
    xl = x0 + 10
    fk.text(s, x0, 58, t["cases"], bold=True, size=10.5)
    y, pitch = 84, 16
    for block, items in t["blocks"]:
        fk.text(s, x0, y, block, bold=True, size=10, c=SOFT)
        fk.line(s, [(x0 + fk.width(s, block, bold=True, size=10) + 8, y), (x1, y)], c=EDGE, lw=0.8)
        y += 21
        for it in items:
            top = y
            name_w = fk.width(s, it["name"] + "  ", bold=True)
            if it["ids"]:
                fk.rich(s, xl, y, [(it["name"] + "  ", B), (it["ids"], L)])
                used = name_w + fk.width(s, it["ids"])
            else:
                fk.text(s, xl, y, it["name"], bold=True)
                used = name_w
            if it["tag"]:
                tag_x0 = grid_tag(s, x1, y, it["tag"])
                if xl + used + 8 > tag_x0:
                    warnings.warn(f"tag {it['tag']!r} overlaps the name line of {it['name']!r}")
            for row in it["more"]:
                y += pitch
                if isinstance(row, tuple):
                    c2 = xl + max(fk.width(s, a) for a, _ in it["more"]) + 14
                    fk.text(s, xl, y, row[0])
                    if row[1]:
                        fk.text(s, c2, y, row[1], room=x1 - c2)
                else:
                    fk.text(s, xl, y, row, room=x1 - xl)
            for line in ([it["line"]] if isinstance(it["line"], str) else it["line"]):
                y += pitch
                fk.text(s, xl, y, line, c=SOFT, room=x1 - xl)
            if it["status"]:
                status_bar(s, x0 + 1, top - 7, y + 7, it["status"])
            y += pitch + 6
        y += 1
    # Key.
    ky = y + 4
    kx = x0
    for kind, label in t["key"]:
        if kind == "tag":
            s.box(kx, ky - 8, 22, 16, fill=TAG_FILL, edge=TAG_FILL, radius=4, lw=0.6, z=4)
            kx += 22 + 6
        else:
            status_bar(s, kx + 1.5, ky - 8, ky + 8, kind)
            kx += 9
        fk.text(s, kx, ky, label, c=SOFT)
        kx += fk.width(s, label) + 16
    if kx - 16 > x1:
        warnings.warn(f"key ends at {kx - 16:.0f}")
    return ky


def main(preview: Path | None = None) -> None:
    for lang in LABELS:
        draw(lang, preview)


def draw(lang: str, preview: Path | None = None) -> Sheet:
    t = LABELS[lang]
    fig_check._ARROWS.clear()     # the arrows tracked for this language only
    s = Sheet(W, H, NAME)
    renderer = RendererAgg(W, H, 100)

    fk.text(s, 24, 28, t["title"], bold=True, size=11)
    fk.text(s, 24 + fk.width(s, t["title"], bold=True, size=11) + 8, 28.5, t["subtitle"], c=SOFT,
            room=W - 38 - 24 - fk.width(s, t["title"], bold=True, size=11) - 8)

    dims_bottom = draw_block(s, t)
    for k, line in enumerate(t["notes_under"]):
        fk.text(s, 24, dims_bottom + 22 + 15 * k, line, c=SOFT, room=CARD[2] - 24)
    card_bottom = draw_card(s, t)
    list_bottom = draw_list(s, t)
    print(f"[{lang}] dims end at y={dims_bottom:.0f}, notes at {dims_bottom + 37:.0f}, "
          f"card {CARD[1]}-{CARD[3]}, card text ends at y={card_bottom:.0f}, list ends at y={list_bottom:.0f}")

    # Widths checked again with RendererAgg.
    for artist in s.ax.texts:
        bb = artist.get_window_extent(renderer)
        if bb.x1 > W - 14 or bb.x0 < 14:
            warnings.warn(f"{artist.get_text()[:30]!r} spans {bb.x0:.0f}-{bb.x1:.0f}")
    report(s)
    svg = s.save(STATIC / "validation", lang, preview)
    print("wrote", svg.name)
    return s


if __name__ == "__main__":
    main(Path(sys.argv[1]) if len(sys.argv) > 1 else None)


# Sources of every element: docs pages of this site, and the canonical V-tilted rasters of
# the MATLAB model (50 rows x 81 columns of 20 m).
FACTS = {
    "shared catchment; DEM, soil, land cover, LAI, groundwater, boundary setting":
        "validation/overview.md; validation/hydrologic-modules.md",
    "synthetic; 20 m": "validation/overview.md; validation/hydrodynamics-routing.md",
    "81 x 50 cells of 20 m, 1620 m x 1000 m": "DEM raster: 50 rows x 81 columns, 20 m, bounds 0-1620 and 0-1000",
    "left plane 40 cells (800 m), channel 2 cells (40 m), right plane 39 cells (780 m)":
        "LULC and SOIL rasters: columns 0-39 class 1, 40-41 class 2, 42-80 class 3",
    "cross slope 0.05 on both planes": "DEM: 1 m drop per 20 m cell across each plane",
    "0.02 along planes and channel, toward the north edge": "DEM: 0.4 m per 20 m row in every column; row 0 lowest",
    "contours every 10 m": "drawn from the DEM rule z = 0.05 d + 0.02 y",
    "outlet: north edge, row 0, columns 40 and 41, normal flow, slope 0.02":
        "the V-tilted benchmark set-up; validation/hydrodynamics-routing.md (outlet cells)",
    "closed edges (only the outlet faces are open)": "the V-tilted benchmark set-up",
    "water table 0.5 m below the surface": "GW_table raster = DEM - 0.5 m in every cell",
    "bedrock 1 m below the surface": "DTB raster = 1 m in every cell; configuration/general_data.md (DTB is depth below the land surface)",
    "soil and land-cover class 1, 2, 3 per zone (LULC and SOIL are the same raster)": "LULC and SOIL rasters",
    "LAI 0.5, 0, 2.0": "LAI raster; validation/hydrologic-modules.md",
    "Manning n 0.015, 0.15, 0.015 in the benchmark": "the V-tilted benchmark roughness by land-cover class",
    "soil properties set by each case": "validation/hydrologic-modules.md",
    "benchmark storm 10.8 mm/h for 90 min, dry to 180 min, losses off":
        "validation/hydrodynamics-routing.md; inputs/optional-forcing.md",
    "Canopy interception VAL-CANOPY-001": "validation/hydrologic-modules.md; validation/validation-status.md",
    "Snow VAL-SNOW-001": "validation/hydrologic-modules.md; validation/validation-status.md",
    "Infiltration VAL-INFIL-VT-000 to 006, on the 81 x 50 raster":
        "validation/hydrologic-modules.md; validation/validation-status.md; full-model summary (97 200 m3 for 60 mm, i.e. 1.62 km2)",
    "ET VAL-ET-VT-000 to 006, on a 3 x 3 grid of the three zones":
        "validation/hydrologic-modules.md; validation/validation-status.md; per-cell ET results",
    "Local groundwater VAL-GW-ASYNC-001, -002, VAL-GW-CAP-001, VAL-GW-MOUND-001, on 3 x 3 and 7 x 7 V grids":
        "validation/groundwater-recharge.md; validation/validation-status.md",
    "Layered subsurface: no case ID; full-model runs, Python-MATLAB step parity on a 2 x 2 grid":
        "validation/groundwater-recharge.md; validation/validation-status.md",
    "Symmetry and conservation: five routing families, IDs, on a 31 x 41 grid":
        "validation/hydrodynamics-routing.md; the MATLAB validation case list",
    "Benchmark hydrograph: no case ID, all five families, this raster": "validation/hydrodynamics-routing.md",
    "Gauges and case workbook: MATLAB checks, cross-section discharge, identical results":
        "validation/validation-status.md; configuration/general_data.md",
    "status: validated vs controlled tests": "validation/validation-status.md",
}
