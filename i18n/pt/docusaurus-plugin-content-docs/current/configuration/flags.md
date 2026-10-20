---
title: Bandeiras modelo
---

# Bandeiras modelo

HydroPol2D é controlado por meio de sinalizadores binários e categóricos definidos em `General_Data.xlsx`. Esta página documenta o comportamento público exposto por esses sinalizadores e destaca onde um sinalizador ativa um caminho padrão validado versus um caminho de diagnóstico ou experimental.

---

## Limite e sinalizadores de forçamento

| Bandeira | Descrição |
|---|---|
| $\mathrm{flag\_rainfall}$ | Ativa o forçamento da chuva sobre o domínio. |
| $\mathrm{flag\_spatial\_rainfall}$ | Usa chuvas distribuídas espacialmente em vez de chuvas uniformes. |
| $\mathrm{flag\_ETP}$ | Ativa o cálculo da evapotranspiração do forçamento meteorológico. |
| $\mathrm{flag\_input\_rainfall\_map}$ | Usa entrada de precipitação baseada em raster. |
| $\mathrm{flag\_rainfall\_multiple\_runs}$ | Em desenvolvimento. |
| $\mathrm{flag\_data\_source}$ | Em desenvolvimento. |
| $\mathrm{flag\_inflow}$ | Ativa as condições de contorno do hidrograma de afluência. |
| $\mathrm{flag\_satellite\_rainfall}$ | Usa produtos de chuva derivados de satélite. |
| $\mathrm{flag\_alternated\_blocks}$ | Ativa o método de design-storm de Bloco Alternado. |
| $\mathrm{flag\_huff}$ | Ativa o método de distribuição de tempestade Huff. |
| $\mathrm{flag\_stage\_hydrograph}$ | Aplica condições de limite de estágio (nível de água). |
| $\mathrm{flag\_input\_ETP\_map}$ | Usa entradas de evapotranspiração baseadas em raster. |

---

## Sinalizadores de processo e roteamento

