import json
import re
import os
import sys

def slugify(text):
    """Convierte el nombre del tema en un nombre de carpeta válido."""
    if not text:
        return "investigacion_nueva"
    text = text.lower().replace(" ", "_")
    return re.sub(r'(?u)[^-\w.]', '', text)

def extract_json_blocks(content):
    """
    Extrae TODOS los bloques JSON del contenido.
    Retorna: (json_estructura_principal, dict_mapas_por_seccion)
    """
    # Encontrar todos los bloques ```json ... ```
    json_blocks = re.findall(r'```json\s*(\{.*?\})\s*```', content, re.DOTALL)
    
    if not json_blocks:
        return None, {}
    
    # El PRIMER bloque JSON siempre es la estructura principal (tiene "titulo" y "secciones")
    estructura_principal = None
    mapas_por_seccion = {}
    
    for block in json_blocks:
        try:
            data = json.loads(block)
            # Identificar si es la estructura principal o un mapa seccional
            if "titulo" in data and "secciones" in data:
                estructura_principal = data
            elif "mapa_uso" in data or "seccion_nro" in data:
                # Es un mapa de uso de referencias
                nro_seccion = data.get("seccion_nro", data.get("seccion", 0))
                mapas_por_seccion[nro_seccion] = data
        except json.JSONDecodeError:
            continue
    
    return estructura_principal, mapas_por_seccion

def generate_research_files(input_file, project_name=None):
    if not os.path.exists(input_file):
        print(f"Error: No se encuentra {input_file}")
        return

    with open(input_file, 'r', encoding='utf-8') as f:
        content = f.read()

    # Limpieza de caracteres invisibles
    content = content.replace('\u00a0', ' ')

    # 🔧 CORRECCIÓN 1: Extraer estructura principal Y mapas de uso
    data, mapas_referencias = extract_json_blocks(content)
    
    if not data:
        print("Error: No se encontró el JSON de estructura principal (debe contener 'titulo' y 'secciones').")
        return

    # Extraer bloques BibTeX
    bib_blocks = re.findall(r'```bib(?:tex)?\s*(.*?)\s*```', content, re.DOTALL)

    if not bib_blocks:
        print("Error: No se encontraron bloques BibTeX en el archivo.")
        return

    # 2. Gestión de Directorio del Proyecto
    if not project_name:
        project_name = data.get("titulo", "investigacion_nueva")

    input_dir = os.path.dirname(os.path.abspath(input_file))
    folder_name = slugify(project_name)
    output_path = os.path.join(input_dir, folder_name)

    if not os.path.exists(output_path):
        os.makedirs(output_path)
        print(f"Carpeta creada exitosamente en: {output_path}")
    else:
        print(f"Usando carpeta existente: {output_path}")

    def path(filename):
        return os.path.join(output_path, filename)

    # 3. Guardar references.bib
    full_bib_content = '\n\n'.join([b.strip() for b in bib_blocks])
    with open(path('references.bib'), 'w', encoding='utf-8') as f:
        f.write(full_bib_content)

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
\usepackage{amsmath, amssymb, amsfonts, amsthm}
\usepackage{graphicx}
\usepackage{booktabs}
\usepackage{array}
\usepackage{url}
\usepackage{hyperref}
\usepackage{color, xcolor}
\usepackage[backend=biber, style=ieee, natbib=true]{biblatex}

% --- CONFIGURACIÓN DE BIBLIOGRAFÍA ---
\addbibresource{references.bib}

% --- METADATOS DEL DOCUMENTO ---
\title{""" + data.get("titulo", project_name) + r"""}

\author{\IEEEauthorblockN{Lic. Héctor Martínez\\}
\IEEEauthorblockA{Unidad de Telecomunicaciones\\
Agencia Bolivariana para Actividades Espaciales\\
Email: hmartinez@abae.gob.ve}}

\begin{document}
\maketitle

\input{abstract.tex}

