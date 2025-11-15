# 🧪 Scripts and Tests Directory

Esta carpeta contiene scripts de desarrollo, pruebas y archivos temporales del proyecto.

## 📋 Contenido

### 🔬 Scripts de Prueba (Tests)
- `test_*.py` - Scripts de testing de diferentes componentes
- `test_complete_system_integration.py` - Test de integración completa del sistema
- `test_launcher_web_integration.py` - Test de integración web logging
- `test_web_logging*.py` - Tests específicos del sistema de logging web

### 🛠️ Scripts de Desarrollo
- `analyze_logs_and_metrics.py` - Análisis comprehensivo de logs existentes
- `integration_example.py` - Ejemplos de integración entre componentes
- `simple_*.py` - Scripts simples para pruebas rápidas
- `start_monitor_client.py` - Cliente de monitoreo para testing

### 📚 Documentación de Desarrollo
- `BACKEND_DEPLOYMENT_SUCCESS.md` - Log del despliegue exitoso del backend
- `BACKEND_STATUS_FINAL.md` - Estado final del backend web
- `SISTEMA_WEB_COMPLETADO.md` - Documentación del sistema web completado
- `ARCHITECTURE_HYBRID.md` - Documentación de arquitectura híbrida

## 🎯 Propósito

Estos archivos fueron utilizados durante el desarrollo e integración del sistema:

1. **Testing**: Validación de funcionalidades específicas
2. **Debugging**: Diagnóstico de problemas durante desarrollo  
3. **Integration**: Pruebas de conectividad entre componentes
4. **Metrics**: Análisis de rendimiento y logs del sistema
5. **Documentation**: Estados temporales del proyecto

## ⚠️ Uso

- Estos scripts están archivados y pueden no reflejar el estado actual del sistema
- Algunos pueden requerir dependencias específicas o configuraciones
- Úsalos como referencia para debugging o desarrollo futuro
- No son parte del sistema de producción

## 🗂️ Organización

```
scripts_and_tests/
├── test_*.py                    # Scripts de testing
├── analyze_logs_and_metrics.py  # Análisis de logs
├── integration_example.py       # Ejemplos de integración
├── simple_*.py                  # Scripts auxiliares
└── *.md                        # Documentación temporal
```

---
✅ **Nota**: El sistema principal está en los archivos del directorio raíz (`launcher.py`, carpetas `core/`, `plugins/`, etc.)