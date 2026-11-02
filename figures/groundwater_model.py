"""Hillslope cross-section of the default groundwater scheme, for docs/theory/groundwater-model.md.

Three model cells from a hillside down to a river cell. Each cell has one ground elevation,
one water-table head h and one aquifer base z_0, so the section steps from cell to cell and
the lateral flow between cells shows. Thin blue ribbons are the exchanges of every surface
step, the broad ribbon is the lateral flow on the groundwater clock, dashed arrows are
optional modules that are off by default.

Facts (HydroPol2D-Python, release/studio-0.9.0rc2; HydroPol2D MATLAB; read only):
  near-surface layer 0.05 m: config/models.py:1685 (ltop_m), core/engine.py:1001;
    MATLAB HydroPol2D_preprocessing.m:2328
  three vadose layers, cut by the water table: modules/soil.py:178-183
  aquifer base z_0 = ground - soil depth: core/preprocess.py:1640
  infiltration into the layers, top down: core/engine.py:2265, modules/infiltration.py:178
  recharge R_down from the transmission zone: core/engine.py:2323
  capillary rise C_up, on by default: core/engine.py:2372, config/models.py:1700;
    MATLAB Groundwater_Module.m:235
  deep aquifer: a fraction f_d of the downward recharge, one linear reservoir per
    subbasin, outflow to the surface water of the river cells: core/engine.py:2347-2365,
    modules/deep_aquifer.py:40-59; MATLAB Groundwater_Module.m:206-228
  river exchange either way, (K_rb / b) A_rb (h - stage), off by default:
    core/engine.py:2405-2465, modules/groundwater.py:113-179, config/models.py:235;
    MATLAB Groundwater_Module.m:309-330, hp2d_structured_river_exchange.m
  the head moves by the net exchange every surface step, exfiltration where h passes the
    ground: core/engine.py:2467-2508, modules/groundwater.py:453-490;
    MATLAB Groundwater_Module.m:332-345
  saturation excess when the table rises: core/engine.py:2510-2520, modules/soil.py:377
  lateral 2D Boussinesq flow only when the scheduler is due, with zero recharge (the heads
    already carry it): core/engine.py:2543-2570; MATLAB Groundwater_Module.m:389-392
  scheduler: target 86400 s (groundwater_target_dt_s), minimum 60 s, head-change
    and stability triggers, always asynchronous: config/models.py:1691-1699,
    modules/groundwater.py:280-302

Run from the repository root:

    python3 figures/groundwater_model.py [preview-folder]

Output: static/img/theory/groundwater-model.svg (en), groundwater-model.pt.svg and
groundwater-model.es.svg, and a PNG of each in the preview folder, if given.
"""

from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
from matplotlib.patches import Polygon, Rectangle

sys.dont_write_bytecode = True  # never leave __pycache__ in the docs repo
from site_style import INK, SOFT, STATIC, WATER, Sheet, color, oklch_hex  # noqa: E402
from layered_column import _kite_head  # noqa: E402  (on the path through site_style)
import flow_kit as fk  # noqa: E402
from fig_check import _ARROWS, report, track  # noqa: E402

NAME = "groundwater-model"

