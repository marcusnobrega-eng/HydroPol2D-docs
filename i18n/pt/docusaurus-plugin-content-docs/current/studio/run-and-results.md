---
title: Execução e resultados
---

# Execução e resultados

## Run {#run}

A área de trabalho Run tem dois painéis.

- **Outputs**: o perfil de saída, a pasta de saída, os intervalos de gravação de mapas, séries
  temporais, saída nativa da malha e pilhas de rasters, a forma como os mapas são armazenados durante
  a simulação e as configurações de animação.
- **Computing backend**: os backends que este computador consegue executar. Nos apps para Mac e
  Windows, é a CPU; as GPUs da Apple não têm a aritmética de 64 bits de que o modelo precisa.
- **Save results to**: a pasta desta simulação. Você pode digitar outra pasta só para esta
  simulação; **Show in Finder** (Explorer no Windows) abre essa pasta.
- **Check inputs** executa a verificação das entradas, **Run model** inicia a simulação e
  **Cancel run** a interrompe. O Run verifica as entradas antes de começar.
- **Live diagnostics** mostra gráficos da simulação a cada intervalo salvo, e o log da simulação
  lista cada etapa.

## Results {#results}

**Results** abre a saída de uma simulação, ou um pacote de resultados aberto pela tela Home. Ele tem
o seu próprio painel de camadas, então mudar uma sobreposição de resultado não muda o mapa do Study
area.

- A reprodução anda para a frente ou para trás e pode repetir em loop, avançar quadro a quadro ou
  saltar para um tempo decorrido ou uma data do calendário. Os mapas de máximo, mínimo e final
  resumem a variável ativa sem alterar o arquivo.
- Clique com o botão direito em uma célula de resultado para plotar a série temporal salva dela,
  exportar os dados da célula, inspecionar todas as variáveis de mapa salvas ou iniciar uma linha de
  perfil.
- Os mapas são exportados em PNG, PDF, SVG, GeoTIFF ou MP4. Os gráficos de séries temporais mantêm
  variáveis independentes nos eixos esquerdo e direito e são exportados em PNG, PDF, SVG ou CSV.
- Na drenagem urbana, tubulações, poços de visita, bocas de lobo e condições de contorno internas
  aceitas podem ser coloridas por uma grandeza salva no tempo selecionado, e cada uma também está
  disponível como uma série temporal com nome.
