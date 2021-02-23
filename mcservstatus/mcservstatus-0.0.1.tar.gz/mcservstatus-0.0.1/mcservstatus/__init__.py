import requests
import json

edebug = False

def log(output: str):
    if edebug:
        print(output)

class MCServStatsClient:

    def __init__(self):
        pass

    def check_server(self, address: str):
        _request = requests.get(url=f"https://api.mcsrvstat.us/2/{address}")
        if not _request.status_code == 200:
            return None
        else:
            _parsed_json = json.loads(_request.text)
            if _parsed_json["online"]:
                _parsed_json["motd"]["clean"].append(_parsed_json["motd"]["clean"][0] + "\n" + _parsed_json["motd"]["clean"][1])
                _parsed_json["motd"]["raw"].append(_parsed_json["motd"]["raw"][0] + "\n" + _parsed_json["motd"]["raw"][1])
                return _parsed_json
            else:
                return _parsed_json

    def uncenter_motd(self, motd: list):
        for letter in motd[0]:
            if letter == " ":
                motd[0] = motd[0][:0] + motd[0][1:]
            else:
                break
        for letter in motd[1]:
            if letter == " ":
                motd[1] = motd[1][:0] + motd[1][1:]
            else:
                break
        motd[2] = motd[0] + "\n" + motd[1]
        return motd