set(CMAKE_SYSTEM_NAME      $ENV{CMAKE_SYSTEM_NAME})
set(CMAKE_SYSTEM_PROCESSOR $ENV{CMAKE_SYSTEM_PROCESSOR})

if(CMAKE_SYSTEM_NAME STREQUAL "Linux")
    set(CROSS_TARGET "linux-musl")
endif()

if(CMAKE_SYSTEM_NAME STREQUAL "Windows")
    set(CROSS_TARGET "windows-gnu")
endif()

if(CMAKE_SYSTEM_NAME STREQUAL "Darwin")
    set(CROSS_TARGET "macos-none")
endif()

if(CMAKE_SYSTEM_PROCESSOR MATCHES "^(aarch64|ARM64|arm64)$")
    set(CROSS_ARCH "aarch64")
endif()

if(CMAKE_SYSTEM_PROCESSOR MATCHES "^(x86_64|AMD64|amd64)$")
    set(CROSS_ARCH "x86_64")
endif()

find_program(ZIG zig REQUIRED)

if(NOT EXISTS "${CMAKE_BINARY_DIR}/zig-cc")
    execute_process(
        COMMAND ${ZIG} cc "${CMAKE_CURRENT_LIST_DIR}/zig.c" -o "${CMAKE_BINARY_DIR}/zig-cc"
    )
    foreach(WRAPPER c++ ar ranlib objcopy)
        file(COPY_FILE "${CMAKE_BINARY_DIR}/zig-cc" "${CMAKE_BINARY_DIR}/zig-${WRAPPER}")
    endforeach()
endif()

set(CMAKE_C_COMPILER   "${CMAKE_BINARY_DIR}/zig-cc")
set(CMAKE_ASM_COMPILER "${CMAKE_BINARY_DIR}/zig-cc")
set(CMAKE_CXX_COMPILER "${CMAKE_BINARY_DIR}/zig-c++")
set(CMAKE_AR           "${CMAKE_BINARY_DIR}/zig-ar")
set(CMAKE_RANLIB       "${CMAKE_BINARY_DIR}/zig-ranlib")
set(CMAKE_OBJCOPY      "${CMAKE_BINARY_DIR}/zig-objcopy")

set(CMAKE_C_COMPILER_AR     "${CMAKE_AR}")
set(CMAKE_C_COMPILER_RANLIB "${CMAKE_RANLIB}")
set(CMAKE_C_COMPILER_TARGET "${CROSS_ARCH}-${CROSS_TARGET}")

set(CMAKE_CXX_COMPILER_AR     "${CMAKE_AR}")
set(CMAKE_CXX_COMPILER_RANLIB "${CMAKE_RANLIB}")
set(CMAKE_CXX_COMPILER_TARGET "${CROSS_ARCH}-${CROSS_TARGET}")

include("${CMAKE_CURRENT_LIST_DIR}/base.cmake")
