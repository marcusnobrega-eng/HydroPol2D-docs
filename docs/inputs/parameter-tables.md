---
title: Parameter Tables
---

# Parameter Tables

HydroPol2D uses parameter tables to assign physical properties to categorical raster inputs.

Categorical maps such as LULC and Soil are not used directly in the governing equations. Instead, each class acts as an index into a parameter table, where the corresponding physical parameters are defined.

This structure separates spatial information from parameter definition and makes the model easier to calibrate, adapt, and interpret.

---

## Where the Tables Live {#where-the-tables-live}

In MATLAB Excel mode the class tables are tabs of the case workbook `HydroPol2D_Inputs.xlsx`. Each tab is a cell-for-cell copy of the workbook it replaces, because the model reads some columns by position. Keep the rows and the column order; add a class as a new row.

| Tab | Was | Read when |
|---|---|---|
| Soil classes | `SOIL_parameters.xlsx` | always |
| Land use classes | `LULC_parameters.xlsx` | always (read from row 2 by position) |
| Human instability | `human_risk.xlsx` | `flag_human_instability = 1` or `3` |
| Mesh | `Voronoi_Settings.xlsx` | `flag_voronoi = 1` |
| Control structures | `BC_Control_structure.xlsx` | `flag_reservoir = 1` |

In the older layout the same tables are the separate workbooks of the second column, in the folder of `General_Data.xlsx`. The model reads the tab when the case workbook has it, and the older workbook otherwise. HydroPol2D-Python reads the same class properties from the Case Builder contract.

---

## General Structure

Each parameter table contains:

- a **class identifier** (`Index`)
- a set of **parameters associated with that class**

At runtime, HydroPol2D:

1. reads the raster value at each grid cell,
2. uses that value as an index,
3. assigns the corresponding parameters from the table.

For mapped classes, raster values and table indices must match exactly. When a valid LULC, soil, or snow code is absent from its parameter table, HydroPol2D assigns the area-weighted mean of properties represented by mapped cells and writes the decision to `Input_Class_Code_Audit.csv`. Duplicate indices, non-numeric indices, or a table with no mapped classes remain input errors.

---

## LULC Parameter Table

The LULC table defines surface-related properties controlling flow resistance, interception, imperviousness, pollutant-related behavior, and root-zone depth when layered soil storage is active.

### Example structure

| Land Cover | Index | $n$<br />$(\mathrm{s\,m^{-1/3}})$ | $h_0$<br />$(\mathrm{mm})$ | $d_0$<br />$(\mathrm{mm})$ | $C_1$ | $C_2$ | $C_3$ | $C_4$ | $\mathrm{index\_impervious}$ | $\mathrm{root\_depth\_m}$ |
|:----------:|:-----:|:---------------------------------:|:--------------------------:|:--------------------------:|:-----:|:-----:|:-----:|:-----:|:----------------------------:|:--------------------------:|
| Tree cover | 10 | 0.10 | 0 | 0 | 10 | 0.20 | 800 | 1.20 | 50 | 1.50 |
| Shrubland | 20 | 0.08 | 0 | 0 | 12 | 0.20 | 900 | 1.20 | NaN | 1.00 |
| Grassland | 30 | 0.06 | 0 | 0 | 15 | 0.22 | 1000 | 1.20 | NaN | 0.60 |
| Cropland | 40 | 0.05 | 0 | 0 | 30 | 0.25 | 1400 | 1.30 | NaN | 1.00 |
| Built-up | 50 | 0.03 | 0 | 0 | 80 | 0.30 | 2000 | 1.30 | NaN | 0.00 |
| Bare / sparse vegetation | 60 | 0.035 | 0 | 0 | 45 | 0.25 | 1600 | 1.25 | NaN | 0.10 |
| Snow and ice | 70 | 0.02 | 0 | 0 | 1 | 0.10 | 200 | 1.10 | NaN | 0.00 |
| Permanent water bodies | 80 | 0.035 | 0 | 0 | 0 | 0 | 0 | 0 | NaN | 0.00 |
| Herbaceous wetland | 90 | 0.12 | 0 | 0 | 8 | 0.18 | 700 | 1.20 | NaN | 0.40 |
| Mangroves | 95 | 0.15 | 0 | 0 | 8 | 0.18 | 700 | 1.20 | NaN | 1.00 |
| Moss and lichen | 100 | 0.08 | 0 | 0 | 5 | 0.15 | 500 | 1.15 | NaN | 0.15 |

*Table 1. HydroPol2D LULC parameter table. The `Index` values must match the categorical values in the LULC raster.*

### Variable definitions

- $n$: Manning’s roughness coefficient
- $h_0$: interception parameter
- $d_0$: initial surface storage parameter
- $C_1$–$C_4$: coefficients associated with the pollutant build-up and wash-off formulation
- $\mathrm{index\_impervious}$: identifier used to associate a class with impervious behavior
- $\mathrm{root\_depth\_m}$: vegetation-controlled root-zone depth used by the layered soil/vadose model

