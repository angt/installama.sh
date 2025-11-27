#include <vulkan/vulkan.h>

int
main(void)
{
    VkInstanceCreateInfo createInfo = {
        .sType = VK_STRUCTURE_TYPE_INSTANCE_CREATE_INFO,
    };

    VkInstance instance;

    if (vkCreateInstance(&createInfo, NULL, &instance) != VK_SUCCESS)
        return 1;

    vkDestroyInstance(instance, NULL);
    return 0;
}
