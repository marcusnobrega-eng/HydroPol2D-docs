---
title: Estado da Fase 1
---
import useBaseUrl from '@docusaurus/useBaseUrl';

# Estado da validacao da Fase 1

A tabela abaixo resume o estado atual de validação dos módulos do HydroPol2D. Métricas detalhadas, figuras e descrições dos casos estão disponíveis no <a href={useBaseUrl('/reports/validation_report.pdf')}>relatório de validação da Fase 1</a>, na página [Visão geral da validação](./overview) e na [Validação do modelo subgrade de Neal (2012)](./neal-subgrid).

| Modulo | Estado atual | Evidencia usada |
|---|---|---|
| Interceptacao pelo dossel | Pronto para relatorio | Referencia independente de armazenamento em bucket e balanco de massa exato. |
| Modulo de neve | Pronto para relatorio | Particao chuva-neve, derretimento, sublimacao e bookkeeping de SWE. |
| Infiltracao | Pronto para relatorio em casos controlados | Testes analiticos e controlados com solos em camadas. |
| Evapotranspiracao | Pronto para relatorio | Calculos independentes de ET e verificacoes de limites de extracao. |
| Groundwater e recarga | Pronto para relatorio | Verificacoes analiticas de subida do nivel, equivalencia do scheduler, bookkeeping de ascensao capilar e benchmarks analiticos de encosta. |
| Hidrodinamica full momentum | Pronto para relatorio | Benchmarks de tilted plane, V-tilted, Ritter dam-break, non-breaking wave e contornos. |
| Hidrodinamica local inertial | Pronto para relatorio com ressalvas do metodo | Testes de tilted plane, V-tilted, contornos de stage e conservacao. |
| Cellular automata | Pronto para relatorio em conservacao e bookkeeping | Testes V-tilted, plane e contornos. |
| Roteamentos kinematic e diffusive | Prontos para relatorio em benchmarks controlados corrigidos | Testes de tilted plane, conservacao em V-tilted e bookkeeping em contornos de stage. |
| Modelo subgrade de Neal (2012) | Pronto para relatório em casos controlados de canal e extravasamento | Referências numéricas em grade fina para escoamento dentro das margens, canal composto permanente e transiente, ativação das margens e extensão máxima da inundação. A recessão tardia permanece limitada. |
| Reservatorios e estruturas de controle | Pronto para relatorio | ODE analitica de deplecao por curva-chave e balanco volumetrico exato. |
| Contorno com hidrografa de entrada | Pronto para relatorio | Volume prescrito de hidrografa e bookkeeping de armazenamento e saida. |
| Contorno com stage hydrograph | Pronto para relatorio | Aplicacao prescrita de nivel e resposta volumetrica. |
| Chuva espacial em raster | Pronto para relatorio | Pilha raster pequena com chuva exata por celula e alvos de volume no dominio. |
| Qualidade da agua | Pronto para relatorio | Washoff analitico em massa com escala conceitual inspirada no SWMM. |
| Risco humano e instabilidade | Pronto para relatorio | Referencias independentes de limiares e classificacao por equilibrio de forcas. |

## Ressalvas importantes

Pronto para relatorio significa que o modulo passou em testes controlados de equacoes e dinamica da Fase 1. Isso nao significa, por si so, que o modulo esteja calibrado para um sitio de campo especifico.

Casos com referencia numerica ajudam a ganhar confianca no comportamento da implementacao, mas sao evidencias mais fracas do que verdades analiticas ou independentes.
