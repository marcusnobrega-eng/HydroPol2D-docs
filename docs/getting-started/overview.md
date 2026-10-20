---
title: Overview
---

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

## How HydroPol2D advances a run

At a high level, HydroPol2D advances the coupled system in this order:

1. apply rainfall, inflow, and meteorological forcing;
2. update interception, snow, evapotranspiration, infiltration, and vadose storage;
3. accumulate recharge and capillary exchange for groundwater;
4. route surface water with the selected routing family;
5. update groundwater heads when the groundwater scheduler is due;
6. return exfiltration, saturation excess, water quality, and optional hazard diagnostics to the evolving state.

This sequencing is what links the hydrologic, groundwater, routing, and diagnostic modules into one model.

## How to read the documentation

For most users, the clearest reading order is:

1. [Run from Excel](./excel-workflow) for tested regular and Voronoi spreadsheet workflows.
2. [Configuration Overview](../configuration/overview) for the public controls and flags.
3. [Ecosystem Architecture](./ecosystem-architecture) for mesh generation, shared contracts, and repository responsibilities.
4. [Mathematical Overview](../theory/overview) for the governing equations and conceptual structure.
5. [Validation Overview](../validation/overview) for the evidence supporting each module.
6. [Examples](../Examples/RainfallRunoff) for reproducible case-study workflows.
