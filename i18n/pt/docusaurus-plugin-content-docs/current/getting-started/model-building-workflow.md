---
title: Fluxo de construção do modelo
---

# Fluxo de construção do modelo

O HydroPol2D tem um único fluxo científico de construção de casos e dois motores de modelo compatíveis. O Case Builder cria o caso. O HydroPol2D-Python e o HydroPol2D-MATLAB o consomem. A calibração das águas subterrâneas é um procedimento opcional em Python que atualiza o caso antes de qualquer um dos motores ser executado.

```text
Case Builder: domínio físico provisório
                    |
                    v
   Calibração opcional das águas subterrâneas em Python
                    |
                    v
Case Builder: parâmetros e estados iniciais finalizados
                    |
                    v
                 Preflight
                    |
          +---------+---------+
          |                   |
          v                   v
 HydroPol2D-Python     HydroPol2D-MATLAB
          |                   |
          +---------+---------+
                    |
                    v
      Resultados compartilhados e QA
```

## A regra central {#the-central-rule}

Um domínio preparado não é necessariamente um caso pronto para rodar. Um caso só fica pronto para rodar depois que os parâmetros e os estados iniciais selecionados são gravados nos adaptadores dos solvers e a verificação prévia (preflight) é aprovada.

O diretório do caso gerenciado pelo Builder é a fonte da verdade. O YAML do Python, as planilhas do MATLAB, os adaptadores de caminhos do MATLAB e os scripts de execução gerados são visões desse caso para cada solver. Eles não devem adquirir configurações científicas independentes.

## Fluxo padrão {#standard-workflow}

Use este caminho quando os parâmetros padrão ou fornecidos pelo usuário forem adequados.

1. **Definir o experimento.** Selecione o domínio, a resolução do modelo, o período, as forçantes, os processos ativos, o tratamento do terreno, a representação dos rios, os adaptadores de solver, as variáveis de saída e o intervalo de saída.
2. **Visualizar o domínio e o custo.** Inspecione a bacia, o exutório, o número de células ativas, a disponibilidade dos dados de origem e as estimativas de memória, transferência e saídas salvas.
3. **Preparar o caso completo.** O Builder baixa ou organiza os dados de origem, cria o terreno hidráulico e os produtos de rio, alinha os rasters estáticos, prepara as forçantes e registra a proveniência e o QA.
4. **Finalizar parâmetros e estados iniciais.** Valores padrão, rasters espaciais ou valores explícitos do usuário são resolvidos nos campos finais da grade do modelo.
5. **Rodar o preflight.** O preflight verifica arquivos, grades, unidades, cobertura das forçantes, condições de contorno, parâmetros obrigatórios e combinações de solver suportadas.
6. **Selecionar o motor.** Rode Python, MATLAB ou ambos. Escolher um motor não reconstrói o domínio nem altera o caso científico.
7. **Inspecionar os resultados.** Use os instantes salvos pelo modelo, os diagnósticos de balanço de massa, hidrogramas, mapas e animações. O tempo de atualização da interface não é o tempo do modelo.

## Fluxo calibrado pelas águas subterrâneas {#groundwater-calibrated-workflow}

A calibração das águas subterrâneas introduz, de propósito, uma construção em duas passagens.

### Passagem 1: caso provisório {#pass-1-provisional-case}

O Builder prepara a geometria do domínio e as entradas de que o experimento de calibração precisa.

- DEM hidráulico, domínio ativo, rios, exutórios e sub-bacias;
- mapas de solo, cobertura do solo, profundidade radicular, fundo do aquífero e leito do rio;
- forçantes e a série observada do posto fluviométrico, quando disponível;
- parâmetros provisórios das águas subterrâneas suficientes para carregar o domínio.

Esse caso provisório não é a simulação de produção.

### Calibração em Python {#python-calibration}

O procedimento de calibração em Python faz o seguinte.

1. Filtra o hidrograma observado e constrói uma curva mestra de recessão.
2. Identifica o tempo de resposta do reservatório linear profundo a partir da cauda lenta.
3. Faz o período de aquecimento (spin-up) e libera o aquífero de Boussinesq distribuído.
4. Estima a condutividade horizontal uniforme efetiva e o rendimento específico.
5. Salva o campo de cargas das águas subterrâneas, o armazenamento raso e a vazão rasa em cada estado da recessão.
6. Grava os diagnósticos da calibração e o arquivo de estados de volta no diretório do caso.

A calibração é implementada uma única vez, em Python. O MATLAB não repete esse procedimento inverso.

### Passagem 2: caso final {#pass-2-final-case}

O Builder importa os artefatos de calibração aceitos e resolve as condições iniciais finais.

- um estado do aquífero raso selecionado pela depleção normalizada do armazenamento;
- vazão profunda igual ao escoamento de base inicial filtrado menos a vazão rasa selecionada;
- armazenamento profundo igual à vazão profunda multiplicada pelo tempo de resposta calibrado;
- a fração configurada da recarga futura encaminhada ao reservatório profundo;
- umidade da camada superficial e da zona radicular no início do evento, a partir de campos do ERA5-Land tratados por profundidade;
- umidade da zona de transmissão a partir da drenagem gravitacional permanente e da influência capilar do lençol freático selecionado.

Em seguida, o Builder regenera os dois adaptadores de solver solicitados e roda o preflight de novo. Só esse caso finalizado deve ser usado na simulação de produção.

