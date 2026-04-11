---
title: DTB
---

# Depth to Bedrock (DTB)

The Depth to Bedrock (DTB) defines the vertical extent of the soil column available for water storage in HydroPol2D.

It represents the distance between the land surface and a limiting layer that constrains vertical water movement. This layer may correspond to actual bedrock or to an effective boundary such as the top of a shallow aquifer.

---

## Role in HydroPol2D

DTB is used to define:

- Maximum subsurface storage capacity  
- Vertical limit for infiltration and percolation  
- Effective thickness of the vadose zone  
- Onset of saturation within the soil column  

Within the model, DTB acts as a **geometric constraint** on storage rather than a fully resolved vertical profile.

---

## Representation

DTB is provided as a **continuous raster map**, where each cell contains a depth value (in meters).

This allows spatial variability in storage capacity across the domain.

- Shallow DTB → rapid saturation and runoff generation  
- Deep DTB → larger storage and delayed hydrological response  

---

## Alternative Definition: Depth to Aquifer

In many applications, the objective is not to explicitly resolve groundwater dynamics but to constrain the depth of the vadose zone.

In this case, DTB can be interpreted as the **depth to the aquifer surface**, rather than the depth to the impermeable bedrock.

Under this assumption:

- The vadose zone is limited to the depth between the surface and the aquifer  
- Storage is constrained by available unsaturated soil volume  
- No explicit representation of the saturated aquifer is required  

This approach is appropriate when:

- Groundwater processes are not explicitly modeled  
- The focus is on surface and near-surface hydrological response  
- A realistic upper bound for soil storage is needed  

---

## Default Assignment from Soil Classes

If a DTB map is not available, values can be assigned through the **soil parameter tables**.

In this case:

- Each soil class is associated with a representative DTB value  
- The DTB field is constructed implicitly from the soil classification  

This approach ensures consistency between:

- Soil hydraulic properties  
- Available storage depth  

It is particularly useful in data-scarce environments.

---

## Units and Requirements

The DTB input must:

- Be expressed in **meters**  
- Use a **projected CRS** consistent with all other rasters  
- Align spatially with the DEM and other inputs  

Values must remain within physically realistic ranges for the study area.

---

## Data Sources

DTB data is not as widely standardized as DEM or LULC, but can be derived from:

### SoilGrids (Depth to Bedrock)
- Region: Global  
- Provides estimates of depth to bedrock  
- Download: https://soilgrids.org/

---

### Regional Geological Surveys
- National or regional datasets may provide higher-quality estimates  
- Often derived from geological mapping or subsurface models  

---

### Derived or Assumed Values
- DTB can be approximated based on soil type or geological context  
- Constant values may be used when spatial variability is unknown  

---

## Interaction with Soil Properties

DTB complements the soil parameterization:

- Soil parameters control infiltration behavior  
- DTB limits the total volume available for storage  

This combination determines the effective response of the system without requiring explicit vertical discretization.

---

## Practical Considerations

When defining DTB:

- Avoid unrealistically large values  
- Maintain consistency with soil classification  
- Ensure spatial coherence  
- Use simplified assumptions when necessary, but document them  

DTB is often uncertain and should be evaluated as part of sensitivity analysis when possible.

---

## Summary

DTB defines the effective vertical storage available to the model and constrains the depth of the vadose zone.

It can represent either the depth to bedrock or the depth to the aquifer surface, depending on the modeling objective.

Even though it is simple in form, it plays a central role in controlling runoff generation and storage capacity in HydroPol2D.