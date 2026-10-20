---
title: Limitações
---

# Limitações da validação

O pacote de validação atual é uma campanha de verificação e análise de dinâmica controlada. Os testes avaliam as equações, o armazenamento, a interpretação das forçantes, as opções de roteamento e as condições de contorno em casos com referências conhecidas.

Esses testes não substituem calibração de campo, análise de incerteza ou validação observacional específica para cada local.

## Subsuperfície em Camadas e Calibração por Recessão {#layered-subsurface-and-recession-calibration}

A subsuperfície em camadas tem testes controlados e paridade Python-MATLAB em domínios sintéticos em V, e não validação de campo. Os limites ainda em aberto são estes.

- não há fluxo lateral de água suspensa sobre regolito não saturado;
- não há tabela de classes de regolito nem saídas raster por camada;
- a água circula para cima e para baixo perto de um lençol freático raso, o que infla a ascensão capilar e a recarga brutas no balanço enquanto a troca líquida fica perto de zero;
- o fluxo implícito no lençol freático foi testado apenas em Python;
- o laço compilado do Python para cidades ainda não roda o esquema em camadas com fluxo lateral de águas subterrâneas.

A calibração por recessão foi testada com um experimento gêmeo em um vale sintético, e não com poços observados ou com um hidrograma de campo.

## Limites das evidências

Alguns casos hidrodinâmicos e de água subterrânea usam referências numéricas. Essas comparações permitem verificar a implementação quando não há solução analítica disponível, mas devem ser distinguidas da validação analítica.

Exemplos aplicados, como Stanford, mostram a configuração e a execução do modelo. Eles só constituem validação quando incluem observações, resultados calibrados ou de modelagem inversa, ou outra referência independente adequada.

## Recessão do modelo subgrade de Neal (2012)

Os testes do canal subgrade de Neal (2012) reproduzem o escoamento dentro das margens, a ativação da planície, a vazão de pico e a extensão máxima da inundação nas geometrias avaliadas. Uma célula grosseira com canal tem um único nível representativo de água. A água armazenada nas bancadas internas ou na planície externa não pode, portanto, receder de forma independente do canal embutido.

No teste escalonado, esse comportamento faz a planície do modelo de Neal (2012) secar antes da referência numérica em grade fina. Aplicações em que a drenagem tardia da planície controla o resultado devem comparar o tempo de recessão com observações ou com uma simulação hidráulica mais fina.
