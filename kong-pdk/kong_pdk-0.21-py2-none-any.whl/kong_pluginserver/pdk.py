class FakeClasses(object):
    def __init__(self, prefix, call):
        self.prefix = prefix
        self.call = call
    
    def __call__(self, *a):
        return self.call(self.prefix, *a)
    
    # TODO
    def __str__(self):
        return self.call(self.prefix)
    
    def __getattr__(self, k):
        return FakeClasses(self.prefix + "." + k, self.call)

def rpc_of(ch):
    def f(m, *a):
        ch.put({
            "Method": m,
            "Args": a,
        })
        return ch.get()
    return f

class Kong(object):
    def __init__(self, ch):
        self.kong = FakeClasses("kong", self.bridge)
        self.rpc = rpc_of(ch)

    def bridge(self, attr, *args):
        return self.rpc(attr, *args)

def start_server(name, plugin, _version=None, _priority=0):
    import cli
    import sys
    import msgpack
    from .const import PY3K
    from . import PluginServer
    from .server import UnixStreamServer
    from .logger import Logger
    from .module import Module

    args = cli.parse(dedicated=True)

    ps = PluginServer(loglevel=Logger.WARNING - args.verbose)
    ss = UnixStreamServer(ps, args.prefix)
    
    if args.dump:
        ret, err = ps.get_plugin_info(name)
        if err:
            raise Exception("error dump info: " + err)
        if PY3K:
            sys.stdout.buffer.write(msgpack.packb(ret))
        else:
            sys.stdout.write(msgpack.packb(ret))
        sys.exit(0)

    class mod(object):
        Plugin = plugin
        version = _version
        priority = _priority

    mod = Module(name, module=mod)
    ps.plugins[name] = mod
    
    ss.serve_forever()
