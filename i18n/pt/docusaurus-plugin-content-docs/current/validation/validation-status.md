---
title: Estado da validação
---
import useBaseUrl from '@docusaurus/useBaseUrl';

# Estado da validação

O <a href={useBaseUrl('/reports/validation_report.pdf')}>relatório de validação</a> documenta os métodos, as métricas e os resultados da suíte de validação do HydroPol2D. A tabela apresenta um índice conciso das evidências atuais.

<div style={{margin: '1rem 0 1.5rem 0'}}>
  <a className="button button--primary button--lg" href={useBaseUrl('/reports/validation_report.pdf')}>
    Abrir o relatório de validação
  </a>
</div>

| Módulo | Estado | Evidência |
|---|---|---|
| Interceptação pelo dossel | Validado | Referência independente de armazenamento em dossel e balanço exato de massa. |
| Neve | Validado | Parâmetros por LULC, mapas iniciais opcionais, refinamento temporal, equivalência entre planilha e script, e balanço do evento em V. |
| Infiltração | Validado | Casos analíticos e de solo estratificado em domínios de coluna e V. |
| Evapotranspiração | Validado | Cálculos independentes de ET de referência e limites de extração. |
| Águas subterrâneas e recarga | Validado | Testes de elevação do nível freático, agendamento, ascensão capilar e encostas analíticas. |
| Subsuperfície em camadas (opcional) | Testes controlados e paridade Python-MATLAB | Paridade dos kernels e do passo da coluna (fluxo implícito nos dois modelos), simulações do modelo completo na bacia em V, fechamento de massa na malha Voronoi e testes do fluxo implícito e da reposição capilar. Sem caso de campo. |
| Estresse hídrico radicular de Feddes (opcional) | Testes controlados de consistência | A ET de Feddes nos esquemas padrão e em camadas concorda para o mesmo estado; o Feddes nunca excede a absorção sem estresse. |
| Estado inicial do aquífero profundo (opcional) | Paridade com fixture | $S_0 = q_0 A \tau$ verificado em Python e MATLAB contra um fixture compartilhado. |
| Calibração por recessão em camadas | Apenas experimento gêmeo | Multiplicadores conhecidos recuperados com 0, 5 e 10 % de ruído em um vale sintético, como o único par aceitável. Sem teste de campo. |
| Seções transversais de vazão nos postos (MATLAB) | Verificações controladas | Vazão na seção transversal no caso em V, nas duas convenções de face do roteamento; 3 de 3 verificações. |
| Planilha única do caso (MATLAB) | Verificação de equivalência | O caso em V dá resultados idênticos com `HydroPol2D_Inputs.xlsx` e com o formato antigo `General_Data.xlsx`; 3 de 3 verificações. |
| Hidrodinâmica de momento completo | Validado | Plano inclinado, bacia em V, ruptura de barragem de Ritter, onda não quebrante e contornos. |
| Hidrodinâmica inercial local | Validado | Plano inclinado, bacia em V, contorno de nível e conservação. |
| Autômatos celulares | Validado | Casos de bacia em V, plano e condições de contorno. |
| Ondas cinemática e difusiva | Validado | Benchmarks de plano, bacia em V e contorno de nível adequados às equações reduzidas. |
| Modelo subgrid de Neal (2012) | Validado para as geometrias testadas | Referências de malha fina para escoamento em canal, canal composto, ativação de margens e extensão inundada. |
| Reservatórios e estruturas de controle | Validado | Solução de depleção por curva-chave e balanço de volume. |
| Contorno por hidrograma de entrada | Validado | Volume do hidrograma prescrito e balanço de armazenamento ou saída. |
| Contorno por hidrograma de nível | Validado | Aplicação do nível prescrito e resposta de volume. |
| Rasters de chuva espacial | Validado | Totais exatos por célula e por domínio. |
| Qualidade da água | Validado | Escala de acumulação do SWMM e soluções analíticas de lavagem por escoamento. |
| Risco e instabilidade humana | Validado | Referências independentes de limiares e equilíbrio de forças. |

A tabela abaixo traz os resultados mais recentes das suítes completas de testes.

| Suíte | Resultado | Data |
|---|---|---|
| HydroPol2D-Python | 937 aprovados, 0 com falha, 2 testes opt-in pulados | 2026-10-19 |
| Case Builder | 181 aprovados | 2026-10-19 |
| Verificações de release das águas subterrâneas no MATLAB | 17 de 17 | 2026-10-20 |
| Verificações dos postos e da planilha única no MATLAB | 3 de 3 cada | 2026-10-20 |
| Validação de release do MATLAB | 22 de 23 diretamente; a verificação da interceptação pelo dossel é pontuada pelo seu script de comparação em Python e passa quando esse script roda | 2026-10-20 |

As mudanças no modelo que afetam resultados estão listadas no [Registro de Alterações](./changelog).

Os casos de roteamento são interpretados de acordo com as equações que cada método resolve. A ruptura de barragem seca de Ritter é um benchmark de aceitação para o momento completo; os métodos reduzidos são avaliados com casos de escoamento gradual, conservação, simetria e condições de contorno.
