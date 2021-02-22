import random
from calendar import monthrange
from datetime import datetime
from typing import Any, Dict, List

import numpy as np
from pytz import timezone

from sktmls.models import MLSLightGBMModel, MLSModelError

TZ = timezone("Asia/Seoul")
PRODUCTS = [
    {"id": "NA00006535", "name": "T플랜 안심2.5G", "price": 43000, "seg": ["tplan", "young"]},
    {"id": "NA00006536", "name": "T플랜 안심4G", "price": 50000, "seg": ["tplan"]},
    {"id": "NA00006537", "name": "T플랜 에센스", "price": 69000, "seg": ["tplan"]},
    {"id": "NA00006538", "name": "T플랜 스페셜", "price": 79000, "seg": ["tplan", "young"]},
    {"id": "NA00006539", "name": "T플랜 맥스", "price": 100000, "seg": ["tplan", "young"]},
    {"id": "NA00006155", "name": "0플랜 스몰", "price": 33000, "seg": ["young"]},
    {"id": "NA00006156", "name": "0플랜 미디엄", "price": 50000, "seg": ["young"]},
    {"id": "NA00006157", "name": "0플랜 라지", "price": 69000, "seg": ["young"]},
    {"id": "NA00006794", "name": "T플랜 시니어 안심 2.8G", "price": 43000, "seg": ["senior"]},
    {"id": "NA00006795", "name": "T플랜 시니어 안심 4.5G", "price": 50000, "seg": ["senior"]},
    {"id": "NA00006796", "name": "T플랜 시니어 에센스", "price": 69000, "seg": ["senior"]},
    {"id": "NA00006797", "name": "T플랜 시니어 스페셜", "price": 79000, "seg": ["senior"]},
    {"id": "NA00006403", "name": "5GX 스탠다드", "price": 75000, "seg": ["5g"]},
    {"id": "NA00006404", "name": "5GX 프라임", "price": 89000, "seg": ["5g"]},
    {"id": "NA00006405", "name": "5GX 플래티넘", "price": 125000, "seg": ["5g"]},
]


