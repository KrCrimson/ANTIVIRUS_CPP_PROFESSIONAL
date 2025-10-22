#!/bin/bash

echo "🛡️  Setting up Antivirus Professional C++ Project"
echo "================================================="

# Create build directory
echo "📁 Creating build directory..."
mkdir -p backend/build

# Check for dependencies
echo "🔍 Checking dependencies..."

# Check for CMake
if command -v cmake &> /dev/null; then
    echo "✅ CMake found: $(cmake --version | head -n1)"
else
    echo "❌ CMake not found. Please install CMake 3.20+"
    exit 1
fi

# Check for Visual Studio (Windows)
if [[ "$OSTYPE" == "msys" ]] || [[ "$OSTYPE" == "win32" ]]; then
    if [ -d "C:/Program Files/Microsoft Visual Studio" ]; then
        echo "✅ Visual Studio found"
    else
        echo "⚠️  Visual Studio not found. Please install Visual Studio 2022"
    fi
fi

# Check for Node.js
if command -v node &> /dev/null; then
    echo "✅ Node.js found: $(node --version)"
else
    echo "❌ Node.js not found. Please install Node.js 18+"
    exit 1
fi

# Configure CMake
echo "⚙️  Configuring CMake..."
cd backend
cmake -B build -S . -DCMAKE_BUILD_TYPE=Debug

if [ $? -eq 0 ]; then
    echo "✅ CMake configuration successful"
else
    echo "❌ CMake configuration failed"
    exit 1
fi

# Build project
echo "🔨 Building project..."
cmake --build build --config Debug

if [ $? -eq 0 ]; then
    echo "✅ Build successful"
else
    echo "⚠️  Build completed with warnings/errors"
fi

cd ..

# Setup frontend
echo "📦 Setting up frontend..."
cd frontend

if [ -f "package.json" ]; then
    echo "📥 Installing frontend dependencies..."
    npm install
    
    if [ $? -eq 0 ]; then
        echo "✅ Frontend dependencies installed"
    else
        echo "❌ Frontend setup failed"
        exit 1
    fi
else
    echo "❌ package.json not found in frontend directory"
    exit 1
fi

cd ..

echo ""
echo "🎉 Setup complete!"
echo ""
echo "Next steps:"
echo "1. Backend: cd backend && cmake --build build --config Release"
echo "2. Frontend: cd frontend && npm run dev"
echo "3. Open VS Code and start developing!"
echo ""
echo "📊 Development URLs:"
echo "   Backend API: http://localhost:8080"
echo "   Frontend Dev: http://localhost:3000"
echo ""