---
title: DEM
---

# Digital Elevation Model (DEM)

The Digital Elevation Model (DEM) defines the topographic structure of the simulation domain and is the primary control on surface flow dynamics in HydroPol2D.

It is one of the most critical inputs in the model, as it governs terrain gradients, flow directions, and the spatial organization of hydrological processes.

---

## Role in HydroPol2D

The DEM is used to compute:

- Surface elevation across the domain  
- Local slopes driving flow routing  
- Flow connectivity between grid cells  
- Watershed boundaries and drainage patterns  

Because HydroPol2D operates on a raster grid, the DEM also defines the computational mesh on which all surface processes are simulated.

---

## Available DEM Datasets

Several high-quality global DEM datasets are freely available and suitable for HydroPol2D applications:

### SRTM (Shuttle Radar Topography Mission)
- Resolution: ~30 m (1 arc-second)  
- Coverage: Near-global (±60° latitude)  
- Widely used and easily accessible  
- May contain vegetation and urban artifacts  
- Download: https://earthexplorer.usgs.gov/

---

### Copernicus DEM (GLO-30 / GLO-90)
- Resolution: 30 m and 90 m  
- High-quality global dataset  
- Improved consistency and fewer voids than SRTM  
- Recommended for general applications  
- Download: https://spacedata.copernicus.eu/

---

### FABDEM (Forest And Buildings removed DEM)
- Resolution: ~30 m  
- Derived from Copernicus DEM  
- Vegetation and building biases removed  
- Particularly useful for hydrological modeling  
- Download: https://data.bris.ac.uk/data/dataset/25wfy0f9ukoge2gs7a5mqpq2j7

---

### MERIT DEM
- Resolution: ~90 m  
- Error-reduced global DEM  
- Corrected for multiple biases (striping, noise, vegetation effects)  
- Suitable for large-scale simulations  
- Download: http://hydro.iis.u-tokyo.ac.jp/~yamadai/MERIT_DEM/

---

### USGS 3DEP (3D Elevation Program)
- Region: United States  
- Resolution: 1 m to 10 m (depending on location)  
- Includes high-resolution LiDAR-derived DEMs  
- One of the best sources for U.S.-based studies  
- Download: https://apps.nationalmap.gov/downloader/

---

## High-Resolution Data (Recommended)

If available, **LiDAR-based DEMs** are strongly recommended.

Advantages:
- Very high spatial resolution (sub-meter to a few meters)  
- Accurate representation of terrain and micro-topography  
- Better representation of flow paths, channels, and urban features  

These datasets are particularly valuable for:

- Urban flood modeling  
- Small catchments  
- Detailed hydraulic analysis  

### LiDAR Data (United States)

LiDAR data for the U.S. can be accessed through:

- USGS National Map (3DEP): https://apps.nationalmap.gov/downloader/  
- NOAA Digital Coast: https://coast.noaa.gov/dataviewer/#/lidar/search/  

These platforms provide access to high-resolution elevation datasets derived from airborne LiDAR surveys.

---

## Coordinate System Requirements

The DEM **must be in a projected coordinate reference system (CRS)**.

- Geographic coordinates (latitude/longitude) are **not supported**  
- Units must be in **meters**  
- Distances and slopes must be physically meaningful  

All other raster inputs (LULC, Soil, DTB, LAI, Albedo) must:

- Use the **same CRS**  
- Have the **same spatial resolution**  
- Share the **same spatial extent**  

---

## Domain Definition and Masking

In practice, input rasters may not perfectly overlap.

HydroPol2D handles this by:

- Defining a **minimum common domain**  
- Creating a mask where **all required rasters are valid**  
- Restricting simulations to this consistent domain  

This ensures:

- No missing data during simulation  
- Consistent coupling between processes  
- Numerical stability  

---

## Resampling and Alignment

If input rasters are not aligned, HydroPol2D provides a **resampling option**.

When the resampling flag is activated:

- The DEM is automatically interpolated to match the model grid  
- **Bilinear interpolation** is used  

This allows users to:

- Integrate datasets with different resolutions  
- Avoid manual preprocessing in GIS software  

However, users should still ensure that:

- Resampling does not introduce artifacts  
- Resolution remains appropriate for the simulation scale  

---

## Subgrid Modeling (Advanced)

HydroPol2D supports a **subgrid parameterization approach**.

In this case, users can provide:

- A **high-resolution DEM** (fine grid)  
- A **coarser computational grid** (model resolution)  

The model then:

- Derives hydraulic properties at the coarse scale  
- Estimates subgrid variability (e.g., storage, wetted area, conveyance)  
- Improves representation of small-scale terrain features  

This approach is particularly useful when:

- High-resolution topography is available  
- Computational efficiency is required  
- Fine-scale hydraulics influence large-scale behavior  

---

## Preprocessing Recommendations

Before using a DEM, users should:

- Check for missing values or voids  
- Remove noise or artifacts  
- Ensure proper alignment with other rasters  
- Verify CRS and units  
- Evaluate whether smoothing or filtering is needed  

In some cases, depression filling or conditioning may be applied depending on the modeling objectives.

---

## Use of DEM vs. DSM in Different Applications

Care must be taken when selecting the type of elevation model depending on the modeling approach.

For **rain-on-grid simulations**, where rainfall is directly applied over the entire domain, it is recommended to use a **bare-earth DEM**. Digital Surface Models (DSMs), which include buildings and other elevated structures, may introduce artificial slopes and barriers that are not consistent with the assumptions of the local inertial formulation. Building edges can generate unrealistic gradients that lead to non-physical flow behavior.

In contrast, for **fluvial simulations** driven by inflow hydrographs at domain boundaries, DSMs can be used to better represent urban features, provided that simulated water depths remain physically consistent and do not exceed building elevations.

Therefore:

- **Rain-on-grid applications** → use **bare-earth DEM**  
- **Fluvial / boundary-driven applications** → DSM may be used with care  

---

## Summary

The DEM provides the geometric and hydraulic foundation of HydroPol2D simulations.

Its resolution, accuracy, and consistency with other inputs directly influence model performance, numerical stability, and physical realism.

Careful selection and preprocessing of the DEM are essential for obtaining reliable simulation results.