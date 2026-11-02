---
title: Resumen
---
import useBaseUrl from '@docusaurus/useBaseUrl';

# HydroPol2D

HydroPol2D es un modelo hidrológico-hidrodinámico en malla ráster para simular, de forma acoplada, agua superficial, almacenamiento en la zona vadosa, agua subterránea, calidad del agua, nieve y diagnósticos de riesgo.

Esta documentación describe el modelo tal como está implementado hoy. También distingue entre rutas validadas, rutas diagnósticas y funcionalidades que siguen pausadas o experimentales.

## Alcance actual

El código actual incluye:

- intercepción del dosel, evapotranspiración, nieve, infiltración y almacenamiento vadoso en capas;
- recarga subterránea, ascenso capilar, actualización del nivel freático en cada paso y flujo lateral bidimensional de Boussinesq con un calendario asíncrono cuando el baseflow está activo;
- enrutamiento superficial con las opciones local inertial, full momentum, diffusive D4, kinematic D4 y cellular automata;
- transporte de calidad del agua y exportación en la salida;
- diagnósticos opcionales de inestabilidad humana.

<p align="center">
  <img src={useBaseUrl('/img/getting-started/questions-modules-outputs.es.svg')} width="720" alt="Seis filas, cada una con una pregunta, el módulo de HydroPol2D que la responde, con su estado estándar u opcional y su evidencia de validación, y la salida en mapa o serie de tiempo que la muestra, sobre una leyenda y una nota acerca de lo que muestra Results" />
</p>

<p align="center">
  <em>Figura 1. Preguntas que HydroPol2D responde, el módulo que responde cada una, con su estado, y la salida que la muestra. El estado sigue las páginas de validación.</em>
</p>

## Cómo avanza una simulación en HydroPol2D

A nivel general, HydroPol2D avanza el sistema acoplado en este orden:

1. aplica la lluvia y los forzantes meteorológicos;
2. actualiza intercepción, nieve, evapotranspiración, infiltración y almacenamiento vadoso;
3. acumula recarga e intercambio capilar para el groundwater;
4. actualiza el nivel freático en cada paso, devuelve la exfiltración y el exceso de saturación a la superficie y ejecuta el flujo subterráneo lateral cuando el programador del agua subterránea lo indica;
5. añade los hidrogramas de entrada y enruta el agua superficial con la familia de enrutamiento seleccionada;
6. actualiza la calidad del agua y los diagnósticos opcionales de riesgo.

Esa secuencia es la que conecta los módulos hidrológicos, subterráneos, hidrodinámicos y diagnósticos en un solo modelo.

<p align="center">
  <img src={useBaseUrl('/img/getting-started/time-step-order.es.svg')} width="720" alt="Seis pasos de un paso de tiempo superficial en ciclo: forzantes; nieve, dosel y suelo; recarga y ascenso capilar; nivel freático; enrutamiento superficial; calidad del agua y riesgo. Al lado, el reloj superficial con su paso de Courant y el reloj del agua subterránea con sus tres disparadores; debajo, una franja con los pasos superficiales y las actualizaciones del flujo lateral a lo largo de una simulación" />
</p>

<p align="center">
  <em>Figura 2. El orden de un paso de tiempo superficial, el reloj superficial que fija su duración y el reloj del agua subterránea que decide cuándo corre el flujo lateral. La franja inferior muestra los dos relojes a lo largo de una simulación, sin escala.</em>
</p>

## Interfaz de escritorio

[HydroPol2D Studio](../studio/overview) es la interfaz de escritorio de HydroPol2D-Python: construye
un modelo a partir de un mapa o de sus propios archivos, lo configura paso a paso, lo ejecuta y
muestra los resultados.

<p align="center">
  <img src={useBaseUrl('/img/getting-started/data-to-results.es.svg')} width="720" alt="Mapas, tablas de parámetros, forzantes y configuración alimentan un caso, un archivo de modelo de HydroPol2D Studio o un libro de HydroPol2D-MATLAB; el caso se ejecuta en Studio o en MATLAB, y las salidas son mapas, series de tiempo, animaciones y un paquete de resultados" />
</p>

<p align="center">
  <em>Figura 3. De los datos a los resultados. Las mismas entradas forman un caso, un archivo de modelo de Studio o un libro de MATLAB, y cada ejecución escribe mapas, series de tiempo y animaciones.</em>
</p>

## Cómo leer la documentación

Para la mayoría de los usuarios, el orden de lectura más claro es:

1. [Ejecutar desde Excel](./excel-workflow) para los flujos de trabajo con hojas de cálculo probados, con malla regular y de Voronoi.
2. [Resumen de configuración](../configuration/overview) para los controles públicos y las flags.
3. [Arquitectura del ecosistema](./ecosystem-architecture) para la generación de mallas, los contratos compartidos y el papel de cada repositorio.
4. [Resumen matemático](../theory/overview) para las ecuaciones gobernantes y la estructura conceptual.
5. [Resumen de validación](../validation/overview) para la evidencia de validación de cada módulo.
6. [Ejemplos](../Examples/RainfallRunoff) para flujos de trabajo reproducibles.
