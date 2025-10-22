import React, { useState, useEffect } from 'react';
import './Header.css';

const Header = ({ systemInfo, backendConnected, currentPage }) => {
    const [currentTime, setCurrentTime] = useState(new Date());
    const [notificationsCount, setNotificationsCount] = useState(3);

    useEffect(() => {
        const timer = setInterval(() => {
            setCurrentTime(new Date());
        }, 1000);

        return () => clearInterval(timer);
    }, []);

    const getPageTitle = (page) => {
        const titles = {
            dashboard: 'Dashboard',
            protection: 'Real-time Protection',
            threats: 'Threat Management',
            quarantine: 'Quarantine Manager',
            reports: 'Security Reports',
            settings: 'System Settings'
        };
        return titles[page] || 'Dashboard';
    };

    const getPageIcon = (page) => {
        const icons = {
            dashboard: '🏠',
            protection: '🛡️',
            threats: '🚨',
            quarantine: '🔒',
            reports: '📊',
            settings: '⚙️'
        };
        return icons[page] || '🏠';
    };

    const formatTime = (date) => {
        return date.toLocaleTimeString('en-US', {
            hour12: false,
            hour: '2-digit',
            minute: '2-digit',
            second: '2-digit'
        });
    };

    const formatDate = (date) => {
        return date.toLocaleDateString('en-US', {
            weekday: 'long',
            year: 'numeric',
            month: 'long',
            day: 'numeric'
        });
    };

    return (
        <header className="header">
            <div className="header-left">
                <div className="page-info">
                    <span className="page-icon">{getPageIcon(currentPage)}</span>
                    <div className="page-text">
                        <h1 className="page-title">{getPageTitle(currentPage)}</h1>
                        <span className="page-breadcrumb">Antivirus C++ / {getPageTitle(currentPage)}</span>
                    </div>
                </div>
            </div>

            <div className="header-center">
                <div className="system-stats">
                    <div className="stat-item">
                        <span className="stat-icon">⚡</span>
                        <span className="stat-label">CPU</span>
                        <span className="stat-value">0.8%</span>
                    </div>
                    <div className="stat-item">
                        <span className="stat-icon">💾</span>
                        <span className="stat-label">RAM</span>
                        <span className="stat-value">24.5MB</span>
                    </div>
                    <div className="stat-item">
                        <span className="stat-icon">🛡️</span>
                        <span className="stat-label">Status</span>
                        <span className={`stat-value ${backendConnected ? 'protected' : 'offline'}`}>
                            {backendConnected ? 'Protected' : 'Offline'}
                        </span>
                    </div>
                </div>
            </div>

            <div className="header-right">
                <div className="header-controls">
                    <div className="notification-center">
                        <button className="notification-btn">
                            <span className="notification-icon">🔔</span>
                            {notificationsCount > 0 && (
                                <span className="notification-count">{notificationsCount}</span>
                            )}
                        </button>
                    </div>

                    <div className="system-menu">
                        <button className="system-menu-btn">
                            <span className="system-menu-icon">⋯</span>
                        </button>
                    </div>

                    <div className="window-controls">
                        <button 
                            className="window-control minimize"
                            onClick={() => window.electronAPI && window.electronAPI.minimizeWindow()}
                            title="Minimize"
                        >
                            ─
                        </button>
                        <button 
                            className="window-control maximize"
                            onClick={() => window.electronAPI && window.electronAPI.toggleMaximize()}
                            title="Maximize"
                        >
                            ⬜
                        </button>
                        <button 
                            className="window-control close"
                            onClick={() => window.electronAPI && window.electronAPI.closeWindow()}
                            title="Close"
                        >
                            ✕
                        </button>
                    </div>
                </div>

                <div className="time-display">
                    <div className="current-time">{formatTime(currentTime)}</div>
                    <div className="current-date">{formatDate(currentTime)}</div>
                </div>
            </div>
        </header>
    );
};

export default Header;