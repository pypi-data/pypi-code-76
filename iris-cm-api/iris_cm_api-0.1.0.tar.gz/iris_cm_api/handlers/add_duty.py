from aiohttp import InvalidURL, ContentTypeError
from vkbottle import BotBlueprint
from vkbottle.bot import Message
from vkbottle.modules import logger

from iris_cm_api.utils import send_request
from iris_cm_api.models import Duty

bot = BotBlueprint()
bot.labeler.vbml_ignore_case = True


@bot.on.private_message(text=[
    "+api <secret_code> <url>",
    "+апи <secret_code> <url>"
])
async def create_duty(m: Message, secret_code: str, url: str):
    try:
        data = await send_request(
            url, dict(
                method="ping",
                user_id=m.from_id,
                secret=secret_code,
                object={},
                message={}
            )
        )
        if not data.get('response') == 'ok':
            return f"Не верный ответ сервера. Ошибка: {data.get('error_code', 0)}"
        duty = await Duty.get_or_none(id=m.from_id)
        if duty is None:
            await Duty.create(id=m.from_id, url=url, secret_code=secret_code)
            return "✅ Сигналы API привязаны!"
        duty.url = url
        duty.secret_code = secret_code
        await duty.save()
        return "✅ Сигналы API привязаны!"
    except InvalidURL:
        return "⚠ Не верный URL сервера API"
    except ContentTypeError:
        return "⚠ Не верный ответ сервера. (Нужен JSON)"
    except Exception as ex:
        logger.exception(ex)
        return f"⚠ Ошибка {ex.__class__.__name__}: {ex}"
