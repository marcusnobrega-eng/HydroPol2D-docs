---
title: Calibração no Studio
---
import useBaseUrl from '@docusaurus/useBaseUrl';

# Calibração no Studio

A área de trabalho **Calibrate** ajusta os parâmetros do modelo à vazão, às profundidades da água, aos níveis da água e às profundidades do lençol freático observados, com um algoritmo genético. É a quarta área de trabalho na barra à esquerda (Cmd+4 no Mac, Ctrl+4 no Windows). O método, as pontuações e as configurações estão explicados em [Calibração com Observações](../calibration/ga-calibration).

A página tem seis seções, na ordem em que são usadas.

## 1. Observed data {#1-observed-data}

Escolha uma tabela e cole linhas do Excel ou de um arquivo de texto (**Paste rows**), ou digite as linhas.

| Coluna | Conteúdo |
|---|---|
| Gauge | O nome da série; as linhas com o mesmo nome formam uma série |
| Easting, Northing | Coordenadas opcionais, no sistema de coordenadas do modelo |
| Time | Minutos a partir do início da simulação |
| Value | O valor observado, nas unidades da tabela |
| Observation uncertainty | Opcional: o erro de medição do valor, como um desvio padrão, nas mesmas unidades |

Há tabelas de vazão, profundidade da água, nível da água, profundidade do lençol freático e umidade do solo superficial. A umidade do solo ainda não pode ser calibrada. **How to fill this table** lista as colunas da tabela selecionada. As linhas entram no modelo assim que são coladas, e o **Save** as grava no arquivo do modelo.

## 2. Observations to match {#2-observations-to-match}

Cada linha é uma série observada. Marque **Use** nas séries a ajustar.

- **Compare with**: um posto de roteamento, um ponto de observação, o exutório do modelo (só vazão) ou a célula nas coordenadas da série. Os postos e os pontos de observação são desenhados em Setup > Study area.
- **Score**: KGE, NSE, NSE dos logaritmos, RMSE / desvio padrão, pico, volume e tempo do pico (vazão) ou erro / incerteza (séries com incerteza).
- **Weight**: Auto dá a cada tipo de observação uma parcela igual. Um número define o peso da série.
- **Changes only**: pontua as subidas e as descidas, e não um deslocamento constante. Serve para poços com datum incerto.
- **Use uncertainty**: pondera cada valor pelo inverso do quadrado da sua incerteza, de modo que os valores incertos contam menos. Vem ligado por padrão quando a série tem incertezas.

**Ignore observations before** define um período de aquecimento, que é simulado mas não é pontuado.

## 3. Parameters to calibrate {#3-parameters-to-calibrate}

Todos os parâmetros que este modelo pode calibrar aparecem na lista, agrupados por processo. Marque **Free** em cada parâmetro que a busca pode mudar. Os outros mantêm os valores do modelo.

- **Multiplicadores** (valor do modelo ×1) escalam juntos o valor, as tabelas de classes e o raster, para que o mapa mantenha o seu padrão. Comece por alguns deles.
- **Lower** e **Upper** definem a faixa de busca e podem ser editados.
- **Group** e **Show free only** encurtam a lista, e a contagem mostra quantos estão livres.
- Uma nota aparece quando há muitos parâmetros livres para os tipos de observação ajustados.

## 4. Search settings {#4-search-settings}

**Genetic algorithm**: tamanho da população (Auto é 10 por parâmetro livre), gerações, fração de elite, tamanho do torneio, probabilidades de cruzamento e de mutação, tamanho da mutação, população inicial, parada antecipada, limite de tempo e semente aleatória. A linha abaixo das configurações mostra o maior número possível de execuções do modelo e, depois de uma primeira calibração, uma estimativa do tempo.

**Computer**

- **Runs**: Auto (mede primeiro a memória de uma execução), One at a time (cada execução usa o computador inteiro) ou Several at a time.
- **Runs at a time** e **Threads per run**, para Several at a time.
- **Use at most**: a parcela da memória livre que várias execuções podem ocupar.
- **Device**: a CPU ou uma GPU, quando o computador tem uma, com a memória da GPU por execução.
- **Results folder**: por padrão, uma pasta nova ao lado do arquivo do modelo.
- **Resume the stopped calibration in this folder** continua uma calibração que foi cancelada ou interrompida.

## 5. Run {#5-run}

**Start calibration** verifica as escolhas e inicia a busca em segundo plano. O Studio continua disponível enquanto isso. A barra de progresso e a linha abaixo dela mostram a geração, a execução e a melhor pontuação até o momento, e o log lista cada execução.

**Cancel** interrompe as execuções em andamento no próximo passo do modelo. As execuções concluídas ficam salvas, e uma calibração retomada não as repete.

## 6. Results {#6-results}

- **Summary**: a melhor pontuação (0 é um ajuste perfeito), por que a busca parou, as execuções e o tempo gasto.
- **Best values**: cada parâmetro livre, o seu valor no modelo, o seu melhor valor, a faixa entre os melhores 10 % dos candidatos e se os dados conseguem determiná-lo.
- **Fit per series**: o erro do modelo atual e o da melhor execução, com o KGE ou o NSE da melhor execução.
- **Show**: todas as séries em painéis pequenos, a pontuação por série, o histórico da busca ou uma única série. Cada painel mostra as observações (com a sua incerteza), o modelo atual e a melhor execução.

<p align="center">
  <img src={useBaseUrl('/img/calibration/ga-calibration-series.png')} width="900" alt="Três painéis ao longo de uma hora com a vazão no exutório, a profundidade da água no canal e a profundidade do lençol freático na encosta, cada um com as observações, o modelo atual e a melhor execução" />
</p>

<p align="center">
  <em>Resultados de uma calibração curta, com as observações e a sua incerteza, o modelo atual (tracejado) e a melhor execução.</em>
</p>

**Apply to model** grava os melhores valores no modelo aberto, e o **Save** os guarda no arquivo. Um multiplicador sobre um raster de entrada grava o raster escalado na pasta de resultados e aponta o modelo para ele, sem mudar o original. **Undo apply** devolve o modelo ao estado anterior, desde que ele não tenha sido editado depois disso. **Show results folder** abre a pasta com as tabelas e as figuras da calibração.
