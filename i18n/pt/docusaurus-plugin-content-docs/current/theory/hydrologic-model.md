---
title: Modelo Hidrológico
---

# Modelo Hidrológico

O componente hidrológico de HydroPol2D governa a partição da entrada atmosférica em interceptação, passagem, infiltração, evapotranspiração, acúmulo e derretimento de neve, armazenamento na zona vadosa, recarga de águas subterrâneas e feedback das águas subterrâneas para a superfície terrestre.
Na escala celular, o modelo hidrológico determina quanta água:
- é armazenado temporariamente pelo dossel,
- atinge a superfície do solo,
- infiltra-se no solo,
- permanece armazenado na zona vadosa,
- recarrega as águas subterrâneas,
- retorna à superfície por exfiltração,
- ou é removido por evaporação e transpiração.

Esses processos são avaliados sequencialmente dentro de cada intervalo de tempo e fornecem o forçamento hidrológico para o modelo hidrodinâmico.

---

## 1. Balanço Hidrológico Conceitual

No nível conceitual, o equilíbrio hidrológico de uma célula da grade pode ser escrito como
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
onde:
- $d$ é a profundidade da água superficial $[\mathrm{L}]$
- $P_{\mathrm{eff}}$ é a precipitação efetiva que atinge o solo $[\mathrm{L}\,\mathrm{T}^{-1}]$
- $M_{\mathrm{snow}}$ é a contribuição do degelo $[\mathrm{L}\,\mathrm{T}^{-1}]$
- $q_{\mathrm{exf}}$ é a exfiltração da água subterrânea para a superfície $[\mathrm{L}\,\mathrm{T}^{-1}]$
- $i$ é a taxa de infiltração $[\mathrm{L}\,\mathrm{T}^{-1}]$
- $E_{\mathrm{surf}}$ é a taxa de evaporação do armazenamento de superfície $[\mathrm{L}\,\mathrm{T}^{-1}]$
- $T_{\mathrm{r}}$ é a taxa de transpiração $[\mathrm{L}\,\mathrm{T}^{-1}]$
- $q_{\mathrm{src}}$ e $q_{\mathrm{sink}}$ são termos adicionais de origem e destino impostos $[\mathrm{L}\,\mathrm{T}^{-1}]$

Nem todos os termos estão ativos simultaneamente. Sua ativação depende da configuração de forçamento selecionada e dos sinalizadores do modelo. No entanto, este equilíbrio fornece o quadro conceptual utilizado para organizar todos os fluxos verticais que actuam numa célula da grelha.

---

## 2. Interceptação do dossel, passagem e fluxo do tronco

HydroPol2D representa a interceptação do dossel usando um modelo de interceptação baseado em armazenamento no qual a precipitação bruta é particionada em:
- armazenamento do dossel,
- queda,
- evaporação do dossel,
- e fluxo de tronco.

A rotina de interceptação recebe:
- precipitação bruta $P_{\mathrm{gross}}$,
- evaporação potencial $E_{\mathrm{p}}$,
- índice de área foliar $\mathrm{LAI}$,
- armazenamento anterior do dossel $S_{\mathrm{can,prev}}$,
- coeficiente de armazenamento do dossel $C_{\mathrm{can}}$,

e retorna armazenamento de dossel atualizado $S_{\mathrm{can}}$, passagem $T_{\mathrm{f}}$, evaporação da água interceptada $E_{\mathrm{can}}$ e fluxo de tronco $F_{\mathrm{stem}}$.
Esta etapa de interceptação controla quanto da entrada de água atmosférica é temporariamente retida pela vegetação e quanto é transferido para a superfície do solo durante o intervalo de tempo atual.
### 2.1 Armazenamento máximo do dossel

O armazenamento máximo de interceptação é calculado como
$$
S_{\mathrm{can,max}} = C_{\mathrm{can}} \,\mathrm{LAI}
$$
onde:
- $S_{\mathrm{can,max}}$ é o armazenamento máximo de água no dossel $[\mathrm{L}]$
- $C_{\mathrm{can}}$ é o coeficiente de armazenamento do dossel $[\mathrm{L}]$
- $\mathrm{LAI}$ é o índice de área foliar $[-]$

Esta relação implica que a vegetação com maior área foliar pode armazenar mais água interceptada.
### 2.2 Fluxo de tronco

O código inclui uma rotina stemflow baseada em uma função de atraso. As expressões intermediárias são
$$
\tau_{\mathrm{stem}}
=
T_0 \exp\!\left(-\alpha_{\mathrm{stem}} P_{\mathrm{gross}}\right)
$$
e
$$
F_{\mathrm{stem}}
=
f_{\mathrm{stem}}
\,
\frac{S_{\mathrm{can,prev}}}{\tau_{\mathrm{stem}}/60}
$$
onde:
- $\tau_{\mathrm{stem}}$ é o atraso do fluxo de tronco $[\mathrm{T}]$
- $T_0$ é o parâmetro de atraso máximo $[\mathrm{T}]$
- $\alpha_{\mathrm{stem}}$ é o coeficiente de decaimento do fluxo de tronco $[-]$
- $f_{\mathrm{stem}}$ é a fração do fluxo-tronco $[-]$
- $F_{\mathrm{stem}}$ é fluxo-tronco $[\mathrm{L}]$

Na implementação atual do HydroPol2D, o stemflow é desativado pela imposição explícita
$$
F_{\mathrm{stem}} = 0
$$
Portanto, o escoamento pelo tronco não contribui atualmente para o equilíbrio das águas superficiais, embora a estrutura da rotina seja mantida no código.
### 2.3 Evaporação do armazenamento de interceptação

