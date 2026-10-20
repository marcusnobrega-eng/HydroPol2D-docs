---
title: Parâmetros de configuração
---

# Parâmetros de configuração

Esta página documenta todas as variáveis ​​definidas em `General_Data.xlsx`.
Cada parâmetro controla um aspecto específico do HydroPol2D, incluindo:
- tempo de simulação
- estabilidade numérica
- processos hidrológicos
- roteamento hidráulico
- conjuntos de dados de entrada
- controle de saída

---

## Controle de execução

| Variável | Unidades | Descrição |
|----------|------|-------------|
| $\mathrm{time\_step\_model}$ | $\mathrm{s}$ | Etapa de tempo inicial do modelo usada na simulação |
| $\mathrm{min\_time\_step}$ | $\mathrm{s}$ | Passo de tempo adaptativo mínimo permitido para estabilidade numérica |
| $\mathrm{max\_time\_step}$ | $\mathrm{s}$ | Passo de tempo adaptativo máximo permitido |
| $\mathrm{time\_step\_change}$ | $\mathrm{s}$ | Incremento usado para ajustar o intervalo de tempo adaptativo |
| $\alpha_{\min}$ | - | Coeficiente mínimo de estabilidade tipo Courant |
| $\alpha_{\max}$ | - | Coeficiente máximo de estabilidade tipo Courant |
| $\mathrm{date\_begin}$ | - | Data e hora de início da simulação |
| $\mathrm{date\_end}$ | - | Data e hora de término da simulação |

---

## Condição limite de fluxo normal

| Variável | Unidades | Descrição |
|----------|------|-------------|
| $\mathrm{slope\_outlet}$ | $\mathrm{m\,m^{-1}}$ | Inclinação prescrita usada para estimar as condições normais de fluxo no limite de saída |

---

## Controle das Águas Subterrâneas {#groundwater-control}

Células D5:E8. Os valores abaixo são os das planilhas distribuídas.

| Variável | Unidades | Valor na planilha | Descrição |
|----------|----------|----------|----------|
| $\mathrm{groundwater\_courant}$ | - | 0.25 | Fator de segurança do limite explícito do passo de tempo das águas subterrâneas. No esquema em camadas, limita os subpassos do fluxo lateral. |
| $\mathrm{deep\_recharge\_fraction}$ | - | 0.05 | Fração da recarga descendente enviada ao aquífero profundo (com $\mathrm{flag\_deep\_aquifer} = 1$). |
| $\mathrm{deep\_aquifer\_tau\_days}$ | dias | 180 | Tempo de resposta $\tau$ dos reservatórios lineares profundos. |

---

## Subsuperfície em Camadas {#layered-subsurface}

Bloco D10:F28. Lido apenas quando $\mathrm{flag\_layered\_subsurface} = 1$. Veja [Subsuperfície em Camadas](../theory/layered-subsurface). Uma célula vazia mantém o padrão ou a alternativa indicada na tabela.

