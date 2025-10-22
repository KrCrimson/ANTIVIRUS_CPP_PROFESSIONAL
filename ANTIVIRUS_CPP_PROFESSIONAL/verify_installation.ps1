# 🔍 Verificador de Instalación - Antivirus C++ Professional
# Script para verificar que todas las dependencias están correctamente instaladas

$ErrorActionPreference = "Continue"

# Colores para output
function Write-ColorOutput {
    param([string]$Message, [string]$Color = "White")
    $colors = @{
        Success = "Green"
        Warning = "Yellow" 
        Error = "Red"
        Info = "Cyan"
        Header = "Magenta"
    }
    Write-Host $Message -ForegroundColor $colors[$Color]
}

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
            Write-ColorOutput "✅ $Name`: $version" "Success"
            return $true
        }
    }
    catch {
        Write-ColorOutput "❌ $Name`: NO INSTALADO" "Error"
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
                Write-ColorOutput "✅ Visual Studio Build Tools: $version" "Success"
                return $true
            }
        }
        catch {}
    }
    Write-ColorOutput "❌ Visual Studio Build Tools: NO INSTALADO" "Error"
    return $false
}

function Test-ProjectStructure {
    Write-ColorOutput "`n📂 Verificando estructura del proyecto..." "Header"
    
    $requiredPaths = @(
        @{ Path = "backend"; Type = "folder"; Name = "Backend C++" },
        @{ Path = "backend\CMakeLists.txt"; Type = "file"; Name = "CMake config" },
        @{ Path = "backend\src"; Type = "folder"; Name = "Código fuente C++" },
        @{ Path = "frontend"; Type = "folder"; Name = "Frontend Electron" },
        @{ Path = "frontend\package.json"; Type = "file"; Name = "Package.json" },
        @{ Path = "README.md"; Type = "file"; Name = "Documentación" }
    )
    
    $allExists = $true
    foreach ($item in $requiredPaths) {
        if (Test-Path $item.Path) {
            Write-ColorOutput "✅ $($item.Name)" "Success"
        }
        else {
            Write-ColorOutput "❌ $($item.Name): $($item.Path)" "Error"
            $allExists = $false
        }
    }
    
    return $allExists
}

function Test-BackendBuild {
    Write-ColorOutput "`n🔨 Verificando configuración del backend..." "Header"
    
    if (-not (Test-Path "backend\build")) {
        Write-ColorOutput "⚠️  Directorio build no existe. Ejecuta: cmake -B build -S ." "Warning"
        return $false
    }
    
    if (Test-Path "backend\build\Debug\AntivirusCPP.exe") {
        Write-ColorOutput "✅ Ejecutable AntivirusCPP.exe encontrado" "Success"
        return $true
    }
    elseif (Test-Path "backend\build\AntivirusCPP.sln") {
        Write-ColorOutput "⚠️  Proyecto configurado pero no compilado" "Warning"
        Write-ColorOutput "💡 Ejecuta: cmake --build build --config Debug --target AntivirusCPP" "Info"
        return $false
    }
    else {
        Write-ColorOutput "❌ Backend no configurado correctamente" "Error"
        return $false
    }
}

function Test-FrontendSetup {
    Write-ColorOutput "`n📱 Verificando configuración del frontend..." "Header"
    
    if (-not (Test-Path "frontend\node_modules")) {
        Write-ColorOutput "⚠️  Node modules no instalados" "Warning"
        Write-ColorOutput "💡 Ejecuta: cd frontend && npm install" "Info"
        return $false
    }
    
    Write-ColorOutput "✅ Node modules instalados" "Success"
    return $true
}

function Show-SystemInfo {
    Write-ColorOutput "`n💻 Información del sistema:" "Header"
    Write-ColorOutput "Sistema: $(Get-ComputerInfo | Select-Object -ExpandProperty WindowsProductName)" "Info"
    Write-ColorOutput "Versión: $(Get-ComputerInfo | Select-Object -ExpandProperty WindowsVersion)" "Info"
    Write-ColorOutput "PowerShell: $($PSVersionTable.PSVersion)" "Info"
    Write-ColorOutput "Arquitectura: $(Get-ComputerInfo | Select-Object -ExpandProperty CsProcessors | Select-Object -First 1 -ExpandProperty Architecture)" "Info"
}

