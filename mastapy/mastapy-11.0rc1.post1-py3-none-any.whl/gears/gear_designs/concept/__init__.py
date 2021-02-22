'''__init__.py'''


from mastapy._internal.dummy_base_class_importer import _DummyBaseClassImport


with _DummyBaseClassImport():
    from ._1086 import ConceptGearDesign
    from ._1087 import ConceptGearMeshDesign
    from ._1088 import ConceptGearSetDesign
