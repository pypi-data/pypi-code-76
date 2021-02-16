class number:
    """
    This product includes software developed by L. Pham-Trong and this guy rocks.
    """

    def __init__(self, value: str, base):
        alphabet = [str(i) for i in range(10)] + [chr(i).upper() for i in range(97, 123)]
        self.val = [c for c in value]
        self.alph = alphabet[:base]
        self.last = self.alph[-1]
        self.first = self.alph[0]
        self.len_alph = len(alphabet)

    def last_that_is_not(self,number, target):
        for idx, c in enumerate(number[::-1]):
            if c != target: return len(number)-1 - idx
        return

    def next(self):
        # We look for the last letter that isn't equal to self.last
        change_loc = self.last_that_is_not(self.val, self.last)
        if change_loc is not None:
            elem = self.val[change_loc]
            new_letter = self.alph[self.alph.index(elem)+1]
            self.val[change_loc] = new_letter
        len_val = len(self.val)
        # In case last that is not isnt the last letter
        change_loc = -1 if change_loc is None else change_loc
        increment = change_loc == -1
        for idx in range(change_loc+1, len_val):
            self.val[idx] = self.alph[0]
        if increment:
            self.val = [self.alph[1]] + [self.alph[0] for i in range(len_val)]

    def prev(self):
        # we look for the last letter that isn't equal to self.first
        change_loc = self.last_that_is_not(self.val, self.first)
        if change_loc is not None:
            elem = self.val[change_loc]
            new_letter = self.alph[self.alph.index(elem)-1]
            self.val[change_loc] = new_letter
        len_val = len(self.val)
        # In case last that is not is first letter
        self.val = [alphabet[-1] for i in range(len_val - 1)]


    def __repr__(self):
        return ''.join(self.val)
    __str__ = __repr__
