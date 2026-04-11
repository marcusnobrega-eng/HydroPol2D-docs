---
title: Parameter Tables
---

# Parameter Tables

HydroPol2D uses parameter tables to assign physical properties to categorical raster inputs.

Categorical maps such as LULC and Soil are not used directly in the governing equations. Instead, each class acts as an index into a parameter table, where the corresponding physical parameters are defined.

This structure separates spatial information from parameter definition and makes the model easier to calibrate, adapt, and interpret.

---

## General Structure

Each parameter table contains:

- a **class identifier** (`Index`)
- a set of **parameters associated with that class**

At runtime, HydroPol2D:

1. reads the raster value at each grid cell,
2. uses that value as an index,
3. assigns the corresponding parameters from the table.

For this reason, raster classes and table indices must match exactly.

---

## LULC Parameter Table

The LULC table defines surface-related properties controlling flow resistance, interception, imperviousness, and pollutant-related behavior.

### Example structure

| Land Cover | Index | $n$<br />$(\mathrm{s\,m^{-1/3}})$ | $h_0$<br />$(\mathrm{mm})$ | $d_0$<br />$(\mathrm{mm})$ | $C_1$ | $C_2$ | $C_3$ | $C_4$ | $\mathrm{index\_impervious}$ |
|:----------:|:-----:|:---------------------------------:|:--------------------------:|:--------------------------:|:-----:|:-----:|:-----:|:-----:|:----------------------------:|
| Tree cover | 10 | 0.10 | 0 | 0 | 10 | 0.20 | 800 | 1.20 | 50 |
| Shrubland | 20 | 0.08 | 0 | 0 | 12 | 0.20 | 900 | 1.20 | NaN |
| Grassland | 30 | 0.06 | 0 | 0 | 15 | 0.22 | 1000 | 1.20 | NaN |
| Cropland | 40 | 0.05 | 0 | 0 | 30 | 0.25 | 1400 | 1.30 | NaN |
| Built-up | 50 | 0.03 | 0 | 0 | 80 | 0.30 | 2000 | 1.30 | NaN |
| Bare / sparse vegetation | 60 | 0.035 | 0 | 0 | 45 | 0.25 | 1600 | 1.25 | NaN |
| Snow and ice | 70 | 0.02 | 0 | 0 | 1 | 0.10 | 200 | 1.10 | NaN |
| Permanent water bodies | 80 | 0.035 | 0 | 0 | 0 | 0 | 0 | 0 | NaN |
| Herbaceous wetland | 90 | 0.12 | 0 | 0 | 8 | 0.18 | 700 | 1.20 | NaN |
| Mangroves | 95 | 0.15 | 0 | 0 | 8 | 0.18 | 700 | 1.20 | NaN |
| Moss and lichen | 100 | 0.08 | 0 | 0 | 5 | 0.15 | 500 | 1.15 | NaN |

*Table 1. HydroPol2D LULC parameter table. The `Index` values must match the categorical values in the LULC raster.*

### Variable definitions

- $n$: Manning’s roughness coefficient
- $h_0$: interception parameter
- $d_0$: initial surface storage parameter
- $C_1$–$C_4$: coefficients associated with the pollutant build-up and wash-off formulation
- $\mathrm{index\_impervious}$: identifier used to associate a class with impervious behavior

The values shown above correspond to the current HydroPol2D parameter table and should be revised as needed for the adopted classification scheme and study area.

---

## Soil Parameter Table

The soil table defines the hydraulic properties used to estimate infiltration and near-surface storage behavior.

### Example structure

