---
title: Visão geral
---

# HydroPol2D Case Builder

O HydroPol2D Case Builder prepara um caso de modelagem completo, pronto para rodar, a partir de
dados globais públicos. Você escolhe uma cidade ou uma bacia. O Builder delimita a área do modelo,
baixa e alinha os mapas, prepara a chuva e o clima e verifica o caso antes da simulação. Ele gera
casos para o HydroPol2D-MATLAB e para o HydroPol2D-Python, o motor do modelo dentro do HydroPol2D
Studio.

:::info[Licença]
O Case Builder é um produto proprietário. Para obter uma licença, escreva para Marcus N. Gomes Jr.
em [marcusnobrega.engcivil@gmail.com](mailto:marcusnobrega.engcivil@gmail.com). Esta página é uma
visão geral. O guia completo virá com a primeira versão licenciada.
:::

## O que ele prepara

| Etapa | O que o Builder faz |
|---|---|
| Área do modelo | Três formas de escolhê-la. **Urban Basin**: uma cidade e todas as bacias que drenam para ela. **Catchment**: um exutório e a bacia a montante. **Urban Area Only**: a área urbanizada e uma faixa ao redor. |
| Estimativa de custo | Antes de qualquer download grande, mostra a área, o número de células e a memória que o caso exige. |
| Terreno e rios | Terreno na resolução do modelo, condicionado para o escoamento com o HydroBathyDEM, com larguras e profundidades dos rios. |
| Mapas | Cobertura do solo, textura do solo, profundidade até a rocha, água subterrânea e umidade do solo iniciais e índice de área foliar. |
| Chuva e clima | Um produto de chuva por caso (IMERG, ERA5 ou MSWEP) e o clima do ERA5. |
| Contornos | Exutórios com escoamento crítico por padrão. Vazões de rios (GloFAS) e níveis costeiros (GTSM) onde se aplicam. |
| Verificação | Uma verificação prévia dos arquivos, grades, datas, unidades e entradas obrigatórias. |
| Simulação | Gera o caso para MATLAB, Python ou ambos e pode iniciar a simulação e mostrar o andamento. |

Um caso aprovado na verificação prévia está completo e consistente. Isso, sozinho, não mostra que
o modelo é preciso em um lugar novo. A calibração e a comparação com observações continuam
necessárias.

## Fontes de dados

| Variável | Fonte |
|---|---|
| Limite da cidade | GHSL Urban Centre Database R2024A |
| Bacias e rios | HydroBASINS v1c (nível 12) e HydroRIVERS v1.0 |
| Terreno | FABDEM v1.2, ou o seu próprio DEM |
| Geometria dos rios | HydroBathyDEM |
| Cobertura do solo | ESA WorldCover |
| Textura do solo | Classes de textura USDA do OpenLandMap |
| Profundidade até a rocha | Shangguan et al. (2017) |
| Água subterrânea inicial | Profundidade global do lençol freático de Fan et al. |
| Umidade inicial do solo | ERA5-Land |
| Clima | ERA5 |
| Índice de área foliar | MODIS MCD15A3H |
| Chuva | IMERG, ERA5 ou MSWEP, escolhido por caso |

Não é preciso ter conta no Google Earth Engine.

## Como ele se relaciona com o Studio e o MATLAB

- **No HydroPol2D Studio**, o assistente **New model** usa as etapas de preparação do Builder para
  criar um modelo a partir de um local no mapa. Veja [Construindo um modelo](../studio/building-a-model).
- **O Builder independente** traz todas as opções: os três tipos de área, a estimativa de custo, o
  relatório da verificação prévia e simulações em MATLAB ou Python.
- **Com o HydroPol2D-MATLAB**, o Builder gera um caso MATLAB com um script `run_case.m` que o
  executa. Veja o [fluxo de construção do modelo](../getting-started/model-building-workflow) para
  entender como o Builder, os modelos e a calibração trabalham juntos.

## Como usar

- um aplicativo local que abre no navegador, com as páginas **Prepare a case** e **Check a case**,
- uma linha de comando, para construções automatizadas e repetidas,
- uma interface em Python, para notebooks e servidores.

## Limites atuais

- Testado no macOS. O Linux é o sistema indicado para simulações grandes. O Windows ainda não foi testado.
- A chuva do MSWEP exige aprovação prévia da GloH2O.
- O albedo é um valor único (0,25) na versão atual.
- Redes de drenagem, reservatórios e calibração de eventos não são adicionados automaticamente.
