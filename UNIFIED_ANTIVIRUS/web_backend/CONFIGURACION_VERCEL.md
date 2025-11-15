# 🚀 CONFIGURACIÓN DE VERCEL PARA RECIBIR DATOS

## ✅ VERIFICACIÓN ACTUAL

### Estado del Sistema:
- ✅ **Antivirus enviando logs**: Funcionando correctamente
- ✅ **Backend API**: Implementado y listo
- ✅ **Autenticación**: API Key configurada
- ✅ **CORS**: Configurado correctamente

### API Key del Antivirus:
```
antivirus-key-2024-prod-12345
```

---

## 📋 PASOS PARA CONFIGURAR VERCEL

### **PASO 1: Verificar que el Backend esté Desplegado**

1. Ve a tu proyecto en Vercel: https://vercel.com/dashboard
2. Verifica que el proyecto esté desplegado
3. Anota la URL de tu deployment (ej: `https://unified-antivirus-duzz48bmm-sebastians-projects-487d2baa.vercel.app`)

---

### **PASO 2: Configurar Variables de Entorno en Vercel**

Ve a tu proyecto en Vercel → **Settings** → **Environment Variables** y agrega:

#### **Variables Requeridas:**

```bash
# API Key para autenticación (DEBE coincidir con la del antivirus)
API_KEY=antivirus-key-2024-prod-12345

# Base de Datos (PostgreSQL)
# Opción 1: Usar PostgreSQL de Vercel (recomendado)
DATABASE_URL=postgresql://user:password@host:port/database?sslmode=require

# Opción 2: Usar SQLite (solo para desarrollo, no recomendado en producción)
# DATABASE_URL=file:./dev.db

# Entorno
NODE_ENV=production
```

#### **Cómo obtener DATABASE_URL:**

**Opción A: PostgreSQL de Vercel (Gratis)**
1. En tu proyecto de Vercel → **Storage** → **Create Database**
2. Selecciona **Postgres**
3. Copia la **Connection String** que te proporciona
4. Pégala como `DATABASE_URL`

**Opción B: Neon.tech (Gratis)**
1. Ve a https://neon.tech
2. Crea una cuenta gratuita
3. Crea un nuevo proyecto
4. Copia la **Connection String**
5. Pégala como `DATABASE_URL`

---

### **PASO 3: Ejecutar Migraciones de Base de Datos**

Después de configurar `DATABASE_URL`, necesitas crear las tablas:

**Opción A: Desde Vercel CLI (Recomendado)**

```bash
cd web_backend
npm install -g vercel
vercel login
vercel link  # Conecta con tu proyecto

# Ejecutar migraciones
npx prisma migrate deploy
```

**Opción B: Desde el Dashboard de Vercel**

1. Ve a tu proyecto → **Settings** → **Build & Development Settings**
2. En **Build Command**, asegúrate de tener:
   ```bash
   npm run vercel-build
   ```
3. En **Install Command**:
   ```bash
   npm install
   ```
4. Esto ejecutará las migraciones automáticamente en cada deploy

---

### **PASO 4: Verificar que el Backend Recibe Datos**

#### **Test Manual:**

1. **Verificar que el endpoint funciona:**
   ```bash
   curl -X POST https://tu-app.vercel.app/api/logs \
     -H "Content-Type: application/json" \
     -H "x-api-key: antivirus-key-2024-prod-12345" \
     -d '{
       "clientId": "test-client-123",
       "hostname": "test-pc",
       "version": "1.0.0",
       "os": "Windows 10",
       "logs": [{
         "timestamp": "2024-11-15T02:17:03Z",
         "level": "INFO",
         "logger": "test",
         "message": "Test log message",
         "component": "test"
       }]
     }'
   ```

2. **Respuesta esperada:**
   ```json
   {
     "success": true,
     "message": "1 logs processed successfully",
     "clientId": "test-client-123",
     "timestamp": "2024-11-15T02:17:03.000Z"
   }
   ```

