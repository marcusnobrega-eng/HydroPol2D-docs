---
title: Resumen
---

# Configuracion del modelo

En el modo Excel de MATLAB, un caso de HydroPol2D es un solo libro de Excel, `HydroPol2D_Inputs.xlsx`. Sus pestañas de parámetros seleccionan el conjunto de procesos, la familia de enrutamiento, los controles del agua subterránea, los archivos de entrada y los diagnósticos opcionales. Sus otras pestañas contienen las tablas de clases y las series temporales. Los casos antiguos con `General_Data.xlsx` y libros de Excel separados siguen funcionando (ver [Ejecutar desde Excel](../getting-started/excel-workflow#older-layout)). HydroPol2D-Python lee los mismos parámetros desde el YAML de su caso.

Las paginas de configuracion y teoria cumplen funciones distintas:

- la teoria explica lo que hace cada modulo;
- la configuracion explica que controles publicos exponen ese comportamiento.

## Logica actual de configuracion

La configuracion publica debe coincidir con el modelo implementado:

- el almacenamiento vadoso en capas y el acoplamiento con groundwater son la ruta por defecto cuando el groundwater esta activo;
- la familia de enrutamiento incluye local inertial, full momentum, diffusive D4, kinematic D4 y cellular automata;
- solo una familia principal de enrutamiento debe estar activa por simulacion.

## Capacidades y madurez

| Capacidad | Principales controles publicos | Estado actual |
|---|---|---|
| Nucleo hidrologico | `flag_infiltration`, controles de ET, lluvia y nieve, tablas de suelo y LULC | Predeterminado + validado |
| Recarga subterranea en capas y programador asincrono | `flag_groundwater_modeling`, `flag_groundwater_async`, `groundwater_target_dt_min`, `groundwater_min_dt_min`, `groundwater_max_head_change_m`, `groundwater_courant` | Predeterminado + validado |
| Ascenso capilar | `flag_capillary_rise` | Opcional + validado en benchmarks controlados |
| Subsuelo en capas | `flag_layered_subsurface`, `flag_implicit_water_table_flux` | Opcional + pruebas controladas y paridad Python-MATLAB |
| Estrés de Feddes en la absorción de agua por las raíces | `flag_feddes` | Opcional + pruebas de consistencia |
| Acuífero profundo | `flag_deep_aquifer` | Opcional + pruebas con fixtures del estado inicial |
| Enrutamiento local inertial | `flag_inertial`, `flag_numerical_scheme` | Predeterminado + validado |
| Enrutamiento full momentum | `flag_full_momentum` | Opcional + validado en benchmarks controlados |
| Enrutamiento diffusive | `flag_diffusive` | Opcional + validado en benchmarks controlados |
| Enrutamiento kinematic | `flag_kinematic` | Opcional + validado en benchmarks controlados |
| Cellular automata | `flag_CA` | Opcional + validado para conservacion y bookkeeping |
| Inestabilidad humana | `flag_human_instability` | Opcional + validada para los modos `1` y `3` |

## Principales dominios de configuracion

### 1. Control de simulacion y forzantes

Las pestañas Run control, Rain and ET, Design storm y Surface flow definen el tiempo de simulación, los forzamientos de lluvia y meteorológicos, las condiciones de contorno de caudal de entrada y de nivel, la frecuencia de salida y las opciones de ejecución, como el paso de tiempo adaptativo o la ejecución en GPU. Todos los parámetros se listan en [Parámetros del libro del caso](./general_data).

### 2. Seleccion de la familia de enrutamiento

La interfaz publica de enrutamiento incluye:

- `flag_inertial`
- `flag_full_momentum`
- `flag_diffusive`
- `flag_kinematic`
- `flag_CA`

Solo una de estas flags principales debe estar activa en cada simulacion. D8 existe como ruta secundaria y no debe documentarse como una familia teorica paralela.

### 3. Controles de groundwater

Cuando el groundwater esta activo, HydroPol2D expone comportamientos que deben documentarse de forma explicita:

- actualizaciones asincronas del groundwater saturado;
- resoluciones disparadas por cambios acumulados de carga;
- limite explicito de estabilidad para el time step del groundwater;
- ascenso capilar opcional;
- flujo lateral de Boussinesq cuando el baseflow esta activo.

### 4. Diagnosticos de riesgo y calidad del agua

Modulos opcionales, como calidad del agua e inestabilidad humana, tienen flags y parametros propios. Para inestabilidad humana, la documentacion publica debe reflejar que:

- el modo `1` esta implementado;
- el modo `3` esta implementado;
- el modo `2` no esta implementado.

## Lectura recomendada de una configuracion

En simulaciones publicas de HydroPol2D, debe quedar claro:

1. que familia de enrutamiento esta activa;
2. si el groundwater esta acoplado solo localmente o tambien lateralmente mediante Boussinesq;
3. si el ascenso capilar esta activo;
4. si los diagnosticos de inestabilidad humana o calidad del agua estan activos.

Si esas cuatro preguntas quedan claras, la configuracion esta alineada con la historia actual del modelo.
