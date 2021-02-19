import collections


class OrderedSet(collections.MutableSet):
    def __init__(self, iterable=None):
        """
        Set that remembers original insertion order. The purpose of using this
        class is to ensure stable str or repr output for unittest comparison.

        The equality test and hash codes are order independent.

        Implementation based on a doubly linked link and an internal dictionary.
        This design gives OrderedSet the same big-Oh running times as regular sets
        including O(1) adds, removes, and lookups as well as O(n) iteration.

        See: https://code.activestate.com/recipes/576694/
        """
        self.frozen = False
        self._hash_code = None
        self.end = end = []
        end += [None, end, end]  # sentinel node for doubly linked list
        self.map = {}  # key --> [key, prev, next]
        if iterable is not None:
            self |= iterable

    def freeze(self):
        """
        Freezes this object so that no further modification is allowed.
        Afterwards, you can get its hash code and also you can use it as a key in dict.
        """
        self.frozen = True

    def __len__(self):
        return len(self.map)

    def __contains__(self, key):
        return key in self.map

    def add(self, key):
        if self.frozen:
            raise RuntimeError("Cannot modify a frozen OrderedSet.")
        if key not in self.map:
            end = self.end
            curr = end[1]
            curr[2] = end[1] = self.map[key] = [key, curr, end]

    def discard(self, key):
        if self.frozen:
            raise RuntimeError("Cannot modify a frozen OrderedSet.")
        if key in self.map:
            key, prev, next = self.map.pop(key)
            prev[2] = next
            next[1] = prev

    def __iter__(self):
        end = self.end
        curr = end[2]
        while curr is not end:
            yield curr[0]
            curr = curr[2]

    def __reversed__(self):
        end = self.end
        curr = end[1]
        while curr is not end:
            yield curr[0]
            curr = curr[1]

    def pop(self, last=True):
        if self.frozen:
            raise RuntimeError("Cannot modify a frozen OrderedSet.")
        if not self:
            raise KeyError("set is empty")
        key = self.end[1][0] if last else self.end[2][0]
        self.discard(key)
        return key

    def __repr__(self):
        if not self:
            return "%s()" % (self.__class__.__name__,)
        return "%s(%r)" % (self.__class__.__name__, list(self))

    def __eq__(self, other):
        """
        Two OrderedSet are considered equal if the set of keys are the same irregardless of the insert order.
        """
        return (
            isinstance(other, OrderedSet)
            and len(self) == len(other)
            and set(self) == set(other)
        )

    def __ne__(self, other):
        return not self.__eq__(other)

    def __hash__(self):
        """
        Hashcode is generated irregardless of the insert order.
        """
        if not self.frozen:
            raise RuntimeError("Cannot hash an unfrozen OrderedSet.")
        if not self._hash_code:
            self._hash_code = hash(frozenset(self))
        return self._hash_code


if __name__ == "__main__":
    s = OrderedSet("abracadaba")
    t = OrderedSet("simsalabim")
    print(s | t)
    print(s & t)
    print(s - t)
