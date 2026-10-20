---
title: Configuration Parameters
---

# Configuration Parameters

This page documents all variables defined in `General_Data.xlsx`.

Each parameter controls a specific aspect of HydroPol2D, including:

- simulation timing  
- numerical stability  
- hydrological processes  
- hydraulic routing  
- input datasets  
- output control  

---

## Running Control

| Variable | Units | Description |
|----------|------|-------------|
| $\mathrm{time\_step\_model}$ | $\mathrm{s}$ | Initial model time step used in the simulation |
| $\mathrm{min\_time\_step}$ | $\mathrm{s}$ | Minimum allowable adaptive time step for numerical stability |
| $\mathrm{max\_time\_step}$ | $\mathrm{s}$ | Maximum allowable adaptive time step |
| $\mathrm{time\_step\_change}$ | $\mathrm{s}$ | Increment used to adjust the adaptive time step |
| $\alpha_{\min}$ | — | Minimum Courant-like stability coefficient |
| $\alpha_{\max}$ | — | Maximum Courant-like stability coefficient |
| $\mathrm{date\_begin}$ | — | Simulation start date and time |
| $\mathrm{date\_end}$ | — | Simulation end date and time |

---

## Normal Flow Boundary Condition

| Variable | Units | Description |
|----------|------|-------------|
| $\mathrm{slope\_outlet}$ | $\mathrm{m\,m^{-1}}$ | Prescribed slope used to estimate normal flow conditions at the outlet boundary |

---

## Groundwater Control

Cells D5:E8. The values below are those of the distributed workbooks.

| Variable | Units | Workbook value | Description |
|----------|----------|----------|----------|
| $\mathrm{groundwater\_courant}$ | — | 0.25 | Safety factor of the explicit groundwater time-step limit. In the layered scheme it limits the lateral-flow substeps. |
| $\mathrm{deep\_recharge\_fraction}$ | — | 0.05 | Fraction of the downward recharge sent to the deep aquifer (with $\mathrm{flag\_deep\_aquifer} = 1$). |
| $\mathrm{deep\_aquifer\_tau\_days}$ | days | 180 | Response time $\tau$ of the deep linear reservoirs. |

---

## Layered Subsurface

Block D10:F28. Read only when $\mathrm{flag\_layered\_subsurface} = 1$. See [Layered Subsurface](../theory/layered-subsurface). An empty cell keeps the default or the fallback named in the table.

