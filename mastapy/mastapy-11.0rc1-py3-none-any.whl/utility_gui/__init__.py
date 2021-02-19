'''__init__.py'''


from mastapy._internal.dummy_base_class_importer import _DummyBaseClassImport


with _DummyBaseClassImport():
    from ._1571 import ColumnInputOptions
    from ._1572 import DataInputFileOptions
