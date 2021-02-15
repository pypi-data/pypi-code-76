import random
from datetime import datetime
from typing import Any, Dict, List

from pytz import timezone

from sktmls.models import MLSRuleModel, MLSModelError

TZ = timezone("Asia/Seoul")
SEED_FORMAT = {"daily": "%Y%m%d", "weekly": "%Y%W", "monthly": "%Y%m", "yearly": "%Y"}


class RandomPickModel(MLSRuleModel):
    """
    MLS 모델 레지스트리에 등록되는 Rule 기반 클래스입니다.

    주어진 `candidate` 중 `num_pick`개의 결과를 랜덤하게 추출하여 반환하는 모델입니다.
    """

    def __init__(self, model_name: str, model_version: str, candidates: List[Dict[str, Any]], num_pick: int = 1):
        """
        ## Args

        - model_name: (str) 모델 이름
        - model_version: (str) 모델 버전
        - candidates: (list(dict)) 랜덤 추출할 후보 리스트
        - num_pick: (optional) (int) 랜덤 추출할 갯수 (기본값: 1)

        ## Example

        ```python
        my_model_v1 = RandomPickModel(
            model_name="my_model",
            model_version="v1",
            candidates=[
                {
                    "id": "item1",
                    "name": "아이템1",
                    "type": "타입",
                    "props": {}
                },
                {
                    "id": "item2",
                    "name": "아이템2",
                    "type": "타입",
                    "props": {}
                },
                {
                    "id": "item3",
                    "name": "아이템3",
                    "type": "타입",
                    "props": {}
                }
            ],
            num_pick=2)

        result = my_model_v1.predict(None)
        ```
        """
        super().__init__(model_name, model_version, ["user_id"])

        if len(candidates) < num_pick:
            raise MLSModelError("The length of num_pick cannot be greater than that of candidates")

        self.candidates = candidates
        self.num_pick = num_pick

    def predict(self, x: List[Any], **kwargs) -> Dict[str, Any]:
        return {"items": random.sample(self.candidates, self.num_pick)}


class PeriodicRandomPickModel(RandomPickModel):
    """
    MLS 모델 레지스트리에 등록되는 Rule 기반 클래스입니다.

    주어진 `candidate` 중 `num_pick`개의 결과를 랜덤하게 추출하여 반환하는 모델입니다.

    `random_cycle` 값을 참조하여 랜덤 시드를 설정합니다.
    """

    def __init__(
        self,
        model_name: str,
        model_version: str,
        candidates: List[Dict[str, Any]],
        num_pick: int = 1,
        random_cycle: str = "daily",
    ):
        """
        ## Args

        - model_name: (str) 모델 이름
        - model_version: (str) 모델 버전
        - candidates: (dict) 랜덤 추출할 후보 리스트
        - num_pick: (optional) (int) 랜덤 추출할 갯수 (기본값: 1)
        - random_cycle: (optional) (str) 랜덤 시드 초기화 주기 (`daily`|`weekly`|`monthly`|`yearly`) (기본값: `daily`)

        ## Example

        ```python
        my_model_v1 = PeriodicRandomPickModel(
            model_name="my_model",
            model_version="v1",
            candidates=[
                {
                    "id": "item1",
                    "name": "아이템1",
                    "type": "타입",
                    "props": {}
                },
                {
                    "id": "item2",
                    "name": "아이템2",
                    "type": "타입",
                    "props": {}
                },
                {
                    "id": "item3",
                    "name": "아이템3",
                    "type": "타입",
                    "props": {}
                }
            ],
            num_pick=2,
            random_cycle="daily")

        result = my_model_v1.predict("my_svc_mgmt_num")
        ```
        """
        super().__init__(model_name, model_version, candidates, num_pick)

        if random_cycle not in SEED_FORMAT:
            raise MLSModelError("허용되지 않는 `random_cycle`값입니다.")
        self.random_cycle = random_cycle

    def predict(self, x: List[Any], **kwargs) -> Dict[str, Any]:
        user_id = x[0]
        random.seed(f"{user_id}{datetime.now(TZ).strftime(SEED_FORMAT[self.random_cycle])}")
        return super().predict(x)
