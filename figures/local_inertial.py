"""Inside the local inertial solver, for docs/theory/hydrodynamic-model.md, sections 1.2 to 1.11.

Left, top: two neighbouring cells seen from the side, with bed z, depth h, water surface
eta = z + h, the face between them, the face depth H_f and the slope S. Left, bottom: the
grid from above (depth at cell centres, discharge on faces). Right: one time step of the
solver in the order the code runs it, from the water surface to the continuity update.

Facts and their sources are listed in FACTS at the end of this file. Where the docs and
the code disagree the figure follows the code: the slope from eta itself (the docs use
the reconstructed eta* = max(eta, z_f)), h_min tested on the face depth with a 1 mm
default (the docs say 1e-6 m), no maximum-velocity cap (the docs give 10 m/s), and the
donor-volume cap, which the docs do not describe in section 1.

Run from the repository root:

    python3 figures/local_inertial.py [preview-folder]

Output: static/img/theory/local-inertial.svg (en), local-inertial.pt.svg and
local-inertial.es.svg, and a PNG of each in the preview folder, if given.
"""

from __future__ import annotations

import sys
from pathlib import Path

from matplotlib.patches import Circle, Rectangle

sys.dont_write_bytecode = True
sys.path.insert(0, str(Path(__file__).resolve().parent))
from site_style import INK, SOFT, STATIC, WATER, Sheet, color, oklch_hex  # noqa: E402
import flow_kit as fk  # noqa: E402
from fig_check import _ARROWS, report, track  # noqa: E402

# Symbols are the same in every language.
SYMBOLS = {
    "z_i": r"$z_i$", "h_i": r"$h_i$", "eta_i": r"$\eta_i$",
    "z_j": r"$z_{i+1}$", "h_j": r"$h_{i+1}$", "eta_j": r"$\eta_{i+1}$",
    "z_f": r"$z_{\mathrm{f}}$",
    "H_f": r"$H_{\mathrm{f}}$",
    "S": r"$S$",
    "q": r"$q$",
    "dx": r"$\Delta x$",
    "plan_i": r"$i$",
    "plan_j": r"$i+1$",
}
FACE_DEPTH = (r"$H_{\mathrm{f}} = \max(\max(\eta_i,\,\eta_{i+1}) - z_{\mathrm{f}},\ 0)$,  "
              r"$z_{\mathrm{f}} = \max(z_i,\,z_{i+1})$")
BATES = (r"$q^{t+\Delta t} = \dfrac{q^{t} - g\,H_{\mathrm{f}}\,\Delta t\,S}"
         r"{1 + g\,\Delta t\,n^2\,|q^{t}|\,/\,H_{\mathrm{f}}^{7/3}}$")
VOLUME = r"$\Delta V = \Delta t\,(Q_{\mathrm{in}} - Q_{\mathrm{out}})$"
DEPTH = r"$h^{t+\Delta t} = h^{t} + \Delta V / A_{\mathrm{eff}} \geq 0$"
TAGS = ["1.3", "1.4, 1.7", "1.5, 1.10", "1.8, 1.11", ""]

