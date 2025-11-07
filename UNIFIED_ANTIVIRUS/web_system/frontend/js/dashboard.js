// ====================================
//   Dashboard Core Functionality
// ====================================

class Dashboard {
    constructor() {
        this.isInitialized = false;
        this.currentPage = 1;
        this.pageSize = 20;
        this.totalLogs = 0;
        this.currentFilters = {};
        this.selectedLogs = new Set();
        this.refreshTimer = null;
        this.connectionStatus = 'disconnected';
        
        // UI elements
        this.elements = {};
        
        // Data cache
        this.cachedStats = null;
        this.cachedLogs = null;
        
        this.init();
    }

    // Initialize dashboard
    async init() {
        try {
            this.bindElements();
            this.attachEventListeners();
            this.setupConnectionMonitoring();
            await this.loadInitialData();
            this.startAutoRefresh();
            this.isInitialized = true;
            
            console.log('Dashboard initialized successfully');
            
        } catch (error) {
            console.error('Dashboard initialization failed:', error);
            this.showError('Failed to initialize dashboard');
        }
    }

    // Bind DOM elements
    bindElements() {
        this.elements = {
            // Stats cards
            totalLogsCard: document.getElementById('total-logs'),
            errorsCard: document.getElementById('total-errors'),
            warningsCard: document.getElementById('total-warnings'),
            systemStatusCard: document.getElementById('system-status'),
            
            // Controls
            refreshBtn: document.getElementById('refresh-btn'),
            exportBtn: document.getElementById('export-btn'),
            filtersBtn: document.getElementById('filters-btn'),
            settingsBtn: document.getElementById('settings-btn'),
            
            // Filters
            filtersPanel: document.getElementById('filters-panel'),
            componentFilter: document.getElementById('component-filter'),
            levelFilter: document.getElementById('level-filter'),
            dateFromFilter: document.getElementById('date-from'),
            dateToFilter: document.getElementById('date-to'),
            searchFilter: document.getElementById('search-logs'),
            applyFiltersBtn: document.getElementById('apply-filters'),
            clearFiltersBtn: document.getElementById('clear-filters'),
            
            // Table and pagination
            logsTable: document.getElementById('logs-table'),
            logsTableBody: document.querySelector('#logs-table tbody'),
            paginationContainer: document.getElementById('pagination'),
            pageInfo: document.getElementById('page-info'),
            
            // Modal
            logModal: document.getElementById('log-modal'),
            modalContent: document.querySelector('.modal-content'),
            closeModalBtn: document.querySelector('.close-modal'),
            
            // Status indicators
            connectionStatus: document.getElementById('connection-status'),
            lastUpdate: document.getElementById('last-update'),
            
            // Theme toggle
            themeToggle: document.getElementById('theme-toggle')
        };
    }

    // Attach event listeners
    attachEventListeners() {
        // Control buttons
        if (this.elements.refreshBtn) {
            this.elements.refreshBtn.addEventListener('click', () => this.refreshData());
        }
        
        if (this.elements.exportBtn) {
            this.elements.exportBtn.addEventListener('click', () => this.exportLogs());
        }
        
        if (this.elements.filtersBtn) {
            this.elements.filtersBtn.addEventListener('click', () => this.toggleFiltersPanel());
        }
        
        // Filter controls
        if (this.elements.applyFiltersBtn) {
            this.elements.applyFiltersBtn.addEventListener('click', () => this.applyFilters());
        }
        
        if (this.elements.clearFiltersBtn) {
            this.elements.clearFiltersBtn.addEventListener('click', () => this.clearFilters());
        }
        
        // Search with debounce
        if (this.elements.searchFilter) {
            let searchTimeout;
            this.elements.searchFilter.addEventListener('input', (e) => {
                clearTimeout(searchTimeout);
                searchTimeout = setTimeout(() => {
                    this.currentFilters.search = e.target.value;
                    this.applyFilters();
                }, 500);
            });
        }
        
        // Modal controls
        if (this.elements.closeModalBtn) {
            this.elements.closeModalBtn.addEventListener('click', () => this.closeModal());
        }
        
        if (this.elements.logModal) {
            this.elements.logModal.addEventListener('click', (e) => {
                if (e.target === this.elements.logModal) {
                    this.closeModal();
                }
            });
        }
        
        // Theme toggle
        if (this.elements.themeToggle) {
            this.elements.themeToggle.addEventListener('click', () => this.toggleTheme());
        }
        
        // Keyboard shortcuts
        document.addEventListener('keydown', (e) => {
            if (e.key === 'Escape') {
                this.closeModal();
            } else if (e.ctrlKey && e.key === 'r') {
                e.preventDefault();
                this.refreshData();
            }
        });
    }

