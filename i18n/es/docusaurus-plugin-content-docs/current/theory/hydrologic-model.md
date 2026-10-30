---
title: Modelo hidrológico
---
import useBaseUrl from '@docusaurus/useBaseUrl';

# Modelo hidrológico

El componente hidrológico de HydroPol2D gobierna la partición de la entrada atmosférica en interceptación, caída, infiltración, evapotranspiración, acumulación y derretimiento de nieve, almacenamiento en zonas vadosas, recarga de agua subterránea y retroalimentación de agua subterránea a la superficie terrestre.
A escala celular, el modelo hidrológico determina cuánta agua:
- se almacena temporalmente junto al dosel,
- llega a la superficie del suelo,
- se infiltra en el suelo,
- permanece almacenado en la zona vadosa,
- recarga el agua subterránea,
- regresa a la superficie por exfiltración,
- o se elimina por evaporación y transpiración.

Estos procesos se evalúan secuencialmente dentro de cada paso de tiempo y proporcionan el forzamiento hidrológico para el modelo hidrodinámico.

---

## 1. Balance Hidrológico Conceptual

A nivel conceptual, el equilibrio hidrológico de una celda de la cuadrícula se puede escribir como
$$
\frac{\partial d}{\partial t}
=
P_{\mathrm{eff}}
+
M_{\mathrm{snow}}
+
q_{\mathrm{exf}}
-
i
-
E_{\mathrm{surf}}
-
T_{\mathrm{r}}
+
q_{\mathrm{src}}
-
q_{\mathrm{sink}}
$$
dónde:
- $d$ es la profundidad del agua superficial $[\mathrm{L}]$
- $P_{\mathrm{eff}}$ es la lluvia efectiva que llega al suelo $[\mathrm{L}\,\mathrm{T}^{-1}]$
- $M_{\mathrm{snow}}$ es la contribución del deshielo $[\mathrm{L}\,\mathrm{T}^{-1}]$
- $q_{\mathrm{exf}}$ es la exfiltración de agua subterránea a la superficie $[\mathrm{L}\,\mathrm{T}^{-1}]$
- $i$ es la tasa de infiltración $[\mathrm{L}\,\mathrm{T}^{-1}]$
- $E_{\mathrm{surf}}$ es la tasa de evaporación del almacenamiento en superficie $[\mathrm{L}\,\mathrm{T}^{-1}]$
- $T_{\mathrm{r}}$ es la tasa de transpiración $[\mathrm{L}\,\mathrm{T}^{-1}]$
- $q_{\mathrm{src}}$ y $q_{\mathrm{sink}}$ son términos de origen y sumidero impuestos adicionales $[\mathrm{L}\,\mathrm{T}^{-1}]$

No todos los términos están activos simultáneamente. Su activación depende de la configuración de forzado seleccionada y de los indicadores del modelo. Sin embargo, este equilibrio proporciona el marco conceptual utilizado para organizar todos los flujos verticales que actúan sobre una celda de la cuadrícula.

---

## 2. Intercepción, caída y flujo del tallo del dosel

HydroPol2D representa la interceptación del dosel utilizando un modelo de interceptación basado en almacenamiento en el que la precipitación bruta se divide en:
- almacenamiento de dosel,
- caída,
- evaporación del dosel,
- y flujo de tallo.

La rutina de interceptación recibe:
- precipitación bruta $P_{\mathrm{gross}}$,
- evaporación potencial $E_{\mathrm{p}}$,
- índice de área foliar $\mathrm{LAI}$,
- almacenamiento de dosel anterior $S_{\mathrm{can,prev}}$,
- coeficiente de almacenamiento del dosel $C_{\mathrm{can}}$,

y devuelve el almacenamiento de dosel actualizado $S_{\mathrm{can}}$, el paso $T_{\mathrm{f}}$, la evaporación del agua interceptada $E_{\mathrm{can}}$ y el flujo de tallo $F_{\mathrm{stem}}$.
Este paso de interceptación controla qué cantidad de la entrada de agua atmosférica es retenida temporalmente por la vegetación y cuánta se transfiere a la superficie del suelo durante el paso de tiempo actual.
### 2.1 Almacenamiento máximo en la cubierta

El almacenamiento máximo de interceptación se calcula como
$$
S_{\mathrm{can,max}} = C_{\mathrm{can}} \,\mathrm{LAI}
$$
dónde:
- $S_{\mathrm{can,max}}$ es el almacenamiento máximo de agua del dosel $[\mathrm{L}]$
- $C_{\mathrm{can}}$ es el coeficiente de almacenamiento del dosel $[\mathrm{L}]$
- $\mathrm{LAI}$ es el índice del área foliar $[-]$

Esta relación implica que la vegetación con mayor área foliar puede almacenar más agua interceptada.
### 2.2 flujo de tallo

El código incluye una rutina de flujo de tallo basada en una función de retardo. Las expresiones intermedias son
$$
\tau_{\mathrm{stem}}
=
T_0 \exp\!\left(-\alpha_{\mathrm{stem}} P_{\mathrm{gross}}\right)
$$
y
$$
F_ {\mathrm{stem}}
=
f_ {\mathrm{stem}}
\,
\frac{S_{\mathrm{can,prev}}}{\tau_{\mathrm{stem}}/60}
$$
dónde:
- $\tau_{\mathrm{stem}}$ es el retraso del flujo de tallo $[\mathrm{T}]$
- $T_0$ es el parámetro de retardo máximo $[\mathrm{T}]$
- $\alpha_{\mathrm{stem}}$ es el coeficiente de caída del flujo del tallo $[-]$
- $f_{\mathrm{stem}}$ es la fracción del flujo del tallo $[-]$
- $F_{\mathrm{stem}}$ es flujo de tallo $[\mathrm{L}]$

En la implementación actual de HydroPol2D, el flujo de tallo se desactiva imponiendo explícitamente
$$
F_{\mathrm{stem}} = 0
$$
Por lo tanto, el flujo de tallos no contribuye actualmente al equilibrio hídrico superficial, aunque la estructura de la rutina se mantiene en el código.
### 2.3 Evaporación del almacenamiento de interceptación

