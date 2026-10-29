---
title: Inestabilidad humana
---

# Inestabilidad humana

HydroPol2D incluye un módulo de inestabilidad humana implementado que utiliza la profundidad y la velocidad de la superficie enrutada para estimar el peligro para los peatones. La teoría pública actual debería distinguir claramente entre los modos implementados:
| Modo | Estado actual | Descripción |
|---|---|---|
| `1` | Implementado | Relación de riesgo de equilibrio de fuerza continua basada en la flotabilidad, la fricción disponible y la resistencia hidrodinámica. |
| `2` | No implementado | Sólo marcador de posición. No documentar ni utilizar como opción pública activa. |
| `3` | Implementado | Clasificador de inestabilidad basado en geometría con umbrales de deslizamiento, caída y ahogamiento/dibujo. |

El estado de validación actual para estos modos se rastrea en el [estado de validación](../validation/validation-status).

---

## 1. Entradas y Acoplamiento

El módulo de inestabilidad humana lee el estado hidrodinámico de HydroPol2D:
- profundidad de la superficie enrutada $h$,
- magnitud de velocidad enrutada $v$,
- pendiente local cuando se utiliza el clasificador basado en geometría,
- y parámetros de resistencia y geometría humana proporcionados por el usuario.

Esto significa que las estimaciones de inestabilidad son productos de diagnóstico de la simulación hidrológica-hidrodinámica acoplada en lugar de un solucionador hidráulico independiente.

---

## 2. Modo 1: Relación de riesgo fuerza-equilibrio

El modo `1` representa la inestabilidad como una competencia entre el forzamiento hidrodinámico y el soporte de fricción que queda después de que la flotabilidad reduce el peso corporal.
### 2.1 Peso y flotabilidad

La fuerza del peso corporal es
$$
F_{\mathrm{person}} = m_{\mathrm{person}} g
$$
La fuerza de flotación se aproxima como
$$
F_ {\mathrm{buoy}}
=
w_1 w_2 h \rho_{\mathrm{w}} g
$$
dónde:
- $m_{\mathrm{person}}$ es la masa corporal
- $g$ es la aceleración gravitacional
- $w_1$ y $w_2$ son anchos de cuerpo característicos
- $h$ es la profundidad del agua
- $\rho_{\mathrm{w}}$ es la densidad del agua

### 2.2 Fricción disponible

La fricción disponible para resistir el movimiento es
$$
F_{\mathrm{fric}}
=
\mu \max\!\left(
F_{\mathrm{person}} - F_{\mathrm{buoy}},
0
\right)
$$
donde $\mu$ es el coeficiente de fricción efectivo de contacto con el suelo.
### 2.3 fuerza hidrodinámica

La carga hidrodinámica se representa como
$$
F_{\mathrm{hyd}}
=
\max\!\left(
\frac{1}{2} C_d \rho_{\mathrm{w}} w_1 h v^2,
0
\right)
$$
dónde:
- $C_d$ es el coeficiente de arrastre
- $v$ es la magnitud de la velocidad enrutada

### 2.4 Ratio de riesgo

La relación de riesgo fuerza-equilibrio es entonces
$$
R
=
\frac{F_{\mathrm{hyd}}}{F_{\mathrm{fric}}}
$$
para estados admitidos donde $F_{\mathrm{fric}} > 0$. En la implementación actual:
- a las celdas sin soporte restante pero con una profundidad de agua positiva se les asigna el riesgo total,
- el valor de riesgo final se recorta al rango $0 \le R \le 1$,
- y se puede acumular un mapa de riesgo máximo en ejecución durante la simulación.

Por lo tanto, el modo `1` devuelve un indicador de peligro continuo en lugar de un modo de falla categórico.

---

## 3. Modo 3: Clasificador de inestabilidad basado en geometría

El modo `3` utiliza la geometría de la persona, la profundidad del flujo, la velocidad del flujo y la pendiente del terreno para clasificar el mecanismo de falla dominante.
### 3.1 Geometría sumergida y fuerzas.

El código calcula el área sumergida, el volumen sumergido y el centroide sumergido en función de la profundidad del agua en relación con las dimensiones del cuerpo. Luego, esas cantidades geométricas se utilizan para estimar:
- carga hidrodinámica tipo arrastre y elevación,
- componentes descendentes y normales del peso corporal,
- flotabilidad,
- y los brazos de palanca necesarios para el vuelco.

Conceptualmente, los principales términos de fuerza son:
$$
D \propto \frac{1}{2}\rho_{\mathrm{w}} C_d v^2 A_{\mathrm{sub}}
$$
$$
W_p = m g \sin\beta
\qquad
W_n = m g \cos\beta
$$
$$
B_n = \rho_{\mathrm{w}} g V_{\mathrm{sub}} \cos\beta
$$
dónde:
- $A_{\mathrm{sub}}$ es el área proyectada sumergida
- $V_{\mathrm{sub}}$ es el volumen sumergido
- $\beta$ es el ángulo de pendiente local

### 3.2 Umbral deslizante

La fricción resistente disponible se aproxima como
$$
T = \mu \left(W_n - B_n - L\right)
$$
donde $L$ es la contribución hidrodinámica del tipo de sustentación. El deslizamiento se clasifica cuando la fuerza motriz excede la fricción disponible:
$$
\text{slide if } D + W_p > T
$$
En el mapa de salida, la diapositiva corresponde al código `1`.
### 3.3 Umbral de derrumbe

El módulo también calcula un momento de vuelco a partir de la resistencia, la flotabilidad y la geometría del cuerpo. El vuelco se clasifica cuando el momento motriz supera al momento resistente:
$$
\text{topple if } M > M_{\mathrm{res}}
$$
En el mapa de salida, la caída corresponde al código `2`.
### 3.4 Umbral de ahogamiento/embarazo

La implementación también aplica un umbral de ahogamiento/ahogamiento basado en la profundidad:
$$
\text{drowning/drawing if } h > \frac{13}{16} y
$$
donde $y$ es la altura corporal característica utilizada por la rutina de geometría. En el mapa de salida, este modo de falla corresponde al código `3`.
### 3.5 Mapa categórico final

La clase de peligro final del modo `3` es el máximo de los indicadores de deslizamiento, caída y ahogamiento/extracción:
$$
\text{risk class} = \max(\text{slide},\text{topple},\text{drowning/drawing})
$$
Esto produce un ráster de inestabilidad categórica en lugar de la relación continua devuelta por el modo `1`.

Una celda seca ($h = 0$) es estable (código `0`), como en el modo `1`: sin agua, no hay nadie en el flujo que clasificar. Sin esta regla, el propio peso de la persona haría de toda celda seca con pendiente mayor que $\arctan\mu$ (31° para $\mu = 0{,}6$) un deslizamiento.

---

## 4. Notas de alcance y documentación

La historia pública actual sobre la inestabilidad humana debería mantenerse alineada con el código:
- El modo `1` se implementa y documenta como una relación fuerza-equilibrio,
- el modo `3` está implementado y documentado como un clasificador basado en geometría,
- el modo `2` no está implementado,
- las afirmaciones de validación deben permanecer vinculadas a la evidencia controlada resumida en el [estado de validación](../validation/validation-status),
- y el módulo de inestabilidad humana debe describirse como un diagnóstico de peligro acoplado impulsado por profundidades y velocidades HydroPol2D.
