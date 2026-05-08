=== SPRINT DE ESCRITURA: SECCIÓN {{section_number}} ===

PAPER: {{project_title}}
SECCIÓN: {{sec_title}}

--- CONTEXTO Y OBJETIVOS ---
OBJETIVOS: {{objetivos}}
SUBSECCIONES REQUERIDAS: {{subsecciones}}
INSUMOS (Tablas/Ecuaciones/Figuras): {{insumos}}

--- CITAS BIBLIOGRÁFICAS OBLIGATORIAS ---
Claves BibTeX: {{llaves_bibtex}}

{{instrucciones_citacion}}

--- ⛔ RESTRICCIONES MODULARES (CRÍTICO) ---
Este fragmento se insertará vía \input{section_N.tex} en un main.tex YA CONFIGURADO.
PROHIBIDO INCLUIR: 
  • \documentclass, \begin{document}, preámbulo, metadatos o cualquier configuración global.
  • Comentarios explicativos fuera del código LaTeX.

--- ✅ INSTRUCCIONES DE SALIDA (ESTILO HUMANO ACADÉMICO) ---

Escribe como un investigador experimentado que lleva años trabajando en el tema: estilo formal pero natural, con voz propia y fluidez académica real.

**Técnicas de humanización obligatorias:**

- Varía considerablemente la longitud de las oraciones (mezcla cortas y largas).
- Usa transiciones naturales y sofisticadas, no mecánicas.
- Introduce leve hedging cuando sea apropiado (podría sugerir, tiende a, en la mayoría de los casos estudiados...).
- Incluye algún análisis crítico o matiz propio, no solo descripción.
- Evita patrones repetitivos de IA.

**Aperturas de sección y subsección (CRÍTICO):**
No comiences nunca con "La...", "El...", "Los...", "Este trabajo...", "En este sección...". 
Utiliza aperturas variadas y más sofisticadas:
- Partiendo de un hallazgo o contradicción previa
- Contextualizando históricamente o teóricamente
- Planteando una pregunta retórica o un problema abierto
- Refiriendo a una tendencia o evolución reciente en la literatura
- Destacando una brecha o limitación conocida
- Presentando un enfoque o perspectiva particular

Ejemplos de aperturas aceptables: "A pesar de los avances significativos...", "Uno de los aspectos menos explorados...", "Resulta particularmente interesante cómo...", "Lejos de ser un proceso lineal...", etc.

--- ⚙️ FORMATO DE SALIDA ESTRICTO ---

Tu respuesta debe contener **exactamente dos bloques** de código Markdown. Nada más.

**BLOQUE 1 (Contenido LaTeX):**
```latex
\section{Nombre de la Sección}
\subsection{Subsección 1.1}
Texto con flujo natural y citas \cite{Key} integradas orgánicamente...

\begin{figure}[h]
\centering
\includegraphics[width=\linewidth]{nombre.png}
\caption{Descripción clara y técnica}
\label{fig:nombre}
\end{figure}
```

**BLOQUE 2 (Prompts de Imagen):**
```json
{
  "fig1.png": "2D technical vector diagram, engineering schematic..."
}
```

**Reglas adicionales de calidad:**

1. Extensión: 650-850 palabras (aprox.).
2. Estructura: Solo las subsecciones indicadas en {{subsecciones}}.
3. Citación: Integra las citas de forma natural dentro del flujo argumental. Nunca menciones una referencia sin citarla.
4. Figuras y tablas: Usa entornos IEEE estándar.
5. Estilo visual de las imágenes:
   - Estilo: 2D technical vector diagram, engineering schematic, flat design, minimalista
   - Fondo: blanco puro
   - Colores principales: Azul cobalto (#0047AB), gris técnico (#4A4A4A), negro
   - Sin sombras, sin gradientes, sin texto dentro de la imagen, sin elementos decorativos
