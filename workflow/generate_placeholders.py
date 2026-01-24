import json
import os
import sys
from PIL import Image, ImageDraw

def create_placeholders(project_folder):
    manifest_path = os.path.join(project_folder, 'image_manifest.json')
    
    if not os.path.exists(manifest_path):
        print(f"Error: No se encontró el manifiesto en {manifest_path}")
        return

    with open(manifest_path, 'r', encoding='utf-8') as f:
        manifest = json.load(f)

    print(f"--- Generando Placeholders en: {project_folder} ---")

    for filename, info in manifest.items():
        # Asegurar que el nombre tenga extensión .png
        if not filename.lower().endswith(('.png', '.jpg', '.jpeg')):
            filename += ".png"
            
        file_path = os.path.join(project_folder, filename)
        
        if os.path.exists(file_path):
            print(f"Omitiendo {filename}: Ya existe.")
            continue

        # Crear imagen gris
        img = Image.new('RGB', (800, 600), color=(220, 220, 220))
        d = ImageDraw.Draw(img)
        
        # Extraer información de manera segura según el formato del JSON
        if isinstance(info, dict):
            seccion = info.get('seccion', 'N/A')
            desc = info.get('descripcion_original', 'Diagrama Técnico')
        else:
            seccion = "Procesando..."
            desc = "Revisar Prompt en JSON"

        # Texto simple para el placeholder
        text = f"PLACEHOLDER\nFILE: {filename}\nSEC: {seccion}\n{desc[:40]}..."
        
        # Dibujar texto (usando fuente default si no hay una específica)
        d.text((40, 260), text, fill=(0, 0, 0))
        
        img.save(file_path)
        print(f"Creado satisfactoriamente: {filename}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Uso: python generate_placeholders.py nombre_de_la_carpeta")
    else:
        create_placeholders(sys.argv[1])