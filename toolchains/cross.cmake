include("${CMAKE_CURRENT_LIST_DIR}/init.cmake")

set(CROSS_ABI "none")

if(INSTALLAMA_OS STREQUAL "linux")
    if(CROSS_GLIBC)
        set(CROSS_ABI "gnu.2.27")
    else()
        set(CROSS_ABI "musl")
    endif()
elseif(INSTALLAMA_OS STREQUAL "windows")
    set(CROSS_ABI "gnu")
endif()

set(CROSS_TARGET "${INSTALLAMA_ARCH}-${INSTALLAMA_OS}-${CROSS_ABI}")

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
set(CMAKE_C_COMPILER_TARGET "${CROSS_TARGET}")

set(CMAKE_CXX_COMPILER_AR     "${CMAKE_AR}")
set(CMAKE_CXX_COMPILER_RANLIB "${CMAKE_RANLIB}")
set(CMAKE_CXX_COMPILER_TARGET "${CROSS_TARGET}")

set(HOST_C_COMPILER   "${CMAKE_C_COMPILER}")
set(HOST_CXX_COMPILER "${CMAKE_CXX_COMPILER}")

include("${CMAKE_CURRENT_LIST_DIR}/exit.cmake")
