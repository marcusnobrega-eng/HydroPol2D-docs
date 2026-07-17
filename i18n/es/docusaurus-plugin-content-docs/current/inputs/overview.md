---
title: Resumen
---

# Entradas del modelo

HydroPol2D usa una combinacion de rasters, hojas de calculo de parametros y archivos de forzantes. Esta pagina es el punto de entrada para los archivos que el modelo actual puede leer.

## Entradas espaciales principales

La mayoria de las simulaciones comienzan con tres rasters obligatorios:

1. [DEM](./dem)
2. [LULC](./lulc)
3. [Soil](./soil)

Estos definen la malla del modelo, las clases de uso y cobertura del suelo y las propiedades hidraulicas basicas del suelo.

## Entradas espaciales suplementarias

Otros rasters pueden usarse cuando el flujo de trabajo lo requiere:

- [DTB](./dtb) para profundidad del suelo o profundidad al basamento;
- [LAI](./lai) para la estructura espacial de la vegetacion;
- [Albedo](./albedo) para propiedades espaciales de energia superficial;
- [Additional Spatial Inputs](./additional-spatial-inputs) para groundwater inicial, fraccion impermeable, estados de warmup y rasters de calidad del agua.

Estas entradas son opcionales segun el caso de uso, no experimentales por definicion. Siempre que esten activas en un estudio de caso, eso debe documentarse.

## Entradas tabulares y de control

HydroPol2D tambien lee hojas de calculo:

- [Parameter Tables](./parameter-tables) para clases de LULC y suelo;
- `General_Data.xlsx` para flags, tiempos de simulacion, rutas de archivos y controles de ejecucion;
- hojas de forzantes o condiciones de contorno para lluvia, evapotranspiracion, inflow, stage o estructuras de control, cuando esas opciones esten activas.

## Entradas de forzantes

Los forzantes pueden prescribirse mediante hojas de calculo, calendarios raster o tormentas sinteticas. La pagina [Optional Forcing](./optional-forcing) documenta las rutas soportadas, incluidas series temporales de lluvia, rasters de lluvia, forzantes de evapotranspiracion, hidrogramas de entrada, contornos de nivel y tormentas de diseno.

## Reglas practicas

Los rasters deben:

- usar un sistema de coordenadas proyectado;
- estar alineados con el DEM, o ser reamostrables a esa malla;
- usar unidades consistentes;
- cubrir el dominio del modelo de forma limpia.

HydroPol2D puede reamostrar y enmascarar muchos rasters opcionales internamente, pero los flujos de trabajo reproducibles siguen dependiendo de archivos fuente limpios y consistentes con el dominio.

## Mapa rapido de entradas

| Grupo de entrada | Archivos tipicos |
|---|---|
| Terreno y clases principales | `DEM_path`, `LULC_path`, `SOIL_path` |
| Apoyo de zona vadosa y groundwater | `DTB_path`, `GW_table_path` |
| Refinamientos de propiedades superficiales | `LAI_path`, `Albedo_path`, `ImperviousFraction_path` |
| Estados iniciales | `Warmup_Depth_path`, `Initial_Soil_Moisture_path`, `Initial_Buildup_path` |
| Geometría del canal | `RiverWidths_path`, `RiverDepths_path` |
| Rasters de calidad del agua | `B1_path`, `B2_path`, `W1_path`, `W2_path` |
| Forzantes y archivos de contorno | hojas o calendarios raster de lluvia, ETP, inflow, stage y estructuras de control |

El comportamiento detallado de los rasters suplementarios y de los estados iniciales esta documentado en [Additional Spatial Inputs](./additional-spatial-inputs).
