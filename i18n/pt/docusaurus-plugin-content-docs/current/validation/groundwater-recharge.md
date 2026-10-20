---
title: Águas Subterrâneas e Recarga
---
import useBaseUrl from '@docusaurus/useBaseUrl';

# Validação das Águas Subterrâneas e da Recarga

A seção de águas subterrâneas da suíte de validação testa tanto a contabilidade local das águas subterrâneas quanto a dinâmica lateral. A principal mudança de implementação é o agendador assíncrono. A drenagem vadosa, a produção de recarga e a ascensão capilar são avaliadas a cada passo do modelo de superfície, enquanto o armazenamento saturado e as cargas laterais só são atualizados quando o agendador das águas subterrâneas dispara uma atualização.

## O que foi testado {#what-was-tested}

Quatro casos de águas subterrâneas na bacia em V foram usados para avaliar o armazenamento local e o comportamento do agendador.

- `VAL-GW-ASYNC-001`: elevação do lençol freático sob recarga constante;
- `VAL-GW-ASYNC-002`: equivalência do agendador assíncrono;
- `VAL-GW-CAP-001`: rebaixamento por ascensão capilar;
- `VAL-GW-MOUND-001`: domo de recarga de Boussinesq contra uma referência numérica com passo de tempo fino.

Dois casos adicionais de encosta reforçam a evidência sobre o fluxo lateral das águas subterrâneas.

- `VAL-GW-HILL-STEADY-001`: perfil de Dupuit em regime permanente;
- `VAL-GW-HILL-TRANSIENT-001`: decaimento transiente de Boussinesq linearizado.

## Recarga local e comportamento do agendador {#local-recharge-and-scheduler-behavior}

### Referência e método {#reference-and-method}

O caso de recarga local usa a relação analítica de armazenamento `Δh = RΔt / S_y`, com o fluxo lateral das águas subterrâneas e a exfiltração desativados. O caso de equivalência do agendador compara a atualização legada das águas subterrâneas a cada passo com o agendador assíncrono por acumulação. O caso de ascensão capilar aplica um fluxo ascendente simples, limitado fisicamente, das águas subterrâneas rasas para o armazenamento vadoso seco. O caso do domo de recarga ativa o fluxo lateral e compara o resultado assíncrono com uma referência numérica interna de passo de tempo fino.

### Resultado principal {#main-result}

Os quatro casos locais de águas subterrâneas passaram.

| Caso | Regime | RMSE da carga (m) | Erro máximo de carga (m) | Erro de armazenamento (%) | Resíduo (m³) |
|---|---|---:|---:|---:|---:|
| `VAL-GW-ASYNC-001` | Recarga local | 0.0 | 0.0 | 0.0 | `1.96 × 10^-11` |
| `VAL-GW-ASYNC-002` | Equivalência do agendador | `1.71 × 10^-13` | `1.71 × 10^-13` | `1.67 × 10^-11` | `1.84 × 10^-10` |
| `VAL-GW-CAP-001` | Ascensão capilar | 0.0 | 0.0 | 0.0 | `-1.45 × 10^-12` |
| `VAL-GW-MOUND-001` | Domo de Boussinesq | `1.83 × 10^-8` | `9.90 × 10^-8` | `5.23 × 10^-13` | `3.09 × 10^-11` |

