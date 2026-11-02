---
title: Modelo de qualidade da água
---
import useBaseUrl from '@docusaurus/useBaseUrl';

# Modelo de qualidade da água

## 1. Visão geral

HydroPol2D simula o transporte de poluentes usando uma **formulação de acúmulo e lavagem** acoplada ao modelo hidrodinâmico.
O modelo rastreia:
- massa poluente armazenada na superfície,
- remoção de poluentes devido ao fluxo (lavagem),
- redistribuição entre células vizinhas,
- exportar através dos limites de saída.

<p align="center">
  <img src={useBaseUrl('/img/theory/water-quality.pt.svg')} width="720" alt="Três painéis. 1: a curva de acúmulo, que sobe em direção ao máximo C1 ao longo dos dias secos antecedentes e cai pela lavagem durante a chuva. 2: uma célula cuja massa de poluente sai com a água por cada face de saída. 3: uma grade de células sombreadas pela massa de poluente, com fluxos que levam a massa ao exutório, ao lado do balanço de massa e das equações de concentração" />
</p>

<p align="center">
  <em>Figura 1. As três etapas do modelo de qualidade da água baseado em massa. O acúmulo em tempo seco define a massa inicial, a lavagem a retira de cada célula pelas faces por onde a água sai, e o transporte a leva de célula em célula até o exutório.</em>
</p>

A variável governante é:
$$
B_t
$$
onde:
- $B_t$ = massa poluente por célula $[\mathrm{M}]$

O modelo é totalmente **conservador de massa** e acoplado dinamicamente ao roteamento de fluxo.
A validação atual concentra-se no modo de lavagem baseado em massa
(`flag_wq_model = 0`). A validação usa escalas de parâmetros de construção no estilo SWMM
para sólidos suspensos totais, mas a fonte da verdade é um balanço de massa analítico
solução em vez de uma execução numérica SWMM ou um polutógrafo de campo calibrado.

---

## 2. Armazenamento de poluentes

Cada célula armazena uma massa poluente:
$$
B_t \quad [\mathrm{kg}]
$$
A concentração de área correspondente é:
$$
b = \frac{B_t}{A_{\mathrm{cell}}}
\quad [\mathrm{M}\,\mathrm{L}^{-2}]
$$
onde:
- $A_{\mathrm{cell}}$ = área da célula $[\mathrm{L}^2]$

Os limites mínimo e máximo são definidos:
- $B_{\min}$ → massa mínima de poluente ativo
- $B_{\max}$ → limite de saturação

Abaixo de um limite:
$$
b <b_{\min}
\Rightarrow\text{no wash-off}
$$
---

## 3. Acoplamento hidrodinâmico

O modelo de qualidade da água usa a vazão $Q$ $[\mathrm{L}^3\,\mathrm{T}^{-1}]$, em $\mathrm{m^3/s}$, que sai de uma célula por cada face no passo de roteamento. O Python toma $Q$ diretamente das vazões nas faces calculadas pelo solver de roteamento.

O MATLAB guarda as vazões de saída de uma célula da grade como taxas de lâmina sobre a área da célula
$$
q_{\mathrm{out}} = \{ q_{\mathrm{left}}, q_{\mathrm{right}}, q_{\mathrm{up}}, q_{\mathrm{down}}, q_{\mathrm{outlet}} \}
$$
com unidades
$$
[\mathrm{L}\,\mathrm{T}^{-1}] \quad (\mathrm{mm/h})
$$
e converte cada uma em vazão antes de calcular a lavagem
$$
Q = \frac{q_{\mathrm{out}}}{1000 \cdot 3600} \cdot A_{\mathrm{cell}}
\quad [\mathrm{L}^3\,\mathrm{T}^{-1}]
$$
---

## 4. Formulação lavável

Duas formulações de lavagem são implementadas.

---

### 4.1 Modelo de lavagem da curva de classificação

Este modo existe apenas no MATLAB, e apenas na grade regular, pois uma simulação do MATLAB em malha o recusa. O Python tem apenas o modo baseado em massa da seção 4.2.