    // Setup connection monitoring
    setupConnectionMonitoring() {
        if (window.api) {
            window.api.on('connectionChange', (status) => {
                this.updateConnectionStatus(status);
            });
        }
    }

    // Load initial data
    async loadInitialData() {
        await Promise.all([
            this.loadStats(),
            this.loadLogs(),
            this.loadComponents()
        ]);
        
        // Initialize charts with loaded data
        this.initializeCharts();
    }

    // Load statistics
    async loadStats() {
        try {
            const response = await window.api.getStats();
            
            if (response.success) {
                this.cachedStats = response.data;
                this.updateStatsCards(response.data);
                this.updateLastRefresh();
            } else {
                console.error('Failed to load stats:', response.error);
            }
            
        } catch (error) {
            console.error('Error loading stats:', error);
        }
    }

    // Load logs
    async loadLogs(page = 1) {
        try {
            const params = {
                page: page,
                limit: this.pageSize,
                ...this.currentFilters
            };
            
            const response = await window.api.getLogs(params);
            
            if (response.success) {
                this.cachedLogs = response.data;
                this.currentPage = page;
                this.totalLogs = response.data.total || response.data.logs?.length || 0;
                
                this.updateLogsTable(response.data.logs || response.data);
                this.updatePagination();
                this.updateLastRefresh();
            } else {
                console.error('Failed to load logs:', response.error);
                this.showError('Failed to load logs');
            }
            
        } catch (error) {
            console.error('Error loading logs:', error);
            this.showError('Error loading logs');
        }
    }

    // Load components for filter
    async loadComponents() {
        try {
            const response = await window.api.getComponents();
            
            if (response.success && this.elements.componentFilter) {
                this.populateComponentFilter(response.data);
            }
            
        } catch (error) {
            console.error('Error loading components:', error);
        }
    }

    // Update stats cards
    updateStatsCards(stats) {
        if (this.elements.totalLogsCard) {
            this.elements.totalLogsCard.textContent = stats.total_logs || 0;
        }
        
        if (this.elements.errorsCard) {
            const errors = stats.severity_distribution?.ERROR || 0;
            this.elements.errorsCard.textContent = errors;
        }
        
        if (this.elements.warningsCard) {
            const warnings = stats.severity_distribution?.WARNING || 0;
            this.elements.warningsCard.textContent = warnings;
        }
        
        if (this.elements.systemStatusCard) {
            const status = window.api.getConnectionStatus();
            this.elements.systemStatusCard.textContent = status === 'connected' ? 'Online' : 'Offline';
            this.elements.systemStatusCard.className = `card ${status === 'connected' ? 'status-online' : 'status-offline'}`;
        }
    }

    // Update logs table
    updateLogsTable(logs) {
        if (!this.elements.logsTableBody) return;
        
        this.elements.logsTableBody.innerHTML = '';
        
        if (!logs || logs.length === 0) {
            const row = document.createElement('tr');
            row.innerHTML = '<td colspan="6" class="no-data">No logs found</td>';
            this.elements.logsTableBody.appendChild(row);
            return;
        }
        
        logs.forEach(log => {
            const row = this.createLogRow(log);
            this.elements.logsTableBody.appendChild(row);
        });
    }