A fração de armazenamento da copa exposta à evaporação é definida como
$$
\beta = \frac{S_{\mathrm{can,prev}}}{S_{\mathrm{can,max}}}
$$
e a evaporação do dossel é então calculada como
$$
E_{\mathrm{can}} = \beta \, E_{\mathrm{p}}
$$
sujeito à restrição
$$
E_{\mathrm{can}} \le P_{\mathrm{gross}} + S_{\mathrm{can,prev}}
$$
onde:
- $\beta$ é a fração do armazenamento do dossel preenchido no início do intervalo de tempo $[-]$
- $E_{\mathrm{can}}$ é a evaporação do armazenamento de interceptação $[\mathrm{L}]$
- $E_{\mathrm{p}}$ é a evaporação potencial ao longo do intervalo de tempo $[\mathrm{L}]$

Esta formulação assume que a evaporação do dossel é proporcional à fração de armazenamento ocupada no início do intervalo de tempo, ao mesmo tempo que impõe que a evaporação não pode exceder a água realmente disponível na precipitação mais a água de interceptação armazenada.
### 2.4 Atualização de armazenamento de interceptação

O incremento de armazenamento do dossel é calculado como
$$
\Delta S_{\mathrm{can}} = P_{\mathrm{gross}} - F_{\mathrm{stem}} - E_{\mathrm{can}}
$$
e o armazenamento provisório passa a ser
$$
S_{\mathrm{can}}^{\ast} = S_{\mathrm{can,prev}} + \Delta S_{\mathrm{can}}
$$
O throughfall é então calculado como o excesso acima da capacidade de armazenamento do dossel:
$$
T_{\mathrm{f}} = \max\left(S_{\mathrm{can}}^{\ast} - S_{\mathrm{can,max}},\,0\right)
$$
Finalmente, o armazenamento do velame é truncado em seu valor máximo admissível:
$$
S_{\mathrm{can}} = \min\left(S_{\mathrm{can}}^{\ast},\,S_{\mathrm{can,max}}\right)
$$
onde:
- $\Delta S_{\mathrm{can}}$ é o incremento de armazenamento do dossel ao longo do intervalo de tempo $[\mathrm{L}]$
- $S_{\mathrm{can}}^{\ast}$ é o armazenamento provisório do velame antes do truncamento $[\mathrm{L}]$
- $T_{\mathrm{f}}$ é perda $[\mathrm{L}]$
- $S_{\mathrm{can}}$ é o armazenamento final do dossel $[\mathrm{L}]$

Esta sequência reflete a suposição física de que a precipitação primeiro preenche o armazenamento do dossel. Assim que a copa atinge sua capacidade de armazenamento, o excesso de água é liberado como precipitação.
### 2.5 Chuva efetiva passada para a superfície

A precipitação disponível para a superfície terrestre é definida como
$$
P_{\mathrm{eff}} = T_{\mathrm{f}} + F_{\mathrm{stem}}
$$
onde:
- $P_{\mathrm{eff}}$ é a chuva efetiva que atinge o solo $[\mathrm{L}]$
- $T_{\mathrm{f}}$ é passagem direta $[\mathrm{L}]$
- $F_{\mathrm{stem}}$ é fluxo-tronco $[\mathrm{L}]$

Na implementação actual, uma vez que o escoamento pelo tronco está desactivado, a precipitação efectiva é igual à precipitação. Em termos práticos, $P_{\mathrm{eff}}$ representa a quantidade de água líquida transferida do sistema atmosfera-copa para a superfície terrestre durante o intervalo de tempo, antes do roteamento hidrodinâmico.
Se a rotina de interceptação for desativada, nenhum armazenamento no dossel será resolvido e a precipitação atingirá a superfície diretamente, de modo que
$$
P_{\mathrm{eff}} = P_{\mathrm{gross}}
$$
### 2.6 Aplicação da chuva
Para aplicações validadas, a precipitação que entra no módulo de interceptação é aplicada sobre a célula do modelo ativo como:
$$
P_{\mathrm{int}} = \Delta P_{\mathrm{agg}}
$$
onde $\Delta P_{\mathrm{agg}}$ é a profundidade agregada da precipitação ao longo do intervalo de tempo do modelo.

---

## 3. Evapotranspiração e Evaporação Potenciais

HydroPol2D calcula a evapotranspiração de referência distribuída espacialmente usando uma formulação de Penman-Monteith. Os dados da estação meteorológica são primeiro interpolados na grade usando ponderação de distância inversa, e os campos interpolados são então usados ​​para calcular a evapotranspiração de referência $\mathrm{ETP}$ e um termo semelhante à evaporação $E_{\mathrm{p}}$.
A quantidade $\mathrm{ETP}$ é usada como evapotranspiração de referência padrão, enquanto $E_{\mathrm{p}}$ é usada na rotina de interceptação para estimar a evaporação da água interceptada do dossel.
### 3.1 Interpolação espacial de forçantes meteorológicos

A cada intervalo de tempo, os seguintes campos são interpolados a partir das estações disponíveis:
- $T_{\mathrm{max}}$ temperatura máxima do ar $[\Theta]$
- $T_{\mathrm{min}}$ temperatura mínima do ar $[\Theta]$
- $T_{\mathrm{air}}$ temperatura média do ar $[\Theta]$
- $U_2$ velocidade do vento em $2\,\mathrm{m}$ $[\mathrm{L}\,\mathrm{T}^{-1}]$
- $\mathrm{UR}$ umidade relativa $[-]$
- $G_{\mathrm{soil}}$ fluxo de calor do solo $[\mathrm{E}\,\mathrm{L}^{-2}\,\mathrm{T}^{-1}]$

