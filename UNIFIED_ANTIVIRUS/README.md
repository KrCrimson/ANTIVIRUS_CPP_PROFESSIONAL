# 🛡️ Sistema Anti-Keylogger Unificado - ÍNDICE CENTRAL DE DOCUMENTACIÓN

## 📚 Navegador de Documentación

Bienvenido al índice central de documentación del Sistema Anti-Keylogger Unificado. Desde aquí puedes acceder a toda la documentación organizada por categorías.

---

## 🎯 Descripción General

Sistema avanzado de detección y prevención de keyloggers desarrollado en Python. Implementa múltiples capas de detección utilizando análisis de comportamiento, machine learning, monitoreo de red y análisis heurístico para identificar y neutralizar amenazas de captura de teclado en tiempo real.

Este sistema antivirus modular utiliza una arquitectura basada en plugins con patrones de diseño de software avanzados (Facade, Observer, Strategy, Template Method, Factory) para proporcionar protección integral contra keyloggers y spyware.

---

## 📖 DOCUMENTACIÓN PRINCIPAL

### 🏠 **Documentación General**
- 📋 **[README Principal](./README.md)** - Este archivo (descripción general del proyecto)
- 🔧 **[Documentación Técnica](./doc/COMO_FUNCIONA_TECHNICAL_README.md)** - Funcionamiento interno y arquitectura detallada
- 📊 **[Resumen de Mejoras TDD](./TDD_ENHANCEMENT_SUMMARY.md)** - Mejoras implementadas con desarrollo guiado por pruebas

### 🛠️ **Configuración y Setup**
- ⚙️ **[Configuración General](./config/README.md)** - Configuración del sistema
- 📖 **[Guía de Usuario - Configuración](./config/GUIA_USUARIO_CONFIGURACION.md)** - Guía completa para configurar el sistema
- 📝 **[Configuración Avanzada](./config/README_CONFIGURACION.md)** - Configuraciones avanzadas y personalizaciones

### 🧪 **Testing y Calidad**
- 🔬 **[Tests Generales](./tests/README.md)** - Documentación del sistema de pruebas
- 📐 **[Guía de Implementación TDD](./tests/GUIA_IMPLEMENTACION_TDD.md)** - Metodología de desarrollo guiado por pruebas
- 🎯 **[Test: API Hooking Detection](./tests/tdd_01_api_hooking_detection/README.md)** - Pruebas de detección de hooks de API
- 🌐 **[Test: Port Detection](./tests/tdd_02_port_detection/README.md)** - Pruebas de detección de puertos
- 🔐 **[Test: Safe Process Validation](./tests/tdd_03_safe_process_validation/README.md)** - Validación de procesos seguros

---

## 🏗️ ARQUITECTURA Y COMPONENTES

### 🎯 **Core del Sistema**
- 🚀 **[Core Engine](./core/README.md)** - Motor principal y arquitectura central

### 🔌 **Sistema de Plugins**
- 🔍 **[Plugins - Detectores](./plugins/detectors/README.md)** - Módulos de detección de amenazas
- 📡 **[Plugins - Monitores](./plugins/monitors/README.md)** - Módulos de monitoreo del sistema
- ⚡ **[Plugins - Manejadores](./plugins/handlers/README.md)** - Manejadores de eventos y respuestas

### 🕵️ **Detectores Especializados**
- 🎹 **[Keylogger Detector](./plugins/detectors/keylogger_detector/README.md)** - Detección especializada de keyloggers
- 🧠 **[ML Detector](./plugins/detectors/ml_detector/README.md)** - Detección basada en Machine Learning
- 🌐 **[Network Detector](./plugins/detectors/network_detector/README.md)** - Análisis de tráfico de red
- 👁️ **[Behavior Detector](./plugins/detectors/behavior_detector/README.md)** - Análisis de comportamiento de procesos

### 🛠️ **Utilidades y Herramientas**
- 🔧 **[Utilities](./utils/README.md)** - Herramientas y utilidades del sistema
- 🤖 **[Models](./models/README.md)** - Modelos de Machine Learning y datos

---

## 📂 DIRECTORIOS Y RECURSOS

### 📚 **Recursos Adicionales**
- 📑 **[Directorio XD](./xd/README.md)** - Recursos y documentación adicional
- 📝 **[MDSD](./mdsd/README.md)** - Documentación de desarrollo dirigido por modelos

---

## 🚀 INICIO RÁPIDO

### 📋 **Para Desarrolladores**
1. **[Configuración Inicial](./config/GUIA_USUARIO_CONFIGURACION.md)** - Configurar el entorno
2. **[Guía TDD](./tests/GUIA_IMPLEMENTACION_TDD.md)** - Metodología de desarrollo
3. **[Documentación Técnica](./doc/COMO_FUNCIONA_TECHNICAL_README.md)** - Entender la arquitectura

