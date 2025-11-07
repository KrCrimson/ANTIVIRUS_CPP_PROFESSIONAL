// ====================================
//   Dashboard Configuration
// ====================================

window.DashboardConfig = {
    // API Configuration
    API: {
        BASE_URL: 'http://localhost:8000/api',
        API_KEY: 'dashboard-client-key-2024',
        TIMEOUT: 10000,
        RETRY_ATTEMPTS: 3,
        RETRY_DELAY: 1000
    },

    // Update Intervals (milliseconds)
    INTERVALS: {
        STATS_UPDATE: 30000,        // 30 seconds
        LOGS_UPDATE: 5000,          // 5 seconds
        CHARTS_UPDATE: 60000,       // 1 minute
        REAL_TIME_UPDATE: 2000,     // 2 seconds
        CONNECTION_CHECK: 10000     // 10 seconds
    },

    // UI Configuration
    UI: {
        LOGS_PER_PAGE: 50,
        MAX_REAL_TIME_LOGS: 20,
        CHART_ANIMATION_DURATION: 750,
        TOAST_DURATION: 5000,
        MODAL_ANIMATION_DURATION: 300
    },

    // Chart Colors (matching CSS variables)
    CHART_COLORS: {
        primary: '#2563eb',
        success: '#10b981',
        warning: '#f59e0b',
        error: '#ef4444',
        info: '#06b6d4',
        secondary: '#64748b',
        background: '#f8fafc',
        text: '#1e293b'
    },

    // Log Levels Configuration
    LOG_LEVELS: {
        DEBUG: { color: '#94a3b8', priority: 0 },
        INFO: { color: '#06b6d4', priority: 1 },
        WARNING: { color: '#f59e0b', priority: 2 },
        ERROR: { color: '#ef4444', priority: 3 },
        CRITICAL: { color: '#dc2626', priority: 4 }
    },

    // Date/Time Formatting
    DATE_FORMATS: {
        DISPLAY: 'DD/MM/YYYY HH:mm:ss',
        API: 'YYYY-MM-DDTHH:mm:ss',
        CHART: 'HH:mm',
        FILTER: 'YYYY-MM-DD'
    },

    // Feature Flags
    FEATURES: {
        REAL_TIME_UPDATES: true,
        DARK_THEME: true,
        EXPORT_FUNCTIONALITY: true,
        WEBSOCKETS: false,          // Future feature
        NOTIFICATIONS: true,
        AUTO_REFRESH: true
    },

    // Local Storage Keys
    STORAGE_KEYS: {
        THEME: 'antivirus_dashboard_theme',
        FILTERS: 'antivirus_dashboard_filters',
        SETTINGS: 'antivirus_dashboard_settings',
        LAST_UPDATE: 'antivirus_dashboard_last_update'
    },

    // Error Messages
    ERROR_MESSAGES: {
        CONNECTION_FAILED: 'No se pudo conectar al servidor',
        LOAD_FAILED: 'Error cargando datos',
        EXPORT_FAILED: 'Error exportando datos',
        UNKNOWN_ERROR: 'Error desconocido'
    }
};

