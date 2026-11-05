---
title: Línea de comandos
---

# Línea de comandos

La app es también la línea de comandos del Case Builder, `hydropol-case`, para scripts y lotes de
casos. Usa el mismo código de licencia y la misma caché que la app.

| Computadora | Comando |
|---|---|
| Mac | `"/Applications/HydroPol2D Case Builder.app/Contents/MacOS/HydroPol2D Case Builder"` |
| Windows | `hydropol-case.exe`, en la carpeta donde descomprimió la app |

En un Mac, un nombre corto ahorra escritura. Agregue esta línea a `~/.zshrc` y luego abra una
Terminal nueva:

```bash
alias hydropol-case='"/Applications/HydroPol2D Case Builder.app/Contents/MacOS/HydroPol2D Case Builder"'
```

Los ejemplos de abajo usan `hydropol-case`.

## Comandos {#commands}

| Comando | Qué hace |
|---|---|
| `hydropol-case urban` | un caso Urban Basin |
| `hydropol-case urban-only` | un caso Urban Area Only |
| `hydropol-case catchment` | un caso Catchment |
| `hydropol-case preflight CASE_DIR` | verifica un caso preparado. Imprime `Ready to run: True` o la lista de problemas. |
| `hydropol-case license status` | muestra a quién pertenece la licencia guardada y cuántos días quedan |
| `hydropol-case license activate` | verifica un código y lo guarda (pide el código cuando no se indica) |

`hydropol-case urban --help`, y lo mismo con los demás comandos, lista todas las opciones.

## Primero la vista previa {#preview-first}

`--plan-only` se detiene después de la vista previa: delimita el dominio, escribe `case.json`,
`domain.gpkg` y los mapas de vista previa, e imprime el tamaño del caso. Esta vista previa Catchment
de San Francisquito Creek tarda unos segundos:

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

Imprime, entre otras líneas:

```text
Domain area: 107.8 km2
Matrix: 523 rows x 422 columns (220,706 cells)
Estimated active cells: 119,737
Temporary source-transfer ceiling: 2.8 MiB
Estimated retained forcing inputs: 0.1 MiB
Case directory: /…/outputs/san_francisquito_creek_candidate1_30m_20230108
```

Abra `figures/domain_preview.html` en la carpeta del caso para ver el dominio en un mapa.

## Preparar el caso {#prepare}

Ejecute el mismo comando sin `--plan-only`. Muestra otra vez la vista previa y pregunta
`Continue preparing this case? [y/N]`. Responda `y` después de leer el tamaño. `--yes` omite la
pregunta, para scripts cuyo dominio ya revisó. Un caso completo termina con:

```text
Complete HydroPol2D input package created and accepted by preflight.
```

Este caso Urban Area Only de Tucson, Arizona, en celdas de 250 m, para un día con lluvia de AORC y
modelos para Python y MATLAB, se preparó con:

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

La pestaña **Python and command line** de la app muestra el comando para los ajustes actuales de la
pestaña **Urban Basin**, con todas las opciones escritas. Cópielo para repetir un caso desde un
script.

## Valores por defecto que difieren de la app {#defaults}

| Opción | Línea de comandos | App |
|---|---|---|
| `--warmup-days` | 30 | 0 |
| `--configure-hydropol` | `none` (solo entradas) | HydroPol2D Python |
| `--dem-source` | `copernicus_glo30` | FABDEM |
| `--output-dir` | `outputs` en la carpeta actual | `Documents/HydroPol2D Case Builder/outputs` |

Con el intercambio río-agua subterránea activado (el valor por defecto), indique
`--riverbed-hydraulic-conductivity-m-s`, que equivale a la casilla de confirmación de la app.
`--no-river-groundwater-exchange` o `--no-groundwater` desactivan el intercambio.

## Opciones {#options}

Las opciones más usadas. Todas las fechas están en UTC.

