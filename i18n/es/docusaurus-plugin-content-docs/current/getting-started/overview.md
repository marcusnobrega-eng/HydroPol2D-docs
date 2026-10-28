---
title: Resumen
---

# HydroPol2D

HydroPol2D es un modelo hidrológico-hidrodinámico en malla ráster para simular, de forma acoplada, agua superficial, almacenamiento en la zona vadosa, agua subterránea, calidad del agua, nieve y diagnósticos de riesgo.

Esta documentación describe el modelo tal como está implementado hoy. También distingue entre rutas validadas, rutas diagnósticas y funcionalidades que siguen pausadas o experimentales.

## Alcance actual

El código actual incluye:

- intercepción del dosel, evapotranspiración, nieve, infiltración y almacenamiento vadoso en capas;
- recarga subterránea, ascenso capilar, actualizaciones asíncronas del groundwater saturado y flujo bidimensional de Boussinesq cuando el baseflow está activo;
- enrutamiento superficial con las opciones local inertial, full momentum, diffusive D4, kinematic D4 y cellular automata;
- transporte de calidad del agua y exportación en la salida;
- diagnósticos opcionales de inestabilidad humana.

## Cómo avanza una simulación en HydroPol2D

A nivel general, HydroPol2D avanza el sistema acoplado en este orden:

1. aplica lluvia, caudales de entrada y forzantes meteorológicos;
2. actualiza intercepción, nieve, evapotranspiración, infiltración y almacenamiento vadoso;
3. acumula recarga e intercambio capilar para el groundwater;
4. enruta el agua superficial con la familia de enrutamiento seleccionada;
5. actualiza las cargas subterráneas cuando actúa el programador de groundwater;
6. devuelve exfiltración, exceso de saturación, calidad del agua y diagnósticos opcionales al estado en evolución.

Esa secuencia es la que conecta los módulos hidrológicos, subterráneos, hidrodinámicos y diagnósticos en un solo modelo.

## Interfaz de escritorio

[HydroPol2D Studio](../studio/overview) es la interfaz de escritorio de HydroPol2D-Python: construye
un modelo a partir de un mapa o de sus propios archivos, lo configura paso a paso, lo ejecuta y
muestra los resultados.

## Cómo leer la documentación

Para la mayoría de los usuarios, el orden de lectura más claro es:

1. [Ejecutar desde Excel](./excel-workflow) para los flujos de trabajo con hojas de cálculo probados, con malla regular y de Voronoi.
2. [Resumen de configuración](../configuration/overview) para los controles públicos y las flags.
3. [Arquitectura del ecosistema](./ecosystem-architecture) para la generación de mallas, los contratos compartidos y el papel de cada repositorio.
4. [Resumen matemático](../theory/overview) para las ecuaciones gobernantes y la estructura conceptual.
5. [Resumen de validación](../validation/overview) para la evidencia de validación de cada módulo.
6. [Ejemplos](../Examples/RainfallRunoff) para flujos de trabajo reproducibles.
