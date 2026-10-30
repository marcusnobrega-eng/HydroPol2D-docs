"""Five ways to route surface water, for docs/theory/hydrodynamic-model.md (introduction).

A matrix: rows are the five routing families, columns are the terms of the
shallow-water momentum equation (x direction), with kept and dropped marks. Each row
says how flow moves between cells, the equation the docs give for it, and, where the
docs say so, when to use it.

Facts:
  docs/theory/hydrodynamic-model.md: introduction, sections 1.1 and 1.2 (local
    inertial, the default), 2.1 to 2.3 (full momentum, HLL fluxes), 3.2 and 3.3
    (diffusive D4 on the water-surface slope, kinematic D4 on the bed slope with the
    donor cell's depth and roughness), 4.1 to 4.7 and 4.11 (cellular automata)
  docs/configuration/flags.md and overview.md: one of flag_inertial,
    flag_full_momentum, flag_diffusive, flag_kinematic or flag_CA per run
The Python and MATLAB kernels were read on 2026-10-29 and agree with these equations.

Run from the repository root:

    python3 figures/routing_families.py [preview-folder]

Output: static/img/theory/routing-families.svg (en), routing-families.pt.svg and
routing-families.es.svg, and a PNG of each in the preview folder, if given.
"""

from __future__ import annotations

import sys
from pathlib import Path

from matplotlib.backends.backend_agg import FigureCanvasAgg
from matplotlib.patches import Circle, FancyBboxPatch

sys.path.insert(0, str(Path(__file__).resolve().parent))
from site_style import SOFT, STATIC, WATER, Sheet, color  # noqa: E402
import flow_kit as fk  # noqa: E402

# Math is the same in every language; only the words change.
TERMS = [r"$\dfrac{\partial (hu)}{\partial t}$",
         r"$\dfrac{\partial (hu^2)}{\partial x}$",
         r"$g\,h\,\dfrac{\partial h}{\partial x}$",
         r"$-\,g\,h\,\dfrac{\partial z}{\partial x}$",
         r"$-\,g\,n^2\,\dfrac{u\,|u|}{h^{1/3}}$"]
OPERATORS = ["+", "+", "=", ""]
# Per row: kept terms (None: no momentum equation), the equation, the default flag.
ROWS = [
    {"status": "default", "kept": [1, 0, 1, 1, 1],
     "eq": r"$\dfrac{\partial q}{\partial t} = -\,g\,H_{\mathrm{f}}\,S"
           r" - g\,n^2\,\dfrac{q\,|q|}{H_{\mathrm{f}}^{7/3}}$"},
    {"status": "optional", "kept": [1, 1, 1, 1, 1],
     "eq": r"$\dfrac{\partial \mathbf{U}}{\partial t} + \dfrac{\partial \mathbf{F}}{\partial x}"
           r" + \dfrac{\partial \mathbf{G}}{\partial y} = \mathbf{S}_{\mathrm{bed}}"
           r" + \mathbf{S}_{\mathrm{fric}}$,   $\mathbf{U} = (h,\ hu,\ hv)$"},
    {"status": "optional", "kept": [0, 0, 1, 1, 1],
     "eq": r"$q_f = \mathrm{sign}(S_f)\,\dfrac{H_f^{5/3}}{n}\,\sqrt{|S_f|}$"},
    {"status": "optional", "kept": [0, 0, 0, 1, 1],
     "eq": r"$q_f = \mathrm{sign}(S_b)\,\dfrac{H_{\mathrm{donor}}^{5/3}}{n_{\mathrm{donor}}}"
           r"\,\sqrt{|S_b|}$"},
    {"status": "optional", "kept": None,
     "eq": r"$I_{\mathrm{tot}} = u\,h\,\Delta t\,W_{\mathrm{eff}}$,   "
           r"$u = \dfrac{1}{n}\,h^{2/3}\,S^{1/2}$"},
]