Para uma variável genérica $\phi$, o campo interpolado na localização $\mathbf{x}$ é escrito conceitualmente como
$$
\phi(\mathbf{x})
=
\frac{
\sum_{i=1}^{N} w_i(\mathbf{x})\,\phi_i
}{
\sum_{i=1}^{N} w_i(\mathbf{x})
}
$$
com
$$
w_i(\mathbf{x}) \propto \frac{1}{d_i(\mathbf{x})^p}
$$
onde:
- $\phi_i$ é o valor observado na estação $i$
- $d_i(\mathbf{x})$ é a distância da estação $i$ até o local $\mathbf{x}$ $[\mathrm{L}]$
- $p$ é o parâmetro de potência de ponderação de distância inversa $[-]$

Somente estações com dados completos no intervalo de tempo atual são retidas na interpolação. Este procedimento produz campos de força distribuídos espacialmente que são então usados ​​nos cálculos de evapotranspiração.
### 3.2 Equação de Penman-Monteith

A evapotranspiração de referência é calculada como
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
e o termo semelhante à evaporação é
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
onde:
- $\mathrm{ETP}$ é a evapotranspiração de referência $[\mathrm{L}\,\mathrm{T}^{-1}]$
- $E_{\mathrm{p}}$ é a evaporação potencial sem resistência aerodinâmica da superfície no denominador $[\mathrm{L}\,\mathrm{T}^{-1}]$
- $\Delta$ é a inclinação da curva de pressão de vapor de saturação $[\mathrm{P}\,\Theta^{-1}]$
- $R_n$ é a radiação líquida $[\mathrm{E}\,\mathrm{L}^{-2}\,\mathrm{T}^{-1}]$
- $G_{\mathrm{soil}}$ é o fluxo de calor do solo $[\mathrm{E}\,\mathrm{L}^{-2}\,\mathrm{T}^{-1}]$
- $\gamma$ é a constante psicrométrica $[\mathrm{P}\,\Theta^{-1}]$
- $U_2$ é a velocidade do vento em $2\,\mathrm{m}$ $[\mathrm{L}\,\mathrm{T}^{-1}]$
- $e_s$ é a pressão de vapor de saturação $[\mathrm{P}]$
- $e_a$ é a pressão de vapor real $[\mathrm{P}]$
- $T_{\mathrm{air}}$ é a temperatura média do ar $[\Theta]$

Estas são as formas algébricas implementadas no código atual. A diferença entre $\mathrm{ETP}$ e $E_{\mathrm{p}}$ está no denominador, o que torna $E_{\mathrm{p}}$ um termo semelhante à evaporação mais diretamente adequado para perdas por interceptação do dossel.
### 3.3 Radiação de apoio e termos atmosféricos

HydroPol2D calcula os termos auxiliares de Penman-Monteith usando relações astronômicas e termodinâmicas.
A declinação solar é calculada como
$$
\delta_{\mathrm{sol}}
=
0.409
\sin\!\left(
\frac{2\pi}{365}J - 1.39
\right)
$$
A distância relativa Terra-Sol é
$$
d_r = 1 + 0.033\cos\!\left(\frac{2\pi}{365}J\right)
$$
A radiação extraterrestre é então calculada como
$$
R_a
=
\frac{118.08}{\pi}
d_r
\left[
\omega_s \sin\phi \sin\delta_{\mathrm{sol}}+
\cos\phi \cos\delta_{\mathrm{sol}} \sin\omega_s
\right]
$$
A radiação solar recebida é estimada como
$$
R_s = K_{\mathrm{rs}} R_a \sqrt{T_{\mathrm{max}} - T_{\mathrm{min}}}
$$
A radiação do céu claro é
$$
R_{\mathrm{so}}
=
\left(
0.75 + 2\times10^{-5} z
\right) R_a
$$
A radiação líquida de ondas curtas é
$$
R_{\mathrm{ns}} = (1-\alpha_{\mathrm{land}})\,R_s
$$
A radiação líquida de ondas longas é
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
A radiação líquida é então
$$
R_n = R_{\mathrm{ns}} - R_{\mathrm{nl}}
$$
A inclinação da curva de pressão de vapor de saturação é calculada como
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
A pressão atmosférica é estimada como
$$
P_{\mathrm{atm}}
=
101.3
\left(
\frac{293 - 0.0065 z}{293}
\right)^{5.26}
$$
e a constante psicrométrica é
$$
\gamma = 0.665 \times 10^{-3} P_{\mathrm{atm}}
$$
onde:
- $J$ é o dia do ano $[-]$
- $\delta_{\mathrm{sol}}$ é a declinação solar $[\mathrm{rad}]$
- $d_r$ é a distância relativa Terra-Sol $[-]$
- $R_a$ é radiação extraterrestre $[\mathrm{E}\,\mathrm{L}^{-2}\,\mathrm{T}^{-1}]$
- $\omega_s$ é o ângulo horário do nascer do sol $[\mathrm{rad}]$
- $\phi$ é latitude $[\mathrm{rad}]$
- $R_s$ é a radiação solar recebida $[\mathrm{E}\,\mathrm{L}^{-2}\,\mathrm{T}^{-1}]$
- $K_{\mathrm{rs}}$ é o coeficiente de radiação empírica na estimativa de radiação recebida do tipo Hargreaves $[-]$
- $R_{\mathrm{so}}$ é a radiação solar de céu claro $[\mathrm{E}\,\mathrm{L}^{-2}\,\mathrm{T}^{-1}]$
- $z$ é a elevação do terreno $[\mathrm{L}]$
- $R_{\mathrm{ns}}$ é a radiação líquida de ondas curtas $[\mathrm{E}\,\mathrm{L}^{-2}\,\mathrm{T}^{-1}]$
- $\alpha_{\mathrm{land}}$ é o albedo da superfície terrestre $[-]$
- $R_{\mathrm{nl}}$ é a radiação líquida de ondas longas $[\mathrm{E}\,\mathrm{L}^{-2}\,\mathrm{T}^{-1}]$
- $\sigma$ é a constante de Stefan-Boltzmann
- $P_{\mathrm{atm}}$ é a pressão atmosférica $[\mathrm{P}]$

