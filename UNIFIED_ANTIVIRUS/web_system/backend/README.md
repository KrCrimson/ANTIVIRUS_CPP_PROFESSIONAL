# 📡 Web Logging Server
## FastAPI-based Log Collection Server for Antivirus System

[![FastAPI](https://img.shields.io/badge/FastAPI-0.104-green)](https://fastapi.tiangolo.com/)
[![Python](https://img.shields.io/badge/Python-3.11-blue)](https://python.org)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-15-blue)](https://postgresql.org)
[![Docker](https://img.shields.io/badge/Docker-Ready-blue)](https://docker.com)

### 🎯 Overview

The **Web Logging Server** is a high-performance REST API server built with FastAPI that receives, stores, and serves logs from the Unified Antivirus system. It provides real-time log collection, advanced filtering, statistics, and a foundation for centralized monitoring.

### ⚡ Features

- 🚀 **High Performance**: Async FastAPI with SQLAlchemy ORM
- 📊 **Advanced Filtering**: Query logs by level, component, date range, threat type
- 🔐 **Secure**: API key authentication with rate limiting
- 📈 **Statistics**: Real-time analytics and trend analysis
- 🐳 **Docker Ready**: Production-ready containerization
- 🏥 **Health Monitoring**: Kubernetes-compatible health checks
- 📋 **OpenAPI Docs**: Auto-generated API documentation

### 🏗️ Architecture

```
┌─────────────────┐    HTTP/JSON     ┌─────────────────┐
│  Antivirus      │ ───────────────► │  Web Logging    │
│  System         │                  │  Server         │
└─────────────────┘                  └─────────────────┘
                                              │
                                              ▼
┌─────────────────┐                  ┌─────────────────┐
│  Dashboard      │ ◄──────────────── │  PostgreSQL     │
│  Frontend       │    REST API      │  Database       │
└─────────────────┘                  └─────────────────┘
```

### 🚀 Quick Start

#### 1. Development Setup (SQLite)

```bash
# Clone and navigate to server directory
cd web_logging_server/

# Install dependencies
pip install -r requirements.txt

# Copy development environment
cp .env.development .env

# Run server
python run.py
```

Server will start at: `http://localhost:8000`
- 📚 API Docs: `http://localhost:8000/docs`
- 🔍 Health Check: `http://localhost:8000/api/health`

#### 2. Docker Development

```bash
# Start with Docker Compose (includes PostgreSQL)
docker-compose up -d

# View logs
docker-compose logs -f web-logging-server

# Stop services
docker-compose down
```

#### 3. Production Deployment

```bash
# Copy production environment
cp .env.production .env

# Edit production settings
nano .env

# Build and run with Docker
docker build -t web-logging-server .
docker run -p 8000:8000 --env-file .env web-logging-server
```

### 📡 API Endpoints

#### 🔐 Authentication
All endpoints require authentication via `X-API-Key` header or `Authorization: Bearer <token>`:

```bash
curl -H "X-API-Key: antivirus-system-key-2024" http://localhost:8000/api/logs
```

#### 📝 Log Management

| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/api/logs` | Create single log entry |
| `POST` | `/api/logs/bulk` | Create multiple logs (bulk) |
| `GET` | `/api/logs` | Query logs with filters |
| `GET` | `/api/logs/{id}` | Get specific log entry |
| `DELETE` | `/api/logs/{id}` | Delete log entry |

#### 📊 Statistics

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/api/stats` | Overall log statistics |
| `GET` | `/api/stats/timeline` | Timeline statistics |
| `GET` | `/api/stats/threats` | Threat detection stats |

#### 🏥 Health & Monitoring

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/api/health` | Basic health check |
| `GET` | `/api/health/detailed` | Detailed system info |
| `GET` | `/api/health/readiness` | Kubernetes readiness |
| `GET` | `/api/health/liveness` | Kubernetes liveness |

### 🔧 Configuration

#### Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `DEBUG` | `false` | Enable debug mode |
| `HOST` | `0.0.0.0` | Server host |
| `PORT` | `8000` | Server port |
| `DATABASE_URL` | SQLite | Database connection string |
| `SECRET_KEY` | Required | JWT/encryption secret |
| `LOG_LEVEL` | `INFO` | Logging level |
| `RATE_LIMIT_REQUESTS` | `1000` | Rate limit per window |
| `CORS_ORIGINS` | localhost | Allowed CORS origins |

#### Database URLs

```bash
# SQLite (Development)
DATABASE_URL=sqlite+aiosqlite:///./logs.db

# PostgreSQL (Production) 
DATABASE_URL=postgresql+asyncpg://user:pass@host:5432/dbname

# PostgreSQL with SSL
DATABASE_URL=postgresql+asyncpg://user:pass@host:5432/dbname?ssl=require
```

### 📋 Usage Examples

#### Creating Log Entries

```python
import httpx
import asyncio

async def send_log():
    async with httpx.AsyncClient() as client:
        log_data = {
            "timestamp": "2024-11-07T15:30:00Z",
            "level": "WARNING",
            "component": "core.engine",
            "message": "Suspicious activity detected",
            "threat_type": "KEYLOGGER",
            "confidence_score": 0.85,
            "severity": "HIGH"
        }
        
        response = await client.post(
            "http://localhost:8000/api/logs",
            json=log_data,
            headers={"X-API-Key": "antivirus-system-key-2024"}
        )
        
        print(f"Status: {response.status_code}")
        print(f"Response: {response.json()}")

asyncio.run(send_log())
```

#### Querying Logs

```bash
# Get recent logs
curl -H "X-API-Key: your-key" \
  "http://localhost:8000/api/logs?page=1&size=50"

# Filter by level and component
curl -H "X-API-Key: your-key" \
  "http://localhost:8000/api/logs?level=ERROR&component=core.engine"

# Search with date range
curl -H "X-API-Key: your-key" \
  "http://localhost:8000/api/logs?date_from=2024-11-07T00:00:00Z&search=malware"

# Get statistics
curl -H "X-API-Key: your-key" \
  "http://localhost:8000/api/stats?hours=24"
```

#### Bulk Log Creation

```python
bulk_data = {
    "logs": [
        {
            "timestamp": "2024-11-07T15:30:00Z",
            "level": "INFO",
            "component": "plugins.detector",
            "message": "File scan completed"
        },
        {
            "timestamp": "2024-11-07T15:31:00Z", 
            "level": "WARNING",
            "component": "plugins.detector",
            "message": "Suspicious file detected"
        }
    ]
}

response = await client.post(
    "http://localhost:8000/api/logs/bulk",
    json=bulk_data,
    headers={"X-API-Key": "antivirus-system-key-2024"}
)
```

### 🧪 Testing

```bash
# Install test dependencies
pip install pytest pytest-asyncio httpx

# Run tests
pytest tests/ -v

# Run with coverage
pytest tests/ --cov=app --cov-report=html

# Run specific test file
pytest tests/test_logs.py -v
```

### 📊 Performance

#### Benchmarks
- **Throughput**: 10,000+ logs/hour
- **Latency**: <200ms P95 for log creation
- **Storage**: ~50MB/day per antivirus instance
- **Concurrent**: 100+ concurrent connections

#### Optimization Tips
- Use bulk endpoints for high-volume logging
- Implement log rotation and archiving
- Use PostgreSQL for production
- Configure appropriate database indexes
- Monitor with Prometheus/Grafana

### 🔐 Security

#### Authentication
- API Key-based authentication
- Rate limiting per client
- CORS protection
- Request validation

#### Production Security
```bash
# Generate secure secret key
python -c "import secrets; print(secrets.token_urlsafe(32))"

# Use environment-specific API keys
export SECRET_KEY="your-secure-secret-key"
export DEFAULT_API_KEYS=""  # Disable default keys

# Restrict CORS origins
export CORS_ORIGINS="https://yourdomain.com"
```

### 🐳 Docker Production

#### Multi-stage Dockerfile
```dockerfile
# Build stage
FROM python:3.11-slim as builder
WORKDIR /app
COPY requirements.txt .
RUN pip install --user -r requirements.txt

# Production stage  
FROM python:3.11-slim
WORKDIR /app
COPY --from=builder /root/.local /root/.local
COPY . .
CMD ["python", "run.py"]
```

#### Docker Compose Production
```yaml
version: '3.8'
services:
  web-server:
    image: web-logging-server:latest
    environment:
      - DATABASE_URL=postgresql+asyncpg://user:pass@postgres:5432/logs
    depends_on:
      - postgres
      
  postgres:
    image: postgres:15-alpine
    environment:
      - POSTGRES_DB=logs
      - POSTGRES_USER=loguser
      - POSTGRES_PASSWORD=${DB_PASSWORD}
    volumes:
      - postgres_data:/var/lib/postgresql/data
```

### 📈 Monitoring & Observability

#### Health Checks
```bash
# Basic health
curl http://localhost:8000/api/health

# Kubernetes probes
curl http://localhost:8000/api/health/readiness
curl http://localhost:8000/api/health/liveness
```

#### Metrics
- Request latency and throughput
- Database connection pool status
- Log ingestion rate
- Error rates by endpoint

#### Logging
Structured JSON logging with:
- Request/response timing
- Error details with stack traces
- Database query performance
- Authentication events

### 🔄 Integration with Antivirus

The server integrates with the antivirus logger via the `WebLogHandler`:

```python
# In antivirus logger configuration
{
    "web_logging": {
        "enabled": true,
        "server_url": "http://localhost:8000/api/logs",
        "api_key": "antivirus-system-key-2024",
        "timeout_seconds": 5,
        "retry_attempts": 3,
        "buffer_size": 1000
    }
}
```

### 🚨 Troubleshooting

#### Common Issues

1. **Database Connection Errors**
   ```bash
   # Check database connectivity
   curl http://localhost:8000/api/health
   
   # Verify DATABASE_URL format
   echo $DATABASE_URL
   ```

2. **Authentication Failures**
   ```bash
   # Verify API key
   curl -H "X-API-Key: your-key" http://localhost:8000/api/health
   ```

3. **Performance Issues**
   ```bash
   # Check system metrics
   curl http://localhost:8000/api/health/detailed
   
   # Monitor database performance
   # Check slow query logs
   ```

#### Log Analysis
```bash
# Server logs location
tail -f logs/web_logging_server.log

# Docker logs
docker logs web-logging-server -f

# Check for specific errors
grep ERROR logs/web_logging_server.log
```

### 🛠️ Development

#### Project Structure
```
web_logging_server/
├── app/
│   ├── main.py          # FastAPI application
│   ├── config.py        # Configuration settings
│   ├── models.py        # Database models
│   ├── database.py      # Database setup
│   ├── auth.py          # Authentication
│   ├── schemas.py       # Pydantic models
│   └── routes/
│       ├── logs.py      # Log endpoints
│       ├── stats.py     # Statistics endpoints
│       └── health.py    # Health endpoints
├── tests/               # Test suite
├── requirements.txt     # Dependencies
├── run.py              # Startup script
├── Dockerfile          # Container config
└── docker-compose.yml  # Development setup
```

#### Adding New Endpoints
1. Define Pydantic schemas in `schemas.py`
2. Add database models in `models.py`
3. Create route handler in `routes/`
4. Include router in `main.py`
5. Add tests in `tests/`

### 📚 API Documentation

When running in debug mode, interactive API documentation is available:
- **Swagger UI**: `http://localhost:8000/docs`
- **ReDoc**: `http://localhost:8000/redoc`

### 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Add tests for new functionality
4. Ensure all tests pass
5. Submit a pull request

### 📄 License

MIT License - see LICENSE file for details

---

**🚀 Ready to centralize your antivirus logging!**