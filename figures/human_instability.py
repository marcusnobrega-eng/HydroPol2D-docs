"""When floodwater makes people unstable, for docs/theory/human-instability.md.

Left: a person standing in flowing water on a slope, with the depth h, the speed v,
the slope beta and the four forces the module balances (drag, buoyancy, weight,
friction), then the inputs and where each mode runs. Right: the two implemented modes
of flag_human_instability:

- mode 1, the force-balance risk index: continuous ratio R = F_hyd / F_fric, clipped to
  [0, 1]; it runs on the regular grid and on the Voronoi mesh;
- mode 3, the force-balance classes: 0 stable, 1 slide, 2 topple, 3 drowning, on the
  local DEM slope of each cell and the person's height. The lift lever arm uses the
  tangent of the slope angle, and a dry cell (h = 0) is stable. A mesh run refuses it.

Run from the repository root:

    python3 figures/human_instability.py [preview-folder] [--check]

Output: static/img/theory/human-instability.svg (en), human-instability.pt.svg and
human-instability.es.svg, plus a PNG of each in the preview folder when one is given.
--check prints the text boxes that overlap each other or leave the card.
"""

from __future__ import annotations

import math
import sys
from pathlib import Path

import numpy as np
from matplotlib.backends.backend_agg import FigureCanvasAgg
from matplotlib.patches import Arc, Circle, Polygon, Rectangle

from site_style import INK, SOFT, STATIC, WATER, Sheet, color, oklch_hex
from layered_column import _kite_head  # noqa: E402  (site_style puts figures/ on the path)

# --- text ----------------------------------------------------------------------------------
_EQ_M1 = [
    r"$F_{\mathrm{person}} = m_{\mathrm{person}}\,g$",
    r"$F_{\mathrm{buoy}} = w_1\, w_2\, h\, \rho_{\mathrm{w}}\, g$",
    r"$F_{\mathrm{fric}} = \mu\, \max(F_{\mathrm{person}} - F_{\mathrm{buoy}},\ 0)$",
    r"$F_{\mathrm{hyd}} = \frac{1}{2}\, C_d\, \rho_{\mathrm{w}}\, w_1\, h\, v^2$",
    r"$R = F_{\mathrm{hyd}}\, /\, F_{\mathrm{fric}}$",
]
_EQ_M3 = [
    r"$D,\ L \propto \frac{1}{2}\,\rho_{\mathrm{w}}\, C_d\, v^2 A_{\mathrm{sub}}$"
    r"$\qquad B_n = \rho_{\mathrm{w}}\, g\, V_{\mathrm{sub}}\, \cos\beta$",
    r"$W_p = m\, g\, \sin\beta \qquad W_n = m\, g\, \cos\beta$",
]
_SLIDE = r"$D + W_p > T$"
_TOPPLE = r"$M > M_{\mathrm{res}}$"
_DROWN = r"$h > \frac{13}{16}\, y$"
_T = r"$T = \mu\,(W_n - B_n - L)$"
_ARM = r"$x_c/\cos\beta + (h/2)\tan\beta$"

