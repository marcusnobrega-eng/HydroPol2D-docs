---
title: Hidrodinâmica e roteamento
---
import useBaseUrl from '@docusaurus/useBaseUrl';

# Validação da hidrodinâmica e do roteamento

A validação hidrodinâmica da Fase 1 foi organizada por família de roteamento. A sequência avaliou o modelo de momento completo, os métodos inercial local e autômatos celulares e, por fim, os modelos cinemático e difusivo corrigidos. Os testes verificam hidrogramas, conservação, simetria, condições de contorno e o comportamento esperado de cada conjunto de equações.

## Hidrodinâmica com momento completo

Foram usados cinco casos: hidrograma em plano inclinado, simetria e conservação na bacia em V, ruptura de barragem de Ritter em leito seco, onda sem ruptura e condição de contorno com nível prescrito.

| Caso | RMSE principal | L2 relativo | NSE | Erro de massa (%) |
|---|---:|---:|---:|---:|
| Hidrograma em plano inclinado | 0,0264 | 0,0311 | 0,9961 | `7,80 × 10^-12` |
| Simetria e conservação em V | `3,50 × 10^-18` | -- | -- | `2,74 × 10^-12` |
| Perfil de Ritter | 0,0305 | 0,0567 | 0,9992 | `1,26 × 10^-13` |
| Perfil de onda sem ruptura | 0,0116 | 0,0260 | 0,9997 | 4,5638 |
| Contorno com nível prescrito | 0,0000 | -- | -- | `1,35 × 10^-13` |

O plano inclinado reproduziu o limite de onda cinemática. A bacia em V conservou massa até a precisão numérica e preservou a simetria bilateral. O caso de Ritter verificou um escoamento descontínuo, e a onda sem ruptura avaliou uma perturbação móvel suave.

<img src={useBaseUrl('/validation/phase1/hydrodynamics/P1_HYDRO_FM_PLANE_001.png')} alt="Validação do momento completo no plano inclinado" />

<img src={useBaseUrl('/validation/phase1/hydrodynamics/P1_HYDRO_FM_VTILT_001.png')} alt="Validação do momento completo na bacia em V" />

<img src={useBaseUrl('/validation/phase1/hydrodynamics/P1_HYDRO_FM_RITTER_001.png')} alt="Validação de Ritter com momento completo" />

<img src={useBaseUrl('/validation/phase1/hydrodynamics/P1_HYDRO_FM_NBW_001_PROFILES.png')} alt="Perfis da onda sem ruptura com momento completo" />

## Modelo inercial local e autômatos celulares

O modelo inercial local aproxima as equações de águas rasas. O método de autômatos celulares redistribui escoamento e armazenamento, mas não é um solver de momento. O modelo inercial local passou os testes de plano inclinado, bacia em V e contorno com nível prescrito. A comparação de Ritter permanece diagnóstica. Os autômatos celulares passaram os testes de conservação, simetria e contabilidade nas condições de contorno.

| Método | Caso | RMSE | L2 relativo | NSE | Erro de massa (%) | Estado |
|---|---|---:|---:|---:|---:|---|
| Inercial local | Plano | 0,0169 | 0,0200 | 0,9984 | `7,47 × 10^-12` | passou |
| Inercial local | Bacia em V | 0,0000 | -- | -- | `3,66 × 10^-12` | passou |
| Inercial local | Ritter | 0,1823 | 0,3838 | 0,9552 | `5,05 × 10^-14` | diagnóstico não aprovado |
| Autômatos celulares | Plano | 0,0172 | 0,0204 | 0,9983 | `7,69 × 10^-12` | passou |
| Autômatos celulares | Bacia em V | 0,0000 | -- | -- | `4,04 × 10^-12` | passou |
| Autômatos celulares | Ritter | 0,1592 | 0,2957 | 0,9875 | `7,58 × 10^-14` | diagnóstico |

