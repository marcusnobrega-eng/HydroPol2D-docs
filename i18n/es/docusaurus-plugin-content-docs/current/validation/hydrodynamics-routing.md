---
title: Hidrodinámica y enrutamiento
---
import useBaseUrl from '@docusaurus/useBaseUrl';

# Validación de la hidrodinámica y el enrutamiento

La validación hidrodinámica de la Fase 1 se organizó por familia de enrutamiento. La secuencia evaluó el modelo de momento completo, los métodos inercial local y autómatas celulares y, por último, los modelos cinemático y difusivo corregidos. Las pruebas verifican hidrogramas, conservación, simetría, condiciones de contorno y el comportamiento esperado de cada conjunto de ecuaciones.

## Hidrodinámica con momento completo

Se usaron cinco casos: hidrograma sobre un plano inclinado, simetría y conservación en la cuenca en V, rotura de presa de Ritter sobre lecho seco, onda sin rotura y condición de contorno con nivel prescrito.

| Caso | RMSE principal | L2 relativo | NSE | Error de masa (%) |
|---|---:|---:|---:|---:|
| Hidrograma sobre plano inclinado | 0,0264 | 0,0311 | 0,9961 | `7,80 × 10^-12` |
| Simetría y conservación en V | `3,50 × 10^-18` | -- | -- | `2,74 × 10^-12` |
| Perfil de Ritter | 0,0305 | 0,0567 | 0,9992 | `1,26 × 10^-13` |
| Perfil de onda sin rotura | 0,0116 | 0,0260 | 0,9997 | 4,5638 |
| Contorno con nivel prescrito | 0,0000 | -- | -- | `1,35 × 10^-13` |

El plano inclinado reprodujo el límite de onda cinemática. La cuenca en V conservó la masa hasta la precisión numérica y mantuvo la simetría bilateral. El caso de Ritter verificó un flujo discontinuo, y la onda sin rotura evaluó una perturbación móvil suave.

<img src={useBaseUrl('/validation/phase1/hydrodynamics/P1_HYDRO_FM_PLANE_001.png')} alt="Validación del momento completo sobre el plano inclinado" />

<img src={useBaseUrl('/validation/phase1/hydrodynamics/P1_HYDRO_FM_VTILT_001.png')} alt="Validación del momento completo en la cuenca en V" />

<img src={useBaseUrl('/validation/phase1/hydrodynamics/P1_HYDRO_FM_RITTER_001.png')} alt="Validación de Ritter con momento completo" />

<img src={useBaseUrl('/validation/phase1/hydrodynamics/P1_HYDRO_FM_NBW_001_PROFILES.png')} alt="Perfiles de la onda sin rotura con momento completo" />

## Modelo inercial local y autómatas celulares

El modelo inercial local aproxima las ecuaciones de aguas someras. El método de autómatas celulares redistribuye flujo y almacenamiento, pero no es un solucionador de momento. El modelo inercial local superó las pruebas del plano inclinado, la cuenca en V y el contorno con nivel prescrito. La comparación de Ritter se mantiene como diagnóstico. Los autómatas celulares superaron las pruebas de conservación, simetría y contabilidad en las condiciones de contorno.

| Método | Caso | RMSE | L2 relativo | NSE | Error de masa (%) | Estado |
|---|---|---:|---:|---:|---:|---|
| Inercial local | Plano | 0,0169 | 0,0200 | 0,9984 | `7,47 × 10^-12` | aprobado |
| Inercial local | Cuenca en V | 0,0000 | -- | -- | `3,66 × 10^-12` | aprobado |
| Inercial local | Ritter | 0,1823 | 0,3838 | 0,9552 | `5,05 × 10^-14` | diagnóstico no aprobado |
| Autómatas celulares | Plano | 0,0172 | 0,0204 | 0,9983 | `7,69 × 10^-12` | aprobado |
| Autómatas celulares | Cuenca en V | 0,0000 | -- | -- | `4,04 × 10^-12` | aprobado |
| Autómatas celulares | Ritter | 0,1592 | 0,2957 | 0,9875 | `7,58 × 10^-14` | diagnóstico |

