from .dynamo_data_attribute import DynamoDataAttribute


class DynamoDataListAttribute(DynamoDataAttribute, list):
    def __init__(self, datatype, value=None, initialized=True):
        super(DynamoDataListAttribute, self).__init__(datatype, value, initialized)
        self._appended = []
        self._popped = []

    def __repr__(self):
        return self.value.__repr__()

    def __len__(self):
        return len(self.value)

    def __getitem__(self, key):
        return self.value.__getitem__(key)

    def __setitem__(self, key, value):
        dt = self.datatype.datatype # get Set's datatype
        built = dt.build(attr)
        return self.value.__setitem__(key, built)

    def __deltem__(self, key):
        return self.value.__delitem(key) 

    def __contains__(self, i):
        return self.value.__contains__(i)

    def __length_hint__(self):
        return self.value.__length_hint__()

    def __reversed__(self):
        return self.value.__reversed__()

    def get(self):
        return self

    def append(self, attr):
        return self.insert(len(self), attr)

    def remove(self):
        return self.pop(0)

    def index(self, val):
        return self.value.index(val)

    def count(self, val):
        return self.value.count(val)

    def reverse(self):
        return self.value.reverse()

    def copy(self):
        return self.value.copy()

    def sort(self, resverse=False, key=None):
        return self.value.sort(reverse=reverse, key=key)

    def clear(self):
        self._changed = True
        self._popped.extend(self.copy)
        return self.value.clear()

    def extend(self, values):
        built = self.datatype.build(values)
        self._changed = True
        self._appended.extend(built)
        return self.value.extend(built)

    def insert(self, key, attr):
        dt = self.datatype.datatype # get Set's datatype
        built = dt.build(attr)
        self._changed = True
        self._appended.append(built)
        return self.value.insert(key, built)

    def pop(self, key):
        self._changed = True
        popped = self.value.pop(key)
        self._popped.append(pop)
        return popped