| Soil Type | Index | $K_{\mathrm{sat}}$<br />$(\mathrm{mm\,h^{-1}})$ | $n$ | $\alpha$<br />$(\mathrm{m^{-1}})$ | $\theta_{\mathrm{sat}}$<br />$(\mathrm{cm^3\,cm^{-3}})$ | $\theta_{\mathrm{r}}$<br />$(\mathrm{cm^3\,cm^{-3}})$ | $\theta_{\mathrm{i}}$<br />$(\mathrm{cm^3\,cm^{-3}})$ | $S_{\mathrm{y}}$ | $K_{\mathrm{g,sat}}$<br />$(\mathrm{mm\,h^{-1}})$ | $\mathrm{DTB}$<br />$(\mathrm{m})$ |
|:---------:|:-----:|:-----------------------------------------------:|:---:|:----------------------------------:|:--------------------------------------------------------:|:------------------------------------------------------:|:------------------------------------------------------:|:---------------:|:---------------------------------------------------:|:--------------------------------:|
| Clay | 1 | 0.3 | 1.09 | 0.8 | 0.385 | 0.068 | 0.20 | 0.03 | 6 | 1 |
| Silty Clay | 2 | 0.5 | 1.23 | 1.0 | 0.423 | 0.089 | 0.22 | 0.04 | 10 | 1 |
| Sandy Clay | 3 | 0.6 | 1.31 | 1.5 | 0.321 | 0.075 | 0.17 | 0.06 | 12 | 1 |
| Clay Loam | 4 | 1.0 | 1.31 | 1.9 | 0.309 | 0.095 | 0.16 | 0.08 | 20 | 1 |
| Silty Clay Loam | 5 | 1.0 | 1.23 | 1.5 | 0.432 | 0.089 | 0.22 | 0.09 | 20 | 1 |
| Sandy Clay Loam | 6 | 1.5 | 1.48 | 3.0 | 0.330 | 0.065 | 0.17 | 0.11 | 30 | 1 |
| Silty Loam | 7 | 7.6 | 1.41 | 4.5 | 0.434 | 0.067 | 0.22 | 0.14 | 152 | 1 |
| Loam | 8 | 3.4 | 1.56 | 3.6 | 0.486 | 0.078 | 0.25 | 0.18 | 68 | 1 |
| Sandy Loam | 9 | 10.9 | 1.89 | 7.5 | 0.412 | 0.065 | 0.21 | 0.22 | 218 | 1 |
| Silt | 10 | 3.4 | 1.37 | 4.0 | 0.486 | 0.067 | 0.24 | 0.12 | 68 | 1 |
| Loamy Sand | 11 | 29.9 | 2.28 | 14.5 | 0.401 | 0.057 | 0.20 | 0.25 | 598 | 1 |
| Sand | 12 | 117.8 | 2.68 | 14.5 | 0.417 | 0.045 | 0.21 | 0.30 | 2356 | 1 |
| Water | 0 | 0.3 | 1.09 | 0.8 | 0.385 | 0.068 | 0.20 | 0.03 | 6 | 1 |

*Table 2. HydroPol2D soil parameter table. The `Index` values must match the categorical values in the soil raster.*

### Variable definitions

- $K_{\mathrm{sat}}$: saturated hydraulic conductivity
- $n$: Van Genuchten shape parameter
- $\alpha$: inverse air-entry parameter
- $\theta_{\mathrm{sat}}$: saturated water content
- $\theta_{\mathrm{r}}$: residual water content
- $\theta_{\mathrm{i}}$: initial soil moisture
- $S_{\mathrm{y}}$: specific yield
- $K_{\mathrm{g,sat}}$: saturated conductivity associated with subsurface or groundwater parameterization
- $\mathrm{DTB}$: depth to bedrock or effective storage depth

Only the **surface or near-surface soil class** is used in HydroPol2D to estimate infiltration capacity.

The values shown above correspond to the current HydroPol2D soil parameter table and should be revised as needed for the adopted soil classification and simulation scenario.

---

## DTB Assignment Through the Soil Table

If a DTB raster is not available, DTB values can be assigned directly in the soil table.

In this case:

- each soil class is associated with a representative DTB value,
- the DTB field is constructed implicitly from the soil map,
- storage depth remains consistent with the adopted soil classification.

