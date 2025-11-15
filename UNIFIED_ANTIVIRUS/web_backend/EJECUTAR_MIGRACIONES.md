# 🔧 EJECUTAR MIGRACIONES MANUALMENTE

## ❌ Problema

Las tablas no existen en la base de datos porque la migración SQL estaba usando sintaxis de SQLite en lugar de PostgreSQL.

## ✅ Solución Aplicada

He corregido la migración SQL (`prisma/migrations/20251115064615_init/migration.sql`) para usar sintaxis de PostgreSQL:
- `DATETIME` → `TIMESTAMP(3)`
- `REAL` → `DOUBLE PRECISION`
- Agregados defaults para `updatedAt`

---

## 🚀 OPCIÓN 1: Redeploy en Vercel (Recomendado)

El `vercel.json` ya está configurado para ejecutar `npm run vercel-build` que incluye:
1. `prisma generate`
2. `prisma migrate deploy`
3. `next build`

**Pasos:**
1. Haz commit y push de los cambios:
   ```bash
   git add .
   git commit -m "Fix: Corregir migración SQL para PostgreSQL"
   git push
   ```

2. Vercel detectará el push y hará un nuevo deploy automáticamente

3. Espera a que el deploy termine (2-3 minutos)

4. Verifica que las tablas se crearon:
   - Ve a los logs de Vercel
   - Busca: `Running migrations...`
   - Deberías ver: `Applied migration: 20251115064615_init`

---

## 🛠️ OPCIÓN 2: Ejecutar Migraciones Manualmente (Si el redeploy no funciona)

Si después del redeploy las tablas aún no existen, puedes ejecutar las migraciones manualmente:

### **Paso 1: Instalar Dependencias Localmente**

```bash
cd web_backend
npm install
```

### **Paso 2: Configurar Variable de Entorno**

Asegúrate de tener `DATABASE_URL` configurada:

**Windows (PowerShell):**
```powershell
$env:DATABASE_URL="postgresql://usuario:password@host:5432/database?sslmode=require"
```

**Linux/Mac:**
```bash
export DATABASE_URL="postgresql://usuario:password@host:5432/database?sslmode=require"
```

### **Paso 3: Ejecutar Migraciones**

```bash
# Generar cliente de Prisma
npx prisma generate

# Ejecutar migraciones
npx prisma migrate deploy
```

**O usar el script:**
```bash
node scripts/run-migrations.js
```

### **Paso 4: Verificar que Funcionó**

Deberías ver:
```
✅ Applied migration: 20251115064615_init
```

---

## 🔍 Verificar que las Tablas Existen

### **Opción A: Usar Prisma Studio**

```bash
cd web_backend
npx prisma studio
```

Abre `http://localhost:5555` y verifica que ves las tablas:
- `antivirus_clients`
- `log_entries`
- `alerts`
- `log_statistics`
- `users`

### **Opción B: Consultar Directamente la Base de Datos**

Si tienes acceso a tu base de datos PostgreSQL (Neon, Supabase, etc.), ejecuta:

```sql
SELECT table_name 
FROM information_schema.tables 
WHERE table_schema = 'public';
```

Deberías ver las 5 tablas listadas arriba.

---

## ⚠️ Si Aún Hay Problemas

### **Error: "Migration already applied"**

Si ves este error, significa que la migración se registró pero las tablas no se crearon. En este caso:

1. **Resetear la base de datos (⚠️ CUIDADO: Esto borra todos los datos):**
   ```bash
   npx prisma migrate reset
   ```

2. **O crear las tablas manualmente:**
   ```bash
   npx prisma db push
   ```

### **Error: "Connection refused" o "Authentication failed"**

Verifica que:
- La `DATABASE_URL` es correcta
- La base de datos está accesible desde tu IP
- Las credenciales son correctas

---

## ✅ Después de Ejecutar las Migraciones

1. **Haz un redeploy en Vercel** (si ejecutaste las migraciones localmente)
2. **Prueba el dashboard:**
   - Abre: `https://tu-app.vercel.app`
   - Ingresa la API key: `antivirus-key-2024-prod-12345`
   - Deberías ver el dashboard sin errores

3. **Prueba enviar logs desde el antivirus:**
   ```bash
   python launcher.py
   ```
   - Espera 30-60 segundos
   - Verifica en el dashboard que los logs aparecen

---

## 📝 Notas

- Las migraciones corregidas están en: `web_backend/prisma/migrations/20251115064615_init/migration.sql`
- El `vercel.json` está configurado para ejecutar migraciones automáticamente
- Si necesitas crear nuevas migraciones en el futuro, usa: `npx prisma migrate dev`

