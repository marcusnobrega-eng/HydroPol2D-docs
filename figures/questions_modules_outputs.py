""""What HydroPol2D can answer": schematic for docs/getting-started/overview.md.

A question a user brings, the module that answers it with its status as the docs state it,
and the output Studio shows. Studio's own names stay in English in every language, as on the
Studio pages. Human instability: mode 1 (the risk index) runs on grids and meshes; mode 3
(the classes) also uses the local DEM slope and runs on regular grids only.

Run from the repository root:

    python3 figures/questions_modules_outputs.py [preview-folder]

Output: static/img/getting-started/questions-modules-outputs.svg (en), .pt.svg and .es.svg,
a PNG of each in the preview folder when one is given, and the icon licence log
figures/questions_modules_outputs_icons.csv.

Every element and the docs page it comes from is listed in FACTS at the end of this file.
"""

from __future__ import annotations

import sys
from pathlib import Path

import flow_kit as fk
import lucide_draw as li
from site_style import HERE, INK, SOFT, STATIC, Sheet, color, oklch_hex

NAME = "questions-modules-outputs"
SECTION = "getting-started"
W = 760
B, L = True, False

# Acceptance green of the validation figure, reused so the figures agree: a light fill in the
# hue of the "ground" token, with the ground edge. Not in palette.py.
ACCEPT_FILL = oklch_hex(0.955, 0.030, 145)
ACCEPT_EDGE = color("ground")

