

class MachineData:
    os = None
    instance = None

    def __init__(self, machine_data):
        self.os = self.OS(machine_data.get('os', {}))
        self.instance = self.Instance(machine_data.get('instance', {}))

    class OS:
        system = None
        name = None
        processor = None
        id = None

        def __init__(self, os_data):
            for k, v in os_data.items():
                exec('self.' + k + '=v')

    class Instance:
        accountId = None
        architecture = None
        availabilityZone = None
        billingProducts = None
        devpayProductCodes = None
        marketplaceProductCodes = None
        imageId = None
        instanceId = None
        instanceType = None
        kernelId = None
        pendingTime = None
        privateIp = None
        ramdiskId = None
        region = None
        version = None

        def __init__(self, instance_data):
            for k, v in instance_data.items():
                exec('self.' + k + '=v')