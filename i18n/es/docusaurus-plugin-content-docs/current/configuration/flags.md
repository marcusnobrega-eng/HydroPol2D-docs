---
title: Banderas modelo
---

# Banderas modelo

HydroPol2D se controla mediante indicadores binarios y categóricos definidos en `General_Data.xlsx`. Esta página documenta el comportamiento público expuesto por esas banderas y destaca dónde una bandera activa una ruta predeterminada validada frente a una ruta de diagnóstico o experimental.
---

## Banderas de límites y forzados

| Bandera | Descripción |
|---|---|
| $\mathrm{flag\_rainfall}$ | Activa el forzamiento de la lluvia sobre el dominio. |
| $\mathrm{flag\_spatial\_rainfall}$ | Utiliza lluvia distribuida espacialmente en lugar de lluvia uniforme. |
| $\mathrm{flag\_ETP}$ | Activa el cálculo de la evapotranspiración a partir del forzamiento meteorológico. |
| $\mathrm{flag\_input\_rainfall\_map}$ | Utiliza entrada de lluvia basada en ráster. |
| $\mathrm{flag\_rainfall\_multiple\_runs}$ | En desarrollo. |
| $\mathrm{flag\_data\_source}$ | En desarrollo. |
| $\mathrm{flag\_inflow}$ | Activa las condiciones de contorno del hidrograma de entrada. |
| $\mathrm{flag\_satellite\_rainfall}$ | Utiliza productos de lluvia derivados de satélites. |
| $\mathrm{flag\_alternated\_blocks}$ | Activa el método de tormenta de diseño de bloques alternos. |
| $\mathrm{flag\_huff}$ | Activa el método de distribución de tormentas Huff. |
| $\mathrm{flag\_stage\_hydrograph}$ | Aplica condiciones de contorno de etapa (nivel del agua). |
| $\mathrm{flag\_input\_ETP\_map}$ | Utiliza entradas de evapotranspiración basadas en ráster. |

---

## Banderas de proceso y enrutamiento

| Bandera | Descripción |
|---|---|
| $\mathrm{flag\_infiltration}$ | Activa la infiltración en el suelo y el almacenamiento vadoso. |
| $\mathrm{flag\_groundwater\_modeling}$ | Activa la recarga de aguas subterráneas y el acoplamiento local entre el nivel freático y el nivel freático. Con el suelo en capas habilitado, esto sigue la ruta de agua subterránea vadosa en capas predeterminada actual. |
| $\mathrm{flag\_groundwater\_async}$ | Utiliza actualizaciones asíncronas de agua subterránea saturada mientras mantiene el intercambio vadoso acoplado en cada paso de la superficie. Recomendado cuando el agua subterránea está activa. |
| $\mathrm{groundwater\_target\_dt\_min}$ | Intervalo objetivo de actualización de agua subterránea en minutos. |
| $\mathrm{groundwater\_min\_dt\_min}$ | Intervalo mínimo de actualización de agua subterránea en minutos. |
| $\mathrm{groundwater\_max\_head\_change\_m}$ | Cambio máximo acumulado de cabeza de agua subterránea antes de forzar una actualización. |
| $\mathrm{groundwater\_courant}$ | Factor de seguridad utilizado en el límite temporal explícito del agua subterránea. |
| $\mathrm{flag\_capillary\_rise}$ | Permite el ascenso capilar en capas desde aguas subterráneas poco profundas hasta el almacenamiento vadoso. |
| $\mathrm{flag\_baseflow}$ | Activa el enrutamiento lateral de aguas subterráneas 2D Boussinesq. |
| $\mathrm{flag\_snow\_modeling}$ | Activa acumulación, fusión, sublimación, densidad y profundidad de nieve por LULC. Requiere forzamiento meteorológico interno: `flag_ETP = 1` y `flag_input_ETP_map = 0`. |
| $\mathrm{flag\_waterquality}$ | Activa el transporte de calidad del agua. |
| $\mathrm{flag\_wq\_model}$ | Selecciona el modelo de acumulación/lavado de contaminantes. |
| $\mathrm{flag\_human\_instability}$ | Activa el diagnóstico de inestabilidad humana. Los modos implementados documentados públicamente son `1` y `3`; El modo `2` no está implementado. |
| $\mathrm{flag\_reservoir}$ | Activa el depósito o la lógica de control hidráulico interno. |
| $\mathrm{flag\_critical}$ | Aplica un limitador de flujo crítico cuando lo admite la familia de enrutamiento. |
| $\mathrm{flag\_boundary}$ | Hace cumplir todas las celdas límite como celdas de salida. |
| $\mathrm{flag\_neglect\_infiltration\_river}$ | Desactiva la infiltración en las células del río. |
| $\mathrm{flag\_real\_time\_satellite\_rainfall}$ | Permite la ingesta de lluvia satelital en tiempo real con Persiann. |
| $\mathrm{flag\_dam\_break}$ | En desarrollo. |
| $\mathrm{flag\_river\_rasters}$ | Utiliza entradas de geometría de río basadas en ráster. |
| $\mathrm{flag\_spatial\_albedo}$ | Utiliza albedo distribuido espacialmente en lugar de valores uniformes. |
| $\mathrm{flag\_DTM}$ | Utiliza correcciones o procesamiento de modelos de terreno digitales. |
| $\mathrm{flag\_abstraction}$ | Activa procesos de captación o extracción de agua. |
| $\mathrm{flag\_WQ\_Rasters}$ | Utiliza entradas de contaminantes basadas en ráster. |

