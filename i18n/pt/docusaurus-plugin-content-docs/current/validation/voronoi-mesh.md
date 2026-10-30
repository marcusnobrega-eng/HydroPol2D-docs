---
title: Validação da malha Voronoi
---
import useBaseUrl from '@docusaurus/useBaseUrl';

# Validação da malha Voronoi

Os produtos Voronoi são gerados pelo HydroBathyDEM e consumidos por meio do
contrato de malha compartilhado descrito em [Arquitetura do ecossistema](../getting-started/ecosystem-architecture).
O HydroPolMesh é um protótipo de migração, e não uma dependência de execução.

O caminho de volumes finitos em malha Voronoi é um modo de malha separado do fluxo
de produção raster D4. Ele usa as áreas exatas dos polígonos e a topologia das arestas,
e pode combinar o escoamento 2D resolvido com um grafo de canais subgrade no estilo de
Neal para rios mais estreitos que a malha.

<p align="center">
  <img src={useBaseUrl('/img/validation/grid-voronoi-subgrid.pt.svg')} width="720" alt="Dois painéis comparam a grade regular D4 e a malha Voronoi: células e ligações, métodos de roteamento e módulos opcionais; abaixo, as opções de subgrade de cada uma, com o roteamento que cada opção exige" />
</p>

<p align="center">
  <em>Figura 1. A grade regular e a malha Voronoi, que também roda quadtrees. Na malha, os módulos opcionais rodam no motor de CPU (NumPy), sem a classificação do modo 3.</em>
</p>

## Escopo suportado atualmente {#current-supported-scope}

| Modo de roteamento | Polígonos 2D resolvidos | Grafo de canais de Neal | Estado da execução |
|---|---|---|---|
| Inercial local | sim | sim | Validação em CPU aprovada |
| Cinemático | sim | não | Validação preliminar (smoke) em CPU aprovada |
| Difusivo explícito | sim | não | Validação preliminar (smoke) em CPU aprovada |
| Momento completo | sim | não | Validação por benchmark em CPU aprovada |

A execução em GPU está bloqueada de propósito. As malhas na escala da Índia também ainda
não foram validadas. Nenhuma das duas coisas deve ser inferida a partir dos resultados
controlados em CPU.

As opções públicas de subgrade distinguem o canal de Neal na grade estruturada, as
tabelas de consulta estruturadas e as relações subgrade Voronoi. Ativar uma delas não
ativa silenciosamente nenhuma das outras.

## O que é verificado {#what-is-checked}

Os testes da malha e do solver cobrem a validade da geometria, a conservação, o lago em
repouso, o molhamento e a secagem, a contabilidade das forçantes e das águas subterrâneas,
as transições entre o escoamento resolvido e o subgrade e as comparações com referências
em resolução fina. O passo de tempo é limitado pela soma das capacidades de sinal sobre
todas as faces incidentes. Em um grafo de Neal, ele também usa o limite de percurso de cada
trecho de canal e de cada transição, e o limite de armazenamento em cada nó de canal.

O teste autônomo de CFL dos canais usa dois trechos de 100 m que se encontram em um nó e
uma transição entre o escoamento resolvido e o subgrade. O seu primeiro passo adaptativo é
de 7,821 s, contra um limite de onda de 15,641 s para um único trecho, e a massa fecha
exatamente. Isso confirma que o limitador do grafo considera todos os caminhos incidentes.

## Módulos opcionais {#optional-modules}

No motor de CPU, o HydroPol2D-Python roda os módulos opcionais da grade regular nas células
da malha, cada um com as próprias equações da grade. Os testes rodam cada módulo na grade e
em uma malha formada pelas próprias células quadradas da grade, e comparam:

| Módulo | O que é comparado na malha quadrada |
|---|---|
| Instabilidade humana | Índice final e máximo, mapas do índice; a velocidade na célula da malha contra a da grade em campos aleatórios |
| Neve | Mapas de SWE, profundidade e infiltração, com o esquema de solo padrão e o em camadas |
| Reservatórios | Vazão liberada, armazenamento e todas as séries dos contornos internos |
| Drenagem urbana | Cargas e armazenamento nos nós, vazão nos condutos e nas bocas de lobo, volume nos exutórios da rede, número de subpassos |
| Qualidade da água | Massa, exportação e concentração do poluente; a lavagem pelas arestas contra a da grade em campos aleatórios |
| Infraestrutura verde | Armazenamento, captação, extravasamento, exfiltração e dreno de fundo por unidade, os três mapas de infraestrutura verde, com o esquema de solo padrão e o em camadas |
| Bacias de detenção | Nível, armazenamento, vazão lateral de entrada e vazões dos dispositivos, com e sem águas subterrâneas, com o esquema de solo padrão e o em camadas |

Cada par concorda até 1e-10 ou melhor, e toda simulação na malha fecha o seu balanço hídrico
até 1e-9 m³. As comparações usam escoamento suave, em que os dois solvers de superfície concordam
até o arredondamento; [Limitações](./limitations#voronoi-mesh-mode) lista o que ainda está em aberto.

## Interpretação {#interpretation}

Esses resultados estabelecem que os caminhos numéricos testados se comportam de forma
conservativa nos seus casos controlados. Eles não validam previsões de inundação em escala
de campo, escolhas de geração de malha para uma bacia específica, a execução em GPU nem o
desempenho de produção na Índia. Isso exige QA dedicado da malha, benchmarks de tempo de
execução e comparação com observações ou com uma referência defensável.

O registro executável do lado do modelo é mantido no repositório em
`Validation/Voronoi/README.md` e `Validation/Voronoi/VALIDATION_RESULTS.md`.
