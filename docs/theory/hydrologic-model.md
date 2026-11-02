---
title: Hydrologic Model
---
import useBaseUrl from '@docusaurus/useBaseUrl';

# Hydrologic Model

The hydrologic component of HydroPol2D governs the partitioning of atmospheric input into interception, throughfall, infiltration, evapotranspiration, snow accumulation and melt, vadose-zone storage, groundwater recharge, and groundwater feedback to the land surface.

At the cell scale, the hydrologic model determines how much water:

- is temporarily stored by the canopy,
- reaches the ground surface,
- infiltrates into the soil,
- remains stored in the vadose zone,
- recharges groundwater,
- returns to the surface through exfiltration,
- or is removed by evaporation and transpiration.

These processes are evaluated sequentially within each time step and provide the hydrologic forcing for the hydrodynamic model.

---

## 1. Conceptual Hydrologic Balance

At the conceptual level, the hydrologic balance of a grid cell may be written as

$$
\frac{\partial d}{\partial t}
=
P_{\mathrm{eff}}
+
M_{\mathrm{snow}}
+
q_{\mathrm{exf}}
-
i
-
E_{\mathrm{surf}}
-
T_{\mathrm{r}}
+
q_{\mathrm{src}}
-
q_{\mathrm{sink}}
$$

where:

- $d$ is surface water depth $[\mathrm{L}]$
- $P_{\mathrm{eff}}$ is effective rainfall reaching the ground $[\mathrm{L}\,\mathrm{T}^{-1}]$
- $M_{\mathrm{snow}}$ is snowmelt contribution $[\mathrm{L}\,\mathrm{T}^{-1}]$
- $q_{\mathrm{exf}}$ is groundwater exfiltration to the surface $[\mathrm{L}\,\mathrm{T}^{-1}]$
- $i$ is infiltration rate $[\mathrm{L}\,\mathrm{T}^{-1}]$
- $E_{\mathrm{surf}}$ is evaporation rate from surface storage $[\mathrm{L}\,\mathrm{T}^{-1}]$
- $T_{\mathrm{r}}$ is transpiration rate $[\mathrm{L}\,\mathrm{T}^{-1}]$
- $q_{\mathrm{src}}$ and $q_{\mathrm{sink}}$ are additional imposed source and sink terms $[\mathrm{L}\,\mathrm{T}^{-1}]$

Not all terms are active simultaneously. Their activation depends on the selected forcing configuration and model flags. Nevertheless, this balance provides the conceptual framework used to organize all vertical fluxes acting on a grid cell.

---

## 2. Canopy Interception, Throughfall, and Stemflow

HydroPol2D represents canopy interception using a storage-based interception model in which the precipitation that reaches the canopy is partitioned into:

- canopy storage,
- throughfall,
- canopy evaporation,
- and stemflow.

The interception routine receives:

- gross precipitation $P_{\mathrm{gross}}$ when snow modeling is off, and only the rainfall $P_{\mathrm{rain}}$ of Section 5.1 when it is on,
- potential evaporation $E_{\mathrm{p}}$,
- leaf area index $\mathrm{LAI}$,
- previous canopy storage $S_{\mathrm{can,prev}}$,
- canopy storage coefficient $C_{\mathrm{can}}$,

and returns updated canopy storage $S_{\mathrm{can}}$, throughfall $T_{\mathrm{f}}$, evaporation from intercepted water $E_{\mathrm{can}}$, and stemflow $F_{\mathrm{stem}}$.

With snow modeling on, the snow module splits the precipitation before the canopy. The snowfall goes to the snowpack, the melt goes straight to the surface, and $P_{\mathrm{rain}}$ takes the place of $P_{\mathrm{gross}}$ in the equations of this section.

This interception step controls how much of the atmospheric water input is temporarily retained by vegetation and how much is transferred to the ground surface during the current time step.

### 2.1 Maximum canopy storage

The maximum interception storage is computed as

$$
S_{\mathrm{can,max}} = C_{\mathrm{can}} \,\mathrm{LAI}
$$

where:

- $S_{\mathrm{can,max}}$ is maximum canopy water storage $[\mathrm{L}]$
- $C_{\mathrm{can}}$ is canopy storage coefficient $[\mathrm{L}]$
- $\mathrm{LAI}$ is leaf area index $[-]$

This relation implies that vegetation with larger leaf area can store more intercepted water.

### 2.2 Stemflow

The code includes a stemflow routine based on a delay function. The intermediate expressions are

$$
\tau_{\mathrm{stem}}
=
T_0 \exp\!\left(-\alpha_{\mathrm{stem}} P_{\mathrm{gross}}\right)
$$

and

$$
F_{\mathrm{stem}}
=
f_{\mathrm{stem}}
\,
\frac{S_{\mathrm{can,prev}}}{\tau_{\mathrm{stem}}/60}
$$

where:

- $\tau_{\mathrm{stem}}$ is stemflow delay $[\mathrm{T}]$
- $T_0$ is the maximum delay parameter $[\mathrm{T}]$
- $\alpha_{\mathrm{stem}}$ is the stemflow decay coefficient $[-]$
- $f_{\mathrm{stem}}$ is the stemflow fraction $[-]$
- $F_{\mathrm{stem}}$ is stemflow $[\mathrm{L}]$

In the current HydroPol2D implementation, stemflow is deactivated by explicitly imposing

$$
F_{\mathrm{stem}} = 0
$$

Therefore, stemflow does not currently contribute to the surface-water balance, although the structure of the routine is retained in the code.

### 2.3 Evaporation from interception storage

The fraction of canopy storage exposed to evaporation is defined as

$$
\beta = \frac{S_{\mathrm{can,prev}}}{S_{\mathrm{can,max}}}
$$

