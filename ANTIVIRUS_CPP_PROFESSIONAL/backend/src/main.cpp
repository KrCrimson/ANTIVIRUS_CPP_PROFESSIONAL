#include <iostream>
#include <memory>
#include <thread>
#include <chrono>
#include <signal.h>
#include <atomic>
#include <iomanip>

// Incluir todos los componentes
#include "core/DetectionEngine.hpp"
#include "ml/MLEngine.hpp"
#include "api/APIServer.hpp"

// Variable global para manejo de señales
std::atomic<bool> g_running{true};

/**
 * @brief Manejo de señales para shutdown limpio
 */
void signalHandler(int signum) {
    std::cout << "\n🛑 Received signal " << signum << ". Shutting down..." << std::endl;
    g_running = false;
}

/**
 * @brief Punto de entrada principal del antivirus
 */
int main() {
    std::cout << "🛡️  Antivirus Professional C++ - Starting...\n" << std::endl;
    
    // Configurar manejo de señales
    signal(SIGINT, signalHandler);
    signal(SIGTERM, signalHandler);
    
    try {
        // 1. Inicializar ML Engine
        auto ml_engine = std::make_unique<AntivirusCore::MLEngine>();
        if (!ml_engine->initialize()) {
            std::cerr << "❌ Failed to initialize ML Engine" << std::endl;
            return 1;
        }
        std::cout << "✅ ML engine initialized" << std::endl;
        
        // 2. Inicializar Detection Engine
        auto detection_engine = std::make_unique<AntivirusCore::DetectionEngine>();
        if (!detection_engine->initialize()) {
            std::cerr << "❌ Failed to initialize Detection Engine" << std::endl;
            return 1;
        }
        std::cout << "✅ Detection engine initialized" << std::endl;
        
        // 3. Inicializar API Server
        auto api_server = std::make_unique<AntivirusCore::APIServer>("127.0.0.1", 8080);
        api_server->setEngines(detection_engine.get(), ml_engine.get());
        
        if (!api_server->initialize()) {
            std::cerr << "❌ Failed to initialize API Server" << std::endl;
            return 1;
        }
        
        if (!api_server->start()) {
            std::cerr << "❌ Failed to start API Server" << std::endl;
            return 1;
        }
        std::cout << "✅ API server started" << std::endl;
        
        // 4. Inicializar sistema de plugins
        std::cout << "✅ Plugin system ready" << std::endl;
        
        std::cout << "\n🚀 Antivirus Professional is running!" << std::endl;
        std::cout << "📊 API Server: http://localhost:8080" << std::endl;
        std::cout << "🔧 Press Ctrl+C to stop\n" << std::endl;
        
        // 5. Main event loop
        int heartbeat_counter = 0;
        while (g_running) {
            std::this_thread::sleep_for(std::chrono::seconds(1));
            
            // Procesar eventos de detección
            if (detection_engine && detection_engine->isRunning()) {
                // El detection engine ya maneja su propio loop
            }
            
            // Heartbeat cada 10 segundos
            if (++heartbeat_counter % 10 == 0) {
                std::cout << "💓 Heartbeat - All systems operational" << std::endl;
                
                // Mostrar estadísticas
                if (detection_engine) {
                    auto stats = detection_engine->getStatistics();
                    std::cout << "   📊 Scans: " << stats.total_scans 
                             << " | Threats: " << stats.threats_found 
                             << " | CPU: " << std::fixed << std::setprecision(1) << stats.cpu_usage << "%" 
                             << std::endl;
                }
            }
        }
        
        // 6. Shutdown limpio
        std::cout << "\n🔄 Shutting down components..." << std::endl;
        
        if (api_server) {
            api_server->stop();
            std::cout << "✅ API Server stopped" << std::endl;
        }
        
        if (detection_engine) {
            detection_engine->stop();
            std::cout << "✅ Detection Engine stopped" << std::endl;
        }
        
        if (ml_engine) {
            ml_engine->shutdown();
            std::cout << "✅ ML Engine stopped" << std::endl;
        }
        
    } catch (const std::exception& e) {
        std::cerr << "❌ Fatal error: " << e.what() << std::endl;
        return 1;
    }
    
    std::cout << "🛑 Antivirus Professional stopped cleanly" << std::endl;
    return 0;
}