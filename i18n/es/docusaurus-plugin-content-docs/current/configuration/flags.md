---
title: Banderas del modelo
---

# Banderas del modelo

HydroPol2D se controla mediante interruptores binarios y categóricos. En el libro del caso `HydroPol2D_Inputs.xlsx`, cada interruptor está al inicio del bloque que controla, en la pestaña de su proceso, y el bloque se muestra en gris mientras el interruptor vale 0. No hay una hoja `Flags` separada. La página [Parámetros del libro del caso](./general_data) lista cada bloque con sus parámetros.

Los nombres de las pestañas y de los bloques se mantienen en inglés, como aparecen en el libro de Excel.

Esta página lista todos los interruptores por pestaña y luego las reglas para combinarlos.

---

## Interruptores por pestaña {#switches-by-tab}

Las tablas se generan a partir del catálogo del libro de Excel (`tools/workbook_builder/input_catalog.yaml` en el repositorio de MATLAB). Las descripciones son las notas del libro.

### Run control {#switches-run-control}

| Interruptor | Bloque | Valores | Predeterminado | Descripción |
|---|---|---|---|---|
| `flag_adaptive_timestepping` | Surface time step | 0 / 1 | obligatorio | Actualiza el paso de tiempo del enrutamiento superficial a partir de los límites de estabilidad durante la simulación. Se recomienda mantenerlo activado en la mayoría de las simulaciones dinámicas. |
| `flag_GPU` | Computing | 0 / 1 | obligatorio | Ejecuta los arreglos y cálculos admitidos en una GPU compatible con MATLAB. Se debe dejar desactivado cuando no hay una GPU compatible. |
| `flag_single` | Computing | 0 / 1 | obligatorio | Almacena los arreglos numéricos admitidos en precisión simple para reducir el uso de memoria. Se debe mantener desactivado cuando se requiere la máxima precisión numérica. |
| `flag_export_maps` | Outputs and display | 0 / 1 | obligatorio | Exporta las salidas espaciales programadas del modelo, como la profundidad de inundación y mapas relacionados. |
| `flag_export_groundwater_maps` | Outputs and display | 0 / 1 | `0` | Exporta los rásteres programados de profundidad del nivel freático cuando la modelación del agua subterránea está activada. |
| `flag_wse` | Outputs and display | 0 / 1 | obligatorio | flag_wse controla la salida de mapas de elevación de la superficie del agua (0 la desactiva y 1 la activa). El mapa usa la elevación del DEM más la profundidad de agua simulada donde la profundidad supera depth_wse. |
| `flag_waterbalance` | Outputs and display | 0 / 1 | obligatorio | Escribe diagnósticos del balance hídrico durante la simulación. Se recomienda activarlo para la validación y para las verificaciones rutinarias del modelo. |
| `flag_dashboard` | Outputs and display | 0 / 1 | obligatorio | Crea las salidas configuradas orientadas al panel durante la simulación. |
| `flag_elapsed_time` | Outputs and display | 0 / 1 | obligatorio | Imprime o registra el tiempo de cómputo transcurrido de la simulación. |
| `flag_warmup` | Warm start | 0 / 1 | obligatorio | Inicializa la simulación desde el estado de calentamiento configurado en lugar de los rásteres estándar de estado inicial. |
| `flag_timestep` | Advanced (keep the defaults unless you know why) | 0 / 1 | obligatorio | Selecciona el tratamiento completo de estabilidad del paso de tiempo para los solucionadores de enrutamiento compatibles. Se recomienda usar el valor predeterminado validado, salvo al probar una formulación numérica específica. |

### Soil and groundwater {#switches-soil-and-groundwater}

