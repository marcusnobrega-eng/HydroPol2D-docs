---
title: Validação dos módulos hidrológicos
---
import useBaseUrl from '@docusaurus/useBaseUrl';

# Validação dos módulos hidrológicos

Esta página descreve os testes da validação para interceptação pelo dossel, neve, infiltração e evapotranspiração. A pergunta é direta: cada módulo reproduz suas equações e seu balanço de armazenamento sob condições controladas? Essa evidência é separada de calibração e desempenho em campo.

## Configuração comum

Os casos usam a bacia sintética em V do HydroPol2D quando uma grade espacial é necessária. As soluções analíticas, os cálculos independentes ou os balanços de massa prescritos são a fonte de referência.

## Interceptação pelo dossel

`VAL-CANOPY-001` compara o armazenamento do dossel, a evaporação e a precipitação que chega ao solo com um balanço de reservatório. Os erros de armazenamento, evaporação e passagem de chuva foram inferiores a `5.55 × 10^-17 mm`; o maior resíduo foi `2.22 × 10^-17 m³`.

## Módulo de neve

### O que foi testado

`VAL-SNOW-001` testa o caminho configurável de neve. A sequência inclui precipitação fria, mista e quente; duas classes LULC com parâmetros distintos; estados iniciais sem raster, com SWE, com profundidade e com ambos os mapas; refinamento de passo de tempo; equivalência entre planilha e bypass; e uma simulação acoplada de neve e escoamento na bacia em V.

### Método e resultados

Os testes controlados usam balanços prescritos para a partição chuva-neve, derretimento por graus-dia, conversão entre densidade e profundidade, e armazenamento. O evento completo usa o pré-processamento normal do HydroPol2D e roteamento inercial local. Ele aplica `16,123.82 m³` de precipitação e verifica o balanço de todo o evento, os estados de neve e o resíduo interno do módulo.

Todos os seis testes passaram. O refinamento entre 5, 15 e 60 minutos teve diferença máxima de `1.36 × 10^-12 mm`. O evento completo fechou em `5.82 × 10^-11 m³`, ou `3.61 × 10^-13 %` da precipitação; o resíduo do módulo de neve foi `3.55 × 10^-16 m³`.

| Verificação | Resultado | Critério |
|---|---:|---:|
| Partição e armazenamento | 0.0 mm | exato |
| Estados iniciais e duas classes | 0.0 erro | conversão exata e erro esperado |
| Refinamento de 5, 15 e 60 min | `1.36 × 10^-12 mm` | `< 1 × 10^-6 mm` |
| Acoplamento neve-escoamento na bacia em V | `6.39 × 10^-15 m³` | `< 1 × 10^-6 m³` |
| Equivalência planilha-bypass | 0.0 erro | mapas de parâmetros idênticos |
| Fechamento do evento completo | `3.61 × 10^-13 %` | `< 0.1 %` |

<img src={useBaseUrl('/validation/results/hydrologic/snow-validation-dynamics.png')} alt="Diagnósticos de partição, armazenamento e refinamento temporal da neve" />

<img src={useBaseUrl('/validation/results/hydrologic/snow-full-vtilted.png')} alt="Série temporal de neve e água superficial na bacia em V" />

Os parâmetros de neve são lidos na linha correspondente da tabela de parâmetros LULC. `Initial_SWE_path` e `Initial_Snow_Depth_path` são opcionais. A página do [modelo hidrológico](../theory/hydrologic-model#5-acúmulo-derretimento-e-sublimação-de-neve) descreve a inicialização e o fallback de códigos de classe. Estes casos verificam equações, mapeamento de entrada e balanço acoplado; não calibram a neve com observações de campo.

## Infiltração

Os casos de infiltração verificam regimes sem infiltração, limitados pelo suprimento, limitados pela capacidade, excesso por saturação, percolação em camadas, lençol freático raso e contraste espacial de solos. O armazenamento em camadas permanece não negativo e conservativo.

## Evapotranspiração

Os casos de ET comparam a ET de referência com cálculos independentes e verificam os limites de extração de água do solo e da superfície.

## Interpretação

Os resultados são evidência de validação para fórmulas, armazenamento e dinâmica controlada. Eles não são uma validação observacional de bacias.
