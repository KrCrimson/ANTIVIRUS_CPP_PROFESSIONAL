@echo off
echo ============================================
echo Instalando dependencias del antivirus
echo ============================================

cd /d "%~dp0"

echo.
echo Instalando dependencias principales...
pip install -r requirements.txt --user --quiet

if %ERRORLEVEL% EQU 0 (
    echo [OK] Dependencias instaladas correctamente
) else (
    echo [ERROR] Hubo problemas instalando algunas dependencias
    echo Por favor, ejecuta manualmente: pip install -r requirements.txt
)

echo.
echo Instalando dependencias de monitoreo web...
pip install -r requirements_web_monitor.txt --user --quiet

if %ERRORLEVEL% EQU 0 (
    echo [OK] Dependencias de monitoreo instaladas
) else (
    echo [ADVERTENCIA] Algunas dependencias de monitoreo no se instalaron
)

echo.
echo ============================================
echo Instalacion completada
echo ============================================
pause
