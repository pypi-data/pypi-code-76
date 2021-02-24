from abc import ABC, abstractmethod

import pytest


@pytest.mark.usefixtures(
    "picontrol_data_normalisation", "historical_data_normalisation"
)
class NormaliserIntegrationTester(ABC):
    tclass = None

    @abstractmethod
    def test_get_reference_values():
        """
        Test that reference values are retrieved as intended
        """
