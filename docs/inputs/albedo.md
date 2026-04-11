---
title: Albedo
---

# Albedo

Albedo represents the fraction of incoming shortwave radiation that is reflected by the surface.

In HydroPol2D, albedo is used to characterize surface radiative properties and their influence on energy-related processes, particularly evapotranspiration and snow dynamics.

---

## Role in HydroPol2D

Albedo is used to represent:

- Surface reflectivity to incoming solar radiation  
- Energy available for evapotranspiration  
- Surface energy balance conditions  
- Snowmelt behavior (when snow processes are activated)  

Lower albedo surfaces absorb more energy, while higher albedo surfaces reflect a larger fraction of incoming radiation.

---

## Representation

Albedo is provided as a **continuous raster map**, where each grid cell contains a value between 0 and 1.

Typical values include:

- 0.05 – 0.15 → water bodies, dark surfaces  
- 0.15 – 0.25 → vegetation  
- 0.25 – 0.40 → dry soils  
- 0.60 – 0.90 → snow-covered surfaces  

Values must be physically consistent with land cover and environmental conditions.

---

## Temporal Representation

In the current implementation of HydroPol2D, albedo is treated as a **static input**.

Users should select values representative of the simulation conditions:

- Long-term simulations → use average or median albedo  
- Seasonal simulations → use values consistent with the dominant surface condition  

Dynamic albedo variations (e.g., due to snow cover or vegetation changes) are not explicitly resolved unless provided externally.

---

## Data Sources

Several datasets provide global albedo estimates:

### MODIS Albedo (MCD43A3)
- Region: Global  
- Resolution: 500 m  
- Temporal resolution: 16-day  
- Widely used satellite-derived product  
- Download: https://lpdaac.usgs.gov/products/mcd43a3v061/

---

### Copernicus Global Land Service (Albedo)
- Region: Global  
- Resolution: 300 m  
- Derived from satellite observations  
- Download: https://land.copernicus.eu/global/products/albedo

---

### Google Earth Engine

MODIS and Copernicus albedo datasets are available in Google Earth Engine and can be processed to extract representative values for the simulation domain.

---

## Consistency with Other Inputs

Albedo must be consistent with:

- **LULC** → defines surface type  
- **LAI** → reflects vegetation density  
- **Snow conditions** → strongly influence reflectivity  

Inconsistent albedo values may lead to unrealistic energy partitioning.

---

## Practical Considerations

When preparing albedo inputs:

- Avoid extreme or non-physical values  
- Use temporally aggregated values when necessary  
- Ensure spatial alignment with all raster inputs  
- Verify consistency with land cover and climate conditions  

If no albedo dataset is available, values may be assigned based on LULC classes, with appropriate justification.

---

## Summary

Albedo defines surface radiative properties in HydroPol2D and influences energy-driven processes such as evapotranspiration and snowmelt.

Although simple in structure, it plays an important role in ensuring physically consistent representation of surface–atmosphere interactions.