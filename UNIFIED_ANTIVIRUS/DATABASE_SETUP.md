# PostgreSQL Database Setup para Unified Shield

## 1. Crear Base de Datos en Railway/Neon/Supabase

### Opción A: Railway (Recomendado)
```bash
# 1. Crear cuenta en railway.app
# 2. Crear nuevo proyecto PostgreSQL
# 3. Obtener DATABASE_URL desde variables de entorno
```

### Opción B: Neon (Gratuito)
```bash
# 1. Crear cuenta en neon.tech
# 2. Crear base de datos
# 3. Obtener connection string
```

### Opción C: Supabase
```bash
# 1. Crear cuenta en supabase.com
# 2. Crear proyecto
# 3. Obtener PostgreSQL URL
```

## 2. Configurar Variables de Entorno en Vercel

```bash
# Agregar DATABASE_URL en Vercel
vercel env add DATABASE_URL

# Valor de ejemplo:
# postgresql://user:password@host:5432/database
```

## 3. Actualizar Backend para PostgreSQL

El backend ya está preparado para PostgreSQL, solo necesita:

1. DATABASE_URL configurado
2. Crear las tablas automáticamente al iniciarse

## 4. Schema de Base de Datos

```sql
-- Tabla de instancias de antivirus
CREATE TABLE antivirus_instances (
    id VARCHAR(36) PRIMARY KEY,
    hostname VARCHAR(255),
    os_info VARCHAR(255),
    antivirus_version VARCHAR(50),
    status VARCHAR(20) DEFAULT 'active',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    last_seen TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Tabla de logs
CREATE TABLE log_entries (
    id SERIAL PRIMARY KEY,
    timestamp TIMESTAMP,
    level VARCHAR(20),
    component VARCHAR(100),
    message TEXT,
    instance_id VARCHAR(36),
    details JSONB,
    received_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (instance_id) REFERENCES antivirus_instances(id)
);

-- Índices para performance
CREATE INDEX idx_logs_instance_id ON log_entries(instance_id);
CREATE INDEX idx_logs_timestamp ON log_entries(timestamp);
CREATE INDEX idx_logs_level ON log_entries(level);
CREATE INDEX idx_instances_status ON antivirus_instances(status);
```

## 5. Comandos Rápidos

```bash
# 1. Crear base de datos en Railway
railway login
railway new
railway add postgresql
railway variables

# 2. Configurar en Vercel
vercel env add DATABASE_URL
# Pegar la URL de PostgreSQL

# 3. Redesplegar
vercel --prod

# 4. Verificar
curl -H "X-API-Key: TU_API_KEY" "https://unified-shield.vercel.app/api/health"
```

## 6. Beneficios de PostgreSQL

✅ **Persistencia**: Los datos no se pierden entre deploys
✅ **Escalabilidad**: Maneja millones de logs
✅ **Consultas avanzadas**: Filtros, agregaciones, reportes
✅ **Integridad**: Relaciones entre instancias y logs
✅ **Backup automático**: Los proveedores incluyen backups