# --- text per language ---------------------------------------------------------------------
# A step row is (kind, text): "text" and "soft" are lines, "eq" the tall Bates equation,
# "eq1" a one-line equation. "defs" are lines of (text, bold) runs; a run of "" is an
# indent under the bold run of the line above.
LABELS = {
    "en": {
        "side_head": "Two neighbouring cells, seen from the side",
        "cell_i": r"cell $i$",
        "cell_j": r"cell $i+1$",
        "face": "face",
        "datum": "datum",
        "defs": [
            [("Face depth  ", True), (FACE_DEPTH, False)],
            [("Slope  ", True),
             (r"$S = (\eta_{i+1} - \eta_i)\,/\,\Delta x$, from one cell centre to the next", False)],
            [("Discharge  ", True),
             (r"$q$ per metre of face, m$^{2}$ s$^{-1}$; $q > 0$ flows toward cell $i+1$", False)],
        ],
        "plan_head": "Seen from above: depths at centres, discharges on faces",
        "key": [
            ("dot", [r"cell centre: $h$, $z$, $\eta$, $n$"]),
            ("qx", [r"face: $q_x$, positive east"]),
            ("qy", [r"face: $q_y$, positive south"]),
            ("fill", [r"cells $i$ and $i+1$ above"]),
        ],
        "count": [r"$R \times C$ cells have",
                  r"$R \times (C+1)$ faces for $q_x$",
                  r"$(R+1) \times C$ faces for $q_y$"],
        "steps_head": "One time step, in the order the code runs",
        "steps": [
            {"title": "Water surface",
             "rows": [("text", r"$\eta = z + h$ in every cell, with $h$ after"),
                      ("text", "this step's rain, infiltration and ET")]},
            {"title": "Face depth and slope",
             "rows": [("text", r"$H_{\mathrm{f}}$ and $S$ on every face, as on the left"),
                      ("text", r"dry if $H_{\mathrm{f}} \leq h_{\min}$ (default 1 mm): $q = 0$"),
                      ("text", "no flow to cells outside the domain")]},
            {"title": "Face discharge",
             "rows": [("eq", BATES),
                      ("text", r"the last $q^t$, pushed by the slope and"),
                      ("text", "damped by friction (default: Bates)"),
                      ("soft", r"optional: $|q| \leq H_{\mathrm{f}}\sqrt{g\,H_{\mathrm{f}}}$, critical flow")]},
            {"title": "Continuity",
             "rows": [("text", r"$Q = q\,W_{\mathrm{f}}$; a cell's outflows shrink if"),
                      ("text", "they would take more than it holds"),
                      ("eq1", VOLUME),
                      ("eq1", DEPTH),
                      ("soft", r"$W_{\mathrm{f}}$ face width, $A_{\mathrm{eff}}$ cell area")]},
            {"title": "Next step",
             "rows": [("text", r"$q^{t+\Delta t}$ is kept and becomes $q^{t}$")]},
        ],
    },
    "pt": {
        "side_head": "Duas células vizinhas, vistas de lado",
        "cell_i": r"célula $i$",
        "cell_j": r"célula $i+1$",
        "face": "face",
        "datum": "referência",
        "defs": [
            [("Profundidade na face  ", True),
             (r"$H_{\mathrm{f}} = \max(\max(\eta_i,\,\eta_{i+1}) - z_{\mathrm{f}},\ 0)$,", False)],
            [("", True), (r"$z_{\mathrm{f}} = \max(z_i,\,z_{i+1})$", False)],
            [("Inclinação  ", True),
             (r"$S = (\eta_{i+1} - \eta_i)\,/\,\Delta x$, de um centro de célula ao outro", False)],
            [("Descarga  ", True),
             (r"$q$ por metro de face, m$^{2}$ s$^{-1}$; $q > 0$ vai para a célula $i+1$", False)],
        ],
        "plan_head": "Vista de cima: profundidade no centro, descarga na face",
        "key": [
            ("dot", ["centro da célula:", r"$h$, $z$, $\eta$, $n$"]),
            ("qx", [r"face: $q_x$, positivo a leste"]),
            ("qy", [r"face: $q_y$, positivo ao sul"]),
            ("fill", [r"células $i$ e $i+1$ acima"]),
        ],
        "count": [r"$R \times C$ células têm",
                  r"$R \times (C+1)$ faces para $q_x$",
                  r"$(R+1) \times C$ faces para $q_y$"],
        "steps_head": "Um passo de tempo, na ordem do código",
        "steps": [
            {"title": "Superfície da água",
             "rows": [("text", r"$\eta = z + h$ em cada célula, após"),
                      ("text", "a chuva, a infiltração e a ET do passo")]},
            {"title": ["Profundidade e", "inclinação na face"],
             "rows": [("text", r"$H_{\mathrm{f}}$ e $S$ em cada face, como ao lado"),
                      ("text", r"se $H_{\mathrm{f}} \leq h_{\min}$ (padrão 1 mm),"),
                      ("text", r"a face está seca: $q = 0$"),
                      ("text", "sem fluxo a células fora do domínio")]},
            {"title": "Descarga na face",
             "rows": [("eq", BATES),
                      ("text", r"o último $q^t$, empurrado pela"),
                      ("text", "inclinação e amortecido pelo atrito"),
                      ("text", "(padrão: Bates)"),
                      ("soft", r"opcional: $|q| \leq H_{\mathrm{f}}\sqrt{g\,H_{\mathrm{f}}}$, fluxo crítico")]},
            {"title": "Continuidade",
             "rows": [("text", r"$Q = q\,W_{\mathrm{f}}$; nenhuma célula perde mais"),
                      ("text", "do que contém: as saídas diminuem"),
                      ("eq1", VOLUME),
                      ("eq1", DEPTH),
                      ("soft", r"$W_{\mathrm{f}}$ largura da face,"),
                      ("soft", r"$A_{\mathrm{eff}}$ área da célula")]},
            {"title": "Próximo passo",
             "rows": [("text", r"$q^{t+\Delta t}$ é guardado e passa a ser $q^{t}$")]},
        ],
    },
    "es": {
        "side_head": "Dos celdas vecinas, vistas de lado",
        "cell_i": r"celda $i$",
        "cell_j": r"celda $i+1$",
        "face": "cara",
        "datum": "referencia",
        "defs": [
            [("Profundidad en la cara  ", True),
             (r"$H_{\mathrm{f}} = \max(\max(\eta_i,\,\eta_{i+1}) - z_{\mathrm{f}},\ 0)$,", False)],
            [("", True), (r"$z_{\mathrm{f}} = \max(z_i,\,z_{i+1})$", False)],
            [("Pendiente  ", True),
             (r"$S = (\eta_{i+1} - \eta_i)\,/\,\Delta x$, de un centro de celda al otro", False)],
            [("Descarga  ", True),
             (r"$q$ por metro de cara, m$^{2}$ s$^{-1}$; $q > 0$ va hacia la celda $i+1$", False)],
        ],
        "plan_head": "Vista en planta: profundidad en centros, descarga en caras",
        "key": [
            ("dot", ["centro de la celda:", r"$h$, $z$, $\eta$, $n$"]),
            ("qx", [r"cara: $q_x$, positivo al este"]),
            ("qy", [r"cara: $q_y$, positivo al sur"]),
            ("fill", [r"celdas $i$ e $i+1$, arriba"]),
        ],
        "count": [r"$R \times C$ celdas tienen",
                  r"$R \times (C+1)$ caras para $q_x$",
                  r"$(R+1) \times C$ caras para $q_y$"],
        "steps_head": "Un paso de tiempo, en el orden del código",
        "steps": [
            {"title": "Superficie del agua",
             "rows": [("text", r"$\eta = z + h$ en cada celda, tras la"),
                      ("text", "lluvia, la infiltración y la ET del paso")]},
            {"title": ["Profundidad y", "pendiente en la cara"],
             "rows": [("text", r"$H_{\mathrm{f}}$ y $S$ en cada cara, como al lado"),
                      ("text", r"si $H_{\mathrm{f}} \leq h_{\min}$ (1 mm por defecto),"),
                      ("text", r"la cara está seca: $q = 0$"),
                      ("text", "sin flujo a celdas fuera del dominio")]},
            {"title": "Descarga en la cara",
             "rows": [("eq", BATES),
                      ("text", r"el último $q^t$, impulsado por la"),
                      ("text", "pendiente y amortiguado por la"),
                      ("text", "fricción (por defecto: Bates)"),
                      ("soft", r"opcional: $|q| \leq H_{\mathrm{f}}\sqrt{g\,H_{\mathrm{f}}}$, flujo crítico")]},
            {"title": "Continuidad",
             "rows": [("text", r"$Q = q\,W_{\mathrm{f}}$; las salidas de una celda se"),
                      ("text", "reducen si superan lo que contiene"),
                      ("eq1", VOLUME),
                      ("eq1", DEPTH),
                      ("soft", r"$W_{\mathrm{f}}$ ancho de la cara,"),
                      ("soft", r"$A_{\mathrm{eff}}$ área de la celda")]},
            {"title": "Paso siguiente",
             "rows": [("text", r"$q^{t+\Delta t}$ se guarda y pasa a ser $q^{t}$")]},
        ],
    },
}

