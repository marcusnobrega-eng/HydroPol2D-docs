---
title: Mathematical Overview
---
import useBaseUrl from '@docusaurus/useBaseUrl';

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
| Hydrologic core: interception, ET, infiltration, layered vadose storage | [Hydrologic Model](./hydrologic-model) | Default + validated |
| Snow accumulation, melt and sublimation | [Hydrologic Model](./hydrologic-model#5-snow-accumulation-melt-and-sublimation) | Optional (off unless turned on) + validated |
| Groundwater recharge, async scheduler, capillary rise, Boussinesq lateral flow | [Groundwater Model](./groundwater-model) | Default + validated |
| Layered soil-over-regolith subsurface | [Layered Subsurface](./layered-subsurface) | Optional + kernel parity and controlled V-tilted tests |
| Feddes root-water-uptake stress | [Hydrologic Model](./hydrologic-model#35-feddes-root-water-uptake-stress) | Optional + consistency tests |
| Deep aquifer: linear reservoirs per subbasin and their starting state | [Groundwater Model](./groundwater-model#13-deep-aquifer) | Optional + starting-state fixture tests |
| Local inertial routing | [Hydrodynamic Model](./hydrodynamic-model) | Default + validated |
| Full-momentum routing | [Hydrodynamic Model](./hydrodynamic-model) | Optional + validated in controlled benchmarks |
| Diffusive and kinematic D4 routing | [Hydrodynamic Model](./hydrodynamic-model) | Optional + validated in controlled benchmarks |
| Cellular automata routing | [Hydrodynamic Model](./hydrodynamic-model) | Optional + validated for conservation and routing bookkeeping |
| Human instability modes `1` and `3` | [Human Instability](./human-instability) | Optional + validated in controlled benchmarks |
| River-aquifer exchange | [Groundwater Model](./groundwater-model#10-riveraquifer-exchange) | Implemented in Python and MATLAB + controlled groundwater tests |

## Theory map

### 1. Hydrologic processes

The hydrologic theory pages document how HydroPol2D partitions atmospheric input into canopy storage, throughfall, infiltration, evapotranspiration, snow accumulation and melt, vadose storage, recharge, and groundwater feedback.

<p align="center">
  <img src={useBaseUrl('/img/theory/cell-water-budget.svg')} width="720" alt="One model cell seen from the side: rain falls on a tree canopy and snow on a snowpack; throughfall, snowmelt, exfiltration and saturation excess feed the surface water, which infiltrates into the vadose zone and flows to a lower neighbour cell; recharge and capillary rise link the vadose zone to the groundwater, which flows laterally; grey arrows return vapour to the atmosphere" />
</p>

<p align="center">
  <em>Figure 1. The stores and fluxes of one model cell (not to scale). Blue arrows carry liquid water and grey arrows vapour; only the rain passes through the canopy, and the snowmelt goes straight to the surface water.</em>
</p>

### 2. Groundwater coupling

Groundwater theory documents the current layered recharge pathway, optional capillary rise, asynchronous groundwater scheduler, exfiltration, and 2D Boussinesq lateral flow when baseflow is active. The optional [layered subsurface](./layered-subsurface) replaces the soil-bound aquifer with a soil-over-regolith column, and the optional deep aquifer adds slow linear reservoirs per subbasin.

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

1. applying rainfall and meteorological forcing;
2. updating interception, snow, evapotranspiration, infiltration, and vadose storage;
3. accumulating recharge and capillary exchange for groundwater;
4. changing the water-table heads in every surface-water step by the net exchange and returning exfiltration and saturation excess to the surface; the groundwater scheduler is always asynchronous, and only the lateral groundwater flow, when it is on, waits for it;
5. applying inflow hydrographs and updating the active routing family;
6. updating water quality and optional diagnostics.

This sequential structure is what connects the individual theory pages into one model.