This is particularly useful in data-scarce applications.



---

## Consistency Requirements

The following conditions must be satisfied:

- all raster class values must exist in the corresponding table,
- class identifiers must not be duplicated,
- parameter fields must not be left empty,
- units must be consistent with the model formulation.

Any inconsistency between raster classes and parameter tables will lead to incorrect assignment of physical properties.

---

## Practical Use

Parameter tables are the main mechanism used to:

- calibrate the model,
- adapt the model to different environments,
- perform sensitivity analysis,
- test alternative physical assumptions without modifying the code.

In HydroPol2D, most practical modifications to model behavior are made by editing these tables.

---

## Internal Boundary Conditions (Control Structures)

HydroPol2D allows the definition of internal boundary conditions (IBCs) that locally modify the hydraulic response of the domain.

These structures are implemented through a simple rating-curve approach that converts water depth into discharge. At the selected control cells, flow is no longer determined solely by the standard local inertial update. Instead, discharge is imposed through a depth–discharge relationship defined by user-specified parameters.

This allows the model to represent localized hydraulic controls such as:

- culverts  
- gates  
- weirs  
- outlets  
- engineered control sections  

---

### Concept

Each internal boundary condition is linked to a control cell defined by its spatial coordinates. The discharge through that control is computed from the local water depth using a rating-curve formulation.

In the current HydroPol2D implementation, the control structure spreadsheet defines two rating-curve branches, each with its own coefficient and threshold parameters. This makes it possible to represent piecewise hydraulic behavior under different flow depths or operating conditions.

The resulting discharge is imposed at the corresponding control location and therefore modifies the local flow dynamics within the numerical solver.

---

### Function in the Model

Internal boundary conditions affect the simulation by:

- imposing a discharge response based on local depth  
- modifying inlet or outlet cell fluxes within the local inertial solver  
- introducing controlled internal flow exchange within the computational domain  

These structures can strongly influence:

- upstream storage  
- downstream propagation  
- flood attenuation  
- local backwater effects  

---

### Role in the Numerical Model

At cells where an internal boundary condition is defined:

- water depth is evaluated at the control point  
- discharge is computed from the rating-curve parameters  
- the resulting flow is imposed in the hydraulic update  

This means that the local inertial solver is locally modified by the control structure behavior. The discharge is prescribed from the rating relationship rather than being obtained exclusively from the standard face-based flux computation.

---

### Input Table Structure

Internal boundary conditions are defined through a dedicated spreadsheet.

#### Table structure

| Parameter | Units | Description |
|:---------:|:-----:|-------------|
| $\mathrm{Index}$ | — | Identifier of the control structure |
| $x$ | $\mathrm{m}$ | Easting coordinate of the control cell |
| $y$ | $\mathrm{m}$ | Northing coordinate of the control cell |
| $k_1$ | — | Coefficient of the first rating-curve branch |
| $h_{0,1}$ | $\mathrm{m}$ | Reference depth or threshold associated with the first branch |
| $k_2$ | — | Exponent or shape parameter associated with the first branch |
| $x_{\mathrm{d},1}$ | $\mathrm{m}$ | Easting coordinate of the first discharge control point |
| $y_{\mathrm{d},1}$ | $\mathrm{m}$ | Northing coordinate of the first discharge control point |
| $k_3$ | — | Coefficient of the second rating-curve branch |
| $h_{0,2}$ | $\mathrm{m}$ | Reference depth or threshold associated with the second branch |
| $k_4$ | — | Exponent or shape parameter associated with the second branch |
| $x_{\mathrm{d},2}$ | $\mathrm{m}$ | Easting coordinate of the second discharge control point |
| $y_{\mathrm{d},2}$ | $\mathrm{m}$ | Northing coordinate of the second discharge control point |

*Table 3. HydroPol2D internal boundary condition parameter table. These parameters define the rating-curve behavior used to convert depth into discharge.*

