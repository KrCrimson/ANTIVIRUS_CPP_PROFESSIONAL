# 🛡️ Antivirus C++ Professional - Instalador Automático de Dependencias
# Script de instalación completa para Windows
# Ejecutar como Administrador: Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser

param(
    [switch]$SkipVisualStudio,
    [switch]$SkipChocolatey,
    [switch]$Verbose
)

$ErrorActionPreference = "Stop"

# Colores para output
$colors = @{
    Success = "Green"
    Warning = "Yellow" 
    Error = "Red"
    Info = "Cyan"
    Header = "Magenta"
}

function Write-ColorOutput {
    param([string]$Message, [string]$Color = "White")
    Write-Host $Message -ForegroundColor $colors[$Color]
}

function Test-Administrator {
    $currentUser = [Security.Principal.WindowsIdentity]::GetCurrent()
    $principal = New-Object Security.Principal.WindowsPrincipal($currentUser)
    return $principal.IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)
}

function Install-Chocolatey {
    Write-ColorOutput "🍫 Instalando Chocolatey Package Manager..." "Header"
    
    if (Get-Command choco -ErrorAction SilentlyContinue) {
        Write-ColorOutput "✅ Chocolatey ya está instalado" "Success"
        return
    }

    try {
        Set-ExecutionPolicy Bypass -Scope Process -Force
        [System.Net.ServicePointManager]::SecurityProtocol = [System.Net.ServicePointManager]::SecurityProtocol -bor 3072
        iex ((New-Object System.Net.WebClient).DownloadString('https://community.chocolatey.org/install.ps1'))
        
        # Refresh PATH
        $env:PATH = [System.Environment]::GetEnvironmentVariable("PATH", "Machine") + ";" + [System.Environment]::GetEnvironmentVariable("PATH", "User")
        
        Write-ColorOutput "✅ Chocolatey instalado correctamente" "Success"
    }
    catch {
        Write-ColorOutput "❌ Error instalando Chocolatey: $_" "Error"
        throw
    }
}

function Install-VisualStudioBuildTools {
    Write-ColorOutput "🔨 Instalando Visual Studio Build Tools 2022..." "Header"
    
    # Verificar si ya está instalado
    $vsWhere = "${env:ProgramFiles(x86)}\Microsoft Visual Studio\Installer\vswhere.exe"
    if (Test-Path $vsWhere) {
        $installations = & $vsWhere -products * -requires Microsoft.VisualStudio.Component.VC.Tools.x86.x64 -format json | ConvertFrom-Json
        if ($installations.Count -gt 0) {
            Write-ColorOutput "✅ Visual Studio Build Tools ya está instalado" "Success"
            return
        }
    }

    try {
        choco install visualstudio2022buildtools --package-parameters "--add Microsoft.VisualStudio.Component.VC.Tools.x86.x64 --add Microsoft.VisualStudio.Component.Windows11SDK.22000 --add Microsoft.VisualStudio.Component.VC.CMake.Project" -y
        Write-ColorOutput "✅ Visual Studio Build Tools 2022 instalado" "Success"
    }
    catch {
        Write-ColorOutput "❌ Error instalando Visual Studio Build Tools: $_" "Error"
        Write-ColorOutput "⚠️ Instalación manual requerida desde: https://visualstudio.microsoft.com/downloads/#build-tools-for-visual-studio-2022" "Warning"
    }
}

function Install-CMake {
    Write-ColorOutput "🏗️ Instalando CMake..." "Header"
    
    if (Get-Command cmake -ErrorAction SilentlyContinue) {
        $version = cmake --version | Select-String -Pattern "\d+\.\d+\.\d+"
        Write-ColorOutput "✅ CMake ya está instalado: $($version.Matches[0].Value)" "Success"
        return
    }

    try {
        choco install cmake -y
        Write-ColorOutput "✅ CMake instalado correctamente" "Success"
    }
    catch {
        Write-ColorOutput "❌ Error instalando CMake: $_" "Error"
        throw
    }
}