"""

    # --- BLOQUE DE MANIFIESTO DE IMÁGENES ---
    manifest_path = path('image_manifest.json')
    manifest_data = {}
    if os.path.exists(manifest_path):
        try:
            with open(manifest_path, 'r', encoding='utf-8') as mf:
                manifest_data = json.load(mf)
        except json.JSONDecodeError:
            manifest_data = {}

    for sec in sections:
        n = sec.get('nro', 0)
        sec_title = sec.get('titulo_seccion', f"Seccion {n}")
        main_tex += f"\\input{{section_{n}.tex}}\n"
        
        # 🔧 CORRECCIÓN 2: Obtener el mapa de uso para esta sección
        mapa_uso = mapas_referencias.get(n, {})
        mapa_detalle = mapa_uso.get("mapa_uso", {})
        
        # Construir instrucciones detalladas de citación
        instrucciones_citacion = []
        if mapa_detalle:
            instrucciones_citacion.append("\n📚 MAPA DE USO DE REFERENCIAS (OBLIGATORIO):")
            for key, info in mapa_detalle.items():
                razon = info.get("razon_seleccion", "Sin justificación")
                guia = info.get("guia_redaccion", "Integrar de forma natural")
                subseccion = info.get("subseccion_destino", "Cualquiera")
                instrucciones_citacion.append(f"\n• **{key}** (Subsección {subseccion}):")
                instrucciones_citacion.append(f"  - Razón: {razon}")
                instrucciones_citacion.append(f"  - Instrucción: {guia}")
        
        instrucciones_citacion_text = '\n'.join(instrucciones_citacion) if instrucciones_citacion else ""
        
        # Archivo .tex para la sección
        with open(path(f"section_{n}.tex"), 'w', encoding='utf-8') as f:
            f.write(f"% Contenido para la sección: {sec_title}\n")
            f.write(f"\\section{{{sec_title}}}\n")

        # 🔧 CORRECCIÓN 2 (cont.): Archivo de Prompt MEJORADO con restricciones modulares
        with open(path(f"prompt_section_{n}.txt"), 'w', encoding='utf-8') as f:
            f.write(f"=== SPRINT DE ESCRITURA: SECCIÓN {n} ===\n\n")
            f.write(f"PAPER: {data.get('titulo', project_name)}\n")
            f.write(f"SECCIÓN: {sec_title}\n\n")
            
            f.write("--- CONTEXTO Y OBJETIVOS ---\n")
            f.write(f"OBJETIVOS: {', '.join(sec.get('objetivos', []))}\n")
            f.write(f"SUBSECCIONES REQUERIDAS: {', '.join(sec.get('subsecciones', []))}\n")
            f.write(f"INSUMOS (Tablas/Ecuaciones/Figuras): {', '.join(sec.get('insumos', []))}\n\n")
            
            f.write("--- CITAS BIBLIOGRÁFICAS OBLIGATORIAS ---\n")
            f.write(f"Claves BibTeX: {', '.join(sec.get('llaves_bibtex', []))}\n")
            
            if instrucciones_citacion_text:
                f.write(instrucciones_citacion_text)
            else:
                f.write("\n⚠️ ADVERTENCIA: No se encontró mapa de uso para esta sección. Integra las citas de forma coherente.\n")
            
            f.write("\n\n--- ⛔ RESTRICCIONES MODULARES (CRÍTICO) ---\n")
            f.write("Este fragmento se insertará vía \\input{section_N.tex} en un main.tex YA CONFIGURADO.\n")
            f.write("PROHIBIDO INCLUIR:\n")
            f.write("  • \\documentclass, \\begin{document}, \\end{document}\n")
            f.write("  • \\usepackage{}, \\addbibresource{}, \\bibliographystyle{}, \\bibliography{}\n")
            f.write("  • \\begin{filecontents}{...} ... \\end{filecontents}\n")
            f.write("  • Preambulo, metadatos, autor, título o configuración de bibliografía.\n")
            f.write("  • Comentarios explicativos fuera de LaTeX.\n\n")
            
            f.write("--- ✅ INSTRUCCIONES DE SALIDA ---\n")

            f.write("\n\n--- ⚙️ FORMATO DE SALIDA ESTRICTO (OBLIGATORIO) ---\n")
            f.write("Tu respuesta debe contener EXACTAMENTE dos bloques de código Markdown. Nada más.\n\n")
            f.write("BLOQUE 1 (Contenido LaTeX):\n")
            f.write("```latex\n")
            f.write("\\section{Nombre Sección}\n")
            f.write("\\subsection{Subsección 1.1}\n")
            f.write("Texto académico con \\cite{Key} ...\n")
            f.write("\\begin{figure}[h]\\centering\\includegraphics[width=\\linewidth]{fig.png}\\caption{Desc}\\label{fig:1}\\end{figure}\n")
            f.write("```\n\n")
            f.write("BLOQUE 2 (Prompts de Imagen):\n")
            f.write("```json\n")
            f.write("{\n")
            f.write('  "fig1.png": "2D technical vector diagram..."\n')
            f.write("}\n")
            f.write("```\n\n")

            f.write("1. EXTENSIÓN: 600-800 palabras.\n")
            f.write("2. ESTRUCTURA: Solo \\section{} y \\subsection{} según lo listado.\n")
            f.write("3. CITAS: Usa \\cite{clave} en línea. NUNCA menciones una referencia sin citarla.\n")
            f.write("4. FIGURAS/TABLAS: Usa entornos figure/table estándar de IEEE.\n")
            f.write("5. AL FINAL: Un único bloque ```json con prompts para DALL-E 3.\n\n")
            
            f.write("FORMATO DE FIGURAS:\n")
            f.write("\\begin{figure}[h]\n\\centering\n\\includegraphics[width=\\linewidth]{nombre_archivo.png}\n\\caption{Descripción técnica}\n\\label{fig:nombre_archivo}\n\\end{figure}\n\n")
            
            f.write("REGLAS PARA PROMPTS DE IMAGEN:\n")
            f.write("- Estilo: '2D technical vector diagram, engineering schematic, flat design'\n")
            f.write("- Fondo: Blanco puro, sin texto interno, sin perspectiva 3D\n")
            f.write("- Colores: Azul cobalto (#0047AB), Gris técnico (#4A4A4A), Negro\n")
            f.write("- Evita: Sombras, gradientes, elementos decorativos\n")

        # Actualizar manifiesto de imágenes
        for insumo in sec.get('insumos', []):
            if "Fig" in insumo or "Imagen" in insumo or "Figure" in insumo:
                img_key = slugify(insumo) + ".png"
                if img_key not in manifest_data:
                    manifest_data[img_key] = {
                        "seccion": n,
                        "descripcion_original": insumo,
                        "prompt_ia": "Pendiente de generación por el Sprint de Escritura"
                    }

    # Guardar manifiesto
    with open(manifest_path, 'w', encoding='utf-8') as mf:
        json.dump(manifest_data, mf, indent=4, ensure_ascii=False)

    # Finalizar main.tex
    main_tex += "\n% --- BIBLIOGRAFÍA ---\n%\\nocite{*}\n" + r"\printbibliography" + "\n\\end{document}"
    with open(path('main.tex'), 'w', encoding='utf-8') as f:
        f.write(main_tex)

    # --- BLOQUE REGISTER PROMPT ---
    with open(path('prompt_register.txt'), 'w', encoding='utf-8') as f:
        f.write(f'Necesito ingresar en el sistema de gestión documental de la Agencia los datos de la investigación: **{data.get("titulo", project_name)}**.\n\n')
        f.write('Campos requeridos:\n')
        f.write('* Title\n')
        f.write('* Description\n')
        f.write('* General Objective\n')
        f.write('* Specific Objectives\n')
        f.write('* Justification\n')
        f.write('* Methodology\n')
        f.write('* Scope (máximo 200 caracteres)\n')
        f.write('* Activities\n')
        f.write('* Resources\n')
        f.write('* Limitations\n\n')
        f.write('Proporciona los valores en español basándote en el abstract y la estructura del paper.')
    # ---------------------------------------

    print(f"✅ Éxito. Archivos generados en: {folder_name}")
    print(f"📊 Mapas de uso detectados: {len(mapas_referencias)} secciones")
    if mapas_referencias:
        print(f"   Secciones con mapa: {sorted(mapas_referencias.keys())}")

if __name__ == "__main__":
    file_arg = sys.argv[1] if len(sys.argv) > 1 else 'workflow/workflow/research_plan.md'
    name_arg = sys.argv[2] if len(sys.argv) > 2 else 'outputs'
    
    generate_research_files(file_arg, name_arg)