La fracción de almacenamiento del dosel expuesta a la evaporación se define como
$$
\beta = \frac{S_{\mathrm{can,prev}}}{S_{\mathrm{can,max}}}
$$
y la evaporación del dosel se calcula entonces como
$$
E_{\mathrm{can}} = \beta \, E_{\mathrm{p}}
$$
sujeto a la restricción
$$
E_{\mathrm{can}} \le P_{\mathrm{gross}} + S_{\mathrm{can,prev}}
$$
dónde:
- $\beta$ es la fracción del almacenamiento de la cubierta llena al comienzo del paso de tiempo $[-]$
- $E_{\mathrm{can}}$ es la evaporación del almacenamiento de interceptación $[\mathrm{L}]$
- $E_{\mathrm{p}}$ es la evaporación potencial durante el paso de tiempo $[\mathrm{L}]$

Esta formulación supone que la evaporación del dosel es proporcional a la fracción de almacenamiento ocupada al comienzo del paso de tiempo, al mismo tiempo que impone que la evaporación no puede exceder el agua realmente disponible en la precipitación más el agua de interceptación almacenada.
### 2.4 Actualización del almacenamiento de interceptación

El incremento del almacenamiento del dosel se calcula como
$$
\Delta S_{\mathrm{can}} = P_{\mathrm{gross}} - F_{\mathrm{stem}} - E_{\mathrm{can}}
$$
y el almacenamiento provisional se convierte
$$
S_{\mathrm{can}}^{\ast} = S_{\mathrm{can,prev}} + \Delta S_{\mathrm{can}}
$$
Luego, el rendimiento se calcula como el exceso por encima de la capacidad de almacenamiento del dosel:
$$
T_{\mathrm{f}} = \max\left(S_{\mathrm{can}}^{\ast} - S_{\mathrm{can,max}},\,0\right)
$$
Finalmente, el almacenamiento de la marquesina se trunca a su valor máximo admisible:
$$
S_{\mathrm{can}} = \min\left(S_{\mathrm{can}}^{\ast},\,S_{\mathrm{can,max}}\right)
$$
dónde:
- $\Delta S_{\mathrm{can}}$ es el incremento de almacenamiento de la cubierta a lo largo del paso de tiempo $[\mathrm{L}]$
- $S_{\mathrm{can}}^{\ast}$ es el almacenamiento provisional en la cubierta antes del truncamiento $[\mathrm{L}]$
- $T_{\mathrm{f}}$ es total $[\mathrm{L}]$
- $S_{\mathrm{can}}$ es el almacenamiento final del dosel $[\mathrm{L}]$

Esta secuencia refleja la suposición física de que la precipitación primero llena el almacenamiento del dosel. Una vez que el dosel alcanza su capacidad de almacenamiento, el exceso de agua se libera como paso.
### 2.5 La lluvia efectiva pasó a la superficie

La lluvia disponible en la superficie terrestre se define como
$$
P_{\mathrm{eff}} = T_{\mathrm{f}} + F_{\mathrm{stem}}
$$
dónde:
- $P_{\mathrm{eff}}$ es la lluvia efectiva que llega al suelo $[\mathrm{L}]$
- $T_{\mathrm{f}}$ es el paso directo $[\mathrm{L}]$
- $F_{\mathrm{stem}}$ es flujo de tallo $[\mathrm{L}]$

Según la implementación actual, dado que el flujo por tallos está desactivado, la lluvia efectiva es igual a la precipitación total. En términos prácticos, $P_{\mathrm{eff}}$ representa la cantidad de agua líquida transferida desde el sistema atmósfera-dosel a la superficie terrestre durante el paso de tiempo, antes de la ruta hidrodinámica.
Si la rutina de interceptación está desactivada, entonces no se resuelve ningún almacenamiento en el dosel y la precipitación llega directamente a la superficie, de modo que
$$
P_{\mathrm{eff}} = P_{\mathrm{gross}}
$$
### 2.6 Aplicación de la lluvia
Para aplicaciones validadas, la precipitación que ingresa al módulo de interceptación se aplica sobre la celda del modelo activo como:
$$
P_{\mathrm{int}} = \Delta P_{\mathrm{agg}}
$$
donde $\Delta P_{\mathrm{agg}}$ es la profundidad de lluvia agregada durante el paso de tiempo del modelo.

---

## 3. Evapotranspiración y evaporación potencial

HydroPol2D calcula la evapotranspiración de referencia distribuida espacialmente utilizando una formulación de Penman-Monteith. Los datos de la estación meteorológica primero se interpolan sobre la cuadrícula usando ponderación de distancia inversa, y los campos interpolados luego se usan para calcular tanto la evapotranspiración de referencia $\mathrm{ETP}$ como un término similar a la evaporación $E_{\mathrm{p}}$.
La cantidad $\mathrm{ETP}$ se utiliza como evapotranspiración de referencia estándar, mientras que $E_{\mathrm{p}}$ se utiliza en la rutina de interceptación para estimar la evaporación del agua interceptada del dosel.
### 3.1 Interpolación espacial del forzamiento meteorológico

En cada paso de tiempo, los siguientes campos se interpolan a partir de las estaciones disponibles:
- $T_{\mathrm{max}}$ temperatura máxima del aire $[\Theta]$
- $T_{\mathrm{min}}$ temperatura mínima del aire $[\Theta]$
- $T_{\mathrm{air}}$ temperatura media del aire $[\Theta]$
- $U_2$ velocidad del viento en $2\,\mathrm{m}$ $[\mathrm{L}\,\mathrm{T}^{-1}]$
- $\mathrm{UR}$ humedad relativa $[-]$
- $G_{\mathrm{soil}}$ flujo de calor del suelo $[\mathrm{E}\,\mathrm{L}^{-2}\,\mathrm{T}^{-1}]$

Para una variable genérica $\phi$, el campo interpolado en la ubicación $\mathbf{x}$ se escribe conceptualmente como
$$
\phi(\mathbf{x})
=
\frac{
\sum_{i=1}^{N} w_i(\mathbf{x})\,\phi_i
}{
\sum_{i=1}^{N} w_i(\mathbf{x})
}
$$
con
$$
w_i(\mathbf{x}) \propto \frac{1}{d_i(\mathbf{x})^p}
$$
dónde:
- $\phi_i$ es el valor observado en la estación $i$
- $d_i(\mathbf{x})$ es la distancia desde la estación $i$ hasta la ubicación $\mathbf{x}$ $[\mathrm{L}]$
- $p$ es el parámetro de potencia de ponderación de distancia inversa $[-]$

En la interpolación sólo se retienen las estaciones con datos completos en el intervalo de tiempo actual. Este procedimiento produce campos de forzamiento distribuidos espacialmente que luego se utilizan en los cálculos de evapotranspiración.
### 3.2 Ecuación de Penman-Monteith

