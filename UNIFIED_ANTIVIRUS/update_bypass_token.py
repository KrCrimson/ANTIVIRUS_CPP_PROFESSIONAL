#!/usr/bin/env python3
"""
Script para actualizar el bypass token de Vercel en el antivirus
================================================================

Uso:
python update_bypass_token.py <nuevo_token>
"""

import json
import sys
import shutil
from pathlib import Path

def update_bypass_token(new_token):
    """Actualiza el bypass token en los archivos de configuración"""
    
    # Rutas de configuración
    config_paths = [
        Path("config/web_logging_config.json"),  # Fuente
        Path("C:/Program Files/AntivirusProfesional/config/web_logging_config.json")  # Instalado
    ]
    
    for config_path in config_paths:
        if config_path.exists():
            try:
                # Leer configuración actual
                with open(config_path, 'r', encoding='utf-8') as f:
                    config = json.load(f)
                
                # Actualizar token
                if 'web_logging' in config:
                    config['web_logging']['bypass_token'] = new_token
                    config['_last_updated'] = "2025-12-01"
                    
                    # Escribir configuración actualizada
                    with open(config_path, 'w', encoding='utf-8') as f:
                        json.dump(config, f, indent=2, ensure_ascii=False)
                    
                    print(f"✅ Token actualizado en: {config_path}")
                else:
                    print(f"❌ Estructura incorrecta en: {config_path}")
                    
            except Exception as e:
                print(f"❌ Error actualizando {config_path}: {e}")
        else:
            print(f"⚠️ Archivo no encontrado: {config_path}")

def main():
    if len(sys.argv) != 2:
        print("Uso: python update_bypass_token.py <nuevo_token>")
        print("Ejemplo: python update_bypass_token.py abc123xyz456")
        return
    
    new_token = sys.argv[1]
    print(f"🔄 Actualizando bypass token a: {new_token}")
    
    update_bypass_token(new_token)
    
    print("\n🎯 Para aplicar los cambios:")
    print("1. Reiniciar el antivirus si está ejecutándose")
    print("2. O recompilar e instalar nueva versión")

if __name__ == "__main__":
    main()