| Variable | Units | Default | Description |
|----------|----------|----------|----------|
| $\mathrm{subsurface\_soil\_base\_depth\_m}$ | m | 2.0 | Soil base: bottom of the three soil slots. $\mathrm{SoilBaseDepth\_path}$ wins where finite. |
| $\mathrm{subsurface\_depth\_to\_bedrock\_m}$ | m | empty | Bottom of the whole column. Priority: $\mathrm{DTB\_path}$, then this value, then the default soil depth (1 m when $\mathrm{DTB\_path}$ is empty), with a warning. |
| $\mathrm{subsurface\_max\_depth\_m}$ | m | 50 | Cap on the column depth: the column base is $\min(\mathrm{DTB}, \text{cap})$. |
| $\mathrm{subsurface\_deep\_first\_thickness\_m}$ | m | 0.25 | Thickness of the first regolith slot below the soil base. |
| $\mathrm{subsurface\_deep\_growth\_ratio}$ | — | 2 | Thickness ratio between consecutive regolith slots. |
| $\mathrm{subsurface\_deep\_max\_thickness\_m}$ | m | 4 | Maximum regolith slot thickness. |
| $\mathrm{regolith\_theta\_s}$ | m³/m³ | 0.35 | Saturated water content of the regolith. Raster: $\mathrm{RegolithThetaS\_path}$. |
| $\mathrm{regolith\_theta\_r}$ | m³/m³ | 0.05 | Residual water content of the regolith. Raster: $\mathrm{RegolithThetaR\_path}$. |
| $\mathrm{regolith\_alpha\_vg\_m\_inverse}$ | 1/m | 2 | van Genuchten $\alpha$ of the regolith. Raster: $\mathrm{RegolithAlphaVG\_path}$. |
| $\mathrm{regolith\_n\_vg}$ | — | 1.5 | van Genuchten $n$ of the regolith. Raster: $\mathrm{RegolithNVG\_path}$. |
| $\mathrm{regolith\_ksat\_v\_mm\_h}$ | mm/h | 5 | Vertical saturated conductivity of the regolith. Raster: $\mathrm{RegolithKsatV\_path}$. |
| $\mathrm{regolith\_ksat\_h\_mm\_h}$ | mm/h | empty | Horizontal saturated conductivity of the regolith. Empty: $\mathrm{kgsat}$ of the soil table. Raster: $\mathrm{RegolithKsatH\_path}$. |
| $\mathrm{regolith\_specific\_yield}$ | — | empty | Specific yield of the regolith. Empty: $\theta_s - \theta_{fc}$ of the regolith curve. Raster: $\mathrm{RegolithSpecificYield\_path}$. |
| $\mathrm{soil\_lateral\_anisotropy}$ | — | 1 | $K_h/K_v$ of the soil slots. |
| $\mathrm{subsurface\_drainage\_substeps}$ | — | 1 | Substeps of the drainage cascade per model step. |
| $\mathrm{capillary\_field\_capacity\_head\_m}$ | m | 3.3 | Suction at field capacity. Sets $S_y = \theta_s - \theta_{fc}$ for every slot. |
| $\mathrm{groundwater\_target\_dt\_s}$ | s | 3600 | Interval of the lateral groundwater update. |
| $\mathrm{groundwater\_min\_dt\_s}$ | s | 60 | Minimum interval of the lateral groundwater update. |

---

## Feddes Root-Water Stress

