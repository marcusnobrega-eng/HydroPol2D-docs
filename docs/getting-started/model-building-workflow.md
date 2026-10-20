---
title: Model-building workflow
---

# Model-building workflow

HydroPol2D has one scientific case-building workflow and two compatible model
engines. The Case Builder creates the case. HydroPol2D-Python and
HydroPol2D-MATLAB consume it. Groundwater calibration is an optional Python
procedure that updates the case before either engine is launched.

```text
Case Builder: provisional physical domain
                    |
                    v
       Optional Python groundwater calibration
                    |
                    v
Case Builder: finalized parameters and initial states
                    |
                    v
                 Preflight
                    |
          +---------+---------+
          |                   |
          v                   v
 HydroPol2D-Python     HydroPol2D-MATLAB
          |                   |
          +---------+---------+
                    |
                    v
          Shared results and QA
```

## The central rule

A prepared domain is not necessarily a run-ready case. A case is run-ready
only after its selected parameters and initial states have been written to the
solver adapters and preflight has passed.

The Builder-managed case directory is the source of truth. Generated Python
YAML, MATLAB workbooks, MATLAB path adapters, and launch scripts are solver
views of that case. They should not acquire independent scientific settings.

## Standard workflow

Use this path when default or user-supplied parameters are adequate.

1. **Define the experiment.** Select the domain, model resolution, period,
   forcing, active processes, terrain treatment, river representation, solver
   adapters, output variables, and output interval.
2. **Preview the domain and cost.** Inspect the watershed, outlet, active-cell
   count, source-data availability, memory, transfer, and saved-output estimates.
3. **Prepare the complete case.** The Builder downloads or stages source data,
   creates the hydraulic terrain and river products, aligns static rasters,
   prepares forcing, and records provenance and QA.
4. **Finalize parameters and initial states.** Defaults, spatial rasters, or
   explicit user values are resolved into the final model-grid fields.
5. **Run preflight.** Preflight checks files, grids, units, forcing coverage,
   boundary conditions, required parameters, and supported solver combinations.
6. **Select the engine.** Run Python, MATLAB, or both. Choosing an engine does
   not rebuild the domain or change the scientific case.
7. **Inspect results.** Use saved model timestamps, mass-balance diagnostics,
   hydrographs, maps, and animations. Interface refresh time is not model time.

## Groundwater-calibrated workflow

Groundwater calibration introduces a deliberate two-pass build.

### Pass 1: provisional case

The Builder prepares the domain geometry and the inputs needed by the
calibration experiment:

- hydraulic DEM, active domain, rivers, outlets, and subbasins;
- soil, land-cover, root-depth, aquifer-bottom, and riverbed maps;
- forcing and the observed gauge record when available;
- provisional groundwater parameters sufficient to load the domain.

This provisional case is not the production simulation.

### Python calibration

The Python calibration procedure:

1. filters the observed hydrograph and constructs a master recession curve;
2. identifies the deep linear-reservoir response time from the slow tail;
3. spins up and releases the distributed Boussinesq aquifer;
4. estimates effective uniform horizontal conductivity and specific yield;
5. saves the groundwater-head field, shallow storage, and shallow discharge at
   each recession state;
6. writes calibration diagnostics and the state archive back into the case
   directory.

Calibration is implemented once in Python. MATLAB does not repeat this inverse
procedure.

### Pass 2: final case

The Builder imports the accepted calibration artifacts and resolves the final
initial conditions:

- a shallow-aquifer state selected by normalized storage depletion;
- deep discharge equal to filtered initial baseflow minus selected shallow
  discharge;
- deep storage equal to deep discharge multiplied by the calibrated response
  time;
- the configured fraction of future recharge routed to the deep reservoir;
- event-start near-surface and root-zone moisture from depth-aware ERA5-Land
  fields;
- transmission-zone moisture from steady gravity drainage and capillary
  influence from the selected groundwater table.

The Builder then regenerates both requested solver adapters and reruns
preflight. Only this finalized case should be used for the production run.

