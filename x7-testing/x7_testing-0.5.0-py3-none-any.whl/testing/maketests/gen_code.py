import importlib
import inspect
import sys
from typing import Iterable, Tuple, Union

from x7.lib.inspect_more import item_name
from x7.testing.maketests.mod_support import gen_test_class_name, is_local, mod_tail_join, mod_split
from x7.testing.maketests.outmap import OutputMap
from x7.testing.maketests.parse import parse_module
from x7.testing.maketests.types import OptClass, DictAdded, DictTested, OptStr, Module, ParsedModule, MaketestsError

FILE_HEADER = '''
from unittest import TestCase
from x7.lib.annotations import tests
%s
'''.strip('\n')
CLASS_HEADER_old = ['''
    @classmethod
    def setUpClass(cls):
        pass

    @classmethod
    def tearDownClass(cls):
        pass

    def setUp(self):
        # Once per test
        pass

    def tearDown(self):
        pass
''']
CLASS_HEADER = []


def coverage_gets_confused():
    """A dummy function to call because sometimes branch coverages gets confused"""
    pass


def gen_func(name: str, func: callable, klass: OptClass, added: DictAdded, tested: DictTested) -> OptStr:
    if klass:
        fullname = '.'.join((klass.__module__, klass.__qualname__, name))
        tailname = mod_tail_join(klass.__module__, klass.__qualname__, name)
        tag = item_name(klass)
    else:
        fullname = '.'.join((func.__module__, name))
        tailname = mod_tail_join(func.__module__, name)
        tag = 'module:'+func.__module__
    if fullname in tested:
        return None
    added[fullname] = tag

    out = [
        '    @tests(%s)' % tailname,
        '    def test_%s(self):' % name,
        '        # %s%s' % (name, inspect.signature(func)),
        '        pass  # TODO-impl %s test' % fullname,
    ]
    return '\n'.join(out)


def gen_property(name: str, prop: property, klass: type, added: DictAdded, tested: DictTested) -> OptStr:
    fullname = '.'.join((klass.__module__, klass.__qualname__, name))
    tailname = mod_tail_join(klass.__module__, klass.__qualname__, name)
    tag = item_name(klass)
    if fullname in tested:
        return None
    added[fullname] = tag

    out = [
        '    @tests(%s)' % tailname,
        '    def test_%s(self):' % name,
        '        # value = self.%s' % name if prop.fget else None,
        '        # self.%s = value' % name if prop.fset else None,
        '        # del self.%s' % name if prop.fdel else None,
        '        pass  # TODO-impl %s test' % fullname,
    ]
    return '\n'.join(filter(None, out))


def gen_class(name: str, klass: type, added: DictAdded, tested: DictTested, verbose=False) -> Tuple[str, bool]:
    """
        Generate code to test member functions in <klass>

        Add new classes/functions to <added>, capture existing tests in <tested>.
        Capture any subclasses in <more>.
    """
    out = []
    fullname = item_name(klass)
    tailname = mod_tail_join(klass.__module__, klass.__qualname__)
    isnew = fullname not in tested
    if isnew:
        # No tested funcs passed implies brand-new class
        added[fullname] = 'class'
        out.append('@tests(%s)' % tailname)
        out.append('class %s(TestCase):' % gen_test_class_name(name))
        out.extend(CLASS_HEADER)
    baselen = len(out)
    mod = sys.modules[klass.__module__]
    for member, value in inspect.getmembers(klass):
        if member in ('__class__', '__module__', '__weakref__'):
            pass
        elif inspect.isfunction(value) or inspect.ismethod(value):
            implclass = value.__qualname__.rpartition('.')[0]
            if implclass != klass.__qualname__:
                # Looks like an inherited function, so skip
                if verbose:
                    print('skipping apparently inherited function: %s in %s' % (member, fullname))
                coverage_gets_confused()
                continue
            func_text = gen_func(member, value, klass, added, tested)
            if func_text:
                if len(out) != baselen:
                    out.append('')
                out.append(func_text)
        elif inspect.isclass(value):
            if is_local(value, mod):
                if verbose:
                    print('found class-local class: %s, should already be handled' % item_name(value))
        elif isinstance(value, property):
            if verbose:
                print('.%s: found property: %s' % (member, value))
                func_names = tuple(item_name(f) if f else 'None' for f in (value.fget, value.fset, value.fdel))
                print('   with fget=%s fset=%s fdel=%s' % func_names)
            implclass = value.fget.__qualname__.rpartition('.')[0]
            if implclass != klass.__qualname__:
                # Looks like an inherited function, so skip
                if verbose:
                    print('skipping apparently inherited property: %s in %s' % (member, fullname))
                coverage_gets_confused()
                continue
            func_text = gen_property(member, value, klass, added, tested)
            if func_text:
                if len(out) != baselen:
                    out.append('')
                out.append(func_text)
        else:
            if verbose and not member.startswith('__'):
                print('? gen_class(%s)-what is %s:%s' % (fullname, member, value))
    if len(out) == baselen and isnew:
        out.append('    pass')
    return '\n'.join(out), isnew


