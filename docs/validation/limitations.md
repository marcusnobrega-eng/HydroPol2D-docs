---
title: Limitations
---

# Validation Limitations

The current validation package is a Phase 1 verification and controlled-dynamics
campaign. It confirms that the model equations, storage ledgers, forcing
interpretation, routing options, and boundary conditions behave as expected in
cases with known references.

It is not a substitute for field calibration, uncertainty analysis, or
site-specific observational validation.

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
