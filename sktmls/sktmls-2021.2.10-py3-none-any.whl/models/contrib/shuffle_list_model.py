import random
from datetime import datetime
from typing import Any, Dict, List

from pytz import timezone

from sktmls.models import MLSRuleModel, MLSModelError

TZ = timezone("Asia/Seoul")
SEED_FORMAT = {"daily": "%Y%m%d", "weekly": "%Y%W", "monthly": "%Y%m", "yearly": "%Y"}


class ShuffleListModel(MLSRuleModel):
    """
    MLS 모델 레지스트리에 등록되는 Rule 기반 클래스입니다.

    주어진 `shuffle_list`를 랜덤하게 섞은 뒤 props에 넣어 반환하는 모델입니다.
    """

    def __init__(self, model_name: str, model_version: str, item_id: str, item_name: str, shuffle_list: List[str]):
        """
        ## Args

        - model_name: (str) 모델 이름
        - model_version: (str) 모델 버전
        - item_id: (str) 결과의 `id`에 표기할 값
        - item_name: (str) 결과의 `name`에 표기할 값
        - shuffle_list: (list(str)) 순서를 섞어서 반환할 input 리스트

        ## Example

        ```python
        my_model_v1 = ShuffleListModel(
            model_name="my_model",
            model_version="v1",
            item_id="item1",
            item_name="아이템1",
            shuffle_list=["hello", "world", "good", "morning"]
        )

        result = my_model_v1.predict(None)
        ```
        """
        super().__init__(model_name, model_version, ["user_id"])

        self.item_id = item_id
        self.item_name = item_name
        self.shuffle_list = shuffle_list

    def predict(self, x: List[Any], **kwargs) -> Dict[str, Any]:
        random.shuffle(self.shuffle_list)
        return {
            "items": [
                {
                    "id": self.item_id,
                    "name": self.item_name,
                    "props": {self.item_id: self.shuffle_list},
                    "type": self.item_id,
                }
            ]
        }


class PeriodicShuffleListModel(ShuffleListModel):
    """
    MLS 모델 레지스트리에 등록되는 Rule 기반 클래스입니다.

    주어진 `shuffle_list`를 랜덤하게 섞은 뒤 props에 넣어 반환하는 모델입니다.

    `shuffle_cycle` 값을 참조하여 랜덤 시드를 설정합니다.
    """

    def __init__(
        self,
        model_name: str,
        model_version: str,
        item_id: str,
        item_name: str,
        shuffle_list: List[str],
        shuffle_cycle: str = "daily",
    ):
        """
        ## Args

        - model_name: (str) 모델 이름
        - model_version: (str) 모델 버전
        - item_id: (str) 결과의 `id`에 표기할 값
        - item_name: (str) 결과의 `name`에 표기할 값
        - shuffle_list: (list(str)) 순서를 섞어서 반환할 input 리스트
        - shuffle_cycle: (optional) (str) 랜덤 시드 초기화 주기 (`daily`|`weekly`|`monthly`|`yearly`) (기본값: `daily`)

        ## Example

        ```python
        my_model_v1 = PeriodicShuffleListModel(
            model_name="my_model",
            model_version="v1",
            item_id="item1",
            item_name="아이템1",
            shuffle_list=["hello", "world", "good", "morning"],
            shuffle_cycle="weekly"
        )

        result = my_model_v1.predict("my_svc_mgmt_num")
        ```
        """
        super().__init__(model_name, model_version, item_id, item_name, shuffle_list)

        if shuffle_cycle not in SEED_FORMAT:
            raise MLSModelError("허용되지 않는 `shuffle_cycle`값입니다.")
        self.shuffle_cycle = shuffle_cycle

    def predict(self, x: List[Any], **kwargs) -> Dict[str, Any]:
        user_id = x[0]
        random.seed(f"{user_id}{datetime.now(TZ).strftime(SEED_FORMAT[self.shuffle_cycle])}")
        return {
            "items": [
                {
                    "id": self.item_id,
                    "name": self.item_name,
                    "props": {self.item_id: random.sample(self.shuffle_list, len(self.shuffle_list))},
                    "type": self.item_id,
                }
            ]
        }