La evapotranspiración de referencia se calcula como
$$
\mathrm{ETP}
=
\frac{
0.408\,\Delta\,(R_n - G_{\mathrm{soil}})
+
\gamma
\left(
\frac{900\,U_2\,(e_s - e_a)}{T_{\mathrm{air}} + 273}
\right)
}{
\Delta + \gamma\left(1 + 0.34\,U_2\right)
}
$$
y el término similar a la evaporación es
$$
E_{\mathrm{p}}
=
\frac{
0.408\,\Delta\,(R_n - G_{\mathrm{soil}})
+
\gamma
\left(
\frac{900\,U_2\,(e_s - e_a)}{T_{\mathrm{air}} + 273}
\right)
}{
\Delta + \gamma
}
$$
dónde:
- $\mathrm{ETP}$ es la evapotranspiración de referencia $[\mathrm{L}\,\mathrm{T}^{-1}]$
- $E_{\mathrm{p}}$ es la evaporación potencial sin resistencia aerodinámica de la superficie en el denominador $[\mathrm{L}\,\mathrm{T}^{-1}]$
- $\Delta$ es la pendiente de la curva de presión de vapor de saturación $[\mathrm{P}\,\Theta^{-1}]$
- $R_n$ es la radiación neta $[\mathrm{E}\,\mathrm{L}^{-2}\,\mathrm{T}^{-1}]$
- $G_{\mathrm{soil}}$ es el flujo de calor del suelo $[\mathrm{E}\,\mathrm{L}^{-2}\,\mathrm{T}^{-1}]$
- $\gamma$ es la constante psicrométrica $[\mathrm{P}\,\Theta^{-1}]$
- $U_2$ es la velocidad del viento en $2\,\mathrm{m}$ $[\mathrm{L}\,\mathrm{T}^{-1}]$
- $e_s$ es la presión de vapor de saturación $[\mathrm{P}]$
- $e_a$ es la presión de vapor real $[\mathrm{P}]$
- $T_{\mathrm{air}}$ es la temperatura media del aire $[\Theta]$

Estas son las formas algebraicas implementadas en el código actual. La diferencia entre $\mathrm{ETP}$ y $E_{\mathrm{p}}$ radica en el denominador, lo que hace que $E_{\mathrm{p}}$ sea un término similar a la evaporación más directamente adecuado para las pérdidas por intercepción del dosel.
### 3.3 Términos de apoyo a la radiación y la atmósfera

HydroPol2D calcula los términos auxiliares de Penman-Monteith utilizando relaciones astronómicas y termodinámicas.
La declinación solar se calcula como
$$
\delta_{\mathrm{sol}}
=
0.409
\sin\!\left(
\frac{2\pi}{365}J - 1.39
\right)
$$
La distancia relativa entre la Tierra y el Sol es
$$
d_r = 1 + 0.033\cos\!\left(\frac{2\pi}{365}J\right)
$$
La radiación extraterrestre se calcula entonces como
$$
R_a
=
\frac{118.08}{\pi}
d_r
\left[
\omega_s \sin\phi \sin\delta_{\mathrm{sol}}
+
\cos\phi \cos\delta_{\mathrm{sol}} \sin\omega_s
\right]
$$
La radiación solar entrante se estima en
$$
R_s = K_{\mathrm{rs}} R_a \sqrt{T_{\mathrm{max}} - T_{\mathrm{min}}}
$$
La radiación de cielo despejado es
$$
R_{\mathrm{so}}
=
\left(
0.75 + 2\times10^{-5} z
\right) R_a
$$
La radiación neta de onda corta es
$$
R_{\mathrm{ns}} = (1-\alpha_{\mathrm{land}})\,R_s
$$
La radiación neta de onda larga es
$$
R_{\mathrm{nl}}
=
\sigma
\left(
\frac{
(T_{\mathrm{max}}+273.16)^4 + (T_{\mathrm{min}}+273.16)^4
}{2}
\right)
\left(
0.34 - 0.14\sqrt{e_a}
\right)
\left(
1.35\frac{R_s}{R_{\mathrm{so}}} - 0.35
\right)
$$
La radiación neta es entonces
$$
R_n = R_{\mathrm{ns}} - R_{\mathrm{nl}}
$$
La pendiente de la curva de presión de vapor de saturación se calcula como
$$
\Delta
=
\frac{
4098
\left[
0.6108\exp\!\left(
\frac{17.27\,T_{\mathrm{air}}}{T_{\mathrm{air}}+237.3}
\right)
\right]
}{
(T_{\mathrm{air}}+237.3)^2
}
$$
La presión atmosférica se estima como
$$
P_{\mathrm{atm}}
=
101.3
\left(
\frac{293 - 0.0065 z}{293}
\right)^{5.26}
$$
y la constante psicrométrica es
$$
\gamma = 0.665 \times 10^{-3} P_{\mathrm{atm}}
$$
dónde:
- $J$ es el día del año $[-]$
- $\delta_{\mathrm{sol}}$ es la declinación solar $[\mathrm{rad}]$
- $d_r$ es la distancia relativa entre la Tierra y el Sol $[-]$
- $R_a$ es radiación extraterrestre $[\mathrm{E}\,\mathrm{L}^{-2}\,\mathrm{T}^{-1}]$
- $\omega_s$ es el ángulo horario del amanecer $[\mathrm{rad}]$
- $\phi$ es la latitud $[\mathrm{rad}]$
- $R_s$ es la radiación solar entrante $[\mathrm{E}\,\mathrm{L}^{-2}\,\mathrm{T}^{-1}]$
- $K_{\mathrm{rs}}$ es el coeficiente de radiación empírico en la estimación de radiación entrante tipo Hargreaves $[-]$
- $R_{\mathrm{so}}$ es la radiación solar en cielo despejado $[\mathrm{E}\,\mathrm{L}^{-2}\,\mathrm{T}^{-1}]$
- $z$ es la elevación del terreno $[\mathrm{L}]$
- $R_{\mathrm{ns}}$ es la radiación neta de onda corta $[\mathrm{E}\,\mathrm{L}^{-2}\,\mathrm{T}^{-1}]$
- $\alpha_{\mathrm{land}}$ es el albedo de la superficie terrestre $[-]$
- $R_{\mathrm{nl}}$ es la radiación neta de onda larga $[\mathrm{E}\,\mathrm{L}^{-2}\,\mathrm{T}^{-1}]$
- $\sigma$ es la constante de Stefan-Boltzmann
- $P_{\mathrm{atm}}$ es la presión atmosférica $[\mathrm{P}]$