def gen_mod_class_test(in_mod: str, dstmap: OutputMap, src: ParsedModule):
    """Generate the TestMod<in_mod> code for stand-alone functions in <in_mod>"""

    out = []
    if in_mod not in dstmap.testmap:
        mod_head, mod_tail = mod_split(in_mod)
        mod_tail_camelcase = ''.join(s.capitalize() for s in mod_tail.split('_'))
        # out.append('')
        # out.append('')
        out.append('@tests(%s)' % mod_tail)
        out.append('class %s(TestCase):' % gen_test_class_name('Mod' + mod_tail_camelcase))
        out.append('    """Tests for stand-alone functions in %s module"""' % in_mod)
    for member_name, f in src.functions.items():
        func_text = gen_func(member_name, f, None, dstmap.added, dstmap.tested)
        if func_text:
            if out:
                out.append('')
            out.append(func_text)
    out = '\n'.join(out)
    return out


def gen_module(inmod: Module, outmod: str, header: str,
               verbose=False, dryrun=False, doprint=False, debug=False):
    # TODO - warn about extraneous tests, i.e. things tested that aren't part of the source file

    in_mod_name = inmod.__name__
    src = parse_module(inmod, verbose, debug)
    test_inputs_found = False
    try:
        import tests.test_inputs
        assert tests.test_inputs        # Flag as used to flake8
        test_inputs_found = True
    except ModuleNotFoundError:
        pass
    if not test_inputs_found:
        print('gen_module: tests.test_inputs module not found.  Make sure you have created this package')
        raise MaketestsError('tests.test_inputs module not found: make sure you have created this package')
    try:
        output_module = importlib.import_module(outmod)
    except ModuleNotFoundError as err:
        if err.name != outmod:
            print('gen_module: Unexpected import error:', err)
            raise
        output_module = None

    dstmap = OutputMap(verbose, debug=debug)
    dstmap.build(output_module or outmod)
    if debug:       # pragma: no cover
        if dstmap.lines:
            print('do_module: lines=%d' % len(dstmap.lines))
            for elem in dstmap.lines:
                print(elem)
        else:
            print('do_module: lines=%s' % dstmap.lines)

    def import_statement(head: str, tail: str):
        return 'from %s import %s' % (head, tail) if head else 'import %s' % tail

    def import_statements(mod_list: Iterable[Union[Module, str]]):
        return '\n'.join(import_statement(*mod_split(m)) for m in sorted(mod_list))

    if dstmap.lines:        # Output module exists, must do special processing
        # Imports we have: dstmap.imports
        # Imports we need: src.required_imports
        if debug:       # pragma: no cover
            print('We have:', dstmap.imports)
            print('We need:', src.required_imports)
        additional = set()
        for required in src.required_imports:
            if mod_split(required) not in dstmap.imports:
                additional.add(required)
        if additional:
            base_line = dstmap.imports[mod_split(in_mod_name)]
            dstmap.lines[base_line].extend([import_statements(additional), '\n'])
            if debug:       # pragma: no cover
                print('Additional:', additional)
                print('Base line:', base_line, dstmap.lines[base_line])
                print(import_statements(additional))

        # Determine insert points for new module functions and new classes
        if in_mod_name not in dstmap.testmap:
            modinsert = len(dstmap.lines)-1
            clsinsert = len(dstmap.lines)-1
        else:
            modinfo = dstmap.classes[dstmap.testmap[in_mod_name]]
            modinsert = modinfo.last
            clsinsert = modinfo.start - 1

        # Handle classes in <in_mod_name> module
        for member_name, c in src.classes.items():
            name = item_name(c)
            class_text, class_is_new = gen_class(member_name, c, dstmap.added, dstmap.tested)
            if class_is_new:
                to_insert = ['>ins_class:%s<\n' % name, class_text, '\n\n\n', '>out_class<\n']
                dstmap.lines[clsinsert].extend(to_insert)
            else:
                if name in dstmap.testmap:
                    tester = dstmap.testmap[name]
                    insert = dstmap.classes[tester].last - 1
                    if class_text:
                        to_insert = ['\n', '>ins_member<\n', class_text, '\n', '>out_member<\n']
                        dstmap.lines[insert].extend(to_insert)
                else:       # pragma: no cover
                    err = "Can't find where to put %s code [%d lines], use TEST_IGNORE?" % (name, class_text.count('\n'))
                    raise MaketestsError(err)

        # Handle plain functions in <in_mod_name> module
        out = gen_mod_class_test(in_mod_name, dstmap, src)
        if out:
            if modinsert >= len(dstmap.lines):
                modinsert = len(dstmap.lines)-1
            if out.startswith('@tests'):
                # Need one extra blank line when inserting new test class
                dstmap.lines[modinsert].extend(['\n'])
            dstmap.lines[modinsert].extend(['>ins:module<\n', '\n', out, '\n', '>out3:module<\n'])

        # print('==== extra funcs ====\n'+out+'==== extra end ====')
        # text = '\n'.join(out)
        # for l in dst.lines:
        #     print(l)
        text = ''.join(l.text() for l in dstmap.lines)
        if debug:       # pragma: no cover
            text = text.replace('\n>ins', '\n#>ins').replace('\n>out', '\n#>out')
        if not dryrun:
            text = ''.join(l for l in text.splitlines(True) if not l.startswith(('>ins', '>out')))

        if verbose:
            print('Classes:')
            for key, csi in dstmap.classes.items():
                print('  %s: %s' % (key, csi))
            print('Testmap:')
            for key, val in dstmap.testmap.items():
                print('  %s: %s' % (key, val))
    else:       # Output module is new
        mod_import = import_statements(src.required_imports)
        out = [header, '', FILE_HEADER % mod_import]
        for member_name, c in src.classes.items():
            class_text, isnew = gen_class(member_name, c, dstmap.added, dstmap.tested)
            out.extend(['', ''])
            out.append(class_text)

        out.append('')
        out.append('')
        out.append(gen_mod_class_test(in_mod_name, dstmap, src))
        text = '\n'.join(out)

    if verbose:
        def print_wide(title: str, d: dict):
            import textwrap
            msg = title + ', '.join(sorted(d.keys()))
            print('\n'.join(textwrap.wrap(msg, 160, subsequent_indent='    ')))

        print_wide('Testmap: ', dstmap.testmap)
        print_wide('Tested: ', dstmap.tested)
        print_wide('Added: ', dstmap.added)
    if dstmap.added:
        print('Items to add:')
        prev = None
        for member_name, t in sorted(dstmap.added.items(), key=lambda v: (v[1].startswith('module:'), v)):
            if t == 'class':
                prev = member_name
                print('    class %s:' % member_name)
            else:
                if t != prev:
                    print('    funcs in', t)
                    prev = t
                print('        %s' % member_name)
    if not text.endswith('\n'):
        text += '\n'
    if dryrun:
        if doprint:
            print(text)

        import unittest.mock
        mock = unittest.mock.MagicMock()

        # Since imports don't really import into globals in exec() below, just mock the required modules
        g = dict(tests=mock)
        for mod in src.required_imports:
            g[mod_split(mod)[1]] = mock
        l = dict()
        # Make sure everything parses
        try:
            exec(text, g, l)
        except Exception as err:
            print('ERROR parsing generated result:', err)
    return text