function Show-NextSteps {
    param([bool]$AllReady)
    
    Write-ColorOutput "`n📋 RESUMEN DE VERIFICACIÓN" "Header"
    Write-ColorOutput "═══════════════════════════════════════════════════════════════" "Header"
    
    if ($AllReady) {
        Write-ColorOutput "✅ ¡SISTEMA LISTO PARA DESARROLLO!" "Success"
        Write-ColorOutput "`n🚀 Comandos para ejecutar:" "Info"
        Write-ColorOutput "# Terminal 1 - Backend:" "Info"
        Write-ColorOutput "cd backend" "Info"
        Write-ColorOutput "cmake --build build --config Debug --target AntivirusCPP" "Info"
        Write-ColorOutput ".\build\Debug\AntivirusCPP.exe" "Info"
        Write-ColorOutput "`n# Terminal 2 - Frontend:" "Info"
        Write-ColorOutput "cd frontend" "Info"
        Write-ColorOutput "npm start" "Info"
        Write-ColorOutput "`n🌐 Acceso:" "Info"
        Write-ColorOutput "- Backend API: http://localhost:8080/api/status" "Info"
        Write-ColorOutput "- Frontend: Se abrirá automáticamente" "Info"
    }
    else {
        Write-ColorOutput "⚠️  CONFIGURACIÓN INCOMPLETA" "Warning"
        Write-ColorOutput "`n🔧 Acciones requeridas:" "Info"
        Write-ColorOutput "1. Ejecutar: .\install_dependencies.ps1" "Warning"
        Write-ColorOutput "2. Reiniciar PowerShell después de la instalación" "Warning"
        Write-ColorOutput "3. Ejecutar este script nuevamente" "Warning"
    }
}

# ========================================
# MAIN EXECUTION
# ========================================

Write-ColorOutput "🔍 VERIFICADOR DE INSTALACIÓN - ANTIVIRUS C++ PROFESSIONAL" "Header"
Write-ColorOutput "═══════════════════════════════════════════════════════════════" "Header"

Show-SystemInfo

Write-ColorOutput "`n🧪 Verificando dependencias..." "Header"

# Test all dependencies
$results = @{
    Git = Test-Command "git" "--version" "Git"
    CMake = Test-Command "cmake" "--version" "CMake" 
    NodeJS = Test-Command "node" "--version" "Node.js"
    NPM = Test-Command "npm" "--version" "NPM"
    VisualStudio = Test-VisualStudio
    ProjectStructure = Test-ProjectStructure
    BackendBuild = Test-BackendBuild
    FrontendSetup = Test-FrontendSetup
}

# Count successes
$successCount = ($results.Values | Where-Object { $_ -eq $true }).Count
$totalCount = $results.Count

Write-ColorOutput "`n📊 Resultado: $successCount/$totalCount verificaciones exitosas" "Info"

# Determine if system is ready
$criticalComponents = @("Git", "CMake", "NodeJS", "NPM", "VisualStudio", "ProjectStructure")
$allCriticalReady = $true
foreach ($component in $criticalComponents) {
    if (-not $results[$component]) {
        $allCriticalReady = $false
        break
    }
}

Show-NextSteps -AllReady $allCriticalReady

if ($allCriticalReady) {
    Write-ColorOutput "`n🎯 Estado actual del proyecto:" "Header"
    Write-ColorOutput "Sprint 1: ✅ COMPLETADO (Backend C++)" "Success"
    Write-ColorOutput "Sprint 2: 🔄 EN PROGRESO (Frontend React)" "Warning"
    Write-ColorOutput "Sprint 3: ⏳ PENDIENTE (Detección Avanzada)" "Info"
    Write-ColorOutput "Sprint 4: ⏳ PENDIENTE (Producción)" "Info"
    exit 0
}
else {
    exit 1
}