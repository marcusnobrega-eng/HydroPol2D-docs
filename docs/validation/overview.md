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

<p align="center">
  <img src={useBaseUrl('/img/validation/validation-logic.svg')} width="720" alt="Flow from a module to its validation case, then a comparison against a reference of one of five evidence types, ending as acceptance evidence or a diagnostic; below, the shared V-tilted catchment, the dedicated hydrodynamic benchmarks and two cases traced through" />
</p>

<p align="center">
  <em>Figure 1. How a module is validated. A case counts as acceptance evidence only when it has a proper reference and meets its thresholds; otherwise it stays visible as a diagnostic.</em>
</p>

## Shared V-tilted catchment

Many hydrologic and groundwater cases use the synthetic V-tilted catchment. It provides a common DEM, soil, land-cover, LAI, groundwater, and boundary-condition setting while allowing individual processes to be assessed against their own reference. Dedicated hydrodynamic benchmarks, including the Ritter dam-break and non-breaking wave, use geometries designed for those solutions.

<p align="center">
  <img src={useBaseUrl('/img/validation/vtilted-catchment.svg')} width="720" alt="Oblique view of the V-tilted catchment: two planes sloping 0.05 toward a central two-cell channel, all falling 0.02 to the outlet on the north edge, with the common soil, land-cover, LAI and groundwater setting and the validation cases that use it" />
</p>

<p align="center">
  <em>Figure 2. The shared V-tilted catchment, 81 by 50 cells of 20 m, with the outlet on the north edge. Several cases run on smaller grids with the same three zones, as the grey tags show.</em>
</p>

## Validation cases

- [Hydrologic Modules](./hydrologic-modules)
- [Groundwater and Recharge](./groundwater-recharge)
- [Hydrodynamics and Routing](./hydrodynamics-routing)
- [Voronoi Mesh Validation](./voronoi-mesh)
- [Reservoirs, Boundaries, Water Quality, and Risk](./ancillary-modules)

The [Validation Status](./validation-status) page summarizes the evidence available for each module.