LABELS = {
    "en": {
        "scene_title": "Forces on a person in flowing water",
        "scene_sub": [r"depth $h$ and speed $v$ come from the routing,",
                      "in every cell and at every time step"],
        "velocity": r"speed $v$",
        "depth": r"depth $h$",
        "slope": r"slope $\beta$",
        "drag": "drag",
        "buoyancy": "buoyancy",
        "weight": "weight",
        "friction": "friction",
        "top_view": ["mode 1 body block,", "seen from above"],
        "inputs_title": "What the module uses",
        "inputs": [r"$h$ and $v$ of each cell, from the routing",
                   r"body mass $m$, height $y$ and widths, friction",
                   r"coefficient $\mu$ and drag coefficient $C_d$,",
                   "from the human-risk parameters of the model",
                   r"water density $\rho_{\mathrm{w}}$, gravity $g$; DEM slope $\beta$ in mode 3"],
        "runs_title": "Where each mode runs",
        "runs": ["mode 1: the regular grid and the Voronoi mesh",
                 "mode 3: the regular grid only; a mesh run refuses it",
                 "mode 2 is not implemented"],
        "m1_title": "Mode 1: force-balance risk index",
        "m1_names": ["weight", "buoyancy", "friction", "drag", "ratio"],
        "m1_ramp_lo": "0",
        "m1_ramp_hi": "1, full risk",
        "m1_notes": [r"clipped to $0 \leq R \leq 1$; $R = 1$ when buoyancy",
                     r"carries the whole weight and $h > 0$",
                     r"each cell keeps its maximum $R$ over the run"],
        "m3_title": "Mode 3: slide, topple and drowning classes",
        "m3_lines": [r"$A_{\mathrm{sub}}$, $V_{\mathrm{sub}}$, $x_c$: submerged area, volume and centroid",
                     r"$\beta$: local slope of the DEM in each cell"],
        "classes": [
            ("1", "slide", _SLIDE, [_T + ", available friction"]),
            ("2", "topple", _TOPPLE,
             [r"$M$: moments of $D$, $L$, $B_n$ and $W_p$",
              r"lever arm of $L$: " + _ARM,
              r"$M_{\mathrm{res}}$: moment of $W_n$"]),
            ("3", "drowning", _DROWN, [r"$y$: body height"]),
        ],
        "m3_final": ["the class is the highest code that applies; 0 is stable",
                     r"a dry cell ($h = 0$) is stable, even on a steep slope"],
    },
    "pt": {
        "scene_title": "Forças sobre uma pessoa no escoamento",
        "scene_sub": [r"a profundidade $h$ e a velocidade $v$ vêm do roteamento,",
                      "em cada célula e a cada passo de tempo"],
        "velocity": r"velocidade $v$",
        "depth": r"profundidade $h$",
        "slope": r"declive $\beta$",
        "drag": "arrasto",
        "buoyancy": "empuxo",
        "weight": "peso",
        "friction": "atrito",
        "top_view": ["bloco do corpo do modo 1,", "visto de cima"],
        "inputs_title": "O que o módulo usa",
        "inputs": [r"$h$ e $v$ de cada célula, do roteamento",
                   r"massa corporal $m$, altura $y$, larguras, coeficientes",
                   r"de atrito $\mu$ e de arrasto $C_d$: parâmetros do modelo",
                   r"densidade da água $\rho_{\mathrm{w}}$, gravidade $g$",
                   r"no modo 3, a declividade $\beta$ do DEM"],
        "runs_title": "Onde cada modo roda",
        "runs": ["modo 1: na grade regular e na malha Voronoi",
                 "modo 3: só na grade regular; a malha Voronoi o recusa",
                 "o modo 2 não está implementado"],
        "m1_title": "Modo 1: risco por equilíbrio de forças",
        "m1_names": ["peso", "empuxo", "atrito", "arrasto", "razão"],
        "m1_ramp_lo": "0",
        "m1_ramp_hi": "1, risco total",
        "m1_notes": [r"limitado a $0 \leq R \leq 1$; $R = 1$ quando o empuxo",
                     r"sustenta todo o peso e $h > 0$",
                     r"cada célula guarda o seu $R$ máximo da simulação"],
        "m3_title": "Modo 3: classes de instabilidade",
        "m3_lines": [r"$A_{\mathrm{sub}}$, $V_{\mathrm{sub}}$, $x_c$: área, volume e centroide submersos",
                     r"$\beta$: declividade local do DEM em cada célula"],
        "classes": [
            ("1", "deslizamento", _SLIDE, [_T + ", atrito disponível"]),
            ("2", "tombamento", _TOPPLE,
             [r"$M$: momentos de $D$, $L$, $B_n$ e $W_p$",
              r"braço de $L$: " + _ARM,
              r"$M_{\mathrm{res}}$: momento de $W_n$"]),
            ("3", "afogamento", _DROWN, [r"$y$: altura do corpo"]),
        ],
        "m3_final": ["a classe é o maior código que se aplica; 0 é estável",
                     r"célula seca ($h = 0$) é estável em qualquer declive"],
    },
    "es": {
        "scene_title": "Fuerzas sobre una persona en el flujo",
        "scene_sub": [r"la profundidad $h$ y la velocidad $v$ vienen del enrutamiento,",
                      "en cada celda y en cada paso de tiempo"],
        "velocity": r"velocidad $v$",
        "depth": r"profundidad $h$",
        "slope": r"pendiente $\beta$",
        "drag": "arrastre",
        "buoyancy": "flotabilidad",
        "weight": "peso",
        "friction": "fricción",
        "top_view": ["bloque del cuerpo del modo 1,", "visto desde arriba"],
        "inputs_title": "Lo que usa el módulo",
        "inputs": [r"$h$ y $v$ de cada celda, del enrutamiento",
                   r"masa corporal $m$, altura $y$, anchos, coeficientes",
                   r"de fricción $\mu$ y de arrastre $C_d$: parámetros del modelo",
                   r"densidad del agua $\rho_{\mathrm{w}}$, gravedad $g$",
                   r"en el modo 3, la pendiente $\beta$ del DEM"],
        "runs_title": "Dónde se ejecuta cada modo",
        "runs": ["modo 1: en la malla regular y en la malla de Voronoi",
                 "modo 3: solo en la malla regular; la de Voronoi lo rechaza",
                 "el modo 2 no está implementado"],
        "m1_title": "Modo 1: riesgo por equilibrio de fuerzas",
        "m1_names": ["peso", "flotabilidad", "fricción", "arrastre", "razón"],
        "m1_ramp_lo": "0",
        "m1_ramp_hi": "1, riesgo total",
        "m1_notes": [r"recortado a $0 \leq R \leq 1$; $R = 1$ cuando la flotabilidad",
                     r"sostiene todo el peso y $h > 0$",
                     r"cada celda guarda su $R$ máximo de la simulación"],
        "m3_title": "Modo 3: clases de inestabilidad",
        "m3_lines": [r"$A_{\mathrm{sub}}$, $V_{\mathrm{sub}}$, $x_c$: área, volumen y centroide sumergidos",
                     r"$\beta$: pendiente local del DEM en cada celda"],
        "classes": [
            ("1", "deslizamiento", _SLIDE, [_T + ", fricción disponible"]),
            ("2", "vuelco", _TOPPLE,
             [r"$M$: momentos de $D$, $L$, $B_n$ y $W_p$",
              r"brazo de $L$: " + _ARM,
              r"$M_{\mathrm{res}}$: momento de $W_n$"]),
            ("3", "ahogamiento", _DROWN, [r"$y$: altura corporal"]),
        ],
        "m3_final": ["la clase es el mayor código aplicable; 0 es estable",
                     r"una celda seca ($h = 0$) es estable en toda pendiente"],
    },
}