and the canopy evaporation is then computed as

$$
E_{\mathrm{can}} = \beta \, E_{\mathrm{p}}
$$

subject to the constraint

$$
E_{\mathrm{can}} \le P_{\mathrm{gross}} + S_{\mathrm{can,prev}}
$$

where:

- $\beta$ is the fraction of canopy storage filled at the beginning of the time step $[-]$
- $E_{\mathrm{can}}$ is evaporation from interception storage $[\mathrm{L}]$
- $E_{\mathrm{p}}$ is potential evaporation over the time step $[\mathrm{L}]$

This formulation assumes that canopy evaporation is proportional to the fraction of storage occupied at the beginning of the time step, while also enforcing that evaporation cannot exceed the water actually available in precipitation plus stored interception water.

### 2.4 Interception storage update

The canopy storage increment is computed as

$$
\Delta S_{\mathrm{can}} = P_{\mathrm{gross}} - F_{\mathrm{stem}} - E_{\mathrm{can}}
$$

and the provisional storage becomes

$$
S_{\mathrm{can}}^{\ast} = S_{\mathrm{can,prev}} + \Delta S_{\mathrm{can}}
$$

Throughfall is then computed as the excess above the canopy storage capacity:

$$
T_{\mathrm{f}} = \max\left(S_{\mathrm{can}}^{\ast} - S_{\mathrm{can,max}},\,0\right)
$$

Finally, the canopy storage is truncated at its maximum admissible value:

$$
S_{\mathrm{can}} = \min\left(S_{\mathrm{can}}^{\ast},\,S_{\mathrm{can,max}}\right)
$$

where:

- $\Delta S_{\mathrm{can}}$ is the canopy storage increment over the time step $[\mathrm{L}]$
- $S_{\mathrm{can}}^{\ast}$ is provisional canopy storage before truncation $[\mathrm{L}]$
- $T_{\mathrm{f}}$ is throughfall $[\mathrm{L}]$
- $S_{\mathrm{can}}$ is final canopy storage $[\mathrm{L}]$

This sequence reflects the physical assumption that precipitation first fills canopy storage. Once the canopy reaches its storage capacity, the excess water is released as throughfall.

### 2.5 Effective rainfall passed to the surface

The rainfall available to the land surface is defined as

$$
P_{\mathrm{eff}} = T_{\mathrm{f}} + F_{\mathrm{stem}}
$$

where:

- $P_{\mathrm{eff}}$ is effective rainfall reaching the ground $[\mathrm{L}]$
- $T_{\mathrm{f}}$ is direct throughfall $[\mathrm{L}]$
- $F_{\mathrm{stem}}$ is stemflow $[\mathrm{L}]$

Under the current implementation, since stemflow is deactivated, effective rainfall is equal to throughfall. In practical terms, $P_{\mathrm{eff}}$ represents the amount of liquid water transferred from the atmosphere–canopy system to the land surface during the time step, prior to hydrodynamic routing.

If the interception routine is disabled, then no canopy storage is resolved and precipitation reaches the surface directly, so that

$$
P_{\mathrm{eff}} = P_{\mathrm{gross}}
$$

### 2.6 Rainfall application

For validated applications, precipitation entering the interception module is applied over the active model cell as:

$$
P_{\mathrm{int}} = \Delta P_{\mathrm{agg}}
$$

where $\Delta P_{\mathrm{agg}}$ is the aggregated rainfall depth over the model time step. With snow modeling on, $P_{\mathrm{int}}$ is only the rain part of $\Delta P_{\mathrm{agg}}$, the $P_{\mathrm{rain}}$ of Section 5.1.

---

## 3. Potential Evapotranspiration and Evaporation

HydroPol2D computes spatially distributed reference evapotranspiration using a Penman–Monteith formulation. Meteorological station data are first interpolated over the grid using inverse distance weighting, and the interpolated fields are then used to compute both reference evapotranspiration $\mathrm{ETP}$ and an evaporation-like term $E_{\mathrm{p}}$.

The quantity $\mathrm{ETP}$ is used as the standard reference evapotranspiration, while $E_{\mathrm{p}}$ is used in the interception routine to estimate evaporation from intercepted canopy water.

### 3.1 Spatial interpolation of meteorological forcing

At each time step, the following fields are interpolated from available stations:

- $T_{\mathrm{max}}$ maximum air temperature $[\Theta]$
- $T_{\mathrm{min}}$ minimum air temperature $[\Theta]$
- $T_{\mathrm{air}}$ mean air temperature $[\Theta]$
- $U_2$ wind speed at $2\,\mathrm{m}$ $[\mathrm{L}\,\mathrm{T}^{-1}]$
- $\mathrm{UR}$ relative humidity $[-]$
- $G_{\mathrm{soil}}$ soil heat flux $[\mathrm{E}\,\mathrm{L}^{-2}\,\mathrm{T}^{-1}]$

For a generic variable $\phi$, the interpolated field at location $\mathbf{x}$ is written conceptually as

$$
\phi(\mathbf{x})
=
\frac{
\sum_{i=1}^{N} w_i(\mathbf{x})\,\phi_i
}{
\sum_{i=1}^{N} w_i(\mathbf{x})
}
$$

with

$$
w_i(\mathbf{x}) \propto \frac{1}{d_i(\mathbf{x})^p}
$$

where:

- $\phi_i$ is the value observed at station $i$
- $d_i(\mathbf{x})$ is the distance from station $i$ to location $\mathbf{x}$ $[\mathrm{L}]$
- $p$ is the inverse-distance weighting power parameter $[-]$

Only stations with complete data at the current time step are retained in the interpolation. This procedure yields spatially distributed forcing fields that are then used in the evapotranspiration calculations.

