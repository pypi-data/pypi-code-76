class DynamoDataAttribute(object):
    def __init__(self, datatype, value=None, initialized=True):
        """initialize the DynamoDataAttribute

        This class stores the current value of the attribute on
        the model and some extra metadata about the attribute itself
        datatype - the Datatype of the corresponding Model attribute
        value - the current value
        initialized - if this attribute was included when the Model
            was instantiated
        _changed - has the set() method be called

        initialized / _changed help determine what attributes to include
        in the model.put() and model.update()

        value is built using datatype.build() to handle default values
        """
        self.datatype = datatype
        self.value = self.datatype.build(value)
        self.initialized = initialized
        self._changed = False

    def get(self):
        return self.value

    def set(self, newvalue):
        self._changed = True
        self.value = newvalue
