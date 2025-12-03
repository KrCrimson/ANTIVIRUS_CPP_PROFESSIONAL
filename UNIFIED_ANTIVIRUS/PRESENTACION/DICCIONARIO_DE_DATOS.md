# Diccionario de Datos - UNIFIED ANTIVIRUS

> **Documento de Referencia Técnica**  
> Versión: 1.0  
> Fecha: Diciembre 2025  
> Sistema: Unified Shield Anti-Keylogger Professional

---

## 📋 Tabla de Contenidos

1. [Introducción](#introducción)
2. [Modelos de Datos Core](#modelos-de-datos-core)
3. [Estructuras de Base de Datos](#estructuras-de-base-de-datos)
4. [Interfaces y Contratos](#interfaces-y-contratos)
5. [Eventos del Sistema](#eventos-del-sistema)
6. [Configuraciones](#configuraciones)
7. [Estructuras de Plugins](#estructuras-de-plugins)
8. [Tipos de Datos Comunes](#tipos-de-datos-comunes)

---

## Introducción

Este documento define todas las estructuras de datos utilizadas en el sistema UNIFIED ANTIVIRUS. Incluye modelos de dominio, esquemas de base de datos, interfaces de plugins, formatos de eventos, y configuraciones del sistema.

### Convenciones de Notación

- **Campo obligatorio**: Marcado con `*`
- **Campo opcional**: Sin marca especial
- **Tipo de dato**: Especificado entre `< >`
- **Valores por defecto**: Indicados con `= valor`

---

## Modelos de Datos Core

### 1. ThreatInfo

**Descripción**: Clase de datos para información estandarizada de amenazas detectadas.

**Ubicación**: `core/interfaces.py`

| Campo | Tipo | Obligatorio | Descripción | Valores Posibles |
|-------|------|-------------|-------------|------------------|
| `threat_id` | `<string>` | * | Identificador único de la amenaza | Formato: `{tipo}_{timestamp}` |
| `threat_type` | `<string>` | * | Tipo de amenaza detectada | `keylogger`, `malware`, `suspicious_behavior`, `network_threat` |
| `severity` | `<string>` | * | Nivel de severidad | `LOW`, `MEDIUM`, `HIGH`, `CRITICAL` |
| `description` | `<string>` | * | Descripción detallada de la amenaza | Texto libre |
| `source_plugin` | `<string>` | * | Plugin que detectó la amenaza | Nombre del plugin detector |
| `confidence` | `<float>` | * | Nivel de confianza de la detección | 0.0 - 1.0 (default: 1.0) |
| `timestamp` | `<datetime>` | * | Momento de detección | ISO 8601 format |
| `additional_data` | `<dict>` | | Datos adicionales específicos | Estructura variable según tipo |

**Ejemplo JSON**:
```json
{
  "threat_id": "keylogger_1701619200",
  "threat_type": "keylogger",
  "severity": "CRITICAL",
  "description": "Proceso sospechoso con hooks de teclado detectado",
  "source_plugin": "ml_detector",
  "confidence": 0.95,
  "timestamp": "2025-12-03T15:00:00.000Z",
  "additional_data": {
    "process_name": "suspicious.exe",
    "pid": 1234,
    "hooks_detected": ["WH_KEYBOARD_LL"]
  }
}
```

---

### 2. SystemData

**Descripción**: Clase de datos para información estandarizada del sistema monitoreado.

**Ubicación**: `core/interfaces.py`

| Campo | Tipo | Obligatorio | Descripción |
|-------|------|-------------|-------------|
| `timestamp` | `<datetime>` | * | Momento de captura de datos |
| `processes` | `<list[dict]>` | * | Lista de procesos en ejecución |
| `network_connections` | `<list[dict]>` | * | Conexiones de red activas |
| `file_changes` | `<list[dict]>` | * | Cambios en el sistema de archivos |
| `registry_changes` | `<list[dict]>` | * | Modificaciones en el registro (Windows) |
| `system_metrics` | `<dict>` | * | Métricas del sistema (CPU, RAM, etc.) |

**Estructura de Process Info**:
```json
{
  "pid": "<int>",
  "name": "<string>",
  "exe_path": "<string>",
  "cpu_percent": "<float>",
  "memory_mb": "<float>",
  "threads": "<int>",
  "connections": "<int>",
  "create_time": "<datetime>"
}
```

**Estructura de Network Info**:
```json
{
  "local_address": "<string>",
  "local_port": "<int>",
  "remote_address": "<string>",
  "remote_port": "<int>",
  "status": "<string>",
  "pid": "<int>"
}
```

---

### 3. Event

**Descripción**: Representa un evento en el sistema de comunicación (Event Bus).

**Ubicación**: `core/event_bus.py`

| Campo | Tipo | Obligatorio | Descripción |
|-------|------|-------------|-------------|
| `event_id` | `<string>` | * | Identificador único del evento |
| `event_type` | `<string>` | * | Tipo de evento |
| `data` | `<dict>` | * | Datos del evento |
| `source` | `<string>` | | Plugin/componente origen |
| `timestamp` | `<datetime>` | * | Momento de creación del evento |

**Tipos de Eventos Comunes**:
- `threat_detected` - Amenaza detectada
- `scan_complete` - Escaneo completado
- `plugin_started` - Plugin iniciado
- `plugin_stopped` - Plugin detenido
- `config_updated` - Configuración actualizada
- `system_status_changed` - Estado del sistema cambió

---

## Estructuras de Base de Datos

### 1. Tabla: antivirus_instances

**Descripción**: Almacena información de instancias del antivirus desplegadas.

**Motor**: PostgreSQL

| Columna | Tipo | Restricciones | Descripción |
|---------|------|---------------|-------------|
| `id` | `VARCHAR(36)` | PRIMARY KEY | UUID de la instancia |
| `hostname` | `VARCHAR(255)` | | Nombre del host |
| `os_info` | `VARCHAR(255)` | | Información del sistema operativo |
| `antivirus_version` | `VARCHAR(50)` | | Versión del antivirus |
| `status` | `VARCHAR(20)` | DEFAULT 'active' | Estado: `active`, `inactive`, `error` |
| `created_at` | `TIMESTAMP` | DEFAULT CURRENT_TIMESTAMP | Fecha de creación |
| `last_seen` | `TIMESTAMP` | DEFAULT CURRENT_TIMESTAMP | Última comunicación |

**Índices**:
- `idx_instances_status` en `status`

---

### 2. Tabla: log_entries

**Descripción**: Almacena logs del sistema de todas las instancias.

**Motor**: PostgreSQL

| Columna | Tipo | Restricciones | Descripción |
|---------|------|---------------|-------------|
| `id` | `SERIAL` | PRIMARY KEY | ID autoincremental |
| `timestamp` | `TIMESTAMP` | NOT NULL | Momento del log |
| `level` | `VARCHAR(20)` | NOT NULL | Nivel: `DEBUG`, `INFO`, `WARNING`, `ERROR`, `CRITICAL` |
| `component` | `VARCHAR(100)` | | Componente que generó el log |
| `message` | `TEXT` | NOT NULL | Mensaje del log |
| `instance_id` | `VARCHAR(36)` | FOREIGN KEY | Referencia a instancia |
| `details` | `JSONB` | | Detalles adicionales en formato JSON |
| `received_at` | `TIMESTAMP` | DEFAULT CURRENT_TIMESTAMP | Momento de recepción |

**Índices**:
- `idx_logs_instance_id` en `instance_id`
- `idx_logs_timestamp` en `timestamp`
- `idx_logs_level` en `level`

**Relaciones**:
- `instance_id` → `antivirus_instances.id` (ON DELETE CASCADE)

---

## Interfaces y Contratos

### 1. DetectorInterface

**Descripción**: Interface para plugins detectores de amenazas.

**Ubicación**: `core/interfaces.py`

**Métodos Obligatorios**:

| Método | Parámetros | Retorno | Descripción |
|--------|-----------|---------|-------------|
| `detect_threats` | `data: Dict[str, Any]` | `List[Dict[str, Any]]` | Detecta amenazas en los datos |
| `get_confidence_score` | - | `float` | Nivel de confianza (0.0-1.0) |
| `update_signatures` | - | `bool` | Actualiza firmas de detección |
| `get_detection_statistics` | - | `Dict[str, Any]` | Estadísticas de detección |

---

### 2. MonitorInterface

**Descripción**: Interface para plugins de monitoreo del sistema.

**Ubicación**: `core/interfaces.py`

**Métodos Obligatorios**:

| Método | Parámetros | Retorno | Descripción |
|--------|-----------|---------|-------------|
| `start_monitoring` | - | `bool` | Inicia monitoreo continuo |
| `stop_monitoring` | - | `bool` | Detiene monitoreo |
| `get_current_data` | - | `Dict[str, Any]` | Obtiene datos actuales |
| `set_data_callback` | `callback: Callable` | `None` | Establece callback para datos |
| `get_monitoring_statistics` | - | `Dict[str, Any]` | Estadísticas de monitoreo |

---

### 3. HandlerInterface

**Descripción**: Interface para plugins manejadores de amenazas.

**Ubicación**: `core/interfaces.py`

**Métodos Obligatorios**:

| Método | Parámetros | Retorno | Descripción |
|--------|-----------|---------|-------------|
| `handle_threat` | `threat_data: Dict[str, Any]` | `bool` | Maneja una amenaza |
| `can_handle_threat_type` | `threat_type: str` | `bool` | Verifica si puede manejar el tipo |
| `get_handler_priority` | - | `int` | Prioridad del manejador |
| `rollback_action` | `action_id: str` | `bool` | Revierte una acción |

---

### 4. ConfigurableInterface

**Descripción**: Interface para plugins con configuración dinámica.

**Ubicación**: `core/interfaces.py`

**Métodos Obligatorios**:

| Método | Parámetros | Retorno | Descripción |
|--------|-----------|---------|-------------|
| `reload_configuration` | - | `bool` | Recarga configuración |
| `validate_configuration` | `config: Dict[str, Any]` | `List[str]` | Valida configuración |
| `get_configuration_schema` | - | `Dict[str, Any]` | Esquema de configuración |

---

## Eventos del Sistema

### Estructura General de Eventos

Todos los eventos publicados en el Event Bus siguen esta estructura:

```json
{
  "event_id": "<string>",
  "event_type": "<string>",
  "data": {
    // Datos específicos del evento
  },
  "source": "<string>",
  "timestamp": "<ISO 8601 datetime>"
}
```

### Catálogo de Eventos

#### 1. threat_detected

**Descripción**: Se emite cuando se detecta una amenaza.

**Datos**:
```json
{
  "threat_info": {
    "threat_id": "<string>",
    "threat_type": "<string>",
    "severity": "<string>",
    "description": "<string>",
    "confidence": "<float>",
    "process_info": {
      "pid": "<int>",
      "name": "<string>",
      "path": "<string>"
    }
  }
}
```

#### 2. scan_complete

**Descripción**: Se emite al completar un escaneo.

**Datos**:
```json
{
  "scan_id": "<string>",
  "scan_type": "<string>",
  "duration_seconds": "<float>",
  "items_scanned": "<int>",
  "threats_found": "<int>",
  "results": []
}
```

#### 3. plugin_lifecycle

**Descripción**: Eventos de ciclo de vida de plugins.

**Subtipos**: `plugin_started`, `plugin_stopped`, `plugin_error`

**Datos**:
```json
{
  "plugin_name": "<string>",
  "plugin_type": "<string>",
  "status": "<string>",
  "message": "<string>"
}
```

---

## Configuraciones

### 1. plugins_config.json

**Descripción**: Configuración del sistema de plugins.

**Ubicación**: `config/plugins_config.json`

**Estructura**:

```json
{
  "plugin_system": {
    "enabled": "<bool>",
    "auto_discovery": "<bool>",
    "plugin_directories": ["<string>"],
    "default_timeout": "<int>",
    "max_concurrent": "<int>",
    "restart_on_failure": "<bool>",
    "failure_threshold": "<int>"
  },
  "detectors": {
    "<plugin_name>": {
      "enabled": "<bool>",
      "priority": "<int>",
      "config": {}
    }
  },
  "interfaces": {},
  "handlers": {}
}
```

---

### 2. ml_config.json

**Descripción**: Configuración de modelos de Machine Learning.

**Ubicación**: `config/ml_config.json`

**Estructura Principal**:

```json
{
  "models": {
    "primary_model": {
      "name": "<string>",
      "path": "<string>",
      "type": "<string>",
      "enabled": "<bool>",
      "confidence_threshold": "<float>",
      "preprocessing": {}
    }
  },
  "feature_extraction": {
    "process_features": {},
    "behavioral_features": {},
    "temporal_features": {}
  },
  "inference": {
    "batch_size": "<int>",
    "max_latency_ms": "<int>",
    "parallel_processing": "<bool>",
    "gpu_acceleration": "<bool>"
  }
}
```

---

### 3. security_config.json

**Descripción**: Configuración de seguridad del sistema.

**Ubicación**: `config/security_config.json`

**Estructura Principal**:

```json
{
  "security": {
    "access_control": {
      "require_admin": "<bool>",
      "config_protection": "<bool>"
    },
    "integrity": {
      "file_verification": "<bool>",
      "tamper_detection": "<bool>"
    },
    "encryption": {
      "encrypt_logs": "<bool>",
      "algorithm": "<string>"
    }
  },
  "monitoring": {
    "self_protection": {},
    "system_monitoring": {}
  },
  "response": {
    "automated_responses": {},
    "manual_approval": {}
  }
}
```

---

### 4. logging_config.json

**Descripción**: Configuración del sistema de logging.

**Ubicación**: `config/logging_config.json`

**Campos Principales**:

| Campo | Tipo | Descripción |
|-------|------|-------------|
| `version` | `<int>` | Versión del esquema de configuración |
| `disable_existing_loggers` | `<bool>` | Deshabilitar loggers existentes |
| `formatters` | `<dict>` | Formateadores de logs |
| `handlers` | `<dict>` | Manejadores de logs |
| `loggers` | `<dict>` | Configuración de loggers |
| `root` | `<dict>` | Logger raíz |

---

## Estructuras de Plugins

### 1. Plugin Metadata (plugin.json)

**Descripción**: Metadatos de cada plugin.

**Ubicación**: `plugins/<plugin_name>/plugin.json`

```json
{
  "name": "<string>",
  "version": "<string>",
  "type": "<string>",
  "description": "<string>",
  "author": "<string>",
  "dependencies": ["<string>"],
  "interfaces": ["<string>"],
  "config_schema": {}
}
```

**Tipos de Plugin**:
- `detector` - Detector de amenazas
- `monitor` - Monitor del sistema
- `handler` - Manejador de eventos
- `interface` - Interfaz de usuario

---

### 2. Plugin Configuration

**Descripción**: Configuración específica de cada plugin.

**Ubicación**: `plugins/<plugin_name>/config.json`

**Estructura Variable**: Depende del tipo de plugin.

**Ejemplo - Behavior Detector**:
```json
{
  "cpu_threshold": 80,
  "memory_threshold_mb": 100,
  "scan_interval": 5,
  "monitor_new_processes": true,
  "track_process_tree": true
}
```

---

## Tipos de Datos Comunes

### Type Aliases

**Ubicación**: `core/interfaces.py`

```python
ThreatData = Dict[str, Any]
SystemDataDict = Dict[str, Any]
ConfigDict = Dict[str, Any]
StatsDict = Dict[str, Any]
PluginCallback = Callable[[Dict[str, Any]], None]
```

---

### Enumeraciones

#### Severity Levels
- `LOW` - Baja prioridad
- `MEDIUM` - Prioridad media
- `HIGH` - Alta prioridad
- `CRITICAL` - Prioridad crítica

#### Plugin States
- `initialized` - Inicializado
- `running` - En ejecución
- `stopped` - Detenido
- `error` - Error

#### Log Levels
- `DEBUG` - Información de depuración
- `INFO` - Información general
- `WARNING` - Advertencias
- `ERROR` - Errores
- `CRITICAL` - Errores críticos

---

### Formatos de Identificadores

| Tipo | Formato | Ejemplo |
|------|---------|---------|
| Threat ID | `{tipo}_{timestamp}` | `keylogger_1701619200` |
| Event ID | `{tipo}_{fecha}_{microseg}` | `threat_detected_20251203_150000_123456` |
| Instance ID | UUID v4 | `550e8400-e29b-41d4-a716-446655440000` |
| Plugin Name | snake_case | `ml_detector`, `behavior_monitor` |

---

## Métricas del Sistema

### Dashboard Metrics

**Descripción**: Métricas mostradas en el dashboard principal.

```json
{
  "threats_detected": "<int>",
  "processes_monitored": "<int>",
  "cpu_usage": "<float>",
  "memory_usage": "<float>",
  "active_connections": "<int>",
  "scan_status": "<string>",
  "protection_status": "<string>",
  "last_scan_time": "<datetime>"
}
```

---

### Performance Metrics

**Descripción**: Métricas de rendimiento de plugins.

```json
{
  "plugin_name": "<string>",
  "uptime_seconds": "<float>",
  "events_processed": "<int>",
  "avg_processing_time_ms": "<float>",
  "error_count": "<int>",
  "memory_usage_mb": "<float>",
  "cpu_percent": "<float>"
}
```

---

## Apéndice: Diagramas de Relaciones

### Relación de Entidades

```
antivirus_instances (1) ──── (N) log_entries
       │
       └── Identificado por: instance_id (UUID)
```

### Flujo de Datos de Eventos

```
Plugin Detector
    │
    ├─► Event Bus (publish)
    │       │
    │       ├─► Plugin Handler (subscribe)
    │       ├─► UI Plugin (subscribe)
    │       └─► Logger Handler (subscribe)
    │
    └─► Database (log_entries)
```

---

## Glosario

| Término | Definición |
|---------|------------|
| **Event Bus** | Sistema de comunicación pub/sub entre componentes |
| **Plugin** | Módulo extensible que implementa funcionalidad específica |
| **Threat** | Amenaza de seguridad detectada por el sistema |
| **Handler** | Componente que responde a eventos o amenazas |
| **Detector** | Plugin que identifica amenazas |
| **Monitor** | Plugin que observa el estado del sistema |
| **Confidence Score** | Nivel de certeza de una detección (0.0-1.0) |
| **Severity** | Nivel de gravedad de una amenaza |

---

**Fin del Documento**

*Para más información, consultar:*
- [Estándar de Programación](ESTANDAR_DE_PROGRAMACION.md)
- [Documentación Técnica](../COMO_FUNCIONA_TECHNICAL_README.md)
- [Arquitectura del Sistema](../ARCHITECTURE_HYBRID.md)
