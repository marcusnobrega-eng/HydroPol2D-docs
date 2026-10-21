---
title: Validation Status
---
import useBaseUrl from '@docusaurus/useBaseUrl';

# Validation Status

The <a href={useBaseUrl('/reports/validation_report.pdf')}>validation report</a> documents the methods, metrics, and results for the HydroPol2D validation suite. The table below provides a concise index of the current evidence.

<div style={{margin: '1rem 0 1.5rem 0'}}>
  <a className="button button--primary button--lg" href={useBaseUrl('/reports/validation_report.pdf')}>
    Open the Validation Report
  </a>
</div>

| Module | Status | Evidence |
|---|---|---|
| Canopy interception | Validated | Independent bucket-storage reference and exact mass balance. |
| Snow | Validated | LULC-specific parameters, optional initial-state rasters, timestep refinement, spreadsheet-bypass equivalence, and V-tilted event closure. |
| Infiltration | Validated | Analytical and layered-soil cases on V-tilted and column-style domains. |
| Evapotranspiration | Validated | Independent reference ET calculations and extraction-limit checks. |
| Groundwater and recharge | Validated | Recharge-rise, scheduler, capillary-rise, and analytical hillslope benchmarks. |
| Layered subsurface (optional) | Controlled tests and Python-MATLAB parity | Column kernel and step parity (implicit flux in both models), full-model V-tilted runs, Voronoi mesh mass closure, implicit-flux and capillary-refill tests. No field case. |
| Feddes root-water stress (optional) | Controlled consistency tests | Default and layered Feddes ET agree for the same state; Feddes never exceeds unstressed uptake. |
| Deep aquifer starting state (optional) | Fixture parity | $S_0 = q_0 A \tau$ checked in Python and MATLAB against a shared fixture. |
| Layered recession calibration | Twin experiment only | Known multipliers recovered at 0, 5 and 10 % noise on a synthetic valley, as the only acceptable pair. No field test. |
| Gauge discharge cross-sections (MATLAB) | Controlled checks | Cross-section discharge on the V-tilted case, both routing face conventions; 3 of 3 checks. |
| Single case workbook (MATLAB) | Equivalence check | The V-tilted case gives identical results from `HydroPol2D_Inputs.xlsx` and from the older `General_Data.xlsx` layout; 3 of 3 checks. |
| Full-momentum hydrodynamics | Validated | Tilted-plane, V-tilted, Ritter dam-break, non-breaking wave, and boundary-condition benchmarks. |
| Local-inertial hydrodynamics | Validated | Tilted-plane, V-tilted, stage-boundary, and conservation tests. |
| Cellular automata routing | Validated | V-tilted, plane, and boundary-condition checks. |
| Kinematic and diffusive routing | Validated | Plane, V-tilted, and stage-boundary benchmarks appropriate to the reduced equations. |
| Neal (2012) subgrid model | Validated for tested channel geometries | Fine-grid references for in-bank routing, compound-channel flow, bank activation, and inundation extent. |
| Voronoi finite-volume mesh | Controlled CPU validation | Local inertial with Neal graph; resolved-2D kinematic, diffusive, and full momentum. GPU and India-scale execution remain unvalidated. |
| Reservoir and control structures | Validated | Rating-curve storage-depletion solution and volume ledger. |
| Inflow hydrograph boundary | Validated | Prescribed-hydrograph volume and routed storage or outlet ledger. |
| Stage hydrograph boundary | Validated | Prescribed-stage enforcement and volume response. |
| Spatial rainfall rasters | Validated | Exact cellwise rainfall and domain-volume targets. |
| Water quality | Validated | SWMM-style buildup scale and analytical mass-based wash-off solutions. |
| Human risk and instability | Validated | Independent threshold and force-balance classification references. |

Latest full test-suite results:

| Suite | Result | Date |
|---|---|---|
| HydroPol2D-Python | 937 passed, 0 failed, 2 opt-in tests skipped | 2026-10-19 |
| Case Builder | 181 passed | 2026-10-19 |
| MATLAB groundwater release checks | 17 of 17 | 2026-10-20 |
| MATLAB gauge and single-workbook checks | 3 of 3 each | 2026-10-20 |
| MATLAB validation release | 22 of 23 directly; the canopy-interception check is scored by its Python comparison script and passes when that script runs | 2026-10-20 |

Changes to the model that affect results are listed in the [Changelog](./changelog).

The routing cases are interpreted against the governing equations they solve. The Ritter dry-bed dam-break is an acceptance benchmark for full momentum; reduced routing methods are assessed with gradual-flow, conservation, symmetry, and boundary-condition cases.
