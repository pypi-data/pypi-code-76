import os, sys


class dat:
    def __init__(self, p):
        self.dbpath = p
        if not os.path.exists(self.dbpath):
            os.makedirs(self.dbpath)

    def listermreminders(self):
        return os.listdir(self.dbpath)

    def getermreminder(self, name):
        rpath = self.dbpath + name
        if os.path.exists(rpath):
            with open(rpath) as f:
                return f.read()
        else:
            return "No such reminder"

    def setermreminder(self, name, content):
        rpath = self.dbpath + name
        with open(rpath, "w") as f:
            f.write(content)

    def delreminder(self, name):
        rpath = self.dbpath + name
        if os.path.exists(rpath):
            os.remove(rpath)