The values shown above correspond to the current HydroPol2D parameter table and should be revised as needed for the adopted classification scheme and study area.

In the current implementation, `root_depth_m` is the supported way to provide root-depth input to the model. There is no separate root-depth raster path; root depth is assigned per LULC class and then mapped to the grid through the categorical LULC raster.

---

## Snow Parameter Table

The LULC parameter table contains the following snow columns in every `LULC_Index` row. There is no separate snow workbook; this keeps every land-cover-dependent property in one class record.

| Column | Units | Description |
|---|---|---|
| `LULC_Index` | — | LULC code to which the row applies. |
| `Snow_Albedo` | — | Shortwave albedo of the snow surface. |
| `Snow_Emissivity` | — | Longwave emissivity used in the net-radiation calculation. |
| `Sublimation_Coefficient_d_1` | day⁻¹ (m s⁻¹)⁻¹ | Coefficient in the timestep-scaled sublimation term. |
| `Degree_Day_Factor_mm_C_day` | mm °C⁻¹ day⁻¹ | Degree-day melt factor. |
| `T_Snow_All_C` | °C | Temperature at or below which all precipitation is snow. |
| `T_Rain_All_C` | °C | Temperature at or above which all precipitation is rain. It must be no lower than `T_Snow_All_C`. |
| `Rho_Snow_Init_kg_m3` | kg m⁻³ | Fresh-snow density used for zero-snow and single-raster initialization. |
| `Rho_Snow_Max_kg_m3` | kg m⁻³ | Upper bound on snow density after compaction. |
| `Compaction_Temperature_kg_m3_C_day` | kg m⁻³ °C⁻¹ day⁻¹ | Temperature-dependent density increase. |
| `Compaction_SWE_kg_m3_mm_day` | kg m⁻³ mm⁻¹ day⁻¹ | SWE-dependent density increase. |
| `Compaction_Depth_kg_m3_mm_day` | kg m⁻³ mm⁻¹ day⁻¹ | Snow-depth-dependent density increase. |

The degree-day, sublimation, and compaction terms are rates. HydroPol2D multiplies them by the current routing timestep. Snow requires the internal meteorological forcing mode, so the model can obtain mean temperature, minimum temperature, and wind speed.

---

## Soil Parameter Table

The soil table defines the base hydraulic properties used to estimate infiltration, layered vadose storage, recharge, and groundwater behavior.

### Example structure

| Soil Type | Index | $K_{\mathrm{sat}}$<br />$(\mathrm{mm\,h^{-1}})$ | $n$ | $\alpha$<br />$(\mathrm{m^{-1}})$ | $\theta_{\mathrm{sat}}$ | $\theta_{\mathrm{r}}$ | $\theta_{\mathrm{i}}$ | $S_{\mathrm{y}}$ | $K_{\mathrm{g,sat}}$<br />$(\mathrm{mm\,h^{-1}})$ | $\mathrm{DTB}$<br />$(\mathrm{m})$ | $K_s$ near | $K_s$ root | $K_s$ transmission |
|:---------:|:-----:|:-----------------------------------------------:|:---:|:----------------------------------:|:----------------------:|:--------------------:|:--------------------:|:---------------:|:---------------------------------------------------:|:--------------------------------:|:------------:|:----------:|:--------------------:|
| Clay | 1 | 0.3 | 1.09 | 0.8 | 0.385 | 0.068 | 0.0997 | 0.03 | 6 | 1 | 1 | 1 | 1 |
| Silty Clay | 2 | 0.5 | 1.09 | 0.5 | 0.423 | 0.070 | 0.1053 | 0.04 | 10 | 1 | 1 | 1 | 1 |
| Sandy Clay | 3 | 0.6 | 1.23 | 2.7 | 0.321 | 0.100 | 0.1221 | 0.06 | 12 | 1 | 1 | 1 | 1 |
| Clay Loam | 4 | 1.0 | 1.31 | 1.9 | 0.309 | 0.095 | 0.1164 | 0.08 | 20 | 1 | 1 | 1 | 1 |
| Silty Clay Loam | 5 | 1.0 | 1.23 | 1.0 | 0.432 | 0.089 | 0.1233 | 0.09 | 20 | 1 | 1 | 1 | 1 |
| Sandy Clay Loam | 6 | 1.5 | 1.48 | 5.9 | 0.330 | 0.100 | 0.1230 | 0.11 | 30 | 1 | 1 | 1 | 1 |
| Loam | 7 | 3.4 | 1.56 | 3.6 | 0.434 | 0.078 | 0.1136 | 0.18 | 68 | 1 | 1 | 1 | 1 |
| Silty Loam | 8 | 6.5 | 1.41 | 2.0 | 0.486 | 0.067 | 0.1298 | 0.14 | 130 | 1 | 1 | 1 | 1 |
| Sandy Loam | 9 | 10.9 | 1.89 | 7.5 | 0.412 | 0.065 | 0.0997 | 0.22 | 218 | 1 | 1 | 1 | 1 |
| Silt | 10 | 2.5 | 1.37 | 1.6 | 0.460 | 0.034 | 0.1192 | 0.12 | 50 | 1 | 1 | 1 | 1 |
| Loamy Sand | 11 | 29.9 | 2.28 | 12.4 | 0.401 | 0.057 | 0.1258 | 0.25 | 598 | 1 | 1 | 1 | 1 |
| Sand | 12 | 117.8 | 2.68 | 14.5 | 0.417 | 0.045 | 0.1194 | 0.30 | 2356 | 1 | 1 | 1 | 1 |
| Water | 0 | 0.3 | 1.09 | 0.8 | 0.385 | 0.068 | 0.0997 | 0.03 | 6 | 1 | 1 | 1 | 1 |

