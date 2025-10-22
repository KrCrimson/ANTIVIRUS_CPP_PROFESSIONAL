import React from 'react';

const SystemMetrics = ({ systemStatus, isConnected }) => {
  // Función para determinar el color basado en el valor
  const getMetricColor = (value, type) => {
    switch (type) {
      case 'cpu':
        if (value < 2) return '#4CAF50'; // Verde
        if (value < 5) return '#FF9800'; // Naranja  
        return '#F44336'; // Rojo
      case 'memory':
        if (value < 50) return '#4CAF50'; // Verde
        if (value < 100) return '#FF9800'; // Naranja
        return '#F44336'; // Rojo
      default:
        return '#2196F3'; // Azul por defecto
    }
  };
  
  // Función para formatear bytes a MB
  const formatMemory = (mb) => {
    if (mb < 1024) return `${mb.toFixed(0)}MB`;
    return `${(mb / 1024).toFixed(1)}GB`;
  };
  
  // Función para obtener el estado del sistema con emoji
  const getSystemStateEmoji = (state) => {
    if (!isConnected) return '🔧';
    
    switch (state?.toLowerCase()) {
      case 'running':
      case 'active':
        return '✅';
      case 'scanning':
        return '🔍';
      case 'idle':
        return '⏸️';
      case 'warning':
        return '⚠️';
      case 'error':
        return '❌';
      default:
        return '🛡️';
    }
  };
  
  return (
    <div className="system-metrics">
      <div className="metrics-header">
        <h2>📊 Métricas del Sistema</h2>
        <div className={`connection-status ${isConnected ? 'connected' : 'disconnected'}`}>
          {isConnected ? '🟢 Conectado' : '🟡 Desarrollo'}
        </div>
      </div>
      
      <div className="metrics-grid">
        {/* Estado del Sistema */}
        <div className="metric-card state-card">
          <div className="metric-header">
            <span className="metric-icon">{getSystemStateEmoji(systemStatus.state)}</span>
            <span className="metric-title">Estado</span>
          </div>
          <div className="metric-value">
            {systemStatus.state || 'Unknown'}
          </div>
          <div className="metric-subtitle">
            Sistema {isConnected ? 'operacional' : 'en desarrollo'}
          </div>
        </div>
        
        {/* CPU Usage */}
        <div className="metric-card cpu-card">
          <div className="metric-header">
            <span className="metric-icon">🖥️</span>
            <span className="metric-title">CPU</span>
          </div>
          <div className="metric-value">
            <span 
              className="value-number"
              style={{ color: getMetricColor(systemStatus.cpu_usage, 'cpu') }}
            >
              {systemStatus.cpu_usage?.toFixed(1) || '0.0'}%
            </span>
          </div>
          <div className="metric-progress">
            <div 
              className="progress-fill"
              style={{ 
                width: `${Math.min(systemStatus.cpu_usage || 0, 100)}%`,
                backgroundColor: getMetricColor(systemStatus.cpu_usage, 'cpu')
              }}
            ></div>
          </div>
          <div className="metric-subtitle">
            {systemStatus.cpu_usage < 2 ? 'Óptimo' : 
             systemStatus.cpu_usage < 5 ? 'Normal' : 'Alto'}
          </div>
        </div>
        
        {/* Memory Usage */}
        <div className="metric-card memory-card">
          <div className="metric-header">
            <span className="metric-icon">💾</span>
            <span className="metric-title">Memoria RAM</span>
          </div>
          <div className="metric-value">
            <span 
              className="value-number"
              style={{ color: getMetricColor(systemStatus.memory_usage, 'memory') }}
            >
              {formatMemory(systemStatus.memory_usage || 0)}
            </span>
          </div>
          <div className="metric-progress">
            <div 
              className="progress-fill"
              style={{ 
                width: `${Math.min((systemStatus.memory_usage || 0) / 100 * 100, 100)}%`,
                backgroundColor: getMetricColor(systemStatus.memory_usage, 'memory')
              }}
            ></div>
          </div>
          <div className="metric-subtitle">
            {systemStatus.memory_usage < 50 ? 'Eficiente' : 
             systemStatus.memory_usage < 100 ? 'Normal' : 'Alto'}
          </div>
        </div>
        
        {/* Uptime */}
        <div className="metric-card uptime-card">
          <div className="metric-header">
            <span className="metric-icon">⏱️</span>
            <span className="metric-title">Tiempo Activo</span>
          </div>
          <div className="metric-value uptime-value">
            {(() => {
              const uptime = systemStatus.uptime || 0;
              const hours = Math.floor(uptime / 3600);
              const minutes = Math.floor((uptime % 3600) / 60);
              
              if (hours > 0) {
                return `${hours}h ${minutes}m`;
              } else if (minutes > 0) {
                return `${minutes}m`;
              } else {
                return `${uptime}s`;
              }
            })()}
          </div>
          <div className="metric-subtitle">
            Sistema estable
          </div>
        </div>
      </div>
      
      {/* Performance Summary */}
      <div className="performance-summary">
        <div className="summary-item">
          <span className="summary-label">🎯 Performance:</span>
          <span className={`summary-value ${
            (systemStatus.cpu_usage || 0) < 2 && (systemStatus.memory_usage || 0) < 50 
              ? 'excellent' : 'good'
          }`}>
            {(systemStatus.cpu_usage || 0) < 2 && (systemStatus.memory_usage || 0) < 50 
              ? 'Excelente' : 'Bueno'}
          </span>
        </div>
        
        <div className="summary-item">
          <span className="summary-label">📈 Objetivo:</span>
          <span className="summary-value">
            &lt;1% CPU, &lt;30MB RAM
          </span>
        </div>
        
        <div className="summary-item">
          <span className="summary-label">🔧 Versión:</span>
          <span className="summary-value">
            C++ {systemStatus.version || '1.0.0'}
          </span>
        </div>
      </div>
    </div>
  );
};

export default SystemMetrics;