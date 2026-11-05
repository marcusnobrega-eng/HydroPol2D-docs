---
title: Case settings
---
import useBaseUrl from '@docusaurus/useBaseUrl';

# Case settings

Below the model area, each tab of **Prepare a case** has the same groups of settings, from top to
bottom: **Grid and period**, **Forcing and model adapter**, **Simulated processes**, **River
representation** (with **Hydraulic parameters**), **Saved outputs**, **Urban boundary conditions**
(Urban Area Only), the rainfall folders, and **Folders and advanced paths**.

The defaults differ between the urban tabs and the Catchment tab:

| Setting | Urban Basin and Urban Area Only | Catchment |
|---|---|---|
| Cell size | 90 m | 1,000 m |
| River initiation area | 5 km² | 10 km² |
| Rainfall product | IMERG (30 minutes) | MSWEP (3 hourly) |
| Deep-aquifer baseflow | off | on |
| Output package | Standard | Full |
| Map interval | 60 minutes | 180 minutes |
| Hydrograph interval | 10 minutes | 60 minutes |

Any change of a setting asks for a new [preview](preview-and-cost) before the case can be prepared.

## Grid and period {#grid-and-period}

| Setting | What it sets |
|---|---|
| **Grid type** | Urban tabs only. **Uniform grid**, or **Quadtree grid** (see below). |
| **Cell size (m)** | The model cell size. It cannot be finer than the terrain: about 30 m with FABDEM. |
| **Warm-up (days)** | Days simulated before the start date, so that soils and rivers settle. Rain and weather are prepared from the start of the warm-up. Default 0. |
| **River initiation area (km2)** | The upstream area at which a river channel begins. |
| **Terrain source** | **FABDEM**, or **Local georeferenced DEM** with its **Local DEM path**. |
| **Simulation start date (UTC)**, **Start time (UTC)** | The start of the simulation. |
| **Simulation end date (UTC)**, **End time (UTC)** | The end of the simulation. |

Dates are in UTC, from 1979-01-01 to today. You can type the year in the date field.

### Quadtree grid {#quadtree-grid}

A quadtree grid uses square cells of several sizes. The city keeps the fine cells and the rest of
the domain gets coarser ones, which cuts the number of cells of a large basin.

- **Fine cell size (m)**: the cells over the city and its buffer.
- **Coarse cell size (m)**: the cells far from the city. It must be the fine size times 2, 4, 8
  and so on. The default is four times the fine size.
- **Fine-grid buffer (m)**: how far around the city the fine cells reach (120 m by default).

Between the levels, the transition uses two cells per level, and neighbouring cells differ by at
most a factor of two. Rivers do not change the cell size. With 90 m and 360 m, for example, the
city and 120 m around it have 90 m cells, a band of 180 m cells follows, and the rest of the basin
has 360 m cells. The model reads this mesh directly with its native mesh solver.

## Forcing and model adapter {#forcing}

**Rainfall product** chooses one rainfall source for the whole case. The Builder never fills one
product with another.

| Rainfall product | Time step | Area | Account |
|---|---|---|---|
| **IMERG (30 minutes)** | 30 min | global | NASA Earthdata |
| **MSWEP (hourly)** | 1 h | global | GloH2O approval and rclone |
| **MSWEP (3 hourly)** | 3 h | global | GloH2O approval and rclone |
| **ERA5 (hourly)** | 1 h | global | Copernicus CDS |
| **AORC CONUS (hourly, approximately 1 km)** | 1 h | contiguous United States | none |

