---
title: Validation Overview
---
import useBaseUrl from '@docusaurus/useBaseUrl';

# Validation Overview

HydroPol2D validation is organized around controlled Phase 1 benchmarks. The purpose of this phase is to verify that each computational module reproduces the intended equations, storage updates, boundary conditions, and numerical behavior under cases where the expected answer is known.

The full technical report is available here:

<div style={{margin: '1rem 0 1.5rem 0'}}>
  <a className="button button--primary button--lg" href={useBaseUrl('/reports/validation_report.pdf')}>
    Download the Phase 1 Validation Report
  </a>
</div>

## Validation philosophy

A validation claim is made only when the case has an analytical solution, an independent reference calculation, an exact bookkeeping target, a benchmark hydrograph, or a documented numerical reference. Cases based only on qualitative behavior are treated as diagnostics.

Phase 1 does not claim field calibration or watershed-scale observational validation. Field cases and inverse-modeling exercises are separate evidence levels and should be reported separately.

## Evidence levels

| Evidence level | Meaning |
|---|---|
| Analytical solution | Closed-form or exact mathematical solution is available. |
| Independent reference | A separate implementation computes the expected result. |
| Exact bookkeeping | The validation target is conservation, prescribed forcing, or imposed boundary volume. |
| Benchmark hydrograph | A published or digitized benchmark hydrograph is used as the comparison target. |
| Numerical reference | A refined or simpler trusted numerical run is used as the reference. |
| Diagnostic | The case is useful for debugging, but it is not a validation claim. |

## Shared case context

Most Phase 1 hydrologic and groundwater cases use the same synthetic V-tilted catchment context. That shared setup provides a consistent DEM, soil, land-cover, LAI, groundwater, and boundary-condition framework while still allowing each module to be tested against an analytical or independent truth source. Specialized hydrodynamic benchmarks such as Ritter dam-break and the non-breaking wave retain their own geometries because their comparisons require dedicated domains.

## Detailed case pages

The website now expands the Phase 1 package into module-level case pages:

- [Hydrologic Modules](./hydrologic-modules)
- [Groundwater and Recharge](./groundwater-recharge)
- [Hydrodynamics and Routing](./hydrodynamics-routing)
- [Reservoirs, Boundaries, Water Quality, and Risk](./ancillary-modules)

Each page states what was tested, what the truth source was, which figures support the result, and what the case does not validate.

## Current scope

The Phase 1 package covers canopy interception, snow, infiltration, evapotranspiration, groundwater and recharge, hydrodynamic routing, reservoir and boundary-condition behavior, spatial rainfall ingestion, water quality, and human-instability diagnostics. See the [Human Instability](../theory/human-instability) theory page for the implemented mode definitions.
