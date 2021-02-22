'''__init__.py'''


from mastapy._internal.dummy_base_class_importer import _DummyBaseClassImport


with _DummyBaseClassImport():
    from ._480 import DIN3990GearSingleFlankRating
    from ._481 import DIN3990MeshSingleFlankRating