In the Builder, choose **Calibrate from observed streamflow** under
**Hydraulic parameters**. After the provisional case is prepared, open it in
**Check a case**. There the calibration panel accepts either a USGS gauge ID or
a local CSV, candidate `Ksat,h` and `Sy` values, and the normalized shallow
storage-depletion fraction. Calibration runs in the background and survives a
closed browser tab. **Refresh calibration status** reads the saved progress and
artifacts; a successful job applies the result and reruns preflight.

The finalized vadose state retains vertical information. ERA5-Land layers are
depth-overlap averaged for the 0.05 m surface store and LULC-derived root zone.
The transmission store is initialized from a van Genuchten equilibrium profile
conditioned on the selected groundwater table. Both solvers read these three
maps, while older single-moisture cases retain their documented fallback.

### Layered subsurface cases

With `--subsurface-scheme layered` (default `legacy`), the Builder prepares a
[layered subsurface](../theory/layered-subsurface) case for Python, MATLAB or both:

1. **Global inputs.** It derives the soil base from SoilGrids BDRICM, the
   regolith van Genuchten parameters from the texture class at 200 cm, and the
   regolith conductivity from GLHYMPS 2.0. The rules are on the
   [Soil](../inputs/soil#global-sources-used-by-the-case-builder) and
   [DTB](../inputs/dtb#global-sources-used-by-the-case-builder) pages.
2. **Solver adapters.** The Python case gets `vertical.subsurface.scheme: layered`
   and the static paths. The MATLAB adapter passes the soil-base and regolith
   rasters and `HYDROPOL_SUBSURFACE_SCHEME`.
3. **Deep-aquifer starting state.** `--deep-aquifer-initial-baseflow-mm-day`
   or `--deep-aquifer-mean-recharge-mm-year` (at most one) sets the starting
   storage of the deep reservoirs. A calibration's
   `DeepAquiferInitialState.json` replaces both.
4. **Calibration.** In layered cases the recession calibration fits two
   lateral-conductivity multipliers, one for the soil slots and one for the
   regolith slots, instead of `Ksat,h` and `Sy`. Finalization writes them to
   the Python case and to the MATLAB runner. $S_y$ stays on the retention
   curves. See [Groundwater Recession Calibration](../calibration/groundwater-recession).

## Component responsibilities

| Component | Owns | Does not own |
|---|---|---|
| Case Builder | Domain, source data, terrain, river and subgrid products, forcing, aligned parameter maps, initial states, solver adapters, provenance, and preflight | Numerical time stepping or parameter inversion |
| Groundwater calibration | Master recession analysis, effective shallow-aquifer parameters, deep response time, and the saved shallow-state archive | Terrain preparation, production forcing downloads, or a second case format |
| HydroPol2D-Python | Scientific reference implementation, calibration runtime, simulation, tests, and standard outputs | Independent rebuilding of Builder geometry |
| HydroPol2D-MATLAB | Compatible simulation of the finalized case and cross-language verification | A separate calibration workflow or independent Builder defaults |
| Results interface | Reads saved solver outputs and their model timestamps | Changing parameters or defining simulation state during refresh |

## Case states

| State | Meaning | Can run? |
|---|---|---:|
| Draft | Settings are still being edited. | No |
| Previewed | Domain and cost were inspected, but complete inputs may not exist. | No |
| Provisional | Physical domain exists and may be used for calibration. | Calibration only |
| Finalized | Accepted parameters and initial states were written to solver adapters. | Not yet |
| Preflight accepted | All required files and compatibility checks passed. | Yes |
| Running | One solver is advancing the finalized case. | In progress |
| Complete | Solver ended successfully and wrote the requested outputs. | Finished |

Preflight establishes internal consistency, not hydrological accuracy. A
calibrated parameter set establishes a fitted hypothesis, not universal field
truth. Both distinctions must remain visible in the interface and reports.

## Choosing Python or MATLAB

- Use **Python** for groundwater calibration, rapid diagnostics, automated
  testing, and the current scientific reference workflow.
- Use **MATLAB** when the finalized case requires the MATLAB implementation or
  an existing MATLAB production workflow.
- Use **both** for parity studies. Both adapters must come from the same
  finalized Builder case and use identical parameters, forcing, initial states,
  boundaries, and output cadence.

Standalone Python YAML and MATLAB Excel workflows remain useful for examples
and controlled tests. They are separate from a Builder-managed scientific case
and should not be mixed silently with it.
