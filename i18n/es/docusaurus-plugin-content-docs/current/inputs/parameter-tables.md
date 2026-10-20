---
title: Tablas de parámetros
---

# Tablas de parámetros

HydroPol2D utiliza tablas de parámetros para asignar propiedades físicas a entradas ráster categóricas.
Los mapas categóricos como LULC y Soil no se utilizan directamente en las ecuaciones rectoras. En cambio, cada clase actúa como un índice en una tabla de parámetros, donde se definen los parámetros físicos correspondientes.
Esta estructura separa la información espacial de la definición de parámetros y hace que el modelo sea más fácil de calibrar, adaptar e interpretar.
---

## Estructura General

Cada tabla de parámetros contiene:
- un **identificador de clase** (`Index`)
- un conjunto de **parámetros asociados con esa clase**

En tiempo de ejecución, HydroPol2D:
1. lee el valor ráster en cada celda de la cuadrícula,
2. utiliza ese valor como índice,
3. asigna los parámetros correspondientes de la tabla.

Para las clases asignadas, los valores ráster y los índices de tabla deben coincidir. Cuando un código válido de LULC, suelo o nieve no aparece en la tabla, HydroPol2D aplica el promedio ponderado por área de las propiedades de las clases asignadas y registra la decisión en `Input_Class_Code_Audit.csv`. Los índices duplicados, no numéricos o una tabla sin clases asignadas siguen siendo errores de entrada.
---

## Tabla de parámetros LULC

La tabla LULC define las propiedades relacionadas con la superficie que controlan la resistencia al flujo, la intercepción, la impermeabilidad, el comportamiento relacionado con los contaminantes y la profundidad de la zona de las raíces cuando el almacenamiento de suelo en capas está activo.
### Estructura de ejemplo

| Cobertura terrestre | Índice | $n$<br />$(\mathrm{s\,m^{-1/3}})$ | $h_0$<br />$(\mathrm{mm})$ | $d_0$<br />$(\mathrm{mm})$ | $C_1$ | $C_2$ | $C_3$ | $C_4$ | $\mathrm{index\_impervious}$ | $\mathrm{root\_depth\_m}$ |
|:----------:|:-----:|:---------------------------------:|:--------------------------:|:--------------------------:|:-----:|:-----:|:-----:|:-----:|:----------------------------:|:--------------------------:|
| Cobertura de árboles | 10 | 0,10 | 0 | 0 | 10 | 0,20 | 800 | 1.20 | 50 | 1,50 |
| Matorral | 20 | 0,08 | 0 | 0 | 12 | 0,20 | 900 | 1.20 | Yaya | 1.00 |
| Pradera | 30 | 0,06 | 0 | 0 | 15 | 0,22 | 1000 | 1.20 | Yaya | 0,60 |
| Tierras de cultivo | 40 | 0,05 | 0 | 0 | 30 | 0,25 | 1400 | 1.30 | Yaya | 1.00 |
| Construido | 50 | 0,03 | 0 | 0 | 80 | 0,30 | 2000 | 1.30 | Yaya | 0.00 |
| Vegetación desnuda/escasa | 60 | 0.035 | 0 | 0 | 45 | 0,25 | 1600 | 1.25 | Yaya | 0,10 |
| Nieve y hielo | 70 | 0,02 | 0 | 0 | 1 | 0,10 | 200 | 1.10 | Yaya | 0.00 |
| Cuerpos de agua permanentes | 80 | 0.035 | 0 | 0 | 0 | 0 | 0 | 0 | Yaya | 0.00 |
| Humedal herbáceo | 90 | 0,12 | 0 | 0 | 8 | 0,18 | 700 | 1.20 | Yaya | 0,40 |
| Manglares | 95 | 0,15 | 0 | 0 | 8 | 0,18 | 700 | 1.20 | Yaya | 1.00 |
| musgo y liquen | 100 | 0,08 | 0 | 0 | 5 | 0,15 | 500 | 1.15 | Yaya | 0,15 |

*Tabla 1. Tabla de parámetros HydroPol2D LULC. Los valores `Index` deben coincidir con los valores categóricos en el ráster LULC.*
### Definiciones de variables

- $n$: coeficiente de rugosidad de Manning
- $h_0$: parámetro de interceptación
- $d_0$: parámetro de almacenamiento en superficie inicial
- $C_1$–$C_4$: coeficientes asociados con la formulación de acumulación y lavado de contaminantes
- $\mathrm{index\_impervious}$: identificador utilizado para asociar una clase con un comportamiento impermeable
- $\mathrm{root\_depth\_m}$: profundidad de la zona de raíces controlada por la vegetación utilizada por el modelo de suelo/vadose en capas

