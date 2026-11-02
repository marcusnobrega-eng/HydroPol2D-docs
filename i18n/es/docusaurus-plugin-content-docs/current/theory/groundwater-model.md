---
title: Modelo de aguas subterráneas
---
import useBaseUrl from '@docusaurus/useBaseUrl';

# Modelo de aguas subterráneas

## 1. Descripción general

El componente de agua subterránea de HydroPol2D representa la dinámica acoplada de:
- almacenamiento en zona vadosa,
- recargar de la infiltración,
- flujo lateral de agua subterránea saturada,
- exfiltración de agua subterránea a la superficie,
- y la interacción del agua subterránea con las células de los ríos.

La implementación actual combina tres componentes complementarios:
1. un **módulo vadosa/recarga en capas**, que mueve agua a través de un almacenamiento cercano a la superficie, en la zona de raíces y en la zona de transmisión utilizando un cierre Darcy reducido consistente con Richards basado en las relaciones constitutivas de van Genuchten-Mualem,

2. un **módulo de intercambio de elevación capilar**, que puede mover agua hacia arriba desde aguas subterráneas poco profundas hasta un almacenamiento vadoso disponible, y

3. un **solucionador de flujo de agua subterránea Boussinesq bidimensional**, que dirige el flujo saturado lateralmente a través del dominio y devuelve la exfiltración a la superficie terrestre cuando el nivel freático se eleva por encima de la elevación de la superficie local.

Esta estructura permite que HydroPol2D represente el acoplamiento dinámico entre:
- aguas superficiales,
- almacenamiento vadoso,
- recarga de aguas subterráneas,
- flujo de agua subterránea saturada,
- y flujo de retorno de exceso de saturación.


<p align="center">
  <img src={useBaseUrl('/img/theory/groundwater-model.es.svg')} width="720" alt="Tres celdas escalonadas de la ladera al río, con capas de suelo, nivel freático, flujo lateral, exfiltración, intercambio con el río y acuífero profundo" />
</p>
<p align="center">
  <em>Figura 1. El esquema predeterminado de agua subterránea en tres celdas. La recarga y el ascenso capilar mueven el nivel freático h en cada paso superficial. El flujo lateral de Boussinesq sigue el reloj del agua subterránea. La exfiltración y el exceso de saturación devuelven agua donde h alcanza el terreno.</em>
</p>

### 1.1 Dos esquemas de subsuelo {#11-two-subsurface-schemes}

HydroPol2D tiene dos esquemas de subsuelo. Esta página describe el esquema predeterminado.

| Esquema | Acuífero | Activación | Página |
|---|---|---|---|
| Predeterminado | Dentro de la columna de suelo; la base del acuífero es el terreno menos la profundidad del suelo | predeterminado | esta página |
| En capas | Capas de suelo sobre capas de regolito, hasta la profundidad hasta el lecho de roca (limitada a 50 m) | Python `vertical.subsurface.scheme: layered`; MATLAB `flag_layered_subsurface = 1` | [Subsuelo en Capas](./layered-subsurface) |

