---
title: Modelo hidrodinámico
---

# Modelo hidrodinámico

HydroPol2D incluye actualmente cinco familias principales de enrutamiento de superficie:
- inercial local,
- pleno impulso,
- difusivo D4,
- cinemática D4,
- autómatas celulares.

Sólo una de estas formulaciones de enrutamiento principales debe estar activa a la vez. El código actual impone esta exclusividad de la familia de enrutamiento a través de las banderas de modelo correspondientes. El soporte D8 sigue siendo una vía secundaria de alcance limitado.
## 1. Enrutamiento de flujo inercial local

### 1.1 Justificación general

HydroPol2D utiliza la **aproximación inercial local** como formulación de enrutamiento hidrodinámico predeterminada. El objetivo es retener los controles físicos dominantes del flujo superficial y al mismo tiempo evitar la carga computacional de las ecuaciones completas de aguas poco profundas.
El enfoque inercial local es particularmente atractivo para el modelado de inundaciones porque preserva:
- el gradiente de presión en la superficie libre,
- aceleración gravitacional,
- resistencia a la fricción,
- y aceleración temporal local,

mientras se desprecian los términos de aceleración convectiva que a menudo son mucho más pequeños que los términos de presión y fricción en flujos poco profundos que varían gradualmente. Esto produce una formulación que es más consistente físicamente que el enrutamiento cinemático o puramente empírico, pero aún mucho más liviana que un solucionador de ondas dinámicas completo. HydroPol2D utiliza esta formulación como motor principal para las inundaciones terrestres, el intercambio de llanuras aluviales y la redistribución del agua superficial entre celdas ráster.
Desde el punto de vista del modelado, la formulación inercial local es un buen compromiso porque HydroPol2D está destinado a soportar:
- simulaciones de inundaciones impulsadas por lluvias,
- enrutamiento fluvial con afluencia y límites de etapa,
- aplicaciones urbanas y de llanuras aluviales,
- y puntos de referencia de enrutamiento controlados a través de varias aproximaciones numéricas,

todo dentro de un marco hidrológico-hidrodinámico modular. El modelo inercial local es, por tanto, el núcleo hidrodinámico que conecta los módulos de generación de lluvia y escorrentía con la redistribución espacial del agua superficial.
---

### 1.2 Ecuaciones rectoras

El punto de partida es la ecuación de conservación de masa integrada en profundidad:
$$
\frac{\partial h}{\partial t}+
\frac{\partial q_x}{\partial x}+
\frac{\partial q_y}{\partial y}
=
r-
i-
y+
s
$$
dónde:
- $h$ es la profundidad del agua superficial $[\mathrm{L}]$
- $q_x$ es la descarga unitaria en la dirección $x$ $[\mathrm{L}^2\,\mathrm{T}^{-1}]$
- $q_y$ es la descarga unitaria en la dirección $y$ $[\mathrm{L}^2\,\mathrm{T}^{-1}]$
- $r$ es la entrada de lluvia $[\mathrm{L}\,\mathrm{T}^{-1}]$
- $i$ es la pérdida por infiltración $[\mathrm{L}\,\mathrm{T}^{-1}]$
- $et$ es la pérdida por evapotranspiración $[\mathrm{L}\,\mathrm{T}^{-1}]$
- $s$ es la colección de términos fuente y receptor adicionales $[\mathrm{L}\,\mathrm{T}^{-1}]$

En HydroPol2D, los términos hidrológicos se calculan antes del enrutamiento y luego se utiliza el solucionador inercial local para evaluar el término de redistribución de flujo.
Para cada cara, la ecuación del momento de inercia local se escribe en forma simplificada como
$$
\frac{\partial q}{\partial t}
=-
g\,H_{\mathrm{f}}\,S-
g\,n^2\,\frac{q\,|q|}{H_{\mathrm{f}}^{7/3}}
$$

dónde:
- $q$ es la descarga unitaria a través de una cara $[\mathrm{L}^2\,\mathrm{T}^{-1}]$
- $g$ es la aceleración gravitacional $[\mathrm{L}\,\mathrm{T}^{-2}]$
- $H_{\mathrm{f}}$ es la profundidad efectiva del flujo en la cara $[\mathrm{L}]$
- $S$ es el talud de superficie libre en la cara $[-]$
- $n$ es el coeficiente de rugosidad de Manning $[\mathrm{T}\,\mathrm{L}^{-1/3}]$

Esta formulación ignora la aceleración convectiva pero conserva el equilibrio hidráulico dominante entre la aceleración local, el gradiente de presión y la resistencia a la fricción del lecho.
---

### 1.3 Elevación de la superficie del agua y pendientes del frente

El cálculo de la ruta comienza a partir de la elevación de la superficie del agua por celda.
$$
eta = z + h
$$
dónde:
- $\eta$ es la elevación de la superficie del agua $[\mathrm{L}]$
- $z$ es la elevación de la cama $[\mathrm{L}]$
- $h$ es la profundidad del agua $[\mathrm{L}]$

