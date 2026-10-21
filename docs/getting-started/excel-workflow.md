---
title: Run from Excel
---

# Run HydroPol2D from Excel

In Excel mode, a whole MATLAB case lives in one workbook, `HydroPol2D_Inputs.xlsx`: every setting, the class tables and the time series. Bypass mode reads the same settings from MATLAB files under `Config/`. Both use the same numerical solver.

## Start with the tested example {#start-with-the-tested-example}

The repository includes a small V-tilted case. Its workbook is `Examples/VTilted_Excel/Input_Data_Sheets/HydroPol2D_Inputs.xlsx`. Open MATLAB in the HydroPol2D repository and run:

```matlab
run('Examples/VTilted_Excel/run_excel.m')
```

The launcher reads `flag_voronoi` (Surface flow tab) and writes the results to `Examples/VTilted_Excel/Outputs/regular` or `Examples/VTilted_Excel/Outputs/voronoi`. To run the prepared Voronoi mesh, change `flag_voronoi` from `0` to `1` in the same workbook. Do not make a second workbook.

## The case workbook {#the-case-workbook}

| Tabs | Content |
|---|---|
| Start here | How to fill the workbook, the colour legend and a link to every tab |
| Run control, Input maps, Soil and groundwater, Surface flow, Rain and ET, Design storm, Water quality, Risk and gauges | Every setting, one row each, with a note on each value. A block greys out while its switch is 0. |
| Soil classes, Land use classes, Human instability, Mesh, Control structures | The class tables |
| Rain series, Rain gauges, Climate stations, Inflow hydrographs, Stage hydrographs | The time series |

The class-table and series tabs keep the cell layout of the workbooks they replace, because the model reads some of them by position. Keep their rows and columns where they are. A sheet holds up to 1,048,576 rows, which is two years of 1-min data.

The settings are listed on [Case Workbook Settings](../configuration/general_data), the switches on [Model Flags](../configuration/flags), the class tables on [Parameter Tables](../inputs/parameter-tables) and the series on [Optional Forcing](../inputs/optional-forcing).

## Fill a case {#fill-a-case}

1. **Start here.** Read the colour legend: a grey row is switched off, a grey block is advanced (keep its defaults) and an amber block is paused (keep it at 0).
2. **Settings tabs.** Turn processes on or off with the switch at the top of each block. A red asterisk marks a required value. An empty optional value keeps its default; the note on each value says which.
3. **Class tables.** Give one row per class code of the land-use and soil maps. A valid code that is missing from a table gets the area-weighted mean of the mapped classes, and the decision is written to `Input_Class_Code_Audit.csv`.
4. **Series.** Fill only the series that your switches read. The others can stay as empty templates with their headers.
5. **Paths.** Raster and file paths can be absolute or relative to the folder of the workbook.

## Regular grid or Voronoi mesh {#regular-grid-or-voronoi-mesh}

`flag_voronoi` (Surface flow tab, Unstructured mesh block) selects the mesh.

| `flag_voronoi` | Mesh |
|---|---|
| `0` | Raster grid built from the DEM, land-use and soil maps |
| `1` | A prepared case file, named in the Mesh tab, that references the UGRID mesh and raster-overlap files made by HydroBathyDEM |

The Mesh tab settings must match the metadata stored in the UGRID file. HydroPol2D checks background width, minimum width, adjacent-size ratio, urban width, transition buffer and unresolved-river policy before the run, so a workbook cannot silently run a different mesh. Excel selects a prepared mesh; it does not generate or modify it during a run. The MATLAB Voronoi runner is CPU-only.

## Run any workbook without editing the launcher {#run-any-workbook-without-editing-the-launcher}

`HydroPol2D_V115.m` reads `Input_Data_Sheets/HydroPol2D_Inputs.xlsx` by default. To run another case, set the paths in MATLAB and run the normal launcher:

```matlab
setenv('HYDROPOL_RUN_MODE','excel')
setenv('HYDROPOL_INPUT_EXCEL_FILE','/absolute/path/to/HydroPol2D_Inputs.xlsx')
setenv('HYDROPOL_EXPORT_ROOT_DIR','/absolute/path/to/Outputs/my_run')
setenv('HYDROPOL_SKIP_POSTPROCESS','')
run('HydroPol2D_V115.m')
```

Set `HYDROPOL_SKIP_POSTPROCESS` to `1` for a solver-only diagnostic run. Leave it empty for the normal full run.

## Convert an older case {#convert-an-older-case}

From `tools/workbook_builder` in the MATLAB repository:

```bash
python build_input_workbook.py input_catalog.yaml General_Data.xlsx HydroPol2D_Inputs.xlsx
```

The builder carries every value, map path, map list and gauge over, and copies the class tables and series from the workbooks next to the source. The V-tilted case gives identical results from the converted workbook and from the older files (`Validation/Workbook/run_single_workbook_checks.m`).

## Older layout {#older-layout}

Cases made before 2026-10-20 use `General_Data.xlsx` with its `Flags` sheet and separate workbooks (`SOIL_parameters.xlsx`, `LULC_parameters.xlsx`, `Rainfall_Intensity_Data.xlsx` and the others). They still run unchanged:

- `HydroPol2D_V115.m` uses `General_Data.xlsx` when the input folder has no `HydroPol2D_Inputs.xlsx`, or the file that `HYDROPOL_INPUT_EXCEL_FILE` names.
- Each reader takes its tab from the case workbook when the case has one, and the older workbook otherwise.
- Keep the companion workbooks in the same folder as `General_Data.xlsx`. Relative paths are resolved from that folder.

## Configure with MATLAB files instead {#configure-with-matlab-files-instead}

For scripted studies, ensembles, or configuration tracked line by line in Git, use bypass mode:

1. Set `run_mode = 'bypass'` in `HydroPol2D_V115.m`.
2. Set process and numerical controls in `Config/input_data_bypass_script.m`.
3. Set raster and forcing paths in `Config/input_paths_bypass.m`.
4. Run `HydroPol2D_V115.m`.

The V-tilted example has its own code configuration: `addpath('Examples/VTilted_Excel')`, then `run_code('regular')` or `run_code('voronoi')`.

Use Excel mode when a workbook is the most convenient project record. Use bypass mode when the configuration should be generated or reviewed as code.
