---
title: Check a case
---
import useBaseUrl from '@docusaurus/useBaseUrl';

# Check a case

Every build ends with the preflight check. **Check a case** runs it again on any prepared case,
without rebuilding it: for example after you moved a case, edited one of its files, or prepared
it on another day.

1. Open **Check a case**.
2. Paste the folder of the case into **Prepared case directory**.
3. Click **Run preflight**.

The page then says either "Ready to run: all preflight checks passed." or "Not ready to run.",
followed by the list of problems. For a case that is ready, the checked values are in a folded
panel and the run panels follow ([Run the case](run-the-case)). The **Preflight log** keeps the
messages.

## What it checks {#what-it-checks}

| Group | Checks |
|---|---|
| Files | every map and series the chosen model needs is there, and the model files (`case.yaml`, `run_case.m` and their inputs) are complete |
| Grids | every map has the grid of `DEM.tif` and covers every active cell, and the mesh is complete for quadtree and Urban Area Only cases |
| Values | no negative depth to bedrock, soil water, leaf area or rainfall, albedo and impervious fraction between 0 and 1, groundwater between the surface and the bedrock, river widths and depths present |
| Time | every rainfall time step from the start of the warm-up to the end, on one grid over the whole domain, and weather that covers the period |
| Terrain | the HydroBathyDEM report exists and its terrain is accepted for a model run |
| Domain | for a Catchment case, the final catchment and the first HydroSHEDS outline differ by less than a factor of two |
| Boundaries | for Urban Area Only, every outer edge has exactly one condition, and every enabled GloFAS or GTSM boundary has data |

The full report is `quality_report/preflight.json`, with `ready_to_run`, the list of `failures` and
the checked values.

Do not run a case that is not ready. Read the problems, correct the inputs (often by preparing the
case again with other settings), and check again. A passing check says the case is complete and
consistent. It is not a calibration or a validation of the model.

## Groundwater calibration {#groundwater-calibration}

When a Catchment case was prepared with **Shallow-aquifer Ksat,h and Sy** set to **Calibrate from
observed streamflow**, the page shows **Calibrate groundwater parameters** for it. The calibration
fits one horizontal conductivity and one specific yield of the shallow aquifer to the recessions
of an observed hydrograph, then writes them into the case and checks it again.

| Setting | What it sets |
|---|---|
| **Observed streamflow** | **USGS gauge** (with **USGS gauge ID**, for example 02145910) or **Local CSV** (with **Observed-discharge CSV**, columns `date` and `observed_discharge_m3_s`) |
| **Observation start**, **Observation end** | the period of the record to use |
| **Ksat,h candidates (m/s)**, **Sy candidates** | the values to try (layered cases: **Soil Kh multipliers** and **Regolith Kh multipliers**) |
| **Saved shallow-flow fraction** | the starting state is saved when shallow flow falls to this share of the total flow (0.05) |
| **HydroPol2D Python folder** | a folder that holds HydroPol2D Python |

**Run and apply groundwater calibration** starts it in the background, and **Refresh calibration
status** updates the page. The observed flow is filtered with the Lyne-Hollick method, the
recessions form a master recession curve, and a groundwater experiment on a regular grid fits the
two values. When it ends, the page shows "Groundwater calibration was applied and the case passed
preflight.", the fitted **Ksat,h** and **Specific yield**, the chosen recession day, and a figure of
the observed and calibrated recessions. The case cannot be run before this final check passes.

The calibration needs HydroPol2D Python. The app does not download it, so choose a folder that
already holds it. The method is described in
[Groundwater recession calibration](../calibration/groundwater-recession).
