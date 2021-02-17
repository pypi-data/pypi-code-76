"""Various testing support routines"""

from __future__ import annotations

import inspect
import os
import pickle
import sys
import zlib
from base64 import b85encode, b85decode
from io import StringIO
from numbers import Number
from typing import Tuple, Optional, TextIO, List, Dict, Any

ModuleType = type(sys)

__all__ = [
    'Capture', 'Argv',
    'RecorderError', 'RecordedDataModule', 'RecordedData',
    'Pickler', 'PicklerExtension', 'PicklerExtensionImage',
    'warn_class',
]

TupleTextIO = Optional[Tuple[TextIO, TextIO]]
TupleStringIO = Optional[Tuple[StringIO, StringIO]]


# noinspection PyUnusedLocal
def unused(*args):
    pass


class Capture(object):
    """
        Usage:
            with Capture() as cap:
                something()
            self.assertIn('important', cap.stdout())
    """

    def __init__(self):
        self.old: TupleTextIO = None
        self.new: TupleStringIO = None

    def __enter__(self):
        self.old = sys.stderr, sys.stdout
        self.new = StringIO(), StringIO()
        sys.stderr, sys.stdout = self.new
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        sys.stderr, sys.stdout = self.old

    def stderr(self):
        return self.new[0].getvalue().strip()

    def stdout(self):
        return self.new[1].getvalue().strip()


class Argv(object):
    """
        Provide context around changing sys.argv.

        Usage:
            with CaptureArgv(['prog', '-whatever', 'you', 'need']):
                something()
    """

    def __init__(self, new_args: Optional[List] = None):
        self.old = None
        self.new = new_args or []

    def __enter__(self):
        self.old = sys.argv
        sys.argv = self.new
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        sys.argv = self.old


class RecorderError(Exception):
    pass


class PicklerExtension:
    """
        Helper object to add more types to Pickler
    """

    def __init__(self, pickler: 'Pickler'):
        self.pickler = pickler
        self.primitives = ()    # Tuple of additional PRIMITIVE types for which repr() & eval() work
        self.types = ()         # Tuple of types handled by do_pickle which need special import/export call

    def do_pickle(self, data, prefix: str):
        """Pickle data and return str if possible, else return None"""
        ...

    def methods(self) -> Dict[str, Any]:
        """
            Return dictionary of functions/values needed to unpickle TYPES + PRIMITIVES
        """
        return dict()


class PicklerExtensionImage(PicklerExtension):
    """
        Helper object to add PIL.Image type to Pickler
    """

    def __init__(self, pickler: 'Pickler'):
        super().__init__(pickler)
        # noinspection PyPackageRequirements
        import PIL.Image
        self.image_module = PIL.Image       # Put module here to avoid any global imports
        # self.primitives = ()      # No additional primitives
        self.types = (self.image_module.Image, )

    def image(self, mode, size, data):
        return self.image_module.frombytes(mode, size, self.pickler.bytes_in(data))

    def methods(self):
        return dict(image=self.image)

    def do_pickle(self, data, prefix: str):
        """Pickle data and return str if possible, else return None"""
        if isinstance(data, self.image_module.Image):
            return 'image(%r, %r, %s)' % (data.mode, data.size, self.pickler.bytes_out(data.tobytes()))
        return None


