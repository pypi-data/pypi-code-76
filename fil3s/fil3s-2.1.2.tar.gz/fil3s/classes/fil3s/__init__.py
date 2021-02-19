#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# imports.
from fil3s.classes.config import *
from fil3s.classes import utils
import time

# the files class.
class Files():
    #
    # functions.
    def load(path, data="not to be used", format="str"): # keep data as second param to prevent save load errors.
        # correct format.
        if format in ["string", "file"]: format = "str"
        if format in ["dict", "array"]: format = "json"
        # match format.
        if format == "str":
            file = open(path,mode='rb')
            data = file.read().decode()
            file.close()
            return data
        elif format == "json":
            data = None
            with open(path, "r") as json_file:
                data = json.load(json_file)
            return data
        elif format == "bytes":
            data = None
            with open(path, "rb") as file:
                data = file.read()
            return data
        else: raise ValueError(f"Unknown format {format}.")
    def save(path, data, format="str"):
        # correct format.
        if format in ["string", "file"]: format = "str"
        if format in ["dict", "array"]: format = "json"
        # match format.
        if format == "str":
            file = open(path, "w+") 
            file.write(data)
            file.close()
        elif format == "json":
            with open(path, "w") as json_file:
                json.dump(data, json_file, indent=4, ensure_ascii=False)
        elif format == "bytes":
            with open(path, "wb") as file:
                file.write(data)
        else: raise ValueError(f"Unknown format {format}.")
        #
    def delete(path, sudo=False):
        if sudo:
            os.system(f"sudo rm -fr {path}")
        else:
            os.system(f"rm -fr {path}")
    # the file object class.
    class File(object):
        def __init__(self, path=None, data=None, load=False, default=None, check_existance=False):
        	# init.
            if path == False: self.file_path = self.fp = False # used in local memory (not fysical)
            else: self.file_path = self.fp = Formats.FilePath(path, check_existance=check_existance)
            self.data = data
            if default != None and not os.path.exists(self.file_path.path):
                self.save(data=default)
            if load: self.load()
            # can be filled with executing [self.x = x()]:
        def load(self, default=None):
            utils.__check_memory_only__(self.file_path.path)
            if not os.path.exists(self.file_path.path) and default != None: 
                self.save(str(default), self.file_path.path)
            file = open(self.file_path.path,mode='rb')
            data = file.read().decode()
            file.close()
            self.data = data
            return data
        def load_line(self, line_number, default=None):
            utils.__check_memory_only__(self.file_path.path)
            if not os.path.exists(self.file_path.path) and default != None: 
                self.save(str(default), self.file_path.path)
            file = open(self.file_path.path,mode='rb')
            data = file.read()
            file.close()
            return data.decode().split('\n')[line_number]
        def save(self, data=None, path=None, overwrite_duplicates=True):
            if path == None: path = self.file_path.path
            utils.__check_memory_only__(path)
            if data != None: a=1 
            else: data = self.data
            file_name, original_path = Formats.FilePath(path).name(), path
            if overwrite_duplicates:
                file = open(path, "w+") 
                file.write(data)
                file.close()
            else:
                extension = file_name.split('.')[file_name.count('.')]
                file_name_without_extension = file_name.replace(extension, '')
                while True:
                    if not os.path.exists(path): break
                    else: path = original_path.replace(file_name, file_name_without_extension+'-'+str(index)+extension)
                file = open(path, "w+") 
                file.write(data)
                file.close()
            self.data = data
    #
    # the shell script object class.
    class ShellScript(object):
        def __init__(self, path=None, data=None, load=False, default=None):
            # init.
            if path == False: self.file_path = self.fp = False # used in local memory (not fysical)
            else: self.file_path = self.fp = Formats.FilePath(path)
            self.data = data
            if default != None and Formats.check(strings={"default":default}) and not os.path.exists(self.file_path.path): self.save(data=default)
            if load: self.load()
            # can be filled with executing [self.x = x()]:
        def load(self, default=None):
            utils.__check_memory_only__(self.file_path.path)
            if not os.path.exists(self.file_path.path) and default != None: 
                self.save(str(default), self.file_path.path)
            file = open(self.file_path.path,mode='rb')
            data = file.read().decode()
            file.close()
            self.data = data
            return data
        def loadLine(self, line_number, default=None):
            utils.__check_memory_only__(self.file_path.path)
            if not os.path.exists(self.file_path.path) and default != None: 
                self.save(str(default), self.file_path.path)
            file = open(self.file_path.path,mode='rb')
            data = file.read()
            file.close()
            return data.decode().split('\n')[line_number]
        def save(self, data=None, overwrite_duplicates=True):
            utils.__check_memory_only__(self.file_path.path)
            if data != None: a=1 
            else: data = self.data
            file_name, original_path = Formats.FilePath(self.file_path.path).name(), self.file_path.path
            if overwrite_duplicates:
                file = open(self.file_path.path, "wb") 
                file.write(data.encode())
                file.close()
            else:
                extension = file_name.split('.')[file_name.count('.')]
                file_name_without_extension = file_name.replace(extension, '')
                while True:
                    if not os.path.exists(self.file_path.path): break
                    else: self.file_path.path = original_path.replace(file_name, file_name_without_extension+'-'+str(index)+extension)
                file = open(self.file_path.path, "wb") 
                file.write(data.encode())
                file.close()
            self.data = data
        def execute(self, sudo=False, output_append=False, new_terminal=False): # only for executable files.
            if OS == "linux":
                if new_terminal: 
                    if sudo: os.system("sudo gnome-terminal -e 'sh -c {}'".format(self.file_path.path))
                    else: os.system("gnome-terminal -e 'sh -c {}'".format(self.file_path.path))
                else: 
                    if sudo: os.system("sudo "+self.file_path.path)
                    else: os.system(self.file_path.path)
            elif OS == "macos":
                if new_terminal: 
                    if sudo: appscript.app("Terminal").do_script("sudo "+self.file_path.path)
                    else: appscript.app("Terminal").do_script(self.file_path.path)
                else: 
                    if sudo: os.system("sudo "+self.file_path.path)
                    else: os.system(self.file_path.path)
    #
    # the array object class.
    class Array(object):
        def __init__(self, 
            path=False, 
            array=None, 
            # load the data on initialization.
            load=False, 
            # the default array (will be created if file path does not exist).
            default=None,
            check_existance=False,
        ):
            # init.
            if path == False: self.file_path = self.fp = False # used in local memory (not fysical)
            else: self.file_path = self.fp = Formats.FilePath(path, check_existance=check_existance)
            self.array = array
            if default != None and not os.path.exists(self.file_path.path): self.save(array=default)
            if load: self.load()
        def save(self, array=None, ensure_ascii=False, indent=4):
            utils.__check_memory_only__(self.file_path.path)
            if array != None: Formats.check(arrays={"array":array})
            else: array = self.array
            with open(self.file_path.path, 'w+') as json_file:
                json.dump(array, json_file, ensure_ascii=ensure_ascii, indent=indent)
            self.array = array
        def load(self, default=None):
            utils.__check_memory_only__(self.file_path.path)
            Formats.check(nones={"path":self.file_path.path}) # noneCheck is faster then stringCheck
            if not os.path.exists(self.file_path.path) and default != None: 
                Formats.check(arrays={"default":default})
                self.save(default)
            array = None
            try: 
                with open(self.file_path.path, 'r+') as json_file:
                    array = json.load(json_file)
            except PermissionError:
                with open(self.file_path.path, 'r') as json_file:
                    array = json.load(json_file)
            self.array = array
            return array
        def string(self, joiner=" ", sum_first=False):
            string = ""
            for x in self.array:
                if sum_first and string == "": string = joiner + str(x)
                elif string == '': string = str(x)
                else: string += joiner + str(x)
            return str(string)
        def remove(self, items=[]):
            y = []
            for x in self.array:
                if x not in items: y.append(x)
            return y
        def divide(self, into=2):
            avg = len(self.array) / float(into)
            out = []
            last = 0.0
            while last < len(self.array):
                out.append(self.array[int(last):int(last + avg)])
                last += avg
            return out
        def remove(self, indexes=[], values=[], save=False):
            for i in indexes:
                try: self.array.pop(i)
                except: a=1
            if values != []:
                new = []
                for v in self.array:
                    if v not in values: new.append(v)
                self.array = new
            if save: self.save()
            return self.array
        def sort(self, alphabetical=True, ascending=False, reversed=False):
            if alphabetical or ascending:
                return sorted(self.array, reverse=reversed)
            else: raise ValueError("Unknown behaviour, alphabetical=False.")
    #
    # the dictionary object class.
    class Dictionary(object):
        def __init__(self, 
           # the file path.
            path=False, 
            # the dictionary.
            dictionary=None, 
            # load the file path dictionary on init.
            load=False, 
            # specify default to check & create the dict.
            default=None, 
        ):

            # arguments.
            self.dictionary = dictionary
            self.path = path
            self.default = default
            self.file_path = self.fp = False

            # checks.
            if path != False:
                self.file_path = self.fp = Formats.FilePath(path, check_existance=default == None)
            if load: self.load(default=self.default)
            if self.default != None:
                self.load(default=self.default)
                self.check(default=self.default, save=True)
           

            #
            # can be filled with executing [self.x = x()]:
        def save(self, dictionary=None, path=None, ensure_ascii=False, indent=4):
            utils.__check_memory_only__(self.file_path.path)
            if dictionary == None: dictionary = self.dictionary
            if path == None: path = self.file_path.path
            self.dictionary = dictionary
            # save.
            try:
                with open(path, 'w+') as json_file:
                    json.dump(dictionary, json_file, ensure_ascii=ensure_ascii, indent=indent)
            except PermissionError:
                with open(path, 'w') as json_file:
                    json.dump(dictionary, json_file, ensure_ascii=ensure_ascii, indent=indent)
        def load(self, default=None):
            utils.__check_memory_only__(self.file_path.path)
            if not os.path.exists(self.file_path.path) and default != None: 
                self.save(default)
            dictionary = None

            # load.
            try: 
                with open(self.file_path.path, 'r+') as json_file:
                    dictionary = json.load(json_file)
            except PermissionError:
                with open(self.file_path.path, 'r') as json_file:
                    dictionary = json.load(json_file)

            self.dictionary = dictionary
            return dictionary
        def load_line(self, line_number):
            utils.__check_memory_only__(self.file_path.path)
            file = open(self.file_path.path,mode='rb')
            data = file.read()
            file.close()
            return data.decode().split('\n')[line_number]
        def check(self, 
            #   Option 1:
            key=None, # check a certain key, it appends if not present
            value=None, # check a certain key, append the value if not present (no format check)
            #   Option 2:
            default=None, # check based on a default dictionary, it appends it not present.
            #   Optionals:
            dictionary=None, # overwrite the start dictionary, leave None to use self.dictionary.
            save=False, # saves the output & and sets the output to self.dictionary.
        ):  
            def __iterate_dict__(dictionary, default):
                #print("\niterating new dictionary: [{}] & default [{}]\n".format(dictionary, default))
                for identifier, item in default.items():
                    if isinstance(item, dict):
                        try: dictionary[identifier] = __iterate_dict__(dictionary[identifier], item)
                        except KeyError: dictionary[identifier] = dict(item)
                    elif isinstance(item, list):
                        try: dictionary[identifier]
                        except KeyError: dictionary[identifier] = list(item)
                    else:
                        try: dictionary[identifier]
                        except KeyError: dictionary[identifier] = item
                return dictionary

            # init.
            if dictionary == None: dictionary = self.dictionary
            
            #   -   option 1:
            if key == None and value != None: raise ValueError("Define both parameters: [key & value].")
            elif value == None and key != None: raise ValueError("Define both parameters: [key & value].")
            if key != None and value != None:   
                try: dictionary[key]
                except KeyError: dictionary[key] = value
                return dictionary
            Formats.check(booleans={"save":save})
            
            #   -   option 2:
            if default == None: default = self.default
            if default == None: raise ValueError("Define both parameters: [key & value] or parameter [default].")
            dictionary = __iterate_dict__(dictionary, default)
            if save:
                self.dictionary = dictionary
                self.save()
            return dictionary
        def divide(self, into=2):
            "Splits dict by keys. Returns a list of dictionaries."
            return_list = [dict() for idx in range(into)]
            idx = 0
            for k,v in self.dictionary.items():
                return_list[idx][k] = v
                if idx < into-1:  # indexes start at 0
                    idx += 1
                else:
                    idx = 0
            return return_list
        def reversed(self, reversed=False):
            reversed_dict = []
            for key in self.keys(reversed=True):
                reversed_dict[key] = self.dictionary[key]
            return reversed_dict
        def items(self, reversed=False):
            if reversed: return self.reversed().items()
            else: return self.dictionary.items()
        def keys(self, reversed=False):
            if reversed: 
                keys = list(self.dictionary.keys())
                reversed_keys = []
                c = len(keys)-1
                for _ in range(len(keys)):
                    reversed_keys.append(keys[c])
                    c -= 1
                return reversed_keys
            else: return list(self.dictionary.keys())
        def values(self, reversed=False):
            values = []
            for key, value in self.items(reversed=reversed):
                values.append(value)
            return values
        def append(self, 
            # by default it only overwrites if a key does not exist and sums the key if it is a str / int.
            #
            # a dictionary to append.
            dictionary, 
            # the overwrite formats (add "*" for all).
            overwrite=[], 
            # the sum formats (add "*" for all).
            sum=["int", "float"], 
            # the banned dictionary keys.
            banned=[],
            # do not use.
            dictionary_=None,
        ):
            if dictionary_ == None: dictionary_ = self.dictionary
            else: dictionary_ = self.dictionary
            for key, value in dictionary.items():
                if key not in banned:
                    format = Formats.get(value, serialize=True)
                    if format in ["dict"]:
                        try: ldictionary_ = dictionary_[key]
                        except: ldictionary_ = {}
                        value = self.append(value, overwrite=overwrite, sum=sum, banned=banned, dictionary_=ldictionary_)
                    if "*" in sum or format in sum:
                        if format in ["str", "int", "float", "list"]:
                            try: dictionary_[key] += value
                            except KeyError: dictionary_[key] = value
                        else: # already summed.
                            dictionary_[key] = value
                    elif "*" in overwrite or format in overwrite:
                        dictionary_[key] = value
                    else:
                        try: dictionary_[key]
                        except KeyError: dictionary_[key] = value
            return dictionary_
        def unpack(self, defaults:dict):
            list = []
            for key,default in formats.items():
                try: list.append(self.dictionary[key])
                except KeyError: list.append(default)
            return list
        def remove(self, keys=[], values=[], save=False):
            for i in keys:
                try: del self.dictionary[i]
                except: a=1
            if values != []:
                new = {}
                for k,v in self.dictionary.items():
                    if v not in values: new[k] = v
                self.dictionary = new
            if save: self.save()
            return self.dictionary
        def sort(self, alphabetical=True, ascending=False, reversed=False):
            new = {}
            if alphabetical or ascending:
                _sorted_ = Files.Array(path=False, array=list(self.dictionary.keys())).sort(alphabetical=alphabetical, ascending=ascending, reversed=reversed)
            else: raise ValueError("Unknown behaviour, alphabetical=False.")
            for key in _sorted_:
                new[key] = self.dictionary[key]
            return new
        # system functions.
        def __serialize_string__(self, string, banned_characters=["@"]):
            c, s, l = 0, "", False
            for char in string:
                if char not in banned_characters:
                    # regular letter.
                    if char.lower() == char:
                        s += char.lower()
                        l = False
                    # capital letter.
                    else:
                        if c == 0:
                            s += char.lower()
                        else:
                            if l:
                                s += char.lower()
                            else:
                                s += "_"+char.lower()
                        l = True
                    c += 1
            return s
        def __serialize_dictionary__(self, response):
            _response_ = {}
            for key,value in response.items():
                s_key = self.__serialize_string__(key)
                if isinstance(value, dict):
                    _response_[s_key] = self.__serialize_dictionary__(value)
                elif isinstance(value, str):
                    try: integer = int(value)
                    except: integer = False
                    if integer != False:
                        _response_[s_key] = integer
                    elif value in ["false", "False", "FALSE", "DISABLED"]:
                        _response_[s_key] = False
                    elif value in ["true", "True", "TRUE", "ENABLED"]:
                        _response_[s_key] = True
                    else:
                        _response_[s_key] = value
                else:
                    _response_[s_key] = value
            return _response_
        # support item assignment.
        def __setitem__(self, key, value):
            #if "/" in item
            self.dictionary[key] = value
        def __getitem__(self, key):
            #if "/" in item
            return self.dictionary[key]
        def __delitem__(self, key):
            #if "/" in item
            del self.dictionary[key]
        def __splitkey__(self):
            list = key.split("/")
        #  
    #
    # the directory object class.
    class Directory(object):
        def __init__(self, path=None, hierarchy={}):
            # init.
            if path == False: self.file_path = self.fp = False # used in local memory (not fysical)
            else: 
                if path[len(path)-1] != "/": path += "/"
                self.file_path = self.fp = Formats.FilePath(path, check_existance=hierarchy!={})
            self.hierarchy = hierarchy
            if self.hierarchy != {}:
                self.check(hierarchy=hierarchy)

            # can be filled with executing [self.x = x()]:
            # executable functions.
        # actions.
        def create(self, file_paths=[], path=None, sudo=False, owner=None, group=None, permission=None):

            #   -   init:
            if path == None: path = self.file_path.path
            Formats.check(arrays={"file_paths":file_paths})

            #   -   create dir:
            if not os.path.exists(path): 
                if sudo: os.system('sudo mkdir '+path)
                else: os.system('mkdir '+path)

            #   -   copy files:
            commands = []
            for l_path in file_paths: 
                if sudo:
                    command = None
                    if os.path.isdir(l_path): command = 'sudo cp -r {0} {1} '.format(l_path, path+Formats.FilePath(l_path).name())
                    else: command = 'sudo cp {0} {1}'.format(l_path, path+Formats.FilePath(l_path).name())
                    commands.append(command)
                else:
                    command = None
                    if os.path.isdir(l_path): command = 'cp -r {0} {1} '.format(l_path, path+Formats.FilePath(l_path).name())
                    else: command = 'cp {0} {1}'.format(l_path, path+Formats.FilePath(l_path).name())
                    commands.append(command)
            if len(commands) > 0:
                if sudo:
                    script = Files.ShellScript(
                        data=command, 
                        path='/tmp/shell_script-'+str(random.randrange(23984792,23427687323))+'.sh'
                    )
                    script.save()
                    script.setPermission(755)
                    script.execute(sudo=sudo)
                    script.delete()
                else: os.system(Files.Array(array=commands,path=False).string(joiner=" \n "))

            if owner != None or group!=None: self.file_path.ownership.set(owner=owner, group=group, sudo=sudo)
            if permission != None: self.file_path.permission.set(permission=permission, sudo=sudo)
        def delete(self, forced=False):
            if forced: os.system('rm -fr {}'.format(self.file_path.path))
            else: os.system('rm -r {}'.format(self.file_path.path))
        def check(self, 
            #   Required:
            #   -   dictionary format:
            hierarchy=None, 
            #   Optionals:
            #   -   string format:
            owner=None, 
            group=None, 
            #   -   boolean format:
            sudo=False,
            #   -   integer format:
            permission=None, # (octal format)
            recursive=False, # for permission/ownership
            silent=False,
        ):
            format = {
                "my_directory_name":{
                    # Required:
                    "path":"my_directory_name/",
                    # Optionals:
                    "permission":755,
                    "owner":"daanvandenbergh",
                    "group":None,
                    "sudo":False,
                    "directory":True,
                    "recursive":False, # for permission & ownership (directories).
                    "default_data":None, # makes it a file
                    "default":None, # makes it a dictionary
                }
            }
            def checkPermissionOwnership(file_path, dictionary, silent=False, recursive=False):
                if dictionary["permission"] != None and dictionary["permission"] != file_path.permission.permission:
                    #print("editing file [{}] permission [{}] to [{}]...".format(file_path.path, file_path.permission.permission, dictionary["permission"]))
                    file_path.permission.set(permission=dictionary["permission"], sudo=dictionary["sudo"], recursive=recursive, silent=silent)
                if dictionary["owner"] != None and dictionary["owner"] != file_path.ownership.owner:
                    #print("editing file [{}] owner [{}] to [{}]...".format(file_path.path, file_path.ownership.owner, dictionary["owner"]))
                    file_path.ownership.set(owner=dictionary["owner"], group=file_path.ownership.group, sudo=dictionary["sudo"], recursive=recursive, silent=silent)
                #print("file [{}] current group [{}] wanted group [{}]".format(file_path.path, file_path.ownership.group, dictionary["group"]))
                if dictionary["group"] != None and dictionary["group"] != file_path.ownership.group:
                    #print("editing file [{}] group [{}] to [{}]...".format(file_path.path, file_path.ownership.group, dictionary["group"]))
                    file_path.ownership.set(owner=file_path.ownership.owner, group=dictionary["group"], sudo=dictionary["sudo"], recursive=recursive, silent=silent)
            if hierarchy == None: hierarchy = self.hierarchy
            #if owner == None: owner = self.owner
            #if group == None: group = self.group
            #if permission == None: permission = self.permission
            file_path = Formats.FilePath(self.file_path.path)
            if file_path.exists(sudo=sudo) == False:
                file_path.create(
                    directory=True, 
                    permission=permission, 
                    group=group, 
                    owner=owner,
                    sudo=sudo)
            elif group != None or owner != None or permission != None: 
                file_path.permission.permission = file_path.permission.get()
                _owner_,_group_ = file_path.ownership.get()
                file_path.ownership.group = _group_
                file_path.ownership.owner = _owner_
                checkPermissionOwnership(file_path, {"sudo":sudo, "owner":owner, "group":group, "permission":permission}, recursive=recursive, silent=silent)


            if hierarchy == None: raise ValueError("Define dictionary parameter: hierarchy")
            for identifier, dictionary in hierarchy.items():

                #   -   check:
                try: dictionary["path"] = self.file_path.path + dictionary["path"]
                except: raise ValueError("Invalid hierarchy item [{} : {}]. Specify the [path].".format(identifier, "?"))
                try: dictionary["permission"]
                except KeyError: dictionary["permission"] = None
                try: dictionary["owner"]
                except KeyError: dictionary["owner"] = None
                try: dictionary["group"]
                except KeyError: dictionary["group"] = None
                try: dictionary["directory"]
                except KeyError: dictionary["directory"] = False
                try: dictionary["sudo"]
                except KeyError: dictionary["sudo"] = False
                try: dictionary["default_data"]
                except KeyError: dictionary["default_data"] = None
                try: dictionary["default"]
                except KeyError: dictionary["default"] = None
                try: dictionary["recursive"]
                except KeyError: dictionary["recursive"] = False

                #   -   directory:
                if dictionary["directory"]:
                    file_path = Formats.FilePath(dictionary["path"])
                    if file_path.exists(sudo=dictionary["sudo"]) == False:
                        file_path.create(
                            directory=True, 
                            permission=dictionary["permission"], 
                            group=dictionary["group"], 
                            owner=dictionary["owner"],
                            sudo=dictionary["sudo"],)
                    else: 
                        file_path.permission.permission = file_path.permission.get()
                        _owner_,_group_ = file_path.ownership.get()
                        file_path.ownership.group = _group_
                        file_path.ownership.owner = _owner_
                        #if 'back_up_requests/requests' in file_path.path: 
                        #   print("file: {}, owner: {}, group: {}, permission: {}".format(file_path.path, file_path.ownership.owner, file_path.ownership.group, file_path.permission.permission))
                        checkPermissionOwnership(file_path, dictionary, silent=silent, recursive=dictionary["recursive"])

                #   -   file:
                elif dictionary["default_data"] != None:
                    file = Files.File(path=dictionary["path"], check_existance=False)
                    if file.file_path.exists(sudo=dictionary["sudo"]) == False:
                        file.file_path.create(
                            data=dictionary["default_data"], 
                            permission=dictionary["permission"], 
                            group=dictionary["group"], 
                            owner=dictionary["owner"],
                            sudo=dictionary["sudo"])
                    else: 
                        file.file_path.permission.permission = file_path.permission.get()
                        _owner_,_group_ = file_path.ownership.get()
                        file.file_path.ownership.group = _group_
                        file.file_path.ownership.owner = _owner_
                        checkPermissionOwnership(file.file_path, dictionary, silent=silent)

                #   -   dictionary:
                elif dictionary["default"] != None:
                    file = Files.Dictionary(path=dictionary["path"])
                    if file.file_path.exists(sudo=dictionary["sudo"]) == False:
                        file.save(dictionary["default"])
                        file.file_path.permission.check(
                            permission=dictionary["permission"], 
                            sudo=dictionary["sudo"])
                        file.file_path.ownership.check(
                            group=dictionary["group"], 
                            owner=dictionary["owner"],
                            sudo=dictionary["sudo"])
                    else: 
                        file.file_path.permission.permission = file_path.permission.get()
                        _owner_,_group_ = file_path.ownership.get()
                        file.file_path.ownership.group = _group_
                        file.file_path.ownership.owner = _owner_
                        checkPermissionOwnership(file.file_path, dictionary, silent=silent)
                        file.check(default=default, save=True)
                else:
                    raise ValueError("Invalid hierarchy item [{} : {}]. Either [directory] must be enabled, or [default_data / default] must be specified.".format(identifier, dictionary["path"]))

                #
        # returnable functions.
        def paths(self, dirs_only=False, files_only=False, empty_dirs=True, recursive=False, path=None, banned=[], banned_names=[".DS_Store"], extensions=["*"]):
            if dirs_only and files_only: raise ValueError("Both parameters dirs_only & piles_only are True.")
            if path == None: path = self.file_path.path
            if isinstance(extensions, str): extensions = [extensions]
            if len(banned) > 0:
                l_banned = []
                for i in banned:
                    l_banned.append(os.path.join(path, i))
                banned = l_banned
            paths = []
            if recursive:
                # does only work with recursive.
                for root, dirs, files in os.walk(path):
                    if not dirs_only:
                        for name in files:
                            if name not in banned_names and ("*" in extensions or gfp.extension(name=name) in extensions ):
                                l_path = gfp.clean(path=f"{root}/{name}")
                                if l_path not in banned and l_path+"/" not in banned:
                                    paths.append(l_path)
                    if not files_only:
                        for name in dirs:
                            if name not in banned_names and (dirs_only or "*" in extensions or "dir" in extensions ):
                                l_path = gfp.clean(path=f"{root}/{name}/")
                                #print("{} vs {} = {}".format(l_path, banned, l_path not in banned and l_path+"/" not in banned))
                                if l_path not in banned and l_path+"/" not in banned:
                                    paths.append(l_path)
                                    if recursive:
                                        paths += self.paths(recursive=recursive, path=l_path, dirs_only=dirs_only, files_only=files_only, banned=banned, banned_names=banned_names, empty_dirs=empty_dirs)
            else:
                for name in os.listdir(path):
                    l_path = gfp.clean(path=f"{path}/{name}/")
                    if not dirs_only and not os.path.isdir(l_path):
                        if name not in banned_names and ("*" in extensions or gfp.extension(name=name) in extensions ):
                            if l_path not in banned and l_path+"/" not in banned:
                                paths.append(l_path)
                    if not files_only and os.path.isdir(l_path):
                        if name not in banned_names and (dirs_only or "*" in extensions or "dir" in extensions ):
                            if l_path not in banned and l_path+"/" not in banned:
                                paths.append(l_path)
            return paths
        def names(self, dirs_only=False, files_only=False, empty_dirs=True, recursive=False, path=None, banned=[], banned_names=[".DS_Store"], extensions=["*"], remove_extensions=False):
            names = []
            for _path_ in self.paths(dirs_only=dirs_only, files_only=files_only, empty_dirs=empty_dirs, recursive=recursive, path=path, banned=banned, banned_names=banned_names, extensions=extensions):
                if remove_extensions:
                    name = gfp.name(path=_path_)
                    names.append(name[:-len(gfp.extension(name=name))])
                else:
                    names.append(gfp.name(path=_path_))
            return names
        def oldest_path(self):
            files = []
            for i in os.listdir(self.file_path.path):
                if i not in [".DS_Store"]:
                    path = f'{self.file_path.path}/{i}'.replace("//",'/')
                    files.append(path)
            if len(files) == 0: return False
            return min(files, key=os.path.getctime)
        def random_path(self):
            files = []
            for i in os.listdir(self.file_path.path):
                if i not in [".DS_Store"]:
                    path = f'{self.file_path.path}/{i}'.replace("//",'/')
                    files.append(path)
            if len(files) == 0: return False
            return files[random.randrange(0, len(files))]
        def generate_path(self, length=24, type="/"):
            path, paths = None, self.paths()
            for x in range(1000):
                path = self.join(utils.generate.shell_string(length=length), type)
                if path not in paths:
                    break
            if path == None: __error__("Failed to generate a new random path inside directory [{}].".format(self.file_path.path))
            return path
        def structured_join(self, name, type="", structure="alphabetical", create_base=False, sudo=False, owner=None, group=None, permission=None):
            if type not in ["/", ""]:
                type = "."+type
            if structure == "alphabetical":
                alphabetical = None
                try: alphabetical = name[0].upper()
                except: alphabetical = "SPECIAL"
                if str(alphabetical) not in ["A","B","C","D","E","F","G","H","I","J","K","L","M","N","O","P","Q","R","S","T","U","V","W","X","Z","0","1","2","3","4","5","6","7","8","9"]: aplhabetical = "SPECIAL"
                base = self.file_path.path + "/" + alphabetical + "/"
                if create_base and os.path.exists(base) == False:
                    self.create(path=base, sudo=sudo, owner=owner, group=group, permission=permission)
                alph_dir = base + name + type
                return alph_dir
            else: raise ValueError("Invalid usage, parameter structure [{}], valid options: {}".format(structure, ["alphabetical"]))
        def join(self, name=None, type=""):
            return self.file_path.join(name, type)
        def contains(self, name=None, type="/", recursive=False):
            return self.join(name, type) in self.paths(recursive=recursive)
            #
        def subpath(self, fullpath):
            return self.file_path.clean(path=fullpath.replace(self.path, ""), remove_double_slash=True)
        def fullpath(self, subpath):
            return self.file_path.clean(path=f"{self.path}/{subpath}", remove_double_slash=True)
        # return references of each file that includes one of the matches.
        def find(self, matches:list, path=None, recursive=False, log_level=0):
            if path == None: path = self.path
            gfp = Formats.FilePath("")
            c, references = 0, {}
            for string in matches:
                if not os.path.exists(path):
                    raise ValueError(f"Path {path} does not exist.")
                elif not os.path.isdir(path):
                    raise ValueError(f"Path {path} is not a directory.")
                for i_path in self.paths(recursive=recursive, files_only=True, banned_names=[".DS_Store", ".git"], path=path):
                    data = None
                    try:
                        data = Files.load(i_path)
                    except:
                        try:
                            data = f"{Files.load(i_path, format=bytes)}"
                        except: data = None
                    if data != None and string in data: 
                        if log_level >= 0:
                            print("")
                            print(f"{i_path}:")
                        lines, linecount = data.split("\n"), 0
                        for _ in lines:
                            if string in lines[linecount]:
                                try: before = lines[linecount-1]
                                except: before = None
                                try: after = lines[linecount+1]
                                except: after = None
                                if log_level >= 0:
                                    if before != None: print(" * "+before)
                                    print(" * "+lines[linecount])
                                    if after != None: print(" * "+after)
                                references[i_path] = lines[linecount]
                            linecount += 1
                        c += 1
            if log_level >= 0 and c > 0: print("")
            return references
        # replace str within all files.
        def replace(self, replacements:list, path=None, recursive=False, log_level=0):
            if path == None: path = self.path
            gfp = Formats.FilePath("")
            c, updates = 0, []
            for from_, to in replacements:
                if not os.path.exists(path):
                    raise ValueError(f"Path {path} does not exist.")
                elif not os.path.isdir(path):
                    raise ValueError(f"Path {path} is not a directory.")
                for path in self.paths(recursive=recursive, banned_names=[".DS_Store", ".git"], path=path):
                    if not os.path.isdir(path):
                        try:
                            data = Files.load(path)
                        except UnicodeDecodeError: a=1
                        if from_ in data: 
                            if log_level >= 0:
                                loader = syst3m.console.Loader(f"Updating file {path}.")
                            Files.save(path, data.replace(from_, to))
                            if log_level >= 0:
                                loader.stop()
                            updates.append(path)
                            c += 1
            return updates
        #
    #
    # the image object class.
    class Image(object):
        def __init__(self, path=None, image=None, load=False):
            # init.
            if path == False: self.file_path = self.fp = False # used in local memory (not fysical)
            else: self.file_path = self.fp = Formats.FilePath(path)
            self.image = image
            if load: self.load()
        def load(self, path=None):
            if path == None: path = self.file_path.path
            self.image = Image.open(path)
        def edit_pixel(self, pixel=[0, 0], new_pixel_tuple=None):
            pixel = self.image.load()
            pix[15, 15] = value
            self.image.save(self.file_path.path)
        #
    #
    # the zip object class.
    class Zip(object):
        def __init__(self, path=None, check_existance=False):
            
            # init.
            Formats.check(nones={"path":path})
            self.file_path = self.fp = Formats.FilePath(path, check_existance=check_existance)

            #
        def create(self,
            # source can either be a string or an array.
            source=None, 
            # remove the source file(s).
            remove=False,
            # sudo required to move/copy source files.
            sudo=False,
        ):

            # create tmp dir.
            name = self.file_path.name().replace('.encrypted.zip','').replace("."+self.file_path.extension(),'')
            tmp = Formats.FilePath(f'/tmp/zip-{utils.generate.shell_string(24)}')
            tmp_content = Formats.FilePath(tmp.join(name, ""))
            if tmp.exists(): tmp.delete(forced=True)
            if os.path.exists(tmp.path):os.system(f"rm -fr {tmp.path}")
            os.system(f"mkdir {tmp.path}")
            if isinstance(source, str):
                target = Formats.FilePath(source)
                name = target.name().replace('.encrypted.zip','').replace("."+target.extension(),'')
                if remove: target.move(tmp_content.path, sudo=sudo)
                else: target.copy(tmp_content.path, sudo=sudo)
            elif isinstance(source, list):
                tmp_content.create(directory=True)
                for path in source:
                    file_path = Formats.FilePath(path)
                    if remove: file_path.move("/"+tmp_content.join('/'+file_path.name(),"/"), sudo=sudo)
                    else: file_path.copy("/"+tmp_content.join('/'+file_path.name(),"/"), sudo=sudo)
            else: raise ValueError("Parameter [source] must either be a str or list.")

            # write out zip.
            base = self.file_path.base()
            format = self.file_path.extension()
            archive_from = os.path.dirname(tmp_content.path)
            archive_to = os.path.basename(tmp_content.path.strip(os.sep))
            zip_path = shutil.make_archive(name, format, archive_from, archive_to)
            os.system(f'mv {zip_path} {self.file_path.path}')
            tmp.delete(forced=True, sudo=sudo)

            #
        def extract(self, 
            # the base extract directory.
            base=None, 
            # remove the zip after extraction.
            remove=False,
            # if sudo required for removing file path.
            sudo=False,):

            # extract.
            if base == None:
                base = self.file_path.base()
            with zipfile.ZipFile(self.file_path.path, 'r') as zip_ref:
                zip_ref.extractall(base)
            if remove: self.file_path.delete(forced=True, sudo=sudo)
            
            #
        
        #
        #
    #
    # the bytes object class.
    class Bytes(object):
        def __init__(self, path=None,):
           
           # init.
            Formats.check(bytes_={"bytes":bytes})
            self.file_path = self.fp = Formats.FilePath(path, check_existance=check_existance)
            self.bytes = bytes  
            
            #
        def load(self):
            with open(self.file_path.path, 'rb') as file_data:
                bytes = file_data.read()
            self.bytes = bytes
            return bytes
        def save(self, bytes=None):
            if bytes == None: bytes = self.bytes
            self.bytes = bytes
            with open(self.file_path.path, 'wb') as file_data:
                file_data.write(bytes)

        #
        #
    #
