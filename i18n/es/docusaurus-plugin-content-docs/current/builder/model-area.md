---
title: Elegir el área del modelo
---
import useBaseUrl from '@docusaurus/useBaseUrl';

# Elegir el área del modelo

**Prepare a case** tiene tres pestañas, una para cada tipo de área del modelo: **Urban Basin**,
**Urban Area Only** y **Catchment**. Cada pestaña guarda todos los ajustes de su caso, así que puede
tener un caso distinto en cada una. Los campos empiezan con valores de ejemplo. Reemplácelos por su
propio lugar y sus propias fechas.

<p align="center">
  <img src={useBaseUrl('/img/builder/case-builder-areas.es.svg')} width="760" alt="Tres mapas esquemáticos. Urban Basin: una ciudad en el extremo aguas abajo de varias cuencas aguas arriba, todas dentro de un mismo borde del dominio. Urban Area Only: una ciudad dentro de una franja, con dos ríos que entran por el borde y el mar en una esquina. Catchment: una cuenca con su red de ríos, la salida que usted indica y tres salidas candidatas en el río" />
</p>

<p align="center">
  <em>Figura 1. Los tres tipos de área del modelo, como mapas esquemáticos. La línea negra gruesa es el borde del dominio del modelo.</em>
</p>

| Pestaña | Dominio | Úsela para |
|---|---|---|
| **Urban Basin** | la ciudad y todas las cuencas de nivel 12 de HydroBASINS aguas arriba de ella | inundaciones urbanas en las que importa el agua que viene de aguas arriba |
| **Urban Area Only** | la mancha urbana y una franja a su alrededor | la ciudad sola, con caudales de entrada de ríos y niveles costeros en su borde |
| **Catchment** | todo lo que está aguas arriba de una salida que usted elige | una cuenca fluvial, con o sin ciudad |

## Urban Basin {#urban-basin}

**Location input** ofrece **City name** o **Polygon file**.

- **City name**: escriba la **City** y el **Country**. El Builder busca la ciudad en GHSL Urban
  Centre Database R2024A.
- **Polygon file**: la ruta de su propio polígono urbano en **Urban polygon path** (un GeoPackage,
  un Shapefile o cualquier otro archivo vectorial que GeoPandas pueda leer). Úselo cuando GHSL no
  tiene la ciudad o cuando necesita otro límite.

El Builder interseca la ciudad con las cuencas de nivel 12 de HydroBASINS y sigue sus conexiones
aguas arriba. El dominio es la ciudad y todas esas cuencas aguas arriba. El nivel 12 de HydroBASINS
es el nivel global más fino, pero sigue siendo un contorno regional. FABDEM y HydroBathyDEM dan el
terreno y el enrutamiento dentro de él.

