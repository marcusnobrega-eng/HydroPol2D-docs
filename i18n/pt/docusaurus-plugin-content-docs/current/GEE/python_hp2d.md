---
title: Mapas de entrada e forçantes do HP2D com Python
# Hidden until Marcus has run the script once in Earth Engine (checklist in the Pile B report).
draft: true
---

# Mapas de entrada e chuva com o Google Earth Engine (Python)

Este script monta os mapas de entrada de um caso do HydroPol2D com o Google Earth Engine (GEE). Ele recorta
cada conjunto de dados na área do caso, coloca todos os mapas numa mesma grade, no sistema de coordenadas
projetado do caso, e exporta os mapas, duas tabelas-resumo e os mapas de chuva para o Google Drive.

---

## O que o script faz

- Define a área do caso a partir de um retângulo, de um asset de polígono ou de bacias do HydroBASINS.
- Monta uma grade do modelo: o CRS projetado do caso, um tamanho de célula em metros e um canto alinhado a
  esse tamanho. Todos os mapas saem nessa grade, então coincidem célula a célula.
- Exporta os mapas de terreno, uso do solo, solo, vegetação, fração impermeável e população.
- Exporta a umidade inicial do solo no início do evento, como conteúdo volumétrico de água.
- Exporta a chuva do GPM IMERG, média no passo de tempo escolhido e reamostrada para a grade do modelo.
- Grava uma tabela do domínio e uma das bacias, com médias, totais e classes dominantes.

---

## Conjuntos de dados

| Mapa | Conjunto de dados (ID no GEE) | Célula original |
|---|---|---|
| Elevação | MERIT DEM (`MERIT/DEM/v1_0_3`) | 90 m |
| Uso e cobertura do solo | ESA WorldCover 2020 (`ESA/WorldCover/v100/2020`) | 10 m |
| Classe textural do solo | Classe textural USDA do OpenLandMap (`OpenLandMap/SOL/SOL_TEXTURE-CLASS_USDA-TT_M/v02`) | 250 m |
| Índice de área foliar | MODIS MCD15A3H (`MODIS/061/MCD15A3H`) | 500 m |
| Albedo | MODIS MCD43A3 (`MODIS/061/MCD43A3`) | 500 m |
| Fração impermeável | Área construída GHSL 2020 (`JRC/GHSL/P2023A/GHS_BUILT_S/2020`) | 100 m |
| População | WorldPop (`WorldPop/GP/100m/pop`) | 100 m |
| Umidade inicial do solo | ERA5-Land horário (`ECMWF/ERA5_LAND/HOURLY`) | 11 km |
| Chuva | GPM IMERG V07 (`NASA/GPM_L3/IMERG_V07`) | 11 km |

Não há um conjunto público no GEE para a profundidade até a rocha nesta resolução. Informe o seu asset em
`DTB_ASSET`, ou deixe `None` e esse mapa não é exportado.

---

## Saídas

Todos os mapas são GeoTIFFs na grade do modelo, com `-9999` fora da área do caso.

| Arquivo | Conteúdo | Unidade |
|---|---|---|
| `DEM.tif` | Elevação | m |
| `LULC.tif` | Classe do ESA WorldCover | código de classe |
| `SOIL.tif` | Classe textural USDA (1–12) | código de classe |
| `LAI.tif` | Índice de área foliar | m²/m² |
| `Albedo.tif` | Albedo de onda curta (black-sky) | – |
| `Impervious_Fraction.tif` | Parte construída de cada célula | 0–1 |
| `Population_Density.tif` | Pessoas por km² | pessoas/km² |
| `Initial_Soil_Moisture_theta.tif` | Conteúdo volumétrico de água, médio nos primeiros `SOIL_DEPTH_M` | m³/m³ |
| `DTB.tif` (opcional) | Profundidade até a rocha | m |
| `GPM_<passo>min_<aaaa_MM_dd_HH_mm>.tif`, na pasta `<FOLDER_NAME>_Rainfall_Rasters` | Intensidade média da chuva em cada passo, com o nome do início do passo | mm/h |
| `Domain_Log.csv`, `Catchment_Log.csv` | Área, população, percentual impermeável médio, classes dominantes, médias | – |
| `Case_Area.shp` | A área do caso | – |

Os mapas categóricos (uso do solo, solo) recebem a classe mais frequente quando a célula de origem é menor que
a do modelo. Os mapas contínuos recebem a média quando a célula de origem é menor, e interpolação bilinear
quando é maior.

### Unidades que os dois modelos leem