Los valores mostrados arriba corresponden a la tabla de parámetros HydroPol2D actual y deben revisarse según sea necesario para el esquema de clasificación adoptado y el área de estudio.
En la implementación actual, `root_depth_m` es la forma admitida de proporcionar información de profundidad de raíz al modelo. No existe una ruta ráster de profundidad de raíz separada; La profundidad de la raíz se asigna por clase LULC y luego se asigna a la cuadrícula a través del ráster categórico LULC.
---

## Tabla de parámetros del suelo

La tabla de suelos define las propiedades hidráulicas básicas utilizadas para estimar la infiltración, el almacenamiento vadoso en capas, la recarga y el comportamiento del agua subterránea.
### Estructura de ejemplo

| Tipo de suelo | Índice | $K_{\mathrm{sat}}$<br />$(\mathrm{mm\,h^{-1}})$ | $n$ | $\alpha$<br />$(\mathrm{m^{-1}})$ | $\theta_{\mathrm{sat}}$ | $\theta_{\mathrm{r}}$ | $\theta_{\mathrm{i}}$ | $S_{\mathrm{y}}$ | $K_{\mathrm{g,sat}}$<br />$(\mathrm{mm\,h^{-1}})$ | $\mathrm{PHTOKEN0XYZ}$<br />$(\mathrm{m})$ | $K_s$ cerca | $K_s$ raíz | $K_s$ transmisión |
|:---------:|:-----:|:-----------------------------------------------:|:---:|:----------------------------------:|:----------------------:|:--------------------:|:--------------------:|:---------------:|:---------------------------------------------------:|:--------------------------------:|:------------:|:----------:|:--------------------:|
| Arcilla | 1 | 0.3 | 1.09 | 0,8 | 0.385 | 0.068 | 0.0997 | 0,03 | 6 | 1 | 1 | 1 | 1 |
| Arcilla limosa | 2 | 0,5 | 1.23 | 1.0 | 0.423 | 0,089 | 0,1224 | 0,04 | 10 | 1 | 1 | 1 | 1 |
| Arcilla arenosa | 3 | 0,6 | 1.31 | 1.5 | 0.321 | 0,075 | 0.0996 | 0,06 | 12 | 1 | 1 | 1 | 1 |
| Franco arcilloso | 4 | 1.0 | 1.31 | 1.9 | 0.309 | 0.095 | 0.1164 | 0,08 | 20 | 1 | 1 | 1 | 1 |
| Franco arcilloso limoso | 5 | 1.0 | 1.23 | 1.5 | 0,432 | 0,089 | 0.1233 | 0,09 | 20 | 1 | 1 | 1 | 1 |
| Franco arcilloso arenoso | 6 | 1.5 | 1,48 | 3.0 | 0.330 | 0.065 | 0.0915 | 0,11 | 30 | 1 | 1 | 1 | 1 |
| Franco limoso | 7 | 7.6 | 1.41 | 4.5 | 0,434 | 0.067 | 0,1220 | 0,14 | 152 | 1 | 1 | 1 | 1 |
| Marga | 8 | 3.4 | 1,56 | 3.6 | 0,486 | 0,078 | 0.1104 | 0,18 | 68 | 1 | 1 | 1 | 1 |
| Franco arenoso | 9 | 10.9 | 1,89 | 7.5 | 0.412 | 0.065 | 0.1287 | 0,22 | 218 | 1 | 1 | 1 | 1 |
| Limo | 10 | 3.4 | 1.37 | 4.0 | 0,486 | 0.067 | 0,1234 | 0,12 | 68 | 1 | 1 | 1 | 1 |
| Arena franca | 11 | 29,9 | 2.28 | 14.5 | 0.401 | 0.057 | 0.1172 | 0,25 | 598 | 1 | 1 | 1 | 1 |
| Arena | 12 | 117,8 | 2,68 | 14.5 | 0.417 | 0.045 | 0,1225 | 0,30 | 2356 | 1 | 1 | 1 | 1 |
| Agua | 0 | 0.3 | 1.09 | 0,8 | 0.385 | 0.068 | 0.0997 | 0,03 | 6 | 1 | 1 | 1 | 1 |

*Tabla 2. Tabla de parámetros del suelo HydroPol2D. Los valores `Index` deben coincidir con los valores categóricos en el ráster de suelo.*
### Definiciones de variables