Estas expressões são explicitamente implementadas na rotina de evapotranspiração e avaliadas em forma de matriz no domínio computacional.
### 3.4 Evaporação direta e forçamento de transpiração

HydroPol2D também pode usar campos raster de evaporação e transpiração fornecidos externamente. Nessa configuração, o modelo ignora o cálculo interno de Penman – Monteith e aplica os campos $E_{\mathrm{surf}}$ e $T_{\mathrm{r}}$ prescritos diretamente no balanço de massa hidrológico.

### 3.5 Estresse de Feddes na absorção de água pelas raízes {#35-feddes-root-water-uptake-stress}

O estresse de Feddes é opcional. Ele reduz a transpiração do solo quando a zona radicular está úmida demais ou seca demais (Feddes, Kowalik e Zaradny, 1978, *Simulation of Field Water Use and Crop Yield*, Pudoc, Wageningen).

| Modelo | Chave | Padrão |
|---|---|---|
| HydroPol2D-Python | `vertical.feddes.enabled: true` | desligado |
| HydroPol2D (MATLAB) | `flag_feddes = 1` | `0` |

Funciona nos dois esquemas de subsuperfície (padrão e [em camadas](./layered-subsurface)), na grade estruturada e na malha Voronoi.

O fator de redução $\alpha$ é uma função linear por partes da carga matricial $h$ (m, negativa)

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

| Carga | Significado | Padrão (m) |
|---|---|---:|
| $h_1$ | Mais úmido que isso: sem absorção (falta ar para as raízes) | −0.1 |
| $h_2$ | Início da absorção sem estresse | −0.25 |
| $h_3$ | Fim da absorção sem estresse | −4.0 |
| $h_4$ | Ponto de murcha: sem absorção | −80 |

As cargas devem satisfazer $0 \ge h_1 > h_2 \ge h_3 > h_4$. A carga de cada camada vem da sua curva de van Genuchten e do seu conteúdo de água atual.

**$h_3$ dependente da demanda (opcional).** Como no SWAP, $h_3$ pode depender da taxa de transpiração potencial $T_p$. $h_{3,\mathrm{high}}$ vale para $T_p \ge 5$ mm/dia, $h_{3,\mathrm{low}}$ vale para $T_p \le 1$ mm/dia, e $h_3$ é interpolado linearmente entre os dois. Ambos valem $h_3$ por padrão, e a opção fica desligada enquanto não forem definidos.

**Absorção.** A densidade de raízes é uniforme ao longo da profundidade radicular $z_r$. Cada camada com raízes recebe a sua parcela da demanda, reduzida pelo próprio $\alpha$

$$
S_\ell = \alpha(h_\ell)\,T_p\,\frac{z_{r,\ell}}{z_r}
$$

onde $z_{r,\ell}$ é a espessura com raízes da camada $\ell$. Cada retirada é limitada pela água disponível na camada. Não há compensação. A demanda que uma camada não consegue atender não passa para outra camada.

| Configuração | HydroPol2D-Python | HydroPol2D (MATLAB) |
|---|---|---|
| Cargas | `vertical.feddes.h1_m`, `h2_m`, `h3_m`, `h4_m` | `feddes_h1_m`, `feddes_h2_m`, `feddes_h3_m`, `feddes_h4_m` |
| $h_3$ dependente da demanda | `vertical.feddes.h3_low_m`, `h3_high_m` | `feddes_h3_low_m`, `feddes_h3_high_m` |

---

## 4. Infiltração {#4-infiltration}

O módulo de infiltração calcula a transferência de água da superfície para a zona vadosa usando uma formulação baseada em Darcy acoplada às relações constitutivas de van Genuchten-Mualem. A formulação é projetada para aproximar o comportamento do fluxo insaturado do tipo Richards, mantendo a compatibilidade com a estrutura baseada em armazenamento do HydroPol2D.
A cada passo de tempo, a infiltração é controlada por três restrições simultâneas:
1. a disponibilidade de água na superfície,
2. a capacidade hidráulica do solo,
3. a capacidade de armazenamento restante da zona vadosa.

A taxa de infiltração final é determinada como a mínima entre esses limites concorrentes.
### Estrutura vadosa em camadas atual

A implementação atual representa o solo e a coluna de águas subterrâneas rasas com quatro zonas conceituais:
- uma camada próxima à superfície, com uma espessura alvo padrão de $0.10\,\mathrm{m}$;
- uma camada de zona radicular, cuja profundidade é atribuída a partir do uso/cobertura do solo;
- uma camada de zona de transmissão, que ocupa qualquer espessura vadosa remanescente abaixo da zona radicular;
- uma zona de águas subterrâneas, cujo topo é a profundidade atual do lençol freático.

A geometria da camada é recalculada a partir da profundidade do solo, elevação da superfície terrestre e altura da água subterrânea. As regras alternativas são intencionalmente conservadoras:
- se a profundidade da raiz do LULC for menor que o alvo próximo à superfície, a camada explícita da zona raiz entrará em colapso e as raízes serão representadas dentro da camada próxima à superfície;
- se o leito rochoso for mais raso do que a profundidade radicular solicitada, a profundidade radicular será truncada para a profundidade disponível do solo;
- se o lençol freático for mais raso do que a profundidade de raiz solicitada, o armazenamento de raízes vadosas será truncado no lençol freático;
- se o lençol freático atinge a superfície, todas as camadas vadosas têm espessura zero e o feedback da água subterrânea ocorre através da lógica de saturação/exfiltração.