#### **Test desde el Antivirus:**

1. Ejecuta el antivirus:
   ```bash
   python launcher.py
   ```

2. Espera 30-60 segundos para que se envíen los primeros logs

3. Verifica en el dashboard:
   - URL: `https://tu-app.vercel.app`
   - API Key: `antivirus-key-2024-prod-12345`
   - Deberías ver logs apareciendo

---

### **PASO 5: Verificar el Dashboard**

1. Abre tu URL de Vercel en el navegador
2. Ingresa la API Key: `antivirus-key-2024-prod-12345`
3. Deberías ver:
   - ✅ Total de clientes > 0
   - ✅ Logs recientes apareciendo
   - ✅ Gráficos actualizándose cada 30 segundos

---

## 🔧 CONFIGURACIÓN ADICIONAL

### **Ajustar vercel.json (si es necesario):**

El archivo `vercel.json` ya está configurado correctamente con:
- ✅ CORS habilitado
- ✅ Timeout de 30 segundos para APIs
- ✅ Headers correctos

### **Verificar que Prisma esté configurado:**

El archivo `package.json` ya tiene el script correcto:
```json
"vercel-build": "prisma generate && prisma migrate deploy && next build"
```

Esto asegura que:
1. Se generen los clientes de Prisma
2. Se ejecuten las migraciones
3. Se construya la aplicación

---

## 🐛 SOLUCIÓN DE PROBLEMAS

### **Error: "API key inválida"**

**Solución:**
1. Verifica que la variable `API_KEY` en Vercel sea exactamente: `antivirus-key-2024-prod-12345`
2. Verifica que el antivirus esté usando la misma API key en `config/web_logging_production.json`
3. Reinicia el deployment en Vercel después de cambiar variables de entorno

### **Error: "Database connection failed"**

**Solución:**
1. Verifica que `DATABASE_URL` esté configurada correctamente en Vercel
2. Asegúrate de que la base de datos esté accesible desde internet
3. Verifica que el formato de la URL sea correcto (debe incluir `?sslmode=require` para PostgreSQL)

### **Error: "Table does not exist"**

**Solución:**
1. Ejecuta las migraciones:
   ```bash
   cd web_backend
   npx prisma migrate deploy
   ```
2. O verifica que el build command incluya `prisma migrate deploy`

### **Los logs no aparecen en el dashboard**

**Solución:**
1. Verifica que el antivirus esté enviando logs (revisa la consola)
2. Verifica que el endpoint sea correcto: `/api/logs`
3. Revisa los logs de Vercel en el dashboard para ver errores
4. Verifica que la API key sea correcta

---

## ✅ CHECKLIST FINAL

Antes de considerar que todo está configurado:

- [ ] Variables de entorno configuradas en Vercel:
  - [ ] `API_KEY=antivirus-key-2024-prod-12345`
  - [ ] `DATABASE_URL` configurada (PostgreSQL)
  - [ ] `NODE_ENV=production`
- [ ] Migraciones de base de datos ejecutadas
- [ ] Backend desplegado y accesible
- [ ] Test de endpoint `/api/logs` exitoso
- [ ] Antivirus enviando logs correctamente
- [ ] Dashboard mostrando datos

---

## 📞 VERIFICACIÓN RÁPIDA

Ejecuta este comando para verificar que todo funciona:

```bash
# Test del endpoint
curl -X POST https://tu-app.vercel.app/api/logs \
  -H "Content-Type: application/json" \
  -H "x-api-key: antivirus-key-2024-prod-12345" \
  -d '{"clientId":"test","hostname":"test","version":"1.0","os":"Windows","logs":[{"timestamp":"2024-11-15T00:00:00Z","level":"INFO","logger":"test","message":"test"}]}'
```

Si recibes `{"success": true, ...}`, ¡todo está funcionando! ✅