<div style={{display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(280px, 1fr))', gap: '1rem'}}>
  <img src={useBaseUrl('/validation/phase1/hydrodynamics/P1_HYDRO_LI_PLANE_001.png')} alt="Modelo inercial local sobre el plano inclinado" />
  <img src={useBaseUrl('/validation/phase1/hydrodynamics/P1_HYDRO_CA_PLANE_001.png')} alt="Autómatas celulares sobre el plano inclinado" />
</div>

<div style={{display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(280px, 1fr))', gap: '1rem'}}>
  <img src={useBaseUrl('/validation/phase1/hydrodynamics/P1_HYDRO_LI_RITTER_001.png')} alt="Diagnóstico de Ritter para el modelo inercial local" />
  <img src={useBaseUrl('/validation/phase1/hydrodynamics/P1_HYDRO_CA_RITTER_001.png')} alt="Diagnóstico de Ritter para autómatas celulares" />
</div>

El resultado de Ritter para el modelo inercial local identifica un límite del método. No constituye una validación para rotura de presa sobre lecho seco.

## Hidrograma canónico de la cuenca en V

El hidrograma original de la cuenca en V se evaluó con el flujo completo de configuración y preprocesamiento de HydroPol2D. Todos los métodos usaron el mismo ráster de `20 m`, lluvia de `10,8 mm/h` durante `90 min`, las mismas celdas de salida y los procesos de pérdida desactivados.

Los cinco métodos reprodujeron la forma del hidrograma entre `0 min` y `180 min`. El error del balance lluvia-salida-almacenamiento fue `-0,0181 %` en todas las simulaciones.

| Método | RMSE (m³/s) | NSE | Error del pico (%) | Error de volumen (%) | Error de masa (%) |
|---|---:|---:|---:|---:|---:|
| Momento completo | 0,303 | 0,9730 | 0,052 | 7,50 | -0,0181 |
| Inercial local | 0,287 | 0,9759 | 2,05 | 5,04 | -0,0181 |
| Autómatas celulares | 0,323 | 0,9694 | 0,008 | 3,95 | -0,0181 |
| Cinemático | 0,249 | 0,9817 | 0,020 | 3,23 | -0,0181 |
| Difusivo | 0,255 | 0,9809 | 0,063 | 3,20 | -0,0181 |

<img src={useBaseUrl('/validation/phase1/hydrodynamics/P1_HYDRO_VTILT_ROUTING_HYDROGRAPH.png')} alt="Hidrograma canónico de la cuenca en V" />

<img src={useBaseUrl('/validation/phase1/hydrodynamics/P1_HYDRO_VTILT_ROUTING_VOLUME.png')} alt="Volumen acumulado en la salida de la cuenca en V" />

## Enrutamiento cinemático y difusivo corregido

Los modelos cinemático y difusivo usan un núcleo conservativo común para los flujos en las caras D4. Ambos superaron las pruebas del plano inclinado, conservación en la cuenca en V y contorno con nivel prescrito. El caso difusivo de Ritter no se aprobó, como se espera para una aproximación de onda difusiva aplicada a una discontinuidad sobre lecho seco.

| Método | Caso | RMSE | L2 relativo | NSE | Error de masa (%) | Estado |
|---|---|---:|---:|---:|---:|---|
| Cinemático | Plano | 0,0156 | 0,0184 | 0,9986 | `7,66 × 10^-12` | aprobado |
| Cinemático | Cuenca en V | 0,0000 | -- | -- | `4,18 × 10^-12` | aprobado |
| Cinemático | Ritter | 0,2408 | 0,5069 | 0,9245 | 0,0000 | diagnóstico |
| Difusivo | Plano | 0,0172 | 0,0203 | 0,9984 | `7,75 × 10^-12` | aprobado |
| Difusivo | Cuenca en V | 0,0000 | -- | -- | `3,73 × 10^-12` | aprobado |
| Difusivo | Ritter | 0,5670 | 1,1151 | -0,0803 | `1,53 × 10^-12` | diagnóstico no aprobado |

<div style={{display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(280px, 1fr))', gap: '1rem'}}>
  <img src={useBaseUrl('/validation/phase1/hydrodynamics/P1_HYDRO_KIN_PLANE_001.png')} alt="Validación del modelo cinemático corregido" />
  <img src={useBaseUrl('/validation/phase1/hydrodynamics/P1_HYDRO_DIFF_PLANE_001.png')} alt="Validación del modelo difusivo corregido" />
</div>

## Interpretación respaldada por las pruebas

La Fase 1 respalda la implementación actual de momento completo en las pruebas analíticas y de balance indicadas. También respalda los métodos inercial local, autómatas celulares, cinemático y difusivo en los casos controlados presentados. Los resultados de Ritter no deben interpretarse como validación de los modelos inercial local y difusivo para rotura de presa sobre lecho seco.

## Modelo submalla de Neal (2012)

La extensión de Neal (2012) representa un canal más estrecho que la celda inercial local y combina los caudales del canal y de la llanura en cada cara ortogonal. Las comparaciones con referencias numéricas de malla fina abarcan flujo dentro de las márgenes, canal compuesto permanente y transitorio, activación de las márgenes y extensión máxima de inundación. La formulación mejora el hidrograma, el nivel, el almacenamiento y el área mojada respecto de la malla gruesa ordinaria en todos los casos conservados. La recesión tardía en la llanura es menos precisa porque cada celda gruesa tiene un solo nivel representativo de agua.

La geometría, las métricas y las figuras se presentan en [Validación del modelo submalla de Neal (2012)](./neal-subgrid).