En la implementación estándar validada, HydroPol2D utiliza la elevación del lecho DEM directamente para los cálculos de pendiente.
En la cara este entre las celdas $i$ y $i+1$, la elevación del lecho de la cara se toma como
$$
z_{\mathrm{f},x} = \max\!\left(z_i,\;z_{i+1}\right)
$$
y las elevaciones de la superficie del agua reconstruidas hidrostáticamente son
$$
\eta_{\mathrm{L},x}^{\ast} = \max\!\left(\eta_i,\;z_{\mathrm{f},x}\right)
\qquad
\eta_{\mathrm{R},x}^{\ast} = \max\!\left(\eta_{i+1},\;z_{\mathrm{f},x}\right)
$$
La pendiente de la superficie libre en la cara se calcula entonces como
$$
S_x = \frac{\eta_{\mathrm{R},x}^{\ast} - \eta_{\mathrm{L},x}^{\ast}}{\Delta x}
$$
De manera similar, para una cara norte-sur,
$$
z_{\mathrm{f},y} = \max\!\left(z_j,\;z_{j+1}\right)
$$
$$
\eta_{\mathrm{S},y}^{\ast} = \max\!\left(\eta_j,\;z_{\mathrm{f},y}\right)
\qquad
\eta_{\mathrm{N},y}^{\ast} = \max\!\left(\eta_{j+1},\;z_{\mathrm{f},y}\right)
$$
$$
S_y = \frac{\eta_{\mathrm{S},y}^{\ast} - \eta_{\mathrm{N},y}^{\ast}}{\Delta x}
$$
Esta reconstrucción hidrostática es esencial cerca de frentes húmedos-secos porque evita profundidades negativas no físicas y garantiza que el gradiente de presión se evalúe solo sobre la porción mojada de la interfaz conectada hidráulicamente. En términos prácticos, es uno de los ingredientes estabilizadores clave de la implementación inercial local HydroPol2D.
---

### 1.4 Profundidad de cara efectiva

La profundidad hidráulica efectiva utilizada en la ecuación del momento se calcula al nivel de la cara.
Para el caso estándar de rejilla gruesa, la profundidad de la cara es
$$
H_{\mathrm{f},x}
=
\max\!\left(
\max(\eta_i,\eta_{i+1}) - z_{\mathrm{f},x},
0
\right)
$$
y de manera similar en la dirección $y$.
Por lo tanto, la profundidad de la cara no es simplemente el promedio aritmético de las profundidades de las celdas vecinas. En cambio, es una profundidad reconstruida hidrostáticamente referida a la elevación más alta del lecho en la interfaz. Esto hace que el modelo sea mucho más robusto cuando las celdas adyacentes tienen diferentes elevaciones del lecho o cuando un lado está casi seco. La misma definición conceptual ya figura en su documento de antecedentes.
---

### 1.5 Solucionador inercial local discreto

HydroPol2D actualiza la descarga facial explícitamente en el tiempo. La forma discreta base utilizada en el esquema tipo Bates original es
$$
q^{t+\Delta t}
=
\frac{
q^{t}-
g\,H_{\mathrm{f}}\,\Delta t\,S
{}
1+
g\,\Delta t\,n^2
\,\dfrac{|q^{t}|}{H_{\mathrm{f}}^{7/3}}
}
$$

dónde:
- $q^{t}$ es la descarga de cara anterior $[\mathrm{L}^2\,\mathrm{T}^{-1}]$
- $q^{t+\Delta t}$ es la descarga facial actualizada $[\mathrm{L}^2\,\mathrm{T}^{-1}]$
- $\Delta t$ es el paso de tiempo $[\mathrm{T}]$

Esta es la forma exacta implementada en `Inertial_Solver` cuando `flag_numerical_scheme = 1`.
La estructura de esta ecuación es importante:
- el numerador contiene la memoria inercial del paso anterior y el término de conducción en superficie libre,
- el denominador contiene la amortiguación por fricción,
- por lo que el esquema se comporta como un predictor explícito con tratamiento de fricción semiimplícito.

Por eso el método es estable y eficiente para simulaciones de inundaciones poco profundas.
---

### 1.6 Esquemas numéricos disponibles en HydroPol2D

HydroPol2D admite tres variantes inerciales locales:
- esquema Bates original,
- $s$-esquema de ceñida,
- Esquema centrado en $s$.

Estos están controlados por `flag_numerical_scheme`.
#### 1.6.1 Esquema 1: formulación original de Bates

Esta es la actualización inercial local discreta más simple y directa:
$$
q^{t+\Delta t}
=
\frac{
q^{t}-
g\,H_{\mathrm{f}}\,\Delta t\,S
{}
1+
g\,\Delta t\,n^2
\,\dfrac{|q^{t}|}{H_{\mathrm{f}}^{7/3}}
}
$$

Es computacionalmente eficiente y físicamente consistente, pero en entornos de gradiente pronunciado o fuertemente discontinuos puede ser más propenso a un comportamiento oscilatorio que los esquemas modificados.
#### 1.6.2 Esquema 2: formulación $s$-a barlovento

La versión contra el viento introduce una estimación de descarga direccional $q_{\mathrm{upwind}}$ y la combina con la descarga frontal actual usando un factor de difusividad $\theta$:
$$
q^{t+\Delta t}
=
\frac{
\theta q^{t}+
(1-\theta) q_{\mathrm{upwind}}-
g\,H_{\mathrm{f}}\,\Delta t\,S
{}
1+
g\,\Delta t\,n^2
\,\dfrac{|q^{t}|}{H_{\mathrm{f}}^{7/3}}
}
$$

El factor de difusividad se calcula como
$$
\theta
=
1-
\frac{\Delta t}{\Delta x}
\min\!\left(\frac{|q|}{H_{\mathrm{f}}},
\sqrt{g\,H_{\mathrm{f}}}
\right)
$$
Esta cantidad introduce una difusión numérica controlada. En términos prácticos:
- cuando el flujo es lento y está bien resuelto, $\theta$ permanece cerca de $1$ y el esquema se comporta como la actualización inercial local original;
- cuando el flujo se vuelve rápido o el paso de tiempo se acerca al límite local de Courant, el esquema desplaza parte de la actualización hacia el flujo contra el viento, lo que amortigua las oscilaciones.

