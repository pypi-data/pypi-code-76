"""
Bidirectional Unique Dictionary, inspired by
https://stackoverflow.com/questions/3318625/how-to-implement-an-efficient-bidirectional-hash-table
"""


class BidirectionalUniqueDictionary(dict):
    """Bidirectional dictionary that requires that each mapping be unique"""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.inverse = {}
        for key, value in self.items():
            if value in self.inverse:
                raise ValueError('Reverse mapping is not unique for %s' % repr(value))
            self.inverse[value] = key

    def __setitem__(self, key, value):
        if key in self:
            self_val = self[key]
            if self_val != value:   # if self_val==value, this is overwriting, so let it happen
                if value in self.inverse:
                    raise ValueError('Reverse mapping is not unique for %s' % repr(value))
            del self.inverse[self_val]
        else:
            if value in self.inverse:
                raise ValueError('Reverse mapping is not unique for %s' % repr(value))
        super().__setitem__(key, value)
        self.inverse[value] = key

    def __delitem__(self, key):
        del self.inverse[self[key]]
        super().__delitem__(key)
