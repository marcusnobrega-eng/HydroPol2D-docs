---
title: Mapas de entrada HP2D + Forzado con Python
---

# Generación de dominio con Google Earth Engine (Python)

Este flujo de trabajo automatiza la generación de todas las entradas espaciales necesarias para el modelado hidrológico utilizando HydroPol2D.
El script integra múltiples conjuntos de datos globales a través de Google Earth Engine (GEE), los procesa en capas ráster consistentes y exporta resultados tanto espaciales como estadísticos para un dominio de modelado seleccionado.
---

## Qué hace el flujo de trabajo

El script realiza los siguientes pasos:
- Crea un dominio de modelado (país, cuencas o geometría personalizada)
- Extrae conjuntos de datos ambientales (topografía, cobertura terrestre, suelo, vegetación, clima)
- Calcula las condiciones hidrológicas iniciales (humedad del suelo)
- Genera series temporales de lluvia a partir de GPM IMERG
- Calcula estadísticas de todo el dominio y a nivel de cuenca.
- Exporta todos los datos a Google Drive

---

## Características clave

- Flujo de trabajo totalmente automatizado
- Integración de múltiples conjuntos de datos
- Definición de dominio flexible
- Escalable para grandes regiones
- Salidas listas para exportar para HydroPol2D
- Incluye sistema de seguimiento de tareas.

---

## Conjuntos de datos utilizados

### Topografía
- MERIT DEM → Elevación (m)

### Superficie terrestre
- ESA WorldCover → Uso del suelo / Cobertura del suelo
- OpenLandMap → Clases de textura del suelo
- GHSL → Superficies impermeables

### Vegetación y radiación
- MODIS LAI → Índice de área foliar
- MODIS Albedo → Reflectividad de la superficie

### Clima e hidrología
- ERA5-Tierra → Humedad del suelo (condiciones iniciales)
- GPM IMERG → Serie temporal de precipitaciones

### Socioeconómico
- Pop mundial → Densidad de población

---

## Definición de dominio

El dominio se define mediante FeatureCollection.
Ejemplo (India):
```python
india = ee.FeatureCollection("FAO/GAUL/2015/level0") \
    .filter(ee.Filter.eq("ADM0_NAME", "India"))
```

Salidas:- Geometría
- cuadro delimitador
- Características de la cuenca

---

## Especificaciones de salida

### Salidas ráster

| Capa | Descripción | Unidades |
|------|------------|------|
| DEM | Elevación | metro |
| LULC | Cobertura terrestre | categórico |
| SUELO | clase de suelo | categórico |
| DTB | Profundidad hasta el lecho de roca | metro |
| LAI | Índice de área foliar | sin dimensiones |
| Albedo | Reflectancia de superficie | - |
| Humedad del suelo | Condición inicial | milímetros |
| pop mundial | Población | personas/km² |

---

### Mesas

**Registro de dominio**- Población total
- Elevación media
- Humedad media del suelo
- Cobertura terrestre y suelo dominantes.

**Registro de cuenca**- Área
- Población
- Estadísticas hidrológicas por cuenca

---

### Salidas de lluvia

- GPM IMERG rásteres de precipitación
- Resolución temporal configurable (30 min → diaria)
- Unidades: mm/h

Ejemplo de nombre de archivo:
PHTOKEN0XYZ_180min_2025_06_01_00_00.tif
---

## Configuración temporal

| Parámetro | Descripción |
|----------|------------|
| fecha de inicio | Ventana de tiempo del conjunto de datos |
| fecha final | Ventana de tiempo del conjunto de datos |
| gpmFechaInicio | Inicio de lluvia |
| gpmFechaEnd | Fin de las precipitaciones |
| gpmResoluciónTemporal | Minutos |

---

## Configuración espacial

| Parámetro | Descripción |
|----------|------------|
| escala_de_imagen | Resolución ráster (m) |
| CRS | sistema de coordenadas |
| sin valor de datos | Valor de datos faltantes |

---

## Cómo correr

### Paso 1: configurar el entorno

