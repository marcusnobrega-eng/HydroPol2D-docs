"""The Case Builder from first start to a case ready to run, for docs/builder/overview.md.

The license page, the public data, the four steps (choose the area, preview, prepare, check),
the case folder and where the case runs, as in Case Builder 0.1.0. Adapted from the download
page's figure (HydroPol2D-Case-Builder packaging/release_page/workflow_figure.py).

The Builder's interface is English only, so its tab, button and option names stay in English
in every language, as on the Studio pages, and are set in bold ((text, True) runs). Only the
descriptions are translated.

Run from the repository root:

    python3 figures/case_builder_workflow.py [preview-folder]

Output: static/img/builder/case-builder-workflow.svg (en), case-builder-workflow.pt.svg and
case-builder-workflow.es.svg, a PNG of each in the preview folder, if given, and the icon
licence log figures/case_builder_workflow_icons.csv.
"""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import flow_kit as fk  # noqa: E402
import lucide_draw as li  # noqa: E402
from site_style import HERE, INK, STATIC, WATER, Sheet, color  # noqa: E402

W = 760
NAME = "case-builder-workflow"
B, L = True, False  # bold and light runs

# The Builder's own labels, the same in every language.
UI = {
    "activate": "Activate",
    "urban_basin": "Urban Basin",
    "urban_only": "Urban Area Only",
    "catchment": "Catchment",
    "preview": "Preview domain and cost",
    "prepare": "Prepare complete case",
    "check": "Check a case",
    "ready": "Ready to run",
    "run_case": "run_case.m",
    "case_yaml": "case.yaml",
    "new_model": "New model",
}

