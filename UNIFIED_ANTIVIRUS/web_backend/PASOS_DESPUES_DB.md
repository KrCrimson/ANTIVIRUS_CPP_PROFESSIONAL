# ✅ PASOS DESPUÉS DE CREAR LA BASE DE DATOS

## 🎉 ¡Base de Datos Creada!

Ahora necesitas completar la configuración. Sigue estos pasos:

---

## 📋 PASO 1: Verificar Variables de Entorno en Vercel

Ve a tu proyecto en Vercel → **Settings** → **Environment Variables**

### Variables que DEBES tener:

✅ **DATABASE_URL** - Ya está configurada automáticamente por Neon

❓ **API_KEY** - Verifica que esté configurada:
```
API_KEY=antivirus-key-2024-prod-12345
```

❓ **NODE_ENV** - Verifica que esté configurada:
```
NODE_ENV=production
```

**Si faltan, agrégalas:**
1. Haz clic en **"Add New"**
2. Agrega cada variable
3. Asegúrate de seleccionar **"Production"** en el selector de entorno

---

## 📋 PASO 2: Ejecutar Migraciones (Crear Tablas)

Tienes dos opciones:

### **Opción A: Automático (Recomendado) ⭐**

El `package.json` ya tiene configurado el script `vercel-build` que ejecuta las migraciones automáticamente:

```json
"vercel-build": "prisma generate && prisma migrate deploy && next build"
```

**Solo necesitas hacer un nuevo deploy:**

1. Ve a tu proyecto en Vercel
2. Haz clic en **"Deployments"**
3. Haz clic en los **3 puntos** del último deployment
4. Selecciona **"Redeploy"**
5. O simplemente haz un **push a tu repositorio** y se desplegará automáticamente

Las migraciones se ejecutarán automáticamente durante el build.

### **Opción B: Manual (Si quieres hacerlo ahora)**

Si quieres ejecutar las migraciones manualmente desde tu máquina:

```bash
cd web_backend

# Generar cliente de Prisma
npx prisma generate

# Ejecutar migraciones (crear tablas)
npx prisma migrate deploy
```

**Nota:** Para esto necesitas tener acceso a la base de datos desde tu máquina local. Si usas Neon, puedes obtener la connection string desde el dashboard de Neon.

---

## 📋 PASO 3: Verificar que las Tablas se Crearon

### **Desde el Dashboard de Neon:**

1. Ve a tu proyecto en Neon: https://console.neon.tech
2. Haz clic en tu proyecto
3. Ve a **"SQL Editor"**
4. Ejecuta esta consulta:

```sql
SELECT table_name 
FROM information_schema.tables 
WHERE table_schema = 'public';
```

**Deberías ver estas tablas:**
- `antivirus_clients`
- `log_entries`
- `alerts`
- `log_statistics`
- `users`

### **O verifica desde Vercel:**

Después del deploy, revisa los logs del build. Deberías ver algo como:

```
Running prisma migrate deploy...
Applied migration: 20251115064615_init
```

---

## 📋 PASO 4: Probar que Todo Funciona

### **Test 1: Verificar el Endpoint de Logs**

Ejecuta este comando (reemplaza `tu-app.vercel.app` con tu URL):

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
      "timestamp": "2024-11-15T00:00:00Z",
      "level": "INFO",
      "logger": "test",
      "message": "Test log message",
      "component": "test"
    }]
  }'
```

**Respuesta esperada:**
```json
{
  "success": true,
  "message": "1 logs processed successfully",
  "clientId": "test-client-123",
  "timestamp": "2024-11-15T..."
}
```

### **Test 2: Verificar en el Dashboard**

1. Abre tu URL de Vercel en el navegador
2. Ingresa la API Key: `antivirus-key-2024-prod-12345`
3. Deberías ver:
   - ✅ Total de clientes: 1 (o más si ya hay datos)
   - ✅ Logs recientes apareciendo
   - ✅ Gráficos funcionando

### **Test 3: Desde el Antivirus**

1. Asegúrate de que el antivirus esté ejecutándose:
   ```bash
   python launcher.py
   ```

2. Espera 30-60 segundos para que se envíen los primeros logs

3. Refresca el dashboard - deberías ver:
   - Tu cliente apareciendo (hostname de tu PC)
   - Logs en tiempo real
   - Métricas actualizándose

---

## 🐛 SOLUCIÓN DE PROBLEMAS

### **Error: "Table does not exist"**

**Solución:**
- Las migraciones no se ejecutaron
- Haz un nuevo deploy o ejecuta manualmente: `npx prisma migrate deploy`

### **Error: "API key inválida"**

**Solución:**
- Verifica que `API_KEY=antivirus-key-2024-prod-12345` esté en Vercel
- Asegúrate de que el entorno sea "Production"
- Reinicia el deployment después de agregar la variable

### **Error: "Database connection failed"**

**Solución:**
- Verifica que `DATABASE_URL` esté configurada correctamente
- Revisa que la URL incluya `?sslmode=require` al final
- Verifica que la base de datos esté activa en Neon

### **Los logs no aparecen en el dashboard**

**Solución:**
1. Verifica que el antivirus esté enviando logs (revisa la consola)
2. Espera 30-60 segundos (los logs se envían cada 30 segundos)
3. Verifica que la API key sea correcta
4. Revisa los logs de Vercel en el dashboard para ver errores

---

## ✅ CHECKLIST FINAL

Antes de considerar que todo está listo:

- [ ] `DATABASE_URL` configurada (automático con Neon) ✅
- [ ] `API_KEY=antivirus-key-2024-prod-12345` configurada
- [ ] `NODE_ENV=production` configurada
- [ ] Migraciones ejecutadas (automático en deploy o manual)
- [ ] Tablas creadas en la base de datos (verificado)
- [ ] Nuevo deploy realizado
- [ ] Test del endpoint `/api/logs` exitoso
- [ ] Dashboard mostrando datos

---

## 🎯 SIGUIENTE PASO

Una vez que todo esté verificado:

1. **Ejecuta el antivirus** (si no está corriendo):
   ```bash
   python launcher.py
   ```

2. **Abre el dashboard**:
   - URL: `https://tu-app.vercel.app`
   - API Key: `antivirus-key-2024-prod-12345`

3. **¡Disfruta viendo tus logs en tiempo real!** 🎉

---

## 📞 ¿Necesitas Ayuda?

Si algo no funciona:
1. Revisa los logs de Vercel (Deployments → Click en el deployment → View Function Logs)
2. Revisa los logs del antivirus en la consola
3. Verifica que todas las variables de entorno estén correctas

¡Todo debería estar funcionando ahora! 🚀

