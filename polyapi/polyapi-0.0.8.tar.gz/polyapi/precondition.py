# /usr/bin/python3
# -*- coding: utf-8 -*-
""" Модуль с предусловиями для дальнейшего взаимодействия с классами Полиматики """
import requests
from typing import Dict

SERVER_CODES = "server-codes.json"


class Preconditions:
    """
    Предусловия для дальнейшего взаимодействия с классами Полиматики:
    - получение server-codes.json
    - общая часть для создания всех запросов
     """
    def __init__(self, url: str):
        """
        Инициализация класса предусловий
        :param url: базовый URL стенда Полиматики
        """
        self.base_url = url

    def get_server_codes(self) -> Dict:
        """
        Получение GET-запросом методов и кодов типов, которые используются в Полиматике.
        :return: словарь, расположенный по пути BASE_URL/server-codes.json
        """
        r = requests.get(url=self.base_url + "/" + SERVER_CODES)
        assert r.status_code == 200, "Response code == %s!" % r.status_code
        return r.json()

    @classmethod
    def common_request_params(cls, session: str) -> Dict:
        """
        Общая часть для всех запросов.
        Запрос в общем виде: params -> [query1, query2, ..., queryN] -> query1.command (dict), ...
        В запросе: "state": 0, in response: "state": 1
        :param session: session_id
        :return: словарь с общими параметрами для всех запросов
        """
        return {
            "state": 0,
            "session": session,
            "queries": [
                # query1, query2, ..., queryN будут присоединены к этому списку
            ]
        }