LABELS = {
    "en": {
        "methods_head": "Routing family",
        "terms_head": r"Shallow-water momentum equation, $x$ direction",
        "term_names": [["local", "acceleration"], ["convective", "acceleration"],
                       ["pressure", "gradient"], ["bed", "slope"], ["friction", "(Manning)"]],
        "together": r"together: water-surface slope, $\eta = z + h$",
        "default": "default",
        "optional": "optional",
        "use_when": "Use when:",
        "rows": [
            {"name": "Local inertial",
             "how": ["discharge on each face from its last value,",
                     "the water-surface slope and friction"],
             "use": "most applications"},
            {"name": "Full momentum",
             "how": [r"HLL fluxes of $h$, $hu$, $hv$ across each face;",
                     "momentum carried from step to step"],
             "use": "waves and convection matter"},
            {"name": "Diffusive D4",
             "how": ["Manning flux on each face, driven by the",
                     "water-surface slope; backwater-like flow"],
             "use": None},
            {"name": "Kinematic D4",
             "how": ["Manning flux on each face, driven by the",
                     "bed slope and donor depth; no backwater"],
             "use": None},
            {"name": "Cellular automata",
             "how": ["each cell shares its outflow among lower",
                     "neighbors, weighted by the surface drop"],
             "use": "speed matters more than detail",
             "no_momentum": "no momentum equation: transfer rules instead"},
        ],
        "one_per_run": "one per run",
        "kept": "kept",
        "dropped": "dropped",
        "footer": ["Set one of flag_inertial, flag_full_momentum, flag_diffusive,",
                   "flag_kinematic or flag_CA to 1 in a run."],
    },
    "pt": {
        "methods_head": "Família de roteamento",
        "terms_head": r"Equação do momento em águas rasas, direção $x$",
        "term_names": [["aceleração", "local"], ["aceleração", "convectiva"],
                       ["gradiente de", "pressão"], ["inclinação", "do leito"],
                       ["atrito", "(Manning)"]],
        "together": r"juntos: inclinação da superfície da água, $\eta = z + h$",
        "default": "padrão",
        "optional": "opcional",
        "use_when": "Use quando:",
        "rows": [
            {"name": "Inercial local",
             "how": ["descarga em cada face pelo último valor,",
                     "pela inclinação da superfície e pelo atrito"],
             "use": "na maioria das aplicações"},
            {"name": "Momento completo",
             "how": [r"fluxos HLL de $h$, $hu$, $hv$ em cada face;",
                     "o momento passa de um passo ao seguinte"],
             "use": "ondas e convecção importam"},
            {"name": "Difusivo D4",
             "how": ["fluxo de Manning em cada face, dado pela",
                     "inclinação da superfície da água;",
                     "representa o remanso"],
             "use": None},
            {"name": "Cinemático D4",
             "how": ["fluxo de Manning em cada face, dado pela",
                     "inclinação do leito e pela profundidade da",
                     "célula doadora; sem remanso"],
             "use": None},
            {"name": "Autômatos celulares",
             "how": ["cada célula reparte a sua saída entre as",
                     "vizinhas mais baixas, conforme o desnível"],
             "use": "a rapidez é a prioridade",
             "no_momentum": "sem equação do momento: regras de transferência"},
        ],
        "one_per_run": "uma por execução",
        "kept": "mantido",
        "dropped": "desprezado",
        "footer": ["Defina um de flag_inertial, flag_full_momentum, flag_diffusive,",
                   "flag_kinematic ou flag_CA como 1 em cada execução."],
    },
    "es": {
        "methods_head": "Familia de enrutamiento",
        "terms_head": r"Ecuación de momento en aguas poco profundas, dirección $x$",
        "term_names": [["aceleración", "local"], ["aceleración", "convectiva"],
                       ["gradiente de", "presión"], ["pendiente", "del lecho"],
                       ["fricción", "(Manning)"]],
        "together": r"juntos: pendiente de la superficie del agua, $\eta = z + h$",
        "default": "predeterminado",
        "optional": "opcional",
        "use_when": "Úselo si:",
        "rows": [
            {"name": "Inercial local",
             "how": ["descarga por cara desde su valor previo,",
                     "la pendiente de la superficie y la fricción"],
             "use": "en la mayoría de los casos"},
            {"name": "Momento completo",
             "how": [r"flujos HLL de $h$, $hu$, $hv$ en cada cara;",
                     "el momento pasa de un paso al siguiente"],
             "use": "pesan las ondas y la convección"},
            {"name": "Difusivo D4",
             "how": ["flujo de Manning en cada cara, según la",
                     "pendiente de la superficie del agua;",
                     "representa el remanso"],
             "use": None},
            {"name": "Cinemático D4",
             "how": ["flujo de Manning en cada cara, según la",
                     "pendiente del lecho y la profundidad de la",
                     "celda donante; sin remanso"],
             "use": None},
            {"name": "Autómatas celulares",
             "how": ["cada celda reparte su salida entre las",
                     "vecinas más bajas, según el desnivel"],
             "use": "la rapidez es la prioridad",
             "no_momentum": "sin ecuación de momento: reglas de transferencia"},
        ],
        "one_per_run": "una por ejecución",
        "kept": "conservado",
        "dropped": "despreciado",
        "footer": ["Ponga en 1 uno de flag_inertial, flag_full_momentum,",
                   "flag_diffusive, flag_kinematic o flag_CA en cada ejecución."],
    },
}

