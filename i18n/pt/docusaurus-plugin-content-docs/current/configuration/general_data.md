---
title: Configurações da Planilha do Caso
---

# Configurações da Planilha do Caso

Um caso MATLAB é uma única planilha, `HydroPol2D_Inputs.xlsx`. Esta página lista todas as configurações das suas oito abas de configurações. As demais abas estão descritas nas páginas abaixo.

- tabelas de classes (solo, uso da terra, instabilidade humana, malha, estruturas de controle) em [Tabelas de parâmetros](../inputs/parameter-tables);
- séries temporais (chuva, estações climatológicas, hidrogramas de entrada e de nível) em [Forçantes Opcionais](../inputs/optional-forcing);
- todas as chaves, reunidas em uma página, em [Flags do Modelo](./flags);
- como abrir, preencher e rodar um caso em [Rodar pelo Excel](../getting-started/excel-workflow).

Os nomes das abas e dos blocos ficam em inglês, como aparecem na planilha.

Casos antigos, com `General_Data.xlsx`, a sua aba `Flags` e planilhas separadas, continuam rodando. Veja [Formato antigo](#older-layout).

---

## A planilha em resumo {#the-workbook-at-a-glance}

| Grupo | Abas |
|---|---|
| Guia | Start here, com instruções de preenchimento, a legenda de cores e um link para cada aba |
| Configurações (8) | Run control, Input maps, Soil and groundwater, Surface flow, Rain and ET, Design storm, Water quality, Risk and gauges |
| Tabelas de classes (5) | Soil classes, Land use classes, Human instability, Mesh, Control structures |
| Séries (5) | Rain series, Rain gauges, Climate stations, Inflow hydrographs, Stage hydrographs |

`HydroPol2D_V115.m` lê `Input_Data_Sheets/HydroPol2D_Inputs.xlsx` por padrão. `HYDROPOL_INPUT_EXCEL_FILE` aponta para outra planilha.

---

## Como funciona uma aba de configurações {#how-a-settings-tab-works}

Cada configuração ocupa uma linha, com nome, variável, valor, unidade, padrão e condição de uso. Uma nota em cada valor explica o seu significado.

- **Blocos e chaves.** As configurações são agrupadas em blocos. Um bloco que pode ser desligado começa pela sua chave, e as suas linhas ficam em cinza enquanto a chave vale 0. Valores em cinza são ignorados. Não existe uma aba `Flags` separada.
- **Valores obrigatórios** são marcados com um asterisco vermelho. Um valor opcional vazio mantém o padrão ou a alternativa indicada na sua nota.
- **Blocos avançados** (cabeçalho cinza) guardam configurações legadas. Mantenha os padrões, a menos que haja um motivo claro para mudá-los.
- **Blocos pausados** (cabeçalho âmbar) guardam recursos pausados. Mantenha-os em 0, porque o valor 1 interrompe a simulação.
- **Caminhos** podem ser absolutos ou relativos à pasta da planilha.

---

## Referência das configurações {#settings-reference}

As tabelas abaixo são geradas a partir do catálogo que monta a planilha (`tools/workbook_builder/input_catalog.yaml` no repositório MATLAB) e, por isso, coincidem linha a linha com a planilha. As descrições são as notas da planilha.

### Run control {#tab-run-control}

Período de simulação, passo de tempo, desempenho e o que o modelo registra.

#### Simulation period {#simulation-period}

| Configuração | Variável | Unidade | Padrão | Usado quando | Descrição |
|---|---|---|---|---|---|
| Data e hora de início | `date_begin` | data | obrigatório | sempre | date_begin é a data e hora de início da simulação. Use a mesma referência de tempo das séries de chuva, evapotranspiração, vazão de entrada, nível e observação. |
| Data e hora de término | `date_end` | data | obrigatório | sempre | date_end é a data e hora de término da simulação. Deve ser posterior a date_begin. Valores de forçantes fora desse intervalo não entram na simulação. |

#### Surface time step {#surface-time-step}

| Configuração | Variável | Unidade | Padrão | Usado quando | Descrição |
|---|---|---|---|---|---|
| Passo de tempo inicial | `time_step_model` | s | obrigatório | sempre | time_step_model é o passo de tempo nominal do modelo de superfície, em segundos. Ele inicia o laço de roteamento. O passo de tempo adaptativo pode substituí-lo por um valor estável entre min_time_step e max_time_step. |
| Passo de tempo mínimo | `min_time_step` | s | obrigatório | sempre | min_time_step é o menor passo de tempo permitido no roteamento superficial, em segundos. Use um valor positivo, pequeno o bastante para resolver molhamento rápido, escoamento raso e terreno íngreme. |
| Passo de tempo máximo | `max_time_step` | s | obrigatório | sempre | max_time_step é o maior passo de tempo permitido no roteamento superficial, em segundos. Ele limita o passo nos períodos de variação lenta e deve ser maior ou igual a min_time_step. |
| Fator de Courant, inferior | `alfa_min` | - | obrigatório | sempre | alfa_min é o coeficiente de segurança de Courant inferior usado quando o HydroPol2D calcula um passo de tempo estável para o roteamento superficial. Valores menores são mais conservadores e costumam aumentar o tempo de execução. |
| Passo de tempo adaptativo | `flag_adaptive_timestepping` | 0 / 1 | obrigatório | sempre | Atualiza o passo de tempo do roteamento superficial a partir dos limites de estabilidade durante a simulação. Mantenha ativo na maioria das simulações dinâmicas. |

#### Computing {#computing}

| Configuração | Variável | Unidade | Padrão | Usado quando | Descrição |
|---|---|---|---|---|---|
| Rodar na GPU | `flag_GPU` | 0 / 1 | obrigatório | sempre | Roda os arrays e cálculos suportados em uma GPU compatível com o MATLAB. Deixe desativado quando não houver GPU compatível. |
| Precisão simples | `flag_single` | 0 / 1 | obrigatório | sempre | Armazena os arrays numéricos suportados em precisão simples para reduzir o uso de memória. Mantenha desativado quando for necessária a máxima precisão numérica. |

#### Recording intervals {#recording-intervals}

| Configuração | Variável | Unidade | Padrão | Usado quando | Descrição |
|---|---|---|---|---|---|
| Salvar mapas a cada | `record_time_maps` | min | obrigatório | sempre | record_time_maps é o intervalo, em minutos, entre os mapas espaciais salvos. Um intervalo menor aumenta o detalhe das saídas e o uso de disco, sem mudar a física da simulação. |
| Salvar hidrogramas a cada | `record_time_hydrographs` | min | obrigatório | sempre | record_time_hydrographs é o intervalo, em minutos, entre os registros dos hidrogramas de saída, de entrada e dos postos. Escolha um intervalo que resolva a resposta esperada do hidrograma. |
| Salvar mapas de chuva a cada | `record_time_spatial_rainfall` | min | obrigatório | chuva espacial ativa | record_time_spatial_rainfall é o intervalo, em minutos, usado para salvar ou agregar a informação espacial de chuva. Para chuva em raster, deve ser compatível com o intervalo de saída dos mapas. |
| Salvar mapas de ET a cada | `record_time_spatial_ETP` | min | obrigatório | ET ativa | record_time_spatial_ETP é o intervalo, em minutos, entre os produtos espaciais salvos de evaporação e transpiração. Intervalos menores geram arquivos mais detalhados e exigem mais armazenamento. |

#### Outputs and display {#outputs-and-display}

| Configuração | Variável | Unidade | Padrão | Usado quando | Descrição |
|---|---|---|---|---|---|
| Exportar mapas | `flag_export_maps` | 0 / 1 | obrigatório | sempre | Exporta as saídas espaciais programadas, como a profundidade de inundação e mapas relacionados. |
| Exportar mapas de águas subterrâneas | `flag_export_groundwater_maps` | 0 / 1 | `0` | águas subterrâneas ativas | Exporta os rasters programados de profundidade do lençol freático quando a modelagem de águas subterrâneas está ativa. |
| Mapas de elevação da superfície da água | `flag_wse` | 0 / 1 | obrigatório | sempre | flag_wse controla a saída de mapas de elevação da superfície da água (0 desativa, 1 ativa). O mapa usa a elevação do DEM mais a profundidade simulada onde a profundidade excede depth_wse. |
| Profundidade mínima nesses mapas | `depth_wse` | m | obrigatório | mapas de superfície da água ativos | depth_wse é a profundidade mínima de água, em metros, usada nos mapas de elevação da superfície da água. Evita informar uma elevação da superfície da água onde a célula está, na prática, seca. |
| Relatório do balanço hídrico | `flag_waterbalance` | 0 / 1 | obrigatório | sempre | Grava diagnósticos do balanço hídrico durante a simulação. Ative para validação e para verificações de rotina do modelo. |
| Painel em tempo real | `flag_dashboard` | 0 / 1 | obrigatório | sempre | Cria as saídas configuradas do painel durante a simulação. |
| Mostrar o tempo decorrido | `flag_elapsed_time` | 0 / 1 | obrigatório | sempre | Imprime ou registra o tempo computacional decorrido da simulação. |

#### Warm start {#warm-start}

| Configuração | Variável | Unidade | Padrão | Usado quando | Descrição |
|---|---|---|---|---|---|
| Partir de um estado de aquecimento | `flag_warmup` | 0 / 1 | obrigatório | sempre | Inicia a simulação a partir do estado de aquecimento configurado, em vez dos rasters padrão de estado inicial. |

#### Advanced (keep the defaults unless you know why) {#advanced-keep-the-defaults-unless-you-know-why}

| Configuração | Variável | Unidade | Padrão | Usado quando | Descrição |
|---|---|---|---|---|---|
| Fator de Courant, superior | `alfa_max` | - | obrigatório | sempre | alfa_max é o coeficiente superior do passo de tempo adaptativo, mantido para configurações compatíveis de controle de tempo. Mantenha-o positivo e não menor que alfa_min. Os cálculos atuais de estabilidade do roteamento usam alfa_min para o passo candidato conservador. |
| Incremento de atualização do passo de tempo | `time_step_change` | s | obrigatório | sempre | time_step_change é o incremento de tempo positivo, em segundos, usado no controle da atualização do passo de tempo e no alinhamento dos diagnósticos. Não é o intervalo de atualização das águas subterrâneas. |
| Verificação completa da estabilidade do passo | `flag_timestep` | 0 / 1 | obrigatório | sempre | Seleciona o tratamento completo de estabilidade do passo de tempo nos solvers de roteamento suportados. Use o padrão validado, a menos que esteja testando uma formulação numérica específica. |

### Input maps {#tab-input-maps}

Caminhos dos mapas GeoTIFF. Deixe vazios os mapas opcionais para usar as tabelas de classes ou os escalares.

#### Required maps {#required-maps}

| Configuração | Variável | Unidade | Padrão | Usado quando | Descrição |
|---|---|---|---|---|---|
| Elevação do terreno (DEM) | `DEM_path` | m | obrigatório | sempre | DEM_path é o caminho obrigatório do GeoTIFF de elevação do terreno, com elevações em metros. Define o domínio do modelo, a geometria da grade e os gradientes topográficos. |
| Classes de uso e cobertura da terra | `LULC_path` | classe | obrigatório | sempre | LULC_path é o GeoTIFF categórico obrigatório de uso e cobertura da terra. Os códigos de classe do raster são associados à aba Land use classes. Códigos sem correspondência recebem a alternativa documentada, ponderada pela área. |
| Classes de solo | `SOIL_path` | classe | obrigatório | sempre | SOIL_path é o GeoTIFF categórico obrigatório de classes de solo. Os códigos de classe do raster são associados à aba Soil classes. Códigos sem correspondência recebem a alternativa documentada, ponderada pela área. |

#### Land surface {#land-surface}

| Configuração | Variável | Unidade | Padrão | Usado quando | Descrição |
|---|---|---|---|---|---|
| Albedo | `Albedo_path` | 0 a 1 | vazio | albedo espacial ativo | Albedo_path é um raster opcional de albedo da superfície, de 0 a 1. É usado apenas quando o albedo espacial está ativo no cálculo da evapotranspiração por balanço de energia. |
| Índice de área foliar | `LAI_path` | m2/m2 | vazio | interceptação ativa | LAI_path é um raster opcional de índice de área foliar, em m2 de área foliar por m2 de terreno. É usado pela interceptação no dossel e pela evapotranspiração ligada à vegetação quando as chaves correspondentes estão ativas. |
| Fração impermeável | `ImperviousFraction_path` | 0 a 1 | vazio | opcional | ImperviousFraction_path é um raster opcional da fração de cobertura impermeável, de 0 a 1. Refina a infiltração dentro de uma célula. Valores fora desse intervalo não têm significado físico. |

#### Rivers and terrain {#rivers-and-terrain}

| Configuração | Variável | Unidade | Padrão | Usado quando | Descrição |
|---|---|---|---|---|---|
| Largura do rio | `RiverWidths_path` | m | vazio | canal subgrade com mapas de rio | RiverWidths_path é um GeoTIFF opcional de largura do rio, em metros. É obrigatório no modelo de canal embutido de Neal (2012) quando flag_subgrid e flag_river_rasters estão ativas. As larguras válidas do canal embutido devem ser menores que o tamanho da célula grosseira. |
| Profundidade do rio | `RiverDepths_path` | m | vazio | canal subgrade com mapas de rio | RiverDepths_path é um GeoTIFF opcional de profundidade do rio, em metros. Forma par com RiverWidths_path no modelo de canal embutido ativo e deve ser positivo onde houver canal. |

#### Initial states {#initial-states}

| Configuração | Variável | Unidade | Padrão | Usado quando | Descrição |
|---|---|---|---|---|---|
| Profundidade inicial da água na superfície | `Warmup_Depth_path` | m | vazio | partida a quente ativa | Warmup_Depth_path é um GeoTIFF opcional da profundidade inicial da água na superfície, em metros. É lido apenas quando flag_warmup está ativa e inicializa o armazenamento superficial antes do roteamento. |
| Água inicial no solo | `Initial_Soil_Moisture_path` | ver nota | vazio | partida a quente ativa | Initial_Soil_Moisture_path é um GeoTIFF opcional do armazenamento inicial de água no solo. Apesar do nome herdado, os valores são interpretados como armazenamento acima da umidade residual, em mm, e não como conteúdo volumétrico de água. É lido com flag_warmup. |
| Elevação inicial do lençol freático | `GW_table_path` | m | vazio | águas subterrâneas ativas | GW_table_path é um GeoTIFF opcional da elevação inicial do lençol freático, em metros, no mesmo datum vertical do DEM. É lido quando as águas subterrâneas ou o escoamento de base estão ativos e é mantido abaixo da superfície do terreno. |
| Equivalente de água da neve inicial | `Initial_SWE_path` | mm | vazio | neve ativa | Initial_SWE_path é um GeoTIFF opcional do equivalente de água da neve inicial, em mm de equivalente de água. É lido apenas quando a modelagem de neve está ativa. Valores negativos são inválidos, e células sem dados usam a condição padrão sem neve. |
| Profundidade inicial da neve | `Initial_Snow_Depth_path` | mm | vazio | neve ativa | Initial_Snow_Depth_path é um GeoTIFF opcional da profundidade inicial da neve, em mm. É lido apenas quando a modelagem de neve está ativa. Quando combinado com o SWE, o modelo verifica a coerência física dos dois e deriva a densidade. |

#### Soil-property maps (override the SOIL classes) {#soil-property-maps-override-the-soil-classes}

| Configuração | Variável | Unidade | Padrão | Usado quando | Descrição |
|---|---|---|---|---|---|
| theta_s do solo | `ThetaS_path` | m3/m3 | vazio | opcional | ThetaS_path é um GeoTIFF opcional do conteúdo de água na saturação do solo, theta_s, em m3/m3. Substitui o valor de SOIL_parameters de cada classe onde for finito (nodata mantém o valor da classe), em todas as camadas de solo. |
| theta_r do solo | `ThetaR_path` | m3/m3 | vazio | opcional | ThetaR_path é um GeoTIFF opcional do conteúdo de água residual do solo, theta_r, em m3/m3. Substitui o valor de SOIL_parameters de cada classe onde for finito (nodata mantém o valor da classe). |
| alfa de van Genuchten do solo | `AlphaVG_path` | 1/m | vazio | opcional | AlphaVG_path é um GeoTIFF opcional do alfa de van Genuchten do solo, em 1/m. Substitui o valor de SOIL_parameters de cada classe onde for finito (nodata mantém o valor da classe). |
| n de van Genuchten do solo | `NVG_path` | - | vazio | opcional | NVG_path é um GeoTIFF opcional do n de van Genuchten do solo (maior que 1, adimensional). Substitui o valor de SOIL_parameters de cada classe onde for finito (nodata mantém o valor da classe). |
| Ksat, camada superficial | `KsatNearSurface_path` | mm/h | vazio | opcional | KsatNearSurface_path é um GeoTIFF opcional da condutividade hidráulica saturada da camada superficial do solo, em mm/h. Substitui ksat x Ks_multiplier_near_surface de cada classe de SOIL onde for finito (nodata mantém o valor da classe). |
| Ksat, camada da zona radicular | `KsatRootZone_path` | mm/h | vazio | opcional | KsatRootZone_path é um GeoTIFF opcional da condutividade hidráulica saturada da camada de solo da zona radicular, em mm/h. Substitui ksat x Ks_multiplier_root_zone de cada classe de SOIL onde for finito (nodata mantém o valor da classe). |
| Ksat, camada de transmissão | `KsatTransmission_path` | mm/h | vazio | opcional | KsatTransmission_path é um GeoTIFF opcional da condutividade hidráulica saturada da camada de solo de transmissão, em mm/h. Substitui ksat x Ks_multiplier_transmission de cada classe de SOIL onde for finito (nodata mantém o valor da classe). |
| Ksat do aquífero (kgsat) | `GroundwaterKsat_path` | mm/h | vazio | opcional | GroundwaterKsat_path é um GeoTIFF opcional da condutividade horizontal do aquífero, kgsat, em mm/h. Substitui o kgsat de SOIL_parameters de cada classe onde for finito. Na subsuperfície em camadas, é a alternativa para o Kh da rocha quando regolith_ksat_h_mm_h e RegolithKsatH_path estão vazios. |
| Rendimento específico do aquífero | `SpecificYield_path` | - | vazio | esquema legado de águas subterrâneas | SpecificYield_path é um GeoTIFF opcional do rendimento específico do aquífero, Sy (adimensional), para o esquema legado de águas subterrâneas. Substitui o Sy de SOIL_parameters de cada classe onde for finito. Não é usado pela subsuperfície em camadas, em que Sy vem das curvas de retenção (ou de regolith_specific_yield). |

#### Water-quality maps {#water-quality-maps}

| Configuração | Variável | Unidade | Padrão | Usado quando | Descrição |
|---|---|---|---|---|---|
| Massa inicial de poluente | `Initial_Buildup_path` | kg/célula | vazio | build-up inicial ativo | Initial_Buildup_path é um GeoTIFF opcional da massa de poluente, em kg por célula. É lido apenas quando flag_initial_buildup e o módulo de qualidade da água estão ativos. |
| Assíntota de build-up C1 | `B1_path` | ver nota | vazio | qualidade da água com mapas | B1_path é um caminho opcional de GeoTIFF para a assíntota espacial de build-up C1. É lido apenas quando a qualidade da água e as entradas raster de qualidade da água estão ativas. Use valores e unidades coerentes com o parâmetro C1 de LULC. |
| Taxa de build-up C2 | `B2_path` | ver nota | vazio | qualidade da água com mapas | B2_path é um caminho opcional de GeoTIFF para o parâmetro espacial C2 da taxa de build-up. É lido apenas quando a qualidade da água e as entradas raster de qualidade da água estão ativas. |
| Coeficiente de wash-off C3 | `W1_path` | ver nota | vazio | qualidade da água com mapas | W1_path é um caminho opcional de GeoTIFF para o coeficiente espacial de wash-off C3. É lido apenas quando a qualidade da água e as entradas raster de qualidade da água estão ativas. |
| Expoente de wash-off C4 | `W2_path` | ver nota | vazio | qualidade da água com mapas | W2_path é um caminho opcional de GeoTIFF para o expoente espacial de wash-off C4. É lido apenas quando a qualidade da água e as entradas raster de qualidade da água estão ativas. |

### Soil and groundwater {#tab-soil-and-groundwater}

Infiltração, evapotranspiração, águas subterrâneas, subsuperfície em camadas e aquífero profundo. Cada mapa fica logo abaixo do valor que ele substitui.

#### Infiltration and evapotranspiration {#infiltration-and-evapotranspiration}

| Configuração | Variável | Unidade | Padrão | Usado quando | Descrição |
|---|---|---|---|---|---|
| Infiltração | `flag_infiltration` | 0 / 1 | obrigatório | sempre | Ativa a infiltração e o balanço de água do solo em camadas. Desativá-la também desativa a evapotranspiração no modelo atual. |
| Evapotranspiração | `flag_ETP` | 0 / 1 | obrigatório | sempre | Ativa a evapotranspiração. O HydroPol2D usa as entradas meteorológicas ou os mapas configurados para calcular a evaporação e a transpiração. |
| Interceptação no dossel | `flag_abstraction` | 0 / 1 | obrigatório | sempre | Ativa a interceptação no dossel e a abstração inicial. |
| Ascensão capilar | `flag_capillary_rise` | 0 / 1 | `1` | águas subterrâneas ativas | Ativa um fluxo ascendente limitado das águas subterrâneas rasas para a zona de transmissão ou para a zona radicular quando há déficit de armazenamento. |
| Neve | `flag_snow_modeling` | 0 / 1 | obrigatório | sempre | Ativa a partição da precipitação, o armazenamento de neve, o derretimento, a sublimação e a compactação, com as colunas de neve da aba Land use classes. |
| Albedo a partir de um mapa | `flag_spatial_albedo` | 0 / 1 | obrigatório | neve ou ET ativas | Usa o raster de albedo fornecido em vez do albedo escalar padrão. |
| Sem infiltração nas células de rio | `flag_neglect_infiltration_river` | 0 / 1 | obrigatório | infiltração ativa | Zera a infiltração e a abstração inicial nas células identificadas como rio. |

#### Groundwater {#groundwater}

Chave: `flag_groundwater_modeling`. O restante do bloco fica em cinza enquanto ela vale 0.

| Configuração | Variável | Unidade | Padrão | Usado quando | Descrição |
|---|---|---|---|---|---|
| Águas subterrâneas | `flag_groundwater_modeling` | 0 / 1 | obrigatório | chave deste bloco | Ativa o módulo acoplado de recarga pelo solo em camadas e de águas subterrâneas saturadas. |
| Fluxo lateral das águas subterrâneas | `flag_baseflow` | 0 / 1 | obrigatório | águas subterrâneas ativas | Ativa a contribuição de escoamento de base configurada onde o fluxo de trabalho hidrológico selecionado a aceita. |
| Mapa da profundidade até o leito rochoso | `DTB_path` | m | vazio | esquema legado: obrigatório; em camadas: opcional | DTB_path é um GeoTIFF opcional da PROFUNDIDADE ATÉ O LEITO ROCHOSO, em metros abaixo da superfície do terreno. No esquema legado de águas subterrâneas, é a profundidade do solo, e o aquífero fica dentro dela. Na subsuperfície em camadas, é o fundo de toda a coluna (solo mais rocha alterada), e a espessura do solo é definida à parte por subsurface_soil_base_depth_m ou SoilBaseDepth_path. Obrigatório no esquema legado. Opcional com flag_layered_subsurface = 1, caso em que um DTB_path vazio recorre a subsurface_depth_to_bedrock_m e, depois, ao DTB (m) de cada classe de solo da aba Soil classes. |
| Mapa de carga fixa das águas subterrâneas | `GW_Dirichlet_Head_path` | m | vazio | águas subterrâneas ativas | GW_Dirichlet_Head_path é um GeoTIFF opcional da elevação prescrita da carga das águas subterrâneas, em metros. As células finitas do raster definem o contorno de Dirichlet das águas subterrâneas. Células sem dados ficam livres. |
| Série de recarga prescrita | `flag_prescribed_recharge` | 0 / 1 | `0` | águas subterrâneas ativas | Substitui a recarga calculada para o lençol freático pela série de Prescribed_Recharge_Timeseries_File (aba Input maps). Padrão 0. |
| Arquivo de recarga prescrita | `Prescribed_Recharge_Timeseries_File` | arquivo | vazio | recarga prescrita ativa | Prescribed_Recharge_Timeseries_File é um arquivo opcional com uma série temporal de recarga que substitui a recarga calculada para o lençol freático. É lido apenas quando flag_prescribed_recharge = 1. |
| Fator de Courant das águas subterrâneas | `groundwater_courant` | - | `0.25` | fluxo lateral ativo | groundwater_courant é o fator de segurança adimensional que limita o passo de tempo das águas subterrâneas de Boussinesq. Use um valor maior que zero e no máximo igual a um. Valores menores melhoram a estabilidade, ao custo de mais atualizações. |
| Tolerância relativa do relógio lateral | `groundwater_relative_tolerance` | - | `0.001` | fluxo lateral ativo | groundwater_relative_tolerance é a variação relativa do armazenamento das águas subterrâneas que dispara a próxima atualização lateral das águas subterrâneas (o relógio lateral). Valores menores atualizam com mais frequência e custam mais. Padrão 0.001. |
| Tolerância de carga do relógio lateral | `groundwater_head_tolerance_m` | m | `0.001` | fluxo lateral ativo | groundwater_head_tolerance_m é a variação do lençol freático, em metros, que dispara a próxima atualização lateral das águas subterrâneas (o relógio lateral). Valores menores atualizam com mais frequência e custam mais. Padrão 0.001 m. |
| Espessura do leito do rio | `riverbed_thickness_m` | m | `0.5` | águas subterrâneas ativas | riverbed_thickness_m é a espessura do leito do rio, em metros, usada na troca rio-aquífero, com condutância = Ksat do leito x área do leito / espessura. Padrão 0.5 m. |

#### Layered subsurface: column {#layered-subsurface-column}

Chave: `flag_layered_subsurface`. O restante do bloco fica em cinza enquanto ela vale 0.

| Configuração | Variável | Unidade | Padrão | Usado quando | Descrição |
|---|---|---|---|---|---|
| Subsuperfície em camadas | `flag_layered_subsurface` | 0 / 1 | `0` | chave destes blocos | Ativa a subsuperfície em camadas, com três camadas de solo sobre camadas de rocha alterada até o leito rochoso e um lençol freático por célula (regras de Miguez-Macho et al., 2007). As configurações ficam nos blocos da subsuperfície em camadas da aba Soil and groundwater, e os rasters opcionais ficam logo abaixo dos valores que substituem. Requer flag_groundwater_modeling = 1. |
| Espessura do solo | `subsurface_soil_base_depth_m` | m | `2.0` | esquema em camadas ativo | subsurface_soil_base_depth_m é a ESPESSURA DO SOLO, em metros abaixo do terreno, ou seja, a profundidade em que o solo termina e começa a rocha alterada (regolito). As três camadas de solo (superficial, zona radicular, transmissão) usam a aba Soil classes até essa profundidade. SoilBaseDepth_path a substitui célula a célula. É limitada à profundidade até o leito rochoso. Padrão 2.0 m. |
| Mapa da espessura do solo | `SoilBaseDepth_path` | m | vazio | esquema em camadas ativo (prevalece onde tem dados) | SoilBaseDepth_path é um GeoTIFF opcional da ESPESSURA DO SOLO, em metros abaixo do terreno (a base do solo). Substitui subsurface_soil_base_depth_m onde for finito. Apenas para a subsuperfície em camadas. Fonte global: SoilGrids BDRICM. |
| Profundidade até o leito rochoso | `subsurface_depth_to_bedrock_m` | m | vazio | esquema em camadas, onde o mapa de DTB está vazio | subsurface_depth_to_bedrock_m é a PROFUNDIDADE ATÉ O LEITO ROCHOSO, em metros abaixo do terreno, ou seja, o fundo de toda a coluna modelada, com o solo e a rocha alterada abaixo dele. É maior ou igual à espessura do solo. Prioridade: raster DTB_path, depois este valor, depois o DTB (m) de cada classe de solo da aba Soil classes, com aviso. Limitada a subsurface_max_depth_m. |
| Coluna mais profunda | `subsurface_max_depth_m` | m | `50.0` | esquema em camadas ativo | subsurface_max_depth_m limita a coluna modelada, em metros abaixo do terreno, com fundo da coluna = min(profundidade até o leito rochoso, este valor). Padrão 50 m. |
| Espessura da primeira camada de rocha | `subsurface_deep_first_thickness_m` | m | `0.25` | esquema em camadas ativo | subsurface_deep_first_thickness_m é a espessura, em metros, da primeira camada de rocha logo abaixo da base do solo. Cada camada seguinte é subsurface_deep_growth_ratio vezes mais espessa, até subsurface_deep_max_thickness_m. Padrão 0.25 m. |
| Razão de crescimento das camadas de rocha | `subsurface_deep_growth_ratio` | - | `2.0` | esquema em camadas ativo | subsurface_deep_growth_ratio multiplica a espessura de cada camada de rocha para obter a seguinte. Com os padrões, as espessuras são 0.25, 0.5, 1, 2, 4, 4, ... m. Use um valor de pelo menos 1. Padrão 2. |
| Camada de rocha mais espessa | `subsurface_deep_max_thickness_m` | m | `4.0` | esquema em camadas ativo | subsurface_deep_max_thickness_m é a maior espessura de camada de rocha, em metros. As camadas mantêm essa espessura até o fundo da coluna. Padrão 4 m. |

#### Layered subsurface: rock properties {#layered-subsurface-rock-properties}

Fica em cinza enquanto `flag_layered_subsurface` vale 0.

| Configuração | Variável | Unidade | Padrão | Usado quando | Descrição |
|---|---|---|---|---|---|
| theta_s da rocha | `regolith_theta_s` | m3/m3 | `0.35` | esquema em camadas ativo | regolith_theta_s é o conteúdo de água na saturação (porosidade) das camadas de rocha abaixo da base do solo, em m3/m3. RegolithThetaS_path o substitui célula a célula. Padrão 0.35. |
| Mapa do theta_s da rocha | `RegolithThetaS_path` | m3/m3 | vazio | esquema em camadas ativo (prevalece onde tem dados) | RegolithThetaS_path é um GeoTIFF opcional do conteúdo de água na saturação das camadas de rocha, em m3/m3. Substitui regolith_theta_s onde for finito. Apenas para a subsuperfície em camadas. |
| theta_r da rocha | `regolith_theta_r` | m3/m3 | `0.05` | esquema em camadas ativo | regolith_theta_r é o conteúdo de água residual das camadas de rocha, em m3/m3, abaixo de regolith_theta_s. RegolithThetaR_path o substitui célula a célula. Padrão 0.05. |
| Mapa do theta_r da rocha | `RegolithThetaR_path` | m3/m3 | vazio | esquema em camadas ativo (prevalece onde tem dados) | RegolithThetaR_path é um GeoTIFF opcional do conteúdo de água residual das camadas de rocha, em m3/m3. Substitui regolith_theta_r onde for finito. Apenas para a subsuperfície em camadas. |
| alfa de van Genuchten da rocha | `regolith_alpha_vg_m_inverse` | 1/m | `2.0` | esquema em camadas ativo | regolith_alpha_vg_m_inverse é o alfa de van Genuchten das camadas de rocha, em 1/m. Junto com regolith_n_vg, define quanta água a rocha retém depois de drenar e, portanto, o seu rendimento específico. RegolithAlphaVG_path o substitui célula a célula. Padrão 2. |
| Mapa do alfa de van Genuchten da rocha | `RegolithAlphaVG_path` | 1/m | vazio | esquema em camadas ativo (prevalece onde tem dados) | RegolithAlphaVG_path é um GeoTIFF opcional do alfa de van Genuchten das camadas de rocha, em 1/m. Substitui regolith_alpha_vg_m_inverse onde for finito. Apenas para a subsuperfície em camadas. |
| n de van Genuchten da rocha | `regolith_n_vg` | - | `1.5` | esquema em camadas ativo | regolith_n_vg é o n de van Genuchten das camadas de rocha (adimensional, maior que 1). RegolithNVG_path o substitui célula a célula. Padrão 1.5. |
| Mapa do n de van Genuchten da rocha | `RegolithNVG_path` | - | vazio | esquema em camadas ativo (prevalece onde tem dados) | RegolithNVG_path é um GeoTIFF opcional do n de van Genuchten das camadas de rocha. Substitui regolith_n_vg onde for finito. Apenas para a subsuperfície em camadas. |
| Ksat vertical da rocha | `regolith_ksat_v_mm_h` | mm/h | `5.0` | esquema em camadas ativo | regolith_ksat_v_mm_h é a condutividade hidráulica saturada vertical das camadas de rocha, em mm/h. Limita a drenagem e a recarga através da rocha. RegolithKsatV_path a substitui célula a célula. Padrão 5 mm/h. |
| Mapa do Ksat vertical da rocha | `RegolithKsatV_path` | mm/h | vazio | esquema em camadas ativo (prevalece onde tem dados) | RegolithKsatV_path é um GeoTIFF opcional da condutividade saturada vertical das camadas de rocha, em mm/h. Substitui regolith_ksat_v_mm_h onde for finito. Apenas para a subsuperfície em camadas. |
| Ksat horizontal da rocha | `regolith_ksat_h_mm_h` | mm/h | vazio | esquema em camadas ativo (vazio: kgsat) | regolith_ksat_h_mm_h é a condutividade hidráulica saturada horizontal das camadas de rocha, em mm/h, usada no fluxo lateral das águas subterrâneas. Deixe vazio para usar o Ksat das águas subterrâneas (kgsat) da aba Soil classes. RegolithKsatH_path a substitui célula a célula. |
| Mapa do Ksat horizontal da rocha | `RegolithKsatH_path` | mm/h | vazio | esquema em camadas ativo (prevalece onde tem dados) | RegolithKsatH_path é um GeoTIFF opcional da condutividade saturada horizontal das camadas de rocha, em mm/h, usada no fluxo lateral das águas subterrâneas. Substitui regolith_ksat_h_mm_h onde for finito. Apenas para a subsuperfície em camadas. Fonte global: permeabilidade do GLHYMPS 2.0. |
| Rendimento específico da rocha | `regolith_specific_yield` | - | vazio | esquema em camadas ativo (vazio: da curva) | regolith_specific_yield é a porosidade drenável das camadas de rocha (adimensional). Deixe vazio para derivá-la dos valores de van Genuchten, como theta_s menos o conteúdo de água na capacidade de campo. Um valor aqui ou em RegolithSpecificYield_path substitui essa derivação e não pode exceder theta_s menos theta_r. |
| Mapa do rendimento específico da rocha | `RegolithSpecificYield_path` | - | vazio | esquema em camadas ativo (prevalece onde tem dados) | RegolithSpecificYield_path é um GeoTIFF opcional do rendimento específico das camadas de rocha. Substitui o valor derivado (theta_s menos a capacidade de campo) onde for finito. Apenas para a subsuperfície em camadas. |

#### Layered subsurface: soil and numerics {#layered-subsurface-soil-and-numerics}

Fica em cinza enquanto `flag_layered_subsurface` vale 0.

| Configuração | Variável | Unidade | Padrão | Usado quando | Descrição |
|---|---|---|---|---|---|
| Kh / Kv do solo | `soil_lateral_anisotropy` | - | `1.0` | esquema em camadas ativo | soil_lateral_anisotropy é a razão entre as condutividades horizontal e vertical das três camadas de solo, com Kh = anisotropia x Ksat. O valor 1 indica isotropia. Padrão 1. |
| Sucção na capacidade de campo | `capillary_field_capacity_head_m` | m | `3.3` | esquema em camadas ativo | capillary_field_capacity_head_m é a carga de sucção, em metros, que define a capacidade de campo, ou seja, a água que uma camada retém depois que o lençol freático desce abaixo dela. O rendimento específico é theta_s menos theta nessa carga, e a ascensão capilar a partir do lençol freático repõe a água de uma camada apenas até esse conteúdo de água. Padrão 3.3 m (cerca de 33 kPa). Reduza o valor para representar uma franja capilar acima de lençóis freáticos rasos (o rendimento específico diminui junto). |
| Subpassos de drenagem | `subsurface_drainage_substeps` | - | `1` | esquema em camadas ativo | subsurface_drainage_substeps é o número de subpassos da drenagem por gravidade entre camadas dentro de um passo de tempo do modelo. O valor 1 basta na maioria dos casos. Aumente-o (2 a 10) para camadas finas e muito condutivas. Padrão 1. |
| Intervalo da atualização lateral | `groundwater_target_dt_s` | s | `86400` | águas subterrâneas ativas | groundwater_target_dt_s é o intervalo, em segundos, entre as atualizações laterais das águas subterrâneas, nos dois esquemas de subsuperfície. Um intervalo menor é usado quando o limite de estabilidade o exige. Os fluxos verticais no solo continuam rodando a cada passo de tempo do modelo. Padrão 86400 s (um dia). |
| Menor intervalo lateral | `groundwater_min_dt_s` | s | `60` | águas subterrâneas ativas | groundwater_min_dt_s é o menor intervalo, em segundos, permitido entre atualizações laterais das águas subterrâneas, mesmo quando o limite de estabilidade pede menos. Padrão 60 s. |
| Fluxo implícito no lençol freático | `flag_implicit_water_table_flux` | 0 / 1 | `1` | esquema em camadas ativo | Resolve de forma implícita o fluxo de Darcy entre o solo e o lençol freático na subsuperfície em camadas (um passo de Euler implícito linearizado por célula). O valor 1 (padrão) mantém a precisão em passos de tempo longos quando o lençol freático é raso. O valor 0 usa o fluxo explícito, que exige passos curtos nessa situação. Usado apenas com flag_layered_subsurface = 1. |

#### Lateral conductivity multipliers {#lateral-conductivity-multipliers}

Fica em cinza enquanto `flag_layered_subsurface` vale 0.

| Configuração | Variável | Unidade | Padrão | Usado quando | Descrição |
|---|---|---|---|---|---|
| Multiplicador do Kh do solo | `soil_lateral_conductivity_multiplier` | - | `1.0` | esquema em camadas ativo | soil_lateral_conductivity_multiplier multiplica a condutividade horizontal das três camadas de solo (Ksat do solo x soil_lateral_anisotropy) no fluxo lateral das águas subterrâneas. O Ksat vertical e a infiltração não mudam. É ajustado pela calibração por recessão das águas subterrâneas em camadas (as vazões altas drenam pelo solo). O valor 1 mantém os valores mapeados. |
| Multiplicador do Kh da rocha | `regolith_lateral_conductivity_multiplier` | - | `1.0` | esquema em camadas ativo | regolith_lateral_conductivity_multiplier multiplica a condutividade horizontal das camadas de rocha abaixo da base do solo (regolith_ksat_h_mm_h, RegolithKsatH_path ou kgsat). É ajustado pela calibração por recessão das águas subterrâneas em camadas (as vazões baixas drenam pela rocha). O valor 1 mantém os valores mapeados. |

#### Feddes root-water stress {#feddes-root-water-stress}

Chave: `flag_feddes`. O restante do bloco fica em cinza enquanto ela vale 0.

| Configuração | Variável | Unidade | Padrão | Usado quando | Descrição |
|---|---|---|---|---|---|
| Estresse de Feddes | `flag_feddes` | 0 / 1 | `0` | chave deste bloco | Ativa o estresse hídrico radicular de Feddes, em que a transpiração de cada camada de solo é reduzida conforme a sua carga de sucção. As cargas ficam neste bloco. Funciona com o esquema de solo em camadas e com o legado. |
| h1, anaerobiose | `feddes_h1_m` | m | `-0.1` | Feddes ativo | feddes_h1_m é a carga de anaerobiose, em metros (negativa). Com o solo mais úmido que h1, as raízes não retiram água (falta oxigênio). Padrão -0.1 m. |
| h2, início do ótimo | `feddes_h2_m` | m | `-0.25` | Feddes ativo | feddes_h2_m é a carga, em metros (negativa), a partir da qual a absorção se torna ótima. Entre h1 e h2, o fator de estresse sobe de 0 a 1. Padrão -0.25 m. |
| h3, início do estresse | `feddes_h3_m` | m | `-4.0` | Feddes ativo | feddes_h3_m é a carga, em metros (negativa), em que começa o estresse hídrico. Entre h3 e h4, o fator cai de 1 a 0. É usada quando feddes_h3_low_m e feddes_h3_high_m estão vazios. Padrão -4 m. |
| h3 com demanda baixa | `feddes_h3_low_m` | m | vazio | Feddes ativo (vazio: h3) | feddes_h3_low_m é o h3 com demanda de transpiração baixa (ET potencial de 1 mm/d ou menos), em metros (negativo). Com feddes_h3_high_m, h3 é interpolado pela demanda, como no SWAP. Deixe vazio para usar feddes_h3_m. |
| h3 com demanda alta | `feddes_h3_high_m` | m | vazio | Feddes ativo (vazio: h3) | feddes_h3_high_m é o h3 com demanda de transpiração alta (ET potencial de 5 mm/d ou mais), em metros (negativo). Costuma ser menos negativo que feddes_h3_low_m, de modo que o estresse começa mais cedo nos dias de demanda alta. Deixe vazio para usar feddes_h3_m. |
| h4, ponto de murcha | `feddes_h4_m` | m | `-80.0` | Feddes ativo | feddes_h4_m é a carga no ponto de murcha, em metros (negativa). Com o solo mais seco que h4, as raízes não retiram água. Padrão -80 m (-0.8 MPa). |

#### Deep aquifer {#deep-aquifer}

Chave: `flag_deep_aquifer`. O restante do bloco fica em cinza enquanto ela vale 0.

| Configuração | Variável | Unidade | Padrão | Usado quando | Descrição |
|---|---|---|---|---|---|
| Aquífero profundo | `flag_deep_aquifer` | 0 / 1 | `0` | chave deste bloco | Ativa o aquífero profundo. A fração deep_recharge_fraction da recarga do lençol freático vai para um reservatório linear por sub-bacia e volta à superfície depois de deep_aquifer_tau_days. Requer DeepAquiferSubbasins_path e DeepAquiferChannelWeight_path. |
| Mapa das sub-bacias do aquífero profundo | `DeepAquiferSubbasins_path` | ID | vazio | aquífero profundo ativo: obrigatório | DeepAquiferSubbasins_path é um GeoTIFF de inteiros com os IDs das sub-bacias (1, 2, ...). Cada ID é um reservatório do aquífero profundo. Obrigatório apenas quando flag_deep_aquifer = 1. Toda célula ativa precisa de um ID positivo. Um raster só com valores 1 dá um único reservatório para todo o domínio. |
| Mapa dos pesos de retorno do aquífero profundo | `DeepAquiferChannelWeight_path` | - | vazio | aquífero profundo ativo: obrigatório | DeepAquiferChannelWeight_path é um GeoTIFF de pesos não negativos que indica onde a vazão de saída do aquífero profundo de cada sub-bacia volta à superfície, por exemplo 1 nas células de rio e 0 nas demais. Os pesos são normalizados dentro de cada sub-bacia, que precisa de pelo menos um peso positivo. Obrigatório apenas quando flag_deep_aquifer = 1. |
| Fração da recarga para o aquífero profundo | `deep_recharge_fraction` | - | `0.05` | aquífero profundo ativo | deep_recharge_fraction é a fração, em (0, 1], da recarga do lençol freático enviada ao aquífero profundo, um reservatório linear lento por sub-bacia abaixo do modelo 2-D de águas subterrâneas. O restante recarrega o aquífero raso. Lido apenas quando flag_deep_aquifer = 1. |
| Tempo de resposta | `deep_aquifer_tau_days` | dias | `180` | aquífero profundo ativo | deep_aquifer_tau_days é o tempo de resposta do aquífero profundo, em dias. Cada reservatório de sub-bacia drena com vazão de saída = armazenamento / tau, e essa vazão volta à superfície nas células ponderadas por DeepAquiferChannelWeight_path. Lido apenas quando flag_deep_aquifer = 1. |

#### Deep aquifer: starting storage (give one, or none to start empty) {#deep-aquifer-starting-storage-give-one-or-none-to-start-empty}

Fica em cinza enquanto `flag_deep_aquifer` vale 0.

| Configuração | Variável | Unidade | Padrão | Usado quando | Descrição |
|---|---|---|---|---|---|
| Escoamento de base profundo inicial (de um posto) | `deep_aquifer_initial_baseflow_mm_day` | mm/dia | vazio | opção 1 | deep_aquifer_initial_baseflow_mm_day é o escoamento de base do aquífero profundo por unidade de área na data inicial, em mm/dia (opção 1, a partir de um posto, por exemplo com hydropol2d estimate-deep-baseflow, que divide a parte profunda do escoamento de base da data inicial pela área de drenagem). Cada sub-bacia começa com armazenamento S0 = q0 x área da sub-bacia x deep_aquifer_tau_days. Deixe vazio para que o aquífero comece vazio. Informe este valor ou deep_aquifer_mean_recharge_mm_year, não os dois. |
| Recarga média de longo prazo (sem posto) | `deep_aquifer_mean_recharge_mm_year` | mm/ano | vazio | opção 2: regime permanente | deep_aquifer_mean_recharge_mm_year é a recarga média de longo prazo para o lençol freático, em mm/ano (opção 2, sem necessidade de posto). O aquífero profundo começa em regime permanente, com q0 = deep_recharge_fraction x esta recarga e S0 = q0 x área da sub-bacia x deep_aquifer_tau_days. Informe este valor ou deep_aquifer_initial_baseflow_mm_day, não os dois. |
| Armazenamento inicial calibrado (JSON) | `DeepAquiferInitialState_path` | arquivo | vazio | opção 3: do Builder | DeepAquiferInitialState_path é um arquivo JSON opcional com o armazenamento inicial de cada sub-bacia do aquífero profundo (o DeepAquiferInitialState.json do Builder, gerado pela calibração por recessão). Use-o no lugar dos dois valores de estado inicial do aquífero profundo, e não junto com eles. |

### Surface flow {#tab-surface-flow}

Esquema de roteamento, saídas, canais de rio, tratamento do terreno e estruturas.

#### Routing scheme {#routing-scheme}

| Configuração | Variável | Unidade | Padrão | Usado quando | Descrição |
|---|---|---|---|---|---|
| Roteamento inercial local | `flag_inertial` | 0 / 1 | obrigatório | sempre | Seleciona o solver hidrodinâmico inercial local. É o solver de roteamento exigido pela extensão de canal subgrade de Neal (2012). |
| Discretização inercial | `flag_numerical_scheme` | 1 / 2 / 3 | obrigatório | inercial ativo | Escolhe a discretização inercial local (1 = Bates, 2 = upwind na declividade, 3 = centrada na declividade). O valor é usado apenas pelas opções de roteamento que chamam o esquema inercial. |
| Roteamento por autômatos celulares | `flag_CA` | 0 / 1 | obrigatório | sempre | Seleciona a opção de roteamento hidrodinâmico por autômatos celulares. Não a ative junto com o roteamento inercial local ou de momento completo. |
| Onda cinemática | `flag_kinematic` | 0 / 1 | obrigatório | sempre | Seleciona a alternativa de roteamento por onda cinemática. Não a combine com o roteamento inercial local, de momento completo ou por autômatos celulares. |
| Onda difusiva | `flag_diffusive` | 0 / 1 | obrigatório | sempre | Seleciona a alternativa de roteamento por onda difusiva. Não a combine com o roteamento inercial local, de momento completo ou por autômatos celulares. |
| Direções de escoamento D8 | `flag_D8` | 0 / 1 | obrigatório | sempre | Ativa o roteamento no terreno e o pré-processamento da drenagem D8 onde se aplicam. O roteamento inercial local continua baseado em faces. |

#### Outlets and boundaries {#outlets-and-boundaries}

| Configuração | Variável | Unidade | Padrão | Usado quando | Descrição |
|---|---|---|---|---|---|
| Tratamento do contorno aberto | `flag_boundary` | 0 / 1 | obrigatório | sempre | Ativa o tratamento configurado do contorno aberto ou do perímetro. Defina com cuidado a máscara e a declividade da saída, porque esta configuração controla a retirada de água na borda do domínio. |
| Relação na saída | `flag_outlet_type` | 1 / 2 | obrigatório | sempre | Escolhe a relação na saída (1 = saída em fluxo normal com slope_outlet, 2 = saída em fluxo crítico). As células de saída selecionadas determinam onde essa relação é aplicada. |
| Saída em fluxo crítico | `flag_critical` | 0 / 1 | obrigatório | sempre | Usa o tratamento de saída em fluxo crítico onde o solver de roteamento selecionado o suporta. É diferente da saída em fluxo normal selecionada com flag_outlet_type. |
| Declividade da linha de energia na saída | `slope_outlet` | m/m | obrigatório | saída em fluxo normal | slope_outlet é a declividade positiva da linha de energia em fluxo normal, em m/m, aplicada nas células de saída configuradas. Deve representar o gradiente do canal ou do terreno a jusante, além do domínio modelado. |
| Número de células de saída | `n_outlets_data` | - | `1` | sempre | n_outlets_data é o número de células da borda do domínio usadas como saídas (arredondado, no mínimo 1). As saídas crescem a partir da célula mais baixa do perímetro, a menos que seja fornecido um CSV de células de saída. Padrão 1. |

#### River channel (sub-grid) {#river-channel-sub-grid}

| Configuração | Variável | Unidade | Padrão | Usado quando | Descrição |
|---|---|---|---|---|---|
| Canal subgrade de Neal (2012) | `flag_neal_channel` | 0 / 1 | obrigatório | sempre | Ativa a extensão de Neal (2012), com canal retangular embutido e planície de inundação. Requer flag_inertial = 1, topologia raster estruturada e rasters válidos de largura e profundidade do rio. |
| Largura e profundidade do rio a partir de mapas | `flag_river_rasters` | 0 / 1 | obrigatório | canal subgrade ativo | Usa os rasters RiverWidths e RiverDepths fornecidos para definir a geometria do canal no modelo subgrade ativo. |
| n de Manning do canal | `Manning` | s m^-1/3 | obrigatório | sempre | Manning é a rugosidade de Manning do canal dentro das margens, em s m^-1/3, aplicada nas células de rio. As células de terreno e de extravasamento usam a rugosidade da aba Land use classes. |
| Coeficiente da lei de profundidade | `alfa_1` | - | obrigatório | canal pela área de drenagem | alfa_1 é o coeficiente da relação derivada de profundidade do canal, H = alfa_1 A^alfa_2, em que A é a área de contribuição em km2. É usado apenas quando a geometria do canal é derivada, e não fornecida por rasters. |
| Expoente da lei de profundidade | `alfa_2` | - | obrigatório | canal pela área de drenagem | alfa_2 é o expoente da relação derivada de profundidade do canal, H = alfa_1 A^alfa_2. Use um valor calibrado ou justificado para a rede de drenagem em estudo. |
| Coeficiente da lei de largura | `beta_1` | - | obrigatório | canal pela área de drenagem | beta_1 é o coeficiente da relação derivada de largura do canal, W = beta_1 A^beta_2, em que A é a área de contribuição em km2. É ignorado quando há rasters de largura do rio. |
| Expoente da lei de largura | `beta_2` | - | obrigatório | canal pela área de drenagem | beta_2 é o expoente da relação derivada de largura do canal, W = beta_1 A^beta_2. Controla a rapidez com que os canais gerados se alargam para jusante. |

#### Terrain treatment {#terrain-treatment}

| Configuração | Variável | Unidade | Padrão | Usado quando | Descrição |
|---|---|---|---|---|---|
| Reamostrar a grade | `flag_resample` | 0 / 1 | obrigatório | sempre | Reamostra os rasters auxiliares para a grade do DEM durante o pré-processamento quando a grade deles difere da do DEM. |
| Resolução do modelo | `resolution_resample` | m | obrigatório | reamostragem ativa | resolution_resample é a resolução da grade de trabalho do modelo, em metros, quando a reamostragem de rasters está ativa. Todas as entradas do modelo são alinhadas a essa resolução durante o pré-processamento. |
| Preencher depressões | `flag_fill_DEM` | 0 / 1 | obrigatório | sempre | Preenche as depressões do terreno antes de derivar as direções de drenagem e a acumulação de fluxo. |
| Suavizar os perfis dos rios | `flag_smoothening` | 0 / 1 | obrigatório | sempre | Aplica a suavização restrita dos perfis dos cursos d'água durante o pré-processamento do DEM. Esta opção requer a Optimization Toolbox. |
| Área limiar da rede de drenagem | `min_area` | km2 | obrigatório | suavização ativa | min_area é o limiar de área de contribuição, em km2, usado para extrair a rede de drenagem modelada e derivar a geometria hidráulica a partir da acumulação de fluxo. |
| Intensidade da suavização | `K_value` | 0 a 20 | obrigatório | suavização ativa | K_value é a intensidade de suavização passada ao suavizador restrito e regularizado dos perfis dos cursos d'água. É usado apenas quando a suavização do DEM está ativa. Valores maiores produzem uma regularização mais forte do perfil. |
| Regularização da suavização | `tau` | 0 a 1 | obrigatório | suavização ativa | tau é o parâmetro adimensional de regularização passado ao suavizador restrito e regularizado dos perfis dos cursos d'água. É usado apenas quando a suavização do DEM está ativa. |
| Declividade mínima imposta | `sl` | m/m | obrigatório | suavização ativa | sl é o gradiente mínimo de drenagem imposto, em m/m, usado no condicionamento do terreno quando a imposição de declividade mínima está ativa. |
| Suavizar células | `flag_smooth_cells` | 0 / 1 | obrigatório | sempre | Aplica o tratamento configurado de suavização do DEM em nível de célula durante o pré-processamento. |
| Apenas os canais principais | `flag_trunk` | 0 / 1 | obrigatório | sempre | Usa a opção de processamento dos canais principais na preparação do terreno e da rede de drenagem. |
| Rebaixar o DEM | `flag_reduce_DEM` | 0 / 1 | obrigatório | sempre | Aplica o rebaixamento configurado do DEM nos canais de rio durante o pré-processamento. |
| Filtro DTM | `flag_DTM` | 0 / 1 | obrigatório | sempre | Usa o caminho de processamento DTM na preparação do terreno quando os dados de entrada exigem esse fluxo de trabalho. |
| Declividade do filtro DTM | `slope_DTM` | % | obrigatório | filtro DTM ativo | slope_DTM é o limiar de declividade, em porcentagem, usado pelo filtro DTM. É lido apenas quando a opção de filtragem DTM está ativa. |

#### Unstructured mesh {#unstructured-mesh}

| Configuração | Variável | Unidade | Padrão | Usado quando | Descrição |
|---|---|---|---|---|---|
| Malha Voronoi | `flag_voronoi` | 0 / 1 | `0` | sempre | Roda o modelo em uma malha Voronoi (não estruturada) preparada, em vez da grade raster. As opções da malha são lidas da aba Mesh. |
| Tabelas subgrade da malha Voronoi | `flag_voronoi_subgrid` | 0 / 1 | obrigatório | Voronoi ativo | Ativa as tabelas subgrade das faces (área de escoamento, perímetro molhado e fator de condução em função do nível) na malha Voronoi. Usado apenas com flag_voronoi = 1. O caminho da tabela é definido na aba Mesh. |

#### Inflows and structures {#inflows-and-structures}

| Configuração | Variável | Unidade | Padrão | Usado quando | Descrição |
|---|---|---|---|---|---|
| Hidrogramas de entrada | `flag_inflow` | 0 / 1 | obrigatório | sempre | Aplica um ou mais hidrogramas de vazão prescritos nas coordenadas de entrada definidas na aba Inflow hydrographs. |
| Hidrogramas de nível | `flag_stage_hydrograph` | 0 / 1 | obrigatório | sempre | Aplica um hidrograma prescrito de nível de água nos locais configurados de contorno de nível. |
| Reservatórios | `flag_reservoir` | 0 / 1 | obrigatório | sempre | Ativa o módulo de reservatórios e estruturas de controle com as entradas de reservatório configuradas. |

#### Paused (keep at 0: setting 1 stops the run) {#paused-keep-at-0-setting-1-stops-the-run}

| Configuração | Variável | Unidade | Padrão | Usado quando | Descrição |
|---|---|---|---|---|---|
| Subgrade por tabela de consulta (pausado) | `flag_structured_lookup_subgrid` | 0 / 1 | `0` | pausado | Ativa a formulação subgrade estruturada por tabela de consulta no modelo raster regular. Usa propriedades de células e faces dependentes do nível e não pode ser combinada com a subgrade de Neal nem com a de Voronoi. |
| DEM de alta resolução para essa subgrade (pausado) | `Subgrid_DEM_path` | m | vazio | pausado | Subgrid_DEM_path é um GeoTIFF opcional de DEM de alta resolução, em metros, para a subgrade por tabela de consulta. É lido apenas quando a subgrade por tabela de consulta está ativa sem o modo de extravasamento. |

### Rain and ET {#tab-rain-and-et}

Origem da chuva e da evapotranspiração, e as listas de arquivos de mapas.

#### Rainfall source {#rainfall-source}

| Configuração | Variável | Unidade | Padrão | Usado quando | Descrição |
|---|---|---|---|---|---|
| Chuva | `flag_rainfall` | 0 / 1 | obrigatório | sempre | Ativa a forçante de chuva. Use com uma única fonte de chuva selecionada, que pode ser uma série temporal concentrada, a interpolação de pluviômetros, uma sequência programada de rasters ou um produto de satélite. |
| Chuva com variação espacial | `flag_spatial_rainfall` | 0 / 1 | obrigatório | chuva ativa | Interpola a chuva dos pluviômetros configurados para todas as células do modelo. São necessárias as coordenadas dos pluviômetros e uma série temporal comum de chuva. |
| Chuva da lista de mapas abaixo | `flag_input_rainfall_map` | 0 / 1 | obrigatório | chuva ativa | Lê da lista Rainfall maps uma sequência de rasters de chuva indexada no tempo. Não a ative junto com outra fonte de chuva espacial. |
| Chuva por satélite | `flag_satellite_rainfall` | 0 / 1 | obrigatório | chuva ativa | Ativa o fluxo de trabalho de forçante de chuva por satélite. Ele prepara uma programação horária de chuva espacial e ativa a chuva automaticamente. |
| Chuva por satélite em tempo real | `flag_real_time_satellite_rainfall` | 0 / 1 | obrigatório | chuva ativa | Ativa o fluxo de trabalho de chuva por satélite em tempo real. Esta opção experimental cria uma programação curta e contínua de chuva espacial. |

#### Evapotranspiration source {#evapotranspiration-source}

| Configuração | Variável | Unidade | Padrão | Usado quando | Descrição |
|---|---|---|---|---|---|
| ET das listas de mapas abaixo | `flag_input_ETP_map` | 0 / 1 | obrigatório | ET ativa | Lê da aba Rain and ET as programações pareadas de rasters de transpiração e evaporação. As duas programações devem ter as mesmas entradas de tempo. |

#### Advanced (keep the defaults unless you know why) {#advanced-keep-the-defaults-unless-you-know-why-1}

| Configuração | Variável | Unidade | Padrão | Usado quando | Descrição |
|---|---|---|---|---|---|
| Várias simulações de chuva (fluxo de trabalho legado) | `flag_rainfall_multiple_runs` | 0 / 1 | obrigatório | chuva ativa | Ativa o fluxo de trabalho legado de várias simulações de chuva. Deixe desativado para um único evento de chuva padrão. |

### Design storm {#tab-design-storm}

Chuvas sintéticas a partir de uma relação IDF local i = K RP^a / (b + duração)^c.

#### Hyetograph {#hyetograph}

| Configuração | Variável | Unidade | Padrão | Usado quando | Descrição |
|---|---|---|---|---|---|
| Blocos alternados | `flag_alternated_blocks` | 0 / 1 | obrigatório | chuva de projeto | Gera a chuva de projeto configurada por blocos alternados, em vez de ler uma série temporal de chuva. |
| Curvas de Huff | `flag_huff` | 0 / 1 | obrigatório | chuva de projeto | Gera a chuva de projeto configurada por curvas de Huff, em vez de ler uma série temporal de chuva. |
| Período de retorno | `RP` | anos | obrigatório | chuva de projeto | RP é o período de retorno da chuva de projeto, em anos. É usado pela relação IDF selecionada para calcular a intensidade da chuva. |
| Duração da chuva | `Rainfall Duration` | min | obrigatório | chuva de projeto | Rainfall Duration é a duração total da chuva de projeto, em minutos. Define a extensão do hietograma gerado por blocos alternados ou por Huff. |
| Passo de tempo do hietograma | `dt_design` | min | obrigatório | chuva de projeto | dt_design é o incremento de tempo, em minutos, usado para discretizar o hietograma de projeto gerado. Deve ser curto o bastante para resolver o pico de chuva pretendido. |

#### IDF relation {#idf-relation}

| Configuração | Variável | Unidade | Padrão | Usado quando | Descrição |
|---|---|---|---|---|---|
| Escala K da IDF | `K` | ver nota | obrigatório | chuva de projeto | K é o coeficiente de escala da relação IDF local i = K RP^a / (b + duração)^c. As suas unidades devem ser coerentes com a intensidade em mm/h e a duração em minutos. |
| Expoente a do período de retorno | `a` | - | obrigatório | chuva de projeto | a é o expoente adimensional do período de retorno na relação IDF local. Use coeficientes ajustados para o local de estudo. |
| Deslocamento b da duração | `b` | min | obrigatório | chuva de projeto | b é o deslocamento da duração na relação IDF local, em minutos quando a duração é dada em minutos. |
| Expoente c da duração | `c` | - | obrigatório | chuva de projeto | c é o expoente adimensional da duração na relação IDF local. Controla como a intensidade decai com o aumento da duração da chuva. |

### Water quality {#tab-water-quality}

Build-up e wash-off de poluentes.

#### Water quality {#water-quality}

Chave: `flag_waterquality`. O restante do bloco fica em cinza enquanto ela vale 0.

| Configuração | Variável | Unidade | Padrão | Usado quando | Descrição |
|---|---|---|---|---|---|
| Qualidade da água | `flag_waterquality` | 0 / 1 | obrigatório | chave deste bloco | Ativa os cálculos de build-up, wash-off, transporte e saídas de poluentes. |
| Parâmetros a partir de mapas | `flag_WQ_Rasters` | 0 / 1 | obrigatório | qualidade da água ativa | Usa os rasters espaciais dos coeficientes de qualidade da água B1, B2, W1 e W2 em vez dos coeficientes da tabela de cobertura da terra. |
| Build-up inicial a partir de um mapa | `flag_initial_buildup` | 0 / 1 | obrigatório | qualidade da água ativa | Inicializa o build-up de qualidade da água com o período seco antecedente e as configurações de build-up definidos. |
| Dias secos antecedentes | `ADD` | dias | obrigatório | qualidade da água ativa | ADD é o número de dias secos antecedentes. Quando não se usa um raster de build-up inicial, entra na inicialização exponencial do build-up B0 = C1 [1 - exp(-C2 ADD)]. |
| Massa superficial mínima | `min_Bt` | g/m2 | obrigatório | qualidade da água ativa | min_Bt é a densidade superficial mínima de massa de poluente, em g/m2, mantida pelo cálculo de wash-off. Evita o tratamento numérico de massas de poluente desprezíveis. |
| Limite inferior do build-up | `Bmin` | g/m2 | obrigatório | qualidade da água ativa | Bmin é o limite inferior do build-up de poluentes, em g/m2, usado pela formulação de build-up e wash-off selecionada. Use um valor não negativo e não maior que Bmax. |
| Limite superior do build-up | `Bmax` | g/m2 | obrigatório | qualidade da água ativa | Bmax é o limite superior do build-up de poluentes, em g/m2, usado pela formulação de build-up e wash-off selecionada. Limita a massa de poluente fisicamente armazenada quando essa opção está ativa. |
| Limiar de exibição nos mapas | `Pol_min` | mg/L | obrigatório | qualidade da água ativa | Pol_min é a concentração mínima de poluente, em mg/L, exibida nos mapas de qualidade da água. É um limiar de visualização. Valores abaixo dele ficam ocultos nos gráficos, mas não são removidos do balanço de massa. |

#### Advanced (keep the defaults unless you know why) {#advanced-keep-the-defaults-unless-you-know-why-2}

Fica em cinza enquanto `flag_waterquality` vale 0.

| Configuração | Variável | Unidade | Padrão | Usado quando | Descrição |
|---|---|---|---|---|---|
| Formulação (0 = build-up / wash-off por massa) | `flag_wq_model` | 0 / ... | obrigatório | qualidade da água ativa | Seleciona a formulação de qualidade da água. O valor 0 usa o modo de build-up e wash-off baseado em massa. Use outros valores apenas em configurações legadas suportadas. |

### Risk and gauges {#tab-risk-and-gauges}

Risco de instabilidade humana e pontos de observação.

#### Human instability {#human-instability}

| Configuração | Variável | Unidade | Padrão | Usado quando | Descrição |
|---|---|---|---|---|---|
| Risco de instabilidade humana | `flag_human_instability` | 0 / 1 / 3 | obrigatório | sempre | Calcula indicadores de instabilidade humana a partir da profundidade e da velocidade. O valor 0 desativa o cálculo, o valor 1 usa a classificação básica e o valor 3 ativa a classificação estendida. |

#### Observation points {#observation-points}

| Configuração | Variável | Unidade | Padrão | Usado quando | Descrição |
|---|---|---|---|---|---|
| Registrar nos postos abaixo | `flag_obs_gauges` | 0 / 1 | obrigatório | sempre | Exporta os valores modelados nas coordenadas dos postos de observação listados na tabela de postos. |

---

## Tabela de postos e seções transversais de vazão {#gauge-table-and-discharge-cross-sections}

Com `flag_obs_gauges = 1`, o modelo registra resultados em cada posto da tabela de postos da aba Risk and gauges.

| Coluna | Obrigatória | Significado |
|---|---|---|
| Gauge | sim | Número do posto |
| Easting (m), Northing (m) | sim | Posição do posto, na projeção do DEM |
| Label Name | sim | Nome usado nas saídas |
| Cross-section width (cells) | não | Número de células da seção transversal de vazão. Se vazio, 5. Uma largura par é aumentada em 1, para que o posto fique no meio. |
| Downstream direction | não | `auto` (padrão), ou `N`, `S`, `E`, `W` |

A tabela termina na primeira linha vazia.

**O que um posto registra.** A profundidade e o nível da água são tomados na célula do posto. A vazão é somada ao longo de uma seção transversal, uma linha de células que atravessa o escoamento e é centrada na célula do posto.

1. Com `auto`, a direção de jusante é a de descida segundo o gradiente médio do terreno em uma janela quadrada em torno do posto, com lado igual à largura da seção. Use `N`, `S`, `E` ou `W` onde o terreno é plano. `N` ou `S` dá uma linha leste-oeste, e `E` ou `W` dá uma linha norte-sul.
2. As células fora da grade ou do domínio são retiradas da linha.
3. A vazão é a soma com sinal nas faces de jusante da linha, a mesma regra dos postos de roteamento do HydroPol2D-Python. As diagonais D8 que cruzam a linha são contadas.
4. As duas convenções de face dos solvers de roteamento são tratadas, a das saídas de um só lado (autômatos celulares, inercial D8) e a dos fluxos com sinal guardados nas duas faces (inercial D4, difusivo, cinemático, momento completo). Por isso, as simulações inerciais não são contadas em dobro.

**Saídas.**

| Saída | Conteúdo |
|---|---|
| Figuras dos hidrogramas dos postos | Uma linha traço-ponto com a vazão na seção transversal |
| `Rating_Curve_Gauges.csv` | A coluna `Cross-section Discharge (m3/s)` |
| `Gauge_Cross_Sections.csv` | A linha e a coluna da grade de cada célula de cada seção transversal |

No modo bypass, as duas colunas opcionais do CSV de postos são `Cross_section_width_cells` e `Downstream_direction`. As verificações estão em `Validation/Gauges/run_gauge_cross_section_checks.m`.

---

## Modo bypass e variáveis de ambiente {#bypass-mode-and-environment-variables}

- No modo bypass, os mesmos nomes de variáveis são campos de `InputData_Bypass.flags` (chaves e configurações das camadas e de Feddes) e de `InputData_Bypass.general` (demais configurações, como o estado inicial do aquífero profundo).
- As variáveis de ambiente prevalecem sobre a planilha. O Case Builder usa esse recurso.

| Variável de ambiente | Substitui |
|---|---|
| `HYDROPOL_INPUT_EXCEL_FILE` | A planilha a ser lida |
| `HYDROPOL_SUBSURFACE_SCHEME`, `HYDROPOL_ENABLE_FEDDES`, `HYDROPOL_IMPLICIT_WATER_TABLE_FLUX` | As chaves do esquema em camadas, de Feddes e do fluxo implícito |
| `HYDROPOL_<NAME>` | Qualquer configuração numérica das camadas ou de Feddes, pelo nome da variável em maiúsculas |
| `HYDROPOL_DEEP_INITIAL_BASEFLOW_MM_DAY`, `HYDROPOL_DEEP_MEAN_RECHARGE_MM_YEAR`, `HYDROPOL_DEEP_INITIAL_STATE_PATH` | O estado inicial do aquífero profundo |
| `HYDROPOL_SOIL_LATERAL_CONDUCTIVITY_MULTIPLIER`, `HYDROPOL_REGOLITH_LATERAL_CONDUCTIVITY_MULTIPLIER` | Os multiplicadores ajustados da condutividade lateral |

---

## Formato antigo {#older-layout}

Os casos criados antes de 2026-10-20 usam `General_Data.xlsx`, com a sua aba `Flags`, e planilhas separadas. Eles continuam rodando sem mudanças. Cada leitor busca a sua aba na planilha do caso, quando o caso tem uma, e na planilha antiga, caso contrário.

| Planilha do caso | Formato antigo |
|---|---|
| Oito abas de configurações | A aba `General_Data`, com as configurações em blocos e os caminhos dos rasters nas colunas T e U |
| Chaves dentro dos seus blocos | A aba `Flags`, com uma chave por linha e o valor na coluna E |
| Soil classes, Land use classes, Human instability, Mesh, Control structures | `SOIL_parameters.xlsx`, `LULC_parameters.xlsx`, `human_risk.xlsx`, `Voronoi_Settings.xlsx`, `BC_Control_structure.xlsx` |
| Rain series, Rain gauges, Climate stations, Inflow hydrographs, Stage hydrographs | `Rainfall_Intensity_Data.xlsx`, `Rainfall_Spatial_Input.xlsx`, `ETP_input_data.xlsx`, `Inflow_Hydrograph.xlsx`, `Stage_Hydrograph.xlsx` |

Para converter um caso antigo, rode o gerador de planilhas a partir de `tools/workbook_builder`, no repositório MATLAB.

```bash
python build_input_workbook.py input_catalog.yaml General_Data.xlsx HydroPol2D_Inputs.xlsx
```

O gerador transfere todos os valores, caminhos de mapas, listas de mapas e postos, e copia as tabelas de classes e as séries das planilhas que estão ao lado da origem. Uma série que as chaves do caso não leem é mantida como um modelo vazio, com os seus cabeçalhos. O caso V-tilted dá resultados idênticos nos dois formatos (`Validation/Workbook/run_single_workbook_checks.m`).

As planilhas antigas não precisam mais das chaves aposentadas `flag_data_source`, `flag_dam_break` e `flag_river_heigth_compensation` (todas com padrão 0). `flag_subgrid` e `flag_overbanks` são derivadas das chaves do canal, e `time_save_ETP` é opcional.