Before the preview, the page shows the period each source has (for example "NASA IMERG Final Run
availability") and stops a request outside it. MSWEP hourly cases start on a full UTC hour, and
3-hourly cases at 00, 03, 06, 09, 12, 15, 18 or 21 UTC. The weather always comes from ERA5. Rain and weather stay on their own grids, and
HydroPol2D samples them during the run: a 90 m model grid does not make the rain 90 m.

**Prepare for** chooses the model files the case gets:

| Prepare for | The case gets |
|---|---|
| **HydroPol2D Python** | `hydropol_python/case.yaml` and `run_case.py`, for HydroPol2D Studio |
| **HydroPol2D MATLAB** | `hydropol_matlab/run_case.m`, for HydroPol2D MATLAB |
| **Python and MATLAB** | both |
| **Inputs only** | the maps and series, without model files |

## Simulated processes {#processes}

**Canopy interception**, **Infiltration**, **Groundwater** and **Evapotranspiration** are ticked by
default. Untick a process to leave it out. The maps that depend on it are then left out of the
saved outputs, and the groundwater settings below are greyed out when **Groundwater** is off.
Rainfall, local-inertial surface routing and critical-flow boundaries always stay on.

## River representation {#river-representation}

**Subgrid formulation** sets how rivers narrower than a cell are represented:

| Choice | What it does |
|---|---|
| **Auto** | **No subgrid** when the largest cells match the terrain resolution. Otherwise **Neal channel** on uniform grids, and **Hydraulic tables** on quadtree grids and Urban Area Only cases. |
| **Neal channel** | a channel of given width and depth inside each river cell. Uniform grids only, so it is not offered for quadtree grids or Urban Area Only. |
| **Hydraulic tables** | storage and conveyance tables computed from the fine terrain. **Hydraulic table coverage** chooses **Rivers only** or **All active cells**. |
| **No subgrid** | the cell terrain alone. |

**All active cells** treats every cell as a level pool. The page warns that this can distort the
flow driven by rain on steep hillslopes, so choose it on purpose. The terrain conditioned by
HydroBathyDEM becomes the model surface. After the build, the page reports the share of cells it
changed and the largest lowering and raising.

<p align="center">
  <img src={useBaseUrl('/img/builder/builder-river-hydraulics.png')} width="760" alt="The Simulated processes check boxes, the River representation choices Auto, Neal channel, Hydraulic tables and No subgrid, and the open Hydraulic parameters panel with Manning n values, river-groundwater exchange, deep-aquifer settings, the shallow-aquifer parameter source, riverbed conductivity and thickness, the confirmation box and the optional riverbed conductivity raster" />
</p>

<p align="center">
  <em>Figure 1. Simulated processes, River representation and the open Hydraulic parameters panel of an Urban Basin case. The deep-aquifer settings are greyed out because Deep-aquifer baseflow is off.</em>
</p>

### Hydraulic parameters {#hydraulic-parameters}

The **Hydraulic parameters** panel is folded by default.

| Setting | Default | What it sets |
|---|---|---|
| **Channel Manning n** | 0.035 | roughness of the river channels |
| **Surface Manning fallback** | 0.05 | roughness where the land-cover table has none |
| **River-groundwater exchange** | on | water exchange between rivers and groundwater (needs **Groundwater**) |
| **Deep-aquifer baseflow** | on in Catchment | a slow deep store per subbasin that feeds baseflow (Catchment tab, without hydraulic tables) |
| **Deep recharge fraction** | 0.05 | share of recharge that goes to the deep store |
| **Deep response time (days)** | 180 | how slowly the deep store drains |
| **Subbasin threshold (km²)** | 100 | the size of the deep-aquifer subbasins |
| **Deep-aquifer starting state** | Empty | **Empty**, **Baseflow on the start date** (with **Deep baseflow q0 (mm/day)**) or **Steady state from mean recharge** (with **Mean recharge (mm/year)**) |
| **Shallow-aquifer Ksat,h and Sy** | Spatial maps with class fallback | see below |
| **Riverbed conductivity (m/s)** | 1.0e-6 | conductivity of the riverbed for the exchange |
| **Riverbed thickness (m)** | 0.50 | thickness of the riverbed |
| **Confirm this riverbed conductivity for the case** | not ticked | must be ticked while the exchange is on |
| **Riverbed conductivity raster (optional)** | empty | a map that replaces the single value |

The riverbed conductivity has no reliable global map, so the Builder asks you to confirm the
value. With the exchange on and the box not ticked, the preview stops with "Confirm riverbed
hydraulic conductivity when river-groundwater exchange is enabled."

**Shallow-aquifer Ksat,h and Sy** sets the horizontal conductivity and the specific yield of the
shallow aquifer:

- **Spatial maps with class fallback**: the groundwater maps where they have values, and the class
  tables elsewhere.
- **Uniform effective values**: one **Uniform groundwater Ksat,h (m/s)** (default 1.000e-5) and one
  **Uniform specific yield Sy** (default 0.100) over the whole domain, for example values from a
  recession calibration.
- **Calibrate from observed streamflow**: Catchment tab, when the case is prepared for Python. The
  case is prepared first, and the calibration then runs from **Check a case**
  ([Check a case](check-a-case#groundwater-calibration)).

## Saved outputs {#saved-outputs}

| Setting | What it sets |
|---|---|
| **Output package** | **Quick** saves the extremes and the hydrographs. **Standard** adds the native map archive, figures and the main videos. **Full** also writes GeoTIFF copies of every saved map. |
| **Map interval (minutes)** | how often the maps are saved |
| **Hydrograph interval (minutes)** | how often the hydrographs and diagnostics are saved |

The tick boxes below choose the saved maps: overbank flood depth, channel and floodplain velocity,
rainfall intensity, cumulative rainfall, cumulative infiltration, groundwater depth, cumulative
groundwater recharge, cumulative capillary rise, root-zone saturation, transmission-zone
saturation, cumulative potential evaporation and cumulative actual evapotranspiration. A map whose
process is off is greyed out. The preview estimates the size of what you choose.

<p align="center">
  <img src={useBaseUrl('/img/builder/builder-saved-outputs.png')} width="760" alt="The Saved outputs group with Output package Standard, map interval 60 minutes, hydrograph interval 10 minutes and twelve ticked map outputs" />
</p>

<p align="center">
  <em>Figure 2. Saved outputs of an urban case: the Standard package, maps every hour, hydrographs every 10 minutes and all twelve maps.</em>
</p>

## Urban boundary conditions {#urban-boundary-conditions}

This group is on the **Urban Area Only** tab.

| Setting | What it sets |
|---|---|
| **Exterior buffer (km)** | the buffer around the urban footprint (1 km by default) |
| **GloFAS river inflows** | river inflows from GloFAS v4 where rivers enter the domain. The inflow uses the channel width of the case's river map. |
| **GloFAS time handling** | **step** or **linear** between GloFAS values |
| **Coastal water level** | **Disabled**, **GTSM total water level** or **GTSM astronomical tide** |
| **Tide time handling** | **linear** or **step** between GTSM values |
| **Groundwater boundary** | **Local storage only**, **Dynamic no-flow** or **Dynamic fixed head** |
| **GTSM-to-model datum offset (m)** and **Datum confirmed** | shown when a coastal water level is on. GTSM refers to mean sea level. Enter the local offset to the datum of the terrain and tick **Datum confirmed**. Zero, confirmed, says the two are the same here. |
| **Reviewed boundary overrides (optional JSON)** | a file of reviewed boundary choices |

The tide goes only to low outer cells that WorldCover marks as permanent water, near the GTSM
coast. GTSM gives the water level, not the coastline. GTSM series end in 2024, so later dates need
**Disabled**. The build writes the boundary plan and series under `processed_inputs/Forcing/Boundary`
and stops the check if edges overlap or an enabled boundary has no data.

<p align="center">
  <img src={useBaseUrl('/img/builder/builder-urban-boundaries.png')} width="760" alt="The Urban boundary conditions group with a 1 km exterior buffer, GloFAS river inflows not ticked, GloFAS time handling step, coastal water level Disabled, tide time handling linear, groundwater boundary Local storage only and an empty overrides field, with the note that the priority is tide, then GloFAS inflow, then critical flow" />
</p>

<p align="center">
  <em>Figure 3. Urban boundary conditions at their defaults: critical flow on every outer edge.</em>
</p>

## Rainfall folders {#rainfall-folders}

**Existing rainfall directory (optional)** uses rainfall files you already have instead of a
download. The folder must hold every time step from the start of the warm-up to the end of the
simulation, as GeoTIFFs in mm/h named like this:

```text
IMERG_30min_mmhr_YYYY_MM_DD_HH_MM.tif
AORC_1h_mmhr_YYYY_MM_DD_HH_MM.tif
ERA5_1h_mmhr_YYYY_MM_DD_HH_MM.tif
MSWEP_1h_mmhr_YYYY_MM_DD_HH_MM.tif
MSWEP_3h_mmhr_YYYY_MM_DD_HH_MM.tif
```

For an MSWEP product without a local folder, two more fields appear: **MSWEP rclone folder** and
**Shared-folder ID (optional)**. When rclone already has access to the MSWEP folder, the page finds
it and fills both. See [Data sources and accounts](data-accounts#mswep).

## Folders and advanced paths {#folders}

The **Folders and advanced paths** panel is folded by default.

| Setting | What it sets |
|---|---|
| **Output directory** | where new cases go. In the app: `Documents/HydroPol2D Case Builder/outputs` in your home folder. |
| **Cache directory** | where downloaded data and tools are kept (`~/.cache/hydropol2d-case-builder`), shared by all cases |
| **HydroPol2D checkout (optional)** | a HydroPol2D MATLAB folder, recorded with the case |
| **Vadose and aquifer parameters** | **Class tables**, or **SoilGrids + GLHYMPS (CONUS automatic)** |
| **Groundwater Kh/Kv ratio** | the ratio of horizontal to vertical conductivity, used below 2 m (100 by default) |
| **Subsurface scheme** | **legacy**, or **layered** (soil layers over rock layers down to the bedrock, for HydroPol2D Python) |
| **Rock specific yield** | layered only: **derived_capped** (capped by the GLHYMPS porosity) or **derived** |
| **Spatial soil parameter raster directory (optional)** | a folder of soil-parameter GeoTIFFs. Their values replace the class tables where they have data. |

<p align="center">
  <img src={useBaseUrl('/img/builder/builder-folders.png')} width="760" alt="The open Folders and advanced paths panel with the output directory, the cache directory, an empty HydroPol2D checkout field, Vadose and aquifer parameters Class tables, a Kh/Kv ratio of 100, subsurface scheme legacy, rock specific yield derived_capped greyed out, and the spatial soil parameter raster directory" />
</p>

<p align="center">
  <em>Figure 4. Folders and advanced paths. Rock specific yield is greyed out because the subsurface scheme is legacy.</em>
</p>