# the format classes.
class Formats():
    digits = [0,1,2,3,4,5,6,7,8,9,]
    str_digits = ["0","1","2","3","4","5","6","7","8","9"]
    alphabet, capitalized_alphabet = ["a","b","c","d","e","f","g","h","i","j","k","l","m","n","o","p","q","r","s","t","u","v","w","x","y","z"], []
    for i in alphabet: capitalized_alphabet.append(i.upper())
    special_characters = ["±","§","!","@","€","#","£","$","¢","%","∞","^","&","ª","(",")","–","_","+","=","{","}","[","]",";",":","'",'"',"|","\\","//","?",">",".",",","<"]
    def check(
        nones=None,
        booleans=None,
        none_allowed_booleans=None,
        strings=None,
        none_allowed_strings=None,
        integers=None,
        none_allowed_integers=None,
        bytes_=None,
        none_allowed_bytes=None,
        arrays=None,
        none_allowed_arrays=None,
        dictionaries=None,
        none_allowed_dictionaries=None,
    ):
        if nones != None:
            for key,value in nones.items():
                if value == None: raise ValueError(f"Invalid [{key}] format [{value}], required format is [!null].")
        if booleans != None:
            for key,value in booleans.items():
                if not isinstance(value, bool): raise ValueError(f"Invalid [{key}] format [{value}], required format is [bool].")
        if none_allowed_booleans != None:
            for key,value in none_allowed_booleans.items():
                if not isinstance(value, bool) and value != None: raise ValueError(f"Invalid [{key}] format [{value}], required format is [bool].")
        if strings != None:
            for key,value in strings.items():
                if not isinstance(value, str): raise ValueError(f"Invalid [{key}] format [{value}], required format is [str].")
        if none_allowed_strings != None:
            for key,value in none_allowed_strings.items():
                if not isinstance(value, str) and value != None: raise ValueError(f"Invalid [{key}] format [{value}], required format is [str].")
        if integers != None:
            for key,value in integers.items():
                if not isinstance(value, int): raise ValueError(f"Invalid [{key}] format [{value}], required format is [int].")
        if none_allowed_integers != None:
            for key,value in none_allowed_integers.items():
                if not isinstance(value, int) and value != None: raise ValueError(f"Invalid [{key}] format [{value}], required format is [int].")
        if bytes_ != None:
            for key,value in bytes_.items():
                if not isinstance(value, bytes): raise ValueError(f"Invalid [{key}] format [{value}], required format is [bytes].")
        if none_allowed_bytes != None:
            for key,value in none_allowed_bytes.items():
                if not isinstance(value, bytes) and value != None: raise ValueError(f"Invalid [{key}] format [{value}], required format is [bytes].")
        if arrays != None:
            for key,value in arrays.items():
                if not isinstance(value, list): raise ValueError(f"Invalid [{key}] format [{value}], required format is [list].")
        if none_allowed_arrays != None:
            for key,value in none_allowed_arrays.items():
                if not isinstance(value, list) and value != None: raise ValueError(f"Invalid [{key}] format [{value}], required format is [list].")
        if dictionaries != None:
            for key,value in dictionaries.items():
                if not isinstance(value, dict): raise ValueError(f"Invalid [{key}] format [{value}], required format is [dict].")
        if none_allowed_dictionaries != None:
            for key,value in none_allowed_dictionaries.items():
                if not isinstance(value, dict) and value != None: raise ValueError(f"Invalid [{key}] format [{value}], required format is [dict].")
    def get(value, serialize=False):
        if value == None: return None
        elif isinstance(value, bool): 
            if not serialize:   return bool
            else:               return "bool"
        elif isinstance(value, str): 
            if not serialize:   return str
            else:               return "str"
        elif isinstance(value, int): 
            if not serialize:   return int
            else:               return "int"
        elif isinstance(value, bytes): 
            if not serialize:   return bytes
            else:               return "bytes"
        elif isinstance(value, list): 
            if not serialize:   return list
            else:               return "list"
        elif isinstance(value, dict): 
            if not serialize:   return dict
            else:               return "dict"
        elif isinstance(value, object): 
            if not serialize:   return object
            else:               return "object"
        else: raise ValueError(f"Unknown format [{value}].")
        #
    #
    # the file path object class.
    class FilePath(object):
        def __init__(self, path, default=False, check_existance=False, load=False):
            # init.
            self.path = path
            if check_existance == False and default == False and path != False:
                Formats.check(strings={"path":self.path})
                if os.path.isdir(self.path) and self.path[len(self.path)-1] != '/': self.path += '/'
            if check_existance and os.path.exists(self.path) == False: raise FileNotFoundError("Path [{}] does not exist.".format(self.path))
            self.ownership = self.Ownership(path=self.path, load=load)
            self.permission = self.Permission(path=self.path, load=load)

            #
        #   -   objects:
        class Ownership(object):
            def __init__(self, path=None, load=False):
                # init.
                self.path = path
                self.owner = None
                self.group = None
                if load: 
                    get = self.get()
                    self.owner = get["owner"]
                    self.group = get["permission"]

            #   -   info:
            def get(self):
                owner = pwd.getpwuid(os.stat(self.path).st_uid).pw_name
                group = grp.getgrgid(os.stat(self.path).st_gid).gr_name
                return owner, group
            def set(self, owner=None, group=None, sudo=False, recursive=False, silent=False):
                if group == None:
                    if OS in ["macos"]: group = "wheel"
                    elif OS in ["linux"]: group = "root"
                    else: raise ValueError("Unsupported operating system [{}].".format(OS))
                Formats.check(strings={"owner":owner, "group":group})
                silent_option = ""
                if silent: silent_option = ' 2> /dev/null'
                if recursive:
                    if sudo: os.system("sudo chown -R {} {} {}".format(owner+":"+group, self.path, silent_option))
                    else: os.system("chown -R {} {}".format(owner+":"+group, self.path))
                else:
                    if sudo: os.system("sudo chown {} {} {}".format(owner+":"+group, self.path, silent_option))
                    else: os.system("chown {} {} {}".format(owner+":"+group, self.path, silent_option))
            def check(self, owner=None, group=None, sudo=False, silent=False, iterate=False, recursive=False): # combine [recursive] and [iterate] to walk all set all files in an directory and check it with the given permission.
                if group == None:
                    if OS in ["macos"]: group = "wheel"
                    elif OS in ["linux"]: group = "root"
                    else: raise ValueError("Unsupported operating system [{}].".format(OS))
                Formats.check(strings={"owner":owner, "group":group})
                _owner_, _group_ = self.get()
                if _owner_ != owner or _group_ != group:
                    self.set(owner=owner, group=group, sudo=sudo, silent=silent, recursive=recursive)
                if recursive and iterate and os.path.isdir(self.path):
                    for dirpath, subdirs, files in os.walk(self.path):
                        for path in subdirs: 
                            #print("DIRECTORY:",path)
                            #print("> FULL PATH NAME:",dirpath+"/"+path)
                            if path not in ["lost+found"]:
                                file_path = Formats.FilePath(dirpath+"/"+path)
                                file_path.ownership.check(owner=owner, group=group, sudo=sudo, silent=silent)
                        for path in files: 
                            #print("FILE NAME:",path)
                            #print("> FULL PATH:",dirpath+"/"+path)
                            file_path = Formats.FilePath(dirpath+"/"+path)
                            file_path.ownership.check(owner=owner, group=group, sudo=sudo, silent=silent)                           
        class Permission(object):
            def __init__(self, path=None, load=False):
               # init.
                self.path = path
                self.permission = None
                if load: self.permission = self.get()

            #   -   info:
            def get(self):
                status = os.stat(self.path) 
                permission = oct(status.st_mode)[-3:]
                return permission
            def set(self, permission=None, sudo=False, recursive=False, silent=False):
                Formats.check(nones={"permission":permission})
                silent_option = ""
                if silent: silent_option = ' 2> /dev/null'
                if recursive:
                    if sudo: os.system("sudo chmod -R {} {} {}".format(permission, self.path, silent_option))
                    else: os.system("chmod -R {} {} {}".format(permission, self.path, silent_option))
                else:
                    if sudo: os.system("sudo chmod {} {} {}".format(permission, self.path, silent_option))
                    else: os.system("chmod {} {} {}".format(permission, self.path, silent_option))
            def check(self, permission=None, sudo=False, silent=False, iterate=False, recursive=False): # combine [recursive] and [iterate] to walk all set all files in an directory and check it with the given permission.
                Formats.check(nones={"permission":permission})
                if self.get() != permission:
                    self.set(permission=permission, sudo=sudo, silent=silent, recursive=recursive)
                if recursive and iterate and os.path.isdir(self.path):
                    for dirpath, subdirs, files in os.walk(self.path):
                        for path in subdirs: 
                            #print("DIR NAME:",path)
                            #print("> FULL PATH:",dirpath+"/"+path)
                            if path not in ["lost+found"]:
                                file_path = Formats.FilePath(dirpath+"/"+path)
                                file_path.permission.check(permission=permission, sudo=sudo, silent=silent)
                        for path in files: 
                            #print("FILE NAME:",path)
                            #print("> FULL PATH:",dirpath+"/"+path)
                            file_path = Formats.FilePath(dirpath+"/"+path)
                            file_path.permission.check(permission=permission, sudo=sudo, silent=silent)

        #   -   info:
        def join(self, name=None, type="/"):
            if type not in ["", "/"] and "." not in type:
                type = "." + type
            path = self.path
            if path[len(path)-1] != "/": path += '/'
            return "{}{}{}".format(path, name, type)
        def name(self, remove_extension=False, path=None):
            if path == None: path = self.path
            if path in [False, None]: return None
            x = 1
            if path[len(path)-1] == '/': x += 1
            name = path.split('/')[len(path.split('/'))-x]
            if remove_extension:
                count = len(name.split("."))
                if count > 1:
                    c, s = 0, None
                    for i in name.split("."):
                        if c < count-1:
                            if s == None: s = i
                            else: s += "."+i
                        c += 1
                    name = s
            return name
        def extension(self, name=None, path=None):
            if path == None: path = self.path
            #   -   check directory:
            extension = None
            if name == None and os.path.isdir(path): extension = 'dir'
            else:
                #   -   get extension:
                try:
                    if name == None: name = self.name(path=path)
                    extension = name.split('.')[len(name.split('.'))-1]
                except:
                    try:
                        name = self.name(path=path)
                        extension = name.split('.')[len(name.split('.'))-1]
                    except: extension = None
            #   -   check image & video:
            if extension in ["jpg", "png", "gif", "webp", "tiff", "psd", "raw", "bmp", "heig", "indd", "jpeg", "svg", "ai", "eps", "pdf"]: extension = "img"
            elif extension in ["mp4", "m4a", "m4v", "f4v", "f4a", "m4b", "m4r", "f4b", "mov", "3gp", "3gp2", "3g2", "3gpp", "3gpp2", "h.263", "h.264", "hevc", "mpeg4", "theora", "3gp", "windows media 8", "quicktime", "mpeg-4", "vp8", "vp6", "mpeg1", "mpeg2", "mpeg-ts", "mpeg", "dnxhd", "xdcam", "dv", "dvcpro", "dvcprohd", "imx", "xdcam", "hd", "hd422"]: extension = "video"
            return extension
        def base(self, 
            # the path (leave None to use self.path) (param #1).
            path=None,
            # the dirs back.
            back=1,
        ):
            if path == None: path = self.path
            base = path.replace('//','/')
            if base[len(base)-1] == '/': base = base[:-1]
            if len(base.split("/")) <= 1: raise ValueError("Path [{}] has no base.".format(base))
            startslash = True
            if base[0] != "/":
                startslash = False
            base = base.split("/")
            m, c, s = len(base), 0, ""
            for i in base:
                if c >= m-back: break
                if c == 0:
                    s = f"/{i}/"
                else:
                    s += f"{i}/"
                c += 1
            if startslash:
                return s
            else:
                return s[1:]
            ###### OLD.
            base = path.replace('//','/')
            if len(base.split("/")) <= 1: raise ValueError("Path [{}] has no base.".format(base))
            if base[len(base)-1] == '/': base = base[:-1]
            for x in range(back, back+1):
                last = (base.split('/')[len(base.split('/'))-1]).replace('//','/')
                base = base[:-len("/"+last)]
            while True:
                if '//' in base: base = base.replace('//','/')
                else: break
            if base[len(base)-1] != "/": base += '/'
            return base
            """splitted, result, count = path.split('/'), "", 0
            for i in splitted:
                if count < len(splitted) - 1 - back:
                    result += '/' + i
                else: result += "/"
                count += 1
            """
        def basename(self, back=1, path=None):
            if path == None: path = self.path
            return self.name(path=self.base(back=back, path=path))
        def size(self, mode="auto", options=["auto", "bytes", "kb", "mb", "gb", "tb"], type=str, path=None):
            if path == None: path = self.path
            def get_directory_size1(directory):
                total_size = 0
                for path, dirs, files in os.walk(path):
                    for f in files:
                        fp = os.path.join(path,f)
                        try: total_size += os.path.getsize(fp)
                        except: a=1
                return total_size
            #dirs_dict = {}
            #for root, dirs, files in os.walk(path ,topdown=False):
            #   size = sum(os.path.getsize(os.path.join(root, name)) for name in files) 
            #   try: subdir_size = sum(dirs_dict[os.path.join(root,d)] for d in dirs)
            #   except KeyError:
            #       dirs_dict[os.path.join(root,d)] = 0
            #       subdir_size = sum(dirs_dict[os.path.join(root,d)] for d in dirs)
            #   total_size = size + subdir_size
            def get_directory_size2(directory):
                total = 0
                try:
                    # print("[+] Getting the size of", directory)
                    for entry in os.scandir(directory):
                        if entry.is_file():
                            # if it's a file, use stat() function
                            total += entry.stat().st_size
                        elif entry.is_dir():
                            # if it's a directory, recursively call this function
                            total += get_directory_size2(entry.path)
                except NotADirectoryError:
                    # if `directory` isn't a directory, get the file size then
                    return os.path.getsize(directory)
                except PermissionError:
                    # if for whatever reason we can't open the folder, return 0
                    return 0
                return total
            total_size = get_directory_size2(self.path)
            if mode == "auto":
                if int(total_size/1024**4) >= 10:
                    total_size = '{:,} TB'.format(int(round(total_size/1024**4,2))).replace(',', '.')
                elif int(total_size/1024**3) >= 10:
                    total_size = '{:,} GB'.format(int(round(total_size/1024**3,2))).replace(',', '.')
                elif int(total_size/1024**2) >= 10:
                    total_size = '{:,} MB'.format(int(round(total_size/1024**2,2))).replace(',', '.')
                elif int(total_size/1024) >= 10:
                    total_size = '{:,} KB'.format(int(round(total_size/1024,2))).replace(',', '.')
                else:
                    total_size = '{:,} Bytes'.format(int(int(total_size))).replace(',', '.')
            elif mode == "bytes" or mode == "bytes".upper(): total_size = '{:,} Bytes'.format(int(total_size)).replace(',', '.') 
            elif mode == "kb" or mode == "kb".upper(): total_size = '{:,} KB'.format(int(round(total_size/1024,2))).replace(',', '.') 
            elif mode == "mb" or mode == "mb".upper(): total_size = '{:,} MB'.format(int(round(total_size/1024**2,2))).replace(',', '.') 
            elif mode == "gb" or mode == "gb".upper(): total_size = '{:,} GB'.format(int(round(total_size/1024**3,2))).replace(',', '.') 
            elif mode == "tb" or mode == "tb".upper(): total_size = '{:,} TB'.format(int(round(total_size/1024**4,2))).replace(',', '.') 
            else: __error__("selected an invalid size mode [{}], options {}.".format(mode, options))
            if type == int:
                return int(total_size.split(" ")[0])
            else: return total_size 
        def exists(self, path=None, sudo=False):
            if path == None: path = self.path
            if not sudo:
                return os.path.exists(path)
            else:
                try:
                    output = utils.__execute__(["sudo", "ls","-ld",path])
                    if "No such file or directory" in output:
                        return False   
                    else: return True
                except: return False
            #
        def mount(self):
            return os.path.ismount(self.path)
            #
        def directory(self):
            return os.path.isdir(self.path)
            #
        def mtime(self, format='%d-%m-%y %H:%M.%S', path=None):
            if path == None: path = self.path
            fname = pathlib.Path(path)
            try: mtime = fname.stat().st_mtime
            except: mtime = fname.stat().ct_mtime
            if format in ['s', "seconds"]:
                return mtime
            else:
                return Formats.Date().from_seconds(mtime, format=format)
        def clean(self, 
            # the path (leave None to use self.path) (param #1).
            path=None, 
            # the clean options.
            remove_double_slash=True, 
            remove_first_slash=False, 
            remove_last_slash=False,
            ensure_first_slash=False,
            ensure_last_slash=False,
        ):
            if path == None: path = self.path
            while True:
                if remove_double_slash and "//" in path: path = path.replace("//","/")
                elif remove_first_slash and len(path) > 0 and path[0] == "/": path = path[1:]
                elif remove_last_slash and len(path) > 0 and path[len(path)-1] == "/": path = path[:-1]
                elif ensure_first_slash and len(path) > 0 and path[0] != "/": path = "/"+path
                elif ensure_last_slash and len(path) > 0 and path[len(path)-1] != "/": path += "/"
                else: break
            return path
        def absolute(self, 
            # the path (leave None to use self.path) (param #1).
            path=None,
        ):
            if path == None: path = self.path
            return os.path.abspath(path)
        # serialize a requirements file.
        def requirements(self, path=None, format="pip", include_version=True):
            if format in ["pip3"]: format = "pip"
            if format not in ["pip"]: raise ValueError(f"Invalid usage, format [{format}] is not a valid option, options: [pip].")
            # pip requirements.
            if format == "pip":
                requirements = []
                for i in Files.load(path).split("\n"):
                    if len(i) > 0 and i[0] != "#" and i not in [""," "]:
                        while True:
                            if len(i) > 0 and i[len(i)-1] in [" "]: i = i[:-1]
                            else: break
                        if " " not in i:
                            sid = None
                            for lid in ["==", ">=", "<="]:
                                if lid in i: sid = lid ; break
                            if sid != None:
                                if include_version:
                                    requirements.append(i)
                                else:
                                    requirements.append(i.split(sid)[0])
                            else:
                                requirements.append(i)
                return requirements
        #   -   commands:
        def delete(self, 
            # the path (leave None to use self.path) (param #1).
            path=None,
            # the options.
            forced=False,
            sudo=False,
            silent=False,
        ):
            if path == None: path = self.path
            if silent: silent = ' 2> /dev/null'
            else: silent = ""
            if sudo: sudo = "sudo "
            else: sudo = ""
            options = ""
            if forced: 
                options = " -f "
                if os.path.isdir(path): options = " -fr "
            elif os.path.isdir(path): options = " -r "
            os.system(f"{sudo}rm{options}{path}{silent}")
        def move(self, path=None, sudo=False, silent=False):
            if silent: silent = ' 2> /dev/null'
            else: silent = ""
            if sudo: sudo = "sudo "
            else: sudo = ""
            os.system(f"{sudo}mv {self.path} {path}{silent}")
            self.path = path
        def copy(self, path=None, sudo=False, silent=False):
            if silent: silent = ' 2> /dev/null'
            else: silent = ""
            if sudo: sudo = "sudo "
            else: sudo = ""
            if self.directory(): dir = "-r "
            else: dir = ""
            os.system(f"{sudo}cp {dir}{self.path} {path}{silent}")
        def open(self, sudo=False):
            if sudo: sudo = "sudo "
            else: sudo = ""
            if OS in ["macos"]: 
                os.system(f"{sudo}open {self.path}")
            elif OS in ["linux"]: 
                os.system(f"{sudo}nautulis {self.path}")
            else: utils.__invalid_os__(OS)
        def create(self, 
            #   Option 1: (creating a directory)
            #   -   boolean format:
            directory=False,
            #   Option 2: (creating any file extension)
            #   -   string format:
            data="",
            #   Options:
            #   -   integer format:
            permission=None,
            #   -   string format:
            owner=None,
            group=None,
            #   -   boolean format:
            sudo=False,
        ):

            #   -   option 1:
            if directory: 
                if sudo: os.system('sudo mkdir '+self.path)
                else: os.system('mkdir '+self.path)
            
            #   -   option 2:
            elif data != None: 
                if sudo:
                    f = Files.File(path='/tmp/tmp_file', data=data)
                    f.save()
                    os.system(f"sudo mv {f.file_path.path} {self.path}")

                else:
                    Files.File(path=self.path, data=data).save()
                #with open
            
            #   -   invalid option:
            else: raise ValueError("Invalid option, either enable the [directory] boolean to create a directory, or specify [path] and [data] to create any file sort.")

            #   -   default:
            if owner != None or group != None: self.ownership.set(owner=owner, group=group, sudo=sudo)
            if permission != None: self.permission.set(permission, sudo=sudo)


            #
        def check(self, 
            #   Option 1: (creating a directory)
            #   -   boolean format:
            directory=False,
            #   Option 2: (creating any file extension)
            #   -   string format:
            data="",
            #   Options:
            #   -   integer format:
            permission=None,
            #   -   string format:
            owner=None,
            group=None,
            #   -   boolean format:
            sudo=False,
            silent=False,
            recursive=False, # for directories only (for permission & ownership check)
        ):

            #   -   option 1:
            if not self.exists(sudo=sudo):
                self.create(directory=directory, data=data, permission=permission, owner=owner, group=group, sudo=sudo)
            else:
                #   -   default:
                self.ownership.check(owner=owner, group=group, sudo=sudo, silent=silent, recursive=recursive)
                self.permission.check(permission=permission, sudo=sudo, silent=silent, recursive=recursive)
            
            #
        # system functions.
        def __str__(self):
            return self.path
        #
    #
    # the string object class.
    class String(object):
        def __init__(self, string):
           # init.
            Formats.check(strings={"string":string})
            self.string = string
            # can be filled with executing [self.x = x()]:
        def is_numerical(self):
            for i in ["q", "w", "e", "r", "t", "y", "u", "i", "o", "p", "a", "s", "d", "f", "g", "h", "j", "k", "l", "z", "x", "c", "v", "b", "n", "m"]:
                if i in self.string.lower(): return False
            return True
        def bash(self):
            a = self.string.replace('(','\(').replace(')','\)').replace("'","\'").replace(" ","\ ").replace("$","\$").replace("!","\!").replace("?","\?").replace("@","\@").replace("$","\$").replace("%","\%").replace("^","\^").replace("&","\&").replace("*","\*").replace("'","\'").replace('"','\"')       
            return a
        def identifier(self):
            x = self.string.lower().replace(' ','-')
            return x
        def capitalized_scentence(self):
            x = self.string.split(" ")
            cap = [y.capitalize() for y in x]
            return " ".join(cap)
        def capitalized_word(self):
            try:
                new = self.string[0].upper()
                c = 0
                for i in self.string:
                    if c > 0: new += i
                    c += 1
                return new
            except IndexError: return self.string
        def generate(self, 
            # the length of the generated string.
            length=6, 
            # include digits.
            digits=False, 
            # include capital letters.
            capitalize=False, 
            # include special characters.
            special=False,
        ):
            charset = ["a","b","c","d","e","f","g","h","i","j","k","l","m","n","o","p","q","r","s","t","u","v","w","x","y","z"]
            if capitalize:
                for i in  ["a","b","c","d","e","f","g","h","i","j","k","l","m","n","o","p","q","r","s","t","u","v","w","x","y","z"]: charset.append(i.upper())
            if digits: digits = ["1","2","3","4","5","6","7","8","9","0"]
            else: digits = []
            if special: special = ["!", "?", "&", "#","@", "*"]
            else: special = []
            s = ""
            for i in range(length):
                if len(digits) > 0 and random.randrange(1,101) <= 40:
                    s += digits[random.randrange(0, len(digits))]
                elif len(special) > 0 and random.randrange(1,101) <= 10:
                    s += special[random.randrange(0, len(special))]
                else:
                    s += charset[random.randrange(0, len(charset))]
            return s
            #
        # iterate a string (backwards) to check the first occurency of a specified charset.
        def first_occurence(self, charset=[" ", "\n"], reversed=False):
            string = self.string
            if reversed:
                c, space_newline_id = len(string)-1, ""
                for _ in string:
                    char = string[c]
                    if char in charset:
                        a = 0
                        for i in charset:
                            if i == char: return i
                    c -= 1
                return None
            else:
                c, space_newline_id = 0, ""
                for _ in string:
                    char = string[c]
                    if char in charset:
                        a = 0
                        for i in charset:
                            if i == char: return i
                    c += 1
                return None
        # splice a string into before/after by a first occurence.
        # if include is True and both include_before and inluce_after are False it includes at before.
        def before_after_first_occurence(self, slicer=" ", include=True, include_before=False, include_after=False): 
            if isinstance(slicer, list):
                first = self.first_occurence(charset=slicer)
                return self.before_after_first_occurence(slicer=first, include=include, include_before=include_before, include_after=include_after)
            else:
                string = self.string
                before, after, slice_count, slices, _last_ = "", "", string.count(slicer), 0, ""
                for char in string:
                    if len(_last_) >= len(slicer): _last_ = _last_[1:]
                    _last_ += char
                    if _last_ == slicer: 
                        slices += 1
                        if include:
                            if slices != slice_count or include_before:
                                before += char
                            elif include_after:
                                after += char
                            else:
                                before += char
                    elif slices > 0:
                        after += char
                    else: 
                        before += char
                return before, after
        # splice a string into before/selected/after by a first occurence.
        def before_selected_after_first_occurence(self, slicer=" "):
            string = self.string
            before, selected, after, slice_count, open, _last_ = "", "", "", string.count(slicer), False, ""
            selected_sliced_count = 0
            for char in string:
                if isinstance(slicer, str) and len(_last_) >= len(slicer): _last_ = _last_[1:]
                elif isinstance(slicer, list) and len(_last_) >= len(slicer[selected_sliced_count]): _last_ = _last_[1:]
                _last_ += char
                if (isinstance(slicer, str) and _last_ == slicer) or (isinstance(slicer, list) and _last_ == slicer[selected_sliced_count]): 
                    selected_sliced_count += 1
                    selected += char
                    if open: open = False
                    else: open = True
                elif open:
                    after += char
                else: 
                    before += char
            return before, selected, after
        # splice a string into before/after by a last occurence.
        # if include is True and both include_before and inluce_after are False it includes at before.
        def before_after_last_occurence(self, slicer=" ", include=True, include_before=False, include_after=False): 
            string = self.string
            before, after, slice_count, slices, _last_ = "", "", string.count(slicer), 0, ""
            for char in string:
                if len(_last_) >= len(slicer): _last_ = _last_[1:]
                _last_ += char
                if _last_ == slicer: 
                    slices += 1
                    if include:
                        if slices != slice_count or include_before:
                            before += char
                        elif include_after:
                            after += char
                        else:
                            before += char
                elif slices == slice_count:
                    after += char
                else: 
                    before += char
            return before, after
        # splice a string into before/selected/after by a last occurence.
        def before_selected_after_last_occurence(self, slicer=" "):
            string = self.string
            before, selected, after, slice_count, slices, _last_ = "", "", "", string.count(slicer), 0, ""
            for char in string:
                if len(_last_) >= len(slicer): _last_ = _last_[1:]
                _last_ += char
                if _last_ == slicer: 
                    slices += 1
                    selected += char
                elif slices == slice_count:
                    after += char
                else: 
                    before += char
            return before, selected, after
        # get the first text between an 2 string identifiers [start,end] by depth.
        # identifiers must be parameter number 1.
        def between(self, identifiers=["{","}"], depth=1):
            s, open, opened = "", 0, False
            for i in self.string:
                if i == identifiers[0]:
                    open += 1
                elif i == identifiers[1]:
                    open -=1
                if open >= depth:
                    s += i
                    if len(s) > 0:
                        opened = True
                if opened and open < depth:
                    s += i
                    break
            return s
        # increase version.
        def increase_version(self):

            # version 2.
            #
            path = "/tmp/increase_version"
            Files.save(path, f"""version='{self.string}"""+"""' && echo $version | awk -F. -v OFS=. 'NF==1{print ++$NF}; NF>1{if(length($NF+1)>length($NF))$(NF-1)++; $NF=sprintf("%0*d", length($NF), ($NF+1)%(10^length($NF))); print}'""")
            return subprocess.check_output([f"bash", path]).decode().replace("\n","")

            # version 1.
            #
            old_version = self.string
            base, _base_= [], old_version.split(".")
            increase = True
            for i in _base_:
                base.append(int(i))
            count = len(base)-1
            for i in range(len(base)):
                if increase:
                    if base[count] >= 9:
                        if count > 0:
                            base[count-1] += 1
                            base[count] = 0
                            increase = False
                        else:
                            base[count] += 1
                            break
                    else:
                        base[count] += 1
                        break
                else:
                    if count > 0 and int(base[count]) >= 10:
                        base[count-1] += 1
                        base[count] = 0
                        increase = False
                    elif count == 0: break
                count -= 1
            version = ""
            for i in base:
                if version == "": version = str(i)
                else: version += "."+str(i) 
            return version
        # slice dict from string.
        # get the first {} from the string by depth.
        def slice_dict(self, depth=1):
            return self.between(["{", "}"], depth=depth)
        # slice array from string.
        # get the first [] from the string by depth.
        def slice_array(self, depth=1):
            return self.between(["[", "]"], depth=depth)
        # system functions.
        def __str__(self):
            return self.string
    #
    # the boolean object class.
    class Boolean(object):
        def __init__(self, bool):
           # init.
            Formats.check(booleans={"bool":bool})
            self.bool = bool
            if self.bool in ["true", "True", "TRUE", True]: self.bool = True
            else: self.bool = False
            # can be filled with executing [self.x = x()]:
        def convert(self, true="True", false="False"):
            if self.bool:
                return true
            else:
                return false
        #
    #
    # the integer object class.
    class Integer(object):
        def __init__(self, value):
            # init.
            Formats.check(integers={"value":value})
            self.value = value
            self.int = int(value)
            self.float = float(value)
            # self.int = double(value)

            # can be filled with executing [self.x = x()]:
        def increase_version(self):

            # version 1.
            #
            old_version = self.value
            base, _base_= [], old_version.split(".")
            increase = True
            for i in _base_:
                base.append(int(i))
            count = len(base)-1
            for i in range(len(base)):
                if increase:
                    if base[count] >= 9:
                        if count > 0:
                            base[count-1] += 1
                            base[count] = 0
                            increase = False
                        else:
                            base[count] += 1
                            break
                    else:
                        base[count] += 1
                        break
                else:
                    if count > 0 and int(base[count]) >= 10:
                        base[count-1] += 1
                        base[count] = 0
                        increase = False
                    elif count == 0: break
                count -= 1
            version = ""
            for i in base:
                if version == "": version = str(i)
                else: version += "."+str(i) 
            return version
        def round(self, decimals):
            """
            Returns a value rounded down to a specific number of decimal places.
            """
            if not isinstance(decimals, int):
                raise TypeError("decimal places must be an integer")
            else:  return round(self.value, decimals)
        def round_down(self, decimals):
            """
            Returns a value rounded down to a specific number of decimal places.
            """
            if not isinstance(decimals, int):
                raise TypeError("decimal places must be an integer")
            elif decimals < 0:
                raise ValueError("decimal places has to be 0 or more")
            elif decimals == 0:
                return math.ceil(self.value)
            factor = 10 ** decimals
            return math.floor(self.value * factor) / factor
        def generate(self, length=6):
            return utils.generate.pincode(length=length)
            #
        #
    #
    # the date object class.
    class Date(object):
        def __init__(self):
            today = datetime.today()
            self.seconds_format = '%S'
            self.seconds = str(today.strftime(self.seconds_format))
            self.minute_format = '%M'
            self.minute =  str(today.strftime(self.minute_format))
            self.hour_format = '%H'
            self.hour =  str(today.strftime(self.hour_format))
            self.day_format = '%d'
            self.day =  str(today.strftime(self.day_format))
            self.day_name_format = '%a'
            self.day_name =  str(today.strftime(self.day_name_format))
            self.week_format = '%V'
            self.week =  str(today.strftime(self.week_format))
            self.month_format = '%m'
            self.month =  str(today.strftime(self.month_format))
            self.month_name_format = '%h'
            self.month_name = str(today.strftime(self.month_name_format))
            self.year_format = '%Y'
            self.year =  str(today.strftime(self.year_format))
            self.date_format = '%d-%m-%y'
            self.date =  str(today.strftime(self.date_format))
            self.timestamp_format = '%d-%m-%y %H:%M'
            self.timestamp =  str(today.strftime(self.timestamp_format))
            self.shell_timestamp_format = '%d_%m_%y-%H_%M'
            self.shell_timestamp =  str(today.strftime(self.shell_timestamp_format))
            self.seconds_timestamp_format = '%d-%m-%y %H:%M.%S'
            self.seconds_timestamp =  str(today.strftime(self.seconds_timestamp_format))
            self.shell_seconds_timestamp_format = '%d_%m_%y-%H_%M.%S'
            self.shell_seconds_timestamp =  str(today.strftime(self.shell_seconds_timestamp_format))
            self.time = self.hour + ":" + self.minute
        def compare(self, comparison=None, current=None, format="%d-%m-%y %H:%M"):
            comparison = self.to_seconds(comparison, format=format)
            current = self.to_seconds(current, format=format)
            if comparison >= current:
                return "future"
            elif comparison <= current:
                return "past"
            elif comparison == current:
                return "present"
            else:
                raise ValueError(f"Unexpected error, comparison seconds: {comparison} current seconds: {current}.")
        def increase(self, string, weeks=0, days=0, hours=0, minutes=0, seconds=0, format="%d-%m-%y %H:%M"):
            seconds += 60*minutes
            seconds += 3600*hours
            seconds += 3600*24*days
            seconds += 3600*24*7*weeks
            s = self.to_seconds(string, format=format)
            s += seconds
            return self.from_seconds(s, format=format)
        def decrease(self, string, weeks=0, days=0, hours=0, minutes=0, seconds=0, format="%d-%m-%y %H:%M"):
            seconds += 60*minutes
            seconds += 3600*hours
            seconds += 3600*24*days
            seconds += 3600*24*7*weeks
            s = self.to_seconds(string, format=format)
            s -= seconds
            return self.from_seconds(s, format=format)
        def to_seconds(self, string, format="%d-%m-%y %H:%M"):
            return time.mktime(datetime.strptime(string, format).timetuple())
            #
        def from_seconds(self, seconds, format="%d-%m-%y %H:%M"):
            return datetime.fromtimestamp(seconds).strftime(format)
            #
        def convert(self, string, input="%d-%m-%y %H:%M", output="%Y%m%d"):
            string = datetime.strptime(string, input)
            return string.strftime(ouput)
        #

    #
    #

# initialized objects.
gfp = Formats.FilePath("")
gdate = Formats.Date()
#