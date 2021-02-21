import platform
from threading import Thread
from typing import Optional, List

from requests import Session, Response

from .dt import ServerListResp, ServerItem, ServerListForm
from ..vps_ping import PingResult
from ..vps_speed import SpeedResult

__all__ = ["NetworkApi"]


class NetworkApi(object):
    """
    VPS Network API
    """

    def __init__(
        self,
        app_key: Optional[str] = None,
        url: str = "https://vps.qiyutech.tech/api/network/v1",
    ):
        """
        :param app_key: 访问的APPKey
        :param url: 服务器URL
        """
        self._app_key: Optional[str] = app_key
        self._url: str = url
        self._http: Session = Session()

    def ping_report(self, job_id: Optional[str], results: List[PingResult]):
        pass

    def speed_report(self, job_id: Optional[str], results: List[SpeedResult]):
        pass

    def trace_report(self, job_id: Optional[str], results: List[PingResult]):
        pass

    def server_list(self, form: ServerListForm) -> List[ServerItem]:
        """
        获取服务器列表
        """
        url = f"{self._url}/server_list"
        resp = self._http.post(url, json=form.dict())
        if resp.ok:
            ret = ServerListResp(**resp.json())
            return ret.servers
        return []

    def telemetry(self) -> Thread:
        """
        上报遥测数据
        """
        th = Thread(target=self.do_telemetry, name="telemetry")
        th.start()
        return th

    def do_telemetry(self) -> Response:
        """
        执行上报遥测数据
        """
        url = f"{self._url}/telemetry"
        json = {
            "info": {
                "os": platform.system(),
                "host": platform.node(),
                "os-ver": platform.release(),
                "processor": platform.processor(),
                "python": platform.python_version(),
            }
        }
        return self._http.post(url, json=json)