Estas expresiones se implementan explícitamente en la rutina de evapotranspiración y se evalúan en forma matricial en el dominio computacional.
### 3.4 Forzado directo por evaporación y transpiración

HydroPol2D también puede utilizar campos ráster de evaporación y transpiración suministrados externamente. En esa configuración, el modelo omite el cálculo interno de Penman-Monteith y aplica los campos $E_{\mathrm{surf}}$ y $T_{\mathrm{r}}$ prescritos directamente en el balance de masa hidrológico.

### 3.5 Estrés de Feddes en la absorción de agua por las raíces {#35-feddes-root-water-uptake-stress}

El estrés de Feddes es opcional. Reduce la transpiración del suelo cuando la zona de raíces está demasiado húmeda o demasiado seca (Feddes, Kowalik y Zaradny, 1978, *Simulation of Field Water Use and Crop Yield*, Pudoc, Wageningen).

| Modelo | Activación | Predeterminado |
|---|---|---|
| HydroPol2D-Python | `vertical.feddes.enabled: true` | desactivado |
| HydroPol2D (MATLAB) | `flag_feddes = 1` | `0` |

Funciona en ambos esquemas de subsuelo (predeterminado y [en capas](./layered-subsurface)), en la malla estructurada y en la malla de Voronoi.

El factor de reducción $\alpha$ es una función lineal por tramos de la carga matricial $h$ (m, negativa).

$$
\alpha(h)
=
\begin{cases}
0, & h > h_1 \\
\dfrac{h_1 - h}{h_1 - h_2}, & h_2 < h \le h_1 \\
1, & h_3 \le h \le h_2 \\
\dfrac{h - h_4}{h_3 - h_4}, & h_4 < h < h_3 \\
0, & h \le h_4
\end{cases}
$$

| Carga | Significado | Predeterminado (m) |
|---|---|---:|
| $h_1$ | Más húmedo que este valor: sin absorción (falta aire para las raíces) | −0.1 |
| $h_2$ | Inicio de la absorción sin estrés | −0.25 |
| $h_3$ | Fin de la absorción sin estrés | −4.0 |
| $h_4$ | Punto de marchitez: sin absorción | −80 |

Las cargas deben cumplir $0 \ge h_1 > h_2 \ge h_3 > h_4$. La carga de cada capa se obtiene de su curva de van Genuchten y de su contenido de agua actual.

**$h_3$ dependiente de la demanda (opcional).** Como en SWAP, $h_3$ puede depender de la tasa de transpiración potencial $T_p$. $h_{3,\mathrm{high}}$ se aplica con $T_p \ge 5$ mm/día, $h_{3,\mathrm{low}}$ con $T_p \le 1$ mm/día, y $h_3$ se interpola linealmente entre ambos. Los dos valen $h_3$ por defecto, por lo que la opción queda desactivada salvo que se definan.

**Absorción.** La densidad de raíces es uniforme en la profundidad de raíces $z_r$. A cada capa con raíces se le solicita su parte de la demanda, reducida por su propio $\alpha$,

$$
S_\ell = \alpha(h_\ell)\,T_p\,\frac{z_{r,\ell}}{z_r}
$$

donde $S_\ell$ es la extracción de la capa $\ell$ y $z_{r,\ell}$ es el espesor con raíces de la capa $\ell$. Cada extracción está limitada por el agua disponible en esa capa. No hay compensación. La demanda que una capa no puede atender no se traslada a otra capa.

| Parámetro | HydroPol2D-Python | HydroPol2D (MATLAB) |
|---|---|---|
| Cargas | `vertical.feddes.h1_m`, `h2_m`, `h3_m`, `h4_m` | `feddes_h1_m`, `feddes_h2_m`, `feddes_h3_m`, `feddes_h4_m` |
| $h_3$ dependiente de la demanda | `vertical.feddes.h3_low_m`, `h3_high_m` | `feddes_h3_low_m`, `feddes_h3_high_m` |

---

## 4. Infiltración {#4-infiltration}

El módulo de infiltración calcula la transferencia de agua desde la superficie a la zona vadosa utilizando una formulación basada en Darcy junto con relaciones constitutivas de van Genuchten-Mualem. La formulación está diseñada para aproximarse al comportamiento de flujo insaturado tipo Richards manteniendo la compatibilidad con la estructura basada en almacenamiento de HydroPol2D.
En cada paso de tiempo, la infiltración está controlada por tres restricciones simultáneas:
1. la disponibilidad de agua en la superficie,
2. la capacidad hidráulica del suelo,
3. la capacidad de almacenamiento restante de la zona vadosa.

La tasa de infiltración final se determina como el mínimo entre estos límites en competencia.
### Estructura vadosa en capas actual

La implementación actual representa la columna de suelo y agua subterránea somera con cuatro zonas conceptuales:
- una capa cercana a la superficie, con un espesor objetivo predeterminado de $0.10\,\mathrm{m}$;
- una capa de zona de raíces, cuya profundidad se asigna a partir del uso/cobertura del suelo;
- una capa de zona de transmisión, que ocupa cualquier espesor vadoso restante debajo de la zona de la raíz;
- una zona de agua subterránea, cuya cima es la profundidad actual del nivel freático.

La geometría de la capa se vuelve a calcular a partir de la profundidad del suelo, la elevación de la superficie del terreno y la altura del agua subterránea. Las reglas alternativas son intencionalmente conservadoras:
- si la profundidad de la raíz LULC es menor que el objetivo cercano a la superficie, la capa explícita de la zona de raíces colapsa y las raíces se representan dentro de la capa cercana a la superficie;
- si el lecho de roca es menos profundo que la profundidad de raíces solicitada, la profundidad de las raíces se trunca a la profundidad de suelo disponible;
- si el nivel freático es menos profundo que la profundidad de raíz solicitada, el almacenamiento de raíces vadosas se trunca en el nivel freático;
- si el nivel freático llega a la superficie, todas las capas vadosas tienen espesor cero y la retroalimentación del agua subterránea se produce a través de la lógica de saturación/exfiltración.

Los mismos parámetros hidráulicos del suelo base se asignan a las capas cercanas a la superficie, a la zona de las raíces y a la zona de transmisión, mientras que la conductividad hidráulica saturada se puede ajustar mediante multiplicadores de capas:
- `Ks_multiplier_near_surface`,
- `Ks_multiplier_root_zone`,
- `Ks_multiplier_transmission`.

