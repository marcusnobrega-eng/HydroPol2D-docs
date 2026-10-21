---
title: Resumen
---

# Entradas del modelo

HydroPol2D usa una combinación de rasters, hojas de cálculo de parámetros y archivos de forzantes. Esta página es el punto de entrada para los archivos que el modelo actual puede leer.

## Entradas espaciales principales

La mayoría de las simulaciones comienzan con tres rasters obligatorios:

1. [DEM](./dem)
2. [LULC](./lulc)
3. [Soil](./soil)

Estos definen la malla del modelo, las clases de uso y cobertura del suelo y las propiedades hidráulicas básicas del suelo.

## Entradas espaciales suplementarias

Otros rasters pueden usarse cuando el flujo de trabajo lo requiere:

- [DTB](./dtb) para profundidad del suelo o profundidad al basamento;
- [LAI](./lai) para la estructura espacial de la vegetación;
- [Albedo](./albedo) para propiedades espaciales de energía superficial;
- [Additional Spatial Inputs](./additional-spatial-inputs) para groundwater inicial, fracción impermeable, estados de warmup y rasters de calidad del agua.

Estas entradas son opcionales según el caso de uso, no experimentales por definición. Siempre que estén activas en un estudio de caso, eso debe documentarse.

## Entradas tabulares y de control

HydroPol2D también lee hojas de cálculo:

- el libro del caso de MATLAB `HydroPol2D_Inputs.xlsx`, cuyas pestañas de parámetros contienen los interruptores, los tiempos, las rutas de archivos y los controles de ejecución ([Parámetros del libro del caso](../configuration/general_data));
- sus pestañas de tablas de clases para las clases de uso del suelo y de suelo, la inestabilidad humana, la malla y las estructuras de control ([Tablas de parámetros](./parameter-tables));
- sus pestañas de series para la lluvia, las estaciones climáticas, los caudales de entrada y los niveles, cuando esas opciones están activas ([Forzamientos opcionales](./optional-forcing)).

Los casos antiguos guardan estos datos en `General_Data.xlsx` y en libros de Excel separados. Ambos formatos siguen funcionando.

## Entradas de forzantes

Los forzantes pueden prescribirse mediante hojas de cálculo, calendarios raster o tormentas sintéticas. La página [Optional Forcing](./optional-forcing) documenta las rutas soportadas, incluidas series temporales de lluvia, rasters de lluvia, forzantes de evapotranspiración, hidrogramas de entrada, contornos de nivel y tormentas de diseño.

## Reglas prácticas

Los rasters deben:

- usar un sistema de coordenadas proyectado;
- estar alineados con el DEM, o ser reamostrables a esa malla;
- usar unidades consistentes;
- cubrir el dominio del modelo de forma limpia.

HydroPol2D puede reamostrar y enmascarar muchos rasters opcionales internamente, pero los flujos de trabajo reproducibles siguen dependiendo de archivos fuente limpios y consistentes con el dominio.

## Mapa rápido de entradas

| Grupo de entrada | Archivos típicos |
|---|---|
| Terreno y clases principales | `DEM_path`, `LULC_path`, `SOIL_path` |
| Apoyo de zona vadosa y groundwater | `DTB_path`, `GW_table_path` |
| Subsuelo en capas (opcional) | `SoilBaseDepth_path`, `RegolithThetaS_path`, `RegolithThetaR_path`, `RegolithAlphaVG_path`, `RegolithNVG_path`, `RegolithKsatV_path`, `RegolithKsatH_path`, `RegolithSpecificYield_path` |
| Acuífero profundo (opcional) | `DeepAquiferSubbasins_path`, `DeepAquiferChannelWeight_path`, `DeepAquiferInitialState_path` |
| Refinamientos de propiedades superficiales | `LAI_path`, `Albedo_path`, `ImperviousFraction_path` |
| Estados iniciales | `Warmup_Depth_path`, `Initial_Soil_Moisture_path`, `Initial_SWE_path`, `Initial_Snow_Depth_path`, `Initial_Buildup_path` |
| Geometría del canal | `RiverWidths_path`, `RiverDepths_path` |
| Rasters de calidad del agua | `B1_path`, `B2_path`, `W1_path`, `W2_path` |
| Forzantes y archivos de contorno | hojas o calendarios raster de lluvia, ETP, inflow, stage y estructuras de control |

El comportamiento detallado de los rasters suplementarios y de los estados iniciales está documentado en [Additional Spatial Inputs](./additional-spatial-inputs).
