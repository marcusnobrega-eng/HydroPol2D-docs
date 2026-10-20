---
title: Model Flags
---

# Model Flags

HydroPol2D is controlled through binary and categorical flags defined in `General_Data.xlsx`. This page documents the public behavior exposed by those flags and highlights where a flag activates a validated default path versus a diagnostic or experimental pathway.

---

## Boundary and Forcing Flags

| Flag | Description |
|---|---|
| $\mathrm{flag\_rainfall}$ | Activates rainfall forcing over the domain. |
| $\mathrm{flag\_spatial\_rainfall}$ | Uses spatially distributed rainfall instead of uniform rainfall. |
| $\mathrm{flag\_ETP}$ | Activates evapotranspiration computation from meteorological forcing. |
| $\mathrm{flag\_input\_rainfall\_map}$ | Uses raster-based rainfall input. |
| $\mathrm{flag\_rainfall\_multiple\_runs}$ | Under development. |
| $\mathrm{flag\_data\_source}$ | Under development. |
| $\mathrm{flag\_inflow}$ | Activates inflow hydrograph boundary conditions. |
| $\mathrm{flag\_satellite\_rainfall}$ | Uses satellite-derived rainfall products. |
| $\mathrm{flag\_alternated\_blocks}$ | Activates the Alternating Block design-storm method. |
| $\mathrm{flag\_huff}$ | Activates the Huff storm distribution method. |
| $\mathrm{flag\_stage\_hydrograph}$ | Applies stage (water-level) boundary conditions. |
| $\mathrm{flag\_input\_ETP\_map}$ | Uses raster-based evapotranspiration inputs. |

---

## Process and Routing Flags

| Flag | Description |
|---|---|
| $\mathrm{flag\_infiltration}$ | Activates infiltration into the soil and vadose storage. |
| $\mathrm{flag\_groundwater\_modeling}$ | Activates groundwater recharge and local groundwater-table coupling. With layered soil enabled, this follows the current default layered vadose-groundwater path. |
| $\mathrm{flag\_groundwater\_async}$ | Uses asynchronous saturated-groundwater updates while keeping vadose exchange coupled every surface step. Recommended when groundwater is active. |
| $\mathrm{groundwater\_target\_dt\_min}$ | Target groundwater update interval in minutes. |
| $\mathrm{groundwater\_min\_dt\_min}$ | Minimum groundwater update interval in minutes. |
| $\mathrm{groundwater\_max\_head\_change\_m}$ | Maximum accumulated groundwater head change before forcing an update. |
| $\mathrm{groundwater\_courant}$ | Safety factor used in the explicit groundwater timestep cap. |
| $\mathrm{flag\_capillary\_rise}$ | Enables layered capillary rise from shallow groundwater into vadose storage. |
| $\mathrm{flag\_baseflow}$ | Activates 2D Boussinesq lateral groundwater routing. |
| $\mathrm{flag\_snow\_modeling}$ | Activates per-LULC snow accumulation, melt, sublimation, density, and depth. Requires internal meteorological forcing: `flag_ETP = 1` and `flag_input_ETP_map = 0`. |
| $\mathrm{flag\_waterquality}$ | Activates water-quality transport. |
| $\mathrm{flag\_wq\_model}$ | Selects the pollutant build-up/washoff model. |
| $\mathrm{flag\_human\_instability}$ | Activates human-instability diagnostics. Publicly documented implemented modes are `1` and `3`; mode `2` is not implemented. |
| $\mathrm{flag\_reservoir}$ | Activates reservoir or internal hydraulic-control logic. |
| $\mathrm{flag\_critical}$ | Applies a critical-flow limiter where supported by the routing family. |
| $\mathrm{flag\_boundary}$ | Enforces all boundary cells as outlet cells. |
| $\mathrm{flag\_neglect\_infiltration\_river}$ | Disables infiltration in river cells. |
| $\mathrm{flag\_real\_time\_satellite\_rainfall}$ | Enables real-time satellite rainfall ingestion with Persiann. |
| $\mathrm{flag\_dam\_break}$ | Under development. |
| $\mathrm{flag\_river\_rasters}$ | Uses raster-based river geometry inputs. |
| $\mathrm{flag\_spatial\_albedo}$ | Uses spatially distributed albedo instead of uniform values. |
| $\mathrm{flag\_DTM}$ | Uses digital terrain model corrections or processing. |
| $\mathrm{flag\_abstraction}$ | Activates water abstraction or withdrawal processes. |
| $\mathrm{flag\_WQ\_Rasters}$ | Uses raster-based pollutant inputs. |

---

## Routing-Family Flags

