---
title: Overview
---

# Model Inputs

HydroPol2D uses a combination of raster inputs, spreadsheet tables, and forcing files. This page is the entry point for the file-based inputs that the current model can read.

## Core spatial inputs

Most runs start from three required rasters:

1. [DEM](./dem)
2. [LULC](./lulc)
3. [Soil](./soil)

These define the model grid, the land-surface classes, and the base soil hydraulic properties.

## Supplemental spatial inputs

Additional rasters are used when the selected workflow needs them:

- [DTB](./dtb) for soil depth or depth to bedrock;
- [LAI](./lai) for spatial vegetation structure;
- [Albedo](./albedo) for spatial surface-energy properties;
- [Additional Spatial Inputs](./additional-spatial-inputs) for initial groundwater, impervious fraction, warmup states, and water-quality rasters.

These inputs are optional by workflow, not experimental by default. They should be documented whenever they are active in a case study.

## Tabular and control inputs

HydroPol2D also reads spreadsheet-based inputs:

- the MATLAB case workbook `HydroPol2D_Inputs.xlsx`, whose settings tabs hold the switches, timing, file paths and runtime controls ([Case Workbook Settings](../configuration/general_data));
- its class-table tabs for land-use and soil classes, human instability, the mesh and control structures ([Parameter Tables](./parameter-tables));
- its series tabs for rainfall, climate stations, inflow and stage when those options are active ([Optional Forcing](./optional-forcing)).

Older cases keep these in `General_Data.xlsx` and separate workbooks; both layouts still run.

## Forcing inputs

Forcing can be prescribed through spreadsheets, raster schedules, or synthetic storm settings. The [Optional Forcing](./optional-forcing) page documents the supported pathways, including rainfall time series, rainfall rasters, evapotranspiration forcing, inflow hydrographs, stage boundaries, and synthetic design storms.

## Practical rules

Raster inputs should:

- use a projected coordinate reference system;
- align with the DEM, or be resample-ready to that grid;
- use consistent units;
- cover the model domain cleanly.

HydroPol2D can resample and mask many optional rasters internally, but reproducible workflows still depend on clean, domain-consistent source files.

## Quick input map

| Input group | Typical files |
|---|---|
| Core terrain and classes | `DEM_path`, `LULC_path`, `SOIL_path` |
| Vadose / groundwater support | `DTB_path`, `GW_table_path` |
| Layered subsurface (optional) | `SoilBaseDepth_path`, `RegolithThetaS_path`, `RegolithThetaR_path`, `RegolithAlphaVG_path`, `RegolithNVG_path`, `RegolithKsatV_path`, `RegolithKsatH_path`, `RegolithSpecificYield_path` |
| Deep aquifer (optional) | `DeepAquiferSubbasins_path`, `DeepAquiferChannelWeight_path`, `DeepAquiferInitialState_path` |
| Surface-property refinements | `LAI_path`, `Albedo_path`, `ImperviousFraction_path` |
| Initial states | `Warmup_Depth_path`, `Initial_Soil_Moisture_path`, `Initial_SWE_path`, `Initial_Snow_Depth_path`, `Initial_Buildup_path` |
| Channel geometry | `RiverWidths_path`, `RiverDepths_path` |
| Water-quality rasters | `B1_path`, `B2_path`, `W1_path`, `W2_path` |
| Forcing and boundary files | rainfall, ETP, inflow, stage, control-structure spreadsheets or raster schedules |

The detailed behavior of the supplemental raster and initial-state inputs is documented on [Additional Spatial Inputs](./additional-spatial-inputs).
