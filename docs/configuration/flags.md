---
title: Model Flags
---

# Model Flags

HydroPol2D is controlled through a set of binary and categorical flags defined in `General_Data.xlsx`.

These flags determine:

- which physical processes are active  
- how forcing is applied  
- which numerical schemes are used  
- how outputs are generated  

Each flag must be set consistently with the selected modeling approach.

---

## Boundary Condition Flags

| Flag | Description |
|------|------------|
| $\mathrm{flag\_rainfall}$ | Activates rainfall forcing over the domain |
| $\mathrm{flag\_spatial\_rainfall}$ | Uses spatially distributed rainfall instead of uniform rainfall |
| $\mathrm{flag\_ETP}$ | Activates evapotranspiration computation via meteorological forcing |
| $\mathrm{flag\_input\_rainfall\_map}$ | Uses raster-based rainfall input (e.g., satellite or gridded products) |
| $\mathrm{flag\_rainfall\_multiple\_runs}$ | Under Development |
| $\mathrm{flag\_data\_source}$ | Under Development |
| $\mathrm{flag\_inflow}$ | Activates inflow hydrograph boundary conditions |
| $\mathrm{flag\_satellite\_rainfall}$ | Uses satellite-derived rainfall products |
| $\mathrm{flag\_alternated\_blocks}$ | Activates Alternating Block design storm method |
| $\mathrm{flag\_huff}$ | Activates Huff storm distribution method |
| $\mathrm{flag\_stage\_hydrograph}$ | Applies stage (water level) boundary condition |
| $\mathrm{flag\_input\_ETP\_map}$ | Uses raster-based evapotranspiration inputs |

---

## Hydrologic–Hydrodynamic–Water Quality Flags

| Flag | Description |
|------|------------|
| $\mathrm{flag\_infiltration}$ | Activates infiltration into the soil |
| $\mathrm{flag\_critical}$ | Limits flow velocity to the critical flow (Froude = 1) |
| $\mathrm{flag\_D8}$ | Activates D8 flow routing scheme |
| $\mathrm{flag\_CA}$ | Activates Cellular Automata routing |
| $\mathrm{flag\_inertial}$ | Activates Local Inertial shallow water equations (recommended default) |
| $\mathrm{flag\_waterbalance}$ | Distributed mass balance errors in inflow cells (default 0) |
| $\mathrm{flag\_waterquality}$ | Activates water quality transport module |
| $\mathrm{flag\_reservoir}$ | Activates reservoir internal boundary conditions |
| $\mathrm{flag\_wq\_model}$ | Defines which wash-off model to use|
| $\mathrm{flag\_groundwater\_modeling}$ | Activates groundwater recharge computation |
| $\mathrm{flag\_real\_time\_satellite\_rainfall}$ | Enables real-time satellite rainfall ingestion with Persiann |
| $\mathrm{flag\_dam\_break}$ | (Under Development) |
| $\mathrm{flag\_human\_instability}$ | Activates human stability hazard modeling |
| $\mathrm{flag\_boundary}$ | Enforce all boundary cells as outlet cells |
| $\mathrm{flag\_numerical\_scheme}$ | 1: local inertial model, 2: upwind scheme, 3: central scheme |
| $\mathrm{flag\_outlet\_type}$ | 1: normal flow, 2: critical flow |
| $\mathrm{flag\_adaptive\_timestepping}$ | Celerity-based, 2: Celerity + Advection-based stability criteria (1 as default) |
| $\mathrm{flag\_neglect\_infiltration\_river}$ | Disables infiltration in river cells |
| $\mathrm{flag\_subgrid}$ | Activates subgrid hydraulic representation |
| $\mathrm{flag\_spatial\_albedo}$ | Uses spatially distributed albedo instead of uniform values |
| $\mathrm{flag\_river\_rasters}$ | Uses raster-based river geometry inputs |
| $\mathrm{flag\_baseflow}$ | Solves 2D Boussinesq Equation for Aquifers|
| $\mathrm{flag\_kinematic}$ | Activates kinematic wave approximation |
| $\mathrm{flag\_diffusive}$ | Activates diffusive wave routing |
| $\mathrm{flag\_DTM}$ | Uses digital terrain model corrections or processing |
| $\mathrm{flag\_abstraction}$ | Activates water abstraction or withdrawal processes |
| $\mathrm{flag\_overbanks}$ | Activates floodplain overflow dynamics with a subgrid model|
| $\mathrm{flag\_snow\_modeling}$ | Activates snow accumulation and melt processes |
| $\mathrm{flag\_WQ\_Rasters}$ | Uses raster-based pollutant inputs |

---

## Performance Flags

| Flag | Description |
|------|------------|
| $\mathrm{flag\_GPU}$ | Enables GPU acceleration |
| $\mathrm{flag\_single}$ | Uses single precision arithmetic for performance optimization |

---

## Initial Condition Flags

| Flag | Description |
|------|------------|
| $\mathrm{flag\_warmup}$ | Activates model warm-up period to stabilize initial conditions |
| $\mathrm{flag\_initial\_buildup}$ | Initializes pollutant buildup conditions |

---

## DEM Treatment Tools

| Flag | Description |
|------|------------|
| $\mathrm{flag\_resample}$ | Activates raster resampling to target resolution |
| $\mathrm{flag\_smoothening}$ | Applies DEM smoothing filter |
| $\mathrm{flag\_trunk}$ | Smooth only the main river trunk from DEM |
| $\mathrm{flag\_fill\_DEM}$ | Fills sinks in DEM for hydrological consistency |
| $\mathrm{flag\_smooth\_cells}$ | Applies cell-level smoothing to terrain |
| $\mathrm{flag\_reduce\_DEM}$ | Reduces DEM resolution at river cells|

---

## Extra Flags

| Flag | Description |
|------|------------|
| $\mathrm{flag\_export\_maps}$ | Enables export of raster outputs |
| $\mathrm{flag\_dashboard}$ | Activates dashboard-style outputs or visualization |
| $\mathrm{flag\_elapsed\_time}$ | Tracks simulation runtime |
| $\mathrm{flag\_obs\_gauges}$ | Activates output extraction at observation gauge locations |

---

## Notes

- Flags must be used consistently to avoid conflicting configurations  
- Only one routing scheme should be active at a time (e.g., inertial vs diffusive vs kinematic)  
- Subgrid and raster-based river options should not be combined unless explicitly supported  
- Adaptive time stepping is strongly recommended for numerical stability  
- GPU execution requires compatible data structures and hardware  

---

## Summary

Flags define the structure of a HydroPol2D simulation.

They control:

- physics  
- numerics  
- forcing  
- outputs  

Correct configuration of these flags is essential for stable and physically meaningful simulations.