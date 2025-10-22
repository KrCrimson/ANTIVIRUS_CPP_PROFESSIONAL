import React from 'react';

const Header = ({ isConnected, lastUpdate, version }) => {
  return (
    <header className="dashboard-header">
      <div className="header-left">
        <h1 className="app-title">
          🛡️ Antivirus Professional C++
        </h1>
        <span className="version-badge">v{version}</span>
      </div>
      
      <div className="header-center">
        <div className="status-indicator">
          <div className={`status-dot ${isConnected ? 'online' : 'offline'}`}></div>
          <span className="status-text">
            {isConnected ? 'Sistema Activo' : 'Modo Desarrollo'}
          </span>
        </div>
      </div>
      
      <div className="header-right">
        <div className="last-update">
          <span className="update-label">Última actualización:</span>
          <span className="update-time">
            {lastUpdate.toLocaleTimeString()}
          </span>
        </div>
        
        <div className="header-actions">
          <button className="settings-btn" title="Configuración">
            ⚙️
          </button>
          
          <button className="minimize-btn" title="Minimizar">
            ➖
          </button>
          
          <button className="close-btn" title="Cerrar">
            ❌
          </button>
        </div>
      </div>
    </header>
  );
};

export default Header;