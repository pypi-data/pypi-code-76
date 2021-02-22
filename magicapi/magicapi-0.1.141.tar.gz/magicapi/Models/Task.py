import boto3
from datetime import datetime
from magicdb import FrontendParserModel, DateModel, MagicModel

# from magicapi import settings
# from magicapi.Globals.G import g


from magicapi import g

dynamodb = boto3.resource("dynamodb")
table = dynamodb.Table(g.settings.tasks_table_name)

# this is deprecated, only used if you want to use dynamo as Q


class TaskParams(MagicModel):
    args: list
    kwargs: dict


# for now cannot accept an object that does not have the dict ability...
class Task(DateModel):
    task_id: str
    url: str
    status: str
    sent: bool
    secret_token: str
    params: str = None
    local: bool

    class Meta:
        collection_name = "_tasks"

    @staticmethod
    def get_table():
        return table
