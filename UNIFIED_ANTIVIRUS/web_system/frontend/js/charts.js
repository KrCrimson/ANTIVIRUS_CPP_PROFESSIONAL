// ====================================
//   Chart.js Integration for Dashboard
// ====================================

class ChartManager {
    constructor() {
        this.charts = new Map();
        this.updateInterval = null;
        this.isAutoUpdateEnabled = false;
        
        // Chart color schemes
        this.colorSchemes = {
            primary: ['#3B82F6', '#10B981', '#F59E0B', '#EF4444', '#8B5CF6'],
            secondary: ['#60A5FA', '#34D399', '#FBBF24', '#F87171', '#A78BFA'],
            gradient: {
                blue: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
                green: 'linear-gradient(135deg, #f093fb 0%, #f5576c 100%)',
                orange: 'linear-gradient(135deg, #4facfe 0%, #00f2fe 100%)',
                red: 'linear-gradient(135deg, #43e97b 0%, #38f9d7 100%)'
            }
        };

        this.initializeChartDefaults();
    }

    initializeChartDefaults() {
        // Set Chart.js global defaults
        if (typeof Chart !== 'undefined') {
            Chart.defaults.responsive = true;
            Chart.defaults.maintainAspectRatio = false;
            Chart.defaults.plugins.legend.display = true;
            Chart.defaults.plugins.legend.position = 'top';
            Chart.defaults.color = getComputedStyle(document.documentElement)
                .getPropertyValue('--text-color').trim();
        }
    }

