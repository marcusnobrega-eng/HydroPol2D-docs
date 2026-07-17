---
title: Modelo de aguas subterráneas
---

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
  <img src={require('../assets/figures/aquifer/aquifer_schematics.png').default} width="700" />
</p>
<p align="center">
  <em>Figura 1. Representación conceptual del componente acuífero en HydroPol2D.</em>
</p>
---

## 2. Estructura conceptual general

El modelo de aguas subterráneas está acoplado a dos relojes. El intercambio de la zona vadosa se evalúa en cada paso de tiempo del agua superficial porque la infiltración y la evapotranspiración necesitan una rápida retroalimentación de la humedad del suelo. Los cabezales de agua subterránea saturada se actualizan con menos frecuencia, generalmente en un intervalo de tiempo objetivo diario, a menos que los límites de estabilidad o cambio de cabezal requieran una actualización más breve.
La lógica es:
1. calcular la posición del nivel freático a partir de la altura actual del agua subterránea,
2. determinar el almacenamiento no saturado máximo permitido por la profundidad actual del nivel freático,
3. calcular el drenaje/recarga desde las capas vadosas al agua subterránea durante el paso superficial actual,
4. calcular el ascenso capilar desde el agua subterránea hasta las capas vadosas cuando esté habilitado,
5. acumular el volumen neto de intercambio en el programador de aguas subterráneas,
6. actualizar los cabezales de agua subterránea saturada cuando venza el programador,
7. resolver el flujo lateral de agua subterránea usando una ecuación 2D Boussinesq cuando el flujo base está activo,
8. calcular la exfiltración de agua subterránea a la superficie,
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

### 2.1 Programador asincrónico

El programador asincrónico está activo de forma predeterminada cuando el modelado de aguas subterráneas está habilitado. Los principales controles son:
| Control | Por defecto | Significado |
|---|---:|---|
| `flag_groundwater_async` | 1 | Utiliza actualizaciones más lentas de agua subterránea saturada en lugar de actualizar los cabezales en cada paso de la superficie. |
| `groundwater_target_dt_min` | 1440 | Intervalo objetivo de actualización del agua subterránea, en minutos. |
| `groundwater_min_dt_min` | 1 | Intervalo mínimo de actualización de aguas subterráneas, en minutos. |
| `groundwater_max_head_change_m` | 0,25 | Fuerza una actualización cuando el intercambio acumulado cambie de cabeza en esta cantidad. |
| `groundwater_courant` | 0,25 | Factor de estabilidad para la estimación del paso de tiempo del agua subterránea Boussinesq. |
| `flag_capillary_rise` | 1 | Permite un ascenso capilar en capas simple cuando hay almacenamiento de suelo en capas. |

La recarga pendiente, el ascenso capilar y el intercambio neto se almacenan como variables de estado del programador. Cuando se ejecuta una actualización de agua subterránea, la profundidad neta acumulada de intercambio se divide por el intervalo de agua subterránea transcurrido para formar el término de recarga pasado al solucionador saturado.
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
\izquierda(
\theta_{\mathrm{sat}} - \theta_r
\derecha)
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
\frac{S_{\ell}}{z_{\ell}}
$$
$$
S_{e,\ell}
=
\frac{
\theta_{\ell} - \theta_{\mathrm{r},\ell}
{}
\theta_{\mathrm{sat},\ell} - \theta_{\mathrm{r},\ell}
}
$$
$$
K_{\ell}
=
K_{\mathrm{sat},\ell}
S_{e,\ell}^{\ell_v}
\izquierda[
1 - \left(1 - S_{e,\ell}^{1/m_{\ell}}\right)^{m_{\ell}}
\derecha]^2
$$
con
$$
m_{\ell} = 1 - \frac{1}{n_{\ell}}
$$
dónde:
- $\theta_{\ell}$ = contenido de agua de la capa $[-]$
- $S_{e,\ell}$ = saturación efectiva de capa $[-]$
- $K_{\ell}$ = conductividad insaturada de la capa $[\mathrm{L}\,\mathrm{T}^{-1}]$
- $\ell_v$ = Parámetro de conectividad de poros de Mualem $[-]$

Esta es la misma familia constitutiva de van Genuchten-Mualem utilizada por el módulo de infiltración.
### 4.3 Cascada de drenaje descendente

La ruta de recarga en capas se calcula como una cascada descendente:
1. El drenaje cercano a la superficie va a la zona de las raíces cuando existe almacenamiento de raíces.
2. el drenaje de la zona de la raíz va a la zona de transmisión cuando existe almacenamiento de transmisión,
3. El drenaje de la zona de transmisión se convierte en recarga de aguas subterráneas.

Conceptualmente, la profundidad de drenaje de una capa a lo largo de un paso de tiempo se puede resumir como
$$
\Delta D_{\ell} \aprox K_{\ell}\,\Delta t
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

