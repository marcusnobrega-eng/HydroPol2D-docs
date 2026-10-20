---
title: Aguas subterráneas y recarga
---
import useBaseUrl from '@docusaurus/useBaseUrl';

# Validación de aguas subterráneas y recarga

La sección de aguas subterráneas de la suite de validación evalúa tanto la contabilidad local del agua subterránea como su dinámica lateral. El cambio central de la implementación es el programador asincrónico. El drenaje vadoso, la producción de recarga y el ascenso capilar se evalúan en cada paso del modelo superficial, mientras que el almacenamiento saturado y las cargas laterales del agua subterránea se actualizan solo cuando corresponde según el programador.

## Qué se probó {#what-was-tested}

Se usaron cuatro casos de agua subterránea en la cuenca en V para evaluar el almacenamiento local y el comportamiento del programador.

- `VAL-GW-ASYNC-001`: ascenso del nivel freático con recarga constante;
- `VAL-GW-ASYNC-002`: equivalencia del programador asincrónico;
- `VAL-GW-CAP-001`: abatimiento por ascenso capilar;
- `VAL-GW-MOUND-001`: domo de recarga de Boussinesq frente a una referencia numérica de paso de tiempo fino.

Se usaron dos casos adicionales de ladera para reforzar la evidencia sobre el flujo lateral de agua subterránea.

- `VAL-GW-HILL-STEADY-001`: perfil de Dupuit permanente;
- `VAL-GW-HILL-TRANSIENT-001`: decaimiento transitorio de Boussinesq linealizado.

## Recarga local y comportamiento del programador {#local-recharge-and-scheduler-behavior}

### Referencia y método {#reference-and-method}

El caso de recarga local usa la relación analítica de almacenamiento `Δh = RΔt / S_y` con el flujo lateral de agua subterránea y la exfiltración desactivados. El caso de equivalencia del programador compara la actualización heredada del agua subterránea en cada paso con el programador de acumulación asincrónico. El caso de ascenso capilar aplica un flujo ascendente simple, con un límite físico, desde agua subterránea somera hacia un almacenamiento vadoso seco. El caso del domo de recarga activa el flujo lateral de agua subterránea y compara el resultado asincrónico con una referencia numérica interna de paso de tiempo fino.

### Resultado principal {#main-result}

Los cuatro casos locales de agua subterránea superaron las pruebas.

| Caso | Régimen | RMSE de carga (m) | Error máximo de carga (m) | Error de almacenamiento (%) | Residuo (m³) |
|---|---|---:|---:|---:|---:|
| `VAL-GW-ASYNC-001` | Recarga local | 0.0 | 0.0 | 0.0 | `1.96 × 10^-11` |
| `VAL-GW-ASYNC-002` | Equivalencia del programador | `1.71 × 10^-13` | `1.71 × 10^-13` | `1.67 × 10^-11` | `1.84 × 10^-10` |
| `VAL-GW-CAP-001` | Ascenso capilar | 0.0 | 0.0 | 0.0 | `-1.45 × 10^-12` |
| `VAL-GW-MOUND-001` | Domo de Boussinesq | `1.83 × 10^-8` | `9.90 × 10^-8` | `5.23 × 10^-13` | `3.09 × 10^-11` |

