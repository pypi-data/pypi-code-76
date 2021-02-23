import collections
import os
from typing import Union

from py4j.java_gateway import JavaGateway

from .common.types.conversion.type_converters import py_list_to_j_array
from .common.utils.packages import is_flink_1_9
from .config import g_config
from .py4j_util import get_java_gateway, get_java_class, set_java_gateway, LocalJvmBridge

__all__ = ["useLocalEnv", "useRemoteEnv", "useCustomEnv", "getMLEnv", "resetEnv"]

MLEnv = collections.namedtuple('MLEnv', 'benv btenv senv stenv')
_mlenv: MLEnv = None
_in_custom_env: bool = False


def add_default_configurations(configuration, parallelism: int):
    if not is_flink_1_9():
        configuration.setString("taskmanager.memory.managed.size", str(64 * parallelism) + "m")
        configuration.setString("taskmanager.memory.network.min", str(64 * parallelism) + "m")
    else:
        configuration.setBoolean("taskmanager.memory.preallocate", True)
        configuration.setBoolean("taskmanager.memory.off-heap", True)
        configuration.setDouble("taskmanager.memory.fraction", 0.3)


def make_j_configuration(config, parallelism: int):
    configuration = get_java_gateway().jvm.org.apache.flink.configuration.Configuration()
    add_default_configurations(configuration, parallelism)

    if config is None:
        return configuration
    if not isinstance(config, (dict,)):
        raise Exception("Flink configuration should be dict")

    for (key, value) in config.items():
        if isinstance(value, (bool,)):
            configuration.setBoolean(key, value)
        elif isinstance(value, (float,)):
            configuration.setDouble(key, value)
        elif isinstance(value, (int,)):
            configuration.setLong(key, value)
        elif isinstance(value, (str,)):
            configuration.setString(key, value)
        else:
            raise Exception("Unsupported type for key " + key)
    return configuration


def setup_alink_plugins_path():
    alink_plugins_path = g_config['alink_plugins_dir']
    os.makedirs(alink_plugins_path, exist_ok=True)
    from .config import AlinkGlobalConfiguration
    prev_plugin_dir = AlinkGlobalConfiguration.getPluginDir()
    if prev_plugin_dir == 'plugins':    # not set before
        AlinkGlobalConfiguration.setPluginDir(alink_plugins_path)


def setup_py_flink_env(gateway: JavaGateway, j_benv: object, j_senv: object) -> MLEnv:
    from pyflink.dataset import ExecutionEnvironment
    from pyflink.datastream import StreamExecutionEnvironment
    from pyflink.table import BatchTableEnvironment, StreamTableEnvironment
    import pyflink

    pyflink.java_gateway._gateway = gateway
    pyflink.java_gateway.import_flink_view(gateway)

    benv = ExecutionEnvironment(j_benv)
    senv = StreamExecutionEnvironment(j_senv)
    btenv = BatchTableEnvironment.create(benv)
    stenv = StreamTableEnvironment.create(senv)
    return benv, btenv, senv, stenv


def setup_java_ml_env(gateway, benv, btenv, senv, stenv):
    """
    Setup Java MLEnv from PyFlink environments.
    :param gateway:
    :type gateway: JavaGateway
    :param benv:
    :type benv: ExecutionEnvironment
    :param btenv:
    :type btenv: BatchTableEnvironment
    :param senv:
    :type senv: StreamExecutionEnvironment
    :param stenv:
    :type stenv: StreamTableEnvironment
    :return:
    """
    j_mlenv = gateway.jvm.com.alibaba.alink.common.MLEnvironment(
        benv._j_execution_environment,
        btenv._j_tenv,
        senv._j_stream_execution_environment,
        stenv._j_tenv
    )
    gateway.jvm.com.alibaba.alink.common.MLEnvironmentFactory.remove(0)
    gateway.jvm.com.alibaba.alink.common.MLEnvironmentFactory.setDefault(j_mlenv)
    return j_mlenv


