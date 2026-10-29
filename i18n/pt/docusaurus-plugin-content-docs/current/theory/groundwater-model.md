---
title: Modelo de águas subterrâneas
---

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
  <img src={require('../assets/figures/aquifer/aquifer_schematics.png').default} width="700" />
</p>
<p align="center">
  <em>Figura 1. Representação conceitual do componente aquífero em HydroPol2D.</em>
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

O modelo de águas subterrâneas é acoplado a dois relógios. A troca da zona vadosa é avaliada a cada intervalo de tempo da água superficial porque a infiltração e a evapotranspiração precisam de feedback rápido da umidade do solo. As cabeceiras das águas subterrâneas saturadas são atualizadas com menos frequência, geralmente em um intervalo de tempo alvo diário, a menos que a estabilidade ou os limites de mudança de carga exijam uma atualização mais curta.
A lógica é:
1. calcular a posição do lençol freático a partir da atual altura da água subterrânea;
2. determinar o armazenamento não saturado máximo permitido pela profundidade atual do lençol freático;
3. calcular a drenagem/recarga das camadas vadosas para as águas subterrâneas durante a atual etapa de superfície;
4. calcular a ascensão capilar das águas subterrâneas para as camadas vadosas quando ativado,
5. acumular o volume líquido de troca no programador de águas subterrâneas,
6. atualizar as cabeças saturadas de água subterrânea quando o cronograma for devido,
7. resolver o fluxo lateral de águas subterrâneas usando uma equação 2D Boussinesq quando o fluxo de base está ativo;
8. calcular a exfiltração de águas subterrâneas para a superfície;
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

O agendador assíncrono fica sempre ativo quando a modelagem de águas subterrâneas está habilitada. Os principais controles são:
| Controlar | Padrão | Significado |
|---|---:|---|
| `flag_groundwater_async` | 1 | Não é lido: a atualização saturada sempre segue o agendador (Seção 7.1). |
| `groundwater_target_dt_min` | 1440 | Intervalo alvo de atualização das águas subterrâneas, em minutos. |
| `groundwater_min_dt_min` | 1 | Intervalo mínimo de atualização das águas subterrâneas, em minutos. |
| `groundwater_max_head_change_m` | 0,25 | Força uma atualização quando o câmbio acumulado mudaria a cabeça nesse valor. |
| `groundwater_courant` | 0,25 | Fator de estabilidade para a estimativa do intervalo de tempo das águas subterrâneas Boussinesq. |
| `flag_capillary_rise` | 1 | Permite a ascensão capilar em camadas simples quando o armazenamento em camadas do solo está presente. |

A recarga pendente, a ascensão capilar e a troca líquida são armazenadas como variáveis ​​de estado do escalonador. Quando uma atualização das águas subterrâneas é executada, a profundidade líquida de troca acumulada é dividida pelo intervalo decorrido das águas subterrâneas para formar o termo de recarga passado para o solucionador saturado.

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
\frac{S_{\ell}}{z_{\ell}}
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
- $S_{e,\ell}$ = saturação efetiva da camada $[-]$
- $K_{\ell}$ = condutividade insaturada da camada $[\mathrm{L}\,\mathrm{T}^{-1}]$
- $\ell_v$ = Parâmetro de conectividade de poros Mualem $[-]$

Esta é a mesma família constitutiva van Genuchten-Mualem usada pelo módulo de infiltração.
### 4.3 Cascata de drenagem descendente

O caminho de recarga em camadas é calculado como uma cascata descendente:
1. a drenagem próxima à superfície vai para a zona radicular quando existe armazenamento radicular,
2. a drenagem da zona raiz vai para a zona de transmissão quando existe armazenamento de transmissão,
3. a drenagem da zona de transmissão torna-se recarga de água subterrânea.

Conceitualmente, a profundidade de drenagem de uma camada ao longo de um intervalo de tempo pode ser resumida como
$$
\Delta D_{\ell} \approx K_{\ell}\,\Delta t
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

HydroPol2D ainda contém o antigo fechamento de recarga de balde representativo para casos em que os dados explícitos de armazenamento em camadas não estão disponíveis. Nesse modo de fallback, um único estado de armazenamento vadoso é convertido em um conteúdo representativo de água e drenado com um fechamento semelhante ao Darcy. Essa formulação deve ser tratada como **legado/substituto**, e não como o caminho teórico principal para o modelo atual.

---

## 5. Ascensão Capilar Opcional

Quando `flag_capillary_rise = 1`, HydroPol2D permite que águas subterrâneas rasas subam para o armazenamento vadoso disponível. A implementação atual é uma simples regra de ascensão capilar em camadas, e não uma solução completa da equação de Richards.
A troca ascendente aumenta com:
- profundidade mais rasa do lençol freático,
- maior déficit de armazenamento na camada receptora,
- e maior condutividade saturada nessa camada.

Conceitualmente, a transferência capilar ascendente para a camada $\ell$ é limitada por
$$
C_{\ell}
\le
\min\!\left(
S_{\ell,\mathrm{def}},\,
K_{\mathrm{sat},\ell} f_{\mathrm{prox}}(z_{\mathrm{wt}}) f_{\mathrm{dry}}(S_{\ell})
\right)
$$
onde:
- $S_{\ell,\mathrm{def}}$ é o déficit de armazenamento da camada restante
- $f_{\mathrm{prox}}$ é um fator monotônico de proximidade do lençol freático
- $f_{\mathrm{dry}}$ é um fator de secura monotônico

