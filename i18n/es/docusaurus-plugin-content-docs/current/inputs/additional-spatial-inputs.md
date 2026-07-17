---
title: Entradas espaciales adicionales
---

# Entradas espaciales adicionales

Más allá de los rásteres principales DEM, LULC y de suelo, HydroPol2D puede incorporar un conjunto más amplio de rásteres opcionales y entradas de estado inicial. Esta página documenta las entradas basadas en archivos admitidas que históricamente no se describieron en los documentos.
---

## Entradas ráster suplementarias

| Aporte | Clave de ruta pública | cuando se usa | Notas |
|---|---|---|---|
| Nivel freático inicial | `GW_table_path` | Cuando el agua subterránea está activa y se proporciona un ráster de cabecera inicial | El ráster se interpreta como **elevación/altura inicial del nivel freático** en metros, alineado con DEM. Si falta, el modelo vuelve a caer a un nivel freático poco profundo por defecto sobre el lecho de roca. |
| Impermeabilidad fraccionaria | `ImperviousFraction_path` | Cuando se suministra un ráster impermeable fraccional | Los valores pueden estar en porcentaje `[0,1]` o `[0,100]`. Esto refina la impermeabilidad de las células no edificadas. Las celdas clasificadas como acumuladas/impermeables por LULC permanecen completamente selladas. |
| LAI espacial | `LAI_path` | Cuando la configuración activa usa LAI | Ráster opcional de vegetación alineado con el DEM. |
| albedo espacial | `Albedo_path` | Cuando `flag_spatial_albedo = 1` | Ráster de albedo opcional alineado con DEM. |
| Ancho del río | `RiverWidths_path` | Cuando el modo de canal submalla de Neal (2012) usa geometría ráster | Ancho del canal en metros. Los valores deben ser positivos y menores que la resolución de la celda. |
| Profundidad del río | `RiverDepths_path` | Cuando el modo de canal submalla de Neal (2012) usa geometría ráster | Profundidad rectangular del canal o altura de la margen en metros. Se requiere una profundidad positiva donde el ancho del río sea positivo. |
| Rásteres de coeficientes de calidad del agua | `B1_path`, `B2_path`, `W1_path`, `W2_path` | Cuando la calidad del agua está activa y los coeficientes ráster están habilitados | Rásteres opcionales de coeficiente de acumulación/eliminación de contaminantes. |

---

## Entradas ráster de estado inicial

| Aporte | Clave de ruta pública | cuando se usa | Notas |
|---|---|---|---|
| Profundidad inicial del agua superficial | `Warmup_Depth_path` | Cuando se proporciona `flag_warmup = 1` y un ráster de profundidad de calentamiento | El ráster se lee como profundidad inicial del estanque en metros y se convierte internamente a milímetros. |
| Almacenamiento inicial del suelo | `Initial_Soil_Moisture_path` | Cuando se proporciona `flag_warmup = 1` y un ráster de suelo inicial | A pesar del nombre heredado, el código actual interpreta este ráster como **almacenamiento activo inicial del suelo por encima del contenido de agua residual** en milímetros, no como $\theta$ volumétrico bruto. |
| Acumulación inicial de contaminantes | `Initial_Buildup_path` | Cuando la calidad del agua utiliza un ráster de acumulación inicial | Se utiliza para inicializar estados de masa/acumulación de contaminantes. |

---

## Entrada del nivel freático

Si se proporciona `GW_table_path`, HydroPol2D utiliza ese ráster como elevación inicial del nivel freático:
- está alineado con el DEM,
- recortado para conservar un espesor mínimo vadoso,
- enmascarado al dominio activo,
- y se rellena localmente solo cuando al ráster le faltan valores.

Si no se proporciona un ráster del nivel freático, el modelo vuelve a un cabezal inicial predeterminado simple ligeramente por encima del lecho de roca. Esto significa que `GW_table_path` es una verdadera entrada opcional de condición inicial, no un ráster de agua subterránea requerido.
---

## Entrada de impermeabilidad fraccionaria

Si se proporciona `ImperviousFraction_path`, HydroPol2D lee un ráster de fracción impermeable por celdas y lo convierte a:
- fracción impermeable `frac_imp`,
- fracción anterior `frac_perv`,
- y una máscara totalmente impermeable para las células que están selladas de forma eficaz.

Comportamiento actual importante:
- los valores pueden suministrarse como fracciones o porcentajes,
- la trama refina la impermeabilidad principalmente fuera de la clase LULC construida,
- las células ya clasificadas como impermeables/acumuladas por la tabla LULC se ven obligadas a permanecer completamente impermeables.

Por lo tanto, el ráster impermeable debe documentarse como una **anulación/refinamiento de impermeabilidad fraccional**, no como un mapa independiente de cobertura del suelo.
---

## Alineación y remuestreo

Se espera que estos rásteres suplementarios sean consistentes con DEM, pero HydroPol2D también realiza trabajo de alineación internamente:
- los rásteres se vuelven a muestrear en la cuadrícula DEM cuando sea necesario,
- los valores no válidos están enmascarados fuera del dominio activo,
- Algunos rásteres opcionales solo se cargan cuando las banderas correspondientes están activas.

Eso los hace flexibles, pero no elimina la necesidad de un preprocesamiento sensato por parte del usuario.

---

## Geometría del canal de Neal (2012)

El modo de canal submalla de Neal (2012) usa el DEM grueso como elevación de la llanura. `RiverDepths_path` rebaja el lecho rectangular del canal respecto de esa elevación, mientras que `RiverWidths_path` define el ancho del canal en cada celda de río. Los dos rásteres deben suministrarse juntos.

El ancho del canal debe ser menor que la resolución de la celda. Un canal con un ancho igual o mayor que la celda debe resolverse mediante la malla ordinaria. Las rugosidades del canal y de la llanura se asignan por separado mediante los parámetros del río y del uso y cobertura del suelo.

Consulte [Banderas del modelo](../configuration/flags) para la combinación de enrutamiento requerida.
---

## Interpretación pública recomendada

La forma más sencilla de pensar en la superficie de entrada es:
1. DEM, LULC y SOIL definen el dominio base.
2. DTB, tabla GW, LAI, albedo y fracción impermeable refinan ese dominio base.
3. El calentamiento, el almacenamiento inicial del suelo y la acumulación inicial establecen el estado inicial.
4. Los rásteres WQ admiten módulos especializados opcionales.

Esa es la historia de entrada implementada actualmente que los documentos deben seguir.
---

## Profundidad de la raíz

La profundidad de la raíz es parte de la superficie de entrada del modelo actual, pero **no** como una ruta ráster independiente.
Comportamiento implementado actualmente:
- la profundidad de la raíz se lee en la tabla de parámetros LULC como `root_depth_m`,
- ese valor basado en clase se expande a la cuadrícula a través del mapa categórico LULC,
- la profundidad de la raíz resultante luego se trunca por la profundidad del lecho de roca y la posición del nivel freático cuando se construye el perfil vadoso en capas.

Entonces, sí, HydroPol2D puede ingerir información de profundidad de raíz, pero la ruta pública admitida hoy en día es:
1. Ráster LULC para identidad de clase,
2. `root_depth_m` en la tabla de parámetros LULC para la profundidad de raíz por clase.

No hay una entrada ráster `RootDepth_path` separada en el código actual.
