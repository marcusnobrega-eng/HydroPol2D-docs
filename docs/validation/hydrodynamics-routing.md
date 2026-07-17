---
title: Hydrodynamics and Routing
---
import useBaseUrl from '@docusaurus/useBaseUrl';

# Hydrodynamics and Routing Validation

Phase 1 hydrodynamic validation was organized by routing family. Full momentum was validated first, then local inertial and cellular automata, and then the corrected kinematic and diffusive solvers. The purpose was not only to check hydrographs, but also to confirm conservation, symmetry, boundary enforcement, and behavior relative to the intended equation set.

## Full-momentum hydrodynamics

### What was tested

Five current-code cases were used:

- tilted-plane hydrograph;
- V-tilted symmetry and conservation;
- Ritter dry-bed dam-break;
- non-breaking wave;
- prescribed-stage boundary behavior.

### Main result

The full-momentum cases passed the Phase 1 controlled benchmarks.

| Case | Primary RMSE | Relative L2 | NSE | Mass error (%) |
|---|---:|---:|---:|---:|
| Tilted plane hydrograph | 0.0264 | 0.0311 | 0.9961 | `7.80 × 10^-12` |
| V-tilted symmetry and conservation | `3.50 × 10^-18` | -- | -- | `2.74 × 10^-12` |
| Ritter dam-break profile | 0.0305 | 0.0567 | 0.9992 | `1.26 × 10^-13` |
| Non-breaking wave profile | 0.0116 | 0.0260 | 0.9997 | 4.5638 |
| Stage-hydrograph boundary | 0.0000 | -- | -- | `1.35 × 10^-13` |

The tilted-plane case reproduced the kinematic-wave limiting response closely. The V-tilted case conserved mass to machine precision and preserved bilateral symmetry. The Ritter case passed as the main discontinuous-flow analytical benchmark. The non-breaking-wave case provided a smoother traveling-wave benchmark with small profile error and high NSE.

<img src={useBaseUrl('/validation/phase1/hydrodynamics/P1_HYDRO_FM_PLANE_001.png')} alt="Full momentum tilted plane validation" />

<img src={useBaseUrl('/validation/phase1/hydrodynamics/P1_HYDRO_FM_VTILT_001.png')} alt="Full momentum V-tilted validation" />

<img src={useBaseUrl('/validation/phase1/hydrodynamics/P1_HYDRO_FM_RITTER_001.png')} alt="Full momentum Ritter dam-break validation" />

<img src={useBaseUrl('/validation/phase1/hydrodynamics/P1_HYDRO_FM_NBW_001_PROFILES.png')} alt="Full momentum non-breaking wave profiles" />

<p><em>Full-momentum Phase 1 figures. These cases span limiting shallow sheet flow, symmetry and conservation on the shared V-tilted domain, a dry-bed discontinuity benchmark, and a smooth traveling-wave benchmark.</em></p>

## Local inertial and cellular automata

### What was tested

The same Phase 1 sequence was repeated for local-inertial and cellular-automata routing. These results should be interpreted in the context of each method. Local inertial is an approximation to the shallow-water equations. Cellular automata is mainly a routing and storage-redistribution method, not a momentum solver.

### Main result

Local inertial passed the tilted-plane, V-tilted, and stage-boundary cases. Its Ritter comparison is retained as diagnostic evidence rather than a validation claim. Cellular automata passed the conservation, symmetry, and boundary-bookkeeping checks.

| Method | Case | RMSE | Relative L2 | NSE | Mass error (%) | Status |
|---|---|---:|---:|---:|---:|---|
| Local inertial | Plane | 0.0169 | 0.0200 | 0.9984 | `7.47 × 10^-12` | pass |
| Local inertial | V-tilted | 0.0000 | -- | -- | `3.66 × 10^-12` | pass |
| Local inertial | Ritter | 0.1823 | 0.3838 | 0.9552 | `5.05 × 10^-14` | diagnostic fail |
| CA | Plane | 0.0172 | 0.0204 | 0.9983 | `7.69 × 10^-12` | pass |
| CA | V-tilted | 0.0000 | -- | -- | `4.04 × 10^-12` | pass |
| CA | Ritter | 0.1592 | 0.2957 | 0.9875 | `7.58 × 10^-14` | diagnostic |

