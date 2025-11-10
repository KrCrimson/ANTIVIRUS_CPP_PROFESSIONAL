# Estructura del Proyecto Antivirus Professional
===============================================

## 📁 Directorios Principales

### **Producción (Core del Sistema)**
```
📦 UNIFIED_ANTIVIRUS/
├── 🛡️ core/                    # Motor principal del antivirus
├── 🔌 plugins/                 # Detectores y manejadores
├── 🎨 frontend/                # Interfaz de usuario (Dear PyGui)
├── ⚙️  config/                  # Configuración del sistema
├── 🛠️ utils/                    # Utilidades del sistema
├── 🧠 models/                   # Modelos ML para detección
├── 🛡️ threat_intel/            # Inteligencia de amenazas
├── 📊 logs/                     # Logs del sistema en producción
└── 📚 docs/                     # Documentación oficial
```

### **Desarrollo y Testing**
```
📦 dev/                          # Archivos de desarrollo solamente
├── 🐛 debug_scripts/            # Scripts de debug y análisis
├── 🎭 demos/                    # Demos y prototipos
├── 📊 reports/                  # Reportes TDD y análisis
├── 🤖 generated/                # Código generado automáticamente
└── 🔧 check_dependencies.py     # Verificador de dependencias

📦 tests/                        # Suite completa de tests
├── 🧪 tdd_01_api_hooking_detection/
├── 🧪 tdd_02_port_detection/
├── 🧪 tdd_03_safe_process_validation/
├── 🧪 tdd_04_cpu_monitoring/
├── 🧪 tdd_05_detector_initialization/
├── 🧪 tdd_06_feature_extraction/
├── 🧪 tdd_07_consensus/
├── 🧪 tdd_08_memory_threshold/
├── 🔗 integration/              # Tests de integración
└── 🏭 iast_tests/               # Tests IAST específicos
```

## 🚀 Archivos de Ejecución Principal

### **Producción**
- `frontend/main.py` - **PUNTO DE ENTRADA PRINCIPAL**
- `production_launcher.py` - **Launcher alternativo con verificaciones**
- `install_dependencies.py` - **Instalador de dependencias**
- `register_plugins.py` - **Registrador de plugins**

### **Desarrollo**
- `dev/demos/demo_completo.py` - Demo completo del sistema
- `dev/demos/simple_backend.py` - Backend simplificado para testing
- `dev/reports/run_all_tdd_tests.py` - Ejecutor de todos los tests TDD

## 📋 Archivos de Configuración

- `requirements.txt` - Dependencias de producción
- `pytest.ini` - Configuración de pytest
- `.flake8` - Configuración de linting
- `Make.ps1` - Script de construcción
- `README.md` - Documentación principal

## 🎯 Propósito de la Reorganización

### ✅ **Beneficios Logrados**
1. **Separación clara** entre código de producción y desarrollo
2. **Tests organizados** por categorías y funcionalidad
3. **Estructura escalable** para futuras funcionalidades
4. **Fácil mantenimiento** y navegación del código
5. **Deploy limpio** excluyendo archivos de desarrollo

### 🛡️ **Archivos de Producción Core**
Estos son los archivos esenciales para el funcionamiento del antivirus:
- Motor antivirus (`core/`)
- Plugins de detección (`plugins/`)
- Interfaz de usuario (`frontend/`)
- Configuraciones (`config/`)
- Modelos ML (`models/`)

### 🔧 **Archivos de Desarrollo**
Archivos que solo necesitan los desarrolladores:
- Scripts de debug (`dev/debug_scripts/`)
- Demos y prototipos (`dev/demos/`)
- Reportes de análisis (`dev/reports/`)
- Tests exhaustivos (`tests/`)

## 🚀 Comandos de Ejecución

### **Ejecutar Sistema Principal**
```bash
# Interfaz gráfica completa (RECOMENDADO)
python frontend/main.py

# Launcher con verificaciones adicionales
python production_launcher.py
```

### **Desarrollo y Testing**
```bash
# Ejecutar todos los tests TDD
python dev/reports/run_all_tdd_tests.py

# Demo completo
python dev/demos/demo_completo.py

# Scripts de debug específicos
python dev/debug_scripts/debug_memory.py
```

## 📦 Deploy y Distribución

Para crear un paquete de producción, incluir solo:
- Directorios: `core/`, `plugins/`, `frontend/`, `config/`, `utils/`, `models/`, `threat_intel/`
- Archivos: `production_launcher.py`, `install_dependencies.py`, `register_plugins.py`, `requirements.txt`
- Documentación: `README.md`, `docs/`

**Excluir en producción**: `dev/`, `tests/`, archivos `debug_*`, `demo_*`, `*_backup.py`