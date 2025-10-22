import React, { useState, useEffect } from 'react';
import axios from 'axios';
import SystemMetrics from './SystemMetrics.jsx';
import ThreatsDashboard from './ThreatsDashboard.jsx';
import ActivityChart from './ActivityChart.jsx';
import Header from './Header.jsx';
import '../styles/dashboard.css';

const Dashboard = () => {
  // Estados principales del dashboard
  const [systemStatus, setSystemStatus] = useState({
    state: 'Unknown',
    uptime: 0,
    cpu_usage: 0,
    memory_usage: 0,
    version: '1.0.0'
  });
  
  const [threats, setThreats] = useState([]);
  const [scanProgress, setScanProgress] = useState(0);
  const [isConnected, setIsConnected] = useState(false);
  const [lastUpdate, setLastUpdate] = useState(new Date());
  
  // Configuración de la API del backend C++
  const API_BASE = 'http://localhost:8080/api';
  
  // Función para obtener estado del sistema
  const fetchSystemStatus = async () => {
    try {
      const response = await axios.get(`${API_BASE}/status`, {
        timeout: 5000
      });
      
      if (response.data) {
        setSystemStatus(response.data);
        setIsConnected(true);
        setLastUpdate(new Date());
      }
    } catch (error) {
      console.warn('Backend connection failed:', error.message);
      setIsConnected(false);
      // Datos de simulación para desarrollo del frontend
      setSystemStatus({
        state: 'Development Mode',
        uptime: Math.floor(Date.now() / 1000),
        cpu_usage: Math.random() * 3 + 1, // 1-4% CPU
        memory_usage: 25 + Math.random() * 5, // 25-30MB RAM
        version: '1.0.0-dev'
      });
    }
  };
  
  // Función para obtener amenazas detectadas
  const fetchThreats = async () => {
    try {
      const response = await axios.get(`${API_BASE}/threats`, {
        timeout: 5000
      });
      
      if (response.data && response.data.threats) {
        setThreats(response.data.threats);
      }
    } catch (error) {
      console.warn('Threats fetch failed:', error.message);
      // Datos de simulación para desarrollo
      if (!isConnected) {
        setThreats([
          {
            id: 1,
            name: 'Suspicious Process - keylog.exe',
            type: 'Keylogger',
            severity: 'High',
            detected_at: new Date().toISOString(),
            status: 'Active'
          },
          {
            id: 2,
            name: 'Hidden Network Activity',
            type: 'Network Anomaly',
            severity: 'Medium',
            detected_at: new Date(Date.now() - 300000).toISOString(),
            status: 'Quarantined'
          }
        ]);
      }
    }
  };
  
  // Función para iniciar escaneo
  const startScan = async () => {
    try {
      setScanProgress(0);
      const response = await axios.post(`${API_BASE}/scan/start`);
      
      if (response.data && response.data.success) {
        // Simular progreso de escaneo
        const interval = setInterval(() => {
          setScanProgress(prev => {
            if (prev >= 100) {
              clearInterval(interval);
              return 100;
            }
            return prev + 10;
          });
        }, 500);
      }
    } catch (error) {
      console.warn('Scan start failed:', error.message);
      // Simulación para desarrollo
      setScanProgress(0);
      const interval = setInterval(() => {
        setScanProgress(prev => {
          if (prev >= 100) {
            clearInterval(interval);
            fetchThreats(); // Actualizar amenazas después del scan
            return 100;
          }
          return prev + 10;
        });
      }, 500);
    }
  };
  
  // Polling para actualizar datos en tiempo real
  useEffect(() => {
    // Fetch inicial
    fetchSystemStatus();
    fetchThreats();
    
    // Actualización cada 5 segundos
    const interval = setInterval(() => {
      fetchSystemStatus();
      fetchThreats();
    }, 5000);
    
    return () => clearInterval(interval);
  }, []);
  
  // Función para formatear el tiempo de actividad
  const formatUptime = (seconds) => {
    const hours = Math.floor(seconds / 3600);
    const minutes = Math.floor((seconds % 3600) / 60);
    const secs = seconds % 60;
    return `${hours}h ${minutes}m ${secs}s`;
  };
  
  return (
    <div className="dashboard-container">
      <Header 
        isConnected={isConnected}
        lastUpdate={lastUpdate}
        version={systemStatus.version}
      />
      
      <div className="dashboard-grid">
        {/* Métricas del sistema */}
        <div className="metrics-section">
          <SystemMetrics 
            systemStatus={systemStatus}
            isConnected={isConnected}
          />
        </div>
        
        {/* Panel de amenazas */}
        <div className="threats-section">
          <ThreatsDashboard 
            threats={threats}
            onRefresh={fetchThreats}
          />
        </div>
        
        {/* Gráficos de actividad */}
        <div className="charts-section">
          <ActivityChart 
            systemStatus={systemStatus}
            threats={threats}
          />
        </div>
        
        {/* Acciones rápidas */}
        <div className="actions-section">
          <div className="quick-actions">
            <h3>🛡️ Acciones Rápidas</h3>
            
            <button 
              className={`scan-button ${scanProgress > 0 && scanProgress < 100 ? 'scanning' : ''}`}
              onClick={startScan}
              disabled={scanProgress > 0 && scanProgress < 100}
            >
              {scanProgress > 0 && scanProgress < 100 ? 
                `Escaneando... ${scanProgress}%` : 
                '🔍 Iniciar Escaneo'
              }
            </button>
            
            {scanProgress > 0 && scanProgress < 100 && (
              <div className="scan-progress">
                <div 
                  className="progress-bar"
                  style={{ width: `${scanProgress}%` }}
                ></div>
              </div>
            )}
            
            <div className="system-info">
              <div className="info-item">
                <span className="label">Estado:</span>
                <span className={`value ${isConnected ? 'connected' : 'disconnected'}`}>
                  {systemStatus.state}
                </span>
              </div>
              
              <div className="info-item">
                <span className="label">Tiempo Activo:</span>
                <span className="value">
                  {formatUptime(systemStatus.uptime)}
                </span>
              </div>
              
              <div className="info-item">
                <span className="label">CPU:</span>
                <span className="value">
                  {systemStatus.cpu_usage.toFixed(1)}%
                </span>
              </div>
              
              <div className="info-item">
                <span className="label">RAM:</span>
                <span className="value">
                  {systemStatus.memory_usage.toFixed(0)}MB
                </span>
              </div>
            </div>
          </div>
        </div>
      </div>
      
      {/* Indicador de conexión */}
      <div className={`connection-indicator ${isConnected ? 'connected' : 'disconnected'}`}>
        <div className="indicator-dot"></div>
        <span>
          {isConnected ? 
            `✅ Conectado - Última actualización: ${lastUpdate.toLocaleTimeString()}` :
            '⚠️ Modo Desarrollo - Backend desconectado'
          }
        </span>
      </div>
    </div>
  );
};

export default Dashboard;