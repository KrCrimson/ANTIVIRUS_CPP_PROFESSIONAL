# 🛡️ Sistema de Monitoreo Web para Antivirus

Sistema centralizado de monitoreo y visualización de logs para el antivirus unificado. Permite supervisar múltiples PCs desde un dashboard web centralizado.

## 📋 Características

- **📊 Dashboard Web Interactivo**: Métricas en tiempo real, gráficos y estadísticas
- **🖥️ Monitoreo Multi-PC**: Supervisar múltiples equipos desde un panel centralizado  
- **📈 Visualización Avanzada**: Gráficos de actividad, distribución de logs y tendencias
- **🔍 Búsqueda y Filtrado**: Filtros avanzados por PC, nivel, tiempo y contenido
- **📁 Exportación de Datos**: Exportar logs en formato CSV para análisis
- **🔐 Autenticación Segura**: Sistema de login con roles y protección anti-brute force
- **⚡ Tiempo Real**: Actualización automática de métricas y logs
- **📱 Responsive**: Compatible con dispositivos móviles y tablets

## 🚀 Instalación Rápida

### Opción 1: Configuración Automática (Recomendada)

```bash
# 1. Ejecutar configurador automático
python setup_web_monitoring.py

# 2. Iniciar servidor de monitoreo
start_monitor_server.bat

# 3. Configurar clientes en cada PC
start_monitor_client.bat
```

### Opción 2: Instalación Manual

```bash
# 1. Instalar dependencias
pip install -r requirements_web_monitor.txt

# 2. Configurar servidor
python web_monitor_server.py

# 3. Configurar cliente (en cada PC)
python -c "from utils.log_sender import LogSender; sender = LogSender('http://servidor:8000'); sender.start()"
```

### Opción 3: Demo Sin Dependencias

```bash
# Para ver una demostración sin instalar dependencias
python demo_web_monitor.py
```

## 📖 Guía de Uso

### 🖥️ Servidor de Monitoreo

El servidor centraliza todos los logs y proporciona el dashboard web.

**Iniciar servidor:**
```bash
python web_monitor_server.py
```

**Acceso al dashboard:**
- URL: `http://localhost:8000`
- Usuario: `admin` 
- Contraseña: `antivirus2025`

**Endpoints disponibles:**
- `/` - Dashboard principal
- `/pcs` - Gestión de PCs monitoreadas
- `/logs` - Visualización de logs
- `/api/docs` - Documentación de la API

### 💻 Cliente de Envío

Cada PC con antivirus debe ejecutar el cliente para enviar logs.

**Configuración básica:**
```python
from utils.log_sender import LogSender

# Crear cliente
sender = LogSender(
    server_url="http://servidor:8000",
    send_interval=30,  # Enviar cada 30 segundos
    batch_size=100     # Máximo 100 logs por envío
)

# Iniciar envío automático
sender.start()
```

**Integración con el antivirus:**
```python
from utils.logger import setup_web_monitoring

# En el archivo principal del antivirus
setup_web_monitoring("http://servidor:8000")
```

## 📊 Funcionalidades del Dashboard

### Vista Principal
- **Métricas Clave**: Total de logs, PCs activas, errores críticos
- **Gráfico de Actividad**: Logs por hora en las últimas 24 horas
- **Distribución por Nivel**: Porcentaje de cada tipo de log
- **PCs Registradas**: Estado y última actividad de cada equipo
- **Logs Recientes**: Últimos eventos registrados

### Gestión de PCs
- **Lista Completa**: Todas las PCs registradas con detalles técnicos
- **Estados de Conexión**: Online, reciente, offline
- **Estadísticas por PC**: Número de logs, actividad, errores
- **Exportación**: Descargar lista de PCs en CSV

### Visualización de Logs
- **Filtros Avanzados**: Por PC, nivel, fecha, contenido
- **Búsqueda en Tiempo Real**: Buscar texto en mensajes
- **Paginación**: Navegación eficiente por miles de logs
- **Detalles Completos**: Ver log raw y metadata
- **Exportación**: Descargar logs filtrados en CSV

## ⚙️ Configuración Avanzada

### Archivo de Configuración del Servidor

`web_monitor_config.json`:
```json
{
  "server": {
    "host": "0.0.0.0",
    "port": 8000,
    "admin_username": "admin",
    "admin_password": "mi_password_seguro",
    "database_path": "web_monitor.db"
  }
}
```

### Configuración del Cliente

`client_monitor_config.json`:
```json
{
  "server_url": "http://192.168.1.100:8000",
  "send_interval": 30,
  "batch_size": 100,
  "max_retries": 3
}
```

### Variables de Entorno

```bash
# Configuración del servidor
export MONITOR_HOST="0.0.0.0"
export MONITOR_PORT="8000"
export ADMIN_USER="admin"
export ADMIN_PASS="password_seguro"

# Configuración del cliente  
export MONITOR_SERVER="http://servidor:8000"
export SEND_INTERVAL="30"
```

## 🔐 Seguridad

### Autenticación
- **Login básico HTTP**: Usuario y contraseña
- **Tokens JWT**: Para sesiones seguras (si están disponibles las dependencias)
- **Roles de usuario**: Admin y viewer
- **Protección anti-brute force**: Bloqueo temporal por IP

### Mejores Prácticas
1. **Cambiar credenciales por defecto** antes del despliegue
2. **Usar HTTPS** en producción
3. **Configurar firewall** para limitar acceso al puerto 8000
4. **Actualizar contraseñas** periódicamente
5. **Revisar logs de acceso** regularmente

### Configuración Segura para Producción

