# Verificador de Instalacion - Antivirus C++ Professional
# Version simplificada sin caracteres especiales

$ErrorActionPreference = "Continue"

function Test-Command {
    param([string]$Command, [string]$Arguments = "", [string]$Name)
    try {
        if ($Arguments) {
            $result = & $Command $Arguments 2>$null
        } else {
            $result = & $Command 2>$null
        }
        
        if ($LASTEXITCODE -eq 0) {
            $version = ($result | Select-Object -First 1).ToString().Trim()
            Write-Host "[OK] $Name : $version" -ForegroundColor Green
            return $true
        }
    }
    catch {
        Write-Host "[ERROR] $Name : NO INSTALADO" -ForegroundColor Red
        return $false
    }
    return $false
}

function Test-VisualStudio {
    $vsWhere = "${env:ProgramFiles(x86)}\Microsoft Visual Studio\Installer\vswhere.exe"
    if (Test-Path $vsWhere) {
        try {
            $installations = & $vsWhere -products * -requires Microsoft.VisualStudio.Component.VC.Tools.x86.x64 -format json | ConvertFrom-Json
            if ($installations.Count -gt 0) {
                $version = $installations[0].catalog.productDisplayVersion
                Write-Host "[OK] Visual Studio Build Tools: $version" -ForegroundColor Green
                return $true
            }
        }
        catch {}
    }
    Write-Host "[ERROR] Visual Studio Build Tools: NO INSTALADO" -ForegroundColor Red
    return $false
}

function Test-ProjectStructure {
    Write-Host "`nVerificando estructura del proyecto..." -ForegroundColor Cyan
    
    $requiredPaths = @(
        @{ Path = "backend"; Name = "Backend C++" },
        @{ Path = "backend\CMakeLists.txt"; Name = "CMake config" },
        @{ Path = "backend\src"; Name = "Codigo fuente C++" },
        @{ Path = "frontend"; Name = "Frontend Electron" },
        @{ Path = "frontend\package.json"; Name = "Package.json" },
        @{ Path = "README.md"; Name = "Documentacion" }
    )
    
    $allExists = $true
    foreach ($item in $requiredPaths) {
        if (Test-Path $item.Path) {
            Write-Host "[OK] $($item.Name)" -ForegroundColor Green
        }
        else {
            Write-Host "[ERROR] $($item.Name): $($item.Path)" -ForegroundColor Red
            $allExists = $false
        }
    }
    
    return $allExists
}

function Test-BackendBuild {
    Write-Host "`nVerificando configuracion del backend..." -ForegroundColor Cyan
    
    if (-not (Test-Path "backend\build")) {
        Write-Host "[WARNING] Directorio build no existe. Ejecuta: cmake -B build -S ." -ForegroundColor Yellow
        return $false
    }
    
    if (Test-Path "backend\build\Debug\AntivirusCPP.exe") {
        Write-Host "[OK] Ejecutable AntivirusCPP.exe encontrado" -ForegroundColor Green
        return $true
    }
    elseif (Test-Path "backend\build\AntivirusCPP.sln") {
        Write-Host "[WARNING] Proyecto configurado pero no compilado" -ForegroundColor Yellow
        Write-Host "[INFO] Ejecuta: cmake --build build --config Debug --target AntivirusCPP" -ForegroundColor Cyan
        return $false
    }
    else {
        Write-Host "[ERROR] Backend no configurado correctamente" -ForegroundColor Red
        return $false
    }
}

function Test-FrontendSetup {
    Write-Host "`nVerificando configuracion del frontend..." -ForegroundColor Cyan
    
    if (-not (Test-Path "frontend\node_modules")) {
        Write-Host "[WARNING] Node modules no instalados" -ForegroundColor Yellow
        Write-Host "[INFO] Ejecuta: cd frontend && npm install" -ForegroundColor Cyan
        return $false
    }
    
    Write-Host "[OK] Node modules instalados" -ForegroundColor Green
    return $true
}

