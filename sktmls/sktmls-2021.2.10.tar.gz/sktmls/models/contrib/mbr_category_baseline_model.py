import random
from datetime import datetime
from typing import Any, Dict, List

from pytz import timezone

from sktmls.models import MLSRuleModel, MLSModelError

TZ = timezone("Asia/Seoul")
SEED_FORMAT = {"hourly": "%Y%m%d%H", "daily": "%Y%m%d", "weekly": "%Y%W", "monthly": "%Y%m", "yearly": "%Y"}


class MbrCategoryBaselineModel(MLSRuleModel):
    """
    MLS 모델 레지스트리에 등록되는 Rule 기반 클래스입니다.

    멤버십 단독 카테고리 추천에 특화된 모델입니다.
    """

    def __init__(
        self,
        model_name: str,
        model_version: str,
        features: List[str],
        item_type: str,
        context_id: str,
        num_pick: int = 1,
        random_cycle: str = "daily",
    ):
        """
        ## Args

        - model_name: (str) 모델 이름
        - model_version: (str) 모델 버전
        - features: (list(str)) 피쳐 리스트 (필수 피쳐: `user_id`)
        - item_type: (str) 결과의 `type`에 표기할 값
        - context_id: (str) 컨텍스트 ID
        - num_pick: (optional) (int) 랜덤 추출할 갯수 (기본값: 1)
        - random_cycle: (optional) (str) 랜덤 시드 초기화 주기 (`hourly`|`daily`|`weekly`|`monthly`|`yearly`) (기본값: `daily`)

        ## Example

        ```python
        my_model_v1 = MbrCategoryBaselineModel(
            model_name="my_model",
            model_version="v1",
            features=["user_id", "available_benefit_pizza", "used_datediff_pizza"],
            item_type="mbr_pizza",
            context_id="context",
            num_pick=14,
            random_cycle="daily"
        )

        result = my_model_v1.predict(["1234567890", ["2234", "2308", "2306", "2286"], 37])
        ```
        """
        assert (
            isinstance(features, list) and len(features) > 0 and features[0] == "user_id"
        ), "`features`가 유효하지 않습니다. `features`의 첫 값은 반드시 `user_id`이어야 합니다."
        assert isinstance(num_pick, int) and num_pick > 0, "`num_pick`이 유효하지 않습니다. 반드시 1 이상의 값을 가져야 합니다."
        assert random_cycle in SEED_FORMAT, "허용되지 않는 `random_cycle`값입니다."

        super().__init__(model_name, model_version, features)

        self.item_type = item_type
        self.context_id = context_id
        self.num_pick = num_pick
        self.random_cycle = random_cycle

    def predict(self, x: List[Any], **kwargs) -> Dict[str, Any]:
        if len(x) != 3:
            raise MLSModelError("MbrCategoryBaselineModel: x의 길이가 3이어야 합니다.")
        if x[1] is not None and not isinstance(x[1], list):
            raise MLSModelError("MbrCategoryBaselineModel: `available_benefit`이 리스트 형식이 아닙니다.")

        user_id = x[0]
        available_benefit = x[1]
        used_datediff = x[2]
        category_use_yn = "Y" if isinstance(used_datediff, int) and used_datediff <= 365 else "N"

        random.seed(f"{user_id}{self.item_type}{datetime.now(TZ).strftime(SEED_FORMAT[self.random_cycle])}")

        if not available_benefit:
            return {"items": []}

        candidates = [
            {
                "id": i,
                "name": "#",
                "type": self.item_type,
                "props": {
                    "score": str(round(random.random(), 4)),
                    "category_use_yn": category_use_yn,
                    "context_id": self.context_id,
                },
            }
            for i in available_benefit
        ]
        num_pick = min(self.num_pick, len(candidates))
        top_candidates = sorted(candidates, key=lambda k: float(k["props"]["score"]), reverse=True)[:num_pick]

        return {"items": top_candidates}
