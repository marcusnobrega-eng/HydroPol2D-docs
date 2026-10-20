---
title: DTB
---

# Depth to Bedrock (DTB)

The Depth to Bedrock (DTB) defines the vertical extent of the soil column available for water storage in HydroPol2D.

It represents the distance between the land surface and a limiting layer that constrains vertical water movement. This layer may correspond to actual bedrock or to an effective boundary such as the top of a shallow aquifer.

---

## Role in HydroPol2D

What DTB controls depends on the subsurface scheme. In the default scheme, DTB is the soil depth: the soil and the aquifer share the same column. In the [layered subsurface](#dtb-in-the-layered-subsurface), DTB is only the bottom of the aquifer, and a separate soil base marks where the soil ends.

In the default scheme, DTB is used to define:

- Maximum subsurface storage capacity  
- Vertical limit for infiltration and percolation  
- Effective thickness of the vadose zone  
- Onset of saturation within the soil column  

Within the model, DTB acts as a **geometric constraint** on storage rather than a fully resolved vertical profile.

DTB should not be confused with the optional initial groundwater-table raster. In the current model, `DTB_path` defines soil-column thickness, while `GW_table_path` defines the initial saturated head/elevation when groundwater initialization is provided explicitly.

---

## Representation

DTB is provided as a **continuous raster map**, where each cell contains a depth value (in meters).

This allows spatial variability in storage capacity across the domain.

- Shallow DTB → rapid saturation and runoff generation  
- Deep DTB → larger storage and delayed hydrological response  

---

## Alternative Definition: Depth to Aquifer

In many applications, the objective is not to explicitly resolve groundwater dynamics but to constrain the depth of the vadose zone.

In this case, DTB can be interpreted as the **depth to the aquifer surface**, rather than the depth to the impermeable bedrock.

Under this assumption:

- The vadose zone is limited to the depth between the surface and the aquifer  
- Storage is constrained by available unsaturated soil volume  
- No explicit representation of the saturated aquifer is required  

This approach is appropriate when:

- Groundwater processes are not explicitly modeled  
- The focus is on surface and near-surface hydrological response  
- A realistic upper bound for soil storage is needed  

---

## Default Assignment from Soil Classes

If a DTB map is not available, a soil depth per soil class can stand in for it.

- **HydroPol2D-Python** can take the soil depth from its soil table, from a soil-depth raster, or from the scalar `vertical.soil_depth_m`.
- **HydroPol2D (MATLAB)** does not currently read the `DTB (m)` column of `SOIL_parameters.xlsx`. With `DTB_path` empty, the soil depth is 1 m.

Whether the MATLAB `DTB (m)` column should be read or removed is an open decision.

---

## Units and Requirements

The DTB input must:

- Be expressed in **meters**  
- Use a **projected CRS** consistent with all other rasters  
- Align spatially with the DEM and other inputs  

Values must remain within physically realistic ranges for the study area.

---

## Data Sources

DTB data is not as widely standardized as DEM or LULC, but can be derived from:

### SoilGrids (Depth to Bedrock)
- Region: Global  
- Provides estimates of depth to bedrock  
- Download: https://soilgrids.org/

---

### Regional Geological Surveys
- National or regional datasets may provide higher-quality estimates  
- Often derived from geological mapping or subsurface models  

---

### Derived or Assumed Values
- DTB can be approximated based on soil type or geological context  
- Constant values may be used when spatial variability is unknown  

---

## DTB in the Layered Subsurface

With the [layered subsurface](../theory/layered-subsurface) (Python `vertical.subsurface.scheme: layered`, MATLAB `flag_layered_subsurface = 1`), two depths define the column:

| Depth | What it marks | Input |
|---|---|---|
| Soil base | Where soil properties end and regolith begins | `SoilBaseDepth_path` raster, else `subsurface_soil_base_depth_m` (default 2 m) |
| Depth to bedrock | Where the aquifer ends | `DTB_path` raster, else `subsurface_depth_to_bedrock_m`, else the default-scheme soil depth (with a warning) |

The aquifer base is the ground minus $\min(\mathrm{DTB},\ D_{\max})$, with $D_{\max}$ = `subsurface_max_depth_m` (default 50 m). Cells with DTB deeper than the cap stop at the cap.

Between the soil base and the column base, the model places regolith slots on a fixed ruler: 0.25, 0.5, 1, 2, 4, 4, … m from the soil base (first thickness, growth ratio and maximum thickness are configurable). The ruler is cut at the column base, so a deeper DTB adds more 4 m slots.

In Python the same keys are `vertical.subsurface.soil_base_depth_m`, `depth_to_bedrock_m`, `max_depth_m` and `deep_layers`, and the rasters are `static.soil_base_depth_path` and `static.depth_to_bedrock_path`.

Whether `DTB_path` should be required in MATLAB Excel mode when the layered scheme is on is an open decision. Today the fallback to the default soil depth applies, with a warning.

### Global sources used by the Case Builder

The Case Builder applies the same rules to any domain:

| Map | Source |
|---|---|
| `DTB.tif` (column bottom) | SoilGrids depth to bedrock, BDTICM (Shangguan et al., 2017) |
| `SoilBaseDepth.tif` (soil base) | SoilGrids depth to the R horizon, BDRICM, censored at 2 m, converted from cm to m |

Both maps come from the same Shangguan et al. (2017) model, so their definitions agree.

---

## Interaction with Soil Properties

DTB complements the soil parameterization:

- Soil parameters control infiltration behavior  
- DTB limits the total volume available for storage  

This combination determines the effective response of the system without requiring explicit vertical discretization.

---

## Practical Considerations

When defining DTB:

- Avoid unrealistically large values  
- Maintain consistency with soil classification  
- Ensure spatial coherence  
- Use simplified assumptions when necessary, but document them  

DTB is often uncertain and should be evaluated as part of sensitivity analysis when possible.

---

## Summary

In the default scheme, DTB defines the effective vertical storage available to the model and constrains the depth of the vadose zone. In the layered subsurface, DTB sets the aquifer base and the soil base sets the bottom of the soil.

It can represent either the depth to bedrock or the depth to the aquifer surface, depending on the modeling objective.

Even though it is simple in form, it plays a central role in controlling runoff generation and storage capacity in HydroPol2D.
