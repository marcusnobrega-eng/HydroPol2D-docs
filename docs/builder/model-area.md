---
title: Choose the model area
---
import useBaseUrl from '@docusaurus/useBaseUrl';

# Choose the model area

**Prepare a case** has three tabs, one for each kind of model area: **Urban Basin**, **Urban Area
Only** and **Catchment**. Each tab holds all the settings of its case, so you can keep a different
case in each one. The fields start with example values. Replace them with your own place and dates.

<p align="center">
  <img src={useBaseUrl('/img/builder/case-builder-areas.svg')} width="760" alt="Three schematic maps. Urban Basin: a city at the downstream end of several upstream basins, all inside one domain edge. Urban Area Only: a city inside a buffer, with two rivers entering at the edge and the sea at one corner. Catchment: a watershed with its river network, the outlet you enter and three candidate outlets on the river" />
</p>

<p align="center">
  <em>Figure 1. The three kinds of model area, as schematic maps. The thick black line is the edge of the model domain.</em>
</p>

| Tab | Domain | Use it for |
|---|---|---|
| **Urban Basin** | the city and every HydroBASINS level-12 basin upstream of it | urban floods where the water from upstream matters |
| **Urban Area Only** | the urban footprint and a buffer around it | the city alone, with river inflows and coastal water levels at its edge |
| **Catchment** | everything upstream of an outlet you choose | a river basin, with or without a city |

## Urban Basin {#urban-basin}

**Location input** offers **City name** or **Polygon file**.

- **City name**: type the **City** and the **Country**. The Builder looks the city up in the GHSL
  Urban Centre Database R2024A.
- **Polygon file**: the path of your own urban polygon in **Urban polygon path** (a GeoPackage,
  Shapefile or any other vector file GeoPandas can read). Use it when GHSL does not list the city
  or when you need another boundary.

The Builder intersects the city with the HydroBASINS level-12 basins and follows their upstream
links. The domain is the city and all those upstream basins. HydroBASINS level 12 is the finest
global level, but it remains a regional outline. FABDEM and HydroBathyDEM give the terrain and
the routing inside it.

The two urban tabs offer two grid types: a **Uniform grid** or a **Quadtree grid** that keeps the
city fine and the rest coarse ([Case settings](settings#grid-and-period)).

<p align="center">
  <img src={useBaseUrl('/img/builder/builder-urban-basin.png')} width="760" alt="The Urban Basin tab with City Tucson and Country United States, the Quadtree grid selected, fine cell size 90 m, coarse cell size 360 m, fine-grid buffer 120 m, warm-up 0 days, river initiation area 5 km2, terrain source FABDEM, and the simulation dates and times in UTC" />
</p>

<p align="center">
  <em>Figure 2. The Urban Basin tab for Tucson, Arizona, with a quadtree grid of 90 m cells over the city and 360 m cells over the rest of the basin.</em>
</p>

## Urban Area Only {#urban-area-only}

The location input is the same as in Urban Basin. The domain is the connected urban footprint and
an **Exterior buffer** around it (1 km by default), without the upstream basins.

Every outer edge of the domain gets one boundary condition. Critical flow is the default. Where
they apply, **GloFAS river inflows** and a **Coastal water level** from GTSM replace it, in this
order of priority: tide, then GloFAS inflow, then critical flow. The settings are in
[Urban boundary conditions](settings#urban-boundary-conditions).

The preview lists the **Rivers entering the domain**: the HydroRIVERS crossings of the domain edge,
on a map and in a table. In the table you can untick **accepted** for a crossing or move it with
its **longitude** and **latitude**. **Save river-entry review** saves your choices, and **Prepare
complete case** uses them.

<p align="center">
  <img src={useBaseUrl('/img/builder/builder-river-entries.png')} width="700" alt="Rivers entering the domain for Tucson: a map of the urban-only domain with the HydroRIVERS lines and red river-entry points on its edge, and below it the table of candidates with river ID, upstream area, longitude, latitude and an accepted tick box, and the Save river-entry review button" />
</p>

<p align="center">
  <em>Figure 3. Rivers entering the Tucson urban-only domain, after the preview. Each red point is a place where a river crosses the domain edge. The table lists them with their upstream area.</em>
</p>

Urban Area Only cases run on the native mesh solver of HydroPol2D (UGRID), for both grid types.

## Catchment {#catchment}

Give the case a **Catchment name**, then choose the **Outlet input**:

| Outlet input | What you give |
|---|---|
| **Map click** | click the outlet on a topographic map. The page shows the clicked latitude and longitude. |
| **Coordinates** | **Longitude** and **Latitude** in degrees (WGS 84). |
| **Point file** | a vector file with one point. |
| **Polygon file** | a polygon, used either **exact** (as the catchment) or as a **search** area (**Polygon use**). |

Three more settings place the outlet on the river network:

- **Snap radius (km, 0 = automatic)**: how far the outlet may move to reach the river. Automatic is
  the larger of 1 km and two model cells.
- **Outlet candidate**: the preview finds the three strongest nearby outlet cells on the
  HydroSHEDS flow accumulation. Choose 1, 2 or 3. Changing it updates the preview by itself.
- **Critical outlet cells**: the number of connected boundary cells at the outlet that get a
  critical-depth condition (10 by default).

<p align="center">
  <img src={useBaseUrl('/img/builder/builder-prepare-catchment.png')} width="760" alt="The Catchment tab for San Francisquito Creek: catchment name, Coordinates selected with longitude -122.1889 and latitude 37.4239, snap radius 0, outlet candidate 1, 10 critical outlet cells, a 10 m cell size, the dates, IMERG rainfall, HydroPol2D Python and the four simulated processes ticked" />
</p>

<p align="center">
  <em>Figure 4. The Catchment tab for San Francisquito Creek at Stanford, California, with the outlet given by its coordinates and a 10 m grid.</em>
</p>

The preview draws a first outline of the catchment from HydroSHEDS. The complete build then
fills the depressions of the terrain at the model resolution, computes D8 flow directions, snaps
the outlet again and traces every cell upstream. The final catchment and the first outline are
both kept. If their areas differ by more than a factor of two, the case does not pass the check
until you review it (try another candidate or a larger snap radius).

Catchment cases use a uniform grid. They are the only cases with the deep-aquifer baseflow and
the groundwater calibration from observed streamflow ([Case settings](settings#hydraulic-parameters)).
