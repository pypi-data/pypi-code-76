#
# https://stackoverflow.com/questions/100003/what-are-metaclasses-in-python

def make_hook(f):
  """Decorator to turn 'foo' method into '__foo__'"""
  f._urls = [1]
  return f


class _PatchedType(type):
  def __new__(mcls, name, bases, attrs):
    assert name is not None

    for attrname, attrvalue in attrs.items():
      if getattr(attrvalue, 'is_hook', 0):
        # copy to class
        mcls._urls = []

    return super(_PatchedType, mcls).__new__(mcls, name, bases, {})

  def __init__(cls, name, bases, attrs):
    super(_PatchedType, cls).__init__(name, bases, attrs)

    for p in dir(cls):
      attr = getattr(cls, p)

      if hasattr(attr, '_urls'):


class MyObject(metaclass=_PatchedType):
  pass


class NoneSample(MyObject):
  pass


# Will print "NoneType None"
print('>', type(NoneSample), repr(NoneSample))


class Example(MyObject):
  def __init__(self, value):
    self.value = value

  @make_hook
  def add(self, other):
    return self.__class__(self.value + other.value)


# Will unregister the class
# Example.unregister()

inst = Example(10)
# Will fail with an AttributeError
# inst.unregister()

# print(inst + inst)


class Sibling(MyObject):
  pass


# ExampleSibling = Example + Sibling
# # ExampleSibling is now a subclass of both Example and Sibling (with no
# # content of its own) although it will believe it's called 'AutoClass'
# print(ExampleSibling)
# print(ExampleSibling.__mro__)
