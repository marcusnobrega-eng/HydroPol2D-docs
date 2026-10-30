"""How a module is validated, for docs/validation/overview.md.

A module, its validation case, the reference (one of five evidence types), the comparison
and the two outcomes; where the cases run (the shared V-tilted catchment, drawn in plan
with north up and the outlet on the north edge, and the dedicated hydrodynamic
benchmarks); and two cases traced through.

Run from the repository root:

    python3 figures/validation_logic.py [preview-folder]

Output: static/img/validation/validation-logic.svg (en), validation-logic.pt.svg and
validation-logic.es.svg, a PNG of each in the preview folder, if given, and the icon
licence log figures/validation_logic_icons.csv.
"""

from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
from matplotlib.patches import Polygon, Rectangle

sys.path.insert(0, str(Path(__file__).resolve().parent))
import flow_kit as fk  # noqa: E402
import lucide_draw as li  # noqa: E402
from site_style import HERE, INK, SOFT, STATIC, WATER, Sheet, color, oklch_hex  # noqa: E402

W, H = 760, 636
NAME = "validation-logic"
B, L = True, False

# New colour (not in the shared palette): a light fill in the hue of the "ground" green token, for
# acceptance evidence; same lightness as the deep_fill and rock_a tokens.
ACCEPT_FILL = oklch_hex(0.955, 0.030, 145)
ACCEPT_EDGE = color("ground")

