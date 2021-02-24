# All functions computing a name used across components
from typing_extensions import Literal

def get_account_extract_table_name(
    account_id: str,
    client_id: str,
    account_type: str,
    level: Literal['daily', 'hourly'] = 'daily'
    ) -> str:
    return f'{client_id}.{account_type}_extract_{account_id}_campaign_{level}'
