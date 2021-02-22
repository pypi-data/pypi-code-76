'''__init__.py'''


from mastapy._internal.dummy_base_class_importer import _DummyBaseClassImport


with _DummyBaseClassImport():
    from ._873 import DesignConstraint
    from ._874 import DesignConstraintCollectionDatabase
    from ._875 import DesignConstraintsCollection
    from ._876 import GearDesign
    from ._877 import GearDesignComponent
    from ._878 import GearMeshDesign
    from ._879 import GearSetDesign
    from ._880 import SelectedDesignConstraintsCollection
