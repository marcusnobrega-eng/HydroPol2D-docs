---
title: Groundwater Model
---

# Groundwater Model

## 1. Overview

The groundwater component of HydroPol2D represents the coupled dynamics of:

- vadose-zone storage,
- recharge from infiltration,
- lateral saturated groundwater flow,
- groundwater exfiltration to the surface,
- and groundwater interaction with river cells.

The current implementation combines two complementary components:

1. a **recharge module**, which computes the flux from the vadose zone to groundwater using a reduced Richards-consistent Darcy closure based on the van Genuchten–Mualem constitutive relations, and

2. a **two-dimensional Boussinesq groundwater flow solver**, which routes saturated flow laterally across the domain and returns exfiltration to the land surface when the groundwater table rises above the local surface elevation.

This structure allows HydroPol2D to represent dynamic coupling between:

- surface water,
- vadose storage,
- groundwater recharge,
- saturated groundwater flow,
- and saturation-excess return flow.


<p align="center">
  <img src={require('../assets/figures/aquifer/aquifer_schematics.png').default} width="700" />
</p>

<p align="center">
  <em>Figure 1. Conceptual representation of the aquifer component in HydroPol2D.</em>
</p>

---

## 2. General Conceptual Structure

The groundwater model is solved after infiltration and vadose-zone update. Its logic is:

1. compute the water table position from the current groundwater head,
2. determine the maximum unsaturated storage permitted by the current water table depth,
3. compute recharge from the vadose zone to groundwater,
4. solve lateral groundwater flow using a 2D Boussinesq equation,
5. compute groundwater exfiltration to the surface,
6. correct vadose storage if the rising water table reduces the available unsaturated storage,
7. update surface water depth accordingly.

The principal variables are:

- $h$ = groundwater hydraulic head $[\mathrm{L}]$
- $z_0$ = aquifer base elevation or bedrock elevation $[\mathrm{L}]$
- $H = h - z_0$ = saturated thickness $[\mathrm{L}]$
- $R$ = recharge rate to groundwater $[\mathrm{L}\,\mathrm{T}^{-1}]$
- $q_{\mathrm{exf}}$ = exfiltration flux from groundwater to the surface $[\mathrm{L}\,\mathrm{T}^{-1}]$
- $S_y$ = specific yield $[-]$
- $K$ = saturated hydraulic conductivity $[\mathrm{L}\,\mathrm{T}^{-1}]$

---

## 3. Water Table Position and Unsaturated-Zone Capacity

HydroPol2D determines the position of the water table relative to the land surface using the current groundwater head.

Let:

- $z_{\mathrm{surf}}$ = land-surface elevation $[\mathrm{L}]$
- $D_{\mathrm{soil}}$ = soil depth $[\mathrm{L}]$
- $h$ = groundwater hydraulic head $[\mathrm{L}]$

The saturated thickness above the bedrock is computed as

$$
z_{\mathrm{gw}}
=
h - \left(z_{\mathrm{surf}} - D_{\mathrm{soil}}\right)
$$

The depth from the land surface to the water table is then

$$
z_{\mathrm{wt}}
=
D_{\mathrm{soil}} - z_{\mathrm{gw}}
$$

with the constraint

$$
z_{\mathrm{wt}} \ge 0
$$

where:

- $z_{\mathrm{gw}}$ = saturated thickness measured upward from the aquifer base $[\mathrm{L}]$
- $z_{\mathrm{wt}}$ = depth to water table below the ground surface $[\mathrm{L}]$

This variable is central to the coupling between vadose storage and groundwater.

### 3.1 Maximum unsaturated storage

The maximum water that can be stored in the unsaturated zone is defined as

$$
S_{\mathrm{UZ,max}}
=
z_{\mathrm{wt}}
\left(
\theta_{\mathrm{sat}} - \theta_i
\right)
$$

where:

- $S_{\mathrm{UZ,max}}$ = maximum unsaturated storage $[\mathrm{L}]$
- $\theta_{\mathrm{sat}}$ = saturated volumetric water content $[-]$
- $\theta_i$ = initial or reference volumetric water content $[-]$

