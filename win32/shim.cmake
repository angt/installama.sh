set(_shim_dir "${CMAKE_CURRENT_LIST_DIR}")

function(installama_add_win32_shim target)
    if(NOT INSTALLAMA_OS STREQUAL "windows")
        return()
    endif()

    add_library(win32_shim STATIC "${_shim_dir}/shim.c")

    target_compile_options(win32_shim PRIVATE
        -Wno-unused-function
    )
    target_link_libraries(${target} PRIVATE
        -Wl,--whole-archive win32_shim -Wl,--no-whole-archive
    )
endfunction()
