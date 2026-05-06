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


def extract_document_blocks(content):
    """
    Extrae todos los bloques de contenido relevantes del archivo.
    Retorna: (json_estructura_principal, dict_mapas_por_seccion, lista_bibtex)
    """
    json_blocks = re.findall(r'```json\s*(\{.*?\})\s*```', content, re.DOTALL)
    bib_blocks = re.findall(r'```bib(?:tex)?\s*(.*?)\s*```', content, re.DOTALL)
    
    if not json_blocks:
        return None, {}, bib_blocks
    
    estructura_principal = None
    mapas_por_seccion = {}
    
    for block in json_blocks:
        try:
            data = json.loads(block)
            if "titulo" in data and "secciones" in data:
                estructura_principal = data
            elif "mapa_uso" in data or "seccion_nro" in data:
                nro_seccion = data.get("seccion_nro", data.get("seccion", 0))
                mapas_por_seccion[nro_seccion] = data
        except json.JSONDecodeError:
            continue
    
    return estructura_principal, mapas_por_seccion, bib_blocks


def create_output_directory(input_file, project_name):
    input_dir = os.path.dirname(os.path.abspath(input_file))
    folder_name = slugify(project_name)
    output_path = os.path.join(input_dir, folder_name)

    if not os.path.exists(output_path):
        os.makedirs(output_path)
        print(f"Carpeta creada exitosamente en: {output_path}")
    else:
        print(f"Usando carpeta existente: {output_path}")

    return output_path


def load_image_manifest(output_path):
    manifest_path = os.path.join(output_path, 'image_manifest.json')
    if os.path.exists(manifest_path):
        try:
            with open(manifest_path, 'r', encoding='utf-8') as mf:
                return json.load(mf)
        except json.JSONDecodeError:
            return {}
    return {}


def save_image_manifest(output_path, manifest_data):
    manifest_path = os.path.join(output_path, 'image_manifest.json')
    with open(manifest_path, 'w', encoding='utf-8') as mf:
        json.dump(manifest_data, mf, indent=4, ensure_ascii=False)


def write_section_tex_files(data, output_path):
    sections = data.get('secciones', [])
    created = []

    for sec in sections:
        n = sec.get('nro', 0)
        sec_title = sec.get('titulo_seccion', f'Seccion {n}')
        filename = os.path.join(output_path, f'section_{n}.tex')
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(f"% Contenido para la sección: {sec_title}\n")
            f.write(f"\\section{{{sec_title}}}\n")
        created.append(filename)

    print(f"✅ Generados {len(created)} archivos section_*.tex")
    return created


def build_citation_instructions(sec, mapas_referencias):
    n = sec.get('nro', 0)
    mapa_uso = mapas_referencias.get(n, {})
    mapa_detalle = mapa_uso.get('mapa_uso', {})
    instrucciones = []

    if mapa_detalle:
        instrucciones.append("\n📚 MAPA DE USO DE REFERENCIAS (OBLIGATORIO):")
        for key, info in mapa_detalle.items():
            razon = info.get('razon_seleccion', 'Sin justificación')
            guia = info.get('guia_redaccion', 'Integrar de forma natural')
            subseccion = info.get('subseccion_destino', 'Cualquiera')
            instrucciones.append(f"\n• **{key}** (Subsección {subseccion}):")
            instrucciones.append(f"  - Razón: {razon}")
            instrucciones.append(f"  - Instrucción: {guia}")

    return '\n'.join(instrucciones)


def write_prompt_section_files(data, mapas_referencias, output_path, project_name):
    sections = data.get('secciones', [])
    manifest_data = load_image_manifest(output_path)
    created = []

    for sec in sections:
        n = sec.get('nro', 0)
        sec_title = sec.get('titulo_seccion', f'Seccion {n}')
        filename = os.path.join(output_path, f'prompt_section_{n}.txt')
        instrucciones_citacion_text = build_citation_instructions(sec, mapas_referencias)

        with open(filename, 'w', encoding='utf-8') as f:
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

        created.append(filename)

        for insumo in sec.get('insumos', []):
            if 'Fig' in insumo or 'Imagen' in insumo or 'Figure' in insumo:
                img_key = slugify(insumo) + '.png'
                if img_key not in manifest_data:
                    manifest_data[img_key] = {
                        'seccion': n,
                        'descripcion_original': insumo,
                        'prompt_ia': 'Pendiente de generación por el Sprint de Escritura'
                    }

    save_image_manifest(output_path, manifest_data)
    print(f"✅ Generados {len(created)} archivos prompt_section_*.txt")
    return created


def write_register_prompt_file(data, output_path, project_name):
    filename = os.path.join(output_path, 'prompt_register.txt')
    with open(filename, 'w', encoding='utf-8') as f:
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
    print(f"✅ Generado archivo prompt_register.txt")
    return filename


