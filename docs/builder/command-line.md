---
title: Command line
---

# Command line

The app is also the Case Builder's command line, `hydropol-case`, for scripts and batches of
cases. It uses the same license code and the same cache as the app.

| Computer | Command |
|---|---|
| Mac | `"/Applications/HydroPol2D Case Builder.app/Contents/MacOS/HydroPol2D Case Builder"` |
| Windows | `hydropol-case.exe`, in the folder where you unzipped the app |

On a Mac, a short name saves typing. Add this line to `~/.zshrc`, then open a new Terminal:

```bash
alias hydropol-case='"/Applications/HydroPol2D Case Builder.app/Contents/MacOS/HydroPol2D Case Builder"'
```

The examples below use `hydropol-case`.

## Commands {#commands}

| Command | What it does |
|---|---|
| `hydropol-case urban` | an Urban Basin case |
| `hydropol-case urban-only` | an Urban Area Only case |
| `hydropol-case catchment` | a Catchment case |
| `hydropol-case preflight CASE_DIR` | checks a prepared case. Prints `Ready to run: True` or the list of problems. |
| `hydropol-case license status` | shows who the stored license is for and how many days are left |
| `hydropol-case license activate` | checks a code and stores it (it asks for the code when you leave it out) |

`hydropol-case urban --help` and the same for the other commands list every option.

## Preview first {#preview-first}

`--plan-only` stops after the preview: it delineates the domain, writes `case.json`, `domain.gpkg`
and the preview maps, and prints the size of the case. This Catchment preview of San Francisquito
Creek takes a few seconds:

```bash
hydropol-case catchment \
  --name "San Francisquito Creek" \
  --outlet-lon -122.1889 --outlet-lat 37.4239 \
  --resolution 30 \
  --start "2023-01-08 00:00" --end "2023-01-10 00:00" --warmup-days 0 \
  --rainfall aorc \
  --configure-hydropol matlab \
  --riverbed-hydraulic-conductivity-m-s 1e-6 \
  --plan-only
```

It prints, among other lines:

```text
Domain area: 107.8 km2
Matrix: 523 rows x 422 columns (220,706 cells)
Estimated active cells: 119,737
Temporary source-transfer ceiling: 2.8 MiB
Estimated retained forcing inputs: 0.1 MiB
Case directory: /…/outputs/san_francisquito_creek_candidate1_30m_20230108
```

Open `figures/domain_preview.html` in the case folder to see the domain on a map.

## Prepare the case {#prepare}

Run the same command without `--plan-only`. It shows the preview again and asks
`Continue preparing this case? [y/N]`. Answer `y` after you have read the size. `--yes` skips the
question, for scripts whose domain you have already reviewed. A complete case ends with:

```text
Complete HydroPol2D input package created and accepted by preflight.
```

This Urban Area Only case of Tucson, Arizona, on 250 m cells, for one day with AORC rain and
models for both Python and MATLAB, was prepared with:

```bash
hydropol-case urban-only \
  --city Tucson --country "United States" \
  --resolution 250 \
  --start "2021-07-23 00:00" --end "2021-07-24 00:00" --warmup-days 0 \
  --rainfall aorc \
  --configure-hydropol both \
  --dem-source fabdem \
  --riverbed-hydraulic-conductivity-m-s 1e-6 \
  --yes
```

The **Python and command line** tab of the app shows the command for the current settings of the
**Urban Basin** tab, with every option written out. Copy it to repeat a case from a script.

## Defaults that differ from the app {#defaults}

| Option | Command line | App |
|---|---|---|
| `--warmup-days` | 30 | 0 |
| `--configure-hydropol` | `none` (inputs only) | HydroPol2D Python |
| `--dem-source` | `copernicus_glo30` | FABDEM |
| `--output-dir` | `outputs` in the current folder | `Documents/HydroPol2D Case Builder/outputs` |

With river-groundwater exchange on (the default), give `--riverbed-hydraulic-conductivity-m-s`,
which stands for the app's confirmation box. `--no-river-groundwater-exchange` or
`--no-groundwater` turn the exchange off.

## Options {#options}

The most used options. All dates are UTC.