def setup_py_ml_env(gateway: JavaGateway, j_benv: object, j_senv: object):
    benv, btenv, senv, stenv = setup_py_flink_env(gateway, j_benv, j_senv)
    setup_java_ml_env(gateway, benv, btenv, senv, stenv)
    mlenv = MLEnv(benv, btenv, senv, stenv)
    return mlenv


def useLocalEnv(parallelism: int, flinkHome: str = None, config: object = None) -> MLEnv:
    """
    Start a local Flink mini-cluster as the execution environment
    :rtype: object
    :param parallelism: parallelism to run tasks
    :param flinkHome: Flink home directory
    :param config: additional config for Flink local cluster
    :return: a Java MLEnvironment object
    """
    if in_custom_env():
        print("Warning: useLocalEnv will do nothing, since useCustomEnv is used to initialize MLEnv.")
        return
    resetEnv()
    if flinkHome is not None:
        g_config["flink_home"] = flinkHome
    if config is not None and "debug_mode" in config:
        g_config["debug_mode"] = config["debug_mode"]
    j_configuration = make_j_configuration(config, parallelism)
    gateway = get_java_gateway()

    setup_alink_plugins_path()

    j_benv = gateway.jvm.org.apache.flink.api.java.ExecutionEnvironment.createLocalEnvironment(j_configuration)
    j_configuration.setString("classloader.parent-first-patterns.additional", "org.apache.flink.statefun;org.apache.kafka;com.google.protobuf")
    j_senv = gateway.jvm.org.apache.flink.streaming.api.environment.StreamExecutionEnvironment.createLocalEnvironment(
        parallelism, j_configuration)
    j_benv.setParallelism(parallelism)
    j_senv.setParallelism(parallelism)

    global _mlenv
    _mlenv = setup_py_ml_env(gateway, j_benv, j_senv)
    return _mlenv


def useRemoteEnv(host: str, port: Union[int, str], parallelism: int, flinkHome: str = None,
                 localIp: str = None, shipAlinkAlgoJar: bool = True, config: object = None) -> MLEnv:
    """
    Connect an already started Flink cluster as the execution environment
    :param host: hostname
    :param port: rest port
    :param parallelism: parallelism to run tasks
    :param flinkHome: Flink home directory in the local machine
    :param localIp: external ip address, which is used for DataStream display
    :param shipAlinkAlgoJar: whether to ship Alink algorithm jar to the cluster
    :param config: additional config for running tasks
    :return: a Java MLEnvironment object
    """
    if in_custom_env():
        print("Warning: useRemoteEnv will do nothing, since useCustomEnv is used to initialize MLEnv.")
        return

    if localIp is None:
        localIp = g_config["local_ip"]
        print("Warning: localIp is not provided, default value %s is used. "
              "DataStream data display could fail, if the localIp is not reachable from the Flink Cluster."
              % localIp)
    if isinstance(port, str):
        port = int(port)

    resetEnv()
    g_config["collect_storage_type"] = "memory"
    g_config["local_ip"] = localIp
    if flinkHome is not None:
        g_config["flink_home"] = flinkHome
    j_configuration = make_j_configuration(config, parallelism)
    gateway = get_java_gateway()

    setup_alink_plugins_path()

    alink_lib_path = g_config['alink_deps_dir']
    if shipAlinkAlgoJar:
        jar_files = [os.path.join(alink_lib_path, f) for f in os.listdir(alink_lib_path) if f.endswith(".jar")]
    else:
        jar_files = [os.path.join(alink_lib_path, f)
                     for f in os.listdir(alink_lib_path)
                     if f.endswith(".jar") and not f.startswith("alink_core") and not f.startswith("alink_open")
                     ]
    j_jar_files = py_list_to_j_array(gateway.jvm.String, len(jar_files), jar_files)

    j_benv = gateway.jvm.org.apache.flink.api.java.ExecutionEnvironment.createRemoteEnvironment(host, port,
                                                                                                j_configuration,
                                                                                                j_jar_files)
    j_senv = gateway.jvm.org.apache.flink.streaming.api.environment.StreamExecutionEnvironment.createRemoteEnvironment(
        host, port, j_configuration, j_jar_files)
    j_benv.setParallelism(parallelism)
    j_senv.setParallelism(parallelism)

    global _mlenv
    _mlenv = setup_py_ml_env(gateway, j_benv, j_senv)
    return _mlenv


