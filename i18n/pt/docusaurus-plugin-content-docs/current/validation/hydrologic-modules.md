---
title: Módulos hidrológicos
---
import useBaseUrl from '@docusaurus/useBaseUrl';

# Validação dos módulos hidrológicos

Esta página documenta os casos de validação para interceptação pelo dossel, neve, infiltração e evapotranspiração. Esses casos foram planejados para responder primeiro a uma pergunta restrita: cada módulo reproduz as equações pretendidas e a contabilidade do armazenamento sob condições controladas? Essa resposta é então separada de perguntas posteriores sobre parâmetros de campo, calibração e desempenho na bacia.

## Configuração comum {#shared-setup}

A maioria dos casos hidrológicos usa a bacia sintética em V como contexto espacial comum. Esse domínio fornece uma estrutura consistente de DEM, solo, cobertura do solo, LAI e águas subterrâneas, mas a fonte da verdade continua vindo de uma solução analítica ou de uma implementação de referência independente.

## Interceptação pelo dossel {#canopy-interception}

### O que foi testado {#what-was-tested}

O caso `VAL-CANOPY-001` isola a rotina de armazenamento no dossel antes que a infiltração, o escoamento e as águas subterrâneas sejam ativados. A encosta esquerda usa `LAI = 0.5`, a faixa do canal usa `LAI = 0` e a encosta direita usa `LAI = 2.0`. Uma célula representativa de `20 m × 20 m` é usada na conversão de volume.

### Referência e método {#reference-and-method}

A rotina `interceptionModel.m` do HydroPol2D foi executada diretamente e comparada com uma referência independente do tipo balde para o dossel. O caso abrange o enchimento do dossel, o throughfall depois que a capacidade de armazenamento é excedida, o rebaixamento por evaporação e o bypass com `LAI = 0`.

### Resultado principal {#main-result}

O HydroPol2D reproduziu a referência independente até a precisão de arredondamento. As verificações de benchmark, de balanço de massa e de `NaN` passaram.

| Métrica | Valor | Limiar |
|---|---:|---:|
| RMSE do armazenamento no dossel (mm) | `1.50 × 10^-17` | `1.0 × 10^-9` |
| RMSE do throughfall (mm) | `1.31 × 10^-17` | `1.0 × 10^-9` |
| RMSE da evaporação (mm) | `7.31 × 10^-18` | `1.0 × 10^-9` |
| Resíduo máximo de massa (m³) | `2.22 × 10^-17` | `1.0 × 10^-6` |

Este caso valida as fórmulas implementadas do dossel e a contabilidade do armazenamento nas condições testadas. Ele não valida o comportamento da interceptação pelo dossel em campo, porque não usa dados observados de throughfall ou de stemflow.

## Módulo de neve {#snow-module}

### O que foi testado {#what-was-tested-1}

O caso `VAL-SNOW-001` testa o caminho configurável atual de neve. A sequência inclui precipitação fria, mista e quente; duas classes LULC com parâmetros de neve distintos; estados iniciais nulos, apenas com SWE, apenas com profundidade e com o par SWE e profundidade; refinamento do passo de tempo; equivalência entre planilha e bypass; e uma simulação acoplada de neve e escoamento na bacia em V.

### Referência e método {#reference-and-method-1}

Os testes controlados usam cálculos prescritos de balanço de massa para a partição chuva-neve, o derretimento por graus-dia, a conversão entre densidade e profundidade e o armazenamento. O caso completo na bacia em V usa o pré-processamento normal do HydroPol2D e o roteamento inercial local. Ele aplica 16,123.82 m³ de precipitação e verifica o balanço de todo o evento, se os estados de neve são finitos e o resíduo do módulo de neve.

### Resultado principal {#main-result-1}

As seis verificações passaram. O teste do passo de tempo deu uma diferença máxima de `1.36 × 10^-12 mm` entre as integrações de 5, 15 e 60 minutos. O evento acoplado na bacia em V fechou em `5.82 × 10^-11 m³`, ou `3.61 × 10^-13 %` da precipitação do evento. O próprio módulo de neve fechou em `3.55 × 10^-16 m³`.

