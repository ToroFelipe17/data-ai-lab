# Laboratorio de Datos e IA

Este repositorio es un laboratorio público y progresivo para desarrollar y documentar habilidades prácticas relacionadas con datos e inteligencia artificial aplicada. La estructura y los principios de trabajo están definidos, y el primer proyecto fue completado como un experimento reproducible de análisis y clasificación.

> Construir productos con propósito.

El laboratorio sigue un enfoque sencillo: aprender construyendo, demostrar mediante la comprensión y documentar para evolucionar.

## Propósito

El propósito de este repositorio es convertir el aprendizaje técnico en evidencia pública comprensible, reproducible y documentada con honestidad. Cada proyecto futuro deberá hacer visible su razonamiento, no solo sus resultados.

## Áreas de enfoque

El laboratorio abordará progresivamente:

- Python aplicado a datos.
- Limpieza y transformación de datos.
- Análisis exploratorio de datos.
- Visualización de datos.
- Estadística aplicada.
- Aprendizaje automático.
- Evaluación de modelos.
- Procesamiento de datos a gran escala.
- Automatización.
- Inteligencia artificial aplicada.

Estas son áreas de desarrollo planificadas, no afirmaciones sobre trabajo ya realizado.

## Principios de trabajo

- Comprensión antes que complejidad.
- Reproducibilidad desde la preparación de los datos hasta su interpretación.
- Documentación técnica clara.
- Interpretación honesta de los resultados.
- Supuestos y limitaciones explícitos.
- Dificultad progresiva.
- Soluciones simples antes que abstracciones innecesarias.
- Sin errores ocultos ni presentación selectiva de resultados.

## Estructura del repositorio

- `notebooks/`: cuadernos numerados y enfocados en exploración, explicación y experimentación.
- `datasets/`: conjuntos de datos que puedan almacenarse legal y responsablemente, o instrucciones para obtener aquellos que no puedan incluirse en el repositorio.
- `projects/`: proyectos de datos independientes, numerados y con nombres descriptivos.
- `src/`: módulos reutilizables de Python cuando un proyecto concreto justifique compartir código.
- `docs/`: documentación técnica complementaria que no corresponda al README de un proyecto.
- `requirements.txt`: paquetes externos de Python que el código ejecutable del repositorio realmente necesite.

La estructura podrá evolucionar cuando exista una necesidad concreta. `requirements.txt` registra únicamente las dependencias directas necesarias para el código ejecutable actualmente versionado.

## Organización de proyectos

Los proyectos están numerados y tienen nombres descriptivos. El primer proyecto inicializado es:

```text
projects/
└── 01-online-shoppers-purchase-intention/
```

Consulta el [README del Proyecto 01](projects/01-online-shoppers-purchase-intention/README.md) para conocer el problema, el análisis, el baseline reproducible, la decisión sobre `PageValues` y sus limitaciones.

**Proyecto 01:** análisis y predicción de intención de compra en sesiones de comercio electrónico. Utiliza Python, pandas, matplotlib y scikit-learn para documentar un EDA reproducible y un baseline de clasificación. Estado: **completado** como proyecto de aprendizaje; no representa una solución productiva ni una conclusión causal.

Cada proyecto deberá documentar:

- Objetivo.
- Contexto.
- Fuente del conjunto de datos.
- Condiciones de uso o licencia del conjunto de datos.
- Preguntas o hipótesis.
- Preparación de los datos.
- Metodología.
- Resultados.
- Interpretación.
- Limitaciones.
- Conclusiones.
- Próximos pasos.

Las carpetas utilizarán minúsculas y `kebab-case`; los archivos de Python utilizarán minúsculas y `snake_case`. Los cuadernos estarán numerados y tendrán nombres descriptivos, por ejemplo:

```text
notebooks/
├── 01-carga-de-datos.ipynb
├── 02-limpieza-de-datos.ipynb
└── 03-analisis-exploratorio.ipynb
```

El código futuro deberá utilizar nombres claros, evitar duplicación innecesaria, separar responsabilidades cuando sea útil, preferir rutas relativas y evitar supuestos locales sin documentar. Los cuadernos deberán seguir un orden lógico, ejecutarse de principio a fin, distinguir el código y los resultados de su interpretación, utilizar semillas aleatorias cuando corresponda y evitar celdas abandonadas o salidas excesivas.

## Hoja de ruta

1. Base del repositorio — completada con esta configuración inicial.
2. Análisis exploratorio de datos.
3. Aprendizaje supervisado.
4. Segmentación o agrupamiento.
5. Flujos de trabajo con datos a gran escala.
6. Inteligencia artificial aplicada y automatización.

Esta hoja de ruta expresa una dirección para el trabajo futuro, no un calendario de entregas.

## Estado actual

Configuración inicial completada. El Proyecto 01 es el primer proyecto funcional y completado del laboratorio; cuenta con un análisis, un baseline predictivo reproducible y una decisión metodológica documentada sobre `PageValues`.

## Reproducibilidad y documentación

Los proyectos futuros deberán:

- Utilizar fuentes de datos identificables y respetar sus licencias y condiciones de uso.
- Evitar información privada, sensible o personal que no sea necesaria.
- Explicar cómo obtener los conjuntos de datos que no puedan almacenarse en GitHub.
- Preferir rutas relativas cuando sea posible.
- Registrar únicamente dependencias reales y necesarias.
- Ejecutarse en una secuencia clara y reproducible.
- Explicar decisiones, errores y limitaciones.
- Interpretar los resultados en lugar de presentar métricas sin contexto.

## Autor

Felipe Toro — construyendo en la intersección entre software, datos, producto e inteligencia artificial aplicada.
