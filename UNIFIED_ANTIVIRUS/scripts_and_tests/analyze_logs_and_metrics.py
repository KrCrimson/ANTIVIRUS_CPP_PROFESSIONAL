#!/usr/bin/env python3
"""
Script para analizar y documentar todos los logs generados por UNIFIED_ANTIVIRUS
Identifica patrones, tipos, métricas y KPIs disponibles
"""

import os
import json
import re
from datetime import datetime
from collections import defaultdict, Counter
import glob

def analyze_log_files():
    """Analiza todos los archivos de log para identificar patrones y tipos"""
    
    print("🔍 ANÁLISIS COMPLETO DE LOGS DEL ANTIVIRUS")
    print("=" * 50)
    
    logs_dir = "logs"
    if not os.path.exists(logs_dir):
        print("❌ Directorio de logs no encontrado")
        return
    
    # Análisis de archivos de log
    log_files = glob.glob(f"{logs_dir}/*.log") + glob.glob(f"{logs_dir}/*.jsonl")
    
    analysis = {
        "file_types": {},
        "log_levels": Counter(),
        "components": Counter(),
        "message_patterns": Counter(),
        "error_patterns": Counter(),
        "metrics_detected": [],
        "security_events": [],
        "performance_data": [],
        "total_entries": 0
    }
    
    for log_file in log_files:
        print(f"\n📄 Analizando: {os.path.basename(log_file)}")
        
        file_type = "structured" if log_file.endswith('.jsonl') else "text"
        analysis["file_types"][os.path.basename(log_file)] = file_type
        
        try:
            with open(log_file, 'r', encoding='utf-8') as f:
                if file_type == "structured":
                    analyze_structured_logs(f, analysis)
                else:
                    analyze_text_logs(f, analysis)
                    
        except Exception as e:
            print(f"   ⚠️ Error leyendo {log_file}: {e}")
    
    # Generar reporte
    generate_analysis_report(analysis)
    
    # Generar métricas recomendadas
    generate_metrics_recommendations(analysis)
    
    return analysis

def analyze_structured_logs(file_handle, analysis):
    """Analiza logs estructurados en formato JSON"""
    
    entries = 0
    for line in file_handle:
        line = line.strip()
        if not line:
            continue
            
        try:
            log_entry = json.loads(line)
            entries += 1
            analysis["total_entries"] += 1
            
            # Analizar nivel de log
            level = log_entry.get("level", "UNKNOWN")
            analysis["log_levels"][level] += 1
            
            # Analizar componente/logger
            logger = log_entry.get("logger", "unknown")
            analysis["components"][logger] += 1
            
            # Analizar mensaje
            message = log_entry.get("message", "")
            
            # Detectar patrones de seguridad
            if any(keyword in message.lower() for keyword in 
                   ["threat", "malware", "suspicious", "blocked", "quarantine", "virus", "keylogger"]):
                analysis["security_events"].append({
                    "timestamp": log_entry.get("timestamp"),
                    "level": level,
                    "logger": logger,
                    "message": message
                })
            
            # Detectar patrones de error
            if level in ["ERROR", "CRITICAL"]:
                analysis["error_patterns"][message[:100]] += 1
            
            # Detectar datos de rendimiento
            if any(keyword in message.lower() for keyword in 
                   ["cpu", "memory", "performance", "duration", "speed", "time"]):
                analysis["performance_data"].append({
                    "timestamp": log_entry.get("timestamp"),
                    "logger": logger,
                    "message": message
                })
            
            # Patrones de mensaje comunes
            message_pattern = extract_message_pattern(message)
            analysis["message_patterns"][message_pattern] += 1
            
        except json.JSONDecodeError:
            continue
    
    print(f"   ✅ {entries} entradas estructuradas procesadas")

