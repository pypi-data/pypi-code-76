from datetime import datetime
import boto3
from boto3.dynamodb.conditions import Key
from murd import Murd
from murd.murd import group_key, sort_key


ddb_murd_prefix = "murd_"


def list_all_ddb_tablenames():
    ddb = boto3.client("dynamodb")
    resp = ddb.list_tables()
    tablenames = resp['TableNames']
    while 'LastEvaluatedTableName' in resp:
        resp = ddb.list_tables(ExclusiveStartTableName=resp['LastEvaluatedTableName'])
        tablenames.extend(resp['TableNames'])

    return tablenames


def get_murds(force_scan=False):
    if force_scan or not get_murds.murd_tables:
        tablenames = list_all_ddb_tablenames()
        get_murds.murd_tables = [table for table in tablenames if ddb_murd_prefix == table[:len(ddb_murd_prefix)]]
    return get_murds.murd_tables


get_murds.murd_tables = []


class DDBMurd(Murd):
    def __init__(self, table_name=None, connect=True):
        self.default_murd_name = table_name
        try:
            table_name = get_murds()[0] if table_name is None else table_name
            candidate_tables = [t for t in get_murds() if table_name in t]
            self.table_name = candidate_tables[0]
            self.ddb_table = boto3.resource("dynamodb").Table(self.table_name)
        except Exception:
            raise Exception(f"Unable to locate murd ddb table ({table_name})")

        self.murds = {self.default_murd_name: self}
        if connect:
            self.connect_ddb_murds()

    @staticmethod
    def create_murd_table(table_name):
        ddb = boto3.client("dynamodb")
        ddb.create_table(
            TableName=f'{ddb_murd_prefix}{table_name}.{datetime.utcnow().isoformat()[:10]}',
            BillingMode="PAY_PER_REQUEST",
            AttributeDefinitions=[
                {
                    'AttributeName': f'{group_key}',
                    'AttributeType': 'S'
                },
                {
                    'AttributeName': f'{sort_key}',
                    'AttributeType': 'S'
                }
            ],
            KeySchema=[
                {
                    'AttributeName': f'{group_key}',
                    'KeyType': 'HASH'
                },
                {
                    'AttributeName': f'{sort_key}',
                    'KeyType': 'RANGE'
                }
            ]
        )

    def connect_ddb_murds(self):
        for murd in get_murds():
            if murd != self.table_name:
                self.murds[murd] = DDBMurd(murd, connect=False)

    def update_data(self, ms):
        primed_ms = self.prime_ms(ms)
        if len(primed_ms) > 0:
            # Store Ms in DynamoDB table
            with self.ddb_table.batch_writer() as writer:
                for key, m in primed_ms.items():
                    writer.put_item(Item=m)

    @staticmethod
    def complete_table_query(table, kwargs):
        query_result = table.query(**kwargs)
        items = query_result['Items']

        while 'LastEvaluatedKey' in query_result:
            kwargs['ExclusiveStartKey'] = query_result['LastEvaluatedKey']
            query_result = table.query(**kwargs)
            items.extend(query_result['Items'])

            if 'Limit' in kwargs and len(items) >= kwargs['Limit']:
                break

        results = [Murd.M(**item) for item in items]
        if 'Limit' in kwargs:
            results = results[:kwargs['Limit']]

        return results

    def read_data(self,
                  group,
                  sort=None,
                  min_sort=None,
                  max_sort=None,
                  descending_order=False,
                  limit=None):
        kce = Key(group_key).eq(group)
        if sort is not None:
            kce = kce & Key(sort_key).begins_with(sort)

        elif max_sort is not None and min_sort is not None:
            kce = kce & Key(sort_key).between(min_sort, max_sort)

        elif max_sort is not None:
            kce = kce & Key(sort_key).lt(max_sort)
        elif min_sort is not None:
            kce = kce & Key(sort_key).gt(min_sort)

        kwargs = {}
        kwargs['KeyConditionExpression'] = kce
        kwargs['ScanIndexForward'] = descending_order
        if limit is not None:
            kwargs['Limit'] = limit

        results = self.complete_table_query(self.ddb_table, kwargs)
        return results

    def delete_data(self, ms):
        primed_ms = self.prime_ms(ms)
        stubborn_ms = []
        with self.ddb_table.batch_writer() as writer:
            for m in primed_ms.values():
                try:
                    writer.delete_item(
                        Key={
                            group_key: m[group_key],
                            sort_key: m[sort_key]
                        }
                    )
                except Exception:
                    stubborn_ms.append(m)
        if stubborn_ms:
            raise Exception(f"Unable to delete items: {stubborn_ms}")
