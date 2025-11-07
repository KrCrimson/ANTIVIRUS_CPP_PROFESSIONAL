#!/usr/bin/env python3
"""
Sistema de Pruebas E2E para el Dashboard de Antivirus
Sprint 4: Pruebas completas del sistema web de logging
"""

import time
import requests
import json
import threading
from datetime import datetime, timedelta
from concurrent.futures import ThreadPoolExecutor, as_completed
import sys
import os

# Agregar el directorio raíz al path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from utils.logger import get_logger

class DashboardE2ETester:
    def __init__(self):
        self.api_base = "http://localhost:8000"
        self.frontend_base = "http://localhost:8080"
        self.api_key = "dashboard-client-key-2024"
        self.headers = {"X-API-Key": self.api_key}
        self.results = {}
        
    def print_banner(self, title):
        """Imprime un banner decorativo"""
        print(f"\n{'='*70}")
        print(f"🔧 {title}")
        print(f"{'='*70}")
        
    def test_api_connectivity(self):
        """Test 1: Conectividad básica de la API"""
        self.print_banner("TEST 1: CONECTIVIDAD API")
        
        try:
            # Test endpoint de logs
            response = requests.get(f"{self.api_base}/api/logs", headers=self.headers, timeout=5)
            logs_ok = response.status_code == 200
            
            # Test endpoint de estadísticas
            response = requests.get(f"{self.api_base}/api/stats", headers=self.headers, timeout=5)
            stats_ok = response.status_code == 200
            
            # Test documentación
            response = requests.get(f"{self.api_base}/docs", timeout=5)
            docs_ok = response.status_code == 200
            
            self.results['api_connectivity'] = {
                'logs_endpoint': logs_ok,
                'stats_endpoint': stats_ok,
                'documentation': docs_ok,
                'success': logs_ok and stats_ok and docs_ok
            }
            
            print(f"✅ Endpoint /api/logs: {'OK' if logs_ok else 'FAIL'}")
            print(f"✅ Endpoint /api/stats: {'OK' if stats_ok else 'FAIL'}")
            print(f"✅ Documentación: {'OK' if docs_ok else 'FAIL'}")
            
            return self.results['api_connectivity']['success']
            
        except Exception as e:
            print(f"❌ Error de conectividad: {e}")
            self.results['api_connectivity'] = {'success': False, 'error': str(e)}
            return False
    
    def test_frontend_accessibility(self):
        """Test 2: Accesibilidad del frontend"""
        self.print_banner("TEST 2: ACCESIBILIDAD FRONTEND")
        
        try:
            # Test página principal
            response = requests.get(f"{self.frontend_base}/index.html", timeout=10)
            index_ok = response.status_code == 200 and len(response.text) > 1000
            
            # Test archivos CSS
            response = requests.get(f"{self.frontend_base}/css/dashboard.css", timeout=5)
            css_ok = response.status_code == 200
            
            # Test archivos JS
            js_files = ['config.js', 'api.js', 'charts.js', 'dashboard.js', 'app.js']
            js_results = {}
            
            for js_file in js_files:
                response = requests.get(f"{self.frontend_base}/js/{js_file}", timeout=5)
                js_results[js_file] = response.status_code == 200
            
            all_js_ok = all(js_results.values())
            
            self.results['frontend_accessibility'] = {
                'index_html': index_ok,
                'css_files': css_ok,
                'js_files': js_results,
                'success': index_ok and css_ok and all_js_ok
            }
            
            print(f"✅ index.html: {'OK' if index_ok else 'FAIL'}")
            print(f"✅ CSS files: {'OK' if css_ok else 'FAIL'}")
            
            for js_file, ok in js_results.items():
                print(f"✅ {js_file}: {'OK' if ok else 'FAIL'}")
            
            return self.results['frontend_accessibility']['success']
            
        except Exception as e:
            print(f"❌ Error de accesibilidad: {e}")
            self.results['frontend_accessibility'] = {'success': False, 'error': str(e)}
            return False
    
    def test_data_flow(self):
        """Test 3: Flujo de datos desde antivirus hasta dashboard"""
        self.print_banner("TEST 3: FLUJO DE DATOS COMPLETO")
        
        try:
            # Obtener logs iniciales
            response = requests.get(f"{self.api_base}/api/logs", headers=self.headers)
            initial_logs = response.json()
            initial_count = initial_logs['total']
            
            print(f"📊 Logs iniciales: {initial_count}")
            
            # Generar logs de prueba usando el sistema del antivirus
            print("📤 Generando logs de prueba...")
            
            test_loggers = ['e2e_test', 'performance_test', 'integration_test']
            generated_logs = 0
            
            for logger_name in test_loggers:
                logger = get_logger(logger_name)
                
                # Generar diferentes tipos de logs
                logger.info(f"[E2E] Test de flujo completo - {datetime.now()}")
                logger.warning(f"[E2E] Advertencia de prueba - {logger_name}")
                logger.error(f"[E2E] Error controlado para testing - {logger_name}")
                generated_logs += 3
                
                time.sleep(0.5)  # Pequeña pausa entre loggers
            
            # Esperar que se procesen los logs
            print("⏳ Esperando procesamiento de logs...")
            time.sleep(3)
            
            # Verificar que los logs llegaron
            response = requests.get(f"{self.api_base}/api/logs", headers=self.headers)
            final_logs = response.json()
            final_count = final_logs['total']
            
            logs_received = final_count - initial_count
            success = logs_received >= generated_logs * 0.8  # 80% de éxito mínimo
            
            self.results['data_flow'] = {
                'initial_logs': initial_count,
                'generated_logs': generated_logs,
                'final_logs': final_count,
                'logs_received': logs_received,
                'success_rate': (logs_received / generated_logs) * 100 if generated_logs > 0 else 0,
                'success': success
            }
            
            print(f"📊 Logs generados: {generated_logs}")
            print(f"📊 Logs recibidos: {logs_received}")
            print(f"📊 Tasa de éxito: {self.results['data_flow']['success_rate']:.1f}%")
            
            return success
            
        except Exception as e:
            print(f"❌ Error en flujo de datos: {e}")
            self.results['data_flow'] = {'success': False, 'error': str(e)}
            return False
    
    def test_api_performance(self):
        """Test 4: Performance de la API"""
        self.print_banner("TEST 4: PERFORMANCE API")
        
        def make_request(endpoint):
            start_time = time.time()
            try:
                response = requests.get(f"{self.api_base}{endpoint}", headers=self.headers, timeout=10)
                end_time = time.time()
                return {
                    'success': response.status_code == 200,
                    'response_time': end_time - start_time,
                    'status_code': response.status_code
                }
            except Exception as e:
                return {
                    'success': False,
                    'response_time': None,
                    'error': str(e)
                }
        
        try:
            # Test endpoints múltiples veces
            endpoints = ['/api/logs', '/api/stats', '/api/logs?limit=5', '/api/logs?component=core']
            iterations = 10
            
            results_by_endpoint = {}
            
            for endpoint in endpoints:
                print(f"🔄 Testing {endpoint}...")
                
                with ThreadPoolExecutor(max_workers=5) as executor:
                    futures = [executor.submit(make_request, endpoint) for _ in range(iterations)]
                    endpoint_results = [future.result() for future in as_completed(futures)]
                
                # Calcular métricas
                successful_requests = [r for r in endpoint_results if r['success']]
                success_rate = len(successful_requests) / len(endpoint_results) * 100
                
                if successful_requests:
                    avg_response_time = sum(r['response_time'] for r in successful_requests) / len(successful_requests)
                    max_response_time = max(r['response_time'] for r in successful_requests)
                    min_response_time = min(r['response_time'] for r in successful_requests)
                else:
                    avg_response_time = max_response_time = min_response_time = None
                
                results_by_endpoint[endpoint] = {
                    'success_rate': success_rate,
                    'avg_response_time': avg_response_time,
                    'max_response_time': max_response_time,
                    'min_response_time': min_response_time,
                    'total_requests': iterations
                }
                
                print(f"  ✅ Tasa de éxito: {success_rate:.1f}%")
                if avg_response_time:
                    print(f"  ⏱️ Tiempo promedio: {avg_response_time*1000:.0f}ms")
                    print(f"  ⏱️ Tiempo máximo: {max_response_time*1000:.0f}ms")
            
            # Evaluación general
            overall_success = all(r['success_rate'] >= 95 for r in results_by_endpoint.values())
            avg_performance = all(r['avg_response_time'] < 2.0 for r in results_by_endpoint.values() if r['avg_response_time'])
            
            self.results['api_performance'] = {
                'endpoints': results_by_endpoint,
                'overall_success': overall_success,
                'performance_acceptable': avg_performance,
                'success': overall_success and avg_performance
            }
            
            return self.results['api_performance']['success']
            
        except Exception as e:
            print(f"❌ Error en test de performance: {e}")
            self.results['api_performance'] = {'success': False, 'error': str(e)}
            return False
    
    def test_filtering_and_pagination(self):
        """Test 5: Filtros y paginación"""
        self.print_banner("TEST 5: FILTROS Y PAGINACIÓN")
        
        try:
            # Test filtro por nivel
            response = requests.get(f"{self.api_base}/api/logs?level=ERROR", headers=self.headers)
            error_logs = response.json()
            
            # Verificar que todos los logs son ERROR
            error_filter_ok = all(log['level'] == 'ERROR' for log in error_logs['logs'])
            
            # Test filtro por componente
            response = requests.get(f"{self.api_base}/api/logs?component=core", headers=self.headers)
            core_logs = response.json()
            
            # Verificar que todos los logs son del componente core
            component_filter_ok = all(log['component'] == 'core' for log in core_logs['logs'])
            
            # Test paginación
            response = requests.get(f"{self.api_base}/api/logs?limit=5&page=1", headers=self.headers)
            page1 = response.json()
            
            response = requests.get(f"{self.api_base}/api/logs?limit=5&page=2", headers=self.headers)
            page2 = response.json()
            
            # Verificar paginación
            pagination_ok = (
                len(page1['logs']) <= 5 and 
                len(page2['logs']) <= 5 and 
                page1['page'] == 1 and 
                page2['page'] == 2
            )
            
            # Test rango de fechas
            yesterday = (datetime.now() - timedelta(days=1)).isoformat()
            tomorrow = (datetime.now() + timedelta(days=1)).isoformat()
            
            response = requests.get(
                f"{self.api_base}/api/logs?date_from={yesterday}&date_to={tomorrow}", 
                headers=self.headers
            )
            date_filter = response.json()
            date_filter_ok = response.status_code == 200
            
            self.results['filtering_pagination'] = {
                'error_filter': error_filter_ok,
                'component_filter': component_filter_ok,
                'pagination': pagination_ok,
                'date_filter': date_filter_ok,
                'success': error_filter_ok and component_filter_ok and pagination_ok and date_filter_ok
            }
            
            print(f"✅ Filtro por nivel (ERROR): {'OK' if error_filter_ok else 'FAIL'}")
            print(f"✅ Filtro por componente: {'OK' if component_filter_ok else 'FAIL'}")
            print(f"✅ Paginación: {'OK' if pagination_ok else 'FAIL'}")
            print(f"✅ Filtro por fechas: {'OK' if date_filter_ok else 'FAIL'}")
            
            return self.results['filtering_pagination']['success']
            
        except Exception as e:
            print(f"❌ Error en test de filtros: {e}")
            self.results['filtering_pagination'] = {'success': False, 'error': str(e)}
            return False
    
    def test_statistics_accuracy(self):
        """Test 6: Precisión de estadísticas"""
        self.print_banner("TEST 6: PRECISIÓN DE ESTADÍSTICAS")
        
        try:
            # Obtener estadísticas
            response = requests.get(f"{self.api_base}/api/stats", headers=self.headers)
            stats = response.json()
            
            # Obtener todos los logs para verificar
            response = requests.get(f"{self.api_base}/api/logs?limit=1000", headers=self.headers)
            all_logs = response.json()
            
            # Calcular estadísticas manualmente
            manual_stats = {
                'total_logs': len(all_logs['logs']),
                'by_level': {},
                'by_component': {}
            }
            
            for log in all_logs['logs']:
                level = log['level']
                component = log['component']
                
                manual_stats['by_level'][level] = manual_stats['by_level'].get(level, 0) + 1
                manual_stats['by_component'][component] = manual_stats['by_component'].get(component, 0) + 1
            
            # Comparar estadísticas
            total_match = stats['total_logs'] == manual_stats['total_logs']
            level_match = stats['logs_by_level'] == manual_stats['by_level']
            component_match = stats['logs_by_component'] == manual_stats['by_component']
            
            # Verificar que hay datos de timeline
            timeline_ok = 'logs_by_hour' in stats and len(stats['logs_by_hour']) > 0
            
            # Verificar top components
            top_components_ok = 'top_components' in stats and len(stats['top_components']) > 0
            
            self.results['statistics_accuracy'] = {
                'total_logs_match': total_match,
                'level_stats_match': level_match,
                'component_stats_match': component_match,
                'timeline_data': timeline_ok,
                'top_components_data': top_components_ok,
                'success': total_match and level_match and component_match and timeline_ok and top_components_ok
            }
            
            print(f"✅ Total de logs: {'OK' if total_match else 'FAIL'} ({stats['total_logs']} vs {manual_stats['total_logs']})")
            print(f"✅ Stats por nivel: {'OK' if level_match else 'FAIL'}")
            print(f"✅ Stats por componente: {'OK' if component_match else 'FAIL'}")
            print(f"✅ Datos de timeline: {'OK' if timeline_ok else 'FAIL'}")
            print(f"✅ Top components: {'OK' if top_components_ok else 'FAIL'}")
            
            return self.results['statistics_accuracy']['success']
            
        except Exception as e:
            print(f"❌ Error en test de estadísticas: {e}")
            self.results['statistics_accuracy'] = {'success': False, 'error': str(e)}
            return False
    
    def run_all_tests(self):
        """Ejecuta todos los tests E2E"""
        self.print_banner("INICIANDO PRUEBAS E2E DEL SISTEMA DE LOGGING WEB")
        
        start_time = time.time()
        
        tests = [
            ("Conectividad API", self.test_api_connectivity),
            ("Accesibilidad Frontend", self.test_frontend_accessibility),
            ("Flujo de Datos", self.test_data_flow),
            ("Performance API", self.test_api_performance),
            ("Filtros y Paginación", self.test_filtering_and_pagination),
            ("Precisión Estadísticas", self.test_statistics_accuracy)
        ]
        
        test_results = []
        
        for test_name, test_func in tests:
            print(f"\n🔄 Ejecutando: {test_name}")
            try:
                result = test_func()
                test_results.append((test_name, result))
                status = "✅ PASS" if result else "❌ FAIL"
                print(f"   {status}")
            except Exception as e:
                print(f"   ❌ ERROR: {e}")
                test_results.append((test_name, False))
        
        end_time = time.time()
        
        # Resumen final
        self.print_banner("RESUMEN DE PRUEBAS E2E")
        
        passed_tests = sum(1 for _, result in test_results if result)
        total_tests = len(test_results)
        success_rate = (passed_tests / total_tests) * 100
        
        for test_name, result in test_results:
            status = "✅ PASS" if result else "❌ FAIL"
            print(f"{status} {test_name}")
        
        print(f"\n📊 RESULTADOS:")
        print(f"   Tests ejecutados: {total_tests}")
        print(f"   Tests exitosos: {passed_tests}")
        print(f"   Tasa de éxito: {success_rate:.1f}%")
        print(f"   Tiempo total: {end_time - start_time:.1f}s")
        
        # Guardar resultados detallados
        self.results['summary'] = {
            'total_tests': total_tests,
            'passed_tests': passed_tests,
            'success_rate': success_rate,
            'execution_time': end_time - start_time,
            'overall_success': success_rate >= 80.0
        }
        
        if success_rate >= 80.0:
            print(f"\n🎉 ¡SISTEMA APROBADO! Tasa de éxito: {success_rate:.1f}%")
            return True
        else:
            print(f"\n⚠️ SISTEMA REQUIERE ATENCIÓN. Tasa de éxito: {success_rate:.1f}%")
            return False
    
    def save_results(self, filename="e2e_test_results.json"):
        """Guarda los resultados detallados en un archivo JSON"""
        try:
            results_with_metadata = {
                'timestamp': datetime.now().isoformat(),
                'test_configuration': {
                    'api_base': self.api_base,
                    'frontend_base': self.frontend_base,
                    'api_key': 'dashboard-client-key-2024'
                },
                'results': self.results
            }
            
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(results_with_metadata, f, indent=2, ensure_ascii=False)
            
            print(f"📄 Resultados guardados en: {filename}")
            
        except Exception as e:
            print(f"⚠️ No se pudieron guardar los resultados: {e}")

def main():
    """Función principal"""
    print("🚀 Iniciando Sistema de Pruebas E2E")
    print("Sprint 4: Pruebas completas del sistema web de logging")
    
    tester = DashboardE2ETester()
    
    try:
        success = tester.run_all_tests()
        tester.save_results()
        
        return 0 if success else 1
        
    except KeyboardInterrupt:
        print("\n⚠️ Pruebas interrumpidas por el usuario")
        return 1
    except Exception as e:
        print(f"\n❌ Error inesperado: {e}")
        return 1

if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)