Thus, as the water table rises, the vadose zone shrinks and the storage capacity available for infiltration decreases.

---

## 4. Recharge from the Vadose Zone

Recharge is computed using the function `simulate_groundwater_recharge`, which receives infiltration from the infiltration module and updates vadose-zone storage consistently.

### 4.1 Input infiltration

The infiltration module provides the infiltration flux:

$$
i
\quad [\mathrm{L}\,\mathrm{T}^{-1}]
$$

internally stored in HydroPol2D as `Hydro_States.f` in $\mathrm{mm/h}$. This is converted to groundwater-model units:

$$
i_{\mathrm{gw}} = \frac{i}{1000 \cdot 3600}
$$

where:

- $i_{\mathrm{gw}}$ = infiltration input to the recharge model $[\mathrm{m}\,\mathrm{s}^{-1}]$

### 4.2 Vadose storage state

Let:

- $S$ = current vadose-zone storage $[\mathrm{L}]$

The code converts the bucket storage from $\mathrm{mm}$ to $\mathrm{m}$ and uses this as the state variable for recharge.

### 4.3 Representative volumetric water content

The representative water content in the unsaturated zone is approximated as

$$
\theta
=
\theta_i + \frac{S}{z_{\mathrm{wt}}}
$$

bounded as

$$
\theta_i \le \theta \le \theta_{\mathrm{sat}}
$$

The effective saturation is then computed as

$$
S_e
=
\frac{
\theta - \theta_r
}{
\theta_{\mathrm{sat}} - \theta_r
}
$$

where:

- $\theta$ = representative volumetric water content $[-]$
- $\theta_r$ = residual water content $[-]$
- $S_e$ = effective saturation $[-]$

---

## 5. van Genuchten–Mualem Recharge Closure

The recharge model uses the same constitutive functions employed in the infiltration module.

### 5.1 Pressure head relation

The matric pressure head is computed as

$$
m = 1 - \frac{1}{n}
$$

$$
h(\theta)
=
-\frac{1}{\alpha_{\mathrm{vg}}}
\left(
S_e^{-1/m} - 1
\right)^{1/n}
$$

where:

- $h(\theta)$ = representative matric pressure head $[\mathrm{L}]$
- $\alpha_{\mathrm{vg}}$ = van Genuchten inverse air-entry parameter $[\mathrm{L}^{-1}]$
- $n$ = van Genuchten shape parameter $[-]$

At near saturation, HydroPol2D sets

$$
h(\theta) = 0
$$

to avoid numerical singularities.

### 5.2 Unsaturated hydraulic conductivity

The relative conductivity is

$$
K_r
=
S_e^{\ell}
\left[
1 - \left(1 - S_e^{1/m}\right)^m
\right]^2
$$

and the unsaturated conductivity becomes

$$
K(\theta) = K_{\mathrm{sat}} K_r
$$

where:

- $K(\theta)$ = unsaturated hydraulic conductivity $[\mathrm{L}\,\mathrm{T}^{-1}]$
- $K_{\mathrm{sat}}$ = saturated hydraulic conductivity $[\mathrm{L}\,\mathrm{T}^{-1}]$
- $\ell$ = pore-connectivity parameter $[-]$

If $\ell$ is not explicitly provided, HydroPol2D uses $\ell = 0.5$.

### 5.3 Recharge law

Recharge is then computed with a Darcy-like closure:

$$
R
=
K(\theta)
\left(
1 + \frac{h(\theta)}{L_{\mathrm{gw}}}
\right)
$$

where the effective drainage length is defined as

$$
L_{\mathrm{gw}} = 0.5\,z_{\mathrm{wt}}
$$

and:

- $R$ = recharge rate $[\mathrm{L}\,\mathrm{T}^{-1}]$
- $L_{\mathrm{gw}}$ = effective drainage length from the representative bucket state to the water table $[\mathrm{L}]$

The hydraulic gradient term is bounded in the code to avoid unrealistically large drainage or upward capillary-rise fluxes.

### 5.4 Vadose storage update

