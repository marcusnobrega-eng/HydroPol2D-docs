""""From data to results": schematic for docs/getting-started/overview.md.

Inputs, one case (a Studio model file or a MATLAB workbook), the run and the outputs. Studio's
own names (buttons, pages) stay in English in every language, as on the Studio pages, and are
set in bold through (text, True) runs.

Run from the repository root:

    python3 figures/data_to_results.py [preview-folder]

Output: static/img/getting-started/data-to-results.svg (en), data-to-results.pt.svg and
data-to-results.es.svg, a PNG of each in the preview folder when one is given, and the icon
licence log figures/data_to_results_icons.csv.

Every element and the docs page it comes from is listed in FACTS at the end of this file.
"""

from __future__ import annotations

import sys
from pathlib import Path

from matplotlib.patches import Rectangle

import flow_kit as fk
import lucide_draw as li
from site_style import HERE, INK, SOFT, STATIC, WATER, Sheet, color, oklch_hex

NAME = "data-to-results"
SECTION = "getting-started"
W = 760
# Output tiles: Animations has the least text, Results package the longest heading.
TILE_W = [166, 166, 132, 192]
PITCH = 17

# Figure text. The input cards and output tiles grow with their number of lines.
LABELS = {
    "en": {
        "band_inputs": "Inputs",
        "band_case": "One case",
        "band_run": "Run",
        "band_outputs": "Outputs",
        "maps": "Maps",
        "maps_sub": "GeoTIFF rasters in a projected coordinate system, aligned with the DEM",
        "required": "required",
        "optional": "optional, as the case needs",
        "map_items": [["DEM"], ["Land use and", "land cover"], ["Soil"],
                      ["Depth to", "bedrock"], ["LAI"], ["Albedo"], ["Additional", "spatial inputs"]],
        "tables": "Parameter tables",
        "tables_lines": ["one row per class code of the",
                         "land-use and soil maps; also",
                         "human instability, mesh and",
                         "control structures, when used"],
        "forcing": "Forcing",
        "forcing_lines": ["rainfall: series, gauges, maps,",
                          "satellite or a design storm",
                          "evapotranspiration and weather",
                          "inflow and stage hydrographs"],
        "settings": "Settings",
        "settings_lines": ["processes to simulate",
                           "routing solver and time step",
                           "simulation period",
                           "output intervals"],
        "studio": "HydroPol2D Studio",
        "studio_lines": [[("one model file, ", False), ("case.yaml", False)],
                         [("the ", False), ("New model", True), (" wizard can download", False)],
                         "the maps and forcing for the area"],
        "matlab": "HydroPol2D-MATLAB",
        "matlab_lines": ["one workbook, HydroPol2D_Inputs.xlsx",
                         "settings, class-table and series tabs",
                         "and the paths to your map files"],
        "or": "or",
        "run_studio": "Studio",
        "run_studio_lines": [[("Check inputs", True), (", then ", False), ("Run model", True)],
                             "HydroPol2D-Python runs it on the CPU"],
        "run_matlab": "MATLAB",
        "run_matlab_lines": ["run the workbook",
                             "HydroPol2D-MATLAB writes an output folder"],
        "out": [
            ("map", "Maps", ["depth, water-surface", "elevation, groundwater,", "at the map interval"]),
            ("chart-line", "Time series", ["hydrographs at the", "outlet and gauges,", "and the water balance"]),
            ("film", "Animations", ["MP4 videos of the", "saved maps"]),
            ("package", "Results package", ["Studio opens it in",
                                            [("Results", True), (", also without", False)],
                                            "the model"]),
        ],
    },
    "pt": {
        "band_inputs": "Entradas",
        "band_case": "Um caso",
        "band_run": "Execução",
        "band_outputs": "Saídas",
        "maps": "Mapas",
        "maps_sub": "rasters GeoTIFF em um sistema de coordenadas projetado, alinhados ao DEM",
        "required": "obrigatórios",
        "optional": "opcionais, conforme o caso",
        "map_items": [["DEM"], ["Uso e cobertura", "da terra"], ["Solo"],
                      ["Profundidade até", "o embasamento"], ["LAI"], ["Albedo"],
                      ["Outras entradas", "espaciais"]],
        "tables": "Tabelas de parâmetros",
        "tables_lines": ["uma linha por código de classe",
                         "dos mapas de uso da terra e",
                         "de solo; também instabilidade",
                         "humana, malha e estruturas",
                         "de controle, quando usadas"],
        "forcing": "Forçantes",
        "forcing_lines": ["chuva: séries, pluviômetros,",
                          "mapas, satélite ou de projeto",
                          "ET e dados meteorológicos",
                          "hidrogramas de vazão e nível"],
        "settings": "Configurações",
        "settings_lines": ["processos a simular",
                           "roteamento e passo de tempo",
                           "período de simulação",
                           "intervalos de saída"],
        "studio": "HydroPol2D Studio",
        "studio_lines": [[("um arquivo de modelo, ", False), ("case.yaml", False)],
                         [("o assistente ", False), ("New model", True), (" pode baixar os", False)],
                         "mapas e as forçantes da área"],
        "matlab": "HydroPol2D-MATLAB",
        "matlab_lines": ["uma planilha, HydroPol2D_Inputs.xlsx",
                         "abas de configurações, de tabelas de",
                         "classes e de séries, e os caminhos dos mapas"],
        "or": "ou",
        "run_studio": "Studio",
        "run_studio_lines": [[("Check inputs", True), (", depois ", False), ("Run model", True)],
                             "o HydroPol2D-Python roda o modelo na CPU"],
        "run_matlab": "MATLAB",
        "run_matlab_lines": ["rode a planilha",
                             "o HydroPol2D-MATLAB grava uma pasta de saída"],
        "out": [
            ("map", "Mapas", ["profundidade, elevação", "da superfície da água,", "água subterrânea, no",
                              "intervalo dos mapas"]),
            ("chart-line", "Séries temporais", ["hidrogramas no exutório", "e nos postos, e o",
                                                "balanço hídrico"]),
            ("film", "Animações", ["vídeos MP4 dos", "mapas salvos"]),
            ("package", "Pacote de resultados", ["o Studio o abre em",
                                                 [("Results", True), (", mesmo sem", False)],
                                                 "o modelo"]),
        ],
    },
    "es": {
        "band_inputs": "Entradas",
        "band_case": "Un caso",
        "band_run": "Ejecución",
        "band_outputs": "Salidas",
        "maps": "Mapas",
        "maps_sub": "rásteres GeoTIFF en un sistema de coordenadas proyectado, alineados con el DEM",
        "required": "obligatorios",
        "optional": "opcionales, según el caso",
        "map_items": [["DEM"], ["Uso y cobertura", "del suelo"], ["Suelo"],
                      ["Profundidad", "al basamento"], ["LAI"], ["Albedo"],
                      ["Otras entradas", "espaciales"]],
        "tables": "Tablas de parámetros",
        "tables_lines": ["una fila por código de clase",
                         "de los mapas de uso del suelo",
                         "y de suelo; también para la",
                         "inestabilidad humana, la malla",
                         "y las estructuras de control"],
        "forcing": "Forzantes",
        "forcing_lines": ["lluvia: series, pluviómetros,",
                          "mapas, satélite o de diseño",
                          "ET y datos meteorológicos",
                          "hidrogramas de caudal y nivel"],
        "settings": "Configuración",
        "settings_lines": ["procesos que se simulan",
                           "enrutamiento y paso de tiempo",
                           "período de simulación",
                           "intervalos de salida"],
        "studio": "HydroPol2D Studio",
        "studio_lines": [[("un archivo de modelo, ", False), ("case.yaml", False)],
                         [("el asistente ", False), ("New model", True), (" puede descargar", False)],
                         "los mapas y los forzantes del área"],
        "matlab": "HydroPol2D-MATLAB",
        "matlab_lines": ["un libro, HydroPol2D_Inputs.xlsx",
                         "pestañas de parámetros, de tablas de",
                         "clases y de series, y las rutas de los mapas"],
        "or": "o",
        "run_studio": "Studio",
        "run_studio_lines": [[("Check inputs", True), (", luego ", False), ("Run model", True)],
                             "HydroPol2D-Python lo ejecuta en la CPU"],
        "run_matlab": "MATLAB",
        "run_matlab_lines": ["ejecute el libro",
                             "HydroPol2D-MATLAB crea una carpeta de salida"],
        "out": [
            ("map", "Mapas", ["profundidad, elevación", "de la superficie del", "agua, nivel freático,",
                              "al intervalo de mapas"]),
            ("chart-line", "Series de tiempo", ["hidrogramas en la", "salida y en las",
                                                "estaciones, y el", "balance hídrico"]),
            ("film", "Animaciones", ["videos MP4 de los", "mapas guardados"]),
            ("package", "Paquete de resultados", ["Studio lo abre en",
                                                  [("Results", True), (", también sin", False)],
                                                  "el modelo"]),
        ],
    },
}

