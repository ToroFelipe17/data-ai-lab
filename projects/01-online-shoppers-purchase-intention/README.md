# Proyecto 01: Análisis y predicción de intención de compra en sesiones de comercio electrónico

## Estado actual

**Diseño inicializado.** Esta misión documenta el problema, el dataset, el alcance y el plan de trabajo. Todavía no se ha descargado ni auditado el archivo de datos, no se ha realizado análisis exploratorio, no se han preparado datos para Machine Learning y no se han entrenado modelos.

## Descripción y motivación

Este proyecto estudiará sesiones de navegación en un contexto de comercio electrónico y el resultado observado de cada sesión: si terminó o no en una compra. El interés está en conectar comportamientos de navegación, características contextuales de la visita y conversión, manteniendo una metodología comprensible y reproducible.

La motivación es doble:

- comprender qué señales de una sesión están asociadas con una compra observada;
- evaluar, con modelos simples e interpretables, hasta qué punto puede anticiparse ese resultado sin presentar la predicción como una explicación causal ni como una solución productiva.

El proyecto forma parte del laboratorio público `data-ai-lab`, cuyo principio es aprender construyendo, demostrar comprendiendo y documentar para evolucionar.

## Antecedente académico

Anteriormente utilicé este dataset como parte de una actividad universitaria guiada relacionada con Machine Learning, principalmente mediante KNIME. Este proyecto no republica aquella evaluación ni reutiliza sus resultados como si fueran evidencia nueva. Retomo el dataset de forma independiente para profundizar su análisis e implementación mediante Python, por lo que las decisiones de adquisición, auditoría, preparación, evaluación e interpretación deberán justificarse nuevamente.

## Problema y pregunta central

El problema de trabajo es comprender y evaluar la capacidad de utilizar información disponible durante una sesión de comercio electrónico para distinguir entre sesiones que terminan en una compra y sesiones que no terminan en una compra.

**Pregunta central:**

> ¿Qué comportamientos observados durante una sesión de comercio electrónico están asociados con una compra y hasta qué punto puede predecirse la conversión utilizando modelos simples e interpretables?

La palabra “asociados” es deliberada: el proyecto no asumirá que una relación observada sea causal. Del mismo modo, `Revenue` representa un resultado observado de la sesión; no se tratará automáticamente como una medición completa de una intención psicológica no observada.

## Objetivos

### Objetivo general

Comprender la relación entre las características documentadas de una sesión de comercio electrónico y su resultado de compra, y evaluar de forma reproducible y crítica el desempeño de modelos simples e interpretables para predecir ese resultado.

### Objetivos específicos

1. Documentar la procedencia, las condiciones de uso, la estructura declarada y el significado de las variables del dataset.
2. Auditar empíricamente la calidad, los tipos, los valores faltantes, los duplicados, los rangos y las inconsistencias del archivo antes de tomar decisiones de preparación.
3. Explorar las diferencias y asociaciones entre las variables de sesión y el resultado `Revenue`, utilizando visualizaciones y resúmenes adecuados.
4. Establecer un baseline explícito, incluyendo una referencia basada en la clase mayoritaria, antes de comparar modelos.
5. Preparar los datos y separar entrenamiento y prueba de manera reproducible, justificando las decisiones que puedan afectar la evaluación.
6. Comparar un conjunto pequeño de modelos de clasificación simples, priorizando la comprensión y la interpretabilidad por sobre la cantidad de algoritmos.
7. Evaluar el desempeño con métricas apropiadas para la distribución de clases y analizar la matriz de confusión y los tipos de error.
8. Interpretar los resultados sin sobreextenderlos, distinguiendo asociación, capacidad predictiva y posibles implicaciones de negocio.
9. Documentar las limitaciones del dataset, del diseño de evaluación y de cualquier inferencia realizada.
10. Dejar un flujo reproducible, con dependencias declaradas, rutas relativas y documentación suficiente para repetir el trabajo.

## Dataset previsto

### Identidad y fuente primaria

