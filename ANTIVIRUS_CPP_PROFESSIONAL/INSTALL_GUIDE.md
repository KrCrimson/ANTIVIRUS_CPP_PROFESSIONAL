# 🛠️ GUÍA DE INSTALACIÓN DE HERRAMIENTAS DE DESARROLLO

## 📥 OPCIÓN 1: CMake (Recomendado)

### Descarga Manual:
1. Ve a: https://cmake.org/download/
2. Descarga: "Windows x64 Installer" 
3. Ejecuta el instalador
4. ✅ Marca "Add CMake to system PATH"
5. Reinicia PowerShell

### Verificar instalación:
```bash
cmake --version
```

## 📥 OPCIÓN 2: Visual Studio 2022 (Completo)

### Descarga:
1. Ve a: https://visualstudio.microsoft.com/
2. Descarga "Visual Studio Community 2022" (GRATIS)
3. Durante instalación, selecciona:
   - ✅ "Desktop development with C++"
   - ✅ "CMake tools for Visual Studio"
   - ✅ "Windows 10/11 SDK"

## 📥 OPCIÓN 3: Build Tools Only (Ligero)

### Descarga:
1. Ve a: https://visualstudio.microsoft.com/downloads/
2. Busca "Build Tools for Visual Studio 2022"
3. Descarga e instala
4. Selecciona "C++ build tools"

## 📥 OPCIÓN 4: MinGW-w64 (Alternativa ligera)

### Descarga:
1. Ve a: https://www.mingw-w64.org/downloads/
2. Descarga "w64devkit" o "MSYS2"
3. Extrae y agrega al PATH

## 🚀 OPCIÓN 5: Scoop (Gestor de paquetes)

### Instalar Scoop:
```powershell
Set-ExecutionPolicy RemoteSigned -Scope CurrentUser
irm get.scoop.sh | iex
```

### Instalar herramientas:
```powershell
scoop install cmake
scoop install gcc
```

## ⚡ COMPILACIÓN INMEDIATA (Sin instalaciones)

Si no quieres instalar nada ahora, puedes usar el compilador online:

1. Ve a: https://compiler-explorer.com/
2. Copia el código de `simple_main.cpp`
3. Compila y ejecuta directamente en el navegador

## 🎯 PRÓXIMOS PASOS

1. **Instala CMake** (Opción 1 recomendada)
2. **Ejecuta**: `cmake --version` para verificar
3. **Navega a**: `backend/`
4. **Ejecuta**: `cmake -B build -S .`
5. **Compila**: `cmake --build build`

## 🔥 COMPILACIÓN RÁPIDA (AHORA MISMO)

Si tienes cualquier compilador, ejecuta:

```bash
cd backend
./compile.bat
```

Esto detectará automáticamente tu compilador y creará un antivirus simple funcional!