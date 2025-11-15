// ====================================
//   Main Application Entry Point
// ====================================

class AntivirusLogDashboard {
    constructor() {
        this.version = '1.0.0';
        this.isInitialized = false;
        this.modules = {};
        this.eventBus = new EventTarget();
        
        console.log(`Antivirus Log Dashboard v${this.version}`);
        this.init();
    }

    // Initialize the application
    async init() {
        try {
            console.log('🚀 Initializing Antivirus Log Dashboard...');
            
            // Check dependencies
            await this.checkDependencies();
            
            // Initialize modules
            await this.initializeModules();
            
            // Setup global error handling
            this.setupErrorHandling();
            
            // Setup performance monitoring
            this.setupPerformanceMonitoring();
            
            // Apply saved preferences
            this.applySavedPreferences();
            
            this.isInitialized = true;
            console.log('✅ Dashboard initialized successfully');
            
            // Emit ready event
            this.eventBus.dispatchEvent(new CustomEvent('ready'));
            
        } catch (error) {
            console.error('❌ Dashboard initialization failed:', error);
            this.showCriticalError('Failed to initialize dashboard');
        }
    }

    // Check if all required dependencies are loaded
    async checkDependencies() {
        const requiredLibraries = [
            { name: 'Chart.js', check: () => typeof Chart !== 'undefined' },
            { name: 'DashboardConfig', check: () => typeof DashboardConfig !== 'undefined' },
            { name: 'DashboardUtils', check: () => typeof DashboardUtils !== 'undefined' }
        ];

        for (const lib of requiredLibraries) {
            if (!lib.check()) {
                throw new Error(`Required library not loaded: ${lib.name}`);
            }
        }

        console.log('✅ All dependencies loaded');
    }

    // Initialize all modules
    async initializeModules() {
        try {
            // Initialize API Service
            if (window.ApiService) {
                this.modules.api = window.ApiService;
                console.log('✅ API Service initialized');
            }

            // Initialize Chart Manager
            if (window.ChartManager) {
                this.modules.charts = window.ChartManager;
                console.log('✅ Chart Manager initialized');
            }

            // Initialize Dashboard
            // Note: Dashboard initializes itself on DOMContentLoaded
            console.log('✅ Dashboard module will initialize on DOM ready');

            // Setup module communication
            this.setupModuleCommunication();
            
        } catch (error) {
            console.error('Error initializing modules:', error);
            throw error;
        }
    }

    // Setup communication between modules
    setupModuleCommunication() {
        // Listen for API connection changes
        if (this.modules.api) {
            this.modules.api.on('connectionChange', (status) => {
                this.eventBus.dispatchEvent(new CustomEvent('connectionChange', { 
                    detail: { status } 
                }));
                
                // Update UI based on connection status
                this.updateConnectionUI(status);
            });
        }

        // Listen for chart events
        if (this.modules.charts) {
            // Auto-start chart refresh if API is connected
            this.eventBus.addEventListener('connectionChange', (e) => {
                const status = e.detail.status;
                
                if (status === 'connected') {
                    this.modules.charts.startAutoUpdate(DashboardConfig.INTERVALS.CHART_REFRESH);
                } else {
                    this.modules.charts.stopAutoUpdate();
                }
            });
        }

        console.log('✅ Module communication setup complete');
    }

    // Setup global error handling
    setupErrorHandling() {
        // Global error handler
        window.addEventListener('error', (event) => {
            console.error('Global error:', event.error);
            this.logError({
                type: 'javascript_error',
                message: event.message,
                filename: event.filename,
                line: event.lineno,
                column: event.colno,
                stack: event.error?.stack
            });
        });

        // Promise rejection handler
        window.addEventListener('unhandledrejection', (event) => {
            console.error('Unhandled promise rejection:', event.reason);
            this.logError({
                type: 'promise_rejection',
                message: event.reason?.message || 'Unhandled promise rejection',
                stack: event.reason?.stack
            });
        });

        console.log('✅ Error handling setup complete');
    }

