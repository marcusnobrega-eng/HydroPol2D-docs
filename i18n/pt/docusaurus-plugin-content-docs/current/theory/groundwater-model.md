---
title: Modelo de águas subterrâneas
---
import useBaseUrl from '@docusaurus/useBaseUrl';

# Modelo de águas subterrâneas

## 1. Visão geral

O componente de águas subterrâneas de HydroPol2D representa a dinâmica acoplada de:
- armazenamento na zona vadose,
- recarregar da infiltração,
- fluxo lateral saturado de águas subterrâneas,
- exfiltração de águas subterrâneas para a superfície,
- e interação das águas subterrâneas com as células dos rios.

A implementação atual combina três componentes complementares:
1. um **módulo vadose/recarga em camadas**, que move a água através do armazenamento próximo à superfície, zona raiz e zona de transmissão usando um fechamento Darcy reduzido consistente com Richards com base nas relações constitutivas van Genuchten-Mualem,

2. um **módulo de troca de ascensão capilar**, que pode mover a água para cima, de águas subterrâneas rasas para o armazenamento vadoso disponível, e

3. um **solucionador bidimensional de fluxo de água subterrânea Boussinesq**, que direciona o fluxo saturado lateralmente através do domínio e retorna a exfiltração para a superfície da terra quando o lençol freático sobe acima da elevação da superfície local.

Esta estrutura permite que HydroPol2D represente o acoplamento dinâmico entre:
- águas superficiais,
- armazenamento vadoso,
- recarga de águas subterrâneas,
- fluxo saturado de águas subterrâneas,
- e fluxo de retorno com excesso de saturação.


<p align="center">
  <img src={useBaseUrl('/img/theory/groundwater-model.pt.svg')} width="720" alt="Três células em degraus da encosta ao rio, com camadas de solo, lençol freático, fluxo lateral, exfiltração, troca com o rio e aquífero profundo" />
</p>
<p align="center">
  <em>Figura 1. O esquema padrão de água subterrânea em três células. A recarga e a ascensão capilar movem o lençol freático h a cada passo da superfície. O fluxo lateral de Boussinesq segue o relógio da água subterrânea. A exfiltração e o excesso de saturação devolvem água onde h chega ao terreno.</em>
</p>

### 1.1 Dois esquemas de subsuperfície {#11-two-subsurface-schemes}

O HydroPol2D tem dois esquemas de subsuperfície. Esta página descreve o esquema padrão.

| Esquema | Aquífero | Chave | Página |
|---|---|---|---|
| Padrão | Dentro da coluna de solo; a base do aquífero é o terreno menos a profundidade do solo | padrão | esta página |
| Em camadas | Camadas de solo sobre camadas de regolito, até a profundidade do leito rochoso (limitada a 50 m) | Python `vertical.subsurface.scheme: layered`; MATLAB `flag_layered_subsurface = 1` | [Subsuperfície em Camadas](./layered-subsurface) |