Quando `flag_wq_model = 1`, a lavagem é:
$$
W_{\mathrm{out}} =
C_3 \, Q^{C_4} \, f(B_t)
$$
onde:
- $W_{\mathrm{out}}$ = fluxo de massa poluente $[\mathrm{M}\,\mathrm{T}^{-1}]$
- $C_3, C_4$ = coeficientes empíricos
- $Q$ = taxa de fluxo $[\mathrm{L}^3\,\mathrm{T}^{-1}]$

O fator de correção de armazenamento é:
$$
f(B_t) = 1 + \max(B_t - B_r, 0)
$$
onde:
- $B_r$ = limite de massa poluente residual $[\mathrm{M}]$

Esta formulação garante que:
- a lavagem aumenta com o fluxo,
- a lavagem aumenta com a massa poluente disponível.

---

### 4.2 Modelo de lavagem baseado em massa

Quando `flag_wq_model = 0`, a formulação torna-se:
$$
W_{\mathrm{out}} =
C_3 \, Q^{C_4} \, B_t
$$
Esta formulação assume:
- a lavagem é proporcional à massa poluente disponível,
- o transporte aumenta com a magnitude do fluxo.

---

## 5. Fluxos direcionais de poluentes

Os fluxos de poluentes são calculados para cada direção pela qual a água sai da célula. Na grade regular, as direções são
- esquerda
- direita
- acima
- abaixo
- exutório

O MATLAB trata o exutório como uma quinta direção das células de exutório. O Python leva a vazão do exutório pelas faces na borda da grade, de modo que ali o fluxo no exutório é o fluxo por uma face de contorno. Em uma malha de Voronoi ou quadtree, os dois códigos usam cada aresta pela qual a água sai da célula, e uma aresta no contorno do domínio exporta o poluente para fora do modelo.

A saída total de poluentes de uma célula é:
$$
W_{\mathrm{out,tot}} = \sum_k W_{\mathrm{out},k}
$$
Os fluxos de poluentes recebidos são calculados a partir de células vizinhas:
$$
W_{\mathrm{in}} = \sum_k W_{\mathrm{in},k}
$$
---

## 6. Balanço líquido de poluentes

A taxa líquida de poluição é:
$$
dW = W_{\mathrm{out,tot}} - W_{\mathrm{in}}
\quad [\mathrm{M}\,\mathrm{T}^{-1}]
$$
A equação do balanço de massa é:
$$
B_t^{t+\Delta t}
=
B_t^t - dW \cdot \Delta t
$$
Esta formulação é responsável por:
- remoção de poluentes devido à lavagem,
- redistribuição de poluentes pela rede.

---

## 7. Time stepping adaptativo (recurso crítico)

Para garantir a estabilidade e evitar massa negativa, HydroPol2D divide o passo de tempo hidráulico em $n$ **subpassos** iguais:
$$
n = \max\!\left(1,\;\left\lceil \Delta t \,\max\!\left(\frac{W_{\mathrm{out,tot}}}{B_t}\right) \right\rceil\right)
\qquad
\Delta t_i = \frac{\Delta t}{n}
$$
onde:
- o máximo é tomado sobre as células que contêm poluente ($B_t > 0$),
- $W_{\mathrm{out,tot}}/B_t$ é a taxa bruta de saída de uma célula no início do passo, sem o fluxo de entrada $[\mathrm{T}^{-1}]$,
- $\lceil\cdot\rceil$ arredonda para o inteiro seguinte.

Em cada subpasso a lavagem é calculada de novo a partir da massa atual. Uma célula cuja saída removeria mais do que ela contém tem suas saídas reduzidas na proporção necessária para que $W_{\mathrm{out,tot}}\,\Delta t_i \le B_t$. A massa é então atualizada:
$$
B_t^{i+1} = B_t^i - dW \cdot \Delta t_i
$$
O Python e o MATLAB usam esse mesmo esquema. Os subpassos ocorrem dentro do passo hidráulico, de modo que o modelo de qualidade da água não encurta o passo de tempo do modelo.
Isso garante:
- nenhuma massa poluente negativa,
- estabilidade numérica,
- conservação de massa precisa.

