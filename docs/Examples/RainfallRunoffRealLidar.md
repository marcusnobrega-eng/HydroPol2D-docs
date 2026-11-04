---
title: San Francisquito Catchment - 10 m LiDAR Controlled Event
---
import useBaseUrl from '@docusaurus/useBaseUrl';

# San Francisquito Catchment - 10 m LiDAR Controlled Event

## Purpose

This example runs the storm of the [30 m example](RainfallRunoff) on a 10 m grid of the same catchment. It shows how a finer terrain changes where the water goes and how fast it leaves.

## Case setup

The case `Stanford_10m_LiDAR_Website_100mmh_1h_6h` uses:

| Item | Value |
|---|---|
| Domain | San Francisquito Creek catchment, California, USA |
| Grid | 10 m, NAD83 / California Albers (EPSG:3310) |
| Forcing type | Spatially uniform rainfall |
| Rainfall event | 100 mm/h from 15 to 75 min (100 mm) |
| Simulation duration | 6 h |
| Map output interval | 15 min |
| Routing family | Local inertial |
| Outlet treatment | Perimeter outlet |
| Processes | Infiltration on; groundwater, evapotranspiration, snow and water quality off |

## Input data

Two inputs are maps (Figure 1):

- **Terrain.** A 10 m USGS 3D Elevation Program (3DEP) bare-earth DEM, U.S. public domain. Most of it is an earlier 3DEP download kept with the example. Its 5.9 km² gap in the western headwaters was filled on 2026-11-03 from the 3DEPElevation service at 10 m, blended so that the fill meets the earlier file without a step. Twenty-six single-cell pits and spikes were smoothed, and the DEM is clipped to the catchment. The two downloads differ by 2.8 m RMS, most on the steep western slopes, so this DEM is not just a finer copy of the 30 m one.
- **Land use and land cover.** ESA WorldCover 2020 (v100), the 30 m map of the 30 m example, read on the 10 m grid. CC BY 4.0. © ESA WorldCover project 2020 / Contains modified Copernicus Sentinel data (2020) processed by ESA WorldCover consortium.

The other inputs are the uniform values of the 30 m example: one soil class (class 8 of the soil table), a depth to bedrock of 1.5 m, an LAI of 1, an albedo of 0.25 and an initial soil moisture of 0.1104. These maps are on the 30 m grid. On 8,374 cells along the edge of the domain (0.5%), which the 30 m LAI map does not reach, the model uses an LAI of 0, so no rain is intercepted there.

<p align="center">
  <img src={useBaseUrl('/img/examples/stanford-10m-inputs.svg')} width="680" alt="Two maps of the San Francisquito Creek catchment: terrain from the 10 m USGS 3DEP DEM with a hillshade, and ESA WorldCover land cover with the share of each class" />
</p>

<p align="center">
  <em>Figure 1. The two spatial inputs. Top: terrain from the 10 m USGS 3DEP DEM. Bottom: ESA WorldCover 2020 land cover (30 m map), with the share of each class in the domain. The circle marks Searsville Lake, where the deepest water of the run is.</em>
</p>

## Simulation video

The animation below shows the 10 m simulation. The panels show flood depth, velocity, hazard metric, and cumulative infiltration over a hillshade of the DEM. The still frame is t = 3.0 h, the time of the peak outflow across the domain edge.

<div style={{ textAlign: 'center' }}>
  <video
    width="90%"
    controls
    poster={useBaseUrl('/videos/stanford_10m_lidar_100mmh_1h_6h_panels.png')}>
    <source src={useBaseUrl('/videos/stanford_10m_lidar_100mmh_1h_6h_panels.mp4')} type="video/mp4" />
    Your browser does not support the video tag.
  </video>

  <p><em>Stanford 10 m simulation: flood depth, velocity, hazard, and cumulative infiltration over six hours.</em></p>
</div>

Each panel uses one color scale for the full sequence. The scale is based on the `99th` percentile of all saved frames.