# --- text per language. Math stays the same in every language. ------------------------------
# A label is a list of lines, 16 px apart.
LABELS = {
    "en": {
        "surface": r"surface water $d$",
        "near": "near surface",
        "thin": "0.05 m",
        "root": "root zone",
        "transmission": "transmission zone",
        "table": r"water table $h$",
        "thickness": ["saturated thickness", r"$H = h - z_0$"],
        "base": [r"aquifer base $z_0$", "ground minus", "soil depth"],
        "cells": ["hillside cell", "footslope cell", "river cell"],
        "infiltration": ["infiltration", r"$i$"],
        "recharge": ["recharge", r"$R_{\mathrm{down}}$"],
        "capillary": ["capillary rise", r"$C_{\mathrm{up}}$ to the", "root zone"],
        "lateral": [r"lateral flow $\mathbf{F}$, when on", "2D Boussinesq",
                    r"$\mathbf{F} = -K H \nabla h$"],
        "excess": ["saturation excess", r"$S_{\mathrm{excess}}$, as $h$ rises"],
        "earlier": r"earlier $h$",
        "exfiltration": ["exfiltration", r"$q_{\mathrm{exf}}$"],
        "river": ["river exchange", r"$q_{\mathrm{river}}$, either way"],
        "fd": [r"a fraction $f_d$", "of the recharge"],
        "deep": ("Deep aquifer, when on",
                 [r"one linear reservoir per subbasin, $Q = S/\tau$,", "returned to the river cells"]),
        "key": [
            ("Every surface step", [r"$h$ moves at once by $R_{\mathrm{net}}\,\Delta t/S_y$, with",
                                    r"$R_{\mathrm{net}} = R_{\mathrm{down}} - C_{\mathrm{up}}$ and any river exchange;",
                                    "exfiltration and saturation excess follow"]),
            ("Groundwater clock", ["only lateral flow waits; it runs once a day",
                                   "by default (86400 s), sooner when the head",
                                   "change or stability requires it"]),
            ("Optional module, off by default", []),
        ],
    },
    "pt": {
        "surface": r"água superficial $d$",
        "near": "camada superficial",
        "thin": "0,05 m",
        "root": "zona radicular",
        "transmission": "zona de transmissão",
        "table": r"lençol freático $h$",
        "thickness": ["espessura saturada", r"$H = h - z_0$"],
        "base": [r"base do aquífero $z_0$", "terreno menos a", "profundidade do solo"],
        "cells": ["célula de encosta", "célula de sopé", "célula de rio"],
        "infiltration": ["infiltração", r"$i$"],
        "recharge": ["recarga", r"$R_{\mathrm{down}}$"],
        "capillary": ["ascensão", r"capilar $C_{\mathrm{up}}$", "à zona radicular"],
        "lateral": [r"fluxo lateral $\mathbf{F}$, se ativo", "2D de Boussinesq",
                    r"$\mathbf{F} = -K H \nabla h$"],
        "excess": ["excesso de saturação", r"$S_{\mathrm{excess}}$, quando $h$ sobe"],
        "earlier": r"$h$ anterior",
        "exfiltration": ["exfiltração", r"$q_{\mathrm{exf}}$"],
        "river": ["troca rio-aquífero", r"$q_{\mathrm{river}}$, nos dois sentidos"],
        "fd": [r"uma fração $f_d$", "da recarga"],
        "deep": ("Aquífero profundo, se ativo",
                 [r"um reservatório linear por sub-bacia, $Q = S/\tau$,", "devolvido às células de rio"]),
        "key": [
            ("A cada passo da superfície", [r"$h$ muda na hora em $R_{\mathrm{net}}\,\Delta t/S_y$, com",
                                            r"$R_{\mathrm{net}} = R_{\mathrm{down}} - C_{\mathrm{up}}$ e a eventual troca",
                                            "com o rio; seguem a exfiltração e o excesso",
                                            "de saturação"]),
            ("Relógio da água subterrânea", ["só o fluxo lateral espera; roda uma vez por",
                                             "dia por padrão (86400 s), antes se a variação",
                                             "de carga ou a estabilidade exigir"]),
            ("Módulo opcional, desativado por padrão", []),
        ],
    },
    "es": {
        "surface": r"agua superficial $d$",
        "near": "capa superficial",
        "thin": "0,05 m",
        "root": "zona de raíces",
        "transmission": "zona de transmisión",
        "table": r"nivel freático $h$",
        "thickness": ["espesor saturado", r"$H = h - z_0$"],
        "base": [r"base del acuífero $z_0$", "terreno menos la", "profundidad del suelo"],
        "cells": ["celda de ladera", "celda de pie de ladera", "celda de río"],
        "infiltration": ["infiltración", r"$i$"],
        "recharge": ["recarga", r"$R_{\mathrm{down}}$"],
        "capillary": ["ascenso", r"capilar $C_{\mathrm{up}}$", "a la zona", "radicular"],
        "lateral": [r"flujo lateral $\mathbf{F}$, si está activo", "2D de Boussinesq",
                    r"$\mathbf{F} = -K H \nabla h$"],
        "excess": ["exceso de saturación", r"$S_{\mathrm{excess}}$, al subir $h$"],
        "earlier": r"$h$ anterior",
        "exfiltration": ["exfiltración", r"$q_{\mathrm{exf}}$"],
        "river": ["intercambio río-acuífero", r"$q_{\mathrm{river}}$, en ambos sentidos"],
        "fd": [r"una fracción $f_d$", "de la recarga"],
        "deep": ("Acuífero profundo, si está activo",
                 [r"un embalse lineal por subcuenca, $Q = S/\tau$,", "devuelto a las celdas de río"]),
        "key": [
            ("En cada paso superficial", [r"$h$ cambia al instante en $R_{\mathrm{net}}\,\Delta t/S_y$, con",
                                          r"$R_{\mathrm{net}} = R_{\mathrm{down}} - C_{\mathrm{up}}$ y el eventual",
                                          "intercambio con el río; siguen la exfiltración",
                                          "y el exceso de saturación"]),
            ("Reloj del agua subterránea", ["solo el flujo lateral espera; corre una vez al",
                                            "día por defecto (86400 s), antes si el cambio",
                                            "de carga o la estabilidad lo exigen"]),
            ("Módulo opcional, desactivado por defecto", []),
        ],
    },
}

