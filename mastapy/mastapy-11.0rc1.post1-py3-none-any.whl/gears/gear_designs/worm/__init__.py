'''__init__.py'''


from mastapy._internal.dummy_base_class_importer import _DummyBaseClassImport


with _DummyBaseClassImport():
    from ._885 import WormDesign
    from ._886 import WormGearDesign
    from ._887 import WormGearMeshDesign
    from ._888 import WormGearSetDesign
    from ._889 import WormWheelDesign