### 3.2 Penman–Monteith equation

The reference evapotranspiration is computed as

$$
\mathrm{ETP}
=
\frac{
0.408\,\Delta\,(R_n - G_{\mathrm{soil}})
+
\gamma
\left(
\frac{900\,U_2\,(e_s - e_a)}{T_{\mathrm{air}} + 273}
\right)
}{
\Delta + \gamma\left(1 + 0.34\,U_2\right)
}
$$

and the evaporation-like term is

$$
E_{\mathrm{p}}
=
\frac{
0.408\,\Delta\,(R_n - G_{\mathrm{soil}})
+
\gamma
\left(
\frac{900\,U_2\,(e_s - e_a)}{T_{\mathrm{air}} + 273}
\right)
}{
\Delta + \gamma
}
$$

where:

- $\mathrm{ETP}$ is reference evapotranspiration $[\mathrm{L}\,\mathrm{T}^{-1}]$
- $E_{\mathrm{p}}$ is potential evaporation without aerodynamic surface resistance in the denominator $[\mathrm{L}\,\mathrm{T}^{-1}]$
- $\Delta$ is the slope of the saturation vapor pressure curve $[\mathrm{P}\,\Theta^{-1}]$
- $R_n$ is net radiation $[\mathrm{E}\,\mathrm{L}^{-2}\,\mathrm{T}^{-1}]$
- $G_{\mathrm{soil}}$ is soil heat flux $[\mathrm{E}\,\mathrm{L}^{-2}\,\mathrm{T}^{-1}]$
- $\gamma$ is the psychrometric constant $[\mathrm{P}\,\Theta^{-1}]$
- $U_2$ is wind speed at $2\,\mathrm{m}$ $[\mathrm{L}\,\mathrm{T}^{-1}]$
- $e_s$ is saturation vapor pressure $[\mathrm{P}]$
- $e_a$ is actual vapor pressure $[\mathrm{P}]$
- $T_{\mathrm{air}}$ is mean air temperature $[\Theta]$

These are the algebraic forms implemented in the current code. The difference between $\mathrm{ETP}$ and $E_{\mathrm{p}}$ lies in the denominator, which makes $E_{\mathrm{p}}$ an evaporation-like term more directly suited to canopy interception losses.

### 3.3 Supporting radiation and atmospheric terms

HydroPol2D computes the auxiliary Penman–Monteith terms using astronomical and thermodynamic relationships.

Solar declination is computed as

$$
\delta_{\mathrm{sol}}
=
0.409
\sin\!\left(
\frac{2\pi}{365}J - 1.39
\right)
$$

Relative Earth–Sun distance is

$$
d_r = 1 + 0.033\cos\!\left(\frac{2\pi}{365}J\right)
$$

Extraterrestrial radiation is then computed as

$$
R_a
=
\frac{118.08}{\pi}
d_r
\left[
\omega_s \sin\phi \sin\delta_{\mathrm{sol}}
+
\cos\phi \cos\delta_{\mathrm{sol}} \sin\omega_s
\right]
$$

Incoming solar radiation is estimated as

$$
R_s = K_{\mathrm{rs}} R_a \sqrt{T_{\mathrm{max}} - T_{\mathrm{min}}}
$$

Clear-sky radiation is

$$
R_{\mathrm{so}}
=
\left(
0.75 + 2\times10^{-5} z
\right) R_a
$$

Net shortwave radiation is

$$
R_{\mathrm{ns}} = (1-\alpha_{\mathrm{land}})\,R_s
$$

Net longwave radiation is

$$
R_{\mathrm{nl}}
=
\sigma
\left(
\frac{
(T_{\mathrm{max}}+273.16)^4 + (T_{\mathrm{min}}+273.16)^4
}{2}
\right)
\left(
0.34 - 0.14\sqrt{e_a}
\right)
\left(
1.35\frac{R_s}{R_{\mathrm{so}}} - 0.35
\right)
$$

Net radiation is then

$$
R_n = R_{\mathrm{ns}} - R_{\mathrm{nl}}
$$

The slope of the saturation vapor pressure curve is computed as

$$
\Delta
=
\frac{
4098
\left[
0.6108\exp\!\left(
\frac{17.27\,T_{\mathrm{air}}}{T_{\mathrm{air}}+237.3}
\right)
\right]
}{
(T_{\mathrm{air}}+237.3)^2
}
$$

Atmospheric pressure is estimated as

$$
P_{\mathrm{atm}}
=
101.3
\left(
\frac{293 - 0.0065 z}{293}
\right)^{5.26}
$$

and the psychrometric constant is

$$
\gamma = 0.665 \times 10^{-3} P_{\mathrm{atm}}
$$

where:

- $J$ is day of year $[-]$
- $\delta_{\mathrm{sol}}$ is solar declination $[\mathrm{rad}]$
- $d_r$ is relative Earth–Sun distance $[-]$
- $R_a$ is extraterrestrial radiation $[\mathrm{E}\,\mathrm{L}^{-2}\,\mathrm{T}^{-1}]$
- $\omega_s$ is sunrise hour angle $[\mathrm{rad}]$
- $\phi$ is latitude $[\mathrm{rad}]$
- $R_s$ is incoming solar radiation $[\mathrm{E}\,\mathrm{L}^{-2}\,\mathrm{T}^{-1}]$
- $K_{\mathrm{rs}}$ is the empirical radiation coefficient in the Hargreaves-type incoming radiation estimate $[-]$
- $R_{\mathrm{so}}$ is clear-sky solar radiation $[\mathrm{E}\,\mathrm{L}^{-2}\,\mathrm{T}^{-1}]$
- $z$ is the terrain elevation $[\mathrm{L}]$
- $R_{\mathrm{ns}}$ is net shortwave radiation $[\mathrm{E}\,\mathrm{L}^{-2}\,\mathrm{T}^{-1}]$
- $\alpha_{\mathrm{land}}$ is land-surface albedo $[-]$
- $R_{\mathrm{nl}}$ is net longwave radiation $[\mathrm{E}\,\mathrm{L}^{-2}\,\mathrm{T}^{-1}]$
- $\sigma$ is the Stefan–Boltzmann constant
- $P_{\mathrm{atm}}$ is atmospheric pressure $[\mathrm{P}]$

