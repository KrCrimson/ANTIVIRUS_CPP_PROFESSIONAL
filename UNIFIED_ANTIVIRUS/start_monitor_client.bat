@echo off
echo ========================================
echo   CLIENTE DE MONITOREO WEB - ANTIVIRUS
echo ========================================
echo.

REM Verificar que Python está instalado
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Error: Python no está instalado o no está en PATH
    echo 💡 Instale Python desde https://python.org
    pause
    exit /b 1
)

REM Cambiar al directorio del script
cd /d "%~dp0"

REM Verificar que existe el script de cliente
if not exist "start_monitor_client.py" (
    echo ❌ Error: No se encuentra start_monitor_client.py
    echo 💡 Verifique que está en el directorio correcto
    pause
    exit /b 1
)

REM Verificar configuración
if not exist "client_monitor_config.json" (
    echo ❌ Error: No se encuentra client_monitor_config.json
    echo 💡 Ejecute primero: python setup_web_monitoring.py
    pause
    exit /b 1
)

echo ℹ️ Python encontrado: 
python --version
echo.

REM Ejecutar cliente Python
echo 🚀 Iniciando cliente de monitoreo...
echo.

python start_monitor_client.py

echo.
echo 🔚 Cliente de monitoreo finalizado
pause
