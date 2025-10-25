@echo off
echo Iniciando servidor de monitoreo web del antivirus...
echo.

REM Verificar que Python está instalado
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo Error: Python no está instalado o no está en PATH
    pause
    exit /b 1
)

REM Cambiar al directorio del script
cd /d "%~dp0"

REM Iniciar servidor
echo Servidor disponible en: http://localhost:8000
echo Dashboard: http://localhost:8000
echo API Docs: http://localhost:8000/docs
echo.
echo Presiona Ctrl+C para detener el servidor
echo.

python web_monitor_server.py

pause
