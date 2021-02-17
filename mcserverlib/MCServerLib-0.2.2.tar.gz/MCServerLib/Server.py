from requests import get


class Properties:

    def __init__(self, default=False):
        self.default = default
        self.properties = {'enable-jmx-monitoring': 'false', 'rcon.port': '25575', 'level-seed': '', 'gamemode': 'survival', 'enable-command-block': 'false', 'enable-query': 'false', 'generator-settings': '', 'level-name': 'world', 'motd': 'A Minecraft Server', 'query.port': '25565', 'pvp': 'true', 'generate-structures': 'true', 'difficulty': 'easy', 'network-compression-threshold': '256', 'max-tick-time': '60000', 'use-native-transport': 'true', 'max-players': '20', 'online-mode': 'true', 'enable-status': 'true', 'allow-flight': 'false', 'broadcast-rcon-to-ops': 'true', 'view-distance': '10', 'max-build-height': '256', 'server-ip': '', 'allow-nether': 'true', 'server-port': '25565',
                           'enable-rcon': 'false', 'sync-chunk-writes': 'true', 'op-permission-level': '4', 'prevent-proxy-connections': 'false', 'resource-pack': '', 'entity-broadcast-range-percentage': '100', 'rcon.password': '', 'player-idle-timeout': '0', 'debug': 'false', 'force-gamemode': 'false', 'rate-limit': '0', 'hardcore': 'false', 'white-list': 'false', 'broadcast-console-to-ops': 'true', 'spawn-npcs': 'true', 'spawn-animals': 'true', 'snooper-enabled': 'true', 'function-permission-level': '2', 'level-type': 'default', 'text-filtering-config': '', 'spawn-monsters': 'true', 'enforce-whitelist': 'false', 'resource-pack-sha1': '', 'spawn-protection': '16', 'max-world-size': '29999984'}


class Setup:

    def __init__(self, version: str, xmx: str, xms: str, properties: Properties):
        self.version = version
        self.dowload_url = f"https://papermc.io/api/v1/paper/{self.version}/latest/download"
        self.xmx = xmx
        self.xms = xms
        self.jarname = f"paper-{self.version}.jar"
        self.properties = properties

    def downloadAll(self):

        self.downloadPaper()
        self.makeBatch()
        self.makeEula()

        if self.properties.default != True:
            with open("server.properties", "w") as f:
                ppt_str = ""
                for ppt in self.properties.properties.keys():
                    ppt_str += f"{ppt}={self.properties.properties[ppt]}\n"
                f.write(ppt_str)

    def downloadPaper(self):
        with open(self.jarname, "wb") as f:
            print("Downloading Paper Bukkit...")
            response = get(self.dowload_url)
            f.write(response.content)
            print("Download Finished")

    def makeBatch(self):
        with open("server.bat", "w") as f:
            print("Writing Batch File")
            f.write(
                f"java -Xmx{self.xmx} -Xms{self.xms} -jar {self.jarname} nogui")
            print("Writing Finished")

    def makeEula(self, boolean=True):
        with open("eula.txt", "w") as f:
            print("Writing Eula File")
            f.write("eula=true" if boolean else "eula=false")
            print("Writing Finished")