No código atual, a ascensão capilar é avaliada primeiro na zona de transmissão, depois na zona raiz e apenas na camada próxima à superfície quando não existe armazenamento vadoso inferior.
A troca líquida vadose-água subterrânea acumulada pelo programador é, portanto,
$$
R_{\mathrm{net}} = R_{\mathrm{down}} - C_{\mathrm{up}}
$$
onde $C_{\mathrm{up}}$ é o fluxo de ascensão capilar ascendente total.

---

## 6. Modelo bidimensional de fluxo de águas subterrâneas Boussinesq

Uma vez calculada a recarga, HydroPol2D direciona as águas subterrâneas lateralmente usando a função `Boussinesq_2D_explicit`.
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

HydroPol2D avalia esta equação numericamente calculando os fluxos nas interfaces das células e, em seguida, atualizando explicitamente a altura da água subterrânea.
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

Para evitar instabilidade numérica e esgotamento não físico do armazenamento de água subterrânea, HydroPol2D aplica um limitador de fluxo para que nenhuma célula possa perder mais água do que contém durante uma subetapa.
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
Esta é uma característica importante do solucionador de águas subterrâneas HydroPol2D porque garante a admissibilidade da massa local durante a integração explícita.
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

A troca vadose é acumulada a cada etapa da água superficial, mas as alturas saturadas das águas subterrâneas são atualizadas apenas quando o cronograma das águas subterrâneas é devido. O intervalo de atualização das águas subterrâneas é o mínimo de:
- o intervalo alvo do usuário,
- o limite explícito de estabilidade das águas subterrâneas,
- o intervalo implícito na mudança de carga acumulada máxima permitida,
- e o intervalo parcial final no final da corrida.

O agendador não pode ser desligado. Nem o HydroPol2D-Python nem o código MATLAB leem `flag_groundwater_async`, então o valor 0 não força uma atualização a cada passo da superfície. Um `groundwater_target_dt_min` menor deixa as atualizações mais frequentes.
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

Quando uma atualização das águas subterrâneas é acionada, o programador converte a profundidade líquida de troca acumulada em uma taxa média de recarga ao longo do intervalo decorrido das águas subterrâneas e passa-a para o solucionador saturado. O solucionador Boussinesq então avança nesse intervalo usando subetapas internas do preditor-corretor.
Essas subetapas internas são adicionalmente limitadas por uma condição baseada na velocidade da forma
$$
\Delta t_{\mathrm{inner}}
\le
\min\!\left(\frac{C_v \Delta x}{|u_x|},\,
\frac{C_v \Delta y}{|u_y|}
\right)
$$
onde:
- $u_x, u_y$ são velocidades das águas subterrâneas de Darcy
- $C_v$ é o fator de segurança interno baseado na velocidade

O resultado é uma estratégia de dois níveis:
1. um limite externo do programador baseado na estabilidade explícita das águas subterrâneas e na mudança de carga permitida,
2. um loop de subetapa preditor-corretor interno dentro do solucionador Boussinesq.

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

Os limites sem fluxo são impostos por condições de gradiente zero no perímetro do domínio. Na prática, HydroPol2D copia a cabeça do vizinho interior válido mais próximo para a célula do perímetro, aplicando assim uma condição discreta de Neumann.
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

A interface do solucionador atual inclui:
- uma máscara de rio,
- um termo de condutância do rio,
- estágio do rio,
- elevação do leito do rio,

que são projetados para apoiar a troca rio-aquífero. Na implementação atual, a variável de espaço reservado
$$
q_{\mathrm{river}}
$$
é inicializado e transportado pela interface de acoplamento como o termo de troca de rio. Isto significa que a interface está presente, mas a troca rio-aquífero deve atualmente ser descrita como um **espaço reservado/gancho estrutural**, e não uma reivindicação de teoria autônoma madura no mesmo nível que recarga, fluxo lateral de águas subterrâneas, ascensão capilar ou exfiltração.

---

## 11. Correção do excesso de saturação após elevação do lençol freático {#11-saturation-excess-correction-after-water-table-rise}

Após a atualização do Boussinesq, o HydroPol2D recalcula a profundidade do lençol freático e, portanto, o novo armazenamento máximo não saturado:
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
Na implementação padrão em camadas, a mesma correção é aplicada após recalcular a capacidade somada admissível da camada vadose. Esta é uma parte muito importante do HydroPol2D porque garante a **consistência de massa** entre as zonas vadosa e saturada quando o lençol freático sobe durante um intervalo de tempo.

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

Esta quantidade é armazenada como erro de diagnóstico de águas subterrâneas em HydroPol2D.
Quando a água subterrânea assíncrona está ativa, a recarga acumulada e a troca capilar pendentes não são tratadas como perda de modelo. Eles são armazenados como troca de água subterrânea em trânsito até que a próxima atualização saturada consuma o volume do escalonador. Esta distinção é importante para interpretar o diagnóstico do balanço hídrico de todo o modelo.

---

## 15. Resumo {#15-summary}

O modelo de águas subterrâneas HydroPol2D combina:
- um **módulo de recarga de zona vadose em camadas** baseado em um fechamento Darcy – van Genuchten – Mualem,
- **simples ascensão capilar** das águas subterrâneas rasas para o armazenamento vadoso disponível,
- um **programador assíncrono de águas subterrâneas** para atualizações mais lentas de carga saturada,
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