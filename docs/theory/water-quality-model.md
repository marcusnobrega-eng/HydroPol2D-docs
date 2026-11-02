---
title: Water Quality Model
---
import useBaseUrl from '@docusaurus/useBaseUrl';

# Water Quality Model

## 1. Overview

HydroPol2D simulates pollutant transport using a **build-up and wash-off formulation** coupled to the hydrodynamic model.

The model tracks:

- pollutant mass stored on the surface,
- pollutant removal due to flow (wash-off),
- redistribution between neighboring cells,
- export through outlet boundaries.

<p align="center">
  <img src={useBaseUrl('/img/theory/water-quality.svg')} width="720" alt="Three panels. 1: the build-up curve, which rises towards the maximum C1 over the antecedent dry days and falls by wash-off during the storm. 2: one cell whose pollutant mass leaves with the water through each outflow face. 3: a grid of cells shaded by pollutant mass, with fluxes that carry the mass to the outlet, beside the mass balance and the concentration equations" />
</p>

<p align="center">
  <em>Figure 1. The three steps of the mass-based water-quality model. Build-up in dry weather sets the starting mass, wash-off carries it out of each cell through the faces the water leaves by, and transport moves it from cell to cell to the outlet.</em>
</p>

The governing variable is:

$$
B_t
$$

where:

- $B_t$ = pollutant mass per cell $[\mathrm{M}]$

The model is fully **mass conservative** and dynamically coupled to flow routing.

The current validation focuses on the mass-based wash-off mode
(`flag_wq_model = 0`). The validation uses SWMM-style buildup parameter scales
for total suspended solids, but the truth source is an analytical mass-balance
solution rather than a SWMM numerical run or a calibrated field pollutograph.

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

The water quality model uses the discharge $Q$ $[\mathrm{L}^3\,\mathrm{T}^{-1}]$, in $\mathrm{m^3/s}$, that leaves a cell through each face in the routing step. Python takes $Q$ directly from the face discharges of the routing solver.

MATLAB stores the outflows of a grid cell as depth rates over the cell area

$$
q_{\mathrm{out}} = \{ q_{\mathrm{left}}, q_{\mathrm{right}}, q_{\mathrm{up}}, q_{\mathrm{down}}, q_{\mathrm{outlet}} \}
$$

with units

$$
[\mathrm{L}\,\mathrm{T}^{-1}] \quad (\mathrm{mm/h})
$$

and converts each one to a discharge before the wash-off is computed

$$
Q = \frac{q_{\mathrm{out}}}{1000 \cdot 3600} \cdot A_{\mathrm{cell}}
\quad [\mathrm{L}^3\,\mathrm{T}^{-1}]
$$

---

## 4. Wash-off formulation

Two wash-off formulations are implemented.

---

### 4.1 Rating-curve wash-off model

This mode exists only in MATLAB, and only on the regular grid, since a MATLAB mesh run refuses it. Python has only the mass-based mode of section 4.2.

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

Pollutant fluxes are computed for each direction through which water leaves the cell. On the regular grid the directions are

- left
- right
- up
- down
- outlet

MATLAB treats the outlet as a fifth direction of the outlet cells. Python carries the outlet flow on the faces at the edge of the grid, so there the outlet flux is the flux through a boundary face. On a Voronoi or quadtree mesh, both codes use every edge through which water leaves the cell, and an edge on the domain boundary exports the pollutant out of the model.

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

To ensure stability and avoid negative mass, HydroPol2D splits the hydraulic time step into $n$ equal **sub-steps**:

$$
n = \max\!\left(1,\;\left\lceil \Delta t \,\max\!\left(\frac{W_{\mathrm{out,tot}}}{B_t}\right) \right\rceil\right)
\qquad
\Delta t_i = \frac{\Delta t}{n}
$$

where:

- the maximum runs over the cells that hold pollutant ($B_t > 0$),
- $W_{\mathrm{out,tot}}/B_t$ is the gross outflow rate of a cell at the start of the step, without the incoming flux $[\mathrm{T}^{-1}]$,
- $\lceil\cdot\rceil$ rounds up to the next integer.

In each sub-step the wash-off is computed again from the current mass. A cell whose outflow would remove more than it holds has its outflows scaled down so that $W_{\mathrm{out,tot}}\,\Delta t_i \le B_t$. The mass is then updated:

$$
B_t^{i+1} = B_t^i - dW \cdot \Delta t_i
$$

Python and MATLAB both use this scheme. The sub-steps run inside the hydraulic step, so the water quality model does not shorten the model time step.

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
1000 \cdot \frac{W_{\mathrm{out,tot}}}{Q_{\mathrm{tot}}}
\quad [\mathrm{mg/L}]
$$

where:

- $W_{\mathrm{out,tot}}$ = total pollutant outflow of the cell $[\mathrm{kg\,s^{-1}}]$
- $Q_{\mathrm{tot}}$ = total water discharge that leaves the cell $[\mathrm{m^3\,s^{-1}}]$
- the factor 1000 converts $\mathrm{kg\,m^{-3}}$ to $\mathrm{mg/L}$

Python computes $C$ this way and sets $C = 0$ in a cell that no water leaves. On the regular grid, MATLAB computes the same ratio from the depth rates of section 3, as $C = 10^6\, W_{\mathrm{out,tot}} / (q_{\mathrm{out,tot}}\, A_{\mathrm{cell}})$ with $W_{\mathrm{out,tot}}$ in kg/h, the total outflow rate $q_{\mathrm{out,tot}}$ in mm/h and $A_{\mathrm{cell}}$ in m². It uses no less than 10 mm/h for $q_{\mathrm{out,tot}}$ (section 12).

---

## 10. Outlet concentration

The outlet concentration is computed as:

$$
C_{\mathrm{out}} =
1000 \cdot
\frac{
\sum W_{\mathrm{out, outlet}}
}{
\sum Q_{\mathrm{outlet}}
}
\quad [\mathrm{mg/L}]
$$

where the sums run over the faces through which water leaves the domain, $W_{\mathrm{out,outlet}}$ is the pollutant flux through such a face averaged over the time step $[\mathrm{kg\,s^{-1}}]$, and $Q_{\mathrm{outlet}}$ is the water discharge through it $[\mathrm{m^3\,s^{-1}}]$. On the regular grid, MATLAB computes the same ratio as the pollutant mass that reaches the outlet in the time step, in kg, divided by the outlet water volume of the step, in litres, times $10^6$.

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

- a minimum flow for the cell concentration, in MATLAB on the regular grid only:

$$
q_{\mathrm{out,tot}} \ge 10 \quad [\mathrm{mm/h}]
$$

MATLAB applies this floor only to the total outflow rate in the denominator of the cell concentration of section 9, so a cell with very little outflow does not report a very large concentration. It does not change the wash-off, the mass balance or the outlet concentration. Python has no such floor, and its cells that no water leaves have $C = 0$.

---

## Summary

The HydroPol2D water quality model:

- tracks pollutant mass per cell,
- computes wash-off as a function of flow and storage,
- redistributes pollutants across the domain,
- ensures strict mass conservation,
- uses adaptive time stepping to maintain stability.

It provides a robust and flexible framework for simulating pollutant transport coupled with hydrologic and hydrodynamic processes. Current validation evidence supports controlled buildup/washoff mass-balance behavior; site-specific pollutant prediction still requires local pollutant parameters, observations, and calibration.
