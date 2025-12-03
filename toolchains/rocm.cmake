include("${CMAKE_CURRENT_LIST_DIR}/init.cmake")

set(CMAKE_C_COMPILER   "/opt/rocm/lib/llvm/bin/clang")
set(CMAKE_CXX_COMPILER "/opt/rocm/lib/llvm/bin/clang++")
set(CMAKE_HIP_COMPILER "${CMAKE_CXX_COMPILER}")

include("${CMAKE_CURRENT_LIST_DIR}/exit.cmake")
