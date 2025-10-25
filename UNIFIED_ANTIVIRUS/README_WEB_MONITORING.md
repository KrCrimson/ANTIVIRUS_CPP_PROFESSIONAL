# Sistema de Monitoreo Web para Antivirus

## 📋 Descripción

Este sistema permite el monitoreo centralizado de logs del antivirus unificado a través de una interfaz web. Los logs de cada PC son enviados automáticamente a un servidor central donde se pueden visualizar métricas, estadísticas y análisis en tiempo real.

## 🏗️ Arquitectura

```
┌─────────────────┐    HTTP POST     ┌─────────────────────┐
│   PC Cliente    │ ─────────────────▶│  Servidor Central  │
│   (Antivirus)   │   (Logs JSON)     │   (Web Monitor)     │
│                 │                   │                     │
│ • log_sender.py │                   │ • FastAPI Server    │
│ • Auto-envío    │                   │ • SQLite Database   │
│ • Batch logs    │                   │ • Web Dashboard     │
└─────────────────┘                   └─────────────────────┘
                                               │
                                               ▼
                                      ┌─────────────────────┐
                                      │   Administrador     │
                                      │                     │
                                      │ • Dashboard Web     │
                                      │ • Métricas tiempo   │
                                      │   real              │
                                      │ • Gestión PCs       │
                                      └─────────────────────┘
```

## ⚡ Características Principales

### 🖥️ Servidor Central
- **API REST** con FastAPI para recibir logs
- **Dashboard web** responsive con métricas en tiempo real
- **Base de datos SQLite** para almacenamiento eficiente
- **Autenticación segura** con JWT y bcrypt
- **Visualización de datos** con gráficos interactivos
- **Gestión de PCs** registradas
- **Exportación de datos** a CSV
- **Auto-refresh** de la interfaz

### 💻 Cliente (PC con Antivirus)
- **Envío automático** de logs en segundo plano
- **Envío por lotes** para optimizar red
- **Retry automático** si falla el envío
- **Identificación única** de cada PC
- **Parsing inteligente** de diferentes formatos de log
- **Integración transparente** con el sistema de logging existente

## 🚀 Instalación Rápida

### 1. Configuración Automática
```bash
# Ejecutar el configurador automático
python setup_web_monitoring.py

# O con parámetros específicos
python setup_web_monitoring.py --mode server  # Solo servidor
python setup_web_monitoring.py --mode client  # Solo cliente
```

### 2. Instalación Manual

#### Servidor Central
```bash
# Instalar dependencias
pip install -r requirements_web_monitor.txt

# Iniciar servidor
python web_monitor_server.py
```

#### Cliente (PC con Antivirus)
```bash
# Instalar requests si no está disponible
pip install requests

# Integrar en el código del antivirus
from utils.logger import setup_web_monitoring
setup_web_monitoring("http://servidor:8000")
```

## 🔧 Configuración

### Configuración del Servidor (`web_monitor_config.json`)
```json
{
  "server": {
    "host": "0.0.0.0",
    "port": 8000,
    "admin_username": "admin",
    "admin_password": "tu_password_seguro",
    "database_path": "web_monitor.db"
  }
}
```

### Configuración del Cliente (`client_monitor_config.json`)
```json
{
  "server_url": "http://tu-servidor:8000",
  "send_interval": 30,
  "batch_size": 100,
  "max_retries": 3
}
```

## 💡 Uso

### Iniciar el Servidor
```bash
# Opción 1: Script automático (Windows)
start_monitor_server.bat

# Opción 2: Comando directo
python web_monitor_server.py
```

Acceder al dashboard: `http://localhost:8000`

### Configurar Clientes
```bash
# Opción 1: Script automático (Windows)
start_monitor_client.bat

# Opción 2: Integración en código
python integration_example.py
```

### Integración con Antivirus Existente
```python
from utils.logger import setup_web_monitoring, get_logger

# Al inicio de tu aplicación
def init_antivirus():
    # Logger normal
    logger = get_logger("antivirus_main")
    
    # Configurar monitoreo web (opcional)
    try:
        sender = setup_web_monitoring(
            server_url="http://tu-servidor:8000",
            send_interval=30,
            batch_size=50
        )
        logger.info("✅ Monitoreo web configurado")
    except Exception as e:
        logger.warning(f"⚠️ Monitoreo web no disponible: {e}")
    
    return logger
```

## 📊 Dashboard Web

