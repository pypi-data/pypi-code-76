from .world import world


class Entity():
    '''Base entity class'''

    __slots__ = ['type', 'id', 'components', 'initialized']

    default_components = {}


    def __init__(self, ent_type=None, **default_components):
        self.type = ent_type or type(self).__name__
        self.id = None
        self.initialized = False
        self.components = {}

        if self.default_components == {}:
            for key, value in default_components.items():
                self.default_components[key] = value

    def __repr__(self):
        return "<Entity {}: {}>".format(self.id, self.type)

    def __str__(self):
        ent = "<Entity {}: {}>".format(self.id, self.type)
        components = self.components
        # TO DO: return repr of component
        # repr(component)
        return "{}\n{}".format(ent, components)

    def __getitem__(self, key):
        return world.get_component(self, key)

    def __setitem__(self, key, value):
        world.add_component(self, key, value)

    def __delitem__(self, key):
        world.delete_component(self.components[key])

    def __getattr__(self, key):
        if key in super().__getattribute__('__slots__') + ['default_components']:
            return super().__getattr__(key)
        else:
            return world.get_component(self, key)

    def __setattr__(self, key, value):
        if key in super().__getattribute__('__slots__') + ['default_components']:
            super().__setattr__(key, value)
        else:
            world.add_component(self, key, value)

    def __delattr__(self, key):
        world.delete_component(self.components[key])
