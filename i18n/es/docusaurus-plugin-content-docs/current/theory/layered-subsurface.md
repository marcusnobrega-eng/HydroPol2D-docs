---
title: Subsuelo en Capas
---
import useBaseUrl from '@docusaurus/useBaseUrl';

# Subsuelo en Capas (suelo sobre regolito)

## 1. Descripción general {#1-overview}

El subsuelo en capas es una alternativa opcional al esquema de agua subterránea predeterminado descrito en la página [Modelo de aguas subterráneas](./groundwater-model). Reemplaza la columna de suelo de tres capas, en la que el acuífero se encuentra dentro del suelo, por una columna de suelo sobre regolito que alcanza la profundidad hasta el lecho de roca. Las reglas del nivel freático siguen el esquema de agua subterránea MMF de Noah-MP ([Miguez-Macho et al., 2007](https://doi.org/10.1029/2006JD008112)).

| Modelo | Activación | Predeterminado |
|---|---|---|
| HydroPol2D-Python | `vertical.subsurface.scheme: layered` | `legacy` |
| HydroPol2D (MATLAB) | `flag_layered_subsurface = 1` | `0` |

El esquema predeterminado no cambia. Ambos modelos implementan la misma columna, y los núcleos de MATLAB se verifican con datos de referencia (fixtures) generados en Python (ver [Validación de aguas subterráneas y recarga](../validation/groundwater-recharge)).

### 1.1 Por qué existe el esquema en capas {#11-why-the-layered-scheme-exists}

En el esquema predeterminado, la profundidad del suelo representa a la vez el suelo y el acuífero. Un nivel freático en ascenso reduce el almacenamiento no saturado, y el agua que ya no cabe vuelve a la superficie como exceso de saturación (sección 11 del [Modelo de aguas subterráneas](./groundwater-model#11-saturation-excess-correction-after-water-table-rise)). Donde el suelo es delgado y la recarga es alta, el nivel freático llega a la superficie y la infiltración se detiene. Las simulaciones a escala de ciudad mostraron este comportamiento en grandes partes del dominio.

El esquema en capas modifica dos aspectos.

1. El acuífero se extiende por debajo del suelo, a través del regolito, hasta la profundidad hasta el lecho de roca.
2. Un nivel freático en ascenso llena el espacio poroso vacío $\theta_s - \theta$ de las capas no saturadas. El agua ya retenida en ellas permanece en su lugar, en vez de ser empujada hacia la superficie.

---

## 2. Base del suelo y profundidad hasta el lecho de roca {#2-soil-base-and-depth-to-bedrock}

Dos profundidades definen la columna. Ambas se miden hacia abajo desde la superficie del terreno y marcan límites distintos.

| Profundidad | Qué marca | Papel en la columna en capas |
|---|---|---|
| **Base del suelo** | Donde terminan las propiedades del suelo y comienza el regolito | Fondo de las tres capas de suelo. Por debajo, las capas usan parámetros del regolito. |
| **Profundidad hasta el lecho de roca (DTB)** | Donde termina el acuífero | Fondo de toda la columna (suelo más regolito), limitado a `max_depth_m` (50 m por defecto). |

Por lo tanto, la base del acuífero es

$$
z_{\mathrm{base}} = z_{\mathrm{surf}} - \min\left(D_{\mathrm{DTB}},\,D_{\max}\right)
$$

y no $z_{\mathrm{surf}} - D_{\mathrm{soil}}$, como en el esquema predeterminado. Aquí, $z_{\mathrm{surf}}$ es la elevación de la superficie del terreno, $D_{\mathrm{DTB}}$ es la profundidad hasta el lecho de roca, $D_{\max}$ es el límite `max_depth_m` y $D_{\mathrm{soil}}$ es la profundidad del suelo del esquema predeterminado.

**Ejemplo.** Una celda con la base del suelo a 1.5 m y DTB a 30 m tiene capas de suelo entre 0 y 1.5 m y capas de regolito entre 1.5 y 30 m. Con DTB a 80 m, la columna se detiene en el límite de 50 m. Si DTB es menos profunda que la base del suelo, las capas de suelo se cortan en DTB.

Cada profundidad se lee de la primera fuente disponible.

| Profundidad | Fuentes (se usa la primera encontrada) |
|---|---|
| Base del suelo | ráster de base del suelo, luego el escalar `soil_base_depth_m` (2 m por defecto) |
| Profundidad hasta el lecho de roca | ráster de DTB, luego el escalar `depth_to_bedrock_m`, luego la profundidad del suelo de cada clase de suelo (con una advertencia) |

En el esquema en capas, la profundidad del suelo del esquema predeterminado solo se usa como este último recurso. La página [Profundidad hasta el lecho de roca](../inputs/dtb) describe las fuentes de datos globales para ambas profundidades.

---

## 3. Estructura de la columna {#3-column-structure}

<p align="center">
  <img src={useBaseUrl('/img/theory/layered-column.es.svg')} width="720" alt="Columna en capas de suelo sobre regolito: un árbol cuyas raíces alcanzan la profundidad de raíces, tres capas de suelo, capas de regolito cuyo espesor se duplica, un único nivel freático con recarga, ascenso capilar y flujo lateral, la base de la columna en la profundidad hasta el lecho de roca limitada y el embalse lineal profundo en el lecho de roca inferior" />
</p>

<p align="center">
  <em>Figura 1. La columna en capas de una celda (sin escala). El nivel freático divide la capa en la que se encuentra. Los símbolos se definen en la tabla siguiente.</em>
</p>

**Símbolos de la Figura 1**

| Símbolo | Significado | Unidades |
|---|---|---|
| $h$ | Carga hidráulica del nivel freático, una por celda | m |
| $\theta$ | Contenido de agua de la parte no saturada de una capa | m³/m³ |
| $\theta_s$ | Contenido de agua a saturación | m³/m³ |
| $\theta_r$ | Contenido de agua residual | m³/m³ |
| $\theta_{fc}$ | Contenido de agua a capacidad de campo, $\theta(\psi = -3.3\ \mathrm{m})$ por defecto; también es el nivel hasta el que el ascenso capilar rellena una capa | m³/m³ |
| $S_y$ | Rendimiento específico (porosidad drenable), $\theta_s - \theta_{fc}$ | - |
| $S_e$ | Saturación efectiva, $(\theta - \theta_r)/(\theta_s - \theta_r)$ | - |
| $K_v$ | Conductividad hidráulica saturada vertical de una capa | m/s |
| $K_r(S_e)$ | Conductividad relativa de Mualem–van Genuchten | - |
| $K(\theta)$ | Conductividad no saturada de una capa, $K_v\,K_r(S_e)$ | m/s |
| $q$ | Flujo de Darcy entre la capa no saturada más baja y el nivel freático; positivo hacia abajo (recarga), negativo hacia arriba (ascenso capilar) | m/s |
| $\psi$ | Carga matricial de la capa no saturada más baja; $\psi = 0$ en el nivel freático | m |
| $\Delta z$ | Mitad del espesor no saturado de esa capa | m |
| $T$ | Transmisividad para el flujo lateral | m²/s |
| $K_h$ | Conductividad saturada horizontal de una capa, incluido su multiplicador lateral | m/s |
| $b$ | Espesor saturado de una capa | m |
| $z_{\mathrm{surf}}$ | Elevación de la superficie del terreno | m |
| $D_{\mathrm{DTB}}$ | Profundidad hasta el lecho de roca | m |
| 50 m | Límite predeterminado de la profundidad de la columna, `max_depth_m` | m |
| $f_d$ | Fracción de la recarga enviada al acuífero profundo, `deep_recharge_fraction` | - |
| $Q$ | Caudal de salida de un embalse profundo | m³/s |
| $S$ | Almacenamiento de un embalse profundo | m³ |
| $\tau$ | Tiempo de respuesta de los embalses profundos, `deep_aquifer_response_time_days` | días |

| Capa | Intervalo de profundidad | Parámetros |
|---|---|---|
| 1. Cerca de la superficie | $0$ a $l_{\mathrm{top}}$ | curva de van Genuchten del suelo, $K_{\mathrm{sat}}$ cercano a la superficie |
| 2. Zona de raíces | $l_{\mathrm{top}}$ a la profundidad de raíces | curva de van Genuchten del suelo, $K_{\mathrm{sat}}$ de la zona de raíces |
| 3. Transmisión | profundidad de raíces a la base del suelo | curva de van Genuchten del suelo, $K_{\mathrm{sat}}$ de transmisión |
| 4, 5, … Regolito | base del suelo a la base de la columna | curva de van Genuchten del regolito, $K_v$, $K_h$ |

Las capas de regolito siguen una regla fija a partir de la base del suelo, con espesores de 0.25, 0.5, 1, 2, 4, 4, 4, … m (primer espesor de 0.25 m, razón de crecimiento 2 y máximo de 4 m). La regla se corta en la base de la columna.

Tres reglas mantienen regular la columna.

- **Número fijo de capas.** Todas las celdas tienen el mismo número de capas. Las capas situadas por debajo de la base de la columna tienen espesor cero.
- **Capas que colapsan.** Las raíces menos profundas que $l_{\mathrm{top}}$ dejan vacía la capa 2. Las raíces más profundas que la base del suelo dejan vacía la capa 3. Una capa de menos de 5 mm de espesor se fusiona con la capa superior.
- **Un nivel freático por celda.** La carga $h$ se mueve a través de límites fijos entre capas. Divide la capa en la que se encuentra en una parte no saturada arriba y una parte saturada abajo.

### 3.1 Variables de estado {#31-state-variables}

| Variable | Significado | Unidades |
|---|---|---|
| $h$ | carga hidráulica del nivel freático, una por celda | m |
| $W_k$ | agua por encima de $\theta_r$ en la parte no saturada de la capa $k$ | mm |
| $b_k$ | espesor saturado de la capa $k$ (por debajo de $h$, a $\theta_s$) | m |

El contenido de agua de la parte no saturada de la capa $k$, con espesor no saturado $u_k$, es

$$
\theta_k = \theta_{r,k} + \frac{W_k}{u_k}
$$

---

## 4. Reglas de los procesos {#4-process-rules}

### 4.1 Ascenso del nivel freático {#41-rising-water-table}

El agua que se añade en el nivel freático llena el espacio poroso vacío de la parte no saturada de la capa que contiene el nivel freático. Un volumen neto $V$ (por unidad de área) eleva el nivel freático en

$$
\Delta z = \frac{V}{\theta_{s,k} - \theta_k}
$$

donde $\theta_{s,k}$ y $\theta_k$ son el contenido de agua a saturación y el contenido de agua actual de la capa $k$. El agua que ya está en esa parte de la capa permanece allí y pasa a ser agua saturada, de modo que solo hay que llenar el espacio poroso vacío $\theta_{s,k} - \theta_k$. Es el ascenso del nivel freático del esquema de agua subterránea MMF (Miguez-Macho et al., 2007), que Noah-MP hace en la rutina `UPDATEWTD`. El ascenso pasa a la capa superior solo cuando la capa actual está llena, de modo que el redondeo no puede saltar una capa sin llenar. El agua sobrante cuando el nivel freático alcanza el terreno sale a la superficie como exfiltración (afloramiento).

### 4.2 Descenso del nivel freático {#42-falling-water-table}

El agua extraída en el nivel freático lo hace descender. El espesor que queda expuesto por el descenso permanece a capacidad de campo, $\theta_{fc} = \theta(\psi = -3.3\ \mathrm{m})$. Por lo tanto, cada metro de descenso libera

$$
S_y = \theta_s - \theta_{fc}
$$

Esta es la porosidad drenable, con la retención específica tomada como la capacidad de campo ([Lv et al., 2021](https://doi.org/10.1029/2020MS002270)). El agua por encima de $\theta_{fc}$ en el espesor expuesto drena después por gravedad. Un descenso y un ascenso del mismo volumen son reversibles. La extracción que no puede atenderse antes de llegar a la base de la columna se informa como no atendida.

La carga de capacidad de campo es `capillary_field_capacity_head_m` (3.3 m por defecto). Las capas de suelo siempre toman $S_y$ de su propia curva de retención. Las capas de regolito también lo hacen, salvo que se indique un $S_y$ del regolito como escalar o ráster. Ese valor debe estar en $(0,\ \theta_s - \theta_r]$. Se probó un contenido de equilibrio por franja, $\theta_{eq}(z)$, y se descartó porque su liberación tiende a cero en franjas delgadas.

### 4.3 Drenaje entre capas {#43-drainage-between-slots}

El agua drena hacia abajo a través de las capas no saturadas con gradiente unitario, como en el modelo cinemático de zona no saturada UZF1 ([Niswonger et al., 2006](https://pubs.usgs.gov/tm/2006/tm6a19/)), con el flujo

$$
q_k = K_{v,k}\,K_r(S_{e,k})
$$

donde $q_k$ es el flujo de drenaje de la capa $k$ y $K_r$ es la conductividad relativa de Mualem–van Genuchten. Cada flujo está limitado por el agua de la capa donante y por el espacio libre de la siguiente capa inferior que tenga una parte no saturada. Los flujos usan los estados al inicio del paso. El paso puede dividirse en `drainage_substeps` subpasos (1 por defecto). La capa no saturada más baja no drena con esta regla, sino que intercambia agua con el nivel freático (sección 4.4).

### 4.4 Flujo de Darcy en el nivel freático {#44-darcy-flux-at-the-water-table}

Entre la capa no saturada más baja y el nivel freático, HydroPol2D usa un flujo de Darcy, positivo hacia abajo,

$$
q = K(\theta_k)\left(\frac{\psi_k}{\Delta z} + 1\right),
\qquad \Delta z = \tfrac{1}{2}u_k
$$

donde $\psi_k$ es la carga matricial de la capa, con $\psi = 0$ en el nivel freático, $K(\theta_k)$ es la conductividad no saturada de la capa y $u_k$ es su espesor no saturado. Un flujo hacia abajo es recarga, limitada por el agua de la capa. Un flujo hacia arriba es ascenso capilar, limitado por el agua drenable por debajo del nivel freático y por la regla de rellenado que se describe a continuación.

**Regla de rellenado capilar.** El ascenso capilar rellena la capa no saturada más baja solo hasta la capacidad de campo, es decir, hasta el contenido de agua $\theta_{fc}$ que deja un nivel freático en descenso (donde se da un $S_y$ del regolito, $\theta_s - S_y$). Este es el enfoque de HBV (Lindström et al., 1997). Por lo tanto, el flujo ascendente se detiene cuando

$$
\theta_k \ge \theta_{fc}
$$

y nunca humedece el suelo por encima de un nivel freático somero hasta la saturación. La regla se aplica en HydroPol2D-Python (desde `fe81252`) y en el modelo MATLAB (desde `051b52b`), tanto en la malla estructurada como en la malla no estructurada.

Antes de esta regla, el ascenso capilar llenaba la capa hacia el equilibrio hidrostático, mientras que un nivel freático en descenso dejaba el suelo a capacidad de campo. Así, el agua circulaba hacia arriba y hacia abajo cerca de un nivel freático somero. La tabla siguiente muestra el efecto en el valle gemelo de la calibración.

| Medida | Antes | Después |
|---|---:|---:|
| Agua que circula entre el suelo y el nivel freático, solo la columna | 9.3 × 10⁻³ m³/s | 0 |
| Celdas que cambian el signo del flujo en cada paso, solo la columna | 38 | 0 |
| Ascenso capilar bruto, modelo completo | 0.016 m³/s | 0 |
| Caudal del cauce | sin cambio | sin cambio |

La contrapartida es que el modelo no tiene franja capilar. Para representarla, se reduce `capillary_field_capacity_head_m`. En ese caso, $\theta_{fc}$ y $S_y$ cambian juntos.

**Flujo implícito (predeterminado).** Sobre una franja no saturada delgada por encima de un nivel freático somero, el flujo explícito es rígido. Con pasos largos, el flujo se excede y cambia de signo. Por defecto, HydroPol2D evalúa el flujo al final del paso con un paso de Euler implícito (backward Euler) linealizado por celda, sin iteración.

$$
q = \frac{q_0}{1 + \Delta t\,\max\!\left(\dfrac{\partial q}{\partial W} - \dfrac{1}{S_y^{*}}\dfrac{\partial q}{\partial h},\ 0\right)}
$$

donde $q_0$ es el flujo explícito y $W$ es el agua de la capa. La derivada respecto de la carga sigue el movimiento del nivel freático que causa el flujo. Un ascenso conserva el contenido de agua de la franja, y un descenso expone $\theta_{fc}$. $S_y^{*}$ es el costo de almacenamiento de ese movimiento ($\theta_s - \theta_k$ de la franja cuando el agua baja). Solo se conserva la parte amortiguadora de la derivada. Una franja saturada ($\theta_k = \theta_s$) drena a $K_{sat}$ sin amortiguamiento. CLM5 también resuelve su flujo en el nivel freático de forma implícita. Con pasos cortos, ambas formas coinciden.

| Prueba: arena, $\theta = 0.41$, nivel freático a 30 cm de profundidad (franja casi saturada), pasos de 1 h, frente a una simulación con pasos de 1 s | Resultado |
|---|---|
| Flujo implícito | el nivel freático se mantiene a menos de 2 mm de la simulación de 1 s |
| Flujo explícito | drena cerca de 20 veces más agua de la debida |

| Modelo | Interruptor | Derivadas |
|---|---|---|
| HydroPol2D-Python | `implicit_water_table_flux` (`true` por defecto) | `jax.jvp` |
| HydroPol2D (MATLAB) | `flag_implicit_water_table_flux` (`1` por defecto; `HYDROPOL_IMPLICIT_WATER_TABLE_FLUX` lo sobrescribe) | diferencias centrales de cuarto orden |

Los dos modelos coinciden hasta cerca de $10^{-9}$, y sus pruebas de paridad usan una tolerancia de $10^{-8}$.

### 4.5 Flujo lateral {#45-lateral-flow}

El flujo lateral usa la aproximación de Dupuit–Forchheimer con una transmisividad por capas,

$$
T = \sum_k K_{h,k}\,b_k
$$

donde $K_{h,k}$ y $b_k$ son la conductividad horizontal y el espesor saturado de la capa $k$. La transmisividad en una cara es la media aritmética de las dos celdas, y el flujo en una cara de ancho $w$ es $Q = -\bar{T}\,\dfrac{\Delta h}{\Delta x}\,w$. La conductividad horizontal de cada capa se define en la tabla siguiente.

| Capas | $K_h$ |
|---|---|
| Suelo (1–3) | $K_{\mathrm{sat}}$ del suelo × `soil_lateral_anisotropy` × `soil_lateral_conductivity_multiplier` |
| Regolito (4, …) | $K_h$ del regolito × `regolith_lateral_conductivity_multiplier` |

Ambos multiplicadores valen 1 por defecto. La [calibración por recesión del agua subterránea](../calibration/groundwater-recession) los ajusta. Si no se indica un $K_h$ del regolito, se usa el $K_{\mathrm{sat}}$ de agua subterránea del esquema predeterminado.

El flujo lateral avanza con subpasos explícitos limitados por

$$
\Delta t \le C_{\mathrm{gw}}\,\frac{\min(\Delta x,\Delta y)^2\,S_y}{4\,T}
$$

con $C_{\mathrm{gw}}$ = `groundwater_courant` (0.25 por defecto) y $S_y$ evaluado en el nivel freático. La salida de una celda está limitada por su agua drenable. Los volúmenes netos pasan por las reglas de ascenso y descenso anteriores, de modo que las cargas, el agua no saturada y el afloramiento se mantienen consistentes. Las celdas de carga fija (Dirichlet) conservan su carga, y su intercambio se informa como entrada por el contorno. El flujo lateral se ejecuta con el programador de agua subterránea (sección 2.1 del [Modelo de aguas subterráneas](./groundwater-model#21-asynchronous-scheduler)).

### 4.6 Absorción de agua por las raíces {#46-root-water-uptake}

Con el estrés de Feddes activado, la ET del suelo se reduce por $\alpha(h)$ en cada capa con raíces ([Modelo hidrológico, sección 3.5](./hydrologic-model#35-feddes-root-water-uptake-stress)). Sin Feddes, las raíces que llegan por debajo del nivel freático toman del nivel freático la parte no atendida de la demanda. Esa parte es la fracción saturada de la profundidad de raíces y está limitada por el agua drenable.

### 4.7 Acuífero profundo {#47-deep-aquifer}

Cuando el acuífero profundo está activo, una fracción fija de la recarga que llega al nivel freático se envía en su lugar a los embalses lineales profundos ([Modelo de aguas subterráneas, sección 13](./groundwater-model#13-deep-aquifer)).

---

## 5. Orden de las operaciones {#5-order-of-operations}

El intercambio vertical se ejecuta en cada paso superficial. El flujo lateral se ejecuta cuando corresponde según el programador de agua subterránea.

1. Infiltración en las capas de suelo (la infiltración de Darcy del [Modelo hidrológico](./hydrologic-model#4-infiltration)).
2. Evaporación de agua libre y luego ET del suelo, con estrés de Feddes opcional.
3. Cascada de drenaje entre las capas no saturadas.
4. Flujo de Darcy en el nivel freático, como recarga o ascenso capilar.
5. Separación de la recarga hacia el acuífero profundo, si está activo.
6. Actualización del nivel freático. El afloramiento pasa a la superficie.
7. Intercambio río-agua subterránea, si está activo.
8. Flujo lateral, cuando corresponde según el programador.

En la malla de Voronoi, las HRU de una celda comparten su superficie del terreno, su base de columna y su carga. Su intercambio vertical se suma por celda y se aplica en la actualización del agua subterránea, por bisección sobre la curva de almacenamiento de la celda. El flujo lateral usa la transmisividad ponderada por área.

El esquema en capas también admite el intercambio río-agua subterránea en los motores de malla (celdas de lecho de río resueltas y canales de Neal) y la exfiltración desde la infraestructura verde hacia las capas de suelo.

---

## 6. Motores y velocidad {#6-engines-and-speed}

| Motor | HydroPol2D-Python | HydroPol2D (MATLAB) |
|---|---|---|
| Malla estructurada | `core/layered_vertical.py` | `flag_layered_subsurface = 1` |
| Malla de Voronoi | NumPy (`voronoi_layered.py`) y JAX (`mesh_gpu/layered.py`); paridad NumPy–JAX de aproximadamente $10^{-15}$ en términos relativos | Ejecutor de Voronoi (`config.layered_subsurface`) |

En Python, el paso en capas de la malla estructurada se compila una vez por caso. Los resultados son idénticos a los del paso sin compilar. El perfilado del 2026-10-19 dio los resultados siguientes.

| Medida | Antes de compilar | Después de compilar |
|---|---:|---:|
| Paso en capas, 31 pasos | 2.9 s | 0.09 s |
| Una hora con enrutamiento | 4.6 s | 0.7 s |

Después de compilar, el esquema en capas se ejecuta más rápido que el esquema predeterminado. `HYDROPOL2D_LAYERED_JIT=0` ejecuta el paso operación por operación, como referencia.

Se evaluaron relojes separados para el suelo y el agua subterránea (pasos de tiempo multitasa, como en MIKE SHE, GSSHA, Noah-MP y CLM5), y esa opción está en pausa. Después de compilar, el enrutamiento superficial ocupa la mayor parte del tiempo de ejecución, por lo que un reloj separado para el suelo aportaría poco.

---

## 7. Salidas {#7-outputs}

| Salida | Python, malla estructurada | Python, malla | MATLAB | Significado |
|---|---|---|---|---|
| Profundidad del agua subterránea | `groundwater_depth_map_m` | `groundwater_depth_face_m` | `Maps.Hydro.GWdepth_save` | Profundidad del nivel freático bajo el terreno (m), limitada a la base de la columna |
| Base de la columna | `column_base_depth_m` | `column_base_depth_face_m` | `Maps.Hydro.ColumnBaseDepth_m` | $\min(D_{\mathrm{DTB}}, D_{\max})$ bajo el terreno (m), estática |
| Saturación de la zona de raíces y de transmisión | `root_zone_saturation_map`, `transmission_zone_saturation_map` | - | - | $\theta/\theta_s$ de la parte no saturada de las capas 2 y 3; NaN donde la capa está saturada |
| Almacenamiento vadoso profundo | `deep_vadose_storage_map_mm` | `deep_vadose_storage_face_mm` | `Maps.Hydro.DeepVadose_save` | Agua por encima de $\theta_r$ en la parte no saturada de las capas de regolito (mm) |

El espesor saturado es la profundidad de la base de la columna menos la profundidad del agua subterránea. No se guarda. Todavía no se escriben rásteres por capa ni cortes por profundidad. Los estados por capa se conservan en el estado del modelo y en los puntos de control (checkpoints).

---

## 8. Configuración {#8-configuration}

**HydroPol2D-Python**

```yaml
vertical:
  feddes: {enabled: true, h1_m: -0.1, h2_m: -0.25, h3_m: -4.0, h4_m: -80.0}
  groundwater_courant: 0.25          # lateral-flow substep safety factor
  capillary_field_capacity_head_m: 3.3
  subsurface:
    scheme: layered
    soil_base_depth_m: 2.0           # or static.soil_base_depth_path
    depth_to_bedrock_m: 20.0         # or static.depth_to_bedrock_path
    max_depth_m: 50.0
    deep_layers: {first_thickness_m: 0.25, growth_ratio: 2.0, max_thickness_m: 4.0}
    regolith_theta_s: 0.35
    regolith_theta_r: 0.05
    regolith_alpha_vg_m_inverse: 2.0
    regolith_n_vg: 1.5
    regolith_ksat_v_mm_h: 5.0
    regolith_ksat_h_mm_h: null       # null: vertical.groundwater_ksat_mm_h
    regolith_specific_yield: null    # null: theta_s - theta_fc of the regolith curve
    soil_lateral_anisotropy: 1.0
    soil_lateral_conductivity_multiplier: 1.0
    regolith_lateral_conductivity_multiplier: 1.0
    implicit_water_table_flux: true
    drainage_substeps: 1
```

Un ráster `static.regolith_<name>_path` tiene prioridad donde es finito. El escalar completa el resto.

**HydroPol2D (MATLAB).** La pestaña Soil and groundwater del libro del caso contiene todos los parámetros anteriores, bloque por bloque, con su interruptor al inicio del bloque (`flag_layered_subsurface`, `flag_feddes`, `flag_implicit_water_table_flux`). Ver [Parámetros del libro del caso](../configuration/general_data#tab-soil-and-groundwater) y [Banderas del modelo](../configuration/flags).

---

## 9. Límites conocidos {#9-known-limits}

- **Sin flujo lateral de agua colgada.** Una capa de suelo saturada sobre regolito no saturado no genera flujo lateral.
- **Sin tabla de clases de regolito.** Los parámetros del regolito son escalares o rásteres.
- **Sin salidas ráster por capa.**
- **Sin franja capilar.** El ascenso capilar rellena una capa solo hasta la capacidad de campo (sección 4.4). Reducir `capillary_field_capacity_head_m` representa una franja capilar, con un $S_y$ menor.
- **Bucle compilado de ciudad.** El bucle compilado de ciudad de HydroPol2D-Python todavía no ejecuta el esquema en capas con flujo lateral de agua subterránea.
- **Dos formas de calcular las derivadas implícitas.** Python usa `jax.jvp` y MATLAB usa diferencias centrales. Coinciden hasta cerca de $10^{-9}$.

---

## 10. Fuentes {#10-sources}

- Miguez-Macho, G., Fan, Y., Weaver, C. P., Walko, R., and Robock, A. (2007). Incorporating water table dynamics in climate modeling: 2. Formulation, validation, and soil moisture simulation. *Journal of Geophysical Research*, 112, D13108. [doi:10.1029/2006JD008112](https://doi.org/10.1029/2006JD008112)
- Noah-MP, [`GroundWaterMmfMod.F90`](https://github.com/NCAR/noahmp/blob/master/drivers/hrldas/GroundWaterMmfMod.F90).
- Niswonger, R. G., Prudic, D. E., and Regan, R. S. (2006). Documentation of the Unsaturated-Zone Flow (UZF1) Package for modeling unsaturated flow between the land surface and the water table with MODFLOW-2005. USGS Techniques and Methods 6-A19. [pubs.usgs.gov/tm/2006/tm6a19](https://pubs.usgs.gov/tm/2006/tm6a19/)
- Lv, M., et al. (2021). A comprehensive review of specific yield in land surface and groundwater studies. *Journal of Advances in Modeling Earth Systems*, 13, e2020MS002270. [doi:10.1029/2020MS002270](https://doi.org/10.1029/2020MS002270)
- Feddes, R. A., Kowalik, P. J., and Zaradny, H. (1978). *Simulation of Field Water Use and Crop Yield*. Pudoc, Wageningen.
- Lindström, G., Johansson, B., Persson, M., Gardelin, M., and Bergström, S. (1997). Development and test of the distributed HBV-96 hydrological model. *Journal of Hydrology*, 201, 272–288. [doi:10.1016/S0022-1694(97)00041-3](https://doi.org/10.1016/S0022-1694(97)00041-3)