Esto mantiene la parametrización práctica: la tabla de suelo define el comportamiento físico base del suelo, LULC define la profundidad de la zona de raíces y los multiplicadores permiten contrastes verticales cuando los datos o la calibración los respaldan.

---

### 4.1 Almacenamiento insaturado controlado por el nivel freático

La estructura vertical de la columna de suelo está vinculada dinámicamente al nivel freático. El espesor saturado sobre la base del perfil del suelo se calcula como
$$
z_{\mathrm{gw}}
=
h_{\mathrm{gw}}
-
\left(
z_{\mathrm{surf}} - D_{\mathrm{soil}}
\right)
$$
y la profundidad del nivel freático debajo de la superficie terrestre es
$$
z_{\mathrm{wt}}
=
D_{\mathrm{soil}} - z_{\mathrm{gw}}
$$
dónde:
- $h_{\mathrm{gw}}$ es la cabeza del agua subterránea $[\mathrm{L}]$
- $z_{\mathrm{surf}}$ es la elevación de la superficie terrestre $[\mathrm{L}]$
- $D_{\mathrm{soil}}$ es la profundidad del suelo $[\mathrm{L}]$
- $z_{\mathrm{wt}}$ es la profundidad del nivel freático debajo de la superficie $[\mathrm{L}]$

Según la implementación actual, el almacenamiento vadosa se registra como **agua activa por encima del contenido residual**. Por lo tanto, el almacenamiento máximo conceptual disponible en la zona no saturada es
$$
S_{\mathrm{uz,max}}
=
z_{\mathrm{wt}}
\left(
\theta_{\mathrm{sat}} - \theta_{\mathrm{r}}
\right)
$$
y la capacidad de almacenamiento restante es
$$
S_{\mathrm{uz,rem}}
=
\max\left(
S_{\mathrm{uz,max}} - S_{\mathrm{uz}},\,0
\right)
$$
dónde:
- $S_{\mathrm{uz,max}}$ es el almacenamiento vadose máximo $[\mathrm{L}]$
- $S_{\mathrm{uz}}$ es el almacenamiento vadose actual $[\mathrm{L}]$
- $\theta_{\mathrm{r}}$ es el contenido de agua residual $[-]$
- $\theta_{\mathrm{sat}}$ es el contenido de agua saturada $[-]$

Esta formulación garantiza que el almacenamiento disponible responda dinámicamente a las fluctuaciones del agua subterránea. A medida que aumenta el nivel freático, $z_{\mathrm{wt}}$ disminuye y la capacidad de almacenamiento vadosa se reduce en consecuencia. En la implementación en capas predeterminada, esta misma lógica se aplica a través de las capacidades sumadas de los almacenes cercanos a la superficie, de la zona de la raíz y de la zona de transmisión después del truncamiento por la posición actual del nivel freático.

---

### 4.2 Contenido de agua representativo y saturación efectiva

El contenido volumétrico representativo de agua en la zona vadosa se aproxima como
$$
\theta
=
\theta_{\mathrm{r}} + \frac{S_{\mathrm{uz}}}{z_{\mathrm{wt}}}
$$
sujeto a
$$
\theta_{\mathrm{r}} \le \theta \le \theta_{\mathrm{sat}}
$$
La saturación efectiva se define entonces como
$$
S_{\mathrm{e}}
=
\frac{
\theta - \theta_{\mathrm{r}}
}{
\theta_{\mathrm{sat}} - \theta_{\mathrm{r}}
}
$$
dónde:
- $\theta$ es el contenido volumétrico de agua $[-]$
- $\theta_{\mathrm{r}}$ es el contenido de agua residual $[-]$
- $S_{\mathrm{e}}$ es la saturación efectiva $[-]$

Esta saturación efectiva se utiliza para evaluar tanto la succión matricial como la conductividad hidráulica. En la implementación en capas predeterminada, la misma forma constitutiva se evalúa por separado para cada capa vadosa; La expresión de estado único anterior es el equivalente conceptual de la formulación alternativa heredada.

---

### 4.3 Cabezal de presión matricial

La carga de presión matricial se calcula utilizando la curva de retención de van Genuchten:
$$
\psi_{\mathrm{m}}
=
-\frac{1}{\alpha_{\mathrm{vg}}}
\left(
S_{\mathrm{e}}^{-1/m} - 1
\right)^{1/n}
$$
con
$$
m = 1 - \frac{1}{n}
$$
dónde:
- $\psi_{\mathrm{m}}$ es la altura de presión matricial $[\mathrm{L}]$
- $\alpha_{\mathrm{vg}}$ es el parámetro inverso de entrada de aire $[\mathrm{L}^{-1}]$
- $n$ es el parámetro de forma de van Genuchten $[-]$

En condiciones casi saturadas, el modelo impone
$$
\psi_{\mathrm{m}} = 0
$$
para evitar la inestabilidad numérica.

---

### 4.4 Conductividad hidráulica no saturada

La conductividad hidráulica insaturada se calcula como
$$
K(\theta) = K_{\mathrm{sat}} K_r
$$
con
$$
K_r
=
S_{\mathrm{e}}^{\ell}
\left[
1 - \left(1 - S_{\mathrm{e}}^{1/m}\right)^m
\right]^2
$$
dónde:
- $K(\theta)$ es conductividad hidráulica insaturada $[\mathrm{L}\,\mathrm{T}^{-1}]$
- $K_{\mathrm{sat}}$ es conductividad hidráulica saturada $[\mathrm{L}\,\mathrm{T}^{-1}]$
- $\ell$ es el parámetro de conectividad de poros $[-]$

Si no se proporciona $\ell$, se utiliza un valor predeterminado de $\ell = 0.5$.

---

### 4.5 Capacidad de infiltración basada en Darcy

La capacidad de infiltración representa el flujo máximo que se puede transmitir al suelo dado el estado hidráulico actual. En el código actual, esto no se basa en un único valor $K(\theta)$. En cambio, HydroPol2D usa:
- una succión de cubo representativa basada en el almacenamiento vadose actual,
- un predictor de humectación cerca de la superficie dentro del paso,
- y una conductividad ponderada cerca de la superficie que combina la conductividad de entrada saturada con la conductividad de la capa superior humedecida.