# --- colours ---------------------------------------------------------------------------------
SURFACE_WATER = oklch_hex(0.72, 0.090, 245)   # ponded water, as in the cell water budget
SOIL = color("slot_near_surface")
GROUND = color("ground")
GUIDE = color("guide")
EDGE = color("card_edge")
PAIR = color("deep_fill")

# --- layout (px, y downward) -----------------------------------------------------------------
W, H = 760, 606
# Side view
XI0, XF, XI1 = 92, 222, 352          # cell i from XI0 to XF, cell i+1 from XF to XI1
CI, CJ = (XI0 + XF) / 2, (XF + XI1) / 2
DATUM = 260
ZI, ZJ = 220, 186                    # beds: cell i lower than cell i+1
EI, EJ = 112, 146                    # water surfaces: eta_i above eta_{i+1}
TOP = 86                             # top of the cell columns
DEF_Y = 314                          # first definition line
DEF_PITCH = 18
# Plan view
PG = 52                              # cell size
PX0 = 40
NC, NR = 4, 3
PAIR_RC = [(2, 1), (2, 2)]           # row, column of cells i and i+1
KX = PX0 + NC * PG + 28              # key column
# Steps
SX0, SX1 = 456, 724
LOOP_X = 742
STEP_TOP, STEP_GAP = 46, 16
TITLE_PITCH = 17


