import os
import subprocess
import glob
import time

def run_full_workflow(base_path):
    # 1. Definir rutas basadas en la estructura workflow/workflow/outputs
    outputs_path = os.path.join(base_path, "outputs")
    
    if not os.path.exists(outputs_path):
        print(f"Error: No se encontró el directorio {outputs_path}")
        return

    # 2. Contar archivos section_*.tex existentes
    section_files = glob.glob(os.path.join(outputs_path, "section_*.tex"))
    total_sections = len(section_files)

    if total_sections == 0:
        print("No se encontraron archivos section_*.tex para procesar.")
        return

    print(f"🚀 Iniciando proceso para {total_sections} secciones detectadas.")
    print(f"⏱️ Pausa de seguridad: 5 segundos entre secciones.\n")

    # 3. Iterar sobre cada sección para Redacción e Inyección
    for n in range(1, total_sections + 1):
        prompt_file = os.path.join(outputs_path, f"prompt_section_{n}.txt")
        reply_file = os.path.join(base_path, "section.md")
        target_tex = os.path.join(outputs_path, f"section_{n}.tex")
        manifest_json = os.path.join(outputs_path, "image_manifest.json")

        if not os.path.exists(prompt_file):
            print(f"⚠️ Saltando sección {n}: No se encontró {prompt_file}")
            continue

        print(f"--- 📝 Procesando Sección {n} de {total_sections} ---")

        # Paso A: Consultar a la IA
        cmd_ask = ["py", r".\workflow\app.py", "--ask", prompt_file, "--reply", reply_file]
        print(f"🤖 Generando contenido con IA...")
        subprocess.run(cmd_ask, check=True)

        # Paso B: Inyectar contenido y actualizar manifiesto
        cmd_inject = ["py", r".\workflow\injector.py", reply_file, target_tex, manifest_json]
        print(f"💉 Inyectando LaTeX y actualizando manifiesto...")
        subprocess.run(cmd_inject, check=True)
        
        print(f"✅ Sección {n} completada.")

        # Pausa entre secciones
        if n < total_sections:
            print(f"⏳ Esperando 5 segundos...")
            time.sleep(5)
            print("-" * 40)

    # 4. GENERACIÓN DE PLACEHOLDERS (Cierre del flujo)
    print("\n" + "="*40)
    print("🖼️  GENERANDO PLACEHOLDERS DE IMÁGENES")
    print("="*40)
    
    # Llamamos al script de placeholders pasando la carpeta de outputs
    cmd_placeholders = ["py", r".\workflow\generate_placeholders.py", outputs_path]
    
    try:
        subprocess.run(cmd_placeholders, check=True)
        print("✅ Archivos de imagen (placeholders) creados correctamente.")
    except subprocess.CalledProcessError as e:
        print(f"❌ Error al generar placeholders: {e}")

    print("\n🏁 Flujo de trabajo totalizado. El paper está listo para compilar en Overleaf.")

if __name__ == "__main__":
    # Ruta base del proyecto
    path_arg = "workflow/workflow"
    run_full_workflow(path_arg)