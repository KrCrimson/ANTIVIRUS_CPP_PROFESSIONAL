# Antivirus Professional - Guía del Desarrollador
===============================================

## 🚀 Ejecución Rápida

### **Para Usuarios (Producción)**
```bash
# Interfaz principal del antivirus (RECOMENDADO)
python frontend/main.py

# Launcher optimizado para producción (alternativo)
python production_launcher.py
```

### **Para Desarrolladores**
```bash
# Interfaz gráfica directa
python frontend/main.py

# Demo completo con todas las funciones
python dev/demos/demo_completo.py

# Tests TDD completos
python dev/reports/run_all_tdd_tests.py
```

## 📁 Estructura Reorganizada

### ✅ **Archivos de Producción (Core)**
```
🛡️ Core del Sistema:
├── frontend/main.py                        # Interfaz principal (PUNTO DE ENTRADA)
├── production_launcher.py                  # Launcher alternativo
├── core/                                   # Motor antivirus
├── plugins/                                # Detectores y handlers
├── config/                                 # Configuración
├── utils/                                  # Utilidades
├── models/                                 # Modelos ML
└── threat_intel/                           # Base de datos de amenazas
```

### 🔧 **Archivos de Desarrollo**
```
🛠️ Herramientas de Desarrollo:
├── dev/debug_scripts/                      # Scripts de debugging
├── dev/demos/                              # Demos y prototipos  
├── dev/reports/                            # Reportes TDD y análisis
├── dev/generated/                          # Código auto-generado
├── tests/                                  # Suite completa de tests
│   ├── tdd_01_api_hooking_detection/
│   ├── tdd_02_port_detection/
│   ├── ... (8 suites TDD)
│   ├── integration/                        # Tests de integración
│   └── iast_tests/                         # Tests IAST
└── docs/                                   # Documentación técnica
```

## 🧪 Testing y Calidad

### **Tests Organizados por Categorías**
- **TDD Suites (8 completas)**: Detección API hooking, puertos, CPU, memoria, etc.
- **Integration Tests**: Tests end-to-end del sistema completo
- **IAST Tests**: Tests específicos de seguridad interactiva
- **Plugin Tests**: Tests individuales de cada plugin

### **Ejecutar Tests**
```bash
# Todos los tests TDD (82 tests)
python dev/reports/run_all_tdd_tests.py

# Suite específica
python -m pytest tests/tdd_01_api_hooking_detection/

# Tests de integración
python -m pytest tests/integration/
```

## 🛡️ Características del Sistema

### **Detectores Activos (7 Plugins)**
1. **behavior_detector**: Análisis heurístico de comportamiento
2. **keylogger_detector**: Detección especializada de keyloggers  
3. **ml_detector**: Machine Learning para detección avanzada
4. **network_detector**: Monitoreo de conexiones de red
5. **alert_manager**: Gestión de alertas y notificaciones
6. **logger_handler**: Sistema de logging estructurado
7. **quarantine_handler**: Manejo de archivos en cuarentena

### **Interfaz de Usuario**
- **Dear PyGui**: Aceleración GPU para rendimiento óptimo
- **Fuente moderna**: Segoe UI Variable para mejor legibilidad
- **Logs en tiempo real**: Conectados directamente al backend
- **Dashboard interactivo**: Métricas y gráficos en vivo

## 🔧 Desarrollo y Debug

### **Scripts de Debug Disponibles**
- `dev/debug_scripts/debug_memory.py`: Análisis de memoria
- `dev/debug_scripts/debug_consensus.py`: Debug del sistema de consenso
- `dev/debug_scripts/debug_api_scoring.py`: Debug de scoring de APIs

### **Demos Funcionales**
- `dev/demos/demo_completo.py`: Demo completo del sistema
- `dev/demos/simple_backend.py`: Backend simplificado para testing
- `dev/demos/professional_ui_robust.py`: UI robusta con todas las funciones

## 📊 Métricas y Reportes

### **Reportes Disponibles**
- `dev/reports/full_tdd_report.py`: Reporte completo TDD
- `dev/reports/tdd_report.py`: Reporte básico de tests
- `dev/reports/backend_analysis.py`: Análisis del backend
- `dev/reports/refactor_report.py`: Reporte de refactorización

### **Estado Actual del Sistema**
- ✅ **82 tests TDD** pasando exitosamente
- ✅ **7 plugins** activos y funcionando
- ✅ **Detecciones reales** de keyloggers y amenazas
- ✅ **UI profesional** con métricas en tiempo real
- ✅ **Backend completo** sin dependencias de demos

## 🚀 Deploy y Distribución

### **Paquete de Producción**
Incluir solo archivos core:
```bash
# Directorios esenciales
core/ plugins/ frontend/ config/ utils/ models/ threat_intel/ docs/

# Archivos principales  
production_launcher.py install_dependencies.py 
register_plugins.py requirements.txt README.md
```

### **Excluir en Producción**
```bash
# Directorios de desarrollo
dev/ tests/ backup_configs/ xd/ mdsd/

# Archivos temporales
*.log *.tmp *_backup.py debug_* demo_*
```

## ⚡ Comandos Útiles

### **Instalación y Setup**
```bash
# Instalar dependencias
python install_dependencies.py

# Verificar dependencias
python dev/check_dependencies.py

# Registrar plugins
python register_plugins.py
```

### **Desarrollo**
```bash
# Linting
flake8 .

# Tests con pytest
pytest tests/

# Construcción
.\Make.ps1
```

## 🆘 Solución de Problemas

### **Problemas Comunes**
1. **Módulos faltantes**: Ejecutar `install_dependencies.py`
2. **Plugins no detectados**: Verificar `register_plugins.py`
3. **UI no carga**: Verificar Dear PyGui con `pip install dearpygui`
4. **Tests fallan**: Verificar estructura con `dev/check_dependencies.py`

### **Logs de Debug**
- Logs principales: `logs/antivirus.log`
- Logs de UI: `logs/frontend.log`  
- Logs de tests: `logs/test_system.log`

---
**Antivirus Professional v2.0** - Sistema completo de detección y protección