def dim_v(s, x, y0, y1, *, c=SOFT, lw=0.8, bar=4.0, z=6):
    """Vertical dimension line with end bars."""
    fk.line(s, [(x, y0), (x, y1)], c=c, lw=lw, z=z)
    for y in (y0, y1):
        fk.line(s, [(x - bar, y), (x + bar, y)], c=c, lw=lw, z=z)


def dim_h(s, y, x0, x1, *, c=SOFT, lw=0.8, bar=4.0, z=6):
    fk.line(s, [(x0, y), (x1, y)], c=c, lw=lw, z=z)
    for x in (x0, x1):
        fk.line(s, [(x, y - bar), (x, y + bar)], c=c, lw=lw, z=z)


def ext(s, x0, x1, y, *, c=GUIDE):
    """Thin extension line from a dimension to the thing it measures."""
    fk.line(s, [(x0, y), (x1, y)], c=c, lw=0.6, z=5)


def side_view(s, t):
    ax = s.ax
    fk.text(s, 30, 30, t["side_head"], bold=True, size=10.5, room=420)

    # Ground, water and the bed.
    ax.add_patch(Rectangle((XI0, ZI), XF - XI0, DATUM - ZI, facecolor=SOIL, lw=0, zorder=1))
    ax.add_patch(Rectangle((XF, ZJ), XI1 - XF, DATUM - ZJ, facecolor=SOIL, lw=0, zorder=1))
    ax.add_patch(Rectangle((XI0, EI), XF - XI0, ZI - EI, facecolor=SURFACE_WATER, lw=0, zorder=2))
    ax.add_patch(Rectangle((XF, EJ), XI1 - XF, ZJ - EJ, facecolor=SURFACE_WATER, lw=0, zorder=2))
    fk.line(s, [(XI0, ZI), (XF, ZI), (XF, ZJ), (XI1, ZJ)], c=GROUND, lw=2.2, z=4)
    fk.line(s, [(XI0, EI), (XF, EI)], c=WATER, lw=1.4, z=4)
    fk.line(s, [(XF, EJ), (XI1, EJ)], c=WATER, lw=1.4, z=4)
    # Cell columns and the datum.
    for x in (XI0, XI1):
        fk.line(s, [(x, TOP), (x, DATUM)], c=GUIDE, lw=0.8, z=3)
    fk.line(s, [(36, DATUM), (440, DATUM)], c=SOFT, lw=0.9, style=(0, (4, 3)), z=3)
    fk.text(s, 440, DATUM + 11, t["datum"], c=SOFT, ha="right", size=9.5)
    fk.text(s, CI, TOP - 11, t["cell_i"], ha="center")
    fk.text(s, CJ, TOP - 11, t["cell_j"], ha="center")

    # The face: dashed above the higher bed, H_f as its wet part.
    fk.line(s, [(XF, TOP - 22), (XF, ZJ)], c=INK, lw=0.9, style=(0, (3, 2.5)), z=5)
    fk.text(s, XF, TOP - 31, t["face"], ha="center", c=INK, bold=True, size=10)
    fk.line(s, [(XF, ZJ), (XF - 30, ZJ)], c=INK, lw=0.9, style=(0, (1.5, 1.8)), z=5)  # z_f into cell i
    dim_v(s, XF, EI, ZJ, c=WATER, lw=2.4, bar=5.0, z=7)
    fk.text(s, XF - 7, EI + 30, SYMBOLS["H_f"], ha="right", size=11, z=11)
    fk.text(s, XF + 6, ZJ + 12, SYMBOLS["z_f"], size=10.5, z=11)

    # Water-surface slope between the cell centres.
    fk.line(s, [(CI, EI), (CJ, EJ)], c=INK, lw=1.0, style=(0, (4, 2.5)), z=8)
    for x, y in ((CI, EI), (CJ, EJ)):
        fk.dot(s, x, y, r=3.0, z=9)
    fk.text(s, XF + 26, EI + 12, SYMBOLS["S"], size=11, z=11)

    # Discharge through the face.
    yq = ZJ - 15
    with track(s.ax):
        fk.arrow(s, (XF - 30, yq), (XF + 36, yq), c=WATER, z=8)
    fk.text(s, XF + 22, yq - 14, SYMBOLS["q"], size=11, ha="center", z=11)

    # Dimensions: z, h and eta on both sides.
    li, lo = XI0 - 16, XI0 - 48                          # inner and outer, left
    dim_v(s, li, ZI, DATUM)
    dim_v(s, li, EI, ZI)
    dim_v(s, lo, EI, DATUM)
    ext(s, lo + 4, XI0, EI)
    ext(s, li + 4, XI0, ZI)
    fk.text(s, li - 6, (ZI + DATUM) / 2, SYMBOLS["z_i"], ha="right", size=10.5)
    fk.text(s, li - 6, (EI + ZI) / 2, SYMBOLS["h_i"], ha="right", size=10.5)
    fk.text(s, lo - 6, (EI + DATUM) / 2, SYMBOLS["eta_i"], ha="right", size=10.5)
    ri, ro = XI1 + 14, XI1 + 56                          # inner and outer, right
    dim_v(s, ri, ZJ, DATUM)
    dim_v(s, ri, EJ, ZJ)
    dim_v(s, ro, EJ, DATUM)
    ext(s, XI1, ro - 4, EJ)
    ext(s, XI1, ri - 4, ZJ)
    fk.text(s, ri + 6, (ZJ + DATUM) / 2, SYMBOLS["z_j"], size=10.5, room=ro - ri - 10)
    fk.text(s, ri + 6, (EJ + ZJ) / 2, SYMBOLS["h_j"], size=10.5, room=ro - ri - 10)
    fk.text(s, ro + 6, (EJ + DATUM) / 2, SYMBOLS["eta_j"], size=10.5, room=448 - ro - 6)

    # Delta x between the centres, below the datum.
    yd = DATUM + 20
    for x, y in ((CI, EI), (CJ, EJ)):
        fk.line(s, [(x, y + 4), (x, yd - 4)], c=GUIDE, lw=0.6, style=(0, (1.5, 2)), z=3)
    dim_h(s, yd, CI, CJ)
    fk.text(s, (CI + CJ) / 2, yd + 13, SYMBOLS["dx"], ha="center", size=10.5)

    # Definitions. A line that starts with an empty bold run continues the line above,
    # indented under its text.
    indent = 0.0
    for k, parts in enumerate(t["defs"]):
        if parts[0][0]:
            indent = fk.width(s, parts[0][0], bold=True)
            fk.rich(s, 30, DEF_Y + DEF_PITCH * k, parts, room=420)
        else:
            fk.rich(s, 30 + indent, DEF_Y + DEF_PITCH * k, parts[1:], room=420 - indent)
    return DEF_Y + DEF_PITCH * (len(t["defs"]) - 1)


