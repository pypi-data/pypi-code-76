'''__init__.py'''


from mastapy._internal.dummy_base_class_importer import _DummyBaseClassImport


with _DummyBaseClassImport():
    from ._516 import BiasModification
    from ._517 import FlankMicroGeometry
    from ._518 import LeadModification
    from ._519 import LocationOfEvaluationLowerLimit
    from ._520 import LocationOfEvaluationUpperLimit
    from ._521 import LocationOfRootReliefEvaluation
    from ._522 import LocationOfTipReliefEvaluation
    from ._523 import MainProfileReliefEndsAtTheStartOfRootReliefOption
    from ._524 import MainProfileReliefEndsAtTheStartOfTipReliefOption
    from ._525 import Modification
    from ._526 import ParabolicRootReliefStartsTangentToMainProfileRelief
    from ._527 import ParabolicTipReliefStartsTangentToMainProfileRelief
    from ._528 import ProfileModification
