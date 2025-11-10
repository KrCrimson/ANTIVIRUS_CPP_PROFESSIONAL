# Reorganización del Proyecto Antivirus Professional
# ===============================================
# Este script mueve archivos a su ubicación organizacional correcta

Write-Host "🔧 Iniciando reorganización del proyecto..." -ForegroundColor Green

$baseDir = "c:\Users\windows10\Documents\GitHub\ANTIVIRUS_CPP_PROFESSIONAL\UNIFIED_ANTIVIRUS"

# 1. Mover archivos de debug a dev/debug_scripts
Write-Host "📁 Moviendo archivos de debug..." -ForegroundColor Yellow
$debugFiles = @(
    "debug_api_scoring.py",
    "debug_consensus.py", 
    "debug_memory.py"
)

foreach ($file in $debugFiles) {
    $source = Join-Path $baseDir $file
    $dest = Join-Path $baseDir "dev\debug_scripts\$file"
    if (Test-Path $source) {
        Move-Item -Path $source -Destination $dest -Force
        Write-Host "  ✅ $file -> dev/debug_scripts/" -ForegroundColor Green
    }
}

# 2. Mover archivos de demos y ejemplos
Write-Host "📁 Moviendo demos y ejemplos..." -ForegroundColor Yellow
$demoFiles = @(
    "demo_completo.py",
    "professional_ui_robust.py",
    "professional_ui_robust_backup.py",
    "simple_backend.py"
)

foreach ($file in $demoFiles) {
    $source = Join-Path $baseDir $file
    $dest = Join-Path $baseDir "dev\demos\$file"
    if (Test-Path $source) {
        Move-Item -Path $source -Destination $dest -Force
        Write-Host "  ✅ $file -> dev/demos/" -ForegroundColor Green
    }
}

# 3. Mover reportes y análisis
Write-Host "📁 Moviendo reportes y análisis..." -ForegroundColor Yellow
$reportFiles = @(
    "full_tdd_report.py",
    "refactor_report.py", 
    "tdd_report.py",
    "run_all_tdd_tests.py",
    "backend_analysis.py",
    "TDD_ENHANCEMENT_SUMMARY.md",
    "PROYECTO_COMPLETADO.md"
)

foreach ($file in $reportFiles) {
    $source = Join-Path $baseDir $file
    $dest = Join-Path $baseDir "dev\reports\$file"
    if (Test-Path $source) {
        Move-Item -Path $source -Destination $dest -Force
        Write-Host "  ✅ $file -> dev/reports/" -ForegroundColor Green
    }
}

# 4. Mover archivos generados
Write-Host "📁 Moviendo archivos generados..." -ForegroundColor Yellow
$generatedFiles = @(
    "generated_advanced_keylogger_detection.py"
)

foreach ($file in $generatedFiles) {
    $source = Join-Path $baseDir $file
    $dest = Join-Path $baseDir "dev\generated\$file"
    if (Test-Path $source) {
        Move-Item -Path $source -Destination $dest -Force
        Write-Host "  ✅ $file -> dev/generated/" -ForegroundColor Green
    }
}

# 5. Mover tests de integración
Write-Host "📁 Moviendo tests de integración..." -ForegroundColor Yellow
$integrationTests = @(
    "test_iast_integration.py",
    "test_production_integration.py"
)

foreach ($file in $integrationTests) {
    $source = Join-Path $baseDir $file
    $dest = Join-Path $baseDir "tests\integration\$file"
    if (Test-Path $source) {
        Move-Item -Path $source -Destination $dest -Force
        Write-Host "  ✅ $file -> tests/integration/" -ForegroundColor Green
    }
}

# 6. Mover archivos de backup y instalación a dev
Write-Host "📁 Moviendo archivos auxiliares..." -ForegroundColor Yellow
$auxFiles = @(
    "launcher_backup.py",
    "check_dependencies.py"
)

foreach ($file in $auxFiles) {
    $source = Join-Path $baseDir $file
    $dest = Join-Path $baseDir "dev\$file"
    if (Test-Path $source) {
        Move-Item -Path $source -Destination $dest -Force
        Write-Host "  ✅ $file -> dev/" -ForegroundColor Green
    }
}

# 7. Mover diagramas UML a docs
Write-Host "📁 Moviendo diagramas..." -ForegroundColor Yellow
if (Test-Path (Join-Path $baseDir "docs")) {
    $diagramFiles = @(
        "sequence_flow.puml",
        "simple_flow.puml"
    )
    
    foreach ($file in $diagramFiles) {
        $source = Join-Path $baseDir $file
        $dest = Join-Path $baseDir "docs\$file"
        if (Test-Path $source) {
            Move-Item -Path $source -Destination $dest -Force
            Write-Host "  ✅ $file -> docs/" -ForegroundColor Green
        }
    }
}

Write-Host "`n✅ Reorganización completada!" -ForegroundColor Green
Write-Host "📊 Estructura del proyecto optimizada para producción y desarrollo" -ForegroundColor Cyan