---

## Banderas de familia de enrutamiento

| Bandera | Descripción |
|---|---|
| $\mathrm{flag\_inertial}$ | Activa el solucionador inercial local de aguas poco profundas. Esta es la familia de enrutamiento predeterminada recomendada. |
| $\mathrm{flag\_full\_momentum}$ | Activa el solucionador de aguas poco profundas de impulso total. Úselo como alternativa a las otras familias de enrutamiento principales, no en combinación con ellas. |
| $\mathrm{flag\_diffusive}$ | Activa el enrutamiento difusivo D4 impulsado por la pendiente de la superficie del agua. |
| $\mathrm{flag\_kinematic}$ | Activa el enrutamiento cinemático D4 impulsado por la pendiente del lecho y la profundidad del donante. |
| $\mathrm{flag\_CA}$ | Activa el enrutamiento de Cellular Automata. |
| $\mathrm{flag\_D8}$ | Activa una ruta de enrutamiento D8 secundaria. Esto debería tratarse como de alcance limitado y no como una familia de teorías paralelas completas. |
| $\mathrm{flag\_neal\_channel}$ | Activa la representación rectangular de canal incorporado de Neal (2012) en una malla estructurada. Requiere enrutamiento inercial local. |
| $\mathrm{flag\_structured\_lookup\_subgrid}$ | Activa tablas dependientes del nivel para celdas y caras en una malla estructurada. Este modo permanece condicionado a la paridad MATLAB-Python. |
| $\mathrm{flag\_voronoi\_subgrid}$ | Activa las tablas de celdas y caras de HydroBathyDEM en una malla Voronoi. |
| $\mathrm{flag\_voronoi}$ | Selecciona la topología de malla Voronoi. Es independiente de `flag_voronoi_subgrid`, que selecciona la representación hidráulica. |
| $\mathrm{flag\_numerical\_scheme}$ | Selecciona la variante del esquema inercial local: `1` Bates, `2` ceñida, `3` centrado. Se aplica a la familia inercial, no al enrutamiento de impulso total, difusivo, cinemático o CA. |
| $\mathrm{flag\_outlet\_type}$ | Tratamiento de salida: `1` flujo normal, `2` flujo crítico. |
| $\mathrm{flag\_adaptive\_timestepping}$ | Selecciona el control de paso de tiempo adaptativo. |

---

## Configuración del modelo submalla de Neal (2012)

