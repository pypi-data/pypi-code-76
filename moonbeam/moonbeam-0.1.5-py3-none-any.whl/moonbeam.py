# -*- coding: utf-8 -*-

import os

EXTENSION = ".mb"


class Load:
    def __init__(self, path="main", directory="./", default=None):
        if default is None:
            default = {}

        self.directory = directory
        self.default = default
        self.path = path

        try:
            self.file = open(f"""{self.directory}{self.path}{EXTENSION}""", encoding="utf-8").read()
        except FileNotFoundError:
            open(f"""{self.directory}{self.path}{EXTENSION}""", "w", encoding="utf-8").write(
                f"{self.dumps(self.default)}"
            )
            self.file = open(f"""{self.directory}{self.path}{EXTENSION}""", encoding="utf-8").read()

        self.database = self.loads()

    def get(self, name, key=None):
        if key is None:
            if name not in self.database:
                print("Nothing was found. Returned None")
                return None
            return self.database[name]
        else:
            if name not in self.database:
                print("Nothing was found. Returned None")
                return None
            elif key not in self.database[name]:
                print("Nothing was found. Returned None")
                return None
            return self.database[name][key]

    def set(self, key, value):
        if type(key) == list:
            self.database[key[0]][key[1]] = value
            self.save()
        else:
            self.database[key] = value
            self.save()

    def append(self, key, value):
        if type(key) == list:
            self.database[key[0]][key[1]].append(value)
            self.save()
        else:
            self.database[key].append(value)
            self.save()

    def remove(self, key, value):
        if type(key) == list:
            self.database[key[0]][key[1]].remove(value)
            self.save()
        else:
            self.database[key].remove(value)
            self.save()

    def plus(self, key, value):
        if type(key) == list:
            self.database[key[0]][key[1]] += value
            self.save()
        else:
            self.database[key] += value
            self.save()

    def minus(self, key, value):
        if type(key) == list:
            self.database[key[0]][key[1]] -= value
            self.save()
        else:
            self.database[key] -= value
            self.save()

    def delete(self, key):
        if type(key) == list:
            del self.database[key[0]][key[1]]
            self.save()
        else:
            del self.database[key]
            self.save()

    def save(self):
        open(f"""{self.directory}{self.path}{EXTENSION}""", "w", encoding="utf-8").write(f"{self.dumps()}")

    def loads(self, file=None):
        if file is None:
            file = self.file
        result = {}
        for i in file.splitlines():
            obj = i.split(" | ")
            result[obj[0]] = eval(obj[1])
        return result

    def dumps(self, obj=None):
        if obj is None:
            obj = self.database
        result = ""
        for name in obj:
            quot = "\"" if type(obj[name]) == str else ""
            result += f"""{name} | {quot}{obj[name]}{quot}\n"""
        return result


class LoadAll:
    def __init__(self, directory="./"):
        if directory is None:
            self.directory = "./"
        else:
            self.directory = directory

        self.all = [i.replace(EXTENSION, "") for i in os.listdir(self.directory) if i.find(EXTENSION) > 0]
        self.files = {}

        for name in self.all:
            self.files[name] = Load(path=name, directory=self.directory)

    def append(self, name, file):
        self.files[name] = file

    def get(self, name):
        return self.files[name]