These expressions are explicitly implemented in the evapotranspiration routine and evaluated in matrix form over the computational domain.

### 3.4 Direct evaporation and transpiration forcing

HydroPol2D can also use externally supplied raster fields of evaporation and transpiration. In that configuration, the model bypasses the internal Penman–Monteith calculation and applies prescribed $E_{\mathrm{surf}}$ and $T_{\mathrm{r}}$ fields directly in the hydrologic mass balance.

### 3.5 Feddes root-water-uptake stress

Feddes stress is optional. It reduces soil transpiration when the root zone is too wet or too dry (Feddes, Kowalik and Zaradny, 1978, *Simulation of Field Water Use and Crop Yield*, Pudoc, Wageningen).

| Model | Switch | Default |
|---|---|---|
| HydroPol2D-Python | `vertical.feddes.enabled: true` | off |
| HydroPol2D (MATLAB) | `flag_feddes = 1` | `0` |

It works in both subsurface schemes (default and [layered](./layered-subsurface)), on the structured grid and on the Voronoi mesh.

The reduction factor $\alpha$ is a piecewise-linear function of the matric head $h$ (m, negative):

$$
\alpha(h)
=
\begin{cases}
0, & h > h_1 \\
\dfrac{h_1 - h}{h_1 - h_2}, & h_2 < h \le h_1 \\
1, & h_3 \le h \le h_2 \\
\dfrac{h - h_4}{h_3 - h_4}, & h_4 < h < h_3 \\
0, & h \le h_4
\end{cases}
$$

| Head | Meaning | Default (m) |
|---|---|---:|
| $h_1$ | Wetter than this: no uptake (no air for the roots) | −0.1 |
| $h_2$ | Start of unstressed uptake | −0.25 |
| $h_3$ | End of unstressed uptake | −4.0 |
| $h_4$ | Wilting point: no uptake | −80 |

The heads must satisfy $0 \ge h_1 > h_2 \ge h_3 > h_4$. The head of each layer comes from its van Genuchten curve and its current water content.

**Demand-dependent $h_3$ (optional).** As in SWAP, $h_3$ can depend on the potential transpiration rate $T_p$. $h_{3,\mathrm{high}}$ applies at $T_p \ge 5$ mm/day, $h_{3,\mathrm{low}}$ at $T_p \le 1$ mm/day, and $h_3$ is interpolated linearly between them. Both default to $h_3$, so the option is off unless they are set.

**Uptake.** Root density is uniform over the root depth $z_r$. Each rooted layer is asked for its share of the demand, reduced by its own $\alpha$:

$$
S_\ell = \alpha(h_\ell)\,T_p\,\frac{z_{r,\ell}}{z_r}
$$

where $z_{r,\ell}$ is the rooted thickness of layer $\ell$. Each take is limited by the water available in that layer. There is no compensation: demand that one layer cannot meet is not moved to another layer.

| Setting | HydroPol2D-Python | HydroPol2D (MATLAB) |
|---|---|---|
| Heads | `vertical.feddes.h1_m`, `h2_m`, `h3_m`, `h4_m` | `feddes_h1_m`, `feddes_h2_m`, `feddes_h3_m`, `feddes_h4_m` |
| Demand-dependent $h_3$ | `vertical.feddes.h3_low_m`, `h3_high_m` | `feddes_h3_low_m`, `feddes_h3_high_m` |

---

## 4. Infiltration

The infiltration module computes the transfer of water from the surface to the vadose zone using a Darcy-based formulation coupled with van Genuchten–Mualem constitutive relationships. The formulation is designed to approximate Richards-type unsaturated flow behavior while maintaining compatibility with the storage-based structure of HydroPol2D.

At each time step, infiltration is controlled by three simultaneous constraints:

1. the availability of water at the surface,
2. the hydraulic capacity of the soil,
3. the remaining storage capacity of the vadose zone.

The final infiltration rate is determined as the minimum among these competing limits.

### Current layered vadose structure

The current implementation represents the soil and shallow groundwater column with four conceptual zones:

- a near-surface layer, with a default target thickness of $0.05\,\mathrm{m}$ (HydroPol2D-Python takes it from the soil-table length $L_{\mathrm{top}}$ of Section 4.5, and the MATLAB code fixes it at $0.05\,\mathrm{m}$);
- a root-zone layer, whose depth is assigned from land use / land cover;
- a transmission-zone layer, which occupies any remaining vadose thickness below the root zone;
- a groundwater zone, whose top is the current water-table depth.

The layer geometry is recomputed from soil depth, land-surface elevation, and groundwater head. The fallback rules are intentionally conservative:

- if the LULC root depth is shallower than the near-surface target, the explicit root-zone layer collapses and roots are represented within the near-surface layer;
- if bedrock is shallower than the requested root depth, root depth is truncated to available soil depth;
- if the water table is shallower than the requested root depth, vadose root storage is truncated at the water table;
- if the water table reaches the surface, all vadose layers have zero thickness and groundwater feedback occurs through saturation/exfiltration logic.

The same base soil hydraulic parameters are assigned to the near-surface, root-zone, and transmission-zone layers, while saturated hydraulic conductivity can be adjusted by layer multipliers:

