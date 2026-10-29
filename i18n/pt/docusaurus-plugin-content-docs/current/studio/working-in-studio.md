---
title: Trabalhando no Studio
---

# Trabalhando no Studio

## Edições, Save e Revert to saved {#edits-save-and-revert-to-saved}

As edições entram no modelo aberto à medida que você as faz; só o **Save** grava o arquivo do modelo.

- Um valor digitado é aplicado quando você pressiona Enter ou Tab ou sai do campo. Uma caixa de
  seleção ou uma escolha em lista é aplicada na hora. Um número digitado pela metade nunca é usado.
- Uma tabela é aplicada quando uma célula é concluída, e uma vez a cada colagem ou remoção de linhas.
- O cabeçalho mostra "Unsaved changes" até você usar o **Save** (Cmd+S no Mac, Ctrl+S nos outros
  sistemas). O Studio pergunta antes de fechar ou de sair de um modelo com alterações não salvas.
- **Save**, **Check inputs** e **Run** primeiro aplicam todas as edições que ainda não foram
  aplicadas.
- **Revert to saved**, nas páginas Processes e Parameters e no menu File, pede confirmação, depois
  abre de novo o arquivo do modelo e descarta todas as alterações feitas desde o último salvamento.

O editor de malha é a exceção: ele mantém **Apply edits** e **Discard edits**, e o Apply grava a
malha editada na pasta do modelo na hora.

## Valores que o Studio não consegue usar {#values-studio-cannot-use}

Um valor que o Studio não consegue usar ganha uma borda vermelha, e uma linha em vermelho abaixo da
página explica o motivo, por exemplo "Maximum model time step [s] must be a number." Os outros
valores continuam sendo aplicados. **Save**, **Check inputs** e **Run** se recusam a continuar até
que o valor seja corrigido.

## Mensagens de erro {#error-messages}

Uma mensagem de erro diz em uma frase o que deu errado e, abaixo dela, o porquê, em palavras: nomes
de arquivo em vez de caminhos completos e nenhum nome de classe do Python. Os detalhes técnicos
ficam em **Show details**. **Copy details** copia esses detalhes para a área de transferência,
prontos para anexar a um relato de problema.

**Help > Open the log folder** abre a pasta com o log e os relatórios de falha do Studio.

## Tema {#theme}

**View > Theme** oferece **Match system** (o padrão), **Dark** e **Light**. Match system segue a
aparência do macOS ou do Windows, inclusive quando ela muda com o Studio aberto; um tema escolhido
também define a barra de título da janela. O botão no pé da barra à esquerda troca para o outro
tema.

## Menus e atalhos {#menus-and-shortcuts}

No Windows, use Ctrl no lugar de Cmd.

| Menu | Comando | Atalho |
|---|---|---|
| File | New model… | Cmd+N |
| File | Open model… | Cmd+O |
| File | Save model | Cmd+S |
| File | Save model as… | Shift+Cmd+S |
| File | Revert to saved | |
| File | Edit model file (YAML)… | |
| File | Open results… | |
| File | Quit | Cmd+Q (Alt+F4 no Windows) |
| View | Setup, Run, Results, Calibrate | Cmd+1, Cmd+2, Cmd+3, Cmd+4 |
| View | Theme: Match system, Dark, Light | |
| Help | About HydroPol2D Studio (versão e licença) | |
| Help | Documentation (este site) | |
| Help | Open the log folder | |

O Run não tem atalho de propósito: uma simulação pode levar muito tempo, e um único toque de tecla
não deveria iniciá-la.

## Caminhos {#paths}

Caminhos longos, como o do arquivo do modelo, o do DEM e o da pasta de resultados, são encurtados no
meio ("/Users/…/my_model/case.yaml") para que o início e o nome do arquivo continuem visíveis; o
caminho completo aparece na dica (tooltip). **Show in Finder** (Explorer no Windows) abre a pasta com
o arquivo selecionado.

## Telas pequenas {#small-screens}

Todas as páginas cabem em uma janela de 1280 × 720, o tamanho que um notebook Windows com tela 1080p
oferece na sua escala padrão de 150%. Quando a janela é baixa assim, a barra de ferramentas do Study
area mostra só ícones; o nome de cada ferramenta aparece na dica, e os rótulos voltam quando a
janela fica mais alta.