# MAIN EXECUTION
Write-Host "==================================================================" -ForegroundColor Magenta
Write-Host "VERIFICADOR DE INSTALACION - ANTIVIRUS C++ PROFESSIONAL" -ForegroundColor Magenta
Write-Host "==================================================================" -ForegroundColor Magenta

Write-Host "`nInformacion del sistema:" -ForegroundColor Cyan
Write-Host "PowerShell: $($PSVersionTable.PSVersion)" -ForegroundColor White

Write-Host "`nVerificando dependencias..." -ForegroundColor Cyan

# Test all dependencies
$results = @{}
$results.Git = Test-Command "git" "--version" "Git"
$results.CMake = Test-Command "cmake" "--version" "CMake" 
$results.NodeJS = Test-Command "node" "--version" "Node.js"
$results.NPM = Test-Command "npm" "--version" "NPM"
$results.VisualStudio = Test-VisualStudio
$results.ProjectStructure = Test-ProjectStructure
$results.BackendBuild = Test-BackendBuild
$results.FrontendSetup = Test-FrontendSetup

# Count successes
$successCount = ($results.Values | Where-Object { $_ -eq $true }).Count
$totalCount = $results.Count

Write-Host "`nResultado: $successCount/$totalCount verificaciones exitosas" -ForegroundColor Cyan

# Determine if system is ready
$criticalComponents = @("Git", "CMake", "NodeJS", "NPM", "VisualStudio", "ProjectStructure")
$allCriticalReady = $true
foreach ($component in $criticalComponents) {
    if (-not $results[$component]) {
        $allCriticalReady = $false
        break
    }
}

Write-Host "`n==================================================================" -ForegroundColor Magenta
Write-Host "RESUMEN DE VERIFICACION" -ForegroundColor Magenta
Write-Host "==================================================================" -ForegroundColor Magenta

if ($allCriticalReady) {
    Write-Host "SISTEMA LISTO PARA DESARROLLO!" -ForegroundColor Green
    Write-Host "`nComandos para ejecutar:" -ForegroundColor Cyan
    Write-Host "# Terminal 1 - Backend:" -ForegroundColor White
    Write-Host "cd backend" -ForegroundColor White
    Write-Host "cmake --build build --config Debug --target AntivirusCPP" -ForegroundColor White
    Write-Host ".\build\Debug\AntivirusCPP.exe" -ForegroundColor White
    Write-Host "`n# Terminal 2 - Frontend:" -ForegroundColor White
    Write-Host "cd frontend" -ForegroundColor White
    Write-Host "npm start" -ForegroundColor White
    Write-Host "`nAcceso:" -ForegroundColor Cyan
    Write-Host "- Backend API: http://localhost:8080/api/status" -ForegroundColor White
    Write-Host "- Frontend: Se abrira automaticamente" -ForegroundColor White
}
else {
    Write-Host "CONFIGURACION INCOMPLETA" -ForegroundColor Yellow
    Write-Host "`nAcciones requeridas:" -ForegroundColor Cyan
    Write-Host "1. Ejecutar: .\install_dependencies.ps1" -ForegroundColor Yellow
    Write-Host "2. Reiniciar PowerShell despues de la instalacion" -ForegroundColor Yellow
    Write-Host "3. Ejecutar este script nuevamente" -ForegroundColor Yellow
}

Write-Host "`nEstado actual del proyecto:" -ForegroundColor Cyan
Write-Host "Sprint 1: [OK] COMPLETADO (Backend C++)" -ForegroundColor Green
Write-Host "Sprint 2: [WIP] EN PROGRESO (Frontend React)" -ForegroundColor Yellow
Write-Host "Sprint 3: [TODO] PENDIENTE (Deteccion Avanzada)" -ForegroundColor White
Write-Host "Sprint 4: [TODO] PENDIENTE (Produccion)" -ForegroundColor White

if ($allCriticalReady) {
    exit 0
}
else {
    exit 1
}