# --- colours -----------------------------------------------------------------------------
# New colours (not in figures/palette.py), in the palette's OKLCH terms:
# PERSON: a neutral grey on the ink hue, between the "line" token (L 0.72) and card_edge.
PERSON = oklch_hex(0.74, 0.012, 250)
# HAZARD ramp for the risk index and the mode-3 classes: a warm red-orange at lightness
# steps like the soil tokens (0.93 to 0.62), chroma rising to near the water token's.
HAZARD = [oklch_hex(0.93, 0.030, 45), oklch_hex(0.84, 0.060, 40),
          oklch_hex(0.74, 0.090, 34), oklch_hex(0.62, 0.120, 30)]
GROUND_FILL = color("slot_rock_odd")
WATER_ALPHA = 0.17

W, H = 760, 676
SLOPE_DEG = 7.0
S = math.tan(math.radians(SLOPE_DEG))
X_FOOT, Y_FOOT = 200.0, 398.0      # where the person stands on the bed
PH = 276.0                          # drawn body height (px)
HW = 0.42 * PH                      # drawn depth
SCENE_X0, SCENE_X1 = 22.0, 374.0


def bed(x: float) -> float:
    return Y_FOOT + (x - X_FOOT) * S


def surface(x: float) -> float:
    return bed(x) - HW


# --- the person (profile pictogram, no face) ---------------------------------------------


def capsule(p0, p1, r, n=14):
    p0, p1 = np.asarray(p0, float), np.asarray(p1, float)
    a = math.atan2(*(p1 - p0)[::-1])
    t1 = np.linspace(a + math.pi / 2, a - math.pi / 2, n)
    t0 = np.linspace(a - math.pi / 2, a - 3 * math.pi / 2, n)
    return np.vstack([p1 + r * np.column_stack([np.cos(t1), np.sin(t1)]),
                      p0 + r * np.column_stack([np.cos(t0), np.sin(t0)])])


