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

This is the default scheme. The optional [layered subsurface](#soil-and-regolith-in-the-layered-subsurface) keeps the same three soil layers but places regolith layers below them, with their own parameters.

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

## Soil and Regolith in the Layered Subsurface

With the [layered subsurface](../theory/layered-subsurface), the column has three soil slots above the soil base and regolith slots below it. Each slot has its own van Genuchten curve.

### Soil slots

The three soil slots use the soil-class parameters: `ksat` with the three layer multipliers, `n`, `alpha`, `θsat`, `θr` and `l_vg`. Two soil-table columns change role:

| Column | Default scheme | Layered subsurface |
|---|---|---|
| `Sy` | Specific yield of the aquifer | Ignored. Each slot takes $S_y$ from its retention curve. |
| `kgsat` | Lateral conductivity of the aquifer | Horizontal conductivity of the regolith slots, used when `regolith_ksat_h_mm_h` is empty |

The specific yield of every slot is the drainable porosity at field capacity:

$$
S_y = \theta_s - \theta\left(\psi = -h_{fc}\right)
$$

with $h_{fc}$ = `capillary_field_capacity_head_m` (default 3.3 m). In HydroPol2D-Python, `vertical.specific_yield` and `static.specific_yield_path` are not used by the layered scheme; the path raises a warning.

The horizontal conductivity of the soil slots is `ksat` × `soil_lateral_anisotropy` (default 1) × `soil_lateral_conductivity_multiplier` (default 1).

### Regolith slots

Regolith parameters are scalars or rasters. A raster wins wherever it is finite; the scalar fills the rest.

| Parameter | Units | Default | MATLAB raster (`General_Data`) | Python raster |
|---|---|---|---|---|
| `regolith_theta_s` | m³/m³ | 0.35 | `RegolithThetaS_path` | `static.regolith_theta_s_path` |
| `regolith_theta_r` | m³/m³ | 0.05 | `RegolithThetaR_path` | `static.regolith_theta_r_path` |
| `regolith_alpha_vg_m_inverse` | 1/m | 2.0 | `RegolithAlphaVG_path` | `static.regolith_alpha_vg_m_inverse_path` |
| `regolith_n_vg` | — | 1.5 | `RegolithNVG_path` | `static.regolith_n_vg_path` |
| `regolith_ksat_v_mm_h` | mm/h | 5.0 | `RegolithKsatV_path` | `static.regolith_ksat_v_mm_h_path` |
| `regolith_ksat_h_mm_h` | mm/h | empty: `kgsat` | `RegolithKsatH_path` | `static.regolith_ksat_h_mm_h_path` |
| `regolith_specific_yield` | — | empty: $\theta_s - \theta_{fc}$ | `RegolithSpecificYield_path` | `static.regolith_specific_yield_path` |

A given regolith $S_y$ must lie in $(0,\ \theta_s - \theta_r]$. The horizontal conductivity of the regolith slots is multiplied by `regolith_lateral_conductivity_multiplier` (default 1).

There is no regolith class table yet. Regolith properties are scalars or rasters only.

### Root-water-uptake heads

The Feddes heads $h_1$ to $h_4$ are global settings, not soil-class parameters. See [Hydrologic Model, Section 3.5](../theory/hydrologic-model#35-feddes-root-water-uptake-stress).

### Global sources used by the Case Builder

The Case Builder (`--subsurface-scheme layered`) derives the regolith maps from global data, so the same rules apply to any domain:

| Map | Rule | Source |
|---|---|---|
| `RegolithThetaS/ThetaR/AlphaVG/NVG.tif` | USDA texture class at 200 cm, mapped to van Genuchten parameters through the Builder soil table | OpenLandMap texture v0.2, 200 cm |
| `RegolithKsatH.tif` | Permeability × $\rho g/\mu$ at 20 °C. Where GLHYMPS has no polygon, the groundwater Ksat of the 200 cm texture class. | GLHYMPS 2.0 global tiles (Gleeson et al., 2014; Huscroft et al., 2018) |
| `RegolithKsatV.tif` | `RegolithKsatH` ÷ `groundwater_vertical_anisotropy_ratio` | — |
| `RegolithSpecificYield.tif` | Default `derived_capped`: $\theta_s - \theta(3.3\ \mathrm{m})$, capped by GLHYMPS porosity; nodata where GLHYMPS is missing, so the model derives $S_y$ there. With `derived`, no map is written. | `--regolith-specific-yield-rule` |

GLHYMPS tiles are downloaded once, checked against the manifest SHA-256 and cached. Provenance, coverage and statistics go to `quality_report/layered_subsurface_rasters.json`. In layered cases the Builder does not wire `SpecificYield.tif` into the case.

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
