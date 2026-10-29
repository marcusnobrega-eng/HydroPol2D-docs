---
title: Calibración con Observaciones (Algoritmo Genético)
---
import useBaseUrl from '@docusaurus/useBaseUrl';

# Calibración con Observaciones (Algoritmo Genético)

La calibración con algoritmo genético (AG) ajusta los parámetros del modelo a varios tipos de observaciones a la vez. Estos tipos son el caudal, la profundidad del agua, el nivel del agua y la profundidad del agua subterránea. Cada candidato es una simulación completa del evento con el modelo, evaluada frente a todas las series observadas. El usuario elige qué parámetros son libres, y los demás conservan los valores del modelo. En HydroPol2D Studio, es el [espacio de trabajo Calibrate](../studio/calibrate).

Las dos herramientas de calibración responden a preguntas distintas.

| Herramienta | Datos | Ajusta |
|---|---|---|
| Esta página | Series observadas durante un evento o un período (caudal, profundidades, niveles del agua, pozos) | Cualquier parámetro del modelo, elegido por el usuario |
| [Calibración por recesión del agua subterránea](groundwater-recession) | Registros largos de caudal diario, a través de su curva maestra de recesión | Conductividad y almacenamiento del acuífero, y el estado inicial del agua subterránea |

Los valores calibrados son parámetros efectivos para esta estructura del modelo y estos datos. No son mediciones del suelo ni del acuífero.

---

## 1. Observaciones {#1-observations}

Cada serie observada es un objetivo. Un objetivo tiene un tipo, un lugar donde se compara con el modelo y su propia puntuación.

| Tipo | Se compara con |
|---|---|
| Caudal | Una estación de enrutamiento, o la salida del modelo (todo el caudal que sale por los contornos) |
| Profundidad del agua | Una estación de enrutamiento (la media de sus celdas), un punto de observación o la celda en las coordenadas de la serie |
| Nivel del agua (cota) | Igual que la profundidad del agua, con el mismo nivel de referencia que el terreno |
| Profundidad del agua subterránea | Un punto de observación o la celda en las coordenadas de la serie |

- **Los tiempos** están en minutos desde el inicio de la simulación. La salida del modelo se interpola a los tiempos de observación.
- **Un período de calentamiento** se simula, pero no se evalúa. Las observaciones de ese período se ignoran.
- **Changes only** resta la media de cada serie antes de evaluarla. Está pensado para pozos cuyo nivel de referencia es incierto y para profundidades cuya cota del lecho proviene del DEM. Cuentan las subidas y bajadas, pero no un desplazamiento constante.
- **La incertidumbre** (opcional) es el error de medición de cada valor, expresado como una desviación estándar en las unidades del valor. La sección 2.3 explica cómo se usa.

Las observaciones se registran en puntos de observación, que todavía no están disponibles en mallas de Voronoi y quadtree. En esas mallas, solo se puede calibrar el caudal en las estaciones de enrutamiento.

---

## 2. La puntuación {#2-the-score}

### 2.1 Un error por serie {#21-one-error-per-series}

Cada serie recibe un error $E$ sin unidades, que vale 0 para un ajuste perfecto. Así, el caudal, las profundidades y los niveles en pozos se pueden sumar. En la tabla, $s_i$ son los valores simulados y $o_i$ los observados.

| Puntuación | Error $E$ | Predeterminada para |
|---|---|---|
| KGE | $\sqrt{(r-1)^2 + (\alpha-1)^2 + (\beta-1)^2}$ | Caudal, profundidad del agua, profundidad del agua subterránea |
| NSE | $\sum (s_i - o_i)^2 \,/\, \sum (o_i - \bar o)^2$ | Nivel del agua |
| NSE de valores logarítmicos | como NSE, sobre $\ln(x + \bar o/100)$; favorece los caudales bajos | |
| RMSE / desviación estándar | $\mathrm{RMSE} / \sigma_o$ | |
| Pico, volumen y tiempo al pico | la puntuación de hidrograma del GenericGA de HydroPol2D (ver más abajo) | |
| Error / incertidumbre | $\sqrt{\tfrac{1}{n}\sum \left((s_i - o_i)/u_i\right)^2}$ | |

