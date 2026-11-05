---
title: Prepare a case
---
import useBaseUrl from '@docusaurus/useBaseUrl';

# Prepare a case

After a preview with the current settings, **Prepare complete case** builds the case. A status
box shows the stage and a progress bar. The build:

1. downloads the data it does not have yet: terrain, land cover, soils, depth to bedrock,
   groundwater, leaf area, and the rain and weather of the period (the first case of a region
   takes longest; later cases reuse the cache);
2. conditions the terrain with HydroBathyDEM, which comes with the app, so that water reaches the
   outlets, and gives the river channels widths and depths;
3. for a Catchment case, delineates the final catchment on the model grid;
4. maps every layer onto the model grid, and writes the rain, weather and boundary series;
5. writes the model files you chose under **Prepare for**;
6. runs the [preflight check](check-a-case).

When it ends, the box says "Case preparation complete" and the page shows the case, the result of
the check and the run panels ([Run the case](run-the-case)). If it stops, the box says "Case
preparation stopped" with the error, and the **Process log** has the details. A failed build keeps
the files it downloaded, so the next attempt resumes.

How long it takes depends on the size of the domain, the period and the data services. The 10 m
San Francisquito Creek case below (99 km², 987,647 active cells) took 2 to 4 minutes, most of it
waiting for the Copernicus service, and downloaded about 10 MB.

<p align="center">
  <img src={useBaseUrl('/img/builder/stanford-terrain.jpg')} width="620" alt="Shaded terrain of the San Francisquito Creek catchment at Stanford, California, on a 10 m grid, with the river network in blue and the catchment edge" />
</p>

<p align="center">
  <em>Figure 1. Terrain of the San Francisquito Creek catchment prepared by the Case Builder on a 10 m grid, with its river network and the catchment edge. The terrain is USGS 3DEP, which you give as a local DEM or choose on the command line.</em>
</p>

<p align="center">
  <img src={useBaseUrl('/img/builder/stanford-layers.png')} width="760" alt="Three maps of the San Francisquito Creek case on the same 10 m grid: land cover classes, river channel widths, and depth to bedrock" />
</p>

<p align="center">
  <em>Figure 2. Three more layers of the same case on the same grid: land cover, the river channels and the depth to bedrock.</em>
</p>

## What is in the case folder {#case-folder}

The folder is named after the place, the cell size and the start date, for example
`tucson_urban_only_250m_20210723`. A complete case has this general layout. Folders appear only
when the case needs them: `hydropol_matlab` is absent from a case prepared for Python only, for
example.

```text
CASE_DIR/
├── case.json                     the request and the domain estimate
├── manifest.json                 every source, version and file of the case
├── domain.gpkg                   the model domain
├── final_domain.gpkg             Catchment: the catchment on the model grid
├── outlet_candidates.gpkg        Catchment: the entered outlet and the three candidates
├── preliminary_catchment.gpkg    Catchment: the first HydroSHEDS outline
├── hydropol_config.json          the model settings of the case
├── input_contract.json           the list of model inputs and their files
├── figures/                      domain_preview.html and .png, other preview maps
├── hydropol_python/              case.yaml, run_case.py and the rainfall NetCDF
├── hydropol_matlab/              run_case.m and its input paths
├── processed_inputs/
│   ├── Static/                   the maps on the model grid
│   └── Forcing/                  rain, weather and boundary series
├── rainfall_summaries/           rainfall totals for checking
├── quality_report/               preflight.json and the other checks
└── Outputs/                      model results, after a run
```

### The maps {#maps}

The main maps in `processed_inputs/Static/` are:

| File | What it holds |
|---|---|
| `DEM.tif` | the terrain conditioned by HydroBathyDEM, the model surface |
| `DomainMask.tif` | the active model domain |
| `LULC.tif` | ESA WorldCover land-cover classes |
| `SOIL.tif` | USDA soil texture classes |
| `DTB.tif` | depth to bedrock |
| `GW_table.tif` | initial groundwater elevation |
| `Initial_Soil_Moisture.tif` | initial soil water for MATLAB, in mm above the residual water content |
| `Initial_Soil_Moisture_Fraction.tif` | initial volumetric water content for Python |
| `LAI.tif` | leaf area index |
| `Albedo.tif` | albedo, a constant 0.25 in this version |
| `RiverWidths.tif`, `RiverDepths.tif` | the channel geometry |
| `D4_flow_direction.tif`, `D4_idx_facc.tif` | the HydroBathyDEM routing maps |
| `FlowDirectionD8.tif`, `FlowAccumulationD8.tif` | Catchment: the D8 maps that delineate the catchment |
| `BoundaryConditionMask.tif` | Catchment: the critical-depth outlet cells |

Categorical maps (land cover, soil classes) are resampled by nearest neighbour, and continuous
maps by interpolation suited to each source.

### The reports {#reports}

`quality_report/` keeps the checks of the build, among them:

- `preflight.json`: the result of the check ([Check a case](check-a-case));
- `terrain_domain_qa.json` and `hydraulic_terrain_qa.json`: the terrain, the domain and the
  changes HydroBathyDEM made;
- `public_static_sources.json`: the sources of the static maps;
- `rainfall_summary.json`, `initial_soil_moisture.json`, and `mswep_download.json` for MSWEP.

Keep `case.json`, `manifest.json`, `quality_report/` and the model files with any published
simulation: they record how the case was made.

## Before you trust a new case {#before-you-trust}

A case that passes the check is complete and consistent, which says nothing yet about its
accuracy. Before you read results for a new place:

1. look at the basin and the river network;
2. open the terrain, land-cover, soil, groundwater and channel maps in a GIS;
3. compare the rainfall totals with the source product;
4. check the boundary conditions and the coast;
5. compare the simulated discharge or flooding with independent observations;
6. write down any parameter you change after the case is made.
