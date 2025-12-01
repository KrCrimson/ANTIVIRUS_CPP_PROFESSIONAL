import asyncio
import asyncpg
import os

DATABASE_URL = "postgresql://neondb_owner:npg_kE0K3SuXaGZU@ep-dawn-dust-ahynxkwf-pooler.c-3.us-east-1.aws.neon.tech/neondb?sslmode=require"

async def create_tables():
    """Crear las tablas necesarias en PostgreSQL"""
    try:
        print("Conectando a PostgreSQL...")
        conn = await asyncpg.connect(DATABASE_URL)
        print("Conexión establecida")
        
        # Crear tabla de instancias
        print("Creando tabla antivirus_instances...")
        await conn.execute("""
            CREATE TABLE IF NOT EXISTS antivirus_instances (
                id VARCHAR(36) PRIMARY KEY,
                hostname VARCHAR(255),
                os_info VARCHAR(255),
                antivirus_version VARCHAR(50),
                status VARCHAR(20) DEFAULT 'active',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                last_seen TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # Crear tabla de logs
        print("Creando tabla log_entries...")
        await conn.execute("""
            CREATE TABLE IF NOT EXISTS log_entries (
                id SERIAL PRIMARY KEY,
                timestamp TIMESTAMP,
                level VARCHAR(20),
                component VARCHAR(100),
                message TEXT,
                instance_id VARCHAR(36),
                details JSONB,
                received_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # Crear índices
        print("Creando índices...")
        await conn.execute("CREATE INDEX IF NOT EXISTS idx_logs_instance_id ON log_entries(instance_id)")
        await conn.execute("CREATE INDEX IF NOT EXISTS idx_logs_timestamp ON log_entries(timestamp)")
        await conn.execute("CREATE INDEX IF NOT EXISTS idx_logs_level ON log_entries(level)")
        await conn.execute("CREATE INDEX IF NOT EXISTS idx_instances_status ON antivirus_instances(status)")
        
        # Verificar tablas creadas
        print("Verificando tablas...")
        tables = await conn.fetch("SELECT tablename FROM pg_tables WHERE schemaname = 'public'")
        print("Tablas existentes:", [table['tablename'] for table in tables])
        
        # Verificar columnas de log_entries
        columns = await conn.fetch("""
            SELECT column_name, data_type 
            FROM information_schema.columns 
            WHERE table_name = 'log_entries' 
            ORDER BY ordinal_position
        """)
        print("Columnas en log_entries:")
        for col in columns:
            print(f"  - {col['column_name']}: {col['data_type']}")
        
        await conn.close()
        print("¡Tablas creadas exitosamente!")
        
    except Exception as e:
        print(f"Error creando tablas: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(create_tables())