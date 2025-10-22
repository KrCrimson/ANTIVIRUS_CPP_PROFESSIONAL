@echo off
echo 🛡️  Compiling Simple Antivirus (No CMake Required)
echo ================================================

REM Check if we have g++ or cl.exe available
where g++ >nul 2>&1
if %errorlevel% == 0 (
    echo ✅ g++ found - Using MinGW
    echo 🔨 Compiling with g++...
    g++ -std=c++20 -O2 -Wall -Wextra -o simple_antivirus.exe simple_main.cpp -pthread
    
    if %errorlevel% == 0 (
        echo ✅ Compilation successful!
        echo 🚀 Running simple_antivirus.exe...
        echo.
        simple_antivirus.exe
    ) else (
        echo ❌ Compilation failed
    )
    
) else (
    REM Check for Visual Studio
    where cl.exe >nul 2>&1
    if %errorlevel% == 0 (
        echo ✅ cl.exe found - Using MSVC
        echo 🔨 Compiling with MSVC...
        cl /std:c++20 /EHsc /O2 simple_main.cpp /Fe:simple_antivirus.exe
        
        if %errorlevel% == 0 (
            echo ✅ Compilation successful!
            echo 🚀 Running simple_antivirus.exe...
            echo.
            simple_antivirus.exe
        ) else (
            echo ❌ Compilation failed
        )
    ) else (
        echo ❌ No C++ compiler found!
        echo.
        echo Please install one of the following:
        echo 1. MinGW-w64: https://www.mingw-w64.org/
        echo 2. Visual Studio 2022: https://visualstudio.microsoft.com/
        echo 3. Build Tools for Visual Studio 2022
        echo.
        pause
    )
)

pause