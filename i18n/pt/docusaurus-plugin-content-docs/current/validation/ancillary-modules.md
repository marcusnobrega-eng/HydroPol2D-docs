---
title: Reservatórios, contornos, qualidade da água e risco
---
import useBaseUrl from '@docusaurus/useBaseUrl';

# Reservatórios, contornos, qualidade da água e risco

Estes casos validam componentes do modelo que são importantes nas aplicações, mas que são mais fáceis de testar fora de uma simulação completa da bacia. A lógica é a mesma do restante da suíte de validação: isolar o processo, definir claramente a referência e separar o que o caso prova do que ele não prova.

## Depleção do reservatório pela curva-chave {#reservoir-rating-curve-depletion}

O caso `VAL-RES-001` isola a lógica de controle do reservatório usando um reservatório de área constante e uma única curva-chave na saída. Sem vazão de entrada externa, a referência exata é a solução de depleção da EDO do armazenamento.

| Caso | RMSE do armazenamento (m³) | RMSE da vazão de saída (m³/s) | L2 relativo | Erro do k recuperado (%) | Resíduo de massa (%) |
|---|---:|---:|---:|---:|---:|
| `VAL-RES-001` | 0,2730 | `4.96 × 10^-5` | `7.80 × 10^-6` | 0,0000 | `4.37 × 10^-13` |

O caso passou em todos os limiares. A pequena diferença no armazenamento é o erro de truncamento esperado da integração explícita em relação à EDO exata contínua. A contabilidade da água propriamente dita fecha até a precisão numérica.

<img src={useBaseUrl('/validation/results/ancillary/VAL_RES_001_RATING_CURVE.png')} alt="Validação da curva-chave do reservatório" />

## Condição de contorno por hidrograma de entrada {#inflow-hydrograph-boundary-condition}

O caso `VAL-BC-INFLOW-001` impõe um hidrograma triangular conhecido no contorno de montante de um domínio retangular com momento completo. A fonte da verdade é a integral exata do hidrograma de entrada prescrito. O hidrograma de jusante é diagnóstico, porque não se espera uma solução analítica de Saint-Venant para o domínio finito e rugoso.

| Caso | Erro do volume imposto (%) | Resíduo de massa (%) | Pico no exutório (m³/s) | Defasagem do pico (min) | Erro na magnitude do pico (%) |
|---|---:|---:|---:|---:|---:|
| `VAL-BC-INFLOW-001` | `3.41 × 10^-13` | `6.44 × 10^-13` | 7,3771 | 5,0 | 7,7862 |

O caso atendeu aos critérios de volume imposto e de balanço hídrico. Ao final da simulação, o volume de entrada prescrito estava contabilizado na vazão que saiu pelo exutório mais a água que permaneceu armazenada.

<img src={useBaseUrl('/validation/results/ancillary/VAL_BC_INFLOW_001_HYDROGRAPH.png')} alt="Validação do contorno por hidrograma de entrada" />

## Condição de contorno por hidrograma de nível {#stage-hydrograph-boundary-condition}

Os casos com hidrograma de nível prescrevem uma profundidade senoidal no contorno de montante de um domínio retangular. A cada passo, as células de nível de montante são redefinidas para o valor prescrito, o solver de roteamento selecionado propaga a perturbação e a contabilidade da água acompanha o volume adicionado pelo contorno, o volume que sai pelo exutório e o armazenamento restante.

O erro na imposição do nível prescrito foi zero, até a precisão numérica, nos roteamentos de momento completo, inercial local, autômatos celulares, cinemático e difusivo. As amplitudes da resposta a jusante variaram conforme o método, o que é esperado porque as equações de roteamento não são as mesmas, mas todos os erros de balanço hídrico ficaram muito abaixo de `0.1 %`.

