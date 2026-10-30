---
title: Validación de la malla de Voronoi
---
import useBaseUrl from '@docusaurus/useBaseUrl';

# Validación de la malla de Voronoi

Los productos de Voronoi se generan con HydroBathyDEM y se utilizan a través del
contrato de malla compartido descrito en [Arquitectura del ecosistema](../getting-started/ecosystem-architecture).
HydroPolMesh es un prototipo de migración, no una dependencia de ejecución.

La vía de volúmenes finitos de Voronoi es un modo de malla distinto del flujo
de trabajo ráster D4 de producción. Usa las áreas exactas de los polígonos y la
topología de las aristas, y puede combinar el flujo 2D resuelto con un grafo de
canales submalla al estilo de Neal para ríos más estrechos que la malla.

<p align="center">
  <img src={useBaseUrl('/img/validation/grid-voronoi-subgrid.es.svg')} width="720" alt="Dos paneles comparan la malla ráster regular D4 y la malla de Voronoi: celdas y enlaces, métodos de enrutamiento y módulos opcionales; debajo, las opciones de submalla de cada una, con el enrutamiento que exige cada opción" />
</p>

<p align="center">
  <em>Figura 1. La malla ráster regular y la malla de Voronoi, que también ejecuta quadtrees. En la malla, los módulos opcionales se ejecutan en el motor de CPU (NumPy), sin la clasificación del modo 3.</em>
</p>

## Alcance admitido actualmente {#current-supported-scope}

| Modo de enrutamiento | Polígonos 2D resueltos | Grafo de canales de Neal | Estado de ejecución |
|---|---|---|---|
| Inercial local | sí | sí | validación en CPU aprobada |
| Cinemático | sí | no | validación de humo (smoke) en CPU aprobada |
| Difusivo explícito | sí | no | validación de humo (smoke) en CPU aprobada |
| Momento completo | sí | no | validación con benchmark en CPU aprobada |

La ejecución en GPU está bloqueada de forma intencionada. Las mallas a escala de
la India tampoco están validadas todavía. Ninguna de las dos debe deducirse de
los resultados controlados en CPU.

Las opciones públicas de submalla distinguen el canal de Neal en la malla
estructurada, las tablas de consulta estructuradas y las relaciones de submalla
de Voronoi. Activar una de ellas no activa de forma silenciosa ninguna de las
otras.

## Qué se verifica {#what-is-checked}

Las pruebas de la malla y del solucionador abarcan la validez de la geometría,
la conservación, el lago en reposo, el mojado y secado, la contabilidad de los
forzamientos y del agua subterránea, las transiciones entre flujo resuelto y
submalla, y las comparaciones con referencias de malla fina. El paso de tiempo
está limitado por la suma de las capacidades de señal en todas las caras
incidentes. En un grafo de Neal, también se usan el límite de recorrido de cada
enlace de canal y de cada transición, y el límite de almacenamiento en cada nodo
del canal.

La prueba autónoma de CFL del canal usa dos enlaces de 100 m que se unen en un
nodo y una transición entre flujo resuelto y submalla. Su primer paso adaptativo
es de 7,821 s, frente a un límite de onda de 15,641 s para un solo enlace, y la
masa cierra exactamente. Esto confirma que el limitador del grafo tiene en cuenta
todas las trayectorias incidentes.

## Módulos opcionales {#optional-modules}

En el motor de CPU, HydroPol2D-Python ejecuta los módulos opcionales de la malla
ráster regular sobre las celdas de la malla, cada uno con las propias ecuaciones
de la malla ráster. Las pruebas ejecutan cada módulo en la malla ráster y en una
malla formada por las propias celdas cuadradas de la malla ráster, y comparan:

| Módulo | Comparado en la malla cuadrada |
|---|---|
| Inestabilidad humana | Índice final y máximo, mapas del índice; la velocidad en las celdas de la malla frente a la de la malla ráster en campos aleatorios |
| Nieve | Mapas de SWE, profundidad e infiltración, suelo heredado y en capas |
| Embalses | Caudal liberado, almacenamiento y todas las series de los contornos internos |
| Drenaje urbano | Cargas y almacenamiento en los nodos, caudal en tuberías y sumideros, volumen en los puntos de descarga, número de subpasos |
| Calidad del agua | Masa de contaminante, exportación y concentración; el lavado en las aristas frente al de la malla ráster en campos aleatorios |
| Infraestructura verde | Almacenamiento, captura, desbordamiento, exfiltración y dren inferior por instalación, los tres mapas de infraestructura verde, suelo heredado y en capas |
| Estanques de detención | Nivel, almacenamiento, entrada lateral y caudales de los dispositivos, con y sin agua subterránea, suelo heredado y en capas |

Cada par coincide hasta 1e-10 o mejor, y cada simulación en malla cierra su
balance de agua hasta 1e-9 m³. Las comparaciones usan un flujo suave, en el que
los dos solucionadores superficiales coinciden hasta el redondeo;
[Limitaciones](./limitations#voronoi-mesh-mode) enumera lo que sigue abierto.

## Interpretación {#interpretation}

Estos resultados establecen que las vías numéricas evaluadas se comportan de
forma conservativa en sus casos controlados. No validan predicciones de
inundación a escala de campo, decisiones de generación de malla para una cuenca
específica, la ejecución en GPU ni el rendimiento de producción en la India.
Para ello se requieren un control de calidad específico de la malla, pruebas
comparativas del tiempo de ejecución y la comparación con observaciones o con
una referencia justificable.

El registro ejecutable del lado del modelo se mantiene en el repositorio, en
`Validation/Voronoi/README.md` y `Validation/Voronoi/VALIDATION_RESULTS.md`.
