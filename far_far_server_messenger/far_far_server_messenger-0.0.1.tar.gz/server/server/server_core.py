import threading
import select
import socket
import json
import hmac
import binascii
import os
from common.descriptors import Port
from common.vars import *
from common.functions import send_message, get_message
from common.decos import login_required

# Загрузка логера
LOG_SERVER = logging.getLogger('server.app')


class MessageProcessor(threading.Thread):
    '''
    Основной класс сервера. Принимает содинения, словари - пакеты
    от клиентов, обрабатывает поступающие сообщения.
    Работает в качестве отдельного потока.
    '''
    port = Port()

    def __init__(self, listen_address, listen_port, database):
        # параметры подключения
        self.address = listen_address
        self.port = listen_port

        # бд
        self.database = database

        # соке, через который будет очуществляться работа
        self.sock = None

        # список подключенных клиентов
        self.clients = []

        # сокеты
        self.listen_sockets = None
        self.error_sockets = None

        # флаг работы
        self.running = True

        # Словарь содержащий сопоставленные имена и соответствующие им сокеты.
        self.names = dict()

        # Конструктор предка
        super().__init__()

    def run(self):
        # сокет
        self.init_socket()

        while True:
            try:
                client, client_address = self.sock.accept()
            except OSError:
                pass
            else:
                LOG_SERVER.info(
                    f'Установлено соедиение с адресом {client_address}')
                self.clients.append(client)

            recv_data_lst = []
            send_data_lst = []
            err_lst = []

            try:
                if self.clients:
                    recv_data_lst, self.listen_sockets, self.error_sockets = select.select(
                        self.clients, self.clients, [], 0)
            except OSError as err:
                LOG_SERVER.error(f'Ошибка работы с сокетами: {err}')

            # принимаем сообщения,
            # но если происходит ошибка - исключаем клиента
            if recv_data_lst:
                for clint_with_msg in recv_data_lst:
                    try:
                        self.proccess_agent(
                            get_message(clint_with_msg), clint_with_msg)
                    except (OSError, json.JSONDecodeError, TypeError) as err:
                        LOG_SERVER.debug(
                            f'Getting data from client exception.',
                            exc_info=err)
                        self.clients.remove(clint_with_msg)

    def remove_client(self, client):
        '''
        Метод обработчик клиента с которым прервана связь.
        Ищет клиента и удаляет его из списков и базы:
        '''
        LOG_SERVER.info(f'Клиент {client.getpeername()} '
                        f'отключился от сервера.')
        for name in self.names:
            if self.names[name] == client:
                self.database.user_logout(name)
                del self.names[name]
                break
        self.clients.remove(client)
        client.close()

    def init_socket(self):
        '''Метод инициализатор сокета.'''
        LOG_SERVER.info(
            f'Запущен сервер, порт для подключений "{self.port}", адрес '
            f'с которого принимается сообщение "{self.address}", '
            f'если адрес не указан, принимаются сообщения с любых адресов.')

        # создаем сокет
        my_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        my_socket.bind((self.address, self.port))
        my_socket.settimeout(0.5)

        # слушаем сокет
        self.sock = my_socket
        self.sock.listen(MAX_CONNECTONS)

    def process_p2p_message(self, msg):
        '''
        Метод отправки сообщения клиенту.
        '''
        if msg[DESTINATION] in self.names and \
                self.names[msg[DESTINATION]] in self.listen_sockets:
            try:
                send_message(self.names[msg[DESTINATION]], msg)
                LOG_SERVER.info(f'Отпрвлено сообщение пользователю '
                                f'{self.names[msg[DESTINATION]]}'
                                f' от пользователя {self.names[msg[SENDER]]}.')
            except OSError:
                self.remove_client(msg[DESTINATION])
        elif msg[DESTINATION] in self.names \
                and self.names[msg[DESTINATION]] not in self.listen_sockets:
            LOG_SERVER.error(
                f'Связь с клиентом {msg[DESTINATION]} была потеряна.'
                f' Соединение закрыто, доставка невозможна.')
            self.remove_client(self.names[msg[DESTINATION]])
        else:
            LOG_SERVER.error(
                f'Пользователь {msg[DESTINATION]} не зарегестрирован на '
                f'сервере, отправка сообщений от этого пользователя '
                f'не возможна.')

    @login_required
    def proccess_agent(self, msg, client):
        '''Метод отбработчик поступающих сообщений.'''
        LOG_SERVER.debug(f'Разбор сообщения от клиента : {msg}')

        # если принятое сообщение - сообщение о присутствии клиента,
        # то принимаем и отвечаем
        if ACTION in msg and msg[ACTION] == PRESENCE and \
                TIME in msg and USER in msg:
            self.autorize_user(msg, client)

        # Если это сообщение, то отправляем получателю.
        elif ACTION in msg and msg[ACTION] == MESSAGE and \
                TIME in msg and MESSAGE_TEXT in msg and \
                DESTINATION in msg and SENDER in msg \
                and self.names[msg[SENDER]] == client:
            if msg[DESTINATION] in self.names:
                self.database.process_message(msg[SENDER], msg[DESTINATION])
                self.process_p2p_message(msg)
                try:
                    send_message(client, RESPONSE_200)
                except OSError:
                    self.remove_client(client)
            else:
                response = RESPONSE_400
                response[ERROR] = 'Пользователь не зарегестирован на сервере!'
                try:
                    send_message(client, response)
                except OSError:
                    pass
            return

        # Если клиент выходит
        elif ACTION in msg and msg[ACTION] == EXIT and USERNAME in msg \
                and self.names[msg[USERNAME]] == client:
            self.remove_client(client)

        # Если это запрос контакт-листа
        elif ACTION in msg and msg[ACTION] == GET_CONTACTS and USER in msg \
                and self.names[msg[USER]] == client:
            response = RESPONSE_202
            response[LIST_INFO] = self.database.get_contacts(msg[USER])
            try:
                send_message(client, response)
            except OSError:
                self.remove_client(client)

        # Если это добавление контакта
        elif ACTION in msg and msg[ACTION] == ADD_CONTACT and \
                USERNAME in msg and USER in msg \
                and self.names[msg[USER]] == client:
            self.database.add_contact(msg[USER], msg[USERNAME])
            try:
                send_message(client, RESPONSE_200)
            except OSError:
                self.remove_client(client)

        # Если это удаление контакта
        elif ACTION in msg and msg[ACTION] == REMOVE_CONTACT and \
                USERNAME in msg and USER in msg \
                and self.names[msg[USER]] == client:
            self.database.remove_contact(msg[USER], msg[USERNAME])
            try:
                send_message(client, RESPONSE_200)
            except OSError:
                self.remove_client(client)

        # Если это запрос Известных пользователей
        elif ACTION in msg and msg[ACTION] == USERS_REQUEST and \
                USERNAME in msg and self.names[msg[USERNAME]] == client:
            response = RESPONSE_202
            response[LIST_INFO] = [user[0]
                                   for user in self.database.users_list()]
            try:
                send_message(client, response)
            except OSError:
                self.remove_client(client)

        # Если это запрос публичного ключа пользователя
        elif ACTION in msg and msg[ACTION] == PUBLIC_KEY_REQUEST \
                and USERNAME in msg:
            response = RESPONSE_511
            response[DATA] = self.database.get_pubkey(msg[USERNAME])
            # может быть, что ключа ещё нет (пользователь никогда не логинился,
            # тогда шлём 400)
            if response[DATA]:
                try:
                    send_message(client, response)
                except OSError:
                    self.remove_client(client)
            else:
                response = RESPONSE_400
                response[ERROR] = f'Нет публичного ключа для данного пользователя({msg[USERNAME]})'
                try:
                    send_message(client, response)
                except OSError:
                    self.remove_client(client)

        # в иных случаях выдаем bad request
        else:
            response = RESPONSE_400
            response[ERROR] = 'Некорректный запрос'
            try:
                send_message(client, response)
            except OSError:
                self.remove_client(client)
            return

    def autorize_user(self, msg, sock):
        '''Метод реализующий авторизцию пользователей.'''
        LOG_SERVER.debug(f'Start auth process for {msg[USER]}')
        if msg[USER][USERNAME] in self.names.keys():
            response = RESPONSE_400
            response[ERROR] = 'Имя пользователя уже занято'
            try:
                LOG_SERVER.debug(f'Username busy, sending {response}')
                send_message(sock, response)
            except OSError:
                LOG_SERVER.debug(f'OS ERROR')
                pass
            self.clients.remove(sock)
            sock.close()
        # Проверяем что пользователь зарегистрирован на сервере.
        elif not self.database.check_user(msg[USER][USERNAME]):
            response = RESPONSE_400
            response[ERROR] = f'Пользователь не зарегистрирован.'
            try:
                LOG_SERVER.debug(f'Unknown username, sending {response}')
                send_message(sock, response)
            except OSError:
                pass
            self.clients.remove(sock)
            sock.close()
        else:
            LOG_SERVER.debug('Correct username, starting passwd check.')
            # Иначе отвечаем 511 и проводим процедуру авторизации
            # Словарь - заготовка
            msg_auth = RESPONSE_511
            # Набор байтов в hex представлении
            random_str = binascii.hexlify(os.urandom(64))
            # В словарь байты нельзя, декодируем (json.dumps -> TypeError)
            msg_auth[DATA] = random_str.decode('ascii')
            # Создаём хэш пароля и связки с рандомной строкой, сохраняем
            # серверную версию ключа
            hash = hmac.new(
                self.database.get_hash(msg[USER][USERNAME]), random_str, 'MD5')
            digest = hash.digest()
            LOG_SERVER.debug(f'Auth message = {msg_auth}')
            try:
                # Обмен с клиентом
                send_message(sock, msg_auth)
                ans = get_message(sock)
            except OSError as err:
                LOG_SERVER.error('Error in auth, data:', exc_info=err)
                sock.close()
                return
            client_digest = binascii.a2b_base64(ans[DATA])
            # Если ответ клиента корректный, то сохраняем его в список
            # пользователей.
            if RESPONSE in ans and ans[RESPONSE] == 511 \
                    and hmac.compare_digest(digest, client_digest):
                self.names[msg[USER][USERNAME]] = sock
                client_ip, client_port = sock.getpeername()
                try:
                    send_message(sock, RESPONSE_200)
                except OSError:
                    self.remove_client(msg[USER][USERNAME])
                # добавляем пользователя в список активных и
                # если у него изменился открытый ключ - сохраняем новый
                self.database.user_login(msg[USER][USERNAME],
                                         client_ip,
                                         client_port,
                                         msg[USER][PUBLIC_KEY])
            else:
                response = RESPONSE_400
                response[ERROR] = 'Неверный пароль.'
                try:
                    send_message(sock, response)
                except OSError:
                    pass
                self.clients.remove(sock)
                sock.close()

    def service_update_lists(self):
        '''Метод реализующий отправки сервисного сообщения 205 клиентам.'''
        for client in self.names:
            try:
                send_message(self.names[client], RESPONSE_205)
            except OSError:
                self.remove_client(self.names[client])