def generate_section_files(input_file, project_name=None):
    if not os.path.exists(input_file):
        print(f"Error: No se encuentra {input_file}")
        return

    with open(input_file, 'r', encoding='utf-8') as f:
        content = f.read()

    content = content.replace('\u00a0', ' ')
    data, mapas_referencias, bib_blocks = extract_document_blocks(content)

    if not data:
        print("Error: No se encontró el JSON de estructura principal (debe contener 'titulo' y 'secciones').")
        return

    if not project_name:
        project_name = data.get('titulo', 'investigacion_nueva')

    output_path = create_output_directory(input_file, project_name)
    write_section_tex_files(data, output_path)


def generate_prompt_files(input_file, project_name=None):
    if not os.path.exists(input_file):
        print(f"Error: No se encuentra {input_file}")
        return

    with open(input_file, 'r', encoding='utf-8') as f:
        content = f.read()

    content = content.replace('\u00a0', ' ')
    data, mapas_referencias, bib_blocks = extract_document_blocks(content)

    if not data:
        print("Error: No se encontró el JSON de estructura principal (debe contener 'titulo' y 'secciones').")
        return

    if not project_name:
        project_name = data.get('titulo', 'investigacion_nueva')

    output_path = create_output_directory(input_file, project_name)
    write_prompt_section_files(data, mapas_referencias, output_path, project_name)


def generate_register_prompt_file(input_file, project_name=None):
    if not os.path.exists(input_file):
        print(f"Error: No se encuentra {input_file}")
        return

    with open(input_file, 'r', encoding='utf-8') as f:
        content = f.read()

    content = content.replace('\u00a0', ' ')
    data, mapas_referencias, bib_blocks = extract_document_blocks(content)

    if not data:
        print("Error: No se encontró el JSON de estructura principal (debe contener 'titulo' y 'secciones').")
        return

    if not project_name:
        project_name = data.get('titulo', 'investigacion_nueva')

    output_path = create_output_directory(input_file, project_name)
    write_register_prompt_file(data, output_path, project_name)


def generate_research_files(input_file, project_name=None):
    if not os.path.exists(input_file):
        print(f"Error: No se encuentra {input_file}")
        return

    with open(input_file, 'r', encoding='utf-8') as f:
        content = f.read()

    content = content.replace('\u00a0', ' ')
    data, mapas_referencias, bib_blocks = extract_document_blocks(content)

    if not data:
        print("Error: No se encontró el JSON de estructura principal (debe contener 'titulo' y 'secciones').")
        return

    if not bib_blocks:
        print("Error: No se encontraron bloques BibTeX en el archivo.")
        return

    if not project_name:
        project_name = data.get('titulo', 'investigacion_nueva')

    output_path = create_output_directory(input_file, project_name)
    write_section_tex_files(data, output_path)
    write_prompt_section_files(data, mapas_referencias, output_path, project_name)
    write_register_prompt_file(data, output_path, project_name)

    full_bib_content = '\n\n'.join([b.strip() for b in bib_blocks])
    with open(os.path.join(output_path, 'references.bib'), 'w', encoding='utf-8') as f:
        f.write(full_bib_content)

    abstract_content = data.get('abstract_preliminar', 'Abstract no disponible.')
    with open(os.path.join(output_path, 'abstract.tex'), 'w', encoding='utf-8') as f:
        f.write('\\begin{abstract}\n' + abstract_content + '\n\\end{abstract}')

    sections = data.get('secciones', [])
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
\title{""" + data.get('titulo', project_name) + r"""

\author{\IEEEauthorblockN{Lic. Héctor Martínez\\}
\IEEEauthorblockA{Unidad de Telecomunicaciones\\
Agencia Bolivariana para Actividades Espaciales\\
Email: hmartinez@abae.gob.ve}}

\begin{document}
\maketitle

\input{abstract.tex}

"""

    for sec in sections:
        n = sec.get('nro', 0)
        main_tex += f"\\input{{section_{n}.tex}}\n"

    main_tex += "\n% --- BIBLIOGRAFÍA ---\n%\\nocite{*}\n" + "\\printbibliography" + "\n\\end{document}"
    with open(os.path.join(output_path, 'main.tex'), 'w', encoding='utf-8') as f:
        f.write(main_tex)

    print(f"✅ Éxito. Archivos generados en: {project_name}")
    print(f"📊 Mapas de uso detectados: {len(mapas_referencias)} secciones")
    if mapas_referencias:
        print(f"   Secciones con mapa: {sorted(mapas_referencias.keys())}")


def print_usage():
    print('Uso: python sra_5.2.py [modo] [archivo_entrada] [nombre_proyecto]')
    print('Modos disponibles: all, sections, prompts, register')
    print('Ejemplo: python sra_5.2.py sections research_plan.md')


if __name__ == "__main__":
    mode = sys.argv[1] if len(sys.argv) > 1 else 'all'
    input_file = sys.argv[2] if len(sys.argv) > 2 else 'workflow/workflow/research_plan.md'
    project_name = sys.argv[3] if len(sys.argv) > 3 else None

    if mode == 'all':
        generate_research_files(input_file, project_name)
    elif mode == 'sections':
        generate_section_files(input_file, project_name)
    elif mode == 'prompts':
        generate_prompt_files(input_file, project_name)
    elif mode == 'register':
        generate_register_prompt_file(input_file, project_name)
    else:
        print_usage()
