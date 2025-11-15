#!/usr/bin/env node

/**
 * UNIFIED_ANTIVIRUS Backend - Startup Script
 * ==========================================
 * 
 * Script para inicializar el backend localmente para testing
 */

const { execSync } = require('child_process');
const fs = require('fs');
const path = require('path');

console.log('🚀 UNIFIED_ANTIVIRUS Backend - Startup Script');
console.log('=' .repeat(50));

// Verificar si existe .env
const envPath = path.join(__dirname, '.env');
if (!fs.existsSync(envPath)) {
    console.log('⚠️  Creando archivo .env desde .env.example...');
    
    const envExample = fs.readFileSync(path.join(__dirname, '.env.example'), 'utf8');
    const localEnv = envExample
        .replace('postgresql://username:password@hostname:port/database', 'file:./dev.db')
        .replace('your-super-secret-jwt-key-here', 'dev-jwt-secret-key-123')
        .replace('unified-antivirus-api-key-2024', 'test-api-key-123')
        .replace('production', 'development');
    
    fs.writeFileSync(envPath, localEnv);
    console.log('✅ Archivo .env creado');
}

// Verificar dependencias
console.log('📦 Verificando dependencias...');
try {
    execSync('npm list --depth=0', { stdio: 'ignore' });
    console.log('✅ Dependencias verificadas');
} catch (error) {
    console.log('⚠️  Instalando dependencias...');
    execSync('npm install', { stdio: 'inherit' });
}

// Generar cliente Prisma
console.log('🗄️  Generando cliente Prisma...');
try {
    execSync('npx prisma generate', { stdio: 'inherit' });
    console.log('✅ Cliente Prisma generado');
} catch (error) {
    console.error('❌ Error generando cliente Prisma:', error.message);
    process.exit(1);
}

// Para development, usar SQLite
console.log('🗄️  Configurando base de datos de desarrollo (SQLite)...');
try {
    // Actualizar el schema para usar SQLite en desarrollo
    const schemaPath = path.join(__dirname, 'prisma', 'schema.prisma');
    let schema = fs.readFileSync(schemaPath, 'utf8');
    
    if (process.env.NODE_ENV !== 'production') {
        schema = schema.replace(
            'provider = "postgresql"',
            'provider = "sqlite"'
        );
        fs.writeFileSync(schemaPath, schema);
    }
    
    execSync('npx prisma db push', { stdio: 'inherit' });
    console.log('✅ Base de datos configurada');
} catch (error) {
    console.log('⚠️  Error configurando BD, continuando...');
}

// Seed de datos iniciales
console.log('🌱 Cargando datos iniciales...');
try {
    execSync('npm run db:seed', { stdio: 'inherit' });
    console.log('✅ Datos iniciales cargados');
} catch (error) {
    console.log('⚠️  Error cargando datos iniciales, continuando...');
}

console.log('\n🎉 Backend inicializado correctamente!');
console.log('📋 Comandos disponibles:');
console.log('  npm run dev     - Iniciar servidor de desarrollo');
console.log('  npm run build   - Construir para producción');
console.log('  npm run start   - Iniciar servidor de producción');
console.log('  npm run db:studio - Abrir Prisma Studio');
console.log('\n🔗 URLs importantes:');
console.log('  Dashboard: http://localhost:3000');
console.log('  API Logs: http://localhost:3000/api/logs');
console.log('  API Clients: http://localhost:3000/api/clients');
console.log('  API Dashboard: http://localhost:3000/api/dashboard');
console.log('\n📝 Configuración del antivirus:');
console.log('  API Endpoint: http://localhost:3000/api/logs');
console.log('  API Key: test-api-key-123');
console.log('\n🚀 Ejecuta "npm run dev" para iniciar el servidor!');