Instalar dependencias:
```bash
pip install earthengine-api
```

Autenticar:
```bash
earthengine authenticate
```

---

### Paso 2: configurar el script

Modificar:
- Dominio (país o cuencas)
- Fechas
- Resolución
- Carpeta de salida

---

### Paso 3: ejecutar el script

```bash
python HP2D_Inputs.py
```

---

### Paso 4: exportar datos

- Las tareas comienzan automáticamente
- Monitorear el progreso en la consola
- Salidas guardadas en Google Drive

---

## Monitoreo de tareas

El script incluye seguimiento automático:
- Realiza un seguimiento del estado de la tarea
- Detecta fallas
- Imprime actualizaciones de progreso

---

## Notas importantes

- Los resultados se exportan como GeoTIFF y CSV.
- Los dominios grandes pueden tardar mucho tiempo
- Las cuotas GEE pueden limitar las exportaciones simultáneas

---

## Aplicaciones

Este flujo de trabajo admite:
### Modelización hidrológica
- Modelos distribuidos de lluvia-escorrentía
- Simulación de inundaciones
- Análisis de cuencas

### Análisis ambiental
- Caracterización de la superficie terrestre.
- Estudios de suelos y vegetación.
- Procesos impulsados ​​por el clima

### Evaluación de riesgos
- Mapeo del riesgo de inundaciones
- Análisis de escorrentía urbana
- Exposición de la población

---

## Limitaciones

- La resolución GPM (~11 km) puede ser aproximada para cuencas pequeñas
- La humedad del suelo ERA5 se deriva del modelo (no observada)
- El tiempo de exportación depende del tamaño y la duración del dominio.

---

## Flujo de trabajo recomendado con HydroPol2D

1. Genere entradas de dominio usando este script
2. Importar rásteres a HydroPol2D
3. Ejecutar simulación hidrológica
4. Salidas posteriores al proceso

---

## Versión

v1.0: flujo de trabajo de generación de dominios basado en Python para HydroPol2D
---

## Código fuente

