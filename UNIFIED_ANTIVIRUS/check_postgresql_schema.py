import asyncio
import asyncpg

DATABASE_URL = "postgresql://neondb_owner:npg_kE0K3SuXaGZU@ep-dawn-dust-ahynxkwf-pooler.c-3.us-east-1.aws.neon.tech/neondb?sslmode=require"

async def check_database():
    """Verificar el estado actual de la base de datos"""
    try:
        print("Conectando a PostgreSQL...")
        conn = await asyncpg.connect(DATABASE_URL)
        print("Conexión establecida")
        
        # Verificar tablas existentes
        tables = await conn.fetch("SELECT tablename FROM pg_tables WHERE schemaname = 'public'")
        print("Tablas existentes:", [table['tablename'] for table in tables])
        
        # Verificar columnas de cada tabla
        for table in tables:
            table_name = table['tablename']
            print(f"\nColumnas en {table_name}:")
            columns = await conn.fetch("""
                SELECT column_name, data_type, is_nullable
                FROM information_schema.columns 
                WHERE table_name = $1 
                ORDER BY ordinal_position
            """, table_name)
            for col in columns:
                print(f"  - {col['column_name']}: {col['data_type']} ({'NULL' if col['is_nullable'] == 'YES' else 'NOT NULL'})")
        
        await conn.close()
        
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(check_database())