    // Create log table row
    createLogRow(log) {
        const row = document.createElement('tr');
        row.className = `log-row level-${(log.level || 'INFO').toLowerCase()}`;
        row.dataset.logId = log.id;
        
        const timestamp = new Date(log.timestamp).toLocaleString();
        const level = log.level || 'INFO';
        const component = log.component || 'Unknown';
        const message = this.truncateMessage(log.message || '', 100);
        
        row.innerHTML = `
            <td>
                <input type="checkbox" class="log-checkbox" value="${log.id}">
            </td>
            <td class="timestamp">${timestamp}</td>
            <td class="level">
                <span class="level-badge level-${level.toLowerCase()}">${level}</span>
            </td>
            <td class="component">${component}</td>
            <td class="message">${message}</td>
            <td class="actions">
                <button class="btn btn-sm view-log" data-log-id="${log.id}">
                    <i class="fas fa-eye"></i>
                </button>
            </td>
        `;
        
        // Add click handlers
        const checkbox = row.querySelector('.log-checkbox');
        checkbox.addEventListener('change', (e) => {
            if (e.target.checked) {
                this.selectedLogs.add(log.id);
            } else {
                this.selectedLogs.delete(log.id);
            }
        });
        
        const viewBtn = row.querySelector('.view-log');
        viewBtn.addEventListener('click', () => this.viewLogDetails(log));
        
        return row;
    }

    // View log details in modal
    viewLogDetails(log) {
        if (!this.elements.logModal) return;
        
        const modalBody = this.elements.logModal.querySelector('.modal-body');
        if (modalBody) {
            modalBody.innerHTML = `
                <div class="log-detail">
                    <div class="log-header">
                        <h3>Log Details</h3>
                        <span class="level-badge level-${(log.level || 'INFO').toLowerCase()}">
                            ${log.level || 'INFO'}
                        </span>
                    </div>
                    
                    <div class="log-info">
                        <div class="info-row">
                            <strong>ID:</strong> ${log.id}
                        </div>
                        <div class="info-row">
                            <strong>Timestamp:</strong> ${new Date(log.timestamp).toLocaleString()}
                        </div>
                        <div class="info-row">
                            <strong>Component:</strong> ${log.component || 'Unknown'}
                        </div>
                        <div class="info-row">
                            <strong>Level:</strong> ${log.level || 'INFO'}
                        </div>
                    </div>
                    
                    <div class="log-message">
                        <strong>Message:</strong>
                        <pre>${log.message || 'No message'}</pre>
                    </div>
                    
                    ${log.details ? `
                        <div class="log-details">
                            <strong>Details:</strong>
                            <pre>${JSON.stringify(log.details, null, 2)}</pre>
                        </div>
                    ` : ''}
                </div>
            `;
        }
        
        this.elements.logModal.style.display = 'block';
        document.body.style.overflow = 'hidden';
    }

    // Close modal
    closeModal() {
        if (this.elements.logModal) {
            this.elements.logModal.style.display = 'none';
            document.body.style.overflow = 'auto';
        }
    }

    // Update pagination
    updatePagination() {
        if (!this.elements.paginationContainer) return;
        
        const totalPages = Math.ceil(this.totalLogs / this.pageSize);
        
        // Update page info
        if (this.elements.pageInfo) {
            const startItem = (this.currentPage - 1) * this.pageSize + 1;
            const endItem = Math.min(this.currentPage * this.pageSize, this.totalLogs);
            this.elements.pageInfo.textContent = `${startItem}-${endItem} of ${this.totalLogs}`;
        }
        
        // Create pagination buttons
        this.elements.paginationContainer.innerHTML = '';
        
        // Previous button
        const prevBtn = document.createElement('button');
        prevBtn.className = `btn ${this.currentPage === 1 ? 'disabled' : ''}`;
        prevBtn.innerHTML = '<i class="fas fa-chevron-left"></i>';
        prevBtn.disabled = this.currentPage === 1;
        prevBtn.addEventListener('click', () => {
            if (this.currentPage > 1) {
                this.loadLogs(this.currentPage - 1);
            }
        });
        this.elements.paginationContainer.appendChild(prevBtn);
        
        // Page numbers
        const startPage = Math.max(1, this.currentPage - 2);
        const endPage = Math.min(totalPages, this.currentPage + 2);
        
        for (let i = startPage; i <= endPage; i++) {
            const pageBtn = document.createElement('button');
            pageBtn.className = `btn ${i === this.currentPage ? 'active' : ''}`;
            pageBtn.textContent = i;
            pageBtn.addEventListener('click', () => this.loadLogs(i));
            this.elements.paginationContainer.appendChild(pageBtn);
        }
        
        // Next button
        const nextBtn = document.createElement('button');
        nextBtn.className = `btn ${this.currentPage === totalPages ? 'disabled' : ''}`;
        nextBtn.innerHTML = '<i class="fas fa-chevron-right"></i>';
        nextBtn.disabled = this.currentPage === totalPages;
        nextBtn.addEventListener('click', () => {
            if (this.currentPage < totalPages) {
                this.loadLogs(this.currentPage + 1);
            }
        });
        this.elements.paginationContainer.appendChild(nextBtn);
    }

