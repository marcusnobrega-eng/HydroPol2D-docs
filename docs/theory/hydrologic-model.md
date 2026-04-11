---
title: Hydrologic Model
---

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

HydroPol2D represents canopy interception using a storage-based interception model in which gross precipitation is partitioned into:

- canopy storage,
- throughfall,
- canopy evaporation,
- and stemflow.

The interception routine receives:

- gross precipitation $P_{\mathrm{gross}}$,
- potential evaporation $E_{\mathrm{p}}$,
- leaf area index $\mathrm{LAI}$,
- previous canopy storage $S_{\mathrm{can,prev}}$,
- canopy storage coefficient $C_{\mathrm{can}}$,

and returns updated canopy storage $S_{\mathrm{can}}$, throughfall $T_{\mathrm{f}}$, evaporation from intercepted water $E_{\mathrm{can}}$, and stemflow $F_{\mathrm{stem}}$.

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

### 2.6 Subgrid rainfall correction for interception

When subgrid and overbank options are active, the precipitation entering the interception module is scaled by the effective wet area:

$$
P_{\mathrm{int}}
=
\Delta P_{\mathrm{agg}}
\,
\frac{\Delta x^2}{C_a}
$$

where:

- $P_{\mathrm{int}}$ is precipitation used by the interception module $[\mathrm{L}]$
- $\Delta P_{\mathrm{agg}}$ is aggregated rainfall depth $[\mathrm{L}]$
- $\Delta x$ is grid resolution $[\mathrm{L}]$
- $C_a$ is effective wetted cell area $[\mathrm{L}^2]$

Otherwise,

$$
P_{\mathrm{int}} = \Delta P_{\mathrm{agg}}
$$

This correction ensures that interception remains consistent with the hydrologically active portion of the cell area under subgrid inundation or partial wetting conditions.

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

---

## 4. Infiltration

The infiltration module computes the transfer of water from the surface to the vadose zone using a Darcy-based formulation coupled with van Genuchten–Mualem constitutive relationships. The formulation is designed to approximate Richards-type unsaturated flow behavior while maintaining compatibility with the storage-based structure of HydroPol2D.

At each time step, infiltration is controlled by three simultaneous constraints:

1. the availability of water at the surface,
2. the hydraulic capacity of the soil,
3. the remaining storage capacity of the vadose zone.

The final infiltration rate is determined as the minimum among these competing limits.

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

The maximum storage available in the vadose zone is then defined as