# Figure text. A row is one question, its module and its outputs.
#   module["lines"]: (text, role, evidence) per line; role "default" / "optional" / None,
#   evidence "validated" / "tests" / None. The first line is the module name (bold).
#   outputs: (icon, text) per line; icon "map", "chart-line" or None for a continued line.
#   grid (optional): the question, module and output columns, (x0, x1) each, in px.
LABELS = {
    "en": {
        "col_q": "Your question",
        "col_m": "The module that answers it",
        "col_status": "status",
        "col_o": "The output that shows it",
        "role": {"default": "default", "optional": "optional"},
        "evidence": {"validated": "validated", "tests": "tests only"},
        "rows": [
            {
                "icon": "waves-horizontal",
                "q": ["Where does the", "water go, and how", "deep does it get?"],
                "m": [("Surface routing", None, None),
                      ("local inertial", "default", "validated"),
                      ("four other solvers", "optional", "validated")],
                "o": [("map", "depth and water-surface elevation"),
                      (None, "maps; the maximum depth map"),
                      ("chart-line", "outlet and gauge hydrographs")],
            },
            {
                "icon": "cloud-rain",
                "q": ["How much rain", "becomes runoff?"],
                "m": [("Hydrologic core", "default", "validated"),
                      ("interception, evapotranspiration,", None, None),
                      ("infiltration and soil water storage", None, None)],
                "o": [("chart-line", "hydrographs at the outlet"),
                      ("chart-line", "water-balance diagnostics"),
                      ("map", "evaporation and transpiration maps")],
            },
            {
                "icon": "snowflake",
                "q": ["What does", "snowmelt add", "to runoff?"],
                "m": [("Snow", "default", "validated"),
                      ("accumulation, melt, sublimation;", None, None),
                      ("needs weather forcing", None, None)],
                "o": [("map", "snow water equivalent maps"),
                      ("chart-line", "hydrographs at the outlet")],
            },
            {
                "icon": "waves-arrow-down",
                "q": ["Where does the", "water table rise", "and fall?"],
                "m": [("Groundwater", "default", "validated"),
                      ("recharge, water table, lateral flow", None, None),
                      ("layered subsurface", "optional", "tests"),
                      ("deep aquifer", "optional", "tests")],
                "o": [("map", "water-table depth maps"),
                      ("chart-line", "water-table depth at a cell"),
                      ("chart-line", "water-balance diagnostics")],
            },
            {
                "icon": "person-standing",
                "q": ["Are people at risk", "in the floodwater?"],
                "m": [("Human instability", "optional", "validated"),
                      ("hazard diagnostic from depth and velocity;", None, None),
                      ("mode 3 adds the local slope, on grids only", None, None)],
                "o": [("map", "risk ratio maps (mode 1)"),
                      ("map", "slide, topple or drowning class"),
                      (None, "maps (mode 3)")],
            },
            {
                "icon": "flask-conical",
                "q": ["How much", "pollutant leaves", "the catchment?"],
                "m": [("Water quality", "optional", "validated"),
                      ("pollutant build-up, wash-off and", None, None),
                      ("transport (mass-based mode)", None, None)],
                "o": [("chart-line", "outlet concentration over time"),
                      ("chart-line", "washed pollutant mass"),
                      ("map", "concentration maps")],
            },
        ],
        "key_role": [("default", "the model's standard pathway"),
                     ("optional", "switched on, or chosen instead")],
        "key_evidence": [("validated", "meets its thresholds against known references"),
                         ("tests", "controlled tests or fixture checks")],
        "results": [[("In Results", B), (", every saved map plays back over time, with maximum, minimum and final maps;", L)],
                    [("right-click a cell for its time series. Maps export as PNG, PDF, SVG, GeoTIFF or MP4.", L)]],
        "note": [[("The validation cases support these implementations under controlled conditions.", L)],
                 [("They do not replace field calibration, site-specific forcing checks or tests against observations.", L)]],
    },
    "pt": {
        "grid": ((20, 158), (176, 492), (510, 740)),
        "col_q": "A sua pergunta",
        "col_m": "O módulo que responde",
        "col_status": "estado",
        "col_o": "A saída que mostra",
        "role": {"default": "padrão", "optional": "opcional"},
        "evidence": {"validated": "validado", "tests": "só testes"},
        "rows": [
            {
                "icon": "waves-horizontal",
                "q": ["Para onde vai", "a água, e a que", "profundidade?"],
                "m": [("Roteamento superficial", None, None),
                      ("local inertial", "default", "validated"),
                      ("outros quatro solvers", "optional", "validated")],
                "o": [("map", "mapas de profundidade e de"),
                      (None, "elevação da superfície da água;"),
                      (None, "mapa da profundidade máxima"),
                      ("chart-line", "hidrogramas no exutório e"),
                      (None, "nos postos")],
            },
            {
                "icon": "cloud-rain",
                "q": ["Quanta chuva", "vira", "escoamento?"],
                "m": [("Núcleo hidrológico", "default", "validated"),
                      ("interceptação, evapotranspiração,", None, None),
                      ("infiltração e armazenamento de água no solo", None, None)],
                "o": [("chart-line", "hidrogramas no exutório"),
                      ("chart-line", "diagnósticos do balanço hídrico"),
                      ("map", "mapas de evaporação e de"),
                      (None, "transpiração")],
            },
            {
                "icon": "snowflake",
                "q": ["Quanto o degelo", "acrescenta ao", "escoamento?"],
                "m": [("Neve", "default", "validated"),
                      ("acúmulo, degelo e sublimação;", None, None),
                      ("requer forçantes meteorológicas", None, None)],
                "o": [("map", "mapas de equivalente de água"),
                      (None, "da neve"),
                      ("chart-line", "hidrogramas no exutório")],
            },
            {
                "icon": "waves-arrow-down",
                "q": ["Onde o lençol", "freático sobe", "e desce?"],
                "m": [("Água subterrânea", "default", "validated"),
                      ("recarga, lençol freático, fluxo lateral", None, None),
                      ("subsuperfície em camadas", "optional", "tests"),
                      ("aquífero profundo", "optional", "tests")],
                "o": [("map", "mapas de profundidade do"),
                      (None, "lençol freático"),
                      ("chart-line", "profundidade do lençol"),
                      (None, "em uma célula"),
                      ("chart-line", "diagnósticos do balanço hídrico")],
            },
            {
                "icon": "person-standing",
                "q": ["As pessoas", "correm risco na", "inundação?"],
                "m": [("Instabilidade humana", "optional", "validated"),
                      ("diagnóstico de risco pela profundidade e", None, None),
                      ("velocidade; o modo 3 também usa a", None, None),
                      ("declividade e só roda em grades regulares", None, None)],
                "o": [("map", "mapas da razão de risco"),
                      (None, "(modo 1)"),
                      ("map", "mapas de classe (modo 3):"),
                      (None, "deslizamento, tombamento"),
                      (None, "ou afogamento")],
            },
            {
                "icon": "flask-conical",
                "q": ["Quanto poluente", "sai da bacia?"],
                "m": [("Qualidade da água", "optional", "validated"),
                      ("acúmulo, lavagem e transporte de", None, None),
                      ("poluentes (modo baseado em massa)", None, None)],
                "o": [("chart-line", "concentração no exutório ao"),
                      (None, "longo do tempo"),
                      ("chart-line", "massa de poluente lavada"),
                      ("map", "mapas de concentração")],
            },
        ],
        "key_role": [("default", "o caminho padrão do modelo"),
                     ("optional", "ativado, ou escolhido no lugar")],
        "key_evidence": [("validated", "cumpre seus critérios frente a referências conhecidas"),
                         ("tests", "testes controlados ou verificações com fixtures")],
        "results": [[("Em ", L), ("Results", B), (", cada mapa salvo é reproduzido ao longo do tempo, com mapas de máximo,", L)],
                    [("mínimo e final; clique com o botão direito em uma célula para ver a sua série temporal.", L)],
                    [("Os mapas são exportados em PNG, PDF, SVG, GeoTIFF ou MP4.", L)]],
        "note": [[("Os casos de validação sustentam essas implementações em condições controladas. Eles não", L)],
                 [("substituem a calibração em campo, a verificação das forçantes do local nem os testes", L)],
                 [("com observações.", L)]],
    },
    "es": {
        "grid": ((20, 150), (168, 498), (516, 740)),
        "col_q": "Su pregunta",
        "col_m": "El módulo que la responde",
        "col_status": "estado",
        "col_o": "La salida que lo muestra",
        "role": {"default": "estándar", "optional": "opcional"},
        "evidence": {"validated": "validado", "tests": "solo pruebas"},
        "rows": [
            {
                "icon": "waves-horizontal",
                "q": ["¿Adónde va el", "agua y qué", "profundidad", "alcanza?"],
                "m": [("Enrutamiento superficial", None, None),
                      ("local inertial", "default", "validated"),
                      ("otros cuatro solvers", "optional", "validated")],
                "o": [("map", "mapas de profundidad y de"),
                      (None, "elevación de la superficie del"),
                      (None, "agua; profundidad máxima"),
                      ("chart-line", "hidrogramas en la salida y en"),
                      (None, "las estaciones")],
            },
            {
                "icon": "cloud-rain",
                "q": ["¿Cuánta lluvia", "se convierte en", "escorrentía?"],
                "m": [("Núcleo hidrológico", "default", "validated"),
                      ("intercepción, evapotranspiración,", None, None),
                      ("infiltración y almacenamiento de agua en el suelo", None, None)],
                "o": [("chart-line", "hidrogramas en la salida"),
                      ("chart-line", "diagnóstico del balance hídrico"),
                      ("map", "mapas de evaporación y de"),
                      (None, "transpiración")],
            },
            {
                "icon": "snowflake",
                "q": ["¿Cuánto aporta", "el deshielo a la", "escorrentía?"],
                "m": [("Nieve", "default", "validated"),
                      ("acumulación, deshielo y sublimación;", None, None),
                      ("requiere forzantes meteorológicos", None, None)],
                "o": [("map", "mapas de equivalente de agua"),
                      (None, "de nieve"),
                      ("chart-line", "hidrogramas en la salida")],
            },
            {
                "icon": "waves-arrow-down",
                "q": ["¿Dónde sube y", "baja el nivel", "freático?"],
                "m": [("Agua subterránea", "default", "validated"),
                      ("recarga, nivel freático, flujo lateral", None, None),
                      ("subsuelo en capas", "optional", "tests"),
                      ("acuífero profundo", "optional", "tests")],
                "o": [("map", "mapas de profundidad del"),
                      (None, "nivel freático"),
                      ("chart-line", "profundidad del nivel"),
                      (None, "freático en una celda"),
                      ("chart-line", "diagnóstico del balance hídrico")],
            },
            {
                "icon": "person-standing",
                "q": ["¿Hay personas", "en peligro en la", "inundación?"],
                "m": [("Inestabilidad humana", "optional", "validated"),
                      ("diagnóstico de peligro según profundidad", None, None),
                      ("y velocidad; el modo 3 usa también la", None, None),
                      ("pendiente y solo corre en mallas regulares", None, None)],
                "o": [("map", "mapas de relación de riesgo"),
                      (None, "(modo 1)"),
                      ("map", "mapas de clase (modo 3):"),
                      (None, "deslizamiento, caída o"),
                      (None, "ahogamiento")],
            },
            {
                "icon": "flask-conical",
                "q": ["¿Cuánto", "contaminante", "sale de la", "cuenca?"],
                "m": [("Calidad del agua", "optional", "validated"),
                      ("acumulación, lavado y transporte de", None, None),
                      ("contaminantes (modo basado en masa)", None, None)],
                "o": [("chart-line", "concentración en la salida en"),
                      (None, "el tiempo"),
                      ("chart-line", "masa de contaminante lavada"),
                      ("map", "mapas de concentración")],
            },
        ],
        "key_role": [("default", "la vía habitual del modelo"),
                     ("optional", "se activa, o se elige en su lugar")],
        "key_evidence": [("validated", "cumple sus umbrales ante referencias conocidas"),
                         ("tests", "pruebas controladas o verificaciones con fixtures")],
        "results": [[("En ", L), ("Results", B), (", cada mapa guardado se reproduce en el tiempo, con mapas máximo, mínimo", L)],
                    [("y final; haga clic derecho en una celda para ver su serie de tiempo. Los mapas se", L)],
                    [("exportan como PNG, PDF, SVG, GeoTIFF o MP4.", L)]],
        "note": [[("Los casos de validación respaldan estas implementaciones en condiciones controladas.", L)],
                 [("No sustituyen la calibración en campo, la revisión de los forzantes del sitio ni las", L)],
                 [("pruebas con observaciones.", L)]],
    },
}

