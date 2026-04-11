---
title: Overview
---

# HydroPol2D

HydroPol2D is a distributed, physically based hydrological and hydrodynamic modeling framework designed to simulate coupled surface and subsurface processes at high spatial resolution.

The model integrates key components of the terrestrial water cycle, including overland flow routing, infiltration, evapotranspiration, groundwater dynamics, snow processes, and pollutant transport, within a unified raster-based computational environment.

---

## Core Capabilities

HydroPol2D enables the simulation of complex hydrologic systems through:

- **Surface flow routing** using Cellular Automata and Local Inertial formulations  
- **Infiltration and vadose zone processes** based on physically consistent parameterizations  
- **Groundwater–surface water interactions**, including recharge and exfiltration  
- **Evapotranspiration and interception dynamics**  
- **Snow accumulation and melt processes**  
- **Water quality transport and transformation**  
- **GPU-accelerated computation** for large-scale, high-resolution domains  

---

## Modeling Approach

HydroPol2D adopts a spatially distributed approach in which all variables are represented on raster grids, enabling seamless integration of geospatial datasets such as digital elevation models (DEMs), land use/land cover maps, and soil properties.

The model is designed to balance physical realism and computational efficiency, supporting both research-oriented simulations and engineering applications.

---

## Applications

HydroPol2D can be applied to a wide range of hydrological and environmental problems, including:

- Urban flood modeling and risk assessment  
- Watershed-scale hydrological analysis  
- Dam-break and flood wave propagation  
- Climate and land-use change impact studies  
- Environmental hazard and resilience assessment  
- Water quality and pollutant transport modeling  

---

## Design Philosophy

HydroPol2D is developed as a modular and extensible framework, allowing users to:

- Configure simulations based on data availability and objectives  
- Select among multiple process representations and numerical schemes  
- Integrate new modules and datasets as needed  
- Maintain transparency in model assumptions and computational methods  

The model is implemented in MATLAB and supports both CPU and GPU execution, enabling flexible deployment across a range of computational environments.