$$
S_{\mathrm{uz,max}}
=
z_{\mathrm{wt}}
\left(
\theta_{\mathrm{sat}} - \theta_{\mathrm{i}}
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
- $\theta_{\mathrm{i}}$ is initial/reference water content $[-]$
- $\theta_{\mathrm{sat}}$ is saturated water content $[-]$

This formulation ensures that the available storage dynamically responds to groundwater fluctuations. As the water table rises, $z_{\mathrm{wt}}$ decreases and the vadose storage capacity shrinks accordingly.

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

This effective saturation is used to evaluate both matric suction and hydraulic conductivity.

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

The infiltration capacity represents the maximum flux that can be transmitted into the soil given the current hydraulic state. It is computed as

$$
I_{\mathrm{cap}}
=
K(\theta)
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
- $h_{\mathrm{pond}}$ is surface ponding head $[\mathrm{L}]$
- $L_{\mathrm{top}}$ is near-surface resistance length (default $\approx 0.05\,\mathrm{m}$)
- $\Delta h_{\mathrm{max}}$ is maximum driving head difference (typically $1\,\mathrm{m}$)

This formulation accounts for both gravity-driven and capillary-driven infiltration.

---

### 4.6 Supply-limited and storage-limited infiltration

The water available for infiltration is determined from the effective surface water depth. When interception is inactive:

$$
d_{\mathrm{eff}} = d
$$

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

Thus, infiltration is simultaneously **supply-limited**, **capacity-limited**, and **storage-limited**.

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
where:
- $S_{\mathrm{uz,max}}^{\,\mathrm{new}}$ is the updated maximum vadose-zone storage capacity $[\mathrm{L}]$, recomputed at the current time step based on the updated water-table position.
---

## 5. Snow Accumulation, Melt, and Sublimation

When snow modeling is active, precipitation is partitioned into rainfall and snowfall, and snowpack evolution is explicitly tracked through snow water equivalent (SWE), density, and depth.

---

### 5.1 Rain–snow partitioning

Precipitation is partitioned based on air temperature:

$$
P_{\mathrm{snow}} = P_{\mathrm{gross}} f_{\mathrm{snow}}
$$

$$
P_{\mathrm{rain}} = P_{\mathrm{gross}} - P_{\mathrm{snow}}
$$

where $f_{\mathrm{snow}}$ is a temperature-dependent snow fraction $[-]$.

---

### 5.2 Snow water equivalent

The evolution of snow water equivalent is

$$
\mathrm{SWE}_t
=
\mathrm{SWE}_{t-1}
+
P_{\mathrm{snow}}
-
M_{\mathrm{snow}}
-
E_{\mathrm{s}}
$$

where:

- $\mathrm{SWE}$ is snow water equivalent $[\mathrm{L}]$
- $E_{\mathrm{s}}$ is sublimation $[\mathrm{L}]$

---

### 5.3 Snowmelt

Snowmelt is computed as

$$
M_{\mathrm{snow}}
=
\max
\left(
\mathrm{DDF}\,T_{\mathrm{air}}
+
\frac{(1-\alpha_{\mathrm{snow}})\,Q_{\mathrm{net}}}{334},
0
\right)
$$

subject to

$$
M_{\mathrm{snow}} \le \mathrm{SWE}_t
$$

where:

- $\mathrm{DDF}$ is degree-day factor $[\mathrm{L}\,\Theta^{-1}\,\mathrm{T}^{-1}]$
- $\alpha_{\mathrm{snow}}$ is snow albedo $[-]$ that can be either assumed as constant or entered as spatial input in the `General_Data.xlsx`.
- $Q_{\mathrm{net}}$ is net energy flux available for snowmelt $[\mathrm{E}\,\mathrm{L}^{-2}\,\mathrm{T}^{-1}]$, representing the combined radiative and turbulent energy exchanges at the snow surface.

The current snow parameters must be edited in the function `HydroPol2D_Preprocessing.m`.

---

### 5.4 Snow density and depth

Snow density evolves as

$$
\rho_{\mathrm{snow}}^{\,\mathrm{new}}
=
\rho_{\mathrm{snow}}^{\,\mathrm{old}}
+
k_t T_{\mathrm{air}}
+
k_{\mathrm{swe}} \mathrm{SWE}
+
k_D H_{\mathrm{snow}}
$$

subject to

$$
\rho_{\mathrm{snow}} \le \rho_{\mathrm{max}}
$$

Snow depth is

$$
H_{\mathrm{snow}} = \frac{\mathrm{SWE}}{\rho_{\mathrm{snow}}}
$$

---

### 5.5 Sublimation

$$
E_{\mathrm{s}} = C_e\,u\,(q_s - q_a)\,\mathrm{SWE}
$$

where:

- $C_e$ is sublimation coefficient $[-]$
- $u$ is wind speed $[\mathrm{L}\,\mathrm{T}^{-1}]$, taken as the wind speed at $2\,\mathrm{m}$ height.
- $q_s$ is saturation specific humidity at the snow surface $[-]$
- $q_a$ is ambient air specific humidity $[-]$
---

### 5.6 Surface-water update under snow conditions

$$
d_t = d_p + M_{\mathrm{snow}} + P_{\mathrm{rain}}
$$

otherwise

$$
d_t = d_p + P_{\mathrm{eff}}
$$
where:

- $d_t$ is surface water depth at the current time step $[\mathrm{L}]$
- $d_p$ is surface water depth at the previous time step $[\mathrm{L}]$
---

## 6. Vadose Storage, Recharge, and Groundwater Feedback

### 6.1 Recharge

Recharge is computed dynamically using Darcy's law assuming a representative flow width to reach the aquifer free surface

$$
R_{\mathrm{gw}}
=
K(\theta)
\left(
1 + \frac{\psi_{\mathrm{m}}}{L_{\mathrm{gw}}}
\right)
$$

with

$$
L_{\mathrm{gw}} = 0.5\,z_{\mathrm{wt}}
$$

Therefore, the current version considers half of the depth to the aquifer distance as the representative distance to compute the recharge.

---

### 6.2 Storage evolution
By simply computing a reservoir mass balance with a forward explicit Euler numerical scheme, one can obtain:
$$
S_{\mathrm{uz},t+1}
=
S_{\mathrm{uz},t}
+
\Delta t
\left(
i - R_{\mathrm{gw}}
\right)
$$

where $\Delta t$ is in seconds.

---

### 6.3 Mass-consistent recharge

$$
R_{\mathrm{gw}}
=
i
-
\frac{
S_{\mathrm{uz},t+1} - S_{\mathrm{uz},t}
}{\Delta t}
$$

---

### 6.4 Saturation excess

$$
S_{\mathrm{excess}}
=
\max
\left(
S_{\mathrm{uz}} - S_{\mathrm{uz,max}}^{\,\mathrm{new}},
0
\right)
$$

---

### 6.5 Groundwater exfiltration

$$
q_{\mathrm{exf}}
=
\max
\left(
0,\,
h_{\mathrm{gw}} - z_{\mathrm{surf}}
\right)
\frac{S_y}{\Delta t}
$$

where:

- $S_y$ is specific yield $[-]$

---

## 7. Summary

The hydrologic model in HydroPol2D integrates:

- canopy interception,
- Penman–Monteith evapotranspiration,
- Darcy-based infiltration,
- snow accumulation and melt,
- vadose storage and groundwater coupling,

into a unified, mass-consistent framework that resolves vertical water fluxes at the grid-cell scale and provides the hydrologic forcing for the hydrodynamic model.

---