#pragma once

#include <memory>
#include <vector>
#include <atomic>
#include <thread>
#include <functional>
#include <chrono>

#include "ThreatProcessor.hpp"
#include "SystemMonitor.hpp"
#include "../plugins/IDetector.hpp"
#include "../utils/ThreadPool.hpp"
#include "../utils/CircularBuffer.hpp"

namespace AntivirusCore {

/**
 * @brief Motor principal de detección del antivirus
 * 
 * Coordina todos los detectores y monitores del sistema,
 * procesando eventos en tiempo real con alta eficiencia.
 */
class DetectionEngine {
public:
    enum class State {
        STOPPED,
        STARTING,
        RUNNING,
        SCANNING,
        UPDATING,
        ERROR
    };

    struct Config {
        uint32_t max_threads = 8;
        uint32_t buffer_size = 10000;
        std::chrono::milliseconds scan_interval{1000};
        bool enable_realtime_protection = true;
        bool enable_heuristic_analysis = true;
        float threat_threshold = 0.8f;
    };

    struct Statistics {
        std::atomic<uint64_t> events_processed{0};
        std::atomic<uint64_t> threats_detected{0};
        std::atomic<uint64_t> false_positives{0};
        std::atomic<double> avg_processing_time{0.0};
        std::chrono::steady_clock::time_point start_time;
    };

private:
    std::atomic<State> current_state_{State::STOPPED};
    Config config_;
    Statistics stats_;
    
    // Core components
    std::unique_ptr<ThreatProcessor> threat_processor_;
    std::unique_ptr<SystemMonitor> system_monitor_;
    std::unique_ptr<ThreadPool> thread_pool_;
    
    // Event processing
    CircularBuffer<SystemEvent> event_buffer_;
    std::thread processing_thread_;
    std::atomic<bool> should_stop_{false};
    
    // Plugin management
    std::vector<std::unique_ptr<IDetector>> detectors_;
    std::mutex detector_mutex_;

public:
    DetectionEngine(const Config& config = Config{});
    ~DetectionEngine();
    
    // Engine control
    bool initialize();
    bool start();
    bool stop();
    void shutdown();
    
    // State management
    State getState() const { return current_state_.load(); }
    bool isRunning() const { return current_state_.load() == State::RUNNING; }
    
    // Plugin management
    bool loadDetector(std::unique_ptr<IDetector> detector);
    bool unloadDetector(const std::string& detector_name);
    std::vector<std::string> getLoadedDetectors() const;
    
    // Configuration
    void updateConfig(const Config& new_config);
    const Config& getConfig() const { return config_; }
    
    // Statistics and monitoring
    const Statistics& getStatistics() const { return stats_; }
    double getEventsPerSecond() const;
    double getAverageProcessingTime() const;
    
    // Event processing callbacks
    void setThreatDetectedCallback(std::function<void(const ThreatData&)> callback);
    void setSystemEventCallback(std::function<void(const SystemEvent&)> callback);

private:
    void processingLoop();
    void processEvent(const SystemEvent& event);
    bool transitionTo(State new_state);
    void updateStatistics(const SystemEvent& event, double processing_time);
    
    // Event handlers
    void onSystemEvent(const SystemEvent& event);
    void onThreatDetected(const ThreatData& threat);
    void onDetectorError(const std::string& detector_name, const std::exception& error);
};

} // namespace AntivirusCore