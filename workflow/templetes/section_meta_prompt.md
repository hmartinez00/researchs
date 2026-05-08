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
  • \documentclass, \begin{document}, \end{document}
  • \usepackage{}, \addbibresource{}, \bibliographystyle{}, \bibliography{}
  • \begin{filecontents}{...} ... \end{filecontents}
  • Preambulo, metadatos, autor, título o configuración de bibliografía.
  • Comentarios explicativos fuera de LaTeX.

--- ✅ INSTRUCCIONES DE SALIDA ---

--- ⚙️ FORMATO DE SALIDA ESTRICTO (OBLIGATORIO) ---
Tu respuesta debe contener EXACTAMENTE dos bloques de código Markdown. Nada más.

BLOQUE 1 (Contenido LaTeX):
```latex
\section{Nombre Sección}
\subsection{Subsección 1.1}
Texto académico con \cite{Key} ...
\begin{figure}[h]\centering\includegraphics[width=\linewidth]{fig.png}\caption{Desc}\label{fig:1}\end{figure}

```

BLOQUE 2 (Prompts de Imagen):

```json
{
  "fig1.png": "2D technical vector diagram..."
}

```

1. EXTENSIÓN: 600-800 palabras.
2. ESTRUCTURA: Solo \section{} y \subsection{} según lo listado.
3. CITAS: Usa \cite{clave} en línea. NUNCA menciones una referencia sin citarla.
4. FIGURAS/TABLAS: Usa entornos figure/table estándar de IEEE.
5. AL FINAL: Un único bloque ```json con prompts para DALL-E 3.

FORMATO DE FIGURAS:
\begin{figure}[h]
\centering
\includegraphics[width=\linewidth]{nombre_archivo.png}
\caption{Descripción técnica}
\label{fig:nombre_archivo}
\end{figure}

REGLAS PARA PROMPTS DE IMAGEN:

* Estilo: '2D technical vector diagram, engineering schematic, flat design'
* Fondo: Blanco puro, sin texto interno, sin perspectiva 3D
* Colores: Azul cobalto (#0047AB), Gris técnico (#4A4A4A), Negro
* Evita: Sombras, gradientes, elementos decorativos