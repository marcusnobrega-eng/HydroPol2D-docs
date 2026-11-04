---
title: Mapas de entrada y forzantes de HP2D con Python
# Hidden until Marcus has run the script once in Earth Engine (checklist in the Pile B report).
draft: true
---

# Mapas de entrada y lluvia con Google Earth Engine (Python)

Este script arma los mapas de entrada de un caso de HydroPol2D con Google Earth Engine (GEE). Recorta cada
conjunto de datos al área del caso, pone todos los mapas en una misma grilla, en el sistema de coordenadas
proyectado del caso, y exporta los mapas, dos tablas resumen y los mapas de lluvia a Google Drive.

---

## Qué hace el script

- Define el área del caso a partir de un rectángulo, de un asset de polígono o de cuencas de HydroBASINS.
- Arma una grilla del modelo: el CRS proyectado del caso, un tamaño de celda en metros y una esquina alineada a
  ese tamaño. Todos los mapas salen en esa grilla, así que coinciden celda por celda.
- Exporta los mapas de terreno, uso del suelo, suelo, vegetación, fracción impermeable y población.
- Exporta la humedad inicial del suelo al inicio del evento, como contenido volumétrico de agua.
- Exporta la lluvia de GPM IMERG, promediada en el paso de tiempo elegido y remuestreada a la grilla del modelo.
- Escribe una tabla del dominio y una de las cuencas, con promedios, totales y clases dominantes.

---

## Conjuntos de datos

| Mapa | Conjunto de datos (ID en GEE) | Celda original |
|---|---|---|
| Elevación | MERIT DEM (`MERIT/DEM/v1_0_3`) | 90 m |
| Uso y cobertura del suelo | ESA WorldCover 2020 (`ESA/WorldCover/v100/2020`) | 10 m |
| Clase textural del suelo | Clase textural USDA de OpenLandMap (`OpenLandMap/SOL/SOL_TEXTURE-CLASS_USDA-TT_M/v02`) | 250 m |
| Índice de área foliar | MODIS MCD15A3H (`MODIS/061/MCD15A3H`) | 500 m |
| Albedo | MODIS MCD43A3 (`MODIS/061/MCD43A3`) | 500 m |
| Fracción impermeable | Superficie construida GHSL 2020 (`JRC/GHSL/P2023A/GHS_BUILT_S/2020`) | 100 m |
| Población | WorldPop (`WorldPop/GP/100m/pop`) | 100 m |
| Humedad inicial del suelo | ERA5-Land horario (`ECMWF/ERA5_LAND/HOURLY`) | 11 km |
| Lluvia | GPM IMERG V07 (`NASA/GPM_L3/IMERG_V07`) | 11 km |

No hay un conjunto público en GEE para la profundidad hasta la roca con esta resolución. Indique su asset en
`DTB_ASSET`, o déjelo en `None` y ese mapa no se exporta.

---

## Salidas

Todos los mapas son GeoTIFF en la grilla del modelo, con `-9999` fuera del área del caso.

| Archivo | Contenido | Unidad |
|---|---|---|
| `DEM.tif` | Elevación | m |
| `LULC.tif` | Clase de ESA WorldCover | código de clase |
| `SOIL.tif` | Clase textural USDA (1–12) | código de clase |
| `LAI.tif` | Índice de área foliar | m²/m² |
| `Albedo.tif` | Albedo de onda corta (black-sky) | – |
| `Impervious_Fraction.tif` | Parte construida de cada celda | 0–1 |
| `Population_Density.tif` | Personas por km² | personas/km² |
| `Initial_Soil_Moisture_theta.tif` | Contenido volumétrico de agua, promedio en los primeros `SOIL_DEPTH_M` | m³/m³ |
| `DTB.tif` (opcional) | Profundidad hasta la roca | m |
| `GPM_<paso>min_<aaaa_MM_dd_HH_mm>.tif`, en la carpeta `<FOLDER_NAME>_Rainfall_Rasters` | Intensidad media de la lluvia en cada paso, con el nombre del inicio del paso | mm/h |
| `Domain_Log.csv`, `Catchment_Log.csv` | Área, población, porcentaje impermeable medio, clases dominantes, promedios | – |
| `Case_Area.shp` | El área del caso | – |