---

## 8. Conservação e correções de massa

Após a atualização:
- valores negativos são removidos:

$$
B_t = \max(B_t, 0)
$$
- o arredondamento é aplicado para evitar ruído numérico.

A massa perdida devido a correções numéricas é rastreada:
$$
\mathrm{mass}_{\mathrm{lost}}
$$
---

## 9. Concentração de poluentes

A concentração de poluentes é calculada como:
$$
C =
1000 \cdot \frac{W_{\mathrm{out,tot}}}{Q_{\mathrm{tot}}}
\quad [\mathrm{mg/L}]
$$
onde:
- $W_{\mathrm{out,tot}}$ = saída total de poluente da célula $[\mathrm{kg\,s^{-1}}]$
- $Q_{\mathrm{tot}}$ = vazão total de água que sai da célula $[\mathrm{m^3\,s^{-1}}]$
- o fator 1000 converte $\mathrm{kg\,m^{-3}}$ em $\mathrm{mg/L}$

O Python calcula $C$ dessa forma e define $C = 0$ em uma célula da qual não sai água. Na grade regular, o MATLAB calcula a mesma razão a partir das taxas de lâmina da seção 3, como $C = 10^6\, W_{\mathrm{out,tot}} / (q_{\mathrm{out,tot}}\, A_{\mathrm{cell}})$, com $W_{\mathrm{out,tot}}$ em kg/h, a taxa total de saída $q_{\mathrm{out,tot}}$ em mm/h e $A_{\mathrm{cell}}$ em m². Ele usa no mínimo 10 mm/h para $q_{\mathrm{out,tot}}$ (seção 12).

---

## 10. Concentração de saída

A concentração de saída é calculada como:
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
onde as somas percorrem as faces pelas quais a água sai do domínio, $W_{\mathrm{out,outlet}}$ é o fluxo de poluente por uma dessas faces, em média no passo de tempo $[\mathrm{kg\,s^{-1}}]$, e $Q_{\mathrm{outlet}}$ é a vazão de água por ela $[\mathrm{m^3\,s^{-1}}]$. Na grade regular, o MATLAB calcula a mesma razão como a massa de poluente que chega ao exutório no passo de tempo, em kg, dividida pelo volume de água do exutório no passo, em litros, vezes $10^6$.
---

## 11. Massa lavada total

A massa cumulativa de poluentes lavados é:
$$
M_{\mathrm{washed}} =
\sum W_{\mathrm{out,tot}} \cdot \Delta t
\quad [\mathrm{kg}]
$$
---

## 12. Restrições numéricas

O modelo impõe:
- limiar mínimo de poluição:

$$
b < b_{\min} \Rightarrow W_{\mathrm{out}} = 0
$$
- uma vazão mínima para a concentração na célula, só no MATLAB e só na grade regular:

$$
q_{\mathrm{out,tot}} \ge 10 \quad [\mathrm{mm/h}]
$$
O MATLAB aplica esse piso apenas à taxa total de saída no denominador da concentração na célula da seção 9, para que uma célula com saída muito pequena não mostre uma concentração muito alta. Ele não altera a lavagem, o balanço de massa nem a concentração no exutório. O Python não tem esse piso, e suas células das quais não sai água têm $C = 0$.

---

## Resumo

O modelo de qualidade da água HydroPol2D:
- rastreia a massa poluente por célula,
- calcula a lavagem em função do fluxo e do armazenamento;
- redistribui poluentes em todo o domínio,
- garante estrita conservação de massa,
- usa passos de tempo adaptativos para manter a estabilidade.

Ele fornece uma estrutura robusta e flexível para simular o transporte de poluentes juntamente com processos hidrológicos e hidrodinâmicos. As evidências de validação atuais apoiam o comportamento controlado de balanço de massa de acúmulo/lavagem; a previsão de poluentes específicos do local ainda requer parâmetros, observações e calibração de poluentes locais.