```python
# En web_monitor_server.py, modificar:
ADMIN_USERNAME = "mi_admin_seguro"
ADMIN_PASSWORD = "password_complejo_123!"

# Habilitar HTTPS
REQUIRE_HTTPS = True
ALLOWED_IPS = ["192.168.1.0/24"]  # Solo red interna
```

## 📁 Estructura del Proyecto

```
UNIFIED_ANTIVIRUS/
├── web_monitor_server.py      # Servidor web principal
├── web_security.py           # Sistema de autenticación
├── demo_web_monitor.py       # Demo sin dependencias
├── setup_web_monitoring.py   # Configurador automático
├── utils/
│   └── log_sender.py         # Cliente de envío de logs
├── web_templates/            # Plantillas HTML
│   ├── base.html            # Template base
│   ├── dashboard.html       # Dashboard principal  
│   ├── pcs.html            # Gestión de PCs
│   └── logs.html           # Visualización de logs
├── web_static/              # Archivos CSS/JS estáticos
├── requirements_web_monitor.txt  # Dependencias Python
└── *.bat                    # Scripts de inicio Windows
```

## 🛠️ Desarrollo y Personalización

### Agregar Nuevas Métricas

```python
# En web_monitor_server.py, en get_metrics()
def get_custom_metrics():
    # Añadir nuevos cálculos
    cursor.execute('SELECT COUNT(*) FROM logs WHERE level="CRITICAL" AND timestamp > datetime("now", "-1 hour")')
    critical_last_hour = cursor.fetchone()[0]
    
    return {"critical_last_hour": critical_last_hour}
```

### Personalizar Dashboard

```html
<!-- En web_templates/dashboard.html -->
<div class="col-md-3">
    <div class="card metric-card">
        <div class="card-body text-center">
            <i class="fas fa-exclamation fa-3x mb-3"></i>
            <h3>{{ custom_metric }}</h3>
            <p class="mb-0">Mi Métrica</p>
        </div>
    </div>
</div>
```

### Agregar Nuevos Filtros

```python
# En web_monitor_server.py, modificar get_logs()
@app.get("/api/logs")
async def get_logs(
    pc_id: Optional[str] = None,
    level: Optional[str] = None,
    date_from: Optional[str] = None,  # Nuevo filtro
    date_to: Optional[str] = None,    # Nuevo filtro
    limit: int = 100,
    offset: int = 0
):
    # Implementar lógica de filtrado por fechas
```

## 🐛 Solución de Problemas

### Problemas Comunes

**1. Error "FastAPI no disponible"**
```bash
# Solución: Instalar dependencias
pip install -r requirements_web_monitor.txt
```

**2. Cliente no puede conectar al servidor**
```bash
# Verificar conectividad
curl http://servidor:8000/api/health

# Verificar firewall  
telnet servidor 8000
```

**3. Base de datos bloqueada**
```bash
# Solución: Cerrar todas las conexiones y reiniciar servidor
rm web_monitor.db.lock
python web_monitor_server.py
```

**4. Logs no aparecen en el dashboard**
```bash
# Verificar que el cliente esté enviando
python -c "from utils.log_sender import get_log_sender; print(get_log_sender().get_status())"

# Verificar logs del servidor
tail -f logs/unified_antivirus.log
```

### Logs de Depuración

```bash
# Habilitar logging detallado
export LOG_LEVEL=DEBUG
python web_monitor_server.py

# Ver logs del cliente
python -c "
from utils.log_sender import LogSender
import logging
logging.basicConfig(level=logging.DEBUG)
sender = LogSender('http://servidor:8000')
sender.send_manual_log('DEBUG', 'Test de conectividad')
"
```

### Validación de Configuración

```bash
# Verificar configuración del servidor
python -c "
import json
with open('web_monitor_config.json') as f:
    config = json.load(f)
    print('Configuración válida:', config)
"

# Verificar configuración del cliente  
python -c "
import json
with open('client_monitor_config.json') as f:
    config = json.load(f)
    print('Cliente configurado para:', config['server_url'])
"
```

## 📞 Soporte

Para problemas o preguntas:

1. **Revisar esta documentación** y la sección de solución de problemas
2. **Verificar logs** del sistema en `logs/unified_antivirus.log`
3. **Probar la demo** con `python demo_web_monitor.py`
4. **Validar configuración** usando los scripts de validación
5. **Consultar el código fuente** para entender el funcionamiento interno

## 🔄 Actualizaciones

Para actualizar el sistema:

```bash
# 1. Respaldar configuración actual
cp web_monitor_config.json web_monitor_config.json.bak
cp client_monitor_config.json client_monitor_config.json.bak

# 2. Actualizar archivos del sistema
git pull origin main

# 3. Reinstalar dependencias si es necesario  
pip install -r requirements_web_monitor.txt --upgrade

# 4. Reiniciar servicios
# Detener servidor y clientes, luego reiniciar
```

---

## 📋 Resumen de Comandos

| Comando | Descripción |
|---------|-------------|
| `python setup_web_monitoring.py` | Configuración automática completa |
| `python web_monitor_server.py` | Iniciar servidor de monitoreo |
| `python demo_web_monitor.py` | Demo sin dependencias |
| `start_monitor_server.bat` | Iniciar servidor (Windows) |
| `start_monitor_client.bat` | Iniciar cliente (Windows) |
| `http://localhost:8000` | Acceder al dashboard |
| `http://localhost:8000/docs` | Documentación de la API |

¡El sistema de monitoreo web está listo para supervisar tu antivirus de forma centralizada! 🛡️📊