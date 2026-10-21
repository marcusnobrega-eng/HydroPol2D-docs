---
title: Flags do Modelo
---

# Flags do Modelo

O HydroPol2D é controlado por chaves binárias e categóricas. Na planilha do caso, `HydroPol2D_Inputs.xlsx`, cada chave fica no topo do bloco que controla, na aba do seu processo, e o bloco fica em cinza enquanto a chave vale 0. Não existe uma aba `Flags` separada. A página [Configurações da Planilha do Caso](./general_data) lista todos os blocos com as suas configurações.

Os nomes das abas e dos blocos ficam em inglês, como aparecem na planilha.

Esta página lista todas as chaves por aba e, em seguida, as regras para combiná-las.

---

## Chaves por aba {#switches-by-tab}

Tabelas geradas a partir do catálogo da planilha (`tools/workbook_builder/input_catalog.yaml` no repositório MATLAB). As descrições são as notas da planilha.

### Run control {#switches-run-control}

| Chave | Bloco | Valores | Padrão | Descrição |
|---|---|---|---|---|
| `flag_adaptive_timestepping` | Surface time step | 0 / 1 | obrigatório | Atualiza o passo de tempo do roteamento superficial a partir dos limites de estabilidade durante a simulação. Mantenha ativo na maioria das simulações dinâmicas. |
| `flag_GPU` | Computing | 0 / 1 | obrigatório | Roda os arrays e cálculos suportados em uma GPU compatível com o MATLAB. Deixe desativado quando não houver GPU compatível. |
| `flag_single` | Computing | 0 / 1 | obrigatório | Armazena os arrays numéricos suportados em precisão simples para reduzir o uso de memória. Mantenha desativado quando for necessária a máxima precisão numérica. |
| `flag_export_maps` | Outputs and display | 0 / 1 | obrigatório | Exporta as saídas espaciais programadas, como a profundidade de inundação e mapas relacionados. |
| `flag_export_groundwater_maps` | Outputs and display | 0 / 1 | `0` | Exporta os rasters programados de profundidade do lençol freático quando a modelagem de águas subterrâneas está ativa. |
| `flag_wse` | Outputs and display | 0 / 1 | obrigatório | flag_wse controla a saída de mapas de elevação da superfície da água (0 desativa, 1 ativa). O mapa usa a elevação do DEM mais a profundidade simulada onde a profundidade excede depth_wse. |
| `flag_waterbalance` | Outputs and display | 0 / 1 | obrigatório | Grava diagnósticos do balanço hídrico durante a simulação. Ative para validação e para verificações de rotina do modelo. |
| `flag_dashboard` | Outputs and display | 0 / 1 | obrigatório | Cria as saídas configuradas do painel durante a simulação. |
| `flag_elapsed_time` | Outputs and display | 0 / 1 | obrigatório | Imprime ou registra o tempo computacional decorrido da simulação. |
| `flag_warmup` | Warm start | 0 / 1 | obrigatório | Inicia a simulação a partir do estado de aquecimento configurado, em vez dos rasters padrão de estado inicial. |
| `flag_timestep` | Advanced (keep the defaults unless you know why) | 0 / 1 | obrigatório | Seleciona o tratamento completo de estabilidade do passo de tempo nos solvers de roteamento suportados. Use o padrão validado, a menos que esteja testando uma formulação numérica específica. |

### Soil and groundwater {#switches-soil-and-groundwater}

