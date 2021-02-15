import random
from collections import OrderedDict
from datetime import datetime
from typing import Any, Dict, List

from pytz import timezone

from sktmls.models import MLSRuleModel, MLSModelError

TZ = timezone("Asia/Seoul")
SEED_FORMAT = {
    "hourly": "%Y%m%d%H",
    "daily": "%Y%m%d",
    "weekly": "%Y%W",
    "monthly": "%Y%m",
    "yearly": "%Y",
    "none": "%c%f",
}


class MbrCustomBenefitRandomModel(MLSRuleModel):
    """
    MLS 모델 레지스트리에 등록되는 Rule 기반 클래스입니다.

    사전정의된 컨텍스트 기반 추천에 특화된 모델입니다.
    """

    def __init__(
        self,
        model_name: str,
        model_version: str,
        features: List[str],
        categories: List[str],
        item_type: str,
        contexts: Dict[str, List] = None,
        num_pick: int = 1,
        random_cycle: str = "daily",
    ):
        """
        ## Args

        - model_name: (str) 모델 이름
        - model_version: (str) 모델 버전
        - features: (list(str)) 피쳐 리스트 (필수 피쳐: `user_id`)
        - categories: (list(str)) 전체 카테고리 리스트. 필수 피쳐 이후 피쳐 순서와 동일해야 합니다.
        - item_type: (str) 결과의 `type`에 표기할 값
        - contexts: (dict) context_id와 연결된 benefit 리스트가 key, value 인 딕셔너리.
        - num_pick: (optional) (int) 랜덤 추출할 갯수 (기본값: 1)
        - random_cycle: (optional) (str) 랜덤 시드 초기화 주기 (`hourly`|`daily`|`weekly`|`monthly`|`yearly`|`none`) (기본값: `daily`)
            - `none`의 경우 매 호출마다 초기화합니다.

        ## Example

        ```python
        my_model_v1 = MbrCustomBenefitRandomModel(
            model_name="my_model",
            model_version="v1",
            features=["user_id", "available_benefit_activity", "available_benefit_asianfood", "available_benefit_beauty"],
            categories=["mbr_activity", "mbr_asianfood", "mbr_beauty"],
            item_type="mbr_custom_benefit",
            contexts={"37": ["97", "27", "32", "99", "26", "133", "84", "37", "15", "38", "85", "48", "47", "12"]},
            num_pick=14,
            random_cycle="daily",
        )
        result = my_model_v1.predict(["1234567890", None, ["1", "5", "6"], ["a1", "a2", "a3", "a4"]])
        ```
        """
        assert (
            isinstance(features, list) and len(features) > 0 and features[0] == "user_id"
        ), "`features`가 유효하지 않습니다. `features`의 첫 값은 반드시 `user_id`이어야 합니다."
        assert isinstance(categories, list) and len(categories) + 1 == len(
            features
        ), "전체 카테고리 리스트 길이가 필수 피쳐를 제외한 피쳐의 수와 다릅니다."
        assert (
            isinstance(contexts, dict) and len(contexts) > 0
        ), "`contexts`은 반드시 키가 문자열이고 값이 리스트인 딕셔너리 타입이고 적어도 한개의 아이템을 가져야합니다"
        assert isinstance(num_pick, int) and num_pick > 0, "`num_pick`이 유효하지 않습니다. 반드시 1 이상의 값을 가져야 합니다."
        assert random_cycle in SEED_FORMAT, "허용되지 않는 `random_cycle`값입니다."

        super().__init__(model_name, model_version, features)

        self.categories = categories
        self.item_type = item_type
        self.contexts = contexts
        self.num_pick = num_pick
        self.random_cycle = random_cycle

    def predict(self, x: List[Any], **kwargs) -> Dict[str, Any]:
        for i, f in enumerate(x[1:]):
            if f is not None and not isinstance(f, list):
                raise MLSModelError(f"MbrCustomBenefitRandomModel: {self.features[i + 1]}이 리스트 형식으로 전달되지 않았습니다.")
        user_id = x[0]

        available_benefit = {
            category: x[i + 1]
            for i, category in enumerate(self.categories)
            if isinstance(x[i + 1], list) and len(x[i + 1]) >= 1
        }

        random.seed(f"{user_id}{self.item_type}{datetime.now(TZ).strftime(SEED_FORMAT[self.random_cycle])}")
        context_id = random.choice(list(self.contexts.keys()))

        target_benefit_list = self.contexts[context_id]

        available_benefit_list = sum(available_benefit.values(), [])
        valid_target_benefit_list = list(
            OrderedDict.fromkeys(filter(lambda x: x in available_benefit_list, target_benefit_list))
        )

        candidates = [
            {
                "id": benefit,
                "name": "#",
                "type": self.item_type,
                "props": {"context_id": context_id},
            }
            for benefit in valid_target_benefit_list
        ]

        num_pick = min(self.num_pick, len(candidates))
        top_candidates = candidates[:num_pick]

        return {"items": top_candidates}