- $K_{\mathrm{sat}}$: conductividad hidráulica saturada
- $n$: parámetro de forma de Van Genuchten
- $\alpha$: parámetro inverso de entrada de aire
- $\theta_{\mathrm{sat}}$: contenido de agua saturada
- $\theta_{\mathrm{r}}$: contenido de agua residual
- $\theta_{\mathrm{i}}$: humedad inicial del suelo
- $S_{\mathrm{y}}$: rendimiento específico
- $K_{\mathrm{g,sat}}$: conductividad saturada asociada con la parametrización del subsuelo o agua subterránea
- $\mathrm{PHTOKEN0XYZ}$: profundidad al lecho de roca o profundidad de almacenamiento efectiva
- `Ks_multiplier_near_surface`: multiplicador aplicado a la base $K_{\mathrm{sat}}$ en la capa cercana a la superficie
- `Ks_multiplier_root_zone`: multiplicador aplicado a la base $K_{\mathrm{sat}}$ en la capa de la zona raíz
- `Ks_multiplier_transmission`: multiplicador aplicado a la base $K_{\mathrm{sat}}$ en la capa de transmisión

La clase categórica de suelo define las propiedades hidráulicas básicas de la columna. La implementación en capas asigna esas propiedades a las capas cercanas a la superficie, zona de raíz y zona de transmisión, luego aplica multiplicadores de conductividad opcionales donde se proporcionan.
LULC controla la profundidad de la zona de la raíz. La profundidad del lecho rocoso y la posición actual del nivel freático limitan los espesores de las capas finales, por lo que las geometrías de las capas físicamente imposibles colapsan o truncan en lugar de producir un almacenamiento negativo.
Los valores mostrados arriba corresponden a la tabla actual de parámetros del suelo HydroPol2D y deben revisarse según sea necesario para el escenario de simulación y clasificación del suelo adoptado.
---

## DTB Asignación a través de la Tabla de Suelos

Si un ráster DTB no está disponible, los valores DTB se pueden asignar directamente en la tabla de suelos.
En este caso:
- cada clase de suelo está asociada con un valor representativo de DTB,
- el campo DTB se construye implícitamente a partir del mapa de suelo,
- La profundidad de almacenamiento sigue siendo consistente con la clasificación de suelo adoptada.

Esto es particularmente útil en aplicaciones con escasez de datos.


---

## Requisitos de coherencia

Deben cumplirse las siguientes condiciones:
- todos los valores de clase ráster deben existir en la tabla correspondiente,
- los identificadores de clase no deben duplicarse,
- los campos de parámetros no deben dejarse vacíos,
- Las unidades deben ser consistentes con la formulación del modelo.

Cualquier inconsistencia entre las clases de ráster y las tablas de parámetros dará lugar a una asignación incorrecta de propiedades físicas.
---

## Uso práctico

Las tablas de parámetros son el principal mecanismo utilizado para:
- calibrar el modelo,
- adaptar el modelo a diferentes entornos,
- realizar análisis de sensibilidad,
- probar supuestos físicos alternativos sin modificar el código.

En HydroPol2D, la mayoría de las modificaciones prácticas al comportamiento del modelo se realizan editando estas tablas.
---

## Condiciones de límites internos (estructuras de control)

HydroPol2D permite la definición de condiciones de contorno interno (IBC) que modifican localmente la respuesta hidráulica del dominio.
Estas estructuras se implementan mediante un enfoque simple de curva de clasificación que convierte la profundidad del agua en descarga. En las celdas de control seleccionadas, el flujo ya no está determinado únicamente por la actualización inercial local estándar. En cambio, la descarga se impone mediante una relación profundidad-descarga definida por parámetros especificados por el usuario.
Esto permite que el modelo represente controles hidráulicos localizados como:
- alcantarillas
- puertas
- presas
- salidas
- secciones de control diseñadas

---

### Concepto

Cada condición de límite interno está vinculada a una celda de control definida por sus coordenadas espaciales. La descarga a través de ese control se calcula a partir de la profundidad del agua local utilizando una formulación de curva de clasificación.
En la implementación actual de HydroPol2D, la hoja de cálculo de la estructura de control define dos ramas de la curva de calificación, cada una con su propio coeficiente y parámetros de umbral. Esto permite representar el comportamiento hidráulico por partes bajo diferentes profundidades de flujo o condiciones de funcionamiento.
La descarga resultante se impone en la ubicación de control correspondiente y, por lo tanto, modifica la dinámica del flujo local dentro del solucionador numérico.
---

### Función en el modelo

