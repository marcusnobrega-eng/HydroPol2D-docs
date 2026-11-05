---
title: Vista previa y costo
---
import useBaseUrl from '@docusaurus/useBaseUrl';

# Vista previa y costo

**Preview domain and cost** dibuja el dominio y estima el tamaño del caso en segundos, antes de
cualquier descarga grande. Todavía no se construye nada, así que puede cambiar los ajustes y repetir
la vista previa hasta que el dominio sea el correcto. **Prepare complete case** sigue en gris hasta
que la vista previa corresponda a los ajustes actuales.

## Antes de la vista previa {#before-the-preview}

Encima de los dos botones, la página verifica la solicitud:

- el periodo que cubre cada fuente de lluvia, por ejemplo "NASA IMERG Final Run availability:
  1998-01-01 through 2025-09-30";
- las cuentas y las herramientas que necesita el caso. Cuando falta una, un cuadro amarillo dice
  "This case cannot be prepared yet:" y la nombra (vea [Fuentes de datos y cuentas](data-accounts));
- para AORC, que todo el dominio esté dentro de la malla de AORC, lo que confirma la vista previa;
- cuando todo está listo: "Required credentials, source coverage, and local tools are ready for
  this request."

## Qué muestra la vista previa {#what-the-preview-shows}

1. **Case files**: la carpeta del caso, en verde. La vista previa ya escribe allí la solicitud, el
   dominio y los mapas de vista previa.
2. **El dominio en un mapa.** El mapa es interactivo, sobre OpenTopoMap. El control de capas cambia
   a un mapa de calles u oculta las superposiciones. El mapa en línea es solo un fondo: no cambia el
   caso.
3. **Estimated quadtree grid** (casos quadtree): las zonas de resolución de la malla.
4. **Rivers entering the domain** (Urban Area Only): vea [Elegir el área del modelo](model-area#urban-area-only).
5. **El tamaño del caso**: seis números y, para una malla quadtree, las celdas de cada tamaño.

<p align="center">
  <img src={useBaseUrl('/img/builder/builder-preview-map.jpg')} width="760" alt="La vista previa de la cuenca urbana de Tucson: el mensaje de listo, los botones Preview domain and cost y Prepare complete case, la línea verde Case files y un mapa topográfico interactivo con el área urbana en naranja, las cuencas conectadas y las cuencas aguas arriba en azul, y la red de ríos" />
</p>

<p align="center">
  <em>Figura 1. La vista previa de la cuenca urbana de Tucson. La ciudad (naranja) está aguas abajo en la cuenca del río Santa Cruz, por lo que las cuencas aguas arriba se extienden hacia el sur, más allá de la frontera, hasta México.</em>
</p>

<p align="center">
  <img src={useBaseUrl('/img/builder/builder-preview-quadtree.jpg')} width="560" alt="Malla quadtree estimada de la cuenca urbana de Tucson: la ciudad cubierta por celdas de 90 m, una banda delgada de celdas de 180 m a su alrededor y el resto de la cuenca en celdas de 360 m" />
</p>

<p align="center">
  <em>Figura 2. Las zonas quadtree del mismo caso: celdas de 90 m sobre la ciudad y su franja, una banda de celdas de 180 m y celdas de 360 m sobre el resto de la cuenca.</em>
</p>

Para un caso Catchment, el mapa muestra la salida que usted indicó, las tres salidas candidatas en
la red de ríos y un primer contorno de la cuenca.

<p align="center">
  <img src={useBaseUrl('/img/builder/builder-preview-catchment.jpg')} width="760" alt="La vista previa de San Francisquito Creek sobre un mapa topográfico, con la salida indicada como un punto rojo, las salidas candidatas en naranja sobre la red de ríos, el primer contorno de la cuenca y, debajo, las celdas de la matriz, las celdas activas y el área de la cuenca" />
</p>

<p align="center">
  <em>Figura 3. La vista previa de San Francisquito Creek. El punto rojo es la salida que usted indicó, los puntos naranjas son las salidas candidatas y el contorno es un primer esbozo de la cuenca. La construcción completa vuelve a delimitar la cuenca en la malla del modelo.</em>
</p>

## El tamaño del caso {#size}

| Número | Qué significa |
|---|---|
| **Matrix cells** | filas por columnas del rectángulo que rodea todo el dominio |
| **Active cells** | las celdas dentro del dominio |
| **Basin area** | el área del dominio, en km² |
| **Temporary transfer ceiling** | un límite superior de los datos fuente que descarga la construcción, mapas estáticos y forzamiento juntos |
| **Retained forcing inputs** | la lluvia y el clima que se conservan con el caso terminado |
| **Estimated saved outputs** | el tamaño de los resultados que guardará el modelo, según las salidas que usted eligió |

<p align="center">
  <img src={useBaseUrl('/img/builder/builder-preview-metrics.png')} width="760" alt="Los seis números de la vista previa quadtree de Tucson: 1.743.840 celdas de la matriz, 107.512 celdas activas, un área de la cuenca de 8.227 km2, un límite de transferencia de 195,2 MiB, 0,5 MiB de forzamiento conservado y 1,36 GiB de salidas guardadas, luego una tabla con 40.230 celdas de 90 m, 8.426 de 180 m y 58.856 de 360 m, y el panel plegado How these values are estimated" />
</p>

<p align="center">
  <em>Figura 4. El tamaño del caso de Tucson: 107.512 celdas activas en una cuenca de 8.227 km², menos de 200 MiB para descargar y unos 1,4 GiB de resultados.</em>
</p>

La memoria depende sobre todo de la matriz, no solo de las celdas activas. Un dominio alargado o
fragmentado puede necesitar más memoria de lo que sugiere su área. **How these values are
estimated** explica cada número y lista la descarga y las salidas guardadas por fuente. Algunas
notas de ese panel:

- La transferencia cuenta los valores de origen a la resolución propia de cada producto, sobre el
  dominio y el periodo. No cuenta los rásteres de HydroPol2D que escribe la construcción. MSWEP se
  cuenta como valores sin comprimir, así que el tráfico real es menor.
- Los archivos fuente sin procesar se eliminan después de una construcción exitosa. Una
  construcción fallida los conserva, para que el siguiente intento continúe desde allí.
- La estimación de las salidas guardadas cuenta solo los archivos seleccionados, como valores sin
  comprimir.

Empiece los modelos regionales grandes con un tamaño de celda grueso, lea los números y pase a uno
más fino solo cuando quepan en su computadora.

## Cuando cambian los ajustes {#settings-change}

Cualquier cambio después de una vista previa muestra "Settings changed. Run the preview again
before preparing this case." El **Process log** al pie de la pestaña conserva los mensajes de la
última vista previa o construcción.
