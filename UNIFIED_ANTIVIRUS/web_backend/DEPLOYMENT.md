# 🚀 UNIFIED_ANTIVIRUS - Backend Web Deployment Guide

## 📋 Resumen del Sistema

Este backend centralizado recibe logs de todos los antivirus UNIFIED_ANTIVIRUS desplegados, los almacena en PostgreSQL y proporciona un dashboard web para monitoreo en tiempo real.

### ✅ **Estado Actual - COMPLETADO**
- ✅ Backend API completo (Next.js + TypeScript)
- ✅ Base de datos con Prisma ORM (PostgreSQL/SQLite)
- ✅ Dashboard web responsive
- ✅ Cliente Python integrado (`web_log_sender.py`)
- ✅ Sistema de alertas automáticas
- ✅ Autenticación por API Key
- ✅ Scripts de testing y configuración

## 🏗️ **Componentes del Sistema**

### **1. APIs Principales**
- `POST /api/logs` - Recepción de logs de antivirus
- `GET /api/clients` - Lista de clientes registrados
- `GET /api/dashboard` - Estadísticas para dashboard
- `GET /api/logs` - Consulta de logs con filtros

### **2. Base de Datos (PostgreSQL)**
- `AntivirusClient` - Registro de equipos
- `LogEntry` - Logs individuales con metadatos
- `Alert` - Alertas automáticas generadas
- `LogStatistics` - Estadísticas agregadas
- `User` - Usuarios del dashboard

### **3. Dashboard Web**
- Vista general con métricas clave
- Gráficos de logs por nivel/componente
- Lista de alertas recientes
- Estado de clientes en tiempo real

### **4. Cliente Python**
- Envío asíncrono con batching
- Retry logic y buffering local
- Integración automática con logger_handler

## 🚦 **Deployment en Vercel (Producción)**

### **Paso 1: Preparar el Proyecto**
```bash
cd web_backend
npm install
npx prisma generate
```

### **Paso 2: Configurar Variables de Entorno en Vercel**
```bash
# Database (PostgreSQL de Vercel)
DATABASE_URL="postgresql://user:pass@host:port/db"

# Autenticación
JWT_SECRET="your-super-secret-jwt-key-here"
API_SECRET_KEY="unified-antivirus-api-key-2024"

# Entorno
NODE_ENV="production"
NEXTAUTH_URL="https://your-app.vercel.app"
```

### **Paso 3: Deploy**
```bash
# Instalar Vercel CLI
npm i -g vercel

# Deploy
vercel --prod
```

### **Paso 4: Configurar Base de Datos**
```bash
# Crear tablas
npx prisma db push

# Cargar datos iniciales
npm run db:seed
```

## 🧪 **Testing Local**

### **Inicio Rápido**
```bash
cd web_backend
npm run setup      # Configuración automática
npm run dev        # Servidor en http://localhost:3000
```

### **Testing de APIs**
```bash
# Test de logs
cd ..
python test_web_logging.py

# Opciones:
# 1. Test continuo (5 min)
# 2. Batch único
# 3. Test personalizado
```

### **URLs de Testing**
- Dashboard: http://localhost:3000
- API Logs: http://localhost:3000/api/logs
- API Clients: http://localhost:3000/api/clients
- Prisma Studio: `npm run db:studio`

## ⚙️ **Configuración del Antivirus**

### **1. Habilitar Web Logging**
En `plugins/handlers/logger_handler/config.json`:
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

### **2. Logs Automáticos**
- Se envían automáticamente logs WARNING/ERROR/CRITICAL
- Batching cada 30 segundos
- Retry automático en fallos de red
- Buffer local de 1000 logs máximo

## 📊 **Métricas Monitoreadas**

### **Por Cliente**
- Hostname, OS, versión del antivirus
- Total logs por nivel (DEBUG→CRITICAL)
- Actividad por componente (core, plugins, etc.)
- Estado: 🟢 Online / 🟡 Idle / 🔴 Offline

### **Globales**
- Clientes activos/totales
- Distribución de logs por nivel
- Top clientes más activos
- Tendencias temporales

### **Alertas Automáticas**
- **CRITICAL**: Logs nivel CRITICAL
- **THREAT_DETECTED**: Malware/virus detectado  
- **PLUGIN_ERROR**: Errores en plugins
- **CLIENT_OFFLINE**: Cliente sin actividad >30min

## 🔐 **Seguridad**

### **Autenticación**
- API Key para clientes de antivirus
- JWT para dashboard web (futuro)
- Validación de datos con Joi
- Rate limiting configurado

### **Datos**
- Logs encriptados en tránsito (HTTPS)
- Validación de entrada estricta
- Sanitización de metadatos
- Retención configurable de logs

## 📈 **Escalabilidad**

### **Backend**
- APIs serverless en Vercel
- Auto-scaling automático
- CDN global incluido
- Caching de consultas

### **Base de Datos**
- PostgreSQL optimizado
- Índices en campos críticos
- Particionado por fecha (futuro)
- Archivado automático

## 🔧 **Mantenimiento**

### **Comandos Útiles**
```bash
# Desarrollo
npm run dev
npm run db:studio

# Base de datos
npm run db:generate
npm run db:push
npm run db:seed

# Testing
npm run test:logs
python test_web_logging.py

# Producción
npm run build
vercel --prod
```

### **Monitoring**
- Dashboard web para estado general
- Logs de aplicación en Vercel
- Métricas de base de datos
- Alertas por email (configurar)

## 🎯 **Próximos Pasos**

### **Funcionalidades Pendientes**
- [ ] Autenticación de usuarios para dashboard
- [ ] Exportación de logs (CSV/JSON)
- [ ] Configuración de alertas por email
- [ ] Gráficos históricos avanzados
- [ ] API para integración con SIEM

### **Optimizaciones**
- [ ] Compresión de logs antiguos
- [ ] Particionado de tablas por fecha
- [ ] Cache Redis para consultas frecuentes
- [ ] WebSockets para updates en tiempo real

## 📞 **Soporte**

### **Logs de Debug**
- Vercel: Ver logs en dashboard de Vercel
- Local: Logs en consola del servidor Next.js
- Cliente: Logs en `web_sender_stats()`

### **Troubleshooting Común**
- **Error 401**: Verificar API_SECRET_KEY
- **Error 500**: Revisar conexión a BD
- **Logs no llegan**: Verificar configuración del cliente
- **Dashboard vacío**: Ejecutar db:seed

---

## 🎉 **Sistema Listo para Producción**

El backend está **completamente funcional** y listo para recibir logs de todos los antivirus UNIFIED_ANTIVIRUS desplegados. Solo necesitas:

1. **Deploy en Vercel** con las variables de entorno
2. **Configurar la URL** en los antivirus
3. **Monitorear desde el dashboard web**

¡El sistema de logs centralizados está operativo! 🚀