| Option | What it sets |
|---|---|
| `--city NAME --country COUNTRY` | a GHSL city (urban and urban-only) |
| `--polygon PATH` | your own polygon (urban and urban-only), or a catchment or search polygon (catchment, with `--polygon-mode exact` or `search`) |
| `--name NAME` | the case name (catchment) |
| `--outlet-lon`, `--outlet-lat` | the outlet in degrees (catchment) |
| `--outlet-point PATH` | a vector file with one outlet point (catchment) |
| `--candidate-rank 1\|2\|3` | the outlet candidate (catchment, default 1) |
| `--snap-radius-km`, `--outlet-cells` | snap radius and critical outlet cells (catchment) |
| `--resolution METRES` | the cell size (required) |
| `--grid-mode uniform\|quadtree` | the grid type (urban and urban-only) |
| `--coarse-resolution`, `--urban-refinement-buffer` | the quadtree coarse cell size and fine-grid buffer |
| `--start`, `--end`, `--warmup-days` | the period (start and end required) |
| `--rainfall PRODUCT` | `imerg`, `era5`, `mswep-hourly`, `mswep-3hourly` or `aorc` (required) |
| `--configure-hydropol MODE` | `python`, `matlab`, `both` or `none` |
| `--dem-source SOURCE` | `fabdem`, `local` (with `--source-dem PATH`), `usgs_3dep` (United States, 10 m) or `copernicus_glo30` |
| `--river-area-km2 AREA` | the river initiation area (default 5) |
| `--subgrid-method`, `--hydraulic-table-coverage` | the river representation: `auto`, `neal`, `hydraulic_tables` or `none`, and `rivers` or `all` |
| `--no-canopy-interception`, `--no-infiltration`, `--no-groundwater`, `--no-evapotranspiration` | leave a process out |
| `--deep-aquifer` and the `--deep-...` options | the deep-aquifer baseflow (catchment) |
| `--groundwater-parameter-source`, `--groundwater-ksat-h-m-s`, `--groundwater-specific-yield` | the shallow-aquifer parameters (`spatial`, `uniform` or `calibration`) |
| `--urban-buffer-km`, `--glofas-inflow`, `--coastal-tide`, `--tide-datum-offset-m`, `--groundwater-boundary` | the urban boundary conditions (urban-only) |
| `--output-profile`, `--map-output-interval-minutes`, `--diagnostic-output-interval-minutes`, `--output-map-variable` | the saved outputs |
| `--rainfall-source-dir PATH` | rainfall files you already have |
| `--mswep-rclone-source`, `--mswep-rclone-root-folder-id` | the MSWEP folder |
| `--output-dir`, `--cache-dir` | the case and cache folders |
| `--plan-only`, `--yes` | stop after the preview, or skip the question |

The command line has a few options the app does not show, among them:

| Option | What it sets |
|---|---|
| `--land-cover worldcover\|nlcd` | ESA WorldCover (global, default) or USGS NLCD 2021 with imperviousness (lower 48 states) |
| `--snow`, `--water-quality`, `--human-risk` | snow, pollutant build-up and wash-off, and flood danger to people (HydroPol2D Python) |
| `--layer NAME=PATH` | your own raster for one layer: `lulc`, `soil`, `depth_to_bedrock`, `groundwater_table`, `impervious_fraction`, `lai`, `initial_soil_moisture`, `initial_swe` or `initial_snow_depth` (repeat for more) |
| `--refinement-polygon PATH`, `--river-corridor` | quadtree: refine around another polygon, or keep rivers and their floodplain at the fine size |
| `--rainfall dataset --rainfall-dataset PATH` | rainfall from a NetCDF or Zarr file (with `--rainfall-interval-minutes`) |
| `--rainfall meteostat` | hourly Meteostat station rainfall, kept as rain gauges (HydroPol2D Python) |
| `--meteorology-source era5\|meteostat\|dataset` | the weather source |
| `--imerg-run final\|late\|auto` | the IMERG run (default `final`) |

## Exit codes {#exit-codes}

`0` when the command succeeded (for `preflight`, when the case is ready), `2` when the case is not
ready, the request has an error, or the license is missing or not valid. In a terminal, a missing
license makes the command ask for the code once.