- `Ks_multiplier_near_surface`,
- `Ks_multiplier_root_zone`,
- `Ks_multiplier_transmission`.

This keeps the parameterization practical: the soil table defines the base physical soil behavior, LULC defines root-zone depth, and multipliers allow vertical contrasts when data or calibration support them.

---

### 4.1 Water-table-controlled unsaturated storage

The vertical structure of the soil column is dynamically linked to the groundwater table. The saturated thickness above the base of the soil profile is computed as

$$
z_{\mathrm{gw}}
=
h_{\mathrm{gw}}
-
\left(
z_{\mathrm{surf}} - D_{\mathrm{soil}}
\right)
$$

and the depth to the water table below the land surface is

$$
z_{\mathrm{wt}}
=
D_{\mathrm{soil}} - z_{\mathrm{gw}}
$$

where:

- $h_{\mathrm{gw}}$ is groundwater head $[\mathrm{L}]$
- $z_{\mathrm{surf}}$ is land surface elevation $[\mathrm{L}]$
- $D_{\mathrm{soil}}$ is soil depth $[\mathrm{L}]$
- $z_{\mathrm{wt}}$ is water-table depth below the surface $[\mathrm{L}]$

Under the current implementation, vadose storage is tracked as **active water above residual content**. The conceptual maximum storage available in the unsaturated zone is therefore

$$
S_{\mathrm{uz,max}}
=
z_{\mathrm{wt}}
\left(
\theta_{\mathrm{sat}} - \theta_{\mathrm{r}}
\right)
$$

and the remaining storage capacity is

$$
S_{\mathrm{uz,rem}}
=
\max\left(
S_{\mathrm{uz,max}} - S_{\mathrm{uz}},\,0
\right)
$$

where:

- $S_{\mathrm{uz,max}}$ is maximum vadose storage $[\mathrm{L}]$
- $S_{\mathrm{uz}}$ is current vadose storage $[\mathrm{L}]$
- $\theta_{\mathrm{r}}$ is residual water content $[-]$
- $\theta_{\mathrm{sat}}$ is saturated water content $[-]$

This formulation ensures that the available storage dynamically responds to groundwater fluctuations. As the water table rises, $z_{\mathrm{wt}}$ decreases and the vadose storage capacity shrinks accordingly. In the default layered implementation, this same logic is applied through the summed capacities of the near-surface, root-zone, and transmission-zone stores after truncation by the current water-table position.

---

### 4.2 Representative water content and effective saturation

The representative volumetric water content in the vadose zone is approximated as

$$
\theta
=
\theta_{\mathrm{r}} + \frac{S_{\mathrm{uz}}}{z_{\mathrm{wt}}}
$$

subject to

$$
\theta_{\mathrm{r}} \le \theta \le \theta_{\mathrm{sat}}
$$

The effective saturation is then defined as

$$
S_{\mathrm{e}}
=
\frac{
\theta - \theta_{\mathrm{r}}
}{
\theta_{\mathrm{sat}} - \theta_{\mathrm{r}}
}
$$

where:

- $\theta$ is volumetric water content $[-]$
- $\theta_{\mathrm{r}}$ is residual water content $[-]$
- $S_{\mathrm{e}}$ is effective saturation $[-]$

This effective saturation is used to evaluate both matric suction and hydraulic conductivity. In the default layered implementation, the same constitutive form is evaluated separately for each vadose layer; the single-state expression above is the conceptual equivalent for the legacy fallback formulation.

---

### 4.3 Matric pressure head

The matric pressure head is computed using the van Genuchten retention curve:

$$
\psi_{\mathrm{m}}
=
-\frac{1}{\alpha_{\mathrm{vg}}}
\left(
S_{\mathrm{e}}^{-1/m} - 1
\right)^{1/n}
$$

with

$$
m = 1 - \frac{1}{n}
$$

where:

- $\psi_{\mathrm{m}}$ is matric pressure head $[\mathrm{L}]$
- $\alpha_{\mathrm{vg}}$ is inverse air-entry parameter $[\mathrm{L}^{-1}]$
- $n$ is van Genuchten shape parameter $[-]$

At near-saturated conditions, the model imposes

$$
\psi_{\mathrm{m}} = 0
$$

to prevent numerical instability.

---

### 4.4 Unsaturated hydraulic conductivity

The unsaturated hydraulic conductivity is computed as

$$
K(\theta) = K_{\mathrm{sat}} K_r
$$

with

$$
K_r
=
S_{\mathrm{e}}^{\ell}
\left[
1 - \left(1 - S_{\mathrm{e}}^{1/m}\right)^m
\right]^2
$$

where:

- $K(\theta)$ is unsaturated hydraulic conductivity $[\mathrm{L}\,\mathrm{T}^{-1}]$
- $K_{\mathrm{sat}}$ is saturated hydraulic conductivity $[\mathrm{L}\,\mathrm{T}^{-1}]$
- $\ell$ is pore-connectivity parameter $[-]$

If $\ell$ is not provided, a default value of $\ell = 0.5$ is used.

---

### 4.5 Darcy-based infiltration capacity

The infiltration capacity represents the maximum flux that can be transmitted into the soil given the current hydraulic state. In the current code, this is not based on a single $K(\theta)$ value alone. Instead, HydroPol2D uses:

- a representative bucket suction $\psi_{\mathrm{m}}$ based on the current storage of the near-surface layer, so that $\theta$ and $\psi_{\mathrm{m}}$ below are those of that layer (only the legacy single-store fallback uses the whole vadose storage of Section 4.2),
- a within-step near-surface wetting predictor,
- and a weighted near-surface conductivity that blends saturated entry conductivity with the conductivity of the wetted top layer.

