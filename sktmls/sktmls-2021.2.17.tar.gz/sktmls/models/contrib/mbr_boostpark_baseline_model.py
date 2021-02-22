import random
from datetime import datetime
from typing import Any, Dict, List

from pytz import timezone

from sktmls.models import MLSRuleModel, MLSModelError

TZ = timezone("Asia/Seoul")
SEED_FORMAT = {"hourly": "%Y%m%d%H", "daily": "%Y%m%d", "weekly": "%Y%W", "monthly": "%Y%m", "yearly": "%Y"}


class MbrBoostparkBaselineModel(MLSRuleModel):
    """
    MLS 모델 레지스트리에 등록되는 Rule 기반 클래스입니다.

    멤버십 Boostpark 추천에 특화된 모델입니다.
    """

    def __init__(
        self,
        model_name: str,
        model_version: str,
        features: List[str],
        item_type: str,
        num_pick: int = 1,
        random_cycle: str = "daily",
    ):
        """
        ## Args

        - model_name: (str) 모델 이름
        - model_version: (str) 모델 버전
        - features: (list(str)) 피쳐 리스트 (필수 피쳐: `user_id`, `available_boostpark_location`)
        - item_type: (str) 결과의 `type`에 표기할 값
        - num_pick: (optional) (int) 랜덤 추출할 갯수 (기본값: 1)
        - random_cycle: (optional) (str) 랜덤 시드 초기화 주기 (`hourly`|`daily`|`weekly`|`monthly`|`yearly`) (기본값: `daily`)

        ## Example

        ```python
        my_model_v1 = MbrBoostparkBaselineModel(
            model_name="my_model",
            model_version="v1",
            features=["user_id", "available_boostpark_location"],
            item_type="mbr_boostpark",
            num_pick=3,
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
        self.num_pick = num_pick
        self.random_cycle = random_cycle

    def predict(self, x: List[Any], **kwargs) -> Dict[str, Any]:
        if len(x) != 2:
            raise MLSModelError("MbrBoostparkBaselineModel: x의 길이가 2이어야 합니다.")

        user_id = x[0]
        available_boostpark_location = x[1]

        random.seed(f"{user_id}{self.item_type}{datetime.now(TZ).strftime(SEED_FORMAT[self.random_cycle])}")

        if available_boostpark_location is None:
            return {"items": []}

        if not isinstance(available_boostpark_location, dict):
            raise MLSModelError("MbrBoostparkBaselineModel: `available_boostpark_location`이 유효하지 않습니다. dict 형식이어야 합니다.")

        available_benefit = available_boostpark_location.get("available_benefit")
        boostpark = available_boostpark_location.get("boostpark")
        context = available_boostpark_location.get("context")

        if not available_benefit or not isinstance(available_benefit, list):
            raise MLSModelError("MbrBoostparkBaselineModel: `available_benefit`이 유효하지 않습니다. 리스트 형식이어야 합니다.")
        if not boostpark:
            raise MLSModelError("MbrBoostparkBaselineModel: `boostpark`가 유효하지 않습니다.")
        if not context:
            raise MLSModelError("MbrBoostparkBaselineModel: `context`가 유효하지 않습니다.")

        candidates = [
            {
                "id": i,
                "name": "#",
                "type": self.item_type,
                "props": {
                    "boostpark": boostpark,
                    "score": str(round(random.random(), 4)),
                    "location_context": context,
                },
            }
            for i in available_benefit
        ]
        num_pick = min(self.num_pick, len(available_benefit))
        top_candidates = sorted(candidates, key=lambda k: float(k["props"]["score"]), reverse=True)[:num_pick]

        return {"items": top_candidates}