# Grid (px). Three columns joined by arrows; rows top-aligned. The English grid; a language
# with longer module names sets its own.
GRID = ((20, 168), (190, 470), (492, 740))
PITCH = 17          # text line pitch
PITCH_PILL = 18     # next to a line that carries a pill
PITCH_PILLS = 20    # between two lines that carry pills
FIRST = 15          # first line centre below a row's top
PAD_BOTTOM = 12
ROW_GAP = 6
HEAD_Y = 22
ROWS_TOP = 37
PILL_H = 17


def pill(s, x0, y, label, kind):
    """Evidence pill from x0: acceptance green for validated, white with a soft edge for tests.
    Returns the right edge."""
    w = fk.width(s, label) + 14
    s.box(x0, y - PILL_H / 2, w, PILL_H, fill=ACCEPT_FILL if kind == "validated" else "#ffffff",
          edge=ACCEPT_EDGE if kind == "validated" else SOFT, radius=PILL_H / 2, lw=0.9, z=4)
    s.text(x0 + 7, y + 0.6, label, z=5)
    return x0 + w


def pill_width(s, label):
    return fk.width(s, label) + 14


def module_offsets(lines):
    """Line centres below the row top: wider steps next to pills so they never touch."""
    ys, prev = [], None
    for text, role, evidence in lines:
        has = evidence is not None
        if prev is None:
            ys.append(FIRST)
        else:
            step = PITCH_PILLS if (has and prev) else (PITCH_PILL if (has or prev) else PITCH)
            ys.append(ys[-1] + step)
        prev = has
    return ys


