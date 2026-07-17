---
title: Visao geral
---

# HydroPol2D

HydroPol2D e um modelo hidrologico-hidrodinamico em grade raster para simular, de forma acoplada, agua superficial, armazenamento na zona vadosa, agua subterranea, qualidade da agua, neve e diagnosticos de risco.

Esta documentacao descreve o modelo como ele esta implementado hoje. Ela tambem distingue entre caminhos validados, caminhos diagnosticos e funcionalidades que permanecem pausadas ou experimentais.

## Escopo atual

O codigo atual inclui:

- interceptacao pelo dossel, evapotranspiracao, neve, infiltracao e armazenamento vadoso em camadas;
- recarga subterranea, ascensao capilar, atualizacoes assincronas da agua subterranea saturada e fluxo bidimensional de Boussinesq quando o baseflow esta ativo;
- roteamento superficial com as opcoes local inertial, full momentum, diffusive D4, kinematic D4 e cellular automata;
- transporte de qualidade da agua e exportacao no exutorio;
- diagnosticos opcionais de instabilidade humana.

## Como o HydroPol2D avanca uma simulacao

Em alto nivel, o HydroPol2D avanca o sistema acoplado nesta ordem:

1. aplica chuva, vazoes de entrada e forcantes meteorologicas;
2. atualiza interceptacao, neve, evapotranspiracao, infiltracao e armazenamento vadoso;
3. acumula recarga e troca capilar para a agua subterranea;
4. roteia a agua superficial com a familia de roteamento selecionada;
5. atualiza as cargas subterraneas quando o agendador de groundwater entra em acao;
6. devolve exfiltracao, excesso de saturacao, qualidade da agua e diagnosticos opcionais ao estado evolutivo.

Esse encadeamento e o que conecta os modulos hidrologicos, subterraneos, hidrodinamicos e diagnosticos em um unico modelo.

## Como ler a documentacao

Para a maioria dos usuarios, a ordem de leitura mais clara e:

1. [Visao geral da configuracao](../configuration/overview) para os controles publicos e flags.
2. [Visao matematica geral](../theory/overview) para as equacoes governantes e a estrutura conceitual.
3. [Visao geral da validacao](../validation/overview) para as evidencias de validacao de cada modulo.
4. [Exemplos](../Examples/RainfallRunoff) para fluxos de trabalho reprodutiveis.
