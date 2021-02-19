'''__init__.py'''


from mastapy._internal.dummy_base_class_importer import _DummyBaseClassImport


with _DummyBaseClassImport():
    from ._1200 import KeyedJointDesign
    from ._1201 import KeyTypes
    from ._1202 import KeywayJointHalfDesign
    from ._1203 import NumberOfKeys
