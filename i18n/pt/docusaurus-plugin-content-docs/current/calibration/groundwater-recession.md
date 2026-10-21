---
title: Calibração por Recessão das Águas Subterrâneas
---
import useBaseUrl from '@docusaurus/useBaseUrl';

# Calibração por Recessão das Águas Subterrâneas

O HydroPol2D estima parâmetros efetivos das águas subterrâneas, na escala da bacia, ajustando a recessão simulada no exutório a uma curva mestra de recessão (MRC) observada. A calibração roda no HydroPol2D-Python. Os resultados aceitos viram entradas comuns do caso, e assim Python e MATLAB partem dos mesmos parâmetros e estados (veja o [Fluxo de construção do modelo](../getting-started/model-building-workflow#groundwater-calibrated-workflow)).

O que a calibração ajusta depende do esquema de subsuperfície.

| Esquema | Parâmetros ajustados |
|---|---|
| Padrão | Condutividade horizontal uniforme $K_{sat,h}$ e rendimento específico $S_y$ |
| [Em camadas](../theory/layered-subsurface) | Dois multiplicadores da condutividade horizontal, um para as camadas de solo e outro para as camadas de regolito |

Os valores ajustados são parâmetros efetivos. Eles reproduzem a recessão observada dentro desta estrutura de modelo. Não são medições pontuais do material do aquífero.

---

## 1. Fluxo de Trabalho {#1-workflow}

Os dois esquemas seguem as mesmas etapas.

1. Ler um CSV local de vazões diárias ou baixar as vazões diárias de um posto fluviométrico do USGS.
2. Separar o escoamento de base com o filtro de Lyne–Hollick e montar a MRC a partir dos eventos de recessão.
3. Separar a cauda lenta do aquífero profundo do alvo raso, mais rápido.
4. Para cada candidato, rodar um período de aquecimento (spin-up) do modelo até o regime permanente sob a vazão alvo (Seção 4).
5. Equilibrar o estado do rio e propagar a liberação das águas subterrâneas pelo solver hidráulico de superfície até o exutório.
6. Pontuar a recessão propagada até o exutório contra a parte rasa da MRC.
7. Salvar o melhor checkpoint hidráulico completo, com água superficial, águas subterrâneas rasas, água do solo, armazenamentos do aquífero profundo e momento D8.

A pontuação combina forma e volume, para que as vazões altas não dominem o ajuste

$$
J = \mathrm{RMSE}\left(\ln Q_{\mathrm{sim}},\ \ln Q_{\mathrm{obs}}\right) + 0.5\,\frac{\left|V_{\mathrm{sim}} - V_{\mathrm{obs}}\right|}{V_{\mathrm{obs}}}
$$

onde $V$ é o volume da recessão no período pontuado.

**Esquema padrão:**

```bash
hydropol2d calibrate-groundwater-recession case.yaml master_recession calibration \
  --usgs-site 02147020 --start-date 1980-01-01 --end-date 2019-09-29 \
  --ksat-values 1e-5,5e-5,1e-4 --specific-yield-values 0.03,0.05,0.1 \
  --shallow-checkpoint-fraction 0.05
```

Para um arquivo local, substitua os argumentos do USGS por `--discharge-csv observations.csv`. As colunas padrão são `date` e `observed_discharge_m3_s`.

---

## 2. Esquema em Camadas: Dois Multiplicadores da Condutividade Lateral {#2-layered-scheme-two-lateral-conductivity-multipliers}

Com `vertical.subsurface.scheme: layered`, $S_y$ não é ajustado. Cada camada toma $S_y$ da sua curva de retenção ($\theta_s - \theta_{fc}$), e uma recessão restringe apenas a razão $K/S_y$ ([Brutsaert e Nieber, 1977](https://doi.org/10.1029/WR013i003p00637)). A calibração ajusta, em vez disso, dois fatores na escala da bacia, aplicados à condutividade horizontal mapeada.

| Parâmetro | Atua sobre |
|---|---|
| `vertical.subsurface.soil_lateral_conductivity_multiplier` | As três camadas de solo: $K_{sat}$ do solo × `soil_lateral_anisotropy` |
| `vertical.subsurface.regolith_lateral_conductivity_multiplier` | As camadas de regolito: $K_h$ do regolito (escalar, raster ou o $K_{sat}$ das águas subterrâneas) |

**Por que os dois fatores podem ser separados.** As vazões altas do início drenam enquanto o lençol freático está no solo. As vazões baixas do fim drenam enquanto ele está no regolito. A forma da recessão pode, então, separar os dois fatores. Se isso ocorre depende da bacia e da série, em particular da regularização das vazões, do ruído e da frequência com que o lençol chega ao solo. Cada execução informa esse resultado (Seção 3).

```bash
hydropol2d calibrate-groundwater-recession case.yaml master_recession calibration \
  --discharge-csv observations.csv --soil-multipliers 0.1,0.3,1,3,10 \
  --regolith-multipliers 0.1,0.3,1,3,10
```

---

## 3. Saídas de Identificabilidade {#3-identifiability-outputs}

Toda execução em camadas grava `coupled_identifiability.json` e `coupled_objective_surface.png`.

| Saída | Significado |
|---|---|
| Conjunto aceitável | Candidatos com $J \le 1.05\,J_{\mathrm{best}} + 0.01$ |
| Décadas abrangidas | Faixa de cada multiplicador no conjunto aceitável, em unidades de $\log_{10}$ |
| Indicador de borda da grade | Indica se o melhor valor está na borda da grade de candidatos; nesse caso, amplie a grade |
| Correlação dos log-multiplicadores | Correlação entre os logaritmos dos dois multiplicadores no conjunto aceitável; um valor fortemente negativo indica um vale de compensação (trade-off) |
| Expoente de recessão $b$ | Expoente de $-\mathrm{d}Q/\mathrm{d}t = a\,Q^b$, para o alvo e para cada candidato |

Os dois esquemas também gravam os arquivos abaixo.

| Arquivo | Conteúdo |
|---|---|
| `master_recession_curve.csv` | Componentes total, raso e profundo da recessão observada |
| `coupled_candidate_scores.csv` | Função objetivo e diagnósticos de cada candidato |
| `coupled_best_recession.csv` | Alvo observado e recessão propagada até o exutório |
| `coupled_recession_checkpoint.npz` | Estado hidráulico inicial completo selecionado |
| `coupled_calibration_metadata.json` | Parâmetros, método e critério do checkpoint |

O checkpoint selecionado pode ser deslocado para o tempo zero do modelo. Esse deslocamento mantém a água física e as memórias hidráulicas e zera os diagnósticos acumulados e a referência do balanço de massa.

---

## 4. Spin-up {#4-spin-up}

Cada candidato parte do seu próprio regime permanente sob a vazão alvo. Essa é a principal lição numérica da calibração em camadas.

1. **Rodar os próprios fluxos da coluna do modelo.** O spin-up usa a recarga que desce pelas camadas não saturadas, o fluxo de Darcy no lençol freático, a drenagem pelo leito do rio a cada passo e o fluxo lateral no seu próprio relógio. Assim, a recessão não começa com uma zona não saturada longe do regime permanente.
2. **Usar primeiro passos de 1 h.** Eles rodam até que a fonte média na janela e a amplitude do armazenamento fiquem dentro das tolerâncias ao longo de um ano simulado.
3. **Depois, usar os próprios passos do modelo** por 30 dias.
4. **Testar o regime permanente pela amplitude do armazenamento, nunca pelos valores inicial e final.** Um transiente que enche rápido e drena devagar passa num teste de valores inicial e final no seu pico de armazenamento.

**O que dava errado antes da correção.** Na simulação de referência (a "verdade") do experimento gêmeo, o solo ficava na capacidade de campo no início da recessão. A ascensão capilar para esse solo chegou a 0.10 m³/s, contra uma vazão de saída de 0.005 m³/s. Cerca de 50 000 m³ passaram para a zona não saturada em 6 dias, e no dia 18 o rio estava quase desconectado. Quem dominou a recessão foi a ascensão capilar, e não o aquífero.

---

## 5. Experimentos Gêmeos {#5-twin-experiments}

Um experimento gêmeo testa a identificabilidade antes do uso de dados reais.

1. Escolher multiplicadores "verdadeiros" conhecidos.
2. Rodar o modelo para gerar uma recessão sintética.
3. Adicionar ruído log-normal.
4. Calibrar com a recessão ruidosa.
5. Verificar se a verdade é recuperada.

As ferramentas estão em `hydropol2d.calibration.recession_twin` (`run_recession_twin_experiment`, `write_recession_twin_report`).

### 5.1 Resultado em um vale de drenagem rápida {#51-result-on-a-fast-draining-valley}

Esta rodada (2026-10-20) usa a física atual, incluindo a regra de reposição capilar da [subsuperfície em camadas](../theory/layered-subsurface#44-darcy-flux-at-the-water-table).

| Configuração | Valor |
|---|---|
| Vale | Em V, 11 × 15 células de 20 m |
| Rendimento específico | solo cerca de 0.12, regolito 0.05 |
| Início | 1.5 mm/dia de vazão de saída |
| Grade de candidatos | solo 1, 3, 10 × regolito 0.1, 0.3, 1 (3 × 3) |
| Verdade | solo 3, regolito 0.3 |
| Recessão | 30 dias |

| Ruído | Melhor candidato | Candidatos aceitáveis | Função objetivo, melhor | Função objetivo, segundo melhor |
|---|---|---:|---:|---:|
| 0 % | solo 3, regolito 0.3 | 1 | 0.033 | 0.123 |
| 5 % | solo 3, regolito 0.3 | 1 | 0.065 | 0.117 |
| 10 % | solo 3, regolito 0.3 | 1 | 0.106 | 0.131 |

A verdade foi recuperada nos três níveis de ruído e foi o único par aceitável em todos eles. Os nove candidatos propagados levaram 68 min em um notebook com 2 workers. As três linhas pontuam os mesmos nove candidatos propagados. Só muda o ruído adicionado ao alvo.

Na primeira rodada, antes da regra de reposição capilar (2026-10-19), a verdade também foi o melhor candidato, mas com 10 % de ruído o multiplicador do solo foi aceito em toda a faixa de 3 a 10.

<p align="center">
  <img src={useBaseUrl('/img/calibration/layered-twin-experiment.png')} width="900" alt="À esquerda, a recessão alvo com 5 por cento de ruído, a recessão verdadeira e o melhor candidato em eixo logarítmico ao longo de 30 dias. À direita, a função objetivo na grade 3 por 3 de multiplicadores do solo e do regolito, com o melhor candidato coincidindo com a verdade" />
</p>

<p align="center">
  <em>Figura 1. Experimento gêmeo com 5 % de ruído. À esquerda, alvo, verdade e melhor candidato. À direita, função objetivo na grade de candidatos. O candidato circulado é o único aceitável, e é a verdade.</em>
</p>

### 5.2 O que limita o teste {#52-what-limits-the-test}

- **Ruído entre execuções.** Na rodada de 2026-10-19, repetir a simulação com os mesmos parâmetros deu uma dispersão diária de ±2.7 %, vinda de uma oscilação de dois intervalos no canal pequeno. Diferenças entre candidatos abaixo dessa ordem ficam dentro do ruído entre execuções.
- **O vale gêmeo padrão é lento demais.** Com encostas de 500 m e $S_y$ do solo de cerca de 0.29, ele drena ao longo de anos. A recessão caiu apenas 9 % em 20 dias, plana demais para separar os candidatos. Para recessões de semanas, use encostas mais curtas e um $S_y$ menor, como na Seção 5.1.
- **Um teste gêmeo não é um teste de campo.** Ele mostra que o método consegue recuperar parâmetros em um vale sintético com a mesma estrutura de modelo. Séries reais acrescentam regularização das vazões, evapotranspiração e erro de medição.

---

## 6. Estado Inicial do Aquífero Profundo {#6-deep-aquifer-starting-state}

O mesmo filtro, a mesma MRC e a mesma separação da cauda profunda fornecem a vazão inicial de saída do aquífero profundo.

```bash
hydropol2d estimate-deep-baseflow observations.csv --start-date 2019-06-01 \
  --drainage-area-km2 5320 --output deep_baseflow.json
```

A ferramenta posiciona na MRC o escoamento de base da data inicial e divide a sua parte profunda pela área de drenagem. O relatório também fornece o tempo de resposta da cauda, que pode ser usado em `deep_aquifer_response_time_days`. Escolha uma data inicial dentro de uma recessão. A ferramenta avisa quando a vazão na data inicial é mais que o dobro do escoamento de base. A teoria está em [Modelo de Águas Subterrâneas, Seção 13.3](../theory/groundwater-model#133-starting-state).

---

## 7. Case Builder {#7-case-builder}

O Case Builder dispara a calibração para qualquer um dos esquemas.

1. Em um caso em camadas, o disparo passa `--soil-multipliers` e `--regolith-multipliers`.
2. A finalização grava os multiplicadores ajustados no caso Python (`vertical.subsurface`) e no executor MATLAB (`HYDROPOL_SOIL_LATERAL_CONDUCTIVITY_MULTIPLIER`, `HYDROPOL_REGOLITH_LATERAL_CONDUCTIVITY_MULTIPLIER`).
3. $S_y$ permanece nas curvas de retenção. Nenhum raster uniforme de $K_{sat}$ ou de $S_y$ é gravado.
4. O `DeepAquiferInitialState.json` da calibração substitui qualquer escoamento de base inicial ou recarga média informados manualmente.

---

## Fontes {#sources}

- Brutsaert, W., and Nieber, J. L. (1977). Regionalized drought flow hydrographs from a mature glaciated plateau. *Water Resources Research*, 13(3), 637–643. [doi:10.1029/WR013i003p00637](https://doi.org/10.1029/WR013i003p00637)
- Lyne, V., and Hollick, M. (1979). Stochastic time-variable rainfall-runoff modelling. *Institute of Engineers Australia National Conference*, Publication 79/10, 89–93.