def plan_view(s, t, head_y):
    ax = s.ax
    py0 = head_y + 32
    fk.text(s, 30, head_y, t["plan_head"], bold=True, size=10.5, room=420)
    for r, c in PAIR_RC:
        ax.add_patch(Rectangle((PX0 + c * PG, py0 + r * PG), PG, PG, facecolor=PAIR, lw=0, zorder=1))
    for k in range(NC + 1):
        fk.line(s, [(PX0 + k * PG, py0), (PX0 + k * PG, py0 + NR * PG)], c=GUIDE, lw=0.9, z=3)
    for k in range(NR + 1):
        fk.line(s, [(PX0, py0 + k * PG), (PX0 + NC * PG, py0 + k * PG)], c=GUIDE, lw=0.9, z=3)
    half = 11
    with track(ax):
        for r in range(NR):
            yc = py0 + (r + 0.5) * PG
            for k in range(NC + 1):                      # q_x on east-west faces
                xf = PX0 + k * PG
                fk.arrow(s, (xf - half, yc), (xf + half, yc), c=WATER, z=6)
        for c in range(NC):
            xc = PX0 + (c + 0.5) * PG
            for k in range(NR + 1):                      # q_y on north-south faces
                yf = py0 + k * PG
                fk.arrow(s, (xc, yf - half), (xc, yf + half), c=WATER, z=6)
    for r in range(NR):
        for c in range(NC):
            fk.dot(s, PX0 + (c + 0.5) * PG, py0 + (r + 0.5) * PG, r=3.0)
    for (r, c), label in zip(PAIR_RC, (SYMBOLS["plan_i"], SYMBOLS["plan_j"])):
        fk.text(s, PX0 + (c + 0.5) * PG, py0 + NR * PG + 26, label, ha="center", size=10.5, z=11)

    # Key.
    y = py0 + 10
    for kind, rows in t["key"]:
        x = KX
        if kind == "dot":
            fk.dot(s, x + 12, y, r=3.0)
        elif kind == "qx":
            with track(ax):
                fk.arrow(s, (x, y), (x + 24, y), c=WATER)
        elif kind == "qy":
            with track(ax):
                fk.arrow(s, (x + 12, y - 12), (x + 12, y + 12), c=WATER)
        else:
            s.box(x + 3, y - 8, 18, 16, fill=PAIR, edge=GUIDE, radius=2, lw=0.8)
        for i, row in enumerate(rows):
            fk.text(s, x + 34, y + 16 * i, row, room=452 - x - 34)
        y += 16 * len(rows) + 15
    y += 4
    for i, row in enumerate(t["count"]):
        fk.text(s, KX, y + 15 * i, row, c=SOFT, room=448 - KX)
    return py0 + NR * PG + 26


