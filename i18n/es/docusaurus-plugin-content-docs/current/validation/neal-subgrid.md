---
title: Modelo submalla de Neal (2012)
sidebar_label: Modelo submalla
---
import useBaseUrl from '@docusaurus/useBaseUrl';

# Validación del modelo submalla de Neal (2012)

HydroPol2D representa canales más estrechos que una celda del modelo mediante la formulación rectangular de [Neal et al. (2012)](https://doi.org/10.1029/2012WR012514). El canal y la llanura de inundación intercambian agua dentro de cada celda gruesa. Sus caudales se calculan por separado y se combinan en las caras de las celdas.

La validación compara tres simulaciones inerciales locales:

1. una malla fina que resuelve explícitamente el canal y la llanura;
2. una malla gruesa ordinaria sin geometría de canal embebida;
3. una malla gruesa con la formulación de canal submalla de Neal (2012).

La simulación de malla fina es una referencia numérica. Permite evaluar si la representación submalla conserva la respuesta hidráulica que se pierde al aumentar el tamaño de celda.

## Canal simple con flujo dentro de las márgenes

El primer caso aísla el flujo en un canal más estrecho que las celdas gruesas. El tramo tiene un canal de `10 m` de ancho y `1 m` de profundidad, una pendiente de fondo de `0,001` y un coeficiente de Manning $n=0,035$. La referencia explícita usa celdas de `10 m`. Las simulaciones ordinaria y Neal (2012) usan celdas de `30 m`.

Se aplica un caudal constante de $5\ \mathrm{m^3\,s^{-1}}$ a un tramo inicialmente seco de 30 celdas. Como el caudal permanece por debajo de la capacidad del canal, la prueba evalúa el almacenamiento, la propagación de la onda y el nivel del agua sin flujo sobre la llanura.

| Modelo grueso | RMSE del caudal (m³/s) | NSE | RMSE del nivel (m) | RMSE del perfil (m) |
|---|---:|---:|---:|---:|
| Ordinario | 0,677 | 0,561 | 0,689 | 0,689 |
| Neal (2012) | 0,098 | 0,991 | 0,053 | 0,059 |

La malla gruesa ordinaria considera que todo el ancho de `30 m` contiene agua en movimiento. Por ello, almacena demasiada agua y retrasa el hidrograma. El canal embebido de `10 m` produce un nivel y un tiempo de propagación más próximos a la referencia explícita.

<img src={useBaseUrl('/validation/phase1/subgrid-neal/simple-channel-hydrograph-stage.png')} alt="Caudal de salida y nivel interno en las simulaciones fina, gruesa ordinaria y con canal de Neal (2012)" />

<img src={useBaseUrl('/validation/phase1/subgrid-neal/simple-channel-profile.png')} alt="Perfiles longitudinales de la superficie del agua en las simulaciones fina, gruesa ordinaria y con canal de Neal (2012)" />

## Canal compuesto

El segundo caso usa un tramo de `990 m` con un canal de `10 m` de ancho y `1 m` de profundidad y llanuras laterales de `90 m` a cada lado. La pendiente longitudinal es `0,005`, y se usa el coeficiente de Manning $n=0,035$ en toda la sección. La referencia explícita usa celdas de `10 m`; las dos simulaciones gruesas usan celdas de `30 m`.

La prueba permanente aplica $100\ \mathrm{m^3\,s^{-1}}$. La prueba transitoria aplica un hidrograma de Nash con un pico de $100\ \mathrm{m^3\,s^{-1}}$ a los `30 min`.

| Forzamiento | Modelo grueso | RMSE en la salida (m³/s) | NSE en la salida | RMSE interno (m³/s) | RMSE del almacenamiento (m³) |
|---|---|---:|---:|---:|---:|
| Constante | Ordinario | 6,178 | 0,954 | 4,819 | 2.439 |
| Constante | Neal (2012) | 4,189 | 0,979 | 3,346 | 734 |
| Hidrograma de Nash | Ordinario | 7,263 | 0,949 | 5,770 | 3.363 |
| Hidrograma de Nash | Neal (2012) | 4,044 | 0,984 | 2,987 | 781 |

La simulación de Neal (2012) reduce los errores de caudal y almacenamiento con ambos forzamientos. La comparación transitoria muestra que la mejora se mantiene durante el ascenso, el pico y la recesión del hidrograma.

<img src={useBaseUrl('/validation/phase1/subgrid-neal/composite-constant-hydrographs.png')} alt="Hidrogramas con caudal constante para las simulaciones explícita, gruesa ordinaria y con canal de Neal (2012)" />

<img src={useBaseUrl('/validation/phase1/subgrid-neal/composite-nash-hydrographs.png')} alt="Hidrograma de entrada de Nash e hidrogramas simulados en la salida y en la sección interna" />

## Flujo escalonado sobre las márgenes

El tercer caso evalúa la transición entre el canal y la llanura de inundación. El tramo de `1 km` tiene `300 m` de ancho y una pendiente longitudinal de `0,005`. La sección transversal contiene:

- un canal de `50 m` con coeficiente de Manning $n=0,035$;
- dos banquetas de `25 m`, situadas `0,5 m` sobre el lecho del canal;
- una llanura externa situada `1,0 m` sobre el lecho, con coeficiente de Manning $n=0,10$.

La referencia explícita usa celdas de `5 m`. Las simulaciones ordinaria y Neal (2012) usan celdas de `100 m`. Un hidrograma de Nash alcanza $200\ \mathrm{m^3\,s^{-1}}$ a los `45 min`, por encima de los caudales analíticos de activación de $31,4\ \mathrm{m^3\,s^{-1}}$ para las banquetas y $110,8\ \mathrm{m^3\,s^{-1}}$ para la llanura externa.

<img src={useBaseUrl('/validation/phase1/subgrid-neal/staged-geometry-rating.png')} alt="Geometría escalonada del canal y curva analítica de caudal uniforme" />

| Métrica | Ordinario, 100 m | Neal (2012), 100 m |
|---|---:|---:|
| RMSE del caudal en la salida (m³/s) | 15,476 | 2,723 |
| NSE del caudal en la salida | 0,945 | 0,998 |
| RMSE del caudal en la sección interna (m³/s) | 12,053 | 3,043 |
| RMSE de profundidad en las banquetas (m) | 0,180 | 0,018 |
| RMSE de profundidad máxima (m) | 0,280 | 0,040 |
| CSI del área mojada a 0,01 m | 0,334 | 0,998 |

El modelo de Neal (2012) reproduce la activación de las banquetas a los `21 min`, el mismo instante que la referencia explícita. La llanura externa se activa a los `35 min`, frente a `34 min` en la referencia. El hidrograma, la profundidad y la extensión máxima de inundación son más próximos a la referencia que los resultados de la malla ordinaria de `100 m`.

<img src={useBaseUrl('/validation/phase1/subgrid-neal/staged-hydrographs.png')} alt="Hidrogramas en la salida y en la sección interna del canal escalonado" />

<img src={useBaseUrl('/validation/phase1/subgrid-neal/staged-depth-activation.png')} alt="Profundidades en el canal, las banquetas y la llanura externa a lo largo del tiempo" />

<img src={useBaseUrl('/validation/phase1/subgrid-neal/staged-maximum-depth.png')} alt="Mapas de profundidad máxima para las simulaciones explícita, gruesa ordinaria y de Neal (2012)" />

Todos los casos conservados cierran el balance de agua hasta la precisión numérica. La prueba escalonada también identifica una limitación. Las banquetas del modelo de Neal (2012) se secan a los `126 min`, frente a `196 min` en la referencia explícita, y la llanura externa se seca a los `152 min`, frente a `237 min`. Una celda gruesa de Neal (2012) tiene un solo nivel representativo de agua. Por tanto, el agua residual sobre las banquetas y la llanura no puede drenar de forma independiente del canal embebido.

## Interpretación respaldada por las pruebas

Las pruebas respaldan la formulación de Neal (2012) para flujo controlado dentro de las márgenes, activación de la llanura, hidráulica de pico y extensión máxima de inundación en las geometrías evaluadas. No establecen la precisión a escala de campo. Las aplicaciones con recesiones prolongadas en la llanura deben comparar el tiempo de drenaje con observaciones o con una referencia hidráulica más fina.

Las ecuaciones y los datos de entrada necesarios se describen en las páginas [Modelo hidrodinámico](../theory/hydrodynamic-model) y [Banderas del modelo](../configuration/flags).