<div style={{display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(280px, 1fr))', gap: '1rem'}}>
  <img src={useBaseUrl('/validation/results/groundwater/VAL_GW_ASYNC_001_head_recharge.png')} alt="Elevação analítica do lençol freático sob recarga constante" />
  <img src={useBaseUrl('/validation/results/groundwater/VAL_GW_ASYNC_002_equivalence.png')} alt="Equivalência do agendador assíncrono das águas subterrâneas" />
</div>

<p><em>Diagnósticos do agendador de recarga. O primeiro caso verifica a elevação analítica do lençol freático sob recarga constante. O segundo compara o agendador assíncrono com a atualização legada das águas subterrâneas a cada passo.</em></p>

<div style={{display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(280px, 1fr))', gap: '1rem'}}>
  <img src={useBaseUrl('/validation/results/groundwater/VAL_GW_CAP_001_capillary.png')} alt="Validação da ascensão capilar" />
  <img src={useBaseUrl('/validation/results/groundwater/VAL_GW_MOUND_001_reference.png')} alt="Validação do domo de recarga de Boussinesq" />
</div>

<p><em>Diagnósticos de ascensão capilar e de fluxo lateral. O caso do domo é uma evidência útil com referência numérica, mas continua mais fraco que um benchmark analítico.</em></p>

A acumulação da recarga, a atualização assíncrona das águas subterrâneas e o fechamento simples de ascensão capilar se comportaram como esperado em condições controladas.

## Benchmarks analíticos de encosta {#analytical-hillslope-benchmarks}

### Referência e método {#reference-and-method-1}

O caso de encosta em regime permanente compara o HydroPol2D com o perfil de Dupuit em forma fechada, sob recarga uniforme e carga fixa no dreno. O caso transiente compara o solver de Boussinesq do HydroPol2D com o primeiro modo próprio da equação de Boussinesq linearizada, no regime de pequenas perturbações.

### Resultado principal {#main-result-1}

Os dois casos analíticos de encosta passaram.

| Caso | Benchmark | RMSE da carga (m) | Erro máximo de carga (m) | Métrica de vazão |
|---|---|---:|---:|---|
| `VAL-GW-HILL-STEADY-001` | Dupuit em regime permanente | `6.04 × 10^-3` | `9.75 × 10^-3` | Erro na vazão do dreno = `3.74 × 10^-4 %` |
| `VAL-GW-HILL-TRANSIENT-001` | Boussinesq linearizado | `1.94 × 10^-5` | `4.46 × 10^-5` | `NSE = 0.99985` |

<img src={useBaseUrl('/validation/results/groundwater/VAL_GW_HILL_STEADY_001_profile.png')} alt="Benchmark de águas subterrâneas em encosta com perfil de Dupuit em regime permanente" />

<p><em>Benchmark de Dupuit em regime permanente. O painel inferior mostra o erro absoluto do perfil em relação à solução analítica.</em></p>

<img src={useBaseUrl('/validation/results/groundwater/VAL_GW_HILL_TRANSIENT_001_profiles_hydrograph.png')} alt="Benchmark transiente de encosta com a equação de Boussinesq linearizada" />

<p><em>Benchmark transiente de encosta. O painel superior compara os perfis de carga durante o decaimento da perturbação. O painel inferior compara o fluxo no pé da encosta, por unidade de largura, modelado e analítico.</em></p>

## Subsuperfície em camadas {#layered-subsurface}

A [subsuperfície em camadas](../theory/layered-subsurface) foi incluída em outubro de 2026. A evidência reúne testes unitários em Python das regras da coluna, paridade entre Python e MATLAB, simulações do modelo completo na bacia em V em MATLAB e um experimento gêmeo de calibração.

### Testes de coluna em Python {#python-column-tests}

O HydroPol2D-Python testa diretamente a coluna em camadas, o estresse de Feddes e o estado inicial do aquífero profundo (`tests/test_subsurface_column.py`, `test_subsurface_geometry.py`, `test_subsurface_lateral.py`, `test_subsurface_mesh.py`, `test_subsurface_run.py`, `test_feddes.py`, `test_deep_aquifer_initial_state.py`).

O principal teste numérico compara o fluxo explícito e o implícito no lençol freático.

| Caso | Fluxo | Trocas de sinal | Água transferida em 24 h vs. uma referência de 36 s |
|---|---|---:|---:|
| Solo arenoso, úmido, lençol a 15 cm de profundidade, passos de 1 h | Explícito | 2 | 53 % a mais |
| Idem | Implícito (padrão) | 0 | dentro de 0.1 % |

Com passo de 0.01 s, as duas formas concordam até $1.5 \times 10^{-5}$.

### Paridade Python-MATLAB {#python-to-matlab-parity}

A versão em MATLAB é verificada contra fixtures exportados do HydroPol2D-Python (`Validation/Groundwater/Layered` no repositório MATLAB). Os fixtures usam o fluxo explícito no lençol freático, porque o fluxo implícito ainda não foi portado.

| Script | O que verifica | Resultado registrado |
|---|---|---|
| `run_layered_kernel_parity.m` | Todos os kernels da coluna: geometria, atualização do lençol pelo MMF, drenagem, fluxo de Darcy, Feddes, bisseção do lençol compartilhado e avanço lateral | 193 verificações, pior caso $2.8 \times 10^{-16}$ |
| `run_layered_step_parity.m` | O passo vertical completo em camadas em uma grade em V de 2 × 2, com 4 cenários e 312 passos | 3 120 verificações, pior caso $2.1 \times 10^{-17}$ |
| `run_layered_vtilted_case.m` | Simulações do modelo completo na bacia em V: `local`, `lateral`, `feddes`, `legacy`, `deep`, `deep_legacy`, `deep_empty` | Executado a partir de uma cópia de `Examples/VTilted_Excel`; erro de volume do caso `lateral` de $-1.7 \times 10^{-10}$ m³ |
| `run_feddes_legacy_consistency.m` | O Feddes na ET padrão de três camadas é igual à ET de Feddes em camadas para o mesmo estado; o Feddes nunca retira mais que a regra sem estresse | verificação de consistência |
| `run_layered_mesh_case.m` | Malha Voronoi de 20 m na bacia em V com 2 HRUs: padrão, em camadas, em camadas + Feddes | todo passo fecha a massa dentro de $10^{-8}$ do volume de chuva |

`run_deep_aquifer_initial_state_validation.m` verifica o estado inicial profundo $S_0 = q_0 A \tau$ contra um fixture compartilhado com o HydroPol2D-Python. `Validation/Groundwater/run_groundwater_release_checks.m` roda todos esses scripts.

### Experimento gêmeo de calibração {#calibration-twin-experiment}

Um experimento gêmeo recuperou multiplicadores conhecidos da condutividade do solo e do regolito a partir de uma recessão sintética de 30 dias, com 0, 5 e 10 % de ruído. A configuração, os resultados e os limites estão na página [Calibração por Recessão das Águas Subterrâneas](../calibration/groundwater-recession#5-twin-experiments).

### O que a evidência em camadas não cobre {#what-the-layered-evidence-does-not-cover}

- O fluxo implícito no lençol freático foi testado apenas em Python.
- Não há caso de campo. Os testes usam domínios sintéticos em V.
- Os problemas em aberto listados em [Limites Conhecidos](../theory/layered-subsurface#9-known-limits), incluindo a circulação no lençol freático, não são resolvidos por esses testes.

## O que esta validação sustenta {#what-this-validation-supports}

Em conjunto, esses casos sustentam a acumulação de recarga implementada, o agendador assíncrono, a elevação e o rebaixamento locais do lençol freático por meio de `S_y`, a ascensão capilar simples em camadas e a dinâmica lateral idealizada das águas subterrâneas em encostas.

Os testes da subsuperfície em camadas sustentam a implementação da coluna de solo sobre regolito e a concordância entre Python e MATLAB em casos controlados.

Eles não validam parâmetros regionais de aquíferos, escoamento de base em campo, bombeamento de águas subterrâneas, comportamento de aquíferos confinados nem calibração com poços observados.
