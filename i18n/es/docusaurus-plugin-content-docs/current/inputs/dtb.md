---
title: DTB
---

# Profundidad hasta el lecho de roca (DTB)

La profundidad hasta el lecho de roca (DTB) define la extensión vertical de la columna de suelo disponible para el almacenamiento de agua en HydroPol2D.
Representa la distancia entre la superficie terrestre y una capa limitante que restringe el movimiento vertical del agua. Esta capa puede corresponder a un lecho de roca real o a un límite efectivo, como la parte superior de un acuífero poco profundo.
---

## Papel en HydroPol2D

DTB se utiliza para definir:
- Capacidad máxima de almacenamiento subterráneo
- Límite vertical de infiltración y percolación.
- Espesor efectivo de la zona vadosa.
- Inicio de la saturación dentro de la columna del suelo.

Dentro del modelo, DTB actúa como una **restricción geométrica** de almacenamiento en lugar de un perfil vertical completamente resuelto.
DTB no debe confundirse con el ráster inicial opcional del nivel freático. En el modelo actual, `PHTOKEN1XYZ_path` define el espesor de la columna de suelo, mientras que `GW_table_path` define la altura/elevación saturada inicial cuando la inicialización del agua subterránea se proporciona explícitamente.
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

Si no hay un mapa DTB disponible, los valores se pueden asignar a través de las **tablas de parámetros del suelo**.
En este caso:
- Cada clase de suelo está asociada con un valor representativo de DTB.
- El campo DTB se construye implícitamente a partir de la clasificación del suelo.

Este enfoque garantiza la coherencia entre:
- Propiedades hidráulicas del suelo.
- Profundidad de almacenamiento disponible

Es particularmente útil en entornos con escasez de datos.
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

DTB define el almacenamiento vertical efectivo disponible para el modelo y limita la profundidad de la zona vadosa.
Puede representar la profundidad del lecho de roca o la profundidad de la superficie del acuífero, según el objetivo del modelado.
Aunque tiene una forma simple, desempeña un papel central en el control de la generación de escorrentía y la capacidad de almacenamiento en HydroPol2D.