Ver implementación:
```python
# import time
import ee

# -----------------------------------------------------------------------------
# CONFIG
# -----------------------------------------------------------------------------
PROJECT_ID = "ee-marcusep2025"

hybasLevel = 6
catchmentIds = [4060922650, 4060953900, 4060952550, 4060954060]

Folder_Name = "Domain_India_250m"

scale_of_image = 250
scale_stats_continuous = 250
scale_stats_categorical = 250
scale_stats_population = 100

startDate = "2015-01-02"
endDate = "2020-01-01"

gpmStartDate = "2025-06-01"
gpmEndDate = "2025-06-02"   # fixed zero-padding
initialSoilMoistureDate = "2025-06-24"

gpmTemporalResolution = 180  # minutes

worldpopYear = 2020
crs = "EPSG:4326"
noDataValue = -9999
gpmNativeScale = 11132

# -----------------------------------------------------------------------------
# INIT
# -----------------------------------------------------------------------------
def init_ee():
    try:
        ee.Initialize(project=PROJECT_ID)
    except Exception:
        ee.Authenticate()
        ee.Initialize(project=PROJECT_ID)

# -----------------------------------------------------------------------------
# HELPERS
# -----------------------------------------------------------------------------
def start_task(task, label):
    task.start()
    print(f"Started: {label}")

def image_export_task(image, description, folder, file_name_prefix, region, scale, crs_code):
    return ee.batch.Export.image.toDrive(
        image=image,
        description=description,
        folder=folder,
        fileNamePrefix=file_name_prefix,
        region=region,
        scale=scale,
        crs=crs_code,
        maxPixels=1e13,
        formatOptions={"noData": noDataValue},
    )

def table_export_task(collection, description, folder, file_name_prefix, file_format):
    return ee.batch.Export.table.toDrive(
        collection=collection,
        description=description,
        folder=folder,
        fileNamePrefix=file_name_prefix,
        fileFormat=file_format,
    )

def reduce_mean(image, geom, scale):
    band = image.bandNames().get(0)
    out = image.reduceRegion(
        reducer=ee.Reducer.mean(),
        geometry=geom,
        scale=scale,
        maxPixels=1e13,
        bestEffort=True,
        tileScale=4,
    )
    return out.get(band)

def reduce_sum(image, geom, scale):
    band = image.bandNames().get(0)
    out = image.reduceRegion(
        reducer=ee.Reducer.sum(),
        geometry=geom,
        scale=scale,
        maxPixels=1e13,
        bestEffort=True,
        tileScale=4,
    )
    return out.get(band)

def reduce_mode(image, geom, scale):
    band = image.bandNames().get(0)
    out = image.reduceRegion(
        reducer=ee.Reducer.mode(),
        geometry=geom,
        scale=scale,
        maxPixels=1e13,
        bestEffort=True,
        tileScale=4,
    )
    return out.get(band)

def safe_prop(feature, prop_name):
    props = feature.propertyNames()
    return ee.Algorithms.If(props.contains(prop_name), feature.get(prop_name), None)

# -----------------------------------------------------------------------------
# BUILD DOMAIN
# -----------------------------------------------------------------------------
#def build_domain():
#    hybasPath = f"WWF/HydroSHEDS/v1/Basins/hybas_{hybasLevel}"
#    hybas = ee.FeatureCollection(hybasPath)
#    catchments = hybas.filter(ee.Filter.inList("HYBAS_ID", catchmentIds))
#    catchmentUnion = catchments.union(1)
#    geometry = catchmentUnion.geometry()
#    bounds = geometry.bounds()
#    return catchments, catchmentUnion, geometry, bounds

def build_domain():
    india = (
        ee.FeatureCollection("FAO/GAUL/2015/level0")
        .filter(ee.Filter.eq("ADM0_NAME", "India"))
    )

    catchments = india  # keep variable name unchanged
    catchmentUnion = india
    geometry = india.geometry()
    bounds = geometry.bounds()

    return catchments, catchmentUnion, geometry, bounds

# -----------------------------------------------------------------------------
# DATASETS
# -----------------------------------------------------------------------------
def build_datasets(geometry, bounds):
    merit = ee.Image("MERIT/DEM/v1_0_3")
    DEM = merit.select("dem").rename("DEM").clip(geometry)

    LULC = (
        ee.Image("ESA/WorldCover/v100/2020")
        .select("Map")
        .rename("LULC")
        .clip(geometry)
    )

    SOIL = (
        ee.Image("OpenLandMap/SOL/SOL_TEXTURE-CLASS_USDA-TT_M/v02")
        .select("b0")
        .rename("SOIL")
        .clip(geometry)
    )

    DTB = (
        ee.Image("projects/ee-marcusep2025/assets/Depth_to_bedrock")
        .rename("DTB")
        .clip(geometry)
    )

    albedoCollection = (
        ee.ImageCollection("MODIS/061/MCD43A3")
        .select("Albedo_BSA_shortwave")
        .filterDate(startDate, endDate)
    )

    Albedo = (
        albedoCollection.median()
        .multiply(0.001)
        .rename("Albedo")
        .clip(geometry)
    )

    laiCollection = (
        ee.ImageCollection("MODIS/061/MCD15A3H")
        .select("Lai")
        .filterDate(startDate, endDate)
    )

    LAI = laiCollection.median().multiply(0.1).rename("LAI").clip(geometry)

    era5 = (
        ee.ImageCollection("ECMWF/ERA5_LAND/HOURLY")
        .filterDate(
            initialSoilMoistureDate,
            ee.Date(initialSoilMoistureDate).advance(1, "day"),
        )
        .filterBounds(geometry)
    )

    era5Image = era5.first()

    swvl1 = era5Image.select("volumetric_soil_water_layer_1")
    swvl2 = era5Image.select("volumetric_soil_water_layer_2")
    swvl3 = era5Image.select("volumetric_soil_water_layer_3")
    swvl4 = era5Image.select("volumetric_soil_water_layer_4")

    water1 = swvl1.multiply(0.07 * 1000)
    water2 = swvl2.multiply(0.21 * 1000)
    water3 = swvl3.multiply(0.72 * 1000)
    water4 = swvl4.multiply(1.89 * 1000)

    ERA5_IC_volume = (
        water1.add(water2).add(water3).add(water4)
        .rename("soil_moisture_mm")
        .clip(geometry)
    )

    gpmCollection = (
        ee.ImageCollection("NASA/GPM_L3/IMERG_V07")
        .select("precipitation")
        .filterDate(gpmStartDate, gpmEndDate)
        .filterBounds(bounds)
    )

    WorldPop = (
        ee.ImageCollection("WorldPop/GP/100m/pop")
        .filter(ee.Filter.calendarRange(worldpopYear, worldpopYear, "year"))
        .mosaic()
        .rename("WorldPop")
        .clip(geometry)
    )

    Impervious = (
        ee.Image("JRC/GHSL/P2023A/GHS_BUILT_S/2020")
        .select("built_surface")
        .clip(geometry)
    )

    return {
        "DEM": DEM,
        "LULC": LULC,
        "SOIL": SOIL,
        "DTB": DTB,
        "Albedo": Albedo,
        "LAI": LAI,
        "ERA5_IC_volume": ERA5_IC_volume,
        "gpmCollection": gpmCollection,
        "WorldPop": WorldPop,
        "Impervious": Impervious,
    }

# -----------------------------------------------------------------------------
# LOG TABLES
# -----------------------------------------------------------------------------
def build_log_tables(catchments, geometry, layers):
    DEM = layers["DEM"]
    LULC = layers["LULC"]
    SOIL = layers["SOIL"]
    DTB = layers["DTB"]
    Albedo = layers["Albedo"]
    LAI = layers["LAI"]
    ERA5_IC_volume = layers["ERA5_IC_volume"]
    WorldPop = layers["WorldPop"]
    Impervious = layers["Impervious"]

    totalPopulation = reduce_sum(WorldPop, geometry, scale_stats_population)
    meanImpervious = reduce_mean(Impervious, geometry, scale_stats_continuous)
    area_km2 = geometry.area(1).divide(1e6)
    nCatchments = catchments.size()
    dominantLULC = reduce_mode(LULC, geometry, scale_stats_categorical)
    dominantSOIL = reduce_mode(SOIL, geometry, scale_stats_categorical)
    meanAlbedo = reduce_mean(Albedo, geometry, scale_stats_continuous)
    meanElevation = reduce_mean(DEM, geometry, scale_stats_continuous)
    meanDTB = reduce_mean(DTB, geometry, scale_stats_continuous)
    meanLAI = reduce_mean(LAI, geometry, scale_stats_continuous)
    meanInitialSoilMoisture = reduce_mean(ERA5_IC_volume, geometry, scale_stats_continuous)

    catchmentIdsString = ee.List(catchmentIds).join(";")

    domainLogFeature = ee.Feature(
        None,
        {
            "folder_name": Folder_Name,
            "hybas_level": hybasLevel,
            "catchment_ids_used": catchmentIdsString,
            "number_of_catchments": nCatchments,
            "catchment_area_km2": area_km2,
            "population_in_domain": totalPopulation,
            "mean_impervious_rate_percent": meanImpervious,
            "dominant_LULC": dominantLULC,
            "dominant_SOIL": dominantSOIL,
            "avg_albedo": meanAlbedo,
            "mean_elevation_m": meanElevation,
            "mean_DTB_m": meanDTB,
            "mean_LAI": meanLAI,
            "mean_initial_soil_moisture_mm": meanInitialSoilMoisture,
            "initial_condition_date": initialSoilMoistureDate,
            "worldpop_year": worldpopYear,
            "export_scale_m": scale_of_image,
            "gpm_start_date": gpmStartDate,
            "gpm_end_date": gpmEndDate,
            "gpm_temporal_resolution_min": gpmTemporalResolution,
            "crs": crs,
        },
    )

    domainLogTable = ee.FeatureCollection([domainLogFeature])

    catchmentLogTable = catchments.map(
        lambda ft: ee.Feature(
            None,
            {
                "HYBAS_ID": safe_prop(ft, "HYBAS_ID"),
                "MAIN_BAS": safe_prop(ft, "MAIN_BAS"),
                "NEXT_DOWN": safe_prop(ft, "NEXT_DOWN"),
                "UP_AREA": safe_prop(ft, "UP_AREA"),
                "SUB_AREA": safe_prop(ft, "SUB_AREA"),
                "PFAF_ID": safe_prop(ft, "PFAF_ID"),
                "ENDO": safe_prop(ft, "ENDO"),
                "COAST": safe_prop(ft, "COAST"),
                "catchment_area_km2": ft.geometry().area(1).divide(1e6),
                "population": reduce_sum(WorldPop, ft.geometry(), scale_stats_population),
                "mean_impervious_rate_percent": reduce_mean(
                    Impervious, ft.geometry(), scale_stats_continuous
                ),
                "dominant_LULC": reduce_mode(LULC, ft.geometry(), scale_stats_categorical),
                "dominant_SOIL": reduce_mode(SOIL, ft.geometry(), scale_stats_categorical),
                "avg_albedo": reduce_mean(Albedo, ft.geometry(), scale_stats_continuous),
                "mean_elevation_m": reduce_mean(DEM, ft.geometry(), scale_stats_continuous),
                "mean_DTB_m": reduce_mean(DTB, ft.geometry(), scale_stats_continuous),
                "mean_LAI": reduce_mean(LAI, ft.geometry(), scale_stats_continuous),
                "mean_initial_soil_moisture_mm": reduce_mean(
                    ERA5_IC_volume, ft.geometry(), scale_stats_continuous
                ),
            },
        )
    )

    return domainLogTable, catchmentLogTable

# -----------------------------------------------------------------------------
# EXPORT STATIC DATA
# -----------------------------------------------------------------------------
def export_static_layers(catchmentUnion, geometry, layers):
    tasks = []

    tasks.append(
        ("Catchment_Union", table_export_task(
            collection=catchmentUnion,
            description="Catchment_Union",
            folder=Folder_Name,
            file_name_prefix="Catchment_Union",
            file_format="SHP",
        ))
    )

    for name in ["DEM", "LULC", "SOIL", "DTB", "Albedo", "LAI", "WorldPop", "ERA5_IC_volume"]:
        image = layers[name]
        if name == "ERA5_IC_volume":
            image = image.unmask(noDataValue).float()
        else:
            image = image.unmask(noDataValue)

        tasks.append(
            (
                name,
                image_export_task(
                    image=image,
                    description=name,
                    folder=Folder_Name,
                    file_name_prefix=name,
                    region=geometry,
                    scale=scale_of_image,
                    crs_code=crs,
                ),
            )
        )
    return tasks

# -----------------------------------------------------------------------------
# EXPORT LOGS
# -----------------------------------------------------------------------------
def export_logs(domainLogTable, catchmentLogTable):
    tasks = [
        (
            "Domain_Log",
            table_export_task(
                collection=domainLogTable,
                description="Domain_Log",
                folder=Folder_Name,
                file_name_prefix="Domain_Log",
                file_format="CSV",
            ),
        ),
        (
            "Catchment_Log",
            table_export_task(
                collection=catchmentLogTable,
                description="Catchment_Log",
                folder=Folder_Name,
                file_name_prefix="Catchment_Log",
                file_format="CSV",
            ),
        ),
    ]
    return tasks

# -----------------------------------------------------------------------------
# EXPORT GPM
# -----------------------------------------------------------------------------
def export_gpm(bounds, gpmCollection):
    tasks = []
    rainfallFolder = f"{Folder_Name}/Rainfall_Rasters"

    if gpmTemporalResolution == 30:
        n = gpmCollection.size().getInfo()
        img_list = gpmCollection.toList(n)

        for i in range(n):
            img = ee.Image(img_list.get(i))
            date_str = ee.Date(img.get("system:time_start")).format("yyyy_MM_dd_HH_mm").getInfo()
            export_name = f"GPM_30min_{date_str}"

            task = ee.batch.Export.image.toDrive(
                image=img.unmask(noDataValue).float(),
                description=export_name,
                folder=rainfallFolder,
                fileNamePrefix=export_name,
                region=bounds,
                scale=gpmNativeScale,
                crs="EPSG:4326",
                maxPixels=1e13,
                formatOptions={"noData": noDataValue},
            )
            tasks.append((export_name, task))

    else:
        startMillis = ee.Date(gpmStartDate).millis()
        endMillis = ee.Date(gpmEndDate).millis()
        millisPerPeriod = gpmTemporalResolution * 60 * 1000

        numPeriods = endMillis.subtract(startMillis).divide(millisPerPeriod).floor()
        periods = ee.List.sequence(0, numPeriods.subtract(1))

        aggregatedCollection = ee.ImageCollection(
            periods.map(
                lambda p: (
                    gpmCollection
                    .filterDate(
                        ee.Date(startMillis.add(ee.Number(p).multiply(millisPerPeriod))),
                        ee.Date(startMillis.add(ee.Number(p).multiply(millisPerPeriod))).advance(
                            gpmTemporalResolution, "minute"
                        ),
                    )
                    .mean()
                    .rename("precipitation")
                    .set(
                        "system:time_start",
                        ee.Date(startMillis.add(ee.Number(p).multiply(millisPerPeriod))).millis(),
                    )
                    .set("temporal_resolution_min", gpmTemporalResolution)
                    .set("units", "mm/h")
                )
            )
        )

        n = aggregatedCollection.size().getInfo()
        img_list = aggregatedCollection.toList(n)

        for i in range(n):
            img = ee.Image(img_list.get(i))
            date_str = ee.Date(img.get("system:time_start")).format("yyyy_MM_dd_HH_mm").getInfo()
            export_name = f"GPM_{gpmTemporalResolution}min_{date_str}"

            task = ee.batch.Export.image.toDrive(
                image=img.unmask(noDataValue).float(),
                description=export_name,
                folder=rainfallFolder,
                fileNamePrefix=export_name,
                region=bounds,
                scale=gpmNativeScale,
                crs="EPSG:4326",
                maxPixels=1e13,
                formatOptions={"noData": noDataValue},
            )
            tasks.append((export_name, task))

    return tasks

# -----------------------------------------------------------------------------
# TASK MONITOR
# -----------------------------------------------------------------------------
def monitor_tasks(tasks, poll_seconds=30):
    remaining = {name: task for name, task in tasks}
    while remaining:
        print("-" * 80)
        done = []
        for name, task in remaining.items():
            status = task.status()
            state = status.get("state", "UNKNOWN")
            print(f"{name}: {state}")
            if state in ("COMPLETED", "FAILED", "CANCELLED"):
                done.append(name)
                if state == "FAILED":
                    print(f"  Error: {status.get('error_message')}")
        for name in done:
            remaining.pop(name)
        if remaining:
            time.sleep(poll_seconds)

# -----------------------------------------------------------------------------
# MAIN
# -----------------------------------------------------------------------------
def main():
    init_ee()

    catchments, catchmentUnion, geometry, bounds = build_domain()
    layers = build_datasets(geometry, bounds)
    domainLogTable, catchmentLogTable = build_log_tables(catchments, geometry, layers)

    static_tasks = export_static_layers(catchmentUnion, geometry, layers)
    log_tasks = export_logs(domainLogTable, catchmentLogTable)
    gpm_tasks = export_gpm(bounds, layers["gpmCollection"])

    all_tasks = static_tasks + log_tasks + gpm_tasks

    print(f"Total tasks to start: {len(all_tasks)}")
    for label, task in all_tasks:
        start_task(task, label)

    print("\nMonitoring task status...\n")
    monitor_tasks(all_tasks, poll_seconds=60)

    # Optional:
    # monitor_tasks(all_tasks, poll_seconds=60)

if __name__ == "__main__":
    main()
```
