from typing import Any, Dict, List

from sktmls.models import MLSModelError, MLSRuleModel


class BnfLoyaltyRuleModel(MLSRuleModel):
    def predict(self, x: List[Any], **kwargs) -> Dict[str, Any]:
        if len(self.features) != len(x):
            raise MLSModelError("The length of input is different from that of features in model.json")

        svc_scrb_period = x[0] if x[0] is not None else -1
        if svc_scrb_period <= 730:
            return {"items": []}
        else:
            return {"items": [{"id": "BNF0000003", "name": "장기 고객 혜택 정보", "type": "bnf_loyalty", "props": {}}]}
