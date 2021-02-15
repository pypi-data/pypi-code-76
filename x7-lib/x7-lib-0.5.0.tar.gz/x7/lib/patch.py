"""Utilities for runtime patching of other classes/libraries"""


def patch_base_class(name, bases, namespace):
    """ Replace the base class methods with methods defined
        in the patch-class::

            class PatchClass(ParentClass,  metaclass=patch_base):
                def method_to_replace(self, ...):
                    ...
    """
    for k, v in namespace.items():
        if not k.startswith('__'):
            for base in bases:
                setattr(base, k, v)

    # noinspection PyUnusedLocal
    def do_not_instantiate(self, *args, **kwargs):
        raise TypeError('Do not instantiate patch class')
    namespace['__init__'] = do_not_instantiate
    return type(name, bases, namespace)