### 🏃 **Para Usuarios**
1. **[README Principal](./README.md)** - Descripción general
2. **[Guía de Configuración](./config/GUIA_USUARIO_CONFIGURACION.md)** - Configurar el antivirus
3. **[Configuración del Sistema](./config/README.md)** - Ajustes básicos

---

## 📊 MAPA DE NAVEGACIÓN RÁPIDA

| 🎯 **¿Qué buscas?** | 📖 **Ve a este documento** |
|---------------------|----------------------------|
| Entender cómo funciona | [Documentación Técnica](./doc/COMO_FUNCIONA_TECHNICAL_README.md) |
| Configurar el sistema | [Guía de Usuario](./config/GUIA_USUARIO_CONFIGURACION.md) |
| Ejecutar pruebas | [Tests README](./tests/README.md) |
| Desarrollar plugins | [Core README](./core/README.md) |
| Detectores disponibles | [Detectores README](./plugins/detectors/README.md) |
| Machine Learning | [ML Detector](./plugins/detectors/ml_detector/README.md) |
| Arquitectura técnica | [Core Engine](./core/README.md) |
| Utilidades del sistema | [Utils README](./utils/README.md) |

---

## 🌐 SISTEMA DE MONITOREO WEB

### 📊 **Monitoreo Centralizado**
- 🖥️ **[Web Monitor Server](./web_monitor_server.py)** - Servidor web FastAPI para centralizar logs
- 📊 **[Dashboard Web](./web_templates/dashboard.html)** - Interface web para visualizar métricas
- 🔐 **[Sistema de Seguridad Web](./web_security.py)** - Autenticación y seguridad del dashboard
- 📡 **[Cliente de Logs](./utils/log_sender.py)** - Cliente para envío automático de logs
- ⚙️ **[Configuración Web](./client_monitor_config.json)** - Configuración del sistema web

### 🛠️ **Documentación de Integración Web**
- 📋 **Integración Completa** - Sistema totalmente integrado con el antivirus principal
- 🚀 **Servidor HTTP Simple** - Versión simplificada para pruebas (`simple_http_server.py`)
- 🧪 **Scripts de Prueba** - Herramientas de testing para el sistema web

---

## 📁 DOCUMENTACIÓN ADICIONAL

### 🔧 **Desarrollo y Arquitectura**
- 📐 **[Integración de Keyloggers](./doc/KEYLOGGER_INTEGRATION_SUMMARY.md)** - Resumen de integración de detectores
- 🔄 **[Análisis de Refactoring](./refactor_report.py)** - Reportes de mejoras del código
- 📊 **[Reportes TDD](./tdd_report.py)** - Reportes de desarrollo guiado por pruebas
- 🎯 **[Integración de Producción](./test_production_integration.py)** - Tests de integración completa

### 📋 **Scripts y Herramientas**
- 🚀 **[Launcher Principal](./launcher.py)** - Lanzador del sistema backend
- 🎨 **[UI Profesional](./professional_ui_robust.py)** - Interfaz gráfica principal
- 🔧 **[Backend Simple](./simple_backend.py)** - Ejecutor directo del backend
- 📦 **[Registro de Plugins](./register_plugins.py)** - Auto-registro del sistema de plugins
- 🛠️ **[Instalador de Dependencias](./install_dependencies.py)** - Setup automático

### 📊 **Análisis y Diagramas**
- 📈 **[Análisis Backend](./backend_analysis.py)** - Análisis del rendimiento backend
- 🔍 **[Verificador de Dependencias](./check_dependencies.py)** - Validación del entorno
- 📋 **[Reporte TDD Completo](./full_tdd_report.py)** - Análisis completo de pruebas
- 🔄 **[Ejecutor de Tests](./run_all_tdd_tests.py)** - Ejecutor automático de todas las pruebas

---

## 🗺️ DIAGRAMAS Y RECURSOS VISUALES

### 📊 **Diagramas de Flujo**
- 🔄 **[Flujo de Secuencia](./sequence_flow.puml)** - Diagrama PlantUML del flujo de datos
- 🎯 **[Flujo Simple](./simple_flow.puml)** - Diagrama simplificado del sistema

### 📁 **Recursos y Assets**
- 🌐 **[Web Static](./web_static/)** - Recursos estáticos para el dashboard web
- 🗃️ **[Threat Intel](./threat_intel/)** - Base de datos de inteligencia de amenazas
- 📊 **[Logs del Sistema](./logs/)** - Directorio de logs y registros

---

## 🎯 Características Principales

