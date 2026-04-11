---
title: Water Quality Model
---

# Water Quality Model

## 1. Overview

HydroPol2D simulates pollutant transport using a **build-up and wash-off formulation** coupled to the hydrodynamic model.

The model tracks:

- pollutant mass stored on the surface,
- pollutant removal due to flow (wash-off),
- redistribution between neighboring cells,
- export through outlet boundaries.

The governing variable is:

$$
B_t
$$

where:

- $B_t$ = pollutant mass per cell $[\mathrm{M}]$

The model is fully **mass conservative** and dynamically coupled to flow routing.

---

## 2. Pollutant storage

Each cell stores a pollutant mass:

$$
B_t \quad [\mathrm{kg}]
$$

The corresponding areal concentration is:

$$
b = \frac{B_t}{A_{\mathrm{cell}}}
\quad [\mathrm{M}\,\mathrm{L}^{-2}]
$$

where:

- $A_{\mathrm{cell}}$ = cell area $[\mathrm{L}^2]$

Minimum and maximum thresholds are defined:

- $B_{\min}$ → minimum active pollutant mass
- $B_{\max}$ → saturation limit

Below a threshold:

$$
b < b_{\min}
\Rightarrow \text{no wash-off}
$$

---

## 3. Hydrodynamic coupling

The water quality model uses hydrodynamic outflows:

$$
q_{\mathrm{out}} = \{ q_{\mathrm{left}}, q_{\mathrm{right}}, q_{\mathrm{up}}, q_{\mathrm{down}}, q_{\mathrm{outlet}} \}
$$

with units:

$$
[\mathrm{L}\,\mathrm{T}^{-1}] \quad (\mathrm{mm/h})
$$

These are converted internally to volumetric flow:

$$
Q = \frac{q_{\mathrm{out}}}{1000 \cdot 3600} \cdot A_{\mathrm{cell}}
\quad [\mathrm{L}^3\,\mathrm{T}^{-1}]
$$

---

## 4. Wash-off formulation

Two wash-off formulations are implemented.

---

### 4.1 Rating-curve wash-off model

When `flag_wq_model = 1`, the wash-off is:

$$
W_{\mathrm{out}} =
C_3 \, Q^{C_4} \, f(B_t)
$$

where:

- $W_{\mathrm{out}}$ = pollutant mass flux $[\mathrm{M}\,\mathrm{T}^{-1}]$
- $C_3, C_4$ = empirical coefficients
- $Q$ = flow rate $[\mathrm{L}^3\,\mathrm{T}^{-1}]$

The storage correction factor is:

$$
f(B_t) = 1 + \max(B_t - B_r, 0)
$$

where:

- $B_r$ = residual pollutant mass threshold $[\mathrm{M}]$

This formulation ensures that:

- wash-off increases with flow,
- wash-off increases with available pollutant mass.

---

### 4.2 Mass-based wash-off model

When `flag_wq_model = 0`, the formulation becomes:

$$
W_{\mathrm{out}} =
C_3 \, Q^{C_4} \, B_t
$$

This formulation assumes:

- wash-off is proportional to available pollutant mass,
- transport increases with flow magnitude.

---

## 5. Directional pollutant fluxes

Pollutant fluxes are computed for each direction:

- left
- right
- up
- down
- outlet

The total pollutant outflow from a cell is:

$$
W_{\mathrm{out,tot}} = \sum_k W_{\mathrm{out},k}
$$

Incoming pollutant fluxes are computed from neighboring cells:

$$
W_{\mathrm{in}} = \sum_k W_{\mathrm{in},k}
$$

---

## 6. Net pollutant balance

The net pollutant rate is:

$$
dW = W_{\mathrm{out,tot}} - W_{\mathrm{in}}
\quad [\mathrm{M}\,\mathrm{T}^{-1}]
$$

The mass balance equation is:

$$
B_t^{t+\Delta t}
=
B_t^t - dW \cdot \Delta t
$$

This formulation accounts for:

- pollutant removal due to wash-off,
- pollutant redistribution across the grid.

---

## 7. Adaptive time stepping (critical feature)

To ensure stability and avoid negative mass, HydroPol2D computes a **minimum admissible time step**:

$$
\Delta t_{\min}
=
\min \left(
\frac{B_t}{|dW|}
\right)
$$

where:

- only cells losing mass are considered,
- very small values are excluded.

If:

$$
\Delta t_{\min} < \Delta t
$$

the model splits the time step into sub-steps:

$$
\Delta t = \sum \Delta t_i
$$

and updates pollutant mass iteratively:

$$
B_t^{i+1} = B_t^i - dW \cdot \Delta t_i
$$

This ensures:

- no negative pollutant mass,
- numerical stability,
- accurate mass conservation.

---

## 8. Mass conservation and corrections

After updating:

- negative values are removed:

$$
B_t = \max(B_t, 0)
$$

- rounding is applied to avoid numerical noise.

Mass lost due to numerical corrections is tracked:

$$
\mathrm{mass}_{\mathrm{lost}}
$$

---

## 9. Pollutant concentration

Pollutant concentration is computed as:

$$
C =
\frac{W_{\mathrm{out,tot}}}{Q_{\mathrm{tot}} \cdot A_{\mathrm{cell}}}
\cdot 10^6
\quad [\mathrm{mg/L}]
$$

where:

- $Q_{\mathrm{tot}}$ = total water outflow $[\mathrm{L}\,\mathrm{T}^{-1}]$

---

## 10. Outlet concentration

The outlet concentration is computed as:

$$
C_{\mathrm{out}} =
\frac{
\sum W_{\mathrm{out, outlet}}
}{
\sum Q_{\mathrm{outlet}} \cdot A_{\mathrm{cell}}
}
\cdot 1000
\quad [\mathrm{mg/L}]
$$

---

## 11. Total washed mass

The cumulative washed pollutant mass is:

$$
M_{\mathrm{washed}} =
\sum W_{\mathrm{out,tot}} \cdot \Delta t
\quad [\mathrm{kg}]
$$

---

## 12. Numerical constraints

The model enforces:

- minimum pollutant threshold:
  
$$
b < b_{\min} \Rightarrow W_{\mathrm{out}} = 0
$$

- minimum flow threshold:

$$
q_{\mathrm{out}} \ge 10 \quad [\mathrm{mm/h}]
$$

to avoid numerical instability.

---

## Summary

The HydroPol2D water quality model:

- tracks pollutant mass per cell,
- computes wash-off as a function of flow and storage,
- redistributes pollutants across the domain,
- ensures strict mass conservation,
- uses adaptive time stepping to maintain stability.

It provides a robust and flexible framework for simulating pollutant transport coupled with hydrologic and hydrodynamic processes.