import abc
from inspect import isclass


class CompressibleObject(abc.ABC):
    """Abstract case class for dict values that can be compressed and decompressed."""

    def compress(self, o):
        pass

    def decompress(self, o):
        pass

    def __str__(self):
        return self.__class__.__name__


class JSONKeyPress(CompressibleObject):
    """Class to keep data for compression and decompression of dictionary keys."""
    KEY_ALPHABET = [chr(x) for x in list(range(65, 91)) + list(range(97, 123))]

    def _short_key(self, idx):
        """Returns the shortened version of a key given its index using the short key alphabet"""
        kc = self.KEY_ALPHABET
        if idx > len(kc):
            return self._short_key(idx // len(kc)) + kc[idx % len(kc)]
        else:
            return kc[idx]

    class KeyPair:
        """Combines a short and a long key, only used for pretty printing."""

        def __init__(self, short, long):
            self.short = short
            self.long = long

        def __hash__(self):
            return hash(self.long)

        def __str__(self):
            return "(" + str(self.short) + " <-- " + str(self.long) + ")"

        def __repr__(self):
            return str(self)

    class Data:
        def __init__(self, parent, compressed, decompressed):
            self.parent = parent
            self._compressed = compressed
            self._decompressed = decompressed

        def _compress(self):
            if not self._compressed:
                self._compressed = self.parent.compress(self._decompressed)
            return self._compressed

        def _decompress(self):
            if not self._decompressed:
                self._decompressed = self.parent.decompress(self._compressed)
            return self._decompressed

        def get_compressed(self):
            self._compress()
            return self._compressed
        def get_decompressed(self):
            self._decompress()

            return self._decompressed

    def __call__(self, compressed: dict = None, decompressed: dict = None):
        return self.Data(parent=self, compressed=compressed, decompressed=decompressed)

    def __init__(self, schema, alphabet=None):
        if alphabet:
            self.KEY_ALPHABET = alphabet
        self.schema = schema
        # self.short_keyed = self._extract_keys(self.schema)
        self._short_keyed, self._long_keyed, self._paired_keys = self._extract_keys(self.schema)

    def _extract_keys(self, o):
        """Extracts a nested list of keys from a json schema."""
        short, long, pairs = {}, {}, {}
        if isclass(o) and issubclass(o, CompressibleObject):
            # Value is of compressible type
            return o, o, o
        elif isinstance(o, list):
            # Value is a list of values
            if len(o) == 1:
                # Exactly one element in the list
                s, l, p = self._extract_keys(o[0])
                return [s], [l], [p]
            else:
                # List has more than one element: Not supported
                raise ValueError("In a json schema lists must have exactly one item that is a "
                                 "dictionary, a nested list, or some other value.")
        if not isinstance(o, dict):
            # Value is not of compressible type
            return None, None, None

        for i, (k, v) in enumerate(o.items()):
            s, l, p = self._extract_keys(v)
            sk, lk = self._short_key(i), k
            short.update({sk: (lk, s)})
            long.update({lk: (sk, l)})
            pairs.update({self.KeyPair(sk, lk): p})

        return short, long, pairs

    def compress(self, o: dict):
        """Convert a dict with long keys to short keys"""
        return self._convert_to_other(data=o, parent=self._long_keyed, compress=True)

    def decompress(self, o: dict):
        """Convert a dict with short keys to long keys"""
        return self._convert_to_other(data=o, parent=self._short_keyed, compress=False)

    def _convert_to_other(self, data, parent, compress):
        res = {}
        if isinstance(data, dict):
            for k, v in data.items():
                if k in parent:
                    other, sub = parent[k]
                    res.update({other: self._convert_to_other(data=v, parent=sub, compress=compress)})
                else:
                    raise ValueError("The key " + k + " is not part of the schema. Dict contents: " + str(parent))
            return res
        elif isclass(parent) and issubclass(parent, CompressibleObject):
            if compress:
                return parent.compress(parent, data)
            else:
                return parent.decompress(parent, data)
        else:
            return data