<div style={{display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(280px, 1fr))', gap: '1rem'}}>
  <img src={useBaseUrl('/validation/phase1/hydrodynamics/P1_HYDRO_LI_PLANE_001.png')} alt="Modelo inercial local no plano inclinado" />
  <img src={useBaseUrl('/validation/phase1/hydrodynamics/P1_HYDRO_CA_PLANE_001.png')} alt="Autômatos celulares no plano inclinado" />
</div>

<div style={{display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(280px, 1fr))', gap: '1rem'}}>
  <img src={useBaseUrl('/validation/phase1/hydrodynamics/P1_HYDRO_LI_RITTER_001.png')} alt="Diagnóstico de Ritter para o modelo inercial local" />
  <img src={useBaseUrl('/validation/phase1/hydrodynamics/P1_HYDRO_CA_RITTER_001.png')} alt="Diagnóstico de Ritter para autômatos celulares" />
</div>

O resultado de Ritter para o modelo inercial local identifica um limite do método. Ele não constitui validação para ruptura de barragem em leito seco.

## Hidrograma canônico da bacia em V

O hidrograma original da bacia em V foi avaliado com o fluxo completo de configuração e pré-processamento do HydroPol2D. Todos os métodos usaram o mesmo raster de `20 m`, chuva de `10,8 mm/h` durante `90 min`, as mesmas células de saída e os processos de perda desativados.

Os cinco métodos reproduziram o formato do hidrograma entre `0 min` e `180 min`. O erro do balanço chuva-saída-armazenamento foi `-0,0181 %` em todas as simulações.

| Método | RMSE (m³/s) | NSE | Erro do pico (%) | Erro de volume (%) | Erro de massa (%) |
|---|---:|---:|---:|---:|---:|
| Momento completo | 0,303 | 0,9730 | 0,052 | 7,50 | -0,0181 |
| Inercial local | 0,287 | 0,9759 | 2,05 | 5,04 | -0,0181 |
| Autômatos celulares | 0,323 | 0,9694 | 0,008 | 3,95 | -0,0181 |
| Cinemático | 0,249 | 0,9817 | 0,020 | 3,23 | -0,0181 |
| Difusivo | 0,255 | 0,9809 | 0,063 | 3,20 | -0,0181 |

<img src={useBaseUrl('/validation/phase1/hydrodynamics/P1_HYDRO_VTILT_ROUTING_HYDROGRAPH.png')} alt="Hidrograma canônico da bacia em V" />

<img src={useBaseUrl('/validation/phase1/hydrodynamics/P1_HYDRO_VTILT_ROUTING_VOLUME.png')} alt="Volume acumulado na saída da bacia em V" />

## Roteamento cinemático e difusivo corrigido

Os modelos cinemático e difusivo usam um núcleo conservativo comum para os fluxos nas faces D4. Ambos passaram os testes de plano inclinado, conservação na bacia em V e contorno com nível prescrito. O caso difusivo de Ritter não passou, como esperado para uma aproximação de onda difusiva aplicada a uma descontinuidade sobre leito seco.

| Método | Caso | RMSE | L2 relativo | NSE | Erro de massa (%) | Estado |
|---|---|---:|---:|---:|---:|---|
| Cinemático | Plano | 0,0156 | 0,0184 | 0,9986 | `7,66 × 10^-12` | passou |
| Cinemático | Bacia em V | 0,0000 | -- | -- | `4,18 × 10^-12` | passou |
| Cinemático | Ritter | 0,2408 | 0,5069 | 0,9245 | 0,0000 | diagnóstico |
| Difusivo | Plano | 0,0172 | 0,0203 | 0,9984 | `7,75 × 10^-12` | passou |
| Difusivo | Bacia em V | 0,0000 | -- | -- | `3,73 × 10^-12` | passou |
| Difusivo | Ritter | 0,5670 | 1,1151 | -0,0803 | `1,53 × 10^-12` | diagnóstico não aprovado |

<div style={{display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(280px, 1fr))', gap: '1rem'}}>
  <img src={useBaseUrl('/validation/phase1/hydrodynamics/P1_HYDRO_KIN_PLANE_001.png')} alt="Validação do modelo cinemático corrigido" />
  <img src={useBaseUrl('/validation/phase1/hydrodynamics/P1_HYDRO_DIFF_PLANE_001.png')} alt="Validação do modelo difusivo corrigido" />
</div>

## Interpretação admitida pelos testes

A Fase 1 sustenta a implementação atual de momento completo nos testes analíticos e de balanço listados acima. Ela também sustenta os métodos inercial local, autômatos celulares, cinemático e difusivo nos casos controlados apresentados. Os resultados de Ritter não devem ser interpretados como validação dos modelos inercial local e difusivo para ruptura de barragem em leito seco.

## Modelo subgrade de Neal (2012)

A extensão de Neal (2012) representa um canal mais estreito que a célula inercial local e combina as vazões do canal e da planície em cada face ortogonal. As comparações com referências numéricas em grade fina abrangem escoamento dentro das margens, canal composto permanente e transiente, ativação das margens e extensão máxima da inundação. A formulação melhora o hidrograma, o nível, o armazenamento e a área molhada em relação à grade grosseira comum em todos os casos mantidos. A recessão tardia na planície é menos precisa porque cada célula grosseira tem um único nível representativo de água.

A geometria, as métricas e as figuras são apresentadas em [Validação do modelo subgrade de Neal (2012)](./neal-subgrid).
