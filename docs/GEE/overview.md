---
title: HydroPol2D Input Maps
---

# Catchment Characterization with Google Earth Engine

HydroPol2D includes a Google Earth Engine (GEE) script for generating the spatial datasets required to define a hydrological modeling domain.

The workflow extracts, processes, and exports multiple environmental variables from cloud-hosted geospatial datasets, producing a consistent set of raster inputs and summary tables for a selected catchment or group of catchments.

---

## Accessing Google Earth Engine

To use this workflow, users must have access to Google Earth Engine.

### 1. Create an account

Go to:

https://earthengine.google.com/

Click on **"Sign Up"** and register using a Google account.

Approval is typically automatic for academic or research use, but may take some time depending on the request.

---

### 2. Open the Code Editor

Once access is granted, open the GEE Code Editor:

https://code.earthengine.google.com/

This is the environment where the script is executed.

---

### 3. Add the HydroPol2D script

Copy the provided JavaScript code into the Code Editor and run it directly in the browser.

The script uses the Earth Engine API to access datasets, perform spatial operations, and export results to Google Drive.

---

## What the workflow does

The script builds a modeling domain from HydroBASINS catchments and generates a standardized database of raster layers and summary statistics.

The main outputs include:

### Raster datasets

- Digital Elevation Model (DEM)  
- Land Use / Land Cover (LULC)  
- Soil texture class  
- Depth to bedrock (DTB)  
- Surface albedo  
- Leaf Area Index (LAI)  
- Population density (WorldPop)  

All rasters are:

- Clipped to the selected domain  
- Exported at a consistent spatial resolution  
- Reprojected to a user-defined coordinate system  
- Assigned a common no-data value  

---

### Vector and tabular outputs

The script also generates:

- A shapefile of the merged catchment domain  
- A domain-level summary table (CSV)  
- A per-catchment summary table (CSV)  

These outputs provide metadata and aggregated statistics for the study area.

---

## General workflow structure

The code follows a structured sequence:

### 1. User-defined inputs

The user specifies:

- HydroBASINS level (e.g., 6, 7, 8)  
- List of `HYBAS_ID` values  
- Output folder name  
- Spatial resolution (export scale)  
- Coordinate reference system (CRS)  
- Time range for time-dependent datasets  
- Year for population data  

These parameters control the domain definition and dataset processing.

---

### 2. Catchment selection and merging

The script loads HydroBASINS polygons and filters them using the selected `HYBAS_ID` values.

The selected catchments are merged into a single geometry, which defines the modeling domain.

---

### 3. Domain construction

The merged geometry is used to:

- Clip all raster datasets  
- Define export boundaries  
- Compute summary statistics  
- Export the catchment boundary as a shapefile  

---

### 4. Dataset retrieval and processing

The script accesses multiple datasets available in Google Earth Engine, including:

- MERIT DEM for topography  
- ESA WorldCover for land use  
- OpenLandMap for soil classes  
- MODIS products for albedo and LAI  
- WorldPop for population density  
- Global Human Settlement Layer for built-up surfaces

For time-dependent datasets (e.g., albedo and LAI), the script computes median values over the selected time range.

---

### 5. Export of raster layers

Each dataset is:

- Clipped to the domain  
- Standardized in resolution and projection  
- Exported to Google Drive as GeoTIFF  

---

### 6. Computation of summary statistics

The script computes domain-level metrics such as:

- Total area  
- Mean elevation  
- Mean depth to bedrock  
- Mean LAI and albedo  
- Dominant land use and soil class  
- Total population  
- Mean built-up surface fraction  

A second table is generated with the same metrics computed individually for each catchment.

---

## Output structure

All outputs are saved to the specified Google Drive folder and include:

- Raster maps (GeoTIFF)  
- Catchment shapefile (SHP)  
- Domain summary table (CSV)  
- Per-catchment summary table (CSV)  

These files can be directly used as inputs for HydroPol2D or further processed in GIS or modeling environments.

---

## Key Parameters Explained

### HydroBASINS Levels

HydroBASINS provides watershed boundaries at different hierarchical levels (1-12), where:

- **Level 1-3**: Continental and major river basins
- **Level 4-6**: Large regional catchments (recommended for regional studies)
- **Level 7-9**: Sub-catchments (recommended for local/watershed studies)
- **Level 10-12**: Small headwater catchments

**How to choose**: Higher levels = smaller, more detailed catchments. For most applications, levels 6-8 provide a good balance.

---

### Finding HYBAS_ID Values

To identify the `HYBAS_ID` values for your study area:

#### Option 1 - Using GEE Code Editor

- Load HydroBASINS in the Code Editor
- Click on catchments of interest
- The `HYBAS_ID` appears in the Inspector panel

#### Option 2 - Download shapefile

