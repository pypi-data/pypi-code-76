import sys
import os
import logging
import inspect
import socket

sys.path.append(os.path.join(os.getcwd(), '../../..'))
sys.path.append(os.path.join('../log/config'))

if sys.argv[0].find('client') == -1:
    LOGGER = logging.getLogger('server.app')
else:
    LOGGER = logging.getLogger('client.app')


# функция декоратор
def log(func):
    def wrapper(*args, **kwargs):
        wrap = func(*args, **kwargs)
        LOGGER.debug(f'Была вызвана функция {func.__name__} '
                     f'с параметрами {args}, {kwargs}. '
                     f'Вызов из модуля {func.__module__}.'
                     f'Вызов из функции {inspect.stack()[1][3]}', stacklevel=2)
        return wrap
    return wrapper


# класс декоратор
class Log:
    def __call__(self, func):
        def decorated(*args, **kwargs):
            wrap = func(*args, **kwargs)
            LOGGER.debug(f'Была вызвана функция '
                         f'{func.__name__} с параметрами {args}, {kwargs}. '
                         f'Вызов из модуля {func.__module__}. '
                         f'Вызов из функции {inspect.stack()[1][3]}',
                         stacklevel=2)
            return wrap
        return decorated


def login_required(func):
    '''
    Декоратор, проверяющий, что клиент авторизован на сервере.
    Проверяет, что передаваемый объект сокета находится в
    списке авторизованных клиентов.
    За исключением передачи словаря-запроса
    на авторизацию. Если клиент не авторизован,
    генерирует исключение TypeError
    '''
    def checker(*args, **kwargs):
        # проверяем, что первый аргумент - экземпляр MessageProcessor
        # Импортить необходимо тут, иначе ошибка рекурсивного импорта.
        from server.server.server_core import MessageProcessor
        from server.common.vars import ACTION, PRESENCE
        if isinstance(args[0], MessageProcessor):
            found = False
            for arg in args:
                if isinstance(arg, socket.socket):
                    # Проверяем, что данный сокет есть в списке names класса
                    # MessageProcessor
                    for client in args[0].names:
                        if args[0].names[client] == arg:
                            print(f'Проверяем, что данный сокет есть '
                                  f'в списке names класса MessageProcessor')
                            found = True

            # Теперь надо проверить, что передаваемые аргументы не presence
            # сообщение. Если presense, то разрешаем
            for arg in args:
                if isinstance(arg, dict):
                    if ACTION in arg and arg[ACTION] == PRESENCE:
                        print(f'Теперь надо проверить, '
                              f'что передаваемые аргументы '
                              f'не presence сообщение.'
                              f' Если presense, то разрешаем')
                        found = True
            # Если не авторизован и не сообщение начала авторизации, то
            # вызываем исключение.
            if not found:
                print(
                    f'Если не авторизован и не сообщение '
                    f'начала авторизации, то вызываем исключение.')
                raise TypeError
        return func(*args, **kwargs)

    return checker
