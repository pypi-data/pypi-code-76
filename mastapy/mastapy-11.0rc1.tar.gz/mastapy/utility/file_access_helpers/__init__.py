'''__init__.py'''


from mastapy._internal.dummy_base_class_importer import _DummyBaseClassImport


with _DummyBaseClassImport():
    from ._1545 import ColumnTitle
    from ._1546 import TextFileDelimiterOptions
