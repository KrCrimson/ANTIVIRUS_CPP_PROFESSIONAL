#include "APIServer.hpp"
#include "../core/DetectionEngine.hpp"
#include "../ml/MLEngine.hpp"
#include <sstream>
#include <chrono>
#include <iomanip>
#include <iostream>

namespace AntivirusCore {

APIServer::APIServer(const std::string& host, int port)
    : host_(host)
    , port_(port)
    , running_(false)
    , detection_engine_(nullptr)
    , ml_engine_(nullptr) {
    
    // Configuración inicial del sistema
    system_status_.protection_enabled = true;
    system_status_.status = "INITIALIZING";
    system_status_.threats_detected = 0;
    system_status_.processes_scanned = 0;
    system_status_.cpu_usage = 0.0;
    system_status_.memory_usage_mb = 25.0;
    system_status_.last_scan_time = getCurrentTime();
}

APIServer::~APIServer() {
    stop();
}

bool APIServer::initialize() {
    std::lock_guard<std::mutex> lock(server_mutex_);
    
    if (running_) {
        return true;
    }
    
    // Configurar rutas
    setupRoutes();
    
    // Actualizar estado del sistema
    system_status_.status = "READY";
    
    return true;
}

bool APIServer::start() {
    std::lock_guard<std::mutex> lock(server_mutex_);
    
    if (running_) {
        return true;
    }
    
    try {
        // Iniciar servidor en hilo separado
        server_thread_ = std::make_unique<std::thread>([this]() {
            serverLoop();
        });
        
        running_ = true;
        system_status_.status = "RUNNING";
        
        std::cout << "🌐 API Server started on http://" << host_ << ":" << port_ << std::endl;
        return true;
    }
    catch (const std::exception& e) {
        std::cerr << "Error starting API server: " << e.what() << std::endl;
        return false;
    }
}

void APIServer::stop() {
    {
        std::lock_guard<std::mutex> lock(server_mutex_);
        if (!running_) {
            return;
        }
        running_ = false;
        system_status_.status = "STOPPING";
    }
    
    // Esperar que termine el hilo del servidor
    if (server_thread_ && server_thread_->joinable()) {
        server_thread_->join();
    }
    
    system_status_.status = "STOPPED";
    std::cout << "🛑 API Server stopped" << std::endl;
}

void APIServer::setEngines(DetectionEngine* detection_engine, MLEngine* ml_engine) {
    detection_engine_ = detection_engine;
    ml_engine_ = ml_engine;
}

void APIServer::setupRoutes() {
    // Configurar handlers para diferentes endpoints
    route_handlers_["/api/status"] = [this](const HTTPRequest& req) {
        return handleGetStatus(req);
    };
    
    route_handlers_["/api/scan/start"] = [this](const HTTPRequest& req) {
        return handleStartScan(req);
    };
    
    route_handlers_["/api/threats"] = [this](const HTTPRequest& req) {
        return handleGetThreats(req);
    };
    
    route_handlers_["/api/config"] = [this](const HTTPRequest& req) {
        if (req.method == "GET") {
            return handleGetConfig(req);
        } else if (req.method == "POST" || req.method == "PUT") {
            return handleUpdateConfig(req);
        }
        return createErrorResponse(405, "Method not allowed");
    };
    
    route_handlers_["/api/quarantine"] = [this](const HTTPRequest& req) {
        return handleQuarantineThreat(req);
    };
    
    route_handlers_["/api/statistics"] = [this](const HTTPRequest& req) {
        return handleGetStatistics(req);
    };
    
    route_handlers_["/api/health"] = [this](const HTTPRequest& req) {
        return handleHealthCheck(req);
    };
}

void APIServer::serverLoop() {
    // Servidor HTTP simple simulado
    std::cout << "🔄 API Server loop started on port " << port_ << std::endl;
    
    while (running_) {
        // Simular procesamiento de requests
        // En una implementación real, aquí estaría el loop de red
        
        // Actualizar estadísticas del sistema periódicamente
        {
            std::lock_guard<std::mutex> lock(server_mutex_);
            if (detection_engine_) {
                auto stats = detection_engine_->getStatistics();
                system_status_.processes_scanned = stats.total_scans;
                system_status_.threats_detected = stats.threats_found;
                system_status_.cpu_usage = stats.cpu_usage;
            }
            
            if (ml_engine_) {
                auto ml_stats = ml_engine_->getStats();
                system_status_.memory_usage_mb = ml_stats.memory_usage_mb;
            }
        }
        
        // Simular trabajo del servidor
        std::this_thread::sleep_for(std::chrono::milliseconds(1000));
    }
}

HTTPResponse APIServer::handleRequest(const HTTPRequest& request) {
    // Buscar handler para la ruta
    auto it = route_handlers_.find(request.path);
    if (it != route_handlers_.end()) {
        try {
            return it->second(request);
        }
        catch (const std::exception& e) {
            return createErrorResponse(500, "Internal server error: " + std::string(e.what()));
        }
    }
    
    return createErrorResponse(404, "Endpoint not found");
}

HTTPResponse APIServer::handleGetStatus(const HTTPRequest& request) {
    HTTPResponse response;
    response.status_code = 200;
    response.content_type = "application/json";
    response.body = systemStatusToJSON();
    
    // Headers CORS
    response.headers["Access-Control-Allow-Origin"] = "*";
    response.headers["Access-Control-Allow-Methods"] = "GET, POST, OPTIONS";
    
    return response;
}

HTTPResponse APIServer::handleStartScan(const HTTPRequest& request) {
    HTTPResponse response;
    
    if (detection_engine_) {
        // Iniciar escaneo
        bool scan_started = detection_engine_->startFullScan();
        
        if (scan_started) {
            response.status_code = 200;
            response.body = R"({"status": "success", "message": "Full scan started"})";
        } else {
            response.status_code = 500;
            response.body = R"({"status": "error", "message": "Failed to start scan"})";
        }
    } else {
        response.status_code = 503;
        response.body = R"({"status": "error", "message": "Detection engine not available"})";
    }
    
    response.content_type = "application/json";
    response.headers["Access-Control-Allow-Origin"] = "*";
    
    return response;
}

HTTPResponse APIServer::handleGetThreats(const HTTPRequest& request) {
    HTTPResponse response;
    response.status_code = 200;
    response.content_type = "application/json";
    response.body = threatsToJSON();
    response.headers["Access-Control-Allow-Origin"] = "*";
    
    return response;
}

HTTPResponse APIServer::handleGetConfig(const HTTPRequest& request) {
    HTTPResponse response;
    response.status_code = 200;
    response.content_type = "application/json";
    response.body = systemConfigToJSON();
    response.headers["Access-Control-Allow-Origin"] = "*";
    
    return response;
}

HTTPResponse APIServer::handleUpdateConfig(const HTTPRequest& request) {
    HTTPResponse response;
    
    // Simular actualización de configuración
    // En una implementación real, se parsearía el JSON del body
    
    system_config_.real_time_protection = true;
    system_config_.scan_interval_seconds = 30;
    
    response.status_code = 200;
    response.content_type = "application/json";
    response.body = R"({"status": "success", "message": "Configuration updated"})";
    response.headers["Access-Control-Allow-Origin"] = "*";
    
    return response;
}

HTTPResponse APIServer::handleQuarantineThreat(const HTTPRequest& request) {
    HTTPResponse response;
    
    // Simular cuarentena de amenaza
    response.status_code = 200;
    response.content_type = "application/json";
    response.body = R"({"status": "success", "message": "Threat quarantined"})";
    response.headers["Access-Control-Allow-Origin"] = "*";
    
    return response;
}

HTTPResponse APIServer::handleGetStatistics(const HTTPRequest& request) {
    HTTPResponse response;
    response.status_code = 200;
    response.content_type = "application/json";
    response.body = statisticsToJSON();
    response.headers["Access-Control-Allow-Origin"] = "*";
    
    return response;
}

HTTPResponse APIServer::handleHealthCheck(const HTTPRequest& request) {
    HTTPResponse response;
    response.status_code = 200;
    response.content_type = "application/json";
    
    bool healthy = running_ && 
                   (detection_engine_ != nullptr) && 
                   (ml_engine_ != nullptr);
    
    std::ostringstream json;
    json << R"({)"
         << R"("status": ")" << (healthy ? "healthy" : "unhealthy") << R"(",)"
         << R"("timestamp": ")" << getCurrentTime() << R"(",)"
         << R"("uptime_seconds": 3600,)"
         << R"("components": {)"
         << R"("detection_engine": )" << (detection_engine_ ? "true" : "false") << ","
         << R"("ml_engine": )" << (ml_engine_ ? "true" : "false")
         << R"(}})";
    
    response.body = json.str();
    response.headers["Access-Control-Allow-Origin"] = "*";
    
    return response;
}

std::string APIServer::systemStatusToJSON() const {
    std::ostringstream json;
    json << R"({)"
         << R"("protection_enabled": )" << (system_status_.protection_enabled ? "true" : "false") << ","
         << R"("status": ")" << system_status_.status << R"(",)"
         << R"("threats_detected": )" << system_status_.threats_detected << ","
         << R"("processes_scanned": )" << system_status_.processes_scanned << ","
         << R"("cpu_usage": )" << system_status_.cpu_usage << ","
         << R"("memory_usage_mb": )" << system_status_.memory_usage_mb << ","
         << R"("last_scan_time": ")" << system_status_.last_scan_time << R"(",)"
         << R"("version": ")" << system_status_.version << R"(")"
         << R"(})";
    
    return json.str();
}

std::string APIServer::systemConfigToJSON() const {
    std::ostringstream json;
    json << R"({)"
         << R"("real_time_protection": )" << (system_config_.real_time_protection ? "true" : "false") << ","
         << R"("scan_interval_seconds": )" << system_config_.scan_interval_seconds << ","
         << R"("detection_threshold": )" << system_config_.detection_threshold << ","
         << R"("auto_quarantine": )" << (system_config_.auto_quarantine ? "true" : "false") << ","
         << R"("log_level": ")" << system_config_.log_level << R"(",)"
         << R"("notifications_enabled": )" << (system_config_.notifications_enabled ? "true" : "false")
         << R"(})";
    
    return json.str();
}

std::string APIServer::threatsToJSON() const {
    // Simular lista de amenazas detectadas
    std::ostringstream json;
    json << R"({)"
         << R"("threats": [)"
         << R"({)"
         << R"("id": 1,)"
         << R"("name": "Suspicious Process",)"
         << R"("type": "KEYLOGGER",)"
         << R"("level": "HIGH",)"
         << R"("process_name": "suspicious.exe",)"
         << R"("process_id": 1234,)"
         << R"("confidence": 0.95,)"
         << R"("detected_at": ")" << getCurrentTime() << R"(",)"
         << R"("status": "ACTIVE")"
         << R"(})"
         << R"(],)"
         << R"("total_count": 1)"
         << R"(})";
    
    return json.str();
}

std::string APIServer::statisticsToJSON() const {
    std::ostringstream json;
    json << R"({)"
         << R"("scans_performed": )" << system_status_.processes_scanned << ","
         << R"("threats_detected": )" << system_status_.threats_detected << ","
         << R"("threats_quarantined": 0,)"
         << R"("system_performance": {)"
         << R"("cpu_usage": )" << system_status_.cpu_usage << ","
         << R"("memory_usage_mb": )" << system_status_.memory_usage_mb << ","
         << R"("uptime_hours": 1)"
         << R"(},)"
         << R"("detection_accuracy": 0.98)"
         << R"(})";
    
    return json.str();
}

HTTPResponse APIServer::createErrorResponse(int code, const std::string& message) {
    HTTPResponse response;
    response.status_code = code;
    response.content_type = "application/json";
    
    std::ostringstream json;
    json << R"({"error": {"code": )" << code 
         << R"(, "message": ")" << message << R"("}})";
    response.body = json.str();
    
    response.headers["Access-Control-Allow-Origin"] = "*";
    
    return response;
}

std::string APIServer::getCurrentTime() const {
    auto now = std::chrono::system_clock::now();
    auto time_t = std::chrono::system_clock::to_time_t(now);
    
    std::ostringstream oss;
    oss << std::put_time(std::localtime(&time_t), "%Y-%m-%d %H:%M:%S");
    return oss.str();
}

} // namespace AntivirusCore