- Visit [HydroSHEDS](https://www.hydrosheds.org/products/hydrobasins)
- Download the appropriate level for your region
- Open in QGIS/ArcGIS and identify catchments by attributes

#### Option 3 - Interactive viewer

- Use the [HydroSHEDS viewer](https://www.hydrosheds.org/hydroatlas)

**Example**: For a study in Northern California, you might select multiple level 7 catchments that drain into the Sacramento River.

---

### Choosing Coordinate Reference Systems (CRS)

Select a CRS appropriate for your study region:

| Region | Recommended CRS | EPSG Code | Notes |
|--------|----------------|-----------|-------|
| California, USA | California Albers | `EPSG:3310` | Equal-area projection |
| Continental USA | USA Contiguous Albers | `EPSG:5070` | USGS standard |
| Global/Multi-region | WGS 84 / UTM | `EPSG:326XX` | Replace XX with zone |
| India | WGS 84 / UTM Zone 43N-45N | `EPSG:32643-32645` | Depending on longitude |
| Europe | ETRS89 LAEA | `EPSG:3035` | Equal-area |

**Why it matters**: Using a local projection minimizes area/distance distortions and ensures accurate hydrological calculations.

---

### Setting the Export Scale

The `scale_of_image` parameter controls output resolution:

- **30m**: High detail, large file sizes, longer processing
- **90m** (default): Good balance for regional studies
- **250m**: Faster processing, smaller files, appropriate for large domains
- **1000m**: Coarse resolution for continental-scale analysis

**Recommendation**: Match or slightly exceed your model's computational grid resolution.

---

### Date Ranges for Time-Varying Data

The script computes **median values** over the specified time range for:

- **Albedo** (MODIS MCD43A3)
- **LAI** (MODIS MCD15A3H)

**Choosing dates**:
- Use 3-5 year periods to smooth inter-annual variability
- Avoid periods with known extreme events (unless studying them)
- Example: `'2015-01-01'` to `'2020-01-01'` captures recent, relatively stable conditions

---

## Data Sources and Resolutions

### Input Datasets

| Dataset | Source | Native Resolution | Temporal Coverage | Notes |
|---------|--------|------------------|-------------------|-------|
| **DEM** | MERIT DEM v1.0.3 | ~90m | Static (2000s) | Error-removed elevation |
| **Land Use** | ESA WorldCover | 10m | 2020, 2021 | 11 global classes |
| **Soil Texture** | OpenLandMap | 250m | Static | USDA texture classes |
| **Depth to Bedrock** | ORNL DAAC Global Soil Dataset | 1 km | Static | ML-derived estimates |
| **Albedo** | MODIS MCD43A3 | 500m | Daily since 2000 | Black-sky shortwave |
| **LAI** | MODIS MCD15A3H | 500m | 4-day since 2002 | Leaf area index |
| **Population** | WorldPop | 100m | Annual 2000-2020 | Constrained estimate |
| **Built-up Surface** | GHSL Built-up Surface | 100m | 1975-2030 | Global coverage |

---

### Land Use / Land Cover Classes (ESA WorldCover)

The LULC output uses the following classification:

| Value | Class | Description |
|-------|-------|-------------|
| 10 | Tree cover | Forests, woodlands |
| 20 | Shrubland | Shrubs, bushes |
| 30 | Grassland | Natural grasslands |
| 40 | Cropland | Agricultural areas |
| 50 | Built-up | Urban, settlements |
| 60 | Bare/sparse vegetation | Rock, sand, sparse veg |
| 70 | Snow and ice | Permanent snow/ice |
| 80 | Water bodies | Rivers, lakes, ocean |
| 90 | Herbaceous wetland | Marshes, swamps |
| 95 | Mangroves | Mangrove forests |
| 100 | Moss and lichen | Arctic/alpine vegetation |

---

### Soil Texture Classes (USDA)

The SOIL output contains USDA texture classes:

| Value | Texture Class | Description |
|-------|--------------|-------------|
| 1 | Clay | > 40% clay |
| 2 | Silty clay | 40-60% silt, > 40% clay |
| 3 | Sandy clay | < 45% sand, > 35% clay |
| 4 | Clay loam | 27-40% clay, 20-45% sand |
| 5 | Silty clay loam | 27-40% clay, < 20% sand |
| 6 | Sandy clay loam | 20-35% clay, > 45% sand |
| 7 | Loam | 7-27% clay, balanced sand/silt |
| 8 | Silty loam | < 50% sand, 50-87% silt |
| 9 | Sandy loam | > 50% sand, 0-50% silt |
| 10 | Silt | > 80% silt |
| 11 | Loamy sand | 70-90% sand |
| 12 | Sand | > 85% sand |

---

## Understanding the Output Files

### Raster Outputs (GeoTIFF)

All GeoTIFF files share:
- **NoData value**: `-9999`
- **Projection**: As specified by `crs`
- **Resolution**: As specified by `scale_of_image`
- **Extent**: Clipped to catchment union boundary

**File naming**:
- `DEM.tif` – Elevation in meters
- `LULC.tif` – Land use class codes (10-100)
- `SOIL.tif` – Soil texture class codes (1-12)
- `DTB.tif` – Depth to bedrock in meters
- `Albedo.tif` – Surface albedo (0-1, unitless)
- `LAI.tif` – Leaf area index (m²/m²)
- `WorldPop.tif` – Population density (persons/pixel)

---

### Shapefile Output

**Catchment_Union.shp** contains:
- Merged boundary of all selected catchments
- Original HydroBASINS attributes for each sub-catchment
- Can be used to:
  - Visualize the domain in GIS
  - Clip additional datasets
  - Define model boundaries

---

### CSV Outputs

#### Domain_Log.csv

Single-row summary of the entire modeling domain:

| Column | Description | Units |
|--------|-------------|-------|
| `folder_name` | Google Drive export folder | - |
| `hybas_level` | HydroBASINS level used | - |
| `catchment_ids_used` | Semicolon-separated HYBAS_IDs | - |
| `number_of_catchments` | Count of merged catchments | - |
| `catchment_area_km2` | Total domain area | km² |
| `population_in_domain` | Total population | persons |
| `mean_built_surface_percent` | Average built-up surface | % |
| `dominant_LULC` | Most common land use class | code |
| `dominant_SOIL` | Most common soil class | code |
| `avg_albedo` | Mean surface albedo | 0-1 |
| `mean_elevation_m` | Mean elevation | m |
| `mean_DTB_m` | Mean depth to bedrock | m |
| `mean_LAI` | Mean leaf area index | m²/m² |
| `worldpop_year` | WorldPop data year | year |
| `export_scale_m` | Export resolution | m |
| `crs` | Coordinate system | EPSG code |

---

#### Catchment_Log.csv

Per-catchment statistics with one row per sub-catchment:

| Column | Description | Source |
|--------|-------------|--------|
| `HYBAS_ID` | Unique catchment identifier | HydroBASINS |
| `MAIN_BAS` | Main basin ID | HydroBASINS |
| `NEXT_DOWN` | Downstream catchment ID | HydroBASINS |
| `UP_AREA` | Upstream drainage area | km² |
| `SUB_AREA` | Sub-catchment area | km² |
| `PFAF_ID` | Pfafstetter code | HydroBASINS |
| `catchment_area_km2` | Calculated area | km² |
| `population` | Total population | persons |
| `mean_built_surface_percent` | Built-up surface | % |
| `dominant_LULC` | Dominant land use | code |
| `dominant_SOIL` | Dominant soil class | code |
| `avg_albedo` | Mean albedo | 0-1 |
| `mean_elevation_m` | Mean elevation | m |
| `mean_DTB_m` | Mean depth to bedrock | m |
| `mean_LAI` | Mean LAI | m²/m² |

**Use case**: Compare sub-catchment characteristics, identify spatial patterns, validate model inputs.

---

## Troubleshooting

### Common Issues

#### 1. Memory Errors ("Computation timed out")

**Solution**:
- Reduce the number of catchments
- Increase `scale_stats_continuous` and `scale_stats_categorical`
- Export smaller regions separately
- Use `tileScale` parameter in reduction operations (already implemented in the script)

---

#### 2. Depth to Bedrock (DTB) Access

The depth to bedrock layer is sourced from the ORNL DAAC Global Soil Dataset:

**Citation**: Pelletier, J.D., et al. (2016). A gridded global data set of soil, intact regolith, and sedimentary deposit thicknesses for regional and global land surface modeling. *Journal of Advances in Modeling Earth Systems*, 8(1), 41-65.

**Access**:
- Original data: [ORNL DAAC](https://daac.ornl.gov/SOILS/guides/Global_Soil_Regolith_Sediment.html)
- The script uses a pre-processed version uploaded to Google Earth Engine as a custom asset

**If DTB is unavailable**:
- Contact the script authors for asset access
- Use an alternative depth to bedrock dataset
- Comment out Section 7 if not needed for your application

---

## GEE Code
```javascript
//// ============================================================================
//// HYDROLOGICAL DATABASE EXPORT FOR UNION OF HYDROBASINS
//// Author........: Marcus Nobrega, PhD
//// Stanford University
//// Adapted.......: 2026
//// Purpose.......: Export DEM, LULC, SOIL, DTB, Albedo, LAI, and WorldPop for
////                 the union of multiple HydroBASINS catchments selected by HYBAS_ID.
////                 Also export:
////                   1) a domain summary CSV log
////                   2) a per-catchment CSV log with catchment IDs/attributes/stats
////
//// Notes:
//// - User specifies HydroBASINS level and a list of HYBAS_IDs
//// - Outputs are clipped to the union of selected catchments
//// - Filenames are simplified: DEM, LULC, SOIL, DTB, Albedo, LAI, WorldPop
//// - Summary logs are computed at coarser scale to avoid memory errors
//// ============================================================================


//// ============================================================================
//// SECTION 1: USER INPUTS
//// ============================================================================

// -----------------------------
// HydroBASINS level to use
// Examples: 7, 8, 9, ...
// -----------------------------
var hybasLevel = 6;

// -----------------------------
// List of HYBAS_ID values to merge
// Replace with your own IDs
// -----------------------------
var catchmentIds = [
  4060922650,
  4060953900,
  4060952550,
  4060954060
];


// -----------------------------
// Output folder name in Google Drive
// -----------------------------
var Folder_Name = 'Domain_India';

// -----------------------------
// Export scale (m) for rasters
// -----------------------------
var scale_of_image = 90;

// -----------------------------
// Coarser scales for summary logs
// -----------------------------
var scale_stats_continuous = 250;   // DEM, DTB, Albedo, LAI, Impervious
var scale_stats_categorical = 250;  // LULC, SOIL
var scale_stats_population = 100;   // WorldPop

// -----------------------------
// Date range for time-dependent datasets
// -----------------------------
var startDate = '2015-01-01';
var endDate   = '2020-01-01';

// -----------------------------
// WorldPop year
// Available in EE for 2000–2020
// -----------------------------
var worldpopYear = 2020;

// -----------------------------
// Output CRS
// Recommended for California:
//   EPSG:3310 = California Albers
// -----------------------------
var crs = 'EPSG:3310';

// -----------------------------
var noDataValue = -9999;
var mapZoom = 8;


//// ============================================================================
//// SECTION 2: LOAD HYDROBASINS AND BUILD UNION GEOMETRY
//// ============================================================================

// Build HydroBASINS asset path dynamically
var hybasPath = 'WWF/HydroSHEDS/v1/Basins/hybas_' + hybasLevel;

// Load HydroBASINS
var hybas = ee.FeatureCollection(hybasPath);

// Filter selected catchments
var catchments = hybas.filter(ee.Filter.inList('HYBAS_ID', catchmentIds));

// Dissolve into a single feature/geometry
var catchmentUnion = catchments.union(1);

// Alternatively, you can enter the shapefile of your catchment
// Simply change the variable named CatchmentUnion to the catchment you need

var geometry = catchmentUnion.geometry();

// Display
Map.centerObject(catchmentUnion, mapZoom);
Map.addLayer(catchments, {color: 'yellow'}, 'Selected HydroBASINS');
Map.addLayer(catchmentUnion, {color: 'red'}, 'Union Catchment');

// Print basic info
print('HydroBASINS level:', hybasLevel);
print('Selected HYBAS_IDs:', catchmentIds);
print('Selected catchments:', catchments);
print('Union area (km²):', geometry.area(1).divide(1e6));


//// ============================================================================
//// SECTION 3: EXPORT UNION CATCHMENT SHAPEFILE
//// ============================================================================

Export.table.toDrive({
  collection: catchmentUnion,
  description: 'Catchment_Union',
  folder: Folder_Name,
  fileNamePrefix: 'Catchment_Union',
  fileFormat: 'SHP'
});


//// ============================================================================
//// SECTION 4: DEM
//// Source: MERIT DEM
//// ============================================================================

var MERIT = ee.Image("MERIT/DEM/v1_0_3");
var DEM = MERIT.select('dem').rename('DEM').clip(geometry);

var demVis = {
  min: 0,
  max: 4000,
  palette: ['0000ff', '00ff00', 'ffff00', 'ff7f00', 'ff0000']
};

Map.addLayer(DEM, demVis, 'DEM');

Export.image.toDrive({
  image: DEM.unmask(noDataValue),
  description: 'DEM',
  folder: Folder_Name,
  fileNamePrefix: 'DEM',
  region: geometry,
  scale: scale_of_image,
  crs: crs,
  formatOptions: {noData: noDataValue},
  maxPixels: 1e13
});


//// ============================================================================
//// SECTION 5: LULC
//// Source: ESA/WorldCover/v100/2020
//// ============================================================================

var LULC = ee.Image('ESA/WorldCover/v100/2020')
  .select('Map')
  .rename('LULC')
  .clip(geometry);

var lulcVis = {
  min: 10,
  max: 100,
  palette: [
    '#006400',
    '#ffbb22',
    '#ffff4c',
    '#f096ff',
    '#fa0000',
    '#b4b4b4',
    '#f0f0f0',
    '#0064c8',
    '#0096a0',
    '#00cf75',
    '#fae6a0'
  ]
};

Map.addLayer(LULC, lulcVis, 'LULC');

Export.image.toDrive({
  image: LULC.unmask(noDataValue),
  description: 'LULC',
  folder: Folder_Name,
  fileNamePrefix: 'LULC',
  region: geometry,
  scale: scale_of_image,
  crs: crs,
  formatOptions: {noData: noDataValue},
  maxPixels: 1e13
});


//// ============================================================================
//// SECTION 6: SOIL
//// Source: OpenLandMap USDA texture class
//// ============================================================================

var SOIL = ee.Image("OpenLandMap/SOL/SOL_TEXTURE-CLASS_USDA-TT_M/v02")
  .select('b0')
  .rename('SOIL')
  .clip(geometry);

var soilVis = {
  min: 1,
  max: 12,
  palette: [
    'd5c36b', 'b96947', '9d3706', 'ae868f', 'f86714', '46d143',
    '368f20', '3e5a14', 'ffd557', 'fff72e', 'ff5a9d', 'ff005b'
  ]
};

Map.addLayer(SOIL, soilVis, 'SOIL');

Export.image.toDrive({
  image: SOIL.unmask(noDataValue),
  description: 'SOIL',
  folder: Folder_Name,
  fileNamePrefix: 'SOIL',
  region: geometry,
  scale: scale_of_image,
  crs: crs,
  formatOptions: {noData: noDataValue},
  maxPixels: 1e13
});


//// ============================================================================
//// SECTION 7: DEPTH TO BEDROCK (DTB)
//// Source: custom asset
//// ============================================================================

var DTB = ee.Image("projects/ee-marcusep2025/assets/Depth_to_bedrock")
  .rename('DTB')
  .clip(geometry);

var dtbVis = {
  min: 1,
  max: 50,
  palette: [
    'd5c36b', 'b96947', '9d3706', 'ae868f', 'f86714', '46d143',
    '368f20', '3e5a14', 'ffd557', 'fff72e', 'ff5a9d', 'ff005b'
  ]
};

Map.addLayer(DTB, dtbVis, 'DTB');

Export.image.toDrive({
  image: DTB.unmask(noDataValue),
  description: 'DTB',
  folder: Folder_Name,
  fileNamePrefix: 'DTB',
  region: geometry,
  scale: scale_of_image,
  crs: crs,
  formatOptions: {noData: noDataValue},
  maxPixels: 1e13
});


//// ============================================================================
//// SECTION 8: ALBEDO
//// Source: MODIS/061/MCD43A3
//// ============================================================================

var albedoCollection = ee.ImageCollection("MODIS/061/MCD43A3")
  .select('Albedo_BSA_shortwave')
  .filterDate(startDate, endDate);

var Albedo = albedoCollection
  .median()
  .multiply(0.001)
  .rename('Albedo')
  .clip(geometry);

var albedoVis = {
  min: 0,
  max: 0.5,
  palette: ['blue', 'white', 'yellow', 'red']
};

Map.addLayer(Albedo, albedoVis, 'Albedo');

Export.image.toDrive({
  image: Albedo.unmask(noDataValue),
  description: 'Albedo',
  folder: Folder_Name,
  fileNamePrefix: 'Albedo',
  region: geometry,
  scale: scale_of_image,
  crs: crs,
  formatOptions: {noData: noDataValue},
  maxPixels: 1e13
});


//// ============================================================================
//// SECTION 9: LEAF AREA INDEX (LAI)
//// Source: MODIS/061/MCD15A3H
//// Notes:
//// - MODIS LAI scaled by 0.1
//// - Median value over user-defined time range
//// ============================================================================

var laiCollection = ee.ImageCollection('MODIS/061/MCD15A3H')
  .select('Lai')
  .filterDate(startDate, endDate);

var LAI = laiCollection
  .median()
  .multiply(0.1)
  .rename('LAI')
  .clip(geometry);

var laiVis = {
  min: 0,
  max: 6,
  palette: ['red', 'yellow', 'green']
};

Map.addLayer(LAI, laiVis, 'LAI');

Export.image.toDrive({
  image: LAI.unmask(noDataValue),
  description: 'LAI',
  folder: Folder_Name,
  fileNamePrefix: 'LAI',
  region: geometry,
  scale: scale_of_image,
  crs: crs,
  formatOptions: {noData: noDataValue},
  maxPixels: 1e13
});


//// ============================================================================
//// SECTION 10: WORLDPOP
//// Source: WorldPop/GP/100m/pop
//// ============================================================================

var WorldPop = ee.ImageCollection("WorldPop/GP/100m/pop")
  .filter(ee.Filter.calendarRange(worldpopYear, worldpopYear, 'year'))
  .mosaic()
  .rename('WorldPop')
  .clip(geometry);

Map.addLayer(WorldPop, {
  min: 0,
  max: 100,
  palette: ['white', 'yellow', 'orange', 'red', 'darkred']
}, 'WorldPop ' + worldpopYear);

Export.image.toDrive({
  image: WorldPop.unmask(noDataValue),
  description: 'WorldPop',
  folder: Folder_Name,
  fileNamePrefix: 'WorldPop',
  region: geometry,
  scale: scale_of_image,
  crs: crs,
  formatOptions: {noData: noDataValue},
  maxPixels: 1e13
});


//// ============================================================================
//// SECTION 11: IMPERVIOUS RATE (for logs only)
//// Source: NLCD impervious (U.S.-only; appropriate for California)
//// ============================================================================

var Impervious = ee.ImageCollection("USGS/NLCD_RELEASES/2021_REL/NLCD")
  .select('impervious')
  .median()
  .rename('Impervious')
  .clip(geometry);

Map.addLayer(Impervious, {
  min: 0,
  max: 100,
  palette: ['white', 'pink', 'red', 'darkred']
}, 'Impervious (%)');


//// ============================================================================
//// SECTION 12: HELPER FUNCTIONS FOR STATS (MEMORY-SAFE)
//// ============================================================================

function reduceMean(image, geom, scale) {
  var band = ee.String(image.bandNames().get(0));
  var out = image.reduceRegion({
    reducer: ee.Reducer.mean(),
    geometry: geom,
    scale: scale,
    maxPixels: 1e13,
    bestEffort: true,
    tileScale: 4
  });
  return out.get(band);
}

function reduceSum(image, geom, scale) {
  var band = ee.String(image.bandNames().get(0));
  var out = image.reduceRegion({
    reducer: ee.Reducer.sum(),
    geometry: geom,
    scale: scale,
    maxPixels: 1e13,
    bestEffort: true,
    tileScale: 4
  });
  return out.get(band);
}

function reduceMode(image, geom, scale) {
  var band = ee.String(image.bandNames().get(0));
  var out = image.reduceRegion({
    reducer: ee.Reducer.mode(),
    geometry: geom,
    scale: scale,
    maxPixels: 1e13,
    bestEffort: true,
    tileScale: 4
  });
  return out.get(band);
}

function safeProp(feature, propName) {
  var props = feature.propertyNames();
  return ee.Algorithms.If(props.contains(propName), feature.get(propName), null);
}


//// ============================================================================
//// SECTION 13: DOMAIN SUMMARY LOG (CSV)
//// ============================================================================

var totalPopulation = reduceSum(WorldPop, geometry, scale_stats_population);
var meanImpervious = reduceMean(Impervious, geometry, scale_stats_continuous);
var area_km2 = geometry.area(1).divide(1e6);
var nCatchments = catchments.size();
var dominantLULC = reduceMode(LULC, geometry, scale_stats_categorical);
var dominantSOIL = reduceMode(SOIL, geometry, scale_stats_categorical);
var meanAlbedo = reduceMean(Albedo, geometry, scale_stats_continuous);
var meanElevation = reduceMean(DEM, geometry, scale_stats_continuous);
var meanDTB = reduceMean(DTB, geometry, scale_stats_continuous);
var meanLAI = reduceMean(LAI, geometry, scale_stats_continuous);

// Store catchment IDs as a string for traceability
var catchmentIdsString = ee.List(catchmentIds).join(';');

// Build one-row feature
var domainLogFeature = ee.Feature(null, {
  'folder_name': Folder_Name,
  'hybas_level': hybasLevel,
  'catchment_ids_used': catchmentIdsString,
  'number_of_catchments': nCatchments,
  'catchment_area_km2': area_km2,
  'population_in_domain': totalPopulation,
  'mean_impervious_rate_percent': meanImpervious,
  'dominant_LULC': dominantLULC,
  'dominant_SOIL': dominantSOIL,
  'avg_albedo': meanAlbedo,
  'mean_elevation_m': meanElevation,
  'mean_DTB_m': meanDTB,
  'mean_LAI': meanLAI,
  'worldpop_year': worldpopYear,
  'export_scale_m': scale_of_image,
  'crs': crs
});

var domainLogTable = ee.FeatureCollection([domainLogFeature]);

print('Domain summary log:', domainLogTable);

Export.table.toDrive({
  collection: domainLogTable,
  description: 'Domain_Log',
  folder: Folder_Name,
  fileNamePrefix: 'Domain_Log',
  fileFormat: 'CSV'
});


//// ============================================================================
//// SECTION 14: PER-CATCHMENT LOG (CSV)
//// ============================================================================

var catchmentLogTable = catchments.map(function(ft) {
  var g = ft.geometry();
  var areaLocal_km2 = g.area(1).divide(1e6);

  var domLULC_local = reduceMode(LULC, g, scale_stats_categorical);
  var domSOIL_local = reduceMode(SOIL, g, scale_stats_categorical);
  var meanAlb_local = reduceMean(Albedo, g, scale_stats_continuous);
  var meanDEM_local = reduceMean(DEM, g, scale_stats_continuous);
  var meanDTB_local = reduceMean(DTB, g, scale_stats_continuous);
  var meanLAI_local = reduceMean(LAI, g, scale_stats_continuous);
  var pop_local = reduceSum(WorldPop, g, scale_stats_population);
  var imp_local = reduceMean(Impervious, g, scale_stats_continuous);

  return ee.Feature(null, {
    'HYBAS_ID': safeProp(ft, 'HYBAS_ID'),
    'MAIN_BAS': safeProp(ft, 'MAIN_BAS'),
    'NEXT_DOWN': safeProp(ft, 'NEXT_DOWN'),
    'UP_AREA': safeProp(ft, 'UP_AREA'),
    'SUB_AREA': safeProp(ft, 'SUB_AREA'),
    'PFAF_ID': safeProp(ft, 'PFAF_ID'),
    'ENDO': safeProp(ft, 'ENDO'),
    'COAST': safeProp(ft, 'COAST'),
    'catchment_area_km2': areaLocal_km2,
    'population': pop_local,
    'mean_impervious_rate_percent': imp_local,
    'dominant_LULC': domLULC_local,
    'dominant_SOIL': domSOIL_local,
    'avg_albedo': meanAlb_local,
    'mean_elevation_m': meanDEM_local,
    'mean_DTB_m': meanDTB_local,
    'mean_LAI': meanLAI_local
  });
});

print('Per-catchment log:', catchmentLogTable);

Export.table.toDrive({
  collection: catchmentLogTable,
  description: 'Catchment_Log',
  folder: Folder_Name,
  fileNamePrefix: 'Catchment_Log',
  fileFormat: 'CSV'
});


//// ============================================================================
//// SECTION 15: OPTIONAL PRINTED SUMMARY
//// ============================================================================

function computeMeanPrint(image, name, scale) {
  var stats = image.reduceRegion({
    reducer: ee.Reducer.mean(),
    geometry: geometry,
    scale: scale,
    maxPixels: 1e13,
    bestEffort: true,
    tileScale: 4
  });
  print(name + ' mean:', stats);
}

function computeSumPrint(image, name, scale) {
  var stats = image.reduceRegion({
    reducer: ee.Reducer.sum(),
    geometry: geometry,
    scale: scale,
    maxPixels: 1e13,
    bestEffort: true,
    tileScale: 4
  });
  print(name + ' sum:', stats);
}

function computeModePrint(image, name, scale) {
  var stats = image.reduceRegion({
    reducer: ee.Reducer.mode(),
    geometry: geometry,
    scale: scale,
    maxPixels: 1e13,
    bestEffort: true,
    tileScale: 4
  });
  print(name + ' mode:', stats);
}

computeMeanPrint(DEM, 'DEM', scale_stats_continuous);
computeModePrint(LULC, 'LULC', scale_stats_categorical);
computeModePrint(SOIL, 'SOIL', scale_stats_categorical);
computeMeanPrint(DTB, 'DTB', scale_stats_continuous);
computeMeanPrint(Albedo, 'Albedo', scale_stats_continuous);
computeMeanPrint(LAI, 'LAI', scale_stats_continuous);
computeMeanPrint(Impervious, 'Impervious (%)', scale_stats_continuous);
computeSumPrint(WorldPop, 'Total WorldPop', scale_stats_population);

## GEE Code
```javascript
//// ============================================================================
//// HYDROLOGICAL DATABASE EXPORT FOR UNION OF HYDROBASINS
//// Author........: Marcus Nobrega, PhD
//// Stanford University
//// Adapted.......: 2026
//// Purpose.......: Export DEM, LULC, SOIL, DTB, Albedo, LAI, and WorldPop for
////                 the union of multiple HydroBASINS catchments selected by HYBAS_ID.
////                 Also export:
////                   1) a domain summary CSV log
////                   2) a per-catchment CSV log with catchment IDs/attributes/stats
////
//// Notes:
//// - User specifies HydroBASINS level and a list of HYBAS_IDs
//// - Outputs are clipped to the union of selected catchments
//// - Filenames are simplified: DEM, LULC, SOIL, DTB, Albedo, LAI, WorldPop
//// - Summary logs are computed at coarser scale to avoid memory errors
//// ============================================================================


//// ============================================================================
//// SECTION 1: USER INPUTS
//// ============================================================================

// -----------------------------
// HydroBASINS level to use
// Examples: 7, 8, 9, ...
// -----------------------------
var hybasLevel = 6;

// -----------------------------
// List of HYBAS_ID values to merge
// Replace with your own IDs
// -----------------------------
var catchmentIds = [
  4060922650,
  4060953900,
  4060952550,
  4060954060
];


// -----------------------------
// Output folder name in Google Drive
// -----------------------------
var Folder_Name = 'Domain_India';

// -----------------------------
// Export scale (m) for rasters
// -----------------------------
var scale_of_image = 90;

// -----------------------------
// Coarser scales for summary logs
// -----------------------------
var scale_stats_continuous = 250;   // DEM, DTB, Albedo, LAI, Impervious
var scale_stats_categorical = 250;  // LULC, SOIL
var scale_stats_population = 100;   // WorldPop

// -----------------------------
// Date range for time-dependent datasets
// -----------------------------
var startDate = '2015-01-01';
var endDate   = '2020-01-01';

// -----------------------------
// WorldPop year
// Available in EE for 2000–2020
// -----------------------------
var worldpopYear = 2020;

// -----------------------------
// Output CRS
// Recommended for California:
//   EPSG:3310 = California Albers
// -----------------------------
var crs = 'EPSG:3310';

// -----------------------------
var noDataValue = -9999;
var mapZoom = 8;


//// ============================================================================
//// SECTION 2: LOAD HYDROBASINS AND BUILD UNION GEOMETRY
//// ============================================================================

// Build HydroBASINS asset path dynamically
var hybasPath = 'WWF/HydroSHEDS/v1/Basins/hybas_' + hybasLevel;

// Load HydroBASINS
var hybas = ee.FeatureCollection(hybasPath);

// Filter selected catchments
var catchments = hybas.filter(ee.Filter.inList('HYBAS_ID', catchmentIds));

// Dissolve into a single feature/geometry
var catchmentUnion = catchments.union(1);

// Alternatively, you can enter the shapefile of your catchment
// Simply change the variable named CatchmentUnion to the catchment you need

var geometry = catchmentUnion.geometry();

// Display
Map.centerObject(catchmentUnion, mapZoom);
Map.addLayer(catchments, {color: 'yellow'}, 'Selected HydroBASINS');
Map.addLayer(catchmentUnion, {color: 'red'}, 'Union Catchment');

// Print basic info
print('HydroBASINS level:', hybasLevel);
print('Selected HYBAS_IDs:', catchmentIds);
print('Selected catchments:', catchments);
print('Union area (km²):', geometry.area(1).divide(1e6));


//// ============================================================================
//// SECTION 3: EXPORT UNION CATCHMENT SHAPEFILE
//// ============================================================================

Export.table.toDrive({
  collection: catchmentUnion,
  description: 'Catchment_Union',
  folder: Folder_Name,
  fileNamePrefix: 'Catchment_Union',
  fileFormat: 'SHP'
});


//// ============================================================================
//// SECTION 4: DEM
//// Source: MERIT DEM
//// ============================================================================

var MERIT = ee.Image("MERIT/DEM/v1_0_3");
var DEM = MERIT.select('dem').rename('DEM').clip(geometry);

var demVis = {
  min: 0,
  max: 4000,
  palette: ['0000ff', '00ff00', 'ffff00', 'ff7f00', 'ff0000']
};

Map.addLayer(DEM, demVis, 'DEM');

Export.image.toDrive({
  image: DEM.unmask(noDataValue),
  description: 'DEM',
  folder: Folder_Name,
  fileNamePrefix: 'DEM',
  region: geometry,
  scale: scale_of_image,
  crs: crs,
  formatOptions: {noData: noDataValue},
  maxPixels: 1e13
});


//// ============================================================================
//// SECTION 5: LULC
//// Source: ESA/WorldCover/v100/2020
//// ============================================================================

var LULC = ee.Image('ESA/WorldCover/v100/2020')
  .select('Map')
  .rename('LULC')
  .clip(geometry);

var lulcVis = {
  min: 10,
  max: 100,
  palette: [
    '#006400',
    '#ffbb22',
    '#ffff4c',
    '#f096ff',
    '#fa0000',
    '#b4b4b4',
    '#f0f0f0',
    '#0064c8',
    '#0096a0',
    '#00cf75',
    '#fae6a0'
  ]
};

Map.addLayer(LULC, lulcVis, 'LULC');

Export.image.toDrive({
  image: LULC.unmask(noDataValue),
  description: 'LULC',
  folder: Folder_Name,
  fileNamePrefix: 'LULC',
  region: geometry,
  scale: scale_of_image,
  crs: crs,
  formatOptions: {noData: noDataValue},
  maxPixels: 1e13
});


//// ============================================================================
//// SECTION 6: SOIL
//// Source: OpenLandMap USDA texture class
//// ============================================================================

var SOIL = ee.Image("OpenLandMap/SOL/SOL_TEXTURE-CLASS_USDA-TT_M/v02")
  .select('b0')
  .rename('SOIL')
  .clip(geometry);

var soilVis = {
  min: 1,
  max: 12,
  palette: [
    'd5c36b', 'b96947', '9d3706', 'ae868f', 'f86714', '46d143',
    '368f20', '3e5a14', 'ffd557', 'fff72e', 'ff5a9d', 'ff005b'
  ]
};

Map.addLayer(SOIL, soilVis, 'SOIL');

Export.image.toDrive({
  image: SOIL.unmask(noDataValue),
  description: 'SOIL',
  folder: Folder_Name,
  fileNamePrefix: 'SOIL',
  region: geometry,
  scale: scale_of_image,
  crs: crs,
  formatOptions: {noData: noDataValue},
  maxPixels: 1e13
});


//// ============================================================================
//// SECTION 7: DEPTH TO BEDROCK (DTB)
//// Source: custom asset
//// ============================================================================

var DTB = ee.Image("projects/ee-marcusep2025/assets/Depth_to_bedrock")
  .rename('DTB')
  .clip(geometry);

var dtbVis = {
  min: 1,
  max: 50,
  palette: [
    'd5c36b', 'b96947', '9d3706', 'ae868f', 'f86714', '46d143',
    '368f20', '3e5a14', 'ffd557', 'fff72e', 'ff5a9d', 'ff005b'
  ]
};

Map.addLayer(DTB, dtbVis, 'DTB');

Export.image.toDrive({
  image: DTB.unmask(noDataValue),
  description: 'DTB',
  folder: Folder_Name,
  fileNamePrefix: 'DTB',
  region: geometry,
  scale: scale_of_image,
  crs: crs,
  formatOptions: {noData: noDataValue},
  maxPixels: 1e13
});


//// ============================================================================
//// SECTION 8: ALBEDO
//// Source: MODIS/061/MCD43A3
//// ============================================================================

var albedoCollection = ee.ImageCollection("MODIS/061/MCD43A3")
  .select('Albedo_BSA_shortwave')
  .filterDate(startDate, endDate);

var Albedo = albedoCollection
  .median()
  .multiply(0.001)
  .rename('Albedo')
  .clip(geometry);

var albedoVis = {
  min: 0,
  max: 0.5,
  palette: ['blue', 'white', 'yellow', 'red']
};

Map.addLayer(Albedo, albedoVis, 'Albedo');

Export.image.toDrive({
  image: Albedo.unmask(noDataValue),
  description: 'Albedo',
  folder: Folder_Name,
  fileNamePrefix: 'Albedo',
  region: geometry,
  scale: scale_of_image,
  crs: crs,
  formatOptions: {noData: noDataValue},
  maxPixels: 1e13
});


//// ============================================================================
//// SECTION 9: LEAF AREA INDEX (LAI)
//// Source: MODIS/061/MCD15A3H
//// Notes:
//// - MODIS LAI scaled by 0.1
//// - Median value over user-defined time range
//// ============================================================================

var laiCollection = ee.ImageCollection('MODIS/061/MCD15A3H')
  .select('Lai')
  .filterDate(startDate, endDate);

var LAI = laiCollection
  .median()
  .multiply(0.1)
  .rename('LAI')
  .clip(geometry);

var laiVis = {
  min: 0,
  max: 6,
  palette: ['red', 'yellow', 'green']
};

Map.addLayer(LAI, laiVis, 'LAI');

Export.image.toDrive({
  image: LAI.unmask(noDataValue),
  description: 'LAI',
  folder: Folder_Name,
  fileNamePrefix: 'LAI',
  region: geometry,
  scale: scale_of_image,
  crs: crs,
  formatOptions: {noData: noDataValue},
  maxPixels: 1e13
});


//// ============================================================================
//// SECTION 10: WORLDPOP
//// Source: WorldPop/GP/100m/pop
//// ============================================================================

var WorldPop = ee.ImageCollection("WorldPop/GP/100m/pop")
  .filter(ee.Filter.calendarRange(worldpopYear, worldpopYear, 'year'))
  .mosaic()
  .rename('WorldPop')
  .clip(geometry);

Map.addLayer(WorldPop, {
  min: 0,
  max: 100,
  palette: ['white', 'yellow', 'orange', 'red', 'darkred']
}, 'WorldPop ' + worldpopYear);

Export.image.toDrive({
  image: WorldPop.unmask(noDataValue),
  description: 'WorldPop',
  folder: Folder_Name,
  fileNamePrefix: 'WorldPop',
  region: geometry,
  scale: scale_of_image,
  crs: crs,
  formatOptions: {noData: noDataValue},
  maxPixels: 1e13
});


//// ============================================================================
//// SECTION 11: IMPERVIOUS RATE (for logs only)
//// Source: NLCD impervious (U.S.-only; appropriate for California)
//// ============================================================================

var Impervious = ee.ImageCollection("USGS/NLCD_RELEASES/2021_REL/NLCD")
  .select('impervious')
  .median()
  .rename('Impervious')
  .clip(geometry);

Map.addLayer(Impervious, {
  min: 0,
  max: 100,
  palette: ['white', 'pink', 'red', 'darkred']
}, 'Impervious (%)');


//// ============================================================================
//// SECTION 12: HELPER FUNCTIONS FOR STATS (MEMORY-SAFE)
//// ============================================================================

function reduceMean(image, geom, scale) {
  var band = ee.String(image.bandNames().get(0));
  var out = image.reduceRegion({
    reducer: ee.Reducer.mean(),
    geometry: geom,
    scale: scale,
    maxPixels: 1e13,
    bestEffort: true,
    tileScale: 4
  });
  return out.get(band);
}

function reduceSum(image, geom, scale) {
  var band = ee.String(image.bandNames().get(0));
  var out = image.reduceRegion({
    reducer: ee.Reducer.sum(),
    geometry: geom,
    scale: scale,
    maxPixels: 1e13,
    bestEffort: true,
    tileScale: 4
  });
  return out.get(band);
}

function reduceMode(image, geom, scale) {
  var band = ee.String(image.bandNames().get(0));
  var out = image.reduceRegion({
    reducer: ee.Reducer.mode(),
    geometry: geom,
    scale: scale,
    maxPixels: 1e13,
    bestEffort: true,
    tileScale: 4
  });
  return out.get(band);
}

function safeProp(feature, propName) {
  var props = feature.propertyNames();
  return ee.Algorithms.If(props.contains(propName), feature.get(propName), null);
}


//// ============================================================================
//// SECTION 13: DOMAIN SUMMARY LOG (CSV)
//// ============================================================================

var totalPopulation = reduceSum(WorldPop, geometry, scale_stats_population);
var meanImpervious = reduceMean(Impervious, geometry, scale_stats_continuous);
var area_km2 = geometry.area(1).divide(1e6);
var nCatchments = catchments.size();
var dominantLULC = reduceMode(LULC, geometry, scale_stats_categorical);
var dominantSOIL = reduceMode(SOIL, geometry, scale_stats_categorical);
var meanAlbedo = reduceMean(Albedo, geometry, scale_stats_continuous);
var meanElevation = reduceMean(DEM, geometry, scale_stats_continuous);
var meanDTB = reduceMean(DTB, geometry, scale_stats_continuous);
var meanLAI = reduceMean(LAI, geometry, scale_stats_continuous);

// Store catchment IDs as a string for traceability
var catchmentIdsString = ee.List(catchmentIds).join(';');

// Build one-row feature
var domainLogFeature = ee.Feature(null, {
  'folder_name': Folder_Name,
  'hybas_level': hybasLevel,
  'catchment_ids_used': catchmentIdsString,
  'number_of_catchments': nCatchments,
  'catchment_area_km2': area_km2,
  'population_in_domain': totalPopulation,
  'mean_impervious_rate_percent': meanImpervious,
  'dominant_LULC': dominantLULC,
  'dominant_SOIL': dominantSOIL,
  'avg_albedo': meanAlbedo,
  'mean_elevation_m': meanElevation,
  'mean_DTB_m': meanDTB,
  'mean_LAI': meanLAI,
  'worldpop_year': worldpopYear,
  'export_scale_m': scale_of_image,
  'crs': crs
});

var domainLogTable = ee.FeatureCollection([domainLogFeature]);

print('Domain summary log:', domainLogTable);

Export.table.toDrive({
  collection: domainLogTable,
  description: 'Domain_Log',
  folder: Folder_Name,
  fileNamePrefix: 'Domain_Log',
  fileFormat: 'CSV'
});


//// ============================================================================
//// SECTION 14: PER-CATCHMENT LOG (CSV)
//// ============================================================================

var catchmentLogTable = catchments.map(function(ft) {
  var g = ft.geometry();
  var areaLocal_km2 = g.area(1).divide(1e6);

  var domLULC_local = reduceMode(LULC, g, scale_stats_categorical);
  var domSOIL_local = reduceMode(SOIL, g, scale_stats_categorical);
  var meanAlb_local = reduceMean(Albedo, g, scale_stats_continuous);
  var meanDEM_local = reduceMean(DEM, g, scale_stats_continuous);
  var meanDTB_local = reduceMean(DTB, g, scale_stats_continuous);
  var meanLAI_local = reduceMean(LAI, g, scale_stats_continuous);
  var pop_local = reduceSum(WorldPop, g, scale_stats_population);
  var imp_local = reduceMean(Impervious, g, scale_stats_continuous);

  return ee.Feature(null, {
    'HYBAS_ID': safeProp(ft, 'HYBAS_ID'),
    'MAIN_BAS': safeProp(ft, 'MAIN_BAS'),
    'NEXT_DOWN': safeProp(ft, 'NEXT_DOWN'),
    'UP_AREA': safeProp(ft, 'UP_AREA'),
    'SUB_AREA': safeProp(ft, 'SUB_AREA'),
    'PFAF_ID': safeProp(ft, 'PFAF_ID'),
    'ENDO': safeProp(ft, 'ENDO'),
    'COAST': safeProp(ft, 'COAST'),
    'catchment_area_km2': areaLocal_km2,
    'population': pop_local,
    'mean_impervious_rate_percent': imp_local,
    'dominant_LULC': domLULC_local,
    'dominant_SOIL': domSOIL_local,
    'avg_albedo': meanAlb_local,
    'mean_elevation_m': meanDEM_local,
    'mean_DTB_m': meanDTB_local,
    'mean_LAI': meanLAI_local
  });
});

print('Per-catchment log:', catchmentLogTable);

Export.table.toDrive({
  collection: catchmentLogTable,
  description: 'Catchment_Log',
  folder: Folder_Name,
  fileNamePrefix: 'Catchment_Log',
  fileFormat: 'CSV'
});


//// ============================================================================
//// SECTION 15: OPTIONAL PRINTED SUMMARY
//// ============================================================================

function computeMeanPrint(image, name, scale) {
  var stats = image.reduceRegion({
    reducer: ee.Reducer.mean(),
    geometry: geometry,
    scale: scale,
    maxPixels: 1e13,
    bestEffort: true,
    tileScale: 4
  });
  print(name + ' mean:', stats);
}

function computeSumPrint(image, name, scale) {
  var stats = image.reduceRegion({
    reducer: ee.Reducer.sum(),
    geometry: geometry,
    scale: scale,
    maxPixels: 1e13,
    bestEffort: true,
    tileScale: 4
  });
  print(name + ' sum:', stats);
}

function computeModePrint(image, name, scale) {
  var stats = image.reduceRegion({
    reducer: ee.Reducer.mode(),
    geometry: geometry,
    scale: scale,
    maxPixels: 1e13,
    bestEffort: true,
    tileScale: 4
  });
  print(name + ' mode:', stats);
}

computeMeanPrint(DEM, 'DEM', scale_stats_continuous);
computeModePrint(LULC, 'LULC', scale_stats_categorical);
computeModePrint(SOIL, 'SOIL', scale_stats_categorical);
computeMeanPrint(DTB, 'DTB', scale_stats_continuous);
computeMeanPrint(Albedo, 'Albedo', scale_stats_continuous);
computeMeanPrint(LAI, 'LAI', scale_stats_continuous);
computeMeanPrint(Impervious, 'Impervious (%)', scale_stats_continuous);
computeSumPrint(WorldPop, 'Total WorldPop', scale_stats_population);