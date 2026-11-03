---
title: Limitations
---

# Validation Limitations

The current validation package is a verification and controlled-dynamics
campaign. It confirms that the model equations, storage ledgers, forcing
interpretation, routing options, and boundary conditions behave as expected in
cases with known references.

It is not a substitute for field calibration, uncertainty analysis, or
site-specific observational validation.

## Voronoi mesh mode

The Voronoi finite-volume pathway has controlled CPU validation, not
field-scale validation. GPU execution and India-scale performance are gated,
and unresolved channels are supported only by the local-inertial solver. A
case that needs kinematic, diffusive, or full-momentum routing must use fully
resolved 2D channels until a separate channel-coupling validation is added.

In HydroPol2D-Python, the mesh runs the regular grid's optional modules on its CPU
(NumPy) engine: snow, water quality, human instability, reservoirs, urban drainage,
green infrastructure and detention ponds. Each is checked against the regular grid on
a mesh made of the grid's own square cells, where the two agree to round-off. None has
been checked against observations on an irregular mesh. Open limits:

- the GPU (JAX) mesh engine does not run these modules yet;
- human instability runs as the continuous risk index (mode 1) only; a mesh case with
  the slide and topple classification (`human_risk.method: classification`, mode 3)
  stops at the input check, which offers the regular grid;
- reservoirs, urban drainage, green infrastructure and detention ponds need a mesh
  without river channels or sub-grid tables, and water quality one without river
  channels;
- a reservoir, drainage inlet, GI compartment or pond device moves to the mesh cell
  that holds most of its raster cell, and a pond takes the mesh cells it covers by half
  or more;
- with a wash-off exponent other than 1, wash-off depends on how many edges the water
  leaves a cell through, so a Voronoi mesh (about six edges per cell) washes off
  differently from the grid (four faces).

## Optional modules in MATLAB {#matlab-optional-modules}

Since 2026-11-02, HydroPol2D (MATLAB) runs urban drainage, detention ponds, green
infrastructure and D8 local-inertial routing on the regular grid, with the equations of
HydroPol2D-Python. Each is checked against the Python kernel (VAL-UD-001, VAL-POND-001,
VAL-GI-001 and the D8 check). None has been checked against observations. Open limits:

- all four are set up in the bypass script (the `InputData_Bypass` structure of
  `Config/input_data_bypass_script.m`). The case workbook has no inputs for them, so
  `flag_urban_drainage`, `flag_detention_ponds` or `flag_green_infrastructure` = 1 in
  Excel mode stops the run, and `flag_d8_local_inertial` is not read from the workbook;
- urban drainage runs with the local-inertial solver only, without the channel subgrid
  and without water quality;
- D8 local-inertial routing (`flag_d8_local_inertial = 1`) needs `flag_inertial = 1` and
  the Bates scheme. It does not run with the channel subgrid, water quality, human risk,
  snow, inflow or stage hydrographs, observed gauges, river-aquifer exchange, DEM
  reduction, urban drainage, detention ponds or green infrastructure.
  `flag_d8_full_domain = 0` keeps a D8 river graph inside a D4 floodplain; 1 puts every
  cell on the D8 graph;
- the older raster D8 (`flag_D8`) is retired, and `flag_D8 = 1` stops the run;
- a Voronoi or quadtree mesh run refuses urban drainage, detention ponds and green
  infrastructure. Reservoirs, water quality, human risk (mode 1) and snow run on MATLAB
  meshes.

## Layered Subsurface and Recession Calibration

The layered subsurface has controlled tests and Python-MATLAB parity on
synthetic V-tilted domains, not field validation. Open limits:

- no lateral flow of perched water above unsaturated regolith;
- no regolith class table and no per-slot raster outputs;
- no capillary fringe: capillary rise refills the soil above the table only
  up to field capacity;
- the compiled Python city loop does not yet run the layered scheme with
  lateral groundwater flow.

The recession calibration has been tested with a twin experiment on a
synthetic valley, not against observed wells or a field hydrograph.

## Evidence Boundaries

Some hydrodynamic and groundwater cases use numerical references. These are
valuable implementation checks, especially when analytical solutions are not
available, but they should be reported separately from analytical validation.

Applied examples such as Stanford are useful demonstrations of workflow and
model setup. They are not analytical validation cases unless they are paired
with observations, calibrated/inverse-modeled truth, or another defensible
reference.

## Neal (2012) Subgrid Model Recession

The Neal (2012) channel-subgrid benchmarks reproduce in-bank routing, floodplain
activation, peak discharge, and maximum inundation extent within the tested
geometries. A coarse channel cell has one representative water level. Water
stored on internal benches or the external floodplain therefore cannot recede
independently from the embedded channel. In the staged benchmark, this causes
the coarse Neal (2012) floodplain to become dry earlier than the fine-grid numerical
reference. Applications in which late floodplain drainage controls the result
should evaluate recession timing against observations or a finer hydraulic
simulation.