def analyze_text_logs(file_handle, analysis):
    """Analiza logs en formato texto"""
    
    entries = 0
    for line in file_handle:
        line = line.strip()
        if not line:
            continue
            
        entries += 1
        analysis["total_entries"] += 1
        
        # Detectar nivel de log en texto
        level_match = re.search(r'\b(DEBUG|INFO|WARNING|ERROR|CRITICAL)\b', line)
        if level_match:
            analysis["log_levels"][level_match.group(1)] += 1
        
        # Detectar componente en texto
        component_match = re.search(r'\[([^\]]+)\]', line)
        if component_match:
            analysis["components"][component_match.group(1)] += 1
        
        # Detectar patrones de seguridad
        if any(keyword in line.lower() for keyword in 
               ["threat", "malware", "suspicious", "blocked", "quarantine", "virus", "keylogger"]):
            analysis["security_events"].append({
                "timestamp": extract_timestamp_from_text(line),
                "message": line
            })
    
    print(f"   ✅ {entries} líneas de texto procesadas")

def extract_message_pattern(message):
    """Extrae patrón de mensaje removiendo valores específicos"""
    
    # Remover timestamps
    pattern = re.sub(r'\d{4}-\d{2}-\d{2}[T ]\d{2}:\d{2}:\d{2}', '[TIMESTAMP]', message)
    
    # Remover números específicos
    pattern = re.sub(r'\b\d+\b', '[NUMBER]', pattern)
    
    # Remover rutas de archivo
    pattern = re.sub(r'[A-Za-z]:[\\\/][^\s]+', '[PATH]', pattern)
    
    # Remover IPs
    pattern = re.sub(r'\b\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\b', '[IP]', pattern)
    
    return pattern[:100]  # Limitar longitud

def extract_timestamp_from_text(line):
    """Extrae timestamp de una línea de texto"""
    
    timestamp_pattern = r'\d{4}-\d{2}-\d{2}[T ]\d{2}:\d{2}:\d{2}'
    match = re.search(timestamp_pattern, line)
    return match.group(0) if match else None

def generate_analysis_report(analysis):
    """Genera reporte de análisis"""
    
    print(f"\n📊 REPORTE DE ANÁLISIS")
    print("=" * 40)
    
    print(f"📈 Total de entradas de log: {analysis['total_entries']:,}")
    print(f"📁 Archivos analizados: {len(analysis['file_types'])}")
    
    print(f"\n🎯 NIVELES DE LOG:")
    for level, count in analysis["log_levels"].most_common():
        percentage = (count / analysis['total_entries']) * 100
        print(f"   {level}: {count:,} ({percentage:.1f}%)")
    
    print(f"\n🔧 COMPONENTES PRINCIPALES:")
    for component, count in analysis["components"].most_common(10):
        print(f"   {component}: {count:,} logs")
    
    print(f"\n🚨 EVENTOS DE SEGURIDAD DETECTADOS: {len(analysis['security_events'])}")
    print(f"⚡ DATOS DE RENDIMIENTO: {len(analysis['performance_data'])}")
    
    print(f"\n🔥 PATRONES DE ERROR MÁS COMUNES:")
    for pattern, count in analysis["error_patterns"].most_common(5):
        print(f"   {count}x: {pattern}")

def generate_metrics_recommendations(analysis):
    """Genera recomendaciones de métricas y KPIs"""
    
    print(f"\n🎯 MÉTRICAS Y KPIs RECOMENDADOS")
    print("=" * 40)
    
    metrics = {
        "seguridad": [
            "Amenazas detectadas por hora/día",
            "Archivos cuarentenados",
            "Intentos de conexión sospechosos bloqueados",
            "Procesos maliciosos terminados",
            "Falsos positivos identificados",
            "Tiempo de respuesta ante amenazas"
        ],
        "rendimiento": [
            "Uso de CPU promedio/máximo",
            "Uso de memoria promedio/máximo", 
            "Tiempo de escaneo promedio",
            "Archivos escaneados por minuto",
            "Latencia de respuesta del sistema",
            "Uptime del antivirus"
        ],
        "operacional": [
            "Logs generados por componente",
            "Errores por categoría",
            "Plugins activos/inactivos",
            "Configuraciones modificadas",
            "Actualizaciones de base de datos",
            "Conexiones de red monitoreadas"
        ],
        "business": [
            "Disponibilidad del sistema (%)",
            "MTTR (Mean Time To Response)",
            "MTBF (Mean Time Between Failures)",
            "Cobertura de protección (%)",
            "Eficacia de detección (%)",
            "Satisfacción del usuario"
        ]
    }
    
    for category, metric_list in metrics.items():
        print(f"\n📊 {category.upper()}:")
        for metric in metric_list:
            print(f"   • {metric}")
    
    # Generar dashboard layout recomendado
    generate_dashboard_layout()

