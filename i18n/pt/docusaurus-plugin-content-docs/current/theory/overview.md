---
title: Visão geral matemática
---
import useBaseUrl from '@docusaurus/useBaseUrl';

# Visão geral matemática

A seção de teoria é a referência principal para as equações e a estrutura dos módulos do HydroPol2D. O objetivo é descrever as formulações implementadas sem misturar detalhes de configuração ou narrativa de estudo de caso.

O HydroPol2D acopla:

- interceptação, evapotranspiração, infiltração, neve e armazenamento vadoso;
- recarga subterrânea em camadas, ascensão capilar e fluxo lateral de Boussinesq;
- múltiplas famílias de roteamento superficial;
- transporte de qualidade da água;
- diagnósticos opcionais de instabilidade humana.

## Capacidades e maturidade

| Capacidade | Caminho teórico principal | Estado atual |
|---|---|---|
| Núcleo hidrológico: interceptação, ET, infiltração, armazenamento vadoso em camadas | [Hydrologic Model](./hydrologic-model) | Padrão + validado |
| Acúmulo, derretimento e sublimação de neve | [Hydrologic Model](./hydrologic-model#5-snow-accumulation-melt-and-sublimation) | Opcional (desligado até ser ativado) + validado |
| Recarga subterrânea, agendador assíncrono, ascensão capilar e fluxo lateral de Boussinesq | [Groundwater Model](./groundwater-model) | Padrão + validado |
| Subsuperfície em camadas de solo sobre regolito | [Subsuperfície em Camadas](./layered-subsurface) | Opcional + paridade dos kernels e testes controlados na bacia em V |
| Estresse de Feddes na absorção de água pelas raízes | [Modelo Hidrológico](./hydrologic-model#35-feddes-root-water-uptake-stress) | Opcional + testes de consistência |
| Aquífero profundo, com reservatórios lineares por sub-bacia e o seu estado inicial | [Modelo de Águas Subterrâneas](./groundwater-model#13-deep-aquifer) | Opcional + testes com fixtures do estado inicial |
| Roteamento local inertial | [Hydrodynamic Model](./hydrodynamic-model) | Padrão + validado |
| Roteamento full momentum | [Hydrodynamic Model](./hydrodynamic-model) | Opcional + validado em benchmarks controlados |
| Roteamentos diffusive e kinematic D4 | [Hydrodynamic Model](./hydrodynamic-model) | Opcionais + validados em benchmarks controlados |
| Cellular automata | [Hydrodynamic Model](./hydrodynamic-model) | Opcional + validado para conservação e bookkeeping |
| Instabilidade humana, modos `1` e `3` | [Human Instability](./human-instability) | Opcional + validada em benchmarks controlados |
| Troca rio-aquífero | [Modelo de Águas Subterrâneas](./groundwater-model) | Implementada no Python e no MATLAB + testes controlados de águas subterrâneas |

## Mapa da teoria

### 1. Processos hidrológicos

As páginas hidrológicas documentam como o HydroPol2D particiona a entrada atmosférica em armazenamento no dossel, throughfall, infiltração, evapotranspiração, acumulação e derretimento de neve, armazenamento vadoso, recarga e feedback do groundwater.

<p align="center">
  <img src={useBaseUrl('/img/theory/cell-water-budget.pt.svg')} width="720" alt="Uma célula do modelo vista de lado: a chuva cai sobre o dossel de uma árvore e a neve sobre um manto de neve; o throughfall, o degelo, a exfiltração e o excesso de saturação alimentam a água superficial, que infiltra na zona vadosa e escoa para uma célula vizinha mais baixa; a recarga e a ascensão capilar ligam a zona vadosa à água subterrânea, que flui lateralmente; setas cinza devolvem vapor à atmosfera" />
</p>

<p align="center">
  <em>Figura 1. Os reservatórios e fluxos de uma célula do modelo (fora de escala). As setas azuis levam água líquida e as cinza, vapor; só a chuva passa pelo dossel, e o degelo vai direto para a água superficial.</em>
</p>

### 2. Acoplamento do groundwater

A teoria do groundwater documenta o caminho atual de recarga em camadas, a ascensão capilar opcional, o agendador assíncrono, a exfiltração e o fluxo lateral bidimensional de Boussinesq quando o baseflow está ativo. A [subsuperfície em camadas](./layered-subsurface), opcional, substitui o aquífero contido no solo por uma coluna de solo sobre regolito, e o aquífero profundo, também opcional, acrescenta reservatórios lineares lentos por sub-bacia.

### 3. Roteamento superficial

O HydroPol2D documenta hoje cinco famílias principais de roteamento:

- local inertial;
- full momentum;
- diffusive D4;
- kinematic D4;
- cellular automata.

Apenas uma formulação principal deve estar ativa por simulação. O D8 permanece como caminho secundário.

### 4. Instabilidade humana

Instabilidade humana é um diagnóstico de risco acoplado, dirigido pelas profundidades e velocidades produzidas pelo HydroPol2D. A teoria pública atual inclui o modo `1`, baseado em equilíbrio de forças, e o modo `3`, baseado em classificação geométrica.

### 5. Qualidade da água

A teoria de qualidade da água documenta o buildup, o washoff, o transporte e a exportação de constituintes dentro da mesma estrutura de roteamento distribuído usada para o movimento da água.

## Acoplamento numérico

Em alto nível, o HydroPol2D avança o sistema acoplado:

1. aplicando a chuva e as forçantes meteorológicas;
2. atualizando interceptação, neve, evapotranspiração, infiltração e armazenamento vadoso;
3. acumulando recarga e troca capilar para o groundwater;
4. alterando as cargas do lençol freático a cada passo da água superficial pela troca líquida e devolvendo a exfiltração e o excesso de saturação à superfície; o agendador da água subterrânea é sempre assíncrono, e só o fluxo lateral da água subterrânea, quando está ativo, espera por ele;
5. aplicando os hidrogramas de entrada e atualizando a família de roteamento ativa;
6. atualizando a qualidade da água e os diagnósticos opcionais.

Essa estrutura sequencial é o que conecta as páginas individuais de teoria em um único modelo.