| Interruptor | Bloque | Valores | Predeterminado | Descripción |
|---|---|---|---|---|
| `flag_infiltration` | Infiltration and evapotranspiration | 0 / 1 | obligatorio | Activa la infiltración y el balance de agua del suelo en capas. Desactivarla también desactiva la evapotranspiración en el modelo actual. |
| `flag_ETP` | Infiltration and evapotranspiration | 0 / 1 | obligatorio | Activa la evapotranspiración. HydroPol2D usa las entradas meteorológicas o de mapas configuradas para calcular la evaporación y la transpiración. |
| `flag_abstraction` | Infiltration and evapotranspiration | 0 / 1 | obligatorio | Activa la intercepción del dosel y los procesos de abstracción inicial. |
| `flag_capillary_rise` | Infiltration and evapotranspiration | 0 / 1 | `1` | Activa el flujo ascendente limitado desde el agua subterránea somera hacia la zona de transmisión o de raíces cuando existen déficits de almacenamiento. |
| `flag_snow_modeling` | Infiltration and evapotranspiration | 0 / 1 | obligatorio | Activa la partición de la precipitación, el almacenamiento de nieve, el derretimiento, la sublimación y la compactación, con las columnas de nieve de la pestaña Land use classes. |
| `flag_spatial_albedo` | Infiltration and evapotranspiration | 0 / 1 | obligatorio | Usa el ráster de albedo suministrado en lugar del albedo escalar predeterminado. |
| `flag_neglect_infiltration_river` | Infiltration and evapotranspiration | 0 / 1 | obligatorio | Fija en cero la infiltración y la abstracción inicial en las celdas de río identificadas. |
| `flag_groundwater_modeling` | Groundwater | 0 / 1 | obligatorio | Activa el módulo acoplado de recarga del suelo en capas y de agua subterránea saturada. |
| `flag_baseflow` | Groundwater | 0 / 1 | obligatorio | Activa la contribución de flujo base configurada donde el flujo de trabajo hidrológico seleccionado lo admite. |
| `flag_prescribed_recharge` | Groundwater | 0 / 1 | `0` | Reemplaza la recarga calculada hacia el nivel freático por la serie de Prescribed_Recharge_Timeseries_File (pestaña Input maps). Valor predeterminado 0. |
| `flag_layered_subsurface` | Layered subsurface: column | 0 / 1 | `0` | Activa el subsuelo en capas, con tres capas de suelo sobre capas de roca meteorizada hasta el lecho de roca y un nivel freático por celda (reglas de Miguez-Macho et al., 2007). Los parámetros están en los bloques del subsuelo en capas de la pestaña Soil and groundwater, y los rásteres opcionales están debajo de los valores que sobrescriben. Requiere flag_groundwater_modeling = 1. |
| `flag_implicit_water_table_flux` | Layered subsurface: soil and numerics | 0 / 1 | `1` | Resuelve de forma implícita el flujo de Darcy entre el suelo y el nivel freático en el subsuelo en capas (un paso de Euler implícito linealizado por celda). Con 1 (predeterminado), el flujo sigue siendo preciso con pasos de tiempo largos cuando el nivel freático es somero. Con 0, se usa el flujo explícito, que en ese caso requiere pasos cortos. Solo se usa con flag_layered_subsurface = 1. |
| `flag_feddes` | Feddes root-water stress | 0 / 1 | `0` | Activa el estrés de Feddes en la absorción de agua por las raíces, que reduce la transpiración de cada capa de suelo según su carga de succión. Las cargas están en este bloque. Funciona con el esquema de suelo en capas y con el heredado. |
| `flag_deep_aquifer` | Deep aquifer | 0 / 1 | `0` | Activa el acuífero profundo. La fracción deep_recharge_fraction de la recarga del nivel freático va a un embalse lineal por subcuenca y vuelve a la superficie después de deep_aquifer_tau_days. Requiere DeepAquiferSubbasins_path y DeepAquiferChannelWeight_path. |

### Surface flow {#switches-surface-flow}