El predictor de humectación temporal es
$$
w_{\mathrm{wet}}
=
\min\!\left(
d_{\mathrm{eff}},\,
S_{\mathrm{uz,rem}},\,
S_{\mathrm{top,def}}
\right)
$$
$$
\theta_{\mathrm{top}}
=
\min\!\left(
\theta_{\mathrm{sat}},\,
\theta + \frac{w_{\mathrm{wet}}}{L_{\mathrm{top}}}
\right)
$$
dónde:
- $w_{\mathrm{wet}}$ es la profundidad de humectación candidata dentro del paso $[\mathrm{L}]$
- $S_{\mathrm{top,def}}$ es el déficit de almacenamiento restante de la capa cercana a la superficie $[\mathrm{L}]$
- $\theta_{\mathrm{top}}$ es el contenido de agua previsto en el fondo de la capa cercana a la superficie $[-]$

La conductividad de entrada efectiva se evalúa entonces como
$$
K_{\mathrm{soil}}
=
w_K K_{\mathrm{sat}}+
\left(1-w_K\right) K(\theta_{\mathrm{top}})
$$
donde $w_K$ es el peso de conductividad cerca de la superficie. La capacidad de infiltración se calcula entonces como
$$
I_{\mathrm{cap}}
=
K_{\mathrm{soil}}
\left[
\frac{
\min\!\left(
h_{\mathrm{pond}} - \psi_{\mathrm{m}},\,
\Delta h_{\mathrm{max}}
\right)
}{
L_{\mathrm{top}}
}
+
1
\right]
$$
dónde:
- $I_{\mathrm{cap}}$ es la capacidad de infiltración $[\mathrm{L}\,\mathrm{T}^{-1}]$
- $h_{\mathrm{pond}}$ es la cabeza de estanqueidad de superficie $[\mathrm{L}]$
- $L_{\mathrm{top}}$ es la longitud de resistencia cerca de la superficie (valor predeterminado $\approx 0.05\,\mathrm{m}$)
- $\Delta h_{\mathrm{max}}$ es la diferencia máxima de cabeza motriz (normalmente $1\,\mathrm{m}$)

Esta formulación representa tanto la infiltración impulsada por la gravedad como la impulsada por capilares y al mismo tiempo aproxima la humectación rápida en el límite de la superficie. El predictor de humectación **no** agrega agua al estado del suelo por sí solo; sólo el flujo de infiltración aceptado actualiza el almacenamiento vadose.

---

### 4.6 Infiltración limitada por el suministro y el almacenamiento

El agua disponible para la infiltración se determina a partir de la profundidad efectiva del agua superficial. Cuando la interceptación está inactiva:
$$
d_{\mathrm{eff}} = d
$$
La correspondiente tasa de infiltración limitada por el suministro es
$$
i_{\mathrm{sup}} = \frac{d_{\mathrm{eff}}}{\Delta t_{\mathrm{h}}}
$$
dónde:
- $d_{\mathrm{eff}}$ es la profundidad efectiva del agua estancada $[\mathrm{L}]$
- $\Delta t_{\mathrm{h}}$ es el paso de tiempo en horas $[\mathrm{T}]$

La tasa de infiltración limitada por almacenamiento es
$$
i_{\mathrm{store}} = \frac{S_{\mathrm{uz,rem}}}{\Delta t_{\mathrm{h}}}
$$
La tasa de infiltración real es entonces
$$
i = \min\!\left(i_{\mathrm{sup}},\,I_{\mathrm{cap}},\,i_{\mathrm{store}}\right)
$$
Se aplican restricciones adicionales:
- $i = 0$ sobre celdas impermeables
- $i = 0$ cuando $z_{\mathrm{wt}} \le 0$

Por lo tanto, la infiltración está simultáneamente **limitada por el suministro**, **limitada por la capacidad** y **limitada por el almacenamiento**. En el modo en capas, la aceptación está además limitada por el déficit explícito de almacenamiento cerca de la superficie antes de que el agua pueda continuar drenando hacia abajo a través de las capas vadosas más profundas.

<p align="center">
  <img src={useBaseUrl('/img/theory/infiltration-limits.es.svg')} width="720" alt="Tres columnas de suelo de una celda, cada una un caso en que un límite es el menor: lluvia débil sobre suelo seco, limitada por el suministro; lámina alta sobre suelo de baja conductividad, limitada por la capacidad de Darcy; y nivel freático somero, limitado por el espacio de almacenamiento; bajo cada columna, la definición de ese límite y el origen de sus términos" />
</p>

<p align="center">
  <em>Figura 1. Los tres límites de la infiltración, cada uno en un caso en que es el menor (esquema, sin escala). El agua que no se infiltra queda en la superficie y se enruta a las celdas vecinas.</em>
</p>

---

### 4.7 Actualización de almacenamiento de Vadose

La profundidad infiltrada a lo largo del paso del tiempo es
$$
\Delta I = i\,\Delta t_{\mathrm{h}}
$$
y el almacenamiento vadose se actualiza como
$$
S_{\mathrm{uz}}^{\,\mathrm{new}} = S_{\mathrm{uz}} + \Delta I
$$
sujeto a
$$
0 \le S_{\mathrm{uz}}^{\,\mathrm{new}} \le S_{\mathrm{uz,max}}
$$
En la implementación en capas predeterminada, la infiltración aceptada primero llena el almacén cercano a la superficie y luego el almacenamiento vadose total se sincroniza entre:
- almacenamiento cerca de la superficie,
- almacenamiento en la zona raíz,
- almacenamiento en la zona de transmisión.

Por lo tanto, la expresión escalar anterior es el resumen conceptual de una actualización en capas y no la única representación interna.---

## 5. Acumulación, fusión y sublimación de nieve {#5-snow-accumulation-melt-and-sublimation}

Cuando el modelado de nieve está activo, HydroPol2D sigue el equivalente de agua de nieve (SWE), la densidad de la nieve y la profundidad física de la nieve en cada celda activa de la malla. Los parámetros de nieve se leen de la tabla de parámetros LULC y se asignan a la malla a partir de `LULC_Index`. La vía de forzamiento meteorológico interno proporciona la temperatura media del aire, la temperatura mínima del aire y la velocidad del viento. Por tanto, las simulaciones de nieve requieren `flag_ETP = 1`, `flag_input_ETP_map = 0` y un libro meteorológico que cubra el período de simulación.

<p align="center">
  <img src={useBaseUrl('/img/theory/snow.es.svg')} width="720" alt="A la izquierda, un paso de tiempo en una celda: la temperatura del aire separa la precipitación en nieve y lluvia; la nieve forma un manto que pierde agua por fusión hacia el agua superficial y por sublimación hacia la atmósfera, y la lluvia pasa por el almacenamiento del dosel cuando la intercepción está activa. A la derecha, las ecuaciones de la Sección 5. Abajo a la izquierda, una ilustración de la temperatura del aire, la precipitación y el SWE con forzamiento sintético" />
