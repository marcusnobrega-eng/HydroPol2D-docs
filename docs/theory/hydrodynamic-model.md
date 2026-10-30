---
title: Hydrodynamic Model
---
import useBaseUrl from '@docusaurus/useBaseUrl';

# Hydrodynamic Model

HydroPol2D currently includes five major surface-routing families:

- local inertial,
- full momentum,
- diffusive D4,
- kinematic D4,
- cellular automata.

Only one of these major routing formulations should be active at a time. The current code enforces this routing-family exclusivity through the corresponding model flags. D8 support remains a limited-scope secondary pathway.

<p align="center">
  <img src={useBaseUrl('/img/theory/routing-families.svg')} width="720" alt="A table of the five routing families (local inertial, full momentum, diffusive D4, kinematic D4 and cellular automata) against the five terms of the shallow-water momentum equation, with a filled dot for each term a family keeps and the equation it solves" />
</p>

<p align="center">
  <em>Figure 1. The five routing families and the terms of the shallow-water momentum equation that each one keeps. One family is active in a run.</em>
</p>

## 1. Local Inertial Flow Routing

### 1.1 General rationale

HydroPol2D uses the **local inertial approximation** as its default hydrodynamic routing formulation. The objective is to retain the dominant physical controls of shallow-surface flow while avoiding the computational burden of the full shallow-water equations.

The local inertial approach is particularly attractive for flood inundation modeling because it preserves:

- the free-surface pressure gradient,
- gravitational acceleration,
- frictional resistance,
- and local temporal acceleration,

while neglecting the convective acceleration terms that are often much smaller than the pressure and friction terms in gradually varying shallow flows. This produces a formulation that is more physically consistent than kinematic or purely empirical routing, but still much lighter than a full dynamic-wave solver. HydroPol2D uses this formulation as the main engine for overland flooding, floodplain exchange, and surface-water redistribution across raster cells.  

From a modeling standpoint, the local inertial formulation is a good compromise because HydroPol2D is meant to support:

- rainfall-driven flood simulations,
- fluvial routing with inflow and stage boundaries,
- urban and floodplain applications,
- and controlled routing benchmarks across several numerical approximations,

all within a modular hydrologic–hydrodynamic framework. The local inertial model is therefore the hydrodynamic core that connects the rainfall–runoff generation modules to the spatial redistribution of surface water. 

---

### 1.2 Governing equations

The starting point is the depth-integrated mass conservation equation:

$$
\frac{\partial h}{\partial t}
+
\frac{\partial q_x}{\partial x}
+
\frac{\partial q_y}{\partial y}
=
r
-
i
-
et
+
s
$$

where:

- $h$ is surface water depth $[\mathrm{L}]$
- $q_x$ is unit discharge in the $x$ direction $[\mathrm{L}^2\,\mathrm{T}^{-1}]$
- $q_y$ is unit discharge in the $y$ direction $[\mathrm{L}^2\,\mathrm{T}^{-1}]$
- $r$ is rainfall input $[\mathrm{L}\,\mathrm{T}^{-1}]$
- $i$ is infiltration loss $[\mathrm{L}\,\mathrm{T}^{-1}]$
- $et$ is evapotranspiration loss $[\mathrm{L}\,\mathrm{T}^{-1}]$
- $s$ is the collection of additional source and sink terms $[\mathrm{L}\,\mathrm{T}^{-1}]$

In HydroPol2D, the hydrologic terms are computed before routing, and the local inertial solver is then used to evaluate the flux redistribution term.

For each face, the local inertial momentum equation is written in simplified form as

$$
\frac{\partial q}{\partial t}
=
-
g\,H_{\mathrm{f}}\,S
-
g\,n^2\,
\frac{q\,|q|}{H_{\mathrm{f}}^{7/3}}
$$

where:

- $q$ is the unit discharge across a face $[\mathrm{L}^2\,\mathrm{T}^{-1}]$
- $g$ is gravitational acceleration $[\mathrm{L}\,\mathrm{T}^{-2}]$
- $H_{\mathrm{f}}$ is the effective flow depth at the face $[\mathrm{L}]$
- $S$ is the free-surface slope at the face $[-]$
- $n$ is Manning’s roughness coefficient $[\mathrm{T}\,\mathrm{L}^{-1/3}]$

This formulation neglects convective acceleration but retains the dominant hydraulic balance between local acceleration, pressure gradient, and bed-friction resistance. 

<p align="center">
  <img src={useBaseUrl('/img/theory/local-inertial.svg')} width="720" alt="Two neighbouring cells seen from the side with bed elevation, depth, water surface, face depth and slope; the grid seen from above with depths at cell centres and discharges on faces; and the five steps of one local inertial time step, from the water surface to the continuity update" />
</p>

