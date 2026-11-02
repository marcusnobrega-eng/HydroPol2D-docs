---
title: Visão geral
---
import useBaseUrl from '@docusaurus/useBaseUrl';

# HydroPol2D

HydroPol2D é um modelo hidrológico-hidrodinâmico em grade raster para simular, de forma acoplada, água superficial, armazenamento na zona vadosa, água subterrânea, qualidade da água, neve e diagnósticos de risco.

Esta documentação descreve o modelo como ele está implementado hoje. Ela também distingue entre caminhos validados, caminhos diagnósticos e funcionalidades que permanecem pausadas ou experimentais.

## Escopo atual

O código atual inclui:

- interceptação pelo dossel, evapotranspiração, neve, infiltração e armazenamento vadoso em camadas;
- recarga subterrânea, ascensão capilar, atualização do nível freático a cada passo e fluxo lateral bidimensional de Boussinesq em um cronograma assíncrono quando o baseflow está ativo;
- roteamento superficial com as opções local inertial, full momentum, diffusive D4, kinematic D4 e cellular automata;
- transporte de qualidade da água e exportação no exutório;
- diagnósticos opcionais de instabilidade humana.

<p align="center">
  <img src={useBaseUrl('/img/getting-started/questions-modules-outputs.pt.svg')} width="720" alt="Seis linhas, cada uma com uma pergunta, o módulo do HydroPol2D que a responde, com o seu estado padrão ou opcional e a sua evidência de validação, e a saída em mapa ou série temporal que a mostra, acima de uma legenda e de uma nota sobre o que o Results mostra" />
</p>

<p align="center">
  <em>Figura 1. Perguntas que o HydroPol2D responde, o módulo que responde a cada uma, com o seu estado, e a saída que a mostra. O estado segue as páginas de validação.</em>
</p>

## Como o HydroPol2D avança uma simulação

Em alto nível, o HydroPol2D avança o sistema acoplado nesta ordem:

1. aplica a chuva e as forçantes meteorológicas;
2. atualiza interceptação, neve, evapotranspiração, infiltração e armazenamento vadoso;
3. acumula recarga e troca capilar para a água subterrânea;
4. atualiza o lençol freático a cada passo, devolve a exfiltração e o excesso de saturação à superfície e roda o fluxo subterrâneo lateral quando o agendador da água subterrânea dispara;
5. adiciona os hidrogramas de entrada e roteia a água superficial com a família de roteamento selecionada;
6. atualiza a qualidade da água e os diagnósticos opcionais de risco.

Esse encadeamento é o que conecta os módulos hidrológicos, subterrâneos, hidrodinâmicos e diagnósticos em um único modelo.

<p align="center">
  <img src={useBaseUrl('/img/getting-started/time-step-order.pt.svg')} width="720" alt="Seis etapas de um passo de tempo da superfície em ciclo: forçantes; neve, dossel e solo; recarga e ascensão capilar; lençol freático; roteamento superficial; qualidade da água e risco. Ao lado, o relógio da superfície com o seu passo de Courant e o relógio da água subterrânea com os seus três gatilhos; abaixo, uma faixa com os passos da superfície e as atualizações do fluxo lateral ao longo de uma simulação" />
</p>

<p align="center">
  <em>Figura 2. A ordem de um passo de tempo da superfície, o relógio da superfície que define a sua duração e o relógio da água subterrânea que decide quando o fluxo lateral roda. A faixa de baixo mostra os dois relógios ao longo de uma simulação, fora de escala.</em>
</p>

## Interface desktop

O [HydroPol2D Studio](../studio/overview) é a interface desktop do HydroPol2D-Python: ele monta um
modelo a partir de um mapa ou dos seus próprios arquivos, configura o modelo passo a passo, executa
a simulação e mostra os resultados.

<p align="center">
  <img src={useBaseUrl('/img/getting-started/data-to-results.pt.svg')} width="720" alt="Mapas, tabelas de parâmetros, forçantes e configurações alimentam um caso, um arquivo de modelo do HydroPol2D Studio ou uma planilha do HydroPol2D-MATLAB; o caso roda no Studio ou no MATLAB, e as saídas são mapas, séries temporais, animações e um pacote de resultados" />
</p>

<p align="center">
  <em>Figura 3. Dos dados aos resultados. As mesmas entradas formam um caso, um arquivo de modelo do Studio ou uma planilha do MATLAB, e cada execução grava mapas, séries temporais e animações.</em>
</p>

## Como ler a documentação

Para a maioria dos usuários, a ordem de leitura mais clara é:

1. [Rodar pelo Excel](./excel-workflow) para os fluxos de planilha testados, com grade regular e malha de Voronoi.
2. [Visão geral da configuração](../configuration/overview) para os controles públicos e flags.
3. [Arquitetura do ecossistema](./ecosystem-architecture) para a geração de malha, os contratos compartilhados e o papel de cada repositório.
4. [Visão matemática geral](../theory/overview) para as equações governantes e a estrutura conceitual.
5. [Visão geral da validação](../validation/overview) para as evidências de validação de cada módulo.
6. [Exemplos](../Examples/RainfallRunoff) para fluxos de trabalho reprodutíveis.
