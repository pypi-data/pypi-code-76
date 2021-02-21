import logging

# порт по умолчанию
DEFAULT_PORT = 7777
# адресс для подключения клиента по умолчанию
DEFAULT_IP_ADDRESS = '127.0.0.1'
# максимальное количество подключений
MAX_CONNECTONS = 5
# максимальный размер принимаемого сообщения в байтах
MAX_PACKAGE_SIZE = 10240
# кодировка
ENCODING = 'UTF-8'
# База данных для хранения данных сервера:
SERVER_CONFIG = 'server.ini'

# JIM main keys
ACTION = 'action'
USER = 'user'
TIME = 'time'
USERNAME = 'username'
SENDER = 'from'
DESTINATION = 'to'
DATA = 'bin'
PUBLIC_KEY = 'pubkey'

# JIM's another keys
PRESENCE = 'presence'
RESPONSE = 'response'
ERROR = 'error'
MESSAGE = 'message'
MESSAGE_TEXT = 'message text'
EXIT = 'exit'
GET_CONTACTS = 'get_contacts'
LIST_INFO = 'data_list'
REMOVE_CONTACT = 'remove'
ADD_CONTACT = 'add'
USERS_REQUEST = 'get_users'
PUBLIC_KEY_REQUEST = 'pubkey_need'

LOGGING_LEVEL = logging.DEBUG

# типовые словари ответов
# 200
RESPONSE_200 = {RESPONSE: 200}
# 202
RESPONSE_202 = {RESPONSE: 202,
                LIST_INFO: None
                }
# 400
RESPONSE_400 = {
    RESPONSE: 400,
    ERROR: None
}

# 205
RESPONSE_205 = {
    RESPONSE: 205
}

# 511
RESPONSE_511 = {
    RESPONSE: 511,
    DATA: None
}
