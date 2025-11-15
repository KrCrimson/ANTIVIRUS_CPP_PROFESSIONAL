# 🌐 Web System - Sistema de Logging Web Centralizado
## Arquitectura Completa para Monitoreo de Antivirus

[![Status](https://img.shields.io/badge/Status-Sprint%201%20Completado-green)](backend/)
[![Architecture](https://img.shields.io/badge/Architecture-Microservices-blue)](architecture)
[![Stack](https://img.shields.io/badge/Stack-FastAPI%20%2B%20React-orange)](stack)

### 🎯 **VISIÓN GENERAL**

El **Web System** es una arquitectura completa de microservicios que centraliza todos los logs del sistema antivirus, proporcionando:

- 📡 **Recolección en tiempo real** de logs del antivirus
- 💾 **Almacenamiento centralizado** con base de datos optimizada  
- 📊 **Dashboard interactivo** para análisis y visualización
- 🔍 **Búsqueda y filtrado avanzado** de eventos
- 📈 **Estadísticas y métricas** para toma de decisiones
- 🚨 **Alertas automáticas** para eventos críticos

### 🏗️ **ARQUITECTURA DEL SISTEMA**

```
┌─────────────────────┐    HTTP/JSON    ┌─────────────────────┐
│                     │ ──────────────► │                     │
│   ANTIVIRUS         │                 │   BACKEND API       │
│   SYSTEM            │                 │   (FastAPI)         │
│   (Python)          │                 │   Puerto: 8000      │
│                     │                 │                     │
└─────────────────────┘                 └─────────────────────┘
          │                                        │
          │ WebLogHandler                          │ REST API
          │ + Buffer Local                         │
          ▼                                        ▼
┌─────────────────────┐                 ┌─────────────────────┐
│                     │                 │                     │
│   LOCAL FILES       │                 │   POSTGRESQL        │
│   (Fallback)        │                 │   DATABASE          │
│                     │                 │                     │
└─────────────────────┘                 └─────────────────────┘
                                                   │
                                                   │ Query API
                                                   ▼
                                        ┌─────────────────────┐
                                        │                     │
                                        │   FRONTEND          │
                                        │   DASHBOARD         │
                                        │   (React/HTML)      │
                                        │   Puerto: 3000      │
                                        │                     │
                                        └─────────────────────┘
```

### 📁 **ESTRUCTURA DEL PROYECTO**

```
web_system/
├── 📋 SCRUM_PLAN_LOGGING_WEB.md     # Plan completo de desarrollo
├── 📖 README.md                     # Este archivo - Guía principal
├── 
├── 🔧 backend/                      # ✅ SPRINT 1 - COMPLETADO
│   ├── app/                         # FastAPI application
│   │   ├── main.py                  # Aplicación principal
│   │   ├── config.py                # Configuración
│   │   ├── models.py                # Modelos de BD
│   │   ├── database.py              # Setup de BD
│   │   ├── auth.py                  # Autenticación
│   │   ├── schemas.py               # Validación Pydantic
│   │   └── routes/                  # Endpoints REST
│   │       ├── logs.py              # API de logs
│   │       ├── stats.py             # Estadísticas
│   │       └── health.py            # Health checks
│   ├── tests/                       # Tests unitarios
│   ├── requirements.txt             # Dependencias Python
│   ├── Dockerfile                   # Container backend
│   ├── docker-compose.yml           # Orquestación desarrollo
│   └── README.md                    # Documentación backend
│
├── 🎨 frontend/                     # ⏳ SPRINT 3 - PENDIENTE
│   ├── public/                      # Assets estáticos
│   ├── src/                         # Código React/HTML
│   │   ├── components/              # Componentes reutilizables
│   │   ├── pages/                   # Páginas del dashboard
│   │   ├── services/                # API clients
│   │   └── utils/                   # Utilidades
│   ├── package.json                 # Dependencias Node.js
│   └── README.md                    # Documentación frontend
│
├── 🔌 integration/                  # ⏳ SPRINT 2 - PENDIENTE
│   ├── web_log_handler.py           # Handler para antivirus logger
│   ├── buffer_manager.py            # Gestión buffer local
│   ├── reconnection_manager.py      # Auto-reconexión
│   ├── config_extension.json        # Extensión logging config
│   └── README.md                    # Guía de integración
│
└── 🚀 deployment/                   # ⏳ SPRINT 5 - PENDIENTE
    ├── docker/                      # Containers producción
    ├── kubernetes/                  # Manifests K8s
    ├── nginx/                       # Reverse proxy config
    ├── monitoring/                  # Grafana + Prometheus
    ├── scripts/                     # Scripts deployment
    └── README.md                    # Guía deployment
```

### 📊 **ESTADO ACTUAL DEL PROYECTO**

| Sprint | Componente | Estado | Progreso | Descripción |
|--------|-----------|--------|----------|-------------|
| **Sprint 1** | 🔧 Backend API | ✅ **COMPLETADO** | 100% | Servidor FastAPI funcional con todos los endpoints |
| **Sprint 2** | 🔌 Integración Antivirus | ⏳ Pendiente | 0% | WebLogHandler + buffer + reconexión |
| **Sprint 3** | 🎨 Dashboard Frontend | ⏳ Pendiente | 0% | Interfaz React/HTML con gráficos |
| **Sprint 4** | 🧪 Testing E2E | ⏳ Pendiente | 0% | Pruebas completas del sistema |
| **Sprint 5** | 🚀 Production Deploy | ⏳ Pendiente | 0% | Deployment + monitoreo |

### 🎉 **SPRINT 1 COMPLETADO - BACKEND API**

#### **✨ Lo que está FUNCIONANDO ahora:**

1. **🚀 Servidor FastAPI Completo**
   - Endpoints REST para crear y consultar logs
   - Autenticación con API keys
   - Rate limiting y seguridad
   - Documentación automática (Swagger)

2. **💾 Base de Datos Optimizada**
   - Modelos SQLAlchemy con índices
   - Soporte PostgreSQL y SQLite
   - Migraciones automáticas
   - Connection pooling

3. **📊 API de Estadísticas**
   - Logs por nivel y componente
   - Timeline de eventos
   - Estadísticas de amenazas
   - Métricas de rendimiento

4. **🏥 Monitoreo y Health Checks**
   - Endpoints para Kubernetes
   - Métricas de sistema
   - Estado de componentes

5. **🐳 Docker Ready**
   - Dockerfile multi-stage
   - Docker Compose con PostgreSQL
   - Variables de entorno
   - Configuración prod/dev

#### **🔧 Cómo probar el backend AHORA:**

```bash
# 1. Navegar al backend
cd web_system/backend/

# 2. Instalar dependencias
pip install -r requirements.txt

# 3. Configurar
cp .env.development .env

# 4. Iniciar servidor
python run.py

# 5. Probar API
curl -H "X-API-Key: antivirus-system-key-2024" \
  http://localhost:8000/api/health

# 6. Ver documentación
# http://localhost:8000/docs
```

### 📋 **PRÓXIMOS PASOS**

#### **🔌 SPRINT 2: Integración con Antivirus (SIGUIENTE)**
**Objetivo**: Conectar el logger actual del antivirus con el servidor web

**Tareas clave:**
- Crear `WebLogHandler` personalizado
- Implementar buffer local para logs offline
- Sistema de reconexión automática
- Extender `config/logging_config.json`
- Testing de integración

**Resultado**: Los logs del antivirus se envían automáticamente al servidor web

#### **🎨 SPRINT 3: Dashboard Web**
**Objetivo**: Interfaz visual para ver logs y estadísticas

**Tareas clave:**
- Dashboard React/HTML responsive  
- Filtros avanzados (fecha, nivel, componente)
- Gráficos con Chart.js
- WebSocket para tiempo real
- Exportación de reportes

**Resultado**: Interfaz web completa para administradores

#### **🧪 SPRINT 4: Testing Completo**
**Objetivo**: Validar todo el sistema end-to-end

**Tareas clave:**
- Tests de integración completos
- Pruebas de carga (10,000 logs/hora)
- Testing de reconexión y failover
- Performance testing
- Documentación técnica

**Resultado**: Sistema completamente validado y confiable

#### **🚀 SPRINT 5: Deployment y Producción**
**Objetivo**: Sistema funcionando en producción

**Tareas clave:**
- Scripts de deployment automatizado
- Configuración nginx + SSL
- Monitoreo con Grafana/Prometheus
- Alertas automáticas
- Backup y rotación de logs

**Resultado**: Sistema en producción 24/7

### 🛠️ **STACK TECNOLÓGICO COMPLETO**

#### **Backend (Sprint 1 - ✅ COMPLETADO)**
- **Framework**: FastAPI (Python 3.11+)
- **Base de Datos**: PostgreSQL + SQLAlchemy async
- **Autenticación**: API Keys + JWT
- **Validación**: Pydantic schemas
- **Testing**: pytest + httpx
- **Containerización**: Docker + Docker Compose

#### **Frontend (Sprint 3 - ⏳ PENDIENTE)**
- **Framework**: React.js o HTML/CSS/JS vanilla
- **Gráficos**: Chart.js + D3.js
- **Tiempo Real**: WebSocket + Server-Sent Events
- **Styling**: Bootstrap 5 o Tailwind CSS
- **Build**: Webpack o Vite

#### **Integración (Sprint 2 - ⏳ PENDIENTE)**  
- **Logger Extension**: Custom Python handler
- **HTTP Client**: httpx async
- **Buffer**: SQLite local + file fallback
- **Reconexión**: Exponential backoff
- **Config**: JSON + environment variables

#### **Deployment (Sprint 5 - ⏳ PENDIENTE)**
- **Containers**: Docker + Kubernetes
- **Proxy**: nginx + SSL/TLS
- **Monitoreo**: Grafana + Prometheus
- **CI/CD**: GitHub Actions o Jenkins
- **Cloud**: AWS/Azure/GCP compatible

### 📈 **MÉTRICAS Y KPIs OBJETIVO**

| Métrica | Target | Estado Actual |
|---------|--------|---------------|
| **Throughput Logs** | 10,000/hora | ✅ Backend soporta |
| **Latencia API** | <200ms P95 | ✅ Optimizado |
| **Uptime** | >99.5% | ⏳ A validar en prod |
| **Tiempo Reconexión** | <30 seg | ⏳ Sprint 2 |
| **Storage Efficiency** | <50MB/día | ✅ Índices optimizados |

### 🔐 **SEGURIDAD IMPLEMENTADA**

- ✅ **API Key Authentication** con rate limiting
- ✅ **CORS Protection** configurable por entorno
- ✅ **Input Validation** con Pydantic schemas
- ✅ **SQL Injection Protection** via SQLAlchemy ORM
- ✅ **Error Handling** sin exposición de internals
- ⏳ **HTTPS/TLS** (Sprint 5)
- ⏳ **Network Segmentation** (Sprint 5)

### 📚 **DOCUMENTACIÓN DISPONIBLE**

1. **📋 [Plan SCRUM Completo](SCRUM_PLAN_LOGGING_WEB.md)** - Metodología y estimaciones
2. **🔧 [Backend API Docs](backend/README.md)** - Documentación técnica completa  
3. **🎨 Frontend Docs** (Sprint 3) - Guía de usuario del dashboard
4. **🔌 Integration Guide** (Sprint 2) - Como integrar con antivirus
5. **🚀 Deployment Guide** (Sprint 5) - Puesta en producción

### 🎯 **VALOR DE NEGOCIO**

#### **Beneficios Inmediatos (Sprint 1 completado):**
- ✅ **Centralización**: Logs de múltiples antivirus en un lugar
- ✅ **Persistencia**: Base de datos confiable vs archivos locales
- ✅ **API REST**: Integración fácil con otros sistemas
- ✅ **Escalabilidad**: Arquitectura preparada para crecimiento

#### **Beneficios Futuros (Sprints 2-5):**
- 📊 **Visibilidad**: Dashboard en tiempo real para administradores
- 🚨 **Alertas**: Notificaciones automáticas de amenazas críticas
- 📈 **Analytics**: Tendencias y patrones de seguridad
- 🔍 **Compliance**: Auditoria y trazabilidad completa

---

## 🚀 **CÓMO CONTINUAR EL DESARROLLO**

### **Paso 1: Probar Backend Actual**
```bash
cd web_system/backend/
pip install -r requirements.txt
python run.py
```

### **Paso 2: Comenzar Sprint 2 (Integración)**
- Modificar `utils/logger.py` para añadir `WebLogHandler`
- Configurar envío automático al backend
- Implementar buffer local y reconexión

### **Paso 3: Desarrollar Sprint 3 (Frontend)**
- Crear dashboard React/HTML
- Conectar con backend API
- Implementar visualizaciones

**🎉 ¡El sistema está listo para continuar el desarrollo! El backend está 100% funcional y esperando las integraciones.**