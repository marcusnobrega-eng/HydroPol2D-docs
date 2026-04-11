---
title: LULC
---

# Land Use / Land Cover (LULC)

The Land Use / Land Cover (LULC) map defines the spatial distribution of surface characteristics across the simulation domain.

In HydroPol2D, the LULC input is used to represent how different portions of the domain respond to rainfall and surface flow through parameter assignment.

---

## Role in HydroPol2D

The LULC map is used to define spatial variability in:

- Surface roughness (Manning’s coefficient)  
- Interception storage  
- Impervious fraction  
- Surface-related evapotranspiration behavior  

These properties directly influence runoff generation, flow velocity, and water retention at the surface.

---

## LULC Representation

HydroPol2D requires a **categorical LULC map**.

Each grid cell must be assigned a land use class identifier (integer or categorical value). These classes are not used directly in the governing equations. Instead, they serve as **indices into parameter tables**.

For each LULC class, a set of parameters is defined externally in the input tables. This includes:

- Manning’s roughness coefficient  
- Interception capacity  
- Impervious fraction  
- Additional process-specific parameters  

This approach separates spatial information from parameter definition and allows full flexibility in configuring model behavior.

---

## Available LULC Datasets

Several high-quality global and regional LULC datasets are freely available:

### NLCD (National Land Cover Database)
- Region: United States  
- Resolution: 30 m  
- Includes detailed urban classes and impervious surfaces  
- Download: https://www.mrlc.gov/

---

### ESA WorldCover
- Region: Global  
- Resolution: 10 m  
- High-resolution global classification  
- Download: https://worldcover2020.esa.int/

---

### Copernicus Land Monitoring Service
- Region: Europe and global products  
- Resolution: 10–100 m  
- Includes multiple thematic layers  
- Download: https://land.copernicus.eu/

---

### MODIS Land Cover (MCD12Q1)
- Region: Global  
- Resolution: 500 m  
- Long-term annual time series  
- Download: https://lpdaac.usgs.gov/products/mcd12q1v061/

---

### Dynamic World
- Region: Global  
- Resolution: 10 m  
- Near real-time classification derived from Sentinel-2  
- Provides probabilistic class outputs  
- Particularly useful for dynamic or rapidly changing environments  
- Access: Google Earth Engine  

---

## Parameter Association

LULC classes are mapped to model parameters through the input tables.

Each class must be associated with a consistent set of physical values. This mapping determines how the model represents:

- Surface resistance to flow  
- Rainfall interception  
- Runoff generation behavior  

Incorrect or inconsistent parameter assignment will directly affect simulation results.

---

## Impervious Surfaces

Urban classes typically include a significant fraction of impervious area (roads, rooftops, pavements).

These areas are characterized by:

- Negligible infiltration  
- Rapid runoff generation  
- Increased flow velocities  

The impervious fraction parameter is used to represent this behavior and must be carefully assigned for urban land use classes.

---

## Resolution and Alignment

The LULC raster must:

- Match or be resampled to the DEM resolution  
- Use the same projected coordinate reference system (CRS)  
- Align spatially with all other raster inputs  

Misalignment leads to incorrect parameter assignment and inconsistent flow representation.

---

## Reclassification

Raw LULC datasets often contain a large number of classes.

For HydroPol2D applications, it is often preferable to:

- Aggregate classes into a reduced set of representative categories  
- Group similar land use types  
- Simplify the parameterization scheme  

This improves model robustness and reduces unnecessary complexity.

---

## Interaction with Other Inputs

The LULC map defines surface behavior and must be consistent with:

- **DEM** → defines terrain and flow routing  
- **Soil** → controls infiltration capacity  
- **LAI** → influences vegetation-related processes  
- **Albedo** → affects surface energy balance  

Each of these inputs contributes a different aspect of spatial variability in the model.

---

## Summary

In HydroPol2D, LULC is treated as a categorical map used to assign surface-related parameters through lookup tables.

The quality of the classification and the consistency of parameter mapping are critical for accurately representing surface flow resistance, runoff generation, and vegetation effects.