def row_height(row):
    last = max(FIRST + PITCH * (len(row["q"]) - 1), module_offsets(row["m"])[-1],
               FIRST + PITCH * (len(row["o"]) - 1))
    return last + PAD_BOTTOM


def icon_with_dot(s, name, cx, cy, size, *, lw=1.1):
    """Lucide icon whose dot is a zero-length path (info): lucide_draw drops those, so add it."""
    li.draw(s.ax, name, cx, cy, size, INK, lw=lw)
    fk.dot(s, cx, cy - 4 * size / 24, r=0.95, c=INK)


def key_height(t):
    """Height of the key panel: two key rows, then the Results and note paragraphs."""
    return 17 + 46 + PITCH * (len(t["results"]) - 1) + 22 + PITCH * (len(t["note"]) - 1) + 16


def build(lang="en"):
    t = LABELS[lang]
    QX, MX, OX = t.get("grid", GRID)
    pill_right = MX[1] - 10
    # The role words sit in one column, left of the widest pill; the English grid gives the
    # drafted column at MX[0] + 144.
    widest_pill = max(pill_width(None, v) for v in t["evidence"].values())
    widest_role = max(fk.width(None, v) for v in t["role"].values())
    role_x = MX[0] + 144 if "grid" not in t else pill_right - widest_pill - 6 - widest_role

    rows_h = sum(row_height(row) + ROW_GAP for row in t["rows"])
    height = ROWS_TOP + rows_h + 2 + key_height(t) + 14
    s = Sheet(W, height, NAME)

    # ---- column headings -----------------------------------------------------------------
    fk.text(s, QX[0] + 12, HEAD_Y, t["col_q"], bold=True, size=11, room=QX[1] - QX[0] - 12)
    fk.text(s, MX[0] + 12, HEAD_Y, t["col_m"], bold=True, size=11, room=pill_right - 50 - MX[0] - 12)
    fk.text(s, pill_right, HEAD_Y, t["col_status"], c=SOFT, ha="right")
    fk.text(s, OX[0] + 12, HEAD_Y, t["col_o"], bold=True, size=11, room=OX[1] - OX[0] - 12)

    # ---- rows ------------------------------------------------------------------------------
    y0 = ROWS_TOP
    for row in t["rows"]:
        h = row_height(row)
        ymid = y0 + h / 2
        fk.panel(s, QX[0], y0, QX[1] - QX[0], h, fill=color("slot_rock_even"))
        fk.panel(s, MX[0], y0, MX[1] - MX[0], h)
        fk.panel(s, OX[0], y0, OX[1] - OX[0], h)
        fk.arrow(s, (QX[1], ymid), (MX[0], ymid))
        fk.arrow(s, (MX[1], ymid), (OX[0], ymid))

        # Question: topic icon, then the question in plain words.
        li.draw(s.ax, row["icon"], QX[0] + 17, y0 + FIRST, 16, INK, lw=1.1)
        for k, line in enumerate(row["q"]):
            fk.text(s, QX[0] + 34, y0 + FIRST + PITCH * k, line, room=QX[1] - QX[0] - 34 - 4)

        # Module: name, then lines; a line with a role and evidence carries them at the right.
        for k, ((text, role, evidence), dy) in enumerate(zip(row["m"], module_offsets(row["m"]))):
            yy = y0 + dy
            bold = k == 0
            room = (role_x - 8 - MX[0] - 12) if (role or evidence) else (MX[1] - MX[0] - 24)
            fk.text(s, MX[0] + 12, yy, text, bold=bold, size=10.5 if bold else 9.5, room=room)
            if role:
                fk.text(s, role_x, yy, t["role"][role], c=SOFT)
            if evidence:
                label = t["evidence"][evidence]
                pill(s, pill_right - pill_width(s, label), yy, label, evidence)

        # Outputs: a map or chart icon per output, as Studio's Results shows them.
        for k, (icon, text) in enumerate(row["o"]):
            yy = y0 + FIRST + PITCH * k
            if icon:
                li.draw(s.ax, icon, OX[0] + 18, yy, 13, INK, lw=1.0)
            fk.text(s, OX[0] + 30, yy, text, room=OX[1] - 8 - OX[0] - 30)
        y0 += h + ROW_GAP

    # ---- key, Results and the validation note ----------------------------------------------
    KT = y0 + 2
    KB = KT + key_height(t)
    fk.panel(s, 20, KT, 720, KB - KT, fill="#ffffff")
    ky = KT + 17
    role_desc_x = max(96, 34 + widest_role + 14)
    for k, (role, desc) in enumerate(t["key_role"]):
        yy = ky + 21 * k
        fk.text(s, 34, yy, t["role"][role], c=SOFT)
        fk.text(s, role_desc_x, yy, desc, room=310 - role_desc_x)
    ev_desc_x = max(404, 322 + widest_pill + 12)
    for k, (ev, desc) in enumerate(t["key_evidence"]):
        yy = ky + 21 * k
        pill(s, 322, yy, t["evidence"][ev], ev)
        fk.text(s, ev_desc_x, yy, desc, room=740 - 12 - ev_desc_x)
    ry = ky + 46
    li.draw(s.ax, "layers", 42, ry, 15, INK, lw=1.1)
    fk.lines(s, 60, ry, t["results"], room=740 - 12 - 60)
    ny = ry + PITCH * (len(t["results"]) - 1) + 22
    icon_with_dot(s, "info", 42, ny, 15)
    fk.lines(s, 60, ny, t["note"], room=740 - 12 - 60)
    return s


