from requests import get
import MCServerLib.Prop


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