The temporary wetting predictor is

$$
w_{\mathrm{wet}}
=
\min\!\left(
d_{\mathrm{eff}},\,
S_{\mathrm{uz,rem}},\,
S_{\mathrm{top,def}}
\right)
$$

$$
\theta_{\mathrm{top}}
=
\min\!\left(
\theta_{\mathrm{sat}},\,
\theta + \frac{w_{\mathrm{wet}}}{L_{\mathrm{top}}}
\right)
$$

where:

- $w_{\mathrm{wet}}$ is the within-step candidate wetting depth $[\mathrm{L}]$
- $S_{\mathrm{top,def}}$ is the remaining storage deficit of the near-surface layer $[\mathrm{L}]$
- $\theta_{\mathrm{top}}$ is the predicted water content at the bottom of the near-surface layer $[-]$

The effective entry conductivity is then evaluated as

$$
K_{\mathrm{soil}}
=
w_K K_{\mathrm{sat}}
+
\left(1-w_K\right) K(\theta_{\mathrm{top}})
$$

where $w_K$ is the near-surface conductivity weight. The infiltration capacity is then computed as

$$
I_{\mathrm{cap}}
=
K_{\mathrm{soil}}
\left[
\frac{
\min\!\left(
h_{\mathrm{pond}} - \psi_{\mathrm{m}},\,
\Delta h_{\mathrm{max}}
\right)
}{
L_{\mathrm{top}}
}
+
1
\right]
$$

where:

- $I_{\mathrm{cap}}$ is infiltration capacity $[\mathrm{L}\,\mathrm{T}^{-1}]$
- $h_{\mathrm{pond}}$ is surface ponding head, equal to $d_{\mathrm{eff}}$ of Section 4.6 $[\mathrm{L}]$
- $L_{\mathrm{top}}$ is near-surface resistance length (default $\approx 0.05\,\mathrm{m}$)
- $\Delta h_{\mathrm{max}}$ is maximum driving head difference (typically $1\,\mathrm{m}$)

This formulation accounts for both gravity-driven and capillary-driven infiltration while also approximating rapid wetting at the surface boundary. The wetting predictor does **not** add water to the soil state by itself; only the accepted infiltration flux updates vadose storage.

---

### 4.6 Supply-limited and storage-limited infiltration

The water available for infiltration is determined from the effective surface water depth. It is the ponded depth at the start of the step plus the water that reaches the ground during the step,

$$
d_{\mathrm{eff}} = d + P_{\mathrm{eff}} + M_{\mathrm{snow}}
$$

where $P_{\mathrm{eff}}$ is this step's rain on the ground from Section 2.5 (the throughfall $T_{\mathrm{f}}$ when interception is on, the rain itself when it is off) and $M_{\mathrm{snow}}$ is this step's snowmelt, zero when snow modeling is off.

The corresponding supply-limited infiltration rate is

$$
i_{\mathrm{sup}} = \frac{d_{\mathrm{eff}}}{\Delta t_{\mathrm{h}}}
$$

where:

- $d_{\mathrm{eff}}$ is effective ponded water depth $[\mathrm{L}]$
- $\Delta t_{\mathrm{h}}$ is time step in hours $[\mathrm{T}]$

The storage-limited infiltration rate is

$$
i_{\mathrm{store}} = \frac{S_{\mathrm{uz,rem}}}{\Delta t_{\mathrm{h}}}
$$

The actual infiltration rate is then

$$
i = \min\!\left(i_{\mathrm{sup}},\,I_{\mathrm{cap}},\,i_{\mathrm{store}}\right)
$$

Additional constraints are applied:

- $i = 0$ over impervious cells  
- $i = 0$ when $z_{\mathrm{wt}} \le 0$

Thus, infiltration is simultaneously **supply-limited**, **capacity-limited**, and **storage-limited**. In layered mode, acceptance is additionally constrained by the explicit near-surface storage deficit before water can continue to drain downward through the deeper vadose layers.

<p align="center">
  <img src={useBaseUrl('/img/theory/infiltration-limits.svg')} width="720" alt="Three soil columns of one cell, each a case where one limit is the smallest: light rain on a dry soil, limited by the supply; a deep pond on a soil of low conductivity, limited by the Darcy capacity; and a shallow water table, limited by the storage room; under each column, the definition of that limit and where its terms come from" />
</p>

<p align="center">
  <em>Figure 1. The three limits on infiltration, each shown in a case where it is the smallest (schematic, not to scale). The water that does not infiltrate stays on the surface and is routed to the neighbour cells.</em>
</p>

---

### 4.7 Vadose storage update

The infiltrated depth over the time step is

$$
\Delta I = i\,\Delta t_{\mathrm{h}}
$$

and the vadose storage is updated as

$$
S_{\mathrm{uz}}^{\,\mathrm{new}} = S_{\mathrm{uz}} + \Delta I
$$

subject to

$$
0 \le S_{\mathrm{uz}}^{\,\mathrm{new}} \le S_{\mathrm{uz,max}}
$$

In the default layered implementation, the accepted infiltration first fills the near-surface store and the total vadose storage is then synchronized across:

- near-surface storage,
- root-zone storage,
- transmission-zone storage.

The scalar expression above is therefore the conceptual summary of a layered update rather than the only internal representation.

---

## 5. Snow Accumulation, Melt, and Sublimation

When snow modeling is active, HydroPol2D tracks snow water equivalent (SWE), snow density, and physical snow depth in every active grid cell. Snow parameters are read from the LULC parameter table and mapped to the grid from `LULC_Index`. The internal meteorological forcing pathway provides mean air temperature, minimum air temperature, and wind speed. Snow simulations therefore require `flag_ETP = 1`, `flag_input_ETP_map = 0`, and a meteorological workbook that covers the simulation period.

