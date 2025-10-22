#pragma once

// Temporal - comentamos ONNX hasta configurar las dependencias
#include "../../include/onnxruntime_cxx_api.h"
#include <memory>
#include <vector>
#include <string>
#include <atomic>
#include <mutex>
#include <future>
#include <functional>
#include <cstdint>

#include "../core/Types.hpp"
#include "../utils/ThreadPool.hpp"

namespace AntivirusCore {

/**
 * @brief Vector de características para ML
 */
using FeatureVector = std::vector<float>;

/**
 * @brief Metadatos del modelo ML
 */
struct ModelMetadata {
    std::string model_path;
    std::string model_version;
    std::vector<std::string> input_names;
    std::vector<std::string> output_names;
    std::vector<int64_t> input_shape;
    std::vector<std::string> class_labels;
    float confidence_threshold;
    std::chrono::system_clock::time_point load_time;
};

/**
 * @brief Resultado de predicción ML
 */
struct PredictionResult {
    ThreatType predicted_class;
    float confidence;
    std::vector<float> class_probabilities;
    FeatureVector features_used;
    double inference_time_ms;
    bool is_valid;
};

// ProcessInfo ya está definido en Types.hpp

/**
 * @brief Regla heurística para detección
 */
struct HeuristicRule {
    std::string name;
    float weight;
    std::vector<std::string> keywords;
};

/**
 * @brief Estadísticas del motor ML
 */
struct MLEngineStats {
    uint64_t total_predictions;
    bool model_loaded;
    bool initialized;
    double average_inference_time_ms;
    double memory_usage_mb;
};

/**
 * @brief Motor de Machine Learning nativo con ONNX Runtime
 * 
 * Proporciona inferencia de alta performance para detección de amenazas
 * usando modelos ONNX optimizados.
 */
class MLEngine {
private:
    // Model metadata y estado
    ModelMetadata metadata_;
    bool initialized_;
    bool model_loaded_;
    
    // Threading y performance
    std::unique_ptr<ThreadPool> thread_pool_;
    mutable std::mutex model_mutex_;
    std::atomic<uint64_t> inference_count_;
    
    // Reglas heurísticas (temporal, sin ONNX)
    std::vector<HeuristicRule> heuristic_rules_;

public:
    MLEngine();
    ~MLEngine();
    
    /**
     * @brief Inicializa el motor ML
     * @param model_path Ruta al modelo ONNX
     * @param num_threads Número de threads para inferencia
     * @return true si la inicialización fue exitosa
     */
    bool initialize(const std::string& model_path, uint32_t num_threads = 4);
    
    /**
     * @brief Finaliza el motor ML
     */
    void shutdown();
    
    /**
     * @brief Realiza predicción síncrona
     * @param features Vector de características
     * @return Resultado de la predicción
     */
    PredictionResult predict(const FeatureVector& features);
    
    /**
     * @brief Realiza predicción asíncrona
     * @param features Vector de características
     * @return Future con el resultado
     */
    std::future<PredictionResult> predictAsync(const FeatureVector& features);
    
    /**
     * @brief Realiza predicción por lotes
     * @param feature_batch Vector de vectores de características
     * @return Vector de resultados
     */
    std::vector<PredictionResult> predictBatch(const std::vector<FeatureVector>& feature_batch);
    
    /**
     * @brief Obtiene metadatos del modelo
     * @return Metadatos del modelo cargado
     */
    const ModelMetadata& getModelMetadata() const { return metadata_; }
    
    /**
     * @brief Verifica si el motor está inicializado
     * @return true si está inicializado
     */
    bool isInitialized() const { return is_initialized_.load(); }
    
    /**
     * @brief Obtiene estadísticas del motor
     * @return Mapa con estadísticas de rendimiento
     */
    std::unordered_map<std::string, double> getStatistics() const;
    
    /**
     * @brief Actualiza el umbral de confianza
     * @param threshold Nuevo umbral (0.0 - 1.0)
     */
    void setConfidenceThreshold(float threshold);
    
    /**
     * @brief Obtiene el umbral de confianza actual
     * @return Umbral de confianza
     */
    float getConfidenceThreshold() const { return metadata_.confidence_threshold; }
    
    /**
     * @brief Valida el formato del vector de características
     * @param features Vector a validar
     * @return true si el formato es válido
     */
    bool validateFeatures(const FeatureVector& features) const;
    
    /**
     * @brief Carga un nuevo modelo
     * @param model_path Ruta al nuevo modelo
     * @return true si la carga fue exitosa
     */
    bool loadModel(const std::string& model_path);
    
    /**
     * @brief Recarga el modelo actual
     * @return true si la recarga fue exitosa
     */
    bool reloadModel();
    
    /**
     * @brief Obtiene información del modelo
     * @return Metadatos del modelo
     */
    ModelMetadata getModelInfo() const;
    
