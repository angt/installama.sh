find_package(Vulkan REQUIRED)
add_executable(probe probe.c)
target_link_libraries(probe PRIVATE Vulkan::Vulkan)
set_target_properties(probe PROPERTIES OUTPUT_NAME "probe")
