---
title: Overview
---

# Model Configuration

HydroPol2D is configured primarily through `General_Data.xlsx`. That spreadsheet selects the process stack, the routing family, the groundwater timing controls, the input files, and the optional diagnostics.

Configuration pages and theory pages serve different roles:

- theory explains what each module does;
- configuration explains which public controls expose that behavior.

## Current configuration logic

The public configuration story should match the implemented model:

- layered vadose storage and groundwater coupling are the default pathway when groundwater is active;
- the routing family includes local inertial, full momentum, diffusive D4, kinematic D4, and cellular automata;
- only one major routing family should be active at a time.

## Capability and maturity

| Capability | Main public controls | Current status |
|---|---|---|
| Hydrologic core | `flag_infiltration`, ET/rainfall/snow controls, soil/LULC tables | Default + validated |
| Layered groundwater recharge and async scheduler | `flag_groundwater_modeling`, `flag_groundwater_async`, `groundwater_target_dt_min`, `groundwater_min_dt_min`, `groundwater_max_head_change_m`, `groundwater_courant` | Default + validated |
| Capillary rise | `flag_capillary_rise` | Optional + validated in controlled benchmarks |
| Local inertial routing | `flag_inertial`, `flag_numerical_scheme` | Default + validated |
| Full-momentum routing | `flag_full_momentum` | Optional + validated in controlled benchmarks |
| Diffusive routing | `flag_diffusive` | Optional + validated in controlled benchmarks |
| Kinematic routing | `flag_kinematic` | Optional + validated in controlled benchmarks |
| Cellular automata routing | `flag_CA` | Optional + validated for conservation/routing bookkeeping |
| Human instability | `flag_human_instability` | Optional + validated for implemented modes `1` and `3` |

## Main configuration domains

### 1. Simulation and forcing control

`General_Data.xlsx` defines simulation timing, rainfall and meteorological forcing, inflow and stage boundaries, output cadence, and runtime options such as adaptive time stepping or GPU execution.

### 2. Routing-family selection

The current public routing interface includes:

- `flag_inertial`
- `flag_full_momentum`
- `flag_diffusive`
- `flag_kinematic`
- `flag_CA`

Only one of these major routing flags should be active in a given run. D8 exists as a secondary pathway, but it should not be documented as a parallel theory family to the main shallow-water and D4 options.

### 3. Groundwater controls

When groundwater modeling is active, HydroPol2D now exposes behavior that should be documented explicitly:

- asynchronous saturated-groundwater updates;
- head-change-triggered groundwater solves;
- explicit groundwater stability capping;
- optional capillary rise;
- lateral Boussinesq flow when baseflow is active.

### 4. Hazard and water-quality diagnostics

Optional modules such as water quality and human instability are controlled through their own flags and parameter sections. For human instability specifically, the public docs should reflect that:

- mode `1` is implemented;
- mode `3` is implemented;
- mode `2` is not implemented.

## Recommended reading of a configuration

For most public-facing HydroPol2D runs, readers should be able to infer:

1. which routing family is active;
2. whether groundwater is coupled only locally or also laterally through Boussinesq flow;
3. whether capillary rise is enabled;
4. whether human-instability or water-quality diagnostics are enabled.

If those four questions are clear, the configuration is aligned with the current model story.