| Flag | Description |
|---|---|
| $\mathrm{flag\_inertial}$ | Activates the local inertial shallow-water solver. This is the recommended default routing family. |
| $\mathrm{flag\_full\_momentum}$ | Activates the full-momentum shallow-water solver. Use as an alternative to the other major routing families, not in combination with them. |
| $\mathrm{flag\_diffusive}$ | Activates diffusive D4 routing driven by water-surface slope. |
| $\mathrm{flag\_kinematic}$ | Activates kinematic D4 routing driven by bed slope and donor depth. |
| $\mathrm{flag\_CA}$ | Activates Cellular Automata routing. |
| $\mathrm{flag\_D8}$ | Activates a secondary D8 routing pathway. This should be treated as limited-scope rather than a full parallel theory family. |
| $\mathrm{flag\_neal\_channel}$ | Activates the Neal (2012) rectangular embedded-channel representation on a structured grid. Requires local-inertial routing. |
| $\mathrm{flag\_structured\_lookup\_subgrid}$ | Activates level-dependent cell and face lookup tables on a structured grid. This mode remains gated until MATLAB-Python parity is complete. |
| $\mathrm{flag\_voronoi\_subgrid}$ | Activates HydroBathyDEM level-dependent cell and face tables on a Voronoi mesh. |
| $\mathrm{flag\_voronoi}$ | Selects Voronoi mesh topology. It is independent from `flag_voronoi_subgrid`, which selects a hydraulic representation. |
| $\mathrm{flag\_numerical\_scheme}$ | Selects the local inertial scheme variant: `1` Bates, `2` upwind, `3` centered. Applies to the inertial family, not to full momentum, diffusive, kinematic, or CA routing. |
| $\mathrm{flag\_outlet\_type}$ | Outlet treatment: `1` normal flow, `2` critical flow. |
| $\mathrm{flag\_adaptive\_timestepping}$ | Selects adaptive time-step control. |

---

## Neal (2012) Subgrid Model Configuration

The supported channel-subgrid mode follows [Neal et al. (2012)](https://doi.org/10.1029/2012WR012514). Use the following flag combination:

| Flag | Required value |
|---|---:|
| `flag_inertial` | `1` |
| `flag_neal_channel` | `1` |
| `flag_structured_lookup_subgrid` | `0` |
| `flag_voronoi_subgrid` | `0` |
| `flag_voronoi` | `0` |
| `flag_full_momentum` | `0` |
| `flag_diffusive` | `0` |
| `flag_kinematic` | `0` |
| `flag_CA` | `0` |
| `flag_river_rasters` | `1` when channel geometry is supplied as rasters |

The active channel cells require both `RiverWidths_path` and `RiverDepths_path`. Channel width and depth must be positive, and channel width must be smaller than the model-cell resolution. The channel Manning coefficient is assigned through the river or in-bank roughness input. The surrounding LULC roughness supplies the floodplain Manning coefficient.

The solver computes channel and floodplain discharge separately on each orthogonal face and updates cell storage in volume space. The formulation and validation range are described in [Hydrodynamic Model](../theory/hydrodynamic-model#115-neal-2012-subgrid-model) and [Neal (2012) Subgrid Model Validation](../validation/neal-subgrid).

---

## Performance Flags

| Flag | Description |
|---|---|
| $\mathrm{flag\_GPU}$ | Enables GPU acceleration. |
| $\mathrm{flag\_single}$ | Uses single-precision arithmetic for performance optimization. |

---

## Initial-Condition Flags

| Flag | Description |
|---|---|
| $\mathrm{flag\_warmup}$ | Activates model warm-up for state stabilization. |
| $\mathrm{flag\_initial\_buildup}$ | Initializes pollutant buildup conditions. |

---

## DEM and Terrain Processing Flags

| Flag | Description |
|---|---|
| $\mathrm{flag\_resample}$ | Activates raster resampling to a target resolution. |
| $\mathrm{flag\_smoothening}$ | Applies DEM smoothing. |
| $\mathrm{flag\_trunk}$ | Smooths only the main river trunk. |
| $\mathrm{flag\_fill\_DEM}$ | Fills DEM sinks for hydrologic consistency. |
| $\mathrm{flag\_smooth\_cells}$ | Applies cell-level terrain smoothing. |
| $\mathrm{flag\_reduce\_DEM}$ | Reduces DEM elevation in river cells to account for channel bathymetry. |

---

## Output and Utility Flags

| Flag | Description |
|---|---|
| $\mathrm{flag\_export\_maps}$ | Enables export of raster outputs. |
| $\mathrm{flag\_dashboard}$ | Activates dashboard-style outputs or visualization. |
| $\mathrm{flag\_elapsed\_time}$ | Tracks simulation runtime. |
| $\mathrm{flag\_obs\_gauges}$ | Activates output extraction at observation gauges. |

---

## Notes

- Only one major routing family should be active at a time: `flag_full_momentum`, `flag_inertial`, `flag_diffusive`, `flag_kinematic`, or `flag_CA`.
- Select at most one subgrid formulation: Neal channel, structured lookup, or Voronoi lookup.
- The Neal (2012) channel mode requires local-inertial routing and `flag_neal_channel = 1`.
- `flag_voronoi = 1` selects mesh topology; `flag_voronoi_subgrid = 1` additionally enables Voronoi lookup hydraulics.
- Legacy `flag_subgrid` and `flag_overbanks` inputs are accepted only by the migration layer and produce an explicit warning.
- `flag_D8` should be treated as secondary/limited-scope rather than as another report-ready routing family.
- Groundwater async scheduling and capillary rise are public configuration behaviors, not hidden internal details.
- Snow parameters are entered in the LULC parameter table. `Initial_SWE_path` and `Initial_Snow_Depth_path` are optional initial-state rasters.
- Human-instability mode `2` is not implemented and should not be presented as an available public method.