def generate_dashboard_layout():
    """Genera layout recomendado para el dashboard"""
    
    print(f"\n🎨 LAYOUT RECOMENDADO PARA DASHBOARD")
    print("=" * 40)
    
    dashboard_sections = {
        "Estado General": [
            "🟢 Estado del sistema (Online/Offline)",
            "🛡️ Amenazas detectadas (24h)",
            "⚡ Rendimiento actual (CPU/Memoria)",
            "📊 Plugins activos"
        ],
        "Detección de Amenazas": [
            "🚨 Alertas críticas recientes",
            "📈 Gráfico de amenazas por tiempo",
            "🎯 Top tipos de amenazas",
            "🗂️ Archivos en cuarentena"
        ],
        "Rendimiento del Sistema": [
            "📊 Uso de recursos histórico",
            "⏱️ Tiempos de respuesta",
            "🔄 Estadísticas de escaneo",
            "💾 Uso de almacenamiento"
        ],
        "Logs y Auditoría": [
            "📝 Stream de logs en tiempo real",
            "🔍 Filtros por componente/nivel",
            "📊 Distribución de logs por tipo",
            "⚠️ Errores y advertencias"
        ],
        "Análisis de Red": [
            "🌐 Conexiones monitoreadas",
            "🚫 IPs bloqueadas",
            "📡 Tráfico sospechoso",
            "🔐 Puertos monitoreados"
        ]
    }
    
    for section, items in dashboard_sections.items():
        print(f"\n📋 {section}:")
        for item in items:
            print(f"   {item}")

def create_web_logging_config():
    """Crea archivo de configuración optimizado para web logging"""
    
    config = {
        "web_logging": {
            "enabled": True,
            "api_url": "https://unified-antivirus-csitvest3-sebastians-projects-487d2baa.vercel.app/api",
            "api_key": "unified-antivirus-api-key-2024",
            "buffer_size": 1000,
            "batch_size": 50,
            "flush_interval": 10.0,
            "max_retries": 5,
            "timeout": 15.0,
            "connection_test_interval": 120.0,
            "fallback_file": "logs/web_fallback.log",
            "fallback_enabled": True,
            "level": "INFO",
            "compress_logs": True,
            "include_system_info": True,
            "include_performance_metrics": True,
            "include_security_events": True,
            "rate_limit_per_minute": 2000,
            "verify_ssl": False,  # False porque Vercel tiene problemas con cert
            "metadata": {
                "client_version": "2.0.0",
                "environment": "production",
                "hostname_reporting": True,
                "ip_reporting": True
            },
            "filters": {
                "exclude_patterns": [
                    ".*test.*",
                    ".*debug.*"
                ],
                "include_only_levels": ["INFO", "WARNING", "ERROR", "CRITICAL"],
                "priority_components": [
                    "behavior_detector",
                    "ml_detector", 
                    "network_detector",
                    "engine",
                    "plugin_manager"
                ]
            }
        }
    }
    
    config_file = "config/web_logging_optimized.json"
    with open(config_file, 'w', encoding='utf-8') as f:
        json.dump(config, f, indent=2, ensure_ascii=False)
    
    print(f"\n✅ Configuración optimizada guardada en: {config_file}")
    return config

if __name__ == "__main__":
    # Cambiar al directorio del antivirus
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    
    # Ejecutar análisis completo
    analysis_result = analyze_log_files()
    
    # Crear configuración optimizada
    optimized_config = create_web_logging_config()
    
    print(f"\n🎉 ANÁLISIS COMPLETADO")
    print("=" * 30)
    print("✅ Logs analizados y categorizados")
    print("✅ Métricas identificadas")
    print("✅ Dashboard layout diseñado")
    print("✅ Configuración web optimizada creada")
    print(f"\n📋 SIGUIENTE PASO: Habilitar web_logging en la configuración del antivirus")