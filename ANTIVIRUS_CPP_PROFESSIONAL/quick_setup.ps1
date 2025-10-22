# 🚀 Quick Setup - Antivirus C++ Professional
# Script rápido para configurar el proyecto después de clonar

Write-Host "🛡️ ANTIVIRUS C++ - CONFIGURACIÓN RÁPIDA" -ForegroundColor Magenta
Write-Host "════════════════════════════════════════════════" -ForegroundColor Magenta

# Verificar si estamos en el directorio correcto
if (-not (Test-Path "backend") -or -not (Test-Path "frontend")) {
    Write-Host "❌ Error: Ejecuta este script desde la raíz del proyecto" -ForegroundColor Red
    Write-Host "💡 Asegúrate de estar en: ANTIVIRUS_CPP_PROFESSIONAL/" -ForegroundColor Yellow
    exit 1
}

Write-Host "`n1️⃣ Configurando backend C++..." -ForegroundColor Cyan
Set-Location backend

if (Test-Path "build") {
    Write-Host "🗑️ Limpiando build anterior..." -ForegroundColor Yellow
    Remove-Item "build" -Recurse -Force
}

try {
    cmake -B build -S . -G "Visual Studio 17 2022" -T host=x64 -A x64
    Write-Host "✅ Backend configurado correctamente" -ForegroundColor Green
}
catch {
    Write-Host "❌ Error configurando backend: $_" -ForegroundColor Red
    Write-Host "💡 Verifica que Visual Studio 2022 esté instalado" -ForegroundColor Yellow
    Set-Location ..
    exit 1
}

Write-Host "`n2️⃣ Configurando frontend..." -ForegroundColor Cyan
Set-Location ../frontend

if (Test-Path "node_modules") {
    Write-Host "🗑️ Limpiando node_modules anterior..." -ForegroundColor Yellow
    Remove-Item "node_modules" -Recurse -Force
}

try {
    npm install
    Write-Host "✅ Frontend configurado correctamente" -ForegroundColor Green
}
catch {
    Write-Host "❌ Error configurando frontend: $_" -ForegroundColor Red
    Write-Host "💡 Verifica que Node.js esté instalado" -ForegroundColor Yellow
    Set-Location ..
    exit 1
}

Set-Location ..

Write-Host "`n🎯 ¡CONFIGURACIÓN COMPLETADA!" -ForegroundColor Green
Write-Host "══════════════════════════════════════════════" -ForegroundColor Green

Write-Host "`n🚀 Comandos para ejecutar:" -ForegroundColor Cyan
Write-Host "# Terminal 1 - Backend:" -ForegroundColor White
Write-Host "cd backend" -ForegroundColor Gray
Write-Host "cmake --build build --config Debug --target AntivirusCPP" -ForegroundColor Gray
Write-Host ".\build\Debug\AntivirusCPP.exe" -ForegroundColor Gray

Write-Host "`n# Terminal 2 - Frontend:" -ForegroundColor White
Write-Host "cd frontend" -ForegroundColor Gray
Write-Host "npm start" -ForegroundColor Gray

Write-Host "`n📋 Estado actual:" -ForegroundColor Yellow
Write-Host "✅ Sprint 1: Backend C++ funcional" -ForegroundColor Green
Write-Host "🔄 Sprint 2: Frontend en desarrollo (25%)" -ForegroundColor Yellow
Write-Host "⏳ Sprint 3-4: Pendientes" -ForegroundColor Gray

Write-Host "`n📖 Ver README.md para más detalles" -ForegroundColor Cyan