// Configuration for the Antivirus Log Dashboard
// Multi-Instance Support Edition

const CONFIG = {
    // API Endpoint (Change this to your backend URL)
    API_BASE_URL: 'https://your-backend-url.vercel.app/api',  // TODO: Update with Vercel URL
    
    // Alternative: Local development
    // API_BASE_URL: 'http://localhost:8000/api',
    
    // API Authentication
    APIKEY: 'antivirus-system-key-2024',  // TODO: Update with your API key
    
    // Dashboard Settings
    AUTO_REFRESH: true,
    REFRESH_INTERVAL: 30000, // 30 seconds
    
    // Pagination
    DEFAULT_PAGE_SIZE: 20,
    MAX_PAGE_SIZE: 100,
    
    // Instance Management
    DEFAULT_INSTANCE: 'all', // 'all' or specific instance ID
    SHOW_INACTIVE_INSTANCES: false,
    
    // Chart Settings
    CHARTS: {
        timeline: {
            type: 'line',
            maxDataPoints: 24,  // Last 24 hours
            updateInterval: 5000
        },
        severity: {
            type: 'doughnut',
            colors: {
                DEBUG: '#9CA3AF',
                INFO: '#3B82F6',
                WARNING: '#F59E0B',
                ERROR: '#EF4444',
                CRITICAL: '#DC2626'
            }
        },
        components: {
            type: 'bar',
            maxBars: 10
        }
    },
    
    // Theme
    DEFAULT_THEME: 'dark', // 'light' or 'dark'
    
    // Notifications
    SHOW_TOAST_NOTIFICATIONS: true,
    TOAST_DURATION: 3000,
    
    // Logging (for debugging)
    DEBUG_MODE: false,
    LOG_API_CALLS: false
};

// Utility function to log if debug mode is on
function debugLog(...args) {
    if (CONFIG.DEBUG_MODE) {
        console.log('[DEBUG]', ...args);
    }
}

// Export configuration
if (typeof module !== 'undefined' && module.exports) {
    module.exports = CONFIG;
}