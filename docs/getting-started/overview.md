---
title: Overview
---
import useBaseUrl from '@docusaurus/useBaseUrl';

# HydroPol2D

HydroPol2D is a raster-based hydrologic-hydrodynamic model for coupled surface water, vadose-zone storage, groundwater, water quality, snow, and hazard diagnostics.

This documentation describes the model as it is currently implemented. It also distinguishes between validated pathways, diagnostic pathways, and features that remain paused or experimental.

## Current scope

The current codebase includes:

- canopy interception, evapotranspiration, snow, infiltration, and layered vadose storage;
- groundwater recharge, capillary rise, asynchronous saturated-groundwater updates, and 2D Boussinesq flow when baseflow is active;
- surface routing with local inertial, full momentum, diffusive D4, kinematic D4, and cellular automata options;
- water-quality transport and outlet export;
- optional human-instability diagnostics.

<p align="center">
  <img src={useBaseUrl('/img/getting-started/questions-modules-outputs.svg')} width="720" alt="Six rows, each with a question, the HydroPol2D module that answers it with its default or optional status and its validation evidence, and the map or time-series output that shows it, above a key and a note on what Results shows" />
</p>

<p align="center">
  <em>Figure 1. Questions HydroPol2D can answer, the module that answers each one with its status, and the output that shows it. The status follows the validation pages.</em>
</p>

## How HydroPol2D advances a run

At a high level, HydroPol2D advances the coupled system in this order:

1. apply rainfall, inflow, and meteorological forcing;
2. update interception, snow, evapotranspiration, infiltration, and vadose storage;
3. accumulate recharge and capillary exchange for groundwater;
4. route surface water with the selected routing family;
5. update groundwater heads when the groundwater scheduler is due;
6. return exfiltration, saturation excess, water quality, and optional hazard diagnostics to the evolving state.

This sequencing is what links the hydrologic, groundwater, routing, and diagnostic modules into one model.

<p align="center">
  <img src={useBaseUrl('/img/getting-started/time-step-order.svg')} width="720" alt="Six steps of one surface time step in a loop: forcing; snow, canopy and soil; recharge and capillary rise; water table; surface routing; water quality and hazard. Beside them, the surface clock with its Courant time step and the groundwater clock with its three triggers, and below, a strip of surface steps and lateral groundwater updates over a run" />
</p>

<p align="center">
  <em>Figure 2. The order of one surface time step, the surface clock that sets its length, and the groundwater clock that decides when lateral groundwater flow runs. The strip at the bottom shows the two clocks over a run, not to scale.</em>
</p>

## Desktop interface

[HydroPol2D Studio](../studio/overview) is the desktop interface for HydroPol2D-Python: it builds a
model from a map or your own files, sets it up step by step, runs it and shows the results.

<p align="center">
  <img src={useBaseUrl('/img/getting-started/data-to-results.svg')} width="720" alt="Maps, parameter tables, forcing and settings feed one case, either a HydroPol2D Studio model file or a HydroPol2D-MATLAB workbook; the case runs in Studio or in MATLAB, and the outputs are maps, time series, animations and a results package" />
</p>

<p align="center">
  <em>Figure 3. From data to results. The same inputs make one case, a Studio model file or a MATLAB workbook, and each run writes maps, time series and animations.</em>
</p>

## How to read the documentation

For most users, the clearest reading order is:

1. [Run from Excel](./excel-workflow) for tested regular and Voronoi spreadsheet workflows.
2. [Configuration Overview](../configuration/overview) for the public controls and flags.
3. [Ecosystem Architecture](./ecosystem-architecture) for mesh generation, shared contracts, and repository responsibilities.
4. [Mathematical Overview](../theory/overview) for the governing equations and conceptual structure.
5. [Validation Overview](../validation/overview) for the evidence supporting each module.
6. [Examples](../Examples/RainfallRunoff) for reproducible case-study workflows.