- **Detección Multi-Capa**: Combina análisis de comportamiento, ML y monitoreo de red
- **Arquitectura Modular**: Sistema de plugins extensible y escalable
- **Machine Learning**: Modelos ONNX entrenados para detección de keyloggers
- **Monitoreo en Tiempo Real**: Vigilancia continua de procesos, archivos y red
- **Interfaz Gráfica Avanzada**: UI profesional con Dear PyGui para gestión visual moderna
- **Sistema de Cuarentena**: Aislamiento seguro de archivos maliciosos
- **Gestión de Alertas**: Sistema completo de notificaciones y logging
- **Event Bus**: Comunicación desacoplada entre componentes
- **Integration Engine**: Plugin avanzado que integra TDD, IAST y MDSD
- **Logs Individuales**: Cada plugin genera su propio archivo de log independiente
- **TDD Integration**: Test-Driven Development integrado con ejecución automática de tests
- **IAST Security**: Interactive Application Security Testing en tiempo real
- **MDSD Generation**: Model-Driven Software Development con generación automática de código

## 📁 Estructura del Proyecto

```
UNIFIED_ANTIVIRUS/
│
├── launcher.py                      # Punto de entrada principal (backend only)
├── production_launcher.py           # Launcher de producción con Dear PyGui
├── professional_ui_robust.py        # Interfaz gráfica profesional con tkinter (legacy)
├── simple_backend.py                # Ejecutor directo del backend original
├── register_plugins.py              # Sistema de auto-registro de plugins
├── install_dependencies.py          # Instalador de dependencias Python
├── monitor_all_logs.py              # Monitor en tiempo real de todos los logs
├── trigger_detection.py             # Disparador manual de detecciones para pruebas
│
├── core/                            # Núcleo del sistema
│   ├── __init__.py
│   ├── engine.py                    # Motor principal (Facade Pattern)
│   ├── plugin_manager.py            # Gestor de plugins (Factory Pattern)
│   ├── event_bus.py                 # Sistema de eventos (Observer Pattern)
│   ├── base_plugin.py               # Clase base para plugins (Template Method)
│   ├── interfaces.py                # Interfaces de plugins
│   └── plugin_registry.py           # Registro centralizado de plugins
│
├── plugins/                         # Sistema de plugins modular
│   ├── detectors/                   # Plugins de detección
│   │   ├── behavior_detector/       # Detección por comportamiento
│   │   ├── integration_engine/      # Plugin de integración TDD/IAST/MDSD
│   │   ├── keylogger_detector/      # Detector especializado de keyloggers
│   │   ├── ml_detector/             # Detección con Machine Learning
│   │   └── network_detector/        # Análisis de tráfico de red
│   │
│   ├── monitors/                    # Plugins de monitoreo
│   │   ├── file_monitor/            # Monitoreo del sistema de archivos
│   │   ├── network_monitor/         # Monitoreo de conexiones de red
│   │   └── process_monitor/         # Monitoreo de procesos
│   │
│   └── handlers/                    # Plugins de manejo de eventos
│       ├── alert_manager/           # Gestor de alertas
│       ├── logger_handler/          # Handler de logging estructurado
│       └── quarantine_handler/      # Gestor de cuarentena
│
├── config/                          # Archivos de configuración
│   ├── unified_config.toml          # Configuración principal del sistema
│   ├── alerts_config.json           # Configuración de alertas
│   ├── ml_config.json               # Configuración de modelos ML
│   ├── plugins_config.json          # Configuración de plugins
│   ├── security_config.json         # Configuración de seguridad
│   ├── whitelist.json               # Lista blanca de procesos
│   └── safe_profiles.json           # Perfiles de comportamiento seguro
│
├── models/                          # Modelos de Machine Learning
│   ├── keylogger_model_large_*.onnx # Modelo ONNX principal
│   ├── modelo_keylogger_*.onnx      # Modelo alternativo
│   ├── label_classes.json           # Clases de etiquetas
│   └── onnx_metadata_*.json         # Metadatos de modelos
│
├── utils/                           # Utilidades del sistema
│   ├── logger.py                    # Sistema de logging avanzado
│   ├── security_utils.py            # Utilidades de seguridad
│   ├── system_utils.py              # Utilidades del sistema
│   └── file_utils.py                # Utilidades de archivos
│
├── logs/                            # Directorio de logs individuales
│   ├── antivirus.log                # Log principal del sistema
│   ├── frontend.log                 # Log de la interfaz Dear PyGui
│   ├── behavior_detector.log        # Log del detector de comportamiento
│   ├── keylogger_detector.log       # Log del detector de keyloggers
│   ├── ml_detector.log              # Log del detector ML
│   ├── network_detector.log         # Log del detector de red
│   ├── integration_engine.log       # Log del motor de integración
│   ├── tdd_integration.log          # Log de TDD (Test-Driven Development)
│   ├── iast_security.log            # Log de IAST (Interactive Security Testing)
│   └── mdsd_generator.log           # Log de MDSD (Model-Driven Development)
├── threat_intel/                    # Inteligencia de amenazas
│   ├── malicious_ips.txt            # IPs maliciosas conocidas
│   └── domains.txt                  # Dominios sospechosos
├── tests/                           # Suite de tests TDD
│   ├── tdd_01_api_hooking_detection/# Tests de detección de API hooking
│   └── tdd_02_port_detection/       # Tests de detección de puertos
│
└── doc/                             # Documentación
    └── articulo_keylogger_antivirus.tex
```

