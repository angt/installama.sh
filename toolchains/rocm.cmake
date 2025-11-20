set(CMAKE_SYSTEM_NAME      $ENV{CMAKE_SYSTEM_NAME})
set(CMAKE_SYSTEM_PROCESSOR $ENV{CMAKE_SYSTEM_PROCESSOR})

set(CMAKE_C_COMPILER   "/opt/rocm/lib/llvm/bin/clang")
set(CMAKE_CXX_COMPILER "/opt/rocm/lib/llvm/bin/clang++")
set(CMAKE_HIP_COMPILER "${CMAKE_CXX_COMPILER}")

include("${CMAKE_CURRENT_LIST_DIR}/base.cmake")
