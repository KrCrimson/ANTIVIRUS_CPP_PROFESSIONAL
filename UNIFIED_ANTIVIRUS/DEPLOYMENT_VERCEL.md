# 🚀 DEPLOYMENT A VERCEL - ANTIVIRUS DASHBOARD

## 📋 Resumen del Sistema

**✅ SISTEMA COMPLETAMENTE CONFIGURADO PARA PRODUCCIÓN**

- ✅ **Backend Next.js**: Preparado para Vercel con optimizaciones
- ✅ **Base de datos**: Configurado para PostgreSQL en producción
- ✅ **Autenticación**: API Keys múltiples con rate limiting
- ✅ **Launcher inteligente**: Detección automática de entorno
- ✅ **Monitoreo**: Health checks y logging avanzado
- ✅ **CORS & Seguridad**: Configurado para producción

## 🎯 INSTRUCCIONES PASO A PASO

### 1. 🗄️ Configurar Base de Datos PostgreSQL

1. Ve a [Neon.tech](https://neon.tech/) (PostgreSQL gratuito)
2. Crea una cuenta y un nuevo proyecto "unified-antivirus"
3. Copia la **DATABASE_URL** (algo como):
   ```
   postgresql://username:password@ep-xyz.us-east-1.aws.neon.tech/dbname?sslmode=require
   ```

### 2. 🌐 Desplegar en Vercel

```bash
# Instalar Vercel CLI
npm install -g vercel

# Ir al directorio del backend
cd web_backend

# Hacer deployment
vercel

# Seguir las instrucciones:
# - Set up and deploy? [Y/n] Y
# - Which scope? (selecciona tu cuenta)
# - Link to existing project? [y/N] N
# - What's your project's name? unified-antivirus-backend
# - In which directory is your code located? ./
```

### 3. 🔑 Configurar Variables de Entorno en Vercel

1. Ve a [vercel.com](https://vercel.com) → Tu proyecto → Settings → Environment Variables
2. Agrega estas variables:

| Nombre | Valor | Entorno |
|--------|-------|---------|
| `DATABASE_URL` | Tu URL de PostgreSQL de Neon | Production |
| `API_KEY` | `antivirus-secure-api-key-2024` | Production |
| `NODE_ENV` | `production` | Production |
| `CORS_ORIGIN` | `*` | Production |

### 4. 📤 Deployment Final

```bash
# Hacer deployment de producción
vercel --prod
```

**¡Guarda la URL que te dé Vercel!** (ej: `https://unified-antivirus-backend-xyz.vercel.app`)

### 5. 🔄 Configurar Launcher para Producción

Edita `config/web_logging_production.json` y cambia la URL:

```json
{
  "web_logging": {
    "enabled": true,
    "backend_url": "https://TU-URL-DE-VERCEL.vercel.app/api",
    "api_key": "antivirus-secure-api-key-2024",
    "batch_size": 50,
    "flush_interval": 10,
    "timeout": 30,
    "retry_attempts": 3,
    "retry_delay": 5
  }
}
```

### 6. 🚀 Ejecutar en Producción

```bash
# Ejecutar launcher en modo producción
python launcher.py --env production
```

## 🔍 URLs Importantes

Una vez desplegado, tendrás acceso a:

- **Dashboard**: `https://tu-url.vercel.app`
- **API Logs**: `https://tu-url.vercel.app/api/logs`
- **Health Check**: `https://tu-url.vercel.app/api/health`
- **Dashboard Data**: `https://tu-url.vercel.app/api/dashboard`

## 🎛️ Características del Sistema

### 🔐 Autenticación
- API Keys múltiples soportadas
- Rate limiting: 500 requests/hora por IP
- Headers: `x-api-key` o `Authorization: Bearer <key>`

### 📊 Dashboard en Tiempo Real
- Gráficos dinámicos con Chart.js
- Estadísticas por cliente, nivel, componente
- Alertas críticas en tiempo real
- Actividad por horas

### 🚨 Monitoreo
- Health checks automáticos
- Logging de producción
- Métricas de memoria y uptime
- Rate limiting monitoring

### 🎯 Múltiples Clientes
- Soporte para N antivirus simultáneos
- Identificación única por `clientId`
- Batching automático de logs
- Retry automático en fallos

## 🔧 Comandos Útiles

```bash
# Desarrollo local
npm run dev

# Ver logs de Vercel
vercel logs

# Actualizar deployment
vercel --prod

# Ver funciones de Vercel
vercel functions list

# Test de conectividad
curl https://tu-url.vercel.app/api/health
```

## 📈 Escalabilidad

El sistema está preparado para:
- **Miles de logs por minuto**: Batching automático
- **Múltiples clientes**: Database indexada
- **Alta disponibilidad**: Vercel serverless
- **Monitoreo 24/7**: Health checks automáticos

## 🐛 Troubleshooting

### Error de conexión
```bash
# Verificar health check
curl https://tu-url.vercel.app/api/health
```

### Error de API Key
- Verificar que `x-api-key` está en headers
- Comprobar que la key coincide con la configurada

### Error de base de datos
- Verificar DATABASE_URL en variables de entorno
- Comprobar que la base de datos Neon está activa

## ✅ Verificación Final

1. **Health check responde**: ✅ `GET /api/health`
2. **Dashboard carga**: ✅ `GET /`
3. **Launcher conecta**: ✅ Logs enviándose
4. **Autenticación funciona**: ✅ API key válida
5. **Database activa**: ✅ PostgreSQL respondiendo

---

**🎉 ¡Sistema listo para producción 24/7!**

El dashboard estará siempre activo escuchando todos los antivirus que se conecten, mostrando datos en tiempo real con gráficos y métricas automáticas.