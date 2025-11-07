// ====================================
//   API Communication Layer
// ====================================

class ApiClient {
    constructor() {
        this.baseURL = DashboardConfig.API.BASE_URL;
        this.apiKey = DashboardConfig.API.API_KEY;
        this.timeout = DashboardConfig.API.TIMEOUT;
        this.retryAttempts = DashboardConfig.API.RETRY_ATTEMPTS;
        this.retryDelay = DashboardConfig.API.RETRY_DELAY;
    }

    // Generic request method with retry logic
    async request(endpoint, options = {}) {
        const url = `${this.baseURL}${endpoint}`;
        
        const defaultOptions = {
            headers: {
                'Content-Type': 'application/json',
                'X-API-Key': this.apiKey,
                ...options.headers
            },
            timeout: this.timeout,
            ...options
        };

        for (let attempt = 0; attempt <= this.retryAttempts; attempt++) {
            try {
                const controller = new AbortController();
                const timeoutId = setTimeout(() => controller.abort(), this.timeout);
                
                const response = await fetch(url, {
                    ...defaultOptions,
                    signal: controller.signal
                });
                
                clearTimeout(timeoutId);
                
                if (!response.ok) {
                    throw new Error(`HTTP ${response.status}: ${response.statusText}`);
                }
                
                const data = await response.json();
                return { success: true, data, status: response.status };
                
            } catch (error) {
                console.error(`API request failed (attempt ${attempt + 1}):`, error);
                
                if (attempt === this.retryAttempts) {
                    return { 
                        success: false, 
                        error: error.message || 'Request failed',
                        status: error.status || 0
                    };
                }
                
                // Wait before retry (exponential backoff)
                const delay = this.retryDelay * Math.pow(2, attempt);
                await this.sleep(delay);
            }
        }
    }

    // Helper method for delays
    sleep(ms) {
        return new Promise(resolve => setTimeout(resolve, ms));
    }

    // Health check endpoint
    async checkHealth() {
        return this.request('/health');
    }

    // Get logs with pagination and filtering
    async getLogs(params = {}) {
        const queryString = new URLSearchParams(params).toString();
        const endpoint = queryString ? `/logs?${queryString}` : '/logs';
        return this.request(endpoint);
    }

    // Get statistics
    async getStats(params = {}) {
        const queryString = new URLSearchParams(params).toString();
        const endpoint = queryString ? `/stats?${queryString}` : '/stats';
        return this.request(endpoint);
    }

    // Create a new log (for testing)
    async createLog(logData) {
        return this.request('/logs', {
            method: 'POST',
            body: JSON.stringify(logData)
        });
    }
}

// API Service with caching and state management
class ApiService {
    constructor() {
        this.client = new ApiClient();
        this.cache = new Map();
        this.cacheTimeout = 30000; // 30 seconds
        this.connectionStatus = 'disconnected';
        this.listeners = new Map();
        
        // Start periodic health checks
        this.startHealthChecks();
    }

    // Event system for connection status
    on(event, callback) {
        if (!this.listeners.has(event)) {
            this.listeners.set(event, []);
        }
        this.listeners.get(event).push(callback);
    }

    emit(event, data) {
        if (this.listeners.has(event)) {
            this.listeners.get(event).forEach(callback => callback(data));
        }
    }

    // Connection status management
    setConnectionStatus(status) {
        if (this.connectionStatus !== status) {
            this.connectionStatus = status;
            this.emit('connectionChange', status);
        }
    }

    getConnectionStatus() {
        return this.connectionStatus;
    }

    // Cache management
    getCacheKey(endpoint, params) {
        return `${endpoint}_${JSON.stringify(params)}`;
    }

    setCache(key, data) {
        this.cache.set(key, {
            data,
            timestamp: Date.now()
        });
    }

    getCache(key) {
        const cached = this.cache.get(key);
        if (!cached) return null;
        
        const isExpired = Date.now() - cached.timestamp > this.cacheTimeout;
        if (isExpired) {
            this.cache.delete(key);
            return null;
        }
        
        return cached.data;
    }

