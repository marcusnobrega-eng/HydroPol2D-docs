---
title: Optional Forcing
---

# Optional Forcing

HydroPol2D supports multiple types of meteorological and hydrological forcing beyond basic rainfall input.

All forcing configurations are defined through the `General_Data.xlsx` file, which controls:

- the type of forcing used,
- the activation of model components,
- and the associated input datasets.

The model can operate under different forcing strategies depending on data availability and simulation objectives.

---

## Overview

HydroPol2D supports the following forcing options:

- Meteorological forcing for evapotranspiration (Penman–Monteith)
- Direct evaporation ($E$) and transpiration ($T$) inputs
- Spatial rainfall forcing (raster-based or gauge-interpolated)
- Synthetic design storms (Huff and Alternating Block)
- External inflow hydrographs
- Stage boundary conditions

Each forcing type is activated and configured through `General_Data.xlsx`.

---

## Meteorological Forcing (Penman–Monteith)

HydroPol2D computes evapotranspiration using a Penman–Monteith formulation when meteorological forcing is provided.

### Input source

Meteorological data are provided through:

- `ETP_input_data.xlsx`

---

### Spatial interpolation

Meteorological variables are distributed spatially using:

- inverse distance weighting (IDW)

This ensures that atmospheric forcing is consistent across the domain based on available measurement points.

---

### Required variables

Typical inputs include:

- air temperature  
- radiation (net or solar)  
- relative humidity  
- wind speed  

---

### Role in the model

Meteorological forcing is used to compute evapotranspiration, which removes water from:

- surface storage  
- soil moisture  

This approach is recommended when full atmospheric forcing is available.

---

## Direct Evaporation and Transpiration Inputs

HydroPol2D allows direct specification of evaporation and transpiration.

### Inputs

- evaporation ($E$) raster or time series  
- transpiration ($T$) raster or time series  

Units:

- $\mathrm{mm\,h^{-1}}$

---

### Role in the model

These fluxes are applied directly to:

- surface water storage  
- soil moisture  

This approach bypasses the need for meteorological forcing.

---

## Rainfall Forcing

HydroPol2D supports multiple rainfall input configurations.

---

### 1. Concentrated rainfall (uniform)

Defined through:

- `Rainfall_Intensity_Data.xlsx`

---

#### Description

- rainfall is applied uniformly over the domain  
- defined as a time series  

Units:

- $\mathrm{mm\,h^{-1}}$

---

### 2. Gauged rainfall (spatial interpolation)

Defined through:

- `Rainfall_Spatial_Input.xlsx`

---

#### Spatial interpolation

Rainfall fields are computed using:

- inverse distance weighting (IDW)

Gauge measurements are interpolated to all grid cells based on their spatial location.

---

#### Description

- multiple gauges can be specified  
- rainfall varies spatially and temporally  
- suitable for observed precipitation datasets  

Units:

- $\mathrm{mm\,h^{-1}}$

---

### 3. Raster-based rainfall

Rainfall can also be provided as:

- time-varying raster stacks  

Units:

- $\mathrm{mm\,h^{-1}}$

---

### Role in the model

Rainfall drives:

- infiltration  
- runoff generation  
- surface flow routing  

---

## Design Storms

HydroPol2D includes built-in synthetic storm generation.

### Methods available

- Huff distributions  
- Alternating Block method  

---

### Configuration

Defined through `General_Data.xlsx`, including:

- total rainfall depth  
- storm duration  
- temporal distribution  

The model generates the rainfall hyetograph internally.

---

## External Inflow Hydrographs

External inflow is defined through:

- `Inflow_Hydrograph.xlsx`

---

### Role in the model

Used for:

- upstream boundary conditions  
- river inflow  
- dam-break or controlled inflow scenarios  

---

### Implementation

- multiple gauges can be defined  
- each gauge is associated with spatial coordinates  
- inflow is distributed across all cells associated with each gauge  

Units:

- $\mathrm{m^3\,s^{-1}}$

---

## Stage Boundary Conditions

Stage boundary conditions are defined through:

- `Stage_Hydrograph.xlsx`

---

### Role in the model

Used for:

- downstream control  
- backwater effects  
- hydraulic constraints  

---

### Implementation

- stage is prescribed as water depth or elevation  
- all cells associated with the boundary receive the same imposed value  

Units:

- $\mathrm{m}$

---

## Control Through `General_Data.xlsx`

The `General_Data.xlsx` file defines:

- which forcing components are active  
- which datasets are used  
- temporal resolution  
- unit consistency  

It acts as the central interface between user-defined inputs and the model.

---

## Interaction Between Forcing Components

The forcing inputs interact as follows:

- rainfall introduces water into the system  
- evapotranspiration removes water from storage  
- meteorological variables control energy-driven fluxes  
- inflow hydrographs add external discharge  
- stage boundaries constrain hydraulic response  

These interactions define the system dynamics.

---

## Practical Considerations

- ensure temporal consistency across all forcing inputs  
- verify units before simulation  
- avoid mixing incompatible time resolutions  
- confirm correct spatial placement of gauges  
- ensure interpolation inputs are well distributed spatially  
- match forcing resolution with the model time step  

---

## Summary

Optional forcing in HydroPol2D enables flexible simulation setups ranging from simple rainfall-driven scenarios to fully coupled meteorological-hydrological systems.

All forcing configurations are managed through `General_Data.xlsx`, allowing users to:

- switch between forcing strategies  
- integrate external datasets  
- and define synthetic events  

The selected forcing approach should reflect:

- the objective of the simulation  
- data availability  
- and the required level of physical representation  