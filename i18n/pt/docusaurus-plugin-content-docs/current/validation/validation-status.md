---
title: Estado da validacao
---
import useBaseUrl from '@docusaurus/useBaseUrl';

# Estado da validacao

O relatorio de validacao documenta os metodos, as metricas e os resultados da suite de validacao do HydroPol2D. A tabela apresenta um indice conciso das evidencias atuais.

<div style={{margin: '1rem 0 1.5rem 0'}}>
  <a className="button button--primary button--lg" href={useBaseUrl('/reports/validation_report.pdf')}>
    Abrir o relatorio de validacao
  </a>
</div>

| Modulo | Estado | Evidencia |
|---|---|---|
| Interceptacao pelo dossel | Validado | Referencia independente de armazenamento em dossel e balanco exato de massa. |
| Neve | Validado | Parametros por LULC, mapas iniciais opcionais, refinamento temporal, equivalencia entre planilha e script, e balanco do evento em V. |
| Infiltracao | Validado | Casos analiticos e de solo estratificado em dominios de coluna e V. |
| Evapotranspiracao | Validado | Calculos independentes de ET de referencia e limites de extracao. |
| Aguas subterraneas e recarga | Validado | Testes de elevacao do nivel freatico, agendamento, ascensao capilar e encostas analiticas. |
| Hidrodinamica de momento completo | Validado | Plano inclinado, bacia em V, ruptura de barragem de Ritter, onda nao quebrante e contornos. |
| Hidrodinamica inercial local | Validado | Plano inclinado, bacia em V, contorno de nivel e conservacao. |
| Automatos celulares | Validado | Casos de bacia em V, plano e condicoes de contorno. |
| Ondas cinematica e difusiva | Validado | Benchmarks de plano, bacia em V e contorno de nivel adequados as equacoes reduzidas. |
| Modelo subgrid de Neal (2012) | Validado para as geometrias testadas | Referencias de malha fina para escoamento em canal, canal composto, ativacao de margens e extensao inundada. |
| Reservatorios e estruturas de controle | Validado | Solucao de deplecao por curva-chave e balanco de volume. |
| Contorno por hidrograma de entrada | Validado | Volume do hidrograma prescrito e balanco de armazenamento ou saida. |
| Contorno por hidrograma de nivel | Validado | Aplicacao do nivel prescrito e resposta de volume. |
| Rasters de chuva espacial | Validado | Totais exatos por celula e por dominio. |
| Qualidade da agua | Validado | Escala de acumulacao do SWMM e solucoes analiticas de lavagem por escoamento. |
| Risco e instabilidade humana | Validado | Referencias independentes de limiares e equilibrio de forcas. |

Os casos de roteamento sao interpretados de acordo com as equacoes que cada metodo resolve. A ruptura de barragem seca de Ritter e um benchmark de aceitacao para o momento completo; os metodos reduzidos sao avaliados com casos de escoamento gradual, conservacao, simetria e condicoes de contorno.