Es por eso que la variante de ceñida es útil en condiciones de ruta más desafiantes.
#### 1.6.3 Esquema 3: formulación centrada en $s$

El esquema centrado reemplaza la descarga contra el viento por un promedio vecino centrado:
$$
q_{\mathrm{avg}}
=
\frac{q_{i-1} + q_{i+1}}{2}
$$
y actualiza la descarga como
$$
q^{t+\Delta t}
=
\frac{
\theta q^{t}+
(1-\theta) q_{\mathrm{avg}}-
g\,H_{\mathrm{f}}\,\Delta t\,S
{}
1+
g\,\Delta t\,n^2
\,\dfrac{|q^{t}|}{H_{\mathrm{f}}^{7/3}}
}
$$

Este esquema es más simétrico que la versión contra el viento y menos difuso, pero todavía utiliza el mismo coeficiente $\theta$ para suprimir la inestabilidad. En la práctica, proporciona un compromiso entre la respuesta más aguda de la forma Bates original y la amortiguación más fuerte de la forma de ceñida.
---

### 1.7 Tratamiento húmedo-seco y profundidad operatoria mínima

HydroPol2D contiene varias protecciones explícitas para evitar el enrutamiento no físico a través de interfaces secas o no válidas.
Una cara se suprime si:
- la profundidad efectiva de la cara es cero,
- una de las celdas vecinas está fuera del dominio válido,
- o la profundidad de la celda local está por debajo de un umbral operativo mínimo.

En términos de código, HydroPol2D pone a cero:
- pendiente de la cara,
- profundidad efectiva,
- y ancho de cara efectivo

siempre que la cara esté seca o inválida. Luego aplica una lógica adicional de aguas poco profundas basada en una profundidad operativa mínima $h_{\min}$. Si la profundidad de la celda actual está por debajo de $h_{\min}$, los flujos de las caras vecinas se ponen a cero para suprimir el movimiento espurio en celdas casi secas. En el caso estándar, el código usa $h_{\min}=10^{-6}\,\mathrm{m}$, aunque esto se puede establecer en cero cuando se imponen hidrogramas de entrada.
Esta lógica húmedo-seco es una de las razones por las que el modelo sigue siendo sólido en las fases de expansión y recesión de las inundaciones.
---

### 1.9 Conversión de unidades y contabilidad de descargas faciales

Internamente, el solucionador inercial trabaja con **descarga unitaria** $q$ en
$$
[\mathrm{L}^2\,\mathrm{T}^{-1}]
\quad\text{that is,}\quad
[\mathrm{m}^2\,\mathrm{s}^{-1}]
$$
El código primero convierte el estado de flujo de salida actual de unidades de profundidad basadas en celdas a descarga de unidades basadas en frente. Después de realizar la actualización inercial local, el modelo vuelve a convertir a descarga volumétrica por cara:
$$
Q = q\,W_{\mathrm{f}}
$$
y luego a una tasa de profundidad equivalente sobre el área de la celda:
$$
q_{\mathrm{mm/h}}
=
\frac{Q}{A_{\mathrm{cell}}}
\,
1000
\,
3600
$$
dónde:
- $A_{\mathrm{cell}}$ es el área de la celda $[\mathrm{L}^2]$

Esta contabilidad es necesaria porque HydroPol2D acopla los flujos hidrodinámicos a términos hidrológicos que se rastrean en unidades de profundidad como $\mathrm{mm}$ o $\mathrm{mm/h}$.
---

### 1.10 Límites de flujo físico

HydroPol2D impone dos restricciones físicas adicionales después de la actualización inercial.
#### 1.10.1 Límite de flujo crítico

Si el limitador de flujo crítico está activo, la magnitud de la descarga unitaria está limitada por
$$
|q| \le H_{\mathrm{f}} \sqrt{g\,H_{\mathrm{f}}}
$$

Esto evita que el solucionador inercial produzca velocidades que excedan la condición crítica local.
#### 1.10.2 Límite de velocidad máxima

HydroPol2D también impone un umbral de velocidad máximo estricto, actualmente establecido en
$$
u_{\max} = 10 \;\mathrm{m\,s}^{-1}
$$
El límite de descarga unitaria correspondiente es
$$
|q| \le H_{\mathrm{f}}\,u_{\max}
$$

Esta es una salvaguardia numérica pragmática contra picos aislados causados ​​por profundidades abruptas o discontinuidades de pendiente.
---

### 1.11 Actualización de continuidad y equilibrio de volumen de celda

Una vez que se han calculado las descargas frontales, HydroPol2D actualiza cada celda integrando la divergencia del flujo neto a lo largo del paso de tiempo.
A nivel celular, el equilibrio de volumen entre células se puede escribir conceptualmente como
$$
\Delta V
=
\Delta t
\left(
Q_{\mathrm{in}} - Q_{\mathrm{out}}
\right)
$$
La profundidad del agua actualizada es entonces
$$
h^{t+\Delta t}
=
h^t+
\frac{\Delta V}{A_{\mathrm{eff}}}
$$
dónde:
- $A_{\mathrm{eff}}$ es el área de almacenamiento efectiva de la celda $[\mathrm{L}^2]$