<p align="center">
  <em>Figure 2. The local inertial solver on one face and over one time step, in the order the code runs it. Each step gives the sections of this page that describe it.</em>
</p>

---

### 1.3 Water surface elevation and face slopes

The routing calculation begins from the cellwise water surface elevation

$$
\eta = z + h
$$

where:

- $\eta$ is water surface elevation $[\mathrm{L}]$
- $z$ is bed elevation $[\mathrm{L}]$
- $h$ is water depth $[\mathrm{L}]$

In the standard validated implementation, HydroPol2D uses the DEM bed elevation directly for slope calculations.

At the east face between cells $i$ and $i+1$, the face bed elevation is taken as

$$
z_{\mathrm{f},x} = \max\!\left(z_i,\;z_{i+1}\right)
$$

and the hydrostatically reconstructed water surface elevations are

$$
\eta_{\mathrm{L},x}^{\ast} = \max\!\left(\eta_i,\;z_{\mathrm{f},x}\right)
\qquad
\eta_{\mathrm{R},x}^{\ast} = \max\!\left(\eta_{i+1},\;z_{\mathrm{f},x}\right)
$$

The free-surface slope at the face is then computed as

$$
S_x = \frac{\eta_{\mathrm{R},x}^{\ast} - \eta_{\mathrm{L},x}^{\ast}}{\Delta x}
$$

Similarly, for a north–south face,

$$
z_{\mathrm{f},y} = \max\!\left(z_j,\;z_{j+1}\right)
$$

$$
\eta_{\mathrm{S},y}^{\ast} = \max\!\left(\eta_j,\;z_{\mathrm{f},y}\right)
\qquad
\eta_{\mathrm{N},y}^{\ast} = \max\!\left(\eta_{j+1},\;z_{\mathrm{f},y}\right)
$$

$$
S_y = \frac{\eta_{\mathrm{S},y}^{\ast} - \eta_{\mathrm{N},y}^{\ast}}{\Delta x}
$$

This hydrostatic reconstruction is essential near wet–dry fronts because it prevents nonphysical negative depths and ensures that the pressure gradient is evaluated only over the hydraulically connected wetted portion of the interface. In practical terms, it is one of the key stabilizing ingredients of the HydroPol2D local inertial implementation. 

---

### 1.4 Effective face depth

The effective hydraulic depth used in the momentum equation is computed at the face level.

For the standard coarse-grid case, the face depth is

$$
H_{\mathrm{f},x}
=
\max\!\left(
\max(\eta_i,\eta_{i+1}) - z_{\mathrm{f},x},
0
\right)
$$

and similarly in the $y$ direction.

Thus, the face depth is not simply the arithmetic average of neighboring cell depths. Instead, it is a hydrostatically reconstructed depth referenced to the highest bed elevation at the interface. This makes the model much more robust when adjacent cells have different bed elevations or when one side is nearly dry. The same conceptual definition is already stated in your background document. 

---

### 1.5 Discrete local inertial solver

HydroPol2D updates the face discharge explicitly in time. The base discrete form used in the original Bates-type scheme is

$$
q^{t+\Delta t}
=
\frac{
q^{t}
-
g\,H_{\mathrm{f}}\,\Delta t\,S
}{
1
+
g\,\Delta t\,n^2
\,
\dfrac{|q^{t}|}{H_{\mathrm{f}}^{7/3}}
}
$$

where:

- $q^{t}$ is the previous face discharge $[\mathrm{L}^2\,\mathrm{T}^{-1}]$
- $q^{t+\Delta t}$ is the updated face discharge $[\mathrm{L}^2\,\mathrm{T}^{-1}]$
- $\Delta t$ is time step $[\mathrm{T}]$

This is the exact form implemented in the `Inertial_Solver` when `flag_numerical_scheme = 1`. 

The structure of this equation is important:

- the numerator contains the inertial memory from the previous step and the free-surface driving term,
- the denominator contains the frictional damping,
- so the scheme behaves as an explicit predictor with semi-implicit friction treatment.

This is why the method is stable and efficient for shallow-flood simulations.

---

### 1.6 Numerical schemes available in HydroPol2D

HydroPol2D supports three local inertial variants:

- original Bates scheme,
- $s$-upwind scheme,
- $s$-centered scheme.

These are controlled by `flag_numerical_scheme`. 

#### 1.6.1 Scheme 1: original Bates formulation

This is the simplest and most direct discrete local inertial update:

$$
q^{t+\Delta t}
=
\frac{
q^{t}
-
g\,H_{\mathrm{f}}\,\Delta t\,S
}{
1
+
g\,\Delta t\,n^2
\,
\dfrac{|q^{t}|}{H_{\mathrm{f}}^{7/3}}
}
$$