Los mapas categóricos (uso del suelo, suelo) toman la clase más frecuente cuando la celda de origen es menor que
la del modelo. Los mapas continuos toman el promedio cuando la celda de origen es menor, e interpolación bilineal
cuando es mayor.

### Unidades que leen los dos modelos

- **Humedad inicial del suelo.** HydroPol2D (Python) lee `Initial_Soil_Moisture_theta.tif` directamente como θ.
  HydroPol2D en MATLAB lee `Initial_Soil_Moisture_path` como el agua almacenada por encima del contenido
  residual, en mm: I₀ = (θ − θr) × profundidad del suelo × 1000. Convierta el mapa con el fragmento en
  [Para MATLAB: humedad del suelo en mm](#para-matlab-humedad-del-suelo-en-mm).
- **Fracción impermeable.** GHSL da la superficie construida en m² por celda de 100 m. El script divide por el
  área de la celda (10 000 m²), así que el mapa es una fracción de 0 a 1.
- **Población.** WorldPop da personas por celda de 100 m. El script divide por el área de la celda, así que el
  mapa es una densidad en personas por km² y no depende del tamaño de celda del modelo.
- **Lluvia.** La banda `precipitation` de IMERG está en mm/h. Cada mapa exportado es la intensidad media de su paso.

---

## Ajustes

| Ajuste | Significado |
|---|---|
| `PROJECT_ID` | Su proyecto de Earth Engine |
| `CASE_BBOX`, `CASE_ASSET`, `HYBAS_LEVEL`, `HYBAS_IDS` | El área del caso. Se usa la primera que esté definida. |
| `CRS` | El CRS proyectado del caso, por ejemplo `"EPSG:3310"` o una zona UTM. `None` elige la zona UTM del centro del caso. |
| `SCALE` | Tamaño de celda del modelo, en metros |
| `STATIC_START`, `STATIC_END` | Período de las medianas de LAI y albedo |
| `EVENT_START`, `EVENT_END` | Período de la lluvia. La humedad del suelo se toma en `EVENT_START`. |
| `RAIN_STEP_MIN` | Paso de tiempo de la lluvia, en minutos (30 o un múltiplo de 30) |
| `SOIL_DEPTH_M` | Profundidad en la que se promedia θ |
| `WORLDPOP_YEAR` | Año de WorldPop |

Use el CRS y el tamaño de celda de su caso de HydroPol2D, para que los mapas exportados coincidan con los mapas
que ya tiene.

---

## Cómo ejecutarlo

1. Instale la API de Earth Engine e inicie sesión una vez:

   ```bash
   pip install earthengine-api
   ```

   ```bash
   earthengine authenticate
   ```

2. Guarde el script de abajo como `HP2D_Inputs.py` y ajuste `PROJECT_ID`, el área del caso, `CRS`, `SCALE` y las fechas.
3. Ejecútelo:

   ```bash
   python HP2D_Inputs.py
   ```

4. El script inicia todas las exportaciones y muestra su estado cada minuto hasta que terminan. Los mapas y las
   tablas van a la carpeta `FOLDER_NAME` de Google Drive, y los mapas de lluvia a `FOLDER_NAME_Rainfall_Rasters`
   (Earth Engine no escribe en subcarpetas).

Las áreas grandes y los períodos largos de lluvia tardan más, y Earth Engine limita cuántas exportaciones corren
a la vez.

---

## Cómo usar los mapas en HydroPol2D

- **Python (Studio o un archivo de caso).** Apunte `static.dem_path`, `lulc_path`, `soil_path`, `lai_path`,
  `impervious_fraction_path`, `initial_soil_moisture_path` y `depth_to_bedrock_path` a los archivos. Python no lee
  albedo. Los mapas de lluvia van en `forcing.rainfall_raster_mm_h_series`, una entrada por archivo con su inicio
  en segundos (`time_s`).
- **MATLAB.** Ponga las rutas en la pestaña **Input maps** (el DTB va en **Soil and groundwater**). Liste los
  mapas de lluvia en la pestaña **Rain and ET** (tiempo en minutos desde el inicio de la simulación, luego la ruta
  del archivo) y use `flag_input_rainfall_map = 1`. Use el mapa de humedad convertido (abajo) como
  `Initial_Soil_Moisture_path`, con `flag_initial_soil_moisture = 1`.

### Para MATLAB: humedad del suelo en mm

Ejecute esto en su computadora después de la descarga. Tome el θr de cada clase de suelo de su tabla
`SOIL_parameters` y la profundidad de suelo que usa su caso en MATLAB.

```python
import numpy as np
import rasterio

THETA_R = {1: 0.090, 2: 0.068, 3: 0.075}  # theta_r of each SOIL class code, from your soil table
SOIL_DEPTH_M = 1.0                        # soil depth of the MATLAB case
NODATA = -9999

with rasterio.open("SOIL.tif") as soil_file, rasterio.open("Initial_Soil_Moisture_theta.tif") as theta_file:
    soil = soil_file.read(1)
    theta = theta_file.read(1).astype("float64")
    profile = theta_file.profile

theta_r = np.full(theta.shape, np.nan)
for code, value in THETA_R.items():
    theta_r[soil == code] = value
storage_mm = np.clip(theta - theta_r, 0.0, None) * SOIL_DEPTH_M * 1000.0
storage_mm[(theta == NODATA) | np.isnan(theta_r)] = NODATA

profile.update(dtype="float32", nodata=NODATA)
with rasterio.open("Initial_Soil_Moisture_I0_mm.tif", "w", **profile) as out:
    out.write(storage_mm.astype("float32"), 1)
```

---

## Limitaciones

- GPM IMERG y ERA5-Land tienen celdas de 11 km. Remuestrearlos a una grilla de 30 m da mapas suaves, no más
  detalle. En una cuenca pequeña, la lluvia de pluviómetros suele ser mejor.
- La humedad del suelo de ERA5-Land viene de un modelo de superficie, no de observaciones.
- MERIT DEM tiene celdas de 90 m. Para un caso más fino, use un DEM más fino (en Estados Unidos, `USGS/3DEP/10m`).

---

## Script

```python
import math
import time

import ee

# -----------------------------------------------------------------------------
# SETTINGS
# -----------------------------------------------------------------------------
PROJECT_ID = "your-earth-engine-project"

# Case area: the first one that is set is used.
CASE_BBOX = [-122.3182, 37.3144, -122.0965, 37.4625]  # west, south, east, north (degrees)
CASE_ASSET = None    # e.g. "projects/your-project/assets/case_area" (a FeatureCollection)
HYBAS_LEVEL = 12
HYBAS_IDS = []       # HydroBASINS IDs, used only when CASE_BBOX and CASE_ASSET are None

FOLDER_NAME = "HP2D_Stanford_30m"

CRS = "EPSG:3310"    # the case's projected CRS; None picks the UTM zone of the case centre
SCALE = 30           # model cell size [m]

STATIC_START = "2019-01-01"   # LAI and albedo medians
STATIC_END = "2022-01-01"
EVENT_START = "2022-12-31T00:00:00"   # rainfall start, and the soil moisture time
EVENT_END = "2023-01-01T00:00:00"
RAIN_STEP_MIN = 180   # 30 or a multiple of 30
SOIL_DEPTH_M = 1.0    # theta is averaged over this depth
WORLDPOP_YEAR = 2020
DTB_ASSET = None      # your depth-to-bedrock image in metres, or None to skip it

NODATA = -9999
ERA5_LAYERS_M = [(0.00, 0.07), (0.07, 0.28), (0.28, 1.00), (1.00, 2.89)]


# -----------------------------------------------------------------------------
# EARTH ENGINE
# -----------------------------------------------------------------------------
def init_ee():
    try:
        ee.Initialize(project=PROJECT_ID)
    except Exception:
        ee.Authenticate()
        ee.Initialize(project=PROJECT_ID)


# -----------------------------------------------------------------------------
# CASE AREA AND MODEL GRID
# -----------------------------------------------------------------------------
def build_case_area():
    """Return the catchment features and the case geometry."""
    if CASE_BBOX:
        geometry = ee.Geometry.Rectangle(CASE_BBOX, proj="EPSG:4326", geodesic=False)
        catchments = ee.FeatureCollection([ee.Feature(geometry, {"name": "case"})])
    elif CASE_ASSET:
        catchments = ee.FeatureCollection(CASE_ASSET)
        geometry = catchments.geometry()
    elif HYBAS_IDS:
        hybas = ee.FeatureCollection(f"WWF/HydroSHEDS/v1/Basins/hybas_{HYBAS_LEVEL}")
        catchments = hybas.filter(ee.Filter.inList("HYBAS_ID", HYBAS_IDS))
        geometry = catchments.geometry()
    else:
        raise ValueError("Set CASE_BBOX, CASE_ASSET or HYBAS_IDS.")
    return catchments, geometry


def utm_crs(geometry):
    lon, lat = geometry.centroid(1).coordinates().getInfo()
    zone = int((lon + 180) // 6) + 1
    return f"EPSG:{(32600 if lat >= 0 else 32700) + zone}"


def model_grid(geometry, crs):
    """Corner snapped to SCALE in the case CRS; every export uses this grid."""
    ring = geometry.bounds(1, ee.Projection(crs)).coordinates().get(0).getInfo()
    xs = [point[0] for point in ring]
    ys = [point[1] for point in ring]
    west = math.floor(min(xs) / SCALE) * SCALE
    east = math.ceil(max(xs) / SCALE) * SCALE
    south = math.floor(min(ys) / SCALE) * SCALE
    north = math.ceil(max(ys) / SCALE) * SCALE
    transform = [SCALE, 0, west, 0, -SCALE, north]
    region = ee.Geometry.Rectangle([west, south, east, north], proj=crs, geodesic=False)
    print(f"Model grid: {crs}, {SCALE} m, {(east - west) // SCALE} x {(north - south) // SCALE} cells")
    return transform, region


def on_grid(image, native_scale_m, crs, transform, categorical=False):
    """Mode or mean when the source cell is finer than the model cell, else nearest or bilinear."""
    if native_scale_m < SCALE:
        reducer = ee.Reducer.mode() if categorical else ee.Reducer.mean()
        image = image.reduceResolution(reducer=reducer, maxPixels=65535)
    elif not categorical:
        image = image.resample("bilinear")
    return image.reproject(crs=crs, crsTransform=transform)


# -----------------------------------------------------------------------------
# MAPS
# -----------------------------------------------------------------------------
def build_maps(geometry, crs, transform):
    def grid(image, native_scale_m, categorical=False):
        return on_grid(image, native_scale_m, crs, transform, categorical).clip(geometry)

    maps = {}
    maps["DEM"] = grid(ee.Image("MERIT/DEM/v1_0_3").select("dem"), 90).rename("DEM")
    maps["LULC"] = grid(ee.Image("ESA/WorldCover/v100/2020").select("Map"), 10, True).rename("LULC")
    soil = ee.Image("OpenLandMap/SOL/SOL_TEXTURE-CLASS_USDA-TT_M/v02").select("b0")
    maps["SOIL"] = grid(soil, 250, True).rename("SOIL")

    lai = ee.ImageCollection("MODIS/061/MCD15A3H").select("Lai").filterDate(STATIC_START, STATIC_END)
    lai = lai.median().multiply(0.1).setDefaultProjection(lai.first().projection())
    maps["LAI"] = grid(lai, 500).rename("LAI")
    albedo = (
        ee.ImageCollection("MODIS/061/MCD43A3")
        .select("Albedo_BSA_shortwave")
        .filterDate(STATIC_START, STATIC_END)
    )
    albedo = albedo.median().multiply(0.001).setDefaultProjection(albedo.first().projection())
    maps["Albedo"] = grid(albedo, 500).rename("Albedo")

    # GHSL: built-up m2 in each 100 m cell (10,000 m2), so the share is built / 10,000.
    built = ee.Image("JRC/GHSL/P2023A/GHS_BUILT_S/2020").select("built_surface")
    maps["Impervious_Fraction"] = grid(built.divide(10000), 100).rename("Impervious_Fraction")

    # WorldPop: people in each ~100 m cell, divided by the cell area in km2.
    people = (
        ee.ImageCollection("WorldPop/GP/100m/pop")
        .filter(ee.Filter.calendarRange(WORLDPOP_YEAR, WORLDPOP_YEAR, "year"))
        .filterBounds(geometry)
    )
    projection = people.first().projection()
    people = people.mosaic().setDefaultProjection(projection)
    density = people.divide(ee.Image.pixelArea().divide(1e6)).setDefaultProjection(projection)
    maps["Population_Density"] = grid(density, 100).rename("Population_Density")
    maps["_people"] = people.clip(geometry)  # for the population totals in the tables

    # ERA5-Land: depth-weighted theta over the top SOIL_DEPTH_M at EVENT_START.
    era5 = ee.ImageCollection("ECMWF/ERA5_LAND/HOURLY").filterDate(
        EVENT_START, ee.Date(EVENT_START).advance(1, "hour")
    ).first()
    theta = ee.Image(0)
    for number, (top, bottom) in enumerate(ERA5_LAYERS_M, start=1):
        overlap = max(0.0, min(bottom, SOIL_DEPTH_M) - top)
        if overlap > 0:
            layer = era5.select(f"volumetric_soil_water_layer_{number}")
            theta = theta.add(layer.multiply(overlap / SOIL_DEPTH_M))
    theta = theta.setDefaultProjection(era5.projection())
    maps["Initial_Soil_Moisture_theta"] = grid(theta, 11132).rename("theta")

    if DTB_ASSET:
        maps["DTB"] = grid(ee.Image(DTB_ASSET), 250).rename("DTB")
    return maps


def rainfall_maps(geometry, crs, transform):
    """Mean IMERG intensity [mm/h] over each RAIN_STEP_MIN step, on the model grid."""
    imerg = ee.ImageCollection("NASA/GPM_L3/IMERG_V07").select("precipitation")
    imerg = imerg.filterDate(EVENT_START, EVENT_END).filterBounds(geometry)
    projection = imerg.first().projection()
    start = ee.Date(EVENT_START)
    steps = int(ee.Date(EVENT_END).difference(start, "minute").getInfo() // RAIN_STEP_MIN)
    out = []
    for step in range(steps):
        begin = start.advance(step * RAIN_STEP_MIN, "minute")
        mean = imerg.filterDate(begin, begin.advance(RAIN_STEP_MIN, "minute")).mean()
        mean = mean.setDefaultProjection(projection)
        label = begin.format("yyyy_MM_dd_HH_mm").getInfo()
        out.append((f"GPM_{RAIN_STEP_MIN}min_{label}", on_grid(mean, 11132, crs, transform).clip(geometry)))
    return out


# -----------------------------------------------------------------------------
# TABLES
# -----------------------------------------------------------------------------
def region_stat(image, geometry, reducer, scale):
    band = image.bandNames().get(0)
    values = image.reduceRegion(
        reducer=reducer, geometry=geometry, scale=scale, maxPixels=1e13, bestEffort=True, tileScale=4
    )
    return values.get(band)


def summary(geometry, maps):
    return {
        "area_km2": geometry.area(1).divide(1e6),
        "population": region_stat(maps["_people"], geometry, ee.Reducer.sum(), 100),
        "mean_impervious_percent": ee.Number(
            region_stat(maps["Impervious_Fraction"], geometry, ee.Reducer.mean(), SCALE)
        ).multiply(100),
        "dominant_LULC": region_stat(maps["LULC"], geometry, ee.Reducer.mode(), SCALE),
        "dominant_SOIL": region_stat(maps["SOIL"], geometry, ee.Reducer.mode(), SCALE),
        "mean_elevation_m": region_stat(maps["DEM"], geometry, ee.Reducer.mean(), SCALE),
        "mean_LAI": region_stat(maps["LAI"], geometry, ee.Reducer.mean(), SCALE),
        "mean_albedo": region_stat(maps["Albedo"], geometry, ee.Reducer.mean(), SCALE),
        "mean_initial_theta": region_stat(
            maps["Initial_Soil_Moisture_theta"], geometry, ee.Reducer.mean(), SCALE
        ),
    }


def tables(catchments, geometry, maps, crs):
    domain = ee.Feature(None, {
        **summary(geometry, maps),
        "folder": FOLDER_NAME,
        "crs": crs,
        "cell_size_m": SCALE,
        "event_start": EVENT_START,
        "event_end": EVENT_END,
        "rain_step_min": RAIN_STEP_MIN,
        "soil_depth_m": SOIL_DEPTH_M,
        "worldpop_year": WORLDPOP_YEAR,
    })
    per_catchment = catchments.map(
        lambda feature: ee.Feature(
            ee.Feature(None, summary(feature.geometry(), maps)).copyProperties(feature)
        )
    )
    return ee.FeatureCollection([domain]), per_catchment


# -----------------------------------------------------------------------------
# EXPORTS
# -----------------------------------------------------------------------------
def image_task(image, name, folder, crs, transform, region, categorical=False):
    image = image.unmask(NODATA)
    return ee.batch.Export.image.toDrive(
        image=image.toInt16() if categorical else image.toFloat(),
        description=name,
        folder=folder,
        fileNamePrefix=name,
        region=region,
        crs=crs,
        crsTransform=transform,
        maxPixels=1e13,
        formatOptions={"noData": NODATA},
    )


def table_task(collection, name, file_format):
    return ee.batch.Export.table.toDrive(
        collection=collection,
        description=name,
        folder=FOLDER_NAME,
        fileNamePrefix=name,
        fileFormat=file_format,
    )


def monitor(tasks, poll_seconds=60):
    remaining = dict(tasks)
    while remaining:
        print("-" * 72)
        for name, task in list(remaining.items()):
            status = task.status()
            state = status.get("state", "UNKNOWN")
            print(f"{name}: {state}")
            if state == "FAILED":
                print(f"  error: {status.get('error_message')}")
            if state in ("COMPLETED", "FAILED", "CANCELLED"):
                remaining.pop(name)
        if remaining:
            time.sleep(poll_seconds)


def main():
    init_ee()
    catchments, geometry = build_case_area()
    crs = CRS or utm_crs(geometry)
    transform, region = model_grid(geometry, crs)
    maps = build_maps(geometry, crs, transform)
    domain_log, catchment_log = tables(catchments, geometry, maps, crs)

    tasks = [("Case_Area", table_task(catchments, "Case_Area", "SHP"))]
    for name, image in maps.items():
        if not name.startswith("_"):
            categorical = name in ("LULC", "SOIL")
            tasks.append(
                (name, image_task(image, name, FOLDER_NAME, crs, transform, region, categorical))
            )
    tasks += [
        ("Domain_Log", table_task(domain_log, "Domain_Log", "CSV")),
        ("Catchment_Log", table_task(catchment_log, "Catchment_Log", "CSV")),
    ]
    rain_folder = f"{FOLDER_NAME}_Rainfall_Rasters"
    for name, image in rainfall_maps(geometry, crs, transform):
        tasks.append((name, image_task(image, name, rain_folder, crs, transform, region)))

    print(f"Starting {len(tasks)} exports")
    for name, task in tasks:
        task.start()
        print(f"Started: {name}")
    monitor(tasks)


if __name__ == "__main__":
    main()
```