| Variável | Unidades | Padrão | Descrição |
|----------|----------|----------|----------|
| $\mathrm{subsurface\_soil\_base\_depth\_m}$ | m | 2.0 | Base do solo, ou seja, o fundo das três camadas de solo. $\mathrm{SoilBaseDepth\_path}$ prevalece onde for finito. |
| $\mathrm{subsurface\_depth\_to\_bedrock\_m}$ | m | vazio | Fundo de toda a coluna. Prioridade: $\mathrm{DTB\_path}$, depois este valor, depois a profundidade do solo padrão (1 m quando $\mathrm{DTB\_path}$ está vazio), com aviso. |
| $\mathrm{subsurface\_max\_depth\_m}$ | m | 50 | Teto da profundidade da coluna. A base da coluna é $\min(\mathrm{DTB}, \text{cap})$. |
| $\mathrm{subsurface\_deep\_first\_thickness\_m}$ | m | 0.25 | Espessura da primeira camada de regolito abaixo da base do solo. |
| $\mathrm{subsurface\_deep\_growth\_ratio}$ | - | 2 | Razão de espessura entre camadas de regolito consecutivas. |
| $\mathrm{subsurface\_deep\_max\_thickness\_m}$ | m | 4 | Espessura máxima de uma camada de regolito. |
| $\mathrm{regolith\_theta\_s}$ | m³/m³ | 0.35 | Conteúdo de água saturado do regolito. Raster: $\mathrm{RegolithThetaS\_path}$. |
| $\mathrm{regolith\_theta\_r}$ | m³/m³ | 0.05 | Conteúdo de água residual do regolito. Raster: $\mathrm{RegolithThetaR\_path}$. |
| $\mathrm{regolith\_alpha\_vg\_m\_inverse}$ | 1/m | 2 | $\alpha$ de van Genuchten do regolito. Raster: $\mathrm{RegolithAlphaVG\_path}$. |
| $\mathrm{regolith\_n\_vg}$ | - | 1.5 | $n$ de van Genuchten do regolito. Raster: $\mathrm{RegolithNVG\_path}$. |
| $\mathrm{regolith\_ksat\_v\_mm\_h}$ | mm/h | 5 | Condutividade saturada vertical do regolito. Raster: $\mathrm{RegolithKsatV\_path}$. |
| $\mathrm{regolith\_ksat\_h\_mm\_h}$ | mm/h | vazio | Condutividade saturada horizontal do regolito. Vazio: $\mathrm{kgsat}$ da tabela de solos. Raster: $\mathrm{RegolithKsatH\_path}$. |
| $\mathrm{regolith\_specific\_yield}$ | - | vazio | Rendimento específico do regolito. Vazio: $\theta_s - \theta_{fc}$ da curva do regolito. Raster: $\mathrm{RegolithSpecificYield\_path}$. |
| $\mathrm{soil\_lateral\_anisotropy}$ | - | 1 | $K_h/K_v$ das camadas de solo. |
| $\mathrm{subsurface\_drainage\_substeps}$ | - | 1 | Subpassos da cascata de drenagem por passo do modelo. |
| $\mathrm{capillary\_field\_capacity\_head\_m}$ | m | 3.3 | Sucção na capacidade de campo. Define $S_y = \theta_s - \theta_{fc}$ para todas as camadas. |
| $\mathrm{groundwater\_target\_dt\_s}$ | s | 3600 | Intervalo da atualização lateral das águas subterrâneas. |
| $\mathrm{groundwater\_min\_dt\_s}$ | s | 60 | Intervalo mínimo da atualização lateral das águas subterrâneas. |

---

## Estresse Hídrico Radicular de Feddes {#feddes-root-water-stress}

