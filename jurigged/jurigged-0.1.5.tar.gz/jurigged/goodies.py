from .register import registry


def test(x):
    return x * x * x


def develop(fn, registry=registry):
    @registry.activity.register
    def reload(_):
        print(fn())

    def stop():
        registry.activity.remove(reload)

    reload(None)
    return stop