    /**
     * @brief Obtiene estadísticas del motor
     * @return Estadísticas de rendimiento
     */
    MLEngineStats getStats() const;
    
    /**
     * @brief Apaga el motor ML
     */
    void shutdown();
    
    /**
     * @brief Extrae características de un proceso
     * @param process_info Información del proceso
     * @return Vector de características
     */
    FeatureVector extractProcessFeatures(const ProcessInfo& process_info);

private:
    /**
     * @brief Inicializa reglas heurísticas
     */
    void initializeHeuristicRules();
    
    /**
     * @brief Análisis usando reglas heurísticas
     * @param features Vector de características
     * @return Resultado de la predicción
     */
    PredictionResult analyzeWithHeuristics(const FeatureVector& features);
    
    /**
     * @brief Analiza características del proceso
     * @param features Vector de características
     * @param offset Posición de inicio
     * @return Score de sospecha
     */
    float analyzeProcessFeatures(const FeatureVector& features, size_t offset);
    
    /**
     * @brief Analiza características de hooks
     * @param features Vector de características
     * @param offset Posición de inicio
     * @return Score de sospecha
     */
    float analyzeHookFeatures(const FeatureVector& features, size_t offset);
    
    /**
     * @brief Analiza características de actividad
     * @param features Vector de características
     * @param offset Posición de inicio
     * @return Score de sospecha
     */
    float analyzeActivityFeatures(const FeatureVector& features, size_t offset);
    
    /**
     * @brief Calcula la sospecha del nombre del proceso
     * @param process_name Nombre del proceso
     * @return Score de sospecha (0.0 - 1.0)
     */
    float calculateNameSuspicion(const std::string& process_name);
    /**
     * @brief Prepara los tensores de entrada
     * @param features Vector de características
     * @return Vector de tensores ONNX
     */
    std::vector<Ort::Value> prepareInputTensors(const FeatureVector& features);
    
    /**
     * @brief Procesa los tensores de salida
     * @param output_tensors Tensores de salida del modelo
     * @param features_used Características usadas en la predicción
     * @param inference_time Tiempo de inferencia
     * @return Resultado procesado
     */
    PredictionResult processOutputTensors(const std::vector<Ort::Value>& output_tensors,
                                        const FeatureVector& features_used,
                                        double inference_time);
    
    /**
     * @brief Actualiza estadísticas internas
     * @param inference_time Tiempo de inferencia en ms
     * @param threat_detected Si se detectó amenaza
     */
    void updateStatistics(double inference_time, bool threat_detected);
    
    /**
     * @brief Carga metadatos del modelo
     * @param model_path Ruta del modelo
     * @return true si se cargaron correctamente
     */
    bool loadMetadata(const std::string& model_path);
};

/**
 * @brief Extractor de características del sistema
 * 
 * Extrae las 81 características necesarias para la detección ML
 * a partir de eventos del sistema.
 */
class FeatureExtractor {
private:
    struct FeatureCache {
        std::unordered_map<uint32_t, ProcessInfo> process_cache;
        std::unordered_map<std::string, NetworkConnection> network_cache;
        std::chrono::steady_clock::time_point last_update;
    };
    
    FeatureCache cache_;
    std::mutex cache_mutex_;
    std::chrono::seconds cache_ttl_{30}; // TTL del cache

public:
    FeatureExtractor();
    ~FeatureExtractor() = default;
    
    /**
     * @brief Extrae características de un evento del sistema
     * @param event Evento del sistema
     * @return Vector de 81 características
     */
    FeatureVector extractFeatures(const SystemEvent& event);
    
    /**
     * @brief Extrae características específicas de proceso
     * @param process_info Información del proceso
     * @return Vector de características de proceso
     */
    FeatureVector extractProcessFeatures(const ProcessInfo& process_info);
    
    /**
     * @brief Extrae características específicas de red
     * @param connection Información de conexión
     * @return Vector de características de red
     */
    FeatureVector extractNetworkFeatures(const NetworkConnection& connection);
    
    /**
     * @brief Extrae características del sistema global
     * @return Vector de características del sistema
     */
    FeatureVector extractSystemFeatures();
    
    /**
     * @brief Limpia el cache de características
     */
    void clearCache();
    
    /**
     * @brief Configura el TTL del cache
     * @param ttl Tiempo de vida del cache
     */
    void setCacheTTL(std::chrono::seconds ttl) { cache_ttl_ = ttl; }

private:
    /**
     * @brief Actualiza el cache de procesos
     */
    void updateProcessCache();
    
    /**
     * @brief Calcula características agregadas
     * @param event Evento base
     * @return Características agregadas
     */
    FeatureVector calculateAggregatedFeatures(const SystemEvent& event);
    
    /**
     * @brief Normaliza el vector de características
     * @param features Vector a normalizar
     */
    void normalizeFeatures(FeatureVector& features);
};

} // namespace AntivirusCore