Block D30:F36. Read only when $\mathrm{flag\_feddes} = 1$. See [Hydrologic Model, Section 3.5](../theory/hydrologic-model#35-feddes-root-water-uptake-stress). The heads must satisfy $0 \ge h_1 > h_2 \ge h_3 > h_4$.

| Variable | Units | Default | Description |
|----------|----------|----------|----------|
| $\mathrm{feddes\_h1\_m}$ | m | −0.1 | Wetter than this: no uptake (anaerobiosis). |
| $\mathrm{feddes\_h2\_m}$ | m | −0.25 | Start of unstressed uptake. |
| $\mathrm{feddes\_h3\_m}$ | m | −4.0 | End of unstressed uptake. |
| $\mathrm{feddes\_h3\_low\_m}$ | m | empty: $h_3$ | $h_3$ at a potential transpiration of 1 mm/day or less. |
| $\mathrm{feddes\_h3\_high\_m}$ | m | empty: $h_3$ | $h_3$ at a potential transpiration of 5 mm/day or more. |
| $\mathrm{feddes\_h4\_m}$ | m | −80 | Wilting point: no uptake. |

---

## Deep Aquifer Initial State

Block D38:F40. Read only when $\mathrm{flag\_deep\_aquifer} = 1$. Give at most one value, or a file in $\mathrm{DeepAquiferInitialState\_path}$ (T29). With none, the reservoirs start empty. See [Groundwater Model, Section 13](../theory/groundwater-model#13-deep-aquifer).

| Variable | Units | Default | Description |
|----------|----------|----------|----------|
| $\mathrm{deep\_aquifer\_initial\_baseflow\_mm\_day}$ | mm/day | empty | Deep baseflow per unit area $q_0$ on the start date. Each subbasin starts at $S_0 = q_0 A \tau$. |
| $\mathrm{deep\_aquifer\_mean\_recharge\_mm\_year}$ | mm/year | empty | Long-term mean recharge $\bar{R}$. The reservoirs start at steady state, $q_0 = f_d \bar{R}$. |

---

## Lateral Conductivity Multipliers

Block D42:F44. Read only with the layered subsurface. Specific yield is not scaled, because it comes from the retention curves. The [groundwater recession calibration](../calibration/groundwater-recession) fits both factors. The Case Builder passes the fitted values to MATLAB through `HYDROPOL_SOIL_LATERAL_CONDUCTIVITY_MULTIPLIER` and `HYDROPOL_REGOLITH_LATERAL_CONDUCTIVITY_MULTIPLIER`, which override these cells.

| Variable | Units | Default | Description |
|----------|----------|----------|----------|
| $\mathrm{soil\_lateral\_conductivity\_multiplier}$ | — | 1 | Factor on the horizontal conductivity of the three soil slots (soil $K_{sat}$ × anisotropy). |
| $\mathrm{regolith\_lateral\_conductivity\_multiplier}$ | — | 1 | Factor on the horizontal conductivity of the regolith slots. |

---

## Maps and Plots Control

| Variable | Units | Description |
|----------|------|-------------|
| $\mathrm{record\_time\_maps}$ | $\mathrm{min}$ | Time interval for saving raster outputs |
| $\mathrm{record\_time\_hydrographs}$ | $\mathrm{min}$ | Time interval for saving hydrograph outputs |
| $\mathrm{Pol\_min}$ | $\mathrm{mg\,L^{-1}}$ | Minimum pollutant concentration threshold for visualization |
| $\mathrm{depth\_wse}$ | $\mathrm{m}$ | Threshold depth used to define water surface elevation outputs |
| $\mathrm{flag\_wse}$ | — | Flag to activate water surface elevation outputs instead of depth |
| $\mathrm{record\_time\_spatial\_rainfall}$ | $\mathrm{min}$ | Time interval for exporting spatial rainfall maps |
| $\mathrm{time\_save\_ETP}$ | $\mathrm{min}$ | Time interval for saving evapotranspiration outputs |
| $\mathrm{record\_time\_spatial\_ETP}$ | $\mathrm{min}$ | Time interval for exporting spatial ETP fields |

---

## River Geometry Parameters
If `flag_reduce_dem` is activated, river cells elevation are reduced to account for river bathymetry. A set of 4 parameters are then required to describe the flow width and depth. These parameters are valid to convert flow accumulation area [$\mathrm{km^2}$] into flow depth [$\mathrm{m}$] and width [$\mathrm{m}$].
| Variable | Units | Description |
|----------|------|-------------|
| $\alpha_1$ | — | Empirical coefficient controlling channel geometry scaling |
| $\alpha_2$ | — | Secondary coefficient for hydraulic geometry relationships |
| $\beta_1$ | — | Exponent controlling width or hydraulic scaling behavior |
| $\beta_2$ | — | Secondary exponent for hydraulic scaling relationships |
| $n$ | $\mathrm{s\,m^{-1/3}}$ | Manning’s roughness coefficient for channel and surface flow |

---

## Water Quality Inputs

| Variable | Units | Description |
|----------|------|-------------|
| $\mathrm{ADD}$ | $\mathrm{days}$ | Antecedent dry days used in pollutant buildup modeling |
| $\mathrm{min\_Bt}$ | $\mathrm{g\,m^{-2}}$ | Minimum pollutant buildup threshold |
| $\mathrm{Bmin}$ | $\mathrm{g\,m^{-2}}$ | Minimum allowable pollutant mass |
| $\mathrm{Bmax}$ | $\mathrm{g\,m^{-2}}$ | Maximum pollutant buildup capacity |

---

## DEM Processing and Terrain Controls

| Variable | Units | Description |
|----------|------|-------------|
| $\mathrm{min\_area}$ | $\mathrm{km^2}$ | Minimum drainage area threshold for channel initiation |
| $\tau$ | — | Smoothing parameter controlling DEM filtering intensity |
| $\mathrm{K\_value}$ | — | Parameter controlling terrain processing or hydraulic scaling |
| $\mathrm{sl}$ | $\mathrm{m\,m^{-1}}$ | Minimum slope threshold used in DEM conditioning |
| $\mathrm{resolution\_resample}$ | $\mathrm{m}$ | Target resolution for DEM resampling |
| $\mathrm{slope\_DTM}$ | $\%$ | Slope threshold used for terrain correction or filtering |

---

## File Paths and Input Data

| Variable | Units | Description |
|----------|------|-------------|
| $\mathrm{DEM\_path}$ | — | Path to Digital Elevation Model |
| $\mathrm{LULC\_path}$ | — | Path to Land Use / Land Cover raster |
| $\mathrm{SOIL\_path}$ | — | Path to soil classification raster |
| $\mathrm{Warmup\_Depth\_path}$ | — | Path to initial warm-up water depth condition |
| $\mathrm{Initial\_Buildup\_path}$ | — | Path to initial pollutant buildup map |
| $\mathrm{Initial\_Soil\_Moisture\_path}$ | — | Path to initial soil moisture condition |
| $\mathrm{Initial\_SWE\_path}$ | — | Optional path to initial snow water equivalent in millimeters |
| $\mathrm{Initial\_Snow\_Depth\_path}$ | — | Optional path to initial physical snow depth in millimeters |
| $\mathrm{Albedo\_path}$ | — | Path to albedo raster |
| $\mathrm{LAI\_path}$ | — | Path to leaf area index raster |
| $\mathrm{RiverWidths\_path}$ | — | Path to river width raster |
| $\mathrm{RiverDepths\_path}$ | — | Path to river depth raster |
| $\mathrm{DTB\_path}$ | — | Path to depth-to-bedrock raster. In the layered subsurface, the bottom of the whole column |
| $\mathrm{SoilBaseDepth\_path}$ | — | Optional soil-base depth raster (m), layered subsurface (T21) |
| $\mathrm{RegolithThetaS\_path}$ | — | Optional regolith $\theta_s$ raster (T22) |
| $\mathrm{RegolithThetaR\_path}$ | — | Optional regolith $\theta_r$ raster (T23) |
| $\mathrm{RegolithAlphaVG\_path}$ | — | Optional regolith van Genuchten $\alpha$ raster (T24) |
| $\mathrm{RegolithNVG\_path}$ | — | Optional regolith van Genuchten $n$ raster (T25) |
| $\mathrm{RegolithKsatV\_path}$ | — | Optional regolith vertical $K_{sat}$ raster, mm/h (T26) |
| $\mathrm{RegolithKsatH\_path}$ | — | Optional regolith horizontal $K_{sat}$ raster, mm/h (T27) |
| $\mathrm{RegolithSpecificYield\_path}$ | — | Optional regolith specific-yield raster (T28) |
| $\mathrm{DeepAquiferSubbasins\_path}$ | — | Subbasin raster of the deep aquifer: which cells feed which reservoir (T19) |
| $\mathrm{DeepAquiferChannelWeight\_path}$ | — | Channel-weight raster: where each deep reservoir discharges (T20) |
| $\mathrm{DeepAquiferInitialState\_path}$ | — | Optional deep-aquifer initial-state JSON written by the Case Builder calibration (T29) |
| $\mathrm{B1\_path}$ | — | Path to pollutant-related parameter raster |
| $\mathrm{B2\_path}$ | — | Path to pollutant-related parameter raster |
| $\mathrm{W1\_path}$ | — | Path to pollutant wash-off parameter raster |
| $\mathrm{W2\_path}$ | — | Path to pollutant wash-off parameter raster |
| $\mathrm{hydropol2d\_tools}$ | — | Path to HydroPol2D function library |

---

## Human Instability Parameters

| Variable | Units | Description |
|----------|------|-------------|
| $\mu$ | — | Friction coefficient between human body and ground |
| $C_d$ | — | Drag coefficient for human body in flow |
| $\rho_{\mathrm{person}}$ | $\mathrm{kg\,m^{-3}}$ | Density of human body |
| $\mathrm{weight\_person}$ | $\mathrm{kg}$ | Average human weight |
| $\mathrm{height\_person}$ | $\mathrm{m}$ | Average human height |
| $\mathrm{width1\_person}$ | $\mathrm{m}$ | Characteristic frontal width |
| $\mathrm{width2\_person}$ | $\mathrm{m}$ | Secondary width parameter |
| $\rho_{\mathrm{water}}$ | $\mathrm{kg\,m^{-3}}$ | Density of water |
| $g$ | $\mathrm{m\,s^{-2}}$ | Gravitational acceleration |

---

## Observation Points

| Variable | Units | Description |
|----------|------|-------------|
| $\mathrm{Gauge}$ | — | Gauge identifier |
| $\mathrm{Easting}$ | $\mathrm{m}$ | Easting coordinate |
| $\mathrm{Northing}$ | $\mathrm{m}$ | Northing coordinate |
| $\mathrm{Label\ Name}$ | — | Output label for time series |

---

## Design Storm Parameters

| Variable | Units | Description |
|----------|------|-------------|
| $\mathrm{RP}$ | $\mathrm{years}$ | Return period of design storm |
| $\mathrm{Rainfall\ Duration}$ | $\mathrm{min}$ | Total storm duration |
| $K$ | — | Intensity–duration–frequency coefficient |
| $a$ | — | IDF curve parameter |
| $b$ | — | IDF curve parameter |
| $c$ | — | IDF curve parameter |
| $\mathrm{dt\_design}$ | $\mathrm{min}$ | Time resolution of synthetic storm |

---

## Satellite or Radar Rainfall

| Variable | Units | Description |
|----------|------|-------------|
| $\mathrm{Time}$ | $\mathrm{min}$ | Time step of rainfall raster |
| $\mathrm{Raster\ Directory}$ | — | Path to rainfall raster files |

---

## Satellite Transpiration

| Variable | Units | Description |
|----------|------|-------------|
| $\mathrm{Time}$ | $\mathrm{day}$ | Time index for transpiration data |
| $\mathrm{Raster\ Directory}$ | — | Path to transpiration rasters |

---

## Satellite Evaporation

| Variable | Units | Description |
|----------|------|-------------|
| $\mathrm{Time}$ | $\mathrm{day}$ | Time index for evaporation data |
| $\mathrm{Raster\ Directory}$ | — | Path to evaporation rasters |

---

## Workbook Conventions for the Groundwater Blocks

- Every input cell of the distributed `General_Data` workbooks carries a comment that explains it.
- The new blocks use white input cells with side borders.
- In bypass mode the same keys are fields of `InputData_Bypass.flags` (layered and Feddes settings) and `InputData_Bypass.general` (deep-aquifer starting state).
- Environment variables override the workbook: `HYDROPOL_SUBSURFACE_SCHEME`, `HYDROPOL_ENABLE_FEDDES`, `HYDROPOL_<NAME>` for any key above, `HYDROPOL_DEEP_INITIAL_BASEFLOW_MM_DAY`, `HYDROPOL_DEEP_MEAN_RECHARGE_MM_YEAR` and `HYDROPOL_DEEP_INITIAL_STATE_PATH`. The Case Builder uses them.
- Every column of `SOIL_parameters.xlsx` also carries a note, including how the layered subsurface treats `Sy` (ignored), `kgsat` (regolith $K_h$ fallback) and `DTB (m)` (not read).

## Open Decisions

These questions are pending. The current behavior is stated for each.

| Question | Current behavior |
|---|---|
| Should `DTB_path` be required in Excel mode when the layered subsurface is on? | Not required. Without it the column bottom falls back to `subsurface_depth_to_bedrock_m`, then to the default soil depth, with a warning. |
| What happens to the `DTB (m)` column of `SOIL_parameters.xlsx`? | It is not read. The soil depth comes from `DTB_path`, or 1 m when it is empty. |
| Can soil-property rasters be given in Excel mode? | The workbook has no cells for the soil-property rasters (`ThetaS_path`, `KsatNearSurface_path`, …), which the code reads from `InputPaths`. Only the soil-base and regolith rasters (T21:T28) have Excel cells. |

---

## Notes

The descriptions provided here represent the functional role of each parameter within HydroPol2D.

Final definitions should be refined based on:

- spreadsheet comments  
- calibration strategy  
- application context  

This table serves as the central reference for model configuration.
