# OPBOT - pure python3 IRC bot (op/hdl.py)
#
# This file is placed in the Public Domain.

"handler"

# imports

import inspect, os, queue, sys, threading, time
import logging

from .obj import Cfg, Default, Object, Ol, get, update
from .prs import parse
from .thr import launch
from .utl import direct, has_mod, locked, spl

import _thread

# defines

def __dir__():
    return ("Bus", "Core", "CoreBus", "Console", "Command", "Event", "Handler", "cmd")

loadlock = _thread.allocate_lock()

# classes

class Bus(Object):

    objs = []

    def __call__(self, *args, **kwargs):
        return Bus.objs

    def __iter__(self):
        return iter(Bus.objs)

    @staticmethod
    def add(obj):
        Bus.objs.append(obj)

    @staticmethod
    def announce(txt, skip=None):
        for h in Bus.objs:
            if skip is not None and isinstance(h, skip):
                continue
            if "announce" in dir(h):
                h.announce(txt)

    @staticmethod
    def by_orig(orig):
        for o in Bus.objs:
            if repr(o) == orig:
                return o

    @staticmethod
    def say(orig, channel, txt):
        for o in Bus.objs:
            if repr(o) == orig:
                o.say(channel, str(txt))

class Event(Default):

    __slots__ = ("prs", "src")

    def __init__(self, *args, **kw):
        super().__init__(*args, **kw)
        self.channel = ""
        self.done = threading.Event()
        self.orig = None
        self.prs = Default()
        self.result = []
        self.thrs = []
        self.type = "event"

    def direct(self, txt):
        Bus.say(self.orig, self.channel, txt)

    def parse(self):
        parse(self.prs, self.otxt or self.txt)
        args = self.prs.txt.split()
        if args:
            self.cmd = args.pop(0)
        if args:
            self.args = list(args)
            self.rest = " ".join(self.args)
            self.otype = args.pop(0)
        if args:
            self.xargs = args

    def ready(self):
        self.done.set()

    def reply(self, txt):
        self.result.append(txt)

    def show(self):
        for txt in self.result:
            self.direct(txt)

    def wait(self, timeout=1.0):
        self.done.wait(timeout)
        for thr in self.thrs:
            thr.join()

class Command(Event):

    def __init__(self, txt, **kwargs):
        super().__init__([], **kwargs)
        self.type = "cmd"
        if txt:
            self.txt = txt.rstrip()

