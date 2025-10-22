@echo off
echo 🛡️  Setting up Antivirus Professional C++ Project
echo =================================================

REM Create build directory
echo 📁 Creating build directory...
if not exist "backend\build" mkdir "backend\build"

REM Check for dependencies
echo 🔍 Checking dependencies...

REM Check for CMake
cmake --version >nul 2>&1
if %errorlevel% == 0 (
    echo ✅ CMake found
) else (
    echo ❌ CMake not found. Please install CMake 3.20+
    pause
    exit /b 1
)

REM Check for Visual Studio
if exist "C:\Program Files\Microsoft Visual Studio" (
    echo ✅ Visual Studio found
) else (
    echo ⚠️  Visual Studio not found. Please install Visual Studio 2022
)

REM Check for Node.js
node --version >nul 2>&1
if %errorlevel% == 0 (
    echo ✅ Node.js found
) else (
    echo ❌ Node.js not found. Please install Node.js 18+
    pause
    exit /b 1
)

REM Configure CMake
echo ⚙️  Configuring CMake...
cd backend
cmake -B build -S . -DCMAKE_BUILD_TYPE=Debug

if %errorlevel% == 0 (
    echo ✅ CMake configuration successful
) else (
    echo ❌ CMake configuration failed
    pause
    exit /b 1
)

REM Build project
echo 🔨 Building project...
cmake --build build --config Debug

if %errorlevel% == 0 (
    echo ✅ Build successful
) else (
    echo ⚠️  Build completed with warnings/errors
)

cd ..

REM Setup frontend
echo 📦 Setting up frontend...
cd frontend

if exist "package.json" (
    echo 📥 Installing frontend dependencies...
    npm install
    
    if %errorlevel% == 0 (
        echo ✅ Frontend dependencies installed
    ) else (
        echo ❌ Frontend setup failed
        pause
        exit /b 1
    )
) else (
    echo ❌ package.json not found in frontend directory
    pause
    exit /b 1
)

cd ..

echo.
echo 🎉 Setup complete!
echo.
echo Next steps:
echo 1. Backend: cd backend ^&^& cmake --build build --config Release
echo 2. Frontend: cd frontend ^&^& npm run dev
echo 3. Open VS Code and start developing!
echo.
echo 📊 Development URLs:
echo    Backend API: http://localhost:8080
echo    Frontend Dev: http://localhost:3000
echo.
pause