## 🏗️ Arquitectura del Sistema

### Patrones de Diseño Implementados

1. **Facade Pattern** (`engine.py`): Simplifica la interfaz compleja del sistema
2. **Observer Pattern** (`event_bus.py`): Comunicación desacoplada entre componentes
3. **Factory Pattern** (`plugin_manager.py`): Creación dinámica de plugins
4. **Template Method** (`base_plugin.py`): Ciclo de vida común para plugins
5. **Strategy Pattern** (detectores): Diferentes estrategias de detección

### Flujo de Funcionamiento

```
1. Launcher inicia el UnifiedAntivirusEngine
2. Engine descubre y carga plugins automáticamente
3. Plugins se suscriben al Event Bus
4. Monitores capturan eventos del sistema
5. Detectores analizan los eventos
6. Handlers gestionan alertas y acciones
7. UI refleja el estado en tiempo real
```

## 🚀 Uso del Sistema

### Instalación de Dependencias

```bash
# Opción 1: Script automático
python install_dependencies.py

# Opción 2: Manual
pip install -r xd/requirements.txt
```

### Ejecución del Sistema

#### Modo Backend (Sin UI)

```bash
# Iniciar con todos los plugins
python launcher.py

# Solo detectores
python launcher.py --detectors-only

# Categorías específicas
python launcher.py --categories detectors monitors

# Modo debug
python launcher.py --debug
```

#### Modo Producción (Dear PyGui - Recomendado)

```bash
# Interfaz gráfica moderna con Dear PyGui
python production_launcher.py
```

#### Modo UI Legacy (Interfaz Tkinter)

```bash
# Interfaz gráfica profesional con tkinter (versión legacy)
python professional_ui_robust.py
```

#### Monitoreo de Logs en Tiempo Real

```bash
# Monitor de todos los logs del sistema simultáneamente
python monitor_all_logs.py
```

### Configuración

Editar `config/unified_config.toml` para ajustar:
- Umbrales de detección
- Plugins habilitados
- Configuración de ML
- Niveles de logging
- Comportamiento del sistema

## 📋 Archivos Principales

### `launcher.py`
**Propósito**: Punto de entrada principal del sistema (backend sin UI)

**Funcionalidad**:
- Parsea argumentos de línea de comandos
- Inicializa el UnifiedAntivirusEngine
- Gestiona el ciclo de vida del sistema
- Maneja señales de sistema (CTRL+C)
- Mantiene el sistema ejecutándose

**Descripción Técnica**:
Implementa el patrón de entrada única para el sistema. Utiliza `argparse` para configuración flexible por línea de comandos. Inicia el motor principal y mantiene el programa en ejecución hasta recibir señal de terminación.

### `production_launcher.py`
**Propósito**: Launcher de producción con interfaz Dear PyGui moderna

**Funcionalidad**:
- Interfaz gráfica moderna con Dear PyGui 2.1.0
- Dashboard con métricas en tiempo real
- Visualización de amenazas detectadas
- Sistema de logs estructurado con colores
- Control de protección (iniciar/detener)
- Integración completa con todos los plugins

**Descripción Técnica**:
Aplicación Dear PyGui con arquitectura robusta. Utiliza threading para comunicación asíncrona con el motor antivirus. Implementa sistema de actualización en tiempo real sin bloqueos. Interfaz moderna y responsiva optimizada para producción.

### `professional_ui_robust.py`
**Propósito**: Interfaz gráfica profesional legacy con tkinter

**Funcionalidad**:
- Dashboard con métricas en tiempo real
- Visualización de amenazas detectadas
- Panel de configuración de plugins
- Sistema de logs estructurado
- Gráficas de rendimiento del sistema
- Control de protección (iniciar/detener)

**Descripción Técnica**:
Aplicación tkinter robusta con arquitectura MVC. Utiliza threading para actualización asíncrona de UI sin bloqueos. Implementa sistema de colas (`queue.Queue`) para comunicación thread-safe con el motor. Optimizada para manejar grandes volúmenes de datos sin degradación de rendimiento.

**Características técnicas**:
- Sistema de agregación de amenazas para evitar spam
- Buffer circular (deque) para logs con límite de memoria
- Actualización incremental de UI (cada 5 segundos)
- Caché de amenazas para rendimiento
- Manejo robusto de errores y excepciones

### `monitor_all_logs.py`
**Propósito**: Monitor en tiempo real de todos los logs del sistema