It is computationally efficient and physically consistent, but in steep-gradient or strongly discontinuous settings it may be more prone to oscillatory behavior than the modified schemes.

#### 1.6.2 Scheme 2: $s$-upwind formulation

The upwind version introduces a directional discharge estimate $q_{\mathrm{upwind}}$ and blends it with the current face discharge using a diffusivity factor $\theta$:

$$
q^{t+\Delta t}
=
\frac{
\theta q^{t}
+
(1-\theta) q_{\mathrm{upwind}}
-
g\,H_{\mathrm{f}}\,\Delta t\,S
}{
1
+
g\,\Delta t\,n^2
\,
\dfrac{|q^{t}|}{H_{\mathrm{f}}^{7/3}}
}
$$

The diffusivity factor is computed as

$$
\theta
=
1
-
\frac{\Delta t}{\Delta x}
\min\!\left(
\frac{|q|}{H_{\mathrm{f}}},
\sqrt{g\,H_{\mathrm{f}}}
\right)
$$

This quantity introduces controlled numerical diffusion. In practical terms:

- when flow is slow and well resolved, $\theta$ remains close to $1$ and the scheme behaves like the original local inertial update;
- when flow becomes fast or the time step approaches the local Courant limit, the scheme shifts part of the update toward the upwind flux, which damps oscillations.

This is why the upwind variant is useful in more challenging routing conditions. 

#### 1.6.3 Scheme 3: $s$-centered formulation

The centered scheme replaces the upwind discharge by a centered neighbor average:

$$
q_{\mathrm{avg}}
=
\frac{q_{i-1} + q_{i+1}}{2}
$$

and updates the discharge as

$$
q^{t+\Delta t}
=
\frac{
\theta q^{t}
+
(1-\theta) q_{\mathrm{avg}}
-
g\,H_{\mathrm{f}}\,\Delta t\,S
}{
1
+
g\,\Delta t\,n^2
\,
\dfrac{|q^{t}|}{H_{\mathrm{f}}^{7/3}}
}
$$

This scheme is more symmetric than the upwind version and less diffusive, but it still uses the same $\theta$ coefficient to suppress instability. In practice it provides a compromise between the sharper response of the original Bates form and the stronger damping of the upwind form. 

---

### 1.7 Wet–dry treatment and minimum operative depth

HydroPol2D contains several explicit protections to prevent nonphysical routing across dry or invalid interfaces.

A face is suppressed if:

- the effective face depth is zero,
- one of the neighboring cells is outside the valid domain,
- or the local cell depth is below a minimum operative threshold.

In code terms, HydroPol2D zeroes:

- face slope,
- effective depth,
- and effective face width

whenever a face is dry or invalid. It then applies an additional shallow-water logic based on a minimum operative depth $h_{\min}$. If the current cell depth is below $h_{\min}$, neighboring face fluxes are zeroed to suppress spurious motion in nearly dry cells. In the standard case, the code uses $h_{\min}=10^{-6}\,\mathrm{m}$, although this can be set to zero when inflow hydrographs are being imposed. 

This wet–dry logic is one of the reasons the model remains robust in flood expansion and recession phases.

---

### 1.8 Unit conversion and face discharge bookkeeping

Internally, the inertial solver works with **unit discharge** $q$ in

$$
[\mathrm{L}^2\,\mathrm{T}^{-1}]
\quad\text{that is,}\quad
[\mathrm{m}^2\,\mathrm{s}^{-1}]
$$

The code first converts the current outflow state from cell-based depth units into face-based unit discharge. After the local inertial update is performed, the model converts back to volumetric discharge per face:

$$
Q = q\,W_{\mathrm{f}}
$$

and then to an equivalent depth-rate over the cell area:

$$
q_{\mathrm{mm/h}}
=
\frac{Q}{A_{\mathrm{cell}}}
\,
1000
\,
3600
$$

where:

- $A_{\mathrm{cell}}$ is cell area $[\mathrm{L}^2]$

This bookkeeping is necessary because HydroPol2D couples the hydrodynamic fluxes to hydrologic terms that are tracked in depth units such as $\mathrm{mm}$ or $\mathrm{mm/h}$.

---

### 1.10 Physical flow limits

HydroPol2D imposes two additional physical constraints after the inertial update.

#### 1.10.1 Critical-flow limit

If the critical-flow limiter is active, the magnitude of the unit discharge is bounded by

$$
|q| \le H_{\mathrm{f}} \sqrt{g\,H_{\mathrm{f}}}
$$

This prevents the inertial solver from producing velocities that exceed the local critical condition. 

#### 1.10.2 Maximum velocity limit

HydroPol2D also imposes a hard maximum velocity threshold, currently set to

$$
u_{\max} = 10 \;\mathrm{m\,s}^{-1}
$$

The corresponding unit-discharge bound is