W, H = 760, 608
MX0, MX1 = 40, 300                       # method column
COL_W = [78, 90, 84, 84, 92]             # term columns
TX0 = 312
COL_X = [TX0 + sum(COL_W[:k]) for k in range(len(COL_W) + 1)]
TX1 = COL_X[-1]
COL_C = [(a + b) / 2 for a, b in zip(COL_X[:-1], COL_X[1:])]
ROW_TOP, ROW_H = 158, 80
MARK_R = 6.0


class Checker:
    """Warn when a label runs past the room it was given."""

    def __init__(self, sheet: Sheet) -> None:
        self.canvas = FigureCanvasAgg(sheet.fig)
        self.problems: list[str] = []

    def extent(self, artist):
        return artist.get_window_extent(self.canvas.get_renderer())

    def room(self, artist, x_min: float, x_max: float, name: str) -> None:
        box = self.extent(artist)
        if box.x1 > x_max + 0.5 or box.x0 < x_min - 0.5:
            self.problems.append(f"{name}: spans {box.x0:.0f}-{box.x1:.0f}, room {x_min:.0f}-{x_max:.0f}")

    def right(self, artist) -> float:
        return self.extent(artist).x1


def pill(s: Sheet, chk: Checker, x: float, y: float, label: str, *, filled: bool):
    """Status tag: filled water pill for the default, outlined for optional."""
    probe = s.text(x + 7, y, label, bold=filled, size=9, c="#ffffff" if filled else SOFT, z=8)
    width = chk.right(probe) - x + 7
    s.ax.add_patch(FancyBboxPatch((x, y - 7.5), width, 15, boxstyle="round,pad=0,rounding_size=7.5",
                                  facecolor=WATER if filled else "#ffffff",
                                  edgecolor=WATER if filled else color("guide"),
                                  linewidth=0.9, zorder=7))
    return x + width


def mark(s: Sheet, x: float, y: float, kept: bool) -> None:
    if kept:
        s.ax.add_patch(Circle((x, y), MARK_R, facecolor=WATER, edgecolor="none", zorder=6))
    else:
        s.ax.add_patch(Circle((x, y), MARK_R - 0.6, facecolor="#ffffff", edgecolor=color("guide"),
                              linewidth=1.2, zorder=6))


