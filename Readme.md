# Space Research Automator (SRA) 🛰️🤖

**Space Research Automator** es una herramienta de automatización para investigadores del sector aeroespacial y de telecomunicaciones. Permite transformar un plan de investigación estructurado (Blueprint) en un entorno completo de redacción en **LaTeX**, siguiendo los estándares de rigor de la **IEEE**.

## 🛠️ El Blueprint (Input del Sistema)

Para que el script funcione, el archivo `research_plan.md` debe ser generado por un LLM (como Gemini) utilizando el siguiente "Metaprompt" de arquitectura. Este diseño garantiza que la IA defina primero la lógica científica antes de proceder a la redacción.

### Metaprompt de Arquitectura

> "Actúa como Editor Jefe de IEEE. Para el tema de investigación **[Insertar Tema]**, genera un **Desglose Temático Detallado** siguiendo estrictamente este esquema:
> **PARTE 1: ESTRUCTURA JSON**
> Entrega un bloque de código JSON con esta estructura:
> ```json
> {
>   "titulo": "Título técnico en español",
>   "abstract_preliminar": "Resumen técnico de 150-200 palabras siguiendo normas IEEE",
>   "secciones": [
>     {
>       "nro": 1,
>       "titulo_seccion": "Nombre de la sección",
>       "objetivos": ["objetivo 1", "objetivo 2"],
>       "subsecciones": ["1.1...", "1.2..."],
>       "insumos": ["Tabla 1", "Eq. 1"],
>       "llaves_bibtex": ["Key1", "Key2"]
>     }
>   ]
> }
> 
> ```
> 
> 
> **PARTE 2: BLOQUE BIBLIOGRÁFICO**
> Entrega un único bloque de código `bibtex` con las entradas completas de **30 referencias reales (2023-2026)** mencionadas en el JSON.
> **No redactes el contenido aún, solo entrega el JSON y el bloque BibTeX.**"

---

## 🚀 Uso del Script

### 1. Preparación

Guarda la respuesta de la IA en un archivo llamado `research_plan.md`.

### 2. Ejecución

Ejecuta el script pasando el archivo de entrada y el nombre deseado para tu proyecto:

```bash
python sra_v35.py research_plan.md "IA Cloud Masking"

```

### 3. Salida Generada

El script automatiza la creación de:

* **`main.tex`**: Documento raíz configurado con `biblatex` y motor `biber`.
* **`abstract.tex`**: Contenido del resumen extraído del JSON.
* **`references.bib`**: Base de datos de citas lista para procesar.
* **`section_n.tex`**: Archivos modulares para cada sección del paper.
* **`prompt_section_n.txt`**: Prompts de escritura técnica "listos para usar" que incluyen objetivos, subsecciones y las llaves bibliográficas exactas que la IA debe citar.

---

## 📂 Estructura de Archivos Resultante

```text
/IA_Cloud_Masking
├── main.tex             # Compila aquí
├── references.bib       # Referencias centralizadas
├── abstract.tex         # Resumen integrado
├── section_1.tex        # Cuerpo de la Introducción
├── prompt_section_1.txt # Prompt para redactar la Sec. 1
└── ... (secciones restantes)

```

## 📝 Requisitos de Compilación

Para asegurar que las referencias se generen correctamente en el PDF final, se recomienda:

1. Usar una distribución de LaTeX moderna (TeX Live o MiKTeX).
2. Configurar el compilador para usar **Biber** en lugar de BibTeX (estándar en `biblatex` para IEEE).
3. En Overleaf, esto se configura automáticamente al detectar el preámbulo generado.