    // Setup performance monitoring
    setupPerformanceMonitoring() {
        // Monitor performance
        const observer = new PerformanceObserver((list) => {
            for (const entry of list.getEntries()) {
                if (entry.duration > 1000) { // Log slow operations
                    console.warn(`Slow operation detected: ${entry.name} took ${entry.duration}ms`);
                }
            }
        });

        try {
            observer.observe({ entryTypes: ['measure', 'navigation'] });
        } catch (error) {
            console.warn('Performance monitoring not supported in this browser');
        }

        // Memory monitoring (if supported)
        if ('memory' in performance) {
            setInterval(() => {
                const memory = performance.memory;
                if (memory.usedJSHeapSize > memory.jsHeapSizeLimit * 0.9) {
                    console.warn('High memory usage detected');
                }
            }, 30000);
        }

        console.log('✅ Performance monitoring setup complete');
    }

    // Apply saved user preferences
    applySavedPreferences() {
        try {
            // Theme preference
            const savedTheme = DashboardUtils.getPreference('theme', 'light');
            if (savedTheme === 'dark') {
                document.body.classList.add('dark-theme');
            }

            // Auto-refresh preference
            const autoRefresh = DashboardUtils.getPreference('autoRefresh', true);
            if (!autoRefresh && window.dashboard) {
                window.dashboard.stopAutoRefresh();
            }

            // Page size preference
            const pageSize = DashboardUtils.getPreference('pageSize', 20);
            if (window.dashboard) {
                window.dashboard.pageSize = pageSize;
            }

            console.log('✅ Preferences applied');
            
        } catch (error) {
            console.warn('Error applying preferences:', error);
        }
    }

    // Update connection status UI
    updateConnectionUI(status) {
        const indicators = document.querySelectorAll('.connection-indicator');
        indicators.forEach(indicator => {
            indicator.className = `connection-indicator status-${status}`;
            indicator.textContent = status.charAt(0).toUpperCase() + status.slice(1);
        });

        // Show notification for connection changes
        const messages = {
            'connected': 'Connected to antivirus system',
            'disconnected': 'Lost connection to antivirus system',
            'error': 'Connection error occurred'
        };

        if (messages[status]) {
            DashboardUtils.showToast(messages[status], status === 'connected' ? 'success' : 'warning');
        }
    }

    // Log errors for debugging
    logError(errorData) {
        // In a production environment, you might send this to a logging service
        console.error('Application Error:', errorData);
        
        // Store in local storage for debugging
        try {
            const errors = JSON.parse(localStorage.getItem('dashboard_errors') || '[]');
            errors.push({
                ...errorData,
                timestamp: new Date().toISOString(),
                userAgent: navigator.userAgent,
                url: window.location.href
            });
            
            // Keep only the last 50 errors
            if (errors.length > 50) {
                errors.splice(0, errors.length - 50);
            }
            
            localStorage.setItem('dashboard_errors', JSON.stringify(errors));
        } catch (e) {
            console.warn('Could not save error to localStorage:', e);
        }
    }

    // Show critical error message
    showCriticalError(message) {
        const errorDiv = document.createElement('div');
        errorDiv.className = 'critical-error';
        errorDiv.innerHTML = `
            <div class="error-content">
                <h2>⚠️ Critical Error</h2>
                <p>${message}</p>
                <p>Please refresh the page or contact support if the problem persists.</p>
                <button onclick="window.location.reload()" class="btn btn-primary">
                    Refresh Page
                </button>
            </div>
        `;
        
        document.body.appendChild(errorDiv);
    }

