# Backend Vercel - Sistema de Logs del Antivirus

![Vercel](https://img.shields.io/badge/vercel-deployed-black.svg)
![FastAPI](https://img.shields.io/badge/FastAPI-0.104-green.svg)
![Python](https://img.shields.io/badge/python-3.9+-blue.svg)

## 📋 Descripción

Backend FastAPI optimizado para Vercel que recibe y gestiona logs de múltiples instancias del antivirus con sistema de identificación única.

## ✨ Características

- ✅ **Identificación Única**: Cada instalación del antivirus tiene un UUID único
- ✅ **Registro de Instancias**: Tracking de instancias activas/inactivas
- ✅ **API RESTful**: Endpoints para logs, instancias y estadísticas
- ✅ **Autenticación**: Protección mediante API Key
- ✅ **Escalable**: Optimizado para serverless en Vercel
- ✅ **CORS Habilitado**: Acceso desde frontend web

## 🏗️ Arquitectura

```
web_backend/
├── main.py              # API FastAPI principal
├── vercel.json          # Configuración de Vercel
├── requirements.txt     # Dependencias Python
└── README.md           # Esta documentación
```

## 🚀 Despliegue en Vercel

### Paso 1: Preparar el Proyecto

```bash
cd web_backend
```

### Paso 2: Instalar Vercel CLI

```bash
npm install -g vercel
```

### Paso 3: Login en Vercel

```bash
vercel login
```

### Paso 4: Configurar Variables de Entorno

En el dashboard de Vercel, configura:

```bash
API_KEY_MASTER=tu_api_key_super_secreta_aqui
DATABASE_URL=postgresql://... (opcional, para PostgreSQL)
```

### Paso 5: Desplegar

```bash
# Despliegue de prueba
vercel

# Despliegue a producción
vercel --prod
```

Tu API estará disponible en: `https://tu-proyecto.vercel.app`

## 📡 Endpoints de la API

### 🏥 Health Check

```bash
GET /api/health
```

**Respuesta:**
```json
{
  "status": "healthy",
  "timestamp": "2025-11-28T23:00:00",
  "database": "in-memory",
  "total_logs": 150,
  "total_instances": 5
}
```

### 📝 Recibir Log

```bash
POST /api/logs
Headers: X-API-Key: tu_api_key
Content-Type: application/json
```

**Body:**
```json
{
  "timestamp": "2025-11-28T23:00:00",
  "level": "INFO",
  "component": "scanner",
  "message": "Escaneo completado",
  "instance_id": "abc-123-def-456",
  "details": {
    "files_scanned": 100,
    "threats_found": 0
  }
}
```

**Respuesta:**
```json
{
  "success": true,
  "message": "Log recibido exitosamente",
  "log_id": "log_151"
}
```

### 🖥️ Registrar Instancia

```bash
POST /api/instances
Headers: X-API-Key: tu_api_key
Content-Type: application/json
```

**Body:**
```json
{
  "id": "abc-123-def-456",
  "hostname": "PC-USUARIO",
  "os_info": "Windows 10 Pro",
  "antivirus_version": "1.1.0",
  "status": "active"
}
```

**Respuesta:**
```json
{
  "success": true,
  "message": "Instancia registrada",
  "instance": {
    "id": "abc-123-def-456",
    "hostname": "PC-USUARIO",
    "os_info": "Windows 10 Pro",
    "antivirus_version": "1.1.0",
    "status": "active",
    "last_seen": "2025-11-28T23:00:00",
    "created_at": "2025-11-28T22:00:00"
  }
}
```

### 📊 Obtener Logs

```bash
GET /api/logs?instance_id=abc-123&level=ERROR&limit=50
Headers: X-API-Key: tu_api_key
```

**Parámetros:**
- `instance_id` (opcional): Filtrar por instancia
- `level` (opcional): Filtrar por nivel (INFO, WARNING, ERROR)
- `limit` (opcional): Número máximo de logs (default: 100)

**Respuesta:**
```json
{
  "success": true,
  "total": 25,
  "logs": [
    {
      "id": "log_150",
      "timestamp": "2025-11-28T23:00:00",
      "level": "ERROR",
      "component": "scanner",
      "message": "Error al escanear archivo",
      "instance_id": "abc-123-def-456",
      "details": {},
      "received_at": "2025-11-28T23:00:01"
    }
  ]
}
```

### 🖥️ Obtener Instancias

```bash
GET /api/instances?status=active
Headers: X-API-Key: tu_api_key
```

**Parámetros:**
- `status` (opcional): Filtrar por estado (active/inactive)

**Respuesta:**
```json
{
  "success": true,
  "total": 3,
  "instances": [
    {
      "id": "abc-123-def-456",
      "hostname": "PC-USUARIO-1",
      "status": "active",
      "last_seen": "2025-11-28T23:00:00"
    }
  ]
}
```

### 📈 Estadísticas

```bash
GET /api/stats
Headers: X-API-Key: tu_api_key
```

**Respuesta:**
```json
{
  "success": true,
  "stats": {
    "total_logs": 150,
    "total_instances": 5,
    "active_instances": 3,
    "logs_by_level": {
      "INFO": 100,
      "WARNING": 30,
      "ERROR": 20
    },
    "last_log": {
      "timestamp": "2025-11-28T23:00:00",
      "level": "INFO",
      "message": "Sistema funcionando correctamente"
    }
  }
}
```

## 🔐 Autenticación

Todas las peticiones (excepto `/` y `/api/health`) requieren el header:

```
X-API-Key: tu_api_key_secreta
```

## 🧪 Testing Local

```bash
# Instalar dependencias
pip install -r requirements.txt

# Ejecutar servidor local
python main.py

# La API estará en http://localhost:8000
```

### Probar Endpoints

```bash
# Health check
curl http://localhost:8000/api/health

# Enviar log (requiere API key)
curl -X POST http://localhost:8000/api/logs \
  -H "X-API-Key: dev-key-12345" \
  -H "Content-Type: application/json" \
  -d '{
    "timestamp": "2025-11-28T23:00:00",
    "level": "INFO",
    "component": "test",
    "message": "Test log",
    "instance_id": "test-123"
  }'
```

## 🔧 Configuración del Cliente

Para que el antivirus envíe logs a Vercel, configura `client_monitor_config.json`:

```json
{
  "server_url": "https://tu-proyecto.vercel.app",
  "api_endpoint": "/api/logs",
  "api_key": "TU_API_KEY",
  "batch_size": 10,
  "send_interval": 30,
  "enabled": true
}
```

## 📊 Almacenamiento

### Modo In-Memory (Default)

Por defecto, los logs se almacenan en memoria (se pierden al reiniciar).

**Ventajas:**
- ✅ Rápido
- ✅ Sin configuración adicional
- ✅ Ideal para pruebas

**Desventajas:**
- ❌ Los datos se pierden al reiniciar
- ❌ Limitado por la memoria disponible

### Modo PostgreSQL (Producción)

Para persistencia real, configura `DATABASE_URL`:

```bash
DATABASE_URL=postgresql://user:pass@host:5432/dbname
```

Luego actualiza `main.py` para usar PostgreSQL en lugar de almacenamiento en memoria.

## 🚨 Troubleshooting

### Error 401: Unauthorized

**Problema:** API Key incorrecta o no enviada

**Solución:**
```bash
# Verifica que el header esté correcto
curl -H "X-API-Key: tu_key_correcta" ...
```

### Error 500: Internal Server Error

**Problema:** Error en el servidor

**Solución:**
1. Revisa los logs de Vercel
2. Verifica que las variables de entorno estén configuradas
3. Prueba localmente para reproducir el error

### Los logs no llegan

**Problema:** El cliente no puede conectarse

**Solución:**
1. Verifica la URL en `client_monitor_config.json`
2. Verifica que la API Key sea correcta
3. Prueba el endpoint manualmente:
   ```bash
   curl https://tu-proyecto.vercel.app/api/health
   ```

## 📈 Monitoreo

### Logs de Vercel

```bash
# Ver logs en tiempo real
vercel logs

# Ver logs de producción
vercel logs --prod
```

### Métricas

Accede al dashboard de Vercel para ver:
- Requests por segundo
- Tiempo de respuesta
- Errores
- Uso de recursos

## 🔄 Actualización

```bash
# Actualizar código
git pull origin main

# Redesplegar
vercel --prod
```

## 🛡️ Seguridad

### Mejores Prácticas

1. **API Key Segura**: Usa una API key compleja y única
2. **HTTPS**: Vercel proporciona HTTPS automáticamente
3. **Rate Limiting**: Implementa rate limiting si es necesario
4. **Validación**: Todos los datos son validados con Pydantic
5. **CORS**: Configura CORS solo para dominios permitidos

### Ejemplo de API Key Segura

```python
import secrets
api_key = secrets.token_urlsafe(32)
print(api_key)  # Usa esto como API_KEY_MASTER
```

## 📝 Notas Importantes

- ⚠️ El almacenamiento in-memory es temporal
- ⚠️ Para producción, usa PostgreSQL
- ⚠️ Configura límites de rate limiting
- ⚠️ Monitorea el uso de recursos en Vercel
- ⚠️ Mantén la API Key segura y no la compartas

## 🔗 Enlaces Útiles

- [Documentación de Vercel](https://vercel.com/docs)
- [FastAPI Docs](https://fastapi.tiangolo.com/)
- [README Principal](../README.md)
- [Guía de Configuración](../guia_configuracion_vercel.md)

## 📞 Soporte

Si tienes problemas:

1. Revisa los logs de Vercel
2. Verifica la configuración
3. Prueba localmente
4. Abre un issue en GitHub

---

**Desarrollado con ❤️ para el Sistema Antivirus Profesional**