// Utility Functions
window.DashboardUtils = {
    // Format timestamp for display
    formatTimestamp(timestamp, format = DashboardConfig.DATE_FORMATS.DISPLAY) {
        const date = new Date(timestamp);
        const options = {
            year: 'numeric',
            month: '2-digit',
            day: '2-digit',
            hour: '2-digit',
            minute: '2-digit',
            second: '2-digit',
            hour12: false
        };
        
        if (format === DashboardConfig.DATE_FORMATS.CHART) {
            return date.toLocaleTimeString('es-ES', { 
                hour: '2-digit', 
                minute: '2-digit' 
            });
        }
        
        return date.toLocaleString('es-ES', options);
    },

    // Format relative time (e.g., "hace 5 minutos")
    formatRelativeTime(timestamp) {
        const now = new Date();
        const date = new Date(timestamp);
        const diff = now - date;
        
        const seconds = Math.floor(diff / 1000);
        const minutes = Math.floor(seconds / 60);
        const hours = Math.floor(minutes / 60);
        const days = Math.floor(hours / 24);
        
        if (days > 0) return `hace ${days} día${days > 1 ? 's' : ''}`;
        if (hours > 0) return `hace ${hours} hora${hours > 1 ? 's' : ''}`;
        if (minutes > 0) return `hace ${minutes} minuto${minutes > 1 ? 's' : ''}`;
        return 'hace unos segundos';
    },

    // Format numbers with thousands separator
    formatNumber(number) {
        return number.toLocaleString('es-ES');
    },

    // Calculate uptime
    formatUptime(startTime) {
        const now = new Date();
        const start = new Date(startTime);
        const diff = now - start;
        
        const hours = Math.floor(diff / (1000 * 60 * 60));
        const minutes = Math.floor((diff % (1000 * 60 * 60)) / (1000 * 60));
        
        if (hours > 24) {
            const days = Math.floor(hours / 24);
            return `${days}d ${hours % 24}h`;
        }
        
        return `${hours}h ${minutes}m`;
    },

    // Get color for log level
    getLogLevelColor(level) {
        return DashboardConfig.LOG_LEVELS[level]?.color || DashboardConfig.CHART_COLORS.secondary;
    },

    // Truncate text
    truncateText(text, maxLength = 100) {
        if (text.length <= maxLength) return text;
        return text.substring(0, maxLength) + '...';
    },

    // Debounce function
    debounce(func, wait) {
        let timeout;
        return function executedFunction(...args) {
            const later = () => {
                clearTimeout(timeout);
                func(...args);
            };
            clearTimeout(timeout);
            timeout = setTimeout(later, wait);
        };
    },

    // Show toast notification
    showToast(message, type = 'info', duration = DashboardConfig.UI.TOAST_DURATION) {
        // Create toast element
        const toast = document.createElement('div');
        toast.className = `toast toast-${type}`;
        toast.innerHTML = `
            <div class="toast-content">
                <i class="fas fa-${this.getToastIcon(type)}"></i>
                <span>${message}</span>
            </div>
        `;
        
        // Add to page
        document.body.appendChild(toast);
        
        // Show toast
        setTimeout(() => toast.classList.add('show'), 100);
        
        // Hide and remove toast
        setTimeout(() => {
            toast.classList.remove('show');
            setTimeout(() => document.body.removeChild(toast), 300);
        }, duration);
    },

    // Get toast icon
    getToastIcon(type) {
        const icons = {
            success: 'check-circle',
            error: 'exclamation-circle',
            warning: 'exclamation-triangle',
            info: 'info-circle'
        };
        return icons[type] || 'info-circle';
    },

    // Local storage helpers
    saveToStorage(key, data) {
        try {
            localStorage.setItem(key, JSON.stringify(data));
        } catch (e) {
            console.error('Error saving to localStorage:', e);
        }
    },

    loadFromStorage(key, defaultValue = null) {
        try {
            const data = localStorage.getItem(key);
            return data ? JSON.parse(data) : defaultValue;
        } catch (e) {
            console.error('Error loading from localStorage:', e);
            return defaultValue;
        }
    },

    // Export data to CSV
    exportToCSV(data, filename) {
        const csv = this.convertToCSV(data);
        const blob = new Blob([csv], { type: 'text/csv' });
        const url = window.URL.createObjectURL(blob);
        
        const a = document.createElement('a');
        a.href = url;
        a.download = filename;
        document.body.appendChild(a);
        a.click();
        document.body.removeChild(a);
        window.URL.revokeObjectURL(url);
    },

    // Convert array of objects to CSV
    convertToCSV(data) {
        if (!data || data.length === 0) return '';
        
        const headers = Object.keys(data[0]);
        const csv = [
            headers.join(','),
            ...data.map(row => 
                headers.map(header => {
                    const value = row[header];
                    // Escape commas and quotes
                    if (typeof value === 'string' && (value.includes(',') || value.includes('"'))) {
                        return `"${value.replace(/"/g, '""')}"`;
                    }
                    return value;
                }).join(',')
            )
        ];
        
        return csv.join('\n');
    },

    // Generate random ID
    generateId() {
        return Math.random().toString(36).substr(2, 9);
    }
};

// Add toast CSS if not present
if (!document.querySelector('#toast-styles')) {
    const toastStyles = document.createElement('style');
    toastStyles.id = 'toast-styles';
    toastStyles.textContent = `
        .toast {
            position: fixed;
            top: 20px;
            right: 20px;
            background: var(--bg-card);
            border: 1px solid var(--border-color);
            border-radius: var(--radius-md);
            box-shadow: var(--shadow-lg);
            padding: var(--spacing-md);
            z-index: 10000;
            opacity: 0;
            transform: translateX(100%);
            transition: all 0.3s ease;
        }
        
        .toast.show {
            opacity: 1;
            transform: translateX(0);
        }
        
        .toast-content {
            display: flex;
            align-items: center;
            gap: var(--spacing-sm);
        }
        
        .toast-success { border-left: 4px solid var(--success-color); }
        .toast-error { border-left: 4px solid var(--error-color); }
        .toast-warning { border-left: 4px solid var(--warning-color); }
        .toast-info { border-left: 4px solid var(--info-color); }
        
        .toast i {
            font-size: 1rem;
        }
        
        .toast-success i { color: var(--success-color); }
        .toast-error i { color: var(--error-color); }
        .toast-warning i { color: var(--warning-color); }
        .toast-info i { color: var(--info-color); }
    `;
    document.head.appendChild(toastStyles);
}