def draw(lang: str, preview: Path | None = None) -> Path:
    t = LABELS[lang]
    s = Sheet(W, H, "routing-families")
    chk = Checker(s)

    # --- header: the equation, one term per column ----------------------------------
    s.text(MX0, 28, t["methods_head"], bold=True, size=10.5)
    chk.room(s.text(TX0, 28, t["terms_head"], bold=True, size=10.5), TX0, TX1, "terms head")
    y_eq = 66
    for k, (cx, term) in enumerate(zip(COL_C, TERMS)):
        chk.room(s.text(cx, y_eq, term, size=11.5, ha="center"), COL_X[k] + 2, COL_X[k + 1] - 2,
                 f"term {k + 1}")
    for xb, op in zip(COL_X[1:-1], OPERATORS):
        if op:
            s.text(xb, y_eq, f"${op}$", size=11.5, ha="center")
    for k, (cx, lines) in enumerate(zip(COL_C, t["term_names"])):
        for i, line in enumerate(lines):
            chk.room(s.text(cx, 100 + 14 * i, line, size=9.5, ha="center"), COL_X[k] + 2,
                     COL_X[k + 1] - 2, f"term name {k + 1}")
    # Pressure gradient and bed slope together make the water-surface slope.
    xa, xb = COL_C[2] - 30, COL_C[3] + 30
    yb = 128
    s.line([xa, xa, xb, xb], [yb - 4, yb, yb, yb - 4], c=SOFT, lw=0.9)
    chk.room(s.text((xa + xb) / 2, yb + 12, t["together"], size=9, c=SOFT, ha="center"),
             TX0, TX1, "together")
    s.line([MX0 - 16, TX1], [ROW_TOP - 6, ROW_TOP - 6], c=color("guide"), lw=0.9)

    # --- rows ---------------------------------------------------------------------
    for r, (row, fixed) in enumerate(zip(t["rows"], ROWS)):
        y0 = ROW_TOP + r * ROW_H
        if r:
            s.line([MX0 - 16, TX1], [y0 - 6, y0 - 6], c=color("card_edge"), lw=0.8)
        name = s.text(MX0, y0 + 14, row["name"], bold=True, size=10.5)
        end = pill(s, chk, chk.right(name) + 8, y0 + 14, t[fixed["status"]],
                   filled=fixed["status"] == "default")
        if end > MX1:
            chk.problems.append(f"{row['name']} pill ends at {end:.0f}, room to {MX1}")
        for i, line in enumerate(row["how"]):
            chk.room(s.text(MX0, y0 + 33 + 15 * i, line), MX0, MX1, f"{row['name']} how {i + 1}")
        if row["use"]:
            y_use = y0 + 34 + 15 * len(row["how"])
            if y_use > y0 + 64:
                chk.problems.append(f"{row['name']}: 'use when' line below the row")
            # One baseline for the bold lead and the text, so an accented capital
            # (Úselo) does not lower the lead.
            used = fk.rich(s, MX0, y_use, [(t["use_when"], True), (" " + row["use"], False)])
            if MX0 + used > MX1 + 0.5:
                chk.problems.append(f"{row['name']} use: ends at {MX0 + used:.0f}, room to {MX1}")
        if fixed["kept"] is not None:
            for cx, kept in zip(COL_C, fixed["kept"]):
                mark(s, cx, y0 + 14, bool(kept))
        else:
            band = FancyBboxPatch((TX0 + 8, y0 + 5), TX1 - TX0 - 16, 18,
                                  boxstyle="round,pad=0,rounding_size=9", facecolor=color("slot_rock_even"),
                                  edgecolor="none", zorder=4)
            s.ax.add_patch(band)
            chk.room(s.text((TX0 + TX1) / 2, y0 + 14, row["no_momentum"], size=9.5, c=SOFT, ha="center"),
                     TX0 + 8, TX1 - 8, "no momentum")
        chk.room(s.text((TX0 + TX1) / 2, y0 + 48, fixed["eq"], size=10.5, ha="center"), TX0, TX1,
                 f"{row['name']} eq")

    # "One per run": a bracket over the five rows.
    n_rows = len(ROWS)
    y_a, y_b = ROW_TOP + 4, ROW_TOP + n_rows * ROW_H - 14
    s.line([30, 24, 24, 30], [y_a, y_a, y_b, y_b], c=SOFT, lw=1.0)
    s.text(14, (y_a + y_b) / 2, t["one_per_run"], size=9.5, c=SOFT, rotation=90, ha="center")

    # --- footer: key and the rule ---------------------------------------------------
    y_f = ROW_TOP + n_rows * ROW_H + 8
    s.line([MX0 - 16, TX1], [y_f - 6, y_f - 6], c=color("guide"), lw=0.9)
    mark(s, MX0 + 6, y_f + 12, True)
    kept = s.text(MX0 + 18, y_f + 12, t["kept"])
    mark(s, chk.right(kept) + 20, y_f + 12, False)
    dropped = s.text(chk.right(kept) + 32, y_f + 12, t["dropped"])
    if chk.right(dropped) > TX0 - 12:
        chk.problems.append("key runs into the footer")
    for i, line in enumerate(t["footer"]):
        chk.room(s.text(TX0, y_f + 12 + 15 * i, line, size=9.5), TX0, TX1, "footer")

    for problem in chk.problems:
        print(f"{lang} ROOM:", problem)
    svg = s.save(STATIC / "theory", lang, preview)
    print(lang, "->", svg, f"(rows end at {ROW_TOP + n_rows * ROW_H}, footer to {y_f + 27}, H = {H})")
    return svg


def main(preview: Path | None = None) -> None:
    for lang in LABELS:
        draw(lang, preview)


if __name__ == "__main__":
    main(Path(sys.argv[1]) if len(sys.argv) > 1 else None)
