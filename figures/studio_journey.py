"""Studio from first start to results, for docs/studio/overview.md.

The license window, Home, the New model wizard, the four workspaces (Setup, Run, Results
and Calibrate) and how edits, Save and Revert to saved work, as in Studio 0.9.0rc2.

Studio's interface is English only, so button, page, step and status names stay in English
in every language, as on the Studio pages, and are set in bold ((text, True) runs); buttons
are drawn as outlined chips. Only the descriptions are translated.

Run from the repository root:

    python3 figures/studio_journey.py [preview-folder]

Output: static/img/studio/studio-journey.svg (en), studio-journey.pt.svg and
studio-journey.es.svg, a PNG of each in the preview folder, if given, and the icon licence
log figures/studio_journey_icons.csv.
"""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import flow_kit as fk  # noqa: E402
import lucide_draw as li  # noqa: E402
from site_style import HERE, INK, SOFT, STATIC, WATER, Sheet, color  # noqa: E402

W = 760
NAME = "studio-journey"
B = True  # bold run
L = False  # light run

# Studio's own labels, the same in every language.
UI = {
    "activate": "Activate",
    "home": "Home",
    "new_model": "New model",
    "open_existing": "Open existing model",
    "open_results": "Open simulation results",
    "wizard_steps": ["Model area", "Catchment", "Simulation period", "Terrain and grid", "Rain",
                     "Weather", "Land and soil", "Processes", "Review and build"],
    "build_model": "Build model",
    "open_model": "Open model",
    "setup": "Setup",
    "setup_steps": ["Model", "Study area", "Computational mesh", "Processes", "Parameters",
                    "Forcing", "Review"],
    "continue_setup": "Continue setup",
    "run": "Run",
    "check_inputs": "Check inputs",
    "run_model": "Run model",
    "results": "Results",
    "calibrate": "Calibrate",
    "start_calibration": "Start calibration",
    "apply": "Apply to model",
    "undo": "Undo apply",
    "keys": ["Cmd+1", "Cmd+2", "Cmd+3", "Cmd+4"],
    "save": "Save",
    "save_key": "Cmd+S",
    "revert": "Revert to saved",
}

