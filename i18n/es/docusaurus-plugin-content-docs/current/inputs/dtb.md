---
title: DTB
---

# Profundidad hasta el lecho de roca (DTB)

La profundidad hasta el lecho de roca (DTB) define la extensión vertical de la columna de suelo disponible para el almacenamiento de agua en HydroPol2D.
Representa la distancia entre la superficie terrestre y una capa limitante que restringe el movimiento vertical del agua. Esta capa puede corresponder a un lecho de roca real o a un límite efectivo, como la parte superior de un acuífero poco profundo.

---

## Papel en HydroPol2D

Lo que controla DTB depende del esquema de subsuelo. En el esquema predeterminado, DTB es la profundidad del suelo, y el suelo y el acuífero comparten la misma columna. En el [subsuelo en capas](#dtb-in-the-layered-subsurface), DTB es solo el fondo del acuífero, y una base del suelo separada marca dónde termina el suelo.

En el esquema predeterminado, DTB se utiliza para definir:
- Capacidad máxima de almacenamiento subterráneo
- Límite vertical de infiltración y percolación.
- Espesor efectivo de la zona vadosa.
- Inicio de la saturación dentro de la columna del suelo.

Dentro del modelo, DTB actúa como una **restricción geométrica** de almacenamiento en lugar de un perfil vertical completamente resuelto.
DTB no debe confundirse con el ráster inicial opcional del nivel freático. En el modelo actual, `DTB_path` define el espesor de la columna de suelo, mientras que `GW_table_path` define la altura/elevación saturada inicial cuando la inicialización del agua subterránea se proporciona explícitamente.

---

## Representación

DTB se proporciona como un **mapa ráster continuo**, donde cada celda contiene un valor de profundidad (en metros).
Esto permite la variabilidad espacial en la capacidad de almacenamiento en todo el dominio.
- Somero DTB → rápida saturación y generación de escorrentía
- Profundo DTB → mayor almacenamiento y respuesta hidrológica retrasada

---

## Definición alternativa: profundidad al acuífero

En muchas aplicaciones, el objetivo no es resolver explícitamente la dinámica del agua subterránea sino limitar la profundidad de la zona vadosa.
En este caso, DTB puede interpretarse como la **profundidad de la superficie del acuífero**, en lugar de la profundidad del lecho rocoso impermeable.
Bajo este supuesto:
- La zona vadosa se limita a la profundidad entre la superficie y el acuífero.
- El almacenamiento está limitado por el volumen de suelo no saturado disponible.
- No se requiere una representación explícita del acuífero saturado.

Este enfoque es apropiado cuando:
- Los procesos de aguas subterráneas no están modelados explícitamente.
- La atención se centra en la respuesta hidrológica superficial y cercana a la superficie.
- Se necesita un límite superior realista para el almacenamiento del suelo

---

## Asignación predeterminada de clases de suelo

Si no hay un mapa DTB disponible, una profundidad del suelo por clase de suelo puede reemplazarlo.

- **HydroPol2D-Python** puede tomar la profundidad del suelo de su tabla de suelos, de un ráster de profundidad del suelo o del escalar `vertical.soil_depth_m`.
- **HydroPol2D (MATLAB)**, con el subsuelo en capas, toma la columna `DTB (m)` de la pestaña Soil classes como último recurso para el fondo de la columna (desde 2026-10-20). El esquema de agua subterránea predeterminado requiere `DTB_path` y no lee esa columna. Sin agua subterránea, un `DTB_path` vacío da una profundidad del suelo de 1 m.

---

## Unidades y Requisitos

La entrada DTB debe:
- Se expresará en **metros**
- Utilice un **CRS proyectado** coherente con todos los demás rásteres
- Alinearse espacialmente con el DEM y otras entradas

Los valores deben permanecer dentro de rangos físicamente realistas para el área de estudio.

---

## Fuentes de datos

Los datos DTB no están tan ampliamente estandarizados como DEM o LULC, pero pueden derivarse de:
### SoilGrids (profundidad hasta el lecho de roca)
- Región: Global
- Proporciona estimaciones de la profundidad del lecho de roca.
- Descargar: https://soilgrids.org/

---

### Estudios geológicos regionales
- Los conjuntos de datos nacionales o regionales pueden proporcionar estimaciones de mayor calidad
- A menudo derivan de cartografía geológica o modelos del subsuelo.

---

### Valores derivados o supuestos
- DTB se puede aproximar según el tipo de suelo o el contexto geológico
- Se pueden utilizar valores constantes cuando se desconoce la variabilidad espacial.

---

## DTB en el subsuelo en capas {#dtb-in-the-layered-subsurface}

Con el [subsuelo en capas](../theory/layered-subsurface) (Python `vertical.subsurface.scheme: layered`, MATLAB `flag_layered_subsurface = 1`), dos profundidades definen la columna.

| Profundidad | Qué marca | Entrada |
|---|---|---|
| Base del suelo | Donde terminan las propiedades del suelo y comienza el regolito | Ráster `SoilBaseDepth_path`; si no existe, `subsurface_soil_base_depth_m` (2 m por defecto) |
| Profundidad hasta el lecho de roca | Donde termina el acuífero | Ráster `DTB_path`; si no existe, `subsurface_depth_to_bedrock_m`; si tampoco existe, la profundidad del suelo de cada clase de suelo (`DTB (m)` en MATLAB), con una advertencia |

La base del acuífero es el terreno menos $\min(\mathrm{DTB},\ D_{\max})$, con $D_{\max}$ = `subsurface_max_depth_m` (50 m por defecto). En las celdas con DTB más profunda que el límite, la columna se detiene en el límite.

Entre la base del suelo y la base de la columna, el modelo coloca capas de regolito según una regla fija de 0.25, 0.5, 1, 2, 4, 4, … m a partir de la base del suelo (el primer espesor, la razón de crecimiento y el espesor máximo son configurables). La regla se corta en la base de la columna, por lo que una DTB más profunda añade más capas de 4 m.

En Python, las claves equivalentes son `vertical.subsurface.soil_base_depth_m`, `depth_to_bedrock_m`, `max_depth_m` y `deep_layers`, y los rásteres son `static.soil_base_depth_path` y `static.depth_to_bedrock_path`.

`DTB_path` es opcional en el modo en capas. En MATLAB, el fondo de la columna recurre a `subsurface_depth_to_bedrock_m` y luego a la `DTB (m)` de cada clase de suelo, con una advertencia. Antes del 2026-10-20, un `DTB_path` ausente significaba 1 m sin aviso. El esquema de agua subterránea predeterminado sigue requiriendo `DTB_path`.

### Fuentes globales usadas por el Case Builder {#global-sources-used-by-the-case-builder}

El Case Builder aplica las mismas reglas a cualquier dominio.

| Mapa | Fuente |
|---|---|
| `DTB.tif` (fondo de la columna) | Profundidad hasta el lecho de roca de SoilGrids, BDTICM (Shangguan et al., 2017) |
| `SoilBaseDepth.tif` (base del suelo) | Profundidad hasta el horizonte R de SoilGrids, BDRICM, censurada en 2 m y convertida de cm a m |

Ambos mapas provienen del mismo modelo de Shangguan et al. (2017), por lo que sus definiciones son coherentes.

---

## Interacción con las propiedades del suelo

DTB complementa la parametrización del suelo:
- Los parámetros del suelo controlan el comportamiento de la infiltración.
- DTB limita el volumen total disponible para almacenamiento

Esta combinación determina la respuesta efectiva del sistema sin requerir una discretización vertical explícita.

---

## Consideraciones prácticas

Al definir DTB:
- Evite valores excesivamente grandes
- Mantener la coherencia con la clasificación del suelo.
- Garantizar la coherencia espacial
- Utilice suposiciones simplificadas cuando sea necesario, pero documentelas.

DTB suele ser incierto y, cuando sea posible, debe evaluarse como parte del análisis de sensibilidad.

---

## Resumen

En el esquema predeterminado, DTB define el almacenamiento vertical efectivo disponible para el modelo y limita la profundidad de la zona vadosa. En el subsuelo en capas, DTB define la base del acuífero y la base del suelo define el fondo del suelo.
Puede representar la profundidad del lecho de roca o la profundidad de la superficie del acuífero, según el objetivo del modelado.
Aunque tiene una forma simple, desempeña un papel central en el control de la generación de escorrentía y la capacidad de almacenamiento en HydroPol2D.