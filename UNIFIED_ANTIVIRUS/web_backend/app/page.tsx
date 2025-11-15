'use client';

import { useState, useEffect } from 'react';

interface DashboardData {
  overview: {
    totalClients: number;
    activeClients: number;
    totalLogs: number;
    criticalAlerts: number;
    highAlerts: number;
  };
  charts: {
    logsByLevel: Array<{ level: string; count: number }>;
    logsByComponent: Array<{ component: string; count: number }>;
  };
  recentAlerts: Array<{
    id: string;
    type: string;
    severity: string;
    title: string;
    description: string;
    createdAt: string;
  }>;
}

export default function Dashboard() {
  const [data, setData] = useState<DashboardData | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    fetchDashboardData();
    const interval = setInterval(fetchDashboardData, 30000); // Actualizar cada 30 segundos
    return () => clearInterval(interval);
  }, []);

  const fetchDashboardData = async () => {
    try {
      const response = await fetch('/api/dashboard');
      if (!response.ok) {
        throw new Error('Error fetching dashboard data');
      }
      const result = await response.json();
      setData(result);
      setError(null);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Unknown error');
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return (
      <div className="min-h-screen bg-gray-100 flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-32 w-32 border-b-2 border-blue-500 mx-auto"></div>
          <p className="mt-4 text-gray-600">Cargando dashboard...</p>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="min-h-screen bg-gray-100 flex items-center justify-center">
        <div className="bg-red-50 border border-red-200 rounded-lg p-6 max-w-md">
          <h2 className="text-red-800 font-semibold mb-2">Error</h2>
          <p className="text-red-600">{error}</p>
          <button 
            onClick={fetchDashboardData}
            className="mt-4 bg-red-600 text-white px-4 py-2 rounded hover:bg-red-700"
          >
            Reintentar
          </button>
        </div>
      </div>
    );
  }

  if (!data) {
    return (
      <div className="min-h-screen bg-gray-100 flex items-center justify-center">
        <p className="text-gray-600">No hay datos disponibles</p>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-100">
      {/* Header */}
      <header className="bg-white shadow-sm border-b">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center py-6">
            <div className="flex items-center">
              <div className="flex-shrink-0">
                <h1 className="text-2xl font-bold text-gray-900">🛡️ UNIFIED_ANTIVIRUS</h1>
                <p className="text-sm text-gray-500">Dashboard Centralizado de Logs</p>
              </div>
            </div>
            <div className="flex items-center space-x-4">
              <div className="text-sm text-gray-500">
                Última actualización: {new Date().toLocaleTimeString()}
              </div>
              <button
                onClick={fetchDashboardData}
                className="bg-blue-600 text-white px-4 py-2 rounded-md hover:bg-blue-700"
              >
                🔄 Actualizar
              </button>
            </div>
          </div>
        </div>
      </header>

      {/* Dashboard Content */}
      <main className="max-w-7xl mx-auto py-6 sm:px-6 lg:px-8">
        {/* Overview Stats */}
        <div className="grid grid-cols-1 gap-5 sm:grid-cols-2 lg:grid-cols-5 mb-8">
          <div className="bg-white overflow-hidden shadow rounded-lg">
            <div className="p-5">
              <div className="flex items-center">
                <div className="flex-shrink-0">
                  <div className="text-2xl">💻</div>
                </div>
                <div className="ml-5 w-0 flex-1">
                  <dl>
                    <dt className="text-sm font-medium text-gray-500 truncate">
                      Clientes Totales
                    </dt>
                    <dd className="text-lg font-medium text-gray-900">
                      {data.overview.totalClients}
                    </dd>
                  </dl>
                </div>
              </div>
            </div>
          </div>

          <div className="bg-white overflow-hidden shadow rounded-lg">
            <div className="p-5">
              <div className="flex items-center">
                <div className="flex-shrink-0">
                  <div className="text-2xl">🟢</div>
                </div>
                <div className="ml-5 w-0 flex-1">
                  <dl>
                    <dt className="text-sm font-medium text-gray-500 truncate">
                      Clientes Activos
                    </dt>
                    <dd className="text-lg font-medium text-gray-900">
                      {data.overview.activeClients}
                    </dd>
                  </dl>
                </div>
              </div>
            </div>
          </div>

          <div className="bg-white overflow-hidden shadow rounded-lg">
            <div className="p-5">
              <div className="flex items-center">
                <div className="flex-shrink-0">
                  <div className="text-2xl">📝</div>
                </div>
                <div className="ml-5 w-0 flex-1">
                  <dl>
                    <dt className="text-sm font-medium text-gray-500 truncate">
                      Total Logs (24h)
                    </dt>
                    <dd className="text-lg font-medium text-gray-900">
                      {data.overview.totalLogs.toLocaleString()}
                    </dd>
                  </dl>
                </div>
              </div>
            </div>
          </div>

          <div className="bg-white overflow-hidden shadow rounded-lg">
            <div className="p-5">
              <div className="flex items-center">
                <div className="flex-shrink-0">
                  <div className="text-2xl">🚨</div>
                </div>
                <div className="ml-5 w-0 flex-1">
                  <dl>
                    <dt className="text-sm font-medium text-gray-500 truncate">
                      Alertas Críticas
                    </dt>
                    <dd className="text-lg font-medium text-red-600">
                      {data.overview.criticalAlerts}
                    </dd>
                  </dl>
                </div>
              </div>
            </div>
          </div>

          <div className="bg-white overflow-hidden shadow rounded-lg">
            <div className="p-5">
              <div className="flex items-center">
                <div className="flex-shrink-0">
                  <div className="text-2xl">⚠️</div>
                </div>
                <div className="ml-5 w-0 flex-1">
                  <dl>
                    <dt className="text-sm font-medium text-gray-500 truncate">
                      Alertas Altas
                    </dt>
                    <dd className="text-lg font-medium text-orange-600">
                      {data.overview.highAlerts}
                    </dd>
                  </dl>
                </div>
              </div>
            </div>
          </div>
        </div>

        {/* Charts Row */}
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-8">
          {/* Logs by Level */}
          <div className="bg-white shadow rounded-lg p-6">
            <h3 className="text-lg font-medium text-gray-900 mb-4">📊 Logs por Nivel</h3>
            <div className="space-y-3">
              {data.charts.logsByLevel.map((item) => (
                <div key={item.level} className="flex items-center justify-between">
                  <span className={`px-2 py-1 rounded text-sm font-medium ${
                    item.level === 'CRITICAL' ? 'bg-red-100 text-red-800' :
                    item.level === 'ERROR' ? 'bg-orange-100 text-orange-800' :
                    item.level === 'WARNING' ? 'bg-yellow-100 text-yellow-800' :
                    item.level === 'INFO' ? 'bg-blue-100 text-blue-800' :
                    'bg-gray-100 text-gray-800'
                  }`}>
                    {item.level}
                  </span>
                  <span className="text-gray-900 font-medium">{item.count.toLocaleString()}</span>
                </div>
              ))}
            </div>
          </div>

          {/* Logs by Component */}
          <div className="bg-white shadow rounded-lg p-6">
            <h3 className="text-lg font-medium text-gray-900 mb-4">🔧 Logs por Componente</h3>
            <div className="space-y-3">
              {data.charts.logsByComponent.slice(0, 8).map((item) => (
                <div key={item.component} className="flex items-center justify-between">
                  <span className="text-sm text-gray-600 truncate">{item.component}</span>
                  <span className="text-gray-900 font-medium">{item.count.toLocaleString()}</span>
                </div>
              ))}
            </div>
          </div>
        </div>

        {/* Recent Alerts */}
        <div className="bg-white shadow rounded-lg p-6">
          <h3 className="text-lg font-medium text-gray-900 mb-4">🚨 Alertas Recientes</h3>
          {data.recentAlerts.length === 0 ? (
            <p className="text-gray-500 text-center py-4">No hay alertas recientes</p>
          ) : (
            <div className="space-y-3">
              {data.recentAlerts.slice(0, 10).map((alert) => (
                <div key={alert.id} className="border-l-4 border-red-400 bg-red-50 p-4">
                  <div className="flex">
                    <div className="flex-shrink-0">
                      <span className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium ${
                        alert.severity === 'CRITICAL' ? 'bg-red-100 text-red-800' :
                        alert.severity === 'HIGH' ? 'bg-orange-100 text-orange-800' :
                        alert.severity === 'MEDIUM' ? 'bg-yellow-100 text-yellow-800' :
                        'bg-gray-100 text-gray-800'
                      }`}>
                        {alert.severity}
                      </span>
                    </div>
                    <div className="ml-3 flex-1">
                      <h4 className="text-sm font-medium text-gray-900">{alert.title}</h4>
                      <p className="text-sm text-gray-700 mt-1">{alert.description}</p>
                      <p className="text-xs text-gray-500 mt-1">
                        {new Date(alert.createdAt).toLocaleString()}
                      </p>
                    </div>
                  </div>
                </div>
              ))}
            </div>
          )}
        </div>
      </main>
    </div>
  );
}