import os
import argparse
from datetime import datetime

try:
    from jinja2 import Environment, Template
except Exception:
    # Defer friendly error until run, so import doesn't crash tools or static analyzers
    Environment = None
    Template = None

# --- Configuración de Archivos (por defecto, relativos al directorio del script) ---
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ARCHIVO_ORIGEN = os.path.join(BASE_DIR, 'archivo1.md')
# archivo de destino por defecto
ARCHIVO_DESTINO = os.path.join(BASE_DIR, 'archivo2.md')
# archivo de plantilla por defecto (si existe)
ARCHIVO_PLANTILLA = os.path.join(BASE_DIR, 'plantilla.md')
# ---------------------------------------------------------------------------------

def crear_o_actualizar_archivo(contenido_dinamico, archivo_destino=ARCHIVO_DESTINO, archivo_origen=ARCHIVO_ORIGEN, plantilla_text=None):
    """
    Define la plantilla de contenido y la escribe en el archivo de destino.
    El marcador de posición "{contenido_insertado}" se reemplaza por el
    contenido dinámico extraído del archivo de origen.
    """
    
    # 1. PLANTILLA EXTERNA OBLIGATORIA (no usamos plantillas embebidas en el script)
    if plantilla_text is None:
        raise ValueError("No se encontró plantilla. Pasa --plantilla o coloca una plantilla por defecto en 'workflow/plantilla.md'.")
    
    # 2. Renderizar plantilla con Jinja2 (acepta {{contenido_insertado}}, {{archivo_origen}}, {{archivo_destino}}, {{fecha}})
    if Environment is None or Template is None:
        print("❌ Error: Jinja2 no está instalado. Instala con: python -m pip install jinja2")
        return

    env = Environment(autoescape=False)
    template = env.from_string(plantilla_text)
    context = {
        'contenido_insertado': contenido_dinamico,
        'archivo_origen': os.path.basename(archivo_origen),
        'archivo_destino': os.path.basename(archivo_destino),
        'fecha': datetime.now().strftime('%Y-%m-%d')
    }
    contenido_final = template.render(**context)

    # 3. Escribir en el Archivo de Destino
    try:
        # Escribir archivo
        with open(archivo_destino, 'w', encoding='utf-8') as f:
            f.write(contenido_final.strip())  # .strip() limpia los espacios en blanco iniciales
        
        print(f"✅ ¡Éxito! El archivo '{os.path.basename(archivo_destino)}' ha sido actualizado.")
        print(f"Ruta completa: {archivo_destino}")
        print(f"Contenido insertado: {len(contenido_dinamico)} caracteres.")
        
    except IOError as e:
        print(f"❌ Error al escribir en el archivo {archivo_destino}: {e}")

# --- FUNCIÓN PRINCIPAL DE EJECUCIÓN ---
def ejecutar_actualizacion(archivo_origen=ARCHIVO_ORIGEN, archivo_destino=ARCHIVO_DESTINO, plantilla_text=None):
    try:
        # 1. Leer el contenido del archivo de origen
        with open(archivo_origen, 'r', encoding='utf-8') as f:
            contenido_origen = f.read()

        # 2. Llamar a la función para crear/actualizar el archivo de destino
        # Nota: si se desea pasar `plantilla_text`, la función externa debe pasarla como argumento
        crear_o_actualizar_archivo(contenido_origen, archivo_destino=archivo_destino, archivo_origen=archivo_origen, plantilla_text=plantilla_text)

    except FileNotFoundError:
        print(f"❌ Error: El archivo de origen '{archivo_origen}' no se encontró.")
        print(f"Asegúrate de que el archivo exista en la ruta: {archivo_origen}")
    except Exception as e:
        print(f"❌ Ocurrió un error inesperado: {e}")

# Ejecutar el script
def _parse_args():
    parser = argparse.ArgumentParser(description='Actualizar archivo destino a partir de un archivo origen.')
    parser.add_argument('--origen', '-o', help='Archivo origen (ruta o nombre). Si no se indica, se busca archivo1.md al lado del script.', default=ARCHIVO_ORIGEN)
    parser.add_argument('--destino', '-d', help='Archivo destino (ruta o nombre). Si no se indica, se usa archivo2.md al lado del script.', default=ARCHIVO_DESTINO)
    parser.add_argument('--plantilla', '-p', help='Archivo de plantilla (ruta o nombre). Si no se indica, se busca workflow/plantilla.md. Plantilla debe contener {{contenido_insertado}} y puede usar {{archivo_origen}}, {{archivo_destino}}, y {{fecha}}', default=None)
    return parser.parse_args()


def cargar_plantilla(archivo_plantilla=None):
    """Carga el texto de plantilla desde un archivo si se especifica; devuelve None si no existe.

    La plantilla puede contener el marcador {{contenido_insertado}} o {contenido_insertado}.
    """
    if archivo_plantilla is None:
        return None
    try:
        if not os.path.isabs(archivo_plantilla) and not os.path.dirname(archivo_plantilla):
            # nombre simple: interpretarlo relativo al script
            archivo_plantilla = os.path.join(BASE_DIR, archivo_plantilla)
        with open(archivo_plantilla, 'r', encoding='utf-8') as f:
            return f.read()
    except FileNotFoundError:
        print(f"❌ Error: La plantilla '{archivo_plantilla}' no se encontró.")
        return None
    except Exception as e:
        print(f"❌ Error leyendo la plantilla: {e}")
        return None


if __name__ == "__main__":
    args = _parse_args()
    # Si el usuario pasa solo el nombre de archivo (sin separador de ruta), lo interpretamos relativo al script
    origen = args.origen if os.path.isabs(args.origen) or os.path.dirname(args.origen) else os.path.join(BASE_DIR, args.origen)
    destino = args.destino if os.path.isabs(args.destino) or os.path.dirname(args.destino) else os.path.join(BASE_DIR, args.destino)
    # Cargar la plantilla (si se especificó o existe plantilla por defecto)
    plantilla_arg = args.plantilla if hasattr(args, 'plantilla') else None
    plantilla_text = None
    if plantilla_arg:
        plantilla_text = cargar_plantilla(plantilla_arg)
    elif os.path.exists(ARCHIVO_PLANTILLA):
        plantilla_text = cargar_plantilla(ARCHIVO_PLANTILLA)
    else:
        # Plantilla obligatoria para la ejecución
        print("❌ Error: No hay plantilla especificada ni existe 'workflow/plantilla.md'. Pasa --plantilla o crea workflow/plantilla.md.")
        exit(1)

    ejecutar_actualizacion(origen, destino, plantilla_text=plantilla_text)