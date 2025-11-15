const fs = require('fs');
const path = require('path');

// Configuraciones para diferentes entornos
const environments = {
  development: {
    API_URL: 'http://localhost:3001/api',
    DATABASE_URL: 'file:./dev.db',
    CORS_ORIGIN: '*'
  },
  production: {
    API_URL: 'https://your-vercel-app.vercel.app/api',
    DATABASE_URL: process.env.DATABASE_URL || 'postgresql://...',
    CORS_ORIGIN: '*'
  }
};

const env = process.env.NODE_ENV || 'development';
const config = environments[env];

// Crear archivo de configuración para el launcher
const launcherConfig = {
  web_logging: {
    enabled: true,
    backend_url: config.API_URL,
    api_key: process.env.API_KEY || 'antivirus-secure-api-key-2024',
    batch_size: 50,
    flush_interval: 10,
    timeout: 30,
    retry_attempts: 3,
    retry_delay: 5
  }
};

// Escribir configuración
const configPath = path.join(__dirname, '..', '..', 'config', 'web_logging_production.json');
fs.writeFileSync(configPath, JSON.stringify(launcherConfig, null, 2));

console.log(`✅ Configuración generada para ${env}: ${configPath}`);
console.log(`📡 API URL: ${config.API_URL}`);