def titles(step):
    """A step title is one line, or a list of lines when it is too long for one."""
    return [step["title"]] if isinstance(step["title"], str) else step["title"]


def step_layout(t):
    """Row positions and box extents of the steps, before anything is drawn."""
    pitch = {"text": 16, "soft": 16, "eq": 48, "eq1": 21}
    y0 = STEP_TOP
    layout = []
    for step in t["steps"]:
        y = y0 + 37 + TITLE_PITCH * (len(titles(step)) - 1)
        placed = []
        for kind, row in step["rows"]:
            if kind == "eq":
                y += 6
                placed.append((kind, row, y + 16))
                y += pitch[kind]
            elif kind == "eq1":
                placed.append((kind, row, y + 3))
                y += pitch[kind]
            else:
                if kind == "soft" and placed and placed[-1][0] == "text":
                    y += 2                               # room for a square root
                placed.append((kind, row, y))
                y += pitch[kind]
        y1 = y - pitch[step["rows"][-1][0]] + 13
        layout.append((y0, y1, placed))
        y0 = y1 + STEP_GAP
    return layout


def steps(s, t):
    ax = s.ax
    fk.text(s, SX0, 30, t["steps_head"], bold=True, size=10.5, room=LOOP_X + 8 - SX0)
    xt = SX0 + 38
    boxes = []
    for k, (step, (y0, y1, placed)) in enumerate(zip(t["steps"], step_layout(t))):
        core = k in (2, 3)
        s.box(SX0, y0, SX1 - SX0, y1 - y0, fill="#ffffff", edge=WATER if core else GUIDE,
              radius=6, lw=1.1 if core else 1.0)
        ax.add_patch(Circle((SX0 + 19, y0 + 18), 10, facecolor=INK, edgecolor="none", zorder=6))
        s.text(SX0 + 19, y0 + 18.5, str(k + 1), bold=True, size=10, c="#ffffff", ha="center", z=7)
        tag = "§" + TAGS[k] if TAGS[k] else ""
        tag_w = fk.width(s, tag, size=9) + 8 if tag else 0
        for i, line in enumerate(titles(step)):
            fk.text(s, xt, y0 + 18 + TITLE_PITCH * i, line, bold=True, size=10.5,
                    room=SX1 - 10 - (tag_w if i == 0 else 0) - xt)
        if tag:
            fk.text(s, SX1 - 10, y0 + 18, tag, size=9, c=SOFT, ha="right")
        for kind, row, yy in placed:
            if kind == "eq":
                fk.text(s, (SX0 + SX1) / 2 + 6, yy, row, size=10.5, ha="center", room=None)
            elif kind == "eq1":
                fk.text(s, xt, yy, row, size=10.5, room=SX1 - 8 - xt)
            else:
                fk.text(s, xt, yy, row, c=SOFT if kind == "soft" else INK, room=SX1 - 8 - xt)
        boxes.append((y0, y1))
    xm = (SX0 + SX1) / 2
    with track(ax):
        for (a0, a1), (b0, _) in zip(boxes[:-1], boxes[1:]):
            fk.arrow(s, (xm, a1), (xm, b0), c=INK)
        # Loop: from the last step back to the first, on the right.
        ya = (boxes[-1][0] + boxes[-1][1]) / 2
        yb = (boxes[0][0] + boxes[0][1]) / 2
        fk.route(s, [(SX1, ya), (LOOP_X, ya), (LOOP_X, yb), (SX1, yb)], c=INK)
    return boxes


