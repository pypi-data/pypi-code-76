'''__init__.py'''


from mastapy._internal.dummy_base_class_importer import _DummyBaseClassImport


with _DummyBaseClassImport():
    from ._881 import ZerolBevelGearDesign
    from ._882 import ZerolBevelGearMeshDesign
    from ._883 import ZerolBevelGearSetDesign
    from ._884 import ZerolBevelMeshedGearDesign
