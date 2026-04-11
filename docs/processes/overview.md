---
title: Overview
---

# Processes

HydroPol2D simulates a set of coupled hydrological and hydrodynamic processes within a distributed raster-based framework.

The model is designed to represent the spatial and temporal evolution of water movement across the land surface and subsurface, while allowing additional modules such as snow, groundwater, and water quality to be activated depending on the application.

---

## Main Process Groups

### Surface Flow Routing

HydroPol2D includes different routing approaches to simulate water movement over the terrain, including Cellular Automata and Local Inertial formulations.

These schemes estimate the redistribution of surface water based on local gradients, hydraulic conditions, and numerical controls.

---

### Infiltration

Infiltration controls the transfer of water from the land surface into the soil.

This process depends on soil hydraulic properties, antecedent moisture conditions, and the availability of ponded water at the surface.

---

### Evapotranspiration

Evapotranspiration removes water from the soil–plant–atmosphere system and can be represented using input forcing or physically based estimation approaches, depending on the selected configuration.

---

### Groundwater Dynamics

HydroPol2D can represent recharge, subsurface storage, lateral groundwater flow, and groundwater–surface water exchanges.

These processes are important for simulations in which subsurface contributions influence river flow, exfiltration, or long-term water balance.

---

### Snow Processes

For cold-region or seasonally affected simulations, the model can represent snowfall, snow storage, snowmelt, and associated water release to the surface system.

---

### Water Quality

HydroPol2D also supports pollutant build-up, wash-off, and transport, allowing the analysis of contaminant dynamics coupled to hydrological response.

---

## Process Coupling

A key characteristic of HydroPol2D is that these processes are not treated independently. Instead, they interact dynamically during the simulation.

For example:

- Rainfall generates surface water  
- Surface water may infiltrate into the soil  
- Soil water may recharge groundwater  
- Groundwater may later contribute back to channels or the surface domain  
- Flow routing transports both water and dissolved or particulate pollutants  

This coupling is central to the model’s ability to represent complex environmental systems.

---

## Summary

HydroPol2D is built as a modular but integrated framework in which multiple physical processes can be activated and coupled according to the needs of the simulation.

This structure makes the model suitable for both simplified applications and advanced multi-process studies.