**Funcionalidad**:
- Monitoreo simultáneo de 10 archivos de log
- Códigos de color para diferentes tipos de eventos
- Detección automática de nuevos archivos de log
- Visualización en tiempo real de actividad del sistema
- Filtrado por tipo de plugin y severidad

**Descripción Técnica**:
Sistema de monitoreo multi-archivo que utiliza threading para seguimiento simultáneo de logs. Implementa códigos de color específicos para cada tipo de plugin (TDD, IAST, MDSD, detectores). Optimizado para manejar grandes volúmenes de logs sin degradación de rendimiento.

### `register_plugins.py`
**Propósito**: Sistema de auto-registro de plugins

**Funcionalidad**:
- Descubre plugins automáticamente
- Registra plugins en el PluginRegistry
- Valida configuraciones de plugins
- Maneja errores de importación gracefully

**Descripción Técnica**:
Utiliza introspección de Python para descubrir clases de plugins. Implementa patrón Registry centralizado. Proporciona capa de abstracción para registro dinámico sin modificar código del motor.

### `simple_backend.py`
**Propósito**: Ejecutor directo del backend original (ANTIVIRUS_PRODUCTION)

**Funcionalidad**:
- Ejecuta el sistema antivirus legacy
- Proporciona compatibilidad hacia atrás
- Gestiona cambio de directorio y ejecución

**Descripción Técnica**:
Script de compatibilidad que ejecuta `antivirus_launcher.py` del sistema ANTIVIRUS_PRODUCTION usando subprocess. Cambia el working directory temporalmente para ejecución correcta.

### `install_dependencies.py`
**Propósito**: Instalador automático de dependencias

**Funcionalidad**:
- Verifica Python instalado
- Instala pip si no existe
- Instala todas las dependencias necesarias
- Valida instalación correcta

**Descripción Técnica**:
Script de bootstrapping que utiliza subprocess para ejecutar pip. Maneja diferentes sistemas operativos y configuraciones de Python. Proporciona feedback detallado del proceso de instalación.

## 🚀 Integration Engine Plugin

### Características del Integration Engine

El **Integration Engine** es un plugin avanzado que integra metodologías modernas de desarrollo:

#### 🧪 **TDD Integration (Test-Driven Development)**
- **Ejecución automática**: Tests cada 60 segundos
- **Suite de tests**: Incluye `tdd_01_api_hooking_detection` y `tdd_02_port_detection`
- **Logging individual**: `logs/tdd_integration.log`
- **Framework**: Utiliza pytest para ejecución de tests
- **Validación**: Verifica la integridad de los detectores en tiempo real

#### 🛡️ **IAST Integration (Interactive Application Security Testing)**
- **Análisis continuo**: Escaneos de seguridad cada 45 segundos
- **Detección de vulnerabilidades**: SQL Injection, XSS, y otros patrones
- **Logging individual**: `logs/iast_security.log`
- **Resultados reales**: Sin datos ficticios, análisis auténtico
- **Integración**: Se ejecuta junto con el sistema antivirus principal

#### 🏗️ **MDSD Integration (Model-Driven Software Development)**
- **Generación automática**: Templates cada 120 segundos
- **Templates incluidos**: Ransomware Detector, Trojan Detector, Rootkit Detector, Spyware Detector
- **Logging individual**: `logs/mdsd_generator.log`
- **Workflow Engine**: Sistema de generación de código automático
- **Validación**: Verificación de templates generados

### Arquitectura del Integration Engine

```python
IntegrationEnginePlugin
├── TDD Worker (Thread)     # Ejecuta tests automáticamente
├── IAST Worker (Thread)    # Análisis de seguridad continuo  
├── MDSD Worker (Thread)    # Generación de código automática
└── Main Controller         # Coordina todos los workers
```

### Logs Individuales Generados

El sistema genera **10 archivos de log independientes**:

1. **`antivirus.log`** - Log principal del sistema
2. **`frontend.log`** - Interfaz Dear PyGui
3. **`behavior_detector.log`** - Detector de comportamiento
4. **`keylogger_detector.log`** - Detector de keyloggers
5. **`ml_detector.log`** - Detector de Machine Learning
6. **`network_detector.log`** - Detector de red
7. **`integration_engine.log`** - Motor de integración principal
8. **`tdd_integration.log`** - Test-Driven Development
9. **`iast_security.log`** - Interactive Security Testing
10. **`mdsd_generator.log`** - Model-Driven Development

### Ejemplo de Salida de Logs