Os mesmos parâmetros hidráulicos básicos do solo são atribuídos às camadas próximas à superfície, zona radicular e zona de transmissão, enquanto a condutividade hidráulica saturada pode ser ajustada por multiplicadores de camada:
- `Ks_multiplier_near_surface`,
- `Ks_multiplier_root_zone`,
- `Ks_multiplier_transmission`.

Isso mantém a parametrização prática: a tabela de solos define o comportamento físico básico do solo, LULC define a profundidade da zona radicular e os multiplicadores permitem contrastes verticais quando os dados ou a calibração os suportam.

---

### 4.1 Armazenamento insaturado controlado pelo lençol freático

A estrutura vertical da coluna do solo está dinamicamente ligada ao lençol freático. A espessura saturada acima da base do perfil do solo é calculada como
$$
z_{\mathrm{gw}}
=
h_{\mathrm{gw}}-
\left(
z_{\mathrm{surf}} - D_{\mathrm{soil}}
\right)
$$
e a profundidade do lençol freático abaixo da superfície da terra é
$$
z_{\mathrm{wt}}
=
D_{\mathrm{soil}} - z_{\mathrm{gw}}
$$
onde:
- $h_{\mathrm{gw}}$ é a cabeceira da água subterrânea $[\mathrm{L}]$
- $z_{\mathrm{surf}}$ é a elevação da superfície terrestre $[\mathrm{L}]$
- $D_{\mathrm{soil}}$ é a profundidade do solo $[\mathrm{L}]$
- $z_{\mathrm{wt}}$ é a profundidade do lençol freático abaixo da superfície $[\mathrm{L}]$

Na implementação atual, o armazenamento vadoso é rastreado como **água ativa acima do conteúdo residual**. O armazenamento máximo conceitual disponível na zona não saturada é, portanto,
$$
S_{\mathrm{uz,max}}
=
z_{\mathrm{wt}}
\left(
\theta_{\mathrm{sat}} - \theta_{\mathrm{r}}
\right)
$$
e a capacidade de armazenamento restante é
$$
S_{\mathrm{uz,rem}}
=
\max\left(
S_{\mathrm{uz,max}} - S_{\mathrm{uz}},\,0
\right)
$$
onde:
- $S_{\mathrm{uz,max}}$ é o armazenamento vadose máximo $[\mathrm{L}]$
- $S_{\mathrm{uz}}$ é o armazenamento vadose atual $[\mathrm{L}]$
- $\theta_{\mathrm{r}}$ é o teor de água residual $[-]$
- $\theta_{\mathrm{sat}}$ é o conteúdo de água saturada $[-]$

Esta formulação garante que o armazenamento disponível responda dinamicamente às flutuações das águas subterrâneas. À medida que o lençol freático aumenta, $z_{\mathrm{wt}}$ diminui e a capacidade de armazenamento vadose diminui de acordo. Na implementação em camadas padrão, essa mesma lógica é aplicada por meio das capacidades somadas dos armazenamentos próximos à superfície, zona raiz e zona de transmissão após truncamento pela posição atual do lençol freático.

---

### 4.2 Conteúdo representativo de água e saturação efetiva

O conteúdo volumétrico representativo de água na zona vadosa é aproximado como
$$
\theta
=
\theta_{\mathrm{r}} + \frac{S_{\mathrm{uz}}}{z_{\mathrm{wt}}}
$$
sujeito a
$$
\theta_{\mathrm{r}} \le \theta \le \theta_{\mathrm{sat}}
$$
A saturação efetiva é então definida como
$$
S_{\mathrm{e}}
=
\frac{
\theta - \theta_{\mathrm{r}}
}{
\theta_{\mathrm{sat}} - \theta_{\mathrm{r}}
}
$$
onde:
- $\theta$ é o conteúdo volumétrico de água $[-]$
- $\theta_{\mathrm{r}}$ é o teor de água residual $[-]$
- $S_{\mathrm{e}}$ é a saturação efetiva $[-]$

Esta saturação efetiva é usada para avaliar a sucção matricial e a condutividade hidráulica. Na implementação em camadas padrão, a mesma forma constitutiva é avaliada separadamente para cada camada vadosa; a expressão de estado único acima é o equivalente conceitual para a formulação de fallback herdada.

---

### 4.3 Cabeça de pressão matricial

A cabeça de pressão matricial é calculada usando a curva de retenção de van Genuchten:
$$
\psi_{\mathrm{m}}
=
-\frac{1}{\alpha_{\mathrm{vg}}}
\left(
S_{\mathrm{e}}^{-1/m} - 1
\right)^{1/n}
$$
com
$$
m = 1 - \frac{1}{n}
$$
onde:
- $\psi_{\mathrm{m}}$ é a cabeça de pressão matricial $[\mathrm{L}]$
- $\alpha_{\mathrm{vg}}$ é o parâmetro de entrada de ar inverso $[\mathrm{L}^{-1}]$
- $n$ é o parâmetro de forma de van Genuchten $[-]$

Em condições quase saturadas, o modelo impõe
$$
\psi_{\mathrm{m}} = 0
$$
para evitar instabilidade numérica.

---

### 4.4 Condutividade hidráulica insaturada

A condutividade hidráulica não saturada é calculada como
$$
K(\theta) = K_{\mathrm{sat}} K_r
$$
com
$$
K_r
=
S_{\mathrm{e}}^{\ell}
\left[
1 - \left(1 - S_{\mathrm{e}}^{1/m}\right)^m
\right]^2
$$
onde:
- $K(\theta)$ é condutividade hidráulica insaturada $[\mathrm{L}\,\mathrm{T}^{-1}]$
- $K_{\mathrm{sat}}$ é condutividade hidráulica saturada $[\mathrm{L}\,\mathrm{T}^{-1}]$
- $\ell$ é o parâmetro de conectividade dos poros $[-]$