LABELS = {
    "en": {
        "module": "Module",
        "module_lines": ["one module, with", "its process", "isolated"],
        "case": "Validation case",
        "case_lines": ["defined inputs", "expected response", "metrics", "acceptance thresholds", "outputs"],
        "compare": "Compare",
        "compare_lines": ["run the module and", "score its response", "against the reference"],
        "reference": "Reference: one of five evidence types",
        "evidence": [
            ("Analytical solution", "a closed-form or exact solution"),
            ("Independent reference", "a separate calculation of the same process"),
            ("Exact bookkeeping", "conservation under prescribed forcing"),
            ("Benchmark hydrograph", "a published or digitized benchmark"),
            ("Numerical reference", "a documented, refined simulation"),
        ],
        "accept": "Acceptance evidence",
        "accept_lines": ["a proper reference, and", "the thresholds are met;", "it counts toward the",
                         "module's validation status"],
        "diag": "Diagnostic",
        "diag_lines": ["no appropriate reference:", "the case stays visible,", "but is not used as",
                       "acceptance evidence"],
        "vtilt": "Shared V-tilted catchment",
        "vtilt_lines": ["many hydrologic and groundwater", "cases: a common DEM, soil, land",
                        "cover, LAI, groundwater, boundaries"],
        "bench": "Dedicated hydrodynamic benchmarks",
        "bench_lines": ["geometries designed for those", "solutions: the Ritter dam-break",
                        "and the non-breaking wave"],
        "outlet": "outlet",
        "dam": "dam",
        "examples": "Two cases traced through",
        "cols": ["Module", "Case", "Reference", "Result", "Counts as"],
        "ex1": {
            "module": ["Reservoir and", "control", "structures"],
            "case": [[("VAL-RES-001", B)], "a constant-area", "reservoir, one rating", "curve, no inflow"],
            "reference": [[("Analytical solution", B)], "storage depletion", [("Exact bookkeeping", B)], "volume ledger"],
            "result": [[("passed all thresholds", B)], [("storage RMSE 0.2730 m", L), (r"$^{3}$", L)],
                       [("mass residual ", L), (r"$4.37{\times}10^{-13}$", L), (" %", L)]],
            "tags": [("acceptance", "ok", 0)],
        },
        "ex2": {
            "module": ["Full momentum", "", "Local inertial"],
            "case": [[("Ritter dry-bed", B)], [("dam-break", B)], "on a dedicated", "geometry"],
            "reference": [[("Analytical solution", B)], "the Ritter profile"],
            "result": ["NSE 0.9992", "", "NSE 0.9552; its equations", "omit full momentum terms"],
            "tags": [("acceptance", "ok", 0), ("diagnostic", "diag", 2)],
        },
    },
    "pt": {
        "module": "Módulo",
        "module_lines": ["um módulo, com", "o seu processo", "isolado"],
        "case": "Caso de validação",
        "case_lines": ["entradas definidas", "resposta esperada", "métricas", "critérios de aceitação",
                       "resultados"],
        "compare": "Comparar",
        "compare_lines": ["rodar o módulo e", "avaliar a resposta", "contra a referência"],
        "reference": "Referência: um de cinco tipos de evidência",
        "evidence": [
            ("Solução analítica", "uma solução fechada ou exata"),
            ("Referência independente", "um cálculo separado do mesmo processo"),
            ("Balanço exato", "conservação sob forçantes prescritas"),
            ("Hidrograma de referência", "um benchmark publicado ou digitalizado"),
            ("Referência numérica", "uma simulação refinada e documentada"),
        ],
        "accept": "Evidência de aceitação",
        "accept_lines": ["uma referência adequada, e", "os limiares são atingidos;", "conta para o estado de",
                         "validação do módulo"],
        "diag": "Diagnóstico",
        "diag_lines": ["sem referência apropriada:", "o caso continua visível,", "mas não é usado como",
                       "evidência de aceitação"],
        "vtilt": "Bacia sintética em V",
        "vtilt_lines": ["muitos casos hidrológicos e de", "águas subterrâneas: DEM, solo,",
                        "cobertura, IAF, aquífero, contornos"],
        "bench": "Benchmarks hidrodinâmicos dedicados",
        "bench_lines": ["geometrias feitas para essas", "soluções: a ruptura de barragem",
                        "de Ritter e a onda não quebrante"],
        "outlet": "exutório",
        "dam": "barragem",
        "examples": "Dois casos, passo a passo",
        "cols": ["Módulo", "Caso", "Referência", "Resultado", "Conta como"],
        "ex1": {
            "module": ["Reservatórios e", "estruturas de", "controle"],
            "case": [[("VAL-RES-001", B)], "área constante,", "uma curva-chave,", "sem afluência"],
            "reference": [[("Solução analítica", B)], "da depleção", [("Balanço exato", B)], "do volume"],
            "result": [[("passou nos limiares", B)], "RMSE do armazenamento",
                       [("0,2730 m", L), (r"$^{3}$", L)],
                       [("resíduo de massa ", L), (r"$4{,}37{\times}10^{-13}$", L), (" %", L)]],
            "tags": [("aceitação", "ok", 0)],
        },
        "ex2": {
            "module": ["Momento completo", "", "Inercial local"],
            "case": [[("Ruptura de", B)], [("barragem de Ritter", B)], "leito seco, em uma",
                     "geometria dedicada"],
            "reference": [[("Solução analítica", B)], "o perfil de Ritter"],
            "result": ["NSE 0,9992", "", "NSE 0,9552; a formulação", "omite termos de momento"],
            "tags": [("aceitação", "ok", 0), ("diagnóstico", "diag", 2)],
        },
    },
    "es": {
        "module": "Módulo",
        "module_lines": ["un módulo, con", "su proceso", "aislado"],
        "case": "Caso de validación",
        "case_lines": ["entradas definidas", "respuesta esperada", "métricas", "criterios de aceptación",
                       "resultados"],
        "compare": "Comparar",
        "compare_lines": ["ejecutar el módulo", "y evaluar su", "respuesta frente", "a la referencia"],
        "reference": "Referencia: uno de cinco tipos de evidencia",
        "evidence": [
            ("Solución analítica", "una solución cerrada o exacta"),
            ("Referencia independiente", "un cálculo separado del mismo proceso"),
            ("Balance exacto", "conservación bajo forzantes prescritas"),
            ("Hidrograma de referencia", "un benchmark publicado o digitalizado"),
            ("Referencia numérica", "una simulación refinada y documentada"),
        ],
        "accept": "Evidencia de aceptación",
        "accept_lines": ["una referencia adecuada, y", "se cumplen los umbrales;", "cuenta para el estado de",
                         "validación del módulo"],
        "diag": "Diagnóstico",
        "diag_lines": ["sin una referencia apropiada:", "el caso sigue visible,", "pero no se usa como",
                       "evidencia de aceptación"],
        "vtilt": "Cuenca sintética en V",
        "vtilt_lines": ["muchos casos hidrológicos y de", "agua subterránea: DEM, suelo,",
                        "cobertura, IAF, acuífero, contornos"],
        "bench": "Benchmarks hidrodinámicos dedicados",
        "bench_lines": ["geometrías diseñadas para esas", "soluciones: la rotura de presa",
                        "de Ritter y la onda no rompiente"],
        "outlet": "salida",
        "dam": "presa",
        "examples": "Dos casos, paso a paso",
        "cols": ["Módulo", "Caso", "Referencia", "Resultado", "Cuenta como"],
        "ex1": {
            "module": ["Embalses y", "estructuras de", "control"],
            "case": [[("VAL-RES-001", B)], "área constante,", "una curva de gasto,", "sin aporte"],
            "reference": [[("Solución analítica", B)], "del vaciado", [("Balance exacto", B)], "del volumen"],
            "result": [[("superó los umbrales", B)], "RMSE del almacenamiento",
                       [("0,2730 m", L), (r"$^{3}$", L)],
                       [("residuo de masa ", L), (r"$4{,}37{\times}10^{-13}$", L), (" %", L)]],
            "tags": [("aceptación", "ok", 0)],
        },
        "ex2": {
            "module": ["Momento completo", "", "Inercial local"],
            "case": [[("Rotura de presa de", B)], [("Ritter, lecho seco", B)], "en una geometría",
                     "dedicada"],
            "reference": [[("Solución analítica", B)], "el perfil de Ritter"],
            "result": ["NSE 0,9992", "", "NSE 0,9552; sus ecuaciones", "omiten términos de momento"],
            "tags": [("aceptación", "ok", 0), ("diagnóstico", "diag", 2)],
        },
    },
}


