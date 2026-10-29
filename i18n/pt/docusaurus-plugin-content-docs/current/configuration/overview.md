---
title: Visão geral
---

# Configuração do modelo

No modo Excel do MATLAB, um caso do HydroPol2D é uma única planilha, `HydroPol2D_Inputs.xlsx`. As suas abas de configurações selecionam o conjunto de processos, a família de roteamento, os controles das águas subterrâneas, os arquivos de entrada e os diagnósticos opcionais. As demais abas guardam as tabelas de classes e as séries temporais. Os casos antigos, com `General_Data.xlsx` e planilhas separadas, continuam rodando (veja [Rodar pelo Excel](../getting-started/excel-workflow#older-layout)). O HydroPol2D-Python lê as mesmas configurações do YAML do caso.

As páginas de configuração e teoria cumprem papéis diferentes:

- a teoria explica o que cada módulo faz;
- a configuração explica quais controles públicos expõem esse comportamento.

## Lógica atual de configuração

A configuração pública deve refletir o modelo implementado:

- armazenamento vadoso em camadas e acoplamento com groundwater são o caminho padrão quando o groundwater está ativo;
- a família de roteamento inclui local inertial, full momentum, diffusive D4, kinematic D4 e cellular automata;
- apenas uma família principal de roteamento deve estar ativa por simulação.

## Capacidades e maturidade

| Capacidade | Principais controles públicos | Estado atual |
|---|---|---|
| Núcleo hidrológico | `flag_infiltration`, controles de ET, chuva e neve, tabelas de solo e LULC | Padrão + validado |
| Recarga subterrânea em camadas e agendador assíncrono | `flag_groundwater_modeling`, `groundwater_target_dt_min`, `groundwater_min_dt_min`, `groundwater_max_head_change_m`, `groundwater_courant` | Padrão + validado |
| Ascensão capilar | `flag_capillary_rise` | Opcional + validada em benchmarks controlados |
| Subsuperfície em camadas | `flag_layered_subsurface`, `flag_implicit_water_table_flux` | Opcional + testes controlados e paridade Python-MATLAB |
| Estresse hídrico radicular de Feddes | `flag_feddes` | Opcional + testes de consistência |
| Aquífero profundo | `flag_deep_aquifer` | Opcional + testes do estado inicial com fixture |
| Roteamento local inertial | `flag_inertial`, `flag_numerical_scheme` | Padrão + validado |
| Roteamento full momentum | `flag_full_momentum` | Opcional + validado em benchmarks controlados |
| Roteamento diffusive | `flag_diffusive` | Opcional + validado em benchmarks controlados |
| Roteamento kinematic | `flag_kinematic` | Opcional + validado em benchmarks controlados |
| Cellular automata | `flag_CA` | Opcional + validado para conservação e bookkeeping |
| Instabilidade humana | `flag_human_instability` | Opcional + validada para os modos `1` e `3` |

## Principais domínios de configuração

### 1. Controle de simulação e forçantes

As abas Run control, Rain and ET, Design storm e Surface flow definem o tempo da simulação, as forçantes de chuva e meteorológicas, os contornos de vazão de entrada e de nível, a frequência de saída e opções de execução, como o passo de tempo adaptativo ou a GPU. Todas as configurações estão listadas em [Configurações da Planilha do Caso](./general_data).

### 2. Seleção da família de roteamento

A interface pública de roteamento inclui:

- `flag_inertial`
- `flag_full_momentum`
- `flag_diffusive`
- `flag_kinematic`
- `flag_CA`

Apenas uma dessas flags principais deve estar ativa em cada simulação. O D8 existe como caminho secundário e não deve ser documentado como uma família teórica paralela.

### 3. Controles de groundwater

Quando o groundwater está ativo, o HydroPol2D expõe comportamentos que precisam ser documentados de forma explícita:

- atualizações assíncronas do groundwater saturado;
- soluções disparadas por variação acumulada de carga;
- limite explícito de estabilidade para o time step do groundwater;
- ascensão capilar opcional;
- fluxo lateral de Boussinesq quando o baseflow está ativo.

### 4. Diagnósticos de risco e qualidade da água

Módulos opcionais, como qualidade da água e instabilidade humana, possuem flags e parâmetros próprios. Para instabilidade humana, a documentação pública deve refletir que:

- o modo `1` está implementado;
- o modo `3` está implementado;
- o modo `2` não está implementado.

## Leitura recomendada de uma configuração

Em simulações públicas do HydroPol2D, deve ficar claro:

1. qual família de roteamento está ativa;
2. se o groundwater está acoplado apenas localmente ou também lateralmente via Boussinesq;
3. se a ascensão capilar está ativa;
4. se os diagnósticos de instabilidade humana ou qualidade da água estão ativos.

Se essas quatro perguntas estiverem claras, a configuração está alinhada com a história atual do modelo.
