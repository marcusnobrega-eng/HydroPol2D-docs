---
title: Modelo de qualidade da água
---

# Modelo de qualidade da água

## 1. Visão geral

HydroPol2D simula o transporte de poluentes usando uma **formulação de acúmulo e lavagem** acoplada ao modelo hidrodinâmico.
O modelo rastreia:
- massa poluente armazenada na superfície,
- remoção de poluentes devido ao fluxo (lavagem),
- redistribuição entre células vizinhas,
- exportar através dos limites de saída.

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

O modelo de qualidade da água utiliza vazões hidrodinâmicas:
$$
q_{\mathrm{out}} = \{ q_{\mathrm{left}}, q_{\mathrm{right}}, q_{\mathrm{up}}, q_{\mathrm{down}}, q_{\mathrm{outlet}} \}
$$
com unidades:
$$
[\mathrm{L}\,\mathrm{T}^{-1}] \quad (\mathrm{mm/h})
$$
Estes são convertidos internamente em fluxo volumétrico:
$$
Q = \frac{q_{\mathrm{out}}}{1000 \cdot 3600} \cdot A_{\mathrm{cell}}
\quad [\mathrm{L}^3\,\mathrm{T}^{-1}]
$$
---

## 4. Formulação lavável

Duas formulações de lavagem são implementadas.

---

### 4.1 Modelo de lavagem da curva de classificação

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

Os fluxos de poluentes são calculados para cada direção:
- esquerda
- certo
- acima
- abaixo
- tomada

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

Para garantir a estabilidade e evitar massa negativa, HydroPol2D calcula um **passo de tempo mínimo admissível**:
$$
\Delta t_{\min}
=
\min \left(\frac{B_t}{|dW|}
\right)
$$
onde:
- apenas as células que perdem massa são consideradas,
- valores muito pequenos são excluídos.

Se:
$$
\Delta t_{\min} <\Delta t
$$
o modelo divide o passo de tempo em subetapas:
$$
\Delta t = \sum \Delta t_i
$$
e atualiza a massa poluente iterativamente:
$$
B_t^{i+1} = B_t^i - dW \cdot \Delta t_i
$$
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
\frac{W_{\mathrm{out,tot}}}{Q_{\mathrm{tot}} \cdot A_{\mathrm{cell}}}
\cdot 10^6
\quad [\mathrm{mg/L}]
$$
onde:
- $Q_{\mathrm{tot}}$ = vazão total de água $[\mathrm{L}\,\mathrm{T}^{-1}]$

---

## 10. Concentração de saída

A concentração de saída é calculada como:
$$
C_{\mathrm{out}} =
\frac{
\sum W_{\mathrm{out, outlet}}
}{
\sum Q_{\mathrm{outlet}} \cdot A_{\mathrm{cell}}
}
\cdot 1000
\quad [\mathrm{mg/L}]
$$
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
- limite mínimo de fluxo:

$$
q_{\mathrm{out}} \ge 10 \quad [\mathrm{mm/h}]
$$
para evitar instabilidade numérica.

---

## Resumo

O modelo de qualidade da água HydroPol2D:
- rastreia a massa poluente por célula,
- calcula a lavagem em função do fluxo e do armazenamento;
- redistribui poluentes em todo o domínio,
- garante estrita conservação de massa,
- usa passos de tempo adaptativos para manter a estabilidade.

Ele fornece uma estrutura robusta e flexível para simular o transporte de poluentes juntamente com processos hidrológicos e hidrodinâmicos. As evidências de validação atuais apoiam o comportamento controlado de balanço de massa de acúmulo/lavagem; a previsão de poluentes específicos do local ainda requer parâmetros, observações e calibração de poluentes locais.