# New colours (not in palette.py), for the map swatches only. Same OKLCH terms as the tokens.
DEM_RAMP = [oklch_hex(L, 0.012, 250) for L in (0.93, 0.86, 0.78, 0.70, 0.62)]  # cool greys, ink hue
LAI_RAMP = [oklch_hex(0.90, 0.050, 135), color("canopy_light"), color("canopy_shade")]  # light leaf added
ALBEDO_RAMP = [color("slot_rock_even"), color("slot_rock_odd"), color("bedrock_hatch"), color("guide")]


def swatch(s, cx, top, kind, n=4, cell=6):
    """A small raster: n x n cells of one input map, drawn with the palette."""
    x0 = cx - n * cell / 2
    for i in range(n):
        for j in range(n):
            if kind == "dem":
                c = DEM_RAMP[min(4, (i + j) * 5 // (2 * n - 1))]
            elif kind == "lulc":
                c = [color("canopy_light"), color("canopy_shade"), color("slot_rock_odd"),
                     color("slot_near_surface")][((i // 2) * 2 + (j // 2) + (i == 3 and j == 0)) % 4]
            elif kind == "soil":
                c = [color("slot_near_surface"), color("slot_root_zone"), color("slot_transmission")][
                    (0 if i + j < 3 else 1) if j < 3 else 2]
            elif kind == "dtb":
                c = [color("deep_fill"), color("slot_wet_even"), color("slot_wet_odd")][min(2, (i + 2 * j) // 3)]
            elif kind == "lai":
                c = LAI_RAMP[2 - min(2, (i + j) // 2)]
            else:  # albedo
                c = ALBEDO_RAMP[min(3, (3 - i + j) // 2)]
            s.ax.add_patch(Rectangle((x0 + j * cell, top + i * cell), cell, cell, facecolor=c,
                                     edgecolor="none", zorder=4))
    s.ax.add_patch(Rectangle((x0, top), n * cell, n * cell, facecolor="none", edgecolor=color("guide"),
                             linewidth=0.6, zorder=5))


def heading(s, x, y, icon, label, *, size=10.5, icon_size=17, room=None):
    li.draw(s.ax, icon, x + icon_size / 2, y, icon_size, INK, lw=1.1)
    fk.text(s, x + icon_size + 7, y, label, bold=True, size=size, room=room)
    return x + icon_size + 7 + fk.width(s, label, bold=True, size=size)


def build(lang="en"):
    t = LABELS[lang]
    # Four card lines and three tile lines give the drafted 760 x 620 layout; dy is the
    # extra height of the input cards, which moves everything below them down.
    card_lines = max(len(t[k]) for k in ("tables_lines", "forcing_lines", "settings_lines"))
    dy = PITCH * (max(card_lines, 4) - 4)
    # The Run band is 50 px, or as tall as its rotated label needs; its two lines are centred.
    run_h = max(50.0, fk.width(None, t["band_run"], bold=True, size=10) + 12)
    dy_run = dy + run_h - 50
    out_lines = max(len(rows) for _, _, rows in t["out"])
    OUT_TOP = 520 + dy_run
    OUT_BOT = OUT_TOP + 40 + PITCH * (max(out_lines, 3) - 1) + 14
    s = Sheet(W, OUT_BOT + 12, NAME)
    X0, X1 = 60, 740

    # ---- 1 Inputs: a frame with the maps strip and three cards -------------------------
    F_TOP, F_BOT = 20, 278 + dy
    fk.panel(s, X0, F_TOP, X1 - X0, F_BOT - F_TOP, fill=color("slot_rock_even"), radius=9)
    fk.bracket(s, 44, F_TOP + 2, F_BOT - 2, t["band_inputs"])

    # Maps card.
    M_TOP, M_BOT = 30, 152
    fk.panel(s, 70, M_TOP, 660, M_BOT - M_TOP)
    xh = heading(s, 84, 48, "map", t["maps"])
    fk.text(s, xh + 12, 48, t["maps_sub"], c=SOFT, room=716 - xh - 12)
    groups = [(84, 352, t["required"], [140, 226, 312], ["dem", "lulc", "soil"]),
              (380, 716, t["optional"], [424, 512, 598, 676], ["dtb", "lai", "albedo", None])]
    for g0, g1, glabel, centres, kinds in groups:
        s.text((g0 + g1) / 2, 72, glabel, c=SOFT, ha="center")
        s.ax.plot([g0, g0, g1, g1], [86, 81, 81, 86], color=color("guide"), linewidth=0.8, zorder=3)
        for cx, kind in zip(centres, kinds):
            if kind:
                swatch(s, cx, 92, kind)
            else:
                li.draw(s.ax, "layers", cx, 104, 22, INK, lw=1.1)
    items = t["map_items"]
    for cx, rows in zip([140, 226, 312, 424, 512, 598, 676], items):
        for k, row in enumerate(rows):
            fk.text(s, cx, 128 + 15 * k, row, ha="center", room=None)

    # Three cards: parameter tables, forcing, settings.
    C_TOP, C_BOT = 162, 268 + dy
    cards = [(70, "table", t["tables"], t["tables_lines"]),
             (293, "cloud-rain", t["forcing"], t["forcing_lines"]),
             (516, "sliders-horizontal", t["settings"], t["settings_lines"])]
    for x, icon, label, rows in cards:
        fk.panel(s, x, C_TOP, 214, C_BOT - C_TOP)
        heading(s, x + 14, C_TOP + 18, icon, label, room=214 - 45)
        fk.lines(s, x + 14, C_TOP + 41, rows, room=214 - 26)

    # ---- bus from the inputs to the two forms of the case --------------------------------
    BUS1 = 296 + dy
    L_C, R_C = 225, 575  # lane centres
    fk.line(s, [(400, F_BOT), (400, BUS1)])
    fk.line(s, [(L_C, BUS1), (R_C, BUS1)])
    fk.dot(s, 400, BUS1)
    CASE_TOP, CASE_BOT = 318 + dy, 406 + dy
    for xc in (L_C, R_C):
        fk.line(s, [(xc, BUS1 - fk.LINE_PT / 2), (xc, BUS1 + 2)])
        fk.arrow(s, (xc, BUS1), (xc, CASE_TOP))

    # ---- 2 One case -----------------------------------------------------------------------
    fk.bracket(s, 44, CASE_TOP + 2, CASE_BOT - 2, t["band_case"])
    for x0, icon, label, rows in ((X0, "app-window", t["studio"], t["studio_lines"]),
                                  (410, "file-spreadsheet", t["matlab"], t["matlab_lines"])):
        fk.panel(s, x0, CASE_TOP, 330, CASE_BOT - CASE_TOP, fill=color("deep_fill"), edge=WATER)
        heading(s, x0 + 14, CASE_TOP + 18, icon, label)
        fk.lines(s, x0 + 14, CASE_TOP + 40, rows, room=330 - 28)
    s.text(400, (CASE_TOP + CASE_BOT) / 2, t["or"], c=SOFT, ha="center")

    # ---- 3 Run ----------------------------------------------------------------------------
    RUN_TOP = 430 + dy
    RUN_BOT = RUN_TOP + run_h
    row1, row2 = (RUN_TOP + RUN_BOT) / 2 - 9, (RUN_TOP + RUN_BOT) / 2 + 9
    for xc in (L_C, R_C):
        fk.arrow(s, (xc, CASE_BOT), (xc, RUN_TOP))
    fk.bracket(s, 44, RUN_TOP + 2, RUN_BOT - 2, t["band_run"])
    for x0, label, rows in ((X0, t["run_studio"], t["run_studio_lines"]),
                            (410, t["run_matlab"], t["run_matlab_lines"])):
        fk.panel(s, x0, RUN_TOP, 330, RUN_BOT - RUN_TOP)
        xh = heading(s, x0 + 14, row1, "play", label)
        fk.lines(s, xh + 12, row1, rows[:1], room=x0 + 330 - 14 - xh - 12)
        fk.lines(s, x0 + 14, row2, rows[1:], room=330 - 28)

    # ---- bus from both runs to the outputs ----------------------------------------------
    BUS2 = RUN_BOT + 18
    tiles_x = [60 + sum(TILE_W[:k]) + 8 * k for k in range(4)]
    centres = [x + w / 2 for x, w in zip(tiles_x, TILE_W)]
    for xc in (L_C, R_C):
        fk.line(s, [(xc, RUN_BOT), (xc, BUS2)])
        fk.dot(s, xc, BUS2)
    fk.line(s, [(centres[0], BUS2), (centres[-1], BUS2)])
    for xc in centres:
        fk.arrow(s, (xc, BUS2), (xc, OUT_TOP))

    # ---- 4 Outputs ------------------------------------------------------------------------
    fk.bracket(s, 44, OUT_TOP + 2, OUT_BOT - 2, t["band_outputs"])
    for x0, tile_w, (icon, label, rows) in zip(tiles_x, TILE_W, t["out"]):
        fk.panel(s, x0, OUT_TOP, tile_w, OUT_BOT - OUT_TOP)
        heading(s, x0 + 12, OUT_TOP + 18, icon, label, size=10, room=tile_w - 40)
        fk.lines(s, x0 + 12, OUT_TOP + 40, rows, room=tile_w - 22)
    return s


def write_icon_log(path: Path) -> None:
    """The licence log; the icon files are named from the repository root."""
    li.write_licence_log(path)


def main(preview: Path | None = None) -> None:
    for lang in LABELS:
        svg = build(lang).save(STATIC / SECTION, lang, preview)
        print("wrote", svg.relative_to(STATIC.parent.parent))
    write_icon_log(HERE / "data_to_results_icons.csv")


if __name__ == "__main__":
    main(Path(sys.argv[1]) if len(sys.argv) > 1 else None)


# Sources (docs pages), one per element of the figure.
FACTS = {
    "required maps DEM, LULC, soil": "inputs/overview; configuration/general_data",
    "optional maps DTB, LAI, albedo, additional": "inputs/overview",
    "GeoTIFF, projected CRS, aligned with the DEM": "configuration/general_data; inputs/overview",
    "parameter tables, one row per class code": "getting-started/excel-workflow; inputs/parameter-tables",
    "forcing pathways": "inputs/optional-forcing; inputs/overview; studio/building-a-model",
    "settings: processes, routing solver, time step, period, output intervals":
        "configuration/overview; studio/building-a-model; configuration/general_data",
    "Studio model file case.yaml": "studio/overview; studio/working-in-studio",
    "New model wizard downloads the data": "studio/building-a-model",
    "MATLAB workbook HydroPol2D_Inputs.xlsx, its tabs, map paths":
        "getting-started/excel-workflow; configuration/overview",
    "Studio run: Check inputs, Run model, CPU": "studio/run-and-results; studio/overview",
    "MATLAB run writes an output folder": "getting-started/excel-workflow",
    "maps: depth, water-surface elevation, groundwater, map interval":
        "configuration/general_data; studio/run-and-results",
    "time series: hydrographs, gauges, water balance":
        "configuration/general_data; studio/run-and-results",
    "animations, MP4": "studio/run-and-results; getting-started/model-building-workflow",
    "results package opens in Results without the model": "studio/overview; studio/run-and-results",
}
