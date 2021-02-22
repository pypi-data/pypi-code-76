from datetime import datetime
from magicdb import FrontendParserModel, MagicModel


class Params(FrontendParserModel):
    args: list
    kwargs: dict


class BackgroundTask(MagicModel):
    params: Params
    created_at: datetime
    finished_at: datetime = None
    task_took: datetime = None