# Unit-height body in local coordinates (x downstream, y up, feet at the origin).
# The legs end at half height, where the mode-3 geometry splits legs from trunk.
BODY = [
    ("capsule", (-0.022, 0.50), (-0.050, 0.035), 0.040),    # back leg
    ("capsule", (0.022, 0.50), (0.050, 0.035), 0.040),      # front leg
    ("capsule", (-0.050, 0.018), (-0.088, 0.018), 0.019),   # feet, toes upstream
    ("capsule", (0.050, 0.018), (0.012, 0.018), 0.019),
    ("capsule", (0.0, 0.56), (0.0, 0.775), 0.066),          # trunk
    ("capsule", (0.0, 0.80), (0.0, 0.86), 0.028),           # neck
    ("circle", (0.0, 0.928), 0.060),                        # head
    ("capsule", (0.0, 0.765), (-0.075, 0.555), 0.028),      # arm, slightly forward
]


def person(ax, x0, y0, height, *, lean_deg=0.0, fill=PERSON, z=4):
    """Draw the pictogram with its feet at (x0, y0); lean_deg > 0 tips it downstream."""
    c, s = math.cos(math.radians(lean_deg)), math.sin(math.radians(lean_deg))

    def page(p):
        p = np.atleast_2d(p)
        xr = p[:, 0] * c + p[:, 1] * s
        yr = -p[:, 0] * s + p[:, 1] * c
        return np.column_stack([x0 + height * xr, y0 - height * yr])

    for part in BODY:
        if part[0] == "capsule":
            ax.add_patch(Polygon(page(capsule(part[1], part[2], part[3])), closed=True,
                                 facecolor=fill, edgecolor="none", zorder=z))
        else:
            ax.add_patch(Circle(page(part[1])[0], part[2] * height, facecolor=fill,
                                edgecolor="none", zorder=z))


def dimension(ax, x, y_top, y_bot, *, c=WATER, lw=0.9, head=(6.5, 5.5), z=9):
    """Vertical dimension line with a solid notched head at each end."""
    ax.plot([x, x], [y_top + head[0] * 0.6, y_bot - head[0] * 0.6], color=c, linewidth=lw, zorder=z)
    for tip, d in (((x, y_top), (0, -1)), ((x, y_bot), (0, 1))):
        ax.add_patch(Polygon(_kite_head(tip, d, *head), closed=True, facecolor=c,
                             edgecolor="none", zorder=z))


def text_width(sh: Sheet, s: str, *, bold=False, size=9.5) -> float:
    """Width in px of a label, measured with the figure's renderer."""
    renderer = FigureCanvasAgg(sh.fig).get_renderer()
    t = sh.text(0, 0, s, bold=bold, size=size)
    width = t.get_window_extent(renderer).width
    t.remove()
    return width