def draw(lang: str, preview: Path | None = None) -> Path:
    t = LABELS[lang]
    _ARROWS.clear()  # fig_check keeps the arrows of every sheet; check this one only
    # The plan view sits below the definitions; a wrapped definition moves it down.
    head_y = DEF_Y + DEF_PITCH * (len(t["defs"]) - 1) + 26
    plan_bottom = head_y + 32 + NR * PG + 26
    steps_bottom = step_layout(t)[-1][1]
    height = max(H, round(plan_bottom + 16), round(steps_bottom + 36))
    s = Sheet(W, height, "local-inertial")
    side_view(s, t)
    plan_view(s, t, head_y)
    boxes = steps(s, t)
    print(lang, "H =", height, "step boxes:", [(round(a), round(b)) for a, b in boxes], end="; ")
    report(s)
    svg = s.save(STATIC / "theory", lang, preview)
    print(lang, "->", svg)
    return svg


def main(preview: Path | None = None) -> None:
    for lang in LABELS:
        draw(lang, preview)


if __name__ == "__main__":
    main(Path(sys.argv[1]) if len(sys.argv) > 1 else None)


# --- what each element shows and where it is stated --------------------------------------------
# HM = docs/theory/hydrodynamic-model.md, CO = docs/configuration/overview.md. "Code" means
# the HydroPol2D-Python local-inertial kernel and its boundary step, read on 2026-10-29.
FACTS = {
    "local inertial is the default routing family": "HM 1.1; CO",
    "hydrologic terms (rain, infiltration, ET) are applied before routing":
        "HM 1.2; code: the vertical hydrology runs before the routing step",
    "eta = z + h, h = V / cell area": "HM 1.3; code",
    "z_f = max(z_i, z_{i+1})": "HM 1.3; code",
    "H_f = max(max(eta_i, eta_{i+1}) - z_f, 0)": "HM 1.4; code",
    "S = (eta_{i+1} - eta_i) / dx": "code uses eta itself; HM 1.3 uses eta* = max(eta, z_f)",
    "q is unit discharge, m2/s; qx positive east, qy positive south": "HM 1.2, 1.8; code",
    "staggered arrays: qx (R, C+1), qy (R+1, C); h, z, n per cell": "code",
    "dry face: H_f <= h_min gives q = 0": "code; HM 1.7 states the test on the cell depth",
    "h_min default 1 mm": "code default (as in LISFLOOD-FP); HM 1.7 says 1e-6 m",
    "faces next to cells outside the domain carry no flow": "HM 1.7; code",
    "Bates update q^{t+dt} = (q^t - g H_f dt S) / (1 + g dt n^2 |q^t| / H_f^{7/3})": "HM 1.5; code",
    "Bates is the default scheme; s-upwind and s-centred change only the q^t term": "HM 1.6; code",
    "optional critical-flow cap |q| <= H_f sqrt(g H_f), off by default": "HM 1.10.1; code",
    "no maximum-velocity cap": "code retired it; HM 1.10.2 still gives u_max = 10 m/s",
    "Q = q W_f, W_f = dy on x faces, dx on y faces": "HM 1.8; code",
    "donor cap: a cell's outflows are scaled so it cannot lose more than it holds":
        "code; HM 3.4 states it for the D4 wave modes, not in section 1",
    "continuity dV = dt (Q_in - Q_out), h^{t+dt} = h^t + dV / A_eff >= 0, A_eff = cell area":
        "HM 1.11; code",
    "q^{t+dt} is kept for the next step": "HM 1.5 (previous face discharge); code",
}
