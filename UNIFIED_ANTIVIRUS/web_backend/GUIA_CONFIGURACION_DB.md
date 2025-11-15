# 🗄️ GUÍA DE CONFIGURACIÓN DE BASE DE DATOS EN VERCEL

## 🎯 RECOMENDACIÓN: **NEON** (Serverless Postgres)

### ¿Por qué Neon?

✅ **Serverless Postgres** - Perfecto para aplicaciones serverless  
✅ **Tier Gratuito Generoso** - 0.5 GB de almacenamiento, suficiente para empezar  
✅ **Compatible con Prisma** - Funciona perfectamente con nuestro schema  
✅ **Fácil de Configurar** - Integración directa desde Vercel  
✅ **Muy Popular** - Ampliamente usado y confiable  

---

## 📋 PASOS PARA CONFIGURAR NEON

### **PASO 1: Crear Base de Datos Neon desde Vercel**

1. En Vercel, haz clic en **"Neon"** en la lista de Marketplace Database Providers
2. Haz clic en **"Create"** o **"Add Integration"**
3. Si no tienes cuenta de Neon, se creará automáticamente
4. Selecciona o crea un proyecto Neon
5. Vercel configurará automáticamente la variable `DATABASE_URL`

### **PASO 2: Verificar Variables de Entorno**

Después de crear la base de datos, verifica que en Vercel → Settings → Environment Variables tengas:

```bash
DATABASE_URL=postgresql://user:password@ep-xxx-xxx.region.aws.neon.tech/dbname?sslmode=require
```

Esta variable se configura automáticamente cuando usas Neon desde Vercel.

### **PASO 3: Agregar API_KEY (si no está)**

Asegúrate de tener también:

```bash
API_KEY=antivirus-key-2024-prod-12345
NODE_ENV=production
```

### **PASO 4: Ejecutar Migraciones**

Después de configurar la base de datos, necesitas crear las tablas. Tienes dos opciones:

**Opción A: Automático (Recomendado)**

El script `vercel-build` en `package.json` ya incluye las migraciones:

```json
"vercel-build": "prisma generate && prisma migrate deploy && next build"
```

Solo necesitas hacer un nuevo deploy y las migraciones se ejecutarán automáticamente.

**Opción B: Manual (Si necesitas hacerlo ahora)**

```bash
cd web_backend
npx prisma migrate deploy
```

---

## 🔄 ALTERNATIVAS (Si prefieres otra opción)

### **Opción 2: Prisma Postgres** ⭐ (Segunda mejor opción)

**Ventajas:**
- ✅ Hecho específicamente para Prisma
- ✅ Configuración instantánea
- ✅ Integración perfecta

**Pasos:**
1. Selecciona **"Prisma Postgres"** en el Marketplace
2. Haz clic en **"Create"**
3. Se configurará automáticamente

### **Opción 3: Supabase** (Tercera opción)

**Ventajas:**
- ✅ Postgres completo
- ✅ Tier gratuito generoso
- ✅ Panel de administración completo

**Pasos:**
1. Selecciona **"Supabase"** en el Marketplace
2. Conecta tu cuenta de Supabase (o créala)
3. Crea un nuevo proyecto
4. Copia la Connection String y pégala como `DATABASE_URL` en Vercel

---

## ⚠️ NO RECOMENDADO

### **Turso (SQLite)**
- ❌ Nuestro schema está optimizado para PostgreSQL
- ❌ Algunas funciones de Prisma funcionan mejor con Postgres

### **MongoDB Atlas**
- ❌ Nuestro schema usa Prisma con modelo relacional (Postgres/SQLite)
- ❌ Requeriría cambiar todo el schema

---

## ✅ CHECKLIST DESPUÉS DE CONFIGURAR

Después de configurar la base de datos:

- [ ] `DATABASE_URL` configurada en Vercel (automático con Neon)
- [ ] `API_KEY` configurada: `antivirus-key-2024-prod-12345`
- [ ] `NODE_ENV=production` configurada
- [ ] Migraciones ejecutadas (automático en el build o manual)
- [ ] Nuevo deploy realizado
- [ ] Verificar que el endpoint `/api/logs` funciona

---

## 🧪 VERIFICAR QUE FUNCIONA

Después de configurar todo:

1. **Haz un nuevo deploy en Vercel** (o espera a que se despliegue automáticamente)

2. **Verifica que las tablas se crearon:**
   - Ve a tu proyecto Neon → SQL Editor
   - Ejecuta: `SELECT * FROM antivirus_clients LIMIT 1;`
   - Deberías ver la tabla (aunque esté vacía)

3. **Prueba el endpoint:**
   ```bash
   curl -X POST https://tu-app.vercel.app/api/logs \
     -H "Content-Type: application/json" \
     -H "x-api-key: antivirus-key-2024-prod-12345" \
     -d '{
       "clientId": "test-123",
       "hostname": "test-pc",
       "version": "1.0.0",
       "os": "Windows 10",
       "logs": [{
         "timestamp": "2024-11-15T00:00:00Z",
         "level": "INFO",
         "logger": "test",
         "message": "Test message",
         "component": "test"
       }]
     }'
   ```

4. **Verifica en el dashboard:**
   - Abre: `https://tu-app.vercel.app`
   - Ingresa API Key: `antivirus-key-2024-prod-12345`
   - Deberías ver el cliente de prueba aparecer

---

## 📊 COMPARACIÓN RÁPIDA

| Base de Datos | Gratis | Fácil | Prisma | Recomendado |
|--------------|--------|-------|--------|-------------|
| **Neon** | ✅ 0.5 GB | ⭐⭐⭐⭐⭐ | ✅✅✅ | ⭐⭐⭐⭐⭐ |
| **Prisma Postgres** | ✅ | ⭐⭐⭐⭐⭐ | ✅✅✅✅ | ⭐⭐⭐⭐ |
| **Supabase** | ✅ 500 MB | ⭐⭐⭐⭐ | ✅✅✅ | ⭐⭐⭐⭐ |
| **Turso** | ✅ | ⭐⭐⭐ | ⚠️ SQLite | ⭐⭐ |

---

## 🎯 CONCLUSIÓN

**Elige NEON** - Es la mejor opción para este proyecto:
- Serverless Postgres perfecto para Vercel
- Tier gratuito generoso
- Integración automática
- Compatible 100% con Prisma

¡Solo haz clic en "Neon" y sigue los pasos! 🚀

