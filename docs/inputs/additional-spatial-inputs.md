---
title: Additional Spatial Inputs
---

# Additional Spatial Inputs

Beyond the core DEM, LULC, and soil rasters, HydroPol2D can ingest a wider set of optional raster and initial-state inputs. This page documents the supported file-based inputs that were historically under-described in the docs.

---

## Supplemental Raster Inputs

| Input | Public path key | When used | Notes |
|---|---|---|---|
| Initial groundwater table | `GW_table_path` | When groundwater is active and an initial head raster is supplied | Raster is interpreted as **initial groundwater table elevation/head** in meters, aligned to the DEM. If missing, the model falls back to a shallow default water table above bedrock. |
| Fractional imperviousness | `ImperviousFraction_path` | When a fractional impervious raster is supplied | Values can be in `[0,1]` or `[0,100]` percent. This refines imperviousness for non-built-up cells. Cells classified as built-up/impervious by LULC remain fully sealed. |
| Spatial LAI | `LAI_path` | When LAI is used by the active configuration | Optional vegetation raster aligned to the DEM. |
| Spatial albedo | `Albedo_path` | When `flag_spatial_albedo = 1` | Optional albedo raster aligned to the DEM. |
| River width | `RiverWidths_path` | When the Neal (2012) channel-subgrid mode uses raster geometry | Channel width in meters. Values must be positive and smaller than the model-cell resolution. |
| River depth | `RiverDepths_path` | When the Neal (2012) channel-subgrid mode uses raster geometry | Rectangular channel depth or bank height in meters. A positive depth is required wherever river width is positive. |
| Water-quality coefficient rasters | `B1_path`, `B2_path`, `W1_path`, `W2_path` | When water quality is active and raster coefficients are enabled | Optional pollutant buildup / washoff coefficient rasters. |

---

## Initial-State Raster Inputs

| Input | Public path key | When used | Notes |
|---|---|---|---|
| Initial surface water depth | `Warmup_Depth_path` | When `flag_warmup = 1` and a warmup-depth raster is provided | Raster is read as initial ponded depth in meters and converted internally to millimeters. |
| Initial soil storage | `Initial_Soil_Moisture_path` | When `flag_warmup = 1` and an initial soil raster is provided | Despite the legacy name, the current code interprets this raster as **initial active soil storage above residual water content** in millimeters, not raw volumetric $\theta$. |
| Initial pollutant buildup | `Initial_Buildup_path` | When water quality uses an initial buildup raster | Used to initialize pollutant mass/buildup states. |

---

## Groundwater Table Input

If `GW_table_path` is supplied, HydroPol2D uses that raster as the initial groundwater table elevation:

- it is aligned to the DEM,
- clipped so a minimum vadose thickness is preserved,
- masked to the active domain,
- and locally backfilled only where the raster has missing values.

If no groundwater-table raster is provided, the model falls back to a simple default initial head slightly above bedrock. This means `GW_table_path` is a true optional initial-condition input, not a required groundwater raster.

---

## Fractional Imperviousness Input

If `ImperviousFraction_path` is supplied, HydroPol2D reads a cellwise impervious fraction raster and converts it to:

- impervious fraction `frac_imp`,
- pervious fraction `frac_perv`,
- and a fully impervious mask for cells that are effectively sealed.

Important current behavior:

- values may be supplied as fractions or percents,
- the raster refines imperviousness mainly outside the built-up LULC class,
- cells already classified as impervious/built-up by the LULC table are forced to remain fully impervious.

So the impervious raster should be documented as a **fractional imperviousness override/refinement**, not as a separate standalone land-cover map.

---

## Alignment and Resampling

These supplemental rasters are expected to be consistent with the DEM, but HydroPol2D also performs alignment work internally:

- rasters are resampled to the DEM grid when needed,
- invalid values are masked out of the active domain,
- some optional rasters are only loaded when the corresponding flags are active.

That makes them flexible, but it does not remove the need for sensible preprocessing on the user side.

---

## Neal (2012) Channel Geometry

The Neal (2012) channel-subgrid mode uses the coarse DEM as the floodplain elevation. `RiverDepths_path` lowers the embedded rectangular channel bed below that elevation, while `RiverWidths_path` defines the channel width within each active river cell. The two rasters must be supplied together.

The channel width must remain smaller than the model-cell resolution. A channel as wide as or wider than the cell should be resolved by the ordinary grid instead of represented as a subgrid channel. Channel and floodplain roughness are assigned separately through the river and LULC parameter inputs.

See [Model Flags](../configuration/flags#neal-2012-subgrid-model-configuration) for the required routing combination.

---

## Recommended Public Interpretation

The easiest way to think about the input surface is:

1. DEM, LULC, and SOIL define the base domain.
2. DTB, GW table, LAI, albedo, and impervious fraction refine that base domain.
3. Warmup, initial soil storage, and initial buildup set the starting state.
4. Water-quality rasters support optional specialized modules.

That is the current implemented input story the docs should follow.

---

## Root Depth

Root depth is part of the current model input surface, but **not** as a standalone raster path.

Current implemented behavior:

- root depth is read from the LULC parameter table as `root_depth_m`,
- that class-based value is expanded to the grid through the categorical LULC map,
- the resulting root depth is then truncated by bedrock depth and water-table position when the layered vadose profile is built.

So yes, HydroPol2D can ingest root-depth information, but the supported public path today is:

1. LULC raster for class identity,
2. `root_depth_m` in the LULC parameter table for per-class root depth.

There is no separate `RootDepth_path` raster input in the current code.