Las dos pestañas urbanas ofrecen dos tipos de malla: **Uniform grid** o **Quadtree grid**, que
mantiene fina la ciudad y gruesa el resto ([Ajustes del caso](settings#grid-and-period)).

<p align="center">
  <img src={useBaseUrl('/img/builder/builder-urban-basin.png')} width="760" alt="La pestaña Urban Basin con City Tucson y Country United States, Quadtree grid seleccionada, tamaño de celda fino de 90 m, tamaño de celda grueso de 360 m, franja de malla fina de 120 m, calentamiento de 0 días, área de inicio de los ríos de 5 km2, fuente de terreno FABDEM y las fechas y horas de la simulación en UTC" />
</p>

<p align="center">
  <em>Figura 2. La pestaña Urban Basin para Tucson, Arizona, con una malla quadtree de celdas de 90 m sobre la ciudad y de 360 m sobre el resto de la cuenca.</em>
</p>

## Urban Area Only {#urban-area-only}

La entrada de ubicación es la misma que en Urban Basin. El dominio es la mancha urbana conectada y
una franja a su alrededor (**Exterior buffer**, 1 km por defecto), sin las cuencas aguas arriba.

Cada borde exterior del dominio recibe una condición de contorno. El flujo crítico es la opción por
defecto. Donde corresponden, **GloFAS river inflows** y un **Coastal water level** de GTSM lo
reemplazan, en este orden de prioridad: marea, luego caudal de entrada de GloFAS y luego flujo
crítico. Los ajustes están en [Urban boundary conditions](settings#urban-boundary-conditions).

La vista previa lista los **Rivers entering the domain**: los cruces de HydroRIVERS con el borde
del dominio, en un mapa y en una tabla. En la tabla puede desmarcar **accepted** para un cruce o
moverlo con su **longitude** y su **latitude**. **Save river-entry review** guarda sus elecciones,
y **Prepare complete case** las usa.

<p align="center">
  <img src={useBaseUrl('/img/builder/builder-river-entries.png')} width="700" alt="Ríos que entran en el dominio de Tucson: un mapa del dominio Urban Area Only con las líneas de HydroRIVERS y puntos rojos de entrada de ríos en su borde y, debajo, la tabla de candidatos con el ID del río, el área aguas arriba, la longitud, la latitud y una casilla accepted, y el botón Save river-entry review" />
</p>

<p align="center">
  <em>Figura 3. Ríos que entran en el dominio Urban Area Only de Tucson, después de la vista previa. Cada punto rojo es un lugar donde un río cruza el borde del dominio. La tabla los lista con su área aguas arriba.</em>
</p>

Los casos Urban Area Only se ejecutan con el solver de malla nativo de HydroPol2D (UGRID), para los
dos tipos de malla.

## Catchment {#catchment}

Dé al caso un **Catchment name** y luego elija la **Outlet input**:

| Outlet input | Qué indica usted |
|---|---|
| **Map click** | haga clic en la salida sobre un mapa topográfico. La página muestra la latitud y la longitud del clic. |
| **Coordinates** | **Longitude** y **Latitude** en grados (WGS 84). |
| **Point file** | un archivo vectorial con un punto. |
| **Polygon file** | un polígono, usado como **exact** (como la cuenca) o como área de búsqueda, **search** (**Polygon use**). |

Tres ajustes más colocan la salida en la red de ríos:

- **Snap radius (km, 0 = automatic)**: hasta dónde puede moverse la salida para llegar al río. El
  valor automático es el mayor entre 1 km y dos celdas del modelo.
- **Outlet candidate**: la vista previa encuentra las tres celdas de salida cercanas con mayor
  acumulación de flujo de HydroSHEDS. Elija 1, 2 o 3. Al cambiarlo, la vista previa se actualiza
  sola.
- **Critical outlet cells**: el número de celdas de contorno conectadas en la salida que reciben
  una condición de profundidad crítica (10 por defecto).

<p align="center">
  <img src={useBaseUrl('/img/builder/builder-prepare-catchment.png')} width="760" alt="La pestaña Catchment para San Francisquito Creek: nombre de la cuenca, Coordinates seleccionado con longitud -122,1889 y latitud 37,4239, radio de ajuste 0, salida candidata 1, 10 celdas de salida críticas, un tamaño de celda de 10 m, las fechas, la lluvia IMERG, HydroPol2D Python y los cuatro procesos simulados marcados" />
</p>

<p align="center">
  <em>Figura 4. La pestaña Catchment para San Francisquito Creek en Stanford, California, con la salida dada por sus coordenadas y una malla de 10 m.</em>
</p>

La vista previa dibuja un primer contorno de la cuenca a partir de HydroSHEDS. Después, la
construcción completa rellena las depresiones del terreno a la resolución del modelo, calcula las
direcciones de flujo D8, vuelve a ajustar la salida al río y traza todas las celdas aguas arriba.
Se guardan tanto la cuenca final como el primer contorno. Si sus áreas difieren en más de un factor
de dos, el caso no pasa la verificación hasta que usted lo revise (pruebe otra candidata o un radio
de ajuste mayor).

Los casos Catchment usan una malla uniforme. Son los únicos casos con el flujo base del acuífero
profundo y la calibración del agua subterránea a partir del caudal observado
([Ajustes del caso](settings#hydraulic-parameters)).
