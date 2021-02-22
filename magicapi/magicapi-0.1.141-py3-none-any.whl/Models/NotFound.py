from fastapi import Request as FastAPIRequest

from magicdb.Models import MagicModel, DateModel
from magicapi.Models.Call import Request, make_request_obj_from_request

from magicapi.Decorators.background_tasks import run_in_background
from magicapi.Decorators.parse_objects import parse_objects


class NotFound(DateModel):
    request: Request

    class Meta:
        collection_name = '_not_found'


async def save_not_found_from_request(req: FastAPIRequest):
    req_obj = await make_request_obj_from_request(req)
    nf = NotFound(request=req_obj)
    save_not_found(nf)


@run_in_background
@parse_objects
def save_not_found(not_found: NotFound):
    not_found.save()