- **Nombre oficial:** Online Shoppers Purchasing Intention Dataset.
- **Repositorio institucional:** UCI Machine Learning Repository.
- **Identificador UCI:** 468.
- **Fuente primaria:** [ficha oficial del dataset en UCI](https://archive.ics.uci.edu/dataset/468/online%2Bshoppers%2Bpurchasing%2Bintention%2Bdataset).
- **DOI:** [10.24432/C5F88Q](https://doi.org/10.24432/C5F88Q).
- **Creadores indicados por UCI:** C. Sakar y Yomi Kastro.
- **Cita indicada por UCI:** Sakar, C. & Kastro, Y. (2018). *Online Shoppers Purchasing Intention Dataset*. UCI Machine Learning Repository.

La ficha oficial declara 12.330 instancias, 17 características, un área temática de negocios, tareas asociadas de clasificación y clustering, y ausencia de valores faltantes declarados. UCI también informa 10.422 sesiones de clase negativa (84,5 %) y 1.908 de clase positiva. Además, indica que las instancias representan sesiones pertenecientes a usuarios distintos dentro de un período de un año, según la descripción del repositorio. Estas cifras son metadatos declarados por la fuente y deberán comprobarse empíricamente en la Misión 03.

### Variables documentadas oficialmente

La ficha de UCI documenta `Revenue` como etiqueta de clase y describe las siguientes variables de sesión:

- `Administrative`, `Administrative_Duration`;
- `Informational`, `Informational_Duration`;
- `ProductRelated`, `ProductRelated_Duration`;
- `BounceRates`, `ExitRates`, `PageValues`, `SpecialDay`;
- `Month`, `OperatingSystems`, `Browser`, `Region`, `TrafficType`;
- `VisitorType`, `Weekend`;
- `Revenue` como resultado objetivo.

La fuente describe conteos y duraciones de páginas administrativas, informativas y de productos; métricas de Google Analytics como `BounceRates`, `ExitRates` y `PageValues`; cercanía a días especiales mediante `SpecialDay`; y variables contextuales como sistema operativo, navegador, región, tipo de tráfico, tipo de visitante, mes y fin de semana.

Estas son características declaradas por la fuente, no una auditoría del archivo que se usará. En la Misión 03 se verificará que el archivo adquirido corresponda a esta identidad, que los nombres y tipos coincidan, y que las condiciones declaradas se cumplan en la copia utilizada.

### Licencia y uso

UCI indica que el dataset está disponible bajo [Creative Commons Attribution 4.0 International (CC BY 4.0)](https://creativecommons.org/licenses/by/4.0/). El uso del dataset deberá conservar la atribución correspondiente a sus creadores y a UCI. La cita, la URL de la fuente, el DOI, la fecha de adquisición y, cuando corresponda, una suma de comprobación del archivo se registrarán en la documentación de la etapa de adquisición.

No se incorpora todavía una copia del CSV al repositorio. La decisión de almacenarlo o documentar únicamente su descarga se tomará cuando se revise el tamaño, la licencia, la necesidad de versionado y la política del repositorio.

### Riesgos conceptuales a revisar

`PageValues` se describe oficialmente como el valor promedio de una página visitada antes de completar una transacción. Su relación con `Revenue` es una pregunta analítica defendible, pero antes de incluirla en un modelo será necesario revisar si representa información disponible en el momento real de la predicción o si incorpora información demasiado cercana al resultado. Esa revisión no se resuelve en esta misión y deberá quedar explícita en la Misión 03 o en la etapa de modelado.

## Preguntas analíticas

Las preguntas fueron revisadas contra las variables descritas por UCI. Se conservarán como guía, no como promesas de resultados:

1. ¿Qué diferencias presentan las variables de comportamiento de sesión entre sesiones con `Revenue` positivo y sesiones sin compra observada?
2. ¿Cómo se relacionan los conteos, las duraciones y las métricas de navegación con la conversión observada?
3. ¿Qué relación descriptiva existe entre `PageValues` y `Revenue`, y qué implicaciones tiene su disponibilidad temporal para la predicción?
4. ¿Existen patrones de conversión asociados con `VisitorType`?
5. ¿Cambian las tasas de conversión observadas según `Month`?
6. ¿Existen diferencias entre sesiones de días de semana y de fin de semana mediante `Weekend`?
7. ¿Qué variables aportan información predictiva en modelos simples, y cómo cambia esa interpretación según el preprocesamiento?
8. ¿Qué tan difícil es superar un baseline basado en la clase mayoritaria?
9. ¿Qué métricas permiten evaluar responsablemente el desempeño si la clase positiva es menos frecuente?
10. ¿Qué tipos de errores podrían ser más relevantes para una decisión de negocio y qué supuestos se necesitarían para discutirlos?

Todas las preguntas quedan abiertas. En particular, ninguna anticipa que una variable sea importante, que un mes convierta mejor o que un modelo supere el baseline.

## Alcance

El proyecto global podrá incluir, de forma progresiva:

1. adquisición reproducible y documentación de la fuente;
2. auditoría de identidad, calidad y estructura;
3. limpieza y preparación justificadas;
4. análisis exploratorio y visualización;
5. definición de un baseline y una estrategia de separación entrenamiento/prueba;
6. preprocesamiento y entrenamiento de modelos simples de clasificación;
7. comparación, evaluación e interpretación de errores;
8. conclusiones, limitaciones e implicaciones prudentes;
9. documentación de reproducibilidad.

Este alcance describe el proyecto completo. La presente misión solo cubre su diseño e inicialización documental.

## Fuera de alcance inicial

Quedan fuera del alcance inicial, salvo una justificación posterior basada en una necesidad concreta:

- deep learning y redes neuronales;
- LLM y sistemas multiagente;
- APIs productivas y despliegue cloud;
- Kubernetes, microservicios y MLOps completo;
- dashboards complejos;
- optimización exhaustiva de hiperparámetros;
- evaluación de grandes cantidades de modelos sin una razón analítica;
- afirmaciones de causalidad, personalización en tiempo real o impacto comercial medido;
- convertir el proyecto en una réplica de la actividad académica previa.

## Metodología prevista

La secuencia prevista es deliberadamente gradual:

1. **Adquisición y trazabilidad:** registrar la fuente UCI, la licencia, la fecha de descarga, el nombre del archivo y la versión o checksum que corresponda.
2. **Auditoría:** comprobar identidad, columnas, tipos, valores faltantes, duplicados, cardinalidades, rangos y distribución del objetivo sin ocultar incidencias.
3. **Preparación:** documentar cualquier conversión, codificación, tratamiento de valores o exclusión; evitar decisiones que filtren información del conjunto de prueba.
4. **Exploración:** describir la distribución de las sesiones, comparar grupos por `Revenue`, examinar las preguntas analíticas y visualizar solo lo que ayude a responderlas.
5. **Baseline y partición:** definir una referencia de clase mayoritaria y una separación reproducible antes de interpretar modelos.
6. **Modelado simple:** evaluar pocos clasificadores interpretables, por ejemplo un modelo lineal y un árbol acotado, únicamente si la auditoría y la preparación los justifican.
7. **Evaluación e interpretación:** comparar con el baseline, revisar matriz de confusión, precision, recall, F1, ROC-AUC o PR-AUC cuando sean pertinentes, y explicar qué significa cada resultado.
8. **Cierre:** analizar errores, limitaciones, implicaciones y capacidad de reproducción; vincular cada conclusión con evidencia realmente obtenida.

La metodología podrá ajustarse si la auditoría descubre restricciones del archivo, pero cualquier cambio deberá quedar documentado. No se ejecuta ninguna de estas etapas en la Misión 02.

## Principios de evaluación futura

- El baseline será explícito y servirá como referencia mínima.
- `accuracy` no será suficiente por sí sola si la distribución de clases está desbalanceada.
- Las métricas se elegirán según la pregunta, los costos relativos de los errores y las limitaciones del diseño.
- Una cifra superior no bastará para seleccionar un modelo: también se considerarán interpretabilidad, estabilidad, errores y reproducibilidad.
- La evaluación distinguirá desempeño predictivo de explicación causal.
- La inclusión de variables como `PageValues` se revisará considerando el momento en que estarían disponibles.

## Decisión estructural

En esta inicialización se crea únicamente la carpeta del proyecto y este README. No se crean `notebooks/`, `src/`, `outputs/` ni archivos placeholder porque todavía no existen artefactos ejecutables o resultados que justifiquen esas carpetas.

La organización prevista reutiliza la estructura global del repositorio:

```text
data-ai-lab/
├── datasets/                 # archivo o instrucciones de adquisición, cuando corresponda
├── notebooks/                # notebooks futuros, numerados y con prefijo del proyecto
├── projects/
│   └── 01-online-shoppers-purchase-intention/
│       └── README.md         # diseño, decisiones y estado del proyecto
├── src/                      # código reutilizable, solo si existe una necesidad real
└── docs/                     # documentación transversal, si llega a ser necesaria
```

Esta decisión evita duplicar las carpetas globales y permite que el proyecto crezca con artefactos reales. Si la cantidad de notebooks, código o salidas lo justifica más adelante, se reevaluará una estructura específica sin crearla anticipadamente.

## Reproducibilidad esperada

El trabajo terminado deberá indicar cómo obtener el dataset desde la fuente primaria, qué versión o archivo se utilizó, qué dependencias son necesarias, en qué orden se ejecutan los artefactos y qué decisiones afectan los resultados. Se preferirán rutas relativas y configuraciones explícitas; no se aceptarán rutas locales hardcodeadas ni dependencias ocultas.

En esta misión no se agregan dependencias a `requirements.txt`, que permanece vacío intencionalmente porque no hay código ejecutable.

## Criterios de finalización

El Proyecto 01 podrá considerarse terminado cuando:

- el dataset utilizado esté correctamente identificado, citado y documentado;
- el proceso de adquisición y ejecución pueda repetirse desde una instalación documentada;
- la auditoría de datos esté completada y sus hallazgos sean visibles;
- las decisiones de preparación estén justificadas y no oculten problemas relevantes;
- el análisis exploratorio responda las preguntas seleccionadas con evidencia;
- exista un baseline explícito y una separación de evaluación defendible;
- los modelos simples estén comparados con métricas apropiadas y contexto suficiente;
- los errores del modelo estén analizados, no solo resumidos en una cifra;
- las limitaciones y los riesgos conceptuales, incluida la disponibilidad de variables, estén documentados;
- las conclusiones estén vinculadas con resultados efectivamente obtenidos;
- la documentación permita reproducir el flujo sin dependencias ocultas ni rutas locales;
- el autor pueda explicar las decisiones fundamentales, sus supuestos y sus límites.

Estos criterios corresponden a un proyecto individual de aprendizaje; no implican despliegue productivo ni una validación empresarial completa.

## Próximos pasos

La Misión 03 debería adquirir o localizar el archivo desde UCI, registrar su procedencia y realizar una auditoría inicial de identidad, estructura y calidad. No debe adelantar conclusiones de negocio ni entrenamiento de modelos antes de completar esa verificación.