<div style={{display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(280px, 1fr))', gap: '1rem'}}>
  <img src={useBaseUrl('/validation/phase1/hydrodynamics/P1_HYDRO_LI_PLANE_001.png')} alt="Local inertial plane validation" />
  <img src={useBaseUrl('/validation/phase1/hydrodynamics/P1_HYDRO_CA_PLANE_001.png')} alt="Cellular automata plane validation" />
</div>

<div style={{display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(280px, 1fr))', gap: '1rem'}}>
  <img src={useBaseUrl('/validation/phase1/hydrodynamics/P1_HYDRO_LI_RITTER_001.png')} alt="Local inertial Ritter diagnostic" />
  <img src={useBaseUrl('/validation/phase1/hydrodynamics/P1_HYDRO_CA_RITTER_001.png')} alt="Cellular automata Ritter diagnostic" />
</div>

<p><em>The local-inertial Ritter result is a limitation, not a report-ready dam-break validation.</em></p>

## Canonical V-tilted benchmark hydrograph

### What was tested

The original V-tilted benchmark hydrograph was reintroduced as a full routing benchmark using the full HydroPol2D bypass and preprocessing workflow. All routing options used the same `20 m` raster, `10.8 mm/h` rainfall for `90 min`, outlet cells, and disabled-loss hydrologic settings.

### Main result

All five routing options reproduced the benchmark hydrograph shape well over the common `0 min` to `180 min` comparison window. Every run also closed the rainfall-outlet-storage ledger to `-0.0181 %`, which shows that the differences are routing and recession differences rather than mass-balance failures.

| Routing mode | RMSE (m³/s) | NSE | Peak error (%) | Volume error (%) | Mass error (%) |
|---|---:|---:|---:|---:|---:|
| Full momentum | 0.303 | 0.9730 | 0.052 | 7.50 | -0.0181 |
| Local inertial | 0.287 | 0.9759 | 2.05 | 5.04 | -0.0181 |
| Cellular automata | 0.323 | 0.9694 | 0.008 | 3.95 | -0.0181 |
| Kinematic | 0.249 | 0.9817 | 0.020 | 3.23 | -0.0181 |
| Diffusive | 0.255 | 0.9809 | 0.063 | 3.20 | -0.0181 |

<img src={useBaseUrl('/validation/phase1/hydrodynamics/P1_HYDRO_VTILT_ROUTING_HYDROGRAPH.png')} alt="Canonical V-tilted benchmark hydrograph" />

<img src={useBaseUrl('/validation/phase1/hydrodynamics/P1_HYDRO_VTILT_ROUTING_VOLUME.png')} alt="Canonical V-tilted cumulative outlet volume diagnostics" />

## Corrected kinematic and diffusive routing

### What was tested

The kinematic and diffusive solvers were rewritten around a shared conservative D4 face-flux core after an implementation audit identified inconsistent slope logic and solver dispatch problems in the earlier versions.

### Main result

Both corrected solvers passed the tilted-plane, V-tilted conservation, and stage-boundary checks. The diffusive Ritter case failed, as expected for a reduced diffusive-wave approximation under a sharp dry-bed discontinuity.

| Method | Case | RMSE | Relative L2 | NSE | Mass error (%) | Status |
|---|---|---:|---:|---:|---:|---|
| Kinematic | Plane | 0.0156 | 0.0184 | 0.9986 | `7.66 × 10^-12` | pass |
| Kinematic | V-tilted | 0.0000 | -- | -- | `4.18 × 10^-12` | pass |
| Kinematic | Ritter | 0.2408 | 0.5069 | 0.9245 | 0.0000 | diagnostic |
| Diffusive | Plane | 0.0172 | 0.0203 | 0.9984 | `7.75 × 10^-12` | pass |
| Diffusive | V-tilted | 0.0000 | -- | -- | `3.73 × 10^-12` | pass |
| Diffusive | Ritter | 0.5670 | 1.1151 | -0.0803 | `1.53 × 10^-12` | diagnostic fail |

<div style={{display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(280px, 1fr))', gap: '1rem'}}>
  <img src={useBaseUrl('/validation/phase1/hydrodynamics/P1_HYDRO_KIN_PLANE_001.png')} alt="Corrected kinematic plane validation" />
  <img src={useBaseUrl('/validation/phase1/hydrodynamics/P1_HYDRO_DIFF_PLANE_001.png')} alt="Corrected diffusive plane validation" />
</div>

## What this validation supports

Phase 1 supports the current full-momentum implementation for the tested analytical and bookkeeping benchmarks. It also supports local inertial, cellular automata, kinematic, and diffusive routing for the specific controlled benchmarks listed above. The method limits still matter: local inertial and diffusive results should not be over-interpreted as validated dry-bed dam-break solvers.

## Neal (2012) subgrid model

The Neal (2012) extension represents a channel narrower than the local-inertial grid cell and combines channel and floodplain discharge at each orthogonal face. Comparisons against fine-grid numerical references cover in-bank flow, steady and transient compound-channel routing, bank activation, and maximum inundation extent. The formulation improves the coarse-grid hydrograph, stage, storage, and wet-area estimates in all retained cases. Late floodplain recession remains less accurate because each coarse cell has one representative water level.

The geometry, metrics, and figures are provided in [Neal (2012) Subgrid Model Validation](./neal-subgrid).
