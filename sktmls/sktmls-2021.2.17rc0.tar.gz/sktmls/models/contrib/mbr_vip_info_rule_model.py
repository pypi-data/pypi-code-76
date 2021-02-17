from typing import Any, Dict, List

from sktmls.models import MLSModelError, MLSRuleModel


class MbrVipInfoRuleModel(MLSRuleModel):
    def predict(self, x: List[Any], **kwargs) -> Dict[str, Any]:
        if len(self.features) != len(x):
            raise MLSModelError("The length of input is different from that of features in model.json")

        mbr_card_gr_cd = x[0]
        mbr_use_discount_amt_cum = x[1] if x[1] is not None else 0

        if mbr_card_gr_cd != "V" and mbr_use_discount_amt_cum > 0:
            return {"items": [{"id": "INF0000009", "name": "VIP 혜택 및 승급 방법 안내", "type": "mbr_vip_info", "props": {}}]}
        else:
            return {"items": []}
