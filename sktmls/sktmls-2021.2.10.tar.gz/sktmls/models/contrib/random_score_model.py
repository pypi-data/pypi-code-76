import random
from datetime import datetime
from typing import Any, Dict, List

from pytz import timezone

from sktmls.models import MLSRuleModel, MLSModelError

TZ = timezone("Asia/Seoul")
SEED_FORMAT = {"hourly": "%Y%m%d%H", "daily": "%Y%m%d", "weekly": "%Y%W", "monthly": "%Y%m", "yearly": "%Y"}


class RandomScoreModel(MLSRuleModel):
    """
    MLS 모델 레지스트리에 등록되는 Rule 기반 클래스입니다.

    고정된 추천 상품에 대해 random score를 반환합니다.
    """

    def __init__(self, model_name: str, model_version: str, item_id: str, item_name: str, item_type: str):
        """
        ## Args

        - model_name: (str) 모델 이름
        - model_version: (str) 모델 버전
        - item_id: (str) 결과의 `id`에 표기할 값
        - item_name: (str) 결과의 `name`에 표기할 값
        - item_type: (str) 결과의 `type`에 표기할 값

        ## Example

        ```python
        my_model_v1 = RandomScoreModel(
            model_name="my_model",
            model_version="v1",
            item_id="item1",
            item_name="아이템1",
            item_type="type"
        )

        result = my_model_v1.predict(None)
        ```
        """
        super().__init__(model_name, model_version, ["user_id"])

        self.item_id = item_id
        self.item_name = item_name
        self.item_type = item_type

    def predict(self, x: List[Any], **kwargs) -> Dict[str, Any]:
        return {
            "items": [
                {
                    "id": self.item_id,
                    "name": self.item_name,
                    "type": self.item_type,
                    "props": {"score": str(round(random.random(), 4))},
                }
            ]
        }


class PeriodicRandomScoreModel(RandomScoreModel):
    """
    MLS 모델 레지스트리에 등록되는 Rule 기반 클래스입니다.

    고정된 추천 상품에 대해 random score를 반환합니다.

    `random_cycle` 값을 참조하여 랜덤 시드를 설정합니다.
    """

    def __init__(
        self,
        model_name: str,
        model_version: str,
        item_id: str,
        item_name: str,
        item_type: str,
        random_cycle: str = "daily",
    ):
        """
        ## Args

        - model_name: (str) 모델 이름
        - model_version: (str) 모델 버전
        - item_id: (str) 결과의 `id`에 표기할 값
        - item_name: (str) 결과의 `name`에 표기할 값
        - item_type: (str) 결과의 `type`에 표기할 값
        - random_cycle: (optional) (str) 랜덤 시드 초기화 주기 (`hourly`|`daily`|`weekly`|`monthly`|`yearly`) (기본값: `daily`)

        ## Example

        ```python
        my_model_v1 = PeriodicRandomScoreModel(
            model_name="my_model",
            model_version="v1",
            item_id="item1",
            item_name="아이템1",
            item_type="type",
            random_cycle="weekly"
        )

        result = my_model_v1.predict("my_svc_mgmt_num")
        ```
        """
        super().__init__(model_name, model_version, item_id, item_name, item_type)

        if random_cycle not in SEED_FORMAT:
            raise MLSModelError("허용되지 않는 `random_cycle`값입니다.")
        self.random_cycle = random_cycle

    def predict(self, x: List[Any], **kwargs) -> Dict[str, Any]:
        user_id = x[0]
        random.seed(f"{user_id}{self.item_type}{datetime.now(TZ).strftime(SEED_FORMAT[self.random_cycle])}")
        return super().predict(x)
