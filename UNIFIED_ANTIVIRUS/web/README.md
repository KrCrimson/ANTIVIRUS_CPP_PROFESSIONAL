# Web dashboard (Flask + Bootstrap)

Este directorio contiene un scaffold mínimo para un dashboard servido por Flask y una interfaz sencilla con Bootstrap + Chart.js.

Requisitos:
- Python 3.8+
- Crear y activar un virtualenv (recomendado) y luego instalar dependencias:

PowerShell (Windows):

```powershell
python -m venv .venv; .\.venv\Scripts\Activate.ps1; pip install -r web/requirements.txt
```

Ejecutar la app (desarrollo):

```powershell
python web/app.py
# Abrir http://127.0.0.1:5000 en el navegador
```

Notas:
- El servicio lee un archivo de ejemplo `logs/test_system_structured.jsonl` (JSON Lines) si existe y usa esos registros como alertas.
- Esto es un punto de partida: sustituye los endpoints por llamadas al motor real (`core/engine.py` o `plugin_manager`) según la arquitectura de tu proyecto.