HydroPol2D todavía contiene el cierre de recarga del depósito representativo anterior para los casos en los que los datos de almacenamiento en capas explícitos no están disponibles. En ese modo de reserva, un único estado de almacenamiento vadoso se convierte en un contenido de agua representativo y se drena con un cierre tipo Darcy. Esa formulación debe tratarse como un **legado/refuerzo**, no como el camino teórico principal para el modelo actual.
---

## 5. Aumento capilar opcional

Cuando `flag_capillary_rise = 1`, HydroPol2D permite que el agua subterránea poco profunda se mueva hacia arriba hasta el almacenamiento vadoso disponible. La implementación actual es una simple regla de ascenso capilar en capas, no una solución completa de la ecuación de Richards.
El intercambio ascendente aumenta con:
- menor profundidad del nivel freático,
- mayor déficit de almacenamiento en la capa receptora,
- y mayor conductividad saturada en esa capa.

Conceptualmente, la transferencia capilar ascendente hacia la capa $\ell$ está limitada por
$$
C_{\ell}
\le
\min\!\izquierda(
S_{\ell,\mathrm{def}},\,
K_{\mathrm{sat},\ell} f_{\mathrm{prox}}(z_{\mathrm{wt}}) f_{\mathrm{dry}}(S_{\ell})
\derecha)
$$
dónde:
- $S_{\ell,\mathrm{def}}$ es el déficit de almacenamiento de capa restante
- $f_{\mathrm{prox}}$ es un factor monótono de proximidad al nivel freático
- $f_{\mathrm{dry}}$ es un factor de sequedad monótono

En el código actual, el ascenso capilar se evalúa primero en la zona de transmisión, luego en la zona de la raíz y solo en la capa cercana a la superficie cuando no existe un almacenamiento vadoso inferior.
Por lo tanto, el intercambio neto vadoso-agua subterránea acumulado por el programador es
$$
R_{\mathrm{net}} = R_{\mathrm{down}} - C_{\mathrm{up}}
$$
donde $C_{\mathrm{up}}$ es el flujo total de ascenso capilar ascendente.
---

## 6. Modelo bidimensional de flujo de agua subterránea Boussinesq

Una vez calculada la recarga, HydroPol2D encamina el agua subterránea lateralmente utilizando la función `PHTOKEN1XYZ_2D_explicit`.
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

HydroPol2D evalúa esta ecuación numéricamente calculando los flujos en las interfaces de las celdas y luego actualizando explícitamente la cabeza del agua subterránea.
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

Para evitar la inestabilidad numérica y el agotamiento no físico del almacenamiento de agua subterránea, HydroPol2D aplica un limitador de flujo para que ninguna celda pueda perder más agua de la que contiene durante un subpaso.
Por ejemplo, en la dirección $x$, el flujo máximo permitido es
$$
F_{x,\max}
=
\frac{S_y H_{\mathrm{donor}}}{\Delta t}
$$
y el flujo de interfaz final está limitado como
$$
F_x \flecha izquierda \nombreoperador{sign}(F_x)\,\min\izquierda(|F_x|,\,F_{x,\max}\derecha)
$$

Se utiliza una expresión similar en la dirección $y$.
Esta es una característica importante del solucionador de aguas subterráneas HydroPol2D porque garantiza la admisibilidad de la masa local durante la integración explícita.
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
h^t+
\frac{\Delta t}{S_y}
\izquierda(
-\nabla \cdot \mathbf{F}^{\mathrm{avg}} + R
\derecha)
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

El intercambio de vadosa se acumula en cada paso del agua superficial, pero los cabezales de agua subterránea saturada se actualizan solo cuando corresponde el programador de agua subterránea. El intervalo de actualización del agua subterránea es el mínimo de:
- el intervalo objetivo del usuario,
- el límite explícito de estabilidad de las aguas subterráneas,
- el intervalo implicado por el cambio de cabeza acumulado máximo permitido,
- y el intervalo parcial final al final de la carrera.

Si `flag_groundwater_async = 0`, la actualización del agua subterránea saturada se fuerza en cada paso de la superficie.
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
{}
4D_{\max}
}
$$
dónde:
- $D$ = difusividad del agua subterránea $[\mathrm{L}^2\,\mathrm{T}^{-1}]$
- $C_{\mathrm{gw}}$ = agua subterránea Courant/factor de seguridad $[-]$
- $L_{\mathrm{grid}} = \min(\Delta x,\Delta y)$
- $D_{\max}$ = máxima difusividad de dominio sobre las celdas activas de agua subterránea

Este es el límite utilizado por la lógica `estimate_groundwater_stable_timestep` actual.
### 7.3 Subpaso interno Boussinesq

