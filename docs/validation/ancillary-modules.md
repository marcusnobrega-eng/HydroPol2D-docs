---
title: Reservoirs, Boundaries, Water Quality, and Risk
---
import useBaseUrl from '@docusaurus/useBaseUrl';

# Reservoirs, Boundaries, Water Quality, and Risk

These the cases validate model components that are important for applications but are easier to test outside a full watershed run. The logic is the same as in the rest of validation package: isolate the process, define the reference clearly, and separate what the case proves from what it does not prove.

## Reservoir rating-curve depletion

Case `VAL-RES-001` isolates the reservoir-control logic using a constant-area reservoir and a single outlet rating curve. With no external inflow, the exact reference is the depletion solution of the storage ODE.

| Case | Storage RMSE (m³) | Outflow RMSE (m³/s) | Relative L2 | Recovered k error (%) | Mass residual (%) |
|---|---:|---:|---:|---:|---:|
| `VAL-RES-001` | 0.2730 | `4.96 × 10^-5` | `7.80 × 10^-6` | 0.0000 | `4.37 × 10^-13` |

The case passed all thresholds. The small storage difference is the expected explicit-integration truncation error relative to the continuous exact ODE. The water ledger itself closes to numerical precision.

<img src={useBaseUrl('/validation/results/ancillary/VAL_RES_001_RATING_CURVE.png')} alt="Reservoir rating curve validation" />

## Inflow hydrograph boundary condition

Case `VAL-BC-INFLOW-001` imposes a known triangular hydrograph on the upstream boundary of a rectangular full-momentum domain. The truth source is the exact integral of the prescribed inflow hydrograph. The downstream hydrograph is diagnostic because no analytical Saint-Venant solution is expected for the finite rough domain.

| Case | Imposed volume error (%) | Mass residual (%) | Outlet peak (m³/s) | Peak lag (min) | Peak magnitude error (%) |
|---|---:|---:|---:|---:|---:|
| `VAL-BC-INFLOW-001` | `3.41 × 10^-13` | `6.44 × 10^-13` | 7.3771 | 5.0 | 7.7862 |

The case passed the imposed-volume and water-balance criteria. By the end of the run, the prescribed inflow volume was accounted for by outlet discharge plus remaining stored water.

<img src={useBaseUrl('/validation/results/ancillary/VAL_BC_INFLOW_001_HYDROGRAPH.png')} alt="Inflow hydrograph boundary validation" />

## Stage hydrograph boundary condition

The stage-hydrograph cases prescribe a sinusoidal upstream boundary depth in a rectangular domain. At each step, the upstream stage cells are reset to the prescribed value, the selected routing solver propagates the perturbation, and the water ledger tracks boundary-added volume, outlet volume, and remaining storage.

The prescribed-stage enforcement error was zero to numerical precision for full momentum, local inertial, cellular automata, kinematic, and diffusive routing. Downstream response amplitudes differed by method, which is expected because the routing equations are not the same, but all water-balance errors remained far below `0.1 %`.

<div style={{display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(260px, 1fr))', gap: '1rem'}}>
  <img src={useBaseUrl('/validation/results/ancillary/VAL_BC_STAGE_FM_001.png')} alt="Stage boundary full momentum validation" />
  <img src={useBaseUrl('/validation/results/ancillary/VAL_BC_STAGE_LI_001.png')} alt="Stage boundary local inertial validation" />
  <img src={useBaseUrl('/validation/results/ancillary/VAL_BC_STAGE_CA_001.png')} alt="Stage boundary cellular automata validation" />
  <img src={useBaseUrl('/validation/results/ancillary/VAL_BC_STAGE_KIN_001.png')} alt="Stage boundary kinematic validation" />
  <img src={useBaseUrl('/validation/results/ancillary/VAL_BC_STAGE_DIFF_001.png')} alt="Stage boundary diffusive validation" />
</div>

## Spatial rainfall raster ingestion

Case `VAL-RAIN-MAP-001` validates raster ingestion, temporal accumulation, unit conversion, and cellwise volume accounting before rainfall maps are coupled to routing, infiltration, or ET.

| Case | Cellwise RMSE (m) | Max cell error (m) | Total volume (m³) | Volume error (%) | Max step error (%) |
|---|---:|---:|---:|---:|---:|
| `VAL-RAIN-MAP-001` | 0 | 0 | 75.3333 | 0 | 0 |

The case passed exactly. The raster-read accumulated depths matched the prescribed cellwise reference, and each step volume matched the analytical integral.

<img src={useBaseUrl('/validation/results/ancillary/VAL_RAIN_MAP_001_TOTALS.png')} alt="Spatial rainfall raster validation" />

## Water quality

The water-quality case validates HydroPol2D's current mass-based buildup and washoff pathway before any field pollutograph calibration is attempted. The parameter scale follows SWMM-style total suspended solids buildup and washoff, but the truth source is analytical mass balance rather than a SWMM numerical run.

Three deterministic checks were used:

- dry-weather buildup initialization;
- single-cell exponential washoff;
- conservative two-cell transfer and export.

| Case | Mass RMSE (kg) | Export error (%) | Mass residual (kg) | Negative mass count |
|---|---:|---:|---:|---:|
| Dry-weather buildup | 0 | 0 | 0 | 0 |
| Single-cell washoff | `4.998 × 10^-7` | `2.483 × 10^-4` | 0 | 0 |
| Two-cell transfer | `6.272 × 10^-8` | `3.722 × 10^-5` | 0 | 0 |

the also exposed an implementation artifact: the original washoff routine rounded remaining pollutant mass to six decimal places at each substep, which created artificial mass error in analytical tests. That quantization was removed, and the current-code metrics shown above are for the corrected implementation.

<img src={useBaseUrl('/validation/results/ancillary/VAL_WQ_001_SINGLE_CELL.png')} alt="Single-cell water quality validation" />

<img src={useBaseUrl('/validation/results/ancillary/VAL_WQ_001_TWO_CELL.png')} alt="Two-cell water quality validation" />

## Human risk and instability

The human-risk case validates the implemented algebra and classification logic, not field-scale public-safety prediction. Two active HydroPol2D pathways were tested:

- the simple instability index used when `flag_human_instability = 1`;
- the detailed force-balance classifier used when `flag_human_instability = 3`.

| Case | RMSE | Max error | Accuracy (%) | Boundary errors | NaN count |
|---|---:|---:|---:|---:|---:|
| Simple instability index | 0 | 0 | 100 | 0 | 0 |
| Slide/topple/drowning classifier | 0 | 0 | 100 | 0 | 0 |

The detailed classifier grid exercised all implemented output classes and matched the independent reference exactly.

<img src={useBaseUrl('/validation/results/ancillary/VAL_HR_001_SIMPLE_INSTABILITY.png')} alt="Simple human instability validation" />

<img src={useBaseUrl('/validation/results/ancillary/VAL_HR_001_FORCE_BALANCE.png')} alt="Detailed force balance human risk validation" />

## What these cases support

These ancillary cases support the current implementations of reservoir depletion, inflow and stage boundary handling, rainfall-raster ingestion, mass-based water-quality bookkeeping, and human-risk classification under controlled conditions.

They do not replace field calibration, site-specific forcing verification, or observational performance testing.
