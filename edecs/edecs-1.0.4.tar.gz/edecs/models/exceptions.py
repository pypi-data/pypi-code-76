class EntityAlreadyExists(Exception):

    def __init__(self, entity):
        self.entity = entity

    def __str__(self):
        return "Entity {} already exist".format(self.entity)

class EntityDoesNotExist(Exception):

    def __init__(self, entity):
        self.entity = entity

    def __str__(self):
        return "Entity {} does not exist in world".format(self.entity)

class ComponentAlreadyHaveEntity(Exception):

    def __init__(self, component):
        self.component = component

    def __str__(self):
        return "Component {} already have entity {}".format(self.component,
                                                        self.component.entity)

class ComponentHasNoEntity(Exception):

    def __init__(self, component):
        self.component = component

    def __str__(self):
        return "Component {} has no entity".format(self.component)

class SystemTypeAlreadyExists(Exception):

    def __init__(self, system):
        self.system = system

    def __str__(self):
        return "System type {} already exists".format(self.system.type)

class SystemAlreadyInitialized(Exception):

    def __init__(self, system):
        self.system = system

    def __str__(self):
        return "System {} already initialized".format(self.system)

class SystemDoesNotExist(Exception):

    def __init__(self, system):
        self.system = system

    def __str__(self):
        return "System {} does not exist in world".format(self.system)

class SystemIsNotInitialized(Exception):

    def __init__(self, system):
        self.system = system

    def __str__(self):
        return "System {} is not initialized".format(self.system)
