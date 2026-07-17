---
title: Resumen
---

# HydroPol2D

HydroPol2D es un modelo hidrologico-hidrodinamico en malla raster para simular, de forma acoplada, agua superficial, almacenamiento en la zona vadosa, agua subterranea, calidad del agua, nieve y diagnosticos de riesgo.

Esta documentacion describe el modelo tal como esta implementado hoy. Tambien distingue entre rutas validadas, rutas diagnosticas y funcionalidades que siguen pausadas o experimentales.

## Alcance actual

El codigo actual incluye:

- intercepcion del dosel, evapotranspiracion, nieve, infiltracion y almacenamiento vadoso en capas;
- recarga subterranea, ascenso capilar, actualizaciones asincronas del groundwater saturado y flujo bidimensional de Boussinesq cuando el baseflow esta activo;
- enrutamiento superficial con las opciones local inertial, full momentum, diffusive D4, kinematic D4 y cellular automata;
- transporte de calidad del agua y exportacion en la salida;
- diagnosticos opcionales de inestabilidad humana.

## Como avanza una simulacion en HydroPol2D

A nivel general, HydroPol2D avanza el sistema acoplado en este orden:

1. aplica lluvia, caudales de entrada y forzantes meteorologicos;
2. actualiza intercepcion, nieve, evapotranspiracion, infiltracion y almacenamiento vadoso;
3. acumula recarga e intercambio capilar para el groundwater;
4. enruta el agua superficial con la familia de enrutamiento seleccionada;
5. actualiza las cargas subterraneas cuando actua el programador de groundwater;
6. devuelve exfiltracion, exceso de saturacion, calidad del agua y diagnosticos opcionales al estado en evolucion.

Esa secuencia es la que conecta los modulos hidrologicos, subterraneos, hidrodinamicos y diagnosticos en un solo modelo.

## Como leer la documentacion

Para la mayoria de los usuarios, el orden de lectura mas claro es:

1. [Resumen de configuracion](../configuration/overview) para los controles publicos y las flags.
2. [Resumen matematico](../theory/overview) para las ecuaciones gobernantes y la estructura conceptual.
3. [Resumen de validacion](../validation/overview) para la evidencia de validacion de cada modulo.
4. [Ejemplos](../Examples/RainfallRunoff) para flujos de trabajo reproducibles.