The vadose storage is updated as

$$
S^{t+\Delta t}
=
S^t + \Delta t \left(i_{\mathrm{gw}} - R\right)
$$

subject to the constraints

$$
S_{\min} \le S^{t+\Delta t} \le S_{\mathrm{UZ,max}}
$$

Recharge is then recomputed from exact mass conservation:

$$
R
=
i_{\mathrm{gw}} - \frac{S^{t+\Delta t} - S^t}{\Delta t}
$$

This guarantees that recharge is always fully consistent with the actual change in vadose storage.

---

## 6. Two-Dimensional Boussinesq Groundwater Flow Model

Once recharge has been computed, HydroPol2D routes groundwater laterally using the function `Boussinesq_2D_explicit`.

This solver represents the saturated groundwater system through a depth-integrated unconfined flow approximation.

### 6.1 Governing equation

The groundwater routing follows the 2D Boussinesq equation in conservative form:

$$
S_y \frac{\partial h}{\partial t}
=
- \nabla \cdot \mathbf{F}
+
R
$$

where:

- $S_y$ = specific yield $[-]$
- $h$ = groundwater hydraulic head $[\mathrm{L}]$
- $\mathbf{F}$ = groundwater flux vector $[\mathrm{L}^2\,\mathrm{T}^{-1}]$
- $R$ = recharge rate $[\mathrm{L}\,\mathrm{T}^{-1}]$

HydroPol2D evaluates this equation numerically by computing fluxes at cell interfaces and then updating the groundwater head explicitly.

### 6.2 Saturated thickness

The active saturated thickness is defined as

$$
H = \max(h - z_0, 0)
$$

where:

- $H$ = saturated thickness $[\mathrm{L}]$
- $z_0$ = aquifer base elevation or bedrock elevation $[\mathrm{L}]$

This enforces the physical condition that no saturated storage exists below the aquifer base.

### 6.3 Interface fluxes

HydroPol2D computes groundwater fluxes at cell interfaces using Darcy’s law with saturated thickness weighting.

For the $x$ direction:

$$
F_x = -K_x H_x \frac{\partial h}{\partial x}
$$

and for the $y$ direction:

$$
F_y = -K_y H_y \frac{\partial h}{\partial y}
$$

where:

- $F_x, F_y$ = fluxes per unit width $[\mathrm{L}^2\,\mathrm{T}^{-1}]$
- $K_x, K_y$ = hydraulic conductivity at cell interfaces $[\mathrm{L}\,\mathrm{T}^{-1}]$
- $H_x, H_y$ = interface saturated thicknesses $[\mathrm{L}]$

In the implementation, the interface hydraulic conductivity is taken as the arithmetic average of the conductivities in adjacent cells:

$$
K_x = \frac{K_i + K_{i+1}}{2}
\qquad
K_y = \frac{K_j + K_{j+1}}{2}
$$

and the interface saturated thickness is likewise averaged:

$$
H_x = \frac{H_i + H_{i+1}}{2}
\qquad
H_y = \frac{H_j + H_{j+1}}{2}
$$

### 6.4 Conservative flux limiting

To avoid numerical instability and nonphysical depletion of groundwater storage, HydroPol2D applies a flux limiter so that no cell can lose more water than it contains during a substep.

For example, in the $x$ direction, the maximum allowed flux is

$$
F_{x,\max}
=
\frac{S_y H_{\mathrm{donor}}}{\Delta t}
$$

and the final interface flux is limited as

$$
F_x \leftarrow \operatorname{sign}(F_x)\,
\min\left(|F_x|,\,F_{x,\max}\right)
$$

A similar expression is used in the $y$ direction.

This is an important feature of the HydroPol2D groundwater solver because it guarantees local mass admissibility during explicit integration.

### 6.5 Divergence of groundwater fluxes

The divergence of the flux field is then computed from the interface fluxes as

$$
\nabla \cdot \mathbf{F}
=
\frac{\partial F_x}{\partial x}
+
\frac{\partial F_y}{\partial y}
$$

using conservative finite differences on the raster grid.

### 6.6 Explicit predictor–corrector update

