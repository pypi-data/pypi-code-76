
def say_hello(name=None):
    if type(name) == int:
        name = str(name)
    if name is None:
        return "Hello, World!"
    else:
        return f"Hello, {name}!"