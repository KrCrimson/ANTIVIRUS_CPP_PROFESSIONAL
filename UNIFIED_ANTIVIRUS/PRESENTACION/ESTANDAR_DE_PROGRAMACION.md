# Estándar de Programación - UNIFIED ANTIVIRUS

> **Guía de Desarrollo y Mejores Prácticas**  
> Versión: 1.0  
> Fecha: Diciembre 2025  
> Sistema: Unified Shield Anti-Keylogger Professional

---

## 📋 Tabla de Contenidos

1. [Introducción](#introducción)
2. [Convenciones de Nomenclatura](#convenciones-de-nomenclatura)
3. [Organización del Código](#organización-del-código)
4. [Patrones de Diseño](#patrones-de-diseño)
5. [Manejo de Errores](#manejo-de-errores)
6. [Logging y Monitoreo](#logging-y-monitoreo)
7. [Documentación](#documentación)
8. [Testing](#testing)
9. [Seguridad](#seguridad)
10. [Control de Versiones](#control-de-versiones)
11. [Optimización y Rendimiento](#optimización-y-rendimiento)

---

## Introducción

Este documento establece los estándares de programación para el desarrollo del sistema UNIFIED ANTIVIRUS. Todos los desarrolladores deben seguir estas convenciones para mantener la consistencia, calidad y mantenibilidad del código.

### Objetivos

- ✅ **Consistencia**: Código uniforme y predecible
- ✅ **Mantenibilidad**: Fácil de entender y modificar
- ✅ **Escalabilidad**: Preparado para crecer
- ✅ **Calidad**: Menos errores, mejor rendimiento
- ✅ **Colaboración**: Facilitar el trabajo en equipo

### Lenguajes Principales

- **Python 3.8+**: Backend, core, plugins
- **JavaScript/TypeScript**: Frontend web
- **SQL**: Base de datos PostgreSQL
- **JSON/TOML**: Configuración

---

## Convenciones de Nomenclatura

### 1. Archivos y Directorios

#### Archivos Python

**Formato**: `snake_case.py`

```
✅ Correcto:
- behavior_detector.py
- ml_detector.py
- event_bus.py
- plugin_manager.py

❌ Incorrecto:
- BehaviorDetector.py
- MLDetector.py
- eventBus.py
- PluginManager.py
```

#### Directorios

**Formato**: `snake_case`

```
✅ Correcto:
- core/
- plugins/
- web_backend/
- threat_intel/

❌ Incorrecto:
- Core/
- Plugins/
- webBackend/
- ThreatIntel/
```

#### Archivos de Configuración

**Formato**: `snake_case_config.json` o `descriptive_name.toml`

```
✅ Correcto:
- plugins_config.json
- ml_config.json
- security_config.json
- unified_config.toml

❌ Incorrecto:
- PluginsConfig.json
- mlconfig.json
- SecurityCfg.json
```

---

### 2. Clases

**Formato**: `PascalCase`

```python
✅ Correcto:
class BehaviorDetector:
    pass

class MLDetectorPlugin:
    pass

class EventBus:
    pass

class ThreatInfo:
    pass

❌ Incorrecto:
class behavior_detector:
    pass

class mlDetectorPlugin:
    pass

class event_bus:
    pass
```

**Convenciones Especiales**:

- **Interfaces**: Sufijo `Interface`
  ```python
  class DetectorInterface(ABC):
      pass
  
  class MonitorInterface(ABC):
      pass
  ```

- **Clases Base**: Prefijo `Base`
  ```python
  class BasePlugin(ABC):
      pass
  ```

- **Excepciones**: Sufijo `Error` o `Exception`
  ```python
  class PluginLoadError(Exception):
      pass
  
  class ConfigurationException(Exception):
      pass
  ```

---

### 3. Funciones y Métodos

**Formato**: `snake_case`

```python
✅ Correcto:
def detect_threats(data):
    pass

def get_confidence_score():
    pass

def update_signatures():
    pass

def _internal_helper():  # Privado
    pass

❌ Incorrecto:
def DetectThreats(data):
    pass

def getConfidenceScore():
    pass

def UpdateSignatures():
    pass
```

**Convenciones Especiales**:

- **Métodos Privados**: Prefijo `_`
  ```python
  def _validate_config(self):
      pass
  
  def _process_internal_data(self):
      pass
  ```

- **Métodos Protegidos**: Prefijo `_`
  ```python
  def _init_components(self):
      pass
  ```

- **Métodos Especiales**: Doble guión bajo
  ```python
  def __init__(self):
      pass
  
  def __str__(self):
      pass
  ```

---

### 4. Variables

**Formato**: `snake_case`

```python
✅ Correcto:
threat_count = 0
process_list = []
confidence_threshold = 0.7
is_running = False

❌ Incorrecto:
ThreatCount = 0
processList = []
ConfidenceThreshold = 0.7
IsRunning = False
```

**Convenciones Especiales**:

- **Constantes**: `UPPER_SNAKE_CASE`
  ```python
  MAX_THREADS = 10
  DEFAULT_TIMEOUT = 30
  API_VERSION = "1.0"
  LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s"
  ```

- **Variables Privadas**: Prefijo `_`
  ```python
  _internal_state = {}
  _cache = []
  ```

- **Variables de Clase**: `snake_case`
  ```python
  class MyClass:
      class_variable = "value"
      _private_class_var = "private"
  ```

---

### 5. Constantes y Enumeraciones

#### Constantes

**Formato**: `UPPER_SNAKE_CASE`

```python
# Ubicación: Inicio del módulo o clase
MAX_RETRY_ATTEMPTS = 3
DEFAULT_SCAN_INTERVAL = 5
CRITICAL_CPU_THRESHOLD = 80
LOG_ROTATION_SIZE_MB = 10

# Constantes de configuración
CONFIG_DIR = Path("config")
PLUGINS_DIR = Path("plugins")
LOGS_DIR = Path("logs")
```

#### Enumeraciones

**Formato**: Clase `PascalCase`, valores `UPPER_CASE`

```python
from enum import Enum

class ThreatSeverity(Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"

class PluginState(Enum):
    INITIALIZED = "initialized"
    RUNNING = "running"
    STOPPED = "stopped"
    ERROR = "error"
```

---

## Organización del Código

### 1. Estructura de Directorios

```
UNIFIED_ANTIVIRUS/
├── core/                    # Núcleo del sistema
│   ├── __init__.py
│   ├── engine.py           # Motor principal
│   ├── event_bus.py        # Sistema de eventos
│   ├── plugin_manager.py   # Gestor de plugins
│   ├── plugin_registry.py  # Registro de plugins
│   ├── base_plugin.py      # Clase base de plugins
│   └── interfaces.py       # Interfaces comunes
│
├── plugins/                 # Plugins del sistema
│   ├── detectors/          # Detectores de amenazas
│   ├── monitors/           # Monitores del sistema
│   ├── handlers/           # Manejadores de eventos
│   └── interfaces/         # Interfaces de usuario
│
├── config/                  # Configuraciones
│   ├── plugins_config.json
│   ├── ml_config.json
│   ├── security_config.json
│   └── logging_config.json
│
├── models/                  # Modelos ML
│   └── modelo_keylogger_from_datos.onnx
│
├── utils/                   # Utilidades
│   ├── logger.py
│   ├── file_utils.py
│   ├── security_utils.py
│   └── system_utils.py
│
├── web_backend/            # Backend web
│   ├── api/
│   ├── database.py
│   └── main.py
│
├── frontend/               # Frontend (si aplica)
│
├── tests/                  # Tests
│   ├── unit/
│   ├── integration/
│   └── e2e/
│
├── logs/                   # Logs del sistema
├── docs/                   # Documentación
└── scripts/                # Scripts de utilidad
```

---

### 2. Estructura de Archivos Python

**Orden de Elementos**:

```python
#!/usr/bin/env python3
"""
Título del Módulo
=================

Descripción breve del propósito del módulo.
Puede incluir detalles de implementación importantes.
"""

# 1. Imports de biblioteca estándar
import os
import sys
import logging
from typing import Dict, List, Optional
from pathlib import Path

# 2. Imports de terceros
import psutil
import numpy as np

# 3. Imports locales
from core import BasePlugin
from core.interfaces import DetectorInterface
from utils.logger import setup_logger

# 4. Constantes del módulo
MAX_PROCESSES = 100
DEFAULT_THRESHOLD = 0.7
LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s"

# 5. Logger del módulo
logger = logging.getLogger(__name__)

# 6. Clases
class MyDetector(BasePlugin, DetectorInterface):
    """Docstring de la clase"""
    
    def __init__(self):
        """Constructor"""
        pass
    
    def method(self):
        """Método público"""
        pass
    
    def _private_method(self):
        """Método privado"""
        pass

# 7. Funciones del módulo
def utility_function():
    """Función de utilidad"""
    pass

# 8. Bloque principal
if __name__ == "__main__":
    # Código de prueba o ejecución
    pass
```

---

### 3. Organización de Plugins

Cada plugin debe seguir esta estructura:

```
plugins/
└── my_detector/
    ├── __init__.py          # Exporta la clase principal
    ├── plugin.json          # Metadatos del plugin
    ├── config.json          # Configuración por defecto
    ├── detector.py          # Implementación principal
    ├── utils.py             # Utilidades específicas
    ├── README.md            # Documentación
    └── tests/               # Tests del plugin
        └── test_detector.py
```

**Ejemplo de `__init__.py`**:

```python
"""
My Detector Plugin
==================

Descripción del plugin.
"""

from .detector import MyDetector

__version__ = "1.0.0"
__all__ = ["MyDetector"]
```

**Ejemplo de `plugin.json`**:

```json
{
  "name": "my_detector",
  "version": "1.0.0",
  "type": "detector",
  "description": "Descripción del plugin",
  "author": "Nombre del Autor",
  "dependencies": ["psutil", "numpy"],
  "interfaces": ["DetectorInterface"],
  "entry_point": "detector.MyDetector"
}
```

---

## Patrones de Diseño

El sistema utiliza varios patrones de diseño establecidos. Los desarrolladores deben seguir estos patrones al extender el sistema.

### 1. Template Method Pattern

**Uso**: Clase `BasePlugin`

**Propósito**: Define el ciclo de vida común de todos los plugins.

```python
class BasePlugin(ABC):
    """Template Method Pattern"""
    
    def activate(self) -> bool:
        """Método template - NO modificar"""
        self.setup_logging()      # Común
        self.load_config()        # Común
        
        if not self.initialize(): # Específico (abstract)
            return False
        
        if not self.start():      # Específico (abstract)
            return False
        
        return True
    
    @abstractmethod
    def initialize(self) -> bool:
        """Implementar en subclase"""
        pass
    
    @abstractmethod
    def start(self) -> bool:
        """Implementar en subclase"""
        pass
```

**Regla**: Al crear un plugin, heredar de `BasePlugin` e implementar los métodos abstractos.

---

### 2. Strategy Pattern

**Uso**: Interfaces de plugins (`DetectorInterface`, `MonitorInterface`, etc.)

**Propósito**: Permite intercambiar algoritmos de detección/monitoreo.

```python
class DetectorInterface(ABC):
    """Strategy Pattern"""
    
    @abstractmethod
    def detect_threats(self, data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Algoritmo de detección - implementar estrategia específica"""
        pass

# Diferentes estrategias
class MLDetector(DetectorInterface):
    def detect_threats(self, data):
        # Estrategia: Machine Learning
        return ml_based_detection(data)

class BehaviorDetector(DetectorInterface):
    def detect_threats(self, data):
        # Estrategia: Análisis de comportamiento
        return behavior_based_detection(data)
```

---

### 3. Observer Pattern

**Uso**: `EventBus`

**Propósito**: Comunicación desacoplada entre componentes.

```python
# Publisher
event_bus.publish(
    event_type="threat_detected",
    data=threat_info,
    source="ml_detector"
)

# Subscriber
def handle_threat(event: Event):
    print(f"Amenaza detectada: {event.data}")

event_bus.subscribe(
    event_type="threat_detected",
    callback=handle_threat,
    subscriber_name="threat_handler"
)
```

**Regla**: Usar Event Bus para comunicación entre plugins. No llamar directamente a otros plugins.

---

### 4. Registry Pattern

**Uso**: `PluginRegistry`

**Propósito**: Registro centralizado de plugins disponibles.

```python
# Registrar plugin
registry.register_plugin(
    plugin_type="detector",
    plugin_name="ml_detector",
    plugin_class=MLDetector
)

# Obtener plugin
detector = registry.get_plugin("detector", "ml_detector")
```

---

### 5. Singleton Pattern

**Uso**: `EventBus`, `PluginManager`

**Propósito**: Asegurar una única instancia global.

```python
# Implementación implícita
# core/event_bus.py
event_bus = EventBus()  # Instancia global

# Uso
from core.event_bus import event_bus
event_bus.publish(...)
```

**Regla**: No crear múltiples instancias de EventBus o PluginManager.

---

## Manejo de Errores

### 1. Jerarquía de Excepciones

```python
# core/exceptions.py

class AntivirusException(Exception):
    """Excepción base del sistema"""
    pass

class PluginException(AntivirusException):
    """Excepciones relacionadas con plugins"""
    pass

class PluginLoadError(PluginException):
    """Error al cargar plugin"""
    pass

class PluginInitializationError(PluginException):
    """Error al inicializar plugin"""
    pass

class DetectionException(AntivirusException):
    """Excepciones de detección"""
    pass

class ConfigurationException(AntivirusException):
    """Excepciones de configuración"""
    pass
```

---

### 2. Manejo de Excepciones

**Principios**:

1. **Capturar excepciones específicas**, no genéricas
2. **Loggear siempre** antes de re-lanzar
3. **Proporcionar contexto** en mensajes de error
4. **No silenciar errores** sin razón

**Ejemplo Correcto**:

```python
✅ Correcto:
def load_plugin(plugin_path: Path) -> BasePlugin:
    """Carga un plugin desde el path especificado"""
    try:
        # Validar path
        if not plugin_path.exists():
            raise PluginLoadError(f"Plugin no encontrado: {plugin_path}")
        
        # Cargar módulo
        spec = importlib.util.spec_from_file_location(
            plugin_path.stem, 
            plugin_path
        )
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        
        return module.Plugin()
        
    except ImportError as e:
        logger.error(f"Error importando plugin {plugin_path}: {e}")
        raise PluginLoadError(f"No se pudo importar {plugin_path}") from e
    
    except AttributeError as e:
        logger.error(f"Plugin {plugin_path} no tiene clase Plugin: {e}")
        raise PluginLoadError(f"Plugin inválido: {plugin_path}") from e
    
    except Exception as e:
        logger.error(f"Error inesperado cargando {plugin_path}: {e}")
        raise PluginException(f"Error cargando plugin") from e

❌ Incorrecto:
def load_plugin(plugin_path):
    try:
        # ... código ...
        return module.Plugin()
    except:  # ❌ Muy genérico
        pass  # ❌ Silencia el error
```

---

### 3. Context Managers

**Uso**: Para recursos que requieren limpieza (archivos, conexiones, locks).

```python
✅ Correcto:
from contextlib import contextmanager

@contextmanager
def plugin_lock(plugin_name: str):
    """Context manager para lock de plugin"""
    lock = threading.Lock()
    logger.debug(f"Adquiriendo lock para {plugin_name}")
    lock.acquire()
    try:
        yield lock
    finally:
        lock.release()
        logger.debug(f"Lock liberado para {plugin_name}")

# Uso
with plugin_lock("ml_detector"):
    # Operaciones thread-safe
    detector.process_data()
```

---

## Logging y Monitoreo

### 1. Configuración de Logging

**Niveles de Log**:

| Nivel | Uso | Ejemplo |
|-------|-----|---------|
| `DEBUG` | Información detallada de depuración | `logger.debug(f"Procesando {len(data)} items")` |
| `INFO` | Eventos normales del sistema | `logger.info("Plugin iniciado exitosamente")` |
| `WARNING` | Situaciones inesperadas pero manejables | `logger.warning("Configuración no encontrada, usando defaults")` |
| `ERROR` | Errores que impiden operación específica | `logger.error(f"Error procesando archivo: {e}")` |
| `CRITICAL` | Errores críticos del sistema | `logger.critical("Sistema de detección falló")` |

---

### 2. Formato de Logs

**Estándar**:

```python
# Setup del logger
logger = logging.getLogger(__name__)

# Formato estándar
LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
DATE_FORMAT = "%Y-%m-%d %H:%M:%S"

# Ejemplos de uso
logger.info("✅ Plugin activado exitosamente")
logger.warning("⚠️ Configuración no encontrada, usando defaults")
logger.error(f"❌ Error procesando {file_path}: {error}")
logger.critical("🔥 Sistema crítico falló")
```

**Emojis Recomendados**:

- ✅ Éxito
- ⚠️ Advertencia
- ❌ Error
- 🔥 Crítico
- 📄 Archivo/Configuración
- 🚀 Inicio
- 🔴 Parada
- 📊 Estadísticas
- 🔍 Detección

---

### 3. Logging Estructurado

**Para eventos importantes**, usar logging estructurado:

```python
import json

def log_threat_detected(threat_info: Dict[str, Any]):
    """Log estructurado de amenaza detectada"""
    log_data = {
        "event": "threat_detected",
        "threat_id": threat_info["threat_id"],
        "severity": threat_info["severity"],
        "confidence": threat_info["confidence"],
        "timestamp": datetime.now().isoformat()
    }
    
    logger.warning(
        f"🔍 Amenaza detectada: {threat_info['threat_type']}",
        extra={"structured_data": json.dumps(log_data)}
    )
```

---

### 4. Logging en Plugins

**Cada plugin debe**:

1. Crear su propio logger
2. Usar el nombre del módulo
3. Loggear eventos importantes

```python
class MyDetector(BasePlugin):
    def __init__(self):
        super().__init__("my_detector", __file__)
        self.logger = logging.getLogger(f"plugin.{self.plugin_name}")
    
    def detect_threats(self, data):
        self.logger.debug(f"Analizando {len(data)} procesos")
        
        threats = self._analyze(data)
        
        if threats:
            self.logger.warning(f"🔍 {len(threats)} amenazas detectadas")
        else:
            self.logger.info("✅ No se detectaron amenazas")
        
        return threats
```

---

## Documentación

### 1. Docstrings

**Formato**: Google Style

**Módulos**:

```python
"""
Título del Módulo
=================

Descripción breve del módulo y su propósito.

Este módulo implementa [funcionalidad principal]. Incluye:
- Componente 1
- Componente 2
- Componente 3

Ejemplo de uso:
    from module import MyClass
    
    obj = MyClass()
    obj.do_something()

Atributos:
    MODULE_CONSTANT (int): Descripción de la constante.
"""
```

**Clases**:

```python
class ThreatDetector:
    """
    Detector de amenazas basado en Machine Learning.
    
    Esta clase implementa detección de amenazas usando un modelo
    ONNX pre-entrenado. Analiza procesos del sistema y retorna
    amenazas detectadas con su nivel de confianza.
    
    Attributes:
        model_path (Path): Ruta al modelo ONNX.
        confidence_threshold (float): Umbral de confianza (0.0-1.0).
        is_loaded (bool): Indica si el modelo está cargado.
    
    Example:
        >>> detector = ThreatDetector("models/detector.onnx")
        >>> threats = detector.detect_threats(system_data)
        >>> print(f"Detectadas {len(threats)} amenazas")
    """
```

**Métodos**:

```python
def detect_threats(self, data: Dict[str, Any]) -> List[Dict[str, Any]]:
    """
    Detecta amenazas en los datos del sistema proporcionados.
    
    Analiza procesos, conexiones de red y actividad del sistema
    para identificar comportamientos sospechosos usando el modelo ML.
    
    Args:
        data: Diccionario con datos del sistema que incluye:
            - processes: Lista de procesos activos
            - network: Conexiones de red
            - metrics: Métricas del sistema
    
    Returns:
        Lista de diccionarios con amenazas detectadas. Cada amenaza
        contiene:
            - threat_id: Identificador único
            - threat_type: Tipo de amenaza
            - severity: Nivel de severidad
            - confidence: Nivel de confianza (0.0-1.0)
    
    Raises:
        DetectionException: Si ocurre un error durante la detección.
        ValueError: Si los datos de entrada son inválidos.
    
    Example:
        >>> data = get_system_data()
        >>> threats = detector.detect_threats(data)
        >>> for threat in threats:
        ...     print(f"{threat['threat_type']}: {threat['confidence']}")
    """
```

---

### 2. Comentarios

**Principios**:

1. **Explicar el "por qué", no el "qué"**
2. **Comentar decisiones de diseño**
3. **Marcar TODOs y FIXMEs**
4. **Evitar comentarios obvios**

```python
✅ Correcto:
# Usamos threading en lugar de multiprocessing porque necesitamos
# compartir el estado del EventBus entre todos los plugins
thread = threading.Thread(target=self._monitor_loop)

# TODO: Implementar caché de predicciones para mejorar rendimiento
# FIXME: Race condition cuando múltiples plugins publican simultáneamente

❌ Incorrecto:
# Incrementa el contador
counter += 1

# Crea una lista
my_list = []
```

---

### 3. Type Hints

**Obligatorio** para todas las funciones públicas:

```python
✅ Correcto:
from typing import Dict, List, Optional, Any, Callable

def process_data(
    data: Dict[str, Any],
    threshold: float = 0.7,
    callback: Optional[Callable[[Dict], None]] = None
) -> List[Dict[str, Any]]:
    """Procesa datos y retorna resultados"""
    pass

class MyClass:
    def __init__(self, name: str, config: Dict[str, Any]) -> None:
        self.name: str = name
        self.config: Dict[str, Any] = config
        self.results: List[str] = []

❌ Incorrecto:
def process_data(data, threshold=0.7, callback=None):
    pass
```

---

## Testing

### 1. Estructura de Tests

```
tests/
├── unit/                    # Tests unitarios
│   ├── test_event_bus.py
│   ├── test_plugin_manager.py
│   └── test_detectors.py
│
├── integration/             # Tests de integración
│   ├── test_plugin_lifecycle.py
│   └── test_detection_flow.py
│
├── e2e/                     # Tests end-to-end
│   └── test_full_system.py
│
└── conftest.py              # Fixtures compartidos
```

---

### 2. Convenciones de Testing

**Nombres de Tests**:

```python
✅ Correcto:
def test_event_bus_publishes_to_subscribers():
    """Test que el event bus notifica a suscriptores"""
    pass

def test_plugin_manager_loads_valid_plugin():
    """Test que el plugin manager carga plugins válidos"""
    pass

def test_detector_returns_empty_list_when_no_threats():
    """Test que detector retorna lista vacía sin amenazas"""
    pass

❌ Incorrecto:
def test1():
    pass

def test_plugin():
    pass
```

---

### 3. Estructura de Test

**Patrón AAA** (Arrange, Act, Assert):

```python
def test_threat_detector_detects_keylogger():
    """Test que el detector identifica keyloggers"""
    
    # Arrange - Preparar
    detector = ThreatDetector(model_path="models/test_model.onnx")
    test_data = {
        "processes": [
            {"name": "keylogger.exe", "hooks": ["WH_KEYBOARD_LL"]}
        ]
    }
    
    # Act - Ejecutar
    threats = detector.detect_threats(test_data)
    
    # Assert - Verificar
    assert len(threats) == 1
    assert threats[0]["threat_type"] == "keylogger"
    assert threats[0]["confidence"] > 0.7
```

---

### 4. Fixtures

```python
# conftest.py
import pytest
from core import EventBus, PluginManager

@pytest.fixture
def event_bus():
    """Fixture que proporciona un EventBus limpio"""
    bus = EventBus()
    yield bus
    bus.clear_history()

@pytest.fixture
def plugin_manager(event_bus):
    """Fixture que proporciona un PluginManager configurado"""
    manager = PluginManager(event_bus)
    yield manager
    manager.shutdown()

# Uso en tests
def test_plugin_registration(plugin_manager):
    plugin_manager.register_plugin("test_plugin")
    assert "test_plugin" in plugin_manager.get_plugins()
```

---

### 5. Mocking

```python
from unittest.mock import Mock, patch, MagicMock

def test_detector_handles_model_error():
    """Test que el detector maneja errores del modelo"""
    
    # Mock del modelo
    mock_model = Mock()
    mock_model.predict.side_effect = RuntimeError("Model error")
    
    detector = ThreatDetector(model=mock_model)
    
    with pytest.raises(DetectionException):
        detector.detect_threats({})

@patch('psutil.process_iter')
def test_monitor_gets_processes(mock_process_iter):
    """Test que el monitor obtiene procesos del sistema"""
    
    # Configurar mock
    mock_process_iter.return_value = [
        Mock(name="process1.exe"),
        Mock(name="process2.exe")
    ]
    
    monitor = ProcessMonitor()
    processes = monitor.get_processes()
    
    assert len(processes) == 2
```

---

## Seguridad

### 1. Validación de Entrada

**Siempre validar** datos de entrada:

```python
✅ Correcto:
def load_config(config_path: Path) -> Dict[str, Any]:
    """Carga configuración desde archivo"""
    
    # Validar path
    if not isinstance(config_path, Path):
        raise ValueError("config_path debe ser Path")
    
    if not config_path.exists():
        raise FileNotFoundError(f"Configuración no encontrada: {config_path}")
    
    if not config_path.is_file():
        raise ValueError(f"No es un archivo: {config_path}")
    
    # Validar extensión
    if config_path.suffix not in ['.json', '.toml']:
        raise ValueError(f"Formato no soportado: {config_path.suffix}")
    
    # Cargar y validar contenido
    with open(config_path, 'r') as f:
        config = json.load(f)
    
    if not isinstance(config, dict):
        raise ValueError("Configuración debe ser un diccionario")
    
    return config
```

---

### 2. Manejo de Credenciales

**NUNCA** hardcodear credenciales:

```python
❌ Incorrecto:
API_KEY = "sk_live_1234567890abcdef"
DATABASE_URL = "postgresql://user:password@localhost/db"

✅ Correcto:
import os
from pathlib import Path

# Variables de entorno
API_KEY = os.getenv("ANTIVIRUS_API_KEY")
DATABASE_URL = os.getenv("DATABASE_URL")

# Archivo .env (no en git)
from dotenv import load_dotenv
load_dotenv()

# Validar que existan
if not API_KEY:
    raise ConfigurationException("ANTIVIRUS_API_KEY no configurada")
```

---

### 3. Sanitización de Datos

```python
import re
from pathlib import Path

def sanitize_filename(filename: str) -> str:
    """Sanitiza nombre de archivo para prevenir path traversal"""
    
    # Remover caracteres peligrosos
    safe_name = re.sub(r'[^\w\s.-]', '', filename)
    
    # Prevenir path traversal
    safe_name = safe_name.replace('..', '')
    safe_name = safe_name.replace('/', '')
    safe_name = safe_name.replace('\\', '')
    
    return safe_name

def validate_json_input(data: Any) -> Dict[str, Any]:
    """Valida entrada JSON"""
    
    if not isinstance(data, dict):
        raise ValueError("Entrada debe ser diccionario")
    
    # Limitar tamaño
    json_str = json.dumps(data)
    if len(json_str) > 1_000_000:  # 1MB
        raise ValueError("Entrada JSON demasiado grande")
    
    return data
```

---

### 4. Principio de Mínimo Privilegio

```python
# Ejecutar con privilegios mínimos necesarios
def drop_privileges():
    """Reduce privilegios después de inicialización"""
    if os.name == 'nt':  # Windows
        # Implementar reducción de privilegios
        pass
    else:  # Unix
        import pwd
        nobody = pwd.getpwnam('nobody')
        os.setgid(nobody.pw_gid)
        os.setuid(nobody.pw_uid)
```

---

## Control de Versiones

### 1. Commits

**Formato de Mensaje**:

```
<tipo>(<alcance>): <descripción breve>

<descripción detallada opcional>

<footer opcional>
```

**Tipos**:
- `feat`: Nueva funcionalidad
- `fix`: Corrección de bug
- `docs`: Cambios en documentación
- `style`: Formato, sin cambios de código
- `refactor`: Refactorización de código
- `test`: Agregar o modificar tests
- `chore`: Tareas de mantenimiento

**Ejemplos**:

```bash
✅ Correcto:
feat(detector): agregar detector de red basado en ML
fix(event-bus): corregir race condition en publish
docs(readme): actualizar instrucciones de instalación
refactor(plugins): simplificar carga de configuración
test(detector): agregar tests para ML detector

❌ Incorrecto:
update
fixed bug
changes
wip
```

---

### 2. Branching

**Estrategia**: Git Flow simplificado

```
main              # Producción
  └── develop     # Desarrollo
       ├── feature/nueva-funcionalidad
       ├── fix/correccion-bug
       └── refactor/mejora-codigo
```

**Nombres de Ramas**:

```bash
✅ Correcto:
feature/ml-detector-v2
fix/event-bus-race-condition
refactor/plugin-loading
docs/api-documentation

❌ Incorrecto:
new-feature
bugfix
updates
```

---

### 3. Pull Requests

**Template**:

```markdown
## Descripción
Breve descripción de los cambios realizados.

## Tipo de Cambio
- [ ] Nueva funcionalidad (feature)
- [ ] Corrección de bug (fix)
- [ ] Refactorización (refactor)
- [ ] Documentación (docs)

## Checklist
- [ ] El código sigue el estándar de programación
- [ ] Se agregaron tests para los cambios
- [ ] Todos los tests pasan
- [ ] Se actualizó la documentación
- [ ] No hay warnings de linting

## Tests
Descripción de los tests realizados.

## Screenshots (si aplica)
```

---

## Optimización y Rendimiento

### 1. Principios Generales

1. **Medir antes de optimizar**: Usar profiling
2. **Optimizar cuellos de botella**: No todo el código
3. **Mantener legibilidad**: No sacrificar por micro-optimizaciones

---

### 2. Profiling

```python
import cProfile
import pstats
from functools import wraps
import time

def profile_function(func):
    """Decorador para profiling de funciones"""
    @wraps(func)
    def wrapper(*args, **kwargs):
        profiler = cProfile.Profile()
        profiler.enable()
        
        result = func(*args, **kwargs)
        
        profiler.disable()
        stats = pstats.Stats(profiler)
        stats.sort_stats('cumulative')
        stats.print_stats(10)  # Top 10
        
        return result
    return wrapper

@profile_function
def expensive_operation():
    # Código a perfilar
    pass
```

---

### 3. Optimizaciones Comunes

**Caché de Resultados**:

```python
from functools import lru_cache

@lru_cache(maxsize=128)
def expensive_computation(param: str) -> Dict[str, Any]:
    """Función costosa con caché"""
    # Cálculos pesados
    return result
```

**Lazy Loading**:

```python
class MLDetector:
    def __init__(self, model_path: Path):
        self.model_path = model_path
        self._model = None  # No cargar hasta que se necesite
    
    @property
    def model(self):
        """Lazy loading del modelo"""
        if self._model is None:
            self._model = self._load_model()
        return self._model
```

**Batch Processing**:

```python
def process_threats_batch(threats: List[Dict], batch_size: int = 100):
    """Procesa amenazas en lotes para mejor rendimiento"""
    for i in range(0, len(threats), batch_size):
        batch = threats[i:i + batch_size]
        process_batch(batch)
```

---

### 4. Threading y Concurrencia

```python
import threading
from concurrent.futures import ThreadPoolExecutor
from queue import Queue

# Thread-safe con locks
class ThreadSafeCounter:
    def __init__(self):
        self._value = 0
        self._lock = threading.Lock()
    
    def increment(self):
        with self._lock:
            self._value += 1
    
    @property
    def value(self):
        with self._lock:
            return self._value

# Thread pool para tareas paralelas
def process_files_parallel(files: List[Path], max_workers: int = 4):
    """Procesa archivos en paralelo"""
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        results = executor.map(process_file, files)
    return list(results)
```

---

## Apéndice: Checklist de Revisión de Código

### Pre-Commit Checklist

- [ ] El código sigue las convenciones de nomenclatura
- [ ] Todas las funciones públicas tienen docstrings
- [ ] Se agregaron type hints
- [ ] No hay código comentado innecesario
- [ ] No hay imports sin usar
- [ ] No hay variables sin usar
- [ ] Los logs usan el nivel apropiado
- [ ] Se manejan las excepciones correctamente
- [ ] No hay credenciales hardcodeadas
- [ ] Los tests pasan (`pytest`)
- [ ] No hay warnings de linting (`pylint`, `flake8`)

### Code Review Checklist

- [ ] El código es legible y mantenible
- [ ] La lógica es clara y bien estructurada
- [ ] Se siguen los patrones de diseño establecidos
- [ ] No hay duplicación de código
- [ ] Los nombres son descriptivos
- [ ] La complejidad es razonable
- [ ] Hay tests adecuados
- [ ] La documentación está actualizada
- [ ] No hay problemas de seguridad evidentes
- [ ] El rendimiento es aceptable

---

**Fin del Documento**

*Para más información, consultar:*
- [Diccionario de Datos](DICCIONARIO_DE_DATOS.md)
- [Documentación Técnica](../COMO_FUNCIONA_TECHNICAL_README.md)
- [Arquitectura del Sistema](../ARCHITECTURE_HYBRID.md)
