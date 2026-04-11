---
title: Overview
---

# Model Inputs

HydroPol2D requires a combination of spatial datasets and tabular parameter files to define the simulation domain, physical properties, and boundary conditions.

The model is designed to work with raster-based inputs and structured configuration files, enabling flexible setup across a wide range of hydrological applications.

---

## Required Inputs

The following inputs are typically required to run a simulation:

### 1. Digital Elevation Model (DEM)

The DEM defines the topography of the domain and controls:

- Flow directions  
- Surface gradients  
- Watershed boundaries  

High-resolution DEMs are recommended to accurately represent terrain-driven flow processes.

---

### 2. Land Use / Land Cover (LULC)

The LULC map is used to assign spatially distributed parameters such as:

- Manning’s roughness coefficient  
- Interception capacity  
- Impervious fraction  

Each land use class must be linked to parameter values in the input tables.

---

### 3. Soil Properties

Soil maps define hydraulic properties including:

- Saturated hydraulic conductivity  
- Soil water retention characteristics  
- Infiltration capacity  

These parameters control infiltration and subsurface flow dynamics.

---

### 4. Parameter Tables (Excel Files)

HydroPol2D uses structured Excel files to define:

- Land use parameters  
- Soil hydraulic parameters  
- Model configuration flags  
- Boundary conditions  

These tables provide flexibility and allow users to modify model behavior without changing the source code.

---

## Optional Inputs

Depending on the simulation setup, additional inputs may be required:

### Rainfall Data

- Lumped rainfall time series  
- Spatially distributed rainfall maps  
- Satellite-based rainfall products  

---

### Evapotranspiration (ETP)

- Time series inputs  
- Spatial raster maps  

---

### Inflow Hydrographs

Used to define boundary inflows at specific locations.

---

### Reservoir and Dam Data

Required for:

- Reservoir operations  
- Dam-break simulations  

---

### Water Quality Inputs

For pollutant transport simulations:

- Initial concentrations  
- Build-up and wash-off parameters  

---

## Data Preparation Guidelines

To ensure consistent model performance:

- All rasters must share the same spatial resolution and coordinate system  
- Missing values should be handled prior to simulation  
- Units must be consistent across all inputs  
- Domain boundaries should be clearly defined  

---

## Summary

HydroPol2D relies on a structured combination of spatial and tabular inputs to represent hydrological processes in a physically consistent manner.

Proper preparation and validation of these inputs are critical for obtaining reliable simulation results.