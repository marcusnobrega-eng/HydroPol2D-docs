---
title: Calibración por Recesión del Agua Subterránea
---
import useBaseUrl from '@docusaurus/useBaseUrl';

# Calibración por Recesión del Agua Subterránea

HydroPol2D estima parámetros efectivos de agua subterránea a escala de cuenca ajustando la recesión simulada en la salida a una curva maestra de recesión (MRC) observada. La calibración se ejecuta en HydroPol2D-Python. Sus resultados aceptados son entradas ordinarias del caso, por lo que Python y MATLAB parten de los mismos parámetros y estados (ver el [Flujo de trabajo de construcción del modelo](../getting-started/model-building-workflow#groundwater-calibrated-workflow)).

Los parámetros que ajusta la calibración dependen del esquema de subsuelo.

| Esquema | Parámetros ajustados |
|---|---|
| Predeterminado | Conductividad horizontal uniforme $K_{sat,h}$ y rendimiento específico $S_y$ |
| [En capas](../theory/layered-subsurface) | Dos multiplicadores de la conductividad horizontal, uno para las capas de suelo y otro para las capas de regolito |

Los valores ajustados son parámetros efectivos. Reproducen la recesión observada con esta estructura del modelo. No son mediciones puntuales del material del acuífero.

---

## 1. Flujo de trabajo {#1-workflow}

Ambos esquemas siguen los mismos pasos.

1. Leer un CSV local de caudal diario o descargar el caudal diario de una estación de aforo del USGS.
2. Separar el flujo base con el filtro de Lyne–Hollick y reunir los eventos de recesión en una MRC.
3. Separar la cola lenta del acuífero profundo del objetivo somero, que es más rápido.
4. Para cada candidato, ejecutar el período de calentamiento (spin-up) del modelo hasta un estado estacionario bajo el caudal objetivo (sección 4).
5. Equilibrar el estado del río y enrutar la liberación de agua subterránea hasta la salida con el solucionador hidráulico superficial.
6. Evaluar la recesión enrutada en la salida frente a la parte somera de la MRC.
7. Guardar el mejor punto de control (checkpoint) hidráulico completo, con agua superficial, agua subterránea somera, agua del suelo, almacenamientos del acuífero profundo y momento D8.

La función objetivo combina forma y volumen para que los caudales altos no dominen el ajuste.

$$
J = \mathrm{RMSE}\left(\ln Q_{\mathrm{sim}},\ \ln Q_{\mathrm{obs}}\right) + 0.5\,\frac{\left|V_{\mathrm{sim}} - V_{\mathrm{obs}}\right|}{V_{\mathrm{obs}}}
$$

Aquí, $Q_{\mathrm{sim}}$ y $Q_{\mathrm{obs}}$ son los caudales simulado y observado, y $V$ es el volumen de recesión en el período evaluado.

**Esquema predeterminado.**

```bash
hydropol2d calibrate-groundwater-recession case.yaml master_recession calibration \
  --usgs-site 02147020 --start-date 1980-01-01 --end-date 2019-09-29 \
  --ksat-values 1e-5,5e-5,1e-4 --specific-yield-values 0.03,0.05,0.1 \
  --shallow-checkpoint-fraction 0.05
```

Para un archivo local, los argumentos del USGS se reemplazan por `--discharge-csv observations.csv`. Las columnas predeterminadas son `date` y `observed_discharge_m3_s`.

---

## 2. Esquema en capas: dos multiplicadores de la conductividad lateral {#2-layered-scheme-two-lateral-conductivity-multipliers}

Con `vertical.subsurface.scheme: layered`, $S_y$ no se ajusta. Cada capa toma $S_y$ de su curva de retención ($\theta_s - \theta_{fc}$), y una recesión solo restringe la razón $K/S_y$ ([Brutsaert y Nieber, 1977](https://doi.org/10.1029/WR013i003p00637)). En su lugar, la calibración ajusta dos factores a escala de cuenca sobre la conductividad horizontal mapeada.

| Parámetro | Qué escala |
|---|---|
| `vertical.subsurface.soil_lateral_conductivity_multiplier` | Las tres capas de suelo: $K_{sat}$ del suelo × `soil_lateral_anisotropy` |
| `vertical.subsurface.regolith_lateral_conductivity_multiplier` | Las capas de regolito: $K_h$ del regolito (escalar, ráster o el $K_{sat}$ de agua subterránea) |

**Por qué pueden separarse los dos factores.** Los caudales altos del inicio drenan mientras el nivel freático está en el suelo. Los caudales bajos del final drenan mientras está en el regolito. Por eso, la forma de la recesión puede separar los dos factores. Que lo logre depende de la cuenca y del registro, en particular de la regulación, del ruido y de la frecuencia con que el nivel freático llega al suelo. Cada ejecución informa este resultado (sección 3).

```bash
hydropol2d calibrate-groundwater-recession case.yaml master_recession calibration \
  --discharge-csv observations.csv --soil-multipliers 0.1,0.3,1,3,10 \
  --regolith-multipliers 0.1,0.3,1,3,10
```

---

## 3. Salidas de identificabilidad {#3-identifiability-outputs}

Cada ejecución en capas escribe `coupled_identifiability.json` y `coupled_objective_surface.png`.

| Salida | Significado |
|---|---|
| Conjunto aceptable | Candidatos con $J \le 1.05\,J_{\mathrm{best}} + 0.01$ |
| Décadas abarcadas | Rango de cada multiplicador en el conjunto aceptable, en unidades de $\log_{10}$ |
| Indicador de borde de la malla | Indica si el mejor valor está en el borde de la malla de candidatos; en ese caso, se debe ampliar la malla |
| Correlación de los log-multiplicadores | Correlación de los logaritmos de ambos multiplicadores en el conjunto aceptable; un valor fuertemente negativo indica un valle de compensación |
| Exponente de recesión $b$ | Exponente de $-\mathrm{d}Q/\mathrm{d}t = a\,Q^b$, para el objetivo y para cada candidato |

Ambos esquemas también escriben los archivos siguientes.

| Archivo | Contenido |
|---|---|
| `master_recession_curve.csv` | Componentes total, somero y profundo de la recesión observada |
| `coupled_candidate_scores.csv` | Función objetivo y diagnósticos de cada candidato |
| `coupled_best_recession.csv` | Objetivo observado y recesión enrutada en la salida |
| `coupled_recession_checkpoint.npz` | Estado hidráulico inicial completo seleccionado |
| `coupled_calibration_metadata.json` | Parámetros, método y criterio del punto de control |

El punto de control seleccionado puede trasladarse al tiempo cero del modelo. Este traslado conserva el agua física y las memorias hidráulicas, y reinicia los diagnósticos acumulados y la referencia del balance de masa.

---

## 4. Período de calentamiento (spin-up) {#4-spin-up}

Cada candidato parte de su propio estado estacionario bajo el caudal objetivo. Esta es la principal lección numérica de la calibración en capas.

1. **Usar los flujos propios de la columna del modelo.** El spin-up usa la recarga descendente a través de las capas no saturadas, el flujo de Darcy en el nivel freático, el drenaje del lecho del río en cada paso y el flujo lateral con su propio reloj. Así, la recesión no comienza con una zona no saturada alejada del estado estacionario.
2. **Usar primero pasos de 1 h.** Se ejecutan hasta que la fuente media de la ventana y el rango de almacenamiento se mantienen dentro de sus tolerancias durante un año simulado.
3. **Luego usar los pasos propios del modelo** durante 30 días.
4. **Evaluar la estacionariedad con el rango de almacenamiento, nunca con los valores inicial y final.** Un transitorio que se llena rápido y drena lentamente pasa una prueba basada en los valores inicial y final en su pico de almacenamiento.

**Qué falló antes de la corrección.** En la simulación de referencia (verdad) del experimento gemelo, el suelo quedó a capacidad de campo al inicio de la recesión. El ascenso capilar hacia ese suelo alcanzó 0.10 m³/s, frente a un caudal de salida de 0.005 m³/s. Cerca de 50 000 m³ pasaron a la zona no saturada en 6 días, y hacia el día 18 el cauce estaba casi desconectado. La recesión estuvo dominada por el ascenso capilar y no por el acuífero.

---

## 5. Experimentos gemelos {#5-twin-experiments}

Un experimento gemelo evalúa la identificabilidad antes de usar datos reales.

1. Elegir multiplicadores "verdaderos" conocidos.
2. Ejecutar el modelo para generar una recesión sintética.
3. Añadir ruido log-normal.
4. Calibrar con la recesión con ruido.
5. Verificar si se recupera la verdad.

Las herramientas están en `hydropol2d.calibration.recession_twin` (`run_recession_twin_experiment`, `write_recession_twin_report`).

### 5.1 Resultado en un valle de drenaje rápido {#51-result-on-a-fast-draining-valley}

Esta simulación (2026-10-20) usa la física actual, incluida la regla de rellenado capilar del [subsuelo en capas](../theory/layered-subsurface#44-darcy-flux-at-the-water-table).

| Configuración | Valor |
|---|---|
| Valle | En forma de V, 11 × 15 celdas de 20 m |
| Rendimiento específico | suelo cerca de 0.12, regolito 0.05 |
| Inicio | 1.5 mm/día de caudal de salida |
| Malla de candidatos | suelo 1, 3, 10 × regolito 0.1, 0.3, 1 (3 × 3) |
| Verdad | suelo 3, regolito 0.3 |
| Recesión | 30 días |

| Ruido | Mejor candidato | Candidatos aceptables | Función objetivo, mejor | Función objetivo, siguiente mejor |
|---|---|---:|---:|---:|
| 0 % | suelo 3, regolito 0.3 | 1 | 0.033 | 0.123 |
| 5 % | suelo 3, regolito 0.3 | 1 | 0.065 | 0.117 |
| 10 % | suelo 3, regolito 0.3 | 1 | 0.106 | 0.131 |

La verdad se recuperó en los tres niveles de ruido y fue el único par aceptable en cada nivel. Los nueve candidatos enrutados tardaron 68 min en una computadora portátil con 2 procesos de trabajo (workers). Las tres filas evalúan los mismos nueve candidatos enrutados, y solo difiere el ruido añadido al objetivo.

En la primera simulación, antes de la regla de rellenado capilar (2026-10-19), la verdad también fue el mejor candidato, pero con 10 % de ruido se aceptó cualquier multiplicador del suelo entre 3 y 10.

<p align="center">
  <img src={useBaseUrl('/img/calibration/layered-twin-experiment.png')} width="900" alt="Izquierda: recesión objetivo con 5 por ciento de ruido, recesión verdadera y mejor candidato en eje logarítmico durante 30 días. Derecha: función objetivo sobre la malla de 3 por 3 de multiplicadores del suelo y del regolito, con el mejor candidato en los valores verdaderos" />
</p>

<p align="center">
  <em>Figura 1. Experimento gemelo con 5 % de ruido. Izquierda: objetivo, verdad y mejor candidato. Derecha: función objetivo sobre la malla de candidatos; el candidato marcado con un círculo es el único aceptable y coincide con la verdad.</em>
</p>

### 5.2 Qué limita la prueba {#52-what-limits-the-test}

- **Ruido entre repeticiones.** En la simulación del 2026-10-19, repetir la ejecución con los mismos parámetros produjo una dispersión diaria de ±2.7 %, debida a una oscilación de dos intervalos en el canal pequeño. Las diferencias entre candidatos menores que ese valor están dentro del ruido entre repeticiones.
- **El valle gemelo predeterminado es demasiado lento.** Con laderas de 500 m y un $S_y$ del suelo de aproximadamente 0.29, drena a lo largo de años. Su recesión bajó solo 9 % en 20 días, una pendiente demasiado plana para separar los candidatos. Para recesiones de semanas, se deben usar laderas más cortas y un $S_y$ menor, como en la sección 5.1.
- **Una prueba gemela no es una prueba de campo.** Muestra que el método puede recuperar parámetros en un valle sintético con la misma estructura del modelo. Los registros reales añaden regulación, evapotranspiración y error de medición.

---

## 6. Estado inicial del acuífero profundo {#6-deep-aquifer-starting-state}

El mismo filtro, la MRC y la separación de la cola profunda dan el caudal de salida inicial del acuífero profundo.

```bash
hydropol2d estimate-deep-baseflow observations.csv --start-date 2019-06-01 \
  --drainage-area-km2 5320 --output deep_baseflow.json
```

La herramienta ubica el flujo base de la fecha de inicio sobre la MRC y divide su parte profunda por el área de drenaje. El informe también da el tiempo de respuesta de la cola, que puede usarse para `deep_aquifer_response_time_days`. Conviene elegir una fecha de inicio dentro de una recesión. La herramienta emite una advertencia cuando el caudal de la fecha de inicio es mayor que el doble del flujo base. La teoría se presenta en [Modelo de aguas subterráneas, sección 13.3](../theory/groundwater-model#133-starting-state).

---

## 7. Case Builder {#7-case-builder}

El Case Builder lanza la calibración para cualquiera de los dos esquemas.

1. En un caso en capas, el lanzamiento pasa `--soil-multipliers` y `--regolith-multipliers`.
2. La finalización escribe los multiplicadores ajustados en el caso de Python (`vertical.subsurface`) y en el ejecutor de MATLAB (`HYDROPOL_SOIL_LATERAL_CONDUCTIVITY_MULTIPLIER`, `HYDROPOL_REGOLITH_LATERAL_CONDUCTIVITY_MULTIPLIER`).
3. $S_y$ permanece en las curvas de retención. No se escriben rásteres uniformes de $K_{sat}$ ni de $S_y$.
4. El archivo `DeepAquiferInitialState.json` de la calibración reemplaza cualquier flujo base inicial o recarga media indicados manualmente.

---

## Fuentes {#sources}

- Brutsaert, W., and Nieber, J. L. (1977). Regionalized drought flow hydrographs from a mature glaciated plateau. *Water Resources Research*, 13(3), 637–643. [doi:10.1029/WR013i003p00637](https://doi.org/10.1029/WR013i003p00637)
- Lyne, V., and Hollick, M. (1979). Stochastic time-variable rainfall-runoff modelling. *Institute of Engineers Australia National Conference*, Publication 79/10, 89–93.