- **Umidade inicial do solo.** O HydroPol2D (Python) lê `Initial_Soil_Moisture_theta.tif` diretamente como θ.
  O HydroPol2D em MATLAB lê `Initial_Soil_Moisture_path` como a água armazenada acima do teor residual, em mm:
  I₀ = (θ − θr) × profundidade do solo × 1000. Converta o mapa com o trecho em
  [Para o MATLAB: umidade do solo em mm](#para-o-matlab-umidade-do-solo-em-mm).
- **Fração impermeável.** O GHSL dá a área construída em m² por célula de 100 m. O script divide pela área da
  célula (10.000 m²), então o mapa é uma fração de 0 a 1.
- **População.** O WorldPop dá pessoas por célula de 100 m. O script divide pela área da célula, então o mapa
  é uma densidade em pessoas por km² e não depende do tamanho da célula do modelo.
- **Chuva.** A banda `precipitation` do IMERG está em mm/h. Cada mapa exportado é a intensidade média no seu passo.

---

## Configurações

| Configuração | Significado |
|---|---|
| `PROJECT_ID` | O seu projeto do Earth Engine |
| `CASE_BBOX`, `CASE_ASSET`, `HYBAS_LEVEL`, `HYBAS_IDS` | A área do caso. Vale a primeira que estiver definida. |
| `CRS` | O CRS projetado do caso, por exemplo `"EPSG:3310"` ou uma zona UTM. `None` escolhe a zona UTM do centro do caso. |
| `SCALE` | Tamanho da célula do modelo, em metros |
| `STATIC_START`, `STATIC_END` | Período das medianas de LAI e albedo |
| `EVENT_START`, `EVENT_END` | Período da chuva. A umidade do solo é tomada em `EVENT_START`. |
| `RAIN_STEP_MIN` | Passo de tempo da chuva, em minutos (30 ou um múltiplo de 30) |
| `SOIL_DEPTH_M` | Profundidade em que θ é promediado |
| `WORLDPOP_YEAR` | Ano do WorldPop |

Use o CRS e o tamanho de célula do seu caso do HydroPol2D, para que os mapas exportados coincidam com os mapas
que você já tem.

---

## Como executar

1. Instale a API do Earth Engine e faça login uma vez:

   ```bash
   pip install earthengine-api
   ```

   ```bash
   earthengine authenticate
   ```

2. Salve o script abaixo como `HP2D_Inputs.py` e ajuste `PROJECT_ID`, a área do caso, `CRS`, `SCALE` e as datas.
3. Execute:

   ```bash
   python HP2D_Inputs.py
   ```

4. O script inicia todas as exportações e mostra o estado delas a cada minuto até terminarem. Os mapas e as
   tabelas vão para a pasta `FOLDER_NAME` do Google Drive, e os mapas de chuva para `FOLDER_NAME_Rainfall_Rasters`
   (o Earth Engine não grava em subpastas).

Áreas grandes e períodos longos de chuva demoram mais, e o Earth Engine limita quantas exportações rodam ao
mesmo tempo.

---

## Como usar os mapas no HydroPol2D

- **Python (Studio ou um arquivo de caso).** Aponte `static.dem_path`, `lulc_path`, `soil_path`, `lai_path`,
  `impervious_fraction_path`, `initial_soil_moisture_path` e `depth_to_bedrock_path` para os arquivos. O Python
  não lê albedo. Os mapas de chuva vão em `forcing.rainfall_raster_mm_h_series`, uma entrada por arquivo com o
  seu início em segundos (`time_s`).
- **MATLAB.** Coloque os caminhos na aba **Input maps** (o DTB vai em **Soil and groundwater**). Liste os mapas
  de chuva na aba **Rain and ET** (tempo em minutos desde o início da simulação, depois o caminho do arquivo) e
  use `flag_input_rainfall_map = 1`. Use o mapa de umidade convertido (abaixo) como `Initial_Soil_Moisture_path`,
  com `flag_initial_soil_moisture = 1`.

### Para o MATLAB: umidade do solo em mm

Rode isto no seu computador depois do download. Tome o θr de cada classe de solo da sua tabela
`SOIL_parameters` e a profundidade do solo que o seu caso em MATLAB usa.

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

## Limitações

- O GPM IMERG e o ERA5-Land têm células de 11 km. Reamostrar para uma grade de 30 m gera mapas suaves, não mais
  detalhe. Numa bacia pequena, a chuva de pluviômetros costuma ser melhor.
- A umidade do solo do ERA5-Land vem de um modelo de superfície, não de observações.
- O MERIT DEM tem células de 90 m. Para um caso mais fino, use um DEM mais fino (nos Estados Unidos,
  `USGS/3DEP/10m`).

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