En el flujo de trabajo de cuadrícula gruesa validado, $A_{\mathrm{eff}}$ es el área de la celda.
El código luego impone
$$
h^{t+\Delta t} \ge 0
$$
de modo que nunca se permitan profundidades de agua negativas.
---

### 1.12 Condiciones límite de salida

HydroPol2D admite dos tratamientos de salida en el solucionador inercial local.
#### 1.12.1 Salida de profundidad normal

Cuando `outlet_type = 1`, la pendiente de salida se impone como una pendiente prescrita de flujo normal.
$$
S_0 = s_{\mathrm{outlet}}
$$
y la descarga de salida se calcula con la ecuación de Manning.
#### 1.12.2 Salida de profundidad crítica

Cuando `outlet_type \ne 1`, HydroPol2D calcula un control de salida similar a pendiente crítica a partir de la profundidad y rugosidad locales. En ambos casos, el flujo de salida se convierte a una tasa equivalente a la profundidad y se resta de la profundidad final del agua durante la actualización.
Este tratamiento de salida permite que el solucionador inercial local permanezca integrado dentro de un dominio ráster mientras sigue aplicando una condición de límite físicamente interpretable en el perímetro del dominio.
---

### 1.13 Interacción entre el depósito y el control hidráulico

El solucionador inercial local también se puede modificar internamente mediante controles de curva de clasificación o almacenamiento. Cuando el enrutamiento del yacimiento está activo, HydroPol2D impone relaciones de descarga de la forma
$$
Q = k\,(h-h_0)^m
$$
sujeto a limitaciones de agua disponibles y conexiones aguas abajo definidas por el usuario. En la implementación actual, se admite la lógica de control de dos etapas. El volumen descargado resultante se transfiere directamente a las celdas aguas abajo designadas.
Esto significa que el solucionador inercial local no es un bloque de enrutamiento cerrado; es un núcleo de enrutamiento que puede modificarse localmente mediante estructuras de control hidráulico.
---

### 1.14 Por qué el modelo inercial local es el predeterminado en HydroPol2D

La formulación inercial local es el método de enrutamiento predeterminado en HydroPol2D por tres razones.
Primero, conserva la hidráulica dominante necesaria para la propagación de inundaciones:
- gradiente de presión en superficie libre,
- fricción,
- aceleración local.

En segundo lugar, es lo suficientemente eficiente desde el punto de vista computacional como para usarse en grandes dominios ráster y bajo ejecución de GPU.
En tercer lugar, se integra naturalmente con el acoplamiento de procesos validado de HydroPol2D:
- controles hidráulicos,
- condiciones de salida,
- y acoplamiento hidrológico fuente-sumidero.

Por estos motivos, proporciona el mejor equilibrio entre realismo físico y manejabilidad computacional para la mayoría de las aplicaciones HydroPol2D.
---

### 1.15 Modelo submalla de Neal (2012)