    // Initialize charts
    initializeCharts() {
        if (window.ChartManager && this.cachedStats) {
            // Timeline chart
            window.ChartManager.createTimelineChart('timeline-chart', this.cachedStats.timeline || []);
            
            // Severity chart
            if (this.cachedLogs) {
                window.ChartManager.createSeverityChart('severity-chart', this.cachedLogs.logs || this.cachedLogs);
            }
            
            // Components chart
            window.ChartManager.createComponentsChart('components-chart', this.cachedStats.top_components || []);
            
            // Activity chart
            if (this.cachedLogs) {
                window.ChartManager.createActivityChart('activity-chart', this.cachedLogs.logs || this.cachedLogs);
            }
        }
    }

    // Toggle filters panel
    toggleFiltersPanel() {
        if (this.elements.filtersPanel) {
            this.elements.filtersPanel.classList.toggle('show');
        }
    }

    // Apply filters
    async applyFilters() {
        this.currentFilters = {};
        
        // Component filter
        if (this.elements.componentFilter && this.elements.componentFilter.value) {
            this.currentFilters.component = this.elements.componentFilter.value;
        }
        
        // Level filter
        if (this.elements.levelFilter && this.elements.levelFilter.value) {
            this.currentFilters.level = this.elements.levelFilter.value;
        }
        
        // Date filters
        if (this.elements.dateFromFilter && this.elements.dateFromFilter.value) {
            this.currentFilters.date_from = this.elements.dateFromFilter.value;
        }
        
        if (this.elements.dateToFilter && this.elements.dateToFilter.value) {
            this.currentFilters.date_to = this.elements.dateToFilter.value;
        }
        
        // Search filter
        if (this.elements.searchFilter && this.elements.searchFilter.value) {
            this.currentFilters.search = this.elements.searchFilter.value;
        }
        
        // Reset to first page and load
        this.currentPage = 1;
        await this.loadLogs(1);
        
        // Hide filters panel
        if (this.elements.filtersPanel) {
            this.elements.filtersPanel.classList.remove('show');
        }
        
        this.showToast('Filters applied', 'success');
    }

    // Clear filters
    async clearFilters() {
        this.currentFilters = {};
        
        // Clear form inputs
        if (this.elements.componentFilter) this.elements.componentFilter.value = '';
        if (this.elements.levelFilter) this.elements.levelFilter.value = '';
        if (this.elements.dateFromFilter) this.elements.dateFromFilter.value = '';
        if (this.elements.dateToFilter) this.elements.dateToFilter.value = '';
        if (this.elements.searchFilter) this.elements.searchFilter.value = '';
        
        // Reset to first page and load
        this.currentPage = 1;
        await this.loadLogs(1);
        
        this.showToast('Filters cleared', 'info');
    }

    // Populate component filter
    populateComponentFilter(components) {
        if (!this.elements.componentFilter) return;
        
        this.elements.componentFilter.innerHTML = '<option value="">All Components</option>';
        
        components.forEach(component => {
            const option = document.createElement('option');
            option.value = component;
            option.textContent = component;
            this.elements.componentFilter.appendChild(option);
        });
    }