| Chave | Bloco | Valores | Padrão | Descrição |
|---|---|---|---|---|
| `flag_infiltration` | Infiltration and evapotranspiration | 0 / 1 | obrigatório | Ativa a infiltração e o balanço de água do solo em camadas. Desativá-la também desativa a evapotranspiração no modelo atual. |
| `flag_ETP` | Infiltration and evapotranspiration | 0 / 1 | obrigatório | Ativa a evapotranspiração. O HydroPol2D usa as entradas meteorológicas ou os mapas configurados para calcular a evaporação e a transpiração. |
| `flag_abstraction` | Infiltration and evapotranspiration | 0 / 1 | obrigatório | Ativa a interceptação no dossel e a abstração inicial. |
| `flag_capillary_rise` | Infiltration and evapotranspiration | 0 / 1 | `1` | Ativa um fluxo ascendente limitado das águas subterrâneas rasas para a zona de transmissão ou para a zona radicular quando há déficit de armazenamento. |
| `flag_snow_modeling` | Infiltration and evapotranspiration | 0 / 1 | obrigatório | Ativa a partição da precipitação, o armazenamento de neve, o derretimento, a sublimação e a compactação, com as colunas de neve da aba Land use classes. |
| `flag_spatial_albedo` | Infiltration and evapotranspiration | 0 / 1 | obrigatório | Usa o raster de albedo fornecido em vez do albedo escalar padrão. |
| `flag_neglect_infiltration_river` | Infiltration and evapotranspiration | 0 / 1 | obrigatório | Zera a infiltração e a abstração inicial nas células identificadas como rio. |
| `flag_groundwater_modeling` | Groundwater | 0 / 1 | obrigatório | Ativa o módulo acoplado de recarga pelo solo em camadas e de águas subterrâneas saturadas. |
| `flag_baseflow` | Groundwater | 0 / 1 | obrigatório | Ativa a contribuição de escoamento de base configurada onde o fluxo de trabalho hidrológico selecionado a aceita. |
| `flag_prescribed_recharge` | Groundwater | 0 / 1 | `0` | Substitui a recarga calculada para o lençol freático pela série de Prescribed_Recharge_Timeseries_File (aba Input maps). Padrão 0. |
| `flag_layered_subsurface` | Layered subsurface: column | 0 / 1 | `0` | Ativa a subsuperfície em camadas, com três camadas de solo sobre camadas de rocha alterada até o leito rochoso e um lençol freático por célula (regras de Miguez-Macho et al., 2007). As configurações ficam nos blocos da subsuperfície em camadas da aba Soil and groundwater, e os rasters opcionais ficam logo abaixo dos valores que substituem. Requer flag_groundwater_modeling = 1. |
| `flag_implicit_water_table_flux` | Layered subsurface: soil and numerics | 0 / 1 | `1` | Resolve de forma implícita o fluxo de Darcy entre o solo e o lençol freático na subsuperfície em camadas (um passo de Euler implícito linearizado por célula). O valor 1 (padrão) mantém a precisão em passos de tempo longos quando o lençol freático é raso. O valor 0 usa o fluxo explícito, que exige passos curtos nessa situação. Usado apenas com flag_layered_subsurface = 1. |
| `flag_feddes` | Feddes root-water stress | 0 / 1 | `0` | Ativa o estresse hídrico radicular de Feddes, em que a transpiração de cada camada de solo é reduzida conforme a sua carga de sucção. As cargas ficam neste bloco. Funciona com o esquema de solo em camadas e com o legado. |
| `flag_deep_aquifer` | Deep aquifer | 0 / 1 | `0` | Ativa o aquífero profundo. A fração deep_recharge_fraction da recarga do lençol freático vai para um reservatório linear por sub-bacia e volta à superfície depois de deep_aquifer_tau_days. Requer DeepAquiferSubbasins_path e DeepAquiferChannelWeight_path. |

### Surface flow {#switches-surface-flow}

