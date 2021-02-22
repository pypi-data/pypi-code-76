'''__init__.py'''


from mastapy._internal.dummy_base_class_importer import _DummyBaseClassImport


with _DummyBaseClassImport():
    from ._1148 import ElementPropertyClass
    from ._1149 import MaterialPropertyClass
