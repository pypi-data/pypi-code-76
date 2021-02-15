from typing import Any, Dict, List

from sktmls.models import MLSCatBoostModel, MLSModelError


class CatBoostPointwiseRankingModel(MLSCatBoostModel):
    """
    MLS 모델 레지스트리에 등록되는 CatBoost 기반 클래스입니다.

    여러 차례 predict_proba를 수행하여 score가 높은 상품을 추천하는 모델입니다.
    """

    def __init__(
        self,
        model,
        model_name: str,
        model_version: str,
        point_feature: str,
        model_features: List[str],
        context_features: List[str],
        products: Dict[str, Any],
        item_type: str,
        cutoff: float,
        num_pick: int = 0,
    ):
        """
        ## Args

        - model: CatBoost로 학습한 모델 객체
        - model_name: (str) 모델 이름
        - model_version: (str) 모델 버전
        - point_feature: (str) 포인트로 사용되는 값 리스트를 가리키는 피쳐 이름
        - model_features: (list(str)) 모델 피쳐 리스트
        - context_features: (list(str)) 컨텍스트 전용 피쳐 리스트
        - products: (dict) 추천 상품 정보. 형식은 아래 Example 참조
        - item_type: (str) 추천 상품 타입 (`type`에 들어갈 값)
        - cutoff: (float) 추천 기준 스코어
        - num_pick: (optional) (int) 추천할 상위 스코어 상품 수. 0인 경우 cutoff를 넘는 모든 상품 추천 (기본값: 0)

        ## Example

        ```python
        products = {
            "TTT0000000": {
                "name": "T상품1",
                "context_features": ["context_call_overuse"],
                "context_default": "context_default",
            },
            "TTT0000001": {
                "name": "T상품2",
                "context_features": ["app_use_traffic_healthcare_yn", "context_discount_benefit"],
                "context_default": "context_default",
            },
            "TTT0000002": {
                "name": "T상품3",
                "context_features": ["context_school_contact"],
                "context_default": "context_age1020",
            },
        }

        my_model_v1 = PointwiseRankingModel(
            model_name="my_model",
            model_version="v1",
            point_feature="reco_items",
            model_features=["feature1", "feature2", "feature3"],
            context_features=["context_check_bill", "context_school_contact", "context_antivirusapp_usage"],
            products=products,
            item_type="app_sk",
            cutoff=0.0,
            num_pick=3,
        )

        # point_feature + model_features + context_features 순서로 리스트를 구성하여 predict 함수 호출
        result = my_model_v1.predict([["TW50000002", "TW50000005"], 0.3, 0.4, 0.5])
        ```
        """
        assert isinstance(point_feature, str) and len(point_feature) > 0, "`point_feature`가 유효하지 않습니다."
        assert isinstance(model_features, list) and len(model_features) > 0, "`model_features`가 유효하지 않습니다."
        assert isinstance(context_features, list), "`context_features`가 유효하지 않습니다."
        assert isinstance(num_pick, int), "`num_pick`이 유효하지 않습니다."

        super().__init__(model, model_name, model_version, [point_feature] + model_features + context_features)

        self.point_feature = point_feature
        self.model_features = model_features
        self.context_features = context_features
        self.products = products
        self.item_type = item_type
        self.cutoff = cutoff
        self.num_pick = num_pick

    def predict(self, x: List[Any], **kwargs) -> Dict[str, Any]:
        point_feature_values = x[0]
        model_feature_values = x[1 : len(self.model_features) + 1]
        context_feature_values = x[-len(self.context_features) :] if self.context_features else []

        if not point_feature_values:
            return {"items": []}

        if not isinstance(point_feature_values, list):
            raise MLSModelError("PointwiseRankingModel: `point_feature`의 값이 리스트 타입이 아닙니다.")

        context_feature_map = {name: context_feature_values[i] for i, name in enumerate(self.context_features)}

        preprocessed_x = [[item_id] + model_feature_values for item_id in point_feature_values]
        y = self.models[0].predict_proba(preprocessed_x)

        items = []
        for i, proba in enumerate(y):
            score = proba[1]
            item_id = point_feature_values[i]
            if score >= self.cutoff:
                product = self.products.get(item_id, {})
                product_context_features = [
                    f for f in product.get("context_features", []) if context_feature_map.get(f, "N") == "Y"
                ]
                context_id = (
                    product_context_features[0]
                    if product_context_features
                    else product.get("context_default", "context_default")
                )
                items.append(
                    {
                        "id": item_id,
                        "name": product.get("name", "#"),
                        "type": self.item_type,
                        "score": score,
                        "props": {"context_id": context_id},
                    }
                )
        num_pick = min(self.num_pick, len(items)) if self.num_pick > 0 else len(items)
        items = sorted(items, key=lambda x: x["score"], reverse=True)[:num_pick]
        items = [{k: v for k, v in d.items() if k != "score"} for d in items]

        return {"items": items}