    // Create log timeline chart
    createTimelineChart(canvasId, data = []) {
        const ctx = document.getElementById(canvasId);
        if (!ctx) return null;

        const chart = new Chart(ctx, {
            type: 'line',
            data: {
                labels: data.map(item => item.time || item.label),
                datasets: [{
                    label: 'Logs Over Time',
                    data: data.map(item => item.count || item.value),
                    borderColor: '#3B82F6',
                    backgroundColor: 'rgba(59, 130, 246, 0.1)',
                    borderWidth: 2,
                    fill: true,
                    tension: 0.4,
                    pointBackgroundColor: '#3B82F6',
                    pointBorderColor: '#ffffff',
                    pointBorderWidth: 2,
                    pointRadius: 4,
                    pointHoverRadius: 6
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                interaction: {
                    intersect: false,
                    mode: 'index'
                },
                plugins: {
                    legend: {
                        display: true,
                        position: 'top',
                        labels: {
                            usePointStyle: true,
                            padding: 20
                        }
                    },
                    tooltip: {
                        backgroundColor: 'rgba(0, 0, 0, 0.8)',
                        titleColor: '#ffffff',
                        bodyColor: '#ffffff',
                        borderColor: '#3B82F6',
                        borderWidth: 1,
                        cornerRadius: 6,
                        displayColors: true
                    }
                },
                scales: {
                    x: {
                        grid: {
                            color: 'rgba(0, 0, 0, 0.1)',
                            drawBorder: false
                        },
                        ticks: {
                            maxTicksLimit: 10
                        }
                    },
                    y: {
                        beginAtZero: true,
                        grid: {
                            color: 'rgba(0, 0, 0, 0.1)',
                            drawBorder: false
                        },
                        ticks: {
                            stepSize: 1
                        }
                    }
                },
                animation: {
                    duration: 1000,
                    easing: 'easeInOutCubic'
                }
            }
        });

        this.charts.set(canvasId, chart);
        return chart;
    }

    // Create severity distribution donut chart
    createSeverityChart(canvasId, data = []) {
        const ctx = document.getElementById(canvasId);
        if (!ctx) return null;

        // Prepare data for donut chart
        const severityData = this.prepareSeverityData(data);

        const chart = new Chart(ctx, {
            type: 'doughnut',
            data: {
                labels: severityData.labels,
                datasets: [{
                    data: severityData.values,
                    backgroundColor: [
                        '#EF4444', // ERROR - Red
                        '#F59E0B', // WARNING - Orange
                        '#3B82F6', // INFO - Blue
                        '#10B981'  // DEBUG - Green
                    ],
                    borderColor: '#ffffff',
                    borderWidth: 2,
                    hoverBorderWidth: 3
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                cutout: '60%',
                plugins: {
                    legend: {
                        position: 'right',
                        labels: {
                            usePointStyle: true,
                            padding: 20,
                            generateLabels: function(chart) {
                                const data = chart.data;
                                return data.labels.map((label, index) => ({
                                    text: `${label}: ${data.datasets[0].data[index]}`,
                                    fillStyle: data.datasets[0].backgroundColor[index],
                                    strokeStyle: data.datasets[0].borderColor,
                                    lineWidth: data.datasets[0].borderWidth,
                                    pointStyle: 'circle',
                                    hidden: false,
                                    index: index
                                }));
                            }
                        }
                    },
                    tooltip: {
                        callbacks: {
                            label: function(context) {
                                const total = context.dataset.data.reduce((a, b) => a + b, 0);
                                const percentage = ((context.parsed / total) * 100).toFixed(1);
                                return `${context.label}: ${context.parsed} (${percentage}%)`;
                            }
                        }
                    }
                },
                animation: {
                    animateRotate: true,
                    animateScale: false
                }
            }
        });

        this.charts.set(canvasId, chart);
        return chart;
    }

    // Create components distribution bar chart
    createComponentsChart(canvasId, data = []) {
        const ctx = document.getElementById(canvasId);
        if (!ctx) return null;

        const chart = new Chart(ctx, {
            type: 'bar',
            data: {
                labels: data.map(item => item.component || item.label),
                datasets: [{
                    label: 'Logs by Component',
                    data: data.map(item => item.count || item.value),
                    backgroundColor: this.colorSchemes.primary,
                    borderColor: this.colorSchemes.secondary,
                    borderWidth: 1,
                    borderRadius: 4,
                    borderSkipped: false
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                indexAxis: 'y', // Horizontal bar chart
                plugins: {
                    legend: {
                        display: false
                    },
                    tooltip: {
                        callbacks: {
                            label: function(context) {
                                return `${context.label}: ${context.parsed.x} logs`;
                            }
                        }
                    }
                },
                scales: {
                    x: {
                        beginAtZero: true,
                        grid: {
                            color: 'rgba(0, 0, 0, 0.1)'
                        },
                        ticks: {
                            stepSize: 1
                        }
                    },
                    y: {
                        grid: {
                            display: false
                        }
                    }
                },
                animation: {
                    duration: 1200,
                    easing: 'easeOutBounce'
                }
            }
        });

        this.charts.set(canvasId, chart);
        return chart;
    }

    // Create real-time activity chart
    createActivityChart(canvasId, data = []) {
        const ctx = document.getElementById(canvasId);
        if (!ctx) return null;

        // Generate hourly activity data
        const activityData = this.generateHourlyActivity(data);

        const chart = new Chart(ctx, {
            type: 'bar',
            data: {
                labels: activityData.labels,
                datasets: [{
                    label: 'Activity Level',
                    data: activityData.values,
                    backgroundColor: function(context) {
                        const value = context.parsed.y;
                        if (value > 50) return '#EF4444';      // High - Red
                        if (value > 20) return '#F59E0B';      // Medium - Orange
                        if (value > 5) return '#3B82F6';       // Low - Blue
                        return '#10B981';                       // Minimal - Green
                    },
                    borderColor: 'rgba(255, 255, 255, 0.8)',
                    borderWidth: 1,
                    borderRadius: 2
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: {
                        display: false
                    },
                    tooltip: {
                        callbacks: {
                            title: function(context) {
                                return `Hour: ${context[0].label}:00`;
                            },
                            label: function(context) {
                                const level = context.parsed.y > 50 ? 'High' :
                                            context.parsed.y > 20 ? 'Medium' :
                                            context.parsed.y > 5 ? 'Low' : 'Minimal';
                                return `Activity: ${context.parsed.y} logs (${level})`;
                            }
                        }
                    }
                },
                scales: {
                    x: {
                        grid: {
                            display: false
                        },
                        ticks: {
                            maxTicksLimit: 12
                        }
                    },
                    y: {
                        beginAtZero: true,
                        grid: {
                            color: 'rgba(0, 0, 0, 0.1)'
                        },
                        ticks: {
                            stepSize: 10
                        }
                    }
                }
            }
        });

        this.charts.set(canvasId, chart);
        return chart;
    }

    // Update existing chart data
    updateChart(canvasId, newData) {
        const chart = this.charts.get(canvasId);
        if (!chart) return false;

        try {
            switch (chart.config.type) {
                case 'line':
                    this.updateTimelineChart(chart, newData);
                    break;
                case 'doughnut':
                    this.updateSeverityChart(chart, newData);
                    break;
                case 'bar':
                    if (chart.options.indexAxis === 'y') {
                        this.updateComponentsChart(chart, newData);
                    } else {
                        this.updateActivityChart(chart, newData);
                    }
                    break;
            }
            
            chart.update('active');
            return true;
            
        } catch (error) {
            console.error('Error updating chart:', error);
            return false;
        }
    }

    // Update timeline chart data
    updateTimelineChart(chart, data) {
        chart.data.labels = data.map(item => item.time || item.label);
        chart.data.datasets[0].data = data.map(item => item.count || item.value);
    }

    // Update severity chart data
    updateSeverityChart(chart, data) {
        const severityData = this.prepareSeverityData(data);
        chart.data.labels = severityData.labels;
        chart.data.datasets[0].data = severityData.values;
    }

    // Update components chart data
    updateComponentsChart(chart, data) {
        chart.data.labels = data.map(item => item.component || item.label);
        chart.data.datasets[0].data = data.map(item => item.count || item.value);
    }

    // Update activity chart data
    updateActivityChart(chart, data) {
        const activityData = this.generateHourlyActivity(data);
        chart.data.labels = activityData.labels;
        chart.data.datasets[0].data = activityData.values;
    }

    // Destroy a chart
    destroyChart(canvasId) {
        const chart = this.charts.get(canvasId);
        if (chart) {
            chart.destroy();
            this.charts.delete(canvasId);
        }
    }

    // Destroy all charts
    destroyAllCharts() {
        this.charts.forEach((chart, canvasId) => {
            chart.destroy();
        });
        this.charts.clear();
    }

    // Prepare severity distribution data
    prepareSeverityData(logs) {
        const severityCounts = { ERROR: 0, WARNING: 0, INFO: 0, DEBUG: 0 };
        
        logs.forEach(log => {
            const severity = (log.level || log.severity || 'INFO').toUpperCase();
            if (severityCounts.hasOwnProperty(severity)) {
                severityCounts[severity]++;
            }
        });

        return {
            labels: Object.keys(severityCounts),
            values: Object.values(severityCounts)
        };
    }

    // Generate hourly activity data
    generateHourlyActivity(logs) {
        const hours = Array.from({ length: 24 }, (_, i) => i.toString().padStart(2, '0'));
        const hourCounts = new Array(24).fill(0);

        logs.forEach(log => {
            const timestamp = new Date(log.timestamp);
            if (!isNaN(timestamp.getTime())) {
                const hour = timestamp.getHours();
                hourCounts[hour]++;
            }
        });

        return {
            labels: hours,
            values: hourCounts
        };
    }

    // Start auto-update for all charts
    startAutoUpdate(interval = 30000) {
        if (this.updateInterval) {
            clearInterval(this.updateInterval);
        }

        this.isAutoUpdateEnabled = true;
        this.updateInterval = setInterval(async () => {
            await this.refreshAllCharts();
        }, interval);
    }

    // Stop auto-update
    stopAutoUpdate() {
        if (this.updateInterval) {
            clearInterval(this.updateInterval);
            this.updateInterval = null;
        }
        this.isAutoUpdateEnabled = false;
    }

    // Refresh all charts with new data
    async refreshAllCharts() {
        if (!this.isAutoUpdateEnabled) return;

        try {
            // Get fresh data from API
            const statsResponse = await window.api.getStats({}, false);
            const logsResponse = await window.api.getRecentLogs(100);

            if (statsResponse.success && logsResponse.success) {
                const stats = statsResponse.data;
                const logs = logsResponse.data.logs || logsResponse.data;

                // Update each chart
                this.charts.forEach((chart, canvasId) => {
                    if (canvasId.includes('timeline')) {
                        this.updateChart(canvasId, stats.timeline || []);
                    } else if (canvasId.includes('severity')) {
                        this.updateChart(canvasId, logs);
                    } else if (canvasId.includes('components')) {
                        this.updateChart(canvasId, stats.top_components || []);
                    } else if (canvasId.includes('activity')) {
                        this.updateChart(canvasId, logs);
                    }
                });
            }

        } catch (error) {
            console.error('Error refreshing charts:', error);
        }
    }

    // Get chart by ID
    getChart(canvasId) {
        return this.charts.get(canvasId);
    }

    // Get all chart instances
    getAllCharts() {
        return Array.from(this.charts.values());
    }

    // Export chart as image
    exportChart(canvasId, filename) {
        const chart = this.charts.get(canvasId);
        if (!chart) return false;

        try {
            const url = chart.toBase64Image();
            const link = document.createElement('a');
            link.download = filename || `chart_${canvasId}_${Date.now()}.png`;
            link.href = url;
            link.click();
            return true;
        } catch (error) {
            console.error('Error exporting chart:', error);
            return false;
        }
    }

    // Update chart theme (for dark/light mode)
    updateTheme(isDark) {
        const textColor = isDark ? '#ffffff' : '#1f2937';
        const gridColor = isDark ? 'rgba(255, 255, 255, 0.1)' : 'rgba(0, 0, 0, 0.1)';

        this.charts.forEach(chart => {
            chart.options.color = textColor;
            
            if (chart.options.scales) {
                Object.keys(chart.options.scales).forEach(scaleKey => {
                    if (chart.options.scales[scaleKey].grid) {
                        chart.options.scales[scaleKey].grid.color = gridColor;
                    }
                });
            }
            
            chart.update('none');
        });
    }
}

// Create global chart manager instance
window.ChartManager = new ChartManager();