Cuando se activa una actualización de agua subterránea, el programador convierte la profundidad de intercambio neto acumulada en una tasa de recarga promedio durante el intervalo de agua subterránea transcurrido y la pasa al solucionador de saturación. Luego, el solucionador Boussinesq avanza a lo largo de ese intervalo utilizando subpasos internos de predictor-corrector.
Esos subpasos internos están además limitados por una condición basada en la velocidad de la forma
$$
\Delta t_{\mathrm{inner}}
\le
\min\!\izquierda(\frac{C_v \Delta x}{|u_x|},\,
\frac{C_v \Delta y}{|u_y|}
\derecha)
$$
dónde:
- $u_x, u_y$ son velocidades del agua subterránea de Darcy
- $C_v$ es el factor de seguridad interno basado en la velocidad

El resultado es una estrategia de dos niveles:
1. un límite de programación externo basado en la estabilidad explícita del agua subterránea y el cambio de cabeza permitido,
2. un bucle interno de subpaso predictor-corrector dentro del solucionador Boussinesq.

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

Los límites sin flujo se imponen mediante condiciones de gradiente cero en el perímetro del dominio. En la práctica, HydroPol2D copia la cabeza del vecino interior válido más cercano a la celda del perímetro, imponiendo así una condición de Neumann discreta.
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

La interfaz del solucionador actual incluye:
- una máscara de río,
- un término de conductancia del río,
- etapa del río,
- elevación del lecho del río,

que están diseñados para apoyar el intercambio río-acuífero. En la implementación actual, la variable de marcador de posición
$$
q_{\mathrm{river}}
$$
se inicializa y se transporta a través de la interfaz de acoplamiento como el término de intercambio de río. Esto significa que la interfaz está presente, pero el intercambio río-acuífero debería describirse actualmente como un **marcador de posición/gancho estructural**, no como una afirmación teórica madura e independiente en el mismo plano que la recarga, el flujo lateral de agua subterránea, el ascenso capilar o la exfiltración.
---

## 11. Corrección del exceso de saturación después del aumento del nivel freático

Después de la actualización Boussinesq, HydroPol2D vuelve a calcular la profundidad del nivel freático y, por lo tanto, el nuevo almacenamiento insaturado máximo:
$$
S_{\mathrm{UZ,max}}^{\,\mathrm{new}}
=
z_{\mathrm{wt}}^{\,\mathrm{new}}
\izquierda(
\theta_{\mathrm{sat}} - \theta_r
\derecha)
$$
Si el almacenamiento vadose actualizado excede esta nueva capacidad, el exceso se devuelve a la superficie como agua de saturación-exceso:
$$
S_{\mathrm{excess}}
=
\max\izquierda(
S - S_{\mathrm{UZ,max}}^{\,\mathrm{new}},
0
\derecha)
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
En la implementación predeterminada en capas, se aplica la misma corrección después de volver a calcular la capacidad sumada admisible de la capa vadosa. Esta es una parte muy importante de HydroPol2D porque garantiza **consistencia de masa** entre las zonas vadosa y saturada cuando el nivel freático aumenta durante un intervalo de tiempo.
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

## 13. Balance de masa

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

Esta cantidad se almacena como un error de diagnóstico de agua subterránea en HydroPol2D.
Cuando el agua subterránea asíncrona está activa, la recarga acumulada pendiente y el intercambio capilar no se tratan como pérdida del modelo. Se almacenan como intercambio de agua subterránea en tránsito hasta que la próxima actualización saturada consuma el volumen del programador. Esta distinción es importante para interpretar los diagnósticos del balance hídrico de todo el modelo.
---

## 14. Resumen

El modelo de aguas subterráneas HydroPol2D combina:
- un **módulo de recarga de zona vadosa en capas** basado en un cierre de Darcy-van Genuchten-Mualem,
- **ascenso capilar simple** desde aguas subterráneas poco profundas hasta el almacenamiento vadoso disponible,
- un **programador asíncrono de aguas subterráneas** para actualizaciones más lentas de cabezas saturadas,
- un **modelo de flujo de agua subterránea 2D Boussinesq** para flujo saturado lateral,
- **paso de tiempo explícito adaptativo**,
- **exfiltración superficial** cuando el agua subterránea se eleva por encima de la superficie del suelo,
- y una **corrección de exceso de saturación** que preserva la masa cuando el nivel freático reduce la capacidad de almacenamiento vadosa.

Esta estructura permite que HydroPol2D represente un sistema de subsuelo acoplado dinámicamente en el que:
- la infiltración no desaparece simplemente en un cubo estático,
- la recarga afecta la cabeza del agua subterránea,
- El flujo de agua subterránea redistribuye el agua lateralmente.
- y el agua subterránea puede regresar a la superficie terrestre e influir en la generación de flujo superficial.

El resultado es un modelo de agua subterránea que es físicamente interpretable, conservador de masa y completamente integrado con la arquitectura hidrológica e hidrodinámica de HydroPol2D.