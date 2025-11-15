'use client';

import { useState, useEffect } from 'react';
import { 
  Chart as ChartJS, 
  CategoryScale, 
  LinearScale, 
  PointElement, 
  LineElement, 
  BarElement,
  Title, 
  Tooltip, 
  Legend,
  ArcElement 
} from 'chart.js';
import { Line, Bar, Doughnut } from 'react-chartjs-2';

ChartJS.register(
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  BarElement,
  Title,
  Tooltip,
  Legend,
  ArcElement
);

interface DashboardStats {
  totalClients: number;
  activeClients: number;
  totalLogs24h: number;
  criticalAlerts: number;
}

interface LogEntry {
  id: number;
  level: string;
  message: string;
  component: string;
  timestamp: string;
  client_id: string;
}

interface ChartData {
  labels: string[];
  datasets: any[];
}

// Componente de Login Integrado
function LoginComponent() {
  const [apiKey, setApiKey] = useState('');
  const [error, setError] = useState('');
  const [isLoading, setIsLoading] = useState(false);

  const validApiKeys = [
    'antivirus-key-2024-prod-12345',
    'antivirus-dev-key-local-67890'
  ];

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setIsLoading(true);
    setError('');

    try {
      if (!validApiKeys.includes(apiKey)) {
        throw new Error('API key inválida');
      }

      // Probar conexión con el backend
      const response = await fetch('/api/dashboard', {
        headers: { 'x-api-key': apiKey }
      });

      if (!response.ok) {
        const errorData = await response.json().catch(() => ({}));
        const errorMsg = errorData.message || errorData.error || `Error ${response.status}: ${response.statusText}`;
        throw new Error(`Error de conexión con el backend: ${errorMsg}`);
      }

      localStorage.setItem('antivirusApiKey', apiKey);
      window.location.reload(); // Recargar para aplicar la autenticación
      
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Error de autenticación');
    } finally {
      setIsLoading(false);
    }
  };

  const copyApiKey = (key: string) => {
    navigator.clipboard.writeText(key);
    alert('API key copiada al portapapeles');
  };

  return (
    <div style={{ minHeight: '100vh', backgroundColor: '#f3f4f6', display: 'flex', alignItems: 'center', justifyContent: 'center', padding: '20px' }}>
      <div style={{ maxWidth: '400px', width: '100%', backgroundColor: 'white', borderRadius: '8px', boxShadow: '0 4px 6px rgba(0, 0, 0, 0.1)', padding: '32px' }}>
        <div style={{ textAlign: 'center', marginBottom: '24px' }}>
          <h1 style={{ fontSize: '24px', fontWeight: 'bold', color: '#1f2937', margin: '0 0 8px 0' }}>
            🛡️ Unified Antivirus
          </h1>
          <p style={{ color: '#6b7280', margin: '0' }}>Acceso al Dashboard de Monitoreo</p>
        </div>

        <form onSubmit={handleSubmit} style={{ marginBottom: '24px' }}>
          <div style={{ marginBottom: '16px' }}>
            <label style={{ display: 'block', fontSize: '14px', fontWeight: '500', color: '#374151', marginBottom: '4px' }}>
              API Key
            </label>
            <input
              type="password"
              value={apiKey}
              onChange={(e) => setApiKey(e.target.value)}
              style={{ 
                width: '100%', 
                padding: '8px 12px', 
                border: '1px solid #d1d5db', 
                borderRadius: '6px', 
                fontSize: '14px',
                boxSizing: 'border-box'
              }}
              placeholder="Ingresa tu API key"
              required
            />
          </div>

          {error && (
            <div style={{ color: '#dc2626', fontSize: '14px', backgroundColor: '#fef2f2', padding: '8px', borderRadius: '4px', marginBottom: '16px' }}>
              {error}
            </div>
          )}

          <button
            type="submit"
            disabled={isLoading}
            style={{ 
              width: '100%', 
              backgroundColor: '#2563eb', 
              color: 'white', 
              padding: '10px', 
              borderRadius: '6px', 
              border: 'none', 
              fontSize: '14px', 
              fontWeight: '500',
              cursor: isLoading ? 'not-allowed' : 'pointer',
              opacity: isLoading ? 0.5 : 1
            }}
          >
            {isLoading ? 'Verificando...' : 'Acceder al Dashboard'}
          </button>
        </form>

        <div style={{ padding: '16px', backgroundColor: '#f9fafb', borderRadius: '6px' }}>
          <h3 style={{ fontSize: '14px', fontWeight: '500', color: '#374151', margin: '0 0 8px 0' }}>
            📋 API Keys disponibles:
          </h3>
          <div style={{ display: 'flex', flexDirection: 'column', gap: '8px' }}>
            {validApiKeys.map((key, index) => (
              <div key={index} style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', backgroundColor: 'white', padding: '8px', borderRadius: '4px', border: '1px solid #e5e7eb' }}>
                <span style={{ fontFamily: 'monospace', fontSize: '12px', color: '#6b7280' }}>
                  {key.substring(0, 20)}...
                </span>
                <button
                  type="button"
                  onClick={() => copyApiKey(key)}
                  style={{ color: '#2563eb', fontSize: '12px', background: 'none', border: 'none', cursor: 'pointer' }}
                >
                  Copiar
                </button>
              </div>
            ))}
          </div>
          <p style={{ fontSize: '12px', color: '#6b7280', margin: '8px 0 0 0' }}>
            💡 En producción, las API keys se gestionarían de forma segura
          </p>
        </div>

        <div style={{ textAlign: 'center', marginTop: '16px' }}>
          <div style={{ fontSize: '12px', color: '#6b7280' }}>
            <div>✅ Dashboard con gráficos en tiempo real</div>
            <div>✅ Autenticación por API key</div>
            <div>✅ Logs automáticos desde launcher</div>
          </div>
        </div>
      </div>
    </div>
  );
}

