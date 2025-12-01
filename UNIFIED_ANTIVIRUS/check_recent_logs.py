import asyncio
import asyncpg
from datetime import datetime

async def check_recent_logs():
    conn = await asyncpg.connect('postgresql://neondb_owner:npg_kE0K3SuXaGZU@ep-dawn-dust-ahynxkwf-pooler.c-3.us-east-1.aws.neon.tech/neondb?sslmode=require')
    
    try:
        # Contar logs totales
        total = await conn.fetchval('SELECT COUNT(*) FROM log_entries')
        print(f'Total logs en BD: {total}')
        
        # Obtener los últimos 10 logs
        recent = await conn.fetch('''
            SELECT "clientId", timestamp, level, message, "createdAt" 
            FROM log_entries 
            ORDER BY "createdAt" DESC 
            LIMIT 10
        ''')
        
        print('\nÚltimos 10 logs:')
        for log in recent:
            client_id = log['clientId']
            timestamp = log['createdAt']
            level = log['level']
            message = log['message'][:80] + '...' if len(log['message']) > 80 else log['message']
            print(f'- {timestamp} | {level} | {client_id} | {message}')
        
        # Contar clientes activos
        clients = await conn.fetchval('SELECT COUNT(*) FROM antivirus_clients WHERE "isActive" = true')
        print(f'\nClientes activos: {clients}')
        
    finally:
        await conn.close()

if __name__ == "__main__":
    asyncio.run(check_recent_logs())