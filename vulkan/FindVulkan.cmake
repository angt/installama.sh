if(VULKAN_HEADERS)
    set(Vulkan_FOUND TRUE)
    set(Vulkan_VERSION "1.2.0")

    if(NOT Vulkan_GLSLC_EXECUTABLE)
        find_program(GLSLC
            NAMES glslc
            HINTS "$ENV{VULKAN_SDK}/bin" "/opt/vulkan-sdk/bin"
            REQUIRED
        )
        set(Vulkan_GLSLC_EXECUTABLE "${GLSLC}")
    endif()

    if(NOT TARGET Vulkan::Vulkan)
        add_library(Vulkan::Vulkan ALIAS vulkan_stub)
    endif()
else()
    set(Vulkan_FOUND FALSE)
endif()
