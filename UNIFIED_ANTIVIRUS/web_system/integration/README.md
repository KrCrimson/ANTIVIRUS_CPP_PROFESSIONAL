# 🔌 Integration - Integración con Sistema Antivirus
## Sprint 2: Conectar Logger Existente con Backend Web

[![Status](https://img.shields.io/badge/Status-Sprint%202%20Pendiente-yellow)](../README.md)
[![Priority](https://img.shields.io/badge/Priority-SIGUIENTE-red)](../README.md)

### 🎯 **Objetivo del Sprint 2**

Modificar el sistema de logging actual del antivirus (`utils/logger.py`) para que envíe automáticamente todos los logs al servidor web backend, manteniendo compatibilidad con archivos locales como fallback.

### 📋 **Tareas Principales**

1. **🔧 WebLogHandler Personalizado**
   - Crear handler HTTP para envío de logs
   - Integración con logger existente
   - Configuración vía JSON

2. **💾 Buffer Local Inteligente**
   - SQLite local para logs offline
   - Persistencia durante desconexiones
   - Envío automático al reconectar

3. **🔄 Sistema de Reconexión**
   - Exponential backoff para reintentos
   - Detección automática de servidor disponible
   - Logs de diagnóstico de conectividad

4. **⚙️ Configuración Extendida**
   - Opciones web en `config/logging_config.json`
   - Variables de entorno
   - Configuración dinámica sin restart

### 📁 **Archivos a Crear**

- `web_log_handler.py` - Handler HTTP personalizado
- `buffer_manager.py` - Gestión de buffer local
- `reconnection_manager.py` - Lógica de reconexión
- `config_extension.json` - Configuración extendida
- `tests/` - Tests de integración

### 🚀 **Resultado Esperado**

Al completar este sprint:
- ✅ Todos los logs del antivirus se envían automáticamente al servidor web
- ✅ Sistema funciona offline con buffer local
- ✅ Reconexión automática sin pérdida de logs
- ✅ Configuración flexible y dinámica

---

**⏳ Este sprint será desarrollado después de completar el Sprint 1 (Backend).**