```bash
# TDD Integration Log
2025-11-12 15:17:04,162 - tdd_integration - INFO - ✅ Tests en tests/tdd_01_api_hooking_detection: PASSED
2025-11-12 15:17:37,116 - tdd_integration - INFO - ✅ Ciclo TDD completado

# IAST Security Log  
2025-11-12 15:17:36,911 - iast_security - INFO - ✅ Análisis IAST: Sin vulnerabilidades críticas
2025-11-12 15:17:37,039 - iast_security - INFO - 📊 ===== 16 passed in 10.98s =====

# MDSD Generator Log
2025-11-12 15:17:04,299 - mdsd_generator - INFO - 📝 Generando template: Ransomware Detector
2025-11-12 15:17:40,004 - mdsd_generator - INFO - ✅ Ciclo MDSD completado
```

## 🔧 Dependencias Principales

- **dearpygui**: Interfaz gráfica moderna (v2.1.0)
- **psutil**: Monitoreo de procesos y sistema
- **onnxruntime**: Ejecución de modelos ML
- **watchdog**: Monitoreo de archivos
- **pywin32**: APIs de Windows
- **pytest**: Framework de testing para TDD
- **tkinter**: Interfaz gráfica legacy (incluido en Python)
- **toml**: Parseo de configuración
- **numpy**: Operaciones numéricas para ML
- **threading**: Concurrencia para Integration Engine

## 📊 Métricas y Monitoreo

El sistema recopila métricas en tiempo real:
- **Amenazas detectadas**: Totales y únicas identificadas
- **Plugins activos**: Estado de los 8 plugins del sistema
- **Uso de recursos**: CPU, RAM y rendimiento del sistema
- **Tiempo de actividad**: Uptime del sistema antivirus
- **Escaneos completados**: Contadores de análisis realizados
- **TDD Metrics**: Tests ejecutados, passed/failed, cobertura
- **IAST Metrics**: Vulnerabilidades encontradas, tipos de ataques detectados
- **MDSD Metrics**: Templates generados, líneas de código creadas
- **Logs en tiempo real**: Monitoreo de 10 streams de log simultáneos

### Sistema de Monitoreo Avanzado

```bash
# Monitoreo en tiempo real de todos los logs
python monitor_all_logs.py

# Vista de logs específicos por color:
# 🟢 Verde: TDD Integration
# 🔵 Azul: IAST Security  
# 🟡 Amarillo: MDSD Generator
# 🔴 Rojo: Detectores de amenazas
# ⚪ Blanco: Sistema general
```

## 🔐 Seguridad

### Características de Seguridad

- **Whitelisting**: Lista blanca de procesos seguros
- **Cuarentena**: Aislamiento seguro de archivos maliciosos
- **Logging estructurado**: Auditoría completa de eventos
- **Validación de entrada**: Sanitización de datos
- **Cifrado**: Soporte para cifrado de archivos en cuarentena

### Análisis de Amenazas

El sistema detecta:
- Keyloggers basados en hooks de Windows
- Captura de pantalla sospechosa
- Inyección de código
- Conexiones de red maliciosas
- Patrones de archivos de log
- Comportamiento stealth
- APIs sospechosas de Windows

## 🧪 Sistema de Testing Integrado

### TDD Integration (Test-Driven Development)

El sistema incluye **TDD automático** que se ejecuta cada 60 segundos:

**Tests Incluidos:**
- `tests/tdd_01_api_hooking_detection/`: Detección de API hooking
- `tests/tdd_02_port_detection/`: Detección de puertos sospechosos

**Ejecución Automática:**
```bash
# TDD se ejecuta automáticamente con el Integration Engine
python production_launcher.py

# Ver logs de TDD en tiempo real
tail -f logs/tdd_integration.log
```

**Ejecución Manual:**
```bash
# Tests individuales de plugins
python -m pytest plugins/*/test_*.py

# Tests específicos de TDD
python -m pytest tests/tdd_01_api_hooking_detection/
python -m pytest tests/tdd_02_port_detection/

# Ejecutar trigger manual de detecciones
python trigger_detection.py
```

### IAST Integration (Interactive Application Security Testing)

**Tests de Seguridad Automáticos:**
- Análisis de vulnerabilidades SQL Injection
- Detección de XSS (Cross-Site Scripting)
- Evaluación de seguridad de APIs
- Tests de penetración básicos

**Resultados en Tiempo Real:**
```bash
# Ver análisis IAST en vivo
tail -f logs/iast_security.log

# Ejemplo de salida:
# ✅ Análisis IAST: Sin vulnerabilidades críticas
# 📊 ===== 16 passed in 10.98s =====
```

## 📝 Sistema de Logging Avanzado

### Niveles de Logging
- **DEBUG**: Información detallada de desarrollo
- **INFO**: Eventos normales del sistema  
- **WARNING**: Eventos sospechosos
- **ERROR**: Errores recuperables
- **CRITICAL**: Errores críticos

### Archivos de Log Individuales

**Logs del Sistema Principal:**
- `antivirus.log`: Log principal del motor antivirus
- `frontend.log`: Interfaz Dear PyGui y eventos de UI

