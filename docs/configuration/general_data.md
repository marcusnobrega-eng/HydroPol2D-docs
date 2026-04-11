---
title: Configuration Parameters
---

# Configuration Parameters

This page documents all variables defined in `General_Data.xlsx`.

Each parameter controls a specific aspect of HydroPol2D, including:

- simulation timing  
- numerical stability  
- hydrological processes  
- hydraulic routing  
- input datasets  
- output control  

---

## Running Control

| Variable | Units | Description |
|----------|------|-------------|
| $\mathrm{time\_step\_model}$ | $\mathrm{s}$ | Initial model time step used in the simulation |
| $\mathrm{min\_time\_step}$ | $\mathrm{s}$ | Minimum allowable adaptive time step for numerical stability |
| $\mathrm{max\_time\_step}$ | $\mathrm{s}$ | Maximum allowable adaptive time step |
| $\mathrm{time\_step\_change}$ | $\mathrm{s}$ | Increment used to adjust the adaptive time step |
| $\alpha_{\min}$ | — | Minimum Courant-like stability coefficient |
| $\alpha_{\max}$ | — | Maximum Courant-like stability coefficient |
| $\mathrm{date\_begin}$ | — | Simulation start date and time |
| $\mathrm{date\_end}$ | — | Simulation end date and time |

---

## Normal Flow Boundary Condition

| Variable | Units | Description |
|----------|------|-------------|
| $\mathrm{slope\_outlet}$ | $\mathrm{m\,m^{-1}}$ | Prescribed slope used to estimate normal flow conditions at the outlet boundary |

---

## Maps and Plots Control

| Variable | Units | Description |
|----------|------|-------------|
| $\mathrm{record\_time\_maps}$ | $\mathrm{min}$ | Time interval for saving raster outputs |
| $\mathrm{record\_time\_hydrographs}$ | $\mathrm{min}$ | Time interval for saving hydrograph outputs |
| $\mathrm{Pol\_min}$ | $\mathrm{mg\,L^{-1}}$ | Minimum pollutant concentration threshold for visualization |
| $\mathrm{depth\_wse}$ | $\mathrm{m}$ | Threshold depth used to define water surface elevation outputs |
| $\mathrm{flag\_wse}$ | — | Flag to activate water surface elevation outputs instead of depth |
| $\mathrm{record\_time\_spatial\_rainfall}$ | $\mathrm{min}$ | Time interval for exporting spatial rainfall maps |
| $\mathrm{time\_save\_ETP}$ | $\mathrm{min}$ | Time interval for saving evapotranspiration outputs |
| $\mathrm{record\_time\_spatial\_ETP}$ | $\mathrm{min}$ | Time interval for exporting spatial ETP fields |

---

## River Geometry Parameters
If `flag_reduce_dem` is activated, river cells elevation are reduced to account for river bathymetry. A set of 4 parameters are then required to describe the flow width and depth. These parameters are valid to convert flow accumulation area [$\mathrm{km^2}$] into flow depth [$\mathrm{m}$] and width [$\mathrm{m}$].
| Variable | Units | Description |
|----------|------|-------------|
| $\alpha_1$ | — | Empirical coefficient controlling channel geometry scaling |
| $\alpha_2$ | — | Secondary coefficient for hydraulic geometry relationships |
| $\beta_1$ | — | Exponent controlling width or hydraulic scaling behavior |
| $\beta_2$ | — | Secondary exponent for hydraulic scaling relationships |
| $n$ | $\mathrm{s\,m^{-1/3}}$ | Manning’s roughness coefficient for channel and surface flow |

---

## Water Quality Inputs

| Variable | Units | Description |
|----------|------|-------------|
| $\mathrm{ADD}$ | $\mathrm{days}$ | Antecedent dry days used in pollutant buildup modeling |
| $\mathrm{min\_Bt}$ | $\mathrm{g\,m^{-2}}$ | Minimum pollutant buildup threshold |
| $\mathrm{Bmin}$ | $\mathrm{g\,m^{-2}}$ | Minimum allowable pollutant mass |
| $\mathrm{Bmax}$ | $\mathrm{g\,m^{-2}}$ | Maximum pollutant buildup capacity |

---

## DEM Processing and Terrain Controls

| Variable | Units | Description |
|----------|------|-------------|
| $\mathrm{min\_area}$ | $\mathrm{km^2}$ | Minimum drainage area threshold for channel initiation |
| $\tau$ | — | Smoothing parameter controlling DEM filtering intensity |
| $\mathrm{K\_value}$ | — | Parameter controlling terrain processing or hydraulic scaling |
| $\mathrm{sl}$ | $\mathrm{m\,m^{-1}}$ | Minimum slope threshold used in DEM conditioning |
| $\mathrm{resolution\_resample}$ | $\mathrm{m}$ | Target resolution for DEM resampling |
| $\mathrm{slope\_DTM}$ | $\%$ | Slope threshold used for terrain correction or filtering |

