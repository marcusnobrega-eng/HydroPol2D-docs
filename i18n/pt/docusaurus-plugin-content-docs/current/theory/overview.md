---
title: Visao geral matematica
---

# Visao geral matematica

A secao de teoria e a referencia principal para as equacoes e a estrutura dos modulos do HydroPol2D. O objetivo e descrever as formulacoes implementadas sem misturar detalhes de configuracao ou narrativa de estudo de caso.

O HydroPol2D acopla:

- interceptacao, evapotranspiracao, infiltracao, neve e armazenamento vadoso;
- recarga subterranea em camadas, ascensao capilar e fluxo lateral de Boussinesq;
- multiplas familias de roteamento superficial;
- transporte de qualidade da agua;
- diagnosticos opcionais de instabilidade humana.

## Capacidades e maturidade

| Capacidade | Caminho teorico principal | Estado atual |
|---|---|---|
| Nucleo hidrologico: interceptacao, ET, infiltracao, neve, armazenamento vadoso em camadas | [Hydrologic Model](./hydrologic-model) | Padrao + validado |
| Recarga subterranea, agendador assincrono, ascensao capilar e fluxo lateral de Boussinesq | [Groundwater Model](./groundwater-model) | Padrao + validado |
| Subsuperfície em camadas de solo sobre regolito | [Subsuperfície em Camadas](./layered-subsurface) | Opcional + paridade dos kernels e testes controlados na bacia em V |
| Estresse de Feddes na absorção de água pelas raízes | [Modelo Hidrológico](./hydrologic-model#35-feddes-root-water-uptake-stress) | Opcional + testes de consistência |
| Aquífero profundo, com reservatórios lineares por sub-bacia e o seu estado inicial | [Modelo de Águas Subterrâneas](./groundwater-model#13-deep-aquifer) | Opcional + testes com fixtures do estado inicial |
| Roteamento local inertial | [Hydrodynamic Model](./hydrodynamic-model) | Padrao + validado |
| Roteamento full momentum | [Hydrodynamic Model](./hydrodynamic-model) | Opcional + validado em benchmarks controlados |
| Roteamentos diffusive e kinematic D4 | [Hydrodynamic Model](./hydrodynamic-model) | Opcionais + validados em benchmarks controlados |
| Cellular automata | [Hydrodynamic Model](./hydrodynamic-model) | Opcional + validado para conservacao e bookkeeping |
| Instabilidade humana, modos `1` e `3` | [Human Instability](./human-instability) | Opcional + validada em benchmarks controlados |
| Interface rio-aquifero | [Groundwater Model](./groundwater-model) | Interface presente, ainda sem uma reivindicacao teorica madura independente |

## Mapa da teoria

### 1. Processos hidrologicos

As paginas hidrologicas documentam como o HydroPol2D particiona a entrada atmosferica em armazenamento no dossel, throughfall, infiltracao, evapotranspiracao, acumulacao e derretimento de neve, armazenamento vadoso, recarga e feedback do groundwater.

### 2. Acoplamento do groundwater

A teoria do groundwater documenta o caminho atual de recarga em camadas, a ascensao capilar opcional, o agendador assincrono, a exfiltracao e o fluxo lateral bidimensional de Boussinesq quando o baseflow esta ativo. A [subsuperfície em camadas](./layered-subsurface), opcional, substitui o aquífero contido no solo por uma coluna de solo sobre regolito, e o aquífero profundo, também opcional, acrescenta reservatórios lineares lentos por sub-bacia.

### 3. Roteamento superficial

O HydroPol2D documenta hoje cinco familias principais de roteamento:

- local inertial;
- full momentum;
- diffusive D4;
- kinematic D4;
- cellular automata.

Apenas uma formulacao principal deve estar ativa por simulacao. O D8 permanece como caminho secundario.

### 4. Instabilidade humana

Instabilidade humana e um diagnostico de risco acoplado, dirigido pelas profundidades e velocidades produzidas pelo HydroPol2D. A teoria publica atual inclui o modo `1`, baseado em equilibrio de forcas, e o modo `3`, baseado em classificacao geometrica.

### 5. Qualidade da agua

A teoria de qualidade da agua documenta o buildup, o washoff, o transporte e a exportacao de constituintes dentro da mesma estrutura de roteamento distribuido usada para o movimento da agua.

## Acoplamento numerico

Em alto nivel, o HydroPol2D avanca o sistema acoplado:

1. aplicando chuva, inflow e forcantes meteorologicas;
2. atualizando interceptacao, neve, evapotranspiracao, infiltracao e armazenamento vadoso;
3. acumulando recarga e troca capilar para o groundwater;
4. atualizando a familia de roteamento ativa;
5. atualizando as cargas subterraneas quando o agendador assincrono entra em acao;
6. devolvendo exfiltracao, excesso de saturacao e diagnosticos opcionais ao estado acoplado.

Essa estrutura sequencial e o que conecta as paginas individuais de teoria em um unico modelo.