**Logs de Detectores:**
- `behavior_detector.log`: Análisis de comportamiento de procesos
- `keylogger_detector.log`: Detección específica de keyloggers
- `ml_detector.log`: Machine Learning y modelos ONNX
- `network_detector.log`: Análisis de tráfico de red

**Logs de Integration Engine:**
- `integration_engine.log`: Controlador principal de integraciones
- `tdd_integration.log`: Test-Driven Development (tests automáticos)
- `iast_security.log`: Interactive Application Security Testing
- `mdsd_generator.log`: Model-Driven Software Development

### Características del Sistema de Logs

- **UTF-8 Encoding**: Soporte completo para caracteres especiales y emojis
- **Rotación automática**: Prevención de archivos de log excesivamente grandes
- **Threading seguro**: Logging concurrente sin bloqueos
- **Filtrado por severidad**: Configuración independiente por plugin
- **Monitoreo en tiempo real**: `monitor_all_logs.py` para visualización simultánea

## 🤝 Contribución

Este es un proyecto académico del curso de Sistemas Comportamentales.

## 📄 Licencia

Proyecto académico - Universidad Privada de Tacna

---

## ⚙️ ARCHIVOS DE CONFIGURACIÓN IMPORTANTES

### 📋 **Configuración del Sistema**
- 📝 **[requirements.txt](./requirements.txt)** - Dependencias de Python requeridas
- 🔧 **[pytest.ini](./pytest.ini)** - Configuración de pruebas con pytest
- 📊 **[.flake8](./.flake8)** - Configuración de linting y estilo de código

### 🏗️ **Archivos de Build y Deploy**
- 🚀 **[Make.ps1](./Make.ps1)** - Script de construcción para PowerShell
- 📦 **[professional_ui_robust.spec](./professional_ui_robust.spec)** - Configuración de PyInstaller
- 🛠️ **[installer_script.iss](./installer_script.iss)** - Script de instalador con Inno Setup

---

## 🔗 ENLACES RÁPIDOS DE CONFIGURACIÓN

| 📋 **Tipo de Configuración** | 📄 **Archivo** | 📝 **Descripción** |
|------------------------------|---------------|-------------------|
| **Sistema Principal** | [unified_config.toml](./config/unified_config.toml) | Configuración central |
| **Alertas** | [alerts_config.json](./config/alerts_config.json) | Configuración de alertas |
| **Machine Learning** | [ml_config.json](./config/ml_config.json) | Configuración ML |
| **Plugins** | [plugins_config.json](./config/plugins_config.json) | Configuración de plugins |
| **Seguridad** | [security_config.json](./config/security_config.json) | Configuración de seguridad |
| **Logging** | [logging_config.json](./config/logging_config.json) | Configuración de logs |
| **UI** | [ui_config.json](./config/ui_config.json) | Configuración de interfaz |
| **Lista Blanca** | [whitelist.json](./config/whitelist.json) | Procesos permitidos |
| **Monitoreo Web** | [client_monitor_config.json](./client_monitor_config.json) | Config web monitoring |

---

## 🛠️ HERRAMIENTAS Y UTILIDADES ADICIONALES

### 🧪 **Testing y Validación**
- 🔬 **[Validador de Configuración](./config/config_validator.py)** - Validar archivos de configuración
- 📊 **[Test de Integración](./test_production_integration.py)** - Pruebas de integración completa
- 🎯 **[Ejecutor de Tests TDD](./run_all_tdd_tests.py)** - Ejecutar todas las pruebas

### 📊 **Análisis y Reportes**
- 📈 **[Reporte TDD Completo](./full_tdd_report.py)** - Análisis completo de cobertura de pruebas
- � **[Análisis de Refactoring](./refactor_report.py)** - Reportes de mejoras de código
- 📋 **[Análisis de Backend](./backend_analysis.py)** - Performance y análisis del backend

### 🌐 **Sistema de Monitoreo Web**
- 🖥️ **[Servidor Web FastAPI](./web_monitor_server.py)** - Servidor de monitoreo centralizado
- 🏠 **[Servidor HTTP Simple](./simple_http_server.py)** - Versión simplificada para testing
- 📊 **[Dashboard Templates](./web_templates/)** - Templates del dashboard web
- 🔐 **[Sistema de Seguridad Web](./web_security.py)** - Autenticación y seguridad
- 📡 **[Cliente de Logs](./utils/log_sender.py)** - Envío automático de logs al servidor

---

## 🎯 GUÍAS DE INICIO RÁPIDO POR PERFIL

### 👨‍💻 **Para Desarrolladores**
1. **[Guía TDD](./tests/GUIA_IMPLEMENTACION_TDD.md)** - Metodología de desarrollo
2. **[Documentación del Core](./core/README.md)** - Entender la arquitectura
3. **[Desarrollo de Plugins](./plugins/README.md)** - Crear nuevos plugins
4. **[API del Sistema](./doc/COMO_FUNCIONA_TECHNICAL_README.md)** - Documentación técnica

