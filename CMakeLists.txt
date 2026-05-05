cmake_minimum_required(VERSION 3.28)
project(installama LANGUAGES C CXX)

find_program(ZSTD zstd REQUIRED)

include(FetchContent)

macro(FetchDep NAME DEFAULT_REPO DEFAULT_VERSION)
    string(TOUPPER ${NAME} NAME_UPPER)

    if(NOT "$ENV{${NAME_UPPER}_REPO}" STREQUAL "")
        set(DEFAULT_REPO "$ENV{${NAME_UPPER}_REPO}")
    endif()
    set(${NAME_UPPER}_REPO "${DEFAULT_REPO}" CACHE STRING "${NAME} repository")

    if(NOT "$ENV{${NAME_UPPER}_VERSION}" STREQUAL "")
        set(DEFAULT_VERSION "$ENV{${NAME_UPPER}_VERSION}")
    endif()
    set(${NAME_UPPER}_VERSION "${DEFAULT_VERSION}" CACHE STRING "${NAME} version")

    if(EXISTS "${CMAKE_SOURCE_DIR}/deps/${NAME}/CMakeLists.txt")
        FetchContent_Declare(${NAME}
            SOURCE_DIR "${CMAKE_SOURCE_DIR}/deps/${NAME}"
            ${ARGN}
        )
    else()
        FetchContent_Declare(${NAME}
            GIT_REPOSITORY "${${NAME_UPPER}_REPO}"
            GIT_TAG        "${${NAME_UPPER}_VERSION}"
            SOURCE_DIR     "${CMAKE_SOURCE_DIR}/deps/${NAME}"
            ${ARGN}
        )
    endif()
endmacro()

FetchDep(boringssl
    "https://boringssl.googlesource.com/boringssl"
    "main"
    EXCLUDE_FROM_ALL
)

FetchDep(llamacpp
    "https://github.com/ggml-org/llama.cpp"
    "master"
)

set(CMAKE_BUILD_TYPE "Release" CACHE STRING "" FORCE)
set(BUILD_SHARED_LIBS OFF CACHE BOOL "" FORCE)

set(CMAKE_INTERPROCEDURAL_OPTIMIZATION ON CACHE BOOL "" FORCE)
set(CMAKE_POSITION_INDEPENDENT_CODE    ON CACHE BOOL "" FORCE)

set(GGML_CCACHE OFF CACHE BOOL "" FORCE)
set(GGML_NATIVE OFF CACHE BOOL "" FORCE)
set(GGML_OPENMP OFF CACHE BOOL "" FORCE)
set(GGML_LTO    OFF CACHE BOOL "" FORCE)

set(LLAMA_BUILD_BORINGSSL ON  CACHE BOOL "" FORCE)
set(LLAMA_BUILD_COMMON    ON  CACHE BOOL "" FORCE)
set(LLAMA_BUILD_TOOLS     ON  CACHE BOOL "" FORCE)
set(LLAMA_BUILD_SERVER    ON  CACHE BOOL "" FORCE)

#add_compile_options(
#    -ffp-model=fast
#    -fno-finite-math-only
#)

add_compile_options(
    -fmacro-prefix-map=${CMAKE_SOURCE_DIR}/deps/boringssl/=
    -fmacro-prefix-map=${CMAKE_SOURCE_DIR}/deps/llamacpp/=
    -ffunction-sections
    -fdata-sections
    -fno-ident
)

if(CMAKE_C_COMPILER_ID STREQUAL "Clang" OR CMAKE_C_COMPILER_ID STREQUAL "GNU")
    add_link_options(-static-libgcc -static-libstdc++)
    add_link_options(-Wl,--gc-sections -Wl,--strip-all)
elseif(CMAKE_C_COMPILER_ID STREQUAL "AppleClang")
    add_link_options(-Wl,-dead_strip -Wl,-S)
else()
    message(WARNING "Unknown compiler: ${CMAKE_C_COMPILER_ID}")
endif()

include("${CMAKE_CURRENT_LIST_DIR}/vulkan/stub.cmake")
include("${CMAKE_CURRENT_LIST_DIR}/win32/shim.cmake")

if(INSTALLAMA_PROBE)
    add_subdirectory(${INSTALLAMA_PROBE})
    set(INSTALLAMA_TARGET "probe")
else()
    FetchContent_MakeAvailable(llamacpp)
    set(INSTALLAMA_TARGET "llama-server")
endif()

installama_add_win32_shim(${INSTALLAMA_TARGET})

include("${CMAKE_CURRENT_LIST_DIR}/cuda/prune.cmake")
installama_prune_cuda(${INSTALLAMA_TARGET})

set(INSTALLAMA_FILE "${INSTALLAMA_DIR}/${INSTALLAMA_TARGET}.zst")

add_custom_command(
    OUTPUT  ${INSTALLAMA_FILE}.done
    COMMAND ${CMAKE_COMMAND} -E make_directory ${INSTALLAMA_DIR}
    COMMAND ${ZSTD} -f --rm -19 $<TARGET_FILE:${INSTALLAMA_TARGET}> -o ${INSTALLAMA_FILE}
    COMMAND ${CMAKE_COMMAND} -E touch ${INSTALLAMA_FILE}.done
    DEPENDS ${INSTALLAMA_TARGET}
)
add_custom_target(installama DEPENDS ${INSTALLAMA_FILE}.done)
