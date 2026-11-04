---
title: HP2D Input Maps + Forcing w/ Python
# Hidden until Marcus has run the script once in Earth Engine (checklist in the Pile B report).
draft: true
---

# Input maps and rainfall with Google Earth Engine (Python)

This script builds the input maps of a HydroPol2D case with Google Earth Engine (GEE). It cuts every
dataset to the case area, puts every map on one grid in the case's projected coordinate system, and
exports the maps, two summary tables and the rainfall maps to Google Drive.

---

## What the script does

- Builds the case area from a bounding box, a polygon asset, or HydroBASINS catchments.
- Builds one model grid: the case's projected CRS, a cell size in metres, and a corner snapped to that
  cell size. Every map is exported on this grid, so the maps line up cell for cell.
- Exports the terrain, land cover, soil, vegetation, impervious fraction and population maps.
- Exports the initial soil moisture at the event start, as a volumetric water content.
- Exports the GPM IMERG rainfall, averaged over the time step you choose and resampled onto the model grid.
- Writes a domain table and a catchment table with means, totals and dominant classes.

---

## Datasets

| Map | Dataset (GEE ID) | Native cell |
|---|---|---|
| Elevation | MERIT DEM (`MERIT/DEM/v1_0_3`) | 90 m |
| Land cover | ESA WorldCover 2020 (`ESA/WorldCover/v100/2020`) | 10 m |
| Soil texture class | OpenLandMap USDA texture class (`OpenLandMap/SOL/SOL_TEXTURE-CLASS_USDA-TT_M/v02`) | 250 m |
| Leaf area index | MODIS MCD15A3H (`MODIS/061/MCD15A3H`) | 500 m |
| Albedo | MODIS MCD43A3 (`MODIS/061/MCD43A3`) | 500 m |
| Impervious fraction | GHSL built-up surface 2020 (`JRC/GHSL/P2023A/GHS_BUILT_S/2020`) | 100 m |
| Population | WorldPop (`WorldPop/GP/100m/pop`) | 100 m |
| Initial soil moisture | ERA5-Land hourly (`ECMWF/ERA5_LAND/HOURLY`) | 11 km |
| Rainfall | GPM IMERG V07 (`NASA/GPM_L3/IMERG_V07`) | 11 km |

Depth to bedrock has no public GEE dataset at this resolution. Give your own asset in `DTB_ASSET`, or
leave it `None` and the map is skipped.

---

## Outputs

All maps are GeoTIFFs on the model grid, with `-9999` outside the case area.

| File | Content | Unit |
|---|---|---|
| `DEM.tif` | Elevation | m |
| `LULC.tif` | ESA WorldCover class | class code |
| `SOIL.tif` | USDA texture class (1–12) | class code |
| `LAI.tif` | Leaf area index | m²/m² |
| `Albedo.tif` | Shortwave black-sky albedo | – |
| `Impervious_Fraction.tif` | Built-up share of each cell | 0–1 |
| `Population_Density.tif` | People per km² | people/km² |
| `Initial_Soil_Moisture_theta.tif` | Volumetric water content, mean over the top `SOIL_DEPTH_M` | m³/m³ |
| `DTB.tif` (optional) | Depth to bedrock | m |
| `GPM_<step>min_<yyyy_MM_dd_HH_mm>.tif`, in the folder `<FOLDER_NAME>_Rainfall_Rasters` | Mean rainfall intensity over each step, named by its start time | mm/h |
| `Domain_Log.csv`, `Catchment_Log.csv` | Area, population, mean impervious percent, dominant classes, means | – |
| `Case_Area.shp` | The case area | – |

Categorical maps (land cover, soil) take the most frequent class when the source cell is smaller than the
model cell. Continuous maps take the mean when the source cell is smaller, and bilinear interpolation
when it is larger.

### Units the two models read