function Install-NodeJS {
    Write-ColorOutput "📦 Instalando Node.js..." "Header"
    
    if (Get-Command node -ErrorAction SilentlyContinue) {
        $version = node --version
        Write-ColorOutput "✅ Node.js ya está instalado: $version" "Success"
        return
    }

    try {
        choco install nodejs -y
        Write-ColorOutput "✅ Node.js instalado correctamente" "Success"
    }
    catch {
        Write-ColorOutput "❌ Error instalando Node.js: $_" "Error"
        throw
    }
}

function Install-Git {
    Write-ColorOutput "📋 Instalando Git..." "Header"
    
    if (Get-Command git -ErrorAction SilentlyContinue) {
        $version = git --version
        Write-ColorOutput "✅ Git ya está instalado: $version" "Success"
        return
    }

    try {
        choco install git -y
        Write-ColorOutput "✅ Git instalado correctamente" "Success"
    }
    catch {
        Write-ColorOutput "❌ Error instalando Git: $_" "Error"
        throw
    }
}

function Refresh-Environment {
    Write-ColorOutput "🔄 Actualizando variables de entorno..." "Info"
    
    # Refresh PATH from registry
    $machinePath = [System.Environment]::GetEnvironmentVariable("PATH", "Machine")
    $userPath = [System.Environment]::GetEnvironmentVariable("PATH", "User")
    $env:PATH = $machinePath + ";" + $userPath
    
    # Update current session
    if (Get-Command refreshenv -ErrorAction SilentlyContinue) {
        refreshenv
    }
}

function Test-Installation {
    Write-ColorOutput "🧪 Verificando instalaciones..." "Header"
    
    $tests = @(
        @{ Name = "Git"; Command = "git"; Args = "--version" },
        @{ Name = "CMake"; Command = "cmake"; Args = "--version" },
        @{ Name = "Node.js"; Command = "node"; Args = "--version" },
        @{ Name = "NPM"; Command = "npm"; Args = "--version" }
    )
    
    $allPassed = $true
    
    foreach ($test in $tests) {
        try {
            $result = & $test.Command $test.Args 2>$null
            if ($LASTEXITCODE -eq 0) {
                Write-ColorOutput "✅ $($test.Name): OK" "Success"
            }
            else {
                Write-ColorOutput "❌ $($test.Name): FAILED" "Error"
                $allPassed = $false
            }
        }
        catch {
            Write-ColorOutput "❌ $($test.Name): NOT FOUND" "Error"
            $allPassed = $false
        }
    }
    
    return $allPassed
}

function Setup-Project {
    Write-ColorOutput "🚀 Configurando proyecto..." "Header"
    
    $projectRoot = $PSScriptRoot
    Write-ColorOutput "📂 Directorio del proyecto: $projectRoot" "Info"
    
    # Backend setup
    $backendPath = Join-Path $projectRoot "backend"
    if (Test-Path $backendPath) {
        Write-ColorOutput "🔧 Configurando backend C++..." "Info"
        Push-Location $backendPath
        
        try {
            if (Test-Path "build") {
                Remove-Item "build" -Recurse -Force
            }
            
            cmake -B build -S . -G "Visual Studio 17 2022" -T host=x64 -A x64
            Write-ColorOutput "✅ Backend configurado" "Success"
        }
        catch {
            Write-ColorOutput "❌ Error configurando backend: $_" "Error"
        }
        finally {
            Pop-Location
        }
    }
    
    # Frontend setup
    $frontendPath = Join-Path $projectRoot "frontend"
    if (Test-Path $frontendPath) {
        Write-ColorOutput "📱 Configurando frontend..." "Info"
        Push-Location $frontendPath
        
        try {
            if (Test-Path "node_modules") {
                Write-ColorOutput "🗑️ Limpiando node_modules existente..." "Info"
                Remove-Item "node_modules" -Recurse -Force
            }
            
            npm install
            Write-ColorOutput "✅ Frontend configurado" "Success"
        }
        catch {
            Write-ColorOutput "❌ Error configurando frontend: $_" "Error"
        }
        finally {
            Pop-Location
        }
    }
}