The Boussinesq solver uses an explicit predictor–corrector strategy.

#### Predictor step

A first estimate of head is computed using the current fluxes:

$$
h^{\ast}
=
h^t + \frac{\Delta t}{S_y}\left(-\nabla \cdot \mathbf{F}^t\right)
$$

#### Corrector step

Fluxes are recomputed from the predictor state, averaged, and used in the final update:

$$
h^{t+\Delta t}
=
h^t
+
\frac{\Delta t}{S_y}
\left(
-\nabla \cdot \mathbf{F}^{\mathrm{avg}} + R
\right)
$$

where:

- $h^{\ast}$ = predictor hydraulic head $[\mathrm{L}]$
- $h^{t+\Delta t}$ = final hydraulic head after the time step $[\mathrm{L}]$
- $\mathbf{F}^{\mathrm{avg}}$ = average of predictor and corrector interface fluxes

This predictor–corrector procedure improves stability and reduces numerical diffusion relative to a simple explicit Euler update.

---

## 7. Adaptive Time Stepping

The groundwater solver uses adaptive time stepping based on a Courant-type stability condition.

First, Darcy velocities are computed as

$$
u_x = -K_x \frac{\partial h}{\partial x}
\qquad
u_y = -K_y \frac{\partial h}{\partial y}
$$

where:

- $u_x, u_y$ = groundwater velocities $[\mathrm{L}\,\mathrm{T}^{-1}]$

The stable time step is then estimated as

$$
\Delta t_{\max}
=
\min\left(
\frac{\mathrm{Courant}\,\Delta x}{|u_x|},
\frac{\mathrm{Courant}\,\Delta y}{|u_y|}
\right)
$$

where:

- $\mathrm{Courant}$ = stability factor $[-]$
- $\Delta x, \Delta y$ = grid spacing $[\mathrm{L}]$

HydroPol2D then uses the minimum between the requested time step and the newly computed stable step. This ensures that the explicit Boussinesq solver remains stable even under rapidly changing groundwater gradients.

---

## 8. Boundary Conditions

The groundwater solver supports:

- Dirichlet boundary conditions,
- no-flow boundary conditions,
- domain masking.

### 8.1 Dirichlet boundaries

If a Dirichlet mask is provided, the head is prescribed directly:

$$
h = h_{\mathrm{D}}
$$

on the selected boundary cells, where:

- $h_{\mathrm{D}}$ = prescribed boundary head $[\mathrm{L}]$

### 8.2 No-flow boundaries

No-flow boundaries are enforced by zero-gradient conditions at the domain perimeter. In practice, HydroPol2D copies the head from the nearest valid interior neighbor to the perimeter cell, thereby enforcing a discrete Neumann condition.

### 8.3 Catchment mask

All groundwater calculations are restricted to the valid computational domain. Cells outside the catchment mask are set to `NaN`.

---

## 9. Groundwater Exfiltration to the Surface

After updating the groundwater head, HydroPol2D computes exfiltration where the groundwater table rises above the effective land surface.

The surface elevation used for exfiltration is

$$
h_{\mathrm{surf}} = z_0 + D_{\mathrm{soil}}
$$

where:

- $h_{\mathrm{surf}}$ = effective land-surface elevation for groundwater emergence $[\mathrm{L}]$

Exfiltration is then computed as

$$
q_{\mathrm{exf}}
=
\max\left(0,\,h - h_{\mathrm{surf}}\right)
\frac{S_y}{\Delta t}
$$

where:

- $q_{\mathrm{exf}}$ = exfiltration flux $[\mathrm{L}\,\mathrm{T}^{-1}]$

This expression means that if groundwater head exceeds the land surface, the excess saturated storage is expelled upward and transferred to the surface water system.

The groundwater head is then clipped so that

$$
h \le h_{\mathrm{surf}}
$$

which prevents groundwater from remaining above the land surface after exfiltration has been accounted for.

---

## 10. River–Aquifer Exchange

The current solver interface includes:

- a river mask,
- a river conductance term,
- river stage,
- river bed elevation,

