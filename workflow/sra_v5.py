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
# 2. Gestión de Directorio del Proyecto
    if not project_name:
        project_name = data.get("titulo", "investigacion_nueva")
    
    # Obtenemos la ruta del directorio donde está el archivo .md
    input_dir = os.path.dirname(os.path.abspath(input_file))
    
    # Creamos la ruta de salida combinando la carpeta del .md con el nombre del proyecto (ej: 'outputs')
    # Esto asegura que si el md está en workflow/workflow/, el output sea workflow/workflow/outputs/
    folder_name = slugify(project_name)
    output_path = os.path.join(input_dir, folder_name)
    
    if not os.path.exists(output_path):
        os.makedirs(output_path)
        print(f"Carpeta creada exitosamente en: {output_path}")
    else:
        print(f"Usando carpeta existente: {output_path}")

    # Helper para rutas (ahora usa output_path)
    def path(filename):
        return os.path.join(output_path, filename)

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

\author{\IEEEauthorblockN{Lic. Héctor Martínez\\}
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
            # f.write("INSTRUCCIONES: Redacta 600 palabras en formato LaTeX de IEEE.\n")
            # f.write("\n--- TAREA ADICIONAL: PROMPTS DE FIGURAS ---\n")
            # f.write("Al final de tu respuesta, para cada figura generada, proporciona un prompt descriptivo para DALL-E 3.\n")
            # f.write("REGLA DE ORO: Cada prompt debe pedir un '2D technical schematic' sobre fondo blanco, SIN REPETIR EL TITULO DE LA IMAGEN, enfocado en el flujo de datos descrito en tus párrafos.\n")

            f.write("INSTRUCCIONES DE SALIDA:\n")
            f.write("1. Redacta 600 palabras en formato LaTeX de IEEE.\n")
            f.write("2. Por cada figura que decidas incluir (mínimo las mencionadas en INSUMOS), usa: \\includegraphics[width=\\linewidth]{nombre_archivo.png}\n")
            f.write("\n3. AL FINAL DE TU RESPUESTA, entrega un bloque de código ```json con este formato:\n")
            f.write("{\n")
            f.write('  "nombre_archivo.png": "Prompt descriptivo para IA generadora de imagen",\n')
            f.write('  "nombre_archivo_2.png": "..." \n')
            f.write("}\n")
            f.write("\nREGLAS PARA LOS PROMPTS DE IMAGEN:\n")
            f.write("- Estilo: '2D technical vector diagram, engineering schematic, flat design'.\n")
            f.write("- Composición: Fondo blanco puro, sin perspectiva 3D, sin texto interno.\n")
            f.write("- Colores: Paleta técnica (Azul cobalto, Gris, Negro).\n")

    main_tex += "\n% --- BIBLIOGRAFÍA ---\n%\\nocite{*}\n" + r"\printbibliography" + "\n\\end{document}"
    with open(path('main.tex'), 'w', encoding='utf-8') as f:
        f.write(main_tex)


    # --- BLOQUE DE MANIFIESTO DE IMÁGENES ---
    # Definimos el nombre del archivo de control
    manifest_path = path('image_manifest.json')
    
    # Inicializamos o cargamos el manifiesto existente
    manifest_data = {}
    if os.path.exists(manifest_path):
        with open(manifest_path, 'r', encoding='utf-8') as mf:
            try:
                manifest_data = json.load(mf)
            except json.JSONDecodeError:
                manifest_data = {}

    # Agregamos los placeholders detectados en los insumos a la base de datos
    for insumo in sec.get('insumos', []):
        if "Fig" in insumo or "Imagen" in insumo:
            # El nombre del archivo se limpia para ser usado como llave
            img_key = slugify(insumo) + ".png"
            if img_key not in manifest_data:
                manifest_data[img_key] = {
                    "seccion": n,
                    "descripcion_original": insumo,
                    "prompt_ia": "Pendiente de generación por el Sprint de Escritura"
                }

    # Guardamos el manifiesto actualizado
    with open(manifest_path, 'w', encoding='utf-8') as mf:
        json.dump(manifest_data, mf, indent=4, ensure_ascii=False)
    # ---------------------------------------

    print(f"Éxito. Archivos generados en el subdirectorio: {folder_name}")

if __name__ == "__main__":
    # Recibir nombre del tema desde la terminal
    # Uso: python script.py research_plan.md "Nombre del Tema"
    file_arg = sys.argv[1] if len(sys.argv) > 1 else 'workflow/workflow/research_plan.md'
    name_arg = sys.argv[2] if len(sys.argv) > 2 else 'outputs'
    
    generate_research_files(file_arg, name_arg)
    # print(os.listdir())