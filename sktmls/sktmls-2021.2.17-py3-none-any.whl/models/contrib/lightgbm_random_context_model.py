from typing import Any, Dict, List
import random

import numpy as np

from sktmls.models import MLSLightGBMModel, MLSModelError


class LightGBMRandomContextModel(MLSLightGBMModel):
    """
    MLS 모델 레지스트리에 등록되는 LightGBM 기반 클래스입니다.

    주어진 `features`리스트를 이용해 prediction 후 cutoff 필터를 진행합니다.
    이후 `context`, `item_id`, `item_name`, `item_type`을 추가하여 반환하는 모델입니다.
    """

    def __init__(
        self,
        model,
        model_name: str,
        model_version: str,
        model_features: List[str],
        default_feature_values: List[Any],
        default_context_value: str,
        cutoff: float,
        item_id: str,
        item_name: str,
        item_type: str,
        context_features: List[str] = None,
        context_values: List[Any] = None,
    ):
        """
        ## Args

        - model: LightGBM으로 학습한 모델 객체
        - model_name: (str) 모델 이름
        - model_version: (str) 모델 버전
        - model_features: (list(str)) 학습에 사용된 피쳐 리스트
        - default_feature_values: (list) 피쳐 기본값 리스트
        - default_context_value: (str) 기본 컨텍스트 값
        - cutoff: (float) Cutoff 값
        - item_id: (str) Item ID
        - item_name: (str) Item 이름
        - item_type: (str) Item 타입
        - context_features: (optional) (list(str)) 컨텍스트 생성을 위한 피쳐 리스트 (기본값: None)
        - context_values: (optional) (list) 컨텍스트 값 리스트 (기본값: None)

        ## Example

        ```python
        my_model_v20200827 = LightGBMRandomContextModel(
            model=lightgbm_model,
            model_name="my_model",
            model_version="v20200827",
            model_features=["feature1", "feature2", "feature3", "feature4"],
            default_feature_values=[3.0, "Y", 10.0, "N"],
            default_context_value="default_context",
            cutoff=0.3,
            item_id="my_id",
            item_name="my_name",
            item_type="my_type",
            context_features=["feature5", "feature2"],
            context_values=["context_1", "context_2"],
        )

        result = my_model_v20200827.predict(["value_1", "value_2", "value_3", "value_4", "value_5", "value_2"])

        ```
        """
        if context_features and context_values:
            assert len(context_features) == len(context_values), "`context_features`와 `context_values`의 길이는 같아야 합니다."
        else:
            assert (
                not context_features and not context_values
            ), "`context_features`와 `context_values`는 둘 다 전달되거나 둘 다 전달되지 않아야 합니다."

        super().__init__(model, model_name, model_version, model_features + context_features)

        assert len(model_features) == len(
            default_feature_values
        ), "`model_features`와 `default_feature_values`의 길이가 다릅니다."
        assert None not in default_feature_values, "`default_feature_values`에 None이 포함되어 있습니다."
        self.default_feature_values = default_feature_values

        self.context_values = context_values
        self.default_context_value = default_context_value
        self.cutoff = cutoff
        self.item_id = item_id
        self.item_name = item_name
        self.item_type = item_type

    def predict(self, x: List[Any], **kwargs) -> Dict[str, Any]:
        if len(self.features) != len(x):
            raise MLSModelError("`x`와 `features`의 길이가 다릅니다.")

        model_x = x[: len(x) - len(self.context_values)]
        context_x = x[len(x) - len(self.context_values) :]

        model_x = [f if f is not None else self.default_feature_values[i] for i, f in enumerate(model_x)]

        y = self.models[0].predict(np.array([model_x])).flatten().tolist()[0]
        if y < self.cutoff:
            return {"items": []}

        contexts = [self.context_values[i] for i, f in enumerate(context_x) if f == "Y"]
        if len(contexts) == 0:
            context = self.default_context_value
        else:
            context = random.choice(contexts)

        return {
            "items": [
                {
                    "id": self.item_id,
                    "name": self.item_name,
                    "type": self.item_type,
                    "props": {"score": y, "context_id": context},
                }
            ]
        }
