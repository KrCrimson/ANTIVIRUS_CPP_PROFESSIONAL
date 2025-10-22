#pragma once

#include <string>
#include <memory>
#include <mutex>
#include <cstdint>
#include <unordered_map>
#include "../core/Types.hpp"

namespace AntivirusCore {

/**
 * @brief Interface común para todos los detectores de amenazas
 * 
 * Esta interface define el contrato que deben cumplir todos los plugins
 * de detección, permitiendo un sistema modular y extensible.
 */
class IDetector {
public:
    virtual ~IDetector() = default;
    
    /**
     * @brief Inicializa el detector
     * @return true si la inicialización fue exitosa
     */
    virtual bool initialize() = 0;
    
    /**
     * @brief Finaliza y limpia recursos del detector
     */
    virtual void shutdown() = 0;
    
    /**
     * @brief Detecta amenazas en un evento del sistema
     * @param event Evento a analizar
     * @return Resultado de la detección
     */
    virtual DetectionResult detect(const SystemEvent& event) = 0;
    
    /**
     * @brief Obtiene el nombre del detector
     * @return Nombre único del detector
     */
    virtual std::string getName() const = 0;
    
    /**
     * @brief Obtiene la versión del detector
     * @return Versión del detector
     */
    virtual std::string getVersion() const = 0;
    
    /**
     * @brief Obtiene la configuración actual del detector
     * @return Configuración del detector
     */
    virtual DetectorConfig getConfig() const = 0;
    
    /**
     * @brief Actualiza la configuración del detector
     * @param config Nueva configuración
     * @return true si la actualización fue exitosa
     */
    virtual bool updateConfig(const DetectorConfig& config) = 0;
    
    /**
     * @brief Verifica si el detector está habilitado
     * @return true si está habilitado
     */
    virtual bool isEnabled() const = 0;
    
    /**
     * @brief Habilita o deshabilita el detector
     * @param enabled Estado deseado
     */
    virtual void setEnabled(bool enabled) = 0;
    
    /**
     * @brief Obtiene estadísticas del detector
     * @return Estadísticas de rendimiento y detección
     */
    virtual std::unordered_map<std::string, double> getStatistics() const = 0;
    
    /**
     * @brief Verifica si el detector puede manejar un tipo de evento
     * @param event_type Tipo de evento
     * @return true si puede manejar el evento
     */
    virtual bool canHandle(EventType event_type) const = 0;
    
    /**
     * @brief Obtiene la prioridad del detector (mayor número = mayor prioridad)
     * @return Prioridad del detector
     */
    virtual uint32_t getPriority() const = 0;
    
    /**
     * @brief Realiza auto-test del detector
     * @return true si el auto-test fue exitoso
     */
    virtual bool selfTest() = 0;
};

/**
 * @brief Clase base abstracta para implementaciones de detectores
 * 
 * Proporciona funcionalidad común para todos los detectores,
 * reduciendo código duplicado.
 */
class BaseDetector : public IDetector {
protected:
    DetectorConfig config_;
    bool enabled_;
    mutable std::mutex stats_mutex_;
    std::unordered_map<std::string, double> statistics_;
    
public:
    BaseDetector(const std::string& name, const std::string& version);
    virtual ~BaseDetector() = default;
    
    // IDetector implementation
    std::string getName() const override { return config_.name; }
    std::string getVersion() const override;
    DetectorConfig getConfig() const override { return config_; }
    bool updateConfig(const DetectorConfig& config) override;
    bool isEnabled() const override { return enabled_; }
    void setEnabled(bool enabled) override { enabled_ = enabled; }
    std::unordered_map<std::string, double> getStatistics() const override;
    uint32_t getPriority() const override { return config_.priority; }
    
protected:
    /**
     * @brief Actualiza una estadística específica
     * @param key Nombre de la estadística
     * @param value Nuevo valor
     */
    void updateStatistic(const std::string& key, double value);
    
    /**
     * @brief Incrementa una estadística específica
     * @param key Nombre de la estadística
     * @param increment Valor a incrementar (default: 1.0)
     */
    void incrementStatistic(const std::string& key, double increment = 1.0);
    
    /**
     * @brief Crea un ThreatData básico
     * @param type Tipo de amenaza
     * @param level Nivel de amenaza
     * @param description Descripción
     * @param confidence Confianza de la detección
     * @param event Evento fuente
     * @return ThreatData configurado
     */
    ThreatData createThreat(ThreatType type, ThreatLevel level, 
                           const std::string& description, 
                           double confidence, 
                           const SystemEvent& event);

private:
    std::string version_;
};

} // namespace AntivirusCore

/**
 * @brief Macro para exportar detectores como plugins
 * 
 * Cada plugin debe usar esta macro para exportar su función de creación
 */
#define EXPORT_DETECTOR(DetectorClass) \
    extern "C" { \
        std::unique_ptr<AntivirusCore::IDetector> createDetector() { \
            return std::make_unique<DetectorClass>(); \
        } \
        void destroyDetector(AntivirusCore::IDetector* detector) { \
            delete detector; \
        } \
        const char* getDetectorName() { \
            return #DetectorClass; \
        } \
    }