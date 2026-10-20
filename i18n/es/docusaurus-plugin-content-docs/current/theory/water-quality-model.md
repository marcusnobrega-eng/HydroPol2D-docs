---
title: Modelo de Calidad del Agua
---

# Modelo de Calidad del Agua

## 1. Descripción general

HydroPol2D simula el transporte de contaminantes utilizando una **formulación de acumulación y lavado** acoplada al modelo hidrodinámico.
El modelo rastrea:
- masa contaminante almacenada en la superficie,
- eliminación de contaminantes debido al flujo (lavado),
- redistribución entre células vecinas,
- exportar a través de fronteras de salida.

La variable gobernante es:
$$
b_t
$$
dónde:
- $B_t$ = masa de contaminante por celda $[\mathrm{M}]$

El modelo es totalmente **conservador de masas** y está acoplado dinámicamente al enrutamiento de flujo.
La validación actual de la validación se centra en el modo de lavado masivo
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
\Flecha derecha \text{no wash-off}
$$
---

## 3. Acoplamiento hidrodinámico

El modelo de calidad del agua utiliza flujos de salida hidrodinámicos:
$$
q_{\mathrm{out}} = \{ q_{\mathrm{left}}, q_{\mathrm{right}}, q_{\mathrm{up}}, q_{\mathrm{down}}, q_{\mathrm{outlet}} \}
$$
con unidades:
$$
[\mathrm{L}\,\mathrm{T}^{-1}] \quad (\mathrm{mm/h})
$$
Estos se convierten internamente a flujo volumétrico:
$$
Q = \frac{q_{\mathrm{out}}}{1000 \cdot 3600} \cdot A_{\mathrm{cell}}
\quad [\mathrm{L}^3\,\mathrm{T}^{-1}]
$$
---

## 4. Formulación lavable

Se implementan dos formulaciones de lavado.
---

### 4.1 Modelo de lavado de curva de clasificación

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

Los flujos de contaminantes se calculan para cada dirección:
- izquierda
- bien
- arriba
- abajo
- salida

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

Para garantizar la estabilidad y evitar la masa negativa, HydroPol2D calcula un **paso de tiempo mínimo permitido**:
$$
\Delta t_{\min}
=
\min\izquierda(\frac{B_t}{|dw|}
\derecha)
$$
dónde:
- sólo se consideran las células que pierden masa,
- Se excluyen los valores muy pequeños.

Si:
$$
\Delta t_{\min} < \Delta t
$$
el modelo divide el paso de tiempo en subpasos:
$$
\Delta t = \sum \Delta t_i
$$
y actualiza la masa contaminante de forma iterativa:
$$
B_t^{i+1} = B_t^i - dW \cdot \Delta t_i
$$
Esto asegura:
- sin masa contaminante negativa,
- estabilidad numérica,
- conservación de masa precisa.

---

## 8. Conservación masiva y correcciones

Después de la actualización:
- Se eliminan los valores negativos:

$$
Bt = \max(Bt, 0)
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
\frac{W_{\mathrm{out,tot}}}{Q_{\mathrm{tot}} \cdot A_{\mathrm{cell}}}
\cdot 10^6
\quad [\mathrm{mg/L}]
$$
dónde:
- $Q_{\mathrm{tot}}$ = salida total de agua $[\mathrm{L}\,\mathrm{T}^{-1}]$

---

## 10. Concentración de salida

La concentración de salida se calcula como:
$$
C_{\mathrm{out}} =
\frac{
\sum W_{\mathrm{out, outlet}}
{}
\sum Q_{\mathrm{outlet}} \cdot A_{\mathrm{cell}}
}
\cdot 1000
\quad [\mathrm{mg/L}]
$$
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
- umbral de flujo mínimo:

$$
q_{\mathrm{out}} \ge 10 \quad [\mathrm{mm/h}]
$$
para evitar la inestabilidad numérica.
---

## Resumen

El modelo de calidad del agua HydroPol2D:
- rastrea la masa contaminante por celda,
- calcula el lavado en función del flujo y el almacenamiento,
- redistribuye los contaminantes en todo el dominio,
- garantiza una estricta conservación masiva,
- utiliza pasos de tiempo adaptativos para mantener la estabilidad.

Proporciona un marco robusto y flexible para simular el transporte de contaminantes junto con procesos hidrológicos e hidrodinámicos. La evidencia de validación actual respalda el comportamiento controlado del equilibrio de masas de acumulación/eliminación; La predicción de contaminantes específicos del sitio aún requiere parámetros, observaciones y calibración de contaminantes locales.