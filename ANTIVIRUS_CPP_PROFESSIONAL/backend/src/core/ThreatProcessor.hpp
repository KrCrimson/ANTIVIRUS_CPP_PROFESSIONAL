#pragma once

#include "Types.hpp"
#include <string>

namespace AntivirusCore {

/**
 * @brief Información de un proceso del sistema
 */
struct ProcessInfo {
    uint32_t processId;
    std::string name;
    std::string path;
    uint32_t parentId;
    
    ProcessInfo() : processId(0), parentId(0) {}
};

/**
 * @brief Resultado de escaneo de amenazas
 */
struct ThreatScanResult {
    uint32_t processId;
    bool isThreat;
    ThreatType threatType;
    float confidence;
    std::string description;
    std::string errorMessage;
    
    ThreatScanResult() : processId(0), isThreat(false), 
                        threatType(ThreatType::Unknown), confidence(0.0f) {}
};

/**
 * @brief Procesador de amenazas detectadas
 */
class ThreatProcessor {
public:
    void processThreat(const ThreatInfo& threat) {
        // Implementación básica
    }
};

} // namespace AntivirusCore