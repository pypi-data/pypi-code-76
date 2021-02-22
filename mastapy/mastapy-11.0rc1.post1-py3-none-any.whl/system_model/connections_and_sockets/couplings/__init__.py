'''__init__.py'''


from mastapy._internal.dummy_base_class_importer import _DummyBaseClassImport


with _DummyBaseClassImport():
    from ._2018 import ClutchConnection
    from ._2019 import ClutchSocket
    from ._2020 import ConceptCouplingConnection
    from ._2021 import ConceptCouplingSocket
    from ._2022 import CouplingConnection
    from ._2023 import CouplingSocket
    from ._2024 import PartToPartShearCouplingConnection
    from ._2025 import PartToPartShearCouplingSocket
    from ._2026 import SpringDamperConnection
    from ._2027 import SpringDamperSocket
    from ._2028 import TorqueConverterConnection
    from ._2029 import TorqueConverterPumpSocket
    from ._2030 import TorqueConverterTurbineSocket