<p align="center">
  <img src={useBaseUrl('/img/theory/snow.svg')} width="720" alt="Left, one time step in one cell: the air temperature splits precipitation into snow and rain; the snow builds a snowpack that loses melt to the surface water and sublimation to the atmosphere, and the rain passes through the canopy store when interception is on. Right, the equations of Section 5. Bottom left, an illustration of air temperature, precipitation and SWE with synthetic forcing" />
</p>

<p align="center">
  <em>Figure 2. Rain or snow, storage, melt and sublimation in one cell. Only the rain enters the canopy store, the melt goes straight to the surface water, and the bottom panel uses synthetic forcing, not model output.</em>
</p>

---

### 5.1 Rain-snow partitioning

Each LULC class supplies an all-snow threshold $T_{\mathrm{snow}}$ and an all-rain threshold $T_{\mathrm{rain}}$, both in $^{\circ}\mathrm{C}$. The snow fraction is

$$
f_{\mathrm{snow}}
=
\begin{cases}
1, & T_{\mathrm{air}} \le T_{\mathrm{snow}} \\
\dfrac{T_{\mathrm{rain}}-T_{\mathrm{air}}}{T_{\mathrm{rain}}-T_{\mathrm{snow}}}, & T_{\mathrm{snow}} < T_{\mathrm{air}} < T_{\mathrm{rain}} \\
0, & T_{\mathrm{air}} \ge T_{\mathrm{rain}}.
\end{cases}
$$

The thresholds must satisfy $T_{\mathrm{rain}} \ge T_{\mathrm{snow}}$. Equal thresholds give a step partition at that temperature. The resulting snowfall and rainfall are

$$
P_{\mathrm{snow}}=P_{\mathrm{gross}}f_{\mathrm{snow}}
$$

$$
P_{\mathrm{rain}}=P_{\mathrm{gross}}-P_{\mathrm{snow}}
$$

where $f_{\mathrm{snow}}$ is the temperature-dependent snow fraction.

The partition comes before the canopy. Only the rainfall $P_{\mathrm{rain}}$ enters the interception model of Section 2, in place of $P_{\mathrm{gross}}$; the snowfall goes to the snowpack, and the melt $M_{\mathrm{snow}}$ reaches the surface without passing through the canopy.

---

### 5.2 Snow water equivalent

The SWE balance is

$$
\mathrm{SWE}_t=\mathrm{SWE}_{t-1}+P_{\mathrm{snow}}-M_{\mathrm{snow}}-E_{\mathrm{s}}
$$

where all terms are in millimeters of water equivalent and $E_{\mathrm{s}}$ is sublimation.

---

### 5.3 Snowmelt and timestep scaling

Snowmelt is the sum of degree-day and positive net-radiation terms. For a routing step of $\Delta t_s$ seconds and $\Delta t_d=\Delta t_s/86400$ days,

$$
M_{\mathrm{snow}}
=
\min\!\left[
\mathrm{SWE}_{\mathrm{after\ snowfall}},
\max\!\left(
\mathrm{DDF}\max(T_{\mathrm{air}},0)\Delta t_d+
\frac{\max(Q_{\mathrm{net}},0)\Delta t_s}{L_f},
0\right)\right]
$$

Here, $\mathrm{DDF}$ is the LULC-specific degree-day factor $[\mathrm{mm\,^{\circ}C^{-1}\,day^{-1}}]$, $Q_{\mathrm{net}}$ is the internally calculated net-radiation flux $[\mathrm{W\,m^{-2}}]$, and $L_f=3.34\times10^5\ \mathrm{J\,kg^{-1}}$ is the latent heat of fusion. A flux of $1\ \mathrm{kg\,m^{-2}}$ gives $1\ \mathrm{mm}$ of water equivalent. Melt cannot exceed available SWE.

---

### 5.4 Snow density and depth

Fresh snow uses the LULC-specific initial density $\rho_{\mathrm{init}}$. Existing and new snow are mixed by SWE before compaction. Density then evolves as

$$
\rho_{\mathrm{snow}}^{\,\mathrm{new}}=
\rho_{\mathrm{snow}}^{\,\mathrm{mixed}}+
\Delta t_d\left[
k_t\max(T_{\mathrm{air}},0)+
k_{\mathrm{swe}}\mathrm{SWE}+
k_DH_{\mathrm{snow}}\right]
$$

with $\rho_{\mathrm{init}}\le\rho_{\mathrm{snow}}\le\rho_{\mathrm{max}}$. Snow depth is

$$
H_{\mathrm{snow}}=\frac{1000\,\mathrm{SWE}}{\rho_{\mathrm{snow}}}
$$

---

The factor 1000 converts water-equivalent depth to physical snow depth when SWE is in millimeters and density is in $\mathrm{kg\,m^{-3}}$.

### 5.5 Sublimation

$$
E_{\mathrm{s}}
=
\min\!\left[
\mathrm{SWE}_{\mathrm{after\ melt}},
\max\!\left(
C_eu(q_s-q_a)\mathrm{SWE}_{\mathrm{after\ melt}}\Delta t_d,
0
\right)\right]
$$

Here, $C_e$ is the LULC-specific sublimation coefficient, $u$ is wind speed $[\mathrm{m\,s^{-1}}]$, and $q_s$ and $q_a$ are saturation and ambient specific humidity. The current implementation estimates $q_a$ from the available temperature fields. Sublimation is nonnegative and cannot exceed post-melt SWE.

---

### 5.6 Initial snow states and class-code fallback