which are designed to support river–aquifer exchange. In the current explicit implementation, the placeholder variable

$$
q_{\mathrm{river}}
$$

is initialized and carried through the coupling interface as the river-exchange term. This provides the structural basis for river–groundwater interaction within the HydroPol2D framework, even when the present version primarily emphasizes recharge, lateral groundwater flow, and exfiltration.

---

## 11. Saturation-Excess Correction After Water Table Rise

After the Boussinesq update, HydroPol2D recomputes the water-table depth and therefore the new maximum unsaturated storage:

$$
S_{\mathrm{UZ,max}}^{\,\mathrm{new}}
=
z_{\mathrm{wt}}^{\,\mathrm{new}}
\left(
\theta_{\mathrm{sat}} - \theta_i
\right)
$$

If the updated vadose storage exceeds this new capacity, the excess is returned to the surface as saturation-excess water:

$$
S_{\mathrm{excess}}
=
\max\left(
S - S_{\mathrm{UZ,max}}^{\,\mathrm{new}},
0
\right)
$$

The correction is then:

$$
S \leftarrow S - S_{\mathrm{excess}}
$$

and surface water depth is increased by

$$
h_{\mathrm{surf}}^{\,\mathrm{new}}
=
h_{\mathrm{surf}}^{\,\mathrm{old}}
+
S_{\mathrm{excess}}
$$

This is a very important part of HydroPol2D because it guarantees **mass consistency** between the vadose and saturated zones when the water table rises during a time step.

---

## 12. Coupling Back to Surface Water

The groundwater model feeds back to the surface water system in two ways:

1. **exfiltration**, through $q_{\mathrm{exf}}$,
2. **saturation excess**, through $S_{\mathrm{excess}}$.

The surface water depth is updated as

$$
d_t
=
d_t + \Delta t\,q_{\mathrm{exf}}
$$

with the appropriate unit conversion in the code from $\mathrm{m}$ to $\mathrm{mm}$.

This means that HydroPol2D allows groundwater to actively influence flood generation and near-surface wetness, rather than treating it as a disconnected lower boundary process.

---

## 13. Mass Balance

The groundwater solver performs an explicit mass-balance check during each update.

The recharge input volume is

$$
V_{\mathrm{recharge}}
=
\sum R\,\Delta t\,A_{\mathrm{cell}}
$$

The exfiltration loss volume is

$$
V_{\mathrm{exf}}
=
\sum q_{\mathrm{exf}}\,\Delta t\,A_{\mathrm{cell}}
$$

The groundwater storage change is

$$
\Delta V_{\mathrm{storage}}
=
\sum S_y\,\max(h^{t+\Delta t}-z_0,0)\,A_{\mathrm{cell}}
-
\sum S_y\,\max(h^t-z_0,0)\,A_{\mathrm{cell}}
$$

The mass-balance residual is then

$$
\varepsilon_{\mathrm{gw}}
=
V_{\mathrm{recharge}}
-
V_{\mathrm{exf}}
-
\Delta V_{\mathrm{storage}}
$$

where:

- $\varepsilon_{\mathrm{gw}}$ = groundwater mass-balance error $[\mathrm{L}^3]$

This quantity is stored as a groundwater diagnostic error in HydroPol2D.

---

## 14. Summary

The HydroPol2D groundwater model combines:

- a **vadose-zone recharge module** based on a Darcy–van Genuchten–Mualem closure,
- a **2D Boussinesq groundwater flow model** for lateral saturated flow,
- **adaptive explicit time stepping**,
- **surface exfiltration** when groundwater rises above the ground surface,
- and a **saturation-excess correction** that preserves mass when the water table reduces vadose storage capacity.

This structure allows HydroPol2D to represent a dynamically coupled subsurface system in which:

- infiltration does not simply disappear into a static bucket,
- recharge affects groundwater head,
- groundwater flow redistributes water laterally,
- and groundwater can return to the land surface and influence overland flow generation.

The result is a groundwater model that is physically interpretable, mass conservative, and fully integrated with the hydrologic and hydrodynamic architecture of HydroPol2D.