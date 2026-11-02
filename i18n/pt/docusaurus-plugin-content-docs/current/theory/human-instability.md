---
title: Instabilidade Humana
---
import useBaseUrl from '@docusaurus/useBaseUrl';

# Instabilidade Humana

HydroPol2D inclui um módulo de instabilidade humana implementado que usa profundidade e velocidade da superfície roteada para estimar o risco de pedestres. A teoria pública atual deve distinguir claramente entre os modos implementados:
| Modo | Estado atual | Descrição |
|---|---|---|
| `1` | Implementado | Razão de risco de equilíbrio de força contínuo com base na flutuabilidade, atrito disponível e arrasto hidrodinâmico. |
| `2` | Não implementado | Apenas espaço reservado. Não documente ou use como opção pública ativa. |
| `3` | Implementado | Classificador de instabilidade baseado em geometria com limites de deslizamento, tombamento e afogamento/desenho. |

O status de validação atual para esses modos é rastreado no [estado da validação](../validation/validation-status).

---

## 1. Entradas e Acoplamento

O módulo de instabilidade humana lê o estado hidrodinâmico de HydroPol2D:
- profundidade da superfície roteada $h$,
- magnitude da velocidade roteada $v$,
- inclinação local quando o classificador baseado em geometria é usado,
- e parâmetros de geometria e resistência humanos fornecidos pelo usuário.

Isso significa que as estimativas de instabilidade são produtos de diagnóstico da simulação hidrológica-hidrodinâmica acoplada, em vez de um solucionador hidráulico independente.

<p align="center">
  <img src={useBaseUrl('/img/theory/human-instability.pt.svg')} width="720" alt="À esquerda, uma pessoa de pé na água sobre um declive, com a profundidade, a velocidade, a declividade e as forças de arrasto, empuxo, peso e atrito, seguidas das entradas do módulo e de onde cada modo roda. À direita, as equações do modo 1 com a escala de risco de 0 a 1, e as condições de deslizamento, tombamento e afogamento do modo 3, cada uma com um pictograma" />
</p>

<p align="center">
  <em>Figura 1. As forças sobre uma pessoa no escoamento e os dois modos implementados. O modo 1 dá um índice de risco de 0 a 1, e o modo 3 dá uma classe (estável, deslizamento, tombamento ou afogamento) só na grade regular.</em>
</p>

---

## 2. Modo 1: Razão de Risco de Equilíbrio de Forças

O modo `1` representa a instabilidade como uma competição entre o forçamento hidrodinâmico e o suporte de fricção que permanece após a flutuabilidade reduzir o peso corporal.
### 2.1 Peso e flutuabilidade

A força do peso corporal é
$$
F_{\mathrm{person}} = m_{\mathrm{person}} g
$$
A força de empuxo é aproximada como
$$
F_{\mathrm{buoy}}
=
w_1 w_2 h \rho_{\mathrm{w}} g
$$
onde:
- $m_{\mathrm{person}}$ é massa corporal
- $g$ é aceleração gravitacional
- $w_1$ e $w_2$ são larguras de corpo características
- $h$ é a profundidade da água
- $\rho_{\mathrm{w}}$ é a densidade da água

### 2.2 Fricção disponível

O atrito disponível para resistir ao movimento é
$$
F_{\mathrm{fric}}
=
\mu \max\!\left(
F_{\mathrm{person}} - F_{\mathrm{buoy}},
0
\right)
$$
onde $\mu$ é o coeficiente de atrito efetivo de contato com o solo.
### 2.3 Força hidrodinâmica

A carga hidrodinâmica é representada como
$$
F_{\mathrm{hyd}}
=
\max\!\left(
\frac{1}{2} C_d \rho_{\mathrm{w}} w_1 h v^2,
0
\right)
$$
onde:
- $C_d$ é coeficiente de arrasto
- $v$ é a magnitude da velocidade roteada

### 2.4 Razão de risco