| Chave | Bloco | Valores | Padrão | Descrição |
|---|---|---|---|---|
| `flag_inertial` | Routing scheme | 0 / 1 | obrigatório | Seleciona o solver hidrodinâmico inercial local. É o solver de roteamento exigido pela extensão de canal subgrade de Neal (2012). |
| `flag_CA` | Routing scheme | 0 / 1 | obrigatório | Seleciona a opção de roteamento hidrodinâmico por autômatos celulares. Não a ative junto com o roteamento inercial local ou de momento completo. |
| `flag_kinematic` | Routing scheme | 0 / 1 | obrigatório | Seleciona a alternativa de roteamento por onda cinemática. Não a combine com o roteamento inercial local, de momento completo ou por autômatos celulares. |
| `flag_diffusive` | Routing scheme | 0 / 1 | obrigatório | Seleciona a alternativa de roteamento por onda difusiva. Não a combine com o roteamento inercial local, de momento completo ou por autômatos celulares. |
| `flag_D8` | Routing scheme | 0 / 1 | obrigatório | Ativa o roteamento no terreno e o pré-processamento da drenagem D8 onde se aplicam. O roteamento inercial local continua baseado em faces. |
| `flag_boundary` | Outlets and boundaries | 0 / 1 | obrigatório | Ativa o tratamento configurado do contorno aberto ou do perímetro. Defina com cuidado a máscara e a declividade da saída, porque esta configuração controla a retirada de água na borda do domínio. |
| `flag_critical` | Outlets and boundaries | 0 / 1 | obrigatório | Usa o tratamento de saída em fluxo crítico onde o solver de roteamento selecionado o suporta. É diferente da saída em fluxo normal selecionada com flag_outlet_type. |
| `flag_neal_channel` | River channel (sub-grid) | 0 / 1 | obrigatório | Ativa a extensão de Neal (2012), com canal retangular embutido e planície de inundação. Requer flag_inertial = 1, topologia raster estruturada e rasters válidos de largura e profundidade do rio. |
| `flag_river_rasters` | River channel (sub-grid) | 0 / 1 | obrigatório | Usa os rasters RiverWidths e RiverDepths fornecidos para definir a geometria do canal no modelo subgrade ativo. |
| `flag_resample` | Terrain treatment | 0 / 1 | obrigatório | Reamostra os rasters auxiliares para a grade do DEM durante o pré-processamento quando a grade deles difere da do DEM. |
| `flag_fill_DEM` | Terrain treatment | 0 / 1 | obrigatório | Preenche as depressões do terreno antes de derivar as direções de drenagem e a acumulação de fluxo. |
| `flag_smoothening` | Terrain treatment | 0 / 1 | obrigatório | Aplica a suavização restrita dos perfis dos cursos d'água durante o pré-processamento do DEM. Esta opção requer a Optimization Toolbox. |
| `flag_smooth_cells` | Terrain treatment | 0 / 1 | obrigatório | Aplica o tratamento configurado de suavização do DEM em nível de célula durante o pré-processamento. |
| `flag_trunk` | Terrain treatment | 0 / 1 | obrigatório | Usa a opção de processamento dos canais principais na preparação do terreno e da rede de drenagem. |
| `flag_reduce_DEM` | Terrain treatment | 0 / 1 | obrigatório | Aplica o rebaixamento configurado do DEM nos canais de rio durante o pré-processamento. |
| `flag_DTM` | Terrain treatment | 0 / 1 | obrigatório | Usa o caminho de processamento DTM na preparação do terreno quando os dados de entrada exigem esse fluxo de trabalho. |
| `flag_voronoi` | Unstructured mesh | 0 / 1 | `0` | Roda o modelo em uma malha Voronoi (não estruturada) preparada, em vez da grade raster. As opções da malha são lidas da aba Mesh. |
| `flag_voronoi_subgrid` | Unstructured mesh | 0 / 1 | obrigatório | Ativa as tabelas subgrade das faces (área de escoamento, perímetro molhado e fator de condução em função do nível) na malha Voronoi. Usado apenas com flag_voronoi = 1. O caminho da tabela é definido na aba Mesh. |
| `flag_inflow` | Inflows and structures | 0 / 1 | obrigatório | Aplica um ou mais hidrogramas de vazão prescritos nas coordenadas de entrada definidas na aba Inflow hydrographs. |
| `flag_stage_hydrograph` | Inflows and structures | 0 / 1 | obrigatório | Aplica um hidrograma prescrito de nível de água nos locais configurados de contorno de nível. |
| `flag_reservoir` | Inflows and structures | 0 / 1 | obrigatório | Ativa o módulo de reservatórios e estruturas de controle com as entradas de reservatório configuradas. |
| `flag_structured_lookup_subgrid` | Paused (keep at 0: setting 1 stops the run) | 0 / 1 | `0` | Ativa a formulação subgrade estruturada por tabela de consulta no modelo raster regular. Usa propriedades de células e faces dependentes do nível e não pode ser combinada com a subgrade de Neal nem com a de Voronoi. |

