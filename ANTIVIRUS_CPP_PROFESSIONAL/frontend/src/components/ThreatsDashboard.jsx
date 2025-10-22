import React, { useState } from 'react';

const ThreatsDashboard = ({ threats, onRefresh }) => {
  const [selectedThreat, setSelectedThreat] = useState(null);
  const [filterStatus, setFilterStatus] = useState('All');
  
  // Función para obtener el emoji basado en el tipo de amenaza
  const getThreatIcon = (type) => {
    switch (type?.toLowerCase()) {
      case 'keylogger':
        return '⌨️';
      case 'malware':
        return '🦠';
      case 'virus':
        return '🛡️';
      case 'trojan':
        return '🐎';
      case 'network anomaly':
        return '🌐';
      case 'suspicious behavior':
        return '👁️';
      default:
        return '⚠️';
    }
  };
  
  // Función para obtener el color basado en la severidad
  const getSeverityColor = (severity) => {
    switch (severity?.toLowerCase()) {
      case 'critical':
        return '#D32F2F';
      case 'high':
        return '#F57C00';
      case 'medium':
        return '#FBC02D';
      case 'low':
        return '#388E3C';
      default:
        return '#757575';
    }
  };
  
  // Función para obtener el color del estado
  const getStatusColor = (status) => {
    switch (status?.toLowerCase()) {
      case 'active':
        return '#F44336';
      case 'quarantined':
        return '#FF9800';
      case 'resolved':
        return '#4CAF50';
      case 'analyzing':
        return '#2196F3';
      default:
        return '#757575';
    }
  };
  
  // Filtrar amenazas por estado
  const filteredThreats = threats.filter(threat => 
    filterStatus === 'All' || threat.status === filterStatus
  );
  
  // Función para formatear la fecha
  const formatDate = (dateString) => {
    const date = new Date(dateString);
    return date.toLocaleString();
  };
  
  // Función para simular acción de cuarentena
  const handleQuarantine = (threat) => {
    alert(`Amenaza "${threat.name}" enviada a cuarentena. Esta acción se implementará en el backend.`);
  };
  
  // Función para simular eliminación
  const handleDelete = (threat) => {
    const confirmed = window.confirm(`¿Está seguro de eliminar la amenaza "${threat.name}"?`);
    if (confirmed) {
      alert(`Amenaza "${threat.name}" eliminada. Esta acción se implementará en el backend.`);
    }
  };
  
  return (
    <div className="threats-dashboard">
      <div className="threats-header">
        <div className="header-left">
          <h2>🛡️ Amenazas Detectadas</h2>
          <span className="threat-count">
            {threats.length} {threats.length === 1 ? 'amenaza' : 'amenazas'}
          </span>
        </div>
        
        <div className="header-right">
          <select 
            className="filter-select"
            value={filterStatus}
            onChange={(e) => setFilterStatus(e.target.value)}
          >
            <option value="All">Todas</option>
            <option value="Active">Activas</option>
            <option value="Quarantined">En Cuarentena</option>
            <option value="Resolved">Resueltas</option>
            <option value="Analyzing">Analizando</option>
          </select>
          
          <button 
            className="refresh-btn"
            onClick={onRefresh}
            title="Actualizar"
          >
            🔄
          </button>
        </div>
      </div>
      
      <div className="threats-content">
        {filteredThreats.length === 0 ? (
          <div className="no-threats">
            <div className="no-threats-icon">✅</div>
            <h3>Sin amenazas detectadas</h3>
            <p>El sistema está protegido y funcionando correctamente.</p>
          </div>
        ) : (
          <div className="threats-grid">
            {/* Lista de amenazas */}
            <div className="threats-list">
              {filteredThreats.map((threat) => (
                <div 
                  key={threat.id}
                  className={`threat-item ${selectedThreat?.id === threat.id ? 'selected' : ''}`}
                  onClick={() => setSelectedThreat(threat)}
                >
                  <div className="threat-header">
                    <span className="threat-icon">
                      {getThreatIcon(threat.type)}
                    </span>
                    <div className="threat-info">
                      <div className="threat-name">{threat.name}</div>
                      <div className="threat-type">{threat.type}</div>
                    </div>
                  </div>
                  
                  <div className="threat-meta">
                    <span 
                      className="severity-badge"
                      style={{ backgroundColor: getSeverityColor(threat.severity) }}
                    >
                      {threat.severity}
                    </span>
                    
                    <span 
                      className="status-badge"
                      style={{ backgroundColor: getStatusColor(threat.status) }}
                    >
                      {threat.status}
                    </span>
                  </div>
                  
                  <div className="threat-time">
                    {formatDate(threat.detected_at)}
                  </div>
                </div>
              ))}
            </div>
            
            {/* Detalles de amenaza seleccionada */}
            {selectedThreat && (
              <div className="threat-details">
                <div className="details-header">
                  <h3>🔍 Detalles de la Amenaza</h3>
                  <button 
                    className="close-details"
                    onClick={() => setSelectedThreat(null)}
                  >
                    ❌
                  </button>
                </div>
                
                <div className="details-content">
                  <div className="detail-item">
                    <strong>Nombre:</strong>
                    <span>{selectedThreat.name}</span>
                  </div>
                  
                  <div className="detail-item">
                    <strong>Tipo:</strong>
                    <span>
                      {getThreatIcon(selectedThreat.type)} {selectedThreat.type}
                    </span>
                  </div>
                  
                  <div className="detail-item">
                    <strong>Severidad:</strong>
                    <span 
                      className="severity-badge"
                      style={{ backgroundColor: getSeverityColor(selectedThreat.severity) }}
                    >
                      {selectedThreat.severity}
                    </span>
                  </div>
                  
                  <div className="detail-item">
                    <strong>Estado:</strong>
                    <span 
                      className="status-badge"
                      style={{ backgroundColor: getStatusColor(selectedThreat.status) }}
                    >
                      {selectedThreat.status}
                    </span>
                  </div>
                  
                  <div className="detail-item">
                    <strong>Detectado:</strong>
                    <span>{formatDate(selectedThreat.detected_at)}</span>
                  </div>
                  
                  <div className="detail-item">
                    <strong>ID:</strong>
                    <span className="threat-id">#{selectedThreat.id}</span>
                  </div>
                </div>
                
                <div className="threat-actions">
                  <h4>🛠️ Acciones Disponibles</h4>
                  
                  <div className="action-buttons">
                    {selectedThreat.status === 'Active' && (
                      <button 
                        className="action-btn quarantine-btn"
                        onClick={() => handleQuarantine(selectedThreat)}
                      >
                        🔒 Enviar a Cuarentena
                      </button>
                    )}
                    
                    <button 
                      className="action-btn delete-btn"
                      onClick={() => handleDelete(selectedThreat)}
                    >
                      🗑️ Eliminar
                    </button>
                    
                    <button className="action-btn analyze-btn">
                      🔬 Analizar
                    </button>
                    
                    <button className="action-btn whitelist-btn">
                      ✅ Agregar a Lista Blanca
                    </button>
                  </div>
                </div>
              </div>
            )}
          </div>
        )}
      </div>
      
      {/* Resumen de amenazas */}
      <div className="threats-summary">
        <div className="summary-stats">
          <div className="stat-item">
            <span className="stat-number" style={{ color: '#F44336' }}>
              {threats.filter(t => t.status === 'Active').length}
            </span>
            <span className="stat-label">Activas</span>
          </div>
          
          <div className="stat-item">
            <span className="stat-number" style={{ color: '#FF9800' }}>
              {threats.filter(t => t.status === 'Quarantined').length}
            </span>
            <span className="stat-label">En Cuarentena</span>
          </div>
          
          <div className="stat-item">
            <span className="stat-number" style={{ color: '#4CAF50' }}>
              {threats.filter(t => t.status === 'Resolved').length}
            </span>
            <span className="stat-label">Resueltas</span>
          </div>
          
          <div className="stat-item">
            <span className="stat-number" style={{ color: '#D32F2F' }}>
              {threats.filter(t => t.severity === 'High' || t.severity === 'Critical').length}
            </span>
            <span className="stat-label">Críticas</span>
          </div>
        </div>
      </div>
    </div>
  );
};

export default ThreatsDashboard;