export default function Dashboard() {
  const [stats, setStats] = useState<DashboardStats>({
    totalClients: 0,
    activeClients: 0,
    totalLogs24h: 0,
    criticalAlerts: 0
  });
  
  const [recentLogs, setRecentLogs] = useState<LogEntry[]>([]);
  const [logsChartData, setLogsChartData] = useState<ChartData>({
    labels: [],
    datasets: []
  });
  const [levelChartData, setLevelChartData] = useState<ChartData>({
    labels: [],
    datasets: []
  });
  const [loading, setLoading] = useState(true);
  const [isAuthenticated, setIsAuthenticated] = useState(false);

  // Check authentication
  useEffect(() => {
    const apiKey = localStorage.getItem('antivirusApiKey');
    if (!apiKey) {
      setIsAuthenticated(false);
      setLoading(false);
      return;
    }
    setIsAuthenticated(true);
  }, []);

  // Fetch dashboard data
  const fetchDashboardData = async () => {
    const apiKey = localStorage.getItem('antivirusApiKey');
    if (!apiKey) {
      setIsAuthenticated(false);
      return;
    }

    try {
      const headers = { 'x-api-key': apiKey };
      const [statsRes, logsRes] = await Promise.all([
        fetch('/api/dashboard', { headers }),
        fetch('/api/logs?limit=50', { headers })
      ]);
      
      if (statsRes.ok) {
        const statsData = await statsRes.json();
        // El backend devuelve { overview: {...}, charts: {...}, ... }
        if (statsData.overview) {
          setStats({
            totalClients: statsData.overview.totalClients || 0,
            activeClients: statsData.overview.activeClients || 0,
            totalLogs24h: statsData.overview.totalLogs || 0,
            criticalAlerts: statsData.overview.criticalAlerts || 0
          });
        } else {
          // Compatibilidad con formato anterior
          setStats(statsData);
        }
      }
      
      if (logsRes.ok) {
        const logsData = await logsRes.json();
        setRecentLogs(logsData.logs || []);
        updateCharts(logsData.logs || []);
      }
      
      setLoading(false);
    } catch (error) {
      console.error('Error fetching dashboard data:', error);
      setLoading(false);
    }
  };

  // Update chart data based on logs
  const updateCharts = (logs: LogEntry[]) => {
    // Logs over time (last 24 hours)
    const now = new Date();
    const hours = [];
    const logCounts = [];
    
    for (let i = 23; i >= 0; i--) {
      const hour = new Date(now.getTime() - i * 60 * 60 * 1000);
      hours.push(hour.getHours().toString().padStart(2, '0') + ':00');
      
      const hourLogs = logs.filter(log => {
        const logTime = new Date(log.timestamp);
        return logTime.getHours() === hour.getHours() && 
               logTime.getDate() === hour.getDate();
      }).length;
      
      logCounts.push(hourLogs);
    }

    setLogsChartData({
      labels: hours,
      datasets: [{
        label: 'Logs por Hora',
        data: logCounts,
        borderColor: 'rgb(59, 130, 246)',
        backgroundColor: 'rgba(59, 130, 246, 0.1)',
        tension: 0.1
      }]
    });

    // Logs by level
    const levelCounts = logs.reduce((acc: any, log) => {
      acc[log.level] = (acc[log.level] || 0) + 1;
      return acc;
    }, {});

    setLevelChartData({
      labels: Object.keys(levelCounts),
      datasets: [{
        data: Object.values(levelCounts),
        backgroundColor: [
          '#ef4444', // ERROR - red
          '#f59e0b', // WARNING - yellow  
          '#10b981', // INFO - green
          '#3b82f6', // DEBUG - blue
        ]
      }]
    });
  };

  useEffect(() => {
    fetchDashboardData();
    
    // Auto-refresh every 30 seconds
    const interval = setInterval(fetchDashboardData, 30000);
    return () => clearInterval(interval);
  }, []);

  // Mostrar login si no está autenticado
  if (!isAuthenticated && !loading) {
    return <LoginComponent />;
  }

  // Mostrar loading mientras carga
  if (loading) {
    return (
      <div style={{ minHeight: '100vh', backgroundColor: '#f3f4f6', padding: '20px', display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
        <div style={{ textAlign: 'center' }}>
          <div style={{ fontSize: '48px', marginBottom: '16px' }}>🔄</div>
          <div style={{ fontSize: '18px', color: '#6b7280' }}>Cargando dashboard...</div>
        </div>
      </div>
    );
  }

  return (
    <div style={{ minHeight: '100vh', backgroundColor: '#f3f4f6', padding: '20px' }}>
      <div style={{ maxWidth: '1400px', margin: '0 auto' }}>
        <header style={{ backgroundColor: 'white', padding: '20px', borderRadius: '8px', marginBottom: '20px', boxShadow: '0 1px 3px rgba(0,0,0,0.1)' }}>
          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
            <div>
              <h1 style={{ fontSize: '24px', fontWeight: 'bold', color: '#1f2937', margin: '0' }}>
                🛡️ UNIFIED ANTIVIRUS Dashboard
              </h1>
              <p style={{ color: '#6b7280', margin: '8px 0 0 0' }}>
                Monitoreo en tiempo real - Datos actualizados cada 30s
              </p>
            </div>
            <div style={{ 
              backgroundColor: '#10b981', 
              color: 'white', 
              padding: '8px 16px', 
              borderRadius: '20px', 
              fontSize: '14px',
              fontWeight: '500'
            }}>
              🟢 ACTIVO
            </div>
          </div>
        </header>

        {/* Stats Cards */}
        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(200px, 1fr))', gap: '16px', marginBottom: '20px' }}>
          <div style={{ backgroundColor: 'white', padding: '20px', borderRadius: '8px', boxShadow: '0 1px 3px rgba(0,0,0,0.1)' }}>
            <div style={{ fontSize: '32px', marginBottom: '8px' }}>💻</div>
            <div style={{ fontSize: '24px', fontWeight: 'bold', color: '#1f2937' }}>{stats.totalClients}</div>
            <div style={{ fontSize: '14px', color: '#6b7280' }}>Clientes Totales</div>
          </div>
          
          <div style={{ backgroundColor: 'white', padding: '20px', borderRadius: '8px', boxShadow: '0 1px 3px rgba(0,0,0,0.1)' }}>
            <div style={{ fontSize: '32px', marginBottom: '8px' }}>🟢</div>
            <div style={{ fontSize: '24px', fontWeight: 'bold', color: '#10b981' }}>{stats.activeClients}</div>
            <div style={{ fontSize: '14px', color: '#6b7280' }}>Clientes Activos</div>
          </div>
          
          <div style={{ backgroundColor: 'white', padding: '20px', borderRadius: '8px', boxShadow: '0 1px 3px rgba(0,0,0,0.1)' }}>
            <div style={{ fontSize: '32px', marginBottom: '8px' }}>📝</div>
            <div style={{ fontSize: '24px', fontWeight: 'bold', color: '#3b82f6' }}>{stats.totalLogs24h}</div>
            <div style={{ fontSize: '14px', color: '#6b7280' }}>Total Logs (24h)</div>
          </div>
          
          <div style={{ backgroundColor: 'white', padding: '20px', borderRadius: '8px', boxShadow: '0 1px 3px rgba(0,0,0,0.1)' }}>
            <div style={{ fontSize: '32px', marginBottom: '8px' }}>🚨</div>
            <div style={{ fontSize: '24px', fontWeight: 'bold', color: '#ef4444' }}>{stats.criticalAlerts}</div>
            <div style={{ fontSize: '14px', color: '#6b7280' }}>Alertas Críticas</div>
          </div>
        </div>

        {/* Charts Section */}
        <div style={{ display: 'grid', gridTemplateColumns: '2fr 1fr', gap: '20px', marginBottom: '20px' }}>
          <div style={{ backgroundColor: 'white', padding: '20px', borderRadius: '8px', boxShadow: '0 1px 3px rgba(0,0,0,0.1)' }}>
            <h3 style={{ fontSize: '18px', fontWeight: 'bold', color: '#1f2937', marginBottom: '16px' }}>
              📈 Actividad de Logs (24h)
            </h3>
            {logsChartData.labels.length > 0 ? (
              <Line 
                data={logsChartData}
                options={{
                  responsive: true,
                  plugins: {
                    legend: {
                      position: 'top' as const,
                    },
                    tooltip: {
                      mode: 'index',
                      intersect: false,
                    }
                  },
                  scales: {
                    x: {
                      display: true,
                      title: {
                        display: true,
                        text: 'Hora'
                      }
                    },
                    y: {
                      display: true,
                      title: {
                        display: true,
                        text: 'Cantidad de Logs'
                      }
                    }
                  }
                }}
              />
            ) : (
              <div style={{ textAlign: 'center', color: '#6b7280', padding: '40px' }}>
                Sin datos disponibles
              </div>
            )}
          </div>

          <div style={{ backgroundColor: 'white', padding: '20px', borderRadius: '8px', boxShadow: '0 1px 3px rgba(0,0,0,0.1)' }}>
            <h3 style={{ fontSize: '18px', fontWeight: 'bold', color: '#1f2937', marginBottom: '16px' }}>
              🎯 Logs por Nivel
            </h3>
            {levelChartData.labels.length > 0 ? (
              <Doughnut 
                data={levelChartData}
                options={{
                  responsive: true,
                  plugins: {
                    legend: {
                      position: 'bottom' as const,
                    }
                  }
                }}
              />
            ) : (
              <div style={{ textAlign: 'center', color: '#6b7280', padding: '40px' }}>
                Sin datos disponibles
              </div>
            )}
          </div>
        </div>

        {/* Recent Logs */}
        <div style={{ backgroundColor: 'white', padding: '20px', borderRadius: '8px', boxShadow: '0 1px 3px rgba(0,0,0,0.1)' }}>
          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '16px' }}>
            <h3 style={{ fontSize: '18px', fontWeight: 'bold', color: '#1f2937' }}>
              📋 Logs Recientes
            </h3>
            <button 
              onClick={fetchDashboardData}
              style={{ 
                backgroundColor: '#3b82f6', 
                color: 'white', 
                border: 'none', 
                padding: '8px 16px', 
                borderRadius: '6px', 
                cursor: 'pointer',
                fontSize: '14px'
              }}
            >
              🔄 Actualizar
            </button>
          </div>
          
          {recentLogs.length > 0 ? (
            <div style={{ maxHeight: '400px', overflowY: 'auto' }}>
              {recentLogs.slice(0, 10).map((log) => (
                <div 
                  key={log.id} 
                  style={{ 
                    padding: '12px', 
                    borderLeft: `4px solid ${
                      log.level === 'ERROR' ? '#ef4444' : 
                      log.level === 'WARNING' ? '#f59e0b' : 
                      log.level === 'INFO' ? '#10b981' : '#6b7280'
                    }`,
                    marginBottom: '8px',
                    backgroundColor: '#f9fafb',
                    borderRadius: '0 6px 6px 0'
                  }}
                >
                  <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', marginBottom: '4px' }}>
                    <span style={{ 
                      backgroundColor: log.level === 'ERROR' ? '#fee2e2' : 
                                     log.level === 'WARNING' ? '#fef3c7' : 
                                     log.level === 'INFO' ? '#d1fae5' : '#f3f4f6',
                      color: log.level === 'ERROR' ? '#dc2626' : 
                             log.level === 'WARNING' ? '#d97706' : 
                             log.level === 'INFO' ? '#059669' : '#4b5563',
                      padding: '2px 8px',
                      borderRadius: '12px',
                      fontSize: '12px',
                      fontWeight: '500'
                    }}>
                      {log.level}
                    </span>
                    <span style={{ fontSize: '12px', color: '#6b7280' }}>
                      {new Date(log.timestamp).toLocaleString()}
                    </span>
                  </div>
                  <div style={{ fontSize: '14px', color: '#374151', marginBottom: '4px' }}>
                    {log.message}
                  </div>
                  <div style={{ fontSize: '12px', color: '#6b7280' }}>
                    {log.component} • Cliente: {log.client_id}
                  </div>
                </div>
              ))}
            </div>
          ) : (
            <div style={{ 
              textAlign: 'center', 
              color: '#6b7280', 
              padding: '40px',
              backgroundColor: '#f9fafb',
              borderRadius: '8px'
            }}>
              <div style={{ fontSize: '48px', marginBottom: '16px' }}>📝</div>
              <div style={{ fontSize: '16px', marginBottom: '8px' }}>No hay logs disponibles</div>
              <div style={{ fontSize: '14px' }}>
                Los logs aparecerán aquí cuando el antivirus esté enviando datos
              </div>
            </div>
          )}
        </div>

        {/* Status Footer */}
        <div style={{ 
          backgroundColor: 'white', 
          padding: '16px', 
          borderRadius: '8px', 
          boxShadow: '0 1px 3px rgba(0,0,0,0.1)', 
          marginTop: '20px',
          textAlign: 'center'
        }}>
          <div style={{ color: '#6b7280', fontSize: '14px' }}>
            🚀 Backend operativo • 📡 APIs: /api/logs, /api/clients, /api/dashboard • 
            🔧 Auto-refresh cada 30s
          </div>
        </div>
      </div>
    </div>
  );
}