No Builder, escolha **Calibrate from observed streamflow** em **Hydraulic parameters**. Depois que o caso provisório estiver preparado, abra-o em **Check a case**. Ali, o painel de calibração aceita o ID de um posto do USGS ou um CSV local, valores candidatos de `Ksat,h` e `Sy` e a fração normalizada de depleção do armazenamento raso. A calibração roda em segundo plano e continua mesmo com a aba do navegador fechada. **Refresh calibration status** lê o progresso e os artefatos salvos. Um job bem-sucedido aplica o resultado e roda o preflight de novo.

O estado vadoso finalizado preserva a informação vertical. As camadas do ERA5-Land são promediadas pela sobreposição de profundidade para o armazenamento superficial de 0.05 m e para a zona radicular derivada do LULC. O armazenamento de transmissão é inicializado com um perfil de equilíbrio de van Genuchten condicionado ao lençol freático selecionado. Os dois solvers leem esses três mapas, e os casos antigos, com uma única umidade, mantêm a alternativa documentada.

### Casos com subsuperfície em camadas {#layered-subsurface-cases}

Com `--subsurface-scheme layered` (padrão `legacy`), o Builder prepara um caso de [subsuperfície em camadas](../theory/layered-subsurface) para Python, MATLAB ou ambos.

1. **Entradas globais.** Ele deriva a base do solo do BDRICM do SoilGrids, os parâmetros de van Genuchten do regolito da classe textural a 200 cm e a condutividade do regolito do GLHYMPS 2.0. As regras estão nas páginas [Solo](../inputs/soil#global-sources-used-by-the-case-builder) e [DTB](../inputs/dtb#global-sources-used-by-the-case-builder).
2. **Adaptadores de solver.** O caso Python recebe `vertical.subsurface.scheme: layered` e os caminhos estáticos. O adaptador MATLAB passa os rasters da base do solo e do regolito e `HYDROPOL_SUBSURFACE_SCHEME`.
3. **Estado inicial do aquífero profundo.** `--deep-aquifer-initial-baseflow-mm-day` ou `--deep-aquifer-mean-recharge-mm-year` (no máximo um dos dois) define o armazenamento inicial dos reservatórios profundos. O `DeepAquiferInitialState.json` de uma calibração substitui ambos.
4. **Calibração.** Em casos em camadas, a calibração por recessão ajusta dois multiplicadores da condutividade lateral, um para as camadas de solo e outro para as camadas de regolito, em vez de `Ksat,h` e `Sy`. A finalização grava esses valores no caso Python e no executor MATLAB. $S_y$ permanece nas curvas de retenção. Veja [Calibração por Recessão das Águas Subterrâneas](../calibration/groundwater-recession).

## Responsabilidades dos componentes {#component-responsibilities}

| Componente | Responsável por | Não é responsável por |
|---|---|---|
| Case Builder | Domínio, dados de origem, terreno, produtos de rio e de subgrade, forçantes, mapas de parâmetros alinhados, estados iniciais, adaptadores de solver, proveniência e preflight | Avanço numérico no tempo ou inversão de parâmetros |
| Calibração das águas subterrâneas | Análise da curva mestra de recessão, parâmetros efetivos do aquífero raso, tempo de resposta profundo e o arquivo salvo de estados rasos | Preparação do terreno, download das forçantes de produção ou um segundo formato de caso |
| HydroPol2D-Python | Implementação científica de referência, execução da calibração, simulação, testes e saídas padrão | Reconstrução independente da geometria do Builder |
| HydroPol2D-MATLAB | Simulação compatível do caso finalizado e verificação entre linguagens | Um fluxo de calibração separado ou padrões independentes do Builder |
| Interface de resultados | Leitura das saídas salvas dos solvers e dos seus instantes no tempo do modelo | Alteração de parâmetros ou definição do estado da simulação durante a atualização |

## Estados do caso {#case-states}

| Estado | Significado | Pode rodar? |
|---|---|---:|
| Rascunho | As configurações ainda estão em edição. | Não |
| Visualizado | O domínio e o custo foram inspecionados, mas as entradas completas podem não existir. | Não |
| Provisório | O domínio físico existe e pode ser usado na calibração. | Só calibração |
| Finalizado | Parâmetros e estados iniciais aceitos foram gravados nos adaptadores de solver. | Ainda não |
| Preflight aceito | Todos os arquivos obrigatórios e verificações de compatibilidade passaram. | Sim |
| Rodando | Um solver está avançando o caso finalizado. | Em andamento |
| Concluído | O solver terminou com sucesso e gravou as saídas solicitadas. | Encerrado |

O preflight estabelece consistência interna, não precisão hidrológica. Um conjunto de parâmetros calibrado estabelece uma hipótese ajustada, não uma verdade de campo universal. As duas distinções devem continuar visíveis na interface e nos relatórios.

## Escolha entre Python e MATLAB {#choosing-python-or-matlab}

- Use **Python** para a calibração das águas subterrâneas, diagnósticos rápidos, testes automatizados e o fluxo científico de referência atual.
- Use **MATLAB** quando o caso finalizado exigir a implementação em MATLAB ou um fluxo de produção já existente em MATLAB.
- Use **ambos** em estudos de paridade. Os dois adaptadores precisam vir do mesmo caso finalizado do Builder e usar parâmetros, forçantes, estados iniciais, contornos e cadência de saída idênticos.

Os fluxos independentes com YAML do Python e com Excel do MATLAB continuam úteis para exemplos e testes controlados. Eles são separados de um caso científico gerenciado pelo Builder e não devem ser misturados a ele sem aviso.
