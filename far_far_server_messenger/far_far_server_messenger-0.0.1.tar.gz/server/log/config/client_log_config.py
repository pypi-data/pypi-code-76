from logging import getLogger, Formatter, StreamHandler, FileHandler, \
    INFO
from server.common.vars import LOGGING_LEVEL
import os
import sys
sys.path.append(os.path.join('../'))

# настройка пути логирования
PATH = os.path.dirname(os.path.abspath(__file__))
PATH = os.path.join(PATH, '../logs/client/client.log')

# создаем регистратор (логгер)
LOG_CLIENT = getLogger('client.app')
# создаем обработчик

FILE_HANDLER = FileHandler(PATH, encoding='utf-8')
# создаем формттер
FORMATTER = Formatter(
    "%(asctime)-20s %(levelname)-10s %(filename)-10s %(message)s")
# подключаем форматтер к обработчику
FILE_HANDLER.setFormatter(FORMATTER)
# добавляем обработчик регистратору
LOG_CLIENT.addHandler(FILE_HANDLER)
LOG_CLIENT.setLevel(LOGGING_LEVEL)

STREAM_HANDLER = StreamHandler(sys.stderr)
STREAM_HANDLER.setFormatter(FORMATTER)
STREAM_HANDLER.setLevel(INFO)
LOG_CLIENT.addHandler(STREAM_HANDLER)

if __name__ == '__main__':

    # передаем сообщение
    LOG_CLIENT.info('Информационное сообщение')
    LOG_CLIENT.debug('Дебаг')
    LOG_CLIENT.warning('Внимание')
    LOG_CLIENT.error('Ошибка')
    LOG_CLIENT.critical('Критическая ошибка')