    clearCache() {
        this.cache.clear();
    }

    // Health monitoring
    async startHealthChecks() {
        const checkHealth = async () => {
            try {
                const response = await this.client.checkHealth();
                if (response.success) {
                    this.setConnectionStatus('connected');
                } else {
                    this.setConnectionStatus('error');
                }
            } catch (error) {
                this.setConnectionStatus('disconnected');
            }
        };

        // Initial check
        await checkHealth();
        
        // Periodic checks
        setInterval(checkHealth, DashboardConfig.INTERVALS.CONNECTION_CHECK);
    }

    // Get logs with caching
    async getLogs(params = {}, useCache = true) {
        const cacheKey = this.getCacheKey('logs', params);
        
        if (useCache) {
            const cached = this.getCache(cacheKey);
            if (cached) {
                return { success: true, data: cached, fromCache: true };
            }
        }

        try {
            const response = await this.client.getLogs(params);
            
            if (response.success) {
                this.setCache(cacheKey, response.data);
                this.setConnectionStatus('connected');
            } else {
                this.setConnectionStatus('error');
            }
            
            return response;
            
        } catch (error) {
            this.setConnectionStatus('disconnected');
            return { success: false, error: error.message };
        }
    }

    // Get statistics with caching
    async getStats(params = {}, useCache = true) {
        const cacheKey = this.getCacheKey('stats', params);
        
        if (useCache) {
            const cached = this.getCache(cacheKey);
            if (cached) {
                return { success: true, data: cached, fromCache: true };
            }
        }

        try {
            const response = await this.client.getStats(params);
            
            if (response.success) {
                this.setCache(cacheKey, response.data);
                this.setConnectionStatus('connected');
            } else {
                this.setConnectionStatus('error');
            }
            
            return response;
            
        } catch (error) {
            this.setConnectionStatus('disconnected');
            return { success: false, error: error.message };
        }
    }

    // Get real-time logs (recent logs without caching)
    async getRecentLogs(limit = 20) {
        const params = {
            limit,
            sort_by: 'timestamp',
            sort_order: 'desc'
        };
        
        return this.getLogs(params, false); // Don't use cache for real-time data
    }

    // Test connection
    async testConnection() {
        try {
            const response = await this.client.checkHealth();
            return response.success;
        } catch (error) {
            return false;
        }
    }

    // Export logs
    async exportLogs(params = {}) {
        try {
            // Add export-friendly parameters
            const exportParams = {
                ...params,
                limit: 10000, // Large limit for export
                format: 'json'
            };
            
            const response = await this.getLogs(exportParams, false);
            
            if (response.success) {
                return {
                    success: true,
                    data: response.data.logs || response.data,
                    filename: `antivirus_logs_${new Date().toISOString().split('T')[0]}.csv`
                };
            }
            
            return response;
            
        } catch (error) {
            return { success: false, error: error.message };
        }
    }

    // Get component list (for filters)
    async getComponents() {
        try {
            const response = await this.getStats();
            
            if (response.success && response.data.top_components) {
                return {
                    success: true,
                    data: response.data.top_components.map(comp => comp.component)
                };
            }
            
            return { success: false, error: 'No components data available' };
            
        } catch (error) {
            return { success: false, error: error.message };
        }
    }

    // Get system information
    async getSystemInfo() {
        try {
            const response = await this.client.checkHealth();
            
            if (response.success) {
                return {
                    success: true,
                    data: {
                        status: response.data.status,
                        uptime: response.data.uptime_seconds,
                        version: response.data.version,
                        timestamp: response.data.timestamp
                    }
                };
            }
            
            return response;
            
        } catch (error) {
            return { success: false, error: error.message };
        }
    }
}

// Create global API service instance
window.ApiService = new ApiService();

// Export for use in other modules
window.api = window.ApiService;