El modo de canal submalla admitido sigue a [Neal et al. (2012)](https://doi.org/10.1029/2012WR012514). Use la siguiente combinación:

| Bandera | Valor requerido |
|---|---:|
| `flag_inertial` | `1` |
| `flag_neal_channel` | `1` |
| `flag_structured_lookup_subgrid` | `0` |
| `flag_voronoi_subgrid` | `0` |
| `flag_voronoi` | `0` |
| `flag_full_momentum` | `0` |
| `flag_diffusive` | `0` |
| `flag_kinematic` | `0` |
| `flag_CA` | `0` |
| `flag_river_rasters` | `1` cuando la geometría del canal se suministra mediante rásteres |

Las celdas con canal requieren `RiverWidths_path` y `RiverDepths_path`. El ancho y la profundidad deben ser positivos, y el ancho del canal debe ser menor que la resolución de la celda. El coeficiente de Manning del canal se asigna mediante la entrada de rugosidad del río o dentro de las márgenes. La rugosidad del uso y cobertura del suelo suministra el coeficiente de Manning de la llanura.

El solucionador calcula por separado los caudales del canal y de la llanura en cada cara ortogonal y actualiza el almacenamiento en términos de volumen. La formulación y el intervalo de validación se describen en [Modelo hidrodinámico](../theory/hydrodynamic-model) y [Validación del modelo submalla de Neal (2012)](../validation/neal-subgrid).

---

## Banderas de rendimiento

| Bandera | Descripción |
|---|---|
| $\mathrm{flag\_GPU}$ | Habilita la aceleración de GPU. |
| $\mathrm{flag\_single}$ | Utiliza aritmética de precisión simple para optimizar el rendimiento. |

---

## Banderas de condición inicial

| Bandera | Descripción |
|---|---|
| $\mathrm{flag\_warmup}$ | Activa el calentamiento del modelo para la estabilización del estado. |
| $\mathrm{flag\_initial\_buildup}$ | Inicializa las condiciones de acumulación de contaminantes. |

---

## DEM y banderas de procesamiento de terreno

| Bandera | Descripción |
|---|---|
| $\mathrm{flag\_resample}$ | Activa el remuestreo de ráster a una resolución objetivo. |
| $\mathrm{flag\_smoothening}$ | Aplica el suavizado DEM. |
| $\mathrm{flag\_trunk}$ | Solo se alisa el tronco principal del río. |
| $\mathrm{flag\_fill\_DEM}$ | Rellena las depresiones del DEM para lograr consistencia hidrológica. |
| $\mathrm{flag\_smooth\_cells}$ | Aplica suavizado del terreno a nivel de celda. |
| $\mathrm{flag\_reduce\_DEM}$ | Reduce la elevación del DEM en las celdas del río para tener en cuenta la batimetría del canal. |

---

## Banderas de salida y utilidad

| Bandera | Descripción |
|---|---|
| $\mathrm{flag\_export\_maps}$ | Permite la exportación de salidas ráster. |
| $\mathrm{flag\_dashboard}$ | Activa salidas o visualizaciones estilo tablero. |
| $\mathrm{flag\_elapsed\_time}$ | Realiza un seguimiento del tiempo de ejecución de la simulación. |
| $\mathrm{flag\_obs\_gauges}$ | Activa la extracción de salida en los medidores de observación. |

---

## Notas

- Sólo una familia de enrutamiento principal debe estar activa a la vez: `flag_full_momentum`, `flag_inertial`, `flag_diffusive`, `flag_kinematic` o `flag_CA`.
- Seleccione como máximo una formulación submalla: canal Neal, lookup estructurado o lookup Voronoi.
- El modo de canal de Neal (2012) requiere enrutamiento inercial local y `flag_neal_channel = 1`.
- `flag_voronoi = 1` selecciona la topología; `flag_voronoi_subgrid = 1` activa además la hidráulica lookup Voronoi.
- Los antiguos `flag_subgrid` y `flag_overbanks` se aceptan sólo en la capa de migración y generan una advertencia explícita.
- `flag_D8` debe tratarse como secundario/de alcance limitado en lugar de otra familia de enrutamiento lista para generar informes.
- La programación asíncrona del agua subterránea y el ascenso capilar son comportamientos de configuración públicos, no detalles internos ocultos.
- Los parámetros de nieve se definen por clase en la tabla LULC. `Initial_SWE_path` e `Initial_Snow_Depth_path` son rásteres iniciales opcionales.
- El modo de inestabilidad humana `2` no está implementado y no debe presentarse como un método público disponible.