def usePyFlinkEnv(parallelism: int = None, flinkHome: str = None) -> MLEnv:
    if in_custom_env():
        print("Warning: usePyFlinkEnv will do nothing, since useCustomEnv is used to initialize MLEnv.")
        return

    resetEnv()
    if flinkHome is not None:
        g_config["flink_home"] = flinkHome

    if g_config["flink_home"] is None:
        # Running using flink run ***.py
        # Let PyFlink to launch gateway, and warn users to add jars to pyflink lib path
        print("Warning: it seems you're running the script using 'flink run'. "
              "In this case, you have to manually add alink jars to pyflink lib path.")
        import pyflink
        gateway = pyflink.java_gateway.get_gateway()
        pyflink.java_gateway.import_flink_view(gateway)
        set_java_gateway(gateway)
    else:
        # running using python ***.py
        # PyAlink will launch gateway
        import pyflink
        gateway = get_java_gateway()
        pyflink.java_gateway._gateway = gateway
        pyflink.java_gateway.import_flink_view(gateway)

    from pyflink.dataset import ExecutionEnvironment
    from pyflink.datastream import StreamExecutionEnvironment

    benv = ExecutionEnvironment.get_execution_environment()
    senv = StreamExecutionEnvironment.get_execution_environment()
    if parallelism is not None:
        benv.set_parallelism(parallelism)
        senv.set_parallelism(parallelism)

    global _mlenv
    _mlenv = setup_py_ml_env(gateway, benv._j_execution_environment, senv._j_stream_execution_environment)
    return _mlenv


def useCustomEnv(gateway, benv, btenv, senv, stenv):
    """
    Use custom env to initialize PyAlink env
    :param gateway:
    :type gateway: JavaGateway
    :param benv:
    :type benv: ExecutionEnvironment
    :param btenv:
    :type btenv: BatchTableEnvironment
    :param senv:
    :type senv: StreamExecutionEnvironment
    :param stenv:
    :type stenv: StreamTableEnvironment
    :rtype: MLEnv
    """
    if in_custom_env():
        print("Warning: useCustomEnv will do nothing, since useCustomEnv is used to initialize MLEnv.")
        return

    resetEnv()
    set_java_gateway(gateway)
    global _mlenv, _in_custom_env
    _mlenv = MLEnv(benv, btenv, senv, stenv)
    setup_java_ml_env(gateway, *_mlenv)
    _in_custom_env = True
    return _mlenv


def getMLEnv() -> MLEnv:
    global _mlenv
    if _mlenv is None:
        _mlenv = usePyFlinkEnv()
    return _mlenv


def remove_zeppelin_path():
    import sys
    sys.path = list(filter(lambda d: "zeppelin" not in d, sys.path))


def in_custom_env():
    global _in_custom_env
    return _in_custom_env


def resetEnv():
    """
    Reset the execution environment, clear background services.
    :return:
    """
    if in_custom_env():
        print("Warning: resetEnv will do nothing, since useCustomEnv is used to initialize MLEnv.")
        return

    from .py4j_util import _gateway
    if _gateway is not None:
        j_ml_environment_factory_cls = get_java_class("com.alibaba.alink.common.MLEnvironmentFactory")
        if j_ml_environment_factory_cls is not None:
            j_ml_environment_factory_cls.remove(0)
        LocalJvmBridge.inst().close()


remove_zeppelin_path()
