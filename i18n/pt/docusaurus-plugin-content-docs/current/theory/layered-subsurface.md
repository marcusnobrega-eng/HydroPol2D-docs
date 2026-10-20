---
title: Subsuperfície em Camadas
---
import useBaseUrl from '@docusaurus/useBaseUrl';

# Subsuperfície em Camadas (Solo sobre Regolito)

## 1. Visão Geral {#1-overview}

A subsuperfície em camadas é uma alternativa opcional ao esquema padrão de águas subterrâneas descrito na página [Modelo de Águas Subterrâneas](./groundwater-model). Ela substitui a coluna de solo de três camadas, em que o aquífero fica dentro do solo, por uma coluna de solo sobre regolito que vai até a profundidade do leito rochoso. As regras do lençol freático seguem o esquema de águas subterrâneas MMF do Noah-MP ([Miguez-Macho et al., 2007](https://doi.org/10.1029/2006JD008112)).

| Modelo | Chave | Padrão |
|---|---|---|
| HydroPol2D-Python | `vertical.subsurface.scheme: layered` | `legacy` |
| HydroPol2D (MATLAB) | `flag_layered_subsurface = 1` | `0` |

O esquema padrão não muda. Os dois modelos implementam a mesma coluna, e os kernels em MATLAB são verificados contra fixtures gerados no Python (veja [Validação das Águas Subterrâneas e da Recarga](../validation/groundwater-recharge)).

### 1.1 Por que o esquema em camadas existe {#11-why-the-layered-scheme-exists}

No esquema padrão, a profundidade do solo abriga ao mesmo tempo o solo e o aquífero. Um lençol freático em elevação reduz o armazenamento não saturado, e a água que deixa de caber volta à superfície como excesso de saturação (Seção 11 do [Modelo de Águas Subterrâneas](./groundwater-model#11-saturation-excess-correction-after-water-table-rise)). Onde o solo é raso e a recarga é alta, o lençol chega à superfície e a infiltração para. Simulações em escala de cidade mostraram esse comportamento em grandes partes do domínio.

O esquema em camadas muda dois pontos.

1. O aquífero se estende abaixo do solo, pelo regolito, até a profundidade do leito rochoso.
2. Um lençol freático em elevação preenche o espaço poroso vazio $\theta_s - \theta$ das camadas não saturadas. A água que já estava ali permanece no lugar, em vez de ser empurrada para a superfície.

---

## 2. Base do Solo e Profundidade até o Leito Rochoso {#2-soil-base-and-depth-to-bedrock}

Duas profundidades definem a coluna. Ambas são medidas para baixo a partir da superfície do terreno e marcam limites diferentes.

| Profundidade | O que marca | Papel na coluna em camadas |
|---|---|---|
| **Base do solo** | Onde terminam as propriedades do solo e começa o regolito | Fundo das três camadas de solo. Abaixo dela, as camadas usam parâmetros do regolito. |
| **Profundidade até o leito rochoso (DTB)** | Onde termina o aquífero | Fundo de toda a coluna (solo mais regolito), limitado a `max_depth_m` (padrão 50 m). |

A base do aquífero é, portanto,

$$
z_{\mathrm{base}} = z_{\mathrm{surf}} - \min\left(D_{\mathrm{DTB}},\,D_{\max}\right)
$$

e não $z_{\mathrm{surf}} - D_{\mathrm{soil}}$, como no esquema padrão.

**Exemplo.** Uma célula com base do solo a 1.5 m e DTB a 30 m tem camadas de solo de 0 a 1.5 m e camadas de regolito de 1.5 a 30 m. Com DTB a 80 m, a coluna para no teto de 50 m. Se a DTB for mais rasa que a base do solo, as camadas de solo são cortadas na DTB.

Cada profundidade vem da primeira fonte encontrada.

| Profundidade | Fontes, na ordem em que são procuradas |
|---|---|
| Base do solo | raster da base do solo; depois, o escalar `soil_base_depth_m` (padrão 2 m) |
| Profundidade até o leito rochoso | raster de DTB; depois, o escalar `depth_to_bedrock_m`; depois, a profundidade do solo do esquema padrão (com aviso) |

No esquema em camadas, a profundidade do solo do esquema padrão serve apenas como esse último recurso. A página [Profundidade até o leito rochoso](../inputs/dtb) descreve as fontes globais de dados para as duas profundidades.

---

## 3. Estrutura da Coluna {#3-column-structure}

<p align="center">
  <img src={useBaseUrl('/img/theory/layered-column.pt.svg')} width="720" alt="Coluna em camadas de solo sobre regolito, com uma árvore cujas raízes chegam à profundidade radicular, três camadas de solo, camadas de regolito que dobram de espessura, um único lençol freático com recarga, ascensão capilar e fluxo lateral, a base da coluna na profundidade até o leito rochoso limitada pelo teto e o reservatório linear profundo na rocha abaixo" />
</p>

<p align="center">
  <em>Figura 1. A coluna em camadas de uma célula (fora de escala). O lençol freático divide a camada em que se encontra. Os símbolos são definidos na tabela abaixo.</em>
</p>

**Símbolos da Figura 1**

| Símbolo | Significado | Unidades |
|---|---|---|
| $h$ | Carga do lençol freático, uma por célula | m |
| $\theta$ | Conteúdo de água da parte não saturada de uma camada | m³/m³ |
| $\theta_s$ | Conteúdo de água na saturação | m³/m³ |
| $\theta_r$ | Conteúdo de água residual | m³/m³ |
| $\theta_{fc}$ | Conteúdo de água na capacidade de campo, $\theta(\psi = -3.3\ \mathrm{m})$ por padrão | m³/m³ |
| $S_y$ | Rendimento específico (porosidade drenável), $\theta_s - \theta_{fc}$ | - |
| $S_e$ | Saturação efetiva, $(\theta - \theta_r)/(\theta_s - \theta_r)$ | - |
| $K_v$ | Condutividade hidráulica saturada vertical de uma camada | m/s |
| $K_r(S_e)$ | Condutividade relativa de Mualem–van Genuchten | - |
| $K(\theta)$ | Condutividade não saturada de uma camada, $K_v\,K_r(S_e)$ | m/s |
| $q$ | Fluxo de Darcy entre a camada não saturada mais baixa e o lençol freático; positivo para baixo (recarga), negativo para cima (ascensão capilar) | m/s |
| $\psi$ | Carga matricial da camada não saturada mais baixa; $\psi = 0$ no lençol freático | m |
| $\Delta z$ | Metade da espessura não saturada dessa camada | m |
| $T$ | Transmissividade para o fluxo lateral | m²/s |
| $K_h$ | Condutividade saturada horizontal de uma camada, incluindo o seu multiplicador lateral | m/s |
| $b$ | Espessura saturada de uma camada | m |
| $z_{\mathrm{surf}}$ | Elevação da superfície do terreno | m |
| $D_{\mathrm{DTB}}$ | Profundidade até o leito rochoso | m |
| 50 m | Teto padrão da profundidade da coluna, `max_depth_m` | m |
| $f_d$ | Fração da recarga enviada ao aquífero profundo, `deep_recharge_fraction` | - |
| $Q$ | Vazão de saída de um reservatório profundo | m³/s |
| $S$ | Armazenamento de um reservatório profundo | m³ |
| $\tau$ | Tempo de resposta dos reservatórios profundos, `deep_aquifer_response_time_days` | dias |

| Camada | Faixa de profundidade | Parâmetros |
|---|---|---|
| 1. Superficial | $0$ a $l_{\mathrm{top}}$ | curva de van Genuchten do solo, $K_{\mathrm{sat}}$ superficial |
| 2. Zona radicular | $l_{\mathrm{top}}$ até a profundidade radicular | curva de van Genuchten do solo, $K_{\mathrm{sat}}$ da zona radicular |
| 3. Transmissão | profundidade radicular até a base do solo | curva de van Genuchten do solo, $K_{\mathrm{sat}}$ de transmissão |
| 4, 5, … Regolito | base do solo até a base da coluna | curva de van Genuchten do regolito, $K_v$, $K_h$ |

As camadas de regolito seguem uma régua fixa a partir da base do solo, com espessuras de 0.25, 0.5, 1, 2, 4, 4, 4, … m (primeira espessura de 0.25 m, razão de crescimento 2, máximo de 4 m). A régua é cortada na base da coluna.

Três regras mantêm a coluna regular.

- **Número fixo de camadas.** Toda célula tem o mesmo número de camadas. As camadas abaixo da base da coluna têm espessura zero.
- **Camadas que colapsam.** Raízes mais rasas que $l_{\mathrm{top}}$ deixam a camada 2 vazia. Raízes mais profundas que a base do solo deixam a camada 3 vazia. Uma camada com menos de 5 mm de espessura é incorporada à camada de cima.
- **Um lençol freático por célula.** A carga $h$ se move através de limites fixos entre camadas. Ela divide a camada em que está em uma parte não saturada, acima, e uma parte saturada, abaixo.

### 3.1 Variáveis de estado {#31-state-variables}

| Variável | Significado | Unidades |
|---|---|---|
| $h$ | carga do lençol freático, uma por célula | m |
| $W_k$ | água acima de $\theta_r$ na parte não saturada da camada $k$ | mm |
| $b_k$ | espessura saturada da camada $k$ (abaixo de $h$, em $\theta_s$) | m |

O conteúdo de água da parte não saturada da camada $k$, com espessura não saturada $u_k$, é

$$
\theta_k = \theta_{r,k} + \frac{W_k}{u_k}
$$

---

## 4. Regras dos Processos {#4-process-rules}

### 4.1 Elevação do lençol freático {#41-rising-water-table}

A água adicionada no lençol freático preenche o espaço poroso vazio da parte não saturada da camada que contém o lençol. Um volume líquido $V$ (por unidade de área) eleva o lençol em

$$
\Delta z = \frac{V}{\theta_{s,k} - \theta_k}
$$

A água que já estava nessa camada permanece nela (MMF `UPDATEWTD`). A elevação só passa para a camada de cima depois que a camada atual fica cheia, de modo que erros de arredondamento não pulam uma camada ainda não preenchida. A água que sobra quando o lençol atinge o terreno sai para a superfície como exfiltração (afloramento).

### 4.2 Rebaixamento do lençol freático {#42-falling-water-table}

A água retirada no lençol freático o rebaixa. A espessura exposta pelo rebaixamento fica na capacidade de campo, $\theta_{fc} = \theta(\psi = -3.3\ \mathrm{m})$. Cada metro de rebaixamento libera, portanto,

$$
S_y = \theta_s - \theta_{fc}
$$

Essa é a porosidade drenável, com a retenção específica tomada como a capacidade de campo ([Lv et al., 2021](https://doi.org/10.1029/2020MS002270)). A água acima de $\theta_{fc}$ na espessura exposta drena depois, por gravidade. Um rebaixamento e uma elevação de mesmo volume são reversíveis. A retirada que não pode ser atendida antes da base da coluna é registrada como não atendida.

A carga na capacidade de campo é `capillary_field_capacity_head_m` (padrão 3.3 m). As camadas de solo sempre tomam $S_y$ da própria curva de retenção. As camadas de regolito também, a menos que um $S_y$ do regolito seja informado como escalar ou raster. Esse valor deve estar em $(0,\ \theta_s - \theta_r]$. Um conteúdo de equilíbrio por fatia, $\theta_{eq}(z)$, foi testado e descartado, porque a água liberada tende a zero em fatias finas.

### 4.3 Drenagem entre camadas {#43-drainage-between-slots}

A água drena para baixo pelas camadas não saturadas sob gradiente unitário, como no modelo cinemático de zona não saturada UZF1 ([Niswonger et al., 2006](https://pubs.usgs.gov/tm/2006/tm6a19/)). O fluxo que sai da camada $k$ é

$$
q_k = K_{v,k}\,K_r(S_{e,k})
$$

onde $K_r$ é a condutividade relativa de Mualem–van Genuchten. Cada fluxo é limitado pela água da camada doadora e pelo espaço livre na próxima camada abaixo que tenha parte não saturada. Os fluxos usam os estados do início do passo. O passo pode ser dividido em `drainage_substeps` (padrão 1). A camada não saturada mais baixa não drena por essa regra. Ela troca água com o lençol freático (Seção 4.4).

### 4.4 Fluxo de Darcy no lençol freático {#44-darcy-flux-at-the-water-table}

Entre a camada não saturada mais baixa e o lençol freático, o HydroPol2D usa um fluxo de Darcy, positivo para baixo,

$$
q = K(\theta_k)\left(\frac{\psi_k}{\Delta z} + 1\right),
\qquad \Delta z = \tfrac{1}{2}u_k
$$

onde $\psi_k$ é a carga matricial da camada, com $\psi = 0$ no lençol freático. Um fluxo para baixo é recarga, limitada pela água da camada. Um fluxo para cima é ascensão capilar, limitada pelo espaço livre da camada e pela água drenável abaixo do lençol.

**Fluxo implícito (padrão).** Em uma faixa não saturada fina sobre um lençol raso, o fluxo explícito é rígido (stiff). Em passos longos, ele ultrapassa a solução e troca de sinal. Por padrão, o HydroPol2D calcula o fluxo no fim do passo com um único passo de Euler implícito linearizado por célula, sem iteração. Transferir $q\,\Delta t$ drena a camada em $q\,\Delta t$ e eleva o lençol em $q\,\Delta t / S_y$. Assim,

$$
q = \frac{q_0}{1 + \Delta t\,\max\!\left(\dfrac{\partial q}{\partial W} - \dfrac{1}{S_y}\dfrac{\partial q}{\partial h},\ 0\right)}
$$

onde $q_0$ é o fluxo explícito. Só a parte amortecedora da derivada é mantida. O CLM5 também resolve de forma implícita o fluxo no lençol freático. Em passos curtos, as duas formas coincidem.

| Teste: lençol a 15 cm de profundidade, solo arenoso úmido, passos de 1 h, contra uma referência de 36 s | Trocas de sinal | Erro |
|---|---:|---:|
| Fluxo explícito | 2 | 53 % |
| Fluxo implícito | 0 | abaixo de 0.1 % |

A chave é `implicit_water_table_flux` (padrão `true`). O fluxo implícito existe apenas no HydroPol2D-Python. O modelo MATLAB mantém o fluxo explícito, para que os seus fixtures de paridade continuem coincidindo. A versão em MATLAB está planejada.

### 4.5 Fluxo lateral {#45-lateral-flow}

O fluxo lateral usa a aproximação de Dupuit–Forchheimer com uma transmissividade em camadas

$$
T = \sum_k K_{h,k}\,b_k
$$

A transmissividade na face é a média aritmética das duas células, e o fluxo na face é $Q = -\bar{T}\,\dfrac{\Delta h}{\Delta x}\,w$ para uma face de largura $w$. A tabela abaixo dá a condutividade horizontal de cada camada.

| Camadas | $K_h$ |
|---|---|
| Solo (1–3) | $K_{\mathrm{sat}}$ do solo × `soil_lateral_anisotropy` × `soil_lateral_conductivity_multiplier` |
| Regolito (4, …) | $K_h$ do regolito × `regolith_lateral_conductivity_multiplier` |

Os dois multiplicadores valem 1 por padrão. A [calibração por recessão das águas subterrâneas](../calibration/groundwater-recession) ajusta esses fatores. Se nenhum $K_h$ do regolito for informado, o modelo usa o $K_{\mathrm{sat}}$ das águas subterrâneas do esquema padrão.

O fluxo lateral avança em subpassos explícitos limitados por

$$
\Delta t \le C_{\mathrm{gw}}\,\frac{\min(\Delta x,\Delta y)^2\,S_y}{4\,T}
$$

com $C_{\mathrm{gw}}$ = `groundwater_courant` (padrão 0.25) e $S_y$ tomado na posição do lençol freático. A saída de água de uma célula é limitada pela sua água drenável. Os volumes líquidos passam pelas regras de elevação e rebaixamento acima, de modo que cargas, água não saturada e exfiltração permanecem consistentes. As células de carga fixa (Dirichlet) mantêm a sua carga, e a troca nelas é registrada como entrada pelo contorno. O fluxo lateral roda no agendador das águas subterrâneas (Seção 2.1 do [Modelo de Águas Subterrâneas](./groundwater-model#21-asynchronous-scheduler)).

### 4.6 Absorção de água pelas raízes {#46-root-water-uptake}

Com o estresse de Feddes ativo, a ET do solo é reduzida por $\alpha(h)$ em cada camada com raízes ([Modelo Hidrológico, Seção 3.5](./hydrologic-model#35-feddes-root-water-uptake-stress)). Sem Feddes, as raízes que chegam abaixo do lençol freático retiram dele a parte não atendida da demanda. Essa parte corresponde à fração saturada da profundidade radicular e é limitada pela água drenável.

### 4.7 Aquífero profundo {#47-deep-aquifer}

Com o aquífero profundo ativo, uma fração fixa da recarga que chegaria ao lençol freático vai, em vez disso, para os reservatórios lineares profundos ([Modelo de Águas Subterrâneas, Seção 13](./groundwater-model#13-deep-aquifer)).

---

## 5. Ordem das Operações {#5-order-of-operations}

A troca vertical roda a cada passo da superfície. O fluxo lateral roda quando o agendador das águas subterrâneas dispara uma atualização.

1. Infiltração nas camadas de solo (a infiltração de Darcy do [Modelo Hidrológico](./hydrologic-model#4-infiltration)).
2. Evaporação de água livre e, em seguida, ET do solo, com estresse de Feddes opcional.
3. Cascata de drenagem entre as camadas não saturadas.
4. Fluxo de Darcy no lençol freático, como recarga ou ascensão capilar.
5. Separação da parcela da recarga destinada ao aquífero profundo, se ele estiver ativo.
6. Atualização do lençol freático. A exfiltração vai para a superfície.
7. Troca rio-águas subterrâneas, se ativa.
8. Fluxo lateral, quando o agendador dispara.

Na malha Voronoi, as HRUs de uma célula compartilham o terreno, a base da coluna e a carga da célula. A troca vertical das HRUs é somada por célula e aplicada na atualização das águas subterrâneas, por bisseção na curva de armazenamento da célula. O fluxo lateral usa a transmissividade ponderada pela área.

O esquema em camadas também aceita a troca rio-águas subterrâneas nos motores de malha (células de leito de rio resolvidas e canais de Neal) e a exfiltração de infraestrutura verde para as camadas de solo.

---

## 6. Motores de Cálculo e Velocidade {#6-engines-and-speed}

| Motor de cálculo | HydroPol2D-Python | HydroPol2D (MATLAB) |
|---|---|---|
| Grade estruturada | `core/layered_vertical.py` | `flag_layered_subsurface = 1` |
| Malha Voronoi | NumPy (`voronoi_layered.py`) e JAX (`mesh_gpu/layered.py`); paridade NumPy–JAX de cerca de $10^{-15}$ em termos relativos | executor Voronoi (`config.layered_subsurface`) |

No Python, o passo em camadas da grade estruturada é compilado uma vez por caso. Os resultados são idênticos aos do passo não compilado. O perfilamento feito em 2026-10-19 deu os tempos abaixo.

| Medida | Antes da compilação | Depois da compilação |
|---|---:|---:|
| Passo em camadas, 31 passos | 2.9 s | 0.09 s |
| Uma hora com roteamento | 4.6 s | 0.7 s |

Depois da compilação, o esquema em camadas roda mais rápido que o esquema padrão. `HYDROPOL2D_LAYERED_JIT=0` executa o passo operação por operação, como referência.

Relógios separados para o solo e para as águas subterrâneas (passo de tempo multitaxa, como no MIKE SHE, GSSHA, Noah-MP e CLM5) foram avaliados e estão suspensos. Depois da compilação, o roteamento superficial consome a maior parte do tempo de execução, e um relógio separado para o solo ganharia pouco.

---

## 7. Saídas {#7-outputs}

| Saída | Python, grade estruturada | Python, malha | MATLAB | Significado |
|---|---|---|---|---|
| Profundidade das águas subterrâneas | `groundwater_depth_map_m` | `groundwater_depth_face_m` | `Maps.Hydro.GWdepth_save` | Profundidade do lençol freático abaixo do terreno (m), limitada à base da coluna |
| Base da coluna | `column_base_depth_m` | `column_base_depth_face_m` | `Maps.Hydro.ColumnBaseDepth_m` | $\min(D_{\mathrm{DTB}}, D_{\max})$ abaixo do terreno (m), estática |
| Saturação da zona radicular e da zona de transmissão | `root_zone_saturation_map`, `transmission_zone_saturation_map` | - | - | $\theta/\theta_s$ da parte não saturada das camadas 2 e 3; NaN onde a camada está saturada |
| Armazenamento vadoso profundo | `deep_vadose_storage_map_mm` | `deep_vadose_storage_face_mm` | `Maps.Hydro.DeepVadose_save` | Água acima de $\theta_r$ na parte não saturada das camadas de regolito (mm) |

A espessura saturada é a profundidade da base da coluna menos a profundidade das águas subterrâneas. Ela não é salva. Rasters por camada e fatias por profundidade ainda não são gravados. Os estados por camada ficam no estado do modelo e nos checkpoints.

---

## 8. Configuração {#8-configuration}

HydroPol2D-Python:

```yaml
vertical:
  feddes: {enabled: true, h1_m: -0.1, h2_m: -0.25, h3_m: -4.0, h4_m: -80.0}
  groundwater_courant: 0.25          # lateral-flow substep safety factor
  capillary_field_capacity_head_m: 3.3
  subsurface:
    scheme: layered
    soil_base_depth_m: 2.0           # or static.soil_base_depth_path
    depth_to_bedrock_m: 20.0         # or static.depth_to_bedrock_path
    max_depth_m: 50.0
    deep_layers: {first_thickness_m: 0.25, growth_ratio: 2.0, max_thickness_m: 4.0}
    regolith_theta_s: 0.35
    regolith_theta_r: 0.05
    regolith_alpha_vg_m_inverse: 2.0
    regolith_n_vg: 1.5
    regolith_ksat_v_mm_h: 5.0
    regolith_ksat_h_mm_h: null       # null: vertical.groundwater_ksat_mm_h
    regolith_specific_yield: null    # null: theta_s - theta_fc of the regolith curve
    soil_lateral_anisotropy: 1.0
    soil_lateral_conductivity_multiplier: 1.0
    regolith_lateral_conductivity_multiplier: 1.0
    implicit_water_table_flux: true
    drainage_substeps: 1
```

Um raster `static.regolith_<name>_path` prevalece onde for finito. O escalar preenche o restante.

HydroPol2D (MATLAB): `flag_layered_subsurface` e `flag_feddes` na aba `Flags`, e os blocos "Layered Subsurface", "Feddes Root-Water Stress" e "Lateral Conductivity Multipliers" de `General_Data`. Veja [Parâmetros de configuração](../configuration/general_data) e [Bandeiras do modelo](../configuration/flags).

---

## 9. Limites Conhecidos {#9-known-limits}

- **Sem fluxo lateral de água suspensa.** Uma camada de solo saturada sobre regolito não saturado não escoa lateralmente.
- **Sem tabela de classes de regolito.** Os parâmetros do regolito são escalares ou rasters.
- **Sem saídas raster por camada.**
- **Circulação no lençol freático.** A regra de rebaixamento na capacidade de campo e o fluxo de Darcy calculado com a média da camada, juntos, fazem a água circular para cima e para baixo perto de um lençol raso. A troca líquida fica perto de zero, mas a circulação infla a ascensão capilar bruta e a recarga bruta no balanço de água. A questão está em aberto e ainda não foi corrigida.
- **Laço compilado para cidades.** O laço compilado do HydroPol2D-Python para simulações de cidades ainda não roda o esquema em camadas com fluxo lateral de águas subterrâneas.
- **Fluxo implícito apenas no Python.** O modelo MATLAB ainda usa o fluxo explícito no lençol freático.

---

## 10. Fontes {#10-sources}

- Miguez-Macho, G., Fan, Y., Weaver, C. P., Walko, R., and Robock, A. (2007). Incorporating water table dynamics in climate modeling: 2. Formulation, validation, and soil moisture simulation. *Journal of Geophysical Research*, 112, D13108. [doi:10.1029/2006JD008112](https://doi.org/10.1029/2006JD008112)
- Noah-MP, [`GroundWaterMmfMod.F90`](https://github.com/NCAR/noahmp/blob/master/drivers/hrldas/GroundWaterMmfMod.F90).
- Niswonger, R. G., Prudic, D. E., and Regan, R. S. (2006). Documentation of the Unsaturated-Zone Flow (UZF1) Package for modeling unsaturated flow between the land surface and the water table with MODFLOW-2005. USGS Techniques and Methods 6-A19. [pubs.usgs.gov/tm/2006/tm6a19](https://pubs.usgs.gov/tm/2006/tm6a19/)
- Lv, M., et al. (2021). A comprehensive review of specific yield in land surface and groundwater studies. *Journal of Advances in Modeling Earth Systems*, 13, e2020MS002270. [doi:10.1029/2020MS002270](https://doi.org/10.1029/2020MS002270)
- Feddes, R. A., Kowalik, P. J., and Zaradny, H. (1978). *Simulation of Field Water Use and Crop Yield*. Pudoc, Wageningen.
