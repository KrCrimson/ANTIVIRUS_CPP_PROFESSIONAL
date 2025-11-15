#!/usr/bin/env node

const { execSync } = require('child_process');
const fs = require('fs');
const path = require('path');

console.log('🚀 GUÍA DE DEPLOYMENT A VERCEL - ANTIVIRUS BACKEND');
console.log('================================================\n');

// Paso 1: Verificar archivos necesarios
console.log('📋 Paso 1: Verificando archivos necesarios...');
const requiredFiles = [
  'vercel.json',
  'package.json',
  '.env.production',
  'prisma/schema.production.prisma'
];

requiredFiles.forEach(file => {
  if (fs.existsSync(file)) {
    console.log(`✅ ${file} - Encontrado`);
  } else {
    console.log(`❌ ${file} - NO encontrado`);
  }
});

console.log('\n📝 Paso 2: INSTRUCCIONES PARA DEPLOYMENT');
console.log('----------------------------------------');

console.log(`
🔧 CONFIGURACIÓN MANUAL REQUERIDA:

1. 📊 CREAR BASE DE DATOS POSTGRESQL (Gratis):
   - Ve a: https://neon.tech/
   - Crea una cuenta gratis
   - Crea un nuevo proyecto "unified-antivirus"
   - Copia la URL de conexión

2. 🌐 CONFIGURAR VERCEL:
   - Instala Vercel CLI: npm i -g vercel
   - Ve al directorio web_backend
   - Ejecuta: vercel
   - Sigue las instrucciones

3. 🔑 CONFIGURAR VARIABLES DE ENTORNO EN VERCEL:
   - Ve a tu proyecto en vercel.com
   - Settings > Environment Variables
   - Agrega estas variables:

   DATABASE_URL = [Tu URL de PostgreSQL de Neon]
   API_KEY = antivirus-secure-api-key-2024
   NODE_ENV = production
   CORS_ORIGIN = *

4. 📤 HACER DEPLOYMENT:
   - Después de configurar variables: vercel --prod

5. 🔄 ACTUALIZAR CONFIGURACIÓN DEL LAUNCHER:
   - Copia la URL de tu deployment (ej: https://tu-app.vercel.app)
   - Actualiza config/web_logging_production.json
`);

console.log('\n🔄 ¿Quieres que genere la configuración del launcher ahora?');
console.log('Necesitarás proporcionar la URL de tu deployment de Vercel.');

// Generar configuración básica para launcher
const launcherConfig = {
  web_logging: {
    enabled: true,
    backend_url: "https://TU-APP.vercel.app/api",
    api_key: "antivirus-secure-api-key-2024",
    batch_size: 50,
    flush_interval: 10,
    timeout: 30,
    retry_attempts: 3,
    retry_delay: 5
  }
};

const configPath = path.join('..', 'config', 'web_logging_production.json');
fs.writeFileSync(configPath, JSON.stringify(launcherConfig, null, 2));
console.log(`\n✅ Configuración base creada en: ${configPath}`);
console.log('📝 RECUERDA: Cambiar "TU-APP.vercel.app" por tu URL real de Vercel\n');

console.log('🎯 PRÓXIMOS PASOS:');
console.log('1. Crear cuenta en Neon.tech');
console.log('2. Obtener DATABASE_URL');
console.log('3. Ejecutar: vercel');
console.log('4. Configurar variables de entorno');
console.log('5. Ejecutar: vercel --prod');
console.log('6. Actualizar URL en web_logging_production.json');