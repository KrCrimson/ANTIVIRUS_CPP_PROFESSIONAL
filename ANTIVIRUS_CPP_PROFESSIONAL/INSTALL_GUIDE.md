# � INSTALACIÓN RÁPIDA - ANTIVIRUS C++ PROFESSIONAL

## ⚡ INSTALACIÓN AUTOMÁTICA (RECOMENDADA)

### 🎯 **OPCIÓN 1: PC NUEVA (Todo automático - 10 minutos)**

```powershell
# 1. Clonar proyecto
git clone https://github.com/KrCrimson/ANTIVIRUS_CPP_PROFESSIONAL.git
cd ANTIVIRUS_CPP_PROFESSIONAL

# 2. Abrir PowerShell COMO ADMINISTRADOR
Set-ExecutionPolicy RemoteSigned -Scope CurrentUser
.\install_dependencies.ps1

# 3. Ejecutar antivirus
cd backend
cmake --build build --config Debug --target AntivirusCPP
.\build\Debug\AntivirusCPP.exe
```

**✅ Instala automáticamente: Visual Studio 2022, CMake, Node.js, Git**

---

### ⚡ **OPCIÓN 2: YA TIENES HERRAMIENTAS (2 minutos)**

```powershell
# 1. Verificar lo que tienes
.\verify_installation.ps1

# 2. Si sale todo ✅, ejecutar:
cd backend
cmake --build build --config Debug --target AntivirusCPP
.\build\Debug\AntivirusCPP.exe

# 3. Si falta algo:
.\quick_setup.ps1
```

---

### �️ **OPCIÓN 3: INSTALACIÓN MANUAL**

**Solo si los scripts automáticos fallan:**

1. **Visual Studio 2022:** https://visualstudio.microsoft.com/downloads/
   - Descargar "Build Tools for Visual Studio 2022" 
   - Seleccionar "C++ build tools"

2. **CMake:** https://cmake.org/download/
   - Descargar "Windows x64 Installer"
   - ✅ Marcar "Add CMake to system PATH"

3. **Node.js:** https://nodejs.org/
   - Descargar LTS version

4. **Configurar proyecto:**
```powershell
.\quick_setup.ps1
```

---

## 🔍 **VERIFICAR INSTALACIÓN**

```powershell
.\verify_installation.ps1
```

**Debe mostrar:**
```
✅ Git: OK
✅ CMake: OK  
✅ Node.js: OK
✅ Visual Studio Build Tools: OK
📊 Resultado: 8/8 verificaciones exitosas
```

---

## 🎉 **EJECUTAR EL ANTIVIRUS**

```powershell
# Backend (Terminal 1)
cd backend
cmake --build build --config Debug --target AntivirusCPP
.\build\Debug\AntivirusCPP.exe

# Frontend (Terminal 2) 
cd frontend
npm start
```

**URLs:**
- 🔗 Backend API: http://localhost:8080/api/status
- 🖥️ Frontend: Se abre automáticamente

---

## 🚨 **SOLUCIÓN DE PROBLEMAS**

| Error | Solución |
|-------|----------|
| "No se puede ejecutar scripts" | `Set-ExecutionPolicy RemoteSigned -Scope CurrentUser` |
| "Requiere administrador" | Click derecho → "Ejecutar como administrador" |
| "CMake no encontrado" | Ejecutar `.\install_dependencies.ps1` |
| "Visual Studio no encontrado" | Instalar VS2022 Build Tools manualmente |

---

## ⏱️ **TIEMPOS DE INSTALACIÓN**

| Método | Tiempo | Para quién |
|--------|--------|------------|
| `install_dependencies.ps1` | 10-15 min | PC nueva |
| `quick_setup.ps1` | 2-3 min | Ya tienes VS/CMake |
| `verify_installation.ps1` | 30 seg | Verificar estado |
| Manual | 20-30 min | Scripts fallan |

---

## 🎯 **RESULTADO FINAL**

Si todo funciona verás:
```
🛡️ Antivirus Professional C++ - Starting...
✅ Detection engine initialized
✅ ML engine initialized  
✅ API server started
🌐 API Server: http://localhost:8080
```

**¡Antivirus funcionando! 🚀**