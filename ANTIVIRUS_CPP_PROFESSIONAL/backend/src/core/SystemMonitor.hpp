#pragma once

#include "Types.hpp"

namespace AntivirusCore {

/**
 * @brief Monitor del sistema para eventos en tiempo real
 */
class SystemMonitor {
public:
    SystemMonitor() = default;
    
    bool start() {
        return true;
    }
    
    void stop() {
        // Implementación básica
    }
};

} // namespace AntivirusCore