def heading(s, x, y, icon, label, *, size=10.5, icon_size=16, room=None, c=INK):
    if icon:
        li.draw(s.ax, icon, x + icon_size / 2, y, icon_size, c, lw=1.1)
        x += icon_size + 6
    fk.text(s, x, y, label, bold=True, size=size, room=room, c=c)
    return x + fk.width(s, label, bold=True, size=size)


def vtilted(s, x0, y0, w=96, h=52, outlet=""):
    """Plan view of the V-tilted catchment, north up: two hillslopes drain to a central
    channel strip, which drains north to the outlet on the upper edge."""
    ch = 8
    xm = x0 + w / 2
    s.ax.add_patch(Rectangle((x0, y0), w / 2 - ch / 2, h, facecolor=color("slot_near_surface"),
                             edgecolor="none", zorder=4))
    s.ax.add_patch(Rectangle((xm + ch / 2, y0), w / 2 - ch / 2, h, facecolor=color("slot_near_surface"),
                             edgecolor="none", zorder=4))
    s.ax.add_patch(Rectangle((xm - ch / 2, y0), ch, h, facecolor=color("slot_wet_odd"), edgecolor="none",
                             zorder=4))
    s.ax.add_patch(Rectangle((x0, y0), w, h, facecolor="none", edgecolor=INK, linewidth=0.8, zorder=6))

    def small_arrow(p0, p1):
        fk.line(s, [p0, p1], c=INK, lw=0.7)
        d = np.subtract(p1, p0)
        d = d / np.linalg.norm(d)
        n = np.array([-d[1], d[0]])
        tip = np.array(p1)
        s.ax.add_patch(Polygon([tip, tip - 4.5 * d + 2.3 * n, tip - 4.5 * d - 2.3 * n], closed=True,
                               facecolor=INK, edgecolor="none", zorder=7))

    # The planes fall toward the channel and, more gently, toward the north edge.
    for yy in (y0 + 13, y0 + 29):
        small_arrow((x0 + 8, yy), (xm - ch / 2 - 5, yy - 4))
        small_arrow((x0 + w - 8, yy), (xm + ch / 2 + 5, yy - 4))
    small_arrow((xm, y0 + 14), (xm, y0 - 10))
    if outlet:
        fk.text(s, xm + 7, y0 - 8, outlet, c=SOFT)


def ritter(s, x0, y0, w=110, h=46, dam_label=""):
    """Dry-bed dam break: the initial step (dashed) and the Ritter profile h(x, t) at one time."""
    g, h0, t = 9.81, 1.0, 1.0
    c0 = np.sqrt(g * h0)
    xs = np.linspace(-1.6 * c0 * t, 2.4 * c0 * t, 200)
    hx = np.where(xs < -c0 * t, h0, np.where(xs <= 2 * c0 * t, (2 * c0 - xs / t) ** 2 / (9 * g), 0.0))
    X = x0 + (xs - xs[0]) / (xs[-1] - xs[0]) * w
    Y = y0 + h - hx / h0 * (h - 12)
    s.ax.fill_between(X, Y, y0 + h, color=color("slot_wet_even"), linewidth=0, zorder=4)
    s.ax.plot(X, Y, color=WATER, linewidth=1.3, zorder=5)
    xd = x0 + (0 - xs[0]) / (xs[-1] - xs[0]) * w
    s.ax.plot([x0, xd, xd], [y0 + 12, y0 + 12, y0 + h], color=INK, linewidth=0.8, linestyle=(0, (3, 2)), zorder=6)
    fk.line(s, [(x0, y0 + h), (x0 + w, y0 + h)], c=INK, lw=1.0)
    if dam_label:
        fk.text(s, xd + 4, y0 + 4, dam_label, c=SOFT)


