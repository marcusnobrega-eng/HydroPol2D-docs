""""One surface time step, in order": schematic for docs/getting-started/overview.md.

Six steps of one surface time step, in the order of the HydroPol2D-Python main loop, the
surface clock that sets the step length, and the groundwater clock that decides when lateral
groundwater flow runs. A strip at the bottom shows the two clocks over a run.

Snow is split before the canopy: snowfall goes to the snowpack, only rain enters the canopy,
and melt reaches the ground without passing through it (step 2). The local water-table update
runs every step; the head change it makes since the last lateral update is one of the three
triggers of the groundwater clock, which is always asynchronous (step 4 and the right card).
The human-instability step draws the risk index (mode 1) or the classes (mode 3).

Run from the repository root:

    python3 figures/time_step_order.py [preview-folder]

Output: static/img/getting-started/time-step-order.svg (en), time-step-order.pt.svg and
time-step-order.es.svg, and a PNG of each in the preview folder when one is given.
"""

from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
from matplotlib.backends.backend_agg import FigureCanvasAgg
from matplotlib.patches import Circle, Polygon

from site_style import INK, SOFT, STATIC, WATER, Sheet, color
from layered_column import _kite_head

NAME = "time-step-order"
SECTION = "getting-started"

# --- text ---------------------------------------------------------------------------------
# A step is (title, tag, lines); the box grows with its number of lines. Parameter names are
# the case-workbook names, as on the configuration pages.
LABELS = {
    "en": {
        "loop_title": r"One surface time step, of length $\Delta t$",
        "steps": [
            ("Forcing", "", ["rainfall and ET demand for this step; air",
                             "temperature and wind when snow is on"]),
            ("Snow, canopy and soil", "", ["snowfall goes to the snowpack and only rain to the",
                                           "canopy; melt and throughfall infiltrate into the",
                                           "soil layers, then evaporation and soil ET"]),
            ("Recharge and capillary rise", "groundwater on", [
                "drainage from the soil to the water table, and",
                "capillary rise when on; the net goes to the clock"]),
            ("Water table", "groundwater on", [
                r"the head moves by the net exchange over $S_y$;",
                "exfiltration and saturation excess go to the surface;",
                "lateral flow runs only when the clock is due"]),
            ("Surface routing", "", ["inflow hydrographs and stages enter, then the",
                                     "selected routing family moves water between cells"]),
            ("Water quality and hazard", "", ["pollutant washoff and transport, and the risk",
                                              "index or classes of human instability, when on"]),
        ],
        "loop": r"next step,  $t + \Delta t$",
        "surface_title": "Surface clock",
        "surface_eq": r"$\Delta t = \alpha\,\Delta x\,/\,(|u| + \sqrt{g\,h})$",
        "surface_lines": [r"at the wet cell that limits it most; $\alpha$ is the",
                          "Courant number. It stays between the minimum",
                          "and maximum time step, and a step also ends",
                          "at forcing changes and output times."],
        "surface_params": "alfa_min,  min_time_step,  max_time_step",
        "gw_title": "Groundwater clock",
        "gw_intro": [r"Each step adds its $\Delta t$ and the net exchange.",
                     "Lateral flow is due when one of these holds:"],
        "gw_tag": "lateral flow on",
        # Each condition: lines of ("text" | "eq" | "param", string).
        "gw_conditions": [
            [("text", "elapsed time ≥ target interval, shortened"),
             ("text", "when needed to the stability cap"),
             ("eq", r"$\Delta t_{\mathrm{gw}} = C_{\mathrm{gw}}\,L_{\mathrm{grid}}^2\,/\,(4\,D_{\max})$,  $D = K H / S_y$,"),
             ("text", "but never below the minimum interval"),
             ("param", "groundwater_target_dt_min (1440 min),"),
             ("param", r"groundwater_courant ($C_{\mathrm{gw}}$ = 0.25),"),
             ("param", "groundwater_min_dt_min (1 min)")],
            [("text", "head change since the last lateral update"),
             ("text", "≥ its maximum"),
             ("param", "groundwater_max_head_change_m (0.25 m)")],
            [("text", "the run reaches its last step")],
        ],
        "gw_then": ["Then 2D Boussinesq flow runs over the elapsed",
                    "interval, in substeps, and the clock resets."],
        "strip_title": "The two clocks over a run (schematic, not to scale)",
        "strip_rows": ["surface steps", "elapsed time", "lateral flow"],
        "strip_target": "target interval",
        "strip_time": "time",
    },
    "pt": {
        "tags_below": True,
        "loop_title": r"Um passo de tempo superficial, de duração $\Delta t$",
        "steps": [
            ("Forçantes", "", ["chuva e demanda de ET deste passo; temperatura",
                               "do ar e vento quando a neve está ativa"]),
            ("Neve, dossel e solo", "", ["a neve vai para o manto de neve e só a chuva",
                                         "entra no dossel; o degelo e a chuva que passa",
                                         "pelo dossel infiltram nas camadas do solo;",
                                         "depois, evaporação e ET do solo"]),
            ("Recarga e ascensão capilar", "água subterrânea ativa", [
                "drenagem do solo até o lençol freático e ascensão",
                "capilar, se ativa; o saldo vai para o relógio"]),
            ("Lençol freático", "água subterrânea ativa", [
                r"a carga muda com a troca líquida dividida por $S_y$;",
                "exfiltração e excesso de saturação vão à superfície",
                "e o fluxo lateral só roda quando o relógio dispara"]),
            ("Roteamento superficial", "", ["entram os hidrogramas de entrada e os níveis;",
                                            "depois, a família de roteamento selecionada",
                                            "move a água entre as células"]),
            ("Qualidade da água e risco", "", ["lavagem e transporte de poluentes, e o índice ou",
                                               "as classes de instabilidade humana, quando ativos"]),
        ],
        "loop": r"próximo passo,  $t + \Delta t$",
        "surface_title": "Relógio da superfície",
        "surface_eq": r"$\Delta t = \alpha\,\Delta x\,/\,(|u| + \sqrt{g\,h})$",
        "surface_lines": [r"na célula molhada que mais o limita; $\alpha$ é o",
                          "número de Courant. Ele fica entre o passo de",
                          "tempo mínimo e o máximo, e um passo também",
                          "termina nas mudanças de forçante e nos tempos",
                          "de saída."],
        "surface_params": "alfa_min,  min_time_step,  max_time_step",
        "gw_title": "Relógio da água subterrânea",
        "gw_intro": [r"Cada passo soma o seu $\Delta t$ e a troca líquida.",
                     "O fluxo lateral roda quando vale uma destas:"],
        "gw_tag": "fluxo lateral ativo",
        "gw_conditions": [
            [("text", "tempo decorrido ≥ intervalo alvo, encurtado"),
             ("text", "quando preciso até o limite de estabilidade"),
             ("eq", r"$\Delta t_{\mathrm{gw}} = C_{\mathrm{gw}}\,L_{\mathrm{grid}}^2\,/\,(4\,D_{\max})$,  $D = K H / S_y$,"),
             ("text", "mas nunca abaixo do intervalo mínimo"),
             ("param", "groundwater_target_dt_min (1440 min),"),
             ("param", r"groundwater_courant ($C_{\mathrm{gw}}$ = 0,25),"),
             ("param", "groundwater_min_dt_min (1 min)")],
            [("text", "variação da carga desde a última atualização"),
             ("text", "lateral ≥ o seu máximo"),
             ("param", "groundwater_max_head_change_m (0,25 m)")],
            [("text", "a simulação chega ao último passo")],
        ],
        "gw_then": ["Então o fluxo 2D de Boussinesq roda sobre o",
                    "intervalo decorrido, em subpassos, e o relógio",
                    "volta a zero."],
        "strip_title": "Os dois relógios ao longo de uma simulação (esquema, fora de escala)",
        "strip_rows": ["passos da superfície", "tempo decorrido", "fluxo lateral"],
        "strip_target": "intervalo alvo",
        "strip_time": "tempo",
    },
    "es": {
        "tags_below": True,
        "loop_title": r"Un paso de tiempo superficial, de duración $\Delta t$",
        "steps": [
            ("Forzantes", "", ["lluvia y demanda de ET de este paso; temperatura",
                               "del aire y viento cuando la nieve está activa"]),
            ("Nieve, dosel y suelo", "", ["la nevada va al manto de nieve y solo la lluvia",
                                          "entra en el dosel; el deshielo y la lluvia que",
                                          "atraviesa el dosel se infiltran en las capas del",
                                          "suelo; luego, evaporación y ET del suelo"]),
            ("Recarga y ascenso capilar", "agua subterránea activa", [
                "drenaje del suelo al nivel freático y ascenso",
                "capilar, si está activo; el neto va al reloj"]),
            ("Nivel freático", "agua subterránea activa", [
                r"la carga cambia con el intercambio neto sobre $S_y$;",
                "la exfiltración y el exceso de saturación van a la",
                "superficie; el flujo lateral solo corre cuando",
                "vence el reloj"]),
            ("Enrutamiento superficial", "", ["entran los hidrogramas de entrada y los niveles;",
                                              "luego, la familia de enrutamiento elegida",
                                              "mueve el agua entre las celdas"]),
            ("Calidad del agua y riesgo", "", ["lavado y transporte de contaminantes, y el",
                                               "índice o las clases de inestabilidad humana,",
                                               "cuando están activos"]),
        ],
        "loop": r"siguiente paso,  $t + \Delta t$",
        "surface_title": "Reloj superficial",
        "surface_eq": r"$\Delta t = \alpha\,\Delta x\,/\,(|u| + \sqrt{g\,h})$",
        "surface_lines": [r"en la celda mojada que más lo limita; $\alpha$ es el",
                          "número de Courant. Queda entre el paso de",
                          "tiempo mínimo y el máximo, y un paso también",
                          "termina en los cambios de forzante y en los",
                          "tiempos de salida."],
        "surface_params": "alfa_min,  min_time_step,  max_time_step",
        "gw_title": "Reloj del agua subterránea",
        "gw_intro": [r"Cada paso suma su $\Delta t$ y el intercambio neto.",
                     "El flujo lateral corre si se cumple una de estas:"],
        "gw_tag": "flujo lateral activo",
        "gw_conditions": [
            [("text", "tiempo transcurrido ≥ intervalo objetivo,"),
             ("text", "acortado si hace falta al límite de estabilidad"),
             ("eq", r"$\Delta t_{\mathrm{gw}} = C_{\mathrm{gw}}\,L_{\mathrm{grid}}^2\,/\,(4\,D_{\max})$,  $D = K H / S_y$,"),
             ("text", "pero nunca por debajo del intervalo mínimo"),
             ("param", "groundwater_target_dt_min (1440 min),"),
             ("param", r"groundwater_courant ($C_{\mathrm{gw}}$ = 0,25),"),
             ("param", "groundwater_min_dt_min (1 min)")],
            [("text", "cambio de carga desde la última actualización"),
             ("text", "lateral ≥ su máximo"),
             ("param", "groundwater_max_head_change_m (0,25 m)")],
            [("text", "la simulación llega a su último paso")],
        ],
        "gw_then": ["Luego el flujo 2D de Boussinesq corre sobre el",
                    "intervalo transcurrido, en subpasos, y el reloj",
                    "se reinicia."],
        "strip_title": "Los dos relojes a lo largo de una simulación (esquema, sin escala)",
        "strip_rows": ["pasos superficiales", "tiempo transcurrido", "flujo lateral"],
        "strip_target": "intervalo objetivo",
        "strip_time": "tiempo",
    },
}