    // Health check
    async performHealthCheck() {
        const results = {
            timestamp: new Date().toISOString(),
            api: false,
            charts: false,
            dashboard: false,
            localStorage: false,
            performance: {}
        };

        try {
            // API health
            if (this.modules.api) {
                const apiHealth = await this.modules.api.testConnection();
                results.api = apiHealth;
            }

            // Charts health
            if (this.modules.charts) {
                results.charts = this.modules.charts.getAllCharts().length > 0;
            }

            // Dashboard health
            results.dashboard = window.dashboard?.isInitialized || false;

            // localStorage health
            try {
                localStorage.setItem('health_test', 'test');
                localStorage.removeItem('health_test');
                results.localStorage = true;
            } catch (e) {
                results.localStorage = false;
            }

            // Performance metrics
            if ('memory' in performance) {
                results.performance.memory = {
                    used: Math.round(performance.memory.usedJSHeapSize / 1024 / 1024),
                    total: Math.round(performance.memory.totalJSHeapSize / 1024 / 1024),
                    limit: Math.round(performance.memory.jsHeapSizeLimit / 1024 / 1024)
                };
            }

        } catch (error) {
            console.error('Health check failed:', error);
        }

        return results;
    }

    // Export system information for debugging
    async exportSystemInfo() {
        const info = {
            version: this.version,
            timestamp: new Date().toISOString(),
            userAgent: navigator.userAgent,
            url: window.location.href,
            viewport: {
                width: window.innerWidth,
                height: window.innerHeight
            },
            screen: {
                width: screen.width,
                height: screen.height,
                colorDepth: screen.colorDepth
            },
            healthCheck: await this.performHealthCheck(),
            preferences: {
                theme: DashboardUtils.getPreference('theme'),
                autoRefresh: DashboardUtils.getPreference('autoRefresh'),
                pageSize: DashboardUtils.getPreference('pageSize')
            },
            errors: JSON.parse(localStorage.getItem('dashboard_errors') || '[]').slice(-10)
        };

        const blob = new Blob([JSON.stringify(info, null, 2)], { type: 'application/json' });
        const url = URL.createObjectURL(blob);
        
        const link = document.createElement('a');
        link.href = url;
        link.download = `dashboard_system_info_${new Date().toISOString().split('T')[0]}.json`;
        link.click();
        
        URL.revokeObjectURL(url);
        
        DashboardUtils.showToast('System info exported', 'info');
    }

    // Get application status
    getStatus() {
        return {
            version: this.version,
            initialized: this.isInitialized,
            modules: Object.keys(this.modules),
            connectionStatus: this.modules.api?.getConnectionStatus() || 'unknown'
        };
    }

    // Restart application
    async restart() {
        console.log('🔄 Restarting application...');
        
        try {
            // Stop all timers and cleanup
            if (window.dashboard) {
                window.dashboard.destroy();
            }
            
            if (this.modules.charts) {
                this.modules.charts.destroyAllCharts();
                this.modules.charts.stopAutoUpdate();
            }

            // Clear caches
            if (this.modules.api) {
                this.modules.api.clearCache();
            }

            // Reinitialize
            this.isInitialized = false;
            await this.init();
            
            DashboardUtils.showToast('Application restarted successfully', 'success');
            
        } catch (error) {
            console.error('Restart failed:', error);
            DashboardUtils.showToast('Restart failed', 'error');
        }
    }
}

// Initialize application when page loads
document.addEventListener('DOMContentLoaded', () => {
    // Add loading animation
    document.body.classList.add('loading');
    
    // Initialize app
    window.app = new AntivirusLogDashboard();
    
    // Remove loading animation after initialization
    window.app.eventBus.addEventListener('ready', () => {
        document.body.classList.remove('loading');
        
        // Add fade-in animation
        document.body.style.opacity = '0';
        document.body.style.transition = 'opacity 0.5s ease-in-out';
        
        setTimeout(() => {
            document.body.style.opacity = '1';
        }, 100);
    });
});

// Expose app globally for debugging
window.AntivirusApp = {
    version: '1.0.0',
    getApp: () => window.app,
    getDashboard: () => window.dashboard,
    getApi: () => window.api,
    getCharts: () => window.ChartManager,
    exportSystemInfo: () => window.app?.exportSystemInfo(),
    performHealthCheck: () => window.app?.performHealthCheck(),
    restart: () => window.app?.restart()
};

console.log('🎯 Antivirus Log Dashboard loaded. Use window.AntivirusApp for debugging.');