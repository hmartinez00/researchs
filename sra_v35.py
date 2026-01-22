import json
import re
import os
import sys

def slugify(text):
    """Convierte el nombre del tema en un nombre de carpeta válido."""
    text = text.lower().replace(" ", "_")
    return re.sub(r'(?u)[^-\w.]', '', text)

def generate_research_files(input_file, project_name=None):
    if not os.path.exists(input_file):
        print(f"Error: No se encuentra {input_file}")
        return

    with open(input_file, 'r', encoding='utf-8') as f:
        content = f.read()

    # Limpieza de caracteres invisibles
    content = content.replace('\u00a0', ' ')

    # 1. Extraer bloques JSON y BibTeX
    json_block = re.search(r'```json\s*(\{.*?\})\s*```', content, re.DOTALL)
    bib_block = re.search(r'```bib(?:tex)?\s*(.*?)\s*```', content, re.DOTALL)

    if not json_block or not bib_block:
        print("Error: Estructura del archivo .md incorrecta.")
        return

    try:
        data = json.loads(json_block.group(1))
    except json.JSONDecodeError as e:
        print(f"Error en JSON: {e}")
        return

    # 2. Gestión de Directorio del Proyecto
    # Si no se pasa nombre por parámetro, usa el título del JSON
    if not project_name:
        project_name = data.get("titulo", "investigacion_nueva")
    
    folder_name = slugify(project_name)
    
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)
        print(f"Carpeta creada: {folder_name}")
    else:
        print(f"Usando carpeta existente: {folder_name}")

    # Helper para rutas
    def path(filename):
        return os.path.join(folder_name, filename)

    # 3. Guardar references.bib
    with open(path('references.bib'), 'w', encoding='utf-8') as f:
        f.write(bib_block.group(1).strip())

    # 4. Guardar abstract.tex
    abstract_content = data.get("abstract_preliminar", "Abstract no disponible.")
    with open(path('abstract.tex'), 'w', encoding='utf-8') as f:
        f.write("\\begin{abstract}\n" + abstract_content + "\n\\end{abstract}")

    # 5. Generar main.tex y Secciones
    sections = data.get("secciones", [])
    main_tex = r"""\documentclass[10pt, journal, final, twocolumn, letterpaper]{IEEEtran}

% --- PREÁMBULO DE PAQUETES ---
\usepackage[utf8]{inputenc}
\usepackage[T1]{fontenc}
\usepackage{amsmath, amssymb, amsfonts, amsthm} % Matemáticas avanzadas
\usepackage{graphicx} % Inserción de imágenes
\usepackage{booktabs} % Tablas de alta calidad (estilo IEEE)
\usepackage{array} % Control de columnas en tablas
\usepackage{url} % Manejo de URLs
\usepackage{hyperref} % Hipervínculos
\usepackage{color, xcolor} % Colores para edición
\usepackage[backend=biber, style=ieee, natbib=true]{biblatex} % Bibliografía estilo IEEE

% --- CONFIGURACIÓN DE BIBLIOGRAFÍA ---
\addbibresource{references.bib}

% --- METADATOS DEL DOCUMENTO ---
\title{""" + data.get("titulo", project_name) + r"""}

\author{\IEEEauthorblockN{Lic. Héctor Martínez}
\IEEEauthorblockA{Unidad de Telecomunicaciones\\
Agencia Bolivariana para Actividades Espaciales\\
Email: hmartinez@abae.gob.ve}}

% --- ARCHIVO BIBLIOGRÁFICO (Placeholder para 50+ referencias) ---
\begin{filecontents}{references.bib}
@article{sample_ref2024,
  author = {Smith, J. and Doe, A.},
  title = {Quantum Attacks on Satellite Telemetry},
  journal = {IEEE Transactions on Aerospace and Electronic Systems},
  year = {2024},
  volume = {60},
  number = {1},
  pages = {100-115}
}
% Aquí se irán acumulando las 50+ referencias según la taxonomía definida.
\end{filecontents}

\begin{document}
\maketitle

\input{abstract.tex}

"""

    for sec in sections:
        n = sec.get('nro', 0)
        sec_title = sec.get('titulo_seccion', f"Seccion {n}")
        main_tex += f"\\input{{section_{n}.tex}}\n"
        
        # Archivo .tex vacío para la sección
        with open(path(f"section_{n}.tex"), 'w', encoding='utf-8') as f:
            f.write(f"% Contenido para la sección: {sec_title}\n")
            f.write(f"\\section{{{sec_title}}}\n")

        # Archivo de Prompt para la IA
        with open(path(f"prompt_section_{n}.txt"), 'w', encoding='utf-8') as f:
            f.write(f"--- SPRINT DE ESCRITURA: SECCIÓN {n} ---\n")
            f.write(f"Estamos trabajando en el paper: {data.get('titulo', project_name)}\n")
            f.write(f"**Tarea:** Redactar exclusivamente la siguiente sección en formato LaTeX IEEE.\n\n")
            f.write(f"SECCIÓN: {sec_title}\n")
            f.write(f"OBJETIVOS: {', '.join(sec.get('objetivos', []))}\n")
            f.write(f"SUBSECCIONES: {', '.join(sec.get('subsecciones', []))}\n")
            f.write(f"INSUMOS: {', '.join(sec.get('insumos', []))}\n")
            f.write(f"CITAS OBLIGATORIAS: {', '.join(sec.get('llaves_bibtex', []))}\n")
            f.write("-" * 50 + "\n")
            f.write("INSTRUCCIONES: Redacta 600 palabras en formato LaTeX de IEEE.\n")

    main_tex += "\n% --- BIBLIOGRAFÍA ---\n%\\nocite{*}\n" + r"\printbibliography" + "\n\\end{document}"
    with open(path('main.tex'), 'w', encoding='utf-8') as f:
        f.write(main_tex)

    print(f"Éxito. Archivos generados en el subdirectorio: {folder_name}")

if __name__ == "__main__":
    # Recibir nombre del tema desde la terminal
    # Uso: python script.py research_plan.md "Nombre del Tema"
    file_arg = sys.argv[1] if len(sys.argv) > 1 else 'research_plan.md'
    name_arg = sys.argv[2] if len(sys.argv) > 2 else None
    
    generate_research_files(file_arg, name_arg)