def draw(lang: str, preview: Path | None = None, check: bool = False) -> Path:
    t = LABELS[lang]
    sh = Sheet(W, H, "human-instability")
    ax = sh.ax

    # ---------------- left: the scene ----------------
    sh.text(34, 38, t["scene_title"], bold=True, size=11)
    for i, line in enumerate(t["scene_sub"]):
        sh.text(34, 60 + 17 * i, line)

    xs = np.array([SCENE_X0, SCENE_X1])
    ground_depth = 36
    ax.add_patch(Polygon([(SCENE_X0, bed(SCENE_X0)), (SCENE_X1, bed(SCENE_X1)),
                          (SCENE_X1, bed(SCENE_X1) + ground_depth),
                          (SCENE_X0, bed(SCENE_X0) + ground_depth)],
                         closed=True, facecolor=GROUND_FILL, edgecolor="none", zorder=2))
    ax.plot(xs, [bed(x) for x in xs], color=SOFT, linewidth=1.4, solid_capstyle="butt", zorder=6)

    # Person, then the water over the submerged part.
    person(ax, X_FOOT, Y_FOOT, PH)
    ax.add_patch(Polygon([(SCENE_X0, surface(SCENE_X0)), (SCENE_X1, surface(SCENE_X1)),
                          (SCENE_X1, bed(SCENE_X1)), (SCENE_X0, bed(SCENE_X0))],
                         closed=True, facecolor=WATER, alpha=WATER_ALPHA, edgecolor="none", zorder=5))
    ax.plot(xs, [surface(x) for x in xs], color=WATER, linewidth=1.6, solid_capstyle="butt", zorder=6)

    # Water-surface symbol (inverted triangle and two ticks), as in the site's column figure.
    xw = 338.0
    yw = surface(xw)
    ax.add_patch(Polygon([(xw - 8, yw - 11), (xw + 8, yw - 11), (xw, yw - 1)], closed=True,
                         facecolor=WATER, edgecolor="none", zorder=7))
    ax.plot([xw - 7, xw + 7], [yw + 5, yw + 5], color=WATER, linewidth=1.2, zorder=7)
    ax.plot([xw - 4, xw + 4], [yw + 9, yw + 9], color=WATER, linewidth=1.2, zorder=7)

    # Speed: three equal (depth-averaged) arrows upstream of the person, parallel to the bed.
    for frac in (0.34, 0.56, 0.78):
        xa, xb = 40.0, 106.0
        sh.arrow([(xa, bed(xa) - frac * HW), (xb, bed(xb) - frac * HW)], c=WATER,
                 width=(0.9, 2.0), head=(9, 8), z=8)
    sh.text(40, surface(40) - 14, t["velocity"])

    # Depth: dimension line downstream of the person, labelled on its right; a label too
    # long for the water left there goes under the bed, centred on the line.
    xd = 300.0
    dimension(ax, xd, surface(xd), bed(xd))
    if xd + 9 + text_width(sh, t["depth"]) <= SCENE_X1 - 4:
        sh.text(xd + 9, (surface(xd) + bed(xd)) / 2 + 2, t["depth"])
    else:
        sh.text(xd, bed(xd) + 19, t["depth"], ha="center")

    # Slope: horizontal reference and the angle beta at the bed, upstream.
    xs0 = 30.0
    ys0 = bed(xs0)
    ax.plot([xs0, xs0 + 104], [ys0, ys0], color=SOFT, linewidth=0.9, linestyle=(0, (1.2, 2.4)), zorder=7)
    # Arc angles are measured with y up; the axis is flipped, so 0 to +beta opens toward the bed.
    ax.add_patch(Arc((xs0, ys0), 180, 180, theta1=0.0, theta2=SLOPE_DEG, color=SOFT,
                     linewidth=1.0, zorder=7))
    sh.text(xs0 + 10, bed(xs0 + 10) + 18, t["slope"])

    # Forces (ink ribbons) at their points of application.
    fw = dict(width=(1.6, 4.4), head=(12, 11), c=INK, z=9)
    y_com = Y_FOOT - 0.56 * PH
    x_w = X_FOOT + 8
    ax.add_patch(Circle((x_w, y_com), 2.6, facecolor=INK, edgecolor="none", zorder=10))
    sh.arrow([(x_w, y_com), (x_w, y_com + 46)], **fw)
    sh.text(x_w + 16, y_com + 12, t["weight"])

    y_cb = Y_FOOT - HW / 2
    x_b = X_FOOT - 9
    ax.add_patch(Circle((x_b, y_cb), 2.6, facecolor=INK, edgecolor="none", zorder=10))
    sh.arrow([(x_b, y_cb), (x_b, y_cb - 46)], **fw)
    sh.text(x_b - 12, y_cb - 24, t["buoyancy"], ha="right")

    x_d0 = X_FOOT + 16
    sh.arrow([(x_d0, y_cb + (x_d0 - X_FOOT) * S), (x_d0 + 54, y_cb + (x_d0 + 54 - X_FOOT) * S)], **fw)
    sh.text(x_d0 + 10, y_cb - 15 + 10 * S, t["drag"])

    x_f0, x_f1 = X_FOOT - 26, X_FOOT - 80
    sh.arrow([(x_f0, bed(x_f0) + 8), (x_f1, bed(x_f1) + 8)], **fw)
    sh.text(x_f1 + 18, bed(x_f1) + 24, t["friction"])

    # Mode-1 body block seen from above: w1 across the flow, w2 along it. The caption is
    # centred on the block, which moves left when a long caption would reach the card.
    blk_w, blk_h = 22, 38            # 0.20 m along the flow, 0.35 m across it
    cap_w = max(text_width(sh, line, size=9) for line in t["top_view"])
    tvx, tvy = min(302.0, SCENE_X1 + 6 - cap_w / 2 - blk_w / 2), 146
    for i, line in enumerate(t["top_view"]):
        sh.text(tvx + blk_w / 2, tvy - 44 + 15 * i, line, ha="center", size=9, c=SOFT)
    ax.add_patch(Rectangle((tvx, tvy), blk_w, blk_h, facecolor=PERSON, edgecolor="none", zorder=3))
    sh.arrow([(tvx - 38, tvy + blk_h / 2), (tvx - 7, tvy + blk_h / 2)], c=WATER, width=(0.9, 2.0),
             head=(8, 7), z=4)
    sh.text(tvx + blk_w + 6, tvy + blk_h / 2, r"$w_1$", size=10)
    sh.text(tvx + blk_w / 2, tvy + blk_h + 12, r"$w_2$", size=10, ha="center")

    # Inputs and where each mode runs, under the scene.
    y_in = 478
    sh.note(34, y_in, t["inputs_title"], t["inputs"])
    y_runs = y_in + 20 + 17 * (len(t["inputs"]) - 1) + 27
    sh.note(34, y_runs, t["runs_title"], t["runs"])

    # ---------------- right: mode 1 ----------------
    bx, bw = 394, 344
    sh.box(bx, 24, bw, 230, fill="#ffffff", edge=color("card_edge"))
    sh.text(bx + 14, 44, t["m1_title"], bold=True, size=10.5)
    col = bx + 14 + max(68.0, max(text_width(sh, n) for n in t["m1_names"]) + 12)
    y = 70
    for name, eq in zip(t["m1_names"], _EQ_M1):
        sh.text(bx + 14, y, name, c=SOFT)
        sh.text(col, y, eq, size=10)
        y += 22 if r"\frac" in eq else 20
    # The ramp ends where its "1" label still fits inside the card.
    r_x0, r_y = col, y + 4
    r_x1 = min(col + 170, bx + bw - 14 - 6 - text_width(sh, t["m1_ramp_hi"]))
    ramp_strip(ax, r_x0, r_x1, r_y, 10)
    sh.text(r_x0 - 6, r_y + 5, t["m1_ramp_lo"], ha="right")
    sh.text(r_x1 + 6, r_y + 5, t["m1_ramp_hi"])
    y = r_y + 30
    for line in t["m1_notes"]:
        sh.text(bx + 14, y, line)
        y += 17

    # ---------------- right: mode 3 ----------------
    by = 266
    sh.box(bx, by, bw, H - 20 - by, fill="#ffffff", edge=color("card_edge"))
    sh.text(bx + 14, by + 20, t["m3_title"], bold=True, size=10.5)
    y = by + 44
    for line in t["m3_lines"]:
        sh.text(bx + 14, y, line, size=9.5)
        y += 22
    for i, line in enumerate(_EQ_M3):
        sh.text(bx + 14, y, line, size=10)
        y += 23 if i == 0 else 22

    icon_x = bx + 38
    chip_x = bx + 72
    cond_x = chip_x + 26 + max(74.0, max(text_width(sh, c[1], bold=True, size=10)
                                         for c in t["classes"]) + 12)
    yc = y + 30
    for k, (code, name, cond, expl) in enumerate(t["classes"]):
        draw_icon(sh, k, icon_x, yc + 20, 50)
        sh.box(chip_x, yc - 9, 18, 18, fill=HAZARD[k + 1], edge="none", radius=4, z=3)
        sh.text(chip_x + 9, yc + 0.5, code, bold=True, size=10, ha="center",
                c="#ffffff" if k == 2 else INK)
        sh.text(chip_x + 26, yc, name, bold=True, size=10)
        sh.text(cond_x, yc, cond, size=10)
        for j, line in enumerate(expl):
            sh.text(chip_x + 26, yc + 19 + 17 * j, line)
        yc += 56 + 17 * (len(expl) - 1)
    for i, line in enumerate(t["m3_final"]):
        sh.text(bx + 14, H - 20 - 18 - 17 * (len(t["m3_final"]) - 1 - i), line)

    if check:
        report(sh)
    svg = sh.save(STATIC / "theory", lang, preview)
    print("wrote", svg)
    return svg


