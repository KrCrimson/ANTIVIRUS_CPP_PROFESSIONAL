cmake_minimum_required(VERSION 3.20)

project(AntivirusCPP 
    VERSION 1.0.0
    DESCRIPTION "High-Performance Antivirus with ML Detection"
    LANGUAGES CXX
)

# C++20 Standard
set(CMAKE_CXX_STANDARD 20)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_CXX_EXTENSIONS OFF)

# Build type
if(NOT CMAKE_BUILD_TYPE)
    set(CMAKE_BUILD_TYPE Debug)
endif()

# Compiler flags
if(MSVC)
    set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} /W4 /permissive-")
    set(CMAKE_CXX_FLAGS_DEBUG "${CMAKE_CXX_FLAGS_DEBUG} /Od /Zi")
    set(CMAKE_CXX_FLAGS_RELEASE "${CMAKE_CXX_FLAGS_RELEASE} /O2 /DNDEBUG")
else()
    set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -Wall -Wextra -Wpedantic -std=c++20")
    set(CMAKE_CXX_FLAGS_DEBUG "${CMAKE_CXX_FLAGS_DEBUG} -g -O0")
    set(CMAKE_CXX_FLAGS_RELEASE "${CMAKE_CXX_FLAGS_RELEASE} -O3 -DNDEBUG")
endif()

# Find packages
find_package(Threads REQUIRED)

# Include directories
include_directories(
    ${CMAKE_SOURCE_DIR}/src
    ${CMAKE_SOURCE_DIR}/include
)

# Antivirus executable - simplified version for Sprint 1
add_executable(AntivirusCPP
    src/main_simple.cpp
)

# Full version (work in progress)
add_executable(AntivirusCPP_Full
    src/main.cpp
    src/core/DetectionEngine.cpp
    src/ml/MLEngine.cpp  
    src/api/APIServer.cpp
)

target_link_libraries(AntivirusCPP
    PRIVATE
        Threads::Threads
)

target_link_libraries(AntivirusCPP_Full
    PRIVATE
        Threads::Threads
)

# Windows specific libraries
if(WIN32)
    target_link_libraries(AntivirusCPP
        PRIVATE
            ws2_32
            winmm
            psapi
            wbemuuid
            ole32
            oleaut32
    )
    
    target_link_libraries(AntivirusCPP_Full
        PRIVATE
            ws2_32
            winmm
            psapi
            wbemuuid
            ole32
            oleaut32
    )
endif()

# Print configuration info
message(STATUS "Build type: ${CMAKE_BUILD_TYPE}")
message(STATUS "C++ Standard: ${CMAKE_CXX_STANDARD}")
message(STATUS "Compiler: ${CMAKE_CXX_COMPILER_ID}")
message(STATUS "Source directory: ${CMAKE_SOURCE_DIR}")
message(STATUS "Binary directory: ${CMAKE_BINARY_DIR}")