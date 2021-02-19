from zesty.models.hf_interface import IDeviceHF

GB_IN_BYTES = 1024**3

class DiskMonitor:
    def __init__(self, disk_mon_data):
        self.filesystems = {}
        self.unused_devices = {}

        for fs in disk_mon_data.get('filesystems', {}):
            self.filesystems[fs] = FileSystem(disk_mon_data.get('filesystems', {}).get(fs, {}))

        for unused_dev in disk_mon_data.get('unused_devices', {}):
            self.unused_devices[unused_dev] = self.UnusedDevice(disk_mon_data.get('unused_devices', {}).get(unused_dev, {}))

    class UnusedDevice:
        size = None
        map = None

        def __init__(self, block_device_data):
            for k, v in block_device_data.items():
                exec('self.' + k + '=v')


class FileSystem:
    def __init__(self, fs_data):
        self.mount_path = fs_data.get('mount_path')
        self.fs_type = fs_data.get('fs_type')
        self.mount_path = fs_data.get('mount_path')
        self.space = self.Usage(fs_data.get('space'))
        self.inodes = self.Usage(fs_data.get('inodes'))
        self.partition_number = fs_data.get('partition_number')
        self.is_partition = fs_data.get('is_partition')
        self.label = fs_data.get('label')
        self.LV = fs_data.get('LV')
        self.VG = fs_data.get('VG')
        self.lvm_path = fs_data.get('lvm_path')
        self.devices = {}

        for dev in fs_data.get('devices'):
            self.devices[dev] = self.BlockDevice(fs_data.get('devices', {}).get(dev, {}))

    class BlockDevice(IDeviceHF):
        def __init__(self, block_device_data):
            # for k, v in block_device_data.items():
            #     exec('self.' + k + '=v')
            self.size = block_device_data.get('size')
            self.btrfs_dev_id = block_device_data.get('btrfs_dev_id')
            self.volume_id = block_device_data.get('volume_id')
            self.dev_usage = block_device_data.get('dev_usage')
            self.iops_stats = block_device_data.get('iops_stats', {})
            self.map = block_device_data.get('map')
            self.unlock_ts = block_device_data.get('unlock_ts', 0)
            self.volume_type = block_device_data.get('volume_type')
            self.iops = block_device_data.get('iops')
            self.created = block_device_data.get('created')

            if 'parent' in block_device_data.keys():
                self.parent = block_device_data.get('parent')

            if self.volume_id is None:
                print("ERROR : Volume ID is None!")

        def __repr__(self):
            return "<VolumeID: {} | Size: {:.1f} GB | Usage: {:.1f} GB>".format(self.volume_id, self.size/GB_IN_BYTES, self.dev_usage/GB_IN_BYTES)

        def get_dev_id(self) -> str:
            return self.volume_id

        def get_size(self) -> int:
            return self.size

        def get_usage(self) -> int:
            return self.dev_usage

        def get_unlock_ts(self) -> int:
            return self.unlock_ts

        def set_unlock_ts(self, ts):
            self.unlock_ts = ts

        def get_iops_stats(self):
            return self.iops_stats

        def get_volume_id(self):
            return self.volume_id

    class Usage:
        def __init__(self, usage_data):
            self.total = None
            self.used = None
            self.free = None
            self.percent = None

            for k, v in usage_data.items():
                exec('self.' + k + '=v')
