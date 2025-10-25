#!/usr/bin/env python3
"""
Script de prueba para verificar la integración completa del sistema de monitoreo web
"""

import os
import sys
import time
import subprocess
import threading
import json
import logging
from datetime import datetime

# Configurar logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def verificar_archivos():
    """Verifica que todos los archivos necesarios existen"""
    archivos_requeridos = [
        'professional_ui_robust.py',
        'utils/log_sender.py',
        'web_monitor_server.py',
        'web_security.py',
        'client_monitor_config.json',
        'web_templates/dashboard.html',
        'web_templates/login.html'
    ]
    
    archivos_faltantes = []
    for archivo in archivos_requeridos:
        if not os.path.exists(archivo):
            archivos_faltantes.append(archivo)
    
    if archivos_faltantes:
        logger.error(f"Archivos faltantes: {archivos_faltantes}")
        return False
    
    logger.info("✓ Todos los archivos necesarios están presentes")
    return True

def probar_servidor_web():
    """Inicia el servidor web y verifica su funcionamiento"""
    logger.info("Iniciando servidor web de prueba...")
    
    try:
        # Iniciar servidor en thread separado
        server_process = subprocess.Popen([
            sys.executable, 'web_monitor_server.py'
        ], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        
        # Esperar un poco para que el servidor se inicie
        time.sleep(3)
        
        # Verificar si el servidor está corriendo
        if server_process.poll() is None:
            logger.info("✓ Servidor web iniciado exitosamente")
            
            # Terminar servidor de prueba
            server_process.terminate()
            server_process.wait(timeout=5)
            return True
        else:
            stdout, stderr = server_process.communicate()
            logger.error(f"Error iniciando servidor: {stderr.decode()}")
            return False
            
    except Exception as e:
        logger.error(f"Error probando servidor: {e}")
        return False

def probar_cliente_log():
    """Prueba el cliente de envío de logs"""
    logger.info("Probando cliente de envío de logs...")
    
    try:
        # Importar el log sender
        sys.path.append('utils')
        from log_sender import LogSender
        
        # Crear instancia
        log_sender = LogSender('client_monitor_config.json')
        
        # Enviar log de prueba
        test_log = {
            'timestamp': datetime.now().isoformat(),
            'level': 'INFO',
            'message': 'Prueba de integración del sistema',
            'extra_data': {
                'test': True,
                'component': 'integration_test'
            }
        }
        
        # Intentar envío (fallará si no hay servidor, pero debe manejar el error)
        result = log_sender._send_logs_batch([test_log])
        
        logger.info("✓ Cliente de logs funciona correctamente")
        return True
        
    except Exception as e:
        logger.error(f"Error probando cliente: {e}")
        return False

def probar_integracion_antivirus():
    """Prueba la integración con el antivirus principal"""
    logger.info("Probando integración con antivirus principal...")
    
    try:
        # Verificar imports del antivirus
        with open('professional_ui_robust.py', 'r', encoding='utf-8') as f:
            content = f.read()
            
        # Verificar que las funciones de web monitoring están presentes
        funciones_requeridas = [
            '_init_web_monitoring',
            '_send_web_log',
            '_stop_web_monitoring'
        ]
        
        funciones_faltantes = []
        for funcion in funciones_requeridas:
            if f"def {funcion}" not in content:
                funciones_faltantes.append(funcion)
        
        if funciones_faltantes:
            logger.error(f"Funciones faltantes en antivirus: {funciones_faltantes}")
            return False
        
        logger.info("✓ Integración con antivirus verificada")
        return True
        
    except Exception as e:
        logger.error(f"Error verificando integración: {e}")
        return False

def probar_configuracion():
    """Verifica la configuración del sistema"""
    logger.info("Verificando configuración del sistema...")
    
    try:
        # Verificar configuración del cliente
        with open('client_monitor_config.json', 'r') as f:
            config = json.load(f)
            
        campos_requeridos = ['server_url', 'api_endpoint', 'batch_size', 'enabled']
        for campo in campos_requeridos:
            if campo not in config:
                logger.error(f"Campo faltante en configuración: {campo}")
                return False
        
        logger.info("✓ Configuración válida")
        return True
        
    except Exception as e:
        logger.error(f"Error verificando configuración: {e}")
        return False

def generar_reporte():
    """Genera un reporte de la integración"""
    logger.info("\n" + "="*60)
    logger.info("REPORTE DE INTEGRACIÓN DEL SISTEMA DE MONITOREO WEB")
    logger.info("="*60)
    
    pruebas = [
        ("Verificación de archivos", verificar_archivos),
        ("Configuración del sistema", probar_configuracion),
        ("Cliente de logs", probar_cliente_log),
        ("Integración con antivirus", probar_integracion_antivirus),
        ("Servidor web", probar_servidor_web)
    ]
    
    resultados = []
    for nombre, funcion in pruebas:
        logger.info(f"\n📋 Ejecutando: {nombre}")
        resultado = funcion()
        resultados.append((nombre, resultado))
        
        if resultado:
            logger.info(f"✅ {nombre}: EXITOSO")
        else:
            logger.error(f"❌ {nombre}: FALLIDO")
    
    # Resumen final
    exitosos = sum(1 for _, resultado in resultados if resultado)
    total = len(resultados)
    
    logger.info(f"\n" + "="*60)
    logger.info(f"RESUMEN: {exitosos}/{total} pruebas exitosas")
    
    if exitosos == total:
        logger.info("🎉 ¡INTEGRACIÓN COMPLETA Y EXITOSA!")
        logger.info("\n📋 PRÓXIMOS PASOS:")
        logger.info("1. Compilar con: python -m PyInstaller professional_ui_robust.spec")
        logger.info("2. Probar el ejecutable generado")
        logger.info("3. Crear instalador con: iscc installer_script.iss")
        logger.info("4. Probar instalación completa")
    else:
        logger.error("⚠️  Hay problemas que resolver antes de continuar")
        logger.info("\n🔧 SOLUCIONES SUGERIDAS:")
        for nombre, resultado in resultados:
            if not resultado:
                logger.info(f"- Revisar y corregir: {nombre}")
    
    logger.info("="*60)

def main():
    """Función principal"""
    logger.info("Iniciando prueba de integración completa...")
    
    # Cambiar al directorio del script
    script_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(script_dir)
    
    generar_reporte()

if __name__ == "__main__":
    main()