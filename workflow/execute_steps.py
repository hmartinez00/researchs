"""execute_steps.py

Lee un archivo de pasos (steps_v1.txt) y ejecuta cada comando de manera secuencial.
Los comandos deben estar en líneas separadas, uno por línea.

Uso:
    py execute_steps.py [--steps-file STEPS_FILE]

Por defecto busca steps_v1.txt en el directorio del script.
"""

from __future__ import annotations
import argparse
import os
import subprocess
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding='utf-8')

BASE_DIR = Path(__file__).resolve().parent
DEFAULT_STEPS_FILE = BASE_DIR / 'steps_v1.txt'


def parse_args():
    parser = argparse.ArgumentParser(description='Ejecuta comandos de manera secuencial desde un archivo.')
    parser.add_argument('--steps-file', '-f', default=str(DEFAULT_STEPS_FILE), 
                       help='Archivo que contiene los comandos a ejecutar (por defecto: steps_v1.txt)')
    parser.add_argument('--dry-run', action='store_true', 
                       help='No ejecutar los comandos; solo mostrar qué se ejecutaría')
    return parser.parse_args()


def read_steps_file(steps_file: str) -> list[str]:
    """Lee el archivo de pasos y retorna una lista de comandos (líneas no vacías)."""
    steps_path = Path(steps_file)
    
    if not steps_path.exists():
        print(f"❌ Error: archivo de pasos no encontrado: {steps_path}")
        sys.exit(1)
    
    with open(steps_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    # Filtrar líneas vacías y comentarios (líneas que comienzan con #)
    commands = [line.strip() for line in lines if line.strip() and not line.strip().startswith('#')]
    
    return commands


def execute_commands(commands: list[str], dry_run: bool = False) -> None:
    """Ejecuta cada comando de manera secuencial."""
    total = len(commands)
    
    if total == 0:
        print("⚠️  No hay comandos para ejecutar.")
        return
    
    print(f"\n📋 Se ejecutarán {total} comando(s)\n")
    
    for idx, cmd in enumerate(commands, 1):
        print(f"\n{'='*80}")
        print(f"[{idx}/{total}] Ejecutando: {cmd}")
        print(f"{'='*80}")
        
        if dry_run:
            print("(modo dry-run: comando no ejecutado)")
            continue
        
        try:
            # Ejecutar el comando en la shell actual
            result = subprocess.run(cmd, shell=True, cwd=os.getcwd())
            
            if result.returncode != 0:
                print(f"\n⚠️  El comando #{idx} terminó con código de error: {result.returncode}")
                response = input("¿Continuar con el siguiente comando? (s/n): ").strip().lower()
                if response != 's':
                    print("❌ Ejecución cancelada por el usuario.")
                    sys.exit(1)
            else:
                print(f"\n✅ Comando #{idx} ejecutado exitosamente")
        
        except Exception as e:
            print(f"\n❌ Error al ejecutar comando #{idx}: {e}")
            response = input("¿Continuar con el siguiente comando? (s/n): ").strip().lower()
            if response != 's':
                print("❌ Ejecución cancelada por el usuario.")
                sys.exit(1)
    
    print(f"\n{'='*80}")
    print("✅ Todos los comandos se han ejecutado.")
    print(f"{'='*80}\n")


def main():
    args = parse_args()
    
    print(f"📂 Directorio de trabajo: {os.getcwd()}")
    print(f"📄 Archivo de pasos: {args.steps_file}")
    
    if args.dry_run:
        print("🔍 MODO DRY-RUN (sin ejecutar)\n")
    
    commands = read_steps_file(args.steps_file)
    
    print(f"\n📝 Comandos encontrados:\n")
    for idx, cmd in enumerate(commands, 1):
        print(f"  [{idx}] {cmd}")
    
    if not args.dry_run:
        response = input("\n¿Ejecutar los comandos? (s/n): ").strip().lower()
        if response != 's':
            print("❌ Ejecución cancelada por el usuario.")
            sys.exit(0)
    
    execute_commands(commands, dry_run=args.dry_run)


if __name__ == '__main__':
    main()
