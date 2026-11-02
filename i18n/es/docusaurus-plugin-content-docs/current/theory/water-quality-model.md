---
title: Modelo de Calidad del Agua
---
import useBaseUrl from '@docusaurus/useBaseUrl';

# Modelo de Calidad del Agua

## 1. Descripción general

HydroPol2D simula el transporte de contaminantes utilizando una **formulación de acumulación y lavado** acoplada al modelo hidrodinámico.
El modelo rastrea:
- masa contaminante almacenada en la superficie,
- eliminación de contaminantes debido al flujo (lavado),
- redistribución entre células vecinas,
- exportar a través de fronteras de salida.

<p align="center">
  <img src={useBaseUrl('/img/theory/water-quality.es.svg')} width="720" alt="Tres paneles. 1: la curva de acumulación, que sube hacia el máximo C1 durante los días secos antecedentes y baja por el lavado durante la tormenta. 2: una celda cuya masa de contaminante sale con el agua por cada cara de salida. 3: una malla de celdas sombreadas según la masa de contaminante, con flujos que llevan la masa hasta la salida, junto al balance de masa y las ecuaciones de concentración" />
</p>

<p align="center">
  <em>Figura 1. Los tres pasos del modelo de calidad del agua basado en masa. La acumulación en tiempo seco fija la masa inicial, el lavado la saca de cada celda por las caras por donde sale el agua, y el transporte la lleva de celda en celda hasta la salida.</em>
</p>

La variable gobernante es:
$$
B_t
$$
dónde:
- $B_t$ = masa de contaminante por celda $[\mathrm{M}]$

El modelo es totalmente **conservador de masas** y está acoplado dinámicamente al enrutamiento de flujo.
La validación actual se centra en el modo de lavado masivo
(`flag_wq_model = 0`). La validación utiliza escalas de parámetros de acumulación de estilo SWMM.
para sólidos suspendidos totales, pero la fuente verdadera es un balance de masa analítico
solución en lugar de un análisis numérico SWMM o un polutógrafo de campo calibrado.

---

## 2. Almacenamiento de contaminantes

Cada celda almacena una masa contaminante:
$$
B_t \quad [\mathrm{kg}]
$$
La concentración regional correspondiente es:
$$
b = \frac{B_t}{A_{\mathrm{cell}}}
\quad [\mathrm{M}\,\mathrm{L}^{-2}]
$$
dónde:
- $A_{\mathrm{cell}}$ = área de celda $[\mathrm{L}^2]$

Se definen umbrales mínimos y máximos:
- $B_{\min}$ → masa mínima de contaminante activo
- $B_{\max}$ → límite de saturación

Por debajo de un umbral:
$$
b < b_{\min}
\Rightarrow \text{no wash-off}
$$
---

## 3. Acoplamiento hidrodinámico

El modelo de calidad del agua usa el caudal $Q$ $[\mathrm{L}^3\,\mathrm{T}^{-1}]$, en $\mathrm{m^3/s}$, que sale de una celda por cada cara en el paso de tránsito. Python toma $Q$ directamente de los caudales en las caras calculados por el solver de tránsito.

MATLAB guarda los caudales de salida de una celda de la malla regular como tasas de lámina sobre el área de la celda
$$
q_{\mathrm{out}} = \{ q_{\mathrm{left}}, q_{\mathrm{right}}, q_{\mathrm{up}}, q_{\mathrm{down}}, q_{\mathrm{outlet}} \}
$$
con unidades
$$
[\mathrm{L}\,\mathrm{T}^{-1}] \quad (\mathrm{mm/h})
$$
y convierte cada una en caudal antes de calcular el lavado
$$
Q = \frac{q_{\mathrm{out}}}{1000 \cdot 3600} \cdot A_{\mathrm{cell}}
\quad [\mathrm{L}^3\,\mathrm{T}^{-1}]
$$
---

## 4. Formulación lavable

Se implementan dos formulaciones de lavado.

---

### 4.1 Modelo de lavado de curva de clasificación

Este modo existe solo en MATLAB, y solo en la malla regular, ya que una simulación de MATLAB en malla no estructurada lo rechaza. Python tiene solo el modo basado en masa de la sección 4.2.