$$
|q| \le H_{\mathrm{f}}\,u_{\max}
$$

This is a pragmatic numerical safeguard against isolated spikes caused by abrupt depth or slope discontinuities. 

---

### 1.11 Continuity update and cell-volume balance

Once face discharges have been computed, HydroPol2D updates each cell by integrating the net flux divergence over the time step.

At the cell level, the intercell volume balance can be written conceptually as

$$
\Delta V
=
\Delta t
\left(
Q_{\mathrm{in}} - Q_{\mathrm{out}}
\right)
$$

The updated water depth is then

$$
h^{t+\Delta t}
=
h^t
+
\frac{\Delta V}{A_{\mathrm{eff}}}
$$

where:

- $A_{\mathrm{eff}}$ is the effective storage area of the cell $[\mathrm{L}^2]$

In the validated coarse-grid workflow, $A_{\mathrm{eff}}$ is the cell area.

The code then enforces

$$
h^{t+\Delta t} \ge 0
$$

so that negative water depths are never allowed.

---

### 1.12 Outlet boundary conditions

HydroPol2D supports two outlet treatments in the local inertial solver.

#### 1.12.1 Normal-depth outlet

When `outlet_type = 1`, the outlet slope is imposed as a prescribed normal-flow slope

$$
S_0 = s_{\mathrm{outlet}}
$$

and the outlet discharge is computed with Manning’s equation.

#### 1.12.2 Critical-depth outlet

When `outlet_type \ne 1`, HydroPol2D computes a critical-slope-like outlet control from the local depth and roughness. In both cases, the outlet flux is converted to a depth-equivalent rate and subtracted from the final water depth during the update. 

This outlet treatment allows the local inertial solver to remain embedded within a raster domain while still applying a physically interpretable boundary condition at the domain perimeter.

---

### 1.13 Reservoir and hydraulic-control interaction

The local inertial solver can also be modified internally by storage or rating-curve controls. When reservoir routing is active, HydroPol2D imposes discharge relationships of the form

$$
Q = k\,(h-h_0)^m
$$

subject to available water constraints and user-defined downstream connections. In the current implementation, two-stage control logic is supported. The resulting discharged volume is transferred directly to designated downstream cells. 

This means the local inertial solver is not a closed routing block; it is a routing core that can be locally modified by hydraulic control structures.

---

### 1.14 Why the local inertial model is the default in HydroPol2D

The local inertial formulation is the default routing method in HydroPol2D for three reasons.

First, it retains the dominant hydraulics needed for flood propagation:

- free-surface pressure gradient,
- friction,
- local acceleration.

Second, it is computationally efficient enough to be used over large raster domains and under GPU execution.

Third, it integrates naturally with HydroPol2D’s validated process coupling:

- hydraulic controls,
- outlet conditions,
- and hydrologic source–sink coupling.

For these reasons, it provides the best balance between physical realism and computational tractability for the majority of HydroPol2D applications. 

---

### 1.15 Neal (2012) subgrid model