class Pickler(object):
    """
        Pickler is used to generate a (mostly) human readable dump of an object.
        The output is executable Python code.

        Known types such as int, float, list, tuple, dict are output as repr(object).
        Other types are output as pickled data stored as string.
    """
    # TODO-refine the pickle helper concept.  Images should be added with a helper

    MAX_LINE_LEN = 300
    PRIMITIVES = (str, Number)  # Types that require no recursion and can be output via repr
    # , BBox, Point, Vector, ControlPoint, PenBrush, Transform)

    def __init__(self, extension_classes=()):
        self.prefix = '    '
        if not isinstance(extension_classes, (list, tuple)):
            extension_classes = (extension_classes, )
        self.extension_classes = extension_classes
        self.extensions: List[PicklerExtension] = [klass(self) for klass in extension_classes]
        primitives = set(self.PRIMITIVES)
        for ext in self.extensions:
            primitives.update(ext.primitives)
        self.primitives = tuple(primitives)
        self.vars_for_load()  # Validate names in extensions are unique

    def vars_for_load(self):
        """The dictionary of values used during load/eval()"""

        local_funcs = dict(
            pickled=self.pickled,
        )
        all_funcs = [local_funcs] + [ext.methods() for ext in self.extensions]
        all_names = [n for d in all_funcs for n in d.keys()]
        if len(all_names) != len(set(all_names)):
            sorted_names = sorted(all_names)
            dups = ', '.join(a for a, b in zip(sorted_names, sorted_names[1:]) if a == b)
            raise ValueError('duplicate function names: %s' % dups)
        values = dict((n, v) for d in all_funcs for n, v in d.items())
        return values

    def load(self, in_file):
        """Load from a .td file"""
        eval_globals = self.vars_for_load()
        data = eval(in_file.read(), eval_globals)
        return data

    def bytes_out(self, data: bytes):
        out = b85encode(zlib.compress(data)).decode('utf-8')
        return '\n        '.join(repr(out[idx: idx + self.MAX_LINE_LEN]) for idx in range(0, len(out), self.MAX_LINE_LEN))

    @staticmethod
    def bytes_in(data: str):
        return zlib.decompress(b85decode(data))

    def obj_out(self, data: Any) -> str:
        """Generate the Python code for the compressed, utf-8 encoded, pickled version of data"""
        return self.bytes_out(pickle.dumps(data))

    def obj_in(self, data: str) -> Any:
        """Reverse obj_out and return original object"""
        return pickle.loads(self.bytes_in(data))

    def pickled(self, kind, data):
        """Used at load time to handled pickled objects"""
        unused(kind)
        return self.obj_in(data)

    def is_simple(self, data):
        if isinstance(data, self.primitives):
            return True
        if isinstance(data, (tuple, list)):
            return all(map(self.is_simple, data))
        if isinstance(data, dict):
            return self.is_simple(list(data.items()))
        return False

    def do_pickle_dict(self, data, prefix):
        out = []
        for k, v in sorted(data.items()):
            out.append('%s%r: %s,' % (prefix, k, self.do_pickle(v, prefix + self.prefix)))
        return '{\n%s\n}' % '\n'.join(out)

    def do_pickle_extensions(self, data, prefix):
        """Iterate over extensions to see if this data fits any of them"""
        for extension in self.extensions:
            if handled := extension.do_pickle(data, prefix):
                return handled
        return None

    # noinspection PyMethodMayBeStatic
    def do_pickle_helper_anim(self, data, prefix):
        if True:
            class Elem:
                def dump(self, *args): ...

            class DumpContext:
                def __init__(self, **kwargs): ...
                def output(self, **kwargs) -> str: ...
                def append(self, *args, **kwargs): ...
                def add_comma(self, *args, **kwargs): ...

        if isinstance(data, Elem):
            dc = DumpContext(use_vars=False)
            dc.depth = len(prefix) // 4
            data.dump(dc)
            return dc.output(just_lines=True).lstrip()
        elif isinstance(data, list) and all(isinstance(d, Elem) for d in data):
            dc = DumpContext(use_vars=False)
            dc.append('[')
            dc.depth = len(prefix) // 4 + 1
            for e in data:
                e.dump(dc)
                dc.add_comma()
            dc.depth = 0
            dc.append('%s]' % prefix)
            return dc.output(just_lines=True)
        else:
            return None

    def do_pickle(self, data, prefix):
        if self.is_simple(data):
            return repr(data)
        elif isinstance(data, dict) and self.is_simple(list(data.keys())):
            return self.do_pickle_dict(data, prefix + self.prefix)
        elif extended := self.do_pickle_extensions(data, prefix):
            return extended
        else:
            return 'pickled(%r, %s)' % (type(data).__name__, self.obj_out(data))

    def dump_dict(self, data: dict, out_file):
        out_file.write('{\n')
        for k, v in sorted(data.items()):
            out_file.write('   %r: %s,\n' % (k, self.do_pickle(v, self.prefix)))
        out_file.write('}\n')


