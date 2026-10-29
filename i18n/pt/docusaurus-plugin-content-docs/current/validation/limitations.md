---
title: Limitações
---

# Limitações da validação

O pacote de validação atual é uma campanha de verificação e análise de dinâmica controlada. Os testes avaliam as equações, o armazenamento, a interpretação das forçantes, as opções de roteamento e as condições de contorno em casos com referências conhecidas.

Esses testes não substituem calibração de campo, análise de incerteza ou validação observacional específica para cada local.

## Modo de malha Voronoi {#voronoi-mesh-mode}

O caminho de volumes finitos em malha Voronoi tem validação controlada em CPU, e não validação em escala de campo. A execução em GPU e o desempenho na escala da Índia estão bloqueados, e canais não resolvidos são suportados apenas pelo solucionador inercial local. Um caso que precise de roteamento cinemático, difusivo ou de momento completo deve usar canais 2D totalmente resolvidos até que se acrescente uma validação própria do acoplamento de canais.

No HydroPol2D-Python, a malha roda os módulos opcionais da grade regular no seu motor de CPU (NumPy): neve, qualidade da água, instabilidade humana, reservatórios, drenagem urbana, infraestrutura verde e bacias de detenção. Cada um foi comparado com a grade regular em uma malha formada pelas próprias células quadradas da grade, onde os dois concordam até o arredondamento. Nenhum foi comparado com observações em uma malha irregular. Os limites ainda em aberto são estes.

- o motor de malha em GPU (JAX) ainda não roda esses módulos;
- a instabilidade humana roda apenas como índice de risco contínuo (modo 1); um caso em malha com a classificação de deslizamento e tombamento (`human_risk.method: classification`, modo 3) para na verificação de entrada, que oferece a grade regular;
- reservatórios, drenagem urbana, infraestrutura verde e bacias de detenção exigem uma malha sem canais de rio nem tabelas subgrade, e a qualidade da água, uma malha sem canais de rio;
- um reservatório, uma boca de lobo, um compartimento de infraestrutura verde ou um dispositivo de bacia passa para a célula da malha que contém a maior parte da sua célula raster, e uma bacia ocupa as células da malha que cobre pela metade ou mais;
- com expoente de lavagem diferente de 1, a lavagem depende de quantas arestas a água atravessa ao sair de uma célula, de modo que uma malha Voronoi (cerca de seis arestas por célula) lava de forma diferente da grade (quatro faces).

## Subsuperfície em Camadas e Calibração por Recessão {#layered-subsurface-and-recession-calibration}

A subsuperfície em camadas tem testes controlados e paridade Python-MATLAB em domínios sintéticos em V, e não validação de campo. Os limites ainda em aberto são estes.

- não há fluxo lateral de água suspensa sobre regolito não saturado;
- não há tabela de classes de regolito nem saídas raster por camada;
- não há franja capilar, porque a ascensão capilar repõe a água do solo acima do lençol apenas até a capacidade de campo;
- o laço compilado do Python para cidades ainda não roda o esquema em camadas com fluxo lateral de águas subterrâneas.

A calibração por recessão foi testada com um experimento gêmeo em um vale sintético, e não com poços observados ou com um hidrograma de campo.

## Limites das evidências

Alguns casos hidrodinâmicos e de água subterrânea usam referências numéricas. Essas comparações permitem verificar a implementação quando não há solução analítica disponível, mas devem ser distinguidas da validação analítica.

Exemplos aplicados, como Stanford, mostram a configuração e a execução do modelo. Eles só constituem validação quando incluem observações, resultados calibrados ou de modelagem inversa, ou outra referência independente adequada.

## Recessão do modelo subgrade de Neal (2012)

Os testes do canal subgrade de Neal (2012) reproduzem o escoamento dentro das margens, a ativação da planície, a vazão de pico e a extensão máxima da inundação nas geometrias avaliadas. Uma célula grosseira com canal tem um único nível representativo de água. A água armazenada nas bancadas internas ou na planície externa não pode, portanto, receder de forma independente do canal embutido.

No teste escalonado, esse comportamento faz a planície do modelo de Neal (2012) secar antes da referência numérica em grade fina. Aplicações em que a drenagem tardia da planície controla o resultado devem comparar o tempo de recessão com observações ou com uma simulação hidráulica mais fina.