- **Initial soil moisture.** HydroPol2D (Python) reads `Initial_Soil_Moisture_theta.tif` as θ directly.
  MATLAB HydroPol2D reads `Initial_Soil_Moisture_path` as the stored water above the residual water content,
  in mm: I₀ = (θ − θr) × soil depth × 1000. Convert the map with the snippet in
  [For MATLAB: soil moisture in mm](#for-matlab-soil-moisture-in-mm).
- **Impervious fraction.** GHSL gives the built-up area in m² per 100 m cell. The script divides by the cell
  area (10,000 m²), so the map is a fraction from 0 to 1.
- **Population.** WorldPop gives people per 100 m cell. The script divides by the cell area, so the map is a
  density in people per km² and does not depend on the model cell size.
- **Rainfall.** IMERG `precipitation` is in mm/h. Each exported map is the mean intensity over its step.

---

## Settings

| Setting | Meaning |
|---|---|
| `PROJECT_ID` | Your Earth Engine project |
| `CASE_BBOX`, `CASE_ASSET`, `HYBAS_LEVEL`, `HYBAS_IDS` | The case area. The first one that is set is used. |
| `CRS` | The case's projected CRS, for example `"EPSG:3310"` or a UTM zone. `None` picks the UTM zone of the case centre. |
| `SCALE` | Model cell size in metres |
| `STATIC_START`, `STATIC_END` | Period of the LAI and albedo medians |
| `EVENT_START`, `EVENT_END` | Rainfall period. Soil moisture is taken at `EVENT_START`. |
| `RAIN_STEP_MIN` | Rainfall time step in minutes (30 or a multiple of 30) |
| `SOIL_DEPTH_M` | Depth over which θ is averaged |
| `WORLDPOP_YEAR` | WorldPop year |

Use the CRS and cell size of your HydroPol2D case, so the exported maps line up with any map you already have.

---

## How to run

1. Install the Earth Engine API and sign in once:

   ```bash
   pip install earthengine-api
   ```

   ```bash
   earthengine authenticate
   ```

2. Save the script below as `HP2D_Inputs.py` and set `PROJECT_ID`, the case area, `CRS`, `SCALE` and the dates.
3. Run it:

   ```bash
   python HP2D_Inputs.py
   ```

4. The script starts every export and prints their states every minute until all are done. The maps and
   tables go to the Google Drive folder `FOLDER_NAME`, and the rainfall maps to `FOLDER_NAME_Rainfall_Rasters`
   (Earth Engine cannot write into a subfolder).

Large areas and long rainfall periods take longer, and Earth Engine limits how many exports run at once.

---

## Using the maps in HydroPol2D

- **Python (Studio or a case file).** Point `static.dem_path`, `lulc_path`, `soil_path`, `lai_path`,
  `impervious_fraction_path`, `initial_soil_moisture_path` and `depth_to_bedrock_path` to the files. Python does
  not read albedo. The rainfall maps go in `forcing.rainfall_raster_mm_h_series`, one entry per file with its
  start time in seconds (`time_s`).
- **MATLAB.** Put the paths in the **Input maps** tab (DTB goes in **Soil and groundwater**). List the rainfall maps in the **Rain and ET** tab
  (time in minutes from the start of the run, then the file path) and set `flag_input_rainfall_map = 1`. Use
  the converted soil moisture map (below) as `Initial_Soil_Moisture_path`, with `flag_initial_soil_moisture = 1`.

### For MATLAB: soil moisture in mm

Run this on your computer after the download. Take θr of each soil class from your `SOIL_parameters` table,
and the soil depth that your MATLAB case uses.

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

## Limitations

- GPM IMERG and ERA5-Land have 11 km cells. Resampling onto a 30 m grid makes smooth maps, not more detail.
  For a small catchment, gauge rainfall is often better.
- ERA5-Land soil moisture comes from a land-surface model, not from observations.
- MERIT DEM has 90 m cells. For a finer case, use a finer DEM (in the United States, `USGS/3DEP/10m`).

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