Se $\ell$ não for fornecido, um valor padrão de $\ell = 0.5$ será usado.

---

### 4.5 Capacidade de infiltração baseada em Darcy

A capacidade de infiltração representa o fluxo máximo que pode ser transmitido ao solo dado o estado hidráulico atual. No código atual, isso não se baseia apenas em um único valor $K(\theta)$. Em vez disso, HydroPol2D usa:
- uma sucção de balde representativa com base no armazenamento vadose atual,
- um preditor de umedecimento próximo à superfície,
- e uma condutividade próxima da superfície ponderada que combina a condutividade de entrada saturada com a condutividade da camada superior molhada.

O preditor de umedecimento temporário é
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
onde:
- $w_{\mathrm{wet}}$ é a profundidade de umedecimento candidata dentro da etapa $[\mathrm{L}]$
- $S_{\mathrm{top,def}}$ é o déficit de armazenamento restante da camada próxima à superfície $[\mathrm{L}]$
- $\theta_{\mathrm{top}}$ é o conteúdo de água previsto na parte inferior da camada próxima à superfície $[-]$

A condutividade efetiva de entrada é então avaliada como
$$
K_{\mathrm{soil}}
=
w_K K_{\mathrm{sat}}+
\left(1-w_K\right) K(\theta_{\mathrm{top}})
$$
onde $w_K$ é o peso da condutividade próxima à superfície. A capacidade de infiltração é então calculada como
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
onde:
- $I_{\mathrm{cap}}$ é a capacidade de infiltração $[\mathrm{L}\,\mathrm{T}^{-1}]$
- $h_{\mathrm{pond}}$ é a cabeça da superfície $[\mathrm{L}]$
- $L_{\mathrm{top}}$ é o comprimento da resistência próxima à superfície (padrão $\approx 0.05\,\mathrm{m}$)
- $\Delta h_{\mathrm{max}}$ é a diferença máxima da cabeça motriz (normalmente $1\,\mathrm{m}$)

Esta formulação é responsável pela infiltração impulsionada pela gravidade e pela capilaridade, ao mesmo tempo que se aproxima da molhagem rápida no limite da superfície. O preditor de umedecimento **não** adiciona água ao estado do solo por si só; apenas o fluxo de infiltração aceito atualiza o armazenamento vadose.

---

### 4.6 Infiltração limitada por fornecimento e armazenamento limitado

A água disponível para infiltração é determinada a partir da profundidade efetiva da água superficial. Quando a interceptação está inativa:
$$
d_{\mathrm{eff}} = d
$$
A taxa de infiltração correspondente com fornecimento limitado é
$$
i_{\mathrm{sup}} = \frac{d_{\mathrm{eff}}}{\Delta t_{\mathrm{h}}}
$$
onde:
- $d_{\mathrm{eff}}$ é a profundidade efetiva da água da lagoa $[\mathrm{L}]$
- $\Delta t_{\mathrm{h}}$ é o intervalo de tempo em horas $[\mathrm{T}]$

A taxa de infiltração limitada por armazenamento é
$$
i_{\mathrm{store}} = \frac{S_{\mathrm{uz,rem}}}{\Delta t_{\mathrm{h}}}
$$
A taxa de infiltração real é então
$$
i = \min\!\left(i_{\mathrm{sup}},\,I_{\mathrm{cap}},\,i_{\mathrm{store}}\right)
$$
Restrições adicionais são aplicadas:
- $i = 0$ sobre células impermeáveis
- $i = 0$ quando $z_{\mathrm{wt}} \le 0$

Assim, a infiltração é simultaneamente **limitada pelo fornecimento**, **limitada pela capacidade** e **limitada pelo armazenamento**. No modo em camadas, a aceitação é adicionalmente limitada pelo explícito déficit de armazenamento próximo à superfície antes que a água possa continuar a escoar para baixo através das camadas vadosas mais profundas.

---

### 4.7 Atualização de armazenamento Vadose

A profundidade infiltrada ao longo do intervalo de tempo é
$$
\Delta I = i\,\Delta t_{\mathrm{h}}
$$
e o armazenamento vadose é atualizado como
$$
S_{\mathrm{uz}}^{\,\mathrm{new}} = S_{\mathrm{uz}} + \Delta I
$$
sujeito a
$$
0 \le S_{\mathrm{uz}}^{\,\mathrm{new}} \le S_{\mathrm{uz,max}}
$$
Na implementação em camadas padrão, a infiltração aceita primeiro preenche o armazenamento próximo à superfície e o armazenamento vadose total é então sincronizado em:
- armazenamento próximo à superfície,
- armazenamento na zona raiz,
- armazenamento na zona de transmissão.

A expressão escalar acima é, portanto, o resumo conceitual de uma atualização em camadas, e não a única representação interna.---

## 5. Acúmulo, derretimento e sublimação de neve {#5-snow-accumulation-melt-and-sublimation}

Quando a modelagem de neve está ativa, o HydroPol2D acompanha o equivalente de água da neve (SWE), a densidade da neve e a profundidade física da neve em cada célula ativa da grade. Os parâmetros de neve são lidos da tabela de parâmetros LULC e atribuídos à grade a partir do `LULC_Index`. O caminho interno das forçantes meteorológicas fornece a temperatura média do ar, a temperatura mínima do ar e a velocidade do vento. Por isso, as simulações de neve exigem `flag_ETP = 1`, `flag_input_ETP_map = 0` e uma planilha meteorológica que cubra o período da simulação.

---

### 5.1 Particionamento chuva-neve {#51-rain-snow-partitioning}

