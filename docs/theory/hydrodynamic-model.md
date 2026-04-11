---
title: Hydrodynamic Model
---

# Hydrodynamic Model

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
- and subgrid-enhanced coarse-grid calculations,

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

In the current implementation, HydroPol2D explicitly preserves the **DEM bed elevation** for slope calculations, even when subgrid invert elevations are used for lookup-table interpolation. In other words, the pressure-gradient term is always based on the real coarse-grid DEM bed, not on the subgrid invert. This is a deliberate design choice in the updated March 2026 implementation. 

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

### 1.8 Subgrid hydraulic representation inside the local inertial solver

A major strength of HydroPol2D is that the local inertial solver can be coupled with subgrid hydraulic properties. In this mode, a high-resolution DEM is used offline to precompute, for each coarse cell and each face:

- wetted area,
- wetted width,
- and related hydraulic properties

as functions of water depth. These are stored in lookup tables. 

In the updated implementation, when `flag_subgrid = 1` and overbank routing is not being handled by the classical channel–floodplain splitter, HydroPol2D replaces the coarse face depth by a lookup-based depth:

$$
H_{\mathrm{f}} = \frac{A_{\mathrm{face}}}{\Delta x}
$$

where:

- $A_{\mathrm{face}}$ is wetted face area obtained from the subgrid table $[\mathrm{L}^2]$
- $\Delta x$ is coarse-grid resolution $[\mathrm{L}]$

The face width used to convert unit discharge to volumetric discharge is also taken from the subgrid table:

$$
Q = q\,W_{\mathrm{f}}
$$

where:

- $Q$ is face discharge $[\mathrm{L}^3\,\mathrm{T}^{-1}]$
- $W_{\mathrm{f}}$ is wetted face width $[\mathrm{L}]$

This is a very important modeling choice. It means HydroPol2D is not merely correcting the storage term with subgrid information; it is also correcting the **momentum depth** and the **flow width**, which directly influence the hydraulic routing. The result is a much more realistic coarse-grid routing response over strongly heterogeneous topography. 

---

### 1.9 Unit conversion and face discharge bookkeeping

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

This bookkeeping is necessary because HydroPol2D couples the hydrodynamic fluxes to hydrologic terms that are tracked in depth units such as $\mathrm{mm}$ or $\mathrm{mm/h}$. The updated March 2026 implementation explicitly emphasizes that in subgrid mode, this conversion must use the **face width** rather than the coarse cell width. 

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

In the coarse-grid case, $A_{\mathrm{eff}}$ is simply the cell area. In the subgrid channel / overbank formulation, however, the effective area may depend on whether the water level is in-bank or overbank, and the model updates this area dynamically. 

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

Third, it integrates naturally with HydroPol2D’s advanced features:

- subgrid tables,
- overbank transitions,
- hydraulic controls,
- outlet conditions,
- and hydrologic source–sink coupling.

For these reasons, it provides the best balance between physical realism and computational tractability for the majority of HydroPol2D applications. 

---

### 1.15 Summary

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
- subgrid hydraulic lookup tables,
- outlet controls,
- reservoir controls,
- wet–dry front handling,
- critical-flow and velocity limits.

This makes it the main hydrodynamic engine of HydroPol2D for physically based surface-flow routing. 

---

## 2. Cellular Automata Flow Routing

### 2.1 Conceptual formulation

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

### 2.2 Water surface representation

As in the inertial model, the driving variable is the water surface elevation:

$$
\eta = z + h
$$

where:

- $\eta$ = water surface elevation $[\mathrm{L}]$
- $z$ = bed elevation $[\mathrm{L}]$
- $h$ = water depth $[\mathrm{L}]$

---

### 2.3 Driving gradient and flow direction

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

### 2.4 Available transferable volume

The potential volume that can be transferred from cell $i$ to neighbor $j$ is estimated as:

$$
V_{i,j} = A_{\mathrm{cell}} \cdot \max(\Delta \eta_{i,j}, 0)
$$

where:

- $V_{i,j}$ = transferable volume $[\mathrm{L}^3]$
- $A_{\mathrm{cell}}$ = cell area $[\mathrm{L}^2]$

---

### 2.5 Flow partitioning

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

### 2.6 Velocity estimation

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

### 2.7 Outflow computation

The total outflow from a cell is computed as:

$$
I_{\mathrm{tot}} = u \cdot h \cdot \Delta t \cdot W_{\mathrm{eff}}
$$

where:

- $I_{\mathrm{tot}}$ = total outgoing volume $[\mathrm{L}^3]$
- $\Delta t$ = time step $[\mathrm{T}]$
- $W_{\mathrm{eff}}$ = effective flow width $[\mathrm{L}]$

---

### 2.8 Depth update

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

### 2.9 Stability and robustness

The CA model is inherently stable because:

- flow is limited by available water volume,
- redistribution is bounded by local gradients,
- no explicit acceleration terms are present.

However, the method is:

- more diffusive than the Local Inertial Model,
- less accurate for representing dynamic hydraulic processes,
- not suitable for capturing wave propagation or backwater effects.

---

### 2.10 Comparison with Local Inertial Model

| Feature | Local Inertial Model | Cellular Automata |
|--------|----------------------|-------------------|
| Physics | Momentum-based | Empirical |
| Variables | $q$, $h$, $\eta$ | $h$, $\eta$ |
| Accuracy | High | Moderate |
| Stability | Conditional | Very high |
| Computational cost | Moderate | Low |
| Flood dynamics | Well captured | Diffusive |

---

### 2.11 When to use the CA model

The Cellular Automata model is recommended when:

- large-scale simulations are required,
- computational speed is a priority,
- only flood extent or approximate depths are needed,
- detailed hydraulic behavior is not critical.

For physically based flood propagation, the **Local Inertial Model remains the preferred option**.

---

## Summary

The Cellular Automata model in HydroPol2D provides a **mass-conservative, gradient-driven routing alternative** that complements the Local Inertial Model.

While less physically detailed, it offers:

- excellent numerical stability,
- low computational cost,
- and robustness for large-domain simulations.