<div style={{display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(260px, 1fr))', gap: '1rem'}}>
  <img src={useBaseUrl('/validation/results/ancillary/VAL_BC_STAGE_FM_001.png')} alt="Validação do contorno de nível com momento completo" />
  <img src={useBaseUrl('/validation/results/ancillary/VAL_BC_STAGE_LI_001.png')} alt="Validação do contorno de nível com o modelo inercial local" />
  <img src={useBaseUrl('/validation/results/ancillary/VAL_BC_STAGE_CA_001.png')} alt="Validação do contorno de nível com autômatos celulares" />
  <img src={useBaseUrl('/validation/results/ancillary/VAL_BC_STAGE_KIN_001.png')} alt="Validação do contorno de nível com o modelo cinemático" />
  <img src={useBaseUrl('/validation/results/ancillary/VAL_BC_STAGE_DIFF_001.png')} alt="Validação do contorno de nível com o modelo difusivo" />
</div>

## Leitura de rasters espaciais de chuva {#spatial-rainfall-raster-ingestion}

O caso `VAL-RAIN-MAP-001` valida a leitura dos rasters, a acumulação temporal, a conversão de unidades e a contabilidade do volume célula a célula antes que os mapas de chuva sejam acoplados ao roteamento, à infiltração ou à ET.

| Caso | RMSE por célula (m) | Erro máximo em uma célula (m) | Volume total (m³) | Erro de volume (%) | Erro máximo por passo (%) |
|---|---:|---:|---:|---:|---:|
| `VAL-RAIN-MAP-001` | 0 | 0 | 75,3333 | 0 | 0 |

O caso passou de forma exata. As lâminas acumuladas lidas dos rasters coincidiram com a referência prescrita célula a célula, e o volume de cada passo coincidiu com a integral analítica.

<img src={useBaseUrl('/validation/results/ancillary/VAL_RAIN_MAP_001_TOTALS.png')} alt="Validação dos rasters espaciais de chuva" />

## Qualidade da água {#water-quality}

O caso de qualidade da água valida o caminho atual de acumulação e lavagem baseado em massa do HydroPol2D antes de qualquer tentativa de calibração com polutogramas de campo. A escala dos parâmetros segue a acumulação e a lavagem de sólidos suspensos totais no estilo do SWMM, mas a fonte da verdade é o balanço de massa analítico, e não uma simulação numérica do SWMM.

Foram usadas três verificações determinísticas:

- inicialização da acumulação em tempo seco;
- lavagem exponencial em uma única célula;
- transferência e exportação conservativas entre duas células.

| Caso | RMSE da massa (kg) | Erro de exportação (%) | Resíduo de massa (kg) | Número de massas negativas |
|---|---:|---:|---:|---:|
| Acumulação em tempo seco | 0 | 0 | 0 | 0 |
| Lavagem em uma única célula | `4.998 × 10^-7` | `2.483 × 10^-4` | 0 | 0 |
| Transferência entre duas células | `6.272 × 10^-8` | `3.722 × 10^-5` | 0 | 0 |

A validação também revelou um artefato de implementação: a rotina original de lavagem arredondava a massa restante de poluente para seis casas decimais a cada subpasso, o que criava um erro de massa artificial nos testes analíticos. Essa quantização foi removida, e as métricas do código atual mostradas acima se referem à implementação corrigida.

<img src={useBaseUrl('/validation/results/ancillary/VAL_WQ_001_SINGLE_CELL.png')} alt="Validação da qualidade da água em uma única célula" />

<img src={useBaseUrl('/validation/results/ancillary/VAL_WQ_001_TWO_CELL.png')} alt="Validação da qualidade da água em duas células" />

## Risco e instabilidade humana {#human-risk-and-instability}

O caso de risco humano valida a álgebra implementada e a lógica de classificação, e não a previsão de segurança pública em escala de campo. Foram testados dois caminhos ativos do HydroPol2D:

- o índice simples de instabilidade, usado quando `flag_human_instability = 1`;
- o classificador detalhado por equilíbrio de forças, usado quando `flag_human_instability = 3`.

| Caso | RMSE | Erro máximo | Acurácia (%) | Erros nos limites de classe | Número de NaN |
|---|---:|---:|---:|---:|---:|
| Índice simples de instabilidade | 0 | 0 | 100 | 0 | 0 |
| Classificador de deslizamento/tombamento/afogamento | 0 | 0 | 100 | 0 | 0 |

A grade de teste do classificador detalhado percorreu todas as classes de saída implementadas e coincidiu exatamente com a referência independente.

<img src={useBaseUrl('/validation/results/ancillary/VAL_HR_001_SIMPLE_INSTABILITY.png')} alt="Validação do índice simples de instabilidade humana" />

<img src={useBaseUrl('/validation/results/ancillary/VAL_HR_001_FORCE_BALANCE.png')} alt="Validação do risco humano pelo equilíbrio de forças detalhado" />

## O que estes casos sustentam {#what-these-cases-support}

Estes casos complementares sustentam as implementações atuais da depleção de reservatórios, do tratamento dos contornos por vazão de entrada e por nível, da leitura de rasters de chuva, da contabilidade de qualidade da água baseada em massa e da classificação de risco humano, em condições controladas.

Eles não substituem a calibração de campo, a verificação das forçantes específicas de cada local nem os testes de desempenho com observações.