## Summary results

The simulation saved `25` map frames, one every 15 min. The run summary gives:

| Result | Value |
|---|---|
| Drainage area | `157.661 km²` |
| Rain applied | `100.00 mm` |
| Runoff coefficient | `0.40` (over the 6 h) |
| Peak outflow across the domain edge | `663.01 m³/s` at 3.0 h |
| First peak of that outflow | `377.13 m³/s` at 75 min, when the rain stops |
| Maximum flood depth | `7.38 m`, in the Searsville Lake basin (37.411° N, 122.238° W) |
| Area that was deeper than 1 m at some time | `4.4 km²` (2.8% of the domain) |
| Volume error | `-1.68 × 10⁻¹¹` of the inflow |

As in the 30 m example, every cell on the domain edge lets water leave (perimeter outlet), so the hydrograph is the outflow across the domain edge, not the flow at the creek mouth alone. The flows are its 15 min samples. The first peak, 377.13 m³/s at 75 min, is hillslope runoff leaving along the whole edge. The flow then falls to 123 m³/s at 1.75 h. After that the creek's flood wave reaches the stretch where San Francisquito Creek runs on the north edge of the domain. The water that overtops the bank there leaves the model, and the outflow rises again to 663.01 m³/s at 3.0 h. At that time most of the outflow crosses the north edge. At 6 h the outflow is 186.36 m³/s.

## 10 m and 30 m over the same six hours

The 30 m example runs for 24 h. The table compares the first 6 h of both runs, from the same 15 min samples and saved frames:

| Result, first 6 h | 30 m | 10 m |
|---|---|---|
| Drainage area | 156.8 km² | 157.7 km² |
| First peak of the outflow across the domain edge | 402.84 m³/s at 75 min | 377.13 m³/s at 75 min |
| Lowest outflow between the two peaks | 110.1 m³/s at 2.0 h | 123.1 m³/s at 1.75 h |
| Peak outflow across the domain edge | 473.69 m³/s at 3.5 h | 663.01 m³/s at 3.0 h |
| Outflow at 6 h | 144.72 m³/s | 186.36 m³/s |
| Water that left across the edge | 5.34 million m³ (34% of the rain) | 6.27 million m³ (40% of the rain) |
| Maximum depth in the saved frames | 5.82 m | 7.38 m |
| Area deeper than 1 m in some saved frame | 4.2 km² | 4.3 km² |

The storm and the other inputs are the same, so the differences come from the terrain: its finer grid, and a DEM from a different 3DEP download. On the 10 m grid the hillslope peak is slightly lower. The creek water that overtops onto the north edge arrives 30 min earlier, and its peak is 40% higher. In six hours, 17% more water leaves the domain. The deepest water is in the Searsville Lake basin on both grids, 1.56 m deeper on the 10 m grid.

## How to run it

The case is in the HydroPol2D MATLAB repository, in `Examples/Stanford`. In MATLAB, from the root of the repository:

```matlab
addpath(fullfile(pwd,'Examples','Stanford'))
run_stanford_local_case('Resolution',10, ...
  'StaticFolder',fullfile('Examples','Stanford','Static_10m_LiDAR'), ...
  'SimulationMinutes',360, ...
  'RainfallTimeseriesPath',fullfile('Examples','Stanford','Forcing','Rainfall','Rainfall_Intensity_Website_100mmh_1h_24h.csv'), ...
  'RecordTimeMapsMinutes',15,'RecordTimeHydrographsMinutes',15, ...
  'OutputTag','Stanford_10m_LiDAR_Website_100mmh_1h_6h')
```

The results go to `Examples/Stanford/Outputs/Reruns_CurrentModel/Stanford_10m_LiDAR_Website_100mmh_1h_6h/Modeling_Results`, with the same files as the 30 m example. The 10 m grid has nine times as many cells as the 30 m grid. The run took about 10 h on the CPU of a laptop (Apple M4, 24 GB).