Ambos esquemas pueden alimentar el acuífero profundo opcional descrito en la [sección 13](#13-deep-aquifer).

En esta página, "zona vadosa en capas" se refiere a los tres almacenamientos de suelo del esquema predeterminado (cerca de la superficie, zona de raíces y transmisión). No se refiere al esquema de subsuelo en capas.

---

## 2. Estructura conceptual general

El modelo de aguas subterráneas está acoplado a dos relojes. El intercambio de la zona vadosa se evalúa en cada paso de tiempo del agua superficial porque la infiltración y la evapotranspiración necesitan una rápida retroalimentación de la humedad del suelo. Este intercambio neto cambia las cargas del nivel freático en cada paso del agua superficial. El programador de aguas subterráneas es siempre asíncrono, y solo el flujo lateral de agua subterránea, cuando está activo, lo espera. La actualización lateral suele seguir un intervalo objetivo diario, a menos que los límites de estabilidad o de cambio de carga exijan un intervalo más corto.
La lógica es:
1. calcular la posición del nivel freático a partir de la altura actual del agua subterránea,
2. determinar el almacenamiento no saturado máximo permitido por la profundidad actual del nivel freático,
3. calcular el drenaje/recarga desde las capas vadosas al agua subterránea durante el paso superficial actual,
4. calcular el ascenso capilar desde el agua subterránea hasta las capas vadosas cuando esté habilitado,
5. cambiar las cargas del nivel freático con el intercambio neto en cada paso del agua superficial,
6. calcular la exfiltración de agua subterránea a la superficie donde la carga supera la superficie del terreno,
7. resolver el flujo lateral de agua subterránea usando una ecuación 2D Boussinesq cuando el flujo lateral está activo (`flag_baseflow = 1` en MATLAB, `vertical.groundwater_lateral_flow: true` en HydroPol2D-Python) y el programador indica que corresponde,
8. sumar a la superficie la exfiltración de la actualización lateral,
9. almacenamiento vadoso correcto si el aumento del nivel freático reduce el almacenamiento insaturado disponible,
10. actualice la profundidad del agua superficial en consecuencia.

Las principales variables son:
- $h$ = altura hidráulica del agua subterránea $[\mathrm{L}]$
- $z_0$ = elevación de la base del acuífero o elevación del lecho rocoso $[\mathrm{L}]$
- $H = h - z_0$ = espesor saturado $[\mathrm{L}]$
- $R$ = tasa de recarga al agua subterránea $[\mathrm{L}\,\mathrm{T}^{-1}]$
- $q_{\mathrm{exf}}$ = flujo de exfiltración desde el agua subterránea a la superficie $[\mathrm{L}\,\mathrm{T}^{-1}]$
- $S_y$ = rendimiento específico $[-]$
- $K$ = conductividad hidráulica saturada $[\mathrm{L}\,\mathrm{T}^{-1}]$

### 2.1 Programador asincrónico {#21-asynchronous-scheduler}

El programador asincrónico está siempre activo cuando el modelado de aguas subterráneas está habilitado. Solo decide cuándo se ejecuta la actualización lateral de Boussinesq. Los principales controles son:
| Control | Por defecto | Significado |
|---|---:|---|
| `flag_groundwater_async` | 1 | No se lee: la actualización lateral siempre sigue al programador (Sección 7.1). |
| `groundwater_target_dt_s` | 86400 | Intervalo máximo entre actualizaciones laterales, en segundos (un día). HydroPol2D-Python también lo lee de un libro antiguo en minutos, como `groundwater_target_dt_min` (1440). |
| `groundwater_min_dt_s` | 60 | Intervalo mínimo entre actualizaciones laterales y subpaso más corto de Boussinesq, en segundos. En el libro antiguo la clave es `groundwater_min_dt_min` (1). |
| `groundwater_max_head_change_m` | 0,25 | HydroPol2D-Python: fuerza una actualización lateral cuando el nivel freático se ha movido esta cantidad desde la última. El esquema predeterminado de MATLAB no lo usa (Sección 7.1). |
| `groundwater_head_tolerance_m` | 0,001 | Tolerancia absoluta de carga de los subpasos adaptativos de Boussinesq, en metros. MATLAB también la usa en el disparador por cambio de carga. |
| `groundwater_relative_tolerance` | 0,001 | Tolerancia relativa sobre el espesor saturado, usada junto con `groundwater_head_tolerance_m`. |
| `groundwater_courant` | 0,25 | Factor de estabilidad para la estimación del paso de tiempo del agua subterránea Boussinesq. |
| `flag_capillary_rise` | 1 | Activa el ascenso capilar desde el nivel freático hacia la zona de raíces cuando hay almacenamiento de suelo en capas. |

En HydroPol2D-Python estos parámetros están en el bloque `vertical`, y el ascenso capilar es `vertical.capillary_rise` (true por defecto).

El programador guarda el tiempo desde la última actualización lateral, el subpaso sugerido por la última ejecución adaptativa de Boussinesq, el número de actualizaciones laterales y tres láminas por celda. El intercambio neto pendiente guarda solo el intercambio del paso actual. La actualización local lo suma a las cargas y lo pone a cero en el mismo paso. La recarga pendiente y el ascenso capilar pendiente son totales acumulados desde la última actualización lateral y se ponen a cero cuando esa actualización se ejecuta. Para el disparador por cambio de carga, HydroPol2D-Python también guarda el cambio de carga aplicado desde la última actualización lateral, y el código MATLAB guarda la carga de esa actualización. El solucionador de Boussinesq no recibe término de recarga, porque las cargas ya incluyen el intercambio neto. Sin flujo lateral, el programador solo pone a cero estos totales, en cada paso en MATLAB y cuando se cumple el disparador en HydroPol2D-Python.

---

## 3. Posición del nivel freático y capacidad de la zona no saturada

HydroPol2D determina la posición del nivel freático en relación con la superficie terrestre utilizando la cabeza freática actual.
Dejar:
- $z_{\mathrm{surf}}$ = elevación de la superficie terrestre $[\mathrm{L}]$
- $D_{\mathrm{soil}}$ = profundidad del suelo $[\mathrm{L}]$
- $h$ = altura hidráulica del agua subterránea $[\mathrm{L}]$

El espesor saturado sobre el lecho de roca se calcula como
$$
z_{\mathrm{gw}}
=
h - \left(z_{\mathrm{surf}} - D_{\mathrm{soil}}\right)
$$
La profundidad desde la superficie terrestre hasta el nivel freático es entonces
$$
z_{\mathrm{wt}}
=
D_{\mathrm{soil}} - z_{\mathrm{gw}}
$$
con la restricción
$$
z_{\mathrm{wt}} \ge 0
$$
dónde:
- $z_{\mathrm{gw}}$ = espesor saturado medido hacia arriba desde la base del acuífero $[\mathrm{L}]$
- $z_{\mathrm{wt}}$ = profundidad del nivel freático debajo de la superficie del suelo $[\mathrm{L}]$

Esta variable es fundamental para el acoplamiento entre el almacenamiento vadoso y el agua subterránea.
### 3.1 Almacenamiento máximo insaturado

El agua máxima que se puede almacenar en la zona no saturada se define utilizando la convención actual de **almacenamiento activo por encima del contenido de agua residual**:
$$
S_{\mathrm{UZ,max}}
=
z_{\mathrm{wt}}
\left(
\theta_{\mathrm{sat}} - \theta_r
\right)
$$
dónde:
- $S_{\mathrm{UZ,max}}$ = almacenamiento máximo no saturado $[\mathrm{L}]$
- $\theta_{\mathrm{sat}}$ = contenido volumétrico de agua saturada $[-]$
- $\theta_r$ = contenido volumétrico de agua residual $[-]$

Por lo tanto, a medida que aumenta el nivel freático, la zona vadosa se reduce y la capacidad de almacenamiento disponible para la infiltración disminuye. Cuando el almacenamiento de suelo en capas está activo, el código evalúa este límite a través de las capacidades explícitas de los almacenes cerca de la superficie, la zona de las raíces y la zona de transmisión después del truncamiento por la posición actual del nivel freático.

---

## 4. Intercambio predeterminado de vadosa a agua subterránea en capas

La recarga se calcula a partir del almacenamiento vadoso actual después de que el módulo de infiltración ya haya movido el agua de la superficie al suelo. Esto evita la infiltración por duplicado. La ruta predeterminada actual está en capas:
- almacenamiento cerca de la superficie,
- almacenamiento en la zona raíz,
- almacenamiento en zona de transmisión,
- recarga de aguas subterráneas.

### 4.1 Acoplamiento superficie-escalón

El intercambio de dosis se evalúa en cada paso del agua superficial porque la infiltración y la evapotranspiración necesitan una retroalimentación inmediata de la humedad del suelo. En la implementación actual, la infiltración es primero aceptada por el módulo de infiltración, almacenada en las capas vadosas y solo después se le permite drenar hacia el agua subterránea.
### 4.2 Estado constitutivo por capas

Para una capa vadosa genérica $\ell$ con almacenamiento activo $S_{\ell}$ y espesor $z_{\ell}$, HydroPol2D evalúa
$$
\theta_{\ell}
=
\theta_{\mathrm{r},\ell}+
\frac{S_{\ell}}{f_p\, z_{\ell}}
$$
$$
S_{e,\ell}
=
\frac{
\theta_{\ell} - \theta_{\mathrm{r},\ell}
}{
\theta_{\mathrm{sat},\ell} - \theta_{\mathrm{r},\ell}
}
$$
$$
K_{\ell}
=
K_{\mathrm{sat},\ell}
S_{e,\ell}^{\ell_v}
\left[
1 - \left(1 - S_{e,\ell}^{1/m_{\ell}}\right)^{m_{\ell}}
\right]^2
$$
con
$$
m_{\ell} = 1 - \frac{1}{n_{\ell}}
$$
dónde:
- $\theta_{\ell}$ = contenido de agua de la capa $[-]$
- $f_p$ = fracción permeable de la celda $[-]$; el agua de la capa ocupa la parte permeable, y $S_{\ell}$ es una lámina sobre toda la celda
- $S_{e,\ell}$ = saturación efectiva de capa $[-]$
- $K_{\ell}$ = conductividad insaturada de la capa $[\mathrm{L}\,\mathrm{T}^{-1}]$
- $\ell_v$ = Parámetro de conectividad de poros de Mualem $[-]$, fijado en 0,5 en este paso de drenaje en ambos códigos

Esta es la misma familia constitutiva de van Genuchten-Mualem utilizada por el módulo de infiltración.
### 4.3 Cascada de drenaje descendente

La ruta de recarga en capas se calcula como una cascada descendente:
1. El drenaje cercano a la superficie va a la zona de las raíces cuando existe almacenamiento de raíces.
2. el drenaje de la zona de la raíz va a la zona de transmisión cuando existe almacenamiento de transmisión,
3. El drenaje de la zona de transmisión se convierte en recarga de aguas subterráneas.

Conceptualmente, la profundidad de drenaje de una capa a lo largo de un paso de tiempo se puede resumir como
$$
\Delta D_{\ell} \approx f_p\,K_{\ell}\,\Delta t
$$
sujeto a:
- agua disponible en la capa donante,
- capacidad restante en la capa receptora,
- y el espesor de capa actual y los parámetros del suelo.

La recarga neta descendente que llega al agua subterránea es entonces
$$
R_ {\mathrm{down}}
=
\frac{\Delta S_{\rightarrow \mathrm{gw}}}{\Delta t}
$$
donde $\Delta S_{\rightarrow \mathrm{gw}}$ es la transmisión total de agua al agua subterránea durante el paso superficial actual. El drenaje directo desde la zona cercana a la superficie o la zona de las raíces hacia el agua subterránea ocurre sólo cuando las capas vadosas inferiores están ausentes.
### 4.4 Formulación alternativa heredada

El código MATLAB todavía contiene el cierre de recarga del depósito representativo anterior para los casos en los que los datos de almacenamiento en capas explícitos no están disponibles. En ese modo de reserva, un único estado de almacenamiento vadoso se convierte en un contenido de agua representativo y se drena con un cierre tipo Darcy. HydroPol2D-Python no tiene esta alternativa y siempre usa las tres capas. Esa formulación debe tratarse como un **legado/refuerzo**, no como el camino teórico principal para el modelo actual.

---

## 5. Aumento capilar opcional

Cuando `flag_capillary_rise = 1`, HydroPol2D permite que el agua subterránea poco profunda se mueva hacia arriba hasta el almacenamiento vadoso disponible. La implementación actual es una transferencia de van Genuchten-Mualem hacia la zona de raíces, limitada por el almacenamiento disponible, no una solución completa de la ecuación de Richards.
El intercambio ascendente aumenta con:
- menor profundidad del nivel freático,
- mayor déficit de almacenamiento en la capa receptora,
- y mayor conductividad saturada de la zona de raíces.

En un paso de superficie $\Delta t$, la transferencia capilar ascendente es
$$
C_{\mathrm{up}}\,\Delta t
=
\min\!\left(
S_{\mathrm{def}},\;
K_{\mathrm{sat,root}}\,K_r(g)\,\Delta t,\;
S_{\mathrm{gw}}
\right)
$$
con $g = \max(z_{\mathrm{wt}} - z_{\mathrm{root}}, 0)$, $S_e(g) = \left[1 + (\alpha g)^{n}\right]^{-m}$ y $K_r(g) = S_e(g)^{\ell_v}\left[1 - \left(1 - S_e(g)^{1/m}\right)^{m}\right]^2$, donde:
- $S_{\mathrm{def}}$ es el déficit de la capa receptora por debajo de la capacidad de campo, $\max\!\left(S_e(h_{\mathrm{fc}})\,S_{\max} - S, 0\right)$, con $S$ y $S_{\max}$ el almacenamiento y la capacidad de esa capa
- $h_{\mathrm{fc}}$ es la succión de capacidad de campo, `capillary_field_capacity_head_m` (3,3 m por defecto)
- $g$ es la distancia entre el nivel freático y la base de la zona de raíces $z_{\mathrm{root}}$
- $S_{\mathrm{gw}} = S_y\,(h - z_0)$ es el agua subterránea almacenada en la celda
- $\alpha$, $n$, $m$ y $\ell_v$ son los parámetros de van Genuchten-Mualem del suelo

En el código actual, el ascenso capilar llena solo la zona de raíces, o la capa cercana a la superficie cuando las raíces terminan dentro de ella y no hay una zona de raíces separada. La zona de transmisión no recibe ascenso capilar.
Por lo tanto, el intercambio neto vadoso-agua subterránea de cada paso del agua superficial es
$$
R_{\mathrm{net}} = R_{\mathrm{down}} - C_{\mathrm{up}}
$$
donde $C_{\mathrm{up}}$ es el flujo total de ascenso capilar ascendente.

---

## 6. Modelo bidimensional de flujo de agua subterránea Boussinesq

Después de la actualización local de la carga, y solo cuando el flujo lateral está activo y el programador indica que corresponde, HydroPol2D encamina el agua subterránea lateralmente utilizando la función `Boussinesq_2D_explicit`. HydroPol2D-Python usa la misma discretización.
Este solucionador representa el sistema de agua subterránea saturada a través de una aproximación de flujo no confinado integrado en profundidad.
### 6.1 Ecuación rectora

El recorrido del agua subterránea sigue la ecuación 2D Boussinesq en forma conservadora:
$$
S_y \frac{\partial h}{\partial t}
=- \nabla \cdot \mathbf{F}
+
R
$$
dónde:
- $S_y$ = rendimiento específico $[-]$
- $h$ = altura hidráulica del agua subterránea $[\mathrm{L}]$
- $\mathbf{F}$ = vector de flujo de agua subterránea $[\mathrm{L}^2\,\mathrm{T}^{-1}]$
- $R$ = tasa de recarga $[\mathrm{L}\,\mathrm{T}^{-1}]$

HydroPol2D evalúa esta ecuación numéricamente calculando los flujos en las interfaces de las celdas y luego actualizando explícitamente la cabeza del agua subterránea. En el código, el término de recarga se aplica por separado. El intercambio neto cambia las cargas en cada paso del agua superficial (Sección 7.1), y el solucionador lateral se llama con $R = 0$ durante el tiempo transcurrido desde su última ejecución.
### 6.2 Espesor saturado

El espesor saturado activo se define como
$$
H = \max(h - z_0, 0)
$$
dónde:
- $H$ = espesor saturado $[\mathrm{L}]$
- $z_0$ = elevación de la base del acuífero o elevación del lecho rocoso $[\mathrm{L}]$

Esto refuerza la condición física de que no existe almacenamiento saturado debajo de la base del acuífero.
### 6.3 Flujos de interfaz

HydroPol2D calcula los flujos de agua subterránea en las interfaces de las celdas utilizando la ley de Darcy con ponderación de espesor saturado.
Para la dirección $x$:
$$
F_x = -K_x H_x \frac{\partial h}{\partial x}
$$
y para la dirección $y$:
$$
F_y = -K_y H_y \frac{\partial h}{\partial y}
$$
dónde:
- $F_x, F_y$ = flujos por unidad de ancho $[\mathrm{L}^2\,\mathrm{T}^{-1}]$
- $K_x, K_y$ = conductividad hidráulica en las interfaces de las celdas $[\mathrm{L}\,\mathrm{T}^{-1}]$
- $H_x, H_y$ = espesores saturados de interfaz $[\mathrm{L}]$

En la implementación, la conductividad hidráulica de la interfaz se toma como la media aritmética de las conductividades en celdas adyacentes:
$$
K_x = \frac{K_i + K_{i+1}}{2}
\qquad
K_y = \frac{K_j + K_{j+1}}{2}
$$
y el espesor saturado de la interfaz también se promedia:
$$
H_x = \frac{H_i + H_{i+1}}{2}
\qquad
H_y = \frac{H_j + H_{j+1}}{2}
$$
### 6.4 Limitación de flujo conservadora

Para evitar la inestabilidad numérica y el agotamiento no físico del almacenamiento de agua subterránea, HydroPol2D aplica un limitador de flujo para que ninguna interfaz pueda transportar más agua de la que contiene su celda donante durante un subpaso.
Por ejemplo, en la dirección $x$, el flujo máximo permitido es
$$
F_{x,\max}
=
\frac{S_y H_{\mathrm{donor}}}{\Delta t}
$$
y el flujo de interfaz final está limitado como
$$
F_x \leftarrow \operatorname{sign}(F_x)\,
\min\left(|F_x|,\,F_{x,\max}\right)
$$

Se utiliza una expresión similar en la dirección $y$.
Como el límite se aplica a cada interfaz por separado, una celda que drena por varias interfaces todavía puede quedar por debajo de la base del acuífero en un subpaso. El solucionador fija entonces la carga en $z_0$, y el agua añadida aparece como residuo en la verificación del balance de masa de la Sección 14.
### 6.5 Divergencia de los flujos de aguas subterráneas

Luego, la divergencia del campo de flujo se calcula a partir de los flujos de la interfaz como
$$
\nabla \cdot \mathbf{F}
=
\frac{\partial F_x}{\partial x}+
\frac{\partial F_y}{\partial y}
$$
utilizando diferencias finitas conservadoras en la cuadrícula ráster.
### 6.6 Actualización explícita del predictor-corrector

El solucionador Boussinesq utiliza una estrategia predictor-corrector explícita.
#### Paso predictivo

Se calcula una primera estimación de la altura utilizando los flujos de corriente:
$$
h^{\ast}
=
h^t + \frac{\Delta t}{S_y}\left(-\nabla \cdot \mathbf{F}^t\right)
$$
#### Paso corrector

Los flujos se vuelven a calcular a partir del estado del predictor, se promedian y se utilizan en la actualización final:
$$
h^{t+\Delta t}
=
h^t
+
\frac{\Delta t}{S_y}
\left(
-\nabla \cdot \mathbf{F}^{\mathrm{avg}} + R
\right)
$$
dónde:
- $h^{\ast}$ = predictor de altura hidráulica $[\mathrm{L}]$
- $h^{t+\Delta t}$ = altura hidráulica final después del paso de tiempo $[\mathrm{L}]$
- $\mathbf{F}^{\mathrm{avg}}$ = promedio de flujos de interfaz predictor y corrector

Este procedimiento predictor-corrector mejora la estabilidad y reduce la difusión numérica en relación con una simple actualización explícita de Euler.

---

## 7. Cronograma de actualización del agua subterránea y paso del tiempo de adaptación

HydroPol2D utiliza una **lógica de paso de tiempo de agua subterránea de dos niveles**.
### 7.1 Programador asíncrono externo

El intercambio de vadosa cambia las cargas del nivel freático en cada paso del agua superficial. El programador de aguas subterráneas es siempre asíncrono, y solo el flujo lateral de agua subterránea, cuando está activo, lo espera. La actualización lateral se ejecuta al final del primer paso de superficie en el que se cumple una de estas condiciones:
- el tiempo desde la última actualización lateral alcanza $\max\!\left(\min(\Delta t_{\mathrm{target}}, \Delta t_{\mathrm{gw,stable}}, \Delta t_{\mathrm{sugg}}), \Delta t_{\min}\right)$, donde $\Delta t_{\mathrm{target}}$ es `groundwater_target_dt_s`, $\Delta t_{\mathrm{gw,stable}}$ es el límite de estabilidad de la Sección 7.2, $\Delta t_{\mathrm{sugg}}$ es el subpaso sugerido por la última ejecución adaptativa de Boussinesq y $\Delta t_{\min}$ es `groundwater_min_dt_s`,
- el nivel freático se ha movido lo suficiente desde la última actualización lateral,
- el paso de superficie es el último de la simulación.

La prueba de cambio de carga difiere entre los códigos. HydroPol2D-Python compara el mayor cambio de carga aplicado desde la última actualización lateral con `groundwater_max_head_change_m` (0,25 m). El esquema predeterminado de MATLAB no usa ese parámetro. Ejecuta la actualización cuando, en alguna celda, $|h - h_{\mathrm{last}}| \ge \delta_h + \delta_r H$, donde $h_{\mathrm{last}}$ es la carga después de la última actualización lateral, $\delta_h$ es `groundwater_head_tolerance_m` y $\delta_r$ es `groundwater_relative_tolerance` (ambos 0,001 por defecto). El solucionador lateral avanza entonces durante todo el tiempo transcurrido desde su última ejecución.

El programador no se puede desactivar. Ni HydroPol2D-Python ni el código MATLAB leen `flag_groundwater_async`, así que el valor 0 no fuerza una actualización lateral en cada paso de la superficie. Un `groundwater_target_dt_s` más corto hace las actualizaciones laterales más frecuentes.
### 7.2 Límite explícito de estabilidad del agua subterránea

El límite externo del programador se basa en una estimación de difusividad explícita para la ecuación ilimitada Boussinesq:
$$
D = \frac{K H}{S_y}
$$
$$
\Delta t_{\mathrm{gw,stable}}
=
\frac{
C_{\mathrm{gw}} \, L_{\mathrm{grid}}^2
}{
4 D_{\max}
}
$$
dónde:
- $D$ = difusividad del agua subterránea $[\mathrm{L}^2\,\mathrm{T}^{-1}]$
- $C_{\mathrm{gw}}$ = agua subterránea Courant/factor de seguridad $[-]$
- $L_{\mathrm{grid}} = \min(\Delta x,\Delta y)$
- $D_{\max}$ = máxima difusividad de dominio sobre las celdas activas de agua subterránea

Este es el límite utilizado por la lógica `estimate_groundwater_stable_timestep` actual.
### 7.3 Subpaso interno Boussinesq

Cuando se activa una actualización lateral, el solucionador no recibe término de recarga, porque el intercambio neto ya cambió las cargas. Avanza las cargas a lo largo del intervalo transcurrido con subpasos adaptativos de predictor-corrector. Cada subpaso es como máximo el límite de estabilidad de la Sección 7.2 y como mínimo `groundwater_min_dt_s`. Ambos códigos controlan el error por duplicación de paso. Un subpaso se acepta cuando un paso completo y dos medios pasos difieren como máximo $\delta_h + \delta_r H$ en todas las celdas; si no, se acorta y se repite. El siguiente subpaso que el solucionador habría probado queda guardado como paso sugerido para la próxima actualización lateral.
En el código MATLAB, cada uno de esos subpasos se divide además según una condición basada en la velocidad de la forma
$$
\Delta t_{\mathrm{inner}}
\le
\min\!\left(
\frac{C_v \Delta x}{|u_x|},\,
\frac{C_v \Delta y}{|u_y|}
\right)
$$
dónde:
- $u_x, u_y$ son velocidades del agua subterránea de Darcy
- $C_v$ es el factor de seguridad interno basado en la velocidad, el mismo `groundwater_courant`

HydroPol2D-Python hace una sola actualización de predictor-corrector por subpaso y no tiene condición de velocidad.

El resultado es una estrategia de dos niveles:
1. un límite de programación externo basado en la estabilidad explícita del agua subterránea y el cambio de cabeza permitido,
2. un bucle interno de subpasos adaptativos de predictor-corrector dentro del solucionador Boussinesq.

---

## 8. Condiciones de contorno

El solucionador de aguas subterráneas admite:
- Condiciones de contorno de Dirichlet,
- condiciones de contorno sin flujo,
- enmascaramiento de dominio.

### 8.1 Límites de Dirichlet

Si se proporciona una máscara de Dirichlet, la cabeza se prescribe directamente:
$$
h = h_{\mathrm{D}}
$$
en las celdas de límite seleccionadas, donde:
- $h_{\mathrm{D}}$ = límite prescrito $[\mathrm{L}]$

### 8.2 Límites sin flujo

Los límites sin flujo se imponen mediante condiciones de gradiente cero en el perímetro del dominio. En la práctica, HydroPol2D anula el flujo en toda interfaz con una celda fuera del dominio y en el borde exterior de la malla, salvo que la celda del borde tenga una carga prescrita. Es una condición de Neumann discreta; el código no copia cargas a las celdas del perímetro.
### 8.3 Máscara de captación

Todos los cálculos de aguas subterráneas están restringidos al dominio computacional válido. Las celdas fuera de la máscara de captación están configuradas en `NaN`.

---

## 9. Exfiltración de aguas subterráneas a la superficie

Después de actualizar la cabeza del agua subterránea, HydroPol2D calcula la exfiltración donde el nivel del agua subterránea se eleva por encima de la superficie efectiva de la tierra.
La elevación de la superficie utilizada para la exfiltración es
$$
h_{\mathrm{surf}} = z_0 + D_{\mathrm{soil}}
$$
dónde:
- $h_{\mathrm{surf}}$ = elevación efectiva de la superficie terrestre para la emergencia de aguas subterráneas $[\mathrm{L}]$

Luego la exfiltración se calcula como
$$
q_{\mathrm{exf}}
=
\max\left(0,\,h - h_{\mathrm{surf}}\right)
\frac{S_y}{\Delta t}
$$
dónde:
- $q_{\mathrm{exf}}$ = flujo de exfiltración $[\mathrm{L}\,\mathrm{T}^{-1}]$

Esta expresión significa que si la carga de agua subterránea excede la superficie terrestre, el exceso de almacenamiento saturado se expulsa hacia arriba y se transfiere al sistema de agua superficial.
Luego se recorta la altura del agua subterránea para que
$$
h \le h_{\mathrm{surf}}
$$
lo que evita que el agua subterránea permanezca sobre la superficie del terreno una vez contabilizada la exfiltración.

---

## 10. Intercambio río-acuífero

Ambos códigos pueden intercambiar agua entre el acuífero y las celdas de río. El intercambio es opcional y está desactivado por defecto. La activación es `flag_river_groundwater_exchange` en MATLAB y `flags.river_groundwater_exchange` en HydroPol2D-Python. En cada celda de río, el intercambio sigue una ley lineal del lecho,
$$
q_{\mathrm{river}}
=
\frac{K_{\mathrm{bed}}\,A_{\mathrm{bed}}}{b\,A_{\mathrm{cell}}}
\left(h - h_{\mathrm{river}}\right)
$$
donde:
- $q_{\mathrm{river}}$ = tasa de intercambio por unidad de área de la celda, positiva del acuífero al río $[\mathrm{L}\,\mathrm{T}^{-1}]$
- $K_{\mathrm{bed}}$ = conductividad hidráulica del lecho del río $[\mathrm{L}\,\mathrm{T}^{-1}]$
- $A_{\mathrm{bed}}$ = área del lecho, el ancho del río por el tamaño de la celda, como máximo el área de la celda $[\mathrm{L}^2]$
- $b$ = espesor del lecho, `riverbed_thickness_m` (0,5 m por defecto) $[\mathrm{L}]$
- $h_{\mathrm{river}}$ = elevación de la superficie del agua en la celda de río $[\mathrm{L}]$

Cada paso del agua superficial resuelve esta ley de forma exacta para dos almacenamientos acoplados, el acuífero de la celda y su agua superficial, y limita el volumen al agua que contiene el almacenamiento donante. El intercambio se suma al intercambio neto, de modo que cambia la carga del nivel freático en el mismo paso que la recarga y el ascenso capilar.

---

## 11. Corrección del exceso de saturación después del aumento del nivel freático {#11-saturation-excess-correction-after-water-table-rise}

Después de que las cargas cambian en un paso del agua superficial, HydroPol2D vuelve a calcular la profundidad del nivel freático y, por lo tanto, el nuevo almacenamiento insaturado máximo:
$$
S_{\mathrm{UZ,max}}^{\,\mathrm{new}}
=
z_{\mathrm{wt}}^{\,\mathrm{new}}
\left(
\theta_{\mathrm{sat}} - \theta_r
\right)
$$
Si el almacenamiento vadose actualizado excede esta nueva capacidad, el exceso se devuelve a la superficie como agua de saturación-exceso:
$$
S_{\mathrm{excess}}
=
\max\left(
S - S_{\mathrm{UZ,max}}^{\,\mathrm{new}},
0
\right)
$$
La corrección es entonces:
$$
S \leftarrow S - S_{\mathrm{excess}}
$$
y la profundidad del agua superficial aumenta en
$$
h_{\mathrm{surf}}^{\,\mathrm{new}}
=
h_{\mathrm{surf}}^{\,\mathrm{old}}+
S_{\mathrm{excess}}
$$
En la implementación predeterminada en capas, la corrección se aplica capa por capa. Las tres capacidades se recalculan a partir del nuevo nivel freático, cada capa conserva como máximo su propia capacidad, y la suma de los excesos va a la superficie. HydroPol2D-Python aplica la corrección después de la actualización local y otra vez después de una actualización lateral; el código MATLAB la aplica una vez por paso, después de ambas. Esta es una parte muy importante de HydroPol2D porque garantiza **consistencia de masa** entre las zonas vadosa y saturada cuando el nivel freático aumenta durante un intervalo de tiempo.

---

## 12. Acoplamiento de nuevo al agua superficial

El modelo de aguas subterráneas retroalimenta el sistema de aguas superficiales de dos maneras:
1. **exfiltración**, a través de $q_{\mathrm{exf}}$,
2. **exceso de saturación**, a través de $S_{\mathrm{excess}}$.

La profundidad del agua superficial se actualiza como
$$
d_t
=
d_t + \Delta t\,q_{\mathrm{exf}}
$$
con la conversión de unidad apropiada en el código de $\mathrm{m}$ a $\mathrm{mm}$.
Esto significa que HydroPol2D permite que el agua subterránea influya activamente en la generación de inundaciones y la humedad cerca de la superficie, en lugar de tratarlo como un proceso desconectado de límite inferior.

---

## 13. Acuífero profundo {#13-deep-aquifer}

El acuífero profundo opcional representa el agua subterránea lenta situada por debajo del acuífero modelado. Es semidistribuido, con un embalse lineal por subcuenca.

### 13.1 Estructura {#131-structure}

Una fracción fija $f_d$ de la recarga descendente se envía al acuífero profundo antes de que el resto llegue al nivel freático. La recarga de todas las celdas de la subcuenca $k$ alimenta el embalse $k$. El embalse descarga

$$
Q_k = \frac{S_k}{\tau}
$$

donde:

- $S_k$ = almacenamiento del embalse $k$ $[\mathrm{L}^3]$
- $\tau$ = tiempo de respuesta $[\mathrm{T}]$, igual para todas las subcuencas
- $Q_k$ = flujo de retorno profundo $[\mathrm{L}^3\,\mathrm{T}^{-1}]$

Dos rásteres definen la disposición. El ráster de subcuencas indica qué celdas alimentan cada embalse. El ráster de pesos del canal indica dónde descarga cada embalse. El flujo de retorno se reparte entre las celdas de río de su propia subcuenca, en proporción al peso.

### 13.2 Actualización {#132-update}

Para una tasa de entrada $I_k$ durante un paso $\Delta t$, el embalse usa la solución exacta de la ecuación del embalse lineal

$$
S_{k}^{t+\Delta t}
=
S_{k}^{t}\,e^{-\Delta t/\tau}
+
I_k\,\tau\left(1-e^{-\Delta t/\tau}\right)
$$

y el volumen descargado es

$$
V_{Q,k} = I_k\,\Delta t - \left(S_{k}^{t+\Delta t} - S_{k}^{t}\right)
$$

La actualización es conservativa y no depende de la duración del paso.

### 13.3 Estado inicial {#133-starting-state}

Como el caudal de salida es el almacenamiento dividido por $\tau$, el almacenamiento inicial se obtiene de un caudal de salida inicial por unidad de área $q_0$,

$$
S_{k,0} = q_0\,A_k\,\tau
$$

donde $A_k$ es el área activa de la subcuenca $k$. Se debe indicar como máximo una de las opciones siguientes.

| Parámetro | Significado | $q_0$ |
|---|---|---|
| `deep_aquifer_initial_baseflow_mm_day` | Flujo base profundo en la fecha de inicio, por ejemplo a partir de una estación de aforo | el valor indicado |
| `deep_aquifer_mean_recharge_mm_year` | Recarga media de largo plazo $\bar{R}$; los embalses parten en estado estacionario | $f_d\,\bar{R}$ |
| Archivo de estado inicial del acuífero profundo | Almacenamiento por subcuenca, escrito por la calibración del agua subterránea | almacenamiento indicado directamente |

Si no se indica ninguna, los embalses parten vacíos.

**A partir de una estación de aforo.** HydroPol2D-Python estima $q_0$ a partir de un registro diario de caudal con `hydropol2d estimate-deep-baseflow`, en los pasos siguientes.

1. Flujo base de Lyne–Hollick del caudal observado.
2. Segmentos de recesión y una curva maestra de recesión (MRC).
3. Separación de la cola profunda, lenta y lineal, de la MRC, que también da $\tau$.
4. Ubicación del flujo base de la fecha de inicio sobre la MRC y división de su parte profunda por el área de drenaje.

Conviene elegir una fecha de inicio dentro de una recesión. El filtro de flujo base se retrasa respecto de un hidrograma en ascenso, por lo que la herramienta emite una advertencia cuando el caudal de la fecha de inicio es mayor que el doble del flujo base.

### 13.4 Configuración {#134-settings}

| Elemento | HydroPol2D-Python | HydroPol2D (MATLAB) |
|---|---|---|
| Activación | `flags.deep_aquifer` | `flag_deep_aquifer` |
| Subcuencas | `static.deep_aquifer_subbasin_path` | `DeepAquiferSubbasins_path` |
| Pesos del canal | `static.deep_aquifer_channel_weight_path` | `DeepAquiferChannelWeight_path` |
| Fracción de recarga $f_d$ | `vertical.deep_recharge_fraction` | `deep_recharge_fraction` |
| Tiempo de respuesta $\tau$ | `vertical.deep_aquifer_response_time_days` (180 por defecto) | `deep_aquifer_tau_days` |
| Flujo base inicial | `vertical.deep_aquifer_initial_baseflow_mm_day` | `deep_aquifer_initial_baseflow_mm_day` |
| Recarga media | `vertical.deep_aquifer_mean_recharge_mm_year` | `deep_aquifer_mean_recharge_mm_year` |
| Archivo de estado inicial | `static.deep_aquifer_initial_state_path` | `DeepAquiferInitialState_path` |

En MATLAB, los valores del estado inicial están en el bloque "Deep aquifer: starting storage" de la pestaña Soil and groundwater (ver [Parámetros del libro del caso](../configuration/general_data#tab-soil-and-groundwater)). El Case Builder escribe los rásteres de subcuencas y de pesos del canal a partir del terreno D8 acondicionado.

---

## 14. Balance de masa {#14-mass-balance}

El solucionador de aguas subterráneas realiza una verificación explícita del balance de masa durante cada actualización.
El volumen de entrada de recarga es
$$
V_{\mathrm{recharge}}
=
\sum R\,\Delta t\,A_{\mathrm{cell}}
$$
El volumen de pérdida por exfiltración es
$$
V_{\mathrm{exf}}
=
\sum q_{\mathrm{exf}}\,\Delta t\,A_{\mathrm{cell}}
$$
El cambio en el almacenamiento de agua subterránea es
$$
\Delta V_{\mathrm{storage}}
=
\sum S_y\,\max(h^{t+\Delta t}-z_0,0)\,A_{\mathrm{cell}}-
\sum S_y\,\max(h^t-z_0,0)\,A_{\mathrm{cell}}
$$
El residuo del balance de masa es entonces
$$
\varepsilon_{\mathrm{gw}}
=
V_{\mathrm{recharge}}-
V_{\mathrm{exf}}-
\Delta V_{\mathrm{storage}}
$$
dónde:
- $\varepsilon_{\mathrm{gw}}$ = error de balance de masa de agua subterránea $[\mathrm{L}^3]$

La actualización local de cada paso del agua superficial cierra el mismo balance, con el intercambio neto como término de recarga. El solucionador lateral se llama con $R = 0$, y su verificación también cuenta el agua intercambiada con las celdas de carga prescrita. El código MATLAB guarda el residuo lateral como error de diagnóstico de agua subterránea. HydroPol2D-Python no lo guarda y sigue el balance hídrico de todo el modelo.

La recarga y el ascenso capilar no esperan en el programador. El intercambio neto cambia las cargas en el mismo paso del agua superficial, por lo que ningún intercambio queda en tránsito entre actualizaciones laterales. Los totales pendientes de recarga y de ascenso capilar solo cuentan lo que ha pasado desde la última actualización lateral y no son almacenamiento adicional. Esta distinción es importante para interpretar los diagnósticos del balance hídrico de todo el modelo.

---

## 15. Resumen {#15-summary}

El modelo de aguas subterráneas HydroPol2D combina:
- un **módulo de recarga de zona vadosa en capas** basado en un cierre de Darcy-van Genuchten-Mualem,
- **ascenso capilar** desde aguas subterráneas poco profundas hacia la zona de raíces,
- un **programador asíncrono de aguas subterráneas** para el flujo lateral más lento, mientras el intercambio neto cambia las cargas en cada paso del agua superficial,
- un **modelo de flujo de agua subterránea 2D Boussinesq** para flujo saturado lateral,
- **paso de tiempo explícito adaptativo**,
- **exfiltración superficial** cuando el agua subterránea se eleva por encima de la superficie del suelo,
- una **corrección de exceso de saturación** que preserva la masa cuando el nivel freático reduce la capacidad de almacenamiento vadosa,
- y un **acuífero profundo** opcional formado por embalses lineales por subcuenca, con un estado inicial definido a partir de un flujo base o de una recarga media.

Esta estructura permite que HydroPol2D represente un sistema de subsuelo acoplado dinámicamente en el que:
- la infiltración no desaparece simplemente en un cubo estático,
- la recarga afecta la cabeza del agua subterránea,
- El flujo de agua subterránea redistribuye el agua lateralmente.
- y el agua subterránea puede regresar a la superficie terrestre e influir en la generación de flujo superficial.

El resultado es un modelo de agua subterránea que es físicamente interpretable, conservador de masa y completamente integrado con la arquitectura hidrológica e hidrodinámica de HydroPol2D.