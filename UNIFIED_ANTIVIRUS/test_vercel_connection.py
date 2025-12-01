#!/usr/bin/env python3
"""
Script para probar conectividad con Vercel usando bypass token
"""

import asyncio
import aiohttp
import json

async def test_vercel_connection():
    """Prueba la conexión con Vercel usando el bypass token configurado"""
    
    # Leer configuración
    try:
        with open("config/web_logging_config.json", "r") as f:
            config = json.load(f)
        
        api_url = config["web_logging"]["api_url"]
        api_key = config["web_logging"]["api_key"]
        bypass_token = config["web_logging"].get("bypass_token")
        
    except Exception as e:
        print(f"❌ Error leyendo configuración: {e}")
        return
    
    # Construir URL con bypass token
    health_url = f"{api_url}/health"
    if bypass_token and bypass_token != "VERCEL_BYPASS_TOKEN_PLACEHOLDER":
        health_url += f"?x-vercel-set-bypass-cookie=true&x-vercel-protection-bypass={bypass_token}"
    
    # Probar conexión
    headers = {
        "X-API-Key": api_key,
        "Content-Type": "application/json"
    }
    
    async with aiohttp.ClientSession(headers=headers) as session:
        try:
            async with session.get(health_url) as response:
                if response.status == 200:
                    result = await response.json()
                    print("✅ Conexión exitosa con Vercel!")
                    print(f"📊 Respuesta: {result}")
                else:
                    print(f"❌ Error de conexión: {response.status}")
                    text = await response.text()
                    print(f"📄 Respuesta: {text[:200]}...")
                    
        except Exception as e:
            print(f"❌ Error de conexión: {e}")

if __name__ == "__main__":
    print("🔍 Probando conexión con Vercel...")
    asyncio.run(test_vercel_connection())