### 🔧 **Para Administradores**
1. **[Guía de Configuración](./config/GUIA_USUARIO_CONFIGURACION.md)** - Configuración completa
2. **[Configuración de Seguridad](./config/README_CONFIGURACION.md)** - Configuraciones avanzadas
3. **[Monitoreo Web](./web_monitor_server.py)** - Setup del dashboard centralizado
4. **[Logs del Sistema](./utils/README.md)** - Gestión de logs y monitoreo

### 🧪 **Para Testing/QA**
1. **[Tests Generales](./tests/README.md)** - Ejecutar pruebas
2. **[Metodología TDD](./tests/GUIA_IMPLEMENTACION_TDD.md)** - Entender las pruebas
3. **[Tests Específicos](./tests/)** - Casos de prueba por componente
4. **[Validación de Producción](./test_production_integration.py)** - Tests de integración

### 📊 **Para Análisis y Monitoreo**
1. **[Dashboard Web](./web_templates/dashboard.html)** - Interface de monitoreo
2. **[Análisis ML](./models/README.md)** - Modelos y detección avanzada
3. **[Threat Intelligence](./threat_intel/)** - Base de datos de amenazas
4. **[Logs Estructurados](./logs/)** - Análisis de logs del sistema

---

## �👥 Autores

Estudiantes del curso de Sistemas Comportamentales - UPT

## 🎉 Características Avanzadas Recientes

### ✅ **Sistema Completo de Logs Individuales**
- **10 archivos de log** independientes por plugin
- **Monitoreo en tiempo real** de todos los streams
- **Códigos de color** para identificación rápida
- **UTF-8 encoding** para caracteres especiales

### ✅ **Integration Engine Plugin**
- **TDD automático** cada 60 segundos
- **IAST security testing** cada 45 segundos  
- **MDSD code generation** cada 120 segundos
- **Threading concurrente** para máximo rendimiento

### ✅ **Interfaz Moderna Dear PyGui**
- **UI responsiva** y moderna
- **Métricas en tiempo real** actualizadas
- **Gestión completa** de plugins
- **Control total** del sistema

### ✅ **Detección Real de Amenazas**
- **Sin datos ficticios** - solo detecciones reales
- **Análisis de procesos** en tiempo real
- **Machine Learning** con modelos ONNX
- **Inteligencia de amenazas** actualizada

## 📈 Estadísticas del Sistema

```
📊 Plugins Totales: 8
📝 Archivos de Log: 10  
🧪 Tests Automáticos: TDD + IAST
🏗️ Generación de Código: MDSD
🛡️ Detección en Tiempo Real: ✅
🎨 Interfaz Moderna: Dear PyGui 2.1.0
```

<<<<<<< Updated upstream
---

<<<<<<< Updated upstream
## 📞 SOPORTE Y AYUDA

### 🆘 **¿Problemas?**
- 🔧 **Configuración**: Ver [Guía de Usuario](./config/GUIA_USUARIO_CONFIGURACION.md)
- 🐛 **Bugs**: Revisar [Tests](./tests/README.md) y ejecutar diagnósticos
- 🔍 **Detección**: Consultar [Detectores README](./plugins/detectors/README.md)
- 🌐 **Web Monitoring**: Verificar [configuración web](./client_monitor_config.json)

### 📚 **Documentación Clave**
- 📖 **Funcionamiento**: [Documentación Técnica](./doc/COMO_FUNCIONA_TECHNICAL_README.md)
- ⚙️ **Configuración**: [README de Config](./config/README.md)
- 🧪 **Testing**: [Guía TDD](./tests/GUIA_IMPLEMENTACION_TDD.md)
- 🏗️ **Arquitectura**: [Core README](./core/README.md)

---

**Nota**: Este sistema está diseñado para propósitos educativos y de investigación. Para uso en producción, se recomienda realizar auditorías de seguridad adicionales y pruebas exhaustivas.
=======
**Nota**: Este sistema está diseñado para propósitos educativos y de investigación en el curso de Sistemas Comportamentales. Implementa metodologías avanzadas de desarrollo (TDD, IAST, MDSD) integradas con detección de amenazas en tiempo real. Para uso en producción, se recomienda realizar auditorías de seguridad adicionales y pruebas exhaustivas.
>>>>>>> Stashed changes
=======
---

**Nota**: Este sistema está diseñado para propósitos educativos y de investigación en el curso de Sistemas Comportamentales. Implementa metodologías avanzadas de desarrollo (TDD, IAST, MDSD) integradas con detección de amenazas en tiempo real. Para uso en producción, se recomienda realizar auditorías de seguridad adicionales y pruebas exhaustivas.
>>>>>>> Stashed changes