LABELS = {
    "en": {
        "first": "First start",
        "first_l1": "Marcus sends the installer for a Mac (Apple silicon) or Windows, and your license code",
        "first_l2a": "The license window asks for it: paste the whole code, click",
        "first_l2b": [(", and Studio opens on ", L), ("Home", B)],
        "existing_note": "case.yaml or a legacy workbook",
        "results_note": "a results package",
        "wizard": "New model wizard",
        "catchment_note": "outlet choices only",
        "build_note": ["downloads the data and", "builds the model"],
        "status_lines": [[("status: ", L), ("Complete", B), (",", L)],
                         [("Not started", B), (" or", L)], [("Needs check", B)]],
        "continue_note": ["opens the next", "recommended step"],
        "run_rows": [
            [("Outputs", B)], ["intervals, animations"],
            [("Computing backend", B)], ["the CPU in the apps"],
            [("Save results to", B)], ["the folder for this run"],
        ],
        "run_after": ["checks the inputs first"],
        "live": [[("Live diagnostics", B)], ["charts and the run log"]],
        "results_rows": [
            "playback, loop, frame", "steps, jump to a time",
            "", "maximum, minimum", "and final maps",
            "", "right-click a cell: time", "series, cell data, profile",
            "", "maps: PNG, PDF, SVG,", "GeoTIFF or MP4", "charts: also CSV",
            "", "its own layer panel: the", [("Study area", B), (" map stays", L)], "as it is",
        ],
        "cal_obs": [[("Observed data", B)], "discharge, water depths,", "water levels and",
                    "groundwater depths"],
        "cal_search": [[("Search settings", B)], [("Genetic algorithm", B), (" or ", L), ("SCE-UA", B)],
                       [("over the parameters ticked ", L), ("Free", B)]],
        "cal_start_note": "in the background",
        "cal_apply_note": "writes the best values into the open model",
        "edits": "Edits, Save and Revert to saved",
        "open_box": "The open model",
        "open_box_lines": ["edits apply as you make them"],
        "file_box": ["Model file"],
        "file_box_lines": ["case.yaml"],
        "edit_notes": [
            [("Unsaved changes", B), (" shows in the header", L)],
            [("until you ", L), ("Save", B), (". ", L), ("Save", B), (", ", L), ("Check inputs", B), (" and", L)],
            [("Run", B), (" first take every edit not yet applied", L)],
            [("Revert to saved", B), (" asks first, then drops", L)],
            "every change since the last save",
        ],
    },
    "pt": {
        "first": "Primeiro uso",
        "first_l1": "Marcus envia o instalador para Mac (Apple silicon) ou Windows e o seu código de licença",
        "first_l2a": "A janela de licença pede o código: cole o código inteiro, clique em",
        "first_l2b": [(" e o Studio abre na tela ", L), ("Home", B)],
        "existing_note": "case.yaml ou uma planilha do formato antigo",
        "results_note": "um pacote de resultados",
        "wizard": "Assistente",
        "catchment_note": "apenas com exutório",
        "build_note": ["baixa os dados e", "monta o modelo"],
        "status_lines": [[("estado: ", L), ("Complete", B), (",", L)],
                         [("Not started", B), (" ou", L)], [("Needs check", B)]],
        "continue_note": ["abre a próxima", "etapa recomendada"],
        "run_rows": [
            [("Outputs", B)], ["intervalos, animações"],
            [("Computing backend", B)], ["a CPU nos apps"],
            [("Save results to", B)], ["a pasta de saída"],
        ],
        "run_after": ["verifica entradas antes"],
        "live": [[("Live diagnostics", B)], ["gráficos e o log da", "simulação"]],
        "results_rows": [
            "reprodução, loop,", "passo a passo, ir a", "um tempo",
            "", "mapas de máximo, de", "mínimo e final",
            "", "clique direito na célula:", "série, dados, perfil",
            "", "mapas: PNG, PDF,", "SVG, GeoTIFF ou MP4", "gráficos: também CSV",
            "", "painel de camadas", "próprio: o mapa", [("Study area", B), (" não muda", L)],
        ],
        "cal_obs": [[("Observed data", B)], "vazão, profundidade da água,", "nível d'água e profundidade",
                    "do lençol freático"],
        "cal_search": [[("Search settings", B)], [("Genetic algorithm", B), (" ou ", L), ("SCE-UA", B)],
                       [("nos parâmetros marcados ", L), ("Free", B)]],
        "cal_start_note": "em segundo plano",
        "cal_apply_note": "grava os melhores valores no modelo aberto",
        "edits": "Edições, Save e Revert to saved",
        "open_box": "O modelo aberto",
        "open_box_lines": ["as edições valem na hora"],
        "file_box": ["Arquivo do", "modelo"],
        "file_box_lines": ["case.yaml"],
        "edit_notes": [
            [("Unsaved changes", B), (" aparece no cabeçalho", L)],
            [("até o ", L), ("Save", B), (". ", L), ("Save", B), (", ", L), ("Check inputs", B), (" e", L)],
            [("Run", B), (" aplicam antes as edições pendentes", L)],
            [("Revert to saved", B), (" pede confirmação e", L)],
            "descarta tudo desde o último salvamento",
        ],
    },
    "es": {
        "first": "Primer uso",
        "first_l1": "Marcus le envía el instalador para Mac (Apple silicon) o Windows y su código de licencia",
        "first_l2a": "La ventana de licencia pide el código: péguelo completo, haga clic en",
        "first_l2b": [(" y Studio se abre en ", L), ("Home", B)],
        "existing_note": "case.yaml o un libro del formato antiguo",
        "results_note": "un paquete de resultados",
        "wizard": "Asistente",
        "catchment_note": "solo con salida",
        "build_note": ["descarga los datos y", "construye el modelo"],
        "status_lines": [[("estado: ", L), ("Complete", B), (",", L)],
                         [("Not started", B), (" o", L)], [("Needs check", B)]],
        "continue_note": ["abre el siguiente", "paso recomendado"],
        "run_rows": [
            [("Outputs", B)], ["intervalos, animaciones"],
            [("Computing backend", B)], ["la CPU en las apps"],
            [("Save results to", B)], ["la carpeta de salida"],
        ],
        "run_after": ["verifica las entradas"],
        "live": [[("Live diagnostics", B)], ["gráficos y el registro", "de la simulación"]],
        "results_rows": [
            "reproducción, bucle,", "paso a paso, ir a", "un tiempo",
            "", "mapas de máximo, de", "mínimo y final",
            "", "clic derecho en una", "celda: serie, datos", "y perfil",
            "", "mapas: PNG, PDF,", "SVG, GeoTIFF o MP4", "gráficos: también CSV",
            "", "panel de capas propio:", [("el mapa ", L), ("Study area", B)], "no cambia",
        ],
        "cal_obs": [[("Observed data", B)], "caudal, profundidad del agua,", "nivel del agua y profundidad",
                    "del agua subterránea"],
        "cal_search": [[("Search settings", B)], [("Genetic algorithm", B), (" o ", L), ("SCE-UA", B)],
                       [("en los parámetros marcados ", L), ("Free", B)]],
        "cal_start_note": "en segundo plano",
        "cal_apply_note": "pone los mejores valores en el modelo abierto",
        "edits": "Ediciones, Save y Revert to saved",
        "open_box": "El modelo abierto",
        "open_box_lines": ["las ediciones valen al instante"],
        "file_box": ["Archivo del", "modelo"],
        "file_box_lines": ["case.yaml"],
        "edit_notes": [
            [("Unsaved changes", B), (" sale en el encabezado", L)],
            [("hasta el ", L), ("Save", B), (". ", L), ("Save", B), (", ", L), ("Check inputs", B), (" y", L)],
            [("Run", B), (" toman antes las ediciones pendientes", L)],
            [("Revert to saved", B), (" pide confirmación y", L)],
            "descarta todo desde el último guardado",
        ],
    },
}


