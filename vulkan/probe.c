#include <stdlib.h>
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

    uint32_t count = 0;

    if (vkEnumeratePhysicalDevices(instance, &count, NULL) != VK_SUCCESS || !count)
        return 2;

    VkPhysicalDevice *devices = calloc(count, sizeof(VkPhysicalDevice));

    if (!devices)
        return 3;

    if (vkEnumeratePhysicalDevices(instance, &count, devices) != VK_SUCCESS)
        return 4;

    int capable = 0;

    for (uint32_t i = 0; i < count; i++) {
        VkPhysicalDeviceProperties props;
        vkGetPhysicalDeviceProperties(devices[i], &props);

        if (props.deviceType == VK_PHYSICAL_DEVICE_TYPE_CPU)
            continue;

        if (props.apiVersion < VK_MAKE_API_VERSION(0, 1, 2, 0))
            continue;

        uint32_t queue_count = 0;
        vkGetPhysicalDeviceQueueFamilyProperties(devices[i], &queue_count, NULL);

        if (!queue_count)
            continue;

        VkQueueFamilyProperties *queues = calloc(queue_count, sizeof(VkQueueFamilyProperties));

        if (!queues)
            continue;

        vkGetPhysicalDeviceQueueFamilyProperties(devices[i], &queue_count, queues);

        int has_compute = 0;

        for (uint32_t j = 0; j < queue_count; j++) {
            if ((queues[j].queueFlags & VK_QUEUE_COMPUTE_BIT) &&
                (queues[j].queueFlags & VK_QUEUE_TRANSFER_BIT)) {
                has_compute = 1;
                break;
            }
        }
        free(queues);

        if (has_compute)
            capable++;
    }
    return capable ? 0 : 5;
}