Bloco D30:F36. Lido apenas quando $\mathrm{flag\_feddes} = 1$. Veja [Modelo Hidrológico, Seção 3.5](../theory/hydrologic-model#35-feddes-root-water-uptake-stress). As cargas devem satisfazer $0 \ge h_1 > h_2 \ge h_3 > h_4$.

| Variável | Unidades | Padrão | Descrição |
|----------|----------|----------|----------|
| $\mathrm{feddes\_h1\_m}$ | m | −0.1 | Mais úmido que isso: sem absorção (anaerobiose). |
| $\mathrm{feddes\_h2\_m}$ | m | −0.25 | Início da absorção sem estresse. |
| $\mathrm{feddes\_h3\_m}$ | m | −4.0 | Fim da absorção sem estresse. |
| $\mathrm{feddes\_h3\_low\_m}$ | m | vazio: $h_3$ | $h_3$ com transpiração potencial de 1 mm/dia ou menos. |
| $\mathrm{feddes\_h3\_high\_m}$ | m | vazio: $h_3$ | $h_3$ com transpiração potencial de 5 mm/dia ou mais. |
| $\mathrm{feddes\_h4\_m}$ | m | −80 | Ponto de murcha: sem absorção. |

---

## Estado Inicial do Aquífero Profundo {#deep-aquifer-initial-state}

Bloco D38:F40. Lido apenas quando $\mathrm{flag\_deep\_aquifer} = 1$. Informe no máximo um valor, ou um arquivo em $\mathrm{DeepAquiferInitialState\_path}$ (T29). Sem nenhum deles, os reservatórios começam vazios. Veja [Modelo de Águas Subterrâneas, Seção 13](../theory/groundwater-model#13-deep-aquifer).

| Variável | Unidades | Padrão | Descrição |
|----------|----------|----------|----------|
| $\mathrm{deep\_aquifer\_initial\_baseflow\_mm\_day}$ | mm/dia | vazio | Escoamento de base profundo por unidade de área $q_0$ na data inicial. Cada sub-bacia começa com $S_0 = q_0 A \tau$. |
| $\mathrm{deep\_aquifer\_mean\_recharge\_mm\_year}$ | mm/ano | vazio | Recarga média de longo prazo $\bar{R}$. Os reservatórios começam em regime permanente, $q_0 = f_d \bar{R}$. |

---

## Multiplicadores da Condutividade Lateral {#lateral-conductivity-multipliers}

Bloco D42:F44. Lido apenas com a subsuperfície em camadas. O rendimento específico não é escalado, porque vem das curvas de retenção. A [calibração por recessão das águas subterrâneas](../calibration/groundwater-recession) ajusta os dois fatores. O Case Builder passa os valores ajustados ao MATLAB por meio de `HYDROPOL_SOIL_LATERAL_CONDUCTIVITY_MULTIPLIER` e `HYDROPOL_REGOLITH_LATERAL_CONDUCTIVITY_MULTIPLIER`, que se sobrepõem a essas células.

| Variável | Unidades | Padrão | Descrição |
|----------|----------|----------|----------|
| $\mathrm{soil\_lateral\_conductivity\_multiplier}$ | - | 1 | Fator aplicado à condutividade horizontal das três camadas de solo ($K_{sat}$ do solo × anisotropia). |
| $\mathrm{regolith\_lateral\_conductivity\_multiplier}$ | - | 1 | Fator aplicado à condutividade horizontal das camadas de regolito. |

---

## Controle de Mapas e Parcelas

| Variável | Unidades | Descrição |
|----------|------|-------------|
| $\mathrm{record\_time\_maps}$ | $\mathrm{min}$ | Intervalo de tempo para salvar saídas raster |
| $\mathrm{record\_time\_hydrographs}$ | $\mathrm{min}$ | Intervalo de tempo para salvar resultados do hidrograma |
| $\mathrm{Pol\_min}$ | $\mathrm{mg\,L^{-1}}$ | Limite mínimo de concentração de poluentes para visualização |
| $\mathrm{depth\_wse}$ | $\mathrm{m}$ | Profundidade limite usada para definir resultados de elevação da superfície da água |
| $\mathrm{flag\_wse}$ | - | Sinalizador para ativar saídas de elevação da superfície da água em vez de profundidade |
| $\mathrm{record\_time\_spatial\_rainfall}$ | $\mathrm{min}$ | Intervalo de tempo para exportação de mapas espaciais de precipitação |
| $\mathrm{time\_save\_ETP}$ | $\mathrm{min}$ | Intervalo de tempo para salvar as saídas de evapotranspiração |
| $\mathrm{record\_time\_spatial\_ETP}$ | $\mathrm{min}$ | Intervalo de tempo para exportação de campos ETP espaciais |

---

## Parâmetros de geometria do rio
Se `flag_reduce_dem` estiver ativado, a elevação das células do rio será reduzida para compensar a batimetria do rio. Um conjunto de 4 parâmetros é então necessário para descrever a largura e a profundidade do fluxo. Estes parâmetros são válidos para converter a área de acumulação de fluxo [$\mathrm{km^2}$] em profundidade de fluxo [$\mathrm{m}$] e largura [$\mathrm{m}$].

| Variável | Unidades | Descrição |
|----------|------|-------------|
| $\alpha_1$ | - | Coeficiente empírico que controla a escala da geometria do canal |
| $\alpha_2$ | - | Coeficiente secundário para relações de geometria hidráulica |
| $\beta_1$ | - | Expoente controlando largura ou comportamento de escala hidráulica |
| $\beta_2$ | - | Expoente secundário para relações de escala hidráulica |
| $n$ | $\mathrm{s\,m^{-1/3}}$ | Coeficiente de rugosidade de Manning para canal e fluxo superficial |

---

## Insumos de qualidade da água

| Variável | Unidades | Descrição |
|----------|------|-------------|
| $\mathrm{ADD}$ | $\mathrm{days}$ | Dias secos antecedentes usados ​​na modelagem de acúmulo de poluentes |
| $\mathrm{min\_Bt}$ | $\mathrm{g\,m^{-2}}$ | Limiar mínimo de acumulação de poluentes |
| $\mathrm{Bmin}$ | $\mathrm{g\,m^{-2}}$ | Massa poluente mínima permitida |
| $\mathrm{Bmax}$ | $\mathrm{g\,m^{-2}}$ | Capacidade máxima de acumulação de poluentes |

---

## Processamento DEM e controles de terreno

| Variável | Unidades | Descrição |
|----------|------|-------------|
| $\mathrm{min\_area}$ | $\mathrm{km^2}$ | Limite mínimo de área de drenagem para início do canal |
| $\tau$ | - | Parâmetro de suavização que controla a intensidade de filtragem DEM |
| $\mathrm{K\_value}$ | - | Parâmetro que controla o processamento do terreno ou dimensionamento hidráulico |
| $\mathrm{sl}$ | $\mathrm{m\,m^{-1}}$ | Limite mínimo de inclinação usado no condicionamento DEM |
| $\mathrm{resolution\_resample}$ | $\mathrm{m}$ | Resolução alvo para reamostragem DEM |
| $\mathrm{slope\_DTM}$ | $\%$ | Limite de inclinação usado para correção ou filtragem de terreno |

---

## Caminhos de arquivo e dados de entrada

| Variável | Unidades | Descrição |
|----------|------|-------------|
| $\mathrm{DEM\_path}$ | - | Caminho para o modelo digital de elevação |
| $\mathrm{LULC\_path}$ | - | Caminho para o raster de uso e cobertura da terra |
| $\mathrm{SOIL\_path}$ | - | Caminho para o raster de classificação do solo |
| $\mathrm{Warmup\_Depth\_path}$ | - | Caminho para a condição inicial de profundidade da água de aquecimento |
| $\mathrm{Initial\_Buildup\_path}$ | - | Caminho para o mapa inicial de acúmulo de poluentes |
| $\mathrm{Initial\_Soil\_Moisture\_path}$ | - | Caminho para a condição inicial de umidade do solo |
| $\mathrm{Initial\_SWE\_path}$ | - | Caminho opcional para SWE inicial em milímetros |
| $\mathrm{Initial\_Snow\_Depth\_path}$ | - | Caminho opcional para profundidade física inicial da neve em milímetros |
| $\mathrm{Albedo\_path}$ | - | Caminho para raster de albedo |
| $\mathrm{LAI\_path}$ | - | Caminho para raster do índice de área foliar |
| $\mathrm{RiverWidths\_path}$ | - | Caminho para raster da largura do rio |
| $\mathrm{RiverDepths\_path}$ | - | Caminho para raster de profundidade do rio |
| $\mathrm{DTB\_path}$ | - | Caminho para raster da profundidade ao leito rochoso. Na subsuperfície em camadas, define o fundo de toda a coluna |
| $\mathrm{SoilBaseDepth\_path}$ | - | Raster opcional da profundidade da base do solo (m), para a subsuperfície em camadas (T21) |
| $\mathrm{RegolithThetaS\_path}$ | - | Raster opcional de $\theta_s$ do regolito (T22) |
| $\mathrm{RegolithThetaR\_path}$ | - | Raster opcional de $\theta_r$ do regolito (T23) |
| $\mathrm{RegolithAlphaVG\_path}$ | - | Raster opcional de $\alpha$ de van Genuchten do regolito (T24) |
| $\mathrm{RegolithNVG\_path}$ | - | Raster opcional de $n$ de van Genuchten do regolito (T25) |
| $\mathrm{RegolithKsatV\_path}$ | - | Raster opcional de $K_{sat}$ vertical do regolito, em mm/h (T26) |
| $\mathrm{RegolithKsatH\_path}$ | - | Raster opcional de $K_{sat}$ horizontal do regolito, em mm/h (T27) |
| $\mathrm{RegolithSpecificYield\_path}$ | - | Raster opcional do rendimento específico do regolito (T28) |
| $\mathrm{DeepAquiferSubbasins\_path}$ | - | Raster de sub-bacias do aquífero profundo, que indica quais células alimentam cada reservatório (T19) |
| $\mathrm{DeepAquiferChannelWeight\_path}$ | - | Raster de pesos do canal, que indica onde cada reservatório profundo descarrega (T20) |
| $\mathrm{DeepAquiferInitialState\_path}$ | - | JSON opcional do estado inicial do aquífero profundo, gravado pela calibração do Case Builder (T29) |
| $\mathrm{B1\_path}$ | - | Caminho para raster de parâmetros relacionados a poluentes |
| $\mathrm{B2\_path}$ | - | Caminho para raster de parâmetros relacionados a poluentes |
| $\mathrm{W1\_path}$ | - | Caminho para a varredura do parâmetro de lavagem de poluentes |
| $\mathrm{W2\_path}$ | - | Caminho para a varredura do parâmetro de lavagem de poluentes |

---

## Parâmetros de Instabilidade Humana

| Variável | Unidades | Descrição |
|----------|------|-------------|
| $\mu$ | - | Coeficiente de atrito entre o corpo humano e o solo |
| $C_d$ | - | Coeficiente de arrasto para corpo humano em fluxo |
| $\rho_{\mathrm{person}}$ | $\mathrm{kg\,m^{-3}}$ | Densidade do corpo humano |
| $\mathrm{weight\_person}$ | $\mathrm{kg}$ | Peso humano médio |
| $\mathrm{height\_person}$ | $\mathrm{m}$ | Altura humana média |
| $\mathrm{width1\_person}$ | $\mathrm{m}$ | Largura frontal característica |
| $\mathrm{width2\_person}$ | $\mathrm{m}$ | Parâmetro de largura secundária |
| $\rho_{\mathrm{water}}$ | $\mathrm{kg\,m^{-3}}$ | Densidade da água |
| $g$ | $\mathrm{m\,s^{-2}}$ | Aceleração gravitacional |

---

## Pontos de Observação

| Variável | Unidades | Descrição |
|----------|------|-------------|
| $\mathrm{Gauge}$ | - | Identificador do medidor |
| $\mathrm{Easting}$ | $\mathrm{m}$ | Coordenada leste |
| $\mathrm{Northing}$ | $\mathrm{m}$ | Coordenada norte |
| $\mathrm{Label\ Name}$ | - | Rótulo de saída para séries temporais |

---

## Parâmetros de tempestade de design

| Variável | Unidades | Descrição |
|----------|------|-------------|
| $\mathrm{RP}$ | $\mathrm{years}$ | Período de retorno da tempestade de design |
| $\mathrm{Rainfall\ Duration}$ | $\mathrm{min}$ | Duração total da tempestade |
| $K$ | - | Coeficiente intensidade-duração-frequência |
| $a$ | - | Parâmetro da curva IDF |
| $b$ | - | Parâmetro da curva IDF |
| $c$ | - | Parâmetro da curva IDF |
| $\mathrm{dt\_design}$ | $\mathrm{min}$ | Resolução temporal da tempestade sintética |

---

## Precipitação por satélite ou radar

| Variável | Unidades | Descrição |
|----------|------|-------------|
| $\mathrm{Time}$ | $\mathrm{min}$ | Etapa de tempo do raster de precipitação |
| $\mathrm{Raster\ Directory}$ | - | Caminho para arquivos raster de chuva |

---

## Transpiração de Satélite

| Variável | Unidades | Descrição |
|----------|------|-------------|
| $\mathrm{Time}$ | $\mathrm{day}$ | Índice de tempo para dados de transpiração |
| $\mathrm{Raster\ Directory}$ | - | Caminho para rasters de transpiração |

---

## Evaporação por Satélite

| Variável | Unidades | Descrição |
|----------|------|-------------|
| $\mathrm{Time}$ | $\mathrm{day}$ | Índice de tempo para dados de evaporação |
| $\mathrm{Raster\ Directory}$ | - | Caminho para rasters de evaporação |

---

## Convenções da Planilha para os Blocos de Águas Subterrâneas {#workbook-conventions-for-the-groundwater-blocks}

- Toda célula de entrada das planilhas `General_Data` distribuídas tem um comentário que a explica.
- Os novos blocos usam células de entrada brancas com bordas laterais.
- No modo bypass, as mesmas chaves são campos de `InputData_Bypass.flags` (configurações da subsuperfície em camadas e de Feddes) e de `InputData_Bypass.general` (estado inicial do aquífero profundo).
- As variáveis de ambiente `HYDROPOL_SUBSURFACE_SCHEME`, `HYDROPOL_ENABLE_FEDDES`, `HYDROPOL_<NAME>` (para qualquer chave acima), `HYDROPOL_DEEP_INITIAL_BASEFLOW_MM_DAY`, `HYDROPOL_DEEP_MEAN_RECHARGE_MM_YEAR` e `HYDROPOL_DEEP_INITIAL_STATE_PATH` se sobrepõem à planilha. O Case Builder usa essas variáveis.
- Toda coluna de `SOIL_parameters.xlsx` também tem uma nota, incluindo como a subsuperfície em camadas trata `Sy` (ignorada), `kgsat` (alternativa para o $K_h$ do regolito) e `DTB (m)` (não lida).

## Decisões em Aberto {#open-decisions}

Estas questões estão pendentes. A tabela indica o comportamento atual de cada uma.

| Questão | Comportamento atual |
|---|---|
| `DTB_path` deve ser obrigatório no modo Excel quando a subsuperfície em camadas está ativa? | Não é obrigatório. Sem ele, o fundo da coluna recorre a `subsurface_depth_to_bedrock_m` e depois à profundidade do solo padrão, com aviso. |
| O que acontece com a coluna `DTB (m)` de `SOIL_parameters.xlsx`? | Ela não é lida. A profundidade do solo vem de `DTB_path`, ou é 1 m quando esse caminho está vazio. |
| Rasters de propriedades do solo podem ser informados no modo Excel? | A planilha não tem células para os rasters de propriedades do solo (`ThetaS_path`, `KsatNearSurface_path`, …), que o código lê de `InputPaths`. Só os rasters da base do solo e do regolito (T21:T28) têm células no Excel. |

---

## Notas

As descrições fornecidas aqui representam a função funcional de cada parâmetro em HydroPol2D.
As definições finais devem ser refinadas com base em:
- comentários da planilha
- estratégia de calibração
- contexto do aplicativo

Esta tabela serve como referência central para configuração do modelo.
