---
title: Changelog
---

# Changelog

Model changes that affect inputs, results or validation, newest first. Dates are in California time (PDT). The codes in brackets are commits in HydroPol2D-Python (Py), the MATLAB model (ML) and the Case Builder (CB).

## 2026-10-28 to 2026-11-02 {#2026-10-28-to-2026-11-02}

- **Urban drainage, detention ponds, green infrastructure and D8 routing in MATLAB (ML).** The four modules of HydroPol2D-Python now run in MATLAB on the regular grid, with Python's equations. Each has a check against the Python kernel: VAL-UD-001, VAL-POND-001, VAL-GI-001 and the D8 local-inertial check. They are set up in the bypass script, since the case workbook has no inputs for them, and a mesh run refuses drainage, ponds and green infrastructure. The old raster D8 (`flag_D8`) is retired. See [Limitations](./limitations#matlab-optional-modules). [ML `d197b3a`, `cb5c240`, `fcf1272`, `9ec0a60`, `93c23e5`, `2472593`, `57f457c`, `f8ecc9b`]
- **Optional modules on MATLAB meshes (ML).** Reservoirs, water quality, human risk (mode 1) and snow run on Voronoi and quadtree meshes. A mesh run that asks for a module it would skip stops at the input check. [ML `7140eab`, `199e073`, `f7e2e45`]
- **Forcing times start an interval (ML).** MATLAB now reads the times of rain, inflow and ET maps as interval starts, as HydroPol2D-Python does. A table written with interval ends must move each time one step earlier. See [Optional Forcing](../inputs/optional-forcing#rainfall). [ML `caaec0f`]
- **Reservoir releases (ML).** Releases conserve mass, and a (0, 0) destination sends the water out of the model. See [Parameter Tables](../inputs/parameter-tables). [ML `e9818fe`]
- **Human risk mode 3 (Py, ML).** The lift lever arm uses the tangent of the slope angle, the classification uses the local slope of the DEM, and a dry cell (h = 0) is stable. A mesh case with mode 3 stops at the input check. See [Human Instability](../theory/human-instability). [Py `f3037b6`, `f159167`, `6a27027`, `056cc00`; ML `7a6fa79`]
- **Snow and canopy (Py, ML).** Rain and snow are split before the canopy, only rain is intercepted, and melt reaches the surface without passing through the canopy. [Py `c6029a8`, `eda893e`; ML `65176b7`]
- **Groundwater and ET in MATLAB (ML).** A gaining river takes only groundwater stored before this step's recharge. Reference ET uses the ground heat flux of the climate stations. Groundwater time stays in double precision when the heads are single. Both soil schemes use one lateral groundwater update rule. [ML `1a8a1af`, `4f261a9`, `f9ac40c`, `5329336`]
- **Groundwater (Py).** The head-change limit triggers the lateral update again. [Py `e8835e0`]
- **Excel import (Py).** The water-quality block is read, with `min_Bt` converted from g/m² to kg/m². [Py `5df2f4c`]
- **Reported numbers (ML).** The legacy water balance runs every accepted step again. The run summary gives the applied rain and the maximum depth of the whole run. Before, it took the maximum depth from the last chunk of saved maps only, so maximum depths reported before 2026-11-02 can be too low. [ML `4491092`, `bb64049`]
- **Calibration (Py).** A genetic algorithm (now the default) and SCE-UA fit discharge, water depths, water levels and groundwater together, with observation uncertainty and before-and-after fits. Studio has a Calibrate workspace. See [GA Calibration](../calibration/ga-calibration). [Py `30989cc`, `e67ee45`, `713c381`, `ac48b04`, `01a8972`]
- **Stanford example (ML).** The 30 m DEM is now USGS 3DEP. The launcher resolves relative paths and stops when a named rain file is missing. See [San Francisquito, controlled rainfall](../Examples/RainfallRunoff). [ML `8383fc5`, `a378475`]

## 2026-10-27 {#2026-10-27}

- **Optional modules on the mesh (Py).** Snow, water quality, human instability, reservoirs, urban drainage, green infrastructure and detention ponds now run on Voronoi and quadtree meshes, on the CPU engine. Before, a mesh case with any of them stopped at the input check. Each module uses the regular grid's own equations; on a mesh made of the grid's squares the results match the grid's to round-off. When a mesh cannot run a module (the GPU engine, or some modules with mesh river channels), the message names the module and Studio offers to switch the model to the regular grid. See [Limitations](./limitations#voronoi-mesh-mode). [Py `7b6c556` … `d6f8a86`]

## 2026-10-20 {#2026-10-20}

- **One case workbook (ML).** A MATLAB case is now one workbook, `HydroPol2D_Inputs.xlsx`, with 8 settings tabs, 5 class-table tabs and 5 series tabs and a note on every value. The switches sit at the top of their blocks; there is no `Flags` sheet. Older cases (`General_Data.xlsx`, its `Flags` sheet and separate workbooks) still run, and a builder converts them. Check: the V-tilted case gives identical results from either layout, with every old workbook deleted, and doubling the Rain series tab doubles the rain (3 of 3 checks). See [Run from Excel](../getting-started/excel-workflow). [ML `a0a6b7a`, `993d830`]
- **Fix: lists of ET maps (ML, both layouts).** In `General_Data.xlsx` the rainfall, transpiration and evaporation map lists share one header row. Before this fix, the transpiration list read the rainfall list's times (in minutes, with no day-to-minute conversion), and the evaporation list read the transpiration paths. Runs with `flag_input_ETP_map = 1` made before 2026-10-20 used wrong ET inputs; rerun them. Each list now stops at its first empty row, and its columns are searched only under its own title. [ML `993d830`]
- **Gauge discharge cross-sections (ML).** Each gauge records depth and water level at its cell, and discharge across a line of cells across the flow (5 cells by default; downstream direction automatic or N/S/E/W). New outputs: a hydrograph line, a column in `Rating_Curve_Gauges.csv` and `Gauge_Cross_Sections.csv`. The gauge table now ends at its first empty row. Checks: 3 of 3. See [Gauge table](../configuration/general_data#gauge-table-and-discharge-cross-sections). [ML `fa36e1f`]
- **Implicit water-table flux in MATLAB (ML).** Switch `flag_implicit_water_table_flux`, default 1. MATLAB takes the derivatives by fourth-order central differences and agrees with Python to about $10^{-9}$. A saturated gap now drains at $K_{sat}$ by a stated rule in both models (results unchanged). [ML `2559060`; Py `04ca62a`]
- **`DTB_path` optional in layered mode (ML).** The column bottom falls back to `subsurface_depth_to_bedrock_m`, then to the `DTB (m)` of each soil class. Before, a missing `DTB_path` silently meant 1 m. The default groundwater scheme still requires `DTB_path`. [ML `2559060`]
- **Soil-property maps in Excel mode (ML).** Nine optional maps (`ThetaS_path` … `SpecificYield_path`) override the soil-class values cell by cell. [ML `2559060`]
- **Validation fix (ML).** The groundwater check harness wrote its `Flags` grid one cell off, so the Feddes V-tilted run had Feddes off. It now runs with Feddes on, and three runs were added (no `DTB_path`, explicit flux, soil maps). Groundwater release checks: 17 of 17. [ML `2559060`]

## 2026-10-19 {#2026-10-19}

- **Capillary refill rule (Py, ML).** Capillary rise refills a soil layer only up to field capacity (HBV-style). This removed a circulation of water between the soil and a shallow water table; in the twin valley the gross capillary rise fell from 0.016 to 0 m³/s with the stream flow unchanged. The implicit water-table flux now takes its head derivative along the actual table move. See [Layered Subsurface, Section 4.4](../theory/layered-subsurface#44-darcy-flux-at-the-water-table). [Py `fe81252`; ML `051b52b`]
- **Layered recession calibration (Py, CB).** Two lateral-conductivity multipliers, soil and regolith, fitted against a master recession curve, with identifiability outputs and a spin-up that runs the model's own column fluxes. See [Groundwater Recession Calibration](../calibration/groundwater-recession). [Py `b1f686e`, `1ffddd8`, `3390dc6`, `e837f7d`; ML `f78a130`; CB `d45e5be`]
- **Implicit water-table flux (Py)** and a **compiled layered step** (about 6 times faster, identical results). [Py `c384ea4`, `0a4b393`]
- **Deep-aquifer starting state (Py, ML, CB).** $S_0 = q_0 A \tau$ from a starting baseflow or a mean recharge. See [Groundwater Model, Section 13.3](../theory/groundwater-model#133-starting-state). [Py `57ea20a`, `83d7071`; ML `13fa3d8`; CB `52bdbad`]

## 2026-10-15 to 2026-10-17 {#2026-10-15-to-2026-10-17}

- **Layered subsurface and Feddes stress (Py, ML).** The soil-over-regolith column on the structured grid and the Voronoi mesh, Feddes root-water stress in both soil schemes, and the MATLAB port with Python-to-MATLAB parity. See [Layered Subsurface](../theory/layered-subsurface). [Py `b6ced47` … `c268969`; ML `0ded343`, `282cac9`, `383ea82`]
- **Layered inputs (CB, ML).** Global rules for the soil base and regolith maps, layered MATLAB cases, and the Excel inputs for the new blocks. [CB `06f5e75`, `1ec94f4`; ML `2074ae6`]
