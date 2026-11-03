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

## Módulos opcionais no MATLAB {#matlab-optional-modules}

Desde 2026-11-02, o HydroPol2D (MATLAB) roda drenagem urbana, bacias de detenção, infraestrutura verde e roteamento inercial local D8 na grade regular, com as equações do HydroPol2D-Python. Cada um foi comparado com o núcleo do Python (VAL-UD-001, VAL-POND-001, VAL-GI-001 e a verificação do D8). Nenhum foi comparado com observações. Limites em aberto:

- os quatro são configurados no script de bypass (a estrutura `InputData_Bypass` de `Config/input_data_bypass_script.m`). A planilha do caso não tem entradas para eles, então `flag_urban_drainage`, `flag_detention_ponds` ou `flag_green_infrastructure` = 1 no modo Excel interrompe a simulação, e `flag_d8_local_inertial` não é lido da planilha;
- a drenagem urbana roda só com o solucionador inercial local, sem o subgrade de canal e sem qualidade da água;
- o roteamento inercial local D8 (`flag_d8_local_inertial = 1`) exige `flag_inertial = 1` e o esquema de Bates. Ele não roda com o subgrade de canal, qualidade da água, risco humano, neve, hidrogramas de vazão ou de nível, postos observados, troca rio-aquífero, redução do DEM, drenagem urbana, bacias de detenção ou infraestrutura verde. `flag_d8_full_domain = 0` mantém um grafo de rio D8 dentro de uma planície D4; 1 coloca todas as células no grafo D8;
- o D8 antigo em raster (`flag_D8`) foi aposentado, e `flag_D8 = 1` interrompe a simulação;
- uma simulação em malha Voronoi ou quadtree recusa drenagem urbana, bacias de detenção e infraestrutura verde. Reservatórios, qualidade da água, risco humano (modo 1) e neve rodam nas malhas do MATLAB.

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