Cada classe LULC fornece um limiar até o qual toda a precipitação é neve, $T_{\mathrm{snow}}$, e um limiar a partir do qual toda a precipitação é chuva, $T_{\mathrm{rain}}$, ambos em $^{\circ}\mathrm{C}$. A fração de neve é

$$
f_{\mathrm{snow}}
=
\begin{cases}
1, & T_{\mathrm{air}} \le T_{\mathrm{snow}} \\
\dfrac{T_{\mathrm{rain}}-T_{\mathrm{air}}}{T_{\mathrm{rain}}-T_{\mathrm{snow}}}, & T_{\mathrm{snow}} < T_{\mathrm{air}} < T_{\mathrm{rain}} \\
0, & T_{\mathrm{air}} \ge T_{\mathrm{rain}}.
\end{cases}
$$

Os limiares devem satisfazer $T_{\mathrm{rain}} \ge T_{\mathrm{snow}}$. Limiares iguais produzem uma partição em degrau nessa temperatura. A neve e a chuva resultantes são

$$
P_{\mathrm{snow}}=P_{\mathrm{gross}}f_{\mathrm{snow}}
$$

$$
P_{\mathrm{rain}}=P_{\mathrm{gross}}-P_{\mathrm{snow}}
$$

onde $f_{\mathrm{snow}}$ é a fração de neve, que depende da temperatura.

A partição vem antes da copa. Só a chuva $P_{\mathrm{rain}}$ entra no modelo de interceptação da Seção 2, no lugar de $P_{\mathrm{gross}}$; a neve vai para o manto de neve, e o degelo $M_{\mathrm{snow}}$ chega à superfície sem passar pela copa.

---

### 5.2 Equivalente de água da neve {#52-snow-water-equivalent}

O balanço de SWE é

$$
\mathrm{SWE}_t=\mathrm{SWE}_{t-1}+P_{\mathrm{snow}}-M_{\mathrm{snow}}-E_{\mathrm{s}}
$$

onde todos os termos estão em milímetros de equivalente de água e $E_{\mathrm{s}}$ é a sublimação.

---

### 5.3 Derretimento da neve e ajuste ao passo de tempo {#53-snowmelt-and-timestep-scaling}

O derretimento da neve é a soma de um termo de graus-dia e de um termo de radiação líquida positiva. Para um passo de roteamento de $\Delta t_s$ segundos e $\Delta t_d=\Delta t_s/86400$ dias,

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

Aqui, $\mathrm{DDF}$ é o fator de graus-dia específico da classe LULC $[\mathrm{mm\,^{\circ}C^{-1}\,day^{-1}}]$, $Q_{\mathrm{net}}$ é o fluxo de radiação líquida calculado internamente $[\mathrm{W\,m^{-2}}]$ e $L_f=3.34\times10^5\ \mathrm{J\,kg^{-1}}$ é o calor latente de fusão. Um fluxo de $1\ \mathrm{kg\,m^{-2}}$ corresponde a $1\ \mathrm{mm}$ de equivalente de água. O derretimento não pode exceder o SWE disponível.

---

### 5.4 Densidade e profundidade da neve {#54-snow-density-and-depth}

A neve nova usa a densidade inicial específica da classe LULC, $\rho_{\mathrm{init}}$. A neve existente e a neve nova são misturadas na proporção do SWE antes da compactação. A densidade então evolui como

$$
\rho_{\mathrm{snow}}^{\,\mathrm{new}}=
\rho_{\mathrm{snow}}^{\,\mathrm{mixed}}+
\Delta t_d\left[
k_t\max(T_{\mathrm{air}},0)+
k_{\mathrm{swe}}\mathrm{SWE}+
k_DH_{\mathrm{snow}}\right]
$$

com $\rho_{\mathrm{init}}\le\rho_{\mathrm{snow}}\le\rho_{\mathrm{max}}$. A profundidade da neve é

$$
H_{\mathrm{snow}}=\frac{1000\,\mathrm{SWE}}{\rho_{\mathrm{snow}}}
$$

---

O fator 1000 converte a lâmina de equivalente de água em profundidade física da neve quando o SWE está em milímetros e a densidade está em $\mathrm{kg\,m^{-3}}$.

### 5.5 Sublimação {#55-sublimation}

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

Aqui, $C_e$ é o coeficiente de sublimação específico da classe LULC, $u$ é a velocidade do vento $[\mathrm{m\,s^{-1}}]$, e $q_s$ e $q_a$ são a umidade específica de saturação e a umidade específica do ar ambiente. A implementação atual estima $q_a$ a partir dos campos de temperatura disponíveis. A sublimação é não negativa e não pode exceder o SWE que resta após o derretimento.

---

### 5.6 Estados iniciais da neve e fallback de códigos de classe {#56-initial-snow-states-and-class-code-fallback}

`Initial_SWE_path` e `Initial_Snow_Depth_path` são rasters opcionais. Sem nenhum dos dois, o modelo inicializa o SWE e a profundidade da neve com zero e mantém a densidade de neve nova específica da classe LULC. Com apenas um raster, o outro estado é derivado dessa densidade. Com os dois rasters, o modelo deriva a densidade a partir do SWE e da profundidade e rejeita pares positivos fora da faixa de densidade configurada. Nodata no raster significa que nenhuma neve inicial foi especificada para aquela célula.

Se o raster LULC contiver um código válido que não esteja na tabela LULC, de solo ou de neve, o HydroPol2D atribui a média ponderada pela área das propriedades das células mapeadas. O modelo grava `Input_Class_Code_Audit.csv`, que lista os códigos do raster, os índices de tabela mapeados, a área que recebeu o fallback e as propriedades aplicadas. Índices de tabela duplicados ou não numéricos, ou uma tabela sem classes mapeadas, continuam sendo erros de entrada.

### 5.7 Atualização da água superficial em condições de neve {#57-surface-water-update-under-snow-conditions}