    // Refresh all data
    async refreshData() {
        if (this.elements.refreshBtn) {
            this.elements.refreshBtn.classList.add('loading');
        }
        
        try {
            // Clear cache to force fresh data
            if (window.api) {
                window.api.clearCache();
            }
            
            await this.loadInitialData();
            this.showToast('Data refreshed', 'success');
            
        } catch (error) {
            console.error('Error refreshing data:', error);
            this.showToast('Failed to refresh data', 'error');
        } finally {
            if (this.elements.refreshBtn) {
                this.elements.refreshBtn.classList.remove('loading');
            }
        }
    }

    // Export logs
    async exportLogs() {
        try {
            const response = await window.api.exportLogs(this.currentFilters);
            
            if (response.success) {
                this.downloadCSV(response.data, response.filename);
                this.showToast('Logs exported successfully', 'success');
            } else {
                this.showToast('Failed to export logs', 'error');
            }
            
        } catch (error) {
            console.error('Error exporting logs:', error);
            this.showToast('Error exporting logs', 'error');
        }
    }

    // Download CSV file
    downloadCSV(data, filename) {
        const csv = this.convertToCSV(data);
        const blob = new Blob([csv], { type: 'text/csv' });
        const url = window.URL.createObjectURL(blob);
        
        const link = document.createElement('a');
        link.href = url;
        link.download = filename || 'logs.csv';
        link.click();
        
        window.URL.revokeObjectURL(url);
    }

    // Convert data to CSV
    convertToCSV(data) {
        if (!data || data.length === 0) return '';
        
        const headers = ['ID', 'Timestamp', 'Level', 'Component', 'Message'];
        const rows = data.map(log => [
            log.id || '',
            log.timestamp || '',
            log.level || '',
            log.component || '',
            `"${(log.message || '').replace(/"/g, '""')}"`
        ]);
        
        return [headers.join(','), ...rows.map(row => row.join(','))].join('\n');
    }

    // Start auto-refresh
    startAutoRefresh() {
        if (this.refreshTimer) {
            clearInterval(this.refreshTimer);
        }
        
        this.refreshTimer = setInterval(async () => {
            await this.loadStats();
            
            // Only refresh logs if no filters are applied to avoid disrupting user
            if (Object.keys(this.currentFilters).length === 0) {
                await this.loadLogs(this.currentPage);
            }
        }, DashboardConfig.INTERVALS.DATA_REFRESH);
    }

    // Stop auto-refresh
    stopAutoRefresh() {
        if (this.refreshTimer) {
            clearInterval(this.refreshTimer);
            this.refreshTimer = null;
        }
    }

    // Update connection status
    updateConnectionStatus(status) {
        this.connectionStatus = status;
        
        if (this.elements.connectionStatus) {
            this.elements.connectionStatus.textContent = status;
            this.elements.connectionStatus.className = `status status-${status}`;
        }
    }

    // Update last refresh time
    updateLastRefresh() {
        if (this.elements.lastUpdate) {
            this.elements.lastUpdate.textContent = new Date().toLocaleTimeString();
        }
    }

    // Toggle theme
    toggleTheme() {
        const isDark = document.body.classList.toggle('dark-theme');
        
        // Save theme preference
        if (window.DashboardUtils) {
            window.DashboardUtils.setPreference('theme', isDark ? 'dark' : 'light');
        }
        
        // Update charts theme
        if (window.ChartManager) {
            window.ChartManager.updateTheme(isDark);
        }
    }

    // Utility methods
    truncateMessage(message, maxLength = 100) {
        if (message.length <= maxLength) return message;
        return message.substring(0, maxLength) + '...';
    }

    showToast(message, type = 'info') {
        if (window.DashboardUtils) {
            window.DashboardUtils.showToast(message, type);
        }
    }

    showError(message) {
        this.showToast(message, 'error');
    }

    // Cleanup
    destroy() {
        this.stopAutoRefresh();
        
        if (window.ChartManager) {
            window.ChartManager.destroyAllCharts();
        }
        
        this.selectedLogs.clear();
        this.isInitialized = false;
    }
}

// Initialize dashboard when DOM is ready
document.addEventListener('DOMContentLoaded', () => {
    window.dashboard = new Dashboard();
});