Las condiciones de contorno internas afectan la simulación por:
- imponer una respuesta de descarga basada en la profundidad local
- Modificación de los flujos de entrada o salida de las celdas dentro del solucionador inercial local.
- introducir un intercambio de flujo interno controlado dentro del dominio computacional

Estas estructuras pueden influir fuertemente en:
- almacenamiento ascendente
- propagación aguas abajo
- atenuación de inundaciones
- efectos de remanso local

---

### Papel en el modelo numérico

En celdas donde se define una condición de contorno interna:
- La profundidad del agua se evalúa en el punto de control.
- La descarga se calcula a partir de los parámetros de la curva de calificación.
- el flujo resultante se impone en la actualización hidráulica

Esto significa que el solucionador inercial local es modificado localmente por el comportamiento de la estructura de control. La descarga se prescribe a partir de la relación de calificación en lugar de obtenerse exclusivamente del cálculo de flujo estándar basado en caras.
---

### Estructura de la tabla de entrada

Las condiciones de contorno internas se definen mediante una hoja de cálculo dedicada.
#### Estructura de la mesa

| Parámetro | Unidades | Descripción |
|:---------:|:-----:|-------------|
| $\mathrm{Index}$ | — | Identificador de la estructura de control. |
| $x$ | $\mathrm{m}$ | Coordenada este de la celda de control. |
| $y$ | $\mathrm{m}$ | Coordenada norte de la celda de control. |
| $k_1$ | — | Coeficiente de la primera rama de la curva de calificación. |
| $h_{0,1}$ | $\mathrm{m}$ | Profundidad de referencia o umbral asociado a la primera rama. |
| $k_2$ | — | Exponente o parámetro de forma asociado con la primera rama. |
| $x_{\mathrm{d},1}$ | $\mathrm{m}$ | Coordenada este del primer punto de control de descarga. |
| $y_{\mathrm{d},1}$ | $\mathrm{m}$ | Coordenada norte del primer punto de control de descarga |
| $k_3$ | — | Coeficiente de la segunda rama de la curva de calificación |
| $h_{0,2}$ | $\mathrm{m}$ | Profundidad de referencia o umbral asociado a la segunda rama. |
| $k_4$ | — | Exponente o parámetro de forma asociado a la segunda rama. |
| $x_{\mathrm{d},2}$ | $\mathrm{m}$ | Coordenada este del segundo punto de control de descarga. |
| $y_{\mathrm{d},2}$ | $\mathrm{m}$ | Coordenada norte del segundo punto de control de descarga |

*Tabla 3. Tabla de parámetros de condiciones de contorno interno HydroPol2D. Estos parámetros definen el comportamiento de la curva de clasificación utilizado para convertir la profundidad en descarga.*
---

### Valores de ejemplo

| $\mathrm{Index}$ | $x$ $(\mathrm{m})$ | $y$ $(\mathrm{m})$ | $k_1$ | $h_{0,1}$ $(\mathrm{m})$ | $k_2$ | $x_{\mathrm{d},1}$ $(\mathrm{m})$ | $y_{\mathrm{d},1}$ $(\mathrm{m})$ | $k_3$ | $h_{0,2}$ $(\mathrm{m})$ | $k_4$ | $x_{\mathrm{d},2}$ $(\mathrm{m})$ | $y_{\mathrm{d},2}$ $(\mathrm{m})$ |
|:----------------:|-------------------:|-------------------:|------:|-------------------------:|------:|-----------------------------------:|-----------------------------------:|------:|-------------------------:|------:|-----------------------------------:|-----------------------------------:|
| 1 | -5166015.11 | -2706361.32 | 1.5 | 0.0 | 0,50 | -5166037.22 | -2706321.554 | 3.0 | 2.5 | 1.5 | -5166037.22 | -2706321.554 |
| 2 | -5166922.84 | -2704154.64 | 16.0 | 0.0 | 1.5 | -5166922.84 | -2704174.64 | 0.538951413 | 0.1 | 0,5 | -5166922.84 | -2704174.64 |

*Tabla 4. Ejemplo de parámetros de condición de contorno internos utilizados actualmente en HydroPol2D.*
---

### Interpretación

La formulación de la estructura de control se basa en una relación profundidad-caudal de la forma general:
$$
Q = f(h)
$$
dónde:
- $Q$ se descarga a través de la estructura en $\mathrm{m^3\,s^{-1}}$
- $h$ es la profundidad del agua local en $\mathrm{m}$
- los coeficientes $k_1$, $k_2$, $k_3$ y $k_4$ definen la respuesta de la curva de calificación
- los términos $h_{0,1}$ y $h_{0,2}$ definen las profundidades de referencia asociadas con cada rama

