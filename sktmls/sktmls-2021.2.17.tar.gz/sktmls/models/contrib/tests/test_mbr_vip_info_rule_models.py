import pytest

from sktmls.models.contrib import MbrVipInfoRuleModel


class TestMbrVipInfoRuleModels:
    @pytest.fixture(scope="class")
    def param(self):
        return {
            "model": MbrVipInfoRuleModel("test_model", "test_version", ["mbr_card_gr_cd", "mbr_use_discount_amt_cum"])
        }

    def test_000_mbr_vip_info_return(self, param):
        assert param.get("model").predict(["N", 1]) == {
            "items": [{"id": "INF0000009", "name": "VIP 혜택 및 승급 방법 안내", "type": "mbr_vip_info", "props": {}}]
        }

    def test_001_mbr_vip_info_no_return(self, param):
        assert param.get("model").predict(["V", 1]) == {"items": []}

    def test_002_mbr_vip_info_no_return(self, param):
        assert param.get("model").predict(["N", 0]) == {"items": []}
