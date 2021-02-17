from tortoise import Tortoise
from vkbottle import Bot
from iris_cm_api import middlewares
from iris_cm_api.handlers import blueprints
from iris_cm_api.utils import get_config, init_tortoise


if __name__ == "__main__":
    config = get_config()

    bot = Bot(config.bot.token)
    bot.labeler.vbml_ignore_case = True

    bot.loop_wrapper.on_startup += [init_tortoise(config.database.url)]
    bot.loop_wrapper.on_shutdown += [Tortoise.close_connections()]

    for bl in blueprints:
        bl.load(bot)

    bot.labeler.message_view.register_middleware(middlewares.OnlyUsersMiddleware())

    bot.run_forever()
