---
title: San Francisquito Catchment - Observed Rainfall Example
---
import useBaseUrl from '@docusaurus/useBaseUrl';

# San Francisquito Catchment - Observed Rainfall Example

## Purpose

This example describes the San Francisquito event-based setup used when rainfall forcing comes from observed data. It focuses on the inputs needed for event simulation and hydrograph comparison.

## Case setup

The current event simulation uses:

| Item | Value |
|---|---|
| Grid resolution | 30 m |
| Rainfall depth | 75 mm |
| Simulation duration | 48 h |
| Routing family | Local inertial |
| Outlet treatment | Perimeter outlet |
| Discharge observations in the current run | Not available |
| Comparison gauges | Generated from flow-accumulation percentiles |

The current rerun did not include a valid observed discharge file, so HydroPol2D generated comparison points from the drainage network. The page therefore documents the event setup and the model response for the present configuration.

## Simulation video

The animation below shows the 30 m event simulation. The panels show flood depth, velocity, hazard metric, and cumulative infiltration.

<div style={{ textAlign: 'center' }}>
  <video
    width="90%"
    controls
    poster={useBaseUrl('/videos/stanford_30m_outlet020_fullperiod_panels.png')}>
    <source src={useBaseUrl('/videos/stanford_30m_outlet020_fullperiod_panels.mp4')} type="video/mp4" />
    Your browser does not support the video tag.
  </video>

  <p><em>San Francisquito 30 m event simulation: flood depth, velocity, hazard, and cumulative infiltration.</em></p>
</div>

## What this example shows

This example highlights:

- observed rainfall forcing, ideally interpolated from multiple gauges when those data are available;
- observed discharge or stage data at the comparison location;
- explicit treatment of initial conditions, especially antecedent wetness;
- careful confirmation that the observation point represents the modeled drainage area.

## Summary results

The current event simulation produced:

- a peak outlet flow of `260.57 m³/s`;
- a maximum flood depth of `0.31 m`;
- a 48 h routed response with maps saved in the same four-panel format used in the controlled example.
