---
title: Mathematical Overview
---

# Mathematical Overview

HydroPol2D is a distributed, grid-based model designed to simulate the coupled dynamics of surface water flow and hydrological processes over complex terrain.

The model integrates:

- surface flow routing  
- infiltration and soil storage  
- evapotranspiration  
- groundwater interaction (optional)  
- water quality transport (optional)  

within a unified computational framework.

---

## Modeling Philosophy

HydroPol2D follows a physically-based but computationally efficient approach.

The model:

- solves depth-averaged flow equations on a structured grid  
- represents subgrid processes through parameterization  
- uses categorical maps linked to parameter tables  
- allows modular activation of processes through flags  

This design enables flexibility across a wide range of applications, from small catchments to large-scale flood simulations.

---

## General Water Balance

At each grid cell, the model enforces conservation of mass through a balance between:

- incoming water (rainfall, inflow)  
- outgoing water (flow, infiltration, evapotranspiration)  
- storage within the cell  

This balance governs the evolution of water depth over time.

---

## Model Components

The model can be conceptually divided into four interacting components:

---

### 1. Hydrological Processes

Includes:

- rainfall input  
- infiltration into the soil  
- soil moisture storage  
- evapotranspiration  

These processes determine how much water remains available for surface flow.

---

### 2. Surface Flow Routing

Water that is not infiltrated or lost is routed across the domain.

HydroPol2D supports multiple routing approaches:

- Local Inertial (default)  
- Diffusive wave  
- Kinematic wave  
- Cellular Automata  

The selected approach determines how flow velocities and fluxes are computed.

---

### 3. Hydraulic Controls

Localized features modify flow behavior within the domain:

- internal boundary conditions (rating curves)  
- reservoirs and storage elements  
- inflow and stage boundaries  

These introduce controlled flow and storage dynamics.

---

### 4. Numerical Solution

The model is solved using:

- explicit time stepping  
- optional adaptive time stepping  
- stability constraints based on flow conditions  

This ensures computational efficiency while maintaining numerical stability.

---

## Coupling Between Components

All processes are evaluated sequentially within each time step:

1. Apply external forcing (rainfall, inflow, meteorology)  
2. Compute infiltration and losses  
3. Update water depth  
4. Route flow across the domain  
5. Apply hydraulic controls  
6. Store outputs  

This coupling ensures consistency between hydrological and hydraulic processes.

---

## Spatial Representation

The model operates on a raster grid where each cell contains:

- topographic information (DEM)  
- land surface properties (LULC)  
- soil properties  
- optional additional layers (LAI, albedo, DTB)  

All spatial variability is handled through these inputs and associated parameter tables.

---

## Model Flexibility

HydroPol2D is controlled through:

- configuration parameters  
- flags  
- parameter tables  

This allows users to:

- activate or deactivate processes  
- switch between numerical schemes  
- adapt the model to different environments  

without modifying the core code.

---

## Summary

HydroPol2D combines hydrological and hydrodynamic processes within a flexible, grid-based framework.

The model balances:

- physical realism  
- computational efficiency  
- modular configurability  

making it suitable for both research and applied engineering problems.