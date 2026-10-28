---
title: Trabajar en Studio
---

# Trabajar en Studio

## Ediciones, Save y Revert to saved {#edits-save-and-revert-to-saved}

Las ediciones entran en el modelo abierto a medida que las hace; solo **Save** escribe el archivo del
modelo.

- Un valor escrito se aplica cuando pulsa Enter o Tab o sale del campo. Una casilla de verificación o
  una opción de una lista se aplica de inmediato. Un número escrito a medias nunca se usa.
- Una tabla se aplica cuando se termina una celda, y una vez por cada pegado o eliminación de filas.
- El encabezado muestra "Unsaved changes" hasta que use **Save** (Cmd+S en un Mac, Ctrl+S en los
  demás sistemas). Studio pregunta antes de cerrar o de salir de un modelo con cambios sin guardar.
- **Save**, **Check inputs** y **Run** toman primero todas las ediciones que aún no se han aplicado.
- **Revert to saved**, en las páginas Processes y Parameters y en el menú File, pide confirmación,
  luego vuelve a abrir el archivo del modelo y descarta todos los cambios hechos desde el último
  guardado.

El editor de malla es la excepción: mantiene **Apply edits** y **Discard edits**, y Apply escribe la
malla editada en la carpeta del modelo de inmediato.

## Valores que Studio no puede usar {#values-studio-cannot-use}

Un valor que Studio no puede usar recibe un borde rojo, y una línea en rojo debajo de la página
explica por qué, por ejemplo "Maximum model time step [s] must be a number." Los demás valores se
siguen aplicando. **Save**, **Check inputs** y **Run** se niegan a continuar hasta que se corrija el
valor.

## Mensajes de error {#error-messages}

Un mensaje de error dice en una frase qué salió mal y, debajo, por qué, con palabras: nombres de
archivo en lugar de rutas completas y ningún nombre de clase de Python. Los detalles técnicos están
en **Show details**. **Copy details** los copia al portapapeles, listos para adjuntarlos a un
informe de problema.

**Help > Open the log folder** abre la carpeta con el registro y los informes de fallos de Studio.

## Tema {#theme}

**View > Theme** ofrece **Match system** (la opción predeterminada), **Dark** y **Light**. Match
system sigue la apariencia de macOS o de Windows, también cuando cambia con Studio abierto; un tema
elegido también define la barra de título de la ventana. El botón al pie de la barra de la izquierda
cambia al otro tema.

## Menús y atajos {#menus-and-shortcuts}

En Windows, use Ctrl en lugar de Cmd.

| Menú | Comando | Atajo |
|---|---|---|
| File | New model… | Cmd+N |
| File | Open model… | Cmd+O |
| File | Save model | Cmd+S |
| File | Save model as… | Shift+Cmd+S |
| File | Revert to saved | |
| File | Edit model file (YAML)… | |
| File | Open results… | |
| File | Quit | Cmd+Q (Alt+F4 en Windows) |
| View | Setup, Run, Results | Cmd+1, Cmd+2, Cmd+3 |
| View | Theme: Match system, Dark, Light | |
| Help | About HydroPol2D Studio (versión y licencia) | |
| Help | Documentation (este sitio web) | |
| Help | Open the log folder | |

Run no tiene atajo a propósito: una simulación puede tardar mucho, y una sola pulsación de tecla no
debería iniciarla.

## Rutas {#paths}

Las rutas largas, como la del archivo del modelo, la del DEM y la de la carpeta de resultados, se
acortan en el medio ("/Users/…/my_model/case.yaml") para que el inicio y el nombre del archivo sigan
a la vista; la ruta completa aparece en la información emergente (tooltip). **Show in Finder**
(Explorer en Windows) abre la carpeta con el archivo seleccionado.

## Pantallas pequeñas {#small-screens}

Todas las páginas caben en una ventana de 1280 × 720, el tamaño que da un portátil Windows con
pantalla 1080p a su escala predeterminada del 150 %. Cuando la ventana es así de baja, la barra de
herramientas de Study area muestra solo iconos; el nombre de cada herramienta aparece en su
información emergente, y las etiquetas vuelven cuando la ventana es más alta.
