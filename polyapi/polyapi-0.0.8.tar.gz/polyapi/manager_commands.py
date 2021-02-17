# /usr/bin/python3
# -*- coding: utf-8 -*-
""" Создание команд модуля Менеджер, 200 """
from . import precondition

from typing import Dict
import logging


class ManagerCommands(precondition.Preconditions):
    """ Параметры для выполнения команд """
    def __init__(self, session_id: str, uuid: str, url: str, server_codes: Dict, jupiter: bool = False):
        """
        Инициализация класса Manager
        :param session_id: id сессии
        :param uuid: (manager) id
        :param url: базовый URL
        :param server_codes: server_codes.json
        :param jupiter: jupiter
        """
        super().__init__(url)
        self.server_codes = server_codes
        self.uuid = uuid
        self.session_id = session_id
        # Флаг работы в Jupiter Notebook
        self.jupiter = jupiter

    def collect_command(self, module: str, command_name: str, state: str, **kwargs) -> [Dict, str]:
        """
        Распарсить server_codes.json и возвращает словарь с обязательными параметрами (plm_type_code, state)
        :param module: название модуля (Менеджер, 200; OLAP, 500; graph, 600; maps, 700; association, 800; cluster, 900;
                    forecast, 1000)
        :param command_name: название команды
        :param state: название состояния
        :param kwargs: все остальные (необязательные) поля
        :return: (dict) {"plm_type_code": ..., "state": ...}
        """
        query = {
            "uuid": self.uuid,
            "command": "your command"
        }

        # добавляет обязательные поля в словарь, который вернет метод:
        try:
            command = {
                "plm_type_code": self.server_codes[module]["command"][command_name]["id"],
                "state": self.server_codes[module]["command"][command_name]["state"][state]
            }
        except KeyError as e:
            error_msg = 'No such command/state in server_codes.json: "{}"'.format(e.args[0])
            logging.exception("EXCEPTION! {}".format(error_msg))
            logging.info("APPLICATION STOPPED")
            if self.jupiter:
                return "EXCEPTION! {}".format(error_msg)
            raise ValueError(error_msg)
        # если указаны необязательные параметры...
        for i in kwargs:
            if state == "apply_data":
                command.update({"from": 0})
            command.update({i: kwargs[i]})  # ...добавялем их в возвращаемое значение
        # если необязательных полей нет: в словаре останутся только обязательные поля plm_type_code, state
        query["command"] = command
        return query

    def collect_request(self, *args) -> Dict:
        """
        Формирование запроса
        :param args: команды
        :return: конечный запрос
        """
        params = self.common_request_params(self.session_id)
        for query in args:
            params["queries"].append(query)
        return params
