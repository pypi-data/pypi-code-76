import os


class config:
    def __init__(self, p):

        self.CODES = {
            "yellow": "\x1b[33m",
            "red": "\x1b[31m",
            "green": "\x1b[32m",
            "cyan": "\x1b[36m",
        }

        self.configpath = p
        if not os.path.exists(self.configpath):

            default = """# Use this color code as the accent color
# Opts: yellow, red, green, cyan
color: yellow
# Whether or not to use random colors for reminders
random: 1
            """
            with open(self.configpath, "w") as f:
                f.write(default)
            print(
                "This seems to be your first time using remind. \nYou might want to have a look at "
                + self.configpath
            )
            self.colorcode = "\x1b[33m"
            self.randomc = "1"
        else:
            with open(self.configpath) as f:
                raw = f.read()
            lines = raw.split("\n")
            self.colorcode = self.CODES[lines[2].split(": ")[1]]
            self.randomc = lines[4].split(": ")[1]

    def colorc(self):
        return self.colorcode

    def dornd(self):
        if self.randomc == "1":
            return True
        else:
            return False
