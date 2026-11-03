---
title: San Francisquito Catchment - Controlled Rainfall Example
---
import useBaseUrl from '@docusaurus/useBaseUrl';

# San Francisquito Catchment - Controlled Rainfall Example

## Purpose

This example presents a controlled rainfall-runoff simulation for the San Francisquito Creek catchment near Stanford, California. It shows how HydroPol2D responds on a real watershed to a storm whose timing and volume are known exactly.

## Case setup

The case `Stanford_30m_Website_100mmh_1h_24h` uses:

| Item | Value |
|---|---|
| Domain | San Francisquito Creek catchment, California, USA |
| Grid | 30 m, NAD83 / California Albers (EPSG:3310) |
| Forcing type | Spatially uniform rainfall |
| Rainfall event | 100 mm/h from 15 to 75 min (100 mm) |
| Simulation duration | 24 h |
| Map output interval | 15 min |
| Routing family | Local inertial |
| Outlet treatment | Perimeter outlet |
| Processes | Infiltration on; groundwater, evapotranspiration, snow and water quality off |

## Input data

Two inputs are maps (Figure 1):

- **Terrain.** The USGS 3D Elevation Program (3DEP) bare-earth DEM, read from the 3DEPElevation service at 10 m and averaged to the 30 m grid (downloaded 2026-11-02, U.S. public domain).
- **Land use and land cover.** ESA WorldCover 2020 (v100), CC BY 4.0. © ESA WorldCover project 2020 / Contains modified Copernicus Sentinel data (2020) processed by ESA WorldCover consortium. The class codes 10 to 90 of the land-use table are WorldCover's.

The other inputs are uniform values set for the example, not outside data: one soil class (class 8 of the soil table), a depth to bedrock of 1.5 m, an LAI of 1, an albedo of 0.25 and an initial soil moisture of 0.1104. The other parameters come from the Stanford case workbook distributed with the MATLAB model.

<p align="center">
  <img src={useBaseUrl('/img/examples/stanford-30m-inputs.svg')} width="680" alt="Two maps of the San Francisquito Creek catchment: terrain from USGS 3DEP with a hillshade, and ESA WorldCover land cover with the share of each class" />
</p>

<p align="center">
  <em>Figure 1. The two spatial inputs on the 30 m grid. Top: terrain from USGS 3DEP. Bottom: ESA WorldCover 2020 land cover, with the share of each class in the domain. The circle marks Searsville Lake, where the deepest water of the run is.</em>
</p>

## What this case is meant to show

This case highlights:

- runoff generation under a simple, known forcing;
- the interaction between topography, roughness, and infiltration;
- the spatial organization of routed flood depth, velocity, hazard, and cumulative infiltration;
- long recession behavior after the rainfall pulse ends.

## Simulation video

The animation below shows the 30 m simulation. The panels show flood depth, velocity, hazard metric, and cumulative infiltration over a hillshade of the DEM. The still frame is t = 3.5 h, the time of the peak outlet flow.

<div style={{ textAlign: 'center' }}>
  <video
    width="90%"
    controls
    poster={useBaseUrl('/videos/stanford_30m_website_100mmh_1h_24h_panels.png')}>
    <source src={useBaseUrl('/videos/stanford_30m_website_100mmh_1h_24h_panels.mp4')} type="video/mp4" />
    Your browser does not support the video tag.
  </video>

  <p><em>Stanford 30 m controlled rainfall simulation: flood depth, velocity, hazard, and cumulative infiltration.</em></p>
</div>

Each panel uses one color scale for the full sequence. The scale is based on the `99th` percentile of all saved frames.

## Summary results

The simulation saved `97` map frames, one every 15 min. The run summary gives:

| Result | Value |
|---|---|
| Drainage area | `156.823 km²` |
| Rain applied | `100.00 mm` |
| Runoff coefficient | `0.47` |
| Peak outlet flow | `473.69 m³/s` at 3.5 h |
| First outlet peak | `402.84 m³/s` at 75 min, when the rain stops |
| Maximum flood depth | `5.87 m`, in the Searsville Lake basin (37.410° N, 122.234° W) |
| Area that was deeper than 1 m at some time | `4.3 km²` (2.7% of the domain) |
| Volume error | `-6.45 × 10⁻¹²` of the inflow |

The outlet flows are the 15 min samples of the outlet hydrograph. It has two peaks: 402.84 m³/s at 75 min, when the rain stops, and 473.69 m³/s at 3.5 h. Between them the flow falls to 110 m³/s at 2 h and then rises again.

## How to run it

The case is in the HydroPol2D MATLAB repository, in `Examples/Stanford`. In MATLAB, from the root of the repository:

```matlab
addpath(fullfile(pwd,'Examples','Stanford'))
run_stanford_local_case('Resolution',30,'SimulationMinutes',1440, ...
  'RainfallTimeseriesPath',fullfile('Examples','Stanford','Forcing','Rainfall','Rainfall_Intensity_Website_100mmh_1h_24h.csv'), ...
  'RecordTimeMapsMinutes',15,'RecordTimeHydrographsMinutes',15, ...
  'OutputTag','Stanford_30m_Website_100mmh_1h_24h')
```

The results go to `Examples/Stanford/Outputs/Reruns_CurrentModel/Stanford_30m_Website_100mmh_1h_24h/Modeling_Results`: maps of depth, velocity and hazard every 15 min, the outlet hydrograph (`Tables_CSV/Outlet_Hydrograph_Data_Outlet.csv`) and the run summary (`Tables_CSV/Summary_Table.csv`).

A shorter run of the same storm, 3 h instead of 24 h, starts with `run('Examples/Stanford/run_excel.m')` and takes about 14 min on a laptop. The README of the repository lists its expected results.
