/**
 * Script para ejecutar migraciones de Prisma manualmente
 * Útil cuando las migraciones no se ejecutan automáticamente en Vercel
 */

const { execSync } = require('child_process');
const path = require('path');

console.log('🔄 Ejecutando migraciones de Prisma...\n');

try {
  // Cambiar al directorio del backend
  const backendDir = path.join(__dirname, '..');
  process.chdir(backendDir);

  console.log('📦 Generando cliente de Prisma...');
  execSync('npx prisma generate', { stdio: 'inherit' });

  console.log('\n🚀 Ejecutando migraciones...');
  execSync('npx prisma migrate deploy', { stdio: 'inherit' });

  console.log('\n✅ Migraciones completadas exitosamente!');
} catch (error) {
  console.error('\n❌ Error ejecutando migraciones:', error.message);
  process.exit(1);
}