---

## File Paths and Input Data

| Variable | Units | Description |
|----------|------|-------------|
| $\mathrm{topo\_path}$ | — | Path to TopoToolbox directory |
| $\mathrm{DEM\_path}$ | — | Path to Digital Elevation Model |
| $\mathrm{LULC\_path}$ | — | Path to Land Use / Land Cover raster |
| $\mathrm{SOIL\_path}$ | — | Path to soil classification raster |
| $\mathrm{Warmup\_Depth\_path}$ | — | Path to initial warm-up water depth condition |
| $\mathrm{Initial\_Buildup\_path}$ | — | Path to initial pollutant buildup map |
| $\mathrm{Initial\_Soil\_Moisture\_path}$ | — | Path to initial soil moisture condition |
| $\mathrm{Albedo\_path}$ | — | Path to albedo raster |
| $\mathrm{LAI\_path}$ | — | Path to leaf area index raster |
| $\mathrm{RiverWidths\_path}$ | — | Path to river width raster |
| $\mathrm{RiverDepths\_path}$ | — | Path to river depth raster |
| $\mathrm{DTB\_path}$ | — | Path to depth-to-bedrock raster |
| $\mathrm{B1\_path}$ | — | Path to pollutant-related parameter raster |
| $\mathrm{B2\_path}$ | — | Path to pollutant-related parameter raster |
| $\mathrm{W1\_path}$ | — | Path to pollutant wash-off parameter raster |
| $\mathrm{W2\_path}$ | — | Path to pollutant wash-off parameter raster |
| $\mathrm{Subgrid\_DEM\_path}$ | — | Path to high-resolution DEM for subgrid computations |
| $\mathrm{hydropol2d\_tools}$ | — | Path to HydroPol2D function library |

---

## Human Instability Parameters

| Variable | Units | Description |
|----------|------|-------------|
| $\mu$ | — | Friction coefficient between human body and ground |
| $C_d$ | — | Drag coefficient for human body in flow |
| $\rho_{\mathrm{person}}$ | $\mathrm{kg\,m^{-3}}$ | Density of human body |
| $\mathrm{weight\_person}$ | $\mathrm{kg}$ | Average human weight |
| $\mathrm{height\_person}$ | $\mathrm{m}$ | Average human height |
| $\mathrm{width1\_person}$ | $\mathrm{m}$ | Characteristic frontal width |
| $\mathrm{width2\_person}$ | $\mathrm{m}$ | Secondary width parameter |
| $\rho_{\mathrm{water}}$ | $\mathrm{kg\,m^{-3}}$ | Density of water |
| $g$ | $\mathrm{m\,s^{-2}}$ | Gravitational acceleration |

---

## Observation Points

| Variable | Units | Description |
|----------|------|-------------|
| $\mathrm{Gauge}$ | — | Gauge identifier |
| $\mathrm{Easting}$ | $\mathrm{m}$ | Easting coordinate |
| $\mathrm{Northing}$ | $\mathrm{m}$ | Northing coordinate |
| $\mathrm{Label\ Name}$ | — | Output label for time series |

---

## Design Storm Parameters

| Variable | Units | Description |
|----------|------|-------------|
| $\mathrm{RP}$ | $\mathrm{years}$ | Return period of design storm |
| $\mathrm{Rainfall\ Duration}$ | $\mathrm{min}$ | Total storm duration |
| $K$ | — | Intensity–duration–frequency coefficient |
| $a$ | — | IDF curve parameter |
| $b$ | — | IDF curve parameter |
| $c$ | — | IDF curve parameter |
| $\mathrm{dt\_design}$ | $\mathrm{min}$ | Time resolution of synthetic storm |

---

## Satellite or Radar Rainfall

| Variable | Units | Description |
|----------|------|-------------|
| $\mathrm{Time}$ | $\mathrm{min}$ | Time step of rainfall raster |
| $\mathrm{Raster\ Directory}$ | — | Path to rainfall raster files |

---

## Satellite Transpiration

| Variable | Units | Description |
|----------|------|-------------|
| $\mathrm{Time}$ | $\mathrm{day}$ | Time index for transpiration data |
| $\mathrm{Raster\ Directory}$ | — | Path to transpiration rasters |

---

## Satellite Evaporation

| Variable | Units | Description |
|----------|------|-------------|
| $\mathrm{Time}$ | $\mathrm{day}$ | Time index for evaporation data |
| $\mathrm{Raster\ Directory}$ | — | Path to evaporation rasters |

---

## Notes

The descriptions provided here represent the functional role of each parameter within HydroPol2D.

Final definitions should be refined based on:

- spreadsheet comments  
- calibration strategy  
- application context  

This table serves as the central reference for model configuration.