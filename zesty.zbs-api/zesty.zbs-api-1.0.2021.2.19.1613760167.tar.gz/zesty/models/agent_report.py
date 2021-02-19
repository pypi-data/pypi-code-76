from zesty.models.cpu_mon import CpuMonitor
from zesty.models.disk_mon import DiskMonitor
from zesty.models.mem_mon import MemoryMonitor
from zesty.models.network_mon import NetworkMonitor
from zesty.models.overview import MachineData


class AgentReport:
    agent_version = None
    MachineData = None
    Storage = None
    Network = None
    Memory = None
    Cpu = None

    def __init__(self, agent_report):
        self.agent_version = agent_report.get('agent', {}).get('version')
        self.overview = MachineData(agent_report.get('overview', {}))
        self.Storage = DiskMonitor(agent_report.get('plugins', {}).get('disk_mon', {}))
        self.Memory = MemoryMonitor(agent_report.get('plugins', {}).get('mem_mon', {}))
        self.Cpu = CpuMonitor(agent_report.get('plugins', {}).get('cpu_mon', {}))
        self.Network = NetworkMonitor(agent_report.get('plugins', {}).get('network_mon', {}))