class Handler(Object):

    threaded = False

    pkgnames = Object()

    def __init__(self):
        super().__init__()
        self.cbs = Object()
        self.cfg = Cfg()
        self.cmds = Object()
        self.modnames = Object()
        self.names = Ol()
        self.pkgs = []
        self.queue = queue.Queue()
        self.started = []
        self.stopped = False
        self.table = Object()
        self.tablename = "op.tbl"

    def add(self, cmd, func):
        self.cmds[cmd] = func

    def announce(self, txt):
        self.direct(txt)

    def clone(self, hdl):
        update(self.cmds, hdl.cmds)
        update(self.cbs, hdl.cbs)
        update(self.modnames, hdl.modnames)
        update(self.names, hdl.names)
        update(self.pkgnames, hdl.pkgnames)
        self.pkgs = hdl.pkgs
        self.table = hdl.table

    def cmd(self, txt):
        self.register("cmd", cmd)
        c = Command(txt)
        c.orig = repr(self)
        cmd(self, c)
        c.wait()

    def direct(self, txt):
        pass

    def dispatch(self, event):
        if event.type and event.type in self.cbs:
            self.cbs[event.type](self, event)

    def fromdir(self, pkgpath, name=""):
        if not pkgpath:
            return
        if not os.path.exists(pkgpath):
            return
        path, _n = os.path.split(pkgpath)
        sys.path.insert(0, path)
        if not name:
            name = pkgpath.split(os.sep)[-1]
        if not has_mod(name):
            return
        mod = direct(name)
        for mn in [x[:-3] for x in os.listdir(pkgpath)
                   if x and x.endswith(".py")
                   and not x.startswith("__")
                   and not x == "setup.py"]:
            fqn = "%s.%s" % (name, mn)
            if not has_mod(fqn):
                continue
            mod = self.load(fqn)
            self.intro(mod)

    def get_cmd(self, cmd):
        if not self.modnames:
            try:
                mod = direct(self.tablename)
                update(self.modnames, mod.modnames)
            except ImportError:
                pass
        if cmd not in self.cmds:
            mn = get(self.modnames, cmd, None)
            if mn:
                self.load(mn)
        return get(self.cmds, cmd, None)

    def get_mod(self, mn):
        if mn in self.table:
            return self.table[mn]

    def get_names(self, nm):
        if not self.names:
            try:
                mod = direct(self.tablename)
                update(self.names, mod.names)
            except ImportError:
                pass
        return get(self.names, nm, [nm,])

    def init(self, mns):
        thrs = []
        for mn in spl(mns):
            mn = get(self.pkgnames, mn, mn)
            mod = self.get_mod(mn)
            if mod and "init" in dir(mod):
                thrs.append(launch(mod.init, self))
        return thrs

    def input(self):
        while not self.stopped:
            try:
                e = self.poll()
            except EOFError:
                break
            self.put(e)
            e.wait()

    def intro(self, mod):
        fqn = mod.__name__
        mn = fqn.split(".")[-1]
        self.pkgnames[mn] = fqn
        for key, o in inspect.getmembers(mod, inspect.isfunction):
            if o.__code__.co_argcount == 1:
                if o.__code__.co_varnames[0] == "obj":
                    self.register(key, o)
                elif o.__code__.co_varnames[0] == "event":
                    self.cmds[key] = o
                    self.modnames[key] = o.__module__
        for _key, o in inspect.getmembers(mod, inspect.isclass):
            if issubclass(o, Object):
                t = "%s.%s" % (o.__module__, o.__name__)
                if o.__name__.lower() not in self.names:
                    self.names.append(o.__name__.lower(), t)

    @locked(loadlock)
    def load(self, mn):
        self.table[mn] = direct(mn)
        for key, o in inspect.getmembers(self.table[mn], inspect.isfunction):
            if o.__code__.co_argcount == 1:
                if o.__code__.co_varnames[0] == "obj":
                    self.register(key, o)
                elif o.__code__.co_varnames[0] == "event":
                    self.cmds[key] = o
        return self.table[mn]

    def load_mod(self, mns):
        if not self.pkgnames:
            try:
                mod = direct(self.tablename)
                update(self.pkgnames, mod.pkgnames)
            except ImportError:
                pass
        for mn in spl(mns):
            mn = get(self.pkgnames, mn, mn)
            self.load(mn)

    def handler(self):
        self.running = True
        while not self.stopped:
            e = self.queue.get()
            if not e:
                break
            if not e.orig:
                e.orig = repr(self)
            e.thrs.append(launch(self.dispatch, e))

    def put(self, e):
        self.queue.put_nowait(e)

    def register(self, name, callback):
        self.cbs[name] = callback

    def say(self, channel, txt):
        self.direct(txt)

    def start(self, pkgnames=None):
        launch(self.handler)

    def stop(self):
        self.stopped = True
        self.queue.put(None)

    def walk(self, pkgnames):
        for pn in spl(pkgnames):
            if not has_mod(pn):
                continue
            mod = direct(pn)
            if "__file__" in dir(mod) and mod.__file__:
                p = os.path.dirname(mod.__file__)
            else:
                p = list(mod.__path__)[0]
            self.fromdir(p, pn)

    def wait(self):
        while not self.stopped:
            time.sleep(30.0)

class Core(Handler):

    def __init__(self):
        super().__init__()
        self.register("cmd", cmd)

class BusCore(Core):

    def __init__(self):
        super().__init__()
        Bus.add(self)

class Console(BusCore):

    def direct(self, txt):
        pass

    def poll(self):
        return Command(input("> "))

    def start(self):
        super().start()
        launch(self.input)

# functions

def cmd(handler, obj):
    obj.parse()
    res = None
    f = handler.get_cmd(obj.cmd)
    if f:
        res = f(obj)
        obj.show()
    obj.ready()
    return res
