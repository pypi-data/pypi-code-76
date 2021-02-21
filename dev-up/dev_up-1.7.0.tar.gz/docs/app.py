from typing import Optional, Any, List

from aiohttp.web_request import Request
from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from pydantic import BaseModel
from starlette.responses import JSONResponse

from . import models


class ErrorResponseParamModel(BaseModel):
    key: str
    value: Any


class ErrorResponseModel(BaseModel):
    err_code: int
    err_critical_lvl: Optional[str]
    err_msg: Optional[str]
    params: Optional[List[ErrorResponseParamModel]]


class ErrorModel(BaseModel):
    err: ErrorResponseModel


async def request_validation_exception_handler(
    request: Request, exc: RequestValidationError
) -> JSONResponse:
    return JSONResponse(
        status_code=200,
        content=ErrorModel(
            err=ErrorResponseModel(
                err_code=1,
                err_critical_lvl="str",
                err_msg="str",
                params=[ErrorResponseParamModel(key="123", value=2)])
        ).dict(),
    )

app = FastAPI(
    title="DEV UP",
    version="1.0.0",
    servers=[{"url": "https://api.dev-up.ru/method"}],
    exception_handlers={
        RequestValidationError: request_validation_exception_handler
    },
)
app.exception_handlers = {}


class BaseRequestModel(BaseModel):
    key: str


class VkGetStickersRequest(BaseRequestModel):
    user_id: int


class VkGetStickerInfo(BaseRequestModel):
    sticker_id: int


class VkGetGroupsRequest(BaseRequestModel):
    user_id: int


class VkGetAppsRequest(BaseRequestModel):
    user_id: int


class ProfileGetRequest(BaseRequestModel):
    ...


class AudioSpeechRequest(BaseRequestModel):
    url: str


class UtilsMD5GenerateRequest(BaseRequestModel):
    text: str


class UtilsGetServerTimeRequest(BaseRequestModel):
    ...


class UtilsGetShortLinkRequest(BaseRequestModel):
    url: str


class UtilsNotificationsLinksRequest(BaseRequestModel):
    code: str
    status: models.NotificationsLinksStatus


@app.post(
    '/vk.getStickers',
    response_model=models.VkGetStickers,
    description="Получает список стикеров пользователя",
    tags=["vk"]
)
async def get_stickers(params: VkGetStickersRequest) -> models.VkGetStickers:
    ...


@app.post(
    '/vk.getStickerInfo',
    response_model=models.VkGetStickerInfo,
    description="Получает информацию о стикере и стикер-паке",
    tags=["vk"]
)
async def get_sticker_info(params: VkGetStickerInfo) -> models.VkGetStickerInfo:
    ...


@app.post(
    '/vk.getGroups',
    response_model=models.VkGetGroups,
    description="Получает список групп пользователя",
    tags=["vk"]
)
async def get_groups(params: VkGetGroupsRequest) -> models.VkGetGroups:
    ...


@app.post(
    '/vk.getApps',
    response_model=models.VkGetApps,
    description="Получает список приложений пользователя",
    tags=["vk"]
)
async def get_apps(params: VkGetAppsRequest) -> models.VkGetApps:
    ...


@app.post(
    '/profile.get',
    response_model=models.ProfileGet,
    description="Получает информацию о профиле DEV-UP",
    tags=["profile"]
)
async def get(params: ProfileGetRequest) -> models.ProfileGet:
    ...


@app.post(
    '/audio.speech',
    response_model=models.AudioSpeech,
    description="Преобразование аудио в текст",
    tags=["audio"]
)
async def speech(params: AudioSpeechRequest) -> models.AudioSpeech:
    ...


@app.post(
    '/utils.md5Generate',
    response_model=models.UtilsMD5Generate,
    description="Получить хэш md5 из текста",
    tags=["utils"]
)
async def md5_generate(params: UtilsMD5GenerateRequest) -> models.UtilsMD5Generate:
    ...


@app.post(
    '/utils.getServerTime',
    response_model=models.UtilsGetServerTime,
    description="Возвращает текущее время на сервере в unixtime (МСК)",
    tags=["utils"]
)
async def get_server_time(params: UtilsGetServerTimeRequest) -> models.UtilsGetServerTime:
    ...


@app.post(
    '/utils.getShortLink',
    response_model=models.UtilsGetShortLink,
    description="Сокращение ссылок",
    tags=["utils"]
)
async def get_short_link(params: UtilsGetShortLinkRequest) -> models.UtilsGetShortLink:
    ...


@app.post(
    '/utils.notificationsLinks',
    response_model=models.UtilsNotificationsLinks,
    description="Управление уведомлениями от ссылок",
    tags=["utils"]
)
async def notifications_links(params: UtilsNotificationsLinksRequest) -> models.UtilsNotificationsLinks:
    ...
