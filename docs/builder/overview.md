---
title: Overview
---

# HydroPol2D Case Builder

The HydroPol2D Case Builder prepares a complete, ready-to-run model case from public global data.
You choose a city or a catchment. The Builder draws the model area, downloads and aligns the maps,
prepares the rainfall and weather, and checks the case before you run it. It writes cases for
HydroPol2D-MATLAB and for HydroPol2D-Python, the model engine inside HydroPol2D Studio.

:::info[License]
The Case Builder is a proprietary product. To get a license, write to Marcus N. Gomes Jr. at
[marcusnobrega.engcivil@gmail.com](mailto:marcusnobrega.engcivil@gmail.com). This page is an
overview. A full user guide will come with the first licensed release.
:::

## What it prepares

| Step | What the Builder does |
|---|---|
| Model area | Three ways to choose it. **Urban Basin**: a city and every basin that drains into it. **Catchment**: one outlet and the watershed above it. **Urban Area Only**: the built-up area and a buffer around it. |
| Cost preview | Before any large download, it shows the area, the number of grid cells and the memory the case needs. |
| Terrain and rivers | Terrain at the model resolution, conditioned for flow with HydroBathyDEM, with river widths and depths. |
| Maps | Land cover, soil texture, depth to bedrock, initial groundwater and soil water, and leaf area index. |
| Rain and weather | One rainfall product per case (IMERG, ERA5 or MSWEP) and ERA5 weather. |
| Boundaries | Outlets with critical flow by default. River inflows (GloFAS) and coastal water levels (GTSM) where they apply. |
| Check | A preflight check of the files, grids, dates, units and required inputs. |
| Run | It writes the case for MATLAB, Python or both, and it can start the run and show its progress. |

A case that passes the preflight check is complete and consistent. That alone does not show that
the model is accurate for a new place. Calibration and comparison with observations remain
necessary.

## Data sources

| Variable | Source |
|---|---|
| City boundary | GHSL Urban Centre Database R2024A |
| Basins and rivers | HydroBASINS v1c (level 12) and HydroRIVERS v1.0 |
| Terrain | FABDEM v1.2, or your own DEM |
| River geometry | HydroBathyDEM |
| Land cover | ESA WorldCover |
| Soil texture | OpenLandMap USDA texture classes |
| Depth to bedrock | Shangguan et al. (2017) |
| Initial groundwater | Fan et al. global water-table depth |
| Initial soil water | ERA5-Land |
| Weather | ERA5 |
| Leaf area index | MODIS MCD15A3H |
| Rainfall | IMERG, ERA5 or MSWEP, chosen per case |

No Google Earth Engine account is needed.

## How it fits with Studio and MATLAB

- **In HydroPol2D Studio**, the **New model** wizard uses the Builder's preparation steps to make a
  model from a location on the map. See [Building a model](../studio/building-a-model).
- **The standalone Builder** adds the full set of options: the three kinds of model area, the cost
  preview, the preflight report, and runs in MATLAB or Python.
- **With HydroPol2D-MATLAB**, the Builder writes a MATLAB case with a `run_case.m` script that runs
  it. See the [model-building workflow](../getting-started/model-building-workflow) for how the
  Builder, the models and calibration work together.

## How you use it

- a local app that opens in your web browser, with **Prepare a case** and **Check a case** pages,
- a command line, for scripted and repeated builds,
- a Python interface, for notebooks and servers.

## Current limits

- It is tested on macOS. Linux is the intended system for large runs. Windows is not yet tested.
- MSWEP rainfall needs prior approval from GloH2O.
- Albedo is a single value (0.25) in the current version.
- Storm drains, reservoirs and event calibration are not added automatically.
