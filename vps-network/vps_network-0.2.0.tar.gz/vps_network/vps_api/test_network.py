from .dt import ServerListForm
from .network import NetworkApi


def test_telemetry():
    api = NetworkApi()
    resp = api.do_telemetry()
    assert resp.ok


def test_server_list():
    api = NetworkApi()
    server_list = api.server_list(ServerListForm(limit=1))
    assert len(server_list) == 1