</p>

<p align="center">
  <em>Figura 2. Lluvia o nieve, almacenamiento, fusión y sublimación en una celda. Solo la lluvia entra en el almacenamiento del dosel, la fusión va directa al agua superficial, y el panel inferior usa forzamiento sintético, no salida del modelo.</em>
</p>

---

### 5.1 Partición lluvia-nieve {#51-rain-snow-partitioning}

Cada clase LULC define un umbral de nieve total $T_{\mathrm{snow}}$ y un umbral de lluvia total $T_{\mathrm{rain}}$, ambos en $^{\circ}\mathrm{C}$. La fracción de nieve es

$$
f_{\mathrm{snow}}
=
\begin{cases}
1, & T_{\mathrm{air}} \le T_{\mathrm{snow}} \\
\dfrac{T_{\mathrm{rain}}-T_{\mathrm{air}}}{T_{\mathrm{rain}}-T_{\mathrm{snow}}}, & T_{\mathrm{snow}} < T_{\mathrm{air}} < T_{\mathrm{rain}} \\
0, & T_{\mathrm{air}} \ge T_{\mathrm{rain}}.
\end{cases}
$$

Los umbrales deben cumplir $T_{\mathrm{rain}} \ge T_{\mathrm{snow}}$. Si los umbrales son iguales, la partición es un escalón en esa temperatura. La nevada y la lluvia resultantes son

$$
P_{\mathrm{snow}}=P_{\mathrm{gross}}f_{\mathrm{snow}}
$$

$$
P_{\mathrm{rain}}=P_{\mathrm{gross}}-P_{\mathrm{snow}}
$$

donde $f_{\mathrm{snow}}$ es la fracción de nieve, que depende de la temperatura.

La partición va antes del dosel. Solo la lluvia $P_{\mathrm{rain}}$ entra en el modelo de intercepción de la Sección 2, en lugar de $P_{\mathrm{gross}}$; la nevada va al manto de nieve, y el deshielo $M_{\mathrm{snow}}$ llega a la superficie sin pasar por el dosel.

---

### 5.2 Equivalente de agua de nieve {#52-snow-water-equivalent}

El balance de SWE es

$$
\mathrm{SWE}_t=\mathrm{SWE}_{t-1}+P_{\mathrm{snow}}-M_{\mathrm{snow}}-E_{\mathrm{s}}
$$

donde todos los términos están en milímetros de equivalente de agua y $E_{\mathrm{s}}$ es la sublimación.

---

### 5.3 Fusión de la nieve y escalado con el paso de tiempo {#53-snowmelt-and-timestep-scaling}

La fusión de la nieve es la suma de un término de grados-día y un término de radiación neta positiva. Para un paso de enrutamiento de $\Delta t_s$ segundos y $\Delta t_d=\Delta t_s/86400$ días,

$$
M_{\mathrm{snow}}
=
\min\!\left[
\mathrm{SWE}_{\mathrm{after\ snowfall}},
\max\!\left(
\mathrm{DDF}\max(T_{\mathrm{air}},0)\Delta t_d+
\frac{\max(Q_{\mathrm{net}},0)\Delta t_s}{L_f},
0\right)\right]
$$

Aquí, $\mathrm{DDF}$ es el factor de grados-día propio de cada clase LULC $[\mathrm{mm\,^{\circ}C^{-1}\,day^{-1}}]$, $Q_{\mathrm{net}}$ es el flujo de radiación neta calculado internamente $[\mathrm{W\,m^{-2}}]$ y $L_f=3.34\times10^5\ \mathrm{J\,kg^{-1}}$ es el calor latente de fusión. Un flujo de $1\ \mathrm{kg\,m^{-2}}$ equivale a $1\ \mathrm{mm}$ de equivalente de agua. La fusión no puede superar el SWE disponible.

---

### 5.4 Densidad y profundidad de la nieve {#54-snow-density-and-depth}

La nieve fresca usa la densidad inicial propia de su clase LULC, $\rho_{\mathrm{init}}$. La nieve existente y la nueva se mezclan en proporción a su SWE antes de la compactación. Luego, la densidad evoluciona como

$$
\rho_{\mathrm{snow}}^{\,\mathrm{new}}=
\rho_{\mathrm{snow}}^{\,\mathrm{mixed}}+
\Delta t_d\left[
k_t\max(T_{\mathrm{air}},0)+
k_{\mathrm{swe}}\mathrm{SWE}+
k_DH_{\mathrm{snow}}\right]
$$

con $\rho_{\mathrm{init}}\le\rho_{\mathrm{snow}}\le\rho_{\mathrm{max}}$. La profundidad de la nieve es

$$
H_{\mathrm{snow}}=\frac{1000\,\mathrm{SWE}}{\rho_{\mathrm{snow}}}
$$

---

El factor 1000 convierte la profundidad en equivalente de agua en profundidad física de la nieve cuando el SWE está en milímetros y la densidad en $\mathrm{kg\,m^{-3}}$.

### 5.5 Sublimación {#55-sublimation}

$$
E_{\mathrm{s}}
=
\min\!\left[
\mathrm{SWE}_{\mathrm{after\ melt}},
\max\!\left(
C_eu(q_s-q_a)\mathrm{SWE}_{\mathrm{after\ melt}}\Delta t_d,
0
\right)\right]
$$

Aquí, $C_e$ es el coeficiente de sublimación propio de cada clase LULC, $u$ es la velocidad del viento $[\mathrm{m\,s^{-1}}]$, y $q_s$ y $q_a$ son la humedad específica de saturación y la humedad específica del ambiente. La implementación actual estima $q_a$ a partir de los campos de temperatura disponibles. La sublimación no es negativa y no puede superar el SWE posterior a la fusión.

---

### 5.6 Estados iniciales de nieve y fallback de códigos de clase {#56-initial-snow-states-and-class-code-fallback}

`Initial_SWE_path` e `Initial_Snow_Depth_path` son rásteres opcionales. Sin ninguno de los dos rásteres, el modelo inicia con SWE nulo y profundidad de nieve nula, y conserva la densidad de nieve fresca propia de cada clase LULC. Con un solo ráster, el otro estado se deriva de esa densidad. Con ambos rásteres, el modelo deriva la densidad a partir del SWE y de la profundidad, y rechaza los pares positivos que quedan fuera del intervalo de densidad configurado. Un valor nodata en el ráster significa que no se especificó nieve inicial para esa celda.

