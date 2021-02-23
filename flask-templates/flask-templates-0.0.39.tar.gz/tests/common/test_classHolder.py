from unittest import TestCase
from flask_templates.common.class_holder import class_register, ClassHolder, class_getter


def a(self):
    return 123


class A:
    pass


@class_register()
class B(A):
    def __init__(self):
        pass


@class_register()
class C:

    @property
    @class_getter(A)
    def cc(self):
        pass

    def __init__(self):
        self.c = "123"


class TestClassHolder(TestCase):

    def test_put(self):
        c = ClassHolder().get(C)
        print(c)
        c2 = C()
        print(c2)
        c3 = ClassHolder().get(C)
        print(c3)