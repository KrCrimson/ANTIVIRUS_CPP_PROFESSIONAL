#!/usr/bin/env python3
"""
Servidor web de monitoreo - Versión sin auto-reload para pruebas
"""

import uvicorn
import os
import sys

# Cambiar al directorio correcto
script_dir = os.path.dirname(os.path.abspath(__file__))
os.chdir(script_dir)

# Importar el servidor
from web_monitor_server import app

if __name__ == "__main__":
    print("Iniciando servidor web SIN auto-reload...")
    print("Dashboard: http://localhost:8888")
    print("API Docs: http://localhost:8888/docs")
    print("Para detener: Ctrl+C")
    print()
    
    try:
        uvicorn.run(
            app,
            host="0.0.0.0", 
            port=8888,
            reload=False,  # Sin auto-reload
            log_level="info"
        )
    except KeyboardInterrupt:
        print("\nServidor detenido por el usuario.")
    except Exception as e:
        print(f"Error iniciando servidor: {e}")
        sys.exit(1)