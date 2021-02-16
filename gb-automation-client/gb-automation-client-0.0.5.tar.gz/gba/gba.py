import requests
import os


class Config:
    def __init__(self, config=None):
        self.baseUrl = ""

        if config is not None:
            if "baseUrl" in config:
                self.baseUrl = config["baseUrl"]


class Client:
    def __init__(self, config):
        self.config = config

    def list_device_apps(self, deviceId):
        r = requests.get(
            "{baseUrl}/devices/{deviceId}/apps".format(
                baseUrl=self.config.baseUrl, deviceId=deviceId
            )
        )
        r.raise_for_status()
        apps = r.json()
        return apps

    def get_device(self, deviceId):
        r = requests.get(
            "{baseUrl}/devices/{deviceId}".format(
                baseUrl=self.config.baseUrl, deviceId=deviceId
            )
        )
        r.raise_for_status()
        device = r.json()
        return device

    def list_devices(self):
        r = requests.get("{baseUrl}/devices".format(baseUrl=self.config.baseUrl))
        r.raise_for_status()
        devices = r.json()
        return devices

    def start_session(self, deviceId, appId, autoSync=False, screenshots=False):
        requestBody = {
            "deviceId": deviceId,
            "appId": appId,
            "autoSync": autoSync,
            "screenshots": screenshots,
        }
        r = requests.post(
            "{baseUrl}/sessions".format(baseUrl=self.config.baseUrl), json=requestBody
        )
        r.raise_for_status()
        return r.json()

    def stop_session(self, sessionId, outputJson=False):
        requestBody = {
            "includeSessionJsonInResponse": outputJson,
        }
        r = requests.post(
            "{baseUrl}/sessions/{sessionId}/stop".format(
                baseUrl=self.config.baseUrl, sessionId=sessionId
            ),
            json=requestBody
        )
        r.raise_for_status()
        if not outputJson:
            return

        return r.json()

    def sync(self):
        r = requests.post("{baseUrl}/sessions/sync".format(baseUrl=self.config.baseUrl))
        r.raise_for_status()
        return

    def get_properties(self):
        r = requests.get("{baseUrl}/properties".format(baseUrl=self.config.baseUrl))
        r.raise_for_status()
        return r.json()

    def set_properties(self, properties):
        r = requests.put("{baseUrl}/properties".format(baseUrl=self.config.baseUrl), json=properties)
        r.raise_for_status()
        return

    def generate_session_json(self, session_path, target_path=None):
        requestBody = {
            "sessionPath": session_path,
        }
        if target_path:
            requestBody["targetPath"] = target_path

        r = requests.post(
            "{baseUrl}/generate-json".format(baseUrl=self.config.baseUrl),
            json=requestBody,
        )
        r.raise_for_status()
        return

    def enable_wifi_prof(self, device_id):
        r = requests.post(
            "{baseUrl}/devices/{deviceId}/enable-wifi-prof".format(
                baseUrl=self.config.baseUrl, deviceId=device_id
            )
        )
        r.raise_for_status()
        return

    def disable_wifi_prof(self, device_id):
        r = requests.post(
            "{baseUrl}/devices/{deviceId}/disable-wifi-prof".format(
                baseUrl=self.config.baseUrl, deviceId=device_id
            )
        )
        r.raise_for_status()
        return


class ClientFactory:
    def create(self, config=None):
        if config == None:
            config = Config()

        if os.environ.get("GBA_BASE_URL"):
            config.baseUrl = os.environ.get("GBA_BASE_URL")

        return Client(config)