def heading(s, x, y, icon, label, *, size=10.5, icon_size=16, room=None):
    li.draw(s.ax, icon, x + icon_size / 2, y, icon_size, INK, lw=1.1)
    fk.text(s, x + icon_size + 6, y, label, bold=True, size=size, room=room)
    return x + icon_size + 6 + fk.width(s, label, bold=True, size=size)


def steps(s, x, y, names, *, pitch=17, notes=None, room=140):
    """Numbered step list: soft number, bold step name. notes = {index: soft line under it}."""
    notes = notes or {}
    yy = y
    for k, name in enumerate(names):
        fk.text(s, x, yy, f"{k + 1}", c=SOFT)
        fk.text(s, x + 14, yy, name, bold=True, room=room - 14)
        yy += pitch
        if k in notes:
            fk.text(s, x + 14, yy - 2, notes[k], c=SOFT, room=room - 14)
            yy += pitch - 2
    return yy


def main(preview: Path | None = None) -> None:
    for lang in LABELS:
        draw(lang, preview)
    li.write_licence_log(HERE / "studio_journey_icons.csv")


def draw(lang: str, preview: Path | None = None) -> None:
    t = {**UI, **LABELS[lang]}

    # Columns of the second row: wizard, Setup, Run, Results. Calibrate, the fourth
    # workspace, is the full-width row under them, and the edits strip is last.
    COLS = [(20, 186), (206, 376), (396, 558), (578, 740)]
    ROW_TOP, ROW_BOT = 192, 488
    CY0, CY1 = 504, 614
    EY0, EY1 = 630, 732
    H = EY1 + 16
    s = Sheet(W, H, NAME)

    # ---- first start (license) ---------------------------------------------------------
    fk.panel(s, 20, 16, 720, 48)
    xh = heading(s, 34, 31, "key-round", t["first"])
    fk.text(s, xh + 12, 31, t["first_l1"], room=726 - xh - 12)
    w = fk.width(s, t["first_l2a"])
    fk.text(s, 56, 49, t["first_l2a"])
    x0, x1 = fk.chip(s, 56 + w + 6, 49, t["activate"])
    end = x1 + 1 + fk.rich(s, x1 + 1, 49, t["first_l2b"])
    if end > 726:
        print(f"WARNING [{lang}]: license line ends at {end:.0f}")

    # ---- Home ------------------------------------------------------------------------------
    HX0, HX1, HY0, HY1 = 200, 560, 86, 168
    fk.arrow(s, (380, 64), (380, HY0))
    fk.panel(s, HX0, HY0, HX1 - HX0, HY1 - HY0)
    ROW1, ROW2 = HY0 + 44, HY0 + 68
    heading(s, HX0 + 14, HY0 + 18, "house", t["home"])
    nm0, nm1 = fk.chip(s, HX0 + 14, ROW1, t["new_model"])
    ex0, ex1 = fk.chip(s, HX0 + 14, ROW2, t["open_existing"])
    rs0, rs1 = fk.chip(s, ex1 + 8, ROW2, t["open_results"])

    # New model -> wizard (left, then down).
    wiz_c = (COLS[0][0] + COLS[0][1]) / 2
    fk.route(s, [(HX0, ROW1), (wiz_c, ROW1), (wiz_c, ROW_TOP)])
    fk.line(s, [(nm0, ROW1), (HX0, ROW1)])
    # Open existing model -> Setup (down).
    ex_c = (ex0 + ex1) / 2
    res_c = (COLS[3][0] + COLS[3][1]) / 2 + 20
    fk.arrow(s, (ex_c, ROW2 + 9.5), (ex_c, ROW_TOP))
    fk.text(s, ex_c + 8, (HY1 + ROW_TOP) / 2 + 1, t["existing_note"], c=SOFT, room=res_c - ex_c - 20)
    # Open simulation results -> Results (right, then down).
    fk.route(s, [(rs1, ROW2), (res_c, ROW2), (res_c, ROW_TOP)])
    fk.text(s, HX1 + 10, ROW2 - 11, t["results_note"], c=SOFT, room=740 - HX1 - 16)

    # ---- the four columns ----------------------------------------------------------------
    icons = ["wand-sparkles", "sliders-horizontal", "play", "layers"]
    names = [t["wizard"], t["setup"], t["run"], t["results"]]
    for k, ((x0, x1), icon, name) in enumerate(zip(COLS, icons, names)):
        fk.panel(s, x0, ROW_TOP, x1 - x0, ROW_BOT - ROW_TOP,
                 fill="#ffffff" if k == 0 else color("deep_fill"), edge=None if k == 0 else WATER)
        heading(s, x0 + 12, ROW_TOP + 18, icon, name, size=10, room=x1 - x0 - 34)
        if k > 0:
            fk.text(s, x1 - 10, ROW_TOP + 18, t["keys"][k - 1], c=SOFT, ha="right")

    # Wizard.
    x0, x1 = COLS[0]
    y = steps(s, x0 + 12, ROW_TOP + 42, t["wizard_steps"], notes={1: t["catchment_note"]},
              room=x1 - x0 - 24)
    bm0, bm1 = fk.chip(s, x0 + 12, y + 5, t["build_model"])
    fk.lines(s, x0 + 12, y + 26, t["build_note"], c=SOFT, room=x1 - x0 - 24)
    om_y = y + 26 + 17 + 23
    om0, om1 = fk.chip(s, x0 + 12, om_y, t["open_model"])
    fk.route(s, [(om1, om_y), (COLS[1][0], om_y)])

    # Setup.
    x0, x1 = COLS[1]
    y = steps(s, x0 + 12, ROW_TOP + 42, t["setup_steps"], room=x1 - x0 - 24)
    review_y = y - 17
    fk.lines(s, x0 + 12, y + 8, t["status_lines"], room=x1 - x0 - 24)
    cs_y = y + 8 + 2 * 17 + 28
    fk.chip(s, x0 + 12, cs_y, t["continue_setup"])
    fk.lines(s, x0 + 12, cs_y + 22, t["continue_note"], c=SOFT, room=x1 - x0 - 24)

    # Run.
    x0, x1 = COLS[2]
    y = ROW_TOP + 42
    for row in t["run_rows"]:
        if isinstance(row[0], tuple):
            fk.rich(s, x0 + 12, y, row, room=x1 - x0 - 24)
            y += 17
        else:
            fk.lines(s, x0 + 12, y, row, room=x1 - x0 - 24)
            y += 17 * len(row) + 6
    ci_y = y + 4
    fk.chip(s, x0 + 12, ci_y, t["check_inputs"])
    rm_y = ci_y + 26
    rm0, rm1 = fk.chip(s, x0 + 12, rm_y, t["run_model"])
    fk.lines(s, x0 + 12, rm_y + 22, t["run_after"], c=SOFT, room=x1 - x0 - 24)
    y = rm_y + 22 + 26
    fk.rich(s, x0 + 12, y, t["live"][0])
    fk.lines(s, x0 + 12, y + 17, t["live"][1], room=x1 - x0 - 24)
    live_end = y + 17 * len(t["live"][1])
    if live_end > ROW_BOT - 8:
        print(f"WARNING [{lang}]: Run column ends at {live_end:.0f}")

    # Setup -> Run at the Review step; Run model -> Results.
    fk.arrow(s, (COLS[1][1], review_y), (COLS[2][0], review_y))
    fk.route(s, [(rm1, rm_y), (COLS[3][0], rm_y)])

    # Results.
    x0, x1 = COLS[3]
    y = ROW_TOP + 42
    for row in t["results_rows"]:
        if row:
            fk.lines(s, x0 + 12, y, [row], room=x1 - x0 - 24)
            y += 17
        else:
            y += 6

    # ---- Calibrate, the fourth workspace ---------------------------------------------------
    fk.panel(s, 20, CY0, 720, CY1 - CY0, fill=color("deep_fill"), edge=WATER)
    heading(s, 32, CY0 + 18, "target", t["calibrate"], size=10)
    fk.text(s, 730, CY0 + 18, t["keys"][3], c=SOFT, ha="right")
    cy = CY0 + 42
    fk.lines(s, 32, cy, t["cal_obs"], room=236 - 32 - 8)
    fk.lines(s, 236, cy, t["cal_search"], room=450 - 236 - 8)
    sc0, sc1 = fk.chip(s, 450, cy, t["start_calibration"])
    fk.text(s, sc1 + 8, cy, t["cal_start_note"], c=SOFT, room=726 - sc1 - 8)
    ap0, ap1 = fk.chip(s, 450, cy + 26, t["apply"])
    un0, un1 = fk.chip(s, ap1 + 6, cy + 26, t["undo"])
    fk.text(s, 450, cy + 49, t["cal_apply_note"], c=SOFT, room=730 - 450)

    # ---- edits strip ------------------------------------------------------------------------
    fk.panel(s, 20, EY0, 720, EY1 - EY0, fill=color("slot_rock_even"))
    heading(s, 34, EY0 + 18, "save", t["edits"], size=10)
    bx = [(34, 232), (346, 462)]
    by0, by1 = EY0 + 34, EY0 + 90
    fk.panel(s, bx[0][0], by0, bx[0][1] - bx[0][0], by1 - by0)
    fk.text(s, bx[0][0] + 10, by0 + 18, t["open_box"], bold=True, room=bx[0][1] - bx[0][0] - 16)
    fk.lines(s, bx[0][0] + 10, by0 + 36, t["open_box_lines"], room=bx[0][1] - bx[0][0] - 16)
    fk.panel(s, bx[1][0], by0, bx[1][1] - bx[1][0], by1 - by0, fill=color("deep_fill"), edge=WATER)
    # One title line as in English, or two (Portuguese, Spanish) on a tighter pitch.
    title = t["file_box"]
    ty, pitch = (by0 + 18, 18) if len(title) == 1 else (by0 + 13, 15)
    fk.lines(s, bx[1][0] + 10, ty, [[(row, B)] for row in title], pitch=pitch, room=bx[1][1] - bx[1][0] - 16)
    fk.lines(s, bx[1][0] + 10, ty + pitch * len(title), t["file_box_lines"], room=bx[1][1] - bx[1][0] - 16)
    ya, yb = by0 + 19, by1 - 19
    fk.arrow(s, (bx[0][1], ya), (bx[1][0], ya))
    fk.arrow(s, (bx[1][0], yb), (bx[0][1], yb))
    mid = (bx[0][1] + bx[1][0]) / 2
    fk.rich(s, mid, ya - 13, [(t["save"], B), ("  " + t["save_key"], L)], ha="center")
    fk.text(s, mid, yb + 13, t["revert"], bold=True, ha="center")
    fk.lines(s, 474, EY0 + 18, t["edit_notes"], room=740 - 474 - 10)

    svg = s.save(STATIC / "studio", lang, preview)
    print("wrote", svg.name)