Cuando `flag_wq_model = 1`, el lavado es:
$$
W_{\mathrm{out}} =
C_3 \, Q^{C_4} \, f(B_t)
$$
dónde:
- $W_{\mathrm{out}}$ = flujo de masa de contaminantes $[\mathrm{M}\,\mathrm{T}^{-1}]$
- $C_3, C_4$ = coeficientes empíricos
- $Q$ = caudal $[\mathrm{L}^3\,\mathrm{T}^{-1}]$

El factor de corrección de almacenamiento es:
$$
f(B_t) = 1 + \max(B_t - B_r, 0)
$$
dónde:
- $B_r$ = umbral de masa de contaminante residual $[\mathrm{M}]$

Esta formulación asegura que:
- el lavado aumenta con el flujo,
- El lavado aumenta con la masa contaminante disponible.

---

### 4.2 Modelo de lavado basado en masa

Cuando `flag_wq_model = 0`, la formulación pasa a ser:
$$
W_{\mathrm{out}} =
C_3 \, Q^{C_4} \, B_t
$$
Esta formulación supone:
- el lavado es proporcional a la masa contaminante disponible,
- El transporte aumenta con la magnitud del flujo.

---

## 5. Flujos direccionales de contaminantes

Los flujos de contaminantes se calculan para cada dirección por la que el agua sale de la celda. En la malla regular, las direcciones son
- izquierda
- derecha
- arriba
- abajo
- salida

MATLAB trata la salida como una quinta dirección de las celdas de salida. Python lleva el caudal de salida por las caras del borde de la malla, de modo que allí el flujo en la salida es el flujo por una cara de contorno. En una malla de Voronoi o quadtree, ambos códigos usan cada arista por la que el agua sale de la celda, y una arista en el contorno del dominio exporta el contaminante fuera del modelo.

La salida total de contaminantes de una celda es:
$$
W_{\mathrm{out,tot}} = \sum_k W_{\mathrm{out},k}
$$
Los flujos de contaminantes entrantes se calculan a partir de celdas vecinas:
$$
W_{\mathrm{in}} = \sum_k W_{\mathrm{in},k}
$$
---

## 6. Balance neto de contaminantes

La tasa neta de contaminantes es:
$$
dW = W_{\mathrm{out,tot}} - W_{\mathrm{in}}
\quad [\mathrm{M}\,\mathrm{T}^{-1}]
$$
La ecuación del balance de masa es:
$$
B_t^{t+\Delta t}
=
B_t^t - dW \cdot \Delta t
$$
Esta formulación representa:
- eliminación de contaminantes mediante lavado,
- Redistribución de contaminantes a través de la red.

---

## 7. Pasos de tiempo adaptativos (característica crítica)

Para garantizar la estabilidad y evitar la masa negativa, HydroPol2D divide el paso de tiempo hidráulico en $n$ **subpasos** iguales:
$$
n = \max\!\left(1,\;\left\lceil \Delta t \,\max\!\left(\frac{W_{\mathrm{out,tot}}}{B_t}\right) \right\rceil\right)
\qquad
\Delta t_i = \frac{\Delta t}{n}
$$
dónde:
- el máximo se toma sobre las celdas que contienen contaminante ($B_t > 0$),
- $W_{\mathrm{out,tot}}/B_t$ es la tasa bruta de salida de una celda al inicio del paso, sin el flujo de entrada $[\mathrm{T}^{-1}]$,
- $\lceil\cdot\rceil$ redondea al entero siguiente.

En cada subpaso el lavado se calcula de nuevo a partir de la masa actual. Una celda cuya salida retiraría más de lo que contiene tiene sus salidas reducidas en la proporción necesaria para que $W_{\mathrm{out,tot}}\,\Delta t_i \le B_t$. La masa se actualiza entonces:
$$
B_t^{i+1} = B_t^i - dW \cdot \Delta t_i
$$
Python y MATLAB usan este mismo esquema. Los subpasos ocurren dentro del paso hidráulico, de modo que el modelo de calidad del agua no acorta el paso de tiempo del modelo.
Esto asegura:
- sin masa contaminante negativa,
- estabilidad numérica,
- conservación de masa precisa.

---

