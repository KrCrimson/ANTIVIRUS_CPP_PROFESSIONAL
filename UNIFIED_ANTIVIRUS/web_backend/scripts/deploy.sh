#!/bin/bash

echo "🚀 Preparando deployment para Vercel..."

# Instalar dependencias
echo "📦 Instalando dependencias..."
npm install

# Generar Prisma client
echo "🗄️ Generando Prisma client..."
npx prisma generate

# Ejecutar migraciones en producción
echo "🔄 Ejecutando migraciones..."
npx prisma migrate deploy

# Construir la aplicación
echo "🏗️ Construyendo aplicación..."
npm run build

echo "✅ Deployment preparado para Vercel"