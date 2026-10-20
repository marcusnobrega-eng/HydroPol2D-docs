---
title: Modelo subgrade de Neal (2012)
sidebar_label: Modelo subgrade
---
import useBaseUrl from '@docusaurus/useBaseUrl';

# Validação do modelo subgrade de Neal (2012)

O HydroPol2D representa canais mais estreitos que uma célula do modelo por meio da formulação retangular de [Neal et al. (2012)](https://doi.org/10.1029/2012WR012514). O canal e a planície de inundação trocam água dentro de cada célula grosseira. Suas vazões são calculadas separadamente e combinadas nas faces das células.

A validação compara três simulações inerciais locais:

1. uma grade fina que resolve explicitamente o canal e a planície;
2. uma grade grosseira comum, sem geometria de canal embutida;
3. uma grade grosseira com a formulação de canal subgrade de Neal (2012).

A simulação em grade fina é uma referência numérica. Ela permite avaliar se a representação subgrade preserva a resposta hidráulica perdida com o aumento da resolução da grade.

## Canal simples com escoamento dentro das margens

O primeiro caso isola o escoamento em um canal mais estreito que as células grosseiras. O trecho tem canal com `10 m` de largura e `1 m` de profundidade, declividade de fundo de `0,001` e coeficiente de Manning $n=0,035$. A referência explícita usa células de `10 m`. As simulações comum e Neal (2012) usam células de `30 m`.

Uma vazão constante de $5\ \mathrm{m^3\,s^{-1}}$ é aplicada a um trecho inicialmente seco com 30 células. Como a vazão permanece abaixo da capacidade do canal, o teste avalia o armazenamento no canal, a propagação da onda e o nível da água sem escoamento na planície.

| Modelo grosseiro | RMSE da vazão (m³/s) | NSE | RMSE do nível (m) | RMSE do perfil (m) |
|---|---:|---:|---:|---:|
| Comum | 0,677 | 0,561 | 0,689 | 0,689 |
| Neal (2012) | 0,098 | 0,991 | 0,053 | 0,059 |

A grade grosseira comum considera que toda a largura de `30 m` contém água em movimento. Por isso, ela armazena água em excesso e atrasa o hidrograma. O canal embutido de `10 m` produz nível e tempo de propagação mais próximos da referência explícita.

<img src={useBaseUrl('/validation/results/subgrid-neal/simple-channel-hydrograph-stage.png')} alt="Vazão de saída e nível interno nas simulações fina, grosseira comum e com canal de Neal (2012)" />

<img src={useBaseUrl('/validation/results/subgrid-neal/simple-channel-profile.png')} alt="Perfis longitudinais da superfície da água nas simulações fina, grosseira comum e com canal de Neal (2012)" />

## Canal composto

O segundo caso usa um trecho de `990 m` com canal de `10 m` de largura e `1 m` de profundidade e planícies laterais de `90 m` em cada lado. A declividade longitudinal é `0,005`, e o coeficiente de Manning é $n=0,035$ em toda a seção. A referência explícita usa células de `10 m`; as duas simulações grosseiras usam células de `30 m`.

O teste permanente aplica $100\ \mathrm{m^3\,s^{-1}}$. O teste transiente aplica um hidrograma de Nash com pico de $100\ \mathrm{m^3\,s^{-1}}$ em `30 min`.

| Forçante | Modelo grosseiro | RMSE na saída (m³/s) | NSE na saída | RMSE interno (m³/s) | RMSE do armazenamento (m³) |
|---|---|---:|---:|---:|---:|
| Constante | Comum | 6,178 | 0,954 | 4,819 | 2.439 |
| Constante | Neal (2012) | 4,189 | 0,979 | 3,346 | 734 |
| Hidrograma de Nash | Comum | 7,263 | 0,949 | 5,770 | 3.363 |
| Hidrograma de Nash | Neal (2012) | 4,044 | 0,984 | 2,987 | 781 |

A simulação de Neal (2012) reduz os erros de vazão e armazenamento para as duas forçantes. A comparação transiente mostra que a melhoria permanece durante a subida, o pico e a recessão do hidrograma.

<img src={useBaseUrl('/validation/results/subgrid-neal/composite-constant-hydrographs.png')} alt="Hidrogramas com vazão constante nas simulações explícita, grosseira comum e com canal de Neal (2012)" />

<img src={useBaseUrl('/validation/results/subgrid-neal/composite-nash-hydrographs.png')} alt="Hidrograma de entrada de Nash e hidrogramas simulados na saída e na seção interna" />

## Escoamento escalonado sobre as margens

O terceiro caso avalia a transição entre o canal e a planície de inundação. O trecho de `1 km` tem `300 m` de largura e declividade longitudinal de `0,005`. A seção transversal contém:

- um canal de `50 m` com coeficiente de Manning $n=0,035$;
- duas bancadas de `25 m`, situadas `0,5 m` acima do leito do canal;
- uma planície externa situada `1,0 m` acima do leito, com coeficiente de Manning $n=0,10$.

A referência explícita usa células de `5 m`. As simulações comum e Neal (2012) usam células de `100 m`. Um hidrograma de Nash atinge $200\ \mathrm{m^3\,s^{-1}}$ em `45 min`, acima das vazões analíticas de ativação de $31,4\ \mathrm{m^3\,s^{-1}}$ para as bancadas e $110,8\ \mathrm{m^3\,s^{-1}}$ para a planície externa.

<img src={useBaseUrl('/validation/results/subgrid-neal/staged-geometry-rating.png')} alt="Geometria escalonada do canal e curva analítica de vazão uniforme" />

| Métrica | Comum, 100 m | Neal (2012), 100 m |
|---|---:|---:|
| RMSE da vazão na saída (m³/s) | 15,476 | 2,723 |
| NSE da vazão na saída | 0,945 | 0,998 |
| RMSE da vazão na seção interna (m³/s) | 12,053 | 3,043 |
| RMSE da profundidade nas bancadas (m) | 0,180 | 0,018 |
| RMSE da profundidade máxima (m) | 0,280 | 0,040 |
| CSI da área molhada a 0,01 m | 0,334 | 0,998 |

O modelo de Neal (2012) reproduz a ativação das bancadas em `21 min`, no mesmo instante da referência explícita. A planície externa é ativada em `35 min`, comparada com `34 min` na referência. O hidrograma, a profundidade e a extensão máxima da inundação são mais próximos da referência que os resultados da grade comum de `100 m`.

<img src={useBaseUrl('/validation/results/subgrid-neal/staged-hydrographs.png')} alt="Hidrogramas na saída e na seção interna do canal escalonado" />

<img src={useBaseUrl('/validation/results/subgrid-neal/staged-depth-activation.png')} alt="Profundidades no canal, nas bancadas e na planície externa ao longo do tempo" />

<img src={useBaseUrl('/validation/results/subgrid-neal/staged-maximum-depth.png')} alt="Mapas de profundidade máxima para as simulações explícita, grosseira comum e de Neal (2012)" />

Todos os casos mantidos conservam água até a precisão numérica. O teste escalonado também identifica uma limitação. As bancadas do modelo de Neal (2012) secam em `126 min`, comparadas com `196 min` na referência explícita, e a planície externa seca em `152 min`, comparada com `237 min`. Uma célula grosseira de Neal (2012) tem um único nível representativo de água. Portanto, a água residual nas bancadas e na planície não pode drenar de forma independente do canal embutido.

## Interpretação admitida pelos testes

Os testes sustentam o uso da formulação de Neal (2012) para escoamento controlado dentro das margens, ativação da planície, hidráulica de pico e extensão máxima da inundação nas geometrias avaliadas. Eles não estabelecem a precisão em campo. Aplicações com recessões longas na planície devem comparar o tempo de drenagem com observações ou com uma referência hidráulica mais fina.

As equações e os dados de entrada necessários são descritos nas páginas [Modelo hidrodinâmico](../theory/hydrodynamic-model) e [Bandeiras do modelo](../configuration/flags).