def ramp_strip(ax, x0, x1, y, h, n=48):
    """The HAZARD ramp from 0 to 1 as thin vector strips, with a hairline frame."""
    stops = np.array([[int(c[i:i + 2], 16) for i in (1, 3, 5)] for c in HAZARD]) / 255
    for k in range(n):
        f = k / (n - 1) * (len(stops) - 1)
        i = min(int(f), len(stops) - 2)
        rgb = stops[i] + (stops[i + 1] - stops[i]) * (f - i)
        ax.add_patch(Rectangle((x0 + k * (x1 - x0) / n, y), (x1 - x0) / n + 0.3, h,
                               facecolor=rgb, edgecolor="none", zorder=3))
    ax.add_patch(Rectangle((x0, y), x1 - x0, h, fill=False, edgecolor=color("guide"),
                           linewidth=0.6, zorder=4))


def draw_icon(sh: Sheet, kind: int, cx: float, ground_y: float, size: float) -> None:
    """Failure pictograms: 0 slide, 1 topple, 2 drowning, with the feet at (cx, ground_y)."""
    ax = sh.ax
    half = 25
    ax.plot([cx - half, cx + half], [ground_y, ground_y], color=SOFT, linewidth=1.0, zorder=6)
    depth = {0: 0.36, 1: 0.36, 2: 0.88}[kind] * size
    if kind == 0:
        person(ax, cx - 4, ground_y, size)
        sh.arrow([(cx - 1, ground_y - 4), (cx + 21, ground_y - 4)], c=INK, width=(1.0, 2.6),
                 head=(8, 7), z=9)
    elif kind == 1:
        person(ax, cx - 8, ground_y, size, lean_deg=36)
        # Rotation about the feet, drawn above them (negative angles: the axis is flipped).
        r_arc, a0, a1 = 40.0, 104.0, 64.0     # degrees, measured with y up
        ax.add_patch(Arc((cx - 8, ground_y), 2 * r_arc, 2 * r_arc, theta1=-a0, theta2=-a1,
                         color=INK, linewidth=1.1, zorder=9))
        end = np.array([cx - 8 + r_arc * math.cos(math.radians(a1)),
                        ground_y - r_arc * math.sin(math.radians(a1))])
        tangent = np.array([math.sin(math.radians(a1)), math.cos(math.radians(a1))])
        ax.add_patch(Polygon(_kite_head(end + tangent * 4, tangent, 7, 6), closed=True,
                             facecolor=INK, edgecolor="none", zorder=9))
    else:
        person(ax, cx - 4, ground_y, size)
    ax.add_patch(Rectangle((cx - half, ground_y - depth), 2 * half, depth, facecolor=WATER,
                           alpha=WATER_ALPHA + 0.03, edgecolor="none", zorder=5))
    ax.plot([cx - half, cx + half], [ground_y - depth, ground_y - depth], color=WATER,
            linewidth=1.1, zorder=6)


def report(sh: Sheet) -> None:
    """List text boxes that overlap each other, leave the sheet or cross a card edge."""
    renderer = FigureCanvasAgg(sh.fig).get_renderer()
    boxes = []
    for txt in sh.ax.texts:
        bb = txt.get_window_extent(renderer)
        x0, x1, y0, y1 = bb.x0, bb.x1, sh.H - bb.y1, sh.H - bb.y0
        boxes.append((txt.get_text(), x0, y0, x1, y1))
        if x0 < 10 or x1 > sh.W - 10 or y0 < 10 or y1 > sh.H - 10:
            print("OUTSIDE", txt.get_text()[:50], round(x0), round(y0), round(x1), round(y1))
        if (x0 < 394 < x1) or (394 <= x0 and x1 > 738 - 6):
            print("CARD", txt.get_text()[:50], round(x0), round(x1))
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
