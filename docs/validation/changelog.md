---
title: Changelog
---

# Changelog

Model changes that affect inputs, results or validation, newest first. Dates are in California time (PDT). The codes in brackets are commits in HydroPol2D-Python (Py), the MATLAB model (ML) and the Case Builder (CB).

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
