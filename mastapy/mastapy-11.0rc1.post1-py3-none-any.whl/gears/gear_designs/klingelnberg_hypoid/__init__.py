'''__init__.py'''


from mastapy._internal.dummy_base_class_importer import _DummyBaseClassImport


with _DummyBaseClassImport():
    from ._906 import KlingelnbergCycloPalloidHypoidGearDesign
    from ._907 import KlingelnbergCycloPalloidHypoidGearMeshDesign
    from ._908 import KlingelnbergCycloPalloidHypoidGearSetDesign
    from ._909 import KlingelnbergCycloPalloidHypoidMeshedGearDesign