def tag(s, x, y, label, kind):
    w = fk.width(s, label) + 14
    p = s.box(x, y - 9, w, 18, fill=ACCEPT_FILL if kind == "ok" else "#ffffff",
              edge=ACCEPT_EDGE if kind == "ok" else SOFT, radius=9, lw=0.9, z=4)
    if kind != "ok":
        p.set_linestyle((0, (3, 2)))
    s.text(x + 7, y, label, z=5)


def main(preview: Path | None = None) -> None:
    for lang in LABELS:
        draw(lang, preview)
    li.write_licence_log(HERE / "validation_logic_icons.csv")


def draw(lang: str, preview: Path | None = None) -> None:
    t = LABELS[lang]
    s = Sheet(W, H, NAME)

    # ---- logic: module -> case -> compare -> outcomes; reference feeds the comparison ----
    # A narrow Module panel and wide Case and Acceptance panels, so the
    # Portuguese and Spanish headings fit.
    A, Bc, C, D = (20, 144), (164, 336), (356, 500), (536, 740)
    HS = 10                                          # heading size of the logic panels
    TOP, BOT = 16, 130
    MID = 66
    fk.panel(s, A[0], TOP, A[1] - A[0], BOT - TOP)
    heading(s, A[0] + 12, TOP + 18, "box", t["module"], size=HS, room=A[1] - A[0] - 40)
    fk.lines(s, A[0] + 12, TOP + 40, t["module_lines"], pitch=16, room=A[1] - A[0] - 20)
    fk.panel(s, Bc[0], TOP, Bc[1] - Bc[0], BOT - TOP, fill=color("deep_fill"), edge=WATER)
    heading(s, Bc[0] + 12, TOP + 18, "clipboard-list", t["case"], size=HS, room=Bc[1] - Bc[0] - 40)
    fk.lines(s, Bc[0] + 12, TOP + 40, t["case_lines"], pitch=16, room=Bc[1] - Bc[0] - 20)
    fk.panel(s, C[0], TOP, C[1] - C[0], BOT - TOP)
    heading(s, C[0] + 12, TOP + 18, "scale", t["compare"], size=HS, room=C[1] - C[0] - 40)
    fk.lines(s, C[0] + 12, TOP + 40, t["compare_lines"], pitch=16, room=C[1] - C[0] - 20)
    fk.arrow(s, (A[1], MID), (Bc[0], MID))
    fk.arrow(s, (Bc[1], MID), (C[0], MID))

    RT, RB = 154, 270
    fk.panel(s, A[0], RT, C[1] - A[0], RB - RT)
    heading(s, A[0] + 12, RT + 18, "book-open-check", t["reference"], size=HS, room=C[1] - A[0] - 40)
    for k, (name, use) in enumerate(t["evidence"]):
        y = RT + 40 + 16 * k
        fk.text(s, A[0] + 34, y, name, bold=True, room=212 - 34 - 8)
        fk.text(s, A[0] + 212, y, use, room=C[1] - A[0] - 212 - 10)
    cx = (C[0] + C[1]) / 2
    fk.arrow(s, (cx, RT), (cx, BOT))

    # Outcomes: the arrow to acceptance, a branch at a junction dot down to the diagnostic.
    bus_x = 518
    fk.arrow(s, (C[1], MID), (D[0], MID))
    fk.dot(s, bus_x, MID)
    yd = (RT + RB) / 2
    fk.route(s, [(bus_x, MID), (bus_x, yd), (D[0], yd)])
    fk.panel(s, D[0], TOP, D[1] - D[0], BOT - TOP, fill=ACCEPT_FILL, edge=ACCEPT_EDGE)
    heading(s, D[0] + 12, TOP + 18, "circle-check-big", t["accept"], size=HS, room=D[1] - D[0] - 40)
    fk.lines(s, D[0] + 12, TOP + 40, t["accept_lines"], pitch=16, room=D[1] - D[0] - 20)
    diag = fk.panel(s, D[0], RT, D[1] - D[0], RB - RT, fill="#ffffff", edge=SOFT)
    diag.set_linestyle((0, (4, 3)))
    heading(s, D[0] + 12, RT + 18, "circle-alert", t["diag"], size=HS, room=D[1] - D[0] - 40)
    fk.lines(s, D[0] + 12, RT + 40, t["diag_lines"], pitch=16, room=D[1] - D[0] - 20)

    # ---- where the cases run ------------------------------------------------------------
    # Tall enough for the outlet arrow, which leaves the thumbnail through its north edge,
    # below the heading.
    WT, WB = 290, 400
    fk.panel(s, 20, WT, 352, WB - WT, fill=color("slot_rock_even"))
    fk.panel(s, 388, WT, 352, WB - WT, fill=color("slot_rock_even"))
    heading(s, 32, WT + 18, None, t["vtilt"], room=372 - 32 - 10)
    vtilted(s, 32, WT + 48, w=92, h=36, outlet=t["outlet"])
    fk.lines(s, 142, WT + 50, t["vtilt_lines"], pitch=16, room=372 - 142 - 10)
    heading(s, 400, WT + 18, None, t["bench"], room=740 - 400 - 10)
    ritter(s, 400, WT + 40, w=110, h=46, dam_label=t["dam"])
    fk.lines(s, 528, WT + 50, t["bench_lines"], pitch=16, room=740 - 528 - 10)

    # ---- two cases traced through -------------------------------------------------------
    ET = 418
    heading(s, 20, ET + 8, None, t["examples"])
    # Module and Result columns wide enough for the Portuguese and Spanish rows.
    XC = [20, 156, 296, 436, 642, 740]
    for k, name in enumerate(t["cols"]):
        fk.text(s, XC[k] + (8 if k == 4 else 12), ET + 30, name, c=SOFT)
    rows = [(ET + 42, ET + 120, t["ex1"]), (ET + 128, ET + 206, t["ex2"])]
    for r0, r1, ex in rows:
        fk.panel(s, 20, r0, 720, r1 - r0)
        y0 = r0 + 15
        for k, key in enumerate(("module", "case", "reference", "result")):
            yy = y0
            for row in ex[key]:
                if row:
                    fk.lines(s, XC[k] + 12, yy, [row], room=XC[k + 1] - XC[k] - 14)
                yy += 16
        for label, kind, line_index in ex["tags"]:
            tag(s, XC[4] + 8, y0 + 16 * line_index, label, kind)
    # Row 2: a thin divider between the two solvers, outside the shared Case and Reference cells.
    r0, r1, _ = rows[1]
    ymid = r0 + 15 + 16
    for xa, xb in ((XC[0] + 12, XC[1] - 8), (XC[3] + 12, XC[5] - 12)):
        fk.line(s, [(xa, ymid), (xb, ymid)], c=color("card_edge"), lw=0.8)

    svg = s.save(STATIC / "validation", lang, preview)
    print("wrote", svg.name)


