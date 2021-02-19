'''__init__.py'''


from mastapy._internal.dummy_base_class_importer import _DummyBaseClassImport


with _DummyBaseClassImport():
    from ._894 import StraightBevelGearDesign
    from ._895 import StraightBevelGearMeshDesign
    from ._896 import StraightBevelGearSetDesign
    from ._897 import StraightBevelMeshedGearDesign
