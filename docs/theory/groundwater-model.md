---
title: Groundwater Model
---
import useBaseUrl from '@docusaurus/useBaseUrl';

# Groundwater Model

## 1. Overview

The groundwater component of HydroPol2D represents the coupled dynamics of:

- vadose-zone storage,
- recharge from infiltration,
- lateral saturated groundwater flow,
- groundwater exfiltration to the surface,
- and groundwater interaction with river cells.

The current implementation combines three complementary components:

1. a **layered vadose/recharge module**, which moves water through near-surface, root-zone, and transmission-zone storage using a reduced Richards-consistent Darcy closure based on the van Genuchten–Mualem constitutive relations,

2. a **capillary-rise exchange module**, which can move water upward from shallow groundwater into available vadose storage, and

3. a **two-dimensional Boussinesq groundwater flow solver**, which routes saturated flow laterally across the domain and returns exfiltration to the land surface when the groundwater table rises above the local surface elevation.

This structure allows HydroPol2D to represent dynamic coupling between:

- surface water,
- vadose storage,
- groundwater recharge,
- saturated groundwater flow,
- and saturation-excess return flow.


<p align="center">
  <img src={useBaseUrl('/img/theory/groundwater-model.svg')} width="720" alt="Three stepped cells from a hillside to a river, with soil layers, water table, lateral flow, exfiltration, river exchange and a deep aquifer" />
</p>

<p align="center">
  <em>Figure 1. The default groundwater scheme on three model cells. Recharge and capillary rise move the water table h every surface step. Lateral Boussinesq flow runs on the groundwater clock. Exfiltration and saturation excess return water where h reaches the ground.</em>
</p>

### 1.1 Two subsurface schemes

HydroPol2D has two subsurface schemes. This page describes the default one.

| Scheme | Aquifer | Switch | Page |
|---|---|---|---|
| Default | Inside the soil column; the aquifer base is the ground minus the soil depth | default | this page |
| Layered | Soil slots over regolith slots, down to the depth to bedrock (capped at 50 m) | Python `vertical.subsurface.scheme: layered`; MATLAB `flag_layered_subsurface = 1` | [Layered Subsurface](./layered-subsurface) |

