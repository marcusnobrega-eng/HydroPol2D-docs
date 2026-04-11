---
title: Overview
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

Click on **“Sign Up”** and register using a Google account.

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
- Mean impervious fraction  

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

## Next steps

The following sections describe how to configure the script and export each dataset step by step.