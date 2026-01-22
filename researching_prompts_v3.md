## Prompts para generacion de contenidos de investigacion
**Instrucciones para el usuario:** Copia los textos y sustituye los valores entre corchetes según tu especialidad.

### Generacion de lista de 10 temas de investigacion
Esto debería generar una tabla exportable a google sheets, con una lista de los primeros 10 temas de vanguardia a los que tenga acceso el LLM.

**PROMPT:**
```md
> "Actúa como un **[Rol: Ej. Ingeniero TT&C / Aeronáutico / Especialista en Ciberseguridad]** senior con doctorado en el sector aeroespacial. Mi objetivo es identificar oportunidades de innovación disruptiva.
> **CONTEXTO:**
> Mi área de experticia es **[Tu área específica: Ej. Dinámica de Fluidos / Arquitectura de Microservicios]**. Necesito que cruces este conocimiento con las necesidades actuales del sector de *Satélites de Telecomunicaciones y Percepcion Remota / Exploración de Espacio Profundo*, integrando el uso avanzado de **[Tecnología clave: Ej. IA, Big Data, Blockchain, Computación Cuántica]**.
> **TAREA:**
> Genera una lista de **10 temas de investigación** que sean tendencia para el periodo 2026-2030.
> **REQUISITOS DE FORMATO (PARA EXPORTACIÓN):**
> 1. Presenta los resultados en una **Tabla de Markdown** (para habilitar la exportación a Google Sheets).
> 2. Columnas: Orden | Tema de Investigación | Justificación Técnica y Valor para la Unidad.
> 3. Restricciones:
> * Tema: Máximo 60 caracteres.
> * Justificación: Máximo 150 caracteres (enfoque en impacto operativo).
> 
> 
> 
> 
> ## **ENFOQUE ESTRATÉGICO:**
> Prioriza temas que reduzcan el **[KPI a optimizar: Ej. Consumo energético / Latencia / Peso (SWaP) / Costo de desarrollo]**."
> 
> 

```
---

### Generacion de plan de investigacion por tema
Genera un desglose temático detallado de la investigacion, el plan por secciones, y las referencias la base de conocimiento para consultas (bibliografia).

**PROMPT:**
```md
> "Actúa como Editor Jefe de IEEE. Para el tema de investigación **[Insertar Tema]**, genera un **Desglose Temático Detallado** siguiendo estrictamente este esquema de dos partes:
> **PARTE 1: ESTRUCTURA JSON**
> Entrega un bloque de código JSON con la siguiente estructura:
> {
> "titulo": "Título técnico en español",
> "abstract_preliminar": "Resumen técnico de 150 palabras siguiendo normas IEEE",
> "secciones": [
> {
> "nro": 1,
> "titulo_seccion": "Nombre de la sección",
> "objetivos": ["objetivo 1", "objetivo 2"],
> "subsecciones": ["1.1...", "1.2..."],
> "insumos": ["Tabla 1", "Eq. 1"],
> "llaves_bibtex": ["Key1", "Key2"]
> }
> ]
> }
> **PARTE 2: BLOQUE BIBLIOGRÁFICO**
> Entrega un único bloque de código `bibtex` con las entradas completas de las **30 referencias reales (2023-2026)** mencionadas en el JSON.
> **No redactes el contenido aún, solo entrega el JSON y el bloque BibTeX.**"
```
---

### Generar campos de registro de informacion preliminar de investigacion
Genera los campos del formulario de registro de una investigacion en el sistema de gestion de documentacion.

**PROMPT:**
```md
Necesito ingresar en el sistema encargado de gestionar la documentacion de la Agencia para la que trabajo relacionada con el sector espacial, los datos de la siguiente investigación de carácter académico/técnico bajo el nombre **[Titulo definitivo de la investigacion]**. Para eso, requiero llenar un formulario con los siguientes campos:

* Description
* General Objective
* Specific Objectives
* Justification
* Methodology
* Scope (maximo 250 caracateres)
* Activities (las previstas a efectuar para ejecutar la investigacion)
* Resources (Los recursos previstos que se necesitaran para llevarla a cabo)
* Limitations

Dame los valores de los campos en español.
```

### Generar imagenes
**PROMPT**
```md
> "Actúa como un **Diseñador de Infografías Técnicas para el Sector Aeroespacial**.
> **CONTEXTO:**
> Estoy escribiendo un paper titulado: **[Insertar Título del Documento]**.
> Necesito generar una imagen profesional para el siguiente bloque de código LaTeX:
> ```tex
> [Insertar bloque \begin{figure} ... \end{figure}]
> 
> ```
> 
> 
> **TAREA:**
> Genera un **Prompt Detallado** para un motor de IA generadora de imágenes (como DALL-E 3 o Midjourney) que describa esta figura.
> **REQUISITOS DEL PROMPT DE IMAGEN:**
> 1. **Estilo:** Diagrama técnico 3D profesional, estilo 'Digital Twin', limpio, fondo blanco o azul oscuro tecnológico, estética de ingeniería de vanguardia.
> 2. **Elementos:** Describe explícitamente qué objetos deben aparecer (ej. satélites en órbita LEO, estaciones terrestres, rayos de luz representando la conexión D2D).
> 3. **Claridad:** Evita que se repita el titulo de la imagen (que ya esta en bloque .tex que la invoca), enfócate en la simbología y la interconexión.
> 4. **Perspectiva:** Especifica si es una vista isométrica, orbital o un diagrama de flujo de datos."
> 
> 
```