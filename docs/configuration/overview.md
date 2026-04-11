---
title: Overview
---

# Model Configuration

HydroPol2D is fully controlled through the `General_Data.xlsx` spreadsheet.

This file defines:

- which processes are active  
- which datasets are used  
- how forcing is interpreted  
- how the numerical model is executed  

The spreadsheet acts as the central configuration layer linking all inputs, parameters, and model components.

---

## Configuration Philosophy

HydroPol2D is designed as a **flag-driven, spreadsheet-controlled model**.

The user does not modify the source code to change model behavior. Instead:

- all decisions are made in `General_Data.xlsx`  
- the model reads and interprets those settings at runtime  

This ensures:

- reproducibility  
- transparency  
- flexibility across applications  

---

## Structure of `General_Data.xlsx`

The spreadsheet organizes model configuration into logical groups.

Each row corresponds to:

- a parameter  
- a flag  
- or a control variable  

Each column typically contains:

- parameter name  
- assigned value  
- units  
- description or comment  

The model reads these values sequentially and assigns them to internal variables and flags.

---

## Core Configuration Domains

### 1. Simulation Control

Defines the global simulation setup:

- simulation duration  
- start and end times  
- time step configuration  
- output frequency  

These parameters control how the model advances in time and how results are stored.

---

### 2. Forcing Configuration

Defines which forcing datasets are used:

- rainfall type (uniform, spatial, or synthetic)  
- meteorological forcing (Penman–Monteith)  
- direct $E$ and $T$ inputs  
- inflow hydrographs  
- stage boundary conditions  

Each forcing option is activated through flags and linked to its corresponding input file.

---

### 3. Hydrological Processes

Controls activation of:

- infiltration  
- soil moisture dynamics  
- evapotranspiration  
- surface storage  

These processes depend on:

- Soil parameter table  
- LULC parameter table  
- LAI and albedo inputs  

The spreadsheet determines whether each process is active and how it is parameterized.

---

### 4. Hydraulic Routing Configuration

Defines how water is routed across the domain.

---

#### Local Inertial Model

- default routing scheme  
- solves simplified shallow water equations  
- accounts for inertia, slope, and friction  

Used for:

- flood propagation  
- dynamic surface flow  

---

#### Cellular Automata (CA)

- simplified routing scheme  
- lower computational cost  
- reduced physical detail  

Used for:

- large-scale simulations  
- rapid assessments  

---

### 5. Subgrid Configuration

Defines whether subgrid hydraulics are used.

If activated:

- a high-resolution DEM is used  
- storage–depth relationships are precomputed  
- hydraulic properties are derived at sub-cell scale  

This affects:

- volume calculation  
- wetted area  
- flow conveyance  

---

### 6. Numerical Controls

Defines how the model is solved.

---

#### Time stepping

HydroPol2D uses:

- explicit time stepping  
- adaptive time step control  

The time step is governed by:

- a Courant condition  

Typical values:

- $0.3 \leq \mathrm{Courant} \leq 0.7$

---

#### Stability controls

The spreadsheet defines:

- maximum allowable time step  
- safety factors  
- numerical thresholds  

These parameters directly affect stability and performance.

---

### 7. Boundary Conditions

Boundary conditions are defined externally but activated here.

---

#### Inflow boundaries

- linked to `Inflow_Hydrograph.xlsx`  
- multiple gauges allowed  
- each gauge distributes flow to associated cells  

---

#### Stage boundaries

- linked to `Stage_Hydrograph.xlsx`  
- imposed uniformly across boundary cells  

---

### 8. Spatial Configuration

The spreadsheet assumes that all raster inputs:

- share the same projection (projected CRS)  
- have identical resolution  
- are spatially aligned  

A domain mask is constructed internally based on valid cells across all rasters.

---

### 9. Output Configuration

Defines which outputs are generated:

- water depth  
- water surface elevation  
- velocity  
- soil moisture  
- evapotranspiration  
- pollutant concentrations  

Also controls:

- output frequency  
- file formats  

---

## Flags and Logical Control

A key feature of HydroPol2D is the use of flags.

Each process is activated through a binary or logical flag defined in the spreadsheet.

Examples include:

- rainfall activation  
- ET computation method  
- routing scheme selection  
- subgrid activation  

The model evaluates these flags at runtime and dynamically adjusts the simulation workflow.

---

## Execution Workflow

At runtime, HydroPol2D follows:

1. Read `General_Data.xlsx`  
2. Assign flags and parameters  
3. Load spatial datasets  
4. Initialize model state  
5. Apply forcing  
6. Solve hydrological processes  
7. Route flow  
8. Save outputs  

All behavior is dictated by the configuration file.

---

## Practical Considerations

- every activated process must have a corresponding input  
- inconsistent configurations will lead to unstable simulations  
- time resolution of forcing must match model requirements  
- spatial inputs must be aligned prior to execution  
- numerical parameters must be selected with stability in mind  

---

## Important Note

This page provides a structural overview of the configuration system.

A complete description of each parameter, flag, and variable in `General_Data.xlsx` is provided in the next section:

→ **Configuration Parameters**

---

## Summary

The `General_Data.xlsx` file defines the behavior of HydroPol2D.

It controls:

- physical processes  
- numerical solution  
- forcing inputs  
- boundary conditions  
- model outputs  

All simulations are fully reproducible through this configuration file.