class FeeNoEquipSingleEmbModel(MLSLightGBMModel):
    """
    MLS 모델 레지스트리에 등록되는 단일 LightGBM 기반 클래스입니다.

    일반 요금제 추천 모델에 특화된 모델이며, 하나의 임베딩 피쳐를 사용합니다.
    """

    def __init__(
        self,
        model,
        model_name: str,
        model_version: str,
        model_features: List[str],
        default_feature_values: List[Any],
        default_context_value: str,
        emb_feature_indices: List[int] = None,
        conversion_formulas: Dict[str, Dict[str, Any]] = dict(),
        context_features: List[str] = [],
        context_values: List[Any] = [],
        product_context_indices: Dict[str, List[int]] = dict(),
    ):
        """
        ## Args

        - model: LightGBM으로 학습한 모델 객체
        - model_name: (str) 모델 이름
        - model_version: (str) 모델 버전
        - model_features: (list(str)) 피쳐 리스트 (필수 피쳐: `age`, `bas_fee_amt`, `filter_five_g`)
        - default_feature_values: (list) 피쳐 기본값 리스트
        - default_context_value: (str) 기본 컨텍스트 값
        - emb_feature_indices: (optional) (list(int)) 임베딩 피쳐 중 선택할 인덱스 리스트 (기본값: None. 전체 임베딩 피쳐를 사용)
        - conversion_formulas: (optional) (dict(dict)) Feature conversion에 사용할 조건 dict (기본값: {})
        - context_features: (optional) (list(str)) 컨텍스트 생성을 위한 피쳐 리스트 (기본값: [])
        - context_values: (optional) (list) 컨텍스트 값 리스트 (기본값: [])
        - product_context_indices: (optional) (dict) 추천 상품 별 사용 컨텍스트 인덱스 맵 (기본값: {})

        ## Example

        ```python
        fee_no_equip_model_v20200904 = FeeNoEquipSingleEmbModel(
            model=lightgbm_model,
            model_name="fee_no_equip_model",
            model_version="v20200904",
            model_features=["feature1", "feature2", "feature3", "feature4", "emb_feature_list"],
            default_feature_values=[3.0, "Y", 10.0, "S", [0.1, 0.2, 0.3, 0.4]],
            default_context_value="context_default",
            emb_feature_indices=[0, 2],
            conversion_formulas={
                "feature4": {"map": {"S": 1, "D": 2}, "default": 0},
                "feature1": {"conditions": [[">", 0], ["<", 100]], "default": -1}
            },
            context_features=["filter_tfamilymoa", "context_data_overuse", "app_use_traffic_music_ratio_median_yn"],
            context_values=["tfamilymoa_value", "overuse_value", "music_ratio_value"],
            product_context_indices={
                "NA00006537": [0, 1],
                "NA00006539": [0, 1, 2],
                "NA00006817": [1]
            }
        )

        result = fee_no_equip_model_v20200904.predict([0.1, "N", 100, "S", [1, 2, 3, 4]])
        ```
        """
        assert len(model_features) == len(
            default_feature_values
        ), "`model_features`와 `default_feature_values`의 길이가 다릅니다."
        assert None not in default_feature_values, "`default_feature_values`에 None이 포함되어 있습니다."
        assert isinstance(default_feature_values[-1], list), "임베딩 피쳐는 리스트 형식이어야 합니다."
        assert default_feature_values[-1], "임베딩 피쳐의 기본값 리스트가 유효하지 않습니다."

        if emb_feature_indices is not None:
            assert isinstance(emb_feature_indices, list), "`emb_feature_indices`는 리스트 형식이어야 합니다."

        assert isinstance(conversion_formulas, dict), "`conversion_formulas`는 dict 형식이어야 합니다."
        for k, v in conversion_formulas.items():
            assert isinstance(k, str), "`conversion_formulas`의 키는 문자열이어야 합니다."
            assert isinstance(v, dict), "`conversion_formulas`의 값은 dict 형식이어야 합니다."
            assert "map" in v or "conditions" in v, "`conversion_formulas`의 값에 map 또는 conditions 키가 포함되어야 합니다."
            assert "default" in v, "`conversion_formulas`의 값에 default 키가 포함되어야 합니다."

        if context_features and context_values:
            assert len(context_features) == len(context_values), "`context_features`와 `context_values`의 길이는 같아야 합니다."
        else:
            assert (
                not context_features and not context_values
            ), "`context_features`와 `context_values`는 둘 다 전달되거나 둘 다 전달되지 않아야 합니다."

        assert isinstance(product_context_indices, dict), "`product_context_indices`는 dict 형식이어야 합니다."
        product_ids = [p["id"] for p in PRODUCTS]
        for k, v in product_context_indices.items():
            assert isinstance(k, str), "`product_context_indices`의 키는 문자열이어야 합니다."
            assert k in product_ids, "`product_context_indices`에 없는 상품 ID가 포함되어 있습니다."
            assert isinstance(v, list), "`product_context_indices`의 값은 리스트 형식이어야 합니다."
            assert len(v) <= len(context_features), "`product_context_indices`의 리스트가 `context_features`보다 깁니다."

        super().__init__(model, model_name, model_version, model_features + context_features)

        self.default_feature_values = default_feature_values
        self.default_context_value = default_context_value
        self.emb_feature_indices = (
            emb_feature_indices if emb_feature_indices is not None else list(range(len(default_feature_values[-1])))
        )
        self.conversion_formulas = conversion_formulas
        self.context_values = context_values
        self.product_context_indices = product_context_indices

    def predict(self, x: List[Any], **kwargs) -> Dict[str, Any]:
        # x 체크
        if len(self.features) != len(x):
            raise MLSModelError("FeeNoEquipSingleEmbModel: `x`의 길이가 `features`의 길이와 다릅니다.")

        model_x = x[: len(x) - len(self.context_values)]
        context_x = x[len(x) - len(self.context_values) :]

        if model_x[-1] and not isinstance(model_x[-1], list):
            raise MLSModelError("FeeNoEquipSingleEmbModel: model_x의 마지막 element가 list 타입이 아닙니다.")
        if model_x[-1] and (len(model_x[-1]) != len(self.default_feature_values[-1])):
            raise MLSModelError("FeeNoEquipSingleEmbModel: model_x와 `default_feature_values`의 임베딩 피쳐 길이가 다릅니다.")
        if model_x[-1] and (len(model_x[-1]) < len(self.emb_feature_indices)):
            raise MLSModelError("FeeNoEquipSingleEmbModel: `emb_feature_indices`의 길이가 model_x의 임베딩 피쳐 길이보다 큽니다.")

        # Feature 전처리
        non_emb_x = [f if f is not None else self.default_feature_values[i] for i, f in enumerate(model_x[:-1])]
        if model_x[-1]:
            emb_x = [
                model_x[-1][i] if model_x[-1][i] is not None else self.default_feature_values[-1][i]
                for i in self.emb_feature_indices
            ]
        else:
            emb_x = [self.default_feature_values[-1][i] for i in self.emb_feature_indices]

        try:
            preprocessed_x = self._convert(non_emb_x) + emb_x
        except Exception:
            raise MLSModelError("FeeNoEquipSingleEmbModel: Feature conversion에 실패했습니다.")

        # Realtime feature 생성
        now = datetime.now(TZ)
        preprocessed_x.append(now.weekday() + 1)
        _, ndays = monthrange(now.year, now.month)
        preprocessed_x.append(now.day / ndays)

        # 상품 선택을 위한 feature 추출
        try:
            age = preprocessed_x[self.features.index("age")]
            bas_fee_amt = preprocessed_x[self.features.index("bas_fee_amt")]
            filter_five_g = preprocessed_x[self.features.index("filter_five_g")]
        except Exception:
            raise MLSModelError("FeeNoEquipSingleEmbModel: Context feature가 존재하지 않습니다.")
        products = self._get_products(age, filter_five_g)
        if not products:
            return {"items": []}

        # Prediction
        y = self.models[0].predict(np.array([preprocessed_x], dtype=np.float32)).flatten().tolist()[0]
        if y <= 0:
            return {"items": []}

        # 상품 선택
        pred_bas_fee_amt = bas_fee_amt + y * 1000
        rec_prod = None
        min_diff = 999999
        for p in products:
            diff = abs(pred_bas_fee_amt - p["price"])
            if diff > min_diff:
                break
            min_diff = diff
            rec_prod = p
        if rec_prod["price"] <= bas_fee_amt:
            return {"items": []}

        # Context 빌드
        context_indices = self.product_context_indices.get(rec_prod["id"])
        if context_indices:
            contexts = [self.context_values[i] for i in context_indices if context_x[i] == "Y"]
            context = random.choice(contexts) if contexts else self.default_context_value
        else:
            context = self.default_context_value

        return {
            "items": [
                {
                    "id": rec_prod["id"],
                    "name": rec_prod["name"],
                    "type": "fee_no_equip",
                    "props": {"context_id": context},
                }
            ]
        }

    def _get_products(self, age, filter_five_g):
        if 25 <= age < 65 and filter_five_g == 0:
            seg = "tplan"
        elif 19 <= age < 25 and filter_five_g == 0:
            seg = "young"
        elif 65 <= age <= 80 and filter_five_g == 0:
            seg = "senior"
        elif 19 <= age <= 80 and filter_five_g == 1:
            seg = "5g"
        else:
            return None

        prods = list(filter(lambda p: seg in p["seg"], PRODUCTS))
        prods = sorted(prods, key=lambda p: p["price"])
        return prods

    def _convert(self, features):
        converted_features = []
        for i, f in enumerate(features):
            feature_name = self.features[i]
            formula = self.conversion_formulas.get(feature_name)
            if formula:
                if "map" in formula:
                    converted_features.append(formula["map"].get(f, formula["default"]))
                elif "conditions" in formula:
                    conditions = formula["conditions"]
                    conditions_checked = True
                    for condition in conditions:
                        if (
                            (condition[0] == "==" and f != condition[1])
                            or (condition[0] == "!=" and f == condition[1])
                            or (condition[0] == "<" and f >= condition[1])
                            or (condition[0] == "<=" and f > condition[1])
                            or (condition[0] == ">" and f <= condition[1])
                            or (condition[0] == ">=" and f < condition[1])
                        ):
                            conditions_checked = False
                            break
                    converted_features.append(f if conditions_checked else formula["default"])
            else:
                converted_features.append({"Y": 1, "N": 0}.get(f, f))
        return converted_features
