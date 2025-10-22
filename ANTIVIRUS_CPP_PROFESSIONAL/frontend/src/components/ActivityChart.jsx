import React, { useState, useEffect } from 'react';
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend,
  BarElement,
} from 'chart.js';
import { Line, Bar } from 'react-chartjs-2';

// Registrar componentes de Chart.js
ChartJS.register(
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  BarElement,
  Title,
  Tooltip,
  Legend
);

const ActivityChart = ({ systemStatus, threats }) => {
  const [cpuHistory, setCpuHistory] = useState([]);
  const [memoryHistory, setMemoryHistory] = useState([]);
  const [threatHistory, setThreatHistory] = useState([]);
  const [timeLabels, setTimeLabels] = useState([]);
  const [chartType, setChartType] = useState('performance'); // 'performance' o 'threats'
  
  // Actualizar historial cada vez que cambian las métricas
  useEffect(() => {
    const now = new Date();
    const timeLabel = now.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
    
    // Mantener solo los últimos 20 puntos de datos
    const maxDataPoints = 20;
    
    setCpuHistory(prev => {
      const newHistory = [...prev, systemStatus.cpu_usage || 0];
      return newHistory.slice(-maxDataPoints);
    });
    
    setMemoryHistory(prev => {
      const newHistory = [...prev, systemStatus.memory_usage || 0];
      return newHistory.slice(-maxDataPoints);
    });
    
    setThreatHistory(prev => {
      const activeThreats = threats.filter(t => t.status === 'Active').length;
      const newHistory = [...prev, activeThreats];
      return newHistory.slice(-maxDataPoints);
    });
    
    setTimeLabels(prev => {
      const newLabels = [...prev, timeLabel];
      return newLabels.slice(-maxDataPoints);
    });
  }, [systemStatus, threats]);
  
  // Configuración del gráfico de performance
  const performanceData = {
    labels: timeLabels,
    datasets: [
      {
        label: 'CPU Usage (%)',
        data: cpuHistory,
        borderColor: '#2196F3',
        backgroundColor: 'rgba(33, 150, 243, 0.1)',
        borderWidth: 2,
        fill: true,
        tension: 0.4,
      },
      {
        label: 'Memory Usage (MB)',
        data: memoryHistory,
        borderColor: '#4CAF50',
        backgroundColor: 'rgba(76, 175, 80, 0.1)',
        borderWidth: 2,
        fill: true,
        tension: 0.4,
        yAxisID: 'y1',
      }
    ],
  };
  
  // Configuración del gráfico de amenazas
  const threatsData = {
    labels: timeLabels,
    datasets: [
      {
        label: 'Amenazas Activas',
        data: threatHistory,
        borderColor: '#F44336',
        backgroundColor: 'rgba(244, 67, 54, 0.1)',
        borderWidth: 3,
        fill: true,
        tension: 0.3,
      }
    ],
  };
  
  // Opciones para el gráfico de performance
  const performanceOptions = {
    responsive: true,
    maintainAspectRatio: false,
    plugins: {
      legend: {
        position: 'top',
        labels: {
          usePointStyle: true,
          padding: 20,
        }
      },
      title: {
        display: true,
        text: '📊 Rendimiento del Sistema en Tiempo Real',
        font: {
          size: 16,
          weight: 'bold'
        }
      },
    },
    scales: {
      x: {
        grid: {
          display: false,
        },
        title: {
          display: true,
          text: 'Tiempo'
        }
      },
      y: {
        type: 'linear',
        display: true,
        position: 'left',
        min: 0,
        max: 10,
        title: {
          display: true,
          text: 'CPU (%)'
        },
        grid: {
          color: 'rgba(0,0,0,0.1)',
        }
      },
      y1: {
        type: 'linear',
        display: true,
        position: 'right',
        min: 0,
        max: 100,
        title: {
          display: true,
          text: 'Memoria (MB)'
        },
        grid: {
          drawOnChartArea: false,
        },
      },
    },
    interaction: {
      mode: 'index',
      intersect: false,
    },
    animation: {
      duration: 750,
    }
  };
  
  // Opciones para el gráfico de amenazas
  const threatsOptions = {
    responsive: true,
    maintainAspectRatio: false,
    plugins: {
      legend: {
        position: 'top',
        labels: {
          usePointStyle: true,
          padding: 20,
        }
      },
      title: {
        display: true,
        text: '🛡️ Actividad de Amenazas',
        font: {
          size: 16,
          weight: 'bold'
        }
      },
    },
    scales: {
      x: {
        grid: {
          display: false,
        },
        title: {
          display: true,
          text: 'Tiempo'
        }
      },
      y: {
        min: 0,
        title: {
          display: true,
          text: 'Número de Amenazas'
        },
        ticks: {
          stepSize: 1,
        },
        grid: {
          color: 'rgba(244, 67, 54, 0.1)',
        }
      },
    },
    interaction: {
      mode: 'index',
      intersect: false,
    },
    animation: {
      duration: 750,
    }
  };
  
  // Calcular estadísticas
  const avgCpu = cpuHistory.length > 0 ? 
    (cpuHistory.reduce((a, b) => a + b, 0) / cpuHistory.length).toFixed(1) : 0;
  
  const avgMemory = memoryHistory.length > 0 ? 
    (memoryHistory.reduce((a, b) => a + b, 0) / memoryHistory.length).toFixed(0) : 0;
  
  const maxThreats = threatHistory.length > 0 ? Math.max(...threatHistory) : 0;
  
  return (
    <div className="activity-chart">
      <div className="chart-header">
        <h2>📈 Actividad del Sistema</h2>
        
        <div className="chart-controls">
          <button 
            className={`chart-tab ${chartType === 'performance' ? 'active' : ''}`}
            onClick={() => setChartType('performance')}
          >
            ⚡ Performance
          </button>
          
          <button 
            className={`chart-tab ${chartType === 'threats' ? 'active' : ''}`}
            onClick={() => setChartType('threats')}
          >
            🛡️ Amenazas
          </button>
        </div>
      </div>
      
      <div className="chart-container">
        {chartType === 'performance' ? (
          <Line 
            data={performanceData} 
            options={performanceOptions}
            height={300}
          />
        ) : (
          <Line 
            data={threatsData} 
            options={threatsOptions}
            height={300}
          />
        )}
      </div>
      
      <div className="chart-stats">
        {chartType === 'performance' ? (
          <div className="performance-stats">
            <div className="stat-card">
              <div className="stat-icon">🖥️</div>
              <div className="stat-content">
                <div className="stat-value">{avgCpu}%</div>
                <div className="stat-label">CPU Promedio</div>
              </div>
            </div>
            
            <div className="stat-card">
              <div className="stat-icon">💾</div>
              <div className="stat-content">
                <div className="stat-value">{avgMemory}MB</div>
                <div className="stat-label">RAM Promedio</div>
              </div>
            </div>
            
            <div className="stat-card">
              <div className="stat-icon">⚡</div>
              <div className="stat-content">
                <div className="stat-value">
                  {systemStatus.cpu_usage < 2 ? 'Excelente' : 'Bueno'}
                </div>
                <div className="stat-label">Performance</div>
              </div>
            </div>
            
            <div className="stat-card">
              <div className="stat-icon">📊</div>
              <div className="stat-content">
                <div className="stat-value">{cpuHistory.length}</div>
                <div className="stat-label">Puntos de Datos</div>
              </div>
            </div>
          </div>
        ) : (
          <div className="threat-stats">
            <div className="stat-card">
              <div className="stat-icon">🔍</div>
              <div className="stat-content">
                <div className="stat-value">{threats.length}</div>
                <div className="stat-label">Total Detectadas</div>
              </div>
            </div>
            
            <div className="stat-card">
              <div className="stat-icon">🚨</div>
              <div className="stat-content">
                <div className="stat-value">{threats.filter(t => t.status === 'Active').length}</div>
                <div className="stat-label">Activas</div>
              </div>
            </div>
            
            <div className="stat-card">
              <div className="stat-icon">📈</div>
              <div className="stat-content">
                <div className="stat-value">{maxThreats}</div>
                <div className="stat-label">Pico Máximo</div>
              </div>
            </div>
            
            <div className="stat-card">
              <div className="stat-icon">🛡️</div>
              <div className="stat-content">
                <div className="stat-value">
                  {threats.filter(t => t.status === 'Active').length === 0 ? 'Seguro' : 'Alerta'}
                </div>
                <div className="stat-label">Estado</div>
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  );
};

export default ActivityChart;