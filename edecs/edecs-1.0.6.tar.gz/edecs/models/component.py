import json


class Component():
    '''Base component class'''

    defaults = {}

    @property
    def initialized(self):
        return self.entity is not None


    def __init__(self, comp_type=None, **properties):
        self.type = comp_type or type(self).__name__
        self.id = None
        self.entity = None

        if self.defaults == {}:
            for key, value in properties.items():
                self.defaults[key] = value

        for key, value in self.defaults.items():
            setattr(self, key, properties.pop(key, value))

    def __repr__(self):
        # <Component:type; Enity:entity>
        return "<Component: {}; Entity: {}>".format(self.type,
                                            self.entity if self.entity is None
                                                        else self.entity.type)

    def __str__(self):
        # JSON
        comp_str = "<Component: {}; Entity: {}>\n".format(self.type,
                                            self.entity if self.entity is None
                                                        else self.entity.type)

        keys = self.defaults.keys()
        data = {}

        for key in keys:
            data[key] = getattr(self, key)

        json_string = json.dumps(data, indent=4)
        return comp_str + json_string
