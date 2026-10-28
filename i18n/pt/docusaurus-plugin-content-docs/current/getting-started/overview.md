---
title: Visão geral
---

# HydroPol2D

HydroPol2D é um modelo hidrológico-hidrodinâmico em grade raster para simular, de forma acoplada, água superficial, armazenamento na zona vadosa, água subterrânea, qualidade da água, neve e diagnósticos de risco.

Esta documentação descreve o modelo como ele está implementado hoje. Ela também distingue entre caminhos validados, caminhos diagnósticos e funcionalidades que permanecem pausadas ou experimentais.

## Escopo atual

O código atual inclui:

- interceptação pelo dossel, evapotranspiração, neve, infiltração e armazenamento vadoso em camadas;
- recarga subterrânea, ascensão capilar, atualizações assíncronas da água subterrânea saturada e fluxo bidimensional de Boussinesq quando o baseflow está ativo;
- roteamento superficial com as opções local inertial, full momentum, diffusive D4, kinematic D4 e cellular automata;
- transporte de qualidade da água e exportação no exutório;
- diagnósticos opcionais de instabilidade humana.

## Como o HydroPol2D avança uma simulação

Em alto nível, o HydroPol2D avança o sistema acoplado nesta ordem:

1. aplica chuva, vazões de entrada e forçantes meteorológicas;
2. atualiza interceptação, neve, evapotranspiração, infiltração e armazenamento vadoso;
3. acumula recarga e troca capilar para a água subterrânea;
4. roteia a água superficial com a família de roteamento selecionada;
5. atualiza as cargas subterrâneas quando o agendador de groundwater entra em ação;
6. devolve exfiltração, excesso de saturação, qualidade da água e diagnósticos opcionais ao estado evolutivo.

Esse encadeamento é o que conecta os módulos hidrológicos, subterrâneos, hidrodinâmicos e diagnósticos em um único modelo.

## Interface desktop

O [HydroPol2D Studio](../studio/overview) é a interface desktop do HydroPol2D-Python: ele monta um
modelo a partir de um mapa ou dos seus próprios arquivos, configura o modelo passo a passo, executa
a simulação e mostra os resultados.

## Como ler a documentação

Para a maioria dos usuários, a ordem de leitura mais clara é:

1. [Rodar pelo Excel](./excel-workflow) para os fluxos de planilha testados, com grade regular e malha de Voronoi.
2. [Visão geral da configuração](../configuration/overview) para os controles públicos e flags.
3. [Arquitetura do ecossistema](./ecosystem-architecture) para a geração de malha, os contratos compartilhados e o papel de cada repositório.
4. [Visão matemática geral](../theory/overview) para as equações governantes e a estrutura conceitual.
5. [Visão geral da validação](../validation/overview) para as evidências de validação de cada módulo.
6. [Exemplos](../Examples/RainfallRunoff) para fluxos de trabalho reprodutíveis.
