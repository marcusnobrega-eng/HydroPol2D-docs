---
title: Phase 1 Status
---
import useBaseUrl from '@docusaurus/useBaseUrl';

# Phase 1 Validation Status

The table below summarizes the current validation state of HydroPol2D modules. Detailed metrics, figures, and case descriptions are provided in the <a href={useBaseUrl('/reports/validation_report.pdf')}>Phase 1 validation report</a>, the [Validation Overview](./overview), and the detailed module pages:

- [Hydrologic Modules](./hydrologic-modules)
- [Groundwater and Recharge](./groundwater-recharge)
- [Hydrodynamics and Routing](./hydrodynamics-routing)
- [Neal (2012) Subgrid Model](./neal-subgrid)
- [Reservoirs, Boundaries, Water Quality, and Risk](./ancillary-modules)

| Module | Current status | Evidence used |
|---|---|---|
| Canopy interception | Report-ready | Independent bucket-storage reference and exact mass balance. |
| Snow module | Report-ready | Independent rain/snow partition, melt, sublimation, and SWE bookkeeping. |
| Infiltration | Report-ready for controlled cases | Analytical and controlled layered-soil tests on V-tilted and column-style setups. |
| Evapotranspiration | Report-ready | Independent reference ET calculations and extraction-limit checks. |
| Groundwater and recharge | Report-ready | Recharge rise analytical checks, scheduler equivalence, capillary-rise bookkeeping, and hillslope analytical benchmarks. |
| Full-momentum hydrodynamics | Report-ready | Tilted-plane, V-tilted, Ritter dam-break, non-breaking wave, and boundary-condition benchmarks. |
| Local-inertial hydrodynamics | Report-ready with method-specific caveats | Tilted-plane, V-tilted, stage-boundary, and conservation tests. Ritter dam-break is diagnostic for this approximation. |
| Cellular automata routing | Report-ready for conservation and routing bookkeeping | V-tilted, plane, and boundary-condition checks. Momentum-wave benchmarks are diagnostic only. |
| Kinematic and diffusive routing | Report-ready for corrected controlled benchmarks | Analytical or approximation tilted-plane checks, V-tilted conservation, and stage-boundary bookkeeping. |
| Neal (2012) subgrid model | Report-ready for controlled channel and overbank benchmarks | Fine-grid numerical references for in-bank routing, steady and transient compound-channel flow, bank activation, and maximum inundation extent. Late recession remains limited. |
| Reservoir and control structures | Report-ready | Rating-curve storage-depletion analytical ODE and exact volume ledger. |
| Inflow hydrograph boundary | Report-ready | Prescribed hydrograph volume and routed storage or outlet ledger. |
| Stage hydrograph boundary | Report-ready | Prescribed stage enforcement and volume response bookkeeping. |
| Spatial rainfall rasters | Report-ready | Tiny raster stack with exact cellwise rainfall and domain-volume targets. |
| Water quality | Report-ready | SWMM-style buildup scale with analytical mass-based washoff solutions. |
| Human risk and instability | Report-ready | Independent threshold and force-balance classification references. |

## Important caveats

Report-ready means the module passed controlled Phase 1 equation and dynamics tests. It does not automatically mean the module is calibrated for a particular field site.

Numerical-reference cases are useful for confidence in implementation behavior, but they are weaker evidence than analytical or independently derived truth.
