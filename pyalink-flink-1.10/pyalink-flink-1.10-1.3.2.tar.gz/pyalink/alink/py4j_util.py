import os
import sys
from threading import RLock
from typing import Optional, List

from py4j.java_gateway import GatewayParameters, CallbackServerParameters
from py4j.java_gateway import JavaGateway
from py4j.java_gateway import launch_gateway
from py4j.protocol import Py4JNetworkError

from .common.utils.packages import in_ipython

_gateway: Optional[JavaGateway] = None
_lock = RLock()


def set_java_gateway(gateway: JavaGateway):
    global _gateway
    global _lock
    with _lock:
        _gateway = gateway


def check_java_gateway_alive(gateway: JavaGateway) -> bool:
    if gateway is None:
        return False
    try:
        gateway.jvm.System.getProperty("java.runtime.name")
        return True
    except Exception or Py4JNetworkError:
        return False


def get_java_gateway():
    global _gateway
    global _lock
    with _lock:
        if not check_java_gateway_alive(_gateway):
            LocalJvmBridge.inst().close()
            _gateway = None
        if _gateway is None:
            _gateway = LocalJvmBridge.inst().gateway
    return _gateway


def get_java_class(name: str):
    return get_java_gateway().jvm.__getattr__(name)


def list_all_jars() -> List[str]:
    from .config import g_config
    alink_deps_dir = g_config["alink_deps_dir"]
    flink_home = g_config["flink_home"]

    ret = []
    ret += [os.path.join(alink_deps_dir, x) for x in
            os.listdir(alink_deps_dir) if x.endswith('.jar')]
    ret += [os.path.join(flink_home, 'lib', x) for x in
            os.listdir(os.path.join(flink_home, 'lib'))
            if x.endswith('.jar')]

    ret += [os.path.join(flink_home, 'opt', x)
            for x in os.listdir(os.path.join(flink_home, 'opt'))
            if x.endswith('.jar') and x.startswith("flink-python")]
    return ret


class LocalJvmBridge(object):
    _bridge = None

    def __init__(self):
        self.process = None
        self.gateway = None
        self.app = None
        self.port = 0
        pass

    @classmethod
    def inst(cls):
        if cls._bridge is None:
            cls._bridge = LocalJvmBridge()
            cls._bridge.init()
        return cls._bridge

    def init(self):
        from .config import g_config
        debug_mode = g_config["debug_mode"]

        # always redirect stdout, and only redirect stderr in debug_mode and not in IPython (will fail)
        redirect_stderr = sys.stderr if debug_mode and not in_ipython() else None

        if g_config['gateway_port'] is not None:
            self.port = int(g_config['gateway_port'])
        else:
            self.port = launch_gateway(
                port=0, javaopts=[], die_on_exit=True, daemonize_redirect=True,
                redirect_stdout=sys.stdout, redirect_stderr=redirect_stderr,
                classpath=os.pathsep.join(list_all_jars()))
        print('JVM listening on 127.0.0.1:{}'.format(self.port))
        self.gateway = JavaGateway(
            gateway_parameters=GatewayParameters(port=self.port, auto_field=True),
            callback_server_parameters=CallbackServerParameters(port=0, daemonize=True, daemonize_connections=True),
            start_callback_server=False)

        callback_server_port = self.gateway.get_callback_server().get_listening_port()
        self.gateway.java_gateway_server.resetCallbackClient(
            self.gateway.java_gateway_server.getCallbackClient().getAddress(),
            callback_server_port)

    def close(self):
        self.gateway.close(keep_callback_server=True)
        self._bridge = None
