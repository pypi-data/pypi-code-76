'''__init__.py'''


from mastapy._internal.dummy_base_class_importer import _DummyBaseClassImport


with _DummyBaseClassImport():
    from ._1184 import FitAndTolerance
    from ._1185 import SAESplineTolerances