W = 760
HEAD = (10, 9)  # one arrowhead for the whole figure (length, width), px

# Layout grid (px, y downward).
LX0, LX1 = 48, 398          # step boxes
RX0, RX1 = 426, 738         # clock cards
GAP, TOP = 16, 48
LOOP_X = 30                 # return corridor, left of the boxes

# Fills by domain: neutral (forcing, diagnostics), soil, groundwater, surface water.
STEP_FILL = ["slot_rock_even", "slot_near_surface", "deep_fill", "deep_fill",
             "card", "slot_rock_even"]
STEP_EDGE = ["card_edge", "card_edge", "card_edge", "card_edge", "water", "card_edge"]


class Checker:
    """Warn when a label runs past the room it was given."""

    def __init__(self, sheet: Sheet) -> None:
        self.canvas = FigureCanvasAgg(sheet.fig)
        self.problems: list[str] = []

    def room(self, artist, x_max: float, name: str) -> None:
        box = artist.get_window_extent(self.canvas.get_renderer())
        if box.x1 > x_max + 0.5:
            self.problems.append(f"{name}: ends at {box.x1:.0f}, room to {x_max:.0f}")

    def right(self, artist) -> float:
        return artist.get_window_extent(self.canvas.get_renderer()).x1


def line_arrow(s: Sheet, xs, ys, *, c=INK, lw=1.2, z=5, dashed=False):
    """Right-angle polyline ending in the figure's notched head."""
    xs, ys = list(xs), list(ys)
    d = np.array([xs[-1] - xs[-2], ys[-1] - ys[-2]], float)
    d /= np.linalg.norm(d)
    end = np.array([xs[-1], ys[-1]]) - d * HEAD[0] * 0.6
    style = (0, (4, 3)) if dashed else "-"
    s.ax.plot(xs[:-1] + [end[0]], ys[:-1] + [end[1]], color=c, linewidth=lw, linestyle=style,
              solid_capstyle="butt", solid_joinstyle="miter", zorder=z)
    s.ax.add_patch(Polygon(_kite_head((xs[-1], ys[-1]), d, *HEAD), closed=True, facecolor=c,
                           edgecolor="none", zorder=z))