Si el ráster LULC contiene un código válido que no figura en la tabla LULC, de suelo o de nieve, HydroPol2D asigna la media ponderada por área de las propiedades de las celdas con clase asignada. El modelo escribe `Input_Class_Code_Audit.csv`, que enumera los códigos del ráster, los índices de tabla asignados, el área a la que se aplicó el fallback y las propiedades aplicadas. Los índices de tabla duplicados o no numéricos, o una tabla sin clases asignadas, siguen siendo errores de entrada.

### 5.7 Actualización del agua superficial en condiciones de nieve {#57-surface-water-update-under-snow-conditions}

$$
d_t=d_p+M_{\mathrm{snow}}+P_{\mathrm{rain}}
$$

Si el modelado de nieve está desactivado,

$$
d_t=d_p+P_{\mathrm{eff}},
$$
donde $d_t$ y $d_p$ son la profundidad actual y la profundidad anterior del agua superficial.

---

## 6. Almacenamiento, recarga y retroalimentación de aguas subterráneas de vadosa

### 6.1 Estructura vadosa en capas predeterminada

La formulación predeterminada actual es un **sistema vadose en capas**, no un solo cubo de recarga. El agua se rastrea en:
- una capa cercana a la superficie,
- una capa de zona raíz,
- una capa de transmisión,
- y una interfaz de acoplamiento de agua subterránea debajo de la capa de transmisión.

Para una capa vadosa genérica $\ell$ con almacenamiento activo $S_{\ell}$ (agua por encima de $\theta_{\mathrm{r}}$, como lámina sobre toda la celda) y espesor $z_{\ell}$, el agua ocupa la fracción permeable $f_p$ de la celda:
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
K_{\mathrm{sat},\ell} K_r(S_{e,\ell})
$$
La capa comienza con $S_{\ell} = f_p(\theta_i - \theta_{\mathrm{r},\ell})\, z_{\ell}$ y almacena como máximo $f_p(\theta_{\mathrm{sat},\ell} - \theta_{\mathrm{r},\ell})\, z_{\ell}$. En un paso de tiempo $\Delta t$, drena $f_p K_{\ell} \Delta t$ hacia la capa inferior, sujeto a la capacidad de almacenamiento disponible en la capa receptora. (Antes del 26/10/2026, el almacenamiento inicial y el drenaje no incluían $f_p$, por lo que las celdas parcialmente impermeables empezaban demasiado húmedas y drenaban demasiado lento.)
### 6.2 Drenaje descendente y recarga

En la ruta predeterminada:
1. El drenaje cercano a la superficie se mueve primero a la zona de las raíces cuando existe almacenamiento de raíces.
2. el drenaje de la zona de la raíz se mueve a la zona de transmisión cuando existe almacenamiento de transmisión,
3. El drenaje de la zona de transmisión se convierte en recarga al agua subterránea.

Conceptualmente, la recarga de agua subterránea en un período de tiempo se puede resumir como
$$
R_ {\mathrm{gw}}
=
\frac{\Delta S_{\mathrm{trans}\rightarrow\mathrm{gw}}}{\Delta t}
$$
con drenaje directo opcional desde las capas superiores solo donde las capas vadosas inferiores están ausentes. Esta cascada en capas es la historia canónica de recarga de HydroPol2D. El antiguo cierre de Darcy de un solo segmento sigue estando disponible sólo como una formulación alternativa y no debe tratarse como la ruta teórica predeterminada.
### 6.3 Elevación capilar opcional y acoplamiento asíncrono de aguas subterráneas

Cuando `flag_capillary_rise = 1`, el agua subterránea poco profunda puede devolver agua hacia arriba al almacenamiento vadoso disponible. La lógica de ascenso capilar implementada aumenta con:
- menor profundidad del nivel freático,
- mayor déficit de almacenamiento en la capa receptora,
- y conductividad de capa más grande.

Por lo tanto, el intercambio neto vadoso-agua subterránea acumulado por el programador de aguas subterráneas es
$$
R_{\mathrm{net}} = R_{\mathrm{down}} - C_{\mathrm{up}}
$$
dónde:
- $R_{\mathrm{down}}$ es la recarga total descendente del drenaje en capas
- $C_{\mathrm{up}}$ es el intercambio de ascenso capilar ascendente

Este intercambio neto se acumula en cada paso del agua superficial, mientras que los cabezales de agua subterránea saturada se pueden actualizar en un cronograma asincrónico más lento.
### 6.4 Exceso de saturación y exfiltración de aguas subterráneas

Después de la actualización del agua subterránea, HydroPol2D vuelve a calcular la capacidad vadosa utilizando la posición actualizada del nivel freático. Cualquier agua que ya no quepa en la zona no saturada regresa a la superficie como exceso de saturación:
$$
S_{\mathrm{excess}}
=
\max\!\left(
S_{\mathrm{uz}} - S_{\mathrm{uz,max}}^{\,\mathrm{new}},
0
\right)
$$
La cabeza de agua subterránea que se eleva por encima de la superficie local también genera exfiltración:
$$
q_{\mathrm{exf}}
=
\max\!\left(
0,\,
h_{\mathrm{gw}} - z_{\mathrm{surf}}
\right)
\frac{S_y}{\Delta t}
$$
donde $S_y$ es el rendimiento específico. La formulación canónica completa de aguas subterráneas, incluido el programador asíncrono y el solucionador de flujo lateral Boussinesq, está documentada en la página [Modelo de aguas subterráneas] (./groundwater-model).

### 6.5 Opción de subsuelo en capas {#65-layered-subsurface-option}

La estructura anterior es la predeterminada. El [subsuelo en capas](./layered-subsurface) opcional conserva los tres almacenamientos de suelo, pero los coloca sobre capas de regolito que alcanzan la profundidad hasta el lecho de roca. En ese esquema, un nivel freático en ascenso llena el espacio poroso vacío del suelo y del regolito, en lugar de empujar el agua del suelo hacia la superficie.

---

## 7. Resumen

El modelo hidrológico en HydroPol2D integra:
- intercepción del dosel,
- Evapotranspiración de Penman-Monteith,
- Infiltración basada en Darcy con conductividad ponderada cerca de la superficie,
- acumulación de nieve y derretimiento,
- almacenamiento vadoso en capas y acoplamiento de aguas subterráneas,
- estrés opcional de Feddes en la absorción de agua por las raíces,

en un marco unificado y consistente en masa que resuelve los flujos verticales de agua a escala de celda de cuadrícula y proporciona el forzamiento hidrológico para el modelo hidrodinámico.

---