### Página Principal
- **Métricas principales**: Total logs, PCs activas, errores críticos
- **Gráfico de actividad**: Logs por hora en las últimas 24h
- **Distribución por niveles**: Gráfico circular de tipos de log
- **PCs recientes**: Estado de conexión de cada PC
- **Logs recientes**: Últimos logs recibidos

### Gestión de PCs
- **Lista completa** de PCs registradas
- **Estado de conexión** (Online, Reciente, Offline)
- **Información del sistema** (SO, IP, versión Python)
- **Estadísticas por PC** (total logs, última actividad)
- **Filtros y búsqueda**

### Visualización de Logs
- **Tabla paginada** con todos los logs
- **Filtros por PC, nivel, búsqueda**
- **Vista detallada** de cada log
- **Exportación a CSV**
- **Auto-refresh** configurable

## 🔒 Seguridad

### Autenticación
- **Login con usuario y contraseña**
- **Tokens JWT** para sesiones
- **Bloqueo por intentos fallidos**
- **Roles de usuario** (admin, viewer)

### Configuración de Seguridad
- Cambiar credenciales por defecto en producción
- Habilitar HTTPS para comunicaciones remotas
- Configurar firewall para proteger puerto del servidor
- Limitar IPs permitidas si es necesario

## 📁 Estructura de Archivos

```
UNIFIED_ANTIVIRUS/
├── web_monitor_server.py          # Servidor FastAPI
├── utils/
│   └── log_sender.py              # Cliente de envío de logs
├── web_templates/                 # Plantillas HTML
│   ├── base.html
│   ├── dashboard.html
│   ├── pcs.html
│   └── logs.html
├── web_security.py               # Módulo de seguridad
├── setup_web_monitoring.py       # Configurador automático
├── requirements_web_monitor.txt   # Dependencias
├── start_monitor_server.bat      # Script de inicio servidor
├── start_monitor_client.bat      # Script de inicio cliente
├── integration_example.py        # Ejemplo de integración
└── README_WEB_MONITORING.md       # Este archivo
```

## 🔧 API REST

### Endpoints Públicos
- `POST /api/recibir_logs` - Recibir logs desde clientes
- `GET /api/health` - Health check

### Endpoints Protegidos (requieren autenticación)
- `GET /api/metrics` - Métricas del sistema
- `GET /api/pcs` - Lista de PCs registradas  
- `GET /api/logs` - Logs con filtros opcionales
- `GET /` - Dashboard web
- `GET /pcs` - Página de gestión de PCs
- `GET /logs` - Página de visualización de logs

### Documentación Interactiva
Acceder a `http://localhost:8000/docs` para la documentación automática de la API.

## 🐛 Solución de Problemas

### El servidor no inicia
```bash
# Verificar dependencias
pip install -r requirements_web_monitor.txt

# Verificar puerto disponible
netstat -an | findstr :8000
```

### Los clientes no envían logs
- Verificar conectividad de red al servidor
- Revisar URL del servidor en configuración
- Verificar logs de error en el cliente
- Comprobar que el servicio log_sender esté iniciado

### Error de autenticación
- Verificar usuario y contraseña
- Comprobar que no esté bloqueada la IP
- Revisar configuración de seguridad

### Base de datos corrupta
```bash
# Eliminar y recrear base de datos
del web_monitor.db
python web_monitor_server.py
```

## 📈 Optimización

### Rendimiento del Servidor
- Ajustar `batch_size` en clientes según carga
- Configurar `send_interval` apropiado (30-300 segundos)
- Considerar PostgreSQL para grandes volúmenes

### Rendimiento de Red
- Usar compresión HTTP si está disponible
- Ajustar `max_retries` y timeouts
- Implementar balanceador de carga para múltiples servidores

## 🔄 Mantenimiento

### Limpieza Periódica
```sql
-- Eliminar logs antiguos (>30 días)
DELETE FROM logs WHERE received_at < datetime('now', '-30 days');

-- Vacuum de la base de datos
VACUUM;
```

### Backup de Datos
```bash
# Backup de base de datos
copy web_monitor.db web_monitor_backup_%date%.db

# Backup de configuraciones
copy *_config.json backup/
```

### Monitoreo del Sistema
- Revisar logs del servidor regularmente
- Monitorear uso de disco de la base de datos
- Verificar conectividad de clientes periódicamente

## 📞 Soporte

Para reportar problemas o sugerir mejoras:
1. Revisar los logs de error del servidor y cliente
2. Verificar la configuración de red y seguridad
3. Consultar la documentación de la API en `/docs`
4. Revisar los archivos de configuración

---

**¡El sistema de monitoreo web está listo para su uso!** 🎉