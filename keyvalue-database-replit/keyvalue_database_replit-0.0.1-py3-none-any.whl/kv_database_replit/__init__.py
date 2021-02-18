import os, importlib

class DataBase:
  def exist(self): return os.path.isfile(self.path)

  def create(self):
    try:
      file = open(self.path, "w+")
      file.write("DataBase = {}")
      file.close()
    except FileNotFoundError as ex:
      print(ex)
      
  def load(self):
    try:
      db = importlib.import_module(self.path[:-3])
      self.db = db.DataBase
    except ImportError as ex:
      print(ex)

  def __init__(self, path =''):
    self.auto = False
    self.path = path + ".py"
    if self.exist(): self.load()
    else: self.create()
   
  def get(self, key): return self.db[key]
  def isfound(self, key): return (key in self.db)
  def keys(self): return self.db.keys()
  def values(self): return self.db.values()

  def save(self):
    file = open(self.path, "w+")
    file.write("DataBase = ")
    file.write(str(self.db))
    file.close()

  def add(self, key, value):
    try:
      if self.db.get(key):
        raise KeyError("The key is already found in the database, you may use the change method to override it.")
        return
      self.db[key] = value
      if self.auto: self.save()

    except KeyError as msg: print(msg)

  def change(self, key, new_value):
    try:
      if not self.isfound(key):
        raise KeyError("The key is not found in the database, you may add it using add_key method.")
        return
      self.db[key] = new_value
      if self.auto: self.save()

    except KeyError as msg: print(msg)
    
  def delete(self, key):
    try:
      if not self.isfound(key):
        raise KeyError("The key is not found in the database, you may add it using add_key method.")
        return
      del self.db[key]
      if self.auto: self.save()
    except KeyError as msg: print(msg)

  def clear_all(self):
    self.db = {}
    if self.auto: self.save()


  def delete_this_database(self):
    try:
      os.remove(self.path)
      print(f"The DataBase {self.path} has been deleted.")
    except FileNotFoundError as msg:
      raise FileNotFoundError(msg)

  def enable_autosave(self): self.auto = True
  def disable_autosave(self): self.auto = False

  def __str__(self):
    return "<Key-Value DataBase: " + str(len(self.db)) + " row(s)>"