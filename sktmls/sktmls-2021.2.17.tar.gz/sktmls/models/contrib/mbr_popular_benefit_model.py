from collections import OrderedDict
from datetime import datetime
from typing import Any, Dict, List

from pytz import timezone

from sktmls import MLSRuntimeENV
from sktmls.apis import MLSProfileAPIClient
from sktmls.models import MLSRuleModel, MLSModelError

TZ = timezone("Asia/Seoul")


class MbrPopularBenefitModel(MLSRuleModel):
    """
    MLS 모델 레지스트리에 등록되는 Rule 기반 클래스입니다.

    멤버십 인기 혜택 추천에 특화된 모델입니다.
    """

    def __init__(
        self,
        model_name: str,
        model_version: str,
        features: List[str],
        categories: List[str],
        item_type: str,
        hourly_contexts: List[Any],
        num_pick: int = 1,
    ):
        """
        ## Args

        - model_name: (str) 모델 이름
        - model_version: (str) 모델 버전
        - features: (list(str)) 피쳐 리스트 (필수 피쳐: `user_id`, `sex_cd`, `age`, `mbr_card_gr_cd`)
        - categories: (list(str)) 전체 카테고리 리스트. 필수 피쳐 이후 피쳐 순서와 동일해야 합니다.
        - item_type: (str) 결과의 `type`에 표기할 값
        - hourly_contexts: (list) context_id 생성을 위한 정보를 담은 시간별 context 리스트
        - num_pick: (optional) (int) 랜덤 추출할 갯수 (기본값: 1)

        ## Example

        ```python
        my_model_v1 = MbrPopularBenefitModel(
            model_name="my_model",
            model_version="v1",
            features=["user_id", "sex_cd", "age", "mbr_card_gr_cd", "available_benefit_activity", "available_benefit_asianfood", "available_benefit_beauty"],
            categories=["mbr_activity", "mbr_asianfood", "mbr_beauty"],
            item_type="mbr_popular_benefit",
            hourly_contexts=[30, 31,...],
            num_pick=14,
        )
        ```
        """
        assert (
            isinstance(features, list)
            and len(features) > 0
            and features[0] == "user_id"
            and features[1] == "sex_cd"
            and features[2] == "age"
            and features[3] == "mbr_card_gr_cd"
        ), "`features`가 유효하지 않습니다. 위 모델의 필수 피쳐는 `user_id`, `sex_cd`, `age`, `mbr_card_gr_cd`로 순서를 지켜 입력하여야합니다"
        assert isinstance(categories, list) and len(categories) + 4 == len(
            features
        ), "전체 카테고리 리스트 길이가 필수 피쳐를 제외한 피쳐의 수와 다릅니다."
        assert (
            isinstance(hourly_contexts, list) and len(hourly_contexts) == 24
        ), "`hourly_context`가 리스트가 아니거나 유효한 길이(24)가 아닙니다"
        assert isinstance(num_pick, int) and num_pick > 0, "`num_pick`이 유효하지 않습니다. 반드시 1 이상의 값을 가져야 합니다."

        super().__init__(model_name, model_version, features)

        self.categories = categories
        self.item_type = item_type
        self.hourly_contexts = hourly_contexts
        self.num_pick = num_pick

    def predict(self, x: List[Any], **kwargs) -> Dict[str, Any]:
        for i, f in enumerate(x[4:]):
            if f is not None and not isinstance(f, list):
                raise MLSModelError(f"MbrPopularBenefitModel: {self.features[i + 1]}이 리스트 형식으로 전달되지 않았습니다.")

        pf_client = kwargs.get("pf_client") or MLSProfileAPIClient(runtime_env=MLSRuntimeENV.MMS)

        sex_cd = x[1]
        age = x[2]
        mbr_card_gr_cd = x[3]

        if (
            not isinstance(sex_cd, str)
            or not isinstance(age, int)
            or not isinstance(mbr_card_gr_cd, str)
            or sex_cd not in ["1", "2"]
            or age not in range(100)
            or mbr_card_gr_cd not in ["S", "G", "V"]
        ):
            return {"items": []}

        this_time = datetime.now(TZ)
        this_hour = this_time.strftime("%H")
        this_dow = str(this_time.weekday())

        available_benefit = {
            category: x[i + 4]
            for i, category in enumerate(self.categories)
            if isinstance(x[i + 4], list) and len(x[i + 4]) >= 1
        }

        if sex_cd == "1":
            seg_sex_cd = "male"
        else:
            seg_sex_cd = "female"

        if age in range(0, 19):
            seg_age = "age0019"
        elif age in range(19, 34):
            seg_age = "age2034"
        elif age in range(34, 49):
            seg_age = "age3549"
        else:
            seg_age = "age5099"

        seg_id = f"mbr_seg_{seg_sex_cd}_{seg_age}_gr_{mbr_card_gr_cd.lower()}"

        if this_dow in ["0", "1", "2", "3", "4"]:
            weekday_cd = "weekday"
        else:
            weekday_cd = "weekend"
        ranking_dimension = f"benefit_ranking_{weekday_cd}_hour_{this_hour}"

        item_profile = pf_client.get_item_profile(
            profile_id="tmembership_seg",
            item_id=seg_id,
            keys=[ranking_dimension],
        )

        if (
            ranking_dimension not in item_profile
            or not isinstance(item_profile[ranking_dimension], list)
            or not len(item_profile[ranking_dimension]) >= 1
        ):
            return {"items": []}

        target_benefit_list = item_profile[ranking_dimension]

        available_benefit_list = sum(available_benefit.values(), [])

        valid_target_benefit_list = list(
            OrderedDict.fromkeys(filter(lambda x: x in available_benefit_list, target_benefit_list))
        )

        candidates = [
            {
                "id": i,
                "name": "#",
                "type": self.item_type,
                "props": {"context_id": self.hourly_contexts[int(this_hour)]},
            }
            for i in valid_target_benefit_list
        ]
        num_pick = min(self.num_pick, len(candidates))
        top_candidates = candidates[:num_pick]

        return {"items": top_candidates}
