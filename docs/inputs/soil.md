---
title: Soil
---

# Soil Properties

Soil data defines the hydraulic response of the land surface and controls the rate at which water infiltrates into the subsurface in HydroPol2D.

Within the current formulation of the model, soil properties are used to estimate **infiltration capacity, layered vadose-zone storage, drainage/recharge, capillary rise, and groundwater storage behavior**.

---

## Role in HydroPol2D

The soil input is used to represent:

- Infiltration capacity at the surface
- Near-surface, root-zone, and transmission-zone water storage
- Effective hydraulic conductivity by layer
- Initial soil moisture conditions (when not provided as a spatial field)
- Groundwater specific yield and saturated hydraulic conductivity

These properties directly influence the generation of runoff and the timing of the hydrological response.

---

## Soil Representation

HydroPol2D requires a **categorical soil map**.

Each grid cell must be assigned a soil class identifier, which is then linked to a set of hydraulic parameters through the input tables.

This structure allows the model to:

- Assign spatially distributed hydraulic properties  
- Maintain consistency across the domain  
- Separate spatial data from parameter definition  

The soil map still provides one categorical soil class per model cell. That class defines the base hydraulic parameters for the column. The current layered implementation then partitions the available vadose depth into:

- a near-surface layer, with default target depth of $0.10\,\mathrm{m}$;
- a root-zone layer, whose depth is defined by the LULC class;
- a transmission-zone layer below the root zone;
- a groundwater zone beginning at the current water table.

The layer geometry adapts to depth to bedrock and groundwater position. If root depth is shallower than the near-surface layer, the explicit root-zone layer collapses into the near-surface layer. If bedrock or the water table is shallower than the requested root depth, the root zone is truncated to the available vadose depth.

---

## Required Soil Parameters

Hydraulic parameters are defined externally and associated with soil classes. Typical parameters include:

- Saturated hydraulic conductivity (Ks)
- Soil porosity
- Residual water content
- Soil water retention parameters (e.g., Van Genuchten parameters)
- Initial soil moisture (when not prescribed as a spatial field)
- Specific yield and groundwater saturated conductivity
- Optional layer multipliers for saturated hydraulic conductivity

These parameters must be physically consistent and representative of the soil classes defined in the raster.

---

## Soil Data Sources

Several datasets can be used to derive soil classifications and associated hydraulic parameters.

### SoilGrids (ISRIC)
- Region: Global  
- Resolution: up to 250 m  
- Provides continuous estimates of soil properties (texture, bulk density, organic content)  
- Can be used to derive USDA soil texture classes  
- Download: https://soilgrids.org/

---

### FAO / HWSD (Harmonized World Soil Database)
- Region: Global  
- Coarser resolution  
- Provides soil mapping units and associated properties  
- Suitable for large-scale and continental applications  
- Download: https://www.fao.org/soils-portal/data-hub/en/

---

### USDA Soil Classification (Texture-Based)

HydroPol2D commonly relies on **USDA soil texture classes** (e.g., sand, loam, clay) to define hydraulic behavior.

These classes can be derived from:

- SoilGrids texture fractions  
- FAO soil databases  
- Regional soil surveys  

This approach provides a consistent framework for assigning hydraulic parameters such as conductivity and retention characteristics.

---

### SSURGO (Soil Survey Geographic Database)
- Region: United States  
- Very high spatial resolution  
- Detailed soil taxonomy and physical properties  
- Recommended for high-resolution applications  
- Download: https://websoilsurvey.sc.egov.usda.gov/

---

### STATSGO (State Soil Geographic Database)
- Region: United States  
- Coarser resolution than SSURGO  
- Suitable for regional to continental studies  
- Download: https://www.nrcs.usda.gov/resources/data-and-reports/statsgo


## Parameter Association

Soil classes are not used directly in the governing equations. Instead, they serve as **indices into parameter tables**.

Each soil class must be associated with a consistent set of hydraulic properties. The quality of this mapping has a direct impact on model performance.

Users are responsible for ensuring that:

- Parameter values are physically realistic  
- Units are consistent  
- Soil classes are properly defined and interpreted  

---

## Resolution and Alignment

The soil raster must:

- Match or be resampled to the DEM resolution  
- Use the same projected coordinate reference system (CRS)  
- Align spatially with all other raster inputs  

Any mismatch in resolution or alignment will result in incorrect spatial assignment of soil properties.

---

## Practical Considerations

When preparing soil inputs:

- Prefer categorical representations over raw continuous datasets  
- Aggregate detailed soil classifications when necessary  
- Avoid extreme or non-physical parameter values  
- Verify consistency between raster classes and parameter tables  

In many cases, simplifying the number of soil classes improves model stability and interpretability.

---

## Summary

In HydroPol2D, soil data is used to control infiltration, layered vadose storage, recharge, groundwater storage, and groundwater feedback to the surface.

The model relies on a categorical soil representation coupled with externally defined hydraulic parameters, LULC-based root-zone depths, and optional layer multipliers. Proper definition and mapping of these parameters is essential for obtaining reliable simulations.