HydroPol2D incluye la formulación rectangular de canal submalla propuesta por [Neal et al. (2012)](https://doi.org/10.1029/2012WR012514). Esta extensión se usa cuando el río es más estrecho que la celda ráster. El canal se embebe en la celda gruesa, mientras que el flujo bidimensional se mantiene en la llanura que rodea el canal.

Sea $\Delta x$ el ancho de la celda, $z_f$ la elevación de la llanura, $H$ la altura de la margen y $w$ el ancho del canal, con $0<w<\Delta x$. La elevación del lecho del canal es

$$
z_c=z_f-H.
$$

La profundidad $h$ se mide sobre $z_c$. El agua permanece en el canal rectangular cuando $h\le H$ y se extiende sobre la celda gruesa cuando $h>H$.

#### Flujo del canal en una cara

La elevación de la superficie del agua en el canal es

$$
y_c=z_c+h.
$$

Para celdas adyacentes $i$ y $j$, la pendiente de la superficie y la profundidad de flujo en la cara son

$$
S_c=\frac{y_{c,j}-y_{c,i}}{\Delta x},
$$

$$
h_{c,f}=\max\!\left[\max(y_{c,i},y_{c,j})-
\max(z_{c,i},z_{c,j}),0\right].
$$

El ancho compartido del canal es

$$
w_{c,f}=\min(w_i,w_j).
$$

El área de flujo y el radio hidráulico del canal son

$$
A_c=w_{c,f}h_{c,f},
\qquad
R_c=\frac{A_c}{w_{c,f}+2h_{c,f}}.
$$

El caudal del canal se actualiza mediante la ecuación inercial local

$$
Q_c^{t+\Delta t}=
\frac{Q_c^t-gA_c\Delta t S_c}
{1+g\Delta t n_c^2|Q_c^t|/(R_c^{4/3}A_c)},
$$

donde $n_c$ es el coeficiente de Manning del canal.

#### Flujo de la llanura en una cara

La profundidad sobre la llanura se mide sobre el DEM grueso:

$$
h_f=\max(h+z_c-z_f,0),
\qquad y_f=z_f+h_f.
$$

La pendiente y la profundidad en la cara de la llanura se calculan a partir de $y_f$ y $z_f$, de la misma forma que los términos del canal. La actualización inercial local usa el caudal unitario $q_f$:

$$
q_f^{t+\Delta t}=
\frac{q_f^t-gh_{f,f}\Delta t S_f}
{1+g\Delta t n_f^2|q_f^t|/h_{f,f}^{7/3}},
$$

donde $n_f$ es el coeficiente de Manning de la llanura. Los caudales de la llanura y de la cara completa son

$$
Q_f=q_f(\Delta x-w_{c,f}),
\qquad
Q=Q_c+Q_f.
$$

HydroPol2D aplica esta separación en las caras ortogonales D4. La salida usa los mismos componentes de canal y llanura que las caras internas.

#### Transición conservativa del almacenamiento

La ecuación de continuidad de la celda se evalúa en términos de volumen. Para una celda con canal,

$$
V(h)=
\begin{cases}
\Delta x\,w\,h, & h\le H,\\[4pt]
\Delta x\,w\,H+\Delta x^2(h-H), & h>H.
\end{cases}
$$

Por tanto, el área activa de la superficie $\mathrm{d}V/\mathrm{d}h$ cambia de $\Delta xw$, dentro de las márgenes, a $\Delta x^2$, sobre las márgenes. Los flujos de enrutamiento y los términos hidrológicos de fuente o sumidero actualizan primero $V$. Después, HydroPol2D invierte la misma relación por tramos para recuperar $h$. Este procedimiento evita una discontinuidad de masa al cruzar la altura de la margen.

La configuración activa y los datos geométricos se describen en [Banderas del modelo](../configuration/flags). Los resultados de las pruebas controladas se presentan en [Validación del modelo submalla de Neal (2012)](../validation/neal-subgrid).

### 1.16 Resumen

En HydroPol2D, el modelo inercial local es una formulación de enrutamiento basada en ráster integrada en profundidad en la que:
- primero se reconstruye la elevación de la superficie del agua de la celda,
- Los taludes en superficie libre se evalúan en las caras,
- las profundidades efectivas de la cara se calculan hidrostáticamente,
- las descargas frontales se actualizan con una ecuación inercial local tipo Bates,
- los flujos resultantes se convierten en descargas volumétricas,
- y la profundidad del agua se actualiza mediante un equilibrio conservador del volumen de las células.

El solucionador admite:
- el esquema Bates original,
- un esquema estabilizado contra el viento,
- un esquema estabilizado centrado,
- controles de salida,
- controles de depósito,
- manejo frontal mojado-seco,
- Límites críticos de flujo y velocidad.

Esto lo convierte en el principal motor hidrodinámico de HydroPol2D para el enrutamiento físico del flujo superficial.
---

## 2. Enrutamiento de flujo de impulso total

### 2.1 Justificación general

HydroPol2D también incluye un **solucionador de momento total para aguas poco profundas** para casos en los que la aproximación inercial local no es suficiente. Esta opción está destinada a aplicaciones y puntos de referencia hidráulicos controlados donde la aceleración convectiva, la propagación de ondas o los efectos dinámicos más fuertes deben representarse de manera más explícita.
El modelo de momento total resuelve las ecuaciones bidimensionales conservadoras de aguas poco profundas en la cuadrícula ráster. En HydroPol2D, esto se implementa como un núcleo de enrutamiento de volumen finito con almacenamiento explícito y estados de impulso.
El solucionador se activa a través del indicador de enrutamiento de momento total en la configuración del modelo. Debe utilizarse como alternativa, no simultáneamente, al enrutamiento local inercial, cinemático, difusivo, D8 o CA.
---

### 2.2 Ecuaciones conservadoras de aguas poco profundas

El vector de estado conservado es
$$
\mathbf{U}
=
\begin{bmatrix}
h \\
hu \\
hv
\end{bmatrix}
$$
dónde:
- $h$ es la profundidad del agua $[\mathrm{L}]$
- $u$ es la velocidad promedio en profundidad en la dirección $x$ $[\mathrm{L}\,\mathrm{T}^{-1}]$
- $v$ es la velocidad promedio en profundidad en la dirección $y$ $[\mathrm{L}\,\mathrm{T}^{-1}]$
- $hu$ y $hv$ son descargas unitarias o variables de momento $[\mathrm{L}^2\,\mathrm{T}^{-1}]$

Las ecuaciones gobernantes se escriben como
$$
\frac{\partial \mathbf{U}}{\partial t}+
\frac{\partial \mathbf{F}(\mathbf{U})}{\partial x}+
\frac{\partial \mathbf{G}(\mathbf{U})}{\partial y}
=
\mathbf{S}_{\mathrm{bed}}+
\mathbf{S}_{\mathrm{fric}}
$$
con flujos
$$
\mathbf{F}(\mathbf{U})
=
\begin{bmatrix}
hu \\
\dfrac{(hu)^2}{h} + \dfrac{1}{2}gh^2 \\
\dfrac{(hu)(hv)}{h}
\end{bmatrix}
$$
y
$$
\mathbf{G}(\mathbf{U})
=
\begin{bmatrix}
hv \\
\dfrac{(hu)(hv)}{h} \\
\dfrac{(hv)^2}{h} + \dfrac{1}{2}gh^2
\end{bmatrix}
$$
donde $g$ es la aceleración gravitacional.
Los términos de origen de la pendiente del lecho representan el forzamiento topográfico:
$$
\mathbf{S}_{\mathrm{bed}}
=
\begin{bmatrix}
0 \\
-gh\,\dfrac{\partial z}{\partial x} \\
-gh\,\dfrac{\partial z}{\partial y}
\end{bmatrix}
$$
y los términos de la fuente de fricción representan la resistencia Manning.
---

### 2.3 Flujos numéricos y memoria de impulso

HydroPol2D calcula flujos de momento total con un solucionador de volumen finito tipo HLL. En cada cara de celda, se utilizan estados reconstruidos izquierdo y derecho para calcular el flujo de masa y el flujo de momento. La actualización es conservadora en el sentido de que el flujo que sale de una celda ingresa a la celda adyacente con signo opuesto.
A diferencia del solucionador inercial local, el modelo de momento total debe transportar el impulso de un paso de tiempo al siguiente. HydroPol2D almacena:
- el actual estado $hu$ centrado en las células,
- el estado actual $hv$ centrado en la celda,
- flujos de masa de cara convertidos nuevamente a unidades de tasa de profundidad HydroPol2D,
- términos del fregadero de salida.

Esta memoria de impulso es lo que hace que el modelo sea un verdadero solucionador de ondas dinámicas en lugar de un recálculo de descarga basado únicamente en la pendiente actual de la superficie del agua.
---

### 2.4 Pendiente del lecho, fricción y tratamiento de mojado-secado

El solucionador de momento completo incluye varias protecciones numéricas para la simulación de inundaciones ráster:
- las células secas e inactivas se tratan como paredes sólidas;
- se limpian celdas muy poco profundas para evitar velocidades indefinidas;
- el impulso está limitado por una velocidad máxima admisible;
- La fricción Manning se aplica con una actualización semiimplícita o implícita exacta;
- un limitador de drenaje evita que un fundente frontal elimine más agua de la disponible.

La actualización de fricción Manning amortigua el impulso según la profundidad local, la rugosidad y la magnitud de la velocidad. Conceptualmente, los componentes del impulso se relajan mediante un denominador de la forma
$$
1 + g\,n^2\,\Delta t\,\frac{\sqrt{u^2+v^2}}{h^{4/3}}
$$
donde $n$ es el coeficiente de rugosidad de Manning. Esto evita un impulso irrealmente grande en aguas poco profundas y al mismo tiempo conserva la propagación dinámica donde la profundidad del agua es suficiente.
La reconstrucción hidrostática está disponible para terrenos complejos y un tratamiento de pendiente de lecho bien equilibrado, mientras que la ruta de referencia controlada predeterminada utiliza el tratamiento robusto de flujo/fuente HLL implementado en el solucionador actual.
---

### 2.5 Actualización de continuidad y acoplamiento HydroPol2D

Después de calcular los flujos HLL, la actualización de profundidad sigue el equilibrio de volumen finito:
$$
h^{t+\Delta t}
=
h^t-
\frac{\Delta t}{\Delta x}
\left(
F_h^{E} - F_h^{W}+
G_h^{N} - G_h^{S}
\right)
$$
donde $F_h$ y $G_h$ son los componentes del flujo de masa a través de las caras de la celda.
HydroPol2D luego convierte los flujos faciales a la misma convención contable utilizada por el resto del modelo:
$$
q_{\mathrm{mm/h}}
=
\frac{Q}{A_{\mathrm{cell}}}
1000
3600
$$
Esto permite que el solucionador de impulso total siga siendo compatible con los términos hidrológicos de fuente/sumidero, transporte de calidad del agua, controles de embalses y diagnósticos de condiciones límite.
---

### 2.6 Condiciones de contorno y controles hidráulicos

El modelo de impulso total admite la misma arquitectura práctica de condiciones de contorno utilizada por el enrutamiento HydroPol2D:
- paredes reflectantes cerradas a lo largo de caras inactivas o exteriores,
- celdas de sumidero de salida con comportamiento de profundidad normal o profundidad crítica,
- límites impuestos del hidrograma de entrada,
- límites del hidrograma de etapa prescritos,
- yacimientos y estructuras de control de la curva de calificación interna.

Para límites cerrados, el flujo de masa normal es cero, pero los efectos de la presión de la pared se tienen en cuenta en la actualización del impulso. Esto es importante para un comportamiento estable cerca de los bordes del dominio y de las celdas inactivas.
Los flujos de salida se convierten en un sumidero de volumen y se retiran del almacenamiento de agua local, sujeto a las limitaciones de agua disponible.
---

### 2.7 Evidencia de validación actual

El solucionador de impulso total es parte de la suite de validación. La evidencia actual lista para informes incluye:
- escorrentía en plano inclinado contra el límite analítico de onda cinemática;
- Verificaciones de conservación de masa y simetría bilateral de cuencas inclinadas en V;
- Perfiles analíticos de rotura de presas en lecho seco de Ritter;
- propagación de ondas continuas y comparación de perfiles;
- cumplimiento prescrito de los límites de las etapas;
- hidrograma de entrada y contabilidad de yacimientos/estructuras de control cuando se utiliza el enrutamiento de momento total.

Estas pruebas validan la implementación de impulso total como una opción de enrutamiento de onda dinámica controlada. No implican calibración de campo para una cuenca en particular.
---

### 2.8 Uso práctico del solucionador full momentum

El solucionador full momentum está pensado para simulaciones en las que los términos adicionales de advección y aceleración local justifican el mayor costo computacional. En HydroPol2D debe tratarse como una elección propia de familia de enrutamiento, no como un complemento de los modos más livianos.
---

## 3. Enrutamiento D4 difusivo y cinemático

HydroPol2D implementa enrutamiento de ondas **difusivas** y **cinemáticas** a través de un solucionador conservador compartido D4. Estos modos son más livianos que los solucionadores locales inerciales y de momento total, pero aún usan flujos explícitos basados ​​en caras, actualizaciones de volumen conservadoras, manejo de salida y acoplamiento entre depósito y control.
### 3.1 Estructura de enrutamiento conservadora compartida

En ambos modos, HydroPol2D dirige el agua a través de los cuatro vecinos ortogonales de cada celda y actualiza la profundidad de la celda a través de un equilibrio de volumen conservador:
$$
h^{t+\Delta t}
=
h^t+
\frac{V_{\mathrm{in}} - V_{\mathrm{out}}}{A_{\mathrm{cell}}}
$$
dónde:
- $h$ es la profundidad del agua de la celda $[\mathrm{L}]$
- $V_{\mathrm{in}}$ y $V_{\mathrm{out}}$ son volúmenes entrantes y salientes en el subpaso $[\mathrm{L}^3]$
- $A_{\mathrm{cell}}$ es el área de la celda activa $[\mathrm{L}^2]$

El intervalo de enrutamiento se subdivide internamente cuando es necesario. El código actual estima el número de subpasos a partir de una estimación de velocidad de tipo Manning y un objetivo de estilo Courant para que pendientes pronunciadas o aguas profundas no desestabilicen la actualización explícita.
### 3.2 Modo difusivo

En modo difusivo, la pendiente de conducción es la **pendiente de la superficie del agua** entre celdas adyacentes. Para una cara compartida por las celdas izquierda y derecha,
$$
eta = z + h
$$
$$
S_f = \frac{\eta_L - \eta_R}{\Delta x}
$$
con profundidad de frente reconstruida hidrostáticamente
$$
H_f = \max\!\left(\max(\eta_L,\eta_R) - z_f,\,0\right)
$$
Luego se evalúa la descarga de la unidad frontal con una ley de flujo de tipo Manning:
$$
q_f
=
\nombredeloperador{sign}(S_f)
\frac{H_f^{5/3}}{n}\sqrt{|S_f|}
$$

Este modo puede representar una redistribución similar a un remanso impulsada por los gradientes de la superficie del agua y, al mismo tiempo, sigue siendo mucho más barato que resolver una ecuación de impulso.
### 3.3 Modo cinemático

En modo cinemático, la pendiente de conducción es la **pendiente del fondo**, no la pendiente de la superficie del agua:
$$
S_b = \frac{z_L - z_R}{\Delta x}
$$
Luego, el código aplica una regla de profundidad del donante:
- si $S_b > 0$, la celda izquierda es la donante y su profundidad impulsa el flujo,
- si $S_b &lt; 0$, la celda derecha es la donante y su profundidad impulsa el flujo.

Usando la profundidad del donante $H_{\mathrm{donor}}$, la descarga unitaria es
$$
q_f
=
\nombredeloperador{sign}(S_b)
\frac{H_{\mathrm{donor}}^{5/3}}{n_{\mathrm{donor}}}\sqrt{|S_b|}
$$

Esto hace que la ruta cinemática esté estrictamente dirigida a la pendiente y evita que represente el mismo comportamiento de remanso capturado por los solucionadores difusos, inerciales o de momento total.
### 3.4 Controles compartidos, manejo de salida y acoplamiento

Ambos modos de onda D4 comparten la misma maquinaria de enrutamiento conservadora para:
- subpaso interno,
- limitación del almacenamiento disponible para que una célula donada no pueda exportar más volumen del que contiene,
- limitación de flujo crítico opcional,
- eliminación de descarga de salida,
- interacción entre el depósito y el control hidráulico.

Al igual que con las otras familias de rutas, la lluvia, la infiltración, la evapotranspiración, la retroalimentación de las aguas subterráneas y otros términos de fuente/sumidero son manejados por el marco HydroPol2D acoplado en torno a la actualización de rutas.
### 3.5 Alcance y advertencias

Los modos cinemático y difusivo D4 son parte de la familia de enrutamiento implementada y se utilizan en los puntos de referencia de validación controlados actuales. Sin embargo:
- deben tratarse como alternativas, no como combinaciones, de inercia local o de impulso total,
- El apoyo al D8 debe considerarse una vía secundaria de alcance limitado en lugar de una familia de teorías paralelas.
---

## 4. Enrutamiento de flujo de autómatas celulares

### 4.1 Formulación conceptual

Además del modelo inercial local, HydroPol2D proporciona un **esquema de enrutamiento de autómatas celulares (CA)** como una alternativa simplificada para la propagación del flujo superficial.
El modelo CA se basa en la **redistribución local del volumen de agua entre celdas vecinas**, impulsada por diferencias en la elevación de la superficie del agua. A diferencia de la formulación inercial local, este enfoque:
- no resuelve explícitamente una ecuación de momento,
- no rastrea la velocidad o la descarga en las caras,
- se basa en reglas empíricas de redistribución del flujo,
- asegura una estricta conservación de la masa a nivel celular.

Esta formulación es particularmente útil para:
- estimación rápida de la extensión de las inundaciones,
- simulaciones a gran escala donde la eficiencia computacional es crítica,
- Casos en los que no se requiere una dinámica hidráulica detallada.

---

### 4.2 Representación de la superficie del agua

Como en el modelo inercial, la variable determinante es la elevación de la superficie del agua:
$$
eta = z + h
$$
dónde:
- $\eta$ = elevación de la superficie del agua $[\mathrm{L}]$
- $z$ = elevación de la cama $[\mathrm{L}]$
- $h$ = profundidad del agua $[\mathrm{L}]$

---

### 4.3 Pendiente de conducción y dirección del flujo

El flujo entre una celda $i$ y una celda vecina $j$ está impulsado por la diferencia:
$$
\Delta \eta_{i,j} = \eta_i - \eta_j
$$
Sólo los gradientes positivos contribuyen al flujo:
$$
\Delta \eta_{i,j} > 0
$$
Esto garantiza que el agua fluya solo **cuesta abajo en términos de superficie libre**, evitando el reflujo no físico.
---

### 4.4 Volumen transferible disponible

El volumen potencial que se puede transferir desde la celda $i$ a la vecina $j$ se estima como:
$$
V_{i,j} = A_{\mathrm{cell}} \cdot \max(\Delta \eta_{i,j}, 0)
$$
dónde:
- $V_{i,j}$ = volumen transferible $[\mathrm{L}^3]$
- $A_{\mathrm{cell}}$ = área de celda $[\mathrm{L}^2]$

---

### 4.5 Partición del flujo

El volumen total transferible de una celda se distribuye entre sus vecinas proporcionalmente:
$$
w_{i,j} =
\frac{
V_{i,j}
{}
\sum_k V_{i,k} + \varepsilon
}
$$
dónde:
- $w_{i,j}$ = peso asignado al vecino $j$
- $\varepsilon$ = pequeña constante numérica para evitar la división por cero

El flujo total de salida de la celda es entonces:
$$
I_{i,j} = w_{i,j} \cdot I_{\mathrm{tot}}
$$
dónde:
- $I_{\mathrm{tot}}$ = volumen total saliente $[\mathrm{L}^3]$

---

### 4.6 Estimación de velocidad

Aunque el modelo CA no resuelve explícitamente las ecuaciones de momento, se estima una velocidad característica utilizando la ecuación de Manning:
$$
u = \frac{1}{n} h^{2/3} S^{1/2}
$$
dónde:
- $u$ = velocidad del flujo $[\mathrm{L}\mathrm{T}^{-1}]$
- $n$ = coeficiente Manning $[\mathrm{T}\mathrm{L}^{-1/3}]$
- $S$ = pendiente $[-]$

Esta velocidad se utiliza para controlar la **tasa de redistribución del agua**.
---

### 4.7 Cálculo del flujo de salida

El flujo total de salida de una celda se calcula como:
$$
I_{\mathrm{tot}} = u \cdot h \cdot \Delta t \cdot W_{\mathrm{eff}}
$$
dónde:
- $I_{\mathrm{tot}}$ = volumen total saliente $[\mathrm{L}^3]$
- $\Delta t$ = paso de tiempo $[\mathrm{T}]$
- $W_{\mathrm{eff}}$ = ancho de flujo efectivo $[\mathrm{L}]$

---

### 4.8 Actualización de profundidad

Después de la redistribución, la profundidad del agua se actualiza como:
$$
h^{t+\Delta t}
=
h^t+
\frac{
\sum Q_{\mathrm{in}} - \sum Q_{\mathrm{out}}
{}
A___mathrm{cell}}
}
$$
dónde:
- $Q_{\mathrm{in}}$ = volumen entrante $[\mathrm{L}^3]$
- $Q_{\mathrm{out}}$ = volumen saliente $[\mathrm{L}^3]$