| Interruptor | Bloque | Valores | Predeterminado | Descripción |
|---|---|---|---|---|
| `flag_inertial` | Routing scheme | 0 / 1 | obligatorio | Selecciona el solucionador hidrodinámico inercial local. Es el solucionador de enrutamiento obligatorio para la extensión de submalla de canal de Neal (2012). |
| `flag_CA` | Routing scheme | 0 / 1 | obligatorio | Selecciona la opción de enrutamiento hidrodinámico por autómatas celulares. No se debe activar junto con el enrutamiento inercial local o de momento completo. |
| `flag_kinematic` | Routing scheme | 0 / 1 | obligatorio | Selecciona la alternativa de enrutamiento por onda cinemática. No se debe combinar con el enrutamiento inercial local, de momento completo o por autómatas celulares. |
| `flag_diffusive` | Routing scheme | 0 / 1 | obligatorio | Selecciona la alternativa de enrutamiento por onda difusiva. No se debe combinar con el enrutamiento inercial local, de momento completo o por autómatas celulares. |
| `flag_D8` | Routing scheme | 0 / 1 | obligatorio | Retirado: manténgalo en 0. El D8 ráster antiguo estaba incompleto, y 1 detiene la simulación. El enrutamiento inercial local D8 es `flag_d8_local_inertial`, definido en el script de bypass (vea [Limitaciones](../validation/limitations#matlab-optional-modules)). |
| `flag_boundary` | Outlets and boundaries | 0 / 1 | obligatorio | Activa el tratamiento configurado del contorno abierto o perimetral. La máscara y la pendiente de salida deben definirse con cuidado, porque este parámetro controla la salida de agua en el borde del dominio. |
| `flag_critical` | Outlets and boundaries | 0 / 1 | obligatorio | Usa el tratamiento de salida de flujo crítico donde el solucionador de enrutamiento seleccionado lo admite. Es distinto de la salida de flujo normal seleccionada con flag_outlet_type. |
| `flag_neal_channel` | River channel (sub-grid) | 0 / 1 | obligatorio | Activa la extensión de canal rectangular embebido y llanura de inundación de Neal (2012). Requiere flag_inertial = 1, topología ráster estructurada y rásteres válidos de ancho y profundidad del río. |
| `flag_river_rasters` | River channel (sub-grid) | 0 / 1 | obligatorio | Usa los rásteres RiverWidths y RiverDepths suministrados para definir la geometría del canal del modelo de submalla activo. |
| `flag_resample` | Terrain treatment | 0 / 1 | obligatorio | Remuestrea los rásteres auxiliares a la malla del DEM durante el preprocesamiento cuando su malla difiere de la del DEM. |
| `flag_fill_DEM` | Terrain treatment | 0 / 1 | obligatorio | Rellena las depresiones del terreno antes de derivar las direcciones de drenaje y la acumulación de flujo. |
| `flag_smoothening` | Terrain treatment | 0 / 1 | obligatorio | Aplica un suavizado restringido del perfil de los cauces durante el preprocesamiento del DEM. Esta opción requiere Optimization Toolbox. |
| `flag_smooth_cells` | Terrain treatment | 0 / 1 | obligatorio | Aplica el tratamiento configurado de suavizado del DEM por celda durante el preprocesamiento. |
| `flag_trunk` | Terrain treatment | 0 / 1 | obligatorio | Usa la opción de procesamiento de cauces principales durante la preparación del terreno y de la red de drenaje. |
| `flag_reduce_DEM` | Terrain treatment | 0 / 1 | obligatorio | Aplica la reducción configurada del DEM en los canales de los ríos durante el preprocesamiento. |
| `flag_DTM` | Terrain treatment | 0 / 1 | obligatorio | Usa la ruta de procesamiento DTM para preparar el terreno cuando los datos de entrada requieren ese flujo de trabajo. |
| `flag_voronoi` | Unstructured mesh | 0 / 1 | `0` | Ejecuta el modelo en una malla de Voronoi (no estructurada) preparada en lugar de la malla ráster. Las opciones de la malla se leen de la pestaña Mesh. |
| `flag_voronoi_subgrid` | Unstructured mesh | 0 / 1 | obligatorio | Activa las tablas de submalla por cara (nivel frente a área de flujo, perímetro mojado y capacidad de conducción) en la malla de Voronoi. Solo se usa con flag_voronoi = 1. La ruta de la tabla se define en la pestaña Mesh. |
| `flag_inflow` | Inflows and structures | 0 / 1 | obligatorio | Aplica uno o más hidrogramas de caudal prescritos en las coordenadas de entrada definidas en la pestaña Inflow hydrographs. |
| `flag_stage_hydrograph` | Inflows and structures | 0 / 1 | obligatorio | Aplica un hidrograma de nivel del agua prescrito en las ubicaciones configuradas del contorno de nivel. |
| `flag_reservoir` | Inflows and structures | 0 / 1 | obligatorio | Activa el módulo de embalses y estructuras de control con las entradas de embalses configuradas. |
| `flag_structured_lookup_subgrid` | Paused (keep at 0: setting 1 stops the run) | 0 / 1 | `0` | Activa la formulación de submalla estructurada con tablas de consulta en el modelo ráster regular. Usa propiedades de celdas y caras que dependen del nivel, y no puede combinarse con la submalla de Neal ni con la de Voronoi. |

### Rain and ET {#switches-rain-and-et}

| Interruptor | Bloque | Valores | Predeterminado | Descripción |
|---|---|---|---|---|
| `flag_rainfall` | Rainfall source | 0 / 1 | obligatorio | Activa el forzamiento de lluvia. Se usa con una sola fuente de lluvia seleccionada, que puede ser una serie temporal agregada, la interpolación de pluviómetros, una secuencia programada de rásteres o un producto satelital. |
| `flag_spatial_rainfall` | Rainfall source | 0 / 1 | obligatorio | Interpola la lluvia de los pluviómetros configurados a cada celda del modelo. Se requieren las coordenadas de los pluviómetros y una serie temporal de lluvia común. |
| `flag_input_rainfall_map` | Rainfall source | 0 / 1 | obligatorio | Lee una secuencia de rásteres de lluvia indexada en el tiempo desde la lista Rainfall maps. No se debe activar junto con otra fuente de lluvia espacial. |
| `flag_satellite_rainfall` | Rainfall source | 0 / 1 | obligatorio | Activa el flujo de trabajo de forzamiento con lluvia satelital. Prepara una programación horaria de lluvia espacial y activa la lluvia automáticamente. |
| `flag_real_time_satellite_rainfall` | Rainfall source | 0 / 1 | obligatorio | Activa el flujo de trabajo de lluvia satelital en tiempo real. Esta opción experimental crea una programación corta y móvil de lluvia espacial. |
| `flag_input_ETP_map` | Evapotranspiration source | 0 / 1 | obligatorio | Lee programaciones pareadas de rásteres de transpiración y evaporación desde la pestaña Rain and ET. Ambas programaciones deben tener las mismas entradas de tiempo. |
| `flag_rainfall_multiple_runs` | Advanced (keep the defaults unless you know why) | 0 / 1 | obligatorio | Activa el flujo de trabajo heredado de múltiples simulaciones de lluvia. Se debe dejar desactivado para un solo evento de lluvia estándar. |

### Design storm {#switches-design-storm}

| Interruptor | Bloque | Valores | Predeterminado | Descripción |
|---|---|---|---|---|
| `flag_alternated_blocks` | Hyetograph | 0 / 1 | obligatorio | Genera la tormenta de diseño configurada de bloques alternados en lugar de leer una serie temporal de lluvia. |
| `flag_huff` | Hyetograph | 0 / 1 | obligatorio | Genera la tormenta de diseño configurada de Huff en lugar de leer una serie temporal de lluvia. |

### Water quality {#switches-water-quality}

| Interruptor | Bloque | Valores | Predeterminado | Descripción |
|---|---|---|---|---|
| `flag_waterquality` | Water quality | 0 / 1 | obligatorio | Activa los cálculos de build-up, wash-off y transporte de contaminantes, y sus salidas. |
| `flag_WQ_Rasters` | Water quality | 0 / 1 | obligatorio | Usa los rásteres espaciales de coeficientes de calidad del agua B1, B2, W1 y W2 en lugar de los coeficientes de la tabla de cobertura del suelo. |
| `flag_initial_buildup` | Water quality | 0 / 1 | obligatorio | Inicializa el build-up de calidad del agua con los parámetros configurados del período seco antecedente y del build-up. |
| `flag_wq_model` | Advanced (keep the defaults unless you know why) | 0 / ... | obligatorio | Selecciona la formulación de calidad del agua. El valor 0 usa el modo de build-up y wash-off basado en masa. Otros valores solo se deben usar en configuraciones heredadas compatibles. |

### Risk and gauges {#switches-risk-and-gauges}

| Interruptor | Bloque | Valores | Predeterminado | Descripción |
|---|---|---|---|---|
| `flag_human_instability` | Human instability | 0 / 1 / 3 | obligatorio | Calcula indicadores de inestabilidad humana según la profundidad y la velocidad. El valor 0 lo desactiva, el valor 1 usa la clasificación básica y el valor 3 activa la clasificación extendida. |
| `flag_obs_gauges` | Observation points | 0 / 1 | obligatorio | Exporta los valores modelados en las coordenadas de las estaciones de observación de la tabla de estaciones. |

---

## Reglas para combinar interruptores {#rules-for-combining-switches}

- Solo una familia principal de enrutamiento debe estar activa a la vez, entre `flag_full_momentum`, `flag_inertial`, `flag_diffusive`, `flag_kinematic` y `flag_CA`.
- Se debe seleccionar como máximo una formulación de submalla, entre el canal de Neal, la tabla de consulta estructurada y la tabla de consulta de Voronoi.
- `flag_voronoi = 1` selecciona la topología de la malla. `flag_voronoi_subgrid = 1` activa además la hidráulica con tablas de consulta de Voronoi.
- `flag_D8` está retirado; manténgalo en 0. El enrutamiento inercial local D8 (`flag_d8_local_inertial`), el drenaje urbano, los estanques de detención y la infraestructura verde se definen en el script de bypass, no en el libro de cálculo (vea [Limitaciones](../validation/limitations#matlab-optional-modules)).
- `flag_numerical_scheme` (`1` Bates, `2` upwind, `3` centrado) se aplica solo a la familia inercial local.
- La nieve necesita el forzamiento meteorológico interno, es decir, `flag_ETP = 1` y `flag_input_ETP_map = 0`. Los parámetros de nieve son columnas de la tabla de clases de uso del suelo.
- `flag_implicit_water_table_flux` y los demás parámetros del subsuelo en capas solo se leen con `flag_layered_subsurface = 1`.
- El modo `2` de inestabilidad humana no está implementado. Se debe usar `1` o `3`.

### Submalla de canal de Neal (2012) {#neal-2012-subgrid-model-configuration}

El modo de submalla de canal admitido sigue a [Neal et al. (2012)](https://doi.org/10.1029/2012WR012514). Se usa la combinación siguiente.

| Interruptor | Valor requerido |
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
| `flag_river_rasters` | `1` cuando la geometría del canal se suministra como rásteres |

Las celdas de canal activas requieren `RiverWidths_path` y `RiverDepths_path`. El ancho y la profundidad del canal deben ser positivos, y el ancho del canal debe ser menor que la resolución de la celda del modelo. El coeficiente de Manning del canal es el parámetro `Manning` de la pestaña Surface flow. La rugosidad del uso del suelo da el coeficiente de Manning de la llanura de inundación.

El solucionador calcula por separado el caudal del canal y el de la llanura de inundación en cada cara ortogonal, y actualiza el almacenamiento de la celda en términos de volumen. La formulación y el rango de validación se describen en [Modelo hidrodinámico](../theory/hydrodynamic-model#115-neal-2012-subgrid-model) y en [Validación del modelo submalla de Neal (2012)](../validation/neal-subgrid).

---

## Formato anterior {#older-layout}

En los casos que usan `General_Data.xlsx`, los interruptores son filas de su hoja `Flags`, con el valor en la columna E. En los libros de Excel distribuidos, `flag_deep_aquifer`, `flag_layered_subsurface`, `flag_feddes` y `flag_implicit_water_table_flux` son las filas 37 a 40. El modelo lee la hoja `Flags` cuando el caso la tiene y, si no, los interruptores de las pestañas de parámetros.

- Los interruptores retirados `flag_data_source`, `flag_dam_break` y `flag_river_heigth_compensation` ya no son obligatorios (valor predeterminado 0).
- `flag_subgrid` y `flag_overbanks` se derivan de los interruptores del canal. La capa de migración acepta, con una advertencia, las entradas antiguas que todavía los definen.