### Rain and ET {#switches-rain-and-et}

| Chave | Bloco | Valores | Padrão | Descrição |
|---|---|---|---|---|
| `flag_rainfall` | Rainfall source | 0 / 1 | obrigatório | Ativa a forçante de chuva. Use com uma única fonte de chuva selecionada, que pode ser uma série temporal concentrada, a interpolação de pluviômetros, uma sequência programada de rasters ou um produto de satélite. |
| `flag_spatial_rainfall` | Rainfall source | 0 / 1 | obrigatório | Interpola a chuva dos pluviômetros configurados para todas as células do modelo. São necessárias as coordenadas dos pluviômetros e uma série temporal comum de chuva. |
| `flag_input_rainfall_map` | Rainfall source | 0 / 1 | obrigatório | Lê da lista Rainfall maps uma sequência de rasters de chuva indexada no tempo. Não a ative junto com outra fonte de chuva espacial. |
| `flag_satellite_rainfall` | Rainfall source | 0 / 1 | obrigatório | Ativa o fluxo de trabalho de forçante de chuva por satélite. Ele prepara uma programação horária de chuva espacial e ativa a chuva automaticamente. |
| `flag_real_time_satellite_rainfall` | Rainfall source | 0 / 1 | obrigatório | Ativa o fluxo de trabalho de chuva por satélite em tempo real. Esta opção experimental cria uma programação curta e contínua de chuva espacial. |
| `flag_input_ETP_map` | Evapotranspiration source | 0 / 1 | obrigatório | Lê da aba Rain and ET as programações pareadas de rasters de transpiração e evaporação. As duas programações devem ter as mesmas entradas de tempo. |
| `flag_rainfall_multiple_runs` | Advanced (keep the defaults unless you know why) | 0 / 1 | obrigatório | Ativa o fluxo de trabalho legado de várias simulações de chuva. Deixe desativado para um único evento de chuva padrão. |

### Design storm {#switches-design-storm}

| Chave | Bloco | Valores | Padrão | Descrição |
|---|---|---|---|---|
| `flag_alternated_blocks` | Hyetograph | 0 / 1 | obrigatório | Gera a chuva de projeto configurada por blocos alternados, em vez de ler uma série temporal de chuva. |
| `flag_huff` | Hyetograph | 0 / 1 | obrigatório | Gera a chuva de projeto configurada por curvas de Huff, em vez de ler uma série temporal de chuva. |

### Water quality {#switches-water-quality}

| Chave | Bloco | Valores | Padrão | Descrição |
|---|---|---|---|---|
| `flag_waterquality` | Water quality | 0 / 1 | obrigatório | Ativa os cálculos de build-up, wash-off, transporte e saídas de poluentes. |
| `flag_WQ_Rasters` | Water quality | 0 / 1 | obrigatório | Usa os rasters espaciais dos coeficientes de qualidade da água B1, B2, W1 e W2 em vez dos coeficientes da tabela de cobertura da terra. |
| `flag_initial_buildup` | Water quality | 0 / 1 | obrigatório | Inicializa o build-up de qualidade da água com o período seco antecedente e as configurações de build-up definidos. |
| `flag_wq_model` | Advanced (keep the defaults unless you know why) | 0 / ... | obrigatório | Seleciona a formulação de qualidade da água. O valor 0 usa o modo de build-up e wash-off baseado em massa. Use outros valores apenas em configurações legadas suportadas. |

### Risk and gauges {#switches-risk-and-gauges}