if __name__ == "__main__":
    main(Path(sys.argv[1]) if len(sys.argv) > 1 else None)


# Sources in the docs (Studio section), one per element of the figure; checked against
# Studio 0.9.0rc2.
FACTS = {
    "installer and license code from Marcus; Mac Apple silicon or Windows": "studio/install-and-license",
    "license window, Activate, opens on Home": "studio/install-and-license, Activate",
    "Home: New model, Open existing model (case.yaml or legacy workbook), Open simulation results":
        "studio/overview, Home",
    "wizard: nine pages, Catchment only for outlet choices, Build model, Open model":
        "studio/building-a-model, New model wizard",
    "Setup: seven steps, status, Continue setup": "studio/overview, Workspaces; studio/building-a-model",
    "Run: Outputs, Computing backend (CPU), Save results to, Check inputs, Run model, checks first, Live diagnostics":
        "studio/run-and-results, Run",
    "Results: playback, max/min/final maps, right-click, exports, own layer panel": "studio/run-and-results, Results",
    "Calibrate: observed discharge, water depths, water levels, groundwater depths; genetic algorithm or "
    "SCE-UA over the Free parameters; Start calibration in the background; Apply to model, Undo apply":
        "studio/calibrate",
    "Cmd+1 to Cmd+4": "studio/overview, Workspaces; studio/working-in-studio, shortcuts",
    "edits apply as you go, Save writes the model file, Unsaved changes, Save/Check inputs/Run take edits, Revert to saved":
        "studio/working-in-studio, Edits, Save and Revert to saved",
}
