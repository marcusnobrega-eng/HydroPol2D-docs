---
title: Visao geral
---

# Configuracao do modelo

O HydroPol2D e configurado principalmente por `General_Data.xlsx`. Essa planilha seleciona o conjunto de processos, a familia de roteamento, os controles de tempo do groundwater, os arquivos de entrada e os diagnosticos opcionais.

As paginas de configuracao e teoria cumprem papeis diferentes:

- a teoria explica o que cada modulo faz;
- a configuracao explica quais controles publicos expõem esse comportamento.

## Logica atual de configuracao

A configuracao publica deve refletir o modelo implementado:

- armazenamento vadoso em camadas e acoplamento com groundwater sao o caminho padrao quando o groundwater esta ativo;
- a familia de roteamento inclui local inertial, full momentum, diffusive D4, kinematic D4 e cellular automata;
- apenas uma familia principal de roteamento deve estar ativa por simulacao.

## Capacidades e maturidade

| Capacidade | Principais controles publicos | Estado atual |
|---|---|---|
| Nucleo hidrologico | `flag_infiltration`, controles de ET, chuva e neve, tabelas de solo e LULC | Padrao + validado |
| Recarga subterranea em camadas e agendador assincrono | `flag_groundwater_modeling`, `flag_groundwater_async`, `groundwater_target_dt_min`, `groundwater_min_dt_min`, `groundwater_max_head_change_m`, `groundwater_courant` | Padrao + validado |
| Ascensao capilar | `flag_capillary_rise` | Opcional + validada em benchmarks controlados |
| Roteamento local inertial | `flag_inertial`, `flag_numerical_scheme` | Padrao + validado |
| Roteamento full momentum | `flag_full_momentum` | Opcional + validado em benchmarks controlados |
| Roteamento diffusive | `flag_diffusive` | Opcional + validado em benchmarks controlados |
| Roteamento kinematic | `flag_kinematic` | Opcional + validado em benchmarks controlados |
| Cellular automata | `flag_CA` | Opcional + validado para conservacao e bookkeeping |
| Instabilidade humana | `flag_human_instability` | Opcional + validada para os modos `1` e `3` |

## Principais dominios de configuracao

### 1. Controle de simulacao e forcantes

`General_Data.xlsx` define o tempo da simulacao, as forcantes de chuva e meteorologia, as condicoes de contorno de inflow e stage, a frequencia de saida e opcoes de execucao, como time step adaptativo ou GPU.

### 2. Selecao da familia de roteamento

A interface publica de roteamento inclui:

- `flag_inertial`
- `flag_full_momentum`
- `flag_diffusive`
- `flag_kinematic`
- `flag_CA`

Apenas uma dessas flags principais deve estar ativa em cada simulacao. O D8 existe como caminho secundario e nao deve ser documentado como uma familia teorica paralela.

### 3. Controles de groundwater

Quando o groundwater esta ativo, o HydroPol2D expoe comportamentos que precisam ser documentados de forma explicita:

- atualizacoes assincronas do groundwater saturado;
- solucoes disparadas por variacao acumulada de carga;
- limite explicito de estabilidade para o time step do groundwater;
- ascensao capilar opcional;
- fluxo lateral de Boussinesq quando o baseflow esta ativo.

### 4. Diagnosticos de risco e qualidade da agua

Modulos opcionais, como qualidade da agua e instabilidade humana, possuem flags e parametros proprios. Para instabilidade humana, a documentacao publica deve refletir que:

- o modo `1` esta implementado;
- o modo `3` esta implementado;
- o modo `2` nao esta implementado.

## Leitura recomendada de uma configuracao

Em simulacoes publicas do HydroPol2D, deve ficar claro:

1. qual familia de roteamento esta ativa;
2. se o groundwater esta acoplado apenas localmente ou tambem lateralmente via Boussinesq;
3. se a ascensao capilar esta ativa;
4. se os diagnosticos de instabilidade humana ou qualidade da agua estao ativos.

Se essas quatro perguntas estiverem claras, a configuracao esta alinhada com a historia atual do modelo.