if __name__ == "__main__":
    main(Path(sys.argv[1]) if len(sys.argv) > 1 else None)


# Sources in the docs, one per element of the figure.
FACTS = {
    "module tested against a known reference; case defines inputs, expected response, metrics, thresholds, outputs":
        "validation/overview.md",
    "process isolated": "validation/ancillary-modules.md",
    "five evidence types and their use": "validation/overview.md, Evidence",
    "diagnostic: no appropriate reference, stays visible, not acceptance evidence": "validation/overview.md, Evidence",
    "module status index": "validation/validation-status.md",
    "shared V-tilted catchment; dedicated hydrodynamic benchmarks": "validation/overview.md, Shared V-tilted catchment",
    "V-tilted outlet on the north edge (row 0, the two channel cells)":
        "the canonical V-tilted DEM (lowest row is the north row) and its benchmark set-up",
    "VAL-RES-001 set-up, reference, metrics, passed":
        "validation/ancillary-modules.md, Reservoir rating-curve depletion; validation/validation-status.md",
    "Ritter: full momentum NSE 0.9992, acceptance":
        "validation/hydrodynamics-routing.md; validation/validation-status.md",
    "Ritter: local inertial NSE 0.9552, method-limited diagnostic": "validation/hydrodynamics-routing.md",
}