El modelo impone:
$$
h^{t+\Delta t} \ge 0
$$
asegurando la consistencia física.
---

### 4.9 Estabilidad y robustez

El modelo CA es inherentemente estable porque:
- el flujo está limitado por el volumen de agua disponible,
- la redistribución está limitada por gradientes locales,
- no hay términos de aceleración explícitos presentes.

Sin embargo, el método es:
- más difusivo que el modelo inercial local,
- menos preciso para representar procesos hidráulicos dinámicos,
- no es adecuado para capturar la propagación de ondas o los efectos de remanso.

---

### 4.10 Comparación con el modelo inercial local

| Característica | Modelo inercial local | Autómatas celulares |
|--------|----------------------|-------------------|
| Física | Basado en impulso | Empírico |
| variables | $q$, $h$, $\eta$ | $h$, $\eta$ |
| Exactitud | Alto | Moderado |
| Estabilidad | Condicional | muy alto |
| Costo computacional | Moderado | Bajo |
| Dinámica de inundaciones | bien capturado | Difusivo |

---

### 4.11 Cuándo utilizar el modelo CA

El modelo Autómata Celular se recomienda cuando:
- Se requieren simulaciones a gran escala.
- la velocidad computacional es una prioridad,
- sólo se necesita la extensión de la inundación o las profundidades aproximadas,
- El comportamiento hidráulico detallado no es crítico.

Para la propagación de inundaciones basada físicamente, el **Modelo Inercial Local sigue siendo la opción preferida**.
---

## Resumen

HydroPol2D admite una familia de enrutamiento que ahora incluye públicamente:
- **enrutamiento inercial local** como solucionador de inundaciones basado físicamente predeterminado,
- **enrutamiento de impulso total** para puntos de referencia de ondas dinámicas y efectos de impulso más fuertes,
- **D4 difusivo** enrutamiento impulsado por la pendiente de la superficie del agua,
- **enrutamiento cinemático D4** impulsado por la pendiente del lecho y la profundidad del donante,
- **autómatas celulares** enrutamiento para una redistribución rápida y simplificada.

Todas estas rutas comparten el acoplamiento más amplio de HydroPol2D con entradas hidrológicas, retroalimentación de aguas subterráneas, contabilidad de salidas y controles hidráulicos, pero solo una formulación de ruta principal debe estar activa en un tramo determinado. D8 sigue siendo de alcance secundario.