| Chave | Bloco | Valores | Padrão | Descrição |
|---|---|---|---|---|
| `flag_human_instability` | Human instability | 0 / 1 / 3 | obrigatório | Calcula indicadores de instabilidade humana a partir da profundidade e da velocidade. O valor 0 desativa o cálculo, o valor 1 usa a classificação básica e o valor 3 ativa a classificação estendida. |
| `flag_obs_gauges` | Observation points | 0 / 1 | obrigatório | Exporta os valores modelados nas coordenadas dos postos de observação listados na tabela de postos. |

---

## Regras para combinar chaves {#rules-for-combining-switches}

- Apenas uma família principal de roteamento deve estar ativa por vez, entre `flag_full_momentum`, `flag_inertial`, `flag_diffusive`, `flag_kinematic` e `flag_CA`.
- Selecione no máximo uma formulação subgrade, entre canal de Neal, tabela de consulta estruturada e tabela de consulta Voronoi.
- `flag_voronoi = 1` seleciona a topologia da malha. `flag_voronoi_subgrid = 1` ativa, além disso, a hidráulica por tabela de consulta na malha Voronoi.
- `flag_D8` é um caminho de roteamento secundário e de escopo limitado, e não mais uma família de roteamento pronta para relatórios.
- `flag_numerical_scheme` (`1` Bates, `2` upwind, `3` centrado) vale apenas para a família inercial local.
- A neve precisa da forçante meteorológica interna, com `flag_ETP = 1` e `flag_input_ETP_map = 0`. Os parâmetros de neve são colunas da tabela de classes de uso da terra.
- `flag_implicit_water_table_flux` e as demais configurações da subsuperfície em camadas são lidas apenas com `flag_layered_subsurface = 1`.
- O modo `2` de instabilidade humana não está implementado. Use `1` ou `3`.

### Canal subgrade de Neal (2012) {#neal-2012-subgrid-model-configuration}

O modo de canal subgrade suportado segue [Neal et al. (2012)](https://doi.org/10.1029/2012WR012514). Use a combinação abaixo.

| Chave | Valor exigido |
|---|---:|
| `flag_inertial` | `1` |
| `flag_neal_channel` | `1` |
| `flag_structured_lookup_subgrid` | `0` |
| `flag_voronoi_subgrid` | `0` |
| `flag_voronoi` | `0` |
| `flag_full_momentum` | `0` |
| `flag_diffusive` | `0` |
| `flag_kinematic` | `0` |
| `flag_CA` | `0` |
| `flag_river_rasters` | `1` quando a geometria do canal é fornecida por rasters |

As células com canal ativo exigem `RiverWidths_path` e `RiverDepths_path`. A largura e a profundidade do canal devem ser positivas, e a largura do canal deve ser menor que a resolução da célula do modelo. O coeficiente de Manning do canal é a configuração `Manning` da aba Surface flow. A rugosidade do uso da terra fornece o coeficiente de Manning da planície de inundação.

O solver calcula separadamente as vazões do canal e da planície em cada face ortogonal e atualiza o armazenamento da célula em termos de volume. A formulação e a faixa de validação estão descritas em [Modelo Hidrodinâmico](../theory/hydrodynamic-model#115-neal-2012-subgrid-model) e em [Validação do modelo subgrade de Neal (2012)](../validation/neal-subgrid).

---

## Formato antigo {#older-layout}

Nos casos que usam `General_Data.xlsx`, as chaves são linhas da sua aba `Flags`, com o valor na coluna E. Nas planilhas distribuídas, `flag_deep_aquifer`, `flag_layered_subsurface`, `flag_feddes` e `flag_implicit_water_table_flux` ocupam as linhas 37 a 40. O modelo lê a aba `Flags` quando o caso a tem e, caso contrário, as chaves das abas de configurações.

- As chaves aposentadas `flag_data_source`, `flag_dam_break` e `flag_river_heigth_compensation` não são mais exigidas (padrão 0).
- `flag_subgrid` e `flag_overbanks` são derivadas das chaves do canal. Entradas antigas que ainda as definem são aceitas pela camada de migração, com aviso.