*Table 2. HydroPol2D soil parameter table. The `Index` values must match the categorical values in the soil raster; the default codes follow the OpenLandMap USDA texture legend (7 loam, 8 silt loam). $K_{\mathrm{sat}}$ and $\theta_{\mathrm{sat}}$ are the Green–Ampt conductivity and effective porosity of [Rawls et al. (1983)](https://doi.org/10.1061/%28ASCE%290733-9429%281983%29109%3A1%2862%29); $n$, $\alpha$ and $\theta_{\mathrm{r}}$ are the class means of [Carsel and Parrish (1988)](https://doi.org/10.1029/WR024i005p00755). Silt, which Rawls et al. do not list, takes $K_{\mathrm{sat}}$ and $\theta_{\mathrm{sat}}$ from Carsel and Parrish. $\theta_{\mathrm{i}} = \theta_{\mathrm{r}} + S_e(\theta_{\mathrm{sat}} - \theta_{\mathrm{r}})$ with $S_e = 0.1$ (0.15 for silt loam; 0.2 for silt, loamy sand and sand), and $K_{\mathrm{g,sat}} = 20\,K_{\mathrm{sat}}$.*

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
- `Ks_multiplier_near_surface`: multiplier applied to base $K_{\mathrm{sat}}$ in the near-surface layer
- `Ks_multiplier_root_zone`: multiplier applied to base $K_{\mathrm{sat}}$ in the root-zone layer
- `Ks_multiplier_transmission`: multiplier applied to base $K_{\mathrm{sat}}$ in the transmission layer

The categorical soil class defines the base hydraulic properties for the column. The layered implementation assigns those properties to the near-surface, root-zone, and transmission-zone layers, then applies optional conductivity multipliers where they are provided.

LULC controls root-zone depth. Depth to bedrock and the current water-table position constrain the final layer thicknesses, so physically impossible layer geometries collapse or truncate rather than producing negative storage.

The values shown above correspond to the current HydroPol2D soil parameter table and should be revised as needed for the adopted soil classification and simulation scenario.

---

## DTB Assignment Through the Soil Table

The `DTB (m)` column gives a depth to bedrock per soil class. When it is read depends on the subsurface scheme:

| Scheme | Role of `DTB (m)` |
|---|---|
| [Layered subsurface](../theory/layered-subsurface) | Bottom of the column where `DTB_path` and `subsurface_depth_to_bedrock_m` are both empty (MATLAB since 2026-10-20; HydroPol2D-Python reads its soil table the same way) |
| Default groundwater scheme (MATLAB) | Not read. `DTB_path` is required; without groundwater an empty `DTB_path` gives a 1 m soil depth |

Each soil class then carries a representative depth, and the column bottom follows the soil map. This is useful in data-scarce applications.



---

## Consistency Requirements

The following conditions must be satisfied:

- mapped raster class values must be represented by the corresponding table,
- class identifiers must not be duplicated,
- parameter fields must not be left empty,
- units must be consistent with the model formulation.

For an unmapped valid class, the model uses the documented area-weighted fallback and writes `Input_Class_Code_Audit.csv`. Review that file before accepting a run. A table without any class shared with its raster cannot define a meaningful fallback and stops preprocessing.

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

Internal boundary conditions are defined in the Control structures tab of the case workbook (`BC_Control_structure.xlsx` in the older layout), read when `flag_reservoir = 1`. Each row is one structure. The outflow is $Q = k_1 (h - h_{0,1})^{k_2}$ to the cell $(x_{d,1}, y_{d,1})$ and $Q = k_3 (h - h_{0,2})^{k_4}$ to the cell $(x_{d,2}, y_{d,2})$, with coordinates in the DEM projection.

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

The coordinates $\left(x_{\mathrm{d},1}, y_{\mathrm{d},1}\right)$ and $\left(x_{\mathrm{d},2}, y_{\mathrm{d},2}\right)$ are the cells that receive each branch's release. The release leaves the control cell and enters that cell, so the transfer conserves mass. Each release is capped at the water above its threshold, and the second branch uses the depth left after the first. A destination of $(0, 0)$ sends the release out of the model, and it is counted as outlet flow. An empty destination switches that branch off.

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
