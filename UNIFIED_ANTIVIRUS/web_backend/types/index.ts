// Types for UNIFIED_ANTIVIRUS Backend
export interface LogEntryInput {
  timestamp: string;
  level: 'DEBUG' | 'INFO' | 'WARNING' | 'ERROR' | 'CRITICAL';
  logger: string;
  message: string;
  module?: string;
  function?: string;
  line?: number;
  component?: string;
  metadata?: Record<string, any>;
}

export interface ClientRegistration {
  clientId: string;
  hostname: string;
  version: string;
  os: string;
  logs: LogEntryInput[];
}

export interface ClientWithStats {
  clientId: string;
  hostname: string;
  version: string;
  os: string;
  ipAddress?: string;
  lastSeen: Date;
  isActive: boolean;
  createdAt: Date;
  updatedAt: Date;
  stats: {
    totalLogs: number;
    recentLogs: number;
    criticalLogs: number;
    errorLogs: number;
    status: 'online' | 'offline';
  };
}

export interface DashboardStats {
  overview: {
    totalClients: number;
    activeClients: number;
    totalLogs: number;
    criticalAlerts: number;
    highAlerts: number;
    trends: {
      logsTrend: number;
    };
  };
  charts: {
    logsByLevel: Array<{ level: string; count: number }>;
    logsByComponent: Array<{ component: string; count: number }>;
    hourlyActivity: any[];
    topClients: any[];
  };
  recentAlerts: any[];
  timeRange: string;
  generatedAt: string;
}

export interface ApiResponse<T = any> {
  success?: boolean;
  message?: string;
  data?: T;
  error?: string;
  details?: any;
}

export interface PaginationInfo {
  total: number;
  limit: number;
  offset: number;
  hasMore: boolean;
}