| Verificação | Resultado | Critério de aceitação |
|---|---:|---:|
| Partição configurável e armazenamento | erro 0,0 | cálculo prescrito exato |
| Estados iniciais e mapeamento de duas classes | erro 0,0 | conversão exata e verificação do erro esperado |
| Refinamento de 5, 15 e 60 min | `1.36 × 10^-12 mm` | `< 1 × 10^-6 mm` |
| Acoplamento neve-escoamento na bacia em V | `6.39 × 10^-15 m³` | `< 1 × 10^-6 m³` |
| Equivalência entre planilha e bypass | erro 0,0 | equivalência exata dos mapas de parâmetros |
| Fechamento do evento completo na bacia em V | `3.61 × 10^-13 %` | `< 0.1 %` |

<img src={useBaseUrl('/validation/results/hydrologic/snow-validation-dynamics.png')} alt="Diagnósticos de partição da neve, equivalente de água da neve, derretimento, densidade e refinamento do passo de tempo" />

<img src={useBaseUrl('/validation/results/hydrologic/snow-full-vtilted.png')} alt="Séries temporais da profundidade da neve e da lâmina de água superficial no caso acoplado da bacia em V" />

O caminho testado lê os parâmetros de neve na linha correspondente da tabela de parâmetros LULC. `Initial_SWE_path` e `Initial_Snow_Depth_path` são opcionais. A [teoria do modelo hidrológico](../theory/hydrologic-model#5-snow-accumulation-melt-and-sublimation) define as regras de inicialização e o fallback de códigos de classe. Estes casos validam as equações, o mapeamento da configuração e a contabilidade acoplada. Eles não calibram um manto de neve com observações de campo.

## Infiltração {#infiltration}

### O que foi testado {#what-was-tested-2}

A suíte de infiltração usa a bacia em V com propriedades hidráulicas fisicamente interpretáveis das texturas franco-arenosa, franca e franco-argilosa, no estilo do USDA. Foram testados sete regimes:

- bypass sem infiltração;
- chuva limitada pelo suprimento;
- entrada limitada pela capacidade;
- excesso por saturação com armazenamento finito;
- percolação em camadas e recarga com atraso;
- excesso por saturação com lençol freático raso;
- contraste espacial de solos.

### Referência e método {#reference-and-method-2}

A fonte da verdade é uma rotina de referência independente em MATLAB que avalia a contabilidade pretendida da infiltração e do armazenamento em camadas fora do solver hidrodinâmico completo. Os testes seguem a ordem implementada, de cima para baixo: camada próxima à superfície, camada da zona radicular, camada de transmissão e recarga das águas subterrâneas quando o armazenamento vadoso está cheio e a recarga está ativa.

### Resultado principal {#main-result-2}

Os sete casos independentes de infiltração passaram depois que as propriedades do solo foram redefinidas para valores fisicamente consistentes, baseados na textura.

| Caso | Regime | Chuva (mm) | Infiltração (mm) | Escoamento (mm) | Recarga (mm) | Fechamento (mm) |
|---|---|---:|---:|---:|---:|---:|
| `VAL-INFIL-VT-000` | Sem infiltração | 60,0 | 0,0 | 60,0 | 0,0 | 0,0 |
| `VAL-INFIL-VT-001` | Limitado pelo suprimento | 10,0 | 10,0 | 0,0 | 0,0 | 0,0 |
| `VAL-INFIL-VT-002` | Limitado pela capacidade | 120,0 | 34,157 | 85,843 | 0,0 | `1.71 × 10^-13` |
| `VAL-INFIL-VT-003` | Limitado pelo armazenamento | 180,0 | 72,5 | 107,5 | 0,0 | 0,0 |
| `VAL-INFIL-VT-004` | Percolação em camadas | 384,0 | 384,0 | 0,0 | 197,614 | `1.23 × 10^-11` |
| `VAL-INFIL-VT-005` | Lençol freático raso | 150,0 | 75,0 | 75,0 | 22,683 | `-2.84 × 10^-14` |
| `VAL-INFIL-VT-006` | Contraste espacial de solos | 120,0 | 77,880 | 42,120 | 0,0 | `7.11 × 10^-15` |

A principal interpretação está no nível dos processos, e não é apenas numérica. O caso limitado pelo suprimento infiltrou toda a chuva. O caso limitado pela capacidade gerou excesso assim que a chuva superou a capacidade hidráulica de entrada. O caso limitado pelo armazenamento encheu o reservatório vadoso e então produziu escoamento por excesso de saturação. O caso de percolação em camadas atrasou a recarga em vez de enviar a água diretamente às águas subterrâneas.

<img src={useBaseUrl('/validation/results/hydrologic/VTilted_Infiltration_Hydrograph_Overview.png')} alt="Visão geral dos hidrogramas de infiltração na bacia em V" />

<p><em>Diagnósticos de infiltração em forma de hidrograma. As linhas pretas são a chuva, as linhas azuis são o escoamento ou o excesso superficial e as linhas verdes são a recarga.</em></p>

<img src={useBaseUrl('/validation/results/hydrologic/VTilted_Infiltration_Rate_Overview.png')} alt="Visão geral das taxas de infiltração na bacia em V" />

<p><em>Taxas de infiltração aceitas nos mesmos casos. As figuras são apresentadas em mm/h para mostrar como cada regime responde ao longo do tempo.</em></p>

Isso valida a contabilidade implementada da infiltração e a dinâmica do solo em camadas nos regimes de validação testados. Não valida parâmetros de infiltração em campo, o fluxo em macroporos, o fluxo preferencial nem um hidrograma calibrado da bacia.

## Evapotranspiração {#evapotranspiration}

### O que foi testado {#what-was-tested-3}

A suíte de evapotranspiração usa a grade da bacia em V para testar tanto o cálculo da ET potencial quanto a extração da ET real. Foram testados sete regimes:

- reprodução da fórmula da ET potencial;
- limitação pelo armazenamento de água livre;
- extração do solo limitada pela demanda;
- extração do solo limitada pelo armazenamento;
- acesso parcial das raízes à camada próxima à superfície;
- modo interno de ETP;
- mascaramento de células secas, impermeáveis e inválidas.

### Referência e método {#reference-and-method-3}

O primeiro caso compara o cálculo da ET de referência do HydroPol2D com uma implementação independente de Penman-Monteith no estilo da FAO. Os casos de extração comparam a ET real do solo, a evaporação de água livre, o armazenamento final, o comportamento das máscaras e os resíduos de massa com uma referência algébrica independente.

### Resultado principal {#main-result-3}

Os sete casos passaram. O caso da ET de referência produziu valores médios de ET potencial idênticos no HydroPol2D e na referência independente, `5.7669 mm/day`. Nos casos de extração, o HydroPol2D reproduziu a ET do solo, a evaporação de água livre e o armazenamento final até a precisão de máquina.

| Caso | Regime | ETP média (mm/day) | ET do solo (soma em mm) | E superficial (soma em mm) | Resíduo (m³) |
|---|---|---:|---:|---:|---:|
| `VAL-ET-VT-000` | Fórmula da ET potencial | 5,7669 | -- | -- | 0,0 |
| `VAL-ET-VT-001` | Limite de água livre | -- | 0,0 | 27,0 | `-4.44 × 10^-14` |
| `VAL-ET-VT-002` | Limitado pela demanda do solo | -- | 36,0 | 0,0 | `9.24 × 10^-14` |
| `VAL-ET-VT-003` | Limitado pelo armazenamento do solo | -- | 27,0 | 0,0 | `-4.44 × 10^-14` |
| `VAL-ET-VT-004` | Acesso parcial das raízes | -- | 45,0 | 0,0 | 0,0 |
| `VAL-ET-VT-005` | Modo interno de ETP | -- | 18,0 | 12,0 | `3.55 × 10^-15` |
| `VAL-ET-VT-006` | Máscaras e células secas | -- | 12,0 | 0,0 | `4.44 × 10^-15` |

<img src={useBaseUrl('/validation/results/hydrologic/VTilted_ET_Overview.png')} alt="Visão geral da validação da evapotranspiração na bacia em V" />

<p><em>ET potencial, ET real do solo, evaporação de água livre, armazenamento antes e depois da ET e erros absolutos de validação nos casos de ET da bacia em V.</em></p>

Estes testes validam o caminho implementado da fórmula de ET e a contabilidade da extração da ET real em regimes controlados. Eles não validam a ET em escala de campo, os coeficientes de cultura nem a calibração sazonal do balanço hídrico.
