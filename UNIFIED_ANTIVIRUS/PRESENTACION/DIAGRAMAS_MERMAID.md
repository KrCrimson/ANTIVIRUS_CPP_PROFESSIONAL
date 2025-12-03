# Diagramas del Sistema - Unified Shield

> **Documentación Visual Completa**  
> Formato: Mermaid  
> Fecha: Diciembre 2025

---

## 📋 Tabla de Contenidos

1. [Diagrama de Casos de Uso](#diagrama-de-casos-de-uso)
2. [Diagrama de Secuencia](#diagrama-de-secuencia)
3. [Diagrama de Clases](#diagrama-de-clases)
4. [Diagrama de Componentes](#diagrama-de-componentes)
5. [Diagrama de Despliegue](#diagrama-de-despliegue)
6. [Diagrama de Arquitectura](#diagrama-de-arquitectura)

---

## Diagrama de Casos de Uso

```mermaid
graph TB
    subgraph Actores
        User((Usuario))
        Admin((Administrador))
        System((Sistema))
    end
    
    subgraph "Casos de Uso - Usuario"
        UC1[Iniciar Protección]
        UC2[Ver Dashboard]
        UC3[Revisar Alertas]
        UC4[Escanear Sistema]
        UC5[Ver Estadísticas]
        UC6[Configurar Alertas]
    end
    
    subgraph "Casos de Uso - Administrador"
        UC7[Configurar Plugins]
        UC8[Ver Logs Detallados]
        UC9[Gestionar Cuarentena]
        UC10[Actualizar Firmas]
        UC11[Exportar Reportes]
        UC12[Configurar Seguridad]
    end
    
    subgraph "Casos de Uso - Sistema"
        UC13[Detectar Amenazas]
        UC14[Monitorear Procesos]
        UC15[Enviar Logs Remotos]
        UC16[Actualizar Dashboard Web]
        UC17[Generar Alertas]
    end
    
    User --> UC1
    User --> UC2
    User --> UC3
    User --> UC4
    User --> UC5
    User --> UC6
    
    Admin --> UC7
    Admin --> UC8
    Admin --> UC9
    Admin --> UC10
    Admin --> UC11
    Admin --> UC12
    
    System --> UC13
    System --> UC14
    System --> UC15
    System --> UC16
    System --> UC17
    
    UC13 -.->|extends| UC17
    UC14 -.->|includes| UC13
    UC15 -.->|includes| UC16
```

---

## Diagrama de Secuencia

### Flujo de Detección de Amenazas

```mermaid
sequenceDiagram
    participant U as Usuario
    participant UI as Interfaz UI
    participant E as Engine
    participant D as ML Detector
    participant EB as Event Bus
    participant H as Threat Handler
    participant DB as Database
    
    U->>UI: Iniciar protección
    UI->>E: start_protection()
    E->>D: activate()
    D->>D: load_model()
    D->>D: start_monitoring()
    D-->>E: Plugin activado
    E-->>UI: Protección iniciada
    UI-->>U: Mostrar estado activo
    
    loop Monitoreo continuo
        D->>D: get_system_data()
        D->>D: extract_features()
        D->>D: predict_threat(features)
        
        alt Amenaza detectada
            D->>D: create_threat_info()
            D->>EB: publish("threat_detected", threat_info)
            
            par Notificar componentes
                EB->>H: notify(threat_info)
                EB->>UI: notify(threat_info)
                EB->>DB: log_event(threat_info)
            end
            
            H->>H: handle_threat()
            H->>H: quarantine_process()
            H-->>EB: publish("threat_handled")
            
            UI->>U: Mostrar alerta crítica
            U->>UI: Ver detalles
            UI->>U: Mostrar información completa
        else Sin amenazas
            D->>D: continue_monitoring()
        end
    end
```

### Flujo de Logs Remotos

```mermaid
sequenceDiagram
    participant Client as Antivirus Client
    participant Monitor as Monitor Script
    participant API as Vercel API
    participant DB as PostgreSQL
    participant Dashboard as Web Dashboard
    
    rect rgb(200, 220, 255)
        Note over Client,Monitor: Registro de Instancia
        Client->>Monitor: Iniciar monitor
        Monitor->>API: POST /api/instances<br/>{id, hostname, os_info}
        API->>API: Validar API Key
        API->>DB: INSERT INTO antivirus_instances
        DB-->>API: Confirmación
        API-->>Monitor: 200 OK {success: true}
    end
    
    rect rgb(255, 220, 200)
        Note over Client,DB: Envío de Logs
        Client->>Monitor: Evento de seguridad<br/>(Threat detected)
        Monitor->>Monitor: Serializar a JSON
        Monitor->>API: POST /api/logs<br/>{timestamp, level, message}
        API->>API: Validar schema (Pydantic)
        API->>DB: INSERT INTO log_entries
        DB-->>API: Log ID: 3653
        API->>DB: UPDATE instances<br/>SET last_seen = NOW()
        DB-->>API: Updated
        API-->>Monitor: 200 OK {log_id: "3653"}
    end
    
    rect rgb(200, 255, 220)
        Note over Dashboard,DB: Visualización
        Dashboard->>API: GET /api/stats
        API->>DB: SELECT COUNT(*)<br/>GROUP BY level
        DB-->>API: Aggregated data
        API-->>Dashboard: JSON response<br/>{total_logs: 3653}
        Dashboard->>Dashboard: Renderizar gráficos<br/>(Chart.js)
    end
    
    loop Auto-refresh cada 30s
        Dashboard->>API: GET /api/logs?limit=100
        API->>DB: SELECT * FROM log_entries<br/>ORDER BY received_at DESC
        DB-->>API: Latest logs
        API-->>Dashboard: JSON array
        Dashboard->>Dashboard: Actualizar tabla
    end
    
    rect rgb(255, 200, 200)
        Note over Client,Monitor: Manejo de Errores
        Client->>Monitor: Evento crítico
        Monitor->>API: POST /api/logs
        API->>API: Validación fallida
        API-->>Monitor: 500 Internal Error
        Monitor->>Monitor: Retry (1/4)
        Monitor->>API: POST /api/logs (retry)
        API->>DB: INSERT successful
        DB-->>API: OK
        API-->>Monitor: 200 OK
    end
```

---

## Diagrama de Clases

```mermaid
classDiagram
    class BasePlugin {
        <<abstract>>
        +string plugin_name
        +dict config
        +bool is_running
        +Logger logger
        +activate() bool
        +deactivate() bool
        +initialize()* bool
        +start()* bool
        +stop()* bool
        +get_plugin_info()* dict
        #setup_logging() void
        #load_config() void
        #cleanup() void
    }
    
    class DetectorInterface {
        <<interface>>
        +detect_threats(data: dict) list
        +get_confidence_score() float
        +update_signatures() bool
        +get_detection_statistics() dict
    }
    
    class MonitorInterface {
        <<interface>>
        +start_monitoring() bool
        +stop_monitoring() bool
        +get_current_data() dict
        +set_data_callback(callback) void
        +get_monitoring_statistics() dict
    }
    
    class HandlerInterface {
        <<interface>>
        +handle_threat(threat_data: dict) bool
        +can_handle_threat_type(threat_type: str) bool
        +get_handler_priority() int
        +rollback_action(action_id: str) bool
    }
    
    class MLDetector {
        -ONNXModel model
        -float threshold
        -dict feature_extractor
        +detect_threats(data: dict) list
        +load_model() bool
        +extract_features(data: dict) array
        +predict(features: array) float
    }
    
    class BehaviorDetector {
        -dict patterns
        -int cpu_threshold
        -int memory_threshold
        +detect_threats(data: dict) list
        +analyze_behavior(process: dict) bool
        +check_suspicious_patterns() list
    }
    
    class EventBus {
        -dict~str,list~ _subscribers
        -list _event_history
        -RLock _lock
        +subscribe(event_type: str, callback) bool
        +unsubscribe(event_type: str, callback) bool
        +publish(event_type: str, data: dict) bool
        +get_recent_events(event_type: str) list
        +get_statistics() dict
        -_notify_subscribers(event, subscribers) void
    }
    
    class PluginManager {
        -dict plugins
        -EventBus event_bus
        -PluginRegistry registry
        +register_plugin(plugin: BasePlugin) bool
        +unregister_plugin(plugin_name: str) bool
        +load_plugins() bool
        +get_plugin(plugin_name: str) BasePlugin
        +get_all_plugins() list
    }
    
    class UnifiedAntivirusEngine {
        -PluginManager plugin_manager
        -EventBus event_bus
        -dict config
        -bool is_running
        +start() bool
        +stop() bool
        +scan_system() dict
        +get_status() dict
        +update_config(config: dict) bool
    }
    
    class ThreatInfo {
        +string threat_id
        +string threat_type
        +string severity
        +string description
        +string source_plugin
        +float confidence
        +datetime timestamp
        +dict additional_data
        +to_dict() dict
    }
    
    class Event {
        +string event_id
        +string event_type
        +dict data
        +string source
        +datetime timestamp
        +to_dict() dict
    }
    
    BasePlugin <|-- MLDetector
    BasePlugin <|-- BehaviorDetector
    DetectorInterface <|.. MLDetector
    DetectorInterface <|.. BehaviorDetector
    MonitorInterface <|.. BehaviorDetector
    
    UnifiedAntivirusEngine --> PluginManager
    UnifiedAntivirusEngine --> EventBus
    PluginManager --> BasePlugin
    PluginManager --> EventBus
    EventBus --> Event
    MLDetector --> ThreatInfo
    BehaviorDetector --> ThreatInfo
```

---

## Diagrama de Componentes

```mermaid
graph TB
    subgraph "Frontend Layer"
        UI[UI Component<br/>Tkinter/Web]
        Dashboard[Web Dashboard<br/>HTML/JS/Chart.js]
    end
    
    subgraph "Application Layer"
        Engine[Antivirus Engine<br/>Core Controller]
        PM[Plugin Manager<br/>Registry Pattern]
        EB[Event Bus<br/>Observer Pattern]
    end
    
    subgraph "Plugin Layer"
        subgraph "Detectors"
            D1[ML Detector<br/>ONNX Model]
            D2[Behavior Detector<br/>Pattern Analysis]
            D3[Network Detector<br/>Traffic Analysis]
        end
        
        subgraph "Monitors"
            M1[Process Monitor<br/>System Tracking]
            M2[File Monitor<br/>FS Watcher]
        end
        
        subgraph "Handlers"
            H1[Threat Handler<br/>Response Actions]
            H2[Logger Handler<br/>Event Logging]
            H3[Web Handler<br/>Remote Logging]
        end
    end
    
    subgraph "Infrastructure Layer"
        DB[(PostgreSQL<br/>Database)]
        FS[File System<br/>Logs/Config]
        Models[ML Models<br/>ONNX Files]
        API[Web API<br/>FastAPI/Vercel]
    end
    
    UI --> Engine
    Dashboard --> API
    Engine --> PM
    Engine --> EB
    PM --> D1
    PM --> D2
    PM --> D3
    PM --> M1
    PM --> M2
    PM --> H1
    PM --> H2
    PM --> H3
    
    D1 --> Models
    D2 --> M1
    D3 --> M1
    M1 --> FS
    M2 --> FS
    H2 --> FS
    H3 --> API
    API --> DB
    
    EB -.->|events| D1
    EB -.->|events| D2
    EB -.->|events| H1
    EB -.->|events| H2
    EB -.->|events| UI
    
    style UI fill:#667eea,color:#fff
    style Dashboard fill:#667eea,color:#fff
    style Engine fill:#3b82f6,color:#fff
    style PM fill:#3b82f6,color:#fff
    style EB fill:#3b82f6,color:#fff
    style D1 fill:#10b981,color:#fff
    style D2 fill:#10b981,color:#fff
    style D3 fill:#10b981,color:#fff
    style M1 fill:#f59e0b,color:#fff
    style M2 fill:#f59e0b,color:#fff
    style H1 fill:#ef4444,color:#fff
    style H2 fill:#ef4444,color:#fff
    style H3 fill:#ef4444,color:#fff
```

---

## Diagrama de Despliegue

```mermaid
graph TB
    subgraph "Client Machine (Windows)"
        subgraph "Python Runtime"
            App[Antivirus Application<br/>professional_ui_robust.py]
            Plugins[Plugin System<br/>Detectors/Monitors/Handlers]
            Monitor[Monitor Client<br/>start_monitor_client.py]
        end
        
        subgraph "Local Storage"
            Logs[Log Files<br/>logs/]
            Config[Configuration<br/>config/]
            Models[ML Models<br/>models/]
        end
    end
    
    subgraph "Cloud Infrastructure"
        subgraph "Vercel Platform"
            subgraph "Edge Network"
                Edge1[us-east-1]
                Edge2[eu-west-1]
                Edge3[ap-southeast-1]
            end
            
            API[FastAPI Backend<br/>main.py]
            Build[Build Server<br/>CI/CD]
        end
        
        subgraph "Neon (AWS)"
            DB[(PostgreSQL<br/>Serverless)]
            Compute[Compute Layer<br/>Auto-scaling]
            Storage[Storage Layer<br/>Separated]
        end
        
        subgraph "GitHub"
            Repo[Repository]
            Actions[GitHub Actions<br/>Workflows]
            Pages[GitHub Pages<br/>Reports]
        end
    end
    
    subgraph "End Users"
        Browser[Web Browser<br/>Dashboard Access]
    end
    
    App --> Plugins
    App --> Logs
    App --> Config
    Plugins --> Models
    Monitor --> API
    
    API --> Edge1
    API --> Edge2
    API --> Edge3
    
    Edge1 --> DB
    Edge2 --> DB
    Edge3 --> DB
    
    DB --> Compute
    Compute --> Storage
    
    Browser --> Edge1
    Browser --> Edge2
    Browser --> Edge3
    
    Repo --> Actions
    Actions --> Build
    Build --> Edge1
    Actions --> Pages
    
    style App fill:#667eea,color:#fff
    style API fill:#3b82f6,color:#fff
    style DB fill:#10b981,color:#fff
    style Browser fill:#f59e0b,color:#fff
```

---

## Diagrama de Arquitectura

### Arquitectura en Capas

```mermaid
graph TB
    subgraph "Presentation Layer"
        UI1[Desktop UI<br/>Tkinter]
        UI2[Web Dashboard<br/>HTML/JS]
        UI3[CLI Interface<br/>Command Line]
    end
    
    subgraph "Application Layer"
        Engine[Antivirus Engine<br/>Core Orchestrator]
        PM[Plugin Manager<br/>Lifecycle Management]
        EB[Event Bus<br/>Pub/Sub System]
        Config[Configuration Manager<br/>Settings Handler]
    end
    
    subgraph "Domain Layer"
        subgraph "Plugin System"
            Detectors[Threat Detectors<br/>ML, Behavior, Network]
            Monitors[System Monitors<br/>Process, File, Registry]
            Handlers[Event Handlers<br/>Alerts, Logging, Quarantine]
        end
        
        subgraph "Business Logic"
            ThreatAnalysis[Threat Analysis<br/>Risk Assessment]
            ResponseLogic[Response Logic<br/>Action Decisions]
            ReportGen[Report Generation<br/>Statistics & Metrics]
        end
    end
    
    subgraph "Infrastructure Layer"
        subgraph "Data Access"
            LocalDB[Local Storage<br/>SQLite/Files]
            RemoteDB[Remote Database<br/>PostgreSQL]
            Cache[Cache Layer<br/>In-Memory]
        end
        
        subgraph "External Services"
            WebAPI[Web API Client<br/>HTTP/REST]
            MLEngine[ML Engine<br/>ONNX Runtime]
            SystemAPI[System APIs<br/>OS Integration]
        end
    end
    
    subgraph "Cross-Cutting Concerns"
        Logging[Logging System<br/>Multi-level]
        Security[Security Layer<br/>Auth & Encryption]
        Monitoring[Health Monitoring<br/>Performance Metrics]
        ErrorHandling[Error Handling<br/>Exception Management]
    end
    
    UI1 --> Engine
    UI2 --> Engine
    UI3 --> Engine
    
    Engine --> PM
    Engine --> EB
    Engine --> Config
    
    PM --> Detectors
    PM --> Monitors
    PM --> Handlers
    
    Detectors --> ThreatAnalysis
    ThreatAnalysis --> ResponseLogic
    ResponseLogic --> Handlers
    Handlers --> ReportGen
    
    Detectors --> MLEngine
    Monitors --> SystemAPI
    Handlers --> LocalDB
    Handlers --> RemoteDB
    
    Engine --> WebAPI
    WebAPI --> RemoteDB
    
    Logging -.->|logs| Engine
    Logging -.->|logs| PM
    Logging -.->|logs| Detectors
    
    Security -.->|secures| Engine
    Security -.->|secures| WebAPI
    Security -.->|secures| RemoteDB
    
    Monitoring -.->|monitors| Engine
    Monitoring -.->|monitors| PM
    
    ErrorHandling -.->|handles| Engine
    ErrorHandling -.->|handles| Detectors
    
    style UI1 fill:#667eea,color:#fff
    style UI2 fill:#667eea,color:#fff
    style Engine fill:#3b82f6,color:#fff
    style PM fill:#3b82f6,color:#fff
    style EB fill:#3b82f6,color:#fff
    style Detectors fill:#10b981,color:#fff
    style Monitors fill:#10b981,color:#fff
    style Handlers fill:#10b981,color:#fff
    style RemoteDB fill:#f59e0b,color:#fff
    style MLEngine fill:#f59e0b,color:#fff
```

### Patrones de Diseño Implementados

```mermaid
graph LR
    subgraph "Creational Patterns"
        Singleton[Singleton<br/>EventBus, PluginManager]
        Factory[Factory<br/>Plugin Creation]
    end
    
    subgraph "Structural Patterns"
        Adapter[Adapter<br/>External APIs]
        Facade[Facade<br/>Engine Interface]
        Decorator[Decorator<br/>Plugin Enhancement]
    end
    
    subgraph "Behavioral Patterns"
        Observer[Observer<br/>Event Bus]
        Strategy[Strategy<br/>Detection Algorithms]
        Template[Template Method<br/>BasePlugin]
        Command[Command<br/>Threat Actions]
    end
    
    style Singleton fill:#667eea,color:#fff
    style Observer fill:#10b981,color:#fff
    style Strategy fill:#10b981,color:#fff
    style Template fill:#10b981,color:#fff
```

---

## Notas de Implementación

### Tecnologías Utilizadas

| Capa | Tecnologías |
|------|-------------|
| **Frontend** | Tkinter, HTML5, CSS3, JavaScript, Chart.js |
| **Backend** | Python 3.8+, FastAPI, SQLAlchemy |
| **Database** | PostgreSQL (Neon), SQLite (local) |
| **ML** | ONNX Runtime, scikit-learn |
| **Deployment** | Vercel, GitHub Actions |
| **Monitoring** | Custom logging, Web dashboard |

### Principios de Diseño

- **SOLID Principles**: Aplicados en toda la arquitectura
- **DRY (Don't Repeat Yourself)**: Código reutilizable
- **KISS (Keep It Simple, Stupid)**: Simplicidad en diseño
- **Separation of Concerns**: Capas bien definidas
- **Dependency Injection**: Desacoplamiento de componentes

---

**Fin del Documento**

*Estos diagramas proporcionan una visión completa de la arquitectura, componentes, flujos de datos y patrones de diseño del sistema Unified Shield.*