def layout(t):
    """Step boxes: 28 px plus 15 px a line; the strip and the card height follow from them.
    Where the language sets tags_below, a tag takes its own line under the title."""
    below = t.get("tags_below", False)
    step_h = [28 + 15 * (len(lines) + (1 if tag and below else 0)) for _, tag, lines in t["steps"]]
    step_y = [TOP + sum(step_h[:k]) + GAP * k for k in range(len(step_h))]
    strip_top = step_y[-1] + step_h[-1] + 18
    return step_y, step_h, strip_top, strip_top + 105


def build(lang: str = "en") -> Sheet:
    t = LABELS[lang]
    step_y, step_h, strip_top, height = layout(t)
    s = Sheet(W, height, NAME)
    chk = Checker(s)

    # --- the loop of six steps -----------------------------------------------------
    chk.room(s.text(LX0, 28, t["loop_title"], bold=True, size=11), LX1, "loop title")
    for k, (y, h, (title, tag, lines)) in enumerate(zip(step_y, step_h, t["steps"])):
        s.box(LX0, y, LX1 - LX0, h, fill=color(STEP_FILL[k]), edge=color(STEP_EDGE[k]), radius=6)
        s.ax.add_patch(Circle((LX0 + 20, y + 19), 10, facecolor=INK, edgecolor="none", zorder=6))
        s.text(LX0 + 20, y + 19.5, str(k + 1), bold=True, size=10, c="#ffffff", ha="center", z=7)
        head = s.text(LX0 + 40, y + 18, title, bold=True, size=10.5)
        chk.room(head, LX1 - 8, f"step {k + 1} title")
        first = 35
        if tag and t.get("tags_below", False):
            chk.room(s.text(LX0 + 40, y + 34, tag, size=9, c=SOFT), LX1 - 8, f"step {k + 1} tag")
            first = 50
        elif tag:
            chk.room(s.text(chk.right(head) + 8, y + 18, tag, size=9, c=SOFT), LX1 - 8, f"step {k + 1} tag")
        for i, line in enumerate(lines):
            chk.room(s.text(LX0 + 40, y + first + 15 * i, line), LX1 - 8, f"step {k + 1} line {i + 1}")
    xm = (LX0 + LX1) / 2
    for y, h in zip(step_y[:-1], step_h[:-1]):
        line_arrow(s, [xm, xm], [y + h, y + h + GAP])

    # Return to step 1 for the next surface step.
    y_last, y_first = step_y[-1] + step_h[-1] / 2, step_y[0] + step_h[0] / 2
    line_arrow(s, [LX0, LOOP_X, LOOP_X, LX0], [y_last, y_last, y_first, y_first])
    s.text(LOOP_X - 13, (y_first + y_last) / 2, t["loop"], size=9.5, c=SOFT, rotation=90, ha="center")

    # --- surface clock ---------------------------------------------------------------
    sy0 = TOP
    x = RX0 + 14
    s.text(x, sy0 + 18, t["surface_title"], bold=True, size=10.5)
    chk.room(s.text(x, sy0 + 42, t["surface_eq"], size=10.5), RX1 - 8, "surface eq")
    y = sy0 + 63
    for i, line in enumerate(t["surface_lines"]):
        chk.room(s.text(x, y, line), RX1 - 8, f"surface line {i + 1}")
        y += 15
    chk.room(s.text(x, y + 3, t["surface_params"], size=9, c=SOFT), RX1 - 8, "surface params")
    sy1 = y + 17
    s.box(RX0, sy0, RX1 - RX0, sy1 - sy0, fill="#ffffff", edge=color("guide"), radius=6)

    # --- groundwater clock -----------------------------------------------------------
    gy0 = sy1 + 14
    gw_head = s.text(x, gy0 + 18, t["gw_title"], bold=True, size=10.5, c=WATER)
    y = gy0 + 40
    if t.get("tags_below", False):
        chk.room(s.text(x, gy0 + 35, t["gw_tag"], size=9, c=SOFT), RX1 - 8, "gw tag")
        y += 15
    else:
        chk.room(s.text(chk.right(gw_head) + 8, gy0 + 18, t["gw_tag"], size=9, c=SOFT), RX1 - 8, "gw tag")
    for line in t["gw_intro"]:
        chk.room(s.text(x, y, line), RX1 - 8, "gw intro")
        y += 16
    y += 4
    for k, item in enumerate(t["gw_conditions"]):
        s.ax.add_patch(Circle((x + 4, y), 2.6, facecolor=WATER, edgecolor="none", zorder=6))
        for kind, line in item:
            if kind == "eq":
                chk.room(s.text(x + 14, y + 2, line, size=10), RX1 - 8, "gw cap equation")
                y += 20
            elif kind == "param":
                chk.room(s.text(x + 14, y, line, size=9, c=SOFT), RX1 - 8, "gw params")
                y += 14
            else:
                chk.room(s.text(x + 14, y, line), RX1 - 8, f"gw condition {k + 1}")
                y += 16
        y += 5
    y += 2
    for line in t["gw_then"]:
        chk.room(s.text(x, y, line), RX1 - 8, "gw then")
        y += 16
    gy1 = y - 4
    s.box(RX0, gy0, RX1 - RX0, gy1 - gy0, fill=color("deep_fill"), edge=WATER, radius=6)

    # Exchange into the clock (step 3), lateral flow back when due (step 4).
    y3 = step_y[2] + step_h[2] / 2
    y4 = step_y[3] + step_h[3] / 2
    if not (gy0 + 8 < y3 < y4 < gy1 - 8):
        chk.problems.append(f"arrows at {y3:.0f} and {y4:.0f} miss the card {gy0:.0f}-{gy1:.0f}")
    if gy1 > strip_top - 14:
        chk.problems.append(f"groundwater card ends at {gy1:.0f}, strip starts at {strip_top:.0f}")
    line_arrow(s, [LX1, RX0], [y3, y3], c=WATER, lw=1.6)
    line_arrow(s, [RX0, LX1], [y4, y4], c=WATER, lw=1.4, dashed=True)

    # --- strip: the two clocks over a run ----------------------------------------------
    top = strip_top
    chk.room(s.text(LX0, top, t["strip_title"], bold=True, size=10.5), W - 12, "strip title")
    row_tick, row_hi, row_base, row_gw = top + 21, top + 45, top + 72, top + 88
    label_right = max(
        chk.right(s.text(LX0, yy, label, size=9.5, c=SOFT))
        for label, yy in zip(t["strip_rows"], (row_tick, (row_hi + row_base) / 2, row_gw))
    )
    # The axis starts after the longest row label; "time" sits past its arrow.
    time_w = chk.right(s.text(0, -50, t["strip_time"], size=9, c=SOFT))
    ax0, ax1 = max(150.0, label_right + 14), W - 12 - time_w - 18

    # Surface steps: short while water moves fast, longer later (schematic).
    frac, times = 0.0, [0.0]
    while frac < 1.0:
        dt = 0.0065 + 0.018 * (1.0 - np.exp(-((frac - 0.30) / 0.16) ** 2))
        frac = min(1.0, frac + dt)
        times.append(frac)
    times = np.array(times)
    xs = ax0 + (ax1 - ax0) * times
    s.ax.vlines(xs, row_tick - 5, row_tick + 5, colors=INK, linewidth=0.7, zorder=5)

    # Elapsed time since the last lateral update: rises by dt every step and resets
    # at the first step end where it reaches the target interval, and at the run end.
    target = 0.215
    hi = row_base - row_hi
    stair_x, stair_y, updates = [xs[0]], [row_base], []
    elapsed = 0.0
    for k in range(1, len(times)):
        elapsed += times[k] - times[k - 1]
        level = row_base - hi * elapsed / target
        stair_x += [xs[k - 1], xs[k]]
        stair_y += [level, level]
        if elapsed >= target - 1e-12 or k == len(times) - 1:
            updates.append(xs[k])
            stair_x.append(xs[k])
            stair_y.append(row_base)
            elapsed = 0.0
    s.ax.plot(stair_x, stair_y, color=WATER, linewidth=1.1, solid_joinstyle="miter", zorder=6)
    s.line([ax0, ax1], [row_hi, row_hi], c=SOFT, lw=0.8, style=(0, (2, 2)))
    s.text(updates[0] + 8, row_hi - 9, t["strip_target"], size=9, c=SOFT)
    line_arrow(s, [ax0, ax1 + 14], [row_base, row_base], c=INK, lw=0.9)
    for xu in updates:
        s.ax.add_patch(Polygon([(xu, row_gw - 6), (xu + 5, row_gw), (xu, row_gw + 6), (xu - 5, row_gw)],
                               closed=True, facecolor=WATER, edgecolor="none", zorder=7))
    s.text(ax1 + 18, row_base, t["strip_time"], size=9, c=SOFT)

    for problem in chk.problems:
        print(f"ROOM [{lang}]:", problem)
    # Drop the measuring artist placed off the card.
    for artist in list(s.ax.texts):
        if artist.get_position()[1] < 0:
            artist.remove()
    return s


def main(preview: Path | None = None) -> None:
    for lang in LABELS:
        svg = build(lang).save(STATIC / SECTION, lang, preview)
        print("wrote", svg.relative_to(STATIC.parent.parent))


if __name__ == "__main__":
    main(Path(sys.argv[1]) if len(sys.argv) > 1 else None)
