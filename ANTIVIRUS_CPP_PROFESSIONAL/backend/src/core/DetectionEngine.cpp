#include "DetectionEngine.hpp"
#include <iostream>
#include <algorithm>
#include <Windows.h>
#include <Psapi.h>
#include <tlhelp32.h>

namespace AntivirusCore {

DetectionEngine::DetectionEngine(const Config& config) 
    : config_(config), state_(State::STOPPED), 
      thread_pool_(config.max_threads),
      event_buffer_(config.buffer_size) {
    
    statistics_.start_time = std::chrono::steady_clock::now();
    std::cout << "🛡️  DetectionEngine initialized with " << config.max_threads << " threads\n";
}

DetectionEngine::~DetectionEngine() {
    stop();
}

bool DetectionEngine::start() {
    std::lock_guard<std::mutex> lock(state_mutex_);
    
    if (state_ == State::RUNNING) {
        return true;
    }
    
    state_ = State::STARTING;
    
    try {
        // Inicializar componentes
        if (!initializeComponents()) {
            state_ = State::ERROR;
            return false;
        }
        
        // Iniciar hilo principal de monitoreo
        monitoring_thread_ = std::thread(&DetectionEngine::monitoringLoop, this);
        
        state_ = State::RUNNING;
        std::cout << "✅ DetectionEngine started successfully\n";
        return true;
        
    } catch (const std::exception& e) {
        state_ = State::ERROR;
        std::cerr << "❌ Error starting DetectionEngine: " << e.what() << std::endl;
        return false;
    }
}

bool DetectionEngine::stop() {
    std::lock_guard<std::mutex> lock(state_mutex_);
    
    if (state_ == State::STOPPED) {
        return true;
    }
    
    state_ = State::STOPPED;
    
    // Señalar parada a todos los hilos
    stop_flag_.store(true);
    
    // Esperar a que termine el hilo de monitoreo
    if (monitoring_thread_.joinable()) {
        monitoring_thread_.join();
    }
    
    std::cout << "🛑 DetectionEngine stopped\n";
    return true;
}

ThreatScanResult DetectionEngine::scanProcess(uint32_t processId) {
    ThreatScanResult result;
    result.processId = processId;
    
    try {
        // Obtener información del proceso
        ProcessInfo info = getProcessInfo(processId);
        
        // Análisis heurístico básico
        float suspicion_score = 0.0f;
        
        // 1. Verificar nombre sospechoso
        if (isProcessNameSuspicious(info.name)) {
            suspicion_score += 0.3f;
        }
        
        // 2. Verificar ubicación del archivo
        if (isLocationSuspicious(info.path)) {
            suspicion_score += 0.2f;
        }
        
        // 3. Verificar comportamiento (hooks de teclado)
        if (hasKeyboardHooks(processId)) {
            suspicion_score += 0.4f;
        }
        
        // 4. Verificar conexiones de red sospechosas
        if (hasSuspiciousNetworkActivity(processId)) {
            suspicion_score += 0.3f;
        }
        
        // Evaluar resultado
        result.confidence = suspicion_score;
        
        if (suspicion_score >= config_.threat_threshold) {
            result.isThreat = true;
            result.threatType = ThreatType::KEYLOGGER;
            result.description = "Potencial keylogger detectado - Score: " + std::to_string(suspicion_score);
            
            // Registrar amenaza
            ThreatInfo threat;
            threat.processName = info.name;
            threat.processId = processId;
            threat.type = ThreatType::KEYLOGGER;
            threat.level = suspicion_score > 0.9f ? ThreatLevel::CRITICAL : ThreatLevel::HIGH;
            threat.description = result.description;
            threat.detectedAt = std::chrono::system_clock::now();
            threat.filePath = info.path;
            threat.confidence = suspicion_score;
            
            registerThreat(threat);
            statistics_.threats_detected++;
        }
        
        statistics_.events_processed++;
        
    } catch (const std::exception& e) {
        result.errorMessage = "Error scanning process: " + std::string(e.what());
    }
    
    return result;
}

std::vector<ThreatInfo> DetectionEngine::getDetectedThreats() const {
    std::lock_guard<std::mutex> lock(threats_mutex_);
    return detected_threats_;
}

DetectionEngine::Statistics DetectionEngine::getStatistics() const {
    return statistics_;
}

DetectionEngine::State DetectionEngine::getState() const {
    std::lock_guard<std::mutex> lock(state_mutex_);
    return state_;
}

// Métodos privados

bool DetectionEngine::initializeComponents() {
    // Inicializar detectores básicos
    std::cout << "🔧 Initializing detection components...\n";
    
    // TODO: Cargar plugins de detección
    // TODO: Inicializar monitores de sistema
    
    return true;
}

void DetectionEngine::monitoringLoop() {
    std::cout << "🔍 Starting monitoring loop...\n";
    
    while (!stop_flag_.load()) {
        try {
            // Escanear procesos activos cada intervalo
            scanActiveProcesses();
            
            // Dormir hasta el próximo ciclo
            std::this_thread::sleep_for(config_.scan_interval);
            
        } catch (const std::exception& e) {
            std::cerr << "❌ Error in monitoring loop: " << e.what() << std::endl;
            std::this_thread::sleep_for(std::chrono::seconds(1));
        }
    }
    
    std::cout << "🔍 Monitoring loop stopped\n";
}

void DetectionEngine::scanActiveProcesses() {
    HANDLE hProcessSnap = CreateToolhelp32Snapshot(TH32CS_SNAPPROCESS, 0);
    if (hProcessSnap == INVALID_HANDLE_VALUE) {
        return;
    }
    
    PROCESSENTRY32 pe32;
    pe32.dwSize = sizeof(PROCESSENTRY32);
    
    if (Process32First(hProcessSnap, &pe32)) {
        do {
            // Escanear cada proceso en un hilo separado
            thread_pool_.enqueue([this, processId = pe32.th32ProcessID]() {
                scanProcess(processId);
            });
            
        } while (Process32Next(hProcessSnap, &pe32));
    }
    
    CloseHandle(hProcessSnap);
}

ProcessInfo DetectionEngine::getProcessInfo(uint32_t processId) {
    ProcessInfo info;
    info.processId = processId;
    
    HANDLE hProcess = OpenProcess(PROCESS_QUERY_INFORMATION | PROCESS_VM_READ, FALSE, processId);
    if (hProcess != nullptr) {
        char processName[MAX_PATH];
        if (GetModuleBaseNameA(hProcess, nullptr, processName, MAX_PATH)) {
            info.name = processName;
        }
        
        char processPath[MAX_PATH];
        if (GetModuleFileNameExA(hProcess, nullptr, processPath, MAX_PATH)) {
            info.path = processPath;
        }
        
        CloseHandle(hProcess);
    }
    
    return info;
}

bool DetectionEngine::isProcessNameSuspicious(const std::string& name) {
    // Lista de nombres sospechosos comunes
    static const std::vector<std::string> suspicious_names = {
        "keylogger", "keygrab", "keyspy", "spyware", 
        "logger", "capture", "hook", "stealer",
        "keystr", "klog", "winlog", "svchost32"
    };
    
    std::string lower_name = name;
    std::transform(lower_name.begin(), lower_name.end(), lower_name.begin(), ::tolower);
    
    for (const auto& suspicious : suspicious_names) {
        if (lower_name.find(suspicious) != std::string::npos) {
            return true;
        }
    }
    
    return false;
}

bool DetectionEngine::isLocationSuspicious(const std::string& path) {
    // Ubicaciones sospechosas
    static const std::vector<std::string> suspicious_paths = {
        "\\temp\\", "\\tmp\\", "\\appdata\\local\\temp\\",
        "\\users\\public\\", "\\programdata\\", "\\windows\\temp\\"
    };
    
    std::string lower_path = path;
    std::transform(lower_path.begin(), lower_path.end(), lower_path.begin(), ::tolower);
    
    for (const auto& suspicious : suspicious_paths) {
        if (lower_path.find(suspicious) != std::string::npos) {
            return true;
        }
    }
    
    return false;
}

bool DetectionEngine::hasKeyboardHooks(uint32_t processId) {
    // Verificar si el proceso tiene hooks de teclado instalados
    // Esta es una implementación básica - en un sistema real usarías APIs más avanzadas
    
    HANDLE hProcess = OpenProcess(PROCESS_QUERY_INFORMATION, FALSE, processId);
    if (hProcess != nullptr) {
        // TODO: Implementar detección de hooks WH_KEYBOARD_LL
        CloseHandle(hProcess);
    }
    
    return false; // Implementación básica por ahora
}

bool DetectionEngine::hasSuspiciousNetworkActivity(uint32_t processId) {
    // Verificar actividad de red sospechosa
    // TODO: Implementar análisis de conexiones TCP/UDP
    
    return false; // Implementación básica por ahora
}

void DetectionEngine::registerThreat(const ThreatInfo& threat) {
    std::lock_guard<std::mutex> lock(threats_mutex_);
    
    detected_threats_.push_back(threat);
    
    // Mantener solo las últimas 1000 amenazas
    if (detected_threats_.size() > 1000) {
        detected_threats_.erase(detected_threats_.begin());
    }
    
    std::cout << "🚨 THREAT DETECTED: " << threat.processName 
              << " (PID: " << threat.processId << ") - " 
              << threat.description << std::endl;
}

} // namespace AntivirusCore