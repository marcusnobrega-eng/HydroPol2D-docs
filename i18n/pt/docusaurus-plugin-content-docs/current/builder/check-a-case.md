---
title: Verificar um caso
---
import useBaseUrl from '@docusaurus/useBaseUrl';

# Verificar um caso

Toda montagem termina com a verificação prévia (preflight). **Check a case** a roda de novo em
qualquer caso preparado, sem montá-lo de novo: por exemplo, depois que você moveu um caso, editou um
dos seus arquivos ou o preparou em outro dia.

1. Abra **Check a case**.
2. Cole a pasta do caso em **Prepared case directory**.
3. Clique em **Run preflight**.

A página então diz "Ready to run: all preflight checks passed." ou então "Not ready to run." e,
abaixo, a lista de problemas. Para um caso pronto, os valores verificados ficam em um painel
recolhido, e os painéis de simulação vêm em seguida ([Rodar o caso](run-the-case)). O
**Preflight log** guarda as mensagens.

## O que ela verifica {#what-it-checks}

| Grupo | Verificações |
|---|---|
| Arquivos | todo mapa e toda série de que o modelo escolhido precisa estão lá, e os arquivos de modelo (`case.yaml`, `run_case.m` e as suas entradas) estão completos |
| Grades | todo mapa tem a grade de `DEM.tif` e cobre todas as células ativas, e a malha está completa nos casos quadtree e Urban Area Only |
| Valores | nenhuma profundidade até a rocha, umidade do solo, área foliar ou chuva negativa, albedo e fração impermeável entre 0 e 1, águas subterrâneas entre a superfície e a rocha, larguras e profundidades dos rios presentes |
| Tempo | todos os passos de tempo da chuva, do início do aquecimento ao fim, em uma única grade sobre todo o domínio, e um clima que cobre o período |
| Terreno | o relatório do HydroBathyDEM existe e o seu terreno é aceito para uma simulação |
| Domínio | num caso Catchment, a bacia final e o primeiro contorno do HydroSHEDS diferem por menos de um fator de dois |
| Contornos | em Urban Area Only, cada borda externa tem exatamente uma condição, e todo contorno GloFAS ou GTSM ligado tem dados |

O relatório completo é `quality_report/preflight.json`, com `ready_to_run`, a lista de `failures` e
os valores verificados.

Não rode um caso que não está pronto. Leia os problemas, corrija as entradas (muitas vezes
preparando o caso de novo com outras configurações) e verifique de novo. Uma verificação aprovada diz
que o caso está completo e consistente. Ela não é uma calibração nem uma validação do modelo.

## Calibração das águas subterrâneas {#groundwater-calibration}

Quando um caso Catchment foi preparado com **Shallow-aquifer Ksat,h and Sy** em **Calibrate from
observed streamflow**, a página mostra **Calibrate groundwater parameters** para ele. A calibração
ajusta uma condutividade horizontal e um rendimento específico do aquífero raso às recessões de um
hidrograma observado, depois os grava no caso e o verifica de novo.

| Configuração | O que ela define |
|---|---|
| **Observed streamflow** | **USGS gauge** (com **USGS gauge ID**, por exemplo 02145910) ou **Local CSV** (com **Observed-discharge CSV**, colunas `date` e `observed_discharge_m3_s`) |
| **Observation start**, **Observation end** | o período do registro a usar |
| **Ksat,h candidates (m/s)**, **Sy candidates** | os valores a testar (casos em camadas: **Soil Kh multipliers** e **Regolith Kh multipliers**) |
| **Saved shallow-flow fraction** | o estado inicial é salvo quando a vazão rasa cai para esta parcela da vazão total (0,05) |
| **HydroPol2D Python folder** | uma pasta que contém o HydroPol2D Python |

**Run and apply groundwater calibration** a inicia em segundo plano, e **Refresh calibration
status** atualiza a página. A vazão observada é filtrada com o método de Lyne-Hollick, as recessões
formam uma curva mestra de recessão, e um experimento de águas subterrâneas em uma grade regular
ajusta os dois valores. Quando termina, a página mostra "Groundwater calibration was applied and the
case passed preflight.", o **Ksat,h** e o **Specific yield** ajustados, o dia de recessão escolhido
e uma figura das recessões observadas e calibradas. O caso não pode ser rodado antes que essa
verificação final passe.

A calibração precisa do HydroPol2D Python. O app não o baixa, então escolha uma pasta que já o
contenha. O método está descrito em
[Calibração por Recessão das Águas Subterrâneas](../calibration/groundwater-recession).
