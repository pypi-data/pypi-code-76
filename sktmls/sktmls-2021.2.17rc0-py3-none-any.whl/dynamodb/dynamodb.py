from typing import Dict, Any

from sktmls import MLSClient, MLSENV, MLSRuntimeENV, MLSResponse

MLS_DYNAMODB_API_URL = "/api/v1/dynamodb"


class DynamoDBClient(MLSClient):
    """
    DynamoDB 관련 기능들을 제공하는 클라이언트입니다.
    위 클라이언트는 STG 환경만 지원됩니다.
    """

    def __init__(
        self,
        env: MLSENV = None,
        runtime_env: MLSRuntimeENV = None,
        username: str = None,
        password: str = None,
    ):
        """
        ## Args

        - env: (`sktmls.MLSENV`) 접근할 MLS 환경. 본 클라이언트는 STG 환경(`sktmls.MLSENV.STG`)만 지원
        - runtime_env: (`sktmls.MLSRuntimeENV`) 클라이언트가 실행되는 환경 (`sktmls.MLSRuntimeENV.YE`|`sktmls.MLSRuntimeENV.EDD`|`sktmls.MLSRuntimeENV.LOCAL`) (기본값: `sktmls.MLSRuntimeENV.LOCAL`)
        - username: (str) MLS 계정명 (기본값: $MLS_USERNAME)
        - password: (str) MLS 계정 비밀번호 (기본값: $MLS_PASSWORD)

        ## Returns
        `sktmls.dynamodb.DynamoDBClient`

        ## Example

        ```python
        dynamodb_client = DynamoDBClient(env=MLSENV.STG, runtime_env=MLSRuntimeENV.YE, username="mls_account", password="mls_password")
        ```
        """
        super().__init__(env=env, runtime_env=runtime_env, username=username, password=password)
        assert self._MLSClient__env == MLSENV.STG, "STG 환경만 지원합니다"

    def get_item(
        self,
        table_name: str,
        key: Dict[str, Any],
    ) -> Dict[str, Any]:
        """
        주어진 Dynamodb 테이블의 특정 아이템을 조회합니다

        ## Args

        - table_name: (str) 테이블 명
        - key: (dict) 조회할 아이템의 key 값

        ## Returns

        (dict) 해당 아이템 값

        ## Example

        ```python
        item = dynamodb_client.get_item(table_name="sample_table", key={"item_id": "sample"})
        ```
        """
        return self._request(
            method="POST", url=MLS_DYNAMODB_API_URL, data={"type": "get", "table_name": table_name, "body": key}
        ).results

    def put_item(self, table_name: str, item: Dict[str, Any]) -> Dict[str, Any]:
        """
        주어진 Dynamodb 테이블에 특정 아이템을 추가합니다

        ## Args

        - table_name: (str) 테이블 명
        - item: (dict) 추가할 아이템 값

        ## Returns

        (dict) 추가한 아이템 값

        ## Example
        ```python
        dynamodb_client.put_item(
            table_name="sample_table",
            item={"item_id": "sample", "sample_attribute": "sample_value"}
        )
        ```
        """
        return self._request(
            method="POST",
            url=MLS_DYNAMODB_API_URL,
            data={"type": "put", "table_name": table_name, "body": item},
        ).results

    def update_item(self, table_name: str, item: Dict[str, Any]) -> Dict[str, Any]:
        """
        주어진 Dynamodb 테이블의 특정 아이템을 수정합니다

        ## Args

        - table_name: (str) 테이블 명
        - item: (dict) 수정할 아이템 값

        ## Returns

        (dict) 수정한 아이템 값

        ## Example

        ```python
        dynamodb_client.update_item(
            table_name="sample_table",
            item={"item_id": "sample", "sample_attribute": "sample_value_updated", "add_new_field": "added_field_value"}
        )
        ```
        """
        return self._request(
            method="POST",
            url=MLS_DYNAMODB_API_URL,
            data={"type": "update", "table_name": table_name, "body": item},
        ).results

    def delete_item(self, table_name: str, key: Dict[str, Any]) -> MLSResponse:
        """
        주어진 Dynamodb 테이블의 특정 아이템을 삭제합니다

        ## Args

        - table_name: (str) 테이블 명
        - key: (dict) 삭제할 아이템의 key 값

        ## Returns

        `sktmls.MLSResponse`

        ## Example

        ```python
        dynamodb_client.delete_item(
            table_name="sample_table",
            item={"item_id": "sample"}
        )
        ```
        """
        return self._request(
            method="POST",
            url=MLS_DYNAMODB_API_URL,
            data={"type": "delete", "table_name": table_name, "body": key},
        )
