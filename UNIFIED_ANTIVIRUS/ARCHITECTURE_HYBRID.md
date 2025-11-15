# 🏗️ Arquitectura Híbrida: Antivirus + Web System

## 📋 **Separación de Responsabilidades**

### 🖥️ **ANTIVIRUS CORE (Nativo)**
```
Ubicación: Windows Process (No Docker)
Responsabilidad: Protección en Tiempo Real

COMPONENTES:
├── 🚀 launcher.py - Proceso principal
├── 🔧 core/engine.py - Motor de detección  
├── 🔌 plugins/ - Detectores especializados
├── 🛡️ monitors/ - Monitoreo continuo
├── ⚙️ utils/logger.py - Logging + WebLogHandler
└── 🎨 professional_ui_robust.py - Interfaz usuario

ACCESO REQUERIDO:
✅ Administrador Windows
✅ Hooks de sistema
✅ Procesos y archivos
✅ Memoria y red
✅ Registry Windows
```

### 🐳 **WEB SYSTEM (Dockerizado)**
```
Ubicación: Docker Containers (Aislado)
Responsabilidad: Centralización y Visualización

COMPONENTES:
├── 🌐 backend/ - API REST (FastAPI)
├── 📊 database/ - PostgreSQL + Redis
├── 🖥️ frontend/ - Dashboard React
├── 📈 analytics/ - Procesamiento estadísticas
└── 🔐 auth/ - Autenticación multiusuario

VENTAJAS DOCKER:
✅ Deployment independiente
✅ Escalabilidad cloud
✅ Backup automático
✅ Updates sin afectar antivirus
✅ Multi-tenant (múltiples antivirus)
```

## 🔄 **Comunicación Entre Sistemas**

### 📡 **Protocolo de Integración**
```python
# EN EL ANTIVIRUS (utils/logger.py)
class WebLogHandler(logging.Handler):
    def emit(self, record):
        log_data = {
            "timestamp": datetime.utcnow().isoformat(),
            "level": record.levelname,
            "message": record.getMessage(),
            "component": record.name,
            "details": getattr(record, 'extra_data', {})
        }
        
        # HTTP POST al contenedor web
        requests.post(
            "http://localhost:8000/api/logs",
            json=log_data,
            headers={"X-API-Key": "antivirus-system-key-2024"}
        )
```

### 🔗 **Flujo de Datos**
```
1. DETECCIÓN
   Antivirus detecta amenaza → log interno
   
2. TRANSMISIÓN  
   WebLogHandler → HTTP POST → Docker API
   
3. PROCESAMIENTO
   FastAPI recibe → valida → guarda PostgreSQL
   
4. VISUALIZACIÓN
   Dashboard consulta API → muestra estadísticas
```

## 🎯 **Beneficios de esta Arquitectura**

### ⚡ **Performance**
- Antivirus: Máximo rendimiento nativo
- Web: Optimizado para múltiples usuarios

### 🔐 **Seguridad**
- Antivirus: Acceso completo sistema  
- Web: Aislado, solo datos necesarios

### 🚀 **Escalabilidad**
- 1 Antivirus → 1 Dashboard personal
- 100 Antivirus → 1 Dashboard centralizado empresa
- N Antivirus → M Dashboards por departamento

### 🛠️ **Mantenimiento**
- Update antivirus: No afecta dashboard
- Update dashboard: No afecta protección
- Deploy independiente de cada componente

## 📊 **Casos de Uso**

### 🏠 **Uso Personal**
```
PC Usuario → Antivirus Nativo → Web Local (Docker)
```

### 🏢 **Empresa Pequeña**  
```
10 PCs → 10 Antivirus → 1 Servidor Web (Docker)
```

### 🏭 **Enterprise**
```
1000 PCs → 1000 Antivirus → Kubernetes Cluster
                         ↓
                    Load Balancer
                         ↓
              Multiple FastAPI instances
                         ↓ 
              PostgreSQL Cluster + Redis
```

## 🔮 **Evolución Futura**

### Fase 1 (Actual)
- ✅ Antivirus standalone
- ✅ Web system local

### Fase 2 (Sprint 2-3)  
- 🔄 Integración WebLogHandler
- 🖥️ Dashboard funcional

### Fase 3 (Sprint 4-5)
- ☁️ Cloud deployment  
- 📊 Multi-tenant support
- 🚨 Alertas automáticas

Esta arquitectura híbrida nos da **lo mejor de ambos mundos**: 
- **Performance nativo** para la protección
- **Flexibilidad cloud** para la gestión