#pragma once

#include <string>
#include <vector>
#include <memory>
#include <chrono>
#include <variant>
#include <unordered_map>

namespace AntivirusCore {

/**
 * @brief Tipos de eventos del sistema que pueden ser monitoreados
 */
enum class EventType {
    PROCESS_CREATED,
    PROCESS_TERMINATED,
    NETWORK_CONNECTION,
    FILE_OPERATION,
    REGISTRY_OPERATION,
    MEMORY_OPERATION,
    KEYBOARD_INPUT,
    MOUSE_INPUT,
    SYSTEM_CALL
};

/**
 * @brief Niveles de severidad de amenazas
 */
enum class ThreatLevel {
    LOW = 1,
    MEDIUM = 2,
    HIGH = 3,
    CRITICAL = 4
};

/**
 * @brief Tipos de amenazas detectables
 */
enum class ThreatType {
    KEYLOGGER,
    SPYWARE,
    ROOTKIT,
    TROJAN,
    VIRUS,
    WORM,
    ADWARE,
    POTENTIALLY_UNWANTED_PROGRAM,
    SUSPICIOUS_BEHAVIOR,
    UNKNOWN
};

/**
 * @brief Información de proceso
 */
struct ProcessInfo {
    uint32_t pid;
    uint32_t parent_pid;
    std::string name;
    std::string executable_path;
    std::vector<std::string> command_line;
    std::chrono::system_clock::time_point creation_time;
    std::string username;
    
    // Performance metrics
    double cpu_usage;
    uint64_t memory_usage;
    uint32_t thread_count;
    uint32_t handle_count;
    
    // Security attributes
    bool is_signed;
    std::string signature_issuer;
    std::vector<std::string> loaded_dlls;
    std::vector<std::string> open_files;
};

/**
 * @brief Información de conexión de red
 */
struct NetworkConnection {
    std::string local_address;
    uint16_t local_port;
    std::string remote_address;
    uint16_t remote_port;
    std::string protocol;
    std::string state;
    uint32_t process_id;
    
    // Traffic metrics
    uint64_t bytes_sent;
    uint64_t bytes_received;
    std::chrono::system_clock::time_point established_time;
    
    // Security attributes
    bool is_encrypted;
    std::string remote_country;
    bool is_suspicious_port;
    bool is_tor_exit_node;
};

/**
 * @brief Información de operación de archivo
 */
struct FileOperation {
    std::string file_path;
    std::string operation_type; // READ, WRITE, CREATE, DELETE, MODIFY
    uint32_t process_id;
    std::chrono::system_clock::time_point timestamp;
    uint64_t bytes_affected;
    
    // Security attributes
    bool is_system_file;
    bool is_executable;
    bool is_in_temp_directory;
    std::string file_hash;
};

/**
 * @brief Evento del sistema genérico
 */
struct SystemEvent {
    EventType type;
    std::chrono::system_clock::time_point timestamp;
    uint32_t source_process_id;
    
    // Data payload (variant containing specific event data)
    std::variant<ProcessInfo, NetworkConnection, FileOperation> data;
    
    // Metadata
    std::unordered_map<std::string, std::string> metadata;
    bool is_suspicious;
    double suspicion_score;
};

/**
 * @brief Datos de amenaza detectada
 */
struct ThreatData {
    std::string id;
    ThreatType type;
    ThreatLevel level;
    std::string name;
    std::string description;
    
    // Detection info
    std::string detector_name;
    double confidence_score;
    std::chrono::system_clock::time_point detection_time;
    
    // Affected resources
    std::vector<uint32_t> affected_processes;
    std::vector<std::string> affected_files;
    std::vector<NetworkConnection> suspicious_connections;
    
    // Recommended actions
    std::vector<std::string> recommended_actions;
    bool should_quarantine;
    bool should_block_network;
    
    // Source event
    SystemEvent source_event;
    
    // Additional context
    std::unordered_map<std::string, std::string> context;
};

/**
 * @brief Configuración de detector
 */
struct DetectorConfig {
    std::string name;
    bool enabled;
    uint32_t priority;
    double sensitivity;
    std::unordered_map<std::string, std::string> parameters;
    
    // Performance settings
    uint32_t max_threads;
    std::chrono::milliseconds timeout;
    bool enable_caching;
};

/**
 * @brief Resultado de detección
 */
struct DetectionResult {
    bool threat_detected;
    ThreatData threat_data;
    double processing_time_ms;
    std::string error_message;
    
    // Additional metadata
    std::unordered_map<std::string, double> feature_scores;
    std::vector<std::string> triggered_rules;
};

/**
 * @brief Métricas del sistema
 */
struct SystemMetrics {
    std::chrono::system_clock::time_point timestamp;
    
    // CPU metrics
    double cpu_usage_total;
    double cpu_usage_antivirus;
    
    // Memory metrics
    uint64_t memory_total;
    uint64_t memory_available;
    uint64_t memory_used_antivirus;
    
    // Network metrics
    uint64_t network_bytes_sent;
    uint64_t network_bytes_received;
    uint32_t active_connections;
    
    // Process metrics
    uint32_t total_processes;
    uint32_t monitored_processes;
    
    // Detection metrics
    uint32_t events_processed_per_second;
    uint32_t threats_detected_today;
    double average_detection_time;
};

} // namespace AntivirusCore