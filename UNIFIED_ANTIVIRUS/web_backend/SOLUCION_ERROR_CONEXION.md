# 🔧 SOLUCIÓN AL ERROR DE CONEXIÓN

## 🐛 Problema Detectado

El error "Error de conexión con el backend" puede deberse a:

1. **Consulta SQL incompatible** - Estaba usando `strftime` (SQLite) pero ahora usamos PostgreSQL
2. **Migraciones no ejecutadas** - Las tablas pueden no existir aún
3. **Error en la conexión a la base de datos**

## ✅ Correcciones Aplicadas

### 1. Consulta SQL Corregida

Cambié la consulta de SQLite a PostgreSQL:
- ❌ Antes: `strftime('%Y-%m-%d %H:00:00', timestamp)`
- ✅ Ahora: `DATE_TRUNC('hour', timestamp)`

### 2. Manejo de Errores Mejorado

Ahora el frontend muestra el mensaje de error específico del backend.

### 3. Schema Actualizado

Eliminé `@db.Timestamp` que puede causar problemas con PostgreSQL.

---

## 📋 PASOS PARA SOLUCIONAR

### **PASO 1: Crear Migración Nueva**

Necesitas crear una nueva migración porque cambiamos el schema:

```bash
cd web_backend
npx prisma migrate dev --name update_to_postgresql
```

O si estás en producción:

```bash
cd web_backend
npx prisma migrate deploy
```

### **PASO 2: Hacer Nuevo Deploy en Vercel**

1. Haz commit de los cambios:
   ```bash
   git add .
   git commit -m "Fix PostgreSQL compatibility"
   git push
   ```

2. O haz redeploy desde Vercel:
   - Ve a Deployments
   - Click en los 3 puntos
   - Selecciona "Redeploy"

### **PASO 3: Verificar Logs de Vercel**

Si sigue fallando, revisa los logs:

1. Ve a Vercel → Tu Proyecto → Deployments
2. Click en el último deployment
3. Click en "View Function Logs"
4. Busca errores relacionados con:
   - Base de datos
   - Migraciones
   - Prisma

---

## 🧪 VERIFICAR QUE FUNCIONA

### **Test 1: Verificar Migraciones**

Desde el dashboard de Neon, ejecuta:

```sql
SELECT table_name 
FROM information_schema.tables 
WHERE table_schema = 'public';
```

Deberías ver:
- `antivirus_clients`
- `log_entries`
- `alerts`
- `log_statistics`
- `users`

### **Test 2: Probar Endpoint Directamente**

```bash
curl -X GET https://tu-app.vercel.app/api/dashboard \
  -H "x-api-key: antivirus-key-2024-prod-12345"
```

**Respuesta esperada:**
```json
{
  "overview": {
    "totalClients": 0,
    "activeClients": 0,
    "totalLogs": 0,
    "criticalAlerts": 0
  },
  ...
}
```

### **Test 3: Probar desde el Dashboard**

1. Abre el dashboard
2. Ingresa la API key
3. Ahora debería mostrar el error específico (si hay alguno) o cargar correctamente

---

## 🐛 ERRORES COMUNES Y SOLUCIONES

### **Error: "relation does not exist"**

**Causa:** Las migraciones no se ejecutaron

**Solución:**
```bash
cd web_backend
npx prisma migrate deploy
```

### **Error: "function strftime does not exist"**

**Causa:** Ya corregido - la consulta ahora usa `DATE_TRUNC`

**Solución:** Ya está aplicado en el código

### **Error: "connection refused" o "timeout"**

**Causa:** Problema con `DATABASE_URL`

**Solución:**
1. Verifica que `DATABASE_URL` esté configurada en Vercel
2. Verifica que la URL sea correcta (debe incluir `?sslmode=require`)
3. Verifica que la base de datos esté activa en Neon

### **Error: "API key inválida"**

**Causa:** La API key no coincide

**Solución:**
1. Verifica que `API_KEY=antivirus-key-2024-prod-12345` esté en Vercel
2. Verifica que el entorno sea "Production"
3. Reinicia el deployment después de cambiar la variable

---

## ✅ CHECKLIST

- [ ] Schema actualizado (eliminado `@db.Timestamp`)
- [ ] Consulta SQL corregida (usando `DATE_TRUNC`)
- [ ] Manejo de errores mejorado
- [ ] Migraciones ejecutadas
- [ ] Nuevo deploy realizado
- [ ] Logs de Vercel revisados
- [ ] Test del endpoint exitoso

---

## 🎯 SIGUIENTE PASO

Después de hacer el nuevo deploy, el error debería mostrar más información específica. Si sigue fallando, revisa los logs de Vercel para ver el error exacto.

