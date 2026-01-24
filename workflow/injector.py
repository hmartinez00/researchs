import json
import re
import os
import sys

def extract_and_distribute(source_md, target_tex_path, target_json_path):
    if not os.path.exists(source_md):
        print(f"Error: No se encuentra el archivo fuente {source_md}")
        return

    with open(source_md, 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. Extraer bloques usando Regex
    latex_match = re.search(r'```latex\s*(.*?)\s*```', content, re.DOTALL)
    json_match = re.search(r'```json\s*(.*?)\s*```', content, re.DOTALL)

    # 2. Procesar LaTeX (Sobreescritura de la sección específica)
    if latex_match:
        latex_content = latex_match.group(1).strip()
        # Aseguramos que el directorio del archivo tex exista
        os.makedirs(os.path.dirname(target_tex_path), exist_ok=True)
        with open(target_tex_path, 'w', encoding='utf-8') as f:
            f.write(latex_content)
        print(f"✅ LaTeX inyectado en: {target_tex_path}")
    else:
        print("⚠️ No se encontró bloque LaTeX en la fuente.")

    # 3. Procesar JSON (Fusión con contenido previo)
    if json_match:
        new_prompts = json.loads(json_match.group(1).strip())
        
        # Cargar manifiesto existente o crear uno vacío
        existing_data = {}
        if os.path.exists(target_json_path):
            with open(target_json_path, 'r', encoding='utf-8') as f:
                try:
                    existing_data = json.load(f)
                except json.JSONDecodeError:
                    existing_data = {}

        # Fusionar: Las nuevas llaves sobreescriben o se agregan
        for key, prompt in new_prompts.items():
            # Si la llave ya existe como objeto (del script anterior), actualizamos el prompt_ia
            if key in existing_data and isinstance(existing_data[key], dict):
                existing_data[key]["prompt_ia"] = prompt
            else:
                # Si no existe, lo agregamos directamente
                existing_data[key] = prompt

        # Guardar el manifiesto actualizado
        os.makedirs(os.path.dirname(target_json_path), exist_ok=True)
        with open(target_json_path, 'w', encoding='utf-8') as f:
            json.dump(existing_data, f, indent=4, ensure_ascii=False)
        print(f"✅ JSON actualizado y fusionado en: {target_json_path}")
    else:
        print("⚠️ No se encontró bloque JSON en la fuente.")

if __name__ == "__main__":
    # Ejemplo de uso: 
    # py injector.py "ai_response.md" "outputs/section_1.tex" "outputs/image_manifest.json"
    if len(sys.argv) < 4:
        print("Uso: py injector.py <input_md> <target_tex> <target_json>")
    else:
        extract_and_distribute(sys.argv[1], sys.argv[2], sys.argv[3])