A razão de risco do equilíbrio de forças é então
$$
R
=
\frac{F_{\mathrm{hyd}}}{F_{\mathrm{fric}}}
$$
para estados suportados onde $F_{\mathrm{fric}} > 0$. Na implementação atual:
- células sem suporte restante, mas com profundidade de água positiva, recebem risco total,
- o valor final do risco é reduzido ao intervalo $0 \le R \le 1$,
- e um mapa de risco máximo em execução pode ser acumulado durante a simulação.

O modo `1`, portanto, retorna um indicador de perigo contínuo em vez de um modo de falha categórico.

---

## 3. Modo 3: Classificador de Instabilidade Baseado em Geometria

O modo `3` usa a geometria da pessoa, a profundidade do fluxo, a velocidade do fluxo e a inclinação do solo para classificar o mecanismo de falha dominante.
### 3.1 Geometria submersa e forças

O código calcula a área submersa, o volume submerso e o centróide submerso em função da profundidade da água em relação às dimensões do corpo. Essas quantidades geométricas são então usadas para estimar:
- carregamento hidrodinâmico semelhante ao de arrasto e elevação,
- descida e componentes normais do peso corporal,
- flutuabilidade,
- e os braços de alavanca necessários para capotar.

Conceitualmente, os principais termos de força são:
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
onde:
- $A_{\mathrm{sub}}$ é a área projetada submersa
- $V_{\mathrm{sub}}$ é o volume submerso
- $\beta$ é o ângulo de inclinação local

### 3.2 Limiar deslizante

A resistência ao atrito disponível é aproximada como
$$
T = \mu \left(W_n - B_n - L\right)
$$
onde $L$ é a contribuição hidrodinâmica semelhante à sustentação. O deslizamento é classificado quando a força motriz excede o atrito disponível:
$$
\text{slide if } D + W_p > T
$$
No mapa de saída, o slide corresponde ao código `1`.
### 3.3 Limiar de tombamento

O módulo também calcula um momento de tombamento $M$ a partir do arrasto $D$, da sustentação $L$, do empuxo $B_n$ e da componente do peso ao longo da encosta $W_p$, cada um com um braço de alavanca definido pela geometria do corpo, pelo centroide submerso e pela declividade. O momento resistente $M_{\mathrm{res}}$ vem da componente normal do peso $W_n$. O tombamento é classificado quando o momento motriz excede o momento resistente:
$$
\text{topple if } M > M_{\mathrm{res}}
$$
No mapa de saída, topple corresponde ao código `2`.
### 3.4 Limiar de afogamento/desenho

A implementação também aplica um limite de afogamento/afundamento baseado em profundidade:
$$
\text{drowning/drawing if } h > \frac{13}{16} y
$$
onde $y$ é a altura característica do corpo usada pela rotina de geometria. No mapa de saída, este modo de falha corresponde ao código `3`.
### 3.5 Mapa categórico final

A classe de perigo do modo final-`3` é o máximo dos indicadores de deslizamento, tombamento e afogamento/empate:
$$
\text{risk class} = \max(\text{slide},\text{topple},\text{drowning/drawing})
$$
Isso produz um raster de instabilidade categórica em vez da proporção contínua retornada pelo modo `1`.

Uma célula seca ($h = 0$) é estável (código `0`), como no modo `1`: sem água, não há ninguém no escoamento para classificar. Sem essa regra, o próprio peso da pessoa faria de toda célula seca com declividade acima de $\arctan\mu$ (31° para $\mu = 0{,}6$) um deslizamento.

---

## 4. Escopo e Notas de Documentação

A atual história pública sobre a instabilidade humana deve permanecer alinhada com o código:
- o modo `1` é implementado e documentado como uma relação de equilíbrio de força,
- o modo `3` é implementado e documentado como um classificador baseado em geometria,
- o modo `2` não está implementado,
- as reivindicações de validação devem permanecer vinculadas às evidências controladas resumidas no [estado da validação](../validation/validation-status),
- e o módulo de instabilidade humana deve ser descrito como um diagnóstico de perigo acoplado conduzido pelas profundidades e velocidades do HydroPol2D.