## 8. Conservación masiva y correcciones

Después de la actualización:
- Se eliminan los valores negativos:

$$
B_t = \max(B_t, 0)
$$
- Se aplica redondeo para evitar el ruido numérico.

Se realiza un seguimiento de la masa perdida debido a correcciones numéricas:
$$
\mathrm{mass}_{\mathrm{lost}}
$$
---

## 9. Concentración de contaminantes

La concentración de contaminantes se calcula como:
$$
C =
1000 \cdot \frac{W_{\mathrm{out,tot}}}{Q_{\mathrm{tot}}}
\quad [\mathrm{mg/L}]
$$
dónde:
- $W_{\mathrm{out,tot}}$ = salida total de contaminante de la celda $[\mathrm{kg\,s^{-1}}]$
- $Q_{\mathrm{tot}}$ = caudal total de agua que sale de la celda $[\mathrm{m^3\,s^{-1}}]$
- el factor 1000 convierte $\mathrm{kg\,m^{-3}}$ en $\mathrm{mg/L}$

Python calcula $C$ de esta forma y fija $C = 0$ en una celda de la que no sale agua. En la malla regular, MATLAB calcula la misma razón a partir de las tasas de lámina de la sección 3, como $C = 10^6\, W_{\mathrm{out,tot}} / (q_{\mathrm{out,tot}}\, A_{\mathrm{cell}})$, con $W_{\mathrm{out,tot}}$ en kg/h, la tasa total de salida $q_{\mathrm{out,tot}}$ en mm/h y $A_{\mathrm{cell}}$ en m². Usa como mínimo 10 mm/h para $q_{\mathrm{out,tot}}$ (sección 12).

---

## 10. Concentración de salida

La concentración de salida se calcula como:
$$
C_{\mathrm{out}} =
1000 \cdot
\frac{
\sum W_{\mathrm{out, outlet}}
}{
\sum Q_{\mathrm{outlet}}
}
\quad [\mathrm{mg/L}]
$$
donde las sumas recorren las caras por las que el agua sale del dominio, $W_{\mathrm{out,outlet}}$ es el flujo de contaminante por una de esas caras, promediado en el paso de tiempo $[\mathrm{kg\,s^{-1}}]$, y $Q_{\mathrm{outlet}}$ es el caudal de agua por ella $[\mathrm{m^3\,s^{-1}}]$. En la malla regular, MATLAB calcula la misma razón como la masa de contaminante que llega a la salida en el paso de tiempo, en kg, dividida por el volumen de agua de la salida en el paso, en litros, por $10^6$.
---

## 11. Masa total lavada

La masa contaminante lavada acumulada es:
$$
M_{\mathrm{washed}} =
\sum W_{\mathrm{out,tot}} \cdot \Delta t
\quad [\mathrm{kg}]
$$
---

## 12. Restricciones numéricas

El modelo impone:
- umbral mínimo de contaminantes:

$$
b < b_{\min} \Rightarrow W_{\mathrm{out}} = 0
$$
- un caudal mínimo para la concentración en la celda, solo en MATLAB y solo en la malla regular:

$$
q_{\mathrm{out,tot}} \ge 10 \quad [\mathrm{mm/h}]
$$
MATLAB aplica este mínimo solo a la tasa total de salida en el denominador de la concentración en la celda de la sección 9, para que una celda con muy poca salida no muestre una concentración muy alta. No altera el lavado, el balance de masa ni la concentración en la salida. Python no tiene este mínimo, y sus celdas de las que no sale agua tienen $C = 0$.

---

## Resumen

El modelo de calidad del agua HydroPol2D:
- rastrea la masa contaminante por celda,
- calcula el lavado en función del flujo y el almacenamiento,
- redistribuye los contaminantes en todo el dominio,
- garantiza una estricta conservación masiva,
- utiliza pasos de tiempo adaptativos para mantener la estabilidad.

Proporciona un marco robusto y flexible para simular el transporte de contaminantes junto con procesos hidrológicos e hidrodinámicos. La evidencia de validación actual respalda el comportamiento controlado del equilibrio de masas de acumulación/eliminación; La predicción de contaminantes específicos del sitio aún requiere parámetros, observaciones y calibración de contaminantes locales.