def write_icon_log(path: Path) -> None:
    """The licence log; the icon files are named from the repository root."""
    li.write_licence_log(path)


def main(preview: Path | None = None) -> None:
    for lang in LABELS:
        svg = build(lang).save(STATIC / SECTION, lang, preview)
        print("wrote", svg.relative_to(STATIC.parent.parent))
    write_icon_log(HERE / "questions_modules_outputs_icons.csv")


if __name__ == "__main__":
    main(Path(sys.argv[1]) if len(sys.argv) > 1 else None)


# Sources (docs pages), one per element of the figure. The module statuses are those of the
# capability table and the validation status page.
FACTS = {
    # scope and the questions
    "questions drawn from the current scope: routing, hydrologic core, snow, groundwater, water quality, human instability":
        "getting-started/overview; theory/overview",
    # row 1, surface routing
    "local inertial: default + validated": "configuration/overview; theory/overview; "
        "theory/hydrodynamic-model; validation/validation-status",
    "four other solvers (full momentum, diffusive D4, kinematic D4, cellular automata): optional + validated, one at a time":
        "configuration/overview; theory/overview; validation/validation-status",
    "depth and water-surface elevation maps": "configuration/general_data",
    "maximum map of the active variable": "studio/run-and-results",
    "outlet and gauge hydrographs": "configuration/general_data",
    # row 2, hydrologic core
    "hydrologic core: default + validated": "configuration/overview; theory/overview; validation/validation-status",
    "interception, evapotranspiration, infiltration, soil water (vadose) storage": "theory/hydrologic-model; theory/overview",
    "hydrographs at the outlet": "configuration/general_data",
    "water-balance diagnostics": "configuration/general_data; getting-started/model-building-workflow",
    "evaporation and transpiration maps": "configuration/general_data",
    # row 3, snow
    "snow in the default + validated hydrologic core": "configuration/overview; theory/overview; validation/validation-status",
    "accumulation, melt, sublimation": "theory/hydrologic-model",
    "needs weather forcing": "theory/hydrologic-model; configuration/flags",
    "snow water equivalent maps": "validation/voronoi-mesh; theory/hydrologic-model",
    # row 4, groundwater
    "groundwater: default + validated (default pathway when groundwater is active)":
        "configuration/overview; theory/overview; validation/validation-status",
    "recharge, water table, lateral (Boussinesq) flow when baseflow is active":
        "theory/groundwater-model; getting-started/overview",
    "layered subsurface: optional + controlled tests and parity": "configuration/overview; theory/overview; "
        "validation/validation-status",
    "deep aquifer: optional + starting-state fixture tests": "configuration/overview; theory/overview; "
        "validation/validation-status",
    "water-table depth maps": "configuration/general_data; theory/layered-subsurface",
    "time series at a cell (right-click)": "studio/run-and-results",
    "groundwater exchange in the water-balance diagnostics": "theory/groundwater-model",
    # row 5, human instability
    "human instability: optional + validated, modes 1 and 3": "configuration/overview; theory/overview; "
        "validation/validation-status",
    "hazard diagnostic from depth and velocity": "theory/human-instability; theory/overview",
    "mode 3 uses the local slope and person height; meshes run mode 1 only": "theory/human-instability; "
        "the HydroPol2D-Python engine",
    "mode 1: continuous risk ratio map": "theory/human-instability",
    "mode 3: slide, topple, drowning class map": "theory/human-instability",
    # row 6, water quality
    "water quality: optional": "configuration/overview; configuration/flags",
    "water quality: validated (mass-based mode)": "validation/validation-status; theory/water-quality-model; "
        "validation/ancillary-modules",
    "build-up, wash-off, transport": "theory/water-quality-model",
    "outlet concentration over time": "theory/water-quality-model",
    "washed pollutant mass": "theory/water-quality-model",
    "concentration maps": "configuration/general_data; validation/voronoi-mesh",
    # key, Results and note
    "default: the standard pathway; optional: switched on or chosen instead":
        "configuration/overview; theory/hydrodynamic-model",
    "validated: thresholds against known references": "validation/overview; validation/validation-status",
    "tests only: controlled tests or fixture checks": "validation/validation-status",
    "Results: playback, maximum/minimum/final maps, right-click time series, exports":
        "studio/run-and-results",
    "validation supports implementations under controlled conditions; does not replace field calibration":
        "validation/ancillary-modules; validation/limitations",
}