<div style={{display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(280px, 1fr))', gap: '1rem'}}>
  <img src={useBaseUrl('/validation/results/groundwater/VAL_GW_ASYNC_001_head_recharge.png')} alt="Ascenso analítico del agua subterránea con recarga constante" />
  <img src={useBaseUrl('/validation/results/groundwater/VAL_GW_ASYNC_002_equivalence.png')} alt="Equivalencia del programador asincrónico de agua subterránea" />
</div>

<p><em>Diagnósticos del programador de recarga. El primer caso verifica el ascenso analítico del nivel freático con recarga constante. El segundo compara el programador asincrónico con la actualización heredada del agua subterránea en cada paso.</em></p>

<div style={{display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(280px, 1fr))', gap: '1rem'}}>
  <img src={useBaseUrl('/validation/results/groundwater/VAL_GW_CAP_001_capillary.png')} alt="Validación del ascenso capilar" />
  <img src={useBaseUrl('/validation/results/groundwater/VAL_GW_MOUND_001_reference.png')} alt="Validación del domo de recarga de Boussinesq" />
</div>

<p><em>Diagnósticos de ascenso capilar y flujo lateral. El caso del domo es una evidencia útil frente a una referencia numérica, pero sigue siendo más débil que un benchmark analítico.</em></p>

El resultado principal es que la acumulación de recarga, la actualización asincrónica del agua subterránea y el cierre simple de ascenso capilar se comportaron como se esperaba en condiciones controladas.

## Benchmarks analíticos de ladera {#analytical-hillslope-benchmarks}

### Referencia y método {#reference-and-method-1}

El caso de ladera permanente compara HydroPol2D con el perfil de Dupuit en forma cerrada, con recarga uniforme y carga fija en el dren. El caso de ladera transitorio compara el solucionador de Boussinesq de HydroPol2D con el primer modo propio de la ecuación de Boussinesq linealizada en el régimen de perturbaciones pequeñas.

### Resultado principal {#main-result-1}

Ambos casos analíticos de ladera superaron las pruebas.

| Caso | Benchmark | RMSE de carga (m) | Error máximo de carga (m) | Métrica de flujo |
|---|---|---:|---:|---|
| `VAL-GW-HILL-STEADY-001` | Dupuit permanente | `6.04 × 10^-3` | `9.75 × 10^-3` | Error del caudal del dren = `3.74 × 10^-4 %` |
| `VAL-GW-HILL-TRANSIENT-001` | Boussinesq linealizado | `1.94 × 10^-5` | `4.46 × 10^-5` | `NSE = 0.99985` |

<img src={useBaseUrl('/validation/results/groundwater/VAL_GW_HILL_STEADY_001_profile.png')} alt="Benchmark de agua subterránea en ladera con perfil de Dupuit permanente" />

<p><em>Benchmark de Dupuit permanente. El panel inferior muestra el error absoluto del perfil frente a la solución analítica.</em></p>

<img src={useBaseUrl('/validation/results/groundwater/VAL_GW_HILL_TRANSIENT_001_profiles_hydrograph.png')} alt="Benchmark de ladera con Boussinesq linealizado transitorio" />

<p><em>Benchmark de ladera transitorio. El panel superior compara los perfiles de carga durante el decaimiento de la perturbación, y el panel inferior compara el flujo modelado y el analítico en el pie de la ladera, por unidad de ancho.</em></p>

## Subsuelo en capas {#layered-subsurface}

El [subsuelo en capas](../theory/layered-subsurface) se incorporó en octubre de 2026. Su evidencia es de cuatro tipos. Incluye pruebas unitarias en Python de las reglas de la columna, la paridad entre Python y MATLAB, simulaciones del modelo completo en la cuenca en V en MATLAB y un experimento gemelo de calibración.

### Pruebas de la columna en Python {#python-column-tests}

HydroPol2D-Python prueba directamente la columna en capas, el estrés de Feddes y el estado inicial del acuífero profundo (`tests/test_subsurface_column.py`, `test_subsurface_geometry.py`, `test_subsurface_lateral.py`, `test_subsurface_mesh.py`, `test_subsurface_run.py`, `test_feddes.py`, `test_deep_aquifer_initial_state.py`).

La prueba numérica clave compara el flujo explícito y el implícito en el nivel freático.

| Caso | Flujo | Cambios de signo | Agua movida en 24 h frente a una referencia de 36 s |
|---|---|---:|---:|
| Suelo arenoso, húmedo, nivel freático a 15 cm, pasos de 1 h | Explícito | 2 | 53 % en exceso |
| Igual | Implícito (predeterminado) | 0 | dentro de 0.1 % |

Con un paso de 0.01 s, ambas formas coinciden dentro de $1.5 \times 10^{-5}$.

### Paridad entre Python y MATLAB {#python-to-matlab-parity}

La adaptación a MATLAB se verifica con datos de referencia (fixtures) exportados desde HydroPol2D-Python (`Validation/Groundwater/Layered` en el repositorio de MATLAB). Los fixtures usan el flujo explícito en el nivel freático, porque el flujo implícito todavía no se ha adaptado.

| Script | Qué verifica | Resultado registrado |
|---|---|---|
| `run_layered_kernel_parity.m` | Cada núcleo de la columna: geometría, actualización del nivel freático MMF, drenaje, flujo de Darcy, Feddes, bisección del nivel freático compartido y avance lateral | 193 comprobaciones, peor caso $2.8 \times 10^{-16}$ |
| `run_layered_step_parity.m` | El paso vertical en capas completo en una malla en V de 2 × 2, 4 escenarios, 312 pasos | 3 120 comprobaciones, peor caso $2.1 \times 10^{-17}$ |
| `run_layered_vtilted_case.m` | Simulaciones del modelo completo en la cuenca en V: `local`, `lateral`, `feddes`, `legacy`, `deep`, `deep_legacy`, `deep_empty` | Se ejecuta desde una copia de `Examples/VTilted_Excel`; error de volumen de `lateral` de $-1.7 \times 10^{-10}$ m³ |
| `run_feddes_legacy_consistency.m` | La ET de Feddes en el esquema predeterminado de tres capas es igual a la ET de Feddes en capas para el mismo estado; Feddes nunca extrae más que la regla sin estrés | verificación de consistencia |
| `run_layered_mesh_case.m` | Malla de Voronoi de 20 m en la cuenca en V con 2 HRU: predeterminado, en capas, en capas + Feddes | cada paso cierra la masa dentro de $10^{-8}$ del volumen de lluvia |

`run_deep_aquifer_initial_state_validation.m` verifica el estado inicial profundo $S_0 = q_0 A \tau$ con un fixture compartido con HydroPol2D-Python. `Validation/Groundwater/run_groundwater_release_checks.m` ejecuta todos estos scripts.

### Experimento gemelo de calibración {#calibration-twin-experiment}

Un experimento gemelo recuperó multiplicadores conocidos de la conductividad del suelo y del regolito a partir de una recesión sintética de 30 días con 0, 5 y 10 % de ruido. La configuración, los resultados y los límites se presentan en la página [Calibración por Recesión del Agua Subterránea](../calibration/groundwater-recession#5-twin-experiments).

### Lo que no cubre la evidencia del esquema en capas {#what-the-layered-evidence-does-not-cover}

- El flujo implícito en el nivel freático solo se prueba en Python.
- No hay un caso de campo. Las pruebas usan dominios sintéticos en V.
- Estas pruebas no resuelven los problemas abiertos indicados en [Límites conocidos](../theory/layered-subsurface#9-known-limits), incluida la circulación en el nivel freático.

## Lo que respalda esta validación {#what-this-validation-supports}

En conjunto, estos casos respaldan la acumulación de recarga implementada, el programador asincrónico, el ascenso y el abatimiento local del nivel freático a través de `S_y`, el ascenso capilar simple en capas y la dinámica lateral idealizada del agua subterránea en laderas.

Las pruebas del subsuelo en capas respaldan la implementación de la columna de suelo sobre regolito y la concordancia entre Python y MATLAB en casos controlados.

No validan parámetros regionales de acuíferos, flujo base de campo, bombeo de agua subterránea, comportamiento de acuíferos confinados ni calibración con pozos observados.