$$
d_t=d_p+M_{\mathrm{snow}}+P_{\mathrm{rain}}
$$

Se a modelagem de neve estiver desativada,

$$
d_t=d_p+P_{\mathrm{eff}},
$$
onde $d_t$ e $d_p$ são a lâmina de água superficial atual e a anterior.

---

## 6. Armazenamento Vadose, recarga e feedback das águas subterrâneas

### 6.1 Estrutura vadosa em camadas padrão

A formulação padrão atual é um **sistema vadose em camadas**, e não um único balde de recarga. A água é rastreada em:
- uma camada próxima à superfície,
- uma camada da zona raiz,
- uma camada de transmissão,
- e uma interface de acoplamento de águas subterrâneas abaixo da camada de transmissão.

Para uma camada vadosa genérica $\ell$ com armazenamento ativo $S_{\ell}$ (água acima de $\theta_{\mathrm{r}}$, como lâmina sobre a célula inteira) e espessura $z_{\ell}$, a água fica na fração permeável $f_p$ da célula:
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
A camada começa com $S_{\ell} = f_p(\theta_i - \theta_{\mathrm{r},\ell})\, z_{\ell}$ e armazena no máximo $f_p(\theta_{\mathrm{sat},\ell} - \theta_{\mathrm{r},\ell})\, z_{\ell}$. Em um intervalo de tempo $\Delta t$, ela drena $f_p K_{\ell} \Delta t$ para a camada de baixo, limitada pela capacidade de armazenamento disponível na camada receptora. (Antes de 26/10/2026, o armazenamento inicial e a drenagem não incluíam $f_p$, e por isso células parcialmente impermeáveis começavam úmidas demais e drenavam devagar demais.)
### 6.2 Drenagem descendente e recarga

No caminho padrão:
1. a drenagem próxima à superfície move-se primeiro para a zona radicular quando existe armazenamento radicular,
2. a drenagem da zona raiz se move para a zona de transmissão quando existe armazenamento de transmissão,
3. a drenagem da zona de transmissão torna-se recarga para as águas subterrâneas.

Conceitualmente, a recarga das águas subterrâneas ao longo de um intervalo de tempo pode ser resumida como
$$
R_{\mathrm{gw}}
=
\frac{\Delta S_{\mathrm{trans}\rightarrow\mathrm{gw}}}{\Delta t}
$$
com drenagem direta opcional das camadas superiores apenas onde as camadas vadosas inferiores estão ausentes. Esta cascata em camadas é a história canônica de recarga do HydroPol2D. O antigo fechamento Darcy de balde único permanece disponível apenas como uma formulação alternativa e não deve ser tratado como o caminho teórico padrão.
### 6.3 Ascensão capilar opcional e acoplamento assíncrono de águas subterrâneas

Quando `flag_capillary_rise = 1`, as águas subterrâneas rasas podem devolver a água para cima, para o armazenamento vadoso disponível. A lógica de ascensão capilar implementada aumenta com:
- profundidade mais rasa do lençol freático,
- maior déficit de armazenamento na camada receptora,
- e condutividade de camada maior.

A troca líquida vadose-água subterrânea acumulada pelo programador de águas subterrâneas é, portanto,
$$
R_{\mathrm{net}} = R_{\mathrm{down}} - C_{\mathrm{up}}
$$
onde:
- $R_{\mathrm{down}}$ é a recarga total para baixo da drenagem em camadas
- $C_{\mathrm{up}}$ é uma troca de ascensão capilar ascendente

Esta troca líquida é acumulada a cada passo da água superficial, enquanto as cabeceiras saturadas das águas subterrâneas podem ser atualizadas em um cronograma assíncrono mais lento.
### 6.4 Excesso de saturação e exfiltração de águas subterrâneas

Após a atualização das águas subterrâneas, HydroPol2D recalcula a capacidade vadosa usando a posição atualizada do lençol freático. Qualquer água que não caiba mais na zona não saturada retorna à superfície como excesso de saturação:
$$
S_{\mathrm{excess}}
=
\max\!\left(
S_{\mathrm{uz}} - S_{\mathrm{uz,max}}^{\,\mathrm{new}},
0
\right)
$$
A altura da água subterrânea que se eleva acima da superfície local também gera exfiltração:
$$
q_{\mathrm{exf}}
=
\max\!\left(
0,\,
h_{\mathrm{gw}} - z_{\mathrm{surf}}
\right)
\frac{S_y}{\Delta t}
$$
onde $S_y$ é o rendimento específico. A formulação canônica completa das águas subterrâneas, incluindo o programador assíncrono e o solucionador de fluxo lateral Boussinesq, está documentada na página [Modelo de Águas Subterrâneas](./groundwater-model).

### 6.5 Opção de subsuperfície em camadas {#65-layered-subsurface-option}

A estrutura acima é a padrão. A [subsuperfície em camadas](./layered-subsurface), opcional, mantém os três armazenamentos de solo, mas os coloca sobre camadas de regolito que chegam à profundidade do leito rochoso. Nesse esquema, um lençol freático em elevação preenche o espaço poroso vazio do solo e do regolito, em vez de empurrar a água do solo para a superfície.

---

## 7. Resumo

O modelo hidrológico em HydroPol2D integra:
- interceptação do dossel,
- Evapotranspiração de Penman-Monteith,
- Infiltração baseada em Darcy com condutividade próxima à superfície ponderada,
- acúmulo de neve e derretimento,
- armazenamento vadoso em camadas e acoplamento de águas subterrâneas,
- estresse de Feddes opcional na absorção de água pelas raízes,

em uma estrutura unificada e consistente em massa que resolve os fluxos verticais de água na escala da célula da grade e fornece o forçamento hidrológico para o modelo hidrodinâmico.

---
