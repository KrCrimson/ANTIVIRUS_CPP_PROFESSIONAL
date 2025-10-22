import React from 'react';
import { Link, useLocation } from 'react-router-dom';
import './Sidebar.css';

const Sidebar = ({ currentPage, onPageChange, backendConnected }) => {
    const location = useLocation();
    
    const menuItems = [
        {
            id: 'dashboard',
            path: '/',
            icon: '🏠',
            label: 'Dashboard',
            description: 'System overview'
        },
        {
            id: 'protection',
            path: '/protection',
            icon: '🛡️',
            label: 'Real-time Protection',
            description: 'Live monitoring'
        },
        {
            id: 'threats',
            path: '/threats',
            icon: '🚨',
            label: 'Threats',
            description: 'Detected threats'
        },
        {
            id: 'quarantine',
            path: '/quarantine',
            icon: '🔒',
            label: 'Quarantine',
            description: 'Isolated files'
        },
        {
            id: 'reports',
            path: '/reports',
            icon: '📊',
            label: 'Reports',
            description: 'Security reports'
        },
        {
            id: 'settings',
            path: '/settings',
            icon: '⚙️',
            label: 'Settings',
            description: 'Configuration'
        }
    ];

    const isActive = (path) => {
        if (path === '/') {
            return location.pathname === '/';
        }
        return location.pathname.startsWith(path);
    };

    return (
        <div className="sidebar">
            <div className="sidebar-header">
                <div className="logo">
                    <div className="logo-icon">🛡️</div>
                    <div className="logo-text">
                        <h2>Antivirus</h2>
                        <span>C++ Pro</span>
                    </div>
                </div>
                
                <div className={`connection-indicator ${backendConnected ? 'connected' : 'disconnected'}`}>
                    <div className="indicator-dot"></div>
                    <span className="indicator-text">
                        {backendConnected ? 'Protected' : 'Offline'}
                    </span>
                </div>
            </div>

            <nav className="sidebar-nav">
                {menuItems.map((item) => (
                    <Link
                        key={item.id}
                        to={item.path}
                        className={`nav-item ${isActive(item.path) ? 'active' : ''}`}
                        onClick={() => onPageChange && onPageChange(item.id)}
                    >
                        <div className="nav-icon">{item.icon}</div>
                        <div className="nav-content">
                            <span className="nav-label">{item.label}</span>
                            <span className="nav-description">{item.description}</span>
                        </div>
                        <div className="nav-arrow">›</div>
                    </Link>
                ))}
            </nav>

            <div className="sidebar-footer">
                <div className="system-status">
                    <h3>System Status</h3>
                    <div className="status-items">
                        <div className="status-item">
                            <span className="status-label">CPU</span>
                            <span className="status-value">0.8%</span>
                        </div>
                        <div className="status-item">
                            <span className="status-label">Memory</span>
                            <span className="status-value">24.5MB</span>
                        </div>
                        <div className="status-item">
                            <span className="status-label">Uptime</span>
                            <span className="status-value">2h 15m</span>
                        </div>
                    </div>
                </div>
                
                <div className="version-info">
                    <p>Version 1.0.0</p>
                    <p className="build-info">Build 20251022</p>
                </div>
            </div>
        </div>
    );
};

export default Sidebar;