class RecordedDataModule(object):
    """Holder for recorded test data for single module"""
    # TODO-validate that each item was used
    # TODO-delete unused items if save mode is True
    def __init__(self, mod: str, pickler: Pickler):
        self.mod = mod
        self.pickler = pickler
        self.module: ModuleType = sys.modules[self.mod]
        self.modified = False
        self.new = False
        self.data: Dict[str, Any] = {}
        self.load()

    def file_name(self):
        return inspect.getsourcefile(self.module).replace('.py', '.td')

    @staticmethod
    def _key(cls, func, case):
        return '%s.%s:%s' % (cls.__qualname__, func, case)

    def load(self):
        fn = self.file_name()
        if os.path.exists(fn):
            with open(fn, 'rt') as in_file:
                self.data = self.pickler.load(in_file)
        else:
            print('Warning: %s: %s does not exist' % (self.mod, fn), file=sys.stderr)
            self.data = {}
            self.new = True

    def save(self):
        if self.modified:
            fn = self.file_name()
            with open(fn, 'wt') as out_file:
                out_file.write('# noinspection SpellCheckingInspection,PyUnresolvedReferences,PyStatementEffect\n')
                self.pickler.dump_dict(self.data, out_file)
            print('%s:1: saved %d records to %s' % (self.module.__file__, len(self.data), fn))
            self.modified = False

    def get(self, cls, func: str, case: str):
        key = self._key(cls, func, case)
        gotten = self.data.get(key, RecordedData.NONE)
        return gotten
        # return self.data.get(self._key(cls, func, case), RecordedData.NONE)

    def put(self, cls, func: str, case: str, new_data, patch=False):
        """Store data and set .changed=True unless patch=True"""
        # Validate that new_data is picklable
        key = self._key(cls, func, case)
        try:
            pickle.dumps(new_data)
        except Exception as err:
            raise RecorderError('%s: Cannot pickle %r\n%s' % (key, new_data, err)) from err
        self.data[key] = new_data
        if not patch:
            self.modified = True


class RecordedData(object):
    """Holder for recorded test data"""

    NONE = object()     # Unique value for testing
    data: Dict[str, RecordedDataModule] = {}
    setup_done = False

    @classmethod
    def setup(cls, mod: str, pickler: Pickler):
        """Setup once for module"""
        cls.get_mod(mod, pickler)
        if not cls.setup_done:
            cls.setup_done = True

    @classmethod
    def get_mod(cls, mod: str, pickler: Optional[Pickler] = None):
        """Load data for mod"""
        if mod not in cls.data:
            if pickler is None:
                raise ValueError('pickler is required for initial get_mod')
            cls.data[mod] = RecordedDataModule(mod, pickler)
        return cls.data[mod]

    @classmethod
    def save_modules(cls):
        """Save each modified module"""
        for name, mod_data in cls.data.items():
            mod_data.save()

    @classmethod
    def get(cls, klass, func: str, case: str):
        return cls.get_mod(klass.__module__).get(klass, func, case)

    @classmethod
    def put(cls, klass, func: str, case: str, new_data, patch=False):
        return cls.get_mod(klass.__module__).put(klass, func, case, new_data, patch)


def warn_class(klass: type, message):
    """Issue a warning directed at a class, not the line of code issuing the warning."""
    modname = klass.__module__
    module = sys.modules[modname]
    filename = module.__file__
    lineno = inspect.findsource(klass)[1] + 1
    print('%s:%d: Warning: %s: %s' % (filename, lineno, klass.__qualname__, message))