---

### Example Values

| $\mathrm{Index}$ | $x$ $(\mathrm{m})$ | $y$ $(\mathrm{m})$ | $k_1$ | $h_{0,1}$ $(\mathrm{m})$ | $k_2$ | $x_{\mathrm{d},1}$ $(\mathrm{m})$ | $y_{\mathrm{d},1}$ $(\mathrm{m})$ | $k_3$ | $h_{0,2}$ $(\mathrm{m})$ | $k_4$ | $x_{\mathrm{d},2}$ $(\mathrm{m})$ | $y_{\mathrm{d},2}$ $(\mathrm{m})$ |
|:----------------:|-------------------:|-------------------:|------:|-------------------------:|------:|-----------------------------------:|-----------------------------------:|------:|-------------------------:|------:|-----------------------------------:|-----------------------------------:|
| 1 | -5166015.11 | -2706361.32 | 1.5 | 0.0 | 0.50 | -5166037.22 | -2706321.554 | 3.0 | 2.5 | 1.5 | -5166037.22 | -2706321.554 |
| 2 | -5166922.84 | -2704154.64 | 16.0 | 0.0 | 1.5 | -5166922.84 | -2704174.64 | 0.538951413 | 0.1 | 0.5 | -5166922.84 | -2704174.64 |

*Table 4. Example internal boundary condition parameters currently used in HydroPol2D.*

---

### Interpretation

The control structure formulation is based on a depth–discharge relationship of the general form:

$$
Q = f(h)
$$

where:

- $Q$ is discharge through the structure in $\mathrm{m^3\,s^{-1}}$  
- $h$ is local water depth in $\mathrm{m}$  
- the coefficients $k_1$, $k_2$, $k_3$, and $k_4$ define the rating-curve response  
- the terms $h_{0,1}$ and $h_{0,2}$ define the reference depths associated with each branch  

The coordinates $\left(x_{\mathrm{d},1}, y_{\mathrm{d},1}\right)$ and $\left(x_{\mathrm{d},2}, y_{\mathrm{d},2}\right)$ define the locations at which the discharge control is applied or evaluated.

This structure makes it possible to represent a simple piecewise discharge relationship using two parameterized branches.

---

### Practical Meaning of the Parameters

- $k_1$ and $k_3$ control the magnitude of discharge response  
- $k_2$ and $k_4$ control the curvature or nonlinearity of the response  
- $h_{0,1}$ and $h_{0,2}$ define activation thresholds or reference depths  
- $x_{\mathrm{d},1}, y_{\mathrm{d},1}, x_{\mathrm{d},2}, y_{\mathrm{d},2}$ define where the controlled discharge is linked spatially  

Together, these parameters define how the internal structure converts water depth into flow.

---

### Practical Considerations

- control coordinates must be consistent with the DEM projection  
- the selected cells must coincide with valid hydraulic cells in the model domain  
- rating-curve coefficients must be physically realistic  
- excessively steep rating curves may create numerical instability  
- control structures should be tested carefully because they directly alter local mass fluxes  

---

### Summary

Internal boundary conditions in HydroPol2D are represented through a simple rating-curve framework that converts local water depth into discharge.

They are used to:

- impose controlled inlet or outlet fluxes  
- represent hydraulic control structures  
- modify the local inertial dynamics at specific cells  

Their correct parameterization is essential for stable and physically meaningful simulation of engineered hydraulic systems.

---

## Design Philosophy

HydroPol2D separates:

- **spatial inputs**, which define where each class occurs,
- **parameter tables**, which define how each class behaves.

This makes the model easier to maintain, easier to calibrate, and easier to apply across different domains.

---

## Summary

Parameter tables define how HydroPol2D translates categorical spatial data into physical behavior.

They are a central component of the model structure and must be carefully prepared to ensure consistent, stable, and physically meaningful simulations.