from l0n0lnet import se, add_quit_func
from ctypes import *
import logging

_tcps = {}
_name_tcp = {}


def _get_callback(server_id, cb_name):
    name = _tcps.get(server_id)
    if name is None:
        return
    name_data = _name_tcp.get(name)
    if name_data is None:
        return
    return name_data.get(cb_name)


@CFUNCTYPE(None, c_uint32, c_uint32, c_char_p, c_size_t)
def _on_session_read(session_id, server_id, data, size):
    func = _get_callback(server_id, "on_session_read")
    if func is None:
        return
    data = data[:size]
    func(session_id, data, size)


@CFUNCTYPE(None, c_uint32, c_uint32)
def _on_session_connected(session_id, server_id):
    se.regist_on_read_size(session_id, 0, _on_session_read)
    func = _get_callback(server_id, "on_session_connected")
    if func is None:
        return
    func(session_id)


@CFUNCTYPE(None, c_uint32, c_uint32)
def _on_session_disconnected(session_id, server_id):
    func = _get_callback(server_id, "on_session_disconnected")
    if func is None:
        return
    func(session_id)


@CFUNCTYPE(None, c_uint32, c_uint32)
def _on_client_connected(session_id, server_id):
    func = _get_callback(session_id, "on_connected")
    if func is None:
        return
    func()


@CFUNCTYPE(None, c_uint32, c_uint32)
def _on_client_disconnected(session_id, server_id):
    func = _get_callback(session_id, "on_disconnected")
    if func is None:
        return
    func()


@CFUNCTYPE(None, c_uint32, c_uint32)
def _on_client_connect_failed(session_id, server_id):
    func = _get_callback(session_id, "on_connect_failed")
    if func is None:
        return
    func()


@CFUNCTYPE(None, c_uint32, c_uint32, c_char_p, c_size_t)
def _on_client_read(session_id, server_id, data, size):
    func = _get_callback(session_id, "on_read")
    if func is None:
        return
    data = data[:size]
    func(data, size)


def send_message(id: int, data: bytes) -> bool:
    """
    向目标ID发送数据

    @id:int:目标ID
    @data:bytes:数据
    """
    return se.send_message(id, data, len(data))


def close_tcp(id: int):
    """
    用来关闭tcp。如服务器，客户端，session。
    """
    # 关闭tcp
    se.close_tcp(id)

    # 获取名称
    name = _tcps.get(id)
    if not name:
        return

    # 删除名称缓存
    if _name_tcp.get(name):
        del _name_tcp[name]

    # 删除数据
    del _tcps[id]


def create_tcp_server_v4(server_name: str, ip: str, port: int, backlog: int = 1024):
    """
    创建tcp服务器

    @server_name:str:服务器名称
    @ip:str:服务器IP地址
    @port:int:服务器端口号
    @backlog:int:backlog
    @return:int:服务器ID号。0 表示创建失败

    """
    # 创建服务器
    id = se.create_server_v4(ip.encode(), port, backlog)

    # 验证创建结果
    if id == 0:
        return id

    # 注册基本回调
    se.regist_on_session_connected(id, _on_session_connected)
    se.regist_on_session_disconnected(id, _on_session_disconnected)

    # 缓存数据
    if not _name_tcp.get(server_name):
        _name_tcp[server_name] = {"id": id}
    else:
        _name_tcp[server_name]['id'] = id

    _tcps[id] = server_name

    # 返回ID
    return id


def connect_to_v4(client_name: str, ip: str, port: int):
    # 连接目标
    id = se.connect_to_v4(ip.encode(), port)

    # 验证创建结果
    if id == 0:
        return id

    # 注册基本回调
    se.regist_on_connected(id, _on_client_connected)
    se.regist_on_disconnected(id, _on_client_disconnected)
    se.regist_on_connect_failed(id, _on_client_connect_failed)
    se.regist_on_read_size(id, 0, _on_client_read)

    # 缓存数据
    if not _name_tcp.get(client_name):
        _name_tcp[client_name] = {"id": id}
    else:
        _name_tcp[client_name]['id'] = id

    _tcps[id] = client_name

    # 返回ID
    return id


def close_tcp_by_name(name):
    """
    通过名称关闭tcp对象
    """
    namedata = _name_tcp.get(name)
    if not namedata:
        return
    id = namedata.get("id")
    if not id:
        return
    close_tcp(id)


def set_cb(tcp_name, cb_name, cb_fn):
    """
    设置回调
    """
    if not _name_tcp.get(tcp_name):
        _name_tcp[tcp_name] = {cb_name: cb_fn}
    else:
        _name_tcp[tcp_name][cb_name] = cb_fn


def handler_session_connected(server_name: str):
    def wraper(func):
        set_cb(server_name, "on_session_connected", func)
        return func
    return wraper


def handler_session_disconnected(server_name: str):
    def wraper(func):
        set_cb(server_name, "on_session_disconnected", func)
        return func
    return wraper


def handler_session_read(server_name: str):
    def wraper(func):
        set_cb(server_name, "on_session_read", func)
        return func
    return wraper


def _on_quit():
    tcpids = []
    for tcp_data in _name_tcp.values():
        id = tcp_data.get("id")
        if id:
            tcpids.append(id)

    for id in tcpids:
        close_tcp(id)


add_quit_func(_on_quit)


class base_server:
    def __init__(self, ip, port):
        name = self.__class__.__name__
        create_tcp_server_v4(name, ip, port)
        set_cb(name, "on_session_connected", self.on_session_connected)
        set_cb(name, "on_session_disconnected", self.on_session_disconnected)
        set_cb(name, "on_session_read", self.on_session_read)

    def __del__(self):
        self.close()

    def close(self):
        close_tcp_by_name(self.__class__.__name__)

    def send_msg(self, id, data):
        send_message(id, data)

    def on_session_connected(self, session_id):
        pass

    def on_session_disconnected(self, session_id):
        pass

    def on_session_read(self, session_id, data, size):
        pass


class base_client:
    def __init__(self, ip, port):
        name = self.__class__.__name__
        self.id = connect_to_v4(name, ip, port)
        set_cb(name, "on_connected", self.on_connected)
        set_cb(name, "on_connect_failed", self.on_connect_failed)
        set_cb(name, "on_disconnected", self.on_disconnected)
        set_cb(name, "on_read", self.on_read)

    def __del__(self):
        self.close()

    def close(self):
        close_tcp_by_name(self.__class__.__name__)

    def send_msg(self, data):
        send_message(self.id, data)

    def on_connected(self):
        pass

    def on_connect_failed(self):
        pass

    def on_disconnected(self):
        pass

    def on_read(self, data, size):
        pass
