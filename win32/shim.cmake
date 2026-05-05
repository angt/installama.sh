set(_shim_dir "${CMAKE_CURRENT_LIST_DIR}")

if(INSTALLAMA_OS STREQUAL "windows")
    add_library(win32_shim STATIC "${_shim_dir}/shim.c")

    target_compile_options(win32_shim PRIVATE
        -Wno-unused-function
    )

    function(installama_link_win32_shim target)
        target_link_libraries(${target} PRIVATE
            -Wl,--whole-archive win32_shim -Wl,--no-whole-archive
        )
    endfunction()
else()
    function(installama_link_win32_shim target)
    endfunction()
endif()
