#include "MLEngine.hpp"
#include <algorithm>
#include <chrono>
#include <cmath>
#include <random>

namespace AntivirusCore {

MLEngine::MLEngine() 
    : initialized_(false)
    , model_loaded_(false)
    , thread_pool_(std::make_unique<ThreadPool>(4))
    , inference_count_(0) {
}

MLEngine::~MLEngine() {
    shutdown();
}

bool MLEngine::initialize() {
    std::lock_guard<std::mutex> lock(model_mutex_);
    
    if (initialized_) {
        return true;
    }
    
    try {
        // Inicializar reglas heurísticas temporales (sin ONNX)
        initializeHeuristicRules();
        
        // Configurar metadata del modelo simulado
        metadata_.model_version = "Heuristic_v1.0";
        metadata_.confidence_threshold = 0.75f;
        metadata_.class_labels = {
            "SAFE", "KEYLOGGER", "SPYWARE", "SUSPICIOUS", "MALWARE"
        };
        metadata_.load_time = std::chrono::system_clock::now();
        
        model_loaded_ = true;
        initialized_ = true;
        
        return true;
    }
    catch (const std::exception& e) {
        return false;
    }
}

void MLEngine::initializeHeuristicRules() {
    // Reglas heurísticas para detección de keyloggers
    heuristic_rules_.clear();
    
    // Regla 1: Procesos con nombres sospechosos
    HeuristicRule suspicious_names;
    suspicious_names.name = "suspicious_process_names";
    suspicious_names.weight = 0.8f;
    suspicious_names.keywords = {
        "keylog", "keycatch", "keystroke", "keyspy", "logger",
        "winlog", "hook", "capture", "record", "monitor"
    };
    heuristic_rules_.push_back(suspicious_names);
    
    // Regla 2: Comportamiento de hooks
    HeuristicRule hook_behavior;
    hook_behavior.name = "keyboard_hook_behavior";
    hook_behavior.weight = 0.9f;
    heuristic_rules_.push_back(hook_behavior);
    
    // Regla 3: Procesos ocultos
    HeuristicRule hidden_process;
    hidden_process.name = "hidden_process_behavior";
    hidden_process.weight = 0.7f;
    heuristic_rules_.push_back(hidden_process);
}

bool MLEngine::loadModel(const std::string& model_path) {
    if (!initialized_) {
        return false;
    }
    
    std::lock_guard<std::mutex> lock(model_mutex_);
    
    // Simular carga de modelo exitosa
    metadata_.model_path = model_path;
    model_loaded_ = true;
    
    return true;
}

PredictionResult MLEngine::predict(const FeatureVector& features) {
    PredictionResult result;
    auto start_time = std::chrono::high_resolution_clock::now();
    
    if (!model_loaded_) {
        result.is_valid = false;
        result.confidence = 0.0f;
        result.predicted_class = ThreatType::UNKNOWN;
        return result;
    }
    
    // Análisis heurístico basado en características
    result = analyzeWithHeuristics(features);
    
    // Calcular tiempo de inferencia
    auto end_time = std::chrono::high_resolution_clock::now();
    auto duration = std::chrono::duration_cast<std::chrono::microseconds>(end_time - start_time);
    result.inference_time_ms = duration.count() / 1000.0;
    
    result.features_used = features;
    result.is_valid = true;
    
    inference_count_++;
    
    return result;
}

PredictionResult MLEngine::analyzeWithHeuristics(const FeatureVector& features) {
    PredictionResult result;
    result.class_probabilities.resize(5, 0.0f); // 5 clases
    
    float total_score = 0.0f;
    
    // Análisis basado en características extraídas
    if (features.size() >= 10) {
        // Feature 0-2: Información del proceso
        float process_score = analyzeProcessFeatures(features, 0);
        
        // Feature 3-5: Comportamiento de hooks
        float hook_score = analyzeHookFeatures(features, 3);
        
        // Feature 6-9: Actividad de red/archivo
        float activity_score = analyzeActivityFeatures(features, 6);
        
        total_score = (process_score * 0.4f) + (hook_score * 0.5f) + (activity_score * 0.1f);
    }
    
    // Determinar clase basada en score
    if (total_score >= 0.9f) {
        result.predicted_class = ThreatType::KEYLOGGER;
        result.confidence = total_score;
        result.class_probabilities[1] = total_score; // KEYLOGGER
    }
    else if (total_score >= 0.7f) {
        result.predicted_class = ThreatType::SPYWARE;
        result.confidence = total_score;
        result.class_probabilities[2] = total_score; // SPYWARE
    }
    else if (total_score >= 0.5f) {
        result.predicted_class = ThreatType::SUSPICIOUS_BEHAVIOR;
        result.confidence = total_score;
        result.class_probabilities[3] = total_score; // SUSPICIOUS
    }
    else {
        result.predicted_class = ThreatType::UNKNOWN;
        result.confidence = 1.0f - total_score;
        result.class_probabilities[0] = 1.0f - total_score; // SAFE
    }
    
    return result;
}

float MLEngine::analyzeProcessFeatures(const FeatureVector& features, size_t offset) {
    if (offset + 2 >= features.size()) return 0.0f;
    
    float score = 0.0f;
    
    // Análisis del nombre del proceso (simulado)
    float name_suspicion = features[offset];     // 0.0 = normal, 1.0 = muy sospechoso
    float cpu_usage = features[offset + 1];     // % CPU
    float memory_usage = features[offset + 2];  // MB RAM
    
    // Procesos con alta CPU y memoria pueden ser sospechosos
    if (cpu_usage > 10.0f || memory_usage > 50.0f) {
        score += 0.3f;
    }
    
    // Nombre sospechoso es muy importante
    score += name_suspicion * 0.7f;
    
    return std::min(1.0f, score);
}

float MLEngine::analyzeHookFeatures(const FeatureVector& features, size_t offset) {
    if (offset + 2 >= features.size()) return 0.0f;
    
    float hook_count = features[offset];         // Número de hooks
    float keyboard_hooks = features[offset + 1]; // Hooks de teclado específicos
    float hidden_windows = features[offset + 2]; // Ventanas ocultas
    
    float score = 0.0f;
    
    // Los keyloggers típicamente usan hooks de teclado
    if (keyboard_hooks > 0) {
        score += 0.8f;
    }
    
    // Múltiples hooks son sospechosos
    if (hook_count > 3) {
        score += 0.4f;
    }
    
    // Ventanas ocultas son muy sospechosas
    if (hidden_windows > 0) {
        score += 0.6f;
    }
    
    return std::min(1.0f, score);
}

float MLEngine::analyzeActivityFeatures(const FeatureVector& features, size_t offset) {
    if (offset + 3 >= features.size()) return 0.0f;
    
    float file_operations = features[offset];     // Operaciones de archivo por minuto
    float network_activity = features[offset + 1]; // Conexiones de red
    float registry_access = features[offset + 2];  // Accesos al registro
    float encryption_apis = features[offset + 3];  // Uso de APIs de encriptación
    
    float score = 0.0f;
    
    // Actividad de archivos excesiva
    if (file_operations > 100.0f) {
        score += 0.2f;
    }
    
    // Actividad de red sospechosa
    if (network_activity > 10.0f) {
        score += 0.3f;
    }
    
    // Acceso frecuente al registro
    if (registry_access > 50.0f) {
        score += 0.2f;
    }
    
    // Uso de encriptación (para ocultar datos robados)
    if (encryption_apis > 0) {
        score += 0.5f;
    }
    
    return std::min(1.0f, score);
}

std::future<PredictionResult> MLEngine::predictAsync(const FeatureVector& features) {
    if (!thread_pool_) {
        std::promise<PredictionResult> promise;
        promise.set_value(PredictionResult{});
        return promise.get_future();
    }
    
    return thread_pool_->enqueue([this, features]() {
        return predict(features);
    });
}

std::vector<PredictionResult> MLEngine::predictBatch(const std::vector<FeatureVector>& feature_batch) {
    std::vector<PredictionResult> results;
    results.reserve(feature_batch.size());
    
    for (const auto& features : feature_batch) {
        results.push_back(predict(features));
    }
    
    return results;
}

ModelMetadata MLEngine::getModelInfo() const {
    std::lock_guard<std::mutex> lock(model_mutex_);
    return metadata_;
}

MLEngineStats MLEngine::getStats() const {
    MLEngineStats stats;
    stats.total_predictions = inference_count_.load();
    stats.model_loaded = model_loaded_;
    stats.initialized = initialized_;
    stats.average_inference_time_ms = 2.5; // Tiempo promedio simulado
    stats.memory_usage_mb = 25.0; // Uso de memoria simulado
    return stats;
}

bool MLEngine::reloadModel() {
    if (!initialized_ || metadata_.model_path.empty()) {
        return false;
    }
    
    return loadModel(metadata_.model_path);
}

void MLEngine::shutdown() {
    std::lock_guard<std::mutex> lock(model_mutex_);
    
    if (thread_pool_) {
        thread_pool_.reset();
    }
    
    model_loaded_ = false;
    initialized_ = false;
    heuristic_rules_.clear();
}

FeatureVector MLEngine::extractProcessFeatures(const ProcessInfo& process_info) {
    FeatureVector features(10, 0.0f);
    
    // Feature 0: Suspicion del nombre
    features[0] = calculateNameSuspicion(process_info.name);
    
    // Feature 1-2: Recursos del sistema
    features[1] = static_cast<float>(process_info.cpu_usage);
    features[2] = static_cast<float>(process_info.memory_mb);
    
    // Feature 3-5: Información de hooks (simulada)
    features[3] = static_cast<float>(process_info.hook_count);
    features[4] = process_info.has_keyboard_hooks ? 1.0f : 0.0f;
    features[5] = process_info.has_hidden_windows ? 1.0f : 0.0f;
    
    // Feature 6-9: Actividad del sistema
    features[6] = static_cast<float>(process_info.file_operations_per_minute);
    features[7] = static_cast<float>(process_info.network_connections);
    features[8] = static_cast<float>(process_info.registry_accesses);
    features[9] = process_info.uses_encryption_apis ? 1.0f : 0.0f;
    
    return features;
}

float MLEngine::calculateNameSuspicion(const std::string& process_name) {
    std::string lower_name = process_name;
    std::transform(lower_name.begin(), lower_name.end(), lower_name.begin(), ::tolower);
    
    float suspicion = 0.0f;
    
    for (const auto& rule : heuristic_rules_) {
        for (const auto& keyword : rule.keywords) {
            if (lower_name.find(keyword) != std::string::npos) {
                suspicion = std::max(suspicion, rule.weight);
            }
        }
    }
    
    return suspicion;
}

} // namespace AntivirusCore