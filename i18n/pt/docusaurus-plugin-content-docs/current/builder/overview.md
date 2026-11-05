---
title: Visão geral
---
import useBaseUrl from '@docusaurus/useBaseUrl';

# HydroPol2D Case Builder

O HydroPol2D Case Builder prepara um caso de modelagem completo, pronto para rodar, a partir de
dados globais públicos. Você escolhe uma cidade ou uma bacia. O Builder delimita a área do modelo,
baixa e alinha os mapas, prepara a chuva e o clima e verifica o caso antes da simulação. Ele gera
casos para o HydroPol2D-MATLAB e para o HydroPol2D-Python, o motor do modelo dentro do HydroPol2D
Studio.

Esta seção descreve o Case Builder 0.1.0, a primeira versão licenciada (uma versão de teste), para
Macs com Apple silicon e para Windows (64 bits). A interface do Case Builder está em inglês, então
os nomes de abas, botões, campos e mensagens aparecem aqui em inglês, como na tela.

:::info[Licença]
O Case Builder é um produto proprietário. Para obter uma licença, escreva para Marcus N. Gomes Jr.
em [marcusnobrega.engcivil@gmail.com](mailto:marcusnobrega.engcivil@gmail.com).
A página [Instalação e licença](install-and-license) explica os passos.
:::

<p align="center">
  <img src={useBaseUrl('/img/builder/case-builder-workflow.pt.svg')} width="760" alt="O Case Builder do primeiro uso a um caso pronto para rodar: o código de licença, os dados públicos que ele baixa, as quatro etapas Escolha a área, Prévia, Prepare e Verifique, a pasta do caso e onde o caso roda" />
</p>

<p align="center">
  <em>Figura 1. O caminho pelo Case Builder. Os dados públicos alimentam a prévia e o caso completo. A pasta do caso roda no HydroPol2D MATLAB ou no HydroPol2D Studio.</em>
</p>

## O que ele prepara

| Etapa | O que o Builder faz |
|---|---|
| Área do modelo | Três formas de escolhê-la. **Urban Basin**: uma cidade e todas as bacias que drenam para ela. **Catchment**: um exutório e a bacia a montante dele. **Urban Area Only**: a área urbanizada e uma faixa ao redor dela. |
| Prévia do custo | Antes de qualquer download grande, mostra a área, o número de células da grade, os dados a baixar e o tamanho dos resultados salvos. |
| Terreno e rios | Terreno na resolução do modelo, condicionado para o escoamento com o HydroBathyDEM, com larguras e profundidades dos rios. |
| Mapas | Cobertura do solo, textura do solo, profundidade até a rocha, água subterrânea e umidade do solo iniciais e índice de área foliar. |
| Chuva e clima | Um produto de chuva por caso (IMERG, ERA5, MSWEP ou AORC) e o clima do ERA5. |
| Contornos | Exutórios com escoamento crítico por padrão. Vazões de entrada dos rios (GloFAS) e níveis costeiros (GTSM) onde se aplicam. |
| Verificação | Uma verificação prévia dos arquivos, grades, datas, unidades e entradas obrigatórias. |
| Simulação | Gera o caso para MATLAB, Python ou ambos, e pode iniciar a simulação e mostrar o andamento. |

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
| Chuva | IMERG, ERA5, MSWEP ou AORC (Estados Unidos), escolhido por caso |

Não é preciso ter conta no Google Earth Engine. Algumas fontes exigem uma conta gratuita em seu
nome. A página [Fontes de dados e contas](data-accounts) lista essas fontes.

## Como ele se relaciona com o Studio e o MATLAB

- **No HydroPol2D Studio**, o assistente **New model** usa as etapas de preparação do Builder para
  criar um modelo a partir de um local no mapa. Veja [Montando um modelo](../studio/building-a-model).
  Se você tem o Studio, não precisa também do Builder.
- **O Builder independente** acrescenta o conjunto completo de opções: os três tipos de área do
  modelo, a prévia do custo, o relatório da verificação prévia e as simulações em MATLAB.
- **Com o HydroPol2D-MATLAB**, o Builder gera um caso MATLAB com um script `run_case.m` que o
  executa. Veja o [fluxo de construção do modelo](../getting-started/model-building-workflow) para
  entender como o Builder, os modelos e a calibração trabalham juntos.

## Como usar

- um app local que abre no seu navegador, com as páginas **Prepare a case**, **Check a case** e
  **Python and command line**,
- uma linha de comando, para montagens por script e repetidas.

## Nesta seção

1. [Instalação e licença](install-and-license): baixar, instalar e digitar o código de licença.
2. [Escolher a área do modelo](model-area): Urban Basin, Urban Area Only e Catchment.
3. [Configurações do caso](settings): grade, datas, chuva, processos, rios, saídas e pastas.
4. [Prévia e custo](preview-and-cost): o mapa do domínio e o tamanho do caso antes de qualquer download.
5. [Preparar um caso](prepare-a-case): a montagem completa e o que fica na pasta do caso.
6. [Fontes de dados e contas](data-accounts): Copernicus, NASA Earthdata e MSWEP.
7. [Verificar um caso](check-a-case): a verificação prévia.
8. [Rodar o caso](run-the-case): no HydroPol2D MATLAB ou no HydroPol2D Studio.
9. [Linha de comando](command-line): os mesmos casos a partir de um terminal.
10. [Solução de problemas](troubleshooting): mensagens que podem aparecer e o que fazer.

## Limites atuais

- A versão 0.1.0 é uma versão de teste para Macs com Apple silicon e Windows (64 bits).
- O app não baixa o HydroPol2D Python. Rode os casos Python no HydroPol2D Studio.
- A chuva do MSWEP exige aprovação prévia da GloH2O.
- A chuva do AORC cobre só os Estados Unidos contíguos. Os níveis costeiros do GTSM terminam em 2024.
- O albedo é um valor único (0,25) na versão atual.
- Redes de drenagem, reservatórios e calibração de eventos não são adicionados automaticamente.