Os dois esquemas podem alimentar o aquífero profundo opcional descrito na [Seção 13](#13-deep-aquifer).

Nesta página, "vadose em camadas" se refere aos três armazenamentos de solo do esquema padrão (camada superficial, zona radicular e transmissão). Não é o esquema de subsuperfície em camadas.

---

## 2. Estrutura Conceitual Geral

O modelo de águas subterrâneas é acoplado a dois relógios. A troca da zona vadosa é avaliada a cada intervalo de tempo da água superficial porque a infiltração e a evapotranspiração precisam de feedback rápido da umidade do solo. Esta troca líquida altera as cargas do lençol freático a cada passo da água superficial. O programador de águas subterrâneas é sempre assíncrono, e só o fluxo lateral das águas subterrâneas, quando está ativo, espera por ele. A atualização lateral costuma seguir um intervalo alvo diário, a menos que os limites de estabilidade ou de variação de carga exijam um intervalo menor.
A lógica é:
1. calcular a posição do lençol freático a partir da atual altura da água subterrânea;
2. determinar o armazenamento não saturado máximo permitido pela profundidade atual do lençol freático;
3. calcular a drenagem/recarga das camadas vadosas para as águas subterrâneas durante a atual etapa de superfície;
4. calcular a ascensão capilar das águas subterrâneas para as camadas vadosas quando ativado,
5. alterar as cargas do lençol freático pela troca líquida a cada passo da água superficial,
6. calcular a exfiltração das águas subterrâneas para a superfície onde a carga ultrapassa a superfície do terreno,
7. resolver o fluxo lateral de águas subterrâneas usando uma equação 2D Boussinesq quando o fluxo lateral está ativo (`flag_baseflow = 1` no MATLAB, `vertical.groundwater_lateral_flow: true` no HydroPol2D-Python) e a atualização é devida pelo programador;
8. somar à superfície a exfiltração da atualização lateral;
9. armazenamento vadoso correto se o aumento do lençol freático reduzir o armazenamento insaturado disponível,
10. atualizar a profundidade da água superficial em conformidade.

As principais variáveis ​​são:
- $h$ = carga hidráulica da água subterrânea $[\mathrm{L}]$
- $z_0$ = elevação da base do aquífero ou elevação do leito rochoso $[\mathrm{L}]$
- $H = h - z_0$ = espessura saturada $[\mathrm{L}]$
- $R$ = taxa de recarga para águas subterrâneas $[\mathrm{L}\,\mathrm{T}^{-1}]$
- $q_{\mathrm{exf}}$ = fluxo de exfiltração das águas subterrâneas para a superfície $[\mathrm{L}\,\mathrm{T}^{-1}]$
- $S_y$ = rendimento específico $[-]$
- $K$ = condutividade hidráulica saturada $[\mathrm{L}\,\mathrm{T}^{-1}]$

### 2.1 Agendador assíncrono {#21-asynchronous-scheduler}

O agendador assíncrono fica sempre ativo quando a modelagem de águas subterrâneas está habilitada. Ele decide apenas quando a atualização lateral de Boussinesq é executada. Os principais controles são:
| Controlar | Padrão | Significado |
|---|---:|---|
| `flag_groundwater_async` | 1 | Não é lido: a atualização lateral sempre segue o agendador (Seção 7.1). |
| `groundwater_target_dt_s` | 86400 | Intervalo máximo entre atualizações laterais, em segundos (um dia). O HydroPol2D-Python também lê esse valor de uma planilha antiga em minutos, como `groundwater_target_dt_min` (1440). |
| `groundwater_min_dt_s` | 60 | Intervalo mínimo entre atualizações laterais e menor subpasso de Boussinesq, em segundos. Na planilha antiga, a chave é `groundwater_min_dt_min` (1). |
| `groundwater_max_head_change_m` | 0,25 | HydroPol2D-Python: força uma atualização lateral quando o lençol freático variou esse valor desde a última. O esquema padrão do MATLAB não usa essa configuração (Seção 7.1). |
| `groundwater_head_tolerance_m` | 0,001 | Tolerância absoluta de carga dos subpassos adaptativos de Boussinesq, em metros. O MATLAB também a usa no gatilho de variação de carga. |
| `groundwater_relative_tolerance` | 0,001 | Tolerância relativa sobre a espessura saturada, usada junto com `groundwater_head_tolerance_m`. |
| `groundwater_courant` | 0,25 | Fator de estabilidade para a estimativa do intervalo de tempo das águas subterrâneas Boussinesq. |
| `flag_capillary_rise` | 1 | Ativa a ascensão capilar do lençol freático para a zona radicular quando o armazenamento em camadas do solo está presente. |

No HydroPol2D-Python, essas configurações ficam no bloco `vertical`, e a ascensão capilar é `vertical.capillary_rise` (padrão true).

O agendador guarda o tempo desde a última atualização lateral, o subpasso sugerido pela última execução adaptativa de Boussinesq, o número de atualizações laterais e três lâminas por célula. A troca líquida pendente guarda apenas a troca do passo atual. A atualização local a soma às cargas e a zera no mesmo passo. A recarga pendente e a ascensão capilar pendente são totais acumulados desde a última atualização lateral e são zeradas quando essa atualização é executada. Para o gatilho de variação de carga, o HydroPol2D-Python também guarda a variação de carga aplicada desde a última atualização lateral, e o código MATLAB guarda a carga dessa atualização. O solucionador de Boussinesq não recebe termo de recarga, porque as cargas já incluem a troca líquida. Sem fluxo lateral, o agendador apenas zera esses totais, a cada passo no MATLAB e quando o gatilho é acionado no HydroPol2D-Python.

---

## 3. Posição do lençol freático e capacidade da zona não saturada

HydroPol2D determina a posição do lençol freático em relação à superfície da terra usando a altura atual da água subterrânea.
Deixar:
- $z_{\mathrm{surf}}$ = elevação da superfície terrestre $[\mathrm{L}]$
- $D_{\mathrm{soil}}$ = profundidade do solo $[\mathrm{L}]$
- $h$ = carga hidráulica da água subterrânea $[\mathrm{L}]$

A espessura saturada acima do leito rochoso é calculada como
$$
z_{\mathrm{gw}}
=
h - \left(z_{\mathrm{surf}} - D_{\mathrm{soil}}\right)
$$
A profundidade da superfície da terra até o lençol freático é então
$$
z_{\mathrm{wt}}
=
D_{\mathrm{soil}} - z_{\mathrm{gw}}
$$
com a restrição
$$
z_{\mathrm{wt}} \ge 0
$$
onde:
- $z_{\mathrm{gw}}$ = espessura saturada medida para cima a partir da base do aquífero $[\mathrm{L}]$
- $z_{\mathrm{wt}}$ = profundidade até o lençol freático abaixo da superfície do solo $[\mathrm{L}]$

Esta variável é central para o acoplamento entre o armazenamento vadoso e as águas subterrâneas.
### 3.1 Armazenamento máximo não saturado

A água máxima que pode ser armazenada na zona não saturada é definida usando a convenção atual **armazenamento ativo acima do conteúdo de água residual**:
$$
S_{\mathrm{UZ,max}}
=
z_{\mathrm{wt}}
\left(
\theta_{\mathrm{sat}} -\theta_r
\right)
$$
onde:
- $S_{\mathrm{UZ,max}}$ = armazenamento não saturado máximo $[\mathrm{L}]$
- $\theta_{\mathrm{sat}}$ = conteúdo volumétrico saturado de água $[-]$
- $\theta_r$ = teor volumétrico de água residual $[-]$

Assim, à medida que o lençol freático sobe, a zona vadosa diminui e a capacidade de armazenamento disponível para infiltração diminui. Quando o armazenamento em camadas do solo está ativo, o código avalia este limite através das capacidades explícitas dos armazenamentos próximos à superfície, zona radicular e zona de transmissão após truncamento pela posição atual do lençol freático.

---

## 4. Troca de Vadose em Camadas Padrão para Água Subterrânea

A recarga é calculada a partir do armazenamento vadoso atual após o módulo de infiltração já ter movido a água da superfície para o solo. Isso evita infiltração de contagem dupla. O caminho padrão atual é dividido em camadas:
- armazenamento próximo à superfície,
- armazenamento na zona raiz,
- armazenamento na zona de transmissão,
- recarga de águas subterrâneas.

### 4.1 Acoplamento em degrau superficial

A troca vadose é avaliada em cada etapa da água superficial porque a infiltração e a evapotranspiração precisam de feedback imediato da umidade do solo. Na implementação atual, a infiltração é primeiro aceita pelo módulo de infiltração, armazenada nas camadas vadosas e só então drenada para baixo em direção às águas subterrâneas.
### 4.2 Estado constitutivo em camadas

Para uma camada vadosa genérica $\ell$ com armazenamento ativo $S_{\ell}$ e espessura $z_{\ell}$, HydroPol2D avalia
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
com
$$
m_{\ell} = 1 -\frac{1}{n_{\ell}}
$$
onde:
- $\theta_{\ell}$ = teor de água da camada $[-]$
- $f_p$ = fração permeável da célula $[-]$; a água da camada fica na parte permeável, e $S_{\ell}$ é uma lâmina sobre a célula inteira
- $S_{e,\ell}$ = saturação efetiva da camada $[-]$
- $K_{\ell}$ = condutividade insaturada da camada $[\mathrm{L}\,\mathrm{T}^{-1}]$
- $\ell_v$ = Parâmetro de conectividade de poros Mualem $[-]$, fixado em 0,5 nesta etapa de drenagem nos dois códigos

Esta é a mesma família constitutiva van Genuchten-Mualem usada pelo módulo de infiltração.
### 4.3 Cascata de drenagem descendente

O caminho de recarga em camadas é calculado como uma cascata descendente:
1. a drenagem próxima à superfície vai para a zona radicular quando existe armazenamento radicular,
2. a drenagem da zona raiz vai para a zona de transmissão quando existe armazenamento de transmissão,
3. a drenagem da zona de transmissão torna-se recarga de água subterrânea.

Conceitualmente, a profundidade de drenagem de uma camada ao longo de um intervalo de tempo pode ser resumida como
$$
\Delta D_{\ell} \approx f_p\,K_{\ell}\,\Delta t
$$
sujeito a:
- água disponível na camada doadora,
- capacidade restante na camada receptora,
- e a espessura atual da camada e os parâmetros do solo.

A recarga líquida descendente que atinge as águas subterrâneas é então
$$
R_{\mathrm{down}}
=
\frac{\Delta S_{\rightarrow \mathrm{gw}}}{\Delta t}
$$
onde $\Delta S_{\rightarrow \mathrm{gw}}$ é a transmissão total de água para as águas subterrâneas durante a atual etapa de superfície. A drenagem direta da zona próxima à superfície ou radicular para as águas subterrâneas ocorre apenas quando as camadas vadosas inferiores estão ausentes.
### 4.4 Formulação substituta legada

O código MATLAB ainda contém o antigo fechamento de recarga de balde representativo para casos em que os dados explícitos de armazenamento em camadas não estão disponíveis. Nesse modo de fallback, um único estado de armazenamento vadoso é convertido em um conteúdo representativo de água e drenado com um fechamento semelhante ao Darcy. O HydroPol2D-Python não tem essa alternativa e sempre usa as três camadas. Essa formulação deve ser tratada como **legado/substituto**, e não como o caminho teórico principal para o modelo atual.

---

## 5. Ascensão Capilar Opcional

Quando `flag_capillary_rise = 1`, HydroPol2D permite que águas subterrâneas rasas subam para o armazenamento vadoso disponível. A implementação atual é uma transferência de van Genuchten-Mualem para a zona radicular, limitada pelo armazenamento disponível, e não uma solução completa da equação de Richards.
A troca ascendente aumenta com:
- profundidade mais rasa do lençol freático,
- maior déficit de armazenamento na camada receptora,
- e maior condutividade saturada da zona radicular.

Em um passo de superfície $\Delta t$, a transferência capilar ascendente é
$$
C_{\mathrm{up}}\,\Delta t
=
\min\!\left(
S_{\mathrm{def}},\;
K_{\mathrm{sat,root}}\,K_r(g)\,\Delta t,\;
S_{\mathrm{gw}}
\right)
$$
com $g = \max(z_{\mathrm{wt}} - z_{\mathrm{root}}, 0)$, $S_e(g) = \left[1 + (\alpha g)^{n}\right]^{-m}$ e $K_r(g) = S_e(g)^{\ell_v}\left[1 - \left(1 - S_e(g)^{1/m}\right)^{m}\right]^2$, onde:
- $S_{\mathrm{def}}$ é o déficit da camada receptora abaixo da capacidade de campo, $\max\!\left(S_e(h_{\mathrm{fc}})\,S_{\max} - S, 0\right)$, com $S$ e $S_{\max}$ o armazenamento e a capacidade dessa camada
- $h_{\mathrm{fc}}$ é a sucção da capacidade de campo, `capillary_field_capacity_head_m` (padrão 3,3 m)
- $g$ é a distância entre o lençol freático e a base da zona radicular $z_{\mathrm{root}}$
- $S_{\mathrm{gw}} = S_y\,(h - z_0)$ é a água subterrânea armazenada na célula
- $\alpha$, $n$, $m$ e $\ell_v$ são os parâmetros de van Genuchten-Mualem do solo

No código atual, a ascensão capilar preenche apenas a zona radicular, ou a camada próxima à superfície quando as raízes terminam dentro dela e não existe uma zona radicular separada. A zona de transmissão não recebe ascensão capilar.
A troca líquida vadose-água subterrânea de cada passo da água superficial é, portanto,
$$
R_{\mathrm{net}} = R_{\mathrm{down}} - C_{\mathrm{up}}
$$
onde $C_{\mathrm{up}}$ é o fluxo de ascensão capilar ascendente total.

---

## 6. Modelo bidimensional de fluxo de águas subterrâneas Boussinesq

Depois da atualização local da carga, e só quando o fluxo lateral está ativo e a atualização é devida pelo agendador, HydroPol2D direciona as águas subterrâneas lateralmente usando a função `Boussinesq_2D_explicit`. O HydroPol2D-Python usa a mesma discretização.
Este solucionador representa o sistema de águas subterrâneas saturadas através de uma aproximação de fluxo não confinado integrada em profundidade.
### 6.1 Equação governante

O roteamento das águas subterrâneas segue a equação 2D Boussinesq de forma conservadora:
$$
S_y \frac{\partial h}{\partial t}
=- \nabla\cdot\mathbf{F}
+
R
$$
onde:
- $S_y$ = rendimento específico $[-]$
- $h$ = carga hidráulica da água subterrânea $[\mathrm{L}]$
- $\mathbf{F}$ = vetor de fluxo de águas subterrâneas $[\mathrm{L}^2\,\mathrm{T}^{-1}]$
- $R$ = taxa de recarga $[\mathrm{L}\,\mathrm{T}^{-1}]$

HydroPol2D avalia esta equação numericamente calculando os fluxos nas interfaces das células e, em seguida, atualizando explicitamente a altura da água subterrânea. No código, o termo de recarga é aplicado separadamente. A troca líquida altera as cargas a cada passo da água superficial (Seção 7.1), e o solucionador lateral é chamado com $R = 0$ ao longo do tempo decorrido desde sua última execução.
### 6.2 Espessura saturada

A espessura saturada ativa é definida como
$$
H = \max(h - z_0, 0)
$$
onde:
- $H$ = espessura saturada $[\mathrm{L}]$
- $z_0$ = elevação da base do aquífero ou elevação do leito rochoso $[\mathrm{L}]$

Isto reforça a condição física de que não existe armazenamento saturado abaixo da base do aquífero.
### 6.3 Fluxos de interface

HydroPol2D calcula os fluxos de águas subterrâneas nas interfaces das células usando a lei de Darcy com ponderação de espessura saturada.
Para a direção $x$:
$$
F_x = -K_x H_x \frac{\partial h}{\partial x}
$$
e para a direção $y$:
$$
F_y = -K_y H_y \frac{\partial h}{\partial y}
$$
onde:
- $F_x, F_y$ = fluxos por unidade de largura $[\mathrm{L}^2\,\mathrm{T}^{-1}]$
- $K_x, K_y$ = condutividade hidráulica nas interfaces das células $[\mathrm{L}\,\mathrm{T}^{-1}]$
- $H_x, H_y$ = espessuras saturadas de interface $[\mathrm{L}]$

Na implementação, a condutividade hidráulica da interface é tomada como a média aritmética das condutividades nas células adjacentes:
$$
K_x = \frac{K_i + K_{i+1}}{2}
\qquad
K_y = \frac{K_j + K_{j+1}}{2}
$$
e a espessura saturada da interface também é calculada:
$$
H_x = \frac{H_i + H_{i+1}}{2}
\qquad
H_y = \frac{H_j + H_{j+1}}{2}
$$
### 6.4 Limitação conservadora de fluxo

Para evitar instabilidade numérica e esgotamento não físico do armazenamento de água subterrânea, HydroPol2D aplica um limitador de fluxo para que nenhuma interface possa transportar mais água do que a célula doadora contém durante uma subetapa.
Por exemplo, na direção $x$, o fluxo máximo permitido é
$$
F_{x,\max}
=
\frac{S_y H_{\mathrm{donor}}}{\Delta t}
$$
e o fluxo final da interface é limitado como
$$
F_x \leftarrow \operatorname{sign}(F_x)\,\min\left(|F_x|,\,F_{x,\max}\right)
$$

Uma expressão semelhante é usada na direção $y$.
Como o limite vale para cada interface separadamente, uma célula que drena por várias interfaces ainda pode ficar abaixo da base do aquífero em uma subetapa. O solucionador então fixa a carga em $z_0$, e a água acrescentada aparece como resíduo na verificação do balanço de massa da Seção 14.
### 6.5 Divergência dos fluxos de águas subterrâneas

A divergência do campo de fluxo é então calculada a partir dos fluxos de interface como
$$
\nabla\cdot\mathbf{F}
=
\frac{\partial F_x}{\partial x}+
\frac{\partial F_y}{\partial y}
$$
usando diferenças finitas conservadoras na grade raster.
### 6.6 Atualização explícita do preditor-corretor

O solucionador Boussinesq usa uma estratégia explícita de preditor-corretor.
#### Etapa do preditor

Uma primeira estimativa da carga é calculada usando os fluxos atuais:
$$
h^{\ast}
=
h^t + \frac{\Delta t}{S_y}\left(-\nabla \cdot \mathbf{F}^t\right)
$$
#### Etapa do corretor

Os fluxos são recalculados a partir do estado do preditor, calculados em média e usados ​​na atualização final:
$$
h^{t+\Delta t}
=
h^t+
\frac{\Delta t}{S_y}
\left(
-\nabla \cdot \mathbf{F}^{\mathrm{avg}} + R
\right)
$$
onde:
- $h^{\ast}$ = carga hidráulica preditora $[\mathrm{L}]$
- $h^{t+\Delta t}$ = carga hidráulica final após o intervalo de tempo $[\mathrm{L}]$
- $\mathbf{F}^{\mathrm{avg}}$ = média dos fluxos da interface do preditor e do corretor

Este procedimento preditor-corretor melhora a estabilidade e reduz a difusão numérica em relação a uma simples atualização explícita de Euler.

---

## 7. Tempo de atualização das águas subterrâneas e etapa adaptativa do tempo

HydroPol2D usa uma **lógica de passo de tempo de águas subterrâneas de dois níveis**.
### 7.1 Agendador assíncrono externo

A troca vadose altera as cargas do lençol freático a cada passo da água superficial. O programador de águas subterrâneas é sempre assíncrono, e só o fluxo lateral das águas subterrâneas, quando está ativo, espera por ele. A atualização lateral é executada ao final do primeiro passo de superfície em que vale uma destas condições:
- o tempo desde a última atualização lateral chega a $\max\!\left(\min(\Delta t_{\mathrm{target}}, \Delta t_{\mathrm{gw,stable}}, \Delta t_{\mathrm{sugg}}), \Delta t_{\min}\right)$, em que $\Delta t_{\mathrm{target}}$ é `groundwater_target_dt_s`, $\Delta t_{\mathrm{gw,stable}}$ é o limite de estabilidade da Seção 7.2, $\Delta t_{\mathrm{sugg}}$ é o subpasso sugerido pela última execução adaptativa de Boussinesq e $\Delta t_{\min}$ é `groundwater_min_dt_s`,
- o lençol freático variou o suficiente desde a última atualização lateral,
- o passo de superfície é o último da simulação.

O teste de variação de carga difere entre os códigos. O HydroPol2D-Python compara a maior variação de carga aplicada desde a última atualização lateral com `groundwater_max_head_change_m` (0,25 m). O esquema padrão do MATLAB não usa essa configuração. Ele executa a atualização quando, em alguma célula, $|h - h_{\mathrm{last}}| \ge \delta_h + \delta_r H$, em que $h_{\mathrm{last}}$ é a carga após a última atualização lateral, $\delta_h$ é `groundwater_head_tolerance_m` e $\delta_r$ é `groundwater_relative_tolerance` (ambos 0,001 por padrão). O solucionador lateral então avança por todo o tempo decorrido desde sua última execução.

O agendador não pode ser desligado. Nem o HydroPol2D-Python nem o código MATLAB leem `flag_groundwater_async`, então o valor 0 não força uma atualização lateral a cada passo da superfície. Um `groundwater_target_dt_s` menor deixa as atualizações laterais mais frequentes.
### 7.2 Limite explícito de estabilidade das águas subterrâneas

O limite externo do escalonador é baseado em uma estimativa de difusividade explícita para a equação Boussinesq não confinada:
$$
D = \frac{K H}{S_y}
$$
$$
\Delta t_{\mathrm{gw,stable}}
=
\frac{
C_{\mathrm{gw}} \, L_{\mathrm{grid}}^2
}{
4D_{\max}
}
$$
onde:
- $D$ = difusividade das águas subterrâneas $[\mathrm{L}^2\,\mathrm{T}^{-1}]$
- $C_{\mathrm{gw}}$ = Courant de águas subterrâneas/fator de segurança $[-]$
- $L_{\mathrm{grid}} = \min(\Delta x,\Delta y)$
- $D_{\max}$ = difusividade máxima do domínio sobre as células ativas das águas subterrâneas

Este é o limite usado pela lógica `estimate_groundwater_stable_timestep` atual.
### 7.3 Subpasso interno Boussinesq

Quando uma atualização lateral é acionada, o solucionador não recebe termo de recarga, porque a troca líquida já alterou as cargas. Ele avança as cargas ao longo do intervalo decorrido com subetapas adaptativas de preditor-corretor. Cada subetapa é no máximo o limite de estabilidade da Seção 7.2 e no mínimo `groundwater_min_dt_s`. Os dois códigos controlam o erro por duplicação de passo. Uma subetapa é aceita quando um passo inteiro e dois meios passos diferem no máximo $\delta_h + \delta_r H$ em todas as células; caso contrário, ela é encurtada e repetida. A próxima subetapa que o solucionador tentaria fica guardada como passo sugerido para a próxima atualização lateral.
No código MATLAB, cada uma dessas subetapas é ainda dividida por uma condição baseada na velocidade da forma
$$
\Delta t_{\mathrm{inner}}
\le
\min\!\left(\frac{C_v \Delta x}{|u_x|},\,
\frac{C_v \Delta y}{|u_y|}
\right)
$$
onde:
- $u_x, u_y$ são velocidades das águas subterrâneas de Darcy
- $C_v$ é o fator de segurança interno baseado na velocidade, o mesmo `groundwater_courant`

O HydroPol2D-Python faz uma única atualização de preditor-corretor por subetapa e não tem condição de velocidade.

O resultado é uma estratégia de dois níveis:
1. um limite externo do programador baseado na estabilidade explícita das águas subterrâneas e na mudança de carga permitida,
2. um loop interno de subetapas adaptativas de preditor-corretor dentro do solucionador Boussinesq.

---

## 8. Condições Limites

O solucionador de águas subterrâneas suporta:
- Condições de contorno de Dirichlet,
- condições de contorno sem fluxo,
- mascaramento de domínio.

### 8.1 Limites de Dirichlet

Se uma máscara de Dirichlet for fornecida, a cabeça é prescrita diretamente:
$$
h = h_{\mathrm{D}}
$$
nas células de limite selecionadas, onde:
- $h_{\mathrm{D}}$ = limite prescrito $[\mathrm{L}]$

### 8.2 Limites sem fluxo

Os limites sem fluxo são impostos por condições de gradiente zero no perímetro do domínio. Na prática, HydroPol2D zera o fluxo em toda interface com uma célula fora do domínio e na borda externa da grade, a menos que a célula da borda tenha carga prescrita. Esta é uma condição discreta de Neumann; o código não copia cargas para as células do perímetro.
### 8.3 Máscara de captação

Todos os cálculos de águas subterrâneas estão restritos ao domínio computacional válido. As células fora da máscara de captação são definidas como `NaN`.

---

## 9. Exfiltração de águas subterrâneas para a superfície

Depois de atualizar a altura do lençol freático, HydroPol2D calcula a exfiltração onde o lençol freático se eleva acima da superfície efetiva do terreno.
A elevação da superfície usada para exfiltração é
$$
h_{\mathrm{surf}} = z_0 + D_{\mathrm{soil}}
$$
onde:
- $h_{\mathrm{surf}}$ = elevação efetiva da superfície terrestre para emergência de água subterrânea $[\mathrm{L}]$

A exfiltração é então calculada como
$$
q_{\mathrm{exf}}
=
\max\left(0,\,h - h_{\mathrm{surf}}\right)
\frac{S_y}{\Delta t}
$$
onde:
- $q_{\mathrm{exf}}$ = fluxo de exfiltração $[\mathrm{L}\,\mathrm{T}^{-1}]$

Esta expressão significa que se a altura da água subterrânea exceder a superfície da terra, o excesso de armazenamento saturado é expelido para cima e transferido para o sistema de águas superficiais.
A cabeceira da água subterrânea é então cortada de modo que
$$
h\le h_{\mathrm{surf}}
$$
o que evita que as águas subterrâneas permaneçam acima da superfície da terra após a exfiltração ter sido contabilizada.

---

## 10. Intercâmbio Rio-Aquífero

Os dois códigos podem trocar água entre o aquífero e as células de rio. A troca é opcional e fica desligada por padrão. A chave é `flag_river_groundwater_exchange` no MATLAB e `flags.river_groundwater_exchange` no HydroPol2D-Python. Em cada célula de rio, a troca segue uma lei linear do leito,
$$
q_{\mathrm{river}}
=
\frac{K_{\mathrm{bed}}\,A_{\mathrm{bed}}}{b\,A_{\mathrm{cell}}}
\left(h - h_{\mathrm{river}}\right)
$$
onde:
- $q_{\mathrm{river}}$ = taxa de troca por unidade de área da célula, positiva do aquífero para o rio $[\mathrm{L}\,\mathrm{T}^{-1}]$
- $K_{\mathrm{bed}}$ = condutividade hidráulica do leito do rio $[\mathrm{L}\,\mathrm{T}^{-1}]$
- $A_{\mathrm{bed}}$ = área do leito, a largura do rio vezes o tamanho da célula, no máximo a área da célula $[\mathrm{L}^2]$
- $b$ = espessura do leito, `riverbed_thickness_m` (padrão 0,5 m) $[\mathrm{L}]$
- $h_{\mathrm{river}}$ = elevação da superfície da água na célula de rio $[\mathrm{L}]$

Cada passo da água superficial resolve essa lei de forma exata para dois armazenamentos ligados, o aquífero da célula e a sua água superficial, e limita o volume à água que o armazenamento doador contém. A troca é somada à troca líquida e, assim, altera a carga do lençol freático no mesmo passo que a recarga e a ascensão capilar.

---

## 11. Correção do excesso de saturação após elevação do lençol freático {#11-saturation-excess-correction-after-water-table-rise}

Depois que as cargas mudam em um passo da água superficial, o HydroPol2D recalcula a profundidade do lençol freático e, portanto, o novo armazenamento máximo não saturado:
$$
S_{\mathrm{UZ,max}}^{\,\mathrm{new}}
=
z_{\mathrm{wt}}^{\,\mathrm{new}}
\left(
\theta_{\mathrm{sat}} -\theta_r
\right)
$$
Se o armazenamento vadoso atualizado exceder esta nova capacidade, o excesso é devolvido à superfície como excesso de água de saturação:
$$
S_{\mathrm{excess}}
=
\max\left(
S - S_{\mathrm{UZ,max}}^{\,\mathrm{new}},
0
\right)
$$
A correção é então:
$$
S \leftarrow S - S_{\mathrm{excess}}
$$
e a profundidade da água superficial aumenta em
$$
h_{\mathrm{surf}}^{\,\mathrm{new}}
=
h_{\mathrm{surf}}^{\,\mathrm{old}}+
S_{\mathrm{excess}}
$$
Na implementação padrão em camadas, a correção é aplicada camada por camada. As três capacidades são recalculadas a partir do novo lençol freático, cada camada guarda no máximo a sua própria capacidade, e a soma dos excessos vai para a superfície. O HydroPol2D-Python aplica a correção após a atualização local e de novo após uma atualização lateral; o código MATLAB a aplica uma vez por passo, depois das duas. Esta é uma parte muito importante do HydroPol2D porque garante a **consistência de massa** entre as zonas vadosa e saturada quando o lençol freático sobe durante um intervalo de tempo.

---

## 12. Acoplamento de volta às águas superficiais

O modelo de águas subterrâneas retroalimenta o sistema de águas superficiais de duas maneiras:
1. **exfiltração**, através de $q_{\mathrm{exf}}$,
2. **excesso de saturação**, através de $S_{\mathrm{excess}}$.

A profundidade da água superficial é atualizada conforme
$$
d_t
=
d_t + \Delta t\,q_{\mathrm{exf}}
$$
com a conversão de unidade apropriada no código de $\mathrm{m}$ para $\mathrm{mm}$.
Isto significa que HydroPol2D permite que as águas subterrâneas influenciem ativamente a geração de inundações e a humidade próxima da superfície, em vez de tratá-las como um processo desconectado de limites inferiores.

---

## 13. Aquífero Profundo {#13-deep-aquifer}

O aquífero profundo opcional representa as águas subterrâneas lentas abaixo do aquífero modelado. Ele é semidistribuído, com um reservatório linear por sub-bacia.

### 13.1 Estrutura {#131-structure}

Uma fração fixa $f_d$ da recarga descendente vai para o aquífero profundo antes que o restante chegue ao lençol freático. A recarga de todas as células da sub-bacia $k$ alimenta o reservatório $k$. O reservatório libera

$$
Q_k = \frac{S_k}{\tau}
$$

onde:

- $S_k$ = armazenamento do reservatório $k$ $[\mathrm{L}^3]$
- $\tau$ = tempo de resposta $[\mathrm{T}]$, o mesmo para todas as sub-bacias
- $Q_k$ = vazão de retorno profunda $[\mathrm{L}^3\,\mathrm{T}^{-1}]$

Dois rasters definem a organização espacial. O raster de sub-bacias indica quais células alimentam cada reservatório. O raster de pesos do canal indica onde cada reservatório descarrega. A vazão de retorno é distribuída pelas células de rio da própria sub-bacia, em proporção ao peso.

### 13.2 Atualização {#132-update}

Para uma taxa de entrada $I_k$ ao longo de um passo $\Delta t$, o reservatório usa a solução exata da equação do reservatório linear

$$
S_{k}^{t+\Delta t}
=
S_{k}^{t}\,e^{-\Delta t/\tau}
+
I_k\,\tau\left(1-e^{-\Delta t/\tau}\right)
$$

e o volume descarregado é

$$
V_{Q,k} = I_k\,\Delta t - \left(S_{k}^{t+\Delta t} - S_{k}^{t}\right)
$$

A atualização é conservativa e não depende do tamanho do passo.

### 13.3 Estado inicial {#133-starting-state}

Como a vazão de saída é o armazenamento dividido por $\tau$, o armazenamento inicial decorre de uma vazão inicial por unidade de área $q_0$

$$
S_{k,0} = q_0\,A_k\,\tau
$$

onde $A_k$ é a área ativa da sub-bacia $k$. Informe no máximo uma das opções abaixo.

| Configuração | Significado | $q_0$ |
|---|---|---|
| `deep_aquifer_initial_baseflow_mm_day` | Escoamento de base profundo na data inicial, obtido por exemplo de um posto fluviométrico | como informado |
| `deep_aquifer_mean_recharge_mm_year` | Recarga média de longo prazo $\bar{R}$; os reservatórios começam em regime permanente | $f_d\,\bar{R}$ |
| Arquivo de estado inicial do aquífero profundo | Armazenamento por sub-bacia, gravado pela calibração das águas subterrâneas | armazenamento informado diretamente |

Sem nenhuma delas, os reservatórios começam vazios.

**A partir de um posto fluviométrico.** O HydroPol2D-Python estima $q_0$ a partir de uma série de vazões diárias com `hydropol2d estimate-deep-baseflow`, em quatro etapas.

1. Escoamento de base de Lyne–Hollick da vazão observada.
2. Segmentos de recessão e uma curva mestra de recessão (MRC).
3. Separação da cauda profunda, lenta e linear, da MRC, que também fornece $\tau$.
4. Posicionamento do escoamento de base da data inicial na MRC e divisão da sua parte profunda pela área de drenagem.

Escolha uma data inicial dentro de uma recessão. O filtro de escoamento de base fica atrasado em relação a um hidrograma em ascensão, e por isso a ferramenta avisa quando a vazão na data inicial é mais que o dobro do escoamento de base.

### 13.4 Configurações {#134-settings}

| Item | HydroPol2D-Python | HydroPol2D (MATLAB) |
|---|---|---|
| Chave | `flags.deep_aquifer` | `flag_deep_aquifer` |
| Sub-bacias | `static.deep_aquifer_subbasin_path` | `DeepAquiferSubbasins_path` |
| Pesos do canal | `static.deep_aquifer_channel_weight_path` | `DeepAquiferChannelWeight_path` |
| Fração da recarga $f_d$ | `vertical.deep_recharge_fraction` | `deep_recharge_fraction` |
| Tempo de resposta $\tau$ | `vertical.deep_aquifer_response_time_days` (padrão 180) | `deep_aquifer_tau_days` |
| Escoamento de base inicial | `vertical.deep_aquifer_initial_baseflow_mm_day` | `deep_aquifer_initial_baseflow_mm_day` |
| Recarga média | `vertical.deep_aquifer_mean_recharge_mm_year` | `deep_aquifer_mean_recharge_mm_year` |
| Arquivo de estado inicial | `static.deep_aquifer_initial_state_path` | `DeepAquiferInitialState_path` |

No MATLAB, os valores do estado inicial ficam no bloco "Deep aquifer: starting storage" da aba Soil and groundwater (veja [Configurações da Planilha do Caso](../configuration/general_data#tab-soil-and-groundwater)). O Case Builder gera os rasters de sub-bacias e de pesos do canal a partir do terreno D8 condicionado.

---

## 14. Balanço de Massa {#14-mass-balance}

O solucionador de águas subterrâneas realiza uma verificação explícita do balanço de massa durante cada atualização.
O volume de entrada de recarga é
$$
V_{\mathrm{recharge}}
=
\sum R\,\Delta t\,A_{\mathrm{cell}}
$$
O volume de perda por exfiltração é
$$
V_{\mathrm{exf}}
=
\sum q_{\mathrm{exf}}\,\Delta t\,A_{\mathrm{cell}}
$$
A mudança no armazenamento de água subterrânea é
$$
\Delta V_{\mathrm{storage}}
=
\sum S_y\,\max(h^{t+\Delta t}-z_0,0)\,A_{\mathrm{cell}}
-
\sum S_y\,\max(h^t-z_0,0)\,A_{\mathrm{cell}}
$$
O resíduo do balanço de massa é então
$$
\varepsilon_{\mathrm{gw}}
=
V_{\mathrm{recharge}}-
V_{\mathrm{exf}}-
\Delta V_{\mathrm{storage}}
$$
onde:
- $\varepsilon_{\mathrm{gw}}$ = erro de balanço de massa da água subterrânea $[\mathrm{L}^3]$

A atualização local de cada passo da água superficial fecha o mesmo balanço, com a troca líquida como termo de recarga. O solucionador lateral é chamado com $R = 0$, e a sua verificação também conta a água trocada com as células de carga prescrita. O código MATLAB guarda o resíduo lateral como erro de diagnóstico de águas subterrâneas. O HydroPol2D-Python não o guarda e acompanha o balanço hídrico do modelo inteiro.

A recarga e a ascensão capilar não ficam esperando no agendador. A troca líquida altera as cargas no mesmo passo da água superficial, e por isso nenhuma troca fica em trânsito entre atualizações laterais. Os totais pendentes de recarga e de ascensão capilar só contam o que passou desde a última atualização lateral e não são armazenamento adicional. Esta distinção é importante para interpretar o diagnóstico do balanço hídrico de todo o modelo.

---

## 15. Resumo {#15-summary}

O modelo de águas subterrâneas HydroPol2D combina:
- um **módulo de recarga de zona vadose em camadas** baseado em um fechamento Darcy – van Genuchten – Mualem,
- **ascensão capilar** das águas subterrâneas rasas para a zona radicular,
- um **programador assíncrono de águas subterrâneas** para o fluxo lateral mais lento, enquanto a troca líquida altera as cargas a cada passo da água superficial,
- um **modelo 2D Boussinesq de fluxo de águas subterrâneas** para fluxo lateral saturado,
- **passo de tempo explícito adaptativo**,
- **exfiltração superficial** quando a água subterrânea sobe acima da superfície do solo,
- uma **correção do excesso de saturação** que preserva a massa quando o lençol freático reduz a capacidade de armazenamento vadoso,
- e um **aquífero profundo** opcional, com reservatórios lineares por sub-bacia e estado inicial definido a partir de um escoamento de base ou de uma recarga média.

Esta estrutura permite que HydroPol2D represente um sistema de subsuperfície acoplado dinamicamente no qual:
- a infiltração não desaparece simplesmente em um balde estático,
- recarga afeta a altura das águas subterrâneas,
- o fluxo de água subterrânea redistribui a água lateralmente,
- e as águas subterrâneas podem retornar à superfície terrestre e influenciar a geração de fluxo superficial.

O resultado é um modelo de águas subterrâneas fisicamente interpretável, conservador em massa e totalmente integrado à arquitetura hidrológica e hidrodinâmica do HydroPol2D.