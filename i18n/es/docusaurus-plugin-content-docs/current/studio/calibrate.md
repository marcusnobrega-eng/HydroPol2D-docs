---
title: Calibración en Studio
---
import useBaseUrl from '@docusaurus/useBaseUrl';

# Calibración en Studio
**Calibrate** ajusta los parámetros del modelo al caudal, las profundidades del agua, los niveles del agua y las profundidades del agua subterránea observados, con un algoritmo genético. Es el cuarto espacio de trabajo de la barra de la izquierda (Cmd+4 en un Mac, Ctrl+4 en Windows). El método, las puntuaciones y los ajustes se explican en [Calibración con observaciones](../calibration/ga-calibration).

La página tiene seis secciones, en el orden en que se usan.

## 1. Observed data {#1-observed-data}

Elija una tabla y pegue filas desde Excel o desde un archivo de texto (**Paste rows**), o escríbalas.

| Columna | Contenido |
|---|---|
| Gauge | El nombre de la serie; las filas con el mismo nombre forman una serie |
| Easting, Northing | Coordenadas opcionales, en el sistema de coordenadas del modelo |
| Time | Minutos desde el inicio de la simulación |
| Value | El valor observado, en las unidades de la tabla |
| Observation uncertainty | Opcional. El error de medición del valor, expresado como una desviación estándar en las mismas unidades |

Hay tablas para el caudal, la profundidad del agua, el nivel del agua, la profundidad del agua subterránea y la humedad del suelo superficial. La humedad del suelo todavía no se puede calibrar. **How to fill this table** lista las columnas de la tabla seleccionada. Las filas entran en el modelo a medida que se pegan; **Save** las escribe en el archivo del modelo.

## 2. Observations to match {#2-observations-to-match}

Cada fila es una serie observada. Marque **Use** en las series que se deben ajustar.

- **Compare with**: una estación de enrutamiento, un punto de observación, la salida del modelo (solo caudal) o la celda en las coordenadas de la serie. Las estaciones y los puntos de observación se dibujan en Setup > Study area.
- **Score**: KGE, NSE, NSE de valores logarítmicos, RMSE / desviación estándar, pico, volumen y tiempo al pico (caudal) o error / incertidumbre (series con incertidumbre).
- **Weight**: Auto da a cada tipo de observación una parte igual. Un número fija el peso de la serie.
- **Changes only**: evalúa las subidas y bajadas, no un desplazamiento constante. Sirve para pozos con un nivel de referencia incierto.
- **Use uncertainty**: pondera cada valor por uno sobre el cuadrado de su incertidumbre, de modo que los valores inciertos cuentan menos. Está activado por defecto cuando la serie tiene incertidumbres.

**Ignore observations before** define un periodo de calentamiento que se simula pero no se evalúa.

## 3. Parameters to calibrate {#3-parameters-to-calibrate}

Se listan todos los parámetros que este modelo puede calibrar, agrupados por proceso. Marque **Free** en cada parámetro que la búsqueda puede cambiar; los demás conservan los valores del modelo.

- **Los multiplicadores** (valor del modelo ×1) escalan juntos el valor, las tablas de clases y el ráster, de modo que el mapa conserva su patrón. Conviene empezar con unos pocos.
- **Lower** y **Upper** fijan el rango de búsqueda y se pueden editar.
- **Group** y **Show free only** acortan la lista; el contador muestra cuántos son libres.
- Aparece una nota cuando hay muchos parámetros libres para los tipos de observación que se ajustan.

## 4. Search settings {#4-search-settings}

**Genetic algorithm**: tamaño de la población (Auto es 10 por parámetro libre), generaciones, fracción de élite, tamaño del torneo, probabilidades de cruce y de mutación, tamaño de la mutación, población inicial, parada temprana, límite de tiempo y semilla aleatoria. La línea debajo de los ajustes da el número máximo de simulaciones del modelo y, después de una primera calibración, una estimación del tiempo.

**Computer**

- **Runs**: Auto (primero mide la memoria de una simulación), One at a time (cada simulación usa todo el equipo) o Several at a time.
- **Runs at a time** y **Threads per run**, para Several at a time.
- **Use at most**: la fracción de la memoria libre que pueden ocupar varias simulaciones.
- **Device**: la CPU, o una GPU si el equipo tiene una, con la memoria de GPU por simulación.
- **Results folder**: por defecto, una carpeta nueva junto al archivo del modelo.
- **Resume the stopped calibration in this folder** continúa una calibración que se canceló o se interrumpió.

## 5. Run {#5-run}

**Start calibration** verifica las elecciones e inicia la búsqueda en segundo plano; Studio se puede seguir usando. La barra de progreso y la línea debajo de ella muestran la generación, la simulación y la mejor puntuación hasta el momento, y el registro lista cada simulación.

**Cancel** detiene las simulaciones en curso en su siguiente paso del modelo. Las simulaciones terminadas se guardan, así que una calibración reanudada no las repite.

## 6. Results {#6-results}

- **Summary**: la mejor puntuación (0 es un ajuste perfecto), por qué se detuvo la búsqueda, las simulaciones y el tiempo empleado.
- **Best values**: cada parámetro libre, su valor en el modelo, su mejor valor, el rango en el 10 % mejor de los candidatos y si los datos lo determinan.
- **Fit per series**: el error del modelo actual y de la mejor simulación, con el KGE o el NSE de la mejor simulación.
- **Show**: todas las series en paneles pequeños, la puntuación por serie, el historial de la búsqueda o una sola serie. Cada panel muestra las observaciones (con su incertidumbre), el modelo actual y la mejor simulación.

<p align="center">
  <img src={useBaseUrl('/img/calibration/ga-calibration-series.png')} width="900" alt="Tres paneles a lo largo de una hora con el caudal en la salida, la profundidad del agua en el canal y la profundidad del agua subterránea en la ladera, cada uno con las observaciones, el modelo actual y la mejor simulación" />
</p>

<p align="center">
  <em>Resultados de una calibración corta, con las observaciones y su incertidumbre, el modelo actual (línea discontinua) y la mejor simulación.</em>
</p>

**Apply to model** escribe los mejores valores en el modelo abierto, y **Save** los guarda. Un multiplicador sobre un ráster de entrada escribe el ráster escalado en la carpeta de resultados y hace que el modelo apunte a él, sin cambiar el original. **Undo apply** devuelve el modelo a como estaba, siempre que no se haya editado desde entonces. **Show results folder** abre la carpeta con las tablas y las figuras de la calibración.
