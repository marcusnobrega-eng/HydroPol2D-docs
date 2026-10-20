---
title: Mapas de entrada HP2D + forçar com Python
---

# Geração de domínio com Google Earth Engine (Python)

Este fluxo de trabalho automatiza a geração de todas as entradas espaciais necessárias para modelagem hidrológica usando HydroPol2D.
O script integra vários conjuntos de dados globais por meio de Google Earth Engine (GEE), processa-os em camadas raster consistentes e exporta resultados espaciais e estatísticos para um domínio de modelagem selecionado.

---

## O que o fluxo de trabalho faz

O script executa as seguintes etapas:
- Constrói um domínio de modelagem (país, bacias hidrográficas ou geometria personalizada)
- Extrai conjuntos de dados ambientais (topografia, cobertura da terra, solo, vegetação, clima)
- Calcula as condições hidrológicas iniciais (umidade do solo)
- Gera séries temporais de precipitação a partir de GPM IMERG
- Calcula estatísticas em todo o domínio e em nível de captação
- Exporta todos os dados para o Google Drive

---

## Principais recursos

- Fluxo de trabalho totalmente automatizado
- Integração de vários conjuntos de dados
- Definição de domínio flexível
- Escalável para grandes regiões
- Saídas prontas para exportação para HydroPol2D
- Inclui sistema de monitoramento de tarefas

---

## Conjuntos de dados usados

### Topografia
- MERIT DEM → Elevação (m)

### Superfície Terrestre
- ESA WorldCover → Uso/Cobertura do Solo
- OpenLandMap → Classes de textura do solo
- GHSL → Superfícies impermeáveis

### Vegetação e Radiação
- MODIS LAI → Índice de área foliar
- MODIS Albedo → refletividade da superfície

### Clima e Hidrologia
- ERA5-Terra → Umidade do solo (condições iniciais)
- GPM IMERG → Série temporal de precipitação

### Socio-econômico
- WorldPop → Densidade populacional

---

## Definição de Domínio

O domínio é definido usando um FeatureCollection.
Exemplo (Índia):
```python
india = ee.FeatureCollection("FAO/GAUL/2015/level0") \
    .filter(ee.Filter.eq("ADM0_NAME", "India"))
```

Saídas:
- Geometria
- Caixa delimitadora
- Recursos de captação

---

## Especificações de saída

### Saídas rasterizadas

| Camada | Descrição | Unidades |
|------|------------|------|
| DEM | Elevação | m |
| LULC | Cobertura da terra | categórico |
| SOLO | Classe de solo | categórico |
| DTB | Profundidade até o alicerce | m |
| LAI | Índice de área foliar | adimensional |
| Albedo | Refletância de superfície | - |
| Umidade do solo | Condição inicial | mm |
| MundoPop | População | pessoas/km² |

---

### Tabelas

**Registro de domínio**
- População total
- Elevação média
- Umidade média do solo
- Cobertura dominante da terra e solo

**Registro de Captação**
- Área
- População
- Estatísticas hidrológicas por bacia hidrográfica

---

### Resultados de precipitação

- GPM IMERG rasters de precipitação
- Resolução temporal configurável (30 min → diariamente)
- Unidades: mm/h

Exemplo de nome de arquivo:
GPM_180min_2025_06_01_00_00.tif

---

## Configuração temporal

| Parâmetro | Descrição |
|----------|------------|
| data de início | Janela de tempo do conjunto de dados |
| data final | Janela de tempo do conjunto de dados |
| gpmStartDate | Início das chuvas |
| gpmEndDate | Fim da chuva |
| gpmTemporalResolução | Minutos |

---

## Configuração Espacial

| Parâmetro | Descrição |
|----------|------------|
| escala_de_imagem | Resolução raster (m) |
| CRS | Sistema de coordenadas |
| semDataValue | Valor de dados ausente |

---

## Como correr

### Etapa 1: ambiente de configuração

Instale dependências:
```bash
pip install earthengine-api
```

Autenticar:
```bash
earthengine authenticate
```

---

### Etapa 2: configurar o script

Modificar:
- Domínio (país ou bacias hidrográficas)
- Datas
- Resolução
- Pasta de saída

---

### Etapa 3: executar o script

```bash
python HP2D_Inputs.py
```

---

### Etapa 4: exportar dados

- As tarefas são iniciadas automaticamente
- Monitore o progresso no console
- Saídas salvas no Google Drive

---

## Monitoramento de tarefas

O script inclui monitoramento automático:
- Rastreia o status da tarefa
- Detecta falhas
- Imprime atualizações de progresso

---

## Notas importantes

- As saídas são exportadas como GeoTIFF e CSV
- Domínios grandes podem levar um tempo significativo
- As cotas GEE podem limitar as exportações simultâneas

---

## Aplicativos

Este fluxo de trabalho suporta:
### Modelagem Hidrológica
- Modelos distribuídos de chuva-escoamento
- Simulação de inundação
- Análise de bacia hidrográfica

### Análise Ambiental
- Caracterização da superfície terrestre
- Estudos de solo e vegetação
- Processos orientados para o clima

### Avaliação de risco
- Mapeamento de risco de inundação
- Análise de escoamento urbano
- Exposição da população

---

## Limitações

- A resolução GPM (~11 km) pode ser grosseira para pequenas bacias
- A umidade do solo ERA5 é derivada do modelo (não observada)
- O tempo de exportação depende do tamanho e duração do domínio

---

## Fluxo de trabalho recomendado com HydroPol2D

1. Gere entradas de domínio usando este script
2. Importar rasters para HydroPol2D
3. Execute simulação hidrológica
4. Saídas pós-processo

---

## Versão

v1.0 — Fluxo de trabalho de geração de domínio baseado em Python para HydroPol2D

---

## Código Fonte

Veja implementação:
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
