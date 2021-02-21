from enum import Enum


class QueueItemState(Enum):
    created = 'created'
    blocked = 'blocked'
    released = 'released'


def get_sql_to_get_batch_from_queue(table_name: str, pk_field: str, ttl_field: str, items_per_batch: int,
                                    ttl_for_blocking_item_in_seconds: int, state_field: str,
                                    state_blocked=QueueItemState.blocked.value):
    sql = f"""WITH x AS (
      SELECT {pk_field} FROM {table_name} WHERE {state_field} != '{state_blocked}' OR {ttl_field} <= NOW()
      LIMIT {items_per_batch} FOR UPDATE SKIP LOCKED
    )
    UPDATE {table_name}
        SET {ttl_field} = NOW() + INTERVAL '{ttl_for_blocking_item_in_seconds} seconds',
        {state_field} = '{state_blocked}'
    FROM x
        WHERE {table_name}.{pk_field} = x.{pk_field}
    RETURNING *
    """

    return sql


def get_sql_to_release_queue_item(table_name: str, pk_field: str, pk_value: [str, int], ttl_field: str,
                                  state_field: str, state_released=QueueItemState.released.value):
    sql = f"""UPDATE {table_name}
        SET {ttl_field} = 'NOW()', {state_field} = '{state_released}'
        WHERE {pk_field} = {f"'{pk_value}'" if isinstance(pk_value, str) else pk_value}
    """

    return sql


def get_sql_to_delete_queue_item(table_name: str, pk_field: str, pk_value: [str, int]):
    sql = f"""
        DELETE FROM {table_name}
        WHERE {pk_field} = {f"'{pk_value}'" if isinstance(pk_value, str) else pk_value}
    """

    return sql