HydroPol2D includes the rectangular channel-subgrid formulation proposed by [Neal et al. (2012)](https://doi.org/10.1029/2012WR012514). This extension is used when a river is narrower than the raster cell. It embeds a channel within the coarse cell while retaining two-dimensional floodplain routing on the surrounding cell area.

Let $\Delta x$ be the coarse-cell width, $z_f$ the floodplain elevation, $H$ the channel bank height, and $w$ the channel width, where $0<w<\Delta x$. The channel-bed elevation is

$$
z_c = z_f-H.
$$

The model depth $h$ is measured above $z_c$. Water remains in the rectangular channel while $h\le H$ and spreads over the coarse cell when $h>H$.

#### Channel flow at a cell face

The channel water-surface elevation is

$$
y_c=z_c+h.
$$

For adjacent cells $i$ and $j$, the water-surface slope and face flow depth are

$$
S_c=\frac{y_{c,j}-y_{c,i}}{\Delta x},
$$

$$
h_{c,f}=\max\!\left[\max(y_{c,i},y_{c,j})-
\max(z_{c,i},z_{c,j}),0\right].
$$

The shared channel width is the smaller of the two cell widths,

$$
w_{c,f}=\min(w_i,w_j).
$$

The channel flow area and hydraulic radius are

$$
A_c=w_{c,f}h_{c,f},
\qquad
R_c=\frac{A_c}{w_{c,f}+2h_{c,f}}.
$$

The channel discharge is updated with the local-inertial equation

$$
Q_c^{t+\Delta t}=
\frac{Q_c^t-gA_c\Delta t S_c}
{1+g\Delta t n_c^2|Q_c^t|/(R_c^{4/3}A_c)},
$$

where $n_c$ is the channel Manning coefficient.

#### Floodplain flow at a cell face

Floodplain depth is measured above the coarse DEM:

$$
h_f=\max(h+z_c-z_f,0),
\qquad y_f=z_f+h_f.
$$

The floodplain face slope and depth are computed from $y_f$ and $z_f$ in the same way as the channel terms. The local-inertial update uses unit discharge $q_f$:

$$
q_f^{t+\Delta t}=
\frac{q_f^t-gh_{f,f}\Delta t S_f}
{1+g\Delta t n_f^2|q_f^t|/h_{f,f}^{7/3}},
$$

where $n_f$ is the floodplain Manning coefficient. The floodplain and total face discharges are

$$
Q_f=q_f(\Delta x-w_{c,f}),
\qquad
Q=Q_c+Q_f.
$$

HydroPol2D applies this split on orthogonal D4 faces. The outlet uses the same channel and floodplain components as the internal faces.

#### Conservative storage transition

The cell continuity equation is evaluated in volume space. For a channel cell,

$$
V(h)=
\begin{cases}
\Delta x\,w\,h, & h\le H,\\[4pt]
\Delta x\,w\,H+\Delta x^2(h-H), & h>H.
\end{cases}
$$

Thus, the active water-surface area $\mathrm{d}V/\mathrm{d}h$ changes from $\Delta xw$ in-bank to $\Delta x^2$ overbank. Routing fluxes and hydrologic source or sink terms update $V$ first. HydroPol2D then inverts the same piecewise relation to recover $h$. This avoids a mass discontinuity when the water level crosses bankfull.

The active configuration and geometry inputs are documented under [Neal (2012) subgrid model configuration](../configuration/flags#neal-2012-subgrid-model-configuration). Controlled validation results are provided in [Neal (2012) Subgrid Model Validation](../validation/neal-subgrid).

### 1.16 Summary

In HydroPol2D, the Local Inertial Model is a depth-integrated raster-based routing formulation in which:

- the cell water surface elevation is first reconstructed,
- free-surface slopes are evaluated at faces,
- effective face depths are computed hydrostatically,
- face discharges are updated with a Bates-type local inertial equation,
- the resulting fluxes are converted into volumetric discharges,
- and water depth is updated by a conservative cell-volume balance.

The solver supports:

- the original Bates scheme,
- an upwind-stabilized scheme,
- a centered stabilized scheme,
- outlet controls,
- reservoir controls,
- wet–dry front handling,
- critical-flow and velocity limits.

This makes it the main hydrodynamic engine of HydroPol2D for physically based surface-flow routing. 

---

## 2. Full-Momentum Flow Routing

### 2.1 General rationale

HydroPol2D also includes a **full-momentum shallow-water solver** for cases where the local inertial approximation is not sufficient. This option is intended for controlled hydraulic benchmarks and applications where convective acceleration, wave propagation, or stronger dynamic effects need to be represented more explicitly.

The full-momentum model solves the conservative two-dimensional shallow-water equations on the raster grid. In HydroPol2D, this is implemented as a finite-volume routing core with explicit storage and momentum states.

The solver is activated through the full-momentum routing flag in the model configuration. It should be used as an alternative to, not simultaneously with, local inertial, kinematic, diffusive, D8, or CA routing.

---

### 2.2 Conservative shallow-water equations

The conserved state vector is

$$
\mathbf{U}
=
\begin{bmatrix}
h \\
hu \\
hv
\end{bmatrix}
$$

where:

- $h$ is water depth $[\mathrm{L}]$
- $u$ is depth-averaged velocity in the $x$ direction $[\mathrm{L}\,\mathrm{T}^{-1}]$
- $v$ is depth-averaged velocity in the $y$ direction $[\mathrm{L}\,\mathrm{T}^{-1}]$
- $hu$ and $hv$ are unit discharges or momentum variables $[\mathrm{L}^2\,\mathrm{T}^{-1}]$

The governing equations are written as

$$
\frac{\partial \mathbf{U}}{\partial t}
+
\frac{\partial \mathbf{F}(\mathbf{U})}{\partial x}
+
\frac{\partial \mathbf{G}(\mathbf{U})}{\partial y}
=
\mathbf{S}_{\mathrm{bed}}
+
\mathbf{S}_{\mathrm{fric}}
$$

with fluxes

$$
\mathbf{F}(\mathbf{U})
=
\begin{bmatrix}
hu \\
\dfrac{(hu)^2}{h} + \dfrac{1}{2}gh^2 \\
\dfrac{(hu)(hv)}{h}
\end{bmatrix}
$$

and

$$
\mathbf{G}(\mathbf{U})
=
\begin{bmatrix}
hv \\
\dfrac{(hu)(hv)}{h} \\
\dfrac{(hv)^2}{h} + \dfrac{1}{2}gh^2
\end{bmatrix}
$$

where $g$ is gravitational acceleration.

The bed-slope source terms represent topographic forcing:

$$
\mathbf{S}_{\mathrm{bed}}
=
\begin{bmatrix}
0 \\
-gh\,\dfrac{\partial z}{\partial x} \\
-gh\,\dfrac{\partial z}{\partial y}
\end{bmatrix}
$$

and the friction source terms represent Manning resistance.

---

### 2.3 Numerical fluxes and momentum memory

HydroPol2D computes full-momentum fluxes with an HLL-type finite-volume solver. At each cell face, left and right reconstructed states are used to compute mass flux and momentum flux. The update is conservative in the sense that flux leaving one cell enters the adjacent cell with opposite sign.

Unlike the local inertial solver, the full-momentum model must carry momentum from one time step to the next. HydroPol2D stores:

- the current cell-centered $hu$ state,
- the current cell-centered $hv$ state,
- face mass fluxes converted back to HydroPol2D depth-rate units,
- outlet sink terms.

This momentum memory is what makes the model a true dynamic-wave solver rather than a discharge recalculation based only on the current water-surface slope.

---

### 2.4 Bed slope, friction, and wetting-drying treatment

The full-momentum solver includes several numerical protections for raster flood simulation:

- dry and inactive cells are treated as solid walls;
- very shallow cells are cleaned to avoid undefined velocities;
- momentum is limited by a maximum admissible velocity;
- Manning friction is applied with a semi-implicit or exact implicit update;
- a draining limiter prevents a face flux from removing more water than is available.

The Manning friction update damps momentum according to local depth, roughness, and velocity magnitude. Conceptually, the momentum components are relaxed by a denominator of the form

$$
1 + g\,n^2\,\Delta t\,\frac{\sqrt{u^2+v^2}}{h^{4/3}}
$$

where $n$ is Manning's roughness coefficient. This prevents unrealistically large momentum in shallow water while retaining dynamic propagation where water depth is sufficient.

Hydrostatic reconstruction is available for complex terrain and well-balanced bed-slope treatment, while the default controlled-benchmark pathway uses the robust HLL flux/source treatment implemented in the current solver.

---

### 2.5 Continuity update and HydroPol2D coupling

After the HLL fluxes are computed, the depth update follows the finite-volume balance:

$$
h^{t+\Delta t}
=
h^t
-
\frac{\Delta t}{\Delta x}
\left(
F_h^{E} - F_h^{W}
+
G_h^{N} - G_h^{S}
\right)
$$

where $F_h$ and $G_h$ are the mass-flux components through the cell faces.

HydroPol2D then converts the face fluxes to the same bookkeeping convention used by the rest of the model:

$$
q_{\mathrm{mm/h}}
=
\frac{Q}{A_{\mathrm{cell}}}
1000
3600
$$

This allows the full-momentum solver to remain compatible with hydrologic source/sink terms, water-quality transport, reservoir controls, and boundary-condition diagnostics.

---

### 2.6 Boundary conditions and hydraulic controls

The full-momentum model supports the same practical boundary-condition architecture used by HydroPol2D routing:

- closed reflective walls along inactive or exterior faces,
- outlet sink cells with normal-depth or critical-depth behavior,
- imposed inflow hydrograph boundaries,
- prescribed stage hydrograph boundaries,
- reservoir and internal rating-curve control structures.

<p align="center">
  <img src={useBaseUrl('/img/theory/boundaries-structures.svg')} width="720" alt="Plan view of a schematic catchment on a regular grid with an inflow hydrograph, a reservoir behind a dam, a culvert under a road, a detention pond, a stage hydrograph, an outlet and closed walls, each numbered and explained on the right, and an inset with the groundwater boundaries on the same domain" />
</p>

<p align="center">
  <em>Figure 3. Where water enters, leaves or is controlled in a model domain. The terrain, rivers, road and pond are synthetic.</em>
</p>

For closed boundaries, normal mass flux is zero, but wall-pressure effects are accounted for in the momentum update. This is important for stable behavior near domain edges and inactive cells.

Outlet fluxes are converted to a volume sink and removed from the local water storage, subject to available water constraints.

---

### 2.7 Current validation evidence

The full-momentum solver is part of the validation suite. Current report-ready evidence includes:

- tilted-plane runoff against the analytical kinematic-wave limit;
- V-tilted catchment mass-conservation and bilateral-symmetry checks;
- Ritter dry-bed dam-break analytical profiles;
- non-breaking wave propagation and profile comparison;
- prescribed stage-boundary enforcement;
- inflow hydrograph and reservoir/control-structure bookkeeping where full-momentum routing is used.

These tests validate the full-momentum implementation as a controlled dynamic-wave routing option. They do not imply field calibration for a particular watershed.

---

### 2.8 Practical use of the full-momentum solver

The full-momentum solver is intended for runs where the added advective and local-acceleration terms matter enough to justify the extra cost. In HydroPol2D, it should be treated as a standalone routing-family choice, not as a layer on top of the lighter routing options.

---

## 3. Diffusive and Kinematic D4 Routing

HydroPol2D implements both **diffusive** and **kinematic** wave routing through a shared conservative D4 solver. These modes are lighter than the local inertial and full-momentum solvers, but they still use explicit face-based fluxes, conservative volume updates, outlet handling, and reservoir/control coupling.

### 3.1 Shared conservative routing structure

In both modes, HydroPol2D routes water across the four orthogonal neighbors of each cell and updates the cell depth through a conservative volume balance:

$$
h^{t+\Delta t}
=
h^t
+
\frac{V_{\mathrm{in}} - V_{\mathrm{out}}}{A_{\mathrm{cell}}}
$$

where:

- $h$ is cell water depth $[\mathrm{L}]$
- $V_{\mathrm{in}}$ and $V_{\mathrm{out}}$ are incoming and outgoing volumes over the substep $[\mathrm{L}^3]$
- $A_{\mathrm{cell}}$ is the active cell area $[\mathrm{L}^2]$

The routing interval is internally subdivided when needed. The current code estimates the number of substeps from a Manning-type velocity estimate and a Courant-style target so that steep slopes or deep water do not destabilize the explicit update.

### 3.2 Diffusive mode

In diffusive mode, the driving slope is the **water-surface slope** between adjacent cells. For a face shared by left and right cells,

$$
\eta = z + h
$$

$$
S_f = \frac{\eta_L - \eta_R}{\Delta x}
$$

with hydrostatically reconstructed face depth

$$
H_f = \max\!\left(\max(\eta_L,\eta_R) - z_f,\,0\right)
$$

The face unit discharge is then evaluated with a Manning-type flux law:

$$
q_f
=
\operatorname{sign}(S_f)
\frac{H_f^{5/3}}{n}
\sqrt{|S_f|}
$$

This mode can represent backwater-like redistribution driven by water-surface gradients while remaining much cheaper than solving a momentum equation.

### 3.3 Kinematic mode

In kinematic mode, the driving slope is the **bed slope**, not the water-surface slope:

$$
S_b = \frac{z_L - z_R}{\Delta x}
$$

The code then applies a donor-depth rule:

- if $S_b > 0$, the left cell is the donor and its depth drives the flux,
- if $S_b < 0$, the right cell is the donor and its depth drives the flux.

Using donor depth $H_{\mathrm{donor}}$, the unit discharge is

$$
q_f
=
\operatorname{sign}(S_b)
\frac{H_{\mathrm{donor}}^{5/3}}{n_{\mathrm{donor}}}
\sqrt{|S_b|}
$$

This makes the kinematic route strictly slope-directed and prevents it from representing the same backwater behavior captured by the diffusive, inertial, or full-momentum solvers.

### 3.4 Shared controls, outlet handling, and coupling

Both D4 wave modes share the same conservative routing machinery for:

- internal substepping,
- available-storage limiting so a donor cell cannot export more volume than it contains,
- optional critical-flow limiting,
- outlet discharge removal,
- reservoir and hydraulic-control interaction.

As with the other routing families, rainfall, infiltration, evapotranspiration, groundwater feedback, and other source/sink terms are handled by the coupled HydroPol2D framework around the routing update.

### 3.5 Scope and caveats

The D4 diffusive and kinematic modes are part of the implemented routing family and are used in current controlled validation benchmarks. However:

- they should be treated as alternatives to, not combinations with, local inertial or full momentum,
- D8 support should be considered a limited-scope secondary pathway rather than a parallel theory family,
## 4. Cellular Automata Flow Routing

### 4.1 Conceptual formulation

In addition to the Local Inertial Model, HydroPol2D provides a **Cellular Automata (CA) routing scheme** as a simplified alternative for surface flow propagation.

The CA model is based on **local redistribution of water volume between neighboring cells**, driven by differences in water surface elevation. Unlike the local inertial formulation, this approach:

- does not explicitly solve a momentum equation,
- does not track velocity or discharge at faces,
- relies on empirical flow redistribution rules,
- ensures strict mass conservation at the cell level.

This formulation is particularly useful for:

- rapid flood extent estimation,
- large-scale simulations where computational efficiency is critical,
- cases where detailed hydraulic dynamics are not required.

---

### 4.2 Water surface representation

As in the inertial model, the driving variable is the water surface elevation:

$$
\eta = z + h
$$

where:

- $\eta$ = water surface elevation $[\mathrm{L}]$
- $z$ = bed elevation $[\mathrm{L}]$
- $h$ = water depth $[\mathrm{L}]$

---

### 4.3 Driving gradient and flow direction

Flow between a cell $i$ and a neighboring cell $j$ is driven by the difference:

$$
\Delta \eta_{i,j} = \eta_i - \eta_j
$$

Only positive gradients contribute to flow:

$$
\Delta \eta_{i,j} > 0
$$

This ensures that water flows only **downhill in terms of free surface**, preventing nonphysical backflow.

---

### 4.4 Available transferable volume

The potential volume that can be transferred from cell $i$ to neighbor $j$ is estimated as:

$$
V_{i,j} = A_{\mathrm{cell}} \cdot \max(\Delta \eta_{i,j}, 0)
$$

where:

- $V_{i,j}$ = transferable volume $[\mathrm{L}^3]$
- $A_{\mathrm{cell}}$ = cell area $[\mathrm{L}^2]$

---

### 4.5 Flow partitioning

The total transferable volume from a cell is distributed among its neighbors proportionally:

$$
w_{i,j} =
\frac{
V_{i,j}
}{
\sum_k V_{i,k} + \varepsilon
}
$$

where:

- $w_{i,j}$ = weight assigned to neighbor $j$
- $\varepsilon$ = small numerical constant to avoid division by zero

The total outflow from the cell is then:

$$
I_{i,j} = w_{i,j} \cdot I_{\mathrm{tot}}
$$

where:

- $I_{\mathrm{tot}}$ = total outgoing volume $[\mathrm{L}^3]$

---

### 4.6 Velocity estimation

Although the CA model does not explicitly solve momentum equations, a characteristic velocity is estimated using Manning’s equation:

$$
u = \frac{1}{n} h^{2/3} S^{1/2}
$$

where:

- $u$ = flow velocity $[\mathrm{L}\mathrm{T}^{-1}]$
- $n$ = Manning coefficient $[\mathrm{T}\mathrm{L}^{-1/3}]$
- $S$ = slope $[-]$

This velocity is used to control the **rate of water redistribution**.

---

### 4.7 Outflow computation

The total outflow from a cell is computed as:

$$
I_{\mathrm{tot}} = u \cdot h \cdot \Delta t \cdot W_{\mathrm{eff}}
$$

where:

- $I_{\mathrm{tot}}$ = total outgoing volume $[\mathrm{L}^3]$
- $\Delta t$ = time step $[\mathrm{T}]$
- $W_{\mathrm{eff}}$ = effective flow width $[\mathrm{L}]$

---

### 4.8 Depth update

After redistribution, the water depth is updated as:

$$
h^{t+\Delta t}
=
h^t
+
\frac{
\sum Q_{\mathrm{in}} - \sum Q_{\mathrm{out}}
}{
A_{\mathrm{cell}}
}
$$

where:

- $Q_{\mathrm{in}}$ = incoming volume $[\mathrm{L}^3]$
- $Q_{\mathrm{out}}$ = outgoing volume $[\mathrm{L}^3]$

The model enforces:

$$
h^{t+\Delta t} \ge 0
$$

ensuring physical consistency.

---

### 4.9 Stability and robustness

The CA model is inherently stable because:

- flow is limited by available water volume,
- redistribution is bounded by local gradients,
- no explicit acceleration terms are present.

However, the method is:

- more diffusive than the Local Inertial Model,
- less accurate for representing dynamic hydraulic processes,
- not suitable for capturing wave propagation or backwater effects.

---

### 4.10 Comparison with Local Inertial Model

| Feature | Local Inertial Model | Cellular Automata |
|--------|----------------------|-------------------|
| Physics | Momentum-based | Empirical |
| Variables | $q$, $h$, $\eta$ | $h$, $\eta$ |
| Accuracy | High | Moderate |
| Stability | Conditional | Very high |
| Computational cost | Moderate | Low |
| Flood dynamics | Well captured | Diffusive |

---

### 4.11 When to use the CA model

The Cellular Automata model is recommended when:

- large-scale simulations are required,
- computational speed is a priority,
- only flood extent or approximate depths are needed,
- detailed hydraulic behavior is not critical.

For physically based flood propagation, the **Local Inertial Model remains the preferred option**.

---

## Summary

HydroPol2D supports a routing family that now publicly includes:

- **local inertial** routing as the default physically based flood solver,
- **full momentum** routing for dynamic-wave benchmarks and stronger momentum effects,
- **diffusive D4** routing driven by water-surface slope,
- **kinematic D4** routing driven by bed slope and donor depth,
- **cellular automata** routing for fast, simplified redistribution.

All of these routes share HydroPol2D’s broader coupling with hydrologic inputs, groundwater feedback, outlet bookkeeping, and hydraulic controls, but only one major routing formulation should be active in a given run. D8 remains secondary in scope.