`Initial_SWE_path` and `Initial_Snow_Depth_path` are optional rasters. With neither raster, the model initializes zero SWE and zero snow depth, and retains the LULC-specific fresh-snow density. With one raster, the other state is derived from that density. With both rasters, the model derives density from SWE and depth and rejects positive pairs outside the configured density range. Raster nodata means that no initial snow was specified for that cell.

If the LULC raster contains a valid code that is absent from the LULC, soil, or snow table, HydroPol2D assigns the area-weighted mean of properties from mapped cells. The model writes `Input_Class_Code_Audit.csv`, which lists raster codes, mapped table indices, fallback area, and the properties applied. Duplicate or non-numeric table indices, or a table with no mapped classes, remain input errors.

### 5.7 Surface-water update under snow conditions

$$
d_t=d_p+M_{\mathrm{snow}}+P_{\mathrm{eff}}
$$

where $P_{\mathrm{eff}}$ is the rain that reaches the ground (Section 2.5) when $P_{\mathrm{rain}}$ is the input. With interception on, it is the throughfall $T_{\mathrm{f}}$ that the canopy releases from $P_{\mathrm{rain}}$. With interception off, $P_{\mathrm{eff}}=P_{\mathrm{rain}}$.

If snow modeling is off,

$$
d_t=d_p+P_{\mathrm{eff}},
$$
where $d_t$ and $d_p$ are current and previous surface-water depth.

---

## 6. Vadose Storage, Recharge, and Groundwater Feedback

### 6.1 Default layered vadose structure

The current default formulation is a **layered vadose system**, not a single recharge bucket. Water is tracked in:

- a near-surface layer,
- a root-zone layer,
- a transmission layer,
- and a groundwater-coupling interface below the transmission layer.

For a generic vadose layer $\ell$ with active storage $S_{\ell}$ (water above $\theta_{\mathrm{r}}$, as a depth over the whole cell) and thickness $z_{\ell}$, the water sits in the pervious fraction $f_p$ of the cell:

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
K_{\mathrm{sat},\ell} K_r(S_{e,\ell})
$$

The layer starts at $S_{\ell} = f_p(\theta_i - \theta_{\mathrm{r},\ell})\, z_{\ell}$ and holds at most $f_p(\theta_{\mathrm{sat},\ell} - \theta_{\mathrm{r},\ell})\, z_{\ell}$. Over a time step $\Delta t$ it drains $f_p K_{\ell} \Delta t$ to the layer below, subject to the available storage capacity in the receiving layer. (Before 2026-10-26 the initial storage and the drainage left out $f_p$, so partly impervious cells started too wet and drained too slowly.)

### 6.2 Downward drainage and recharge

In the default pathway:

1. near-surface drainage moves first to the root zone when root storage exists,
2. root-zone drainage moves to the transmission zone when transmission storage exists,
3. transmission-zone drainage becomes recharge to groundwater.

Conceptually, the groundwater recharge over a time step can be summarized as

$$
R_{\mathrm{gw}}
=
\frac{\Delta S_{\mathrm{trans}\rightarrow\mathrm{gw}}}{\Delta t}
$$

with optional direct drainage from higher layers only where the lower vadose layers are absent. This layered cascade is the canonical HydroPol2D recharge story. The older single-bucket Darcy closure remains available only as a fallback formulation and should not be treated as the default theory path.

### 6.3 Optional capillary rise and asynchronous groundwater coupling

When `flag_capillary_rise = 1`, shallow groundwater can return water upward into available vadose storage. The implemented capillary-rise logic increases with:

- shallower water-table depth,
- larger storage deficit in the receiving layer,
- and larger layer conductivity.

The net vadose-groundwater exchange of each surface-water step is therefore

$$
R_{\mathrm{net}} = R_{\mathrm{down}} - C_{\mathrm{up}}
$$

where:

- $R_{\mathrm{down}}$ is total downward recharge from layered drainage
- $C_{\mathrm{up}}$ is upward capillary-rise exchange

This net exchange changes the water-table heads in every surface-water step. The groundwater scheduler is always asynchronous, and only the lateral groundwater flow, when it is on, waits for it. HydroPol2D-Python and the MATLAB code no longer read the `flag_groundwater_async` setting.

### 6.4 Saturation excess and groundwater exfiltration

After the groundwater update, HydroPol2D recomputes the vadose capacity using the updated water-table position. Any water that no longer fits in the unsaturated zone is returned to the surface as saturation excess:

$$
S_{\mathrm{excess}}
=
\max\!\left(
S_{\mathrm{uz}} - S_{\mathrm{uz,max}}^{\,\mathrm{new}},
0
\right)
$$

Groundwater head that rises above the local surface also generates exfiltration:

$$
q_{\mathrm{exf}}
=
\max\!\left(
0,\,
h_{\mathrm{gw}} - z_{\mathrm{surf}}
\right)
\frac{S_y}{\Delta t}
$$

where $S_y$ is specific yield. The full canonical groundwater formulation, including the asynchronous scheduler and Boussinesq lateral flow solver, is documented on the [Groundwater Model](./groundwater-model) page.

### 6.5 Layered subsurface option

The structure above is the default. The optional [layered subsurface](./layered-subsurface) keeps the three soil stores but places them over regolith slots that reach the depth to bedrock. In that scheme a rising water table fills the empty pore space of the soil and regolith instead of pushing soil water to the surface.

---

## 7. Summary

The hydrologic model in HydroPol2D integrates:

- canopy interception,
- Penman–Monteith evapotranspiration,
- Darcy-based infiltration with weighted near-surface conductivity,
- snow accumulation and melt,
- layered vadose storage and groundwater coupling,
- optional Feddes root-water-uptake stress,

into a unified, mass-consistent framework that resolves vertical water fluxes at the grid-cell scale and provides the hydrologic forcing for the hydrodynamic model.

---
