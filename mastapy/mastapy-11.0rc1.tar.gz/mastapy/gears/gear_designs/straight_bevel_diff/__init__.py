'''__init__.py'''


from mastapy._internal.dummy_base_class_importer import _DummyBaseClassImport


with _DummyBaseClassImport():
    from ._890 import StraightBevelDiffGearDesign
    from ._891 import StraightBevelDiffGearMeshDesign
    from ._892 import StraightBevelDiffGearSetDesign
    from ._893 import StraightBevelDiffMeshedGearDesign