Las coordenadas $\left(x_{\mathrm{d},1}, y_{\mathrm{d},1}\right)$ y $\left(x_{\mathrm{d},2}, y_{\mathrm{d},2}\right)$ definen las ubicaciones en las que se aplica o evalúa el control de descarga.
Esta estructura permite representar una relación de descarga simple por partes utilizando dos ramas parametrizadas.
---

### Significado práctico de los parámetros

- $k_1$ y $k_3$ controlan la magnitud de la respuesta de descarga
- $k_2$ y $k_4$ controlan la curvatura o no linealidad de la respuesta
- $h_{0,1}$ y $h_{0,2}$ definen umbrales de activación o profundidades de referencia
- $x_{\mathrm{d},1}, y_{\mathrm{d},1}, x_{\mathrm{d},2}, y_{\mathrm{d},2}$ definen dónde se vincula espacialmente la descarga controlada

Juntos, estos parámetros definen cómo la estructura interna convierte la profundidad del agua en flujo.
---

### Consideraciones prácticas

- Las coordenadas de control deben ser consistentes con la proyección DEM.
- las celdas seleccionadas deben coincidir con celdas hidráulicas válidas en el dominio del modelo
- Los coeficientes de la curva de calificación deben ser físicamente realistas.
- Las curvas de calificación excesivamente pronunciadas pueden crear inestabilidad numérica.
- Las estructuras de control deben probarse cuidadosamente porque alteran directamente los flujos de masa locales.

---

### Resumen

Las condiciones de contorno interno en HydroPol2D se representan a través de un marco de curva de calificación simple que convierte la profundidad del agua local en descarga.
Están acostumbrados a:
- imponer flujos de entrada o salida controlados
- representan estructuras de control hidráulico
- Modificar la dinámica inercial local en células específicas.

Su parametrización correcta es esencial para una simulación estable y físicamente significativa de sistemas hidráulicos diseñados.
---

## Tabla de parámetros de nieve

La tabla de parámetros LULC contiene las siguientes columnas de nieve en cada fila de `LULC_Index`. No existe un libro separado para nieve; todas las propiedades dependientes de la cobertura del suelo permanecen en el mismo registro de clase.

| Columna | Unidades | Descripción |
|---|---|---|
| `LULC_Index` | — | Código LULC de la fila. |
| `Snow_Albedo` | — | Albedo de onda corta de la superficie de nieve. |
| `Snow_Emissivity` | — | Emisividad de onda larga usada en el balance de radiación. |
| `Sublimation_Coefficient_d_1` | día⁻¹ (m s⁻¹)⁻¹ | Coeficiente del término de sublimación. |
| `Degree_Day_Factor_mm_C_day` | mm °C⁻¹ día⁻¹ | Factor de fusión por grados-día. |
| `T_Snow_All_C` | °C | Temperatura a la cual toda la precipitación es nieve. |
| `T_Rain_All_C` | °C | Temperatura a la cual toda la precipitación es lluvia; no puede ser menor que `T_Snow_All_C`. |
| `Rho_Snow_Init_kg_m3` | kg m⁻³ | Densidad de nieve nueva usada en la inicialización. |
| `Rho_Snow_Max_kg_m3` | kg m⁻³ | Límite superior de densidad tras compactación. |
| `Compaction_Temperature_kg_m3_C_day` | kg m⁻³ °C⁻¹ día⁻¹ | Aumento de densidad dependiente de la temperatura. |
| `Compaction_SWE_kg_m3_mm_day` | kg m⁻³ mm⁻¹ día⁻¹ | Aumento de densidad dependiente de SWE. |
| `Compaction_Depth_kg_m3_mm_day` | kg m⁻³ mm⁻¹ día⁻¹ | Aumento de densidad dependiente de la profundidad. |

Los factores de grados-día, sublimación y compactación son tasas y el modelo los multiplica por el paso de tiempo actual. La nieve requiere el forzamiento meteorológico interno, para obtener temperatura media, temperatura mínima y viento.

---

## Filosofía del diseño

HydroPol2D separa:
- **entradas espaciales**, que definen dónde ocurre cada clase,
- **tablas de parámetros**, que definen cómo se comporta cada clase.

Esto hace que el modelo sea más fácil de mantener, calibrar y aplicar en diferentes dominios.
---

## Resumen

Las tablas de parámetros definen cómo HydroPol2D traduce datos espaciales categóricos en comportamiento físico.
Son un componente central de la estructura del modelo y deben prepararse cuidadosamente para garantizar simulaciones consistentes, estables y físicamente significativas.
