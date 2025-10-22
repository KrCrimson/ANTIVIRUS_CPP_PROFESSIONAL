// Temporary stub for ONNX Runtime
// This file provides basic definitions until ONNX Runtime is properly installed

#pragma once

#ifndef NO_ONNXRUNTIME

// If ONNX Runtime is not available, define stubs
namespace Ort {
    class Env {
    public:
        Env() = default;
        ~Env() = default;
    };
    
    class Session {
    public:
        Session() = default;
        ~Session() = default;
    };
    
    class MemoryInfo {
    public:
        MemoryInfo() = default;
        ~MemoryInfo() = default;
    };
    
    class Value {
    public:
        Value() = default;
        ~Value() = default;
    };
}

#else

// Stub implementations when ONNX Runtime is not available
namespace Ort {
    class Env {
    public:
        Env() = default;
        ~Env() = default;
    };
    
    class Session {
    public:
        Session() = default;
        ~Session() = default;
    };
    
    class MemoryInfo {
    public:
        MemoryInfo() = default;
        ~MemoryInfo() = default;
    };
    
    class Value {
    public:
        Value() = default;
        ~Value() = default;
    };
}

#endif