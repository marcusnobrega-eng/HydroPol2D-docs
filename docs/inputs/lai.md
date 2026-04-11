---
title: LAI
---

# Leaf Area Index (LAI)

Leaf Area Index (LAI) represents the total leaf area per unit ground area and is used in HydroPol2D to characterize vegetation density and its interaction with rainfall and atmospheric processes.

In the current implementation of the model, LAI is used to represent canopy effects on interception and evapotranspiration.

---

## Role in HydroPol2D

LAI is used to represent:

- Rainfall interception by the vegetation canopy  
- Partitioning between throughfall and canopy storage  
- Vegetation influence on evapotranspiration  

Higher LAI values correspond to denser vegetation and increased canopy storage capacity.

---

## Representation

LAI is provided as a **continuous raster map**, where each grid cell contains a value representing vegetation density.

Typical values range from:

- ~0 → bare soil or impervious surfaces  
- 1–3 → sparse to moderate vegetation  
- 4–7+ → dense vegetation (e.g., forests)  

Values must be consistent with the land cover conditions in the domain.

---

## Temporal Representation

Dynamic LAI is **not currently implemented** in HydroPol2D.

As a result, LAI must be provided as a **static input**.

The recommended approaches are:

- **Median LAI** → for long-term or climatological simulations  
- **Wet-season LAI** → for simulations focused on high vegetation activity  
- **Dry-season LAI** → for simulations focused on reduced vegetation conditions  

The choice should be consistent with the simulation objective and time period.

---

## Data Sources

Several datasets provide global LAI estimates:

### MODIS LAI (MOD15A2H)
- Region: Global  
- Resolution: 500 m  
- Temporal resolution: 8-day  
- Widely used and consistent product  
- Download: https://lpdaac.usgs.gov/products/mod15a2hv061/

---

### Copernicus Global Land Service (LAI)
- Region: Global  
- Resolution: 300 m  
- Temporal resolution: 10-day  
- Derived from satellite observations  
- Download: https://land.copernicus.eu/global/products/lai

---

### VIIRS LAI
- Region: Global  
- Moderate resolution  
- Continuation of MODIS-era products  

---

### Google Earth Engine

LAI datasets from MODIS, Copernicus, and VIIRS are available in Google Earth Engine and can be processed to extract median or seasonal values.

---

## Consistency with LULC

LAI must be consistent with the LULC classification.

Typical correspondence includes:

- Forest → high LAI  
- Grassland → moderate LAI  
- Urban → low or near-zero LAI  

Inconsistencies between LULC and LAI will result in unrealistic canopy behavior.

---

## Practical Considerations

When preparing LAI inputs:

- Use representative values for the simulation period  
- Avoid extreme or noisy values from raw satellite products  
- Apply temporal aggregation (median or seasonal averages) when needed  
- Ensure spatial consistency with other raster inputs  

If no LAI dataset is available, values can be assigned based on LULC classes, although this introduces additional assumptions.

---

## Summary

LAI is used in HydroPol2D to represent vegetation effects on interception and evapotranspiration.

The model currently assumes a static LAI field, and users must select representative values based on the intended simulation period.

Careful selection of LAI is required to ensure consistency with land cover and realistic representation of vegetation processes.