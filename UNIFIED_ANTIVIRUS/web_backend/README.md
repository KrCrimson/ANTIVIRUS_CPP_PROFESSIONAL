# Unified Antivirus - Backend Web Centralizado

Backend en Vercel para recolectar y analizar logs de todos los antivirus desplegados.

## 🚀 Características

### 📊 **Dashboard en Tiempo Real**
- Monitoreo de todos los clientes de antivirus
- Estadísticas por cliente, nivel de log y componente
- Alertas automáticas para eventos críticos
- Gráficos de actividad y tendencias

### 🔐 **Seguridad y Autenticación**
- API Key authentication para clientes
- JWT para dashboard web
- Validación de datos con Joi
- Rate limiting y CORS configurado

### 📈 **Análisis Inteligente**
- Detección automática de patrones de amenazas
- Generación de alertas por niveles críticos
- Estadísticas agregadas por día/cliente
- Correlación de eventos entre clientes

### 🗄️ **Base de Datos**
- PostgreSQL en Vercel
- Schema optimizado con Prisma ORM
- Índices para consultas rápidas
- Retención configurable de logs

## 🏗️ Arquitectura

```
CLIENTES ANTIVIRUS (Python)
    ↓ HTTPS/JSON
WEB_LOG_SENDER → VERCEL API
    ↓ 
POSTGRESQL DATABASE
    ↓
DASHBOARD WEB (Next.js)
```

## 📦 Componentes

### **Backend APIs**
- `/api/logs` - Recepción de logs de clientes
- `/api/clients` - Gestión de clientes
- `/api/dashboard` - Datos para dashboard
- `/api/alerts` - Sistema de alertas

### **Cliente Python**
- `utils/web_log_sender.py` - Envío asíncrono de logs
- Integración con `logger_handler` plugin
- Retry logic y buffering local
- Compresión y batching automático

### **Base de Datos**
- `AntivirusClient` - Registro de clientes
- `LogEntry` - Logs individuales con metadatos
- `Alert` - Alertas generadas automáticamente
- `LogStatistics` - Estadísticas agregadas
- `User` - Usuarios del dashboard

## 🚦 Estados de Clientes

- **🟢 Online**: Enviando logs (< 5 min)
- **🟡 Idle**: Sin actividad reciente (5-30 min)  
- **🔴 Offline**: Sin conexión (> 30 min)

## 🔧 Configuración

### **Variables de Entorno**
```bash
DATABASE_URL="postgresql://..."
JWT_SECRET="your-jwt-secret"
API_SECRET_KEY="unified-antivirus-api-key-2024"
NODE_ENV="production"
```

### **Configuración del Cliente**
```json
{
  "web_logging": {
    "enabled": true,
    "api_endpoint": "https://your-app.vercel.app/api/logs",
    "api_key": "unified-antivirus-api-key-2024",
    "levels": ["WARNING", "ERROR", "CRITICAL"],
    "batch_size": 50,
    "send_interval": 30
  }
}
```

## 📊 Métricas Recolectadas

### **Por Cliente**
- Hostname, OS, versión del antivirus
- Total de logs por nivel (DEBUG, INFO, WARNING, ERROR, CRITICAL)
- Actividad por componente (core, plugins, detectors, etc.)
- Tiempo de respuesta y estado de conexión

### **Globales**
- Total de clientes activos/inactivos
- Distribución de logs por nivel y componente
- Tendencias temporales y comparaciones
- Top clientes por actividad

## 🚨 Sistema de Alertas

### **Alertas Automáticas**
- **CRITICAL**: Logs con nivel CRITICAL
- **PLUGIN_ERROR**: Errores en plugins
- **THREAT_DETECTED**: Detección de amenazas
- **CLIENT_OFFLINE**: Cliente sin actividad > 30 min

### **Severidades**
- **LOW**: Advertencias menores
- **MEDIUM**: Errores recoverable
- **HIGH**: Errores críticos de plugins
- **CRITICAL**: Fallos del sistema

## 📈 Dashboard Features

### **Vista General**
- Resumen de clientes activos
- Alertas pendientes por severidad
- Gráfico de actividad últimas 24h
- Top 5 clientes más activos

### **Detalle de Cliente**
- Información del sistema (OS, versión, etc.)
- Logs recientes con filtros
- Estadísticas por componente
- Alertas específicas del cliente

### **Análisis de Logs**
- Búsqueda y filtrado avanzado
- Exportación de datos
- Correlación temporal
- Detección de patrones

## 🔧 Deployment en Vercel

### **Preparación**
```bash
cd web_backend
npm install
npx prisma generate
npx prisma db push
```

### **Deploy**
```bash
vercel --prod
```

### **Variables de Entorno en Vercel**
- Configurar DATABASE_URL (PostgreSQL)
- Configurar JWT_SECRET
- Configurar API_SECRET_KEY

## 🧪 Testing Local

### **Iniciar Desarrollo**
```bash
npm run dev
# Backend: http://localhost:3000
```

### **Test API**
```bash
# Test endpoint de logs
curl -X POST http://localhost:3000/api/logs \
  -H "Content-Type: application/json" \
  -H "X-API-Key: unified-antivirus-api-key-2024" \
  -d '{
    "clientId": "test-client",
    "hostname": "test-machine",
    "version": "1.0.0",
    "os": "Windows 10",
    "logs": [
      {
        "timestamp": "2024-11-14T10:00:00Z",
        "level": "INFO",
        "logger": "test",
        "message": "Test message"
      }
    ]
  }'
```

## 📚 Integración con Antivirus

### **1. Habilitar Web Logging**
En `plugins/handlers/logger_handler/config.json`:
```json
{
  "web_logging": {
    "enabled": true,
    "api_endpoint": "https://your-app.vercel.app/api/logs",
    "api_key": "your-api-key"
  }
}
```

### **2. Logs Automáticos**
El logger handler enviará automáticamente:
- Logs de nivel WARNING, ERROR, CRITICAL
- Metadatos del sistema y componente
- Batching cada 30 segundos
- Retry automático en caso de fallos

### **3. Monitoreo**
- Dashboard web para visualizar logs
- Alertas en tiempo real
- Estadísticas agregadas
- Correlación entre clientes

## 🏷️ Tags del Sistema

- **#centralized-logging**: Logs centralizados
- **#real-time-monitoring**: Monitoreo en tiempo real  
- **#threat-intelligence**: Inteligencia de amenazas
- **#scalable-backend**: Backend escalable
- **#automated-alerts**: Alertas automáticas