Both schemes can feed the optional deep aquifer described in [Section 13](#13-deep-aquifer).

On this page, "layered vadose" means the three soil stores of the default scheme (near surface, root zone, transmission). It is not the layered subsurface scheme.

---

## 2. General Conceptual Structure

The groundwater model is coupled with two clocks. Vadose-zone exchange is evaluated every surface-water time step because infiltration and evapotranspiration need fast soil-moisture feedback. This net exchange changes the water-table heads in every surface-water step. The groundwater scheduler is always asynchronous, and only the lateral groundwater flow, when it is on, waits for it. The lateral update usually runs on a daily target interval unless stability or head-change limits require a shorter one.

The logic is:

1. compute the water table position from the current groundwater head,
2. determine the maximum unsaturated storage permitted by the current water table depth,
3. compute drainage/recharge from vadose layers to groundwater during the current surface step,
4. compute capillary rise from groundwater to the vadose layers when enabled,
5. change the water-table heads by the net exchange in every surface-water step,
6. compute groundwater exfiltration to the surface where the head rises above the land surface,
7. solve lateral groundwater flow using a 2D Boussinesq equation when lateral flow is on (`flag_baseflow = 1` in MATLAB, `vertical.groundwater_lateral_flow: true` in HydroPol2D-Python) and the scheduler is due,
8. add the exfiltration of the lateral update to the surface,
9. correct vadose storage if the rising water table reduces the available unsaturated storage,
10. update surface water depth accordingly.

The principal variables are:

- $h$ = groundwater hydraulic head $[\mathrm{L}]$
- $z_0$ = aquifer base elevation or bedrock elevation $[\mathrm{L}]$
- $H = h - z_0$ = saturated thickness $[\mathrm{L}]$
- $R$ = recharge rate to groundwater $[\mathrm{L}\,\mathrm{T}^{-1}]$
- $q_{\mathrm{exf}}$ = exfiltration flux from groundwater to the surface $[\mathrm{L}\,\mathrm{T}^{-1}]$
- $S_y$ = specific yield $[-]$
- $K$ = saturated hydraulic conductivity $[\mathrm{L}\,\mathrm{T}^{-1}]$

### 2.1 Asynchronous scheduler

The asynchronous scheduler is always active when groundwater modeling is enabled. It decides only when the lateral Boussinesq update runs. The principal controls are:

| Control | Default | Meaning |
|---|---:|---|
| `flag_groundwater_async` | 1 | Not read: the lateral update always follows the scheduler (Section 7.1). |
| `groundwater_target_dt_s` | 86400 | Longest interval between lateral updates, in seconds (one day). HydroPol2D-Python also reads it from a legacy workbook in minutes, as `groundwater_target_dt_min` (1440). |
| `groundwater_min_dt_s` | 60 | Shortest interval between lateral updates and smallest Boussinesq substep, in seconds. The legacy workbook key is `groundwater_min_dt_min` (1). |
| `groundwater_max_head_change_m` | 0.25 | HydroPol2D-Python: forces a lateral update when the water table has moved by this amount since the last one. The MATLAB default scheme does not use it (Section 7.1). |
| `groundwater_head_tolerance_m` | 0.001 | Absolute head tolerance of the adaptive Boussinesq substeps, in metres. MATLAB also uses it in the head-change trigger. |
| `groundwater_relative_tolerance` | 0.001 | Relative tolerance on the saturated thickness, used together with `groundwater_head_tolerance_m`. |
| `groundwater_courant` | 0.25 | Stability factor for the Boussinesq groundwater timestep estimate. |
| `flag_capillary_rise` | 1 | Enables capillary rise from the water table into the root zone when layered soil storage is present. |

In HydroPol2D-Python these settings sit in the `vertical` block, and capillary rise is `vertical.capillary_rise` (default true).

The scheduler keeps the time since the last lateral update, the substep suggested by the last adaptive Boussinesq run, the number of lateral updates, and three depths per cell. The pending net exchange holds the exchange of the current step only. The local update adds it to the heads and sets it to zero in the same step. The pending recharge and the pending capillary rise are running totals since the last lateral update and are cleared when that update runs. For the head-change trigger, HydroPol2D-Python also keeps the head change applied since the last lateral update, and the MATLAB code keeps the head of that update. The Boussinesq solver receives no recharge term, because the heads already include the net exchange. Without lateral flow, the scheduler only clears these totals, in every step in MATLAB and when the trigger is due in HydroPol2D-Python.

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

The maximum water that can be stored in the unsaturated zone is defined using the current **active storage above residual water content** convention:

$$
S_{\mathrm{UZ,max}}
=
z_{\mathrm{wt}}
\left(
\theta_{\mathrm{sat}} - \theta_r
\right)
$$

where:

- $S_{\mathrm{UZ,max}}$ = maximum unsaturated storage $[\mathrm{L}]$
- $\theta_{\mathrm{sat}}$ = saturated volumetric water content $[-]$
- $\theta_r$ = residual volumetric water content $[-]$

Thus, as the water table rises, the vadose zone shrinks and the storage capacity available for infiltration decreases. When layered soil storage is active, the code evaluates this limit through the explicit capacities of the near-surface, root-zone, and transmission-zone stores after truncation by the current water-table position.

---

## 4. Default Layered Vadose-to-Groundwater Exchange

Recharge is computed from the current vadose storage after the infiltration module has already moved water from the surface into the soil. This avoids double-counting infiltration. The current default pathway is layered:

- near-surface storage,
- root-zone storage,
- transmission-zone storage,
- groundwater recharge.

### 4.1 Surface-step coupling

Vadose exchange is evaluated every surface-water step because infiltration and evapotranspiration need immediate soil-moisture feedback. In the current implementation, infiltration is first accepted by the infiltration module, stored in the vadose layers, and only then allowed to drain downward toward groundwater.

### 4.2 Layerwise constitutive state

For a generic vadose layer $\ell$ with active storage $S_{\ell}$ and thickness $z_{\ell}$, HydroPol2D evaluates

$$
\theta_{\ell}
=
\theta_{\mathrm{r},\ell}
+
\frac{S_{\ell}}{f_p\, z_{\ell}}
$$

$$
S_{e,\ell}
=
\frac{
\theta_{\ell} - \theta_{\mathrm{r},\ell}
}{
\theta_{\mathrm{sat},\ell} - \theta_{\mathrm{r},\ell}
}
$$

$$
K_{\ell}
=
K_{\mathrm{sat},\ell}
S_{e,\ell}^{\ell_v}
\left[
1 - \left(1 - S_{e,\ell}^{1/m_{\ell}}\right)^{m_{\ell}}
\right]^2
$$

with

$$
m_{\ell} = 1 - \frac{1}{n_{\ell}}
$$

where:

- $\theta_{\ell}$ = layer water content $[-]$
- $f_p$ = pervious fraction of the cell $[-]$; the layer water sits in the pervious part, and $S_{\ell}$ is a depth over the whole cell
- $S_{e,\ell}$ = layer effective saturation $[-]$
- $K_{\ell}$ = layer unsaturated conductivity $[\mathrm{L}\,\mathrm{T}^{-1}]$
- $\ell_v$ = Mualem pore-connectivity parameter $[-]$, fixed at 0.5 in this drainage step in both codes

This is the same van Genuchten-Mualem constitutive family used by the infiltration module.

### 4.3 Downward drainage cascade

The layered recharge pathway is computed as a downward cascade:

1. near-surface drainage goes to the root zone when root storage exists,
2. root-zone drainage goes to the transmission zone when transmission storage exists,
3. transmission-zone drainage becomes groundwater recharge.

Conceptually, the drainage depth from a layer over a time step can be summarized as

$$
\Delta D_{\ell} \approx f_p\,K_{\ell}\,\Delta t
$$

subject to:

- water available in the donor layer,
- remaining capacity in the receiving layer,
- and the current layer thickness and soil parameters.

The net downward recharge reaching groundwater is then

$$
R_{\mathrm{down}}
=
\frac{\Delta S_{\rightarrow \mathrm{gw}}}{\Delta t}
$$

where $\Delta S_{\rightarrow \mathrm{gw}}$ is the total transmission of water into groundwater during the current surface step. Direct drainage from the near-surface or root zone to groundwater occurs only when the lower vadose layers are absent.

### 4.4 Legacy fallback formulation

The MATLAB code still contains the older representative-bucket recharge closure for cases where the explicit layered storage data are unavailable. In that fallback mode, a single vadose storage state is converted to a representative water content and drained with a Darcy-like closure. HydroPol2D-Python has no such fallback and always uses the three layers. That formulation should be treated as **legacy/fallback**, not the primary theory path for the current model.

---

## 5. Optional Capillary Rise

When `flag_capillary_rise = 1`, HydroPol2D allows shallow groundwater to move upward into available vadose storage. The current implementation is a storage-limited van Genuchten-Mualem transfer into the root zone, not a full Richards-equation solution.

The upward exchange increases with:

- shallower water-table depth,
- larger storage deficit in the receiving layer,
- and larger saturated conductivity of the root zone.

Over a surface step $\Delta t$, the upward capillary transfer is

$$
C_{\mathrm{up}}\,\Delta t
=
\min\!\left(
S_{\mathrm{def}},\;
K_{\mathrm{sat,root}}\,K_r(g)\,\Delta t,\;
S_{\mathrm{gw}}
\right)
$$

with $g = \max(z_{\mathrm{wt}} - z_{\mathrm{root}}, 0)$, $S_e(g) = \left[1 + (\alpha g)^{n}\right]^{-m}$ and $K_r(g) = S_e(g)^{\ell_v}\left[1 - \left(1 - S_e(g)^{1/m}\right)^{m}\right]^2$, where:

- $S_{\mathrm{def}}$ is the deficit of the receiving layer below field capacity, $\max\!\left(S_e(h_{\mathrm{fc}})\,S_{\max} - S, 0\right)$, with $S$ and $S_{\max}$ the storage and capacity of that layer
- $h_{\mathrm{fc}}$ is the field-capacity suction head, `capillary_field_capacity_head_m` (default 3.3 m)
- $g$ is the gap between the water table and the bottom of the root zone $z_{\mathrm{root}}$
- $S_{\mathrm{gw}} = S_y\,(h - z_0)$ is the groundwater stored in the cell
- $\alpha$, $n$, $m$ and $\ell_v$ are the van Genuchten-Mualem parameters of the soil

In the current code, capillary rise fills only the root zone, or the near-surface layer where the roots end inside it and there is no separate root zone. The transmission zone receives no capillary rise.

The net vadose-groundwater exchange of each surface-water step is therefore

$$
R_{\mathrm{net}} = R_{\mathrm{down}} - C_{\mathrm{up}}
$$

where $C_{\mathrm{up}}$ is the total upward capillary-rise flux.

---

## 6. Two-Dimensional Boussinesq Groundwater Flow Model

After the local head update, and only when lateral flow is on and the scheduler is due, HydroPol2D routes groundwater laterally using the function `Boussinesq_2D_explicit`. HydroPol2D-Python uses the same discretization.

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

HydroPol2D evaluates this equation numerically by computing fluxes at cell interfaces and then updating the groundwater head explicitly. In the code the recharge term is applied separately. The net exchange changes the heads in every surface-water step (Section 7.1), and the lateral solver is called with $R = 0$ over the time elapsed since its last run.

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

To avoid numerical instability and nonphysical depletion of groundwater storage, HydroPol2D applies a flux limiter so that no interface can carry more water than its donor cell holds during a substep.

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

Because the limit applies to each interface separately, a cell that drains through several interfaces can still fall below the aquifer base in one substep. The solver then sets the head to $z_0$, and the added water shows up as a residual in the mass-balance check of Section 14.

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

## 7. Groundwater Update Timing and Adaptive Time Stepping

HydroPol2D uses a **two-level groundwater time-step logic**.

### 7.1 Outer asynchronous scheduler

Vadose exchange changes the water-table heads in every surface-water step. The groundwater scheduler is always asynchronous, and only the lateral groundwater flow, when it is on, waits for it. The lateral update runs at the end of the first surface step in which one of these conditions holds:

- the time since the last lateral update reaches $\max\!\left(\min(\Delta t_{\mathrm{target}}, \Delta t_{\mathrm{gw,stable}}, \Delta t_{\mathrm{sugg}}), \Delta t_{\min}\right)$, where $\Delta t_{\mathrm{target}}$ is `groundwater_target_dt_s`, $\Delta t_{\mathrm{gw,stable}}$ is the stability cap of Section 7.2, $\Delta t_{\mathrm{sugg}}$ is the substep suggested by the last adaptive Boussinesq run, and $\Delta t_{\min}$ is `groundwater_min_dt_s`,
- the water table has moved far enough since the last lateral update,
- the surface step is the last one of the run.

The head-change test differs between the codes. HydroPol2D-Python compares the largest head change applied since the last lateral update with `groundwater_max_head_change_m` (0.25 m). The MATLAB default scheme does not use that setting. It runs the update when, in any cell, $|h - h_{\mathrm{last}}| \ge \delta_h + \delta_r H$, where $h_{\mathrm{last}}$ is the head after the last lateral update, $\delta_h$ is `groundwater_head_tolerance_m` and $\delta_r$ is `groundwater_relative_tolerance` (both 0.001 by default). The lateral solver then advances over the whole time elapsed since its last run.

The scheduler cannot be switched off. Neither HydroPol2D-Python nor the MATLAB code reads `flag_groundwater_async`, so a value of 0 does not force a lateral update every surface step. A shorter `groundwater_target_dt_s` makes the lateral updates more frequent.

### 7.2 Explicit groundwater stability cap

The outer scheduler cap is based on an explicit diffusivity estimate for the unconfined Boussinesq equation:

$$
D = \frac{K H}{S_y}
$$

$$
\Delta t_{\mathrm{gw,stable}}
=
\frac{
C_{\mathrm{gw}} \, L_{\mathrm{grid}}^2
}{
4 D_{\max}
}
$$

where:

- $D$ = groundwater diffusivity $[\mathrm{L}^2\,\mathrm{T}^{-1}]$
- $C_{\mathrm{gw}}$ = groundwater Courant/safety factor $[-]$
- $L_{\mathrm{grid}} = \min(\Delta x,\Delta y)$
- $D_{\max}$ = maximum domain diffusivity over the active groundwater cells

This is the cap used by the current `estimate_groundwater_stable_timestep` logic.

### 7.3 Inner Boussinesq substepping

When a lateral update is triggered, the solver receives no recharge term, because the net exchange has already changed the heads. It advances the heads over the elapsed interval with adaptive predictor-corrector substeps. Each substep is at most the stability cap of Section 7.2 and at least `groundwater_min_dt_s`. Both codes control the error by step doubling. A substep is accepted when one full step and two half steps differ by no more than $\delta_h + \delta_r H$ in every cell; otherwise it is shortened and repeated. The next substep the solver would have tried is kept as the suggested step for the next lateral update.

In the MATLAB code, each of these substeps is further split by a velocity-based condition of the form

$$
\Delta t_{\mathrm{inner}}
\le
\min\!\left(
\frac{C_v \Delta x}{|u_x|},\,
\frac{C_v \Delta y}{|u_y|}
\right)
$$

where:

- $u_x, u_y$ are Darcy groundwater velocities
- $C_v$ is the internal velocity-based safety factor, the same `groundwater_courant`

HydroPol2D-Python takes one predictor-corrector update per substep and has no velocity condition.

The result is a two-level strategy:

1. an outer scheduler cap based on explicit groundwater stability and allowed head change,
2. an inner adaptive predictor-corrector substepping loop inside the Boussinesq solver.

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

No-flow boundaries are enforced by zero-gradient conditions at the domain perimeter. In practice, HydroPol2D sets the flux to zero across every interface with a cell outside the domain and across the outer edge of the grid, unless the edge cell has a prescribed head. This is a discrete Neumann condition; the code does not copy heads into the perimeter cells.

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

Both codes can exchange water between the aquifer and the river cells. The exchange is optional and off by default. The switch is `flag_river_groundwater_exchange` in MATLAB and `flags.river_groundwater_exchange` in HydroPol2D-Python. In each river cell, the exchange follows a linear riverbed law,

$$
q_{\mathrm{river}}
=
\frac{K_{\mathrm{bed}}\,A_{\mathrm{bed}}}{b\,A_{\mathrm{cell}}}
\left(h - h_{\mathrm{river}}\right)
$$

where:

- $q_{\mathrm{river}}$ = exchange rate per unit cell area, positive from the aquifer to the river $[\mathrm{L}\,\mathrm{T}^{-1}]$
- $K_{\mathrm{bed}}$ = riverbed hydraulic conductivity $[\mathrm{L}\,\mathrm{T}^{-1}]$
- $A_{\mathrm{bed}}$ = riverbed area, the river width times the cell size and at most the cell area $[\mathrm{L}^2]$
- $b$ = riverbed thickness, `riverbed_thickness_m` (default 0.5 m) $[\mathrm{L}]$
- $h_{\mathrm{river}}$ = water-surface elevation in the river cell $[\mathrm{L}]$

Each surface-water step solves this law exactly for two linked stores, the aquifer of the cell and its surface water, and limits the volume to the water the donor store holds. The exchange is added to the net exchange, so it changes the water-table head in the same step as recharge and capillary rise.

---

## 11. Saturation-Excess Correction After Water Table Rise

After the heads change in a surface-water step, HydroPol2D recomputes the water-table depth and therefore the new maximum unsaturated storage:

$$
S_{\mathrm{UZ,max}}^{\,\mathrm{new}}
=
z_{\mathrm{wt}}^{\,\mathrm{new}}
\left(
\theta_{\mathrm{sat}} - \theta_r
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

In the layered default implementation, the correction is applied layer by layer. The three layer capacities are recomputed from the new water table, each layer keeps at most its own capacity, and the sum of the excesses goes to the surface. HydroPol2D-Python applies the correction after the local update and again after a lateral update; the MATLAB code applies it once per step, after both. This is a very important part of HydroPol2D because it guarantees **mass consistency** between the vadose and saturated zones when the water table rises during a time step.

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

## 13. Deep Aquifer

The optional deep aquifer represents slow groundwater below the modeled aquifer. It is semi-distributed: each subbasin has one linear reservoir.

### 13.1 Structure

A fixed fraction $f_d$ of the downward recharge goes to the deep aquifer before the rest reaches the water table. The recharge of all cells in subbasin $k$ feeds reservoir $k$. The reservoir releases

$$
Q_k = \frac{S_k}{\tau}
$$

where:

- $S_k$ = storage of reservoir $k$ $[\mathrm{L}^3]$
- $\tau$ = response time $[\mathrm{T}]$, the same for all subbasins
- $Q_k$ = deep return flow $[\mathrm{L}^3\,\mathrm{T}^{-1}]$

Two rasters define the layout. The subbasin raster says which cells feed which reservoir. The channel-weight raster says where each reservoir discharges: the return flow is spread over the river cells of its own subbasin, in proportion to the weight.

### 13.2 Update

For an input rate $I_k$ over a step $\Delta t$, the reservoir uses the exact solution of the linear-reservoir equation:

$$
S_{k}^{t+\Delta t}
=
S_{k}^{t}\,e^{-\Delta t/\tau}
+
I_k\,\tau\left(1-e^{-\Delta t/\tau}\right)
$$

and the discharged volume is

$$
V_{Q,k} = I_k\,\Delta t - \left(S_{k}^{t+\Delta t} - S_{k}^{t}\right)
$$

The update is conservative and does not depend on the step length.

### 13.3 Starting state

Because the outflow is storage over $\tau$, the starting storage follows from a starting outflow per unit area $q_0$:

$$
S_{k,0} = q_0\,A_k\,\tau
$$

where $A_k$ is the active area of subbasin $k$. Give at most one of the following:

| Setting | Meaning | $q_0$ |
|---|---|---|
| `deep_aquifer_initial_baseflow_mm_day` | Deep baseflow on the start date, for example from a gauge | as given |
| `deep_aquifer_mean_recharge_mm_year` | Long-term mean recharge $\bar{R}$; the reservoirs start at steady state | $f_d\,\bar{R}$ |
| Deep-aquifer initial-state file | Storage per subbasin, written by the groundwater calibration | storage given directly |

With none of them, the reservoirs start empty.

**From a gauge.** HydroPol2D-Python estimates $q_0$ from a daily discharge record with `hydropol2d estimate-deep-baseflow`:

1. Lyne–Hollick baseflow of the observed discharge;
2. recession segments and a master recession curve (MRC);
3. separation of the slow, linear deep tail of the MRC, which also gives $\tau$;
4. the start-date baseflow placed on the MRC, and its deep part divided by the drainage area.

Pick a start date in a recession. The baseflow filter lags a rising hydrograph, so the tool warns when the start-date discharge is more than twice the baseflow.

### 13.4 Settings

| Item | HydroPol2D-Python | HydroPol2D (MATLAB) |
|---|---|---|
| Switch | `flags.deep_aquifer` | `flag_deep_aquifer` |
| Subbasins | `static.deep_aquifer_subbasin_path` | `DeepAquiferSubbasins_path` |
| Channel weights | `static.deep_aquifer_channel_weight_path` | `DeepAquiferChannelWeight_path` |
| Recharge fraction $f_d$ | `vertical.deep_recharge_fraction` | `deep_recharge_fraction` |
| Response time $\tau$ | `vertical.deep_aquifer_response_time_days` (default 180) | `deep_aquifer_tau_days` |
| Starting baseflow | `vertical.deep_aquifer_initial_baseflow_mm_day` | `deep_aquifer_initial_baseflow_mm_day` |
| Mean recharge | `vertical.deep_aquifer_mean_recharge_mm_year` | `deep_aquifer_mean_recharge_mm_year` |
| Initial-state file | `static.deep_aquifer_initial_state_path` | `DeepAquiferInitialState_path` |

In MATLAB the starting-state values are in the "Deep aquifer: starting storage" block of the Soil and groundwater tab (see [Case Workbook Settings](../configuration/general_data#tab-soil-and-groundwater)). The Case Builder writes the subbasin and channel-weight rasters from the conditioned D8 terrain.

---

## 14. Mass Balance

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

The local update of every surface-water step closes the same balance, with the net exchange as the recharge term. The lateral solver is called with $R = 0$, and its check also counts the water exchanged with fixed-head cells. The MATLAB code stores the lateral residual as a groundwater diagnostic error. HydroPol2D-Python does not store it and tracks the water balance of the whole model instead.

Recharge and capillary rise do not wait in the scheduler. The net exchange changes the heads in the same surface-water step, so no exchange is in transit between lateral updates. The pending recharge and capillary-rise totals only count what has passed since the last lateral update and are not extra storage. This distinction is important for interpreting whole-model water-balance diagnostics.

---

## 15. Summary

The HydroPol2D groundwater model combines:

- a **layered vadose-zone recharge module** based on a Darcy–van Genuchten–Mualem closure,
- **capillary rise** from shallow groundwater into the root zone,
- an **asynchronous groundwater scheduler** for the slower lateral groundwater flow, while the net exchange changes the heads in every surface-water step,
- a **2D Boussinesq groundwater flow model** for lateral saturated flow,
- **adaptive explicit time stepping**,
- **surface exfiltration** when groundwater rises above the ground surface,
- a **saturation-excess correction** that preserves mass when the water table reduces vadose storage capacity,
- and an optional **deep aquifer** of linear reservoirs per subbasin, with a starting state set from a baseflow or a mean recharge.

This structure allows HydroPol2D to represent a dynamically coupled subsurface system in which:

- infiltration does not simply disappear into a static bucket,
- recharge affects groundwater head,
- groundwater flow redistributes water laterally,
- and groundwater can return to the land surface and influence overland flow generation.

The result is a groundwater model that is physically interpretable, mass conservative, and fully integrated with the hydrologic and hydrodynamic architecture of HydroPol2D.