# --- colours ---------------------------------------------------------------------------------
SATURATED = color("slot_wet_even")
SURFACE_WATER = oklch_hex(0.72, 0.090, 245)  # ponded and river water, as in cell_water_budget.py
LAYERS = (color("slot_near_surface"), color("slot_root_zone"), color("slot_transmission"))

# --- geometry (px, y downward) ---------------------------------------------------------------
W = 760
LX = 150                                  # the left labels end here (right-aligned)
AX0, AX1, BX1, CX1 = 158, 390, 580, 720   # cell edges: hillside, footslope, river cell
GA, NS, RD, HA = 110, 128, 170, 232       # hillside: ground, near-surface base, root depth, table
GB, HB_OLD = 242, 290                     # footslope: ground = table; the table before it rose
GC, HC = 322, 336                         # river cell: bank ground and table under the bank
CH0, BED, STAGE = 650, 362, 344           # channel wall top, bed and river stage
SOIL = 205                                # soil depth, the same in the three cells
ZA, ZB, ZC = GA + SOIL, GB + SOIL, GC + SOIL
HATCH = 22
KEY = (400, 18, 346, 0)                   # clock and key card x, y, w (h follows the text)
KEY_HEAD, KEY_PITCH, KEY_GAP = 19, 16, 10  # heading to first line, line pitch, row gap
ROUTE_X = CX1 + 22                        # the deep return flow climbs here


def main(preview: Path | None = None) -> None:
    for lang in LABELS:
        draw(lang, preview)


def wall_x(y: float) -> float:
    """x of the sloping channel wall at height y."""
    return CH0 + 14 * (y - GC) / (BED - GC)


