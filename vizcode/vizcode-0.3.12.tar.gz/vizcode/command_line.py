import argparse

class Command_Line:
    def __init__(self):
        parser = argparse.ArgumentParser(description = "VizCode: visualize your codebase")
        parser.add_argument("-H", "--Help", help = "Example: Help argument", required = False, default = "")
        parser.add_argument("-p", "--path", help = "Path to your python directory", required = True, default = "")
        parser.add_argument("-e", "--env", help = "Path to python environment", required = False, default = None)
        parser.add_argument("-d", "--deselect", help = "List of paths or files to not be included in visualization", nargs="+", required = False, default = [])
        
        argument = parser.parse_args()
        self.path = None
        self.env = None
        self.deselect = []
        status = False

        if argument.Help:
            print("You have used '-H' or '--Help' with argument: {0}".format(argument.Help))
            status = True
        if argument.path:
            print("You have used '-p or '--path' with argument: {0}".format(argument.path))
            self.path = argument.path
            status = True
        if argument.env:
            print("You have used '-e' or '--env' with argument: {0}".format(argument.env))
            self.env = argument.env
            status = True
        if argument.deselect:
            print("You have used '-d' or '--deselect' with argument: {0}".format(argument.deselect))
            self.deselect = argument.deselect
            status = True
        if not status:
            print("Maybe you want to use -H or -p or -e or -d as arguments ?")

    def get_path(self):
        return self.path

    def get_env(self):
        return self.env
    
    def get_deselect(self):
        return self.deselect