LABELS = {
    "en": {
        "first": "First start",
        "first_l1": "Open the app. A small window starts the Case Builder and opens it in your browser",
        "first_l2": "The page asks for your license code once. Paste the whole code and click",
        "data": "Public data, downloaded once and kept in a cache",
        "data_rows": [
            [[("Terrain ", B), ("FABDEM or your DEM", L)],
             [("Basins, rivers ", B), ("HydroSHEDS", L)],
             [("Cities ", B), ("GHSL urban centres", L)]],
            [[("Land cover ", B), ("ESA WorldCover", L)],
             [("Soil, bedrock ", B), ("OpenLandMap, ISRIC", L)],
             [("Groundwater ", B), ("global water-table depth", L)]],
            [[("Rain ", B), ("IMERG, ERA5, MSWEP, AORC", L)],
             [("Weather ", B), ("ERA5", L)],
             [("Soil water ", B), ("ERA5-Land", L)],
             [("Leaf area ", B), ("MODIS", L)]],
        ],
        "step1": "1  Choose the area",
        "step1_rows": ["a city and every basin", "draining into it", None,
                       "the city and a buffer", None, "all that drains to", "an outlet you choose",
                       "", "then cell size, dates,", "rain and processes"],
        "step2": "2  Preview",
        "step2_rows": ["", "the domain on a map", "grid and active cells", "basin area",
                       "data to download", "size of saved results", "", "nothing is built yet"],
        "step3": "3  Prepare",
        "step3_rows": ["", "downloads the data", "conditions the terrain", "and river channels",
                       "maps every layer onto", "the model grid", "writes rain, weather",
                       "and boundary series"],
        "step4": "4  Check",
        "step4_rows": ["", "files, grids, dates,", "units and model inputs", "", None,
                       "or a list of what", "is missing"],
        "folder": "The case folder",
        "folder_left": ["terrain, land cover, soil, groundwater and",
                        "starting-condition maps on the model grid",
                        "rain, weather and boundary series"],
        "folder_right": [" for MATLAB, ", " for Python"],
        "folder_right2": ["preview maps and quality reports", "a record of every source and version"],
        "run": "Run it",
        "run_l1": [("HydroPol2D MATLAB", B), (" (open source), or", L)],
        "run_l2": [("HydroPol2D Python", B), (" in HydroPol2D Studio", L)],
        "run_r1": [("Studio", B), (" has the Case Builder built in", L)],
        "run_r2": [("as its ", L), ("New model", B), (" step, under Studio's own code", L)],
    },
    "pt": {
        "first": "Primeiro uso",
        "first_l1": "Abra o app. Uma janela pequena inicia o Case Builder e o abre no seu navegador",
        "first_l2": "A página pede o seu código de licença uma vez. Cole o código inteiro e clique em",
        "data": "Dados públicos, baixados uma vez e guardados em cache",
        "data_rows": [
            [[("Terreno ", B), ("FABDEM ou o seu DEM", L)],
             [("Bacias, rios ", B), ("HydroSHEDS", L)],
             [("Cidades ", B), ("centros urbanos GHSL", L)]],
            [[("Cobertura do solo ", B), ("ESA WorldCover", L)],
             [("Solo, rocha ", B), ("OpenLandMap, ISRIC", L)],
             [("Água subterrânea ", B), ("lençol global", L)]],
            [[("Chuva ", B), ("IMERG, ERA5, MSWEP, AORC", L)],
             [("Clima ", B), ("ERA5", L)],
             [("Umidade do solo ", B), ("ERA5-Land", L)],
             [("Área foliar ", B), ("MODIS", L)]],
        ],
        "step1": "1  Escolha a área",
        "step1_rows": ["a cidade e as bacias", "que drenam para ela", None,
                       "a cidade e uma faixa", None, "tudo o que drena para", "um exutório escolhido",
                       "", "depois célula, datas,", "chuva e processos"],
        "step2": "2  Prévia",
        "step2_rows": ["", "o domínio no mapa", "células totais e ativas", "área da bacia",
                       "dados a baixar", "tamanho da saída", "", "nada é construído"],
        "step3": "3  Prepare",
        "step3_rows": ["", "baixa os dados", "condiciona o terreno", "e os canais dos rios",
                       "põe cada camada na", "grade do modelo", "grava chuva, clima e",
                       "séries de contorno"],
        "step4": "4  Verifique",
        "step4_rows": ["", "arquivos, datas,", "grades, unidades", "e entradas", "", None,
                       "ou a lista do que", "está faltando"],
        "folder": "A pasta do caso",
        "folder_left": ["mapas de terreno, cobertura do solo, solo,",
                        "água subterrânea e condições iniciais",
                        "séries de chuva, clima e contorno"],
        "folder_right": [" para MATLAB, ", " para Python"],
        "folder_right2": ["mapas de prévia e relatórios de qualidade", "registro de cada fonte e versão"],
        "run": "Rode o caso",
        "run_l1": [("HydroPol2D MATLAB", B), (" (código aberto) ou", L)],
        "run_l2": [("HydroPol2D Python", B), (" no HydroPol2D Studio", L)],
        "run_r1": [("O Studio", B), (" traz o Case Builder embutido", L)],
        "run_r2": [("na etapa ", L), ("New model", B), (", com o código do Studio", L)],
    },
    "es": {
        "first": "Primer uso",
        "first_l1": "Abra la app. Una ventana pequeña inicia el Case Builder y lo abre en su navegador",
        "first_l2": "La página pide su código de licencia una vez. Pegue el código entero y haga clic en",
        "data": "Datos públicos, descargados una vez y guardados en caché",
        "data_rows": [
            [[("Terreno ", B), ("FABDEM o su DEM", L)],
             [("Cuencas, ríos ", B), ("HydroSHEDS", L)],
             [("Ciudades ", B), ("centros urbanos GHSL", L)]],
            [[("Cobertura ", B), ("ESA WorldCover", L)],
             [("Suelo, roca ", B), ("OpenLandMap, ISRIC", L)],
             [("Agua subterránea ", B), ("nivel freático global", L)]],
            [[("Lluvia ", B), ("IMERG, ERA5, MSWEP, AORC", L)],
             [("Clima ", B), ("ERA5", L)],
             [("Humedad del suelo ", B), ("ERA5-Land", L)],
             [("Área foliar ", B), ("MODIS", L)]],
        ],
        "step1": "1  Elija el área",
        "step1_rows": ["la ciudad y las cuencas", "que drenan a ella", None,
                       "la ciudad y una franja", None, "todo lo que drena a", "una salida que elige",
                       "", "luego celda, fechas,", "lluvia y procesos"],
        "step2": "2  Vista previa",
        "step2_rows": ["", "el dominio en un mapa", "celdas totales y activas", "área de la cuenca",
                       "datos a descargar", "tamaño de resultados", "", "aún no se construye"],
        "step3": "3  Prepare",
        "step3_rows": ["", "descarga los datos", "acondiciona el terreno", "y los cauces",
                       "pone cada capa en la", "malla del modelo", "escribe lluvia, clima y",
                       "series de contorno"],
        "step4": "4  Verifique",
        "step4_rows": ["", "archivos, fechas,", "mallas, unidades", "y entradas", "", None,
                       "o la lista de lo que", "falta"],
        "folder": "La carpeta del caso",
        "folder_left": ["mapas de terreno, cobertura, suelo, agua",
                        "subterránea y condiciones iniciales en la malla",
                        "series de lluvia, clima y contorno"],
        "folder_right": [" para MATLAB, ", " para Python"],
        "folder_right2": ["mapas de vista previa e informes de calidad", "registro de cada fuente y versión"],
        "run": "Ejecute el caso",
        "run_l1": [("HydroPol2D MATLAB", B), (" (código abierto) o", L)],
        "run_l2": [("HydroPol2D Python", B), (" en HydroPol2D Studio", L)],
        "run_r1": [("Studio", B), (" trae el Case Builder integrado", L)],
        "run_r2": [("en el paso ", L), ("New model", B), (", con el código de Studio", L)],
    },
}


def heading(s, x, y, icon, label, *, size=10.5, icon_size=16, room=None):
    li.draw(s.ax, icon, x + icon_size / 2, y, icon_size, INK, lw=1.1)
    fk.text(s, x + icon_size + 6, y, label, bold=True, size=size, room=room)
    return x + icon_size + 6 + fk.width(s, label, bold=True, size=size)