| Opción | Qué define |
|---|---|
| `--city NAME --country COUNTRY` | una ciudad de GHSL (urban y urban-only) |
| `--polygon PATH` | su propio polígono (urban y urban-only), o un polígono de cuenca o de búsqueda (catchment, con `--polygon-mode exact` o `search`) |
| `--name NAME` | el nombre del caso (catchment) |
| `--outlet-lon`, `--outlet-lat` | la salida en grados (catchment) |
| `--outlet-point PATH` | un archivo vectorial con un punto de salida (catchment) |
| `--candidate-rank 1\|2\|3` | la salida candidata (catchment, por defecto 1) |
| `--snap-radius-km`, `--outlet-cells` | el radio de ajuste y las celdas de salida críticas (catchment) |
| `--resolution METRES` | el tamaño de celda (obligatorio) |
| `--grid-mode uniform\|quadtree` | el tipo de malla (urban y urban-only) |
| `--coarse-resolution`, `--urban-refinement-buffer` | el tamaño de celda grueso y la franja de malla fina de la malla quadtree |
| `--start`, `--end`, `--warmup-days` | el periodo (inicio y fin obligatorios) |
| `--rainfall PRODUCT` | `imerg`, `era5`, `mswep-hourly`, `mswep-3hourly` o `aorc` (obligatorio) |
| `--configure-hydropol MODE` | `python`, `matlab`, `both` o `none` |
| `--dem-source SOURCE` | `fabdem`, `local` (con `--source-dem PATH`), `usgs_3dep` (Estados Unidos, 10 m) o `copernicus_glo30` |
| `--river-area-km2 AREA` | el área de inicio de los ríos (por defecto 5) |
| `--subgrid-method`, `--hydraulic-table-coverage` | la representación de los ríos: `auto`, `neal`, `hydraulic_tables` o `none`, y `rivers` o `all` |
| `--no-canopy-interception`, `--no-infiltration`, `--no-groundwater`, `--no-evapotranspiration` | dejar fuera un proceso |
| `--deep-aquifer` y las opciones `--deep-...` | el flujo base del acuífero profundo (catchment) |
| `--groundwater-parameter-source`, `--groundwater-ksat-h-m-s`, `--groundwater-specific-yield` | los parámetros del acuífero somero (`spatial`, `uniform` o `calibration`) |
| `--urban-buffer-km`, `--glofas-inflow`, `--coastal-tide`, `--tide-datum-offset-m`, `--groundwater-boundary` | las condiciones de contorno urbanas (urban-only) |
| `--output-profile`, `--map-output-interval-minutes`, `--diagnostic-output-interval-minutes`, `--output-map-variable` | las salidas guardadas |
| `--rainfall-source-dir PATH` | archivos de lluvia que usted ya tiene |
| `--mswep-rclone-source`, `--mswep-rclone-root-folder-id` | la carpeta de MSWEP |
| `--output-dir`, `--cache-dir` | las carpetas del caso y de la caché |
| `--plan-only`, `--yes` | detenerse después de la vista previa, u omitir la pregunta |

La línea de comandos tiene algunas opciones que la app no muestra, entre ellas:

| Opción | Qué define |
|---|---|
| `--land-cover worldcover\|nlcd` | ESA WorldCover (global, por defecto) o USGS NLCD 2021 con impermeabilidad (los 48 estados contiguos) |
| `--snow`, `--water-quality`, `--human-risk` | la nieve, la acumulación y el lavado de contaminantes, y el peligro de la inundación para las personas (HydroPol2D Python) |
| `--layer NAME=PATH` | su propio ráster para una capa: `lulc`, `soil`, `depth_to_bedrock`, `groundwater_table`, `impervious_fraction`, `lai`, `initial_soil_moisture`, `initial_swe` o `initial_snow_depth` (repita la opción para más capas) |
| `--refinement-polygon PATH`, `--river-corridor` | quadtree: refinar alrededor de otro polígono, o mantener los ríos y su llanura de inundación con el tamaño fino |
| `--rainfall dataset --rainfall-dataset PATH` | lluvia de un archivo NetCDF o Zarr (con `--rainfall-interval-minutes`) |
| `--rainfall meteostat` | lluvia horaria de estaciones Meteostat, conservada como pluviómetros (HydroPol2D Python) |
| `--meteorology-source era5\|meteostat\|dataset` | la fuente del clima |
| `--imerg-run final\|late\|auto` | la ejecución (run) de IMERG (por defecto `final`) |

## Códigos de salida {#exit-codes}

`0` cuando el comando terminó bien (para `preflight`, cuando el caso está listo), `2` cuando el caso
no está listo, la solicitud tiene un error o la licencia falta o no es válida. En una terminal, si
falta la licencia, el comando pide el código una vez.
