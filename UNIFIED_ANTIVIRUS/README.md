# Sistema Antivirus Profesional

![Version](https://img.shields.io/badge/version-1.1.0-blue.svg)
![Python](https://img.shields.io/badge/python-3.8+-green.svg)
![License](https://img.shields.io/badge/license-MIT-orange.svg)

## 📋 Descripción

Sistema antivirus profesional con capacidades de monitoreo en tiempo real, detección de amenazas y sistema de logging centralizado con identificación única de clientes.

## ✨ Características Principales

### 🛡️ Protección en Tiempo Real
- Escaneo de archivos en tiempo real
- Detección de malware y amenazas
- Cuarentena automática de archivos sospechosos
- Protección contra keyloggers

### 📊 Sistema de Logging Avanzado
- **Identificación única de clientes** - Cada instalación tiene un UUID único
- **Logging centralizado** - Envío de logs a backend en Vercel
- **Tracking de instancias** - Monitoreo de instancias activas/inactivas
- **Dashboard web** - Visualización de logs y estadísticas

### 🔌 Arquitectura de Plugins
- Sistema modular y extensible
- Plugins para diferentes tipos de análisis
- Fácil integración de nuevas funcionalidades

### 🖥️ Interfaz Gráfica
- UI moderna con DearPyGUI
- Monitoreo en tiempo real
- Visualización de amenazas
- Configuración intuitiva

## 🏗️ Arquitectura del Sistema

```
UNIFIED_ANTIVIRUS/
├── core/                      # Núcleo del antivirus
│   ├── scanner.py            # Motor de escaneo
│   ├── quarantine.py         # Sistema de cuarentena
│   └── threat_detector.py    # Detección de amenazas
│
├── plugins/                   # Plugins de análisis
│   ├── file_analyzer/        # Análisis de archivos
│   ├── network_monitor/      # Monitoreo de red
│   └── behavior_analyzer/    # Análisis de comportamiento
│
├── web_system/               # Sistema de logging web
│   ├── integration/          # Integración con backend
│   │   ├── client_identity.py    # ✨ Identificación única
│   │   └── web_log_handler.py    # Handler de logs
│   ├── backend/              # Backend FastAPI (local)
│   └── frontend/             # Dashboard web
│
├── web_backend/              # Backend para Vercel
│   ├── main.py              # API FastAPI simplificada
│   ├── vercel.json          # Configuración de Vercel
│   └── requirements.txt     # Dependencias
│
├── frontend/                 # Interfaz gráfica
│   ├── components/          # Componentes UI
│   └── views/               # Vistas de la aplicación
│
├── config/                   # Configuración
│   └── client_identity.json # UUID único (generado automáticamente)
│
└── installer_script.iss     # Script de instalación
```

## 🚀 Instalación

### Opción 1: Instalador (Recomendado)

1. Descarga el instalador `Antivirus_Instalador_v1.1.0.exe`
2. Ejecuta el instalador con permisos de administrador
3. Sigue las instrucciones del asistente
4. El antivirus se iniciará automáticamente

### Opción 2: Desde el Código Fuente

```bash
# Clonar el repositorio
git clone https://github.com/KrCrimson/ANTIVIRUS_CPP_PROFESSIONAL.git
cd UNIFIED_ANTIVIRUS

# Instalar dependencias
pip install -r requirements_web_monitor.txt

# Ejecutar el antivirus
python professional_ui_robust.py
```

## ⚙️ Configuración

### Configurar Conexión con Backend Vercel

Edita `client_monitor_config.json`:

```json
{
  "server_url": "https://tu-backend.vercel.app",
  "api_endpoint": "/api/logs",
  "api_key": "TU_API_KEY",
  "enabled": true
}
```

### Variables de Entorno

Para el backend en Vercel, configura:

```bash
API_KEY_MASTER=tu_api_key_secreta
DATABASE_URL=postgresql://... (opcional)
```

## 📖 Uso

### Iniciar el Antivirus

```bash
# Windows
C:\Program Files\AntivirusProfesional\professional_ui_robust.exe

# Desde código fuente
python professional_ui_robust.py
```

### Escanear Archivos

1. Abre la interfaz del antivirus
2. Selecciona "Escanear"
3. Elige archivos o carpetas
4. Revisa los resultados

### Ver Logs

```bash
# Logs locales
tail -f logs/antivirus.log

# Logs en Vercel
curl -H "X-API-Key: TU_KEY" https://tu-backend.vercel.app/api/logs
```

## 🔧 Desarrollo

### Estructura de Plugins

```python
from core.plugin_base import PluginBase

class MiPlugin(PluginBase):
    def __init__(self):
        super().__init__("mi_plugin", "1.0.0")
    
    def analyze(self, data):
        # Tu lógica aquí
        return resultado
```

### Agregar Nuevo Tipo de Log

```python
from web_system.integration.web_log_handler import WebLogHandler

logger = logging.getLogger("mi_componente")
logger.info("Mi mensaje", extra={
    "threat_type": "malware",
    "severity": "high"
})
```

## 🧪 Testing

```bash
# Tests unitarios
python -m pytest tests/

# Test de integración con Vercel
python test_web_logs.py

# Test del cliente de identificación
python tests/test_client_id_integration.py
```

## 📊 Monitoreo

### Dashboard Web

Accede al dashboard en: `http://localhost:8888/dashboard`

### Estadísticas

```bash
# Ver estadísticas del sistema
curl -H "X-API-Key: TU_KEY" https://tu-backend.vercel.app/api/stats
```

### Instancias Activas

```bash
# Ver todas las instancias
curl -H "X-API-Key: TU_KEY" https://tu-backend.vercel.app/api/instances
```

## 🔐 Seguridad

- ✅ Autenticación mediante API Key
- ✅ Identificación única por instalación
- ✅ Logs encriptados en tránsito (HTTPS)
- ✅ Cuarentena segura de archivos maliciosos
- ✅ Validación de datos en backend

## 📝 Changelog

### v1.1.0 (2025-11-28)
- ✨ **NUEVO**: Sistema de identificación única de clientes
- ✨ **NUEVO**: Backend optimizado para Vercel
- ✨ **NUEVO**: Tracking de instancias activas/inactivas
- 🔧 Mejoras en el sistema de logging
- 🔧 Optimización del instalador

### v1.0.0 (2025-11-15)
- 🎉 Lanzamiento inicial
- ✅ Sistema de escaneo en tiempo real
- ✅ Detección de amenazas
- ✅ Interfaz gráfica
- ✅ Sistema de plugins

## 🤝 Contribuir

1. Fork el proyecto
2. Crea una rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

## 📄 Licencia

Este proyecto está bajo la Licencia MIT. Ver `LICENSE` para más detalles.

## 👥 Autores

- **KrCrimson** - *Desarrollo Principal* - [@KrCrimson](https://github.com/KrCrimson)

## 🙏 Agradecimientos

- Comunidad de Python
- FastAPI Framework
- DearPyGUI
- Vercel Platform

## 📞 Soporte

- 📧 Email: soporte@antivirus.com
- 🐛 Issues: [GitHub Issues](https://github.com/KrCrimson/ANTIVIRUS_CPP_PROFESSIONAL/issues)
- 📖 Docs: [Documentación Completa](./docs/)

## 🔗 Enlaces Útiles

- [Guía de Configuración Vercel](./web_backend/README.md)
- [Documentación Técnica](./COMO_FUNCIONA_TECHNICAL_README.md)
- [Arquitectura del Sistema](./ARCHITECTURE_HYBRID.md)

---

**⚠️ Nota**: Este es un proyecto educativo. Para uso en producción, se recomienda realizar auditorías de seguridad adicionales.
