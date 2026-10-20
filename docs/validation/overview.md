---
title: Validation Overview
---
import useBaseUrl from '@docusaurus/useBaseUrl';

# Validation Overview

HydroPol2D is evaluated with a validation suite that tests each computational module against a known reference. The suite combines analytical solutions, independent calculations, exact water and mass balances, benchmark hydrographs, and refined numerical references. Each case defines its inputs, expected response, metrics, acceptance thresholds, and outputs.

<div style={{margin: '1rem 0 1.5rem 0'}}>
  <a className="button button--primary button--lg" href={useBaseUrl('/reports/validation_report.pdf')}>
    Download the Validation Report
  </a>
</div>

## Evidence

| Evidence type | Use in HydroPol2D validation |
|---|---|
| Analytical solution | Tests equations against a closed-form or exact solution. |
| Independent reference | Compares the model with a separate calculation of the same process. |
| Exact bookkeeping | Tests conservation under prescribed forcing or boundary conditions. |
| Benchmark hydrograph | Compares a routed response with a published or digitized benchmark. |
| Numerical reference | Compares a coarser or reduced representation with a documented, refined simulation. |

Cases that are useful for diagnosis but do not provide an appropriate reference remain visible as diagnostics and are not used as acceptance evidence.

## Shared V-tilted catchment

Many hydrologic and groundwater cases use the synthetic V-tilted catchment. It provides a common DEM, soil, land-cover, LAI, groundwater, and boundary-condition setting while allowing individual processes to be assessed against their own reference. Dedicated hydrodynamic benchmarks, including the Ritter dam-break and non-breaking wave, use geometries designed for those solutions.

## Validation cases

- [Hydrologic Modules](./hydrologic-modules)
- [Groundwater and Recharge](./groundwater-recharge)
- [Hydrodynamics and Routing](./hydrodynamics-routing)
- [Voronoi Mesh Validation](./voronoi-mesh)
- [Reservoirs, Boundaries, Water Quality, and Risk](./ancillary-modules)

The [Validation Status](./validation-status) page summarizes the evidence available for each module.
