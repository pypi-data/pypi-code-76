import pytest

from sktmls.models.contrib import BnfLoyaltyRuleModel


class TestBnfLoyaltyRuleModels:
    @pytest.fixture(scope="class")
    def param(self):
        return {"model": BnfLoyaltyRuleModel("test_model", "test_version", ["svc_scrb_period"])}

    def test_000_bnf_loyalty_return(self, param):
        assert param.get("model").predict([0]) == {"items": []}

    def test_001_bnf_loyalty_return(self, param):
        assert param.get("model").predict([800]) == {
            "items": [{"id": "BNF0000003", "name": "장기 고객 혜택 정보", "type": "bnf_loyalty", "props": {}}]
        }
