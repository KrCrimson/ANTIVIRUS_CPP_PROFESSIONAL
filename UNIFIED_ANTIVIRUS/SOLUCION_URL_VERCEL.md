# 🔧 SOLUCIÓN: Error 401 - Vercel Deployment Protection

## ❌ Problema

El antivirus está recibiendo error 401 porque está intentando acceder a una URL de **preview deployment** que tiene **Vercel Deployment Protection** habilitado.

El error muestra:
```
Error HTTP 401: Authentication Required
This page requires authentication to access
```

## ✅ Solución

Necesitas usar la **URL de producción** de Vercel en lugar de la URL de preview.

### **PASO 1: Encontrar tu URL de Producción**

1. Ve a **Vercel Dashboard** → Tu Proyecto
2. Ve a **Settings** → **Domains**
3. Busca la URL de producción (sin el hash de preview):
   - ❌ Preview: `unified-antivirus-duzz48bmm-sebastians-projects-487d2baa.vercel.app`
   - ✅ Producción: `unified-antivirus-api.vercel.app` o `unified-antivirus.vercel.app`

**O** si tienes un dominio personalizado configurado, usa ese.

### **PASO 2: Actualizar la Configuración**

Actualiza estos archivos con la URL de producción:

**1. `config/web_logging_optimized.json`:**
```json
{
  "web_logging": {
    "api_url": "https://TU-URL-PRODUCCION.vercel.app/api",
    ...
  }
}
```

**2. `config/web_logging_production.json`:**
```json
{
  "web_logging": {
    "api_url": "https://TU-URL-PRODUCCION.vercel.app/api",
    ...
  }
}
```

**3. `utils/web_log_sender.py` (línea 24):**
```python
DEFAULT_API_ENDPOINT = "https://TU-URL-PRODUCCION.vercel.app/api/logs"
```

### **PASO 3: Deshabilitar Deployment Protection (Opcional)**

Si quieres que las preview deployments también funcionen:

1. Ve a **Vercel Dashboard** → Tu Proyecto → **Settings**
2. Ve a **Deployment Protection**
3. Deshabilita la protección para preview deployments
4. O configura un bypass token

**⚠️ Nota:** Es mejor usar la URL de producción para evitar este problema.

---

## 🔍 Verificar que Funciona

Después de actualizar la URL:

1. **Reinicia el antivirus:**
   ```bash
   python launcher.py
   ```

2. **Verifica los logs:**
   - Deberías ver: `Enviados X logs exitosamente`
   - No deberías ver errores 401

3. **Verifica el dashboard:**
   - Abre el dashboard
   - Deberías ver los logs apareciendo en tiempo real

---

## 📝 Notas

- **Preview deployments** tienen URLs con hash: `project-hash-username.vercel.app`
- **Production deployments** tienen URLs sin hash: `project.vercel.app`
- La URL de producción no requiere autenticación de Vercel
- El header `x-api-key` ya está configurado correctamente

---

## ✅ Cambios Aplicados

- ✅ Header cambiado a `x-api-key` (minúscula) para consistencia
- ✅ Configuración lista para usar URL de producción

**Solo necesitas actualizar la URL en los archivos de configuración con tu URL de producción de Vercel.**