| Bandeira | Descrição |
|---|---|
| $\mathrm{flag\_infiltration}$ | Ativa a infiltração no solo e o armazenamento vadoso. |
| $\mathrm{flag\_groundwater\_modeling}$ | Ativa a recarga das águas subterrâneas e o acoplamento local dos lençóis freáticos. Com o solo em camadas ativado, isso segue o caminho vadoso-água subterrânea em camadas padrão atual. |
| $\mathrm{flag\_groundwater\_async}$ | Usa atualizações assíncronas de águas subterrâneas saturadas, mantendo a troca vadosa acoplada a cada etapa da superfície. Recomendado quando as águas subterrâneas estão ativas. |
| $\mathrm{groundwater\_target\_dt\_min}$ | Intervalo alvo de atualização das águas subterrâneas em minutos. |
| $\mathrm{groundwater\_min\_dt\_min}$ | Intervalo mínimo de atualização das águas subterrâneas em minutos. |
| $\mathrm{groundwater\_max\_head\_change\_m}$ | Alteração máxima acumulada da carga subterrânea antes de forçar uma atualização. |
| $\mathrm{groundwater\_courant}$ | Fator de segurança usado no limite explícito do intervalo de tempo das águas subterrâneas. |
| $\mathrm{flag\_capillary\_rise}$ | Permite a ascensão capilar em camadas de águas subterrâneas rasas para o armazenamento vadoso. |
| $\mathrm{flag\_baseflow}$ | Ativa o roteamento lateral de águas subterrâneas 2D Boussinesq. |
| $\mathrm{flag\_layered\_subsurface}$ | Substitui a coluna de solo de três camadas sobre um único aquífero pela [coluna em camadas de solo sobre regolito](../theory/layered-subsurface). Padrão `0`. As configurações ficam nos blocos "Layered Subsurface" e "Lateral Conductivity Multipliers" de [Parâmetros de configuração](./general_data). |
| $\mathrm{flag\_feddes}$ | Adiciona o [estresse de Feddes na absorção de água pelas raízes](../theory/hydrologic-model#35-feddes-root-water-uptake-stress) à ET do solo, em qualquer um dos esquemas de subsuperfície. Padrão `0`. |
| $\mathrm{flag\_deep\_aquifer}$ | Ativa o [aquífero profundo](../theory/groundwater-model#13-deep-aquifer), com um reservatório linear por sub-bacia alimentado pela fração `deep_recharge_fraction` da recarga. Padrão `0`. |
| $\mathrm{flag\_snow\_modeling}$ | Ativa acúmulo, derretimento, sublimação, densidade e profundidade de neve por LULC. Requer forçante meteorológica interna: `flag_ETP = 1` e `flag_input_ETP_map = 0`. |
| $\mathrm{flag\_waterquality}$ | Ativa o transporte com qualidade da água. |
| $\mathrm{flag\_wq\_model}$ | Seleciona o modelo de acúmulo/lavagem de poluentes. |
| $\mathrm{flag\_human\_instability}$ | Ativa diagnósticos de instabilidade humana. Os modos implementados documentados publicamente são `1` e `3`; o modo `2` não está implementado. |
| $\mathrm{flag\_reservoir}$ | Ativa o reservatório ou a lógica interna de controle hidráulico. |
| $\mathrm{flag\_critical}$ | Aplica um limitador de fluxo crítico quando suportado pela família de roteamento. |
| $\mathrm{flag\_boundary}$ | Aplica todas as células de limite como células de saída. |
| $\mathrm{flag\_neglect\_infiltration\_river}$ | Desativa a infiltração nas células do rio. |
| $\mathrm{flag\_real\_time\_satellite\_rainfall}$ | Permite a ingestão de chuvas por satélite em tempo real com persa. |
| $\mathrm{flag\_dam\_break}$ | Em desenvolvimento. |
| $\mathrm{flag\_river\_rasters}$ | Usa entradas de geometria de rio baseadas em raster. |
| $\mathrm{flag\_spatial\_albedo}$ | Usa albedo distribuído espacialmente em vez de valores uniformes. |
| $\mathrm{flag\_DTM}$ | Usa correções ou processamento de modelo digital de terreno. |
| $\mathrm{flag\_abstraction}$ | Ativa processos de captação ou retirada de água. |
| $\mathrm{flag\_WQ\_Rasters}$ | Usa entradas de poluentes baseadas em raster. |

---

## Sinalizadores de família de roteamento

| Bandeira | Descrição |
|---|---|
| $\mathrm{flag\_inertial}$ | Ativa o solucionador inercial local em águas rasas. Esta é a família de roteamento padrão recomendada. |
| $\mathrm{flag\_full\_momentum}$ | Ativa o solucionador de impulso total para águas rasas. Use como uma alternativa às outras famílias de roteamento principais, e não em combinação com elas. |
| $\mathrm{flag\_diffusive}$ | Ativa o roteamento difusivo D4 impulsionado pela inclinação da superfície da água. |
| $\mathrm{flag\_kinematic}$ | Ativa o roteamento cinemático D4 orientado pela inclinação do leito e pela profundidade do doador. |
| $\mathrm{flag\_CA}$ | Ativa o roteamento do Cellular Automata. |
| $\mathrm{flag\_D8}$ | Ativa um caminho de roteamento D8 secundário. Isto deve ser tratado como um escopo limitado, em vez de uma família de teorias paralelas completas. |
| $\mathrm{flag\_neal\_channel}$ | Ativa a representação retangular de canal embutido de Neal (2012) em grade estruturada. Requer roteamento inercial local. |
| $\mathrm{flag\_structured\_lookup\_subgrid}$ | Ativa tabelas dependentes do nível para células e faces em grade estruturada. Este modo permanece condicionado à paridade MATLAB-Python. |
| $\mathrm{flag\_voronoi\_subgrid}$ | Ativa as tabelas de células e faces do HydroBathyDEM em uma malha Voronoi. |
| $\mathrm{flag\_voronoi}$ | Seleciona a topologia de malha Voronoi. É independente de `flag_voronoi_subgrid`, que seleciona a representação hidráulica. |
| $\mathrm{flag\_numerical\_scheme}$ | Seleciona a variante do esquema inercial local: `1` Bates, `2` contra o vento, `3` centralizado. Aplica-se à família inercial, não ao roteamento de impulso total, difusivo, cinemático ou CA. |
| $\mathrm{flag\_outlet\_type}$ | Tratamento de saída: fluxo normal `1`, fluxo crítico `2`. |
| $\mathrm{flag\_adaptive\_timestepping}$ | Seleciona controle de passo de tempo adaptativo. |

---

## Configuração do modelo subgrade de Neal (2012)

O modo de canal subgrade aceito segue [Neal et al. (2012)](https://doi.org/10.1029/2012WR012514). Use a seguinte combinação:

| Bandeira | Valor necessário |
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

As células com canal precisam de `RiverWidths_path` e `RiverDepths_path`. A largura e a profundidade devem ser positivas, e a largura do canal deve ser menor que a resolução da célula. O coeficiente de Manning do canal é definido pela entrada de rugosidade do rio ou dentro das margens. A rugosidade do uso e cobertura da terra fornece o coeficiente de Manning da planície.

O solver calcula separadamente as vazões do canal e da planície em cada face ortogonal e atualiza o armazenamento em termos de volume. A formulação e o intervalo de validação são descritos em [Modelo hidrodinâmico](../theory/hydrodynamic-model) e [Validação do modelo subgrade de Neal (2012)](../validation/neal-subgrid).

---

## Sinalizadores de desempenho

| Bandeira | Descrição |
|---|---|
| $\mathrm{flag\_GPU}$ | Ativa a aceleração da GPU. |
| $\mathrm{flag\_single}$ | Usa aritmética de precisão simples para otimização de desempenho. |

---

## Sinalizadores de condição inicial

| Bandeira | Descrição |
|---|---|
| $\mathrm{flag\_warmup}$ | Ativa o aquecimento do modelo para estabilização do estado. |
| $\mathrm{flag\_initial\_buildup}$ | Inicializa as condições de acúmulo de poluentes. |

---

## DEM e sinalizadores de processamento de terreno

| Bandeira | Descrição |
|---|---|
| $\mathrm{flag\_resample}$ | Ativa a reamostragem raster para uma resolução alvo. |
| $\mathrm{flag\_smoothening}$ | Aplica suavização DEM. |
| $\mathrm{flag\_trunk}$ | Suaviza apenas o tronco principal do rio. |
| $\mathrm{flag\_fill\_DEM}$ | Preenche as depressões do DEM para obter consistência hidrológica. |
| $\mathrm{flag\_smooth\_cells}$ | Aplica suavização de terreno em nível de célula. |
| $\mathrm{flag\_reduce\_DEM}$ | Reduz a elevação do DEM nas células do rio para levar em conta a batimetria do canal. |

---

## Sinalizadores de saída e utilidade

| Bandeira | Descrição |
|---|---|
| $\mathrm{flag\_export\_maps}$ | Permite a exportação de saídas raster. |
| $\mathrm{flag\_dashboard}$ | Ativa saídas ou visualização em estilo de painel. |
| $\mathrm{flag\_elapsed\_time}$ | Acompanha o tempo de execução da simulação. |
| $\mathrm{flag\_obs\_gauges}$ | Ativa a extração de saída em medidores de observação. |

---

## Notas

- Somente uma família de roteamento principal deve estar ativa por vez: `flag_full_momentum`, `flag_inertial`, `flag_diffusive`, `flag_kinematic` ou `flag_CA`.
- Selecione no máximo uma formulação subgrid: canal Neal, lookup estruturado ou lookup Voronoi.
- O modo de canal de Neal (2012) requer roteamento inercial local e `flag_neal_channel = 1`.
- `flag_voronoi = 1` seleciona a topologia; `flag_voronoi_subgrid = 1` também ativa a hidráulica lookup Voronoi.
- `flag_subgrid` e `flag_overbanks` antigos são aceitos apenas pela camada de migração e geram aviso explícito.
- `flag_D8` deve ser tratado como escopo secundário/limitado, e não como outra família de roteamento pronta para relatório.
- A programação assíncrona das águas subterrâneas e a ascensão capilar são comportamentos de configuração pública, e não detalhes internos ocultos.
- `flag_deep_aquifer`, `flag_layered_subsurface` e `flag_feddes` ocupam as linhas 37 a 39 da aba `Flags` (coluna E) nas planilhas distribuídas.
- Os parâmetros de neve são definidos por classe na tabela LULC. `Initial_SWE_path` e `Initial_Snow_Depth_path` são rasters iniciais opcionais.
- O modo de instabilidade humana `2` não está implementado e não deve ser apresentado como um método público disponível.