En KGE ([Gupta et al., 2009](https://doi.org/10.1016/j.jhydrol.2009.08.003)), $r$ es la correlación, $\alpha = \sigma_s/\sigma_o$ es la razón entre las desviaciones estándar y $\beta = \bar s/\bar o$ es la razón entre las medias. El error es $E = 1 - \mathrm{KGE}$. NSE es la eficiencia de [Nash y Sutcliffe (1970)](https://doi.org/10.1016/0022-1694(70)90255-6), y $E = 1 - \mathrm{NSE}$. Los niveles del agua y las cargas hidráulicas usan NSE por defecto porque su nivel de referencia es arbitrario, y la razón entre medias de KGE dice poco sobre un nivel de 500 m. Con Changes only, KGE omite su término de sesgo.

La puntuación de pico, volumen y tiempo al pico es la puntuación compuesta del GenericGA de MATLAB.

$$
E = \frac{\mathrm{RMSE}}{Q_p} + \frac{|V_s - V_o|}{V_o} + 0.75\,\frac{|Q_{p,s} - Q_p|}{Q_p} + 0.25\,\frac{|t_{p,s} - t_p|}{7200\ \mathrm{s}} + 0.25\,\frac{|\bar s - \bar o|}{Q_p}
$$

Aquí, $Q_p$ y $t_p$ son el pico observado y su tiempo, y $V$ es el volumen en la ventana evaluada.

### 2.2 Una puntuación para la calibración {#22-one-score-for-the-calibration}

La calibración minimiza la media ponderada de los errores.

$$
J = \frac{\sum_e \omega_e \sum_k w_k E_k}{\sum_e \omega_e}, \qquad \sum_k w_k = 1
$$

Aquí, $e$ recorre los eventos simulados y $k$ las series de cada evento. Sin pesos explícitos, cada tipo de observación recibe una parte igual, repartida por igual entre sus series. Con una estación de caudal, una estación de profundidad y dos pozos, los pesos son 1/3, 1/3, 1/6 y 1/6. Así, diez pozos no pesan más que una estación de caudal. La profundidad y el nivel del agua cuentan como un solo tipo, y lo mismo ocurre con la profundidad del agua subterránea y la carga hidráulica. Cuando el usuario da un peso a alguna serie, las series sin peso cuentan como 1 y todos los pesos se normalizan.

### 2.3 Uso de la incertidumbre {#23-using-the-uncertainty}

Con **Use uncertainty**, cada punto cuenta con el peso

$$
w_i = \frac{u_i^{-2}}{\sum_j u_j^{-2}},
$$

de modo que los valores más inciertos pesan menos. Las medias, las varianzas, la correlación y las sumas de residuos de KGE, NSE, NSE logarítmico y RMSE / desviación estándar usan entonces estos pesos. Si la incertidumbre es la misma en todos los puntos, las puntuaciones no cambian. Los valores sin incertidumbre toman la mediana de las incertidumbres conocidas. La puntuación de pico, volumen y tiempo al pico ignora la incertidumbre.

La puntuación **error / incertidumbre** la usa directamente. Un valor de 1 significa que el modelo se desvía, en promedio, en un error de medición. Por debajo de 1, el ajuste queda dentro del propio error de los datos. Los resultados también dan la fracción de puntos dentro de $\pm u_i$.

---

## 3. Parámetros {#3-parameters}

Se listan todos los parámetros que el modelo puede calibrar, y cada uno es libre o fijo. Los parámetros fijos conservan los valores del modelo. La lista sigue los módulos activos y el esquema de subsuelo. Un caso sin nieve no tiene parámetros de nieve, y un caso [en capas](../theory/layered-subsurface) no tiene un único rendimiento específico, porque allí $S_y$ proviene de la curva de retención de cada capa.

Un parámetro puede ser de tres tipos.

| Tipo | Ejemplo | Qué cambia |
|---|---|---|
| Un multiplicador sobre un campo del modelo | n de Manning × 1.3 | El valor de configuración, cada fila de clase y el ráster, todos multiplicados, de modo que el mapa conserva su patrón |
| Un valor de una clase | n de Manning de la cobertura del suelo 2 | Esa fila de clase |
| Un valor único | Multiplicador de la conductividad lateral del regolito | Ese valor de configuración |

Un multiplicador de campo da exactamente el factor por el mapa preparado, sea cual sea la entrada que aportó el valor de cada celda. Conviene empezar por ellos. Unos pocos multiplicadores se pueden identificar en casos en que muchos valores de clase no se pueden identificar. Los límites están en escala logarítmica para las conductividades, la rugosidad y otros factores positivos, y en escala lineal para las fracciones.

| Grupo | Parámetros |
|---|---|
| Superficie | n de Manning, almacenamiento en depresiones, n de Manning del canal (canales subgrid) |
| Suelo e infiltración | Conductividad saturada, α y n de van Genuchten, θ<sub>s</sub>, θ<sub>r</sub>, profundidad del suelo |
| Evapotranspiración y dosel | Profundidad de raíces, coeficiente de cultivo, cargas de Feddes h3 y h4, almacenamiento del dosel por unidad de LAI |
| Agua subterránea | Rendimiento específico y conductividad del agua subterránea (esquema predeterminado), conductividad del lecho del río, carga capilar de capacidad de campo, anisotropía vertical |
| Subsuelo en capas | Multiplicadores de la conductividad lateral del suelo y del regolito, anisotropía lateral del suelo, propiedades del regolito, profundidad de la base del suelo, profundidad hasta el lecho de roca |
| Acuífero profundo | Fracción de recarga profunda, tiempo de respuesta, flujo base profundo inicial |
| Nieve | Factor de grados-día, temperaturas de solo nieve y de solo lluvia, albedo, densidad de la nieve fresca |
| Calidad del agua | Máximo y tasa de acumulación (buildup), coeficiente y exponente de lavado (washoff), días secos antecedentes |
| Estado inicial | Contenido de agua inicial del suelo, profundidad inicial del nivel freático |

Cada candidato se verifica con las reglas propias del modelo antes de ejecutarse. Un candidato con $\theta_i > \theta_s$, o con las cargas de Feddes fuera de orden, se rechaza y recibe la peor puntuación.

---

## 4. La búsqueda {#4-the-search}

### 4.1 Algoritmo genético {#41-genetic-algorithm}

El AG trabaja con los parámetros libres en su escala de búsqueda (logarítmica o lineal).

1. **Población inicial.** Se reparte de forma uniforme entre los límites (un hipercubo latino, [McKay et al., 1979](https://doi.org/10.2307/1268522)), con el modelo actual como uno de sus miembros.
2. **Evaluar** cada miembro con una simulación completa del modelo.
3. **Conservar la élite.** La mejor fracción se copia sin cambios a la siguiente generación.
4. **Elegir los padres** por torneo. Cada padre es el mejor de unos pocos miembros elegidos al azar.
5. **Cruzar.** Un hijo toma una mezcla aleatoria de sus dos padres, parámetro por parámetro.
6. **Mutar.** Algunos parámetros reciben un paso gaussiano, recortado a los límites.
7. **Repetir** hasta la última generación, una parada temprana o el límite de tiempo.

Un candidato ya visto (de la élite o duplicado) no se vuelve a ejecutar.

| Ajuste | Valor predeterminado | Significado |
|---|---|---|
| Tamaño de la población | 10 por parámetro libre, al menos 10 | Candidatos por generación |
| Generaciones | 10 | Número máximo de generaciones |
| Fracción de élite | 20 % | Mejores miembros copiados sin cambios |
| Tamaño del torneo | 3 | Miembros comparados para elegir un padre |
| Probabilidad de cruce | 85 % | Probabilidad de que un hijo mezcle dos padres |
| Probabilidad de mutación | 25 % | Probabilidad de que cada parámetro mute |
| Tamaño de la mutación | 15 % del rango | Desviación estándar de un paso de mutación |
| Población inicial | Hipercubo latino, con el modelo actual | O aleatoria uniforme |
| Parada temprana | mejora menor que 1 % en 3 generaciones | Se puede desactivar |
| Límite de tiempo | ninguno | Se verifica antes de cada generación |
| Semilla aleatoria | 42 | La misma semilla y los mismos ajustes repiten la misma búsqueda |

Los operadores y sus valores predeterminados siguen el GenericGA de MATLAB, por lo que ambos dan búsquedas comparables.

### 4.2 Varias simulaciones a la vez {#42-several-runs-at-a-time}

| Modo | Qué se ejecuta |
|---|---|
| One at a time | Cada simulación usa todo el equipo (todos los hilos de la CPU, o la GPU) |
| Several at a time | El número elegido de simulaciones en paralelo, cada una en su propio proceso |
| Auto | Una simulación de prueba mide su memoria. Luego se ejecutan a la vez tantas simulaciones como caben en el 70 % de la memoria libre y en la mitad de los núcleos de la CPU |

- **Memoria.** Cuando varias simulaciones necesitarían más que la fracción permitida de la memoria libre, se ejecutan menos a la vez, y el registro lo indica.
- **Hilos.** El límite de hilos por simulación se aplica a las bibliotecas numéricas y, en Linux, fija cada simulación a sus propios núcleos. En macOS y Windows, JAX elige su propio número de hilos.
- **GPU.** En una GPU, las simulaciones se ejecutan de una en una, salvo que cada simulación reciba una parte de la memoria de la GPU.

En una computadora portátil (10 núcleos, 24 GB), una simulación del caso gemelo descrito más abajo usó cerca de 0.74 GB y dos hilos, y Auto eligió cinco simulaciones a la vez.

### 4.3 Detener y reanudar {#43-stopping-and-resuming}

Cada simulación terminada se guarda en cuanto termina. **Cancel** detiene las simulaciones en curso en su siguiente paso del modelo, y estas no se guardan. Una calibración detenida se reanuda desde su carpeta. La búsqueda repite la misma semilla a partir de las simulaciones guardadas, así que llega exactamente a la población a la que habría llegado una búsqueda sin interrupciones. Al reanudar, solo pueden cambiar el número de generaciones, el límite de tiempo y la parada temprana.

---

## 5. Resultados {#5-results}

### 5.1 ¿Pueden los datos determinar un parámetro? {#51-can-the-data-pin-a-parameter-down}

Para cada parámetro libre, la calibración toma el 10 % mejor de los candidatos terminados (al menos 5) y mide su dispersión. La dispersión se expresa como fracción del rango de búsqueda, en la escala de búsqueda.

| Dispersión | Veredicto |
|---|---|
| hasta 0.25 | Bien identificado |
| de 0.25 a 0.5 | Débilmente identificado |
| más de 0.5 | No identificado; los datos no lo distinguen y es mejor dejarlo fijo |

La verificación necesita al menos 30 simulaciones terminadas, o 10 por parámetro libre si ese número es mayor. Antes de eso, los mejores candidatos están demasiado próximos entre sí para sacar una conclusión.

### 5.2 Modelo actual y mejor simulación {#52-current-model-and-best-run}

El modelo actual es el primer miembro de la primera generación, por lo que cada serie se muestra dos veces, con los valores propios del modelo y con los mejores valores. La comparación muestra qué cambió la calibración en cada serie y si mejoró una serie a costa de otra.

### 5.3 Archivos {#53-files}

| Archivo | Contenido |
|---|---|
| `GA_Settings.json` | Ajustes, parámetros libres y una huella de las observaciones, que se verifican al reanudar |
| `GA_Evaluations.jsonl` | Cada simulación terminada, guardada en cuanto termina |
| `GA_History.csv` | Cada candidato de cada generación, con sus parámetros, su puntuación y el error por serie |
| `Best_Parameters.csv` | El mejor valor de cada parámetro libre, con sus límites |
| `Best_Metrics.csv`, `Best_Series.csv` | Error, componentes de la puntuación y valores observados frente a simulados, por serie |
| `Comparison_Metrics.csv`, `Comparison_Series.csv` | Lo mismo para el modelo actual y la mejor simulación, lado a lado |
| `Identifiability.csv` | La dispersión y el veredicto de la sección 5.1 |
| `GA_Performance.png` | La puntuación de cada candidato y la mejor hasta el momento, por generación |
| `GA_Summary.json` | Por qué se detuvo la búsqueda, las simulaciones, las simulaciones a la vez y el tiempo empleado |

Aplicar el resultado escribe los mejores valores en el modelo. Un multiplicador sobre un ráster de entrada escribe el ráster escalado en `calibrated_inputs`, dentro de la carpeta de resultados, y hace que el modelo apunte a él. El ráster original no cambia.

---

## 6. Experimento gemelo {#6-twin-experiment}

Un experimento gemelo pone a prueba el método antes de usar datos reales. El modelo genera las "observaciones" a partir de valores conocidos de los parámetros, y la calibración tiene que volver a encontrarlos.

| Configuración | Valor |
|---|---|
| Cuenca | En V, 50 × 81 celdas de 20 m; dos laderas y un canal hasta la salida |
| Procesos | Infiltración, agua subterránea local (esquema predeterminado), enrutamiento inercial local |
| Evento | 40 mm/h durante 1.5 h, 3 h simuladas |
| Observaciones cada 5 min | Caudal en la salida, profundidad del agua en un punto del canal, profundidad del agua subterránea en una ladera |
| Ruido | Gaussiano, 0 o 5 % de la desviación estándar de cada serie |
| Parámetros libres | Multiplicador de la n de Manning (0.5 a 2), multiplicador de la conductividad del suelo (0.1 a 10) |
| Verdad | Manning × 1.4, conductividad × 0.5 |
| Ajustes | Predeterminados (20 por generación, 10 generaciones, parada temprana); Auto, 5 simulaciones a la vez |

| Ruido | Manning encontrado | Conductividad encontrada | Simulaciones | Generaciones | Tiempo |
|---|---:|---:|---:|---:|---:|
| 0 % | 1.401 | 0.497 | 100 | 7 (parada temprana) | 4.2 min |
| 5 % | 1.410 | 0.502 | 140 | 10 | 5.1 min |

Ambos parámetros se recuperaron con un error menor que 1 % y quedaron bien identificados en los dos niveles de ruido (simulación del 2026-10-28). El ruido se escala con la variabilidad propia de cada serie. Por eso el nivel freático, que se mueve unos milímetros en este evento, recibe un ruido de milímetros.

<p align="center">
  <img src={useBaseUrl('/img/calibration/ga-calibration-series.png')} width="900" alt="Tres paneles a lo largo de una hora con el caudal en la salida, la profundidad del agua en el canal y la profundidad del agua subterránea en la ladera. Valores observados con su incertidumbre como barras de error, el modelo actual como línea naranja discontinua y la mejor simulación como línea azul. Los títulos dan el ajuste antes y después de la calibración" />
</p>

<p align="center">
  <em>Figura 1. Una calibración corta en Studio sobre la cuenca gemela, con incertidumbre en las observaciones. El caudal se evalúa con error / incertidumbre. Con el modelo actual, el 46 % de los puntos estaba dentro de su error de medición, y el 92 % después de la calibración.</em>
</p>

Un experimento gemelo no es una prueba de campo. Muestra que estas observaciones pueden identificar estos parámetros con esta estructura del modelo. Los registros reales añaden error de medición, regulación y procesos que el modelo no incluye.

---

## 7. Límites actuales {#7-current-limits}

- Las observaciones puntuales (profundidades, niveles, pozos) todavía no se registran en mallas de Voronoi y quadtree.
- La humedad del suelo todavía no se puede calibrar. Su tabla se muestra, pero el modelo informa el almacenamiento de las capas, no el contenido de agua.
- Los tiempos son minutos desde el inicio de la simulación; no se leen fechas del calendario.
- Los mapas de extensión de la inundación no son un tipo de objetivo.
- Studio calibra un solo evento. El motor de calibración también acepta varios eventos y eventos de validación, que se ejecutan solo para el mejor candidato.
- La puntuación es una única suma ponderada; no hay un frente de Pareto entre tipos de observación.

---

## Fuentes {#sources}

- Gupta, H. V., Kling, H., Yilmaz, K. K., and Martinez, G. F. (2009). Decomposition of the mean squared error and NSE performance criteria: implications for improving hydrological modelling. *Journal of Hydrology*, 377(1–2), 80–91. [doi:10.1016/j.jhydrol.2009.08.003](https://doi.org/10.1016/j.jhydrol.2009.08.003)
- McKay, M. D., Beckman, R. J., and Conover, W. J. (1979). A comparison of three methods for selecting values of input variables in the analysis of output from a computer code. *Technometrics*, 21(2), 239–245. [doi:10.2307/1268522](https://doi.org/10.2307/1268522)
- Nash, J. E., and Sutcliffe, J. V. (1970). River flow forecasting through conceptual models, part I: a discussion of principles. *Journal of Hydrology*, 10(3), 282–290. [doi:10.1016/0022-1694(70)90255-6](https://doi.org/10.1016/0022-1694(70)90255-6)
