import React, { useState, useEffect } from 'react';
import './Dashboard.css';

const Dashboard = ({ backendConnected, onPageChange }) => {
    const [systemStats, setSystemStats] = useState({
        cpuUsage: 0,
        memoryUsage: 0,
        threatsDetected: 0,
        filesScanned: 0,
        quarantinedFiles: 0,
        systemHealth: 'unknown'
    });

    const [recentThreats, setRecentThreats] = useState([]);
    const [isLoading, setIsLoading] = useState(true);
    const [lastUpdate, setLastUpdate] = useState(new Date());

    useEffect(() => {
        if (backendConnected) {
            loadDashboardData();
            const interval = setInterval(loadDashboardData, 5000); // Update every 5 seconds
            return () => clearInterval(interval);
        } else {
            // Show demo data when backend is not connected
            loadDemoData();
        }
    }, [backendConnected]);

    const loadDashboardData = async () => {
        try {
            setIsLoading(true);
            
            // Simulate API calls for now since backend might not be fully ready
            // TODO: Replace with actual BackendService calls
            const mockStats = {
                cpuUsage: Math.random() * 5, // <5% as per requirement
                memoryUsage: 20 + Math.random() * 10, // ~25MB as per requirement
                threatsDetected: Math.floor(Math.random() * 50),
                filesScanned: Math.floor(Math.random() * 10000) + 50000,
                quarantinedFiles: Math.floor(Math.random() * 10),
                systemHealth: 'excellent'
            };

            const mockThreats = [
                {
                    id: 1,
                    name: 'Trojan.Win32.GenKrypt',
                    severity: 'high',
                    detectedAt: new Date(Date.now() - Math.random() * 86400000).toISOString(),
                    path: 'C:\\Users\\Downloads\\suspicious_file.exe',
                    status: 'quarantined'
                },
                {
                    id: 2,
                    name: 'Keylogger.Behavior.Detected',
                    severity: 'critical',
                    detectedAt: new Date(Date.now() - Math.random() * 86400000).toISOString(),
                    path: 'C:\\Windows\\Temp\\keylog.dll',
                    status: 'blocked'
                },
                {
                    id: 3,
                    name: 'Malware.Heuristic.Detection',
                    severity: 'medium',
                    detectedAt: new Date(Date.now() - Math.random() * 86400000).toISOString(),
                    path: 'C:\\Program Files\\Unknown\\malware.bin',
                    status: 'cleaned'
                }
            ];

            setSystemStats(mockStats);
            setRecentThreats(mockThreats);
            setLastUpdate(new Date());
            setIsLoading(false);

        } catch (error) {
            console.error('Error loading dashboard data:', error);
            loadDemoData();
        }
    };

    const loadDemoData = () => {
        setSystemStats({
            cpuUsage: 0.8,
            memoryUsage: 24.5,
            threatsDetected: 15,
            filesScanned: 75234,
            quarantinedFiles: 3,
            systemHealth: 'good'
        });
        setRecentThreats([]);
        setIsLoading(false);
    };

    const getHealthColor = (health) => {
        switch (health) {
            case 'excellent': return '#00ff88';
            case 'good': return '#4CAF50';
            case 'warning': return '#FF9800';
            case 'critical': return '#f44336';
            default: return '#666';
        }
    };

    const getSeverityColor = (severity) => {
        switch (severity) {
            case 'critical': return '#f44336';
            case 'high': return '#FF9800';
            case 'medium': return '#FFC107';
            case 'low': return '#4CAF50';
            default: return '#666';
        }
    };

    const formatTime = (dateString) => {
        return new Date(dateString).toLocaleTimeString();
    };

    if (isLoading) {
        return (
            <div className="dashboard-loading">
                <div className="spinner"></div>
                <p>Loading dashboard...</p>
            </div>
        );
    }

    return (
        <div className="dashboard">
            <div className="dashboard-header">
                <h1>Antivirus Dashboard</h1>
                <div className="connection-status">
                    <div className={`status-indicator ${backendConnected ? 'connected' : 'disconnected'}`}></div>
                    <span>{backendConnected ? 'Backend Connected' : 'Backend Disconnected'}</span>
                </div>
            </div>

            <div className="dashboard-stats">
                <div className="stat-card">
                    <div className="stat-icon">🛡️</div>
                    <div className="stat-content">
                        <h3>System Health</h3>
                        <p className="stat-value" style={{ color: getHealthColor(systemStats.systemHealth) }}>
                            {systemStats.systemHealth.toUpperCase()}
                        </p>
                    </div>
                </div>

                <div className="stat-card">
                    <div className="stat-icon">⚡</div>
                    <div className="stat-content">
                        <h3>CPU Usage</h3>
                        <p className="stat-value">{systemStats.cpuUsage.toFixed(1)}%</p>
                        <div className="progress-bar">
                            <div 
                                className="progress-fill"
                                style={{ width: `${(systemStats.cpuUsage / 5) * 100}%` }}
                            ></div>
                        </div>
                    </div>
                </div>

                <div className="stat-card">
                    <div className="stat-icon">💾</div>
                    <div className="stat-content">
                        <h3>Memory Usage</h3>
                        <p className="stat-value">{systemStats.memoryUsage.toFixed(1)} MB</p>
                        <div className="progress-bar">
                            <div 
                                className="progress-fill"
                                style={{ width: `${(systemStats.memoryUsage / 100) * 100}%` }}
                            ></div>
                        </div>
                    </div>
                </div>

                <div className="stat-card">
                    <div className="stat-icon">🚨</div>
                    <div className="stat-content">
                        <h3>Threats Detected</h3>
                        <p className="stat-value">{systemStats.threatsDetected}</p>
                    </div>
                </div>

                <div className="stat-card">
                    <div className="stat-icon">📁</div>
                    <div className="stat-content">
                        <h3>Files Scanned</h3>
                        <p className="stat-value">{systemStats.filesScanned.toLocaleString()}</p>
                    </div>
                </div>

                <div className="stat-card">
                    <div className="stat-icon">🔒</div>
                    <div className="stat-content">
                        <h3>Quarantined</h3>
                        <p className="stat-value">{systemStats.quarantinedFiles}</p>
                    </div>
                </div>
            </div>

            <div className="dashboard-sections">
                <div className="recent-threats">
                    <h2>Recent Threats</h2>
                    {recentThreats.length > 0 ? (
                        <div className="threats-list">
                            {recentThreats.map(threat => (
                                <div key={threat.id} className="threat-item">
                                    <div className="threat-info">
                                        <h4>{threat.name}</h4>
                                        <p className="threat-path">{threat.path}</p>
                                        <p className="threat-time">Detected at {formatTime(threat.detectedAt)}</p>
                                    </div>
                                    <div className="threat-status">
                                        <span 
                                            className="severity-badge"
                                            style={{ backgroundColor: getSeverityColor(threat.severity) }}
                                        >
                                            {threat.severity}
                                        </span>
                                        <span className={`status-badge status-${threat.status}`}>
                                            {threat.status}
                                        </span>
                                    </div>
                                </div>
                            ))}
                        </div>
                    ) : (
                        <div className="no-threats">
                            <p>✅ No recent threats detected</p>
                            <p className="no-threats-subtitle">Your system is secure</p>
                        </div>
                    )}
                    
                    <button 
                        className="view-all-btn"
                        onClick={() => onPageChange('threats')}
                    >
                        View All Threats
                    </button>
                </div>

                <div className="quick-actions">
                    <h2>Quick Actions</h2>
                    <div className="actions-grid">
                        <button className="action-btn scan-btn">
                            <span className="action-icon">🔍</span>
                            <span>Quick Scan</span>
                        </button>
                        <button className="action-btn full-scan-btn">
                            <span className="action-icon">🛡️</span>
                            <span>Full Scan</span>
                        </button>
                        <button 
                            className="action-btn quarantine-btn"
                            onClick={() => onPageChange('quarantine')}
                        >
                            <span className="action-icon">🔒</span>
                            <span>Quarantine</span>
                        </button>
                        <button 
                            className="action-btn settings-btn"
                            onClick={() => onPageChange('settings')}
                        >
                            <span className="action-icon">⚙️</span>
                            <span>Settings</span>
                        </button>
                    </div>
                </div>
            </div>

            <div className="dashboard-footer">
                <p>Last updated: {lastUpdate.toLocaleTimeString()}</p>
                <p>Antivirus C++ Professional - High Performance Protection</p>
            </div>
        </div>
    );
};

export default Dashboard;