function Show-NextSteps {
    Write-ColorOutput "`n🎯 ¡Instalación completada!" "Header"
    Write-ColorOutput "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" "Header"
    
    Write-ColorOutput "`n🚀 Próximos pasos:" "Info"
    Write-ColorOutput "1. Abrir PowerShell NUEVO (para cargar variables de entorno)" "Info"
    Write-ColorOutput "2. Ejecutar:" "Info"
    Write-ColorOutput "   cd backend" "Info"
    Write-ColorOutput "   cmake --build build --config Debug --target AntivirusCPP" "Info"
    Write-ColorOutput "   .\build\Debug\AntivirusCPP.exe" "Info"
    
    Write-ColorOutput "`n📱 Para el frontend:" "Info"
    Write-ColorOutput "   cd frontend" "Info"
    Write-ColorOutput "   npm start" "Info"
    
    Write-ColorOutput "`n📋 Verificar instalación:" "Info"
    Write-ColorOutput "   .\verify_installation.ps1" "Info"
    
    Write-ColorOutput "`n🔗 URLs importantes:" "Info"
    Write-ColorOutput "   - Backend API: http://localhost:8080/api/status" "Info"
    Write-ColorOutput "   - Documentación: README.md" "Info"
    Write-ColorOutput "   - Sprint actual: Sprint 2 (Frontend React)" "Info"
}

# ========================================
# MAIN EXECUTION
# ========================================

try {
    Write-ColorOutput "🛡️ ANTIVIRUS C++ PROFESSIONAL - INSTALADOR AUTOMÁTICO" "Header"
    Write-ColorOutput "═══════════════════════════════════════════════════════════════" "Header"
    
    # Verificar permisos de administrador
    if (-not (Test-Administrator)) {
        Write-ColorOutput "⚠️ Este script requiere permisos de administrador" "Warning"
        Write-ColorOutput "💡 Ejecuta: Start-Process PowerShell -Verb RunAs" "Info"
        Write-ColorOutput "   Luego ejecuta este script nuevamente" "Info"
        exit 1
    }
    
    Write-ColorOutput "✅ Ejecutando como administrador" "Success"
    Write-ColorOutput "⏱️ Tiempo estimado: 10-15 minutos" "Info"
    Write-ColorOutput ""
    
    # Instalación paso a paso
    if (-not $SkipChocolatey) {
        Install-Chocolatey
        Refresh-Environment
    }
    
    Install-Git
    Install-CMake
    Install-NodeJS
    
    if (-not $SkipVisualStudio) {
        Install-VisualStudioBuildTools
    }
    
    Refresh-Environment
    
    # Verificar instalaciones
    Write-ColorOutput "`n" 
    $success = Test-Installation
    
    if ($success) {
        Setup-Project
        Show-NextSteps
        Write-ColorOutput "`n✅ ¡INSTALACIÓN COMPLETADA EXITOSAMENTE!" "Success"
    }
    else {
        Write-ColorOutput "`n❌ Algunas instalaciones fallaron. Revisa los errores arriba." "Error"
        Write-ColorOutput "💡 Intenta ejecutar el script nuevamente o instala manualmente los componentes faltantes." "Warning"
        exit 1
    }
}
catch {
    Write-ColorOutput "`n💥 Error crítico durante la instalación:" "Error"
    Write-ColorOutput $_.Exception.Message "Error"
    Write-ColorOutput "`n🔧 Soluciones sugeridas:" "Warning"
    Write-ColorOutput "1. Ejecutar como administrador" "Warning"
    Write-ColorOutput "2. Verificar conexión a internet" "Warning"
    Write-ColorOutput "3. Desactivar temporalmente el antivirus" "Warning"
    Write-ColorOutput "4. Ejecutar: Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser" "Warning"
    exit 1
}