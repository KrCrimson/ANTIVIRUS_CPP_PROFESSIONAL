# Guía de Estudio UNIFIED_ANTIVIRUS

Esta guía te ayudará a estudiar el proyecto siguiendo el orden lógico de sus componentes principales. Recorre cada módulo para comprender la arquitectura, el flujo de datos y la lógica de negocio del antivirus.

---

## 1) CORE (Cerebro)
**Ubicación:** `core/`
- Motores de detección y consenso: `engine.py`, `consensus_engine.py`, `detector_engine.py`, `simple_engine.py`
- Gestión de plugins: `base_plugin.py`, `plugin_manager.py`, `plugin_registry.py`
- Comunicación interna: `event_bus.py`
- Monitoreo de recursos: `memory_monitor.py`, `resource_monitor.py`
- Interfaces base: `interfaces.py`
- Documentación técnica: `README.md`

---

## 2) CONFIG (Reglas y Configuración)
**Ubicación:** `config/`
- Configuraciones generales y específicas: `unified_config.toml`, `security_config.json`, `plugins_config.json`, `alerts_config.json`, `ml_config.json`, `ui_config.json`, `ui_settings.json`, `safe_profiles.json`, `whitelist.json`
- Validación de configuración: `config_validator.py`
- Configuración de logs: `logging_config.json`
- Documentación de configuración: `README_CONFIGURACION.md`, `README.md`, `GUIA_USUARIO_CONFIGURACION.md`

---

## 3) PLUGINS
**Ubicación:** `plugins/`
- Ejemplo de plugin: `upgrade_intelligence.py`
- Subcarpetas: `detectors/`, `handlers/`, `monitors/`, `shared/`, `backup_configs/`
- Documentación: `README.md`

---

## 4) MODELS (Estudiar los JSON)
**Ubicación:** `models/`
- Modelos ML: archivos `.onnx`
- Metadatos y clases: `label_classes.json`, `onnx_metadata_large_20250918_112840.json`
- Documentación: `README.md`

---

## 5) TEST
**Ubicación:** `tests/`
- Pruebas unitarias y de integración: subcarpetas `iast_tests/`, `integration/`, `tdd_01_api_hooking_detection/`, etc.
- Documentación de testing y TDD: `README.md`, `GUIA_IMPLEMENTACION_TDD.md`

---

## 6) MDSD
**Ubicación:** `mdsd/`
- Scripts y motores de workflow: `mdsd_poc.py`, `simple_generator.py`, `workflow_engine.py`
- Documentación: `README.md`
- Subcarpetas: `configs/`, `templates/`

---

> Consulta los README y la documentación específica de cada carpeta para profundizar en los detalles técnicos.