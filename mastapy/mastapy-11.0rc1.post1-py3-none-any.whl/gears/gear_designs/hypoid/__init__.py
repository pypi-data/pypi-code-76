'''__init__.py'''


from mastapy._internal.dummy_base_class_importer import _DummyBaseClassImport


with _DummyBaseClassImport():
    from ._914 import HypoidGearDesign
    from ._915 import HypoidGearMeshDesign
    from ._916 import HypoidGearSetDesign
    from ._917 import HypoidMeshedGearDesign
