---
title: Overview
---
import useBaseUrl from '@docusaurus/useBaseUrl';

# HydroPol2D Case Builder

The HydroPol2D Case Builder prepares a complete, ready-to-run model case from public global data.
You choose a city or a catchment. The Builder draws the model area, downloads and aligns the maps,
prepares the rainfall and weather, and checks the case before you run it. It writes cases for
HydroPol2D-MATLAB and for HydroPol2D-Python, the model engine inside HydroPol2D Studio.

This section describes Case Builder 0.1.0, the first licensed release (a test version), for Macs
with Apple silicon and for Windows (64-bit).

:::info[License]
The Case Builder is a proprietary product. To get a license, write to Marcus N. Gomes Jr. at
[marcusnobrega.engcivil@gmail.com](mailto:marcusnobrega.engcivil@gmail.com).
[Install and license](install-and-license) explains the steps.
:::

<p align="center">
  <img src={useBaseUrl('/img/builder/case-builder-workflow.svg')} width="760" alt="The Case Builder from first start to a case ready to run: the license code, the public data it downloads, the four steps Choose the area, Preview, Prepare and Check, the case folder, and where the case runs" />
</p>

<p align="center">
  <em>Figure 1. The path through the Case Builder. The public data feed the preview and the complete case. The case folder runs in HydroPol2D MATLAB or in HydroPol2D Studio.</em>
</p>

## What it prepares

| Step | What the Builder does |
|---|---|
| Model area | Three ways to choose it. **Urban Basin**: a city and every basin that drains into it. **Catchment**: one outlet and the watershed above it. **Urban Area Only**: the built-up area and a buffer around it. |
| Cost preview | Before any large download, it shows the area, the number of grid cells, the data to download and the size of the saved results. |
| Terrain and rivers | Terrain at the model resolution, conditioned for flow with HydroBathyDEM, with river widths and depths. |
| Maps | Land cover, soil texture, depth to bedrock, initial groundwater and soil water, and leaf area index. |
| Rain and weather | One rainfall product per case (IMERG, ERA5, MSWEP or AORC) and ERA5 weather. |
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
| Rainfall | IMERG, ERA5, MSWEP or AORC (United States), chosen per case |

No Google Earth Engine account is needed. Some sources need a free account of your own:
[Data sources and accounts](data-accounts) lists them.

## How it fits with Studio and MATLAB

- **In HydroPol2D Studio**, the **New model** wizard uses the Builder's preparation steps to make a
  model from a location on the map. See [Building a model](../studio/building-a-model). If you
  have Studio, you do not need the Builder as well.
- **The standalone Builder** adds the full set of options: the three kinds of model area, the cost
  preview, the preflight report, and runs in MATLAB.
- **With HydroPol2D-MATLAB**, the Builder writes a MATLAB case with a `run_case.m` script that runs
  it. See the [model-building workflow](../getting-started/model-building-workflow) for how the
  Builder, the models and calibration work together.

## How you use it

- a local app that opens in your web browser, with **Prepare a case**, **Check a case** and
  **Python and command line** pages,
- a command line, for scripted and repeated builds.

## In this section

1. [Install and license](install-and-license): download, install, enter the license code.
2. [Choose the model area](model-area): Urban Basin, Urban Area Only and Catchment.
3. [Case settings](settings): grid, dates, rain, processes, rivers, outputs and folders.
4. [Preview and cost](preview-and-cost): the domain map and the size of the case before any download.
5. [Prepare a case](prepare-a-case): the complete build and what is in the case folder.
6. [Data sources and accounts](data-accounts): Copernicus, NASA Earthdata and MSWEP.
7. [Check a case](check-a-case): the preflight check.
8. [Run the case](run-the-case): in HydroPol2D MATLAB or in HydroPol2D Studio.
9. [Command line](command-line): the same cases from a terminal.
10. [Troubleshooting](troubleshooting): messages you may see and what to do.

## Current limits

- Version 0.1.0 is a test version for Macs with Apple silicon and Windows (64-bit).
- The app does not download HydroPol2D Python. Run Python cases in HydroPol2D Studio.
- MSWEP rainfall needs prior approval from GloH2O.
- AORC rainfall covers the contiguous United States only. GTSM coastal water levels end in 2024.
- Albedo is a single value (0.25) in the current version.
- Storm drains, reservoirs and event calibration are not added automatically.