def draw(lang: str, preview: Path | None = None) -> None:
    T = LABELS[lang]
    _ARROWS.clear()  # fig_check keeps the arrows of every sheet; check this one only
    key_h = 32 + sum(KEY_HEAD + KEY_PITCH * len(rows) for _, rows in T["key"]) \
        - KEY_HEAD + KEY_GAP * (len(T["key"]) - 1)
    deep_y = ZC + HATCH + 30
    height = deep_y + 48 + 16
    s = Sheet(W, height, NAME)
    ax = s.ax

    def label(x, y, lines, *, ha="left", c=INK, room=None):
        for k, row in enumerate(lines):
            fk.text(s, x, y + 16 * k, row, ha=ha, c=c, room=room)

    def flux(points, **kw):
        kw.setdefault("width", (1.2, 3.8))
        kw.setdefault("head", (12, 11))
        with track(ax):
            s.arrow(points, c=WATER, **kw)

    def dashed(points):
        """Dashed right-angle route with a solid notched head (a straight arrow for 2 points)."""
        pts = np.asarray(points, float)
        tip, prev = pts[-1], pts[-2]
        d = (tip - prev) / np.linalg.norm(tip - prev)
        head = (10, 9)
        shaft = np.vstack([pts[:-1], tip - d * head[0] * 0.62])
        with track(ax):
            ax.plot(shaft[:, 0], shaft[:, 1], color=WATER, linewidth=1.3, linestyle=(0, (4, 3)),
                    dash_capstyle="round", solid_joinstyle="miter", zorder=5)
            ax.add_patch(Polygon(_kite_head(tip, d, *head), closed=True, facecolor=WATER,
                                 edgecolor="none", zorder=5))

    def rect(x0, y0, x1, y1, fill, z=1):
        ax.add_patch(Rectangle((x0, y0), x1 - x0, y1 - y0, facecolor=fill, lw=0, zorder=z))

    # --- hillside cell: three vadose layers over the saturated zone ---------------------------
    for (y0, y1), fill in zip(((GA, NS), (NS, RD), (RD, HA)), LAYERS):
        rect(AX0, y0, AX1, y1, fill)
    rect(AX0, HA, AX1, ZA, SATURATED)
    rect(AX0, GA - 7, AX1, GA, SURFACE_WATER, z=2)

    # --- footslope cell: the table has reached the ground --------------------------------------
    rect(AX1, GB, BX1, ZB, SATURATED)
    rect(AX1, GB - 8, BX1, GB, SURFACE_WATER, z=2)

    # --- river cell: banks with only a thin near-surface layer, channel with water ------------
    rect(BX1, GC, CH0, HC, LAYERS[0])
    ax.add_patch(Polygon([(CH0, GC), (CH0, HC), (wall_x(HC), HC)], closed=True,
                         facecolor=LAYERS[0], lw=0, zorder=1))
    ax.add_patch(Polygon([(BX1, HC), (wall_x(HC), HC), (wall_x(BED), BED), (CX1, BED), (CX1, ZC),
                          (BX1, ZC)], closed=True, facecolor=SATURATED, lw=0, zorder=1))
    ax.add_patch(Polygon([(wall_x(STAGE), STAGE), (wall_x(BED), BED), (CX1, BED), (CX1, STAGE)],
                         closed=True, facecolor=SURFACE_WATER, lw=0, zorder=2))

    # --- outlines, ground, tables, bases ------------------------------------------------------
    guide = color("guide")
    for x0, x1, top, base in ((AX0, AX1, GA - 7, ZA), (AX1, BX1, GB - 8, ZB)):
        ax.add_patch(Rectangle((x0, top), x1 - x0, base - top, fill=False, edgecolor=guide,
                               lw=0.8, zorder=3))
    s.line([BX1, BX1, CX1, CX1], [GC, ZC, ZC, BED], c=guide, lw=0.8, z=3)
    ground = color("ground")
    s.line([AX0, AX1], [GA, GA], c=ground, lw=2.4, z=4)
    s.line([AX1, BX1], [GB, GB], c=ground, lw=2.4, z=4)
    s.line([BX1, CH0, wall_x(BED), CX1], [GC, GC, BED, BED], c=ground, lw=2.4, z=4)
    s.line([AX0, AX1], [HA, HA], c=WATER, lw=2.0, z=4)
    s.line([BX1, wall_x(HC)], [HC, HC], c=WATER, lw=2.0, z=4)
    s.line([AX1, BX1], [HB_OLD, HB_OLD], c=WATER, lw=1.0, style=(0, (1, 2.5)), z=4)
    for x0, x1, base in ((AX0, AX1, ZA), (AX1, BX1, ZB), (BX1, CX1, ZC)):
        ax.add_patch(Rectangle((x0, base), x1 - x0, HATCH, facecolor=color("card"),
                               edgecolor=color("bedrock_hatch"), hatch="////", lw=0, zorder=1))
        s.line([x0, x1], [base, base], c=INK, lw=2.0, z=4)

    # Water-table symbol on the hillside table.
    tx = AX0 + 14
    ax.add_patch(Polygon([(tx - 8, HA - 11), (tx + 8, HA - 11), (tx, HA - 1)], closed=True,
                         facecolor=WATER, edgecolor="none", zorder=6))
    s.line([tx - 7, tx + 7], [HA + 5, HA + 5], c=WATER, lw=1.2, z=6)
    s.line([tx - 4, tx + 4], [HA + 9, HA + 9], c=WATER, lw=1.2, z=6)

    # --- left labels, level with the hillside cell ---------------------------------------------
    room = LX - 14
    fk.text(s, LX, GA - 9, T["surface"], ha="right", room=room)
    fk.text(s, LX, (GA + NS) / 2 + 2, T["near"], ha="right", room=room)
    fk.text(s, AX1 - 8, (GA + NS) / 2, T["thin"], ha="right", c=SOFT, size=9)
    fk.text(s, LX, (NS + RD) / 2, T["root"], ha="right", room=room)
    fk.text(s, LX, (RD + HA) / 2, T["transmission"], ha="right", room=room)
    fk.text(s, LX, HA, T["table"], ha="right", c=WATER, room=room)
    ax.plot([LX + 2, LX + 6, LX + 6, LX + 2], [HA + 13, HA + 13, ZA - 3, ZA - 3], color=SOFT,
            lw=1.0, zorder=3)
    label(LX - 4, (HA + ZA) / 2 - 8, T["thickness"], ha="right", room=room)
    label(LX, ZA + 8, T["base"], ha="right", room=room)

    # Cell names under the bedrock strips.
    for (x0, x1, base), name in zip(((AX0, AX1, ZA), (AX1, BX1, ZB), (BX1, CX1, ZC)), T["cells"]):
        fk.text(s, (x0 + x1) / 2, base + HATCH + 14, name, ha="center", c=SOFT, size=9)

    # --- vertical exchange in the hillside cell ------------------------------------------------
    xi = AX0 + 38                                    # infiltration, recharge and f_d share a line
    flux([(xi, GA - 6), (xi, NS + 30)])
    label(xi + 8, NS + 4, T["infiltration"])
    flux([(xi, RD + 6), (xi, HA - 1)])
    label(xi + 8, RD + 14, T["recharge"])
    xc = AX0 + 117
    flux([(xc, HA + 1), (xc, RD - 16)])           # capillary rise ends in the root zone
    cap = T["capillary"]
    label(xc + 8, (RD + HA) / 2 - 8 * (len(cap) - 1), cap, room=AX1 - xc - 10)

    # A fraction f_d of the recharge goes on to the deep aquifer.
    dashed([(xi, HA + 4), (xi, deep_y - 1)])
    label(xi + 8, (ZA + HATCH + deep_y) / 2 + 4, T["fd"])

    # --- lateral flow through the saturated zones ----------------------------------------------
    lat = T["lateral"]
    label(xi + 10, HA + 16, lat, room=AX1 - xi - 14)
    with track(ax):
        s.arrow([(xi + 20, HA + 70), (AX1 - 10, HA + 70), (BX1 - 110, ZB - 30), (CH0 - 14, ZC - 82)],
                c=WATER, width=(2.5, 10), head=(18, 20))

    # --- footslope: saturation excess and exfiltration ----------------------------------------
    xe = AX1 + 14
    flux([(xe, HB_OLD - 4), (xe, GB - 6)])
    label(xe + 8, GB + 14, T["excess"], room=BX1 - xe - 12)
    fk.text(s, BX1 - 28, HB_OLD + 11, T["earlier"], ha="right", c=SOFT, size=9)
    xq = BX1 - 20
    flux([(xq, GB + 150), (xq, GB - 6)])
    label(xq - 8, GB + 84, T["exfiltration"], ha="right")

    # --- river cell: exchange with the river, either way --------------------------------------
    for x, up in ((CH0 + 36, True), (CH0 + 60, False)):
        pts = [(x, BED + 46), (x, STAGE + 6)]
        dashed(pts if up else pts[::-1])
    label(BX1 + 8, GC - 30, T["river"], room=ROUTE_X - BX1 - 14)

    # --- deep aquifer and its return flow to the river ----------------------------------------
    x0, w, h = AX0 + 18, CX1 - 20 - (AX0 + 18), 48
    s.box(x0, deep_y, w, h, fill=color("deep_fill"), edge=WATER, radius=7, z=4)
    heading, rows = T["deep"]
    hw = fk.width(s, heading, bold=True, size=10)
    fk.text(s, x0 + 12, deep_y + 15, heading, bold=True, size=10)
    fk.text(s, x0 + 12 + hw + 8, deep_y + 15, rows[0], room=w - hw - 32)
    fk.text(s, x0 + 12 + hw + 8, deep_y + 33, rows[1], room=w - hw - 32)
    dashed([(x0 + w, deep_y + h / 2), (ROUTE_X, deep_y + h / 2), (ROUTE_X, STAGE + 9),
            (CX1 + 1, STAGE + 9)])

    # --- clocks and key -----------------------------------------------------------------------
    kx, ky, kw, _ = KEY
    s.box(kx, ky, kw, key_h, fill="#ffffff", edge=color("card_edge"), radius=8, z=2)
    y = ky + 16
    for (heading, rows), kind in zip(T["key"], ("thin", "broad", "dashed")):
        sx = kx + 12
        if kind == "thin":
            flux([(sx, y), (sx + 30, y)])
        elif kind == "broad":
            with track(ax):
                s.arrow([(sx, y), (sx + 30, y)], c=WATER, width=(2.5, 8), head=(14, 15))
        else:
            dashed([(sx, y), (sx + 30, y)])
        tx0 = sx + 38
        fk.text(s, tx0, y, heading, bold=True, size=10, room=kx + kw - 10 - tx0)
        for k, row in enumerate(rows):
            fk.text(s, tx0, y + KEY_HEAD + KEY_PITCH * k, row, room=kx + kw - 10 - tx0)
        y += KEY_HEAD + KEY_PITCH * len(rows) + KEY_GAP

    print(lang, end=": ")
    report(s)
    print(s.save(STATIC / "theory", lang, preview))


if __name__ == "__main__":
    main(Path(sys.argv[1]) if len(sys.argv) > 1 else None)