def column_lines(s, x, y, rows, room):
    """Rows: a string (light), a list of (text, bold) runs, or "" for a small gap."""
    for row in rows:
        if row == "":
            y += 6
            continue
        if isinstance(row, str):
            fk.text(s, x, y, row, room=room)
        else:
            fk.rich(s, x, y, row, room=room)
        y += 17
    return y


def with_names(rows, names):
    """Put the Builder's bold names where a row is None, in order."""
    names = iter(names)
    return [[(next(names), B)] if row is None else row for row in rows]


def main(preview: Path | None = None) -> None:
    for lang in LABELS:
        draw(lang, preview)
    li.write_licence_log(HERE / "case_builder_workflow_icons.csv")


def draw(lang: str, preview: Path | None = None) -> None:
    t = {**UI, **LABELS[lang]}
    COLS = [(20 + 185 * k, 185 + 185 * k) for k in range(4)]  # 165 px wide, 20 px apart
    DY0, DY1 = 86, 194
    ROW_TOP, ROW_BOT = 216, 446
    OY0, OY1 = 468, 560
    RY0, RY1 = 582, 656
    s = Sheet(W, RY1 + 16, NAME)

    # ---- first start -------------------------------------------------------------------------
    fk.panel(s, 20, 16, 720, 48)
    xh = heading(s, 34, 31, "key-round", t["first"])
    fk.text(s, xh + 12, 31, t["first_l1"], room=726 - xh - 12)
    fk.text(s, 56, 49, t["first_l2"])
    x0, x1 = fk.chip(s, 56 + fk.width(s, t["first_l2"]) + 6, 49, t["activate"])
    if x1 > 726:
        print(f"WARNING [{lang}]: license line ends at {x1:.0f}")
    fk.arrow(s, (380, 64), (380, DY0))

    # ---- public data -------------------------------------------------------------------------
    fk.panel(s, 20, DY0, 720, DY1 - DY0, fill=color("slot_near_surface"), edge=color("slot_transmission"))
    heading(s, 34, DY0 + 18, "layers", t["data"], size=10)
    for (x, room), rows in zip(((34, 212), (254, 242), (504, 228)), t["data_rows"]):
        column_lines(s, x, DY0 + 40, rows, room=room)

    # ---- the four steps ----------------------------------------------------------------------
    steps = [
        ("map", t["step1"], [[(t["urban_basin"], B)],
                             *with_names(t["step1_rows"], (t["urban_only"], t["catchment"]))]),
        ("app-window", t["step2"], [[("Preview domain", B)], [("and cost", B)], *t["step2_rows"]]),
        ("package", t["step3"], [[("Prepare complete", B)], [("case", B)], *t["step3_rows"]]),
        ("circle-check-big", t["step4"], with_names([[(t["check"], B)], *t["step4_rows"]], (t["ready"],))),
    ]
    for k, ((x0, x1), (icon, name, rows)) in enumerate(zip(COLS, steps)):
        fk.panel(s, x0, ROW_TOP, x1 - x0, ROW_BOT - ROW_TOP, fill=color("deep_fill"), edge=WATER)
        heading(s, x0 + 12, ROW_TOP + 18, icon, name, size=10, room=x1 - x0 - 34)
        end = column_lines(s, x0 + 12, ROW_TOP + 42, rows, room=x1 - x0 - 24)
        if end > ROW_BOT:
            print(f"WARNING [{lang}]: column {k + 1} ends at {end:.0f}")
        if k < len(COLS) - 1:
            fk.arrow(s, (x1, ROW_TOP + 18), (COLS[k + 1][0], ROW_TOP + 18))
    # The data feed the preview and the case.
    for k in (1, 2):
        mid = (COLS[k][0] + COLS[k][1]) / 2
        fk.arrow(s, (mid, DY1), (mid, ROW_TOP))

    # ---- the case folder ---------------------------------------------------------------------
    mid3 = (COLS[2][0] + COLS[2][1]) / 2
    fk.arrow(s, (mid3, ROW_BOT), (mid3, OY0))
    fk.panel(s, 20, OY0, 720, OY1 - OY0)
    heading(s, 34, OY0 + 18, "box", t["folder"], size=10)
    column_lines(s, 34, OY0 + 42, t["folder_left"], room=350)
    a, b = t["folder_right"]
    column_lines(s, 396, OY0 + 42, [[(t["run_case"], B), (a, L), (t["case_yaml"], B), (b, L)],
                                    *t["folder_right2"]], room=336)

    # ---- run it ------------------------------------------------------------------------------
    fk.arrow(s, (380, OY1), (380, RY0))
    fk.panel(s, 20, RY0, 720, RY1 - RY0, fill=color("slot_rock_even"))
    heading(s, 34, RY0 + 18, "play", t["run"], size=10)
    fk.rich(s, 34, RY0 + 40, t["run_l1"], room=350)
    fk.rich(s, 34, RY0 + 57, t["run_l2"], room=350)
    fk.rich(s, 396, RY0 + 40, t["run_r1"], room=336)
    fk.rich(s, 396, RY0 + 57, t["run_r2"], room=336)

    svg = s.save(STATIC / "builder", lang, preview)
    print("wrote", svg.name)


if __name__ == "__main__":
    main(Path(sys.argv[1]) if len(sys.argv) > 1 else None)
