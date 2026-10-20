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
Se `flag_reduce_dem` estiver ativado, a elevação das células do rio será reduzida para compensar a batimetria do rio. Um conjunto de 4 parâmetros é então necessário para descrever a largura e a profundidade do fluxo. Estes parâmetros são válidos para converter a área de acumulação de fluxo [$\mathrm{km^2}$] em profundidade de fluxo [$\mathrm{m}$] e largura [$\mathrm{m}$].| Variável | Unidades | Descrição |
|----------|------|-------------|
| $\alfa_1$ | - | Coeficiente empírico que controla a escala da geometria do canal |
| $\alfa_2$ | - | Coeficiente secundário para relações de geometria hidráulica |
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
| $\mathrm{DTB\_path}$ | - | Caminho para raster da profundidade ao leito rochoso |
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

## Notas

As descrições fornecidas aqui representam a função funcional de cada parâmetro em HydroPol2D.
As definições finais devem ser refinadas com base em:
- comentários da planilha
- estratégia de calibração
- contexto do aplicativo

Esta tabela serve como referência central para configuração do modelo.
