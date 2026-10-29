---
title: Human Instability
---

# Human Instability

HydroPol2D includes an implemented human-instability module that uses routed surface depth and velocity to estimate pedestrian hazard. The current public theory should distinguish clearly between the implemented modes:

| Mode | Current state | Description |
|---|---|---|
| `1` | Implemented | Continuous force-balance risk ratio based on buoyancy, available friction, and hydrodynamic drag. |
| `2` | Not implemented | Placeholder only. Do not document or use as an active public option. |
| `3` | Implemented | Geometry-based instability classifier with slide, topple, and drowning/drawing thresholds. |

The current validation status for these modes is tracked in the [validation status](../validation/validation-status).

---

## 1. Inputs and Coupling

The human-instability module reads the hydrodynamic state from HydroPol2D:

- routed surface depth $h$,
- routed velocity magnitude $v$,
- local slope when the geometry-based classifier is used,
- and user-supplied human geometry and resistance parameters.

This means the instability estimates are diagnostic products of the coupled hydrologic-hydrodynamic simulation rather than a standalone hydraulic solver.

---

## 2. Mode 1: Force-Balance Risk Ratio

Mode `1` represents instability as a competition between hydrodynamic forcing and the frictional support that remains after buoyancy reduces body weight.

### 2.1 Weight and buoyancy

The body weight force is

$$
F_{\mathrm{person}} = m_{\mathrm{person}} g
$$

The buoyancy force is approximated as

$$
F_{\mathrm{buoy}}
=
w_1 w_2 h \rho_{\mathrm{w}} g
$$

where:

- $m_{\mathrm{person}}$ is body mass
- $g$ is gravitational acceleration
- $w_1$ and $w_2$ are characteristic body widths
- $h$ is water depth
- $\rho_{\mathrm{w}}$ is water density

### 2.2 Available friction

The friction available to resist motion is

$$
F_{\mathrm{fric}}
=
\mu \max\!\left(
F_{\mathrm{person}} - F_{\mathrm{buoy}},
0
\right)
$$

where $\mu$ is the effective ground-contact friction coefficient.

### 2.3 Hydrodynamic force

The hydrodynamic loading is represented as

$$
F_{\mathrm{hyd}}
=
\max\!\left(
\frac{1}{2} C_d \rho_{\mathrm{w}} w_1 h v^2,
0
\right)
$$

where:

- $C_d$ is drag coefficient
- $v$ is routed velocity magnitude

### 2.4 Risk ratio

The force-balance risk ratio is then

$$
R
=
\frac{F_{\mathrm{hyd}}}{F_{\mathrm{fric}}}
$$

for supported states where $F_{\mathrm{fric}} > 0$. In the current implementation:

- cells with no remaining support but positive water depth are assigned full risk,
- the final risk value is clipped to the range $0 \le R \le 1$,
- and a running maximum-risk map can be accumulated over the simulation.

Mode `1` therefore returns a continuous hazard indicator rather than a categorical failure mode.

---

## 3. Mode 3: Geometry-Based Instability Classifier

Mode `3` uses person geometry, flow depth, flow velocity, and ground slope to classify the dominant failure mechanism.

### 3.1 Submerged geometry and forces

The code computes submerged area, submerged volume, and the submerged centroid as a function of water depth relative to body dimensions. Those geometric quantities are then used to estimate:

- drag and lift-like hydrodynamic loading,
- downslope and normal components of body weight,
- buoyancy,
- and the lever arms needed for overturning.

Conceptually, the main force terms are:

$$
D \propto \frac{1}{2}\rho_{\mathrm{w}} C_d v^2 A_{\mathrm{sub}}
$$

$$
W_p = m g \sin\beta
\qquad
W_n = m g \cos\beta
$$

$$
B_n = \rho_{\mathrm{w}} g V_{\mathrm{sub}} \cos\beta
$$

where:

- $A_{\mathrm{sub}}$ is submerged projected area
- $V_{\mathrm{sub}}$ is submerged volume
- $\beta$ is local slope angle

### 3.2 Sliding threshold

Available resisting friction is approximated as

$$
T = \mu \left(W_n - B_n - L\right)
$$

where $L$ is the lift-like hydrodynamic contribution. Sliding is classified when the driving force exceeds the available friction:

$$
\text{slide if } D + W_p > T
$$

In the output map, slide corresponds to code `1`.

### 3.3 Toppling threshold

The module also computes an overturning moment from drag, buoyancy, and body geometry. Toppling is classified when the driving moment exceeds the resisting moment:

$$
\text{topple if } M > M_{\mathrm{res}}
$$

In the output map, topple corresponds to code `2`.

### 3.4 Drowning/drawing threshold

The implementation also applies a depth-based drowning/drawing threshold:

$$
\text{drowning/drawing if } h > \frac{13}{16} y
$$

where $y$ is the characteristic body height used by the geometry routine. In the output map, this failure mode corresponds to code `3`.

### 3.5 Final categorical map

The final mode-`3` hazard class is the maximum of the slide, topple, and drowning/drawing indicators:

$$
\text{risk class} = \max(\text{slide},\text{topple},\text{drowning/drawing})
$$

This produces a categorical instability raster rather than the continuous ratio returned by mode `1`.

A dry cell ($h = 0$) is stable (code `0`), as in mode `1`: with no water there is no one in the flow to classify. Without this rule, the person's own weight would make every dry cell steeper than $\arctan\mu$ (31° for $\mu = 0.6$) a slide.

---

## 4. Scope and Documentation Notes

The current public story for human instability should stay aligned with the code:

- mode `1` is implemented and documented as a force-balance ratio,
- mode `3` is implemented and documented as a geometry-based classifier,
- mode `2` is not implemented,
- validation claims should remain tied to the controlled evidence summarized on the [validation status](../validation/validation-status),
- and the human-instability module should be described as a coupled hazard diagnostic driven by HydroPol2D depths and velocities.
