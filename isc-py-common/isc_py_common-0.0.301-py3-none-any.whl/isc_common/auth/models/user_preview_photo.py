import logging

from django.conf import settings
from django.http import HttpResponse

from isc_common.auth.models.user import User
from isc_common.http.DSResponse import JsonResponseWithException

logger = logging.getLogger(__name__)

@JsonResponseWithException()
def user_preview_photo(request, id):
    obj = User.objects.get(id=id)
    try:
        response = HttpResponse(obj.attfile.open(mode='rb').read())
        logger.debug(f'Fetch: ID: ({obj.id})  {obj.attfile}')
        return response

    except FileNotFoundError:
        response = HttpResponse(open(settings.THUMB_NOT_FOUND, mode='rb').read())
        logger.debug(f'Fetch: {settings.THUMB_NOT_FOUND}')
        return response
