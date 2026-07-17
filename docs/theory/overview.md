---
title: Mathematical Overview
---

# Mathematical Overview

The theory section is the main reference for HydroPol2D equations and module structure. Its purpose is to describe the implemented process formulations without mixing them with configuration details or case-study narrative.

HydroPol2D couples:

- interception, evapotranspiration, infiltration, snow, and vadose storage;
- layered groundwater recharge, capillary rise, and lateral Boussinesq flow;
- multiple surface-routing families;
- water-quality transport;
- optional human-instability diagnostics.

## Capability and maturity

| Capability | Canonical theory path | Current status |
|---|---|---|
| Hydrologic core: interception, ET, infiltration, snow, layered vadose storage | [Hydrologic Model](./hydrologic-model) | Default + validated |
| Groundwater recharge, async scheduler, capillary rise, Boussinesq lateral flow | [Groundwater Model](./groundwater-model) | Default + validated |
| Local inertial routing | [Hydrodynamic Model](./hydrodynamic-model) | Default + validated |
| Full-momentum routing | [Hydrodynamic Model](./hydrodynamic-model) | Optional + validated in controlled benchmarks |
| Diffusive and kinematic D4 routing | [Hydrodynamic Model](./hydrodynamic-model) | Optional + validated in controlled benchmarks |
| Cellular automata routing | [Hydrodynamic Model](./hydrodynamic-model) | Optional + validated for conservation and routing bookkeeping |
| Human instability modes `1` and `3` | [Human Instability](./human-instability) | Optional + validated in controlled benchmarks |
| River-aquifer exchange interface | [Groundwater Model](./groundwater-model) | Interface present, not yet a mature standalone theory claim |

## Theory map

### 1. Hydrologic processes

The hydrologic theory pages document how HydroPol2D partitions atmospheric input into canopy storage, throughfall, infiltration, evapotranspiration, snow accumulation and melt, vadose storage, recharge, and groundwater feedback.

### 2. Groundwater coupling

Groundwater theory documents the current layered recharge pathway, optional capillary rise, asynchronous groundwater scheduler, exfiltration, and 2D Boussinesq lateral flow when baseflow is active.

### 3. Surface routing

HydroPol2D currently documents five main routing families:

- local inertial;
- full momentum;
- diffusive D4;
- kinematic D4;
- cellular automata.

Only one major routing formulation should be active at a time. D8 remains secondary in scope.

### 4. Human instability

Human instability is a coupled hazard diagnostic driven by HydroPol2D depth and velocity outputs. The current implemented public theory includes mode `1` force-balance risk and mode `3` geometry-based classification.

### 5. Water quality

Water-quality theory documents constituent buildup, washoff, transport, and export within the same distributed routing framework used for water movement.

## Numerical coupling

At a high level, HydroPol2D advances the coupled system by:

1. applying rainfall, inflow, and meteorological forcing;
2. updating interception, snow, evapotranspiration, infiltration, and vadose storage;
3. accumulating recharge and capillary exchange for groundwater;
4. updating the active routing family;
5. updating groundwater heads when the asynchronous scheduler is due;
6. feeding exfiltration, saturation excess, and optional diagnostics back into the coupled state.

This sequential structure is what connects the individual theory pages into one model.
