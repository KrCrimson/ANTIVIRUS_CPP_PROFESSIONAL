#pragma once

#include <string>
#include <memory>
#include <atomic>
#include <thread>
#include <mutex>
#include <map>
#include <functional>
#include <future>
#include "../core/Types.hpp"

// Forward declarations
namespace AntivirusCore {
    class DetectionEngine;
    class MLEngine;
}

namespace AntivirusCore {

/**
 * @brief Respuesta HTTP básica
 */
struct HTTPResponse {
    int status_code = 200;
    std::string content_type = "application/json";
    std::string body;
    std::map<std::string, std::string> headers;
};

/**
 * @brief Request HTTP básico
 */
struct HTTPRequest {
    std::string method;
    std::string path;
    std::string query_string;
    std::map<std::string, std::string> headers;
    std::string body;
};

/**
 * @brief Estado del sistema para API
 */
struct SystemStatus {
    bool protection_enabled = true;
    std::string status = "RUNNING";
    uint64_t threats_detected = 0;
    uint64_t processes_scanned = 0;
    double cpu_usage = 0.0;
    double memory_usage_mb = 0.0;
    std::string last_scan_time;
    std::string version = "1.0.0";
};

/**
 * @brief Configuración del sistema via API
 */
struct SystemConfiguration {
    bool real_time_protection = true;
    int scan_interval_seconds = 30;
    float detection_threshold = 0.75f;
    bool auto_quarantine = false;
    std::string log_level = "INFO";
    bool notifications_enabled = true;
};

/**
 * @brief Servidor API REST simple para comunicación con frontend
 * 
 * Proporciona endpoints HTTP para que el frontend Electron
 * pueda comunicarse con el backend C++.
 */
class APIServer {
private:
    // Configuración del servidor
    std::string host_;
    int port_;
    bool running_;
    
    // Threading
    std::unique_ptr<std::thread> server_thread_;
    mutable std::mutex server_mutex_;
    
    // Referencias a componentes del antivirus
    DetectionEngine* detection_engine_;
    MLEngine* ml_engine_;
    
    // Estado del sistema
    SystemStatus system_status_;
    SystemConfiguration system_config_;
    
    // Handlers de endpoints
    std::map<std::string, std::function<HTTPResponse(const HTTPRequest&)>> route_handlers_;

public:
    APIServer(const std::string& host = "127.0.0.1", int port = 8080);
    ~APIServer();
    
    /**
     * @brief Inicializa el servidor API
     * @return true si se inició correctamente
     */
    bool initialize();
    
    /**
     * @brief Inicia el servidor en un hilo separado
     * @return true si se inició correctamente
     */
    bool start();
    
    /**
     * @brief Detiene el servidor
     */
    void stop();
    
    /**
     * @brief Verifica si el servidor está corriendo
     * @return true si está activo
     */
    bool isRunning() const { return running_; }
    
    /**
     * @brief Configura las referencias a los motores
     * @param detection_engine Puntero al motor de detección
     * @param ml_engine Puntero al motor ML
     */
    void setEngines(DetectionEngine* detection_engine, MLEngine* ml_engine);
    
    /**
     * @brief Obtiene el puerto del servidor
     * @return Puerto configurado
     */
    int getPort() const { return port_; }
    
    /**
     * @brief Obtiene el host del servidor
     * @return Host configurado
     */
    const std::string& getHost() const { return host_; }

private:
    /**
     * @brief Configura los handlers de rutas
     */
    void setupRoutes();
    
    /**
     * @brief Loop principal del servidor
     */
    void serverLoop();
    
    /**
     * @brief Procesa una request HTTP
     * @param request Request a procesar
     * @return Respuesta HTTP
     */
    HTTPResponse handleRequest(const HTTPRequest& request);
    
    /**
     * @brief Simula el procesamiento HTTP (implementación simple)
     * @param port Puerto donde escuchar
     * @return true si se procesó correctamente
     */
    bool startSimpleServer(int port);
    
    // Handlers de endpoints específicos
    HTTPResponse handleGetStatus(const HTTPRequest& request);
    HTTPResponse handleStartScan(const HTTPRequest& request);
    HTTPResponse handleGetThreats(const HTTPRequest& request);
    HTTPResponse handleGetConfig(const HTTPRequest& request);
    HTTPResponse handleUpdateConfig(const HTTPRequest& request);
    HTTPResponse handleQuarantineThreat(const HTTPRequest& request);
    HTTPResponse handleGetStatistics(const HTTPRequest& request);
    HTTPResponse handleHealthCheck(const HTTPRequest& request);
    
    // Utilidades
    std::string generateJSONResponse(const std::string& data);
    std::string systemStatusToJSON() const;
    std::string systemConfigToJSON() const;
    std::string threatsToJSON() const;
    std::string statisticsToJSON() const;
    HTTPResponse createErrorResponse(int code, const std::string& message);
    std::string getCurrentTime() const;
};

} // namespace AntivirusCore