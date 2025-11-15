# 🐛 DEBUG: Error de Conexión con el Backend

## 🔍 Pasos para Diagnosticar el Problema

### **PASO 1: Verificar que el Deploy se Completó**

1. Ve a Vercel → Tu Proyecto → Deployments
2. Verifica que el último deployment tenga estado **"Ready"** (verde)
3. Si está en "Building" o "Error", espera o revisa los logs

### **PASO 2: Probar el Health Check**

Abre en tu navegador:
```
https://tu-app.vercel.app/api/health
```

**Respuesta esperada:**
```json
{
  "status": "ok",
  "timestamp": "2024-11-15T...",
  "database": "connected"
}
```

**Si ves error:**
- `"database": "disconnected"` → Problema con la base de datos
- `404 Not Found` → El deploy no se completó o hay problema de routing

### **PASO 3: Probar el Endpoint de Dashboard Directamente**

Abre en tu navegador (o usa curl):
```
https://tu-app.vercel.app/api/dashboard
```

**Sin API key debería dar:**
```json
{
  "error": "Unauthorized",
  "message": "API key requerida..."
}
```

**Con API key (usando curl):**
```bash
curl -X GET https://tu-app.vercel.app/api/dashboard \
  -H "x-api-key: antivirus-key-2024-prod-12345"
```

### **PASO 4: Revisar Logs de Vercel**

1. Ve a Vercel → Tu Proyecto → Deployments
2. Click en el último deployment
3. Click en **"View Function Logs"**
4. Busca errores relacionados con:
   - Prisma
   - Database connection
   - Migrations

---

## 🔧 Problemas Comunes y Soluciones

### **Problema 1: "El backend no está respondiendo"**

**Causa:** El deploy no se completó o hay un error en el build

**Solución:**
1. Verifica que el deployment esté en estado "Ready"
2. Revisa los logs del build
3. Verifica que no haya errores de compilación

### **Problema 2: "database: disconnected"**

**Causa:** Problema con `DATABASE_URL` o la base de datos

**Solución:**
1. Verifica que `DATABASE_URL` esté configurada en Vercel
2. Verifica que la URL sea correcta (debe incluir `?sslmode=require`)
3. Verifica que la base de datos esté activa en Neon

### **Problema 3: "API key inválida"**

**Causa:** La API key no coincide

**Solución:**
1. Verifica que `API_KEY=antivirus-key-2024-prod-12345` esté en Vercel
2. Verifica que el entorno sea "Production"
3. Reinicia el deployment después de cambiar la variable

### **Problema 4: "Table does not exist"**

**Causa:** Las migraciones no se ejecutaron

**Solución:**
1. Verifica los logs del build - deberías ver `Running prisma migrate deploy...`
2. Si no se ejecutaron, haz un redeploy
3. O ejecuta manualmente desde Neon SQL Editor

---

## 🧪 Test Rápido desde la Consola del Navegador

Abre la consola del navegador (F12) y ejecuta:

```javascript
// Test 1: Health check
fetch('/api/health')
  .then(r => r.json())
  .then(console.log)
  .catch(console.error)

// Test 2: Dashboard con API key
fetch('/api/dashboard', {
  headers: { 'x-api-key': 'antivirus-key-2024-prod-12345' }
})
  .then(r => r.json())
  .then(console.log)
  .catch(console.error)
```

Esto te mostrará el error exacto.

---

## 📋 Checklist de Verificación

- [ ] Deployment en estado "Ready" en Vercel
- [ ] `/api/health` responde correctamente
- [ ] `DATABASE_URL` configurada en Vercel
- [ ] `API_KEY` configurada en Vercel
- [ ] Migraciones ejecutadas (verificar en logs)
- [ ] No hay errores en los logs de Vercel
- [ ] La base de datos está activa en Neon

---

## 🎯 Siguiente Paso

Después de verificar todo lo anterior, comparte:
1. ¿Qué respuesta da `/api/health`?
2. ¿Qué respuesta da `/api/dashboard`?
3. ¿Qué errores ves en los logs de Vercel?

Con esa información podré ayudarte a solucionar el problema específico.

