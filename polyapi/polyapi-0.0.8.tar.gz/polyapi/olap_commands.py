# /usr/bin/python3
# -*- coding: utf-8 -*-
""" Создание команд модуля OLAP, 500"""
from . import precondition

import logging
from typing import Dict


class OlapCommands(precondition.Preconditions):
    """ Параметры для выполнения команд """
    def __init__(self, session_id: str, uuid: str, url: str, server_codes: Dict, jupiter: bool = False):
        """
        Инициализация класса OlapCommands
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
        self.params = self.common_request_params(self.session_id)
        self.olap_command_codes = self.server_codes["olap"]["command"]
        # Флаг работы в Jupiter Notebook
        self.jupiter = jupiter

    def collect_command(self, module: str, command_name: str, state: str, **kwargs) -> [Dict, str]:
        """
        парсит server_codes.json и возвращает словарь с обязательными параметрами (plm_type_code, state)
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

    def multisphere_data(self, multisphere_module_id: str, view: Dict) -> [Dict, str]:
        """
        Параметры должны включать:
        command: 502 (dimension), его state ID
        command: 503 (fact), его state ID
        command: 506 (view), его state ID
        прямоуголные значения (int): "from_row", "from_col", "num_row", "num_col"
        :param multisphere_module_id: id модуля мультисферы
        :param view: (dict) {"from_row": value, "from_col": value, "num_row": value, "num_col": value}
        :return: (dict) dimensions, facts and other data
        """
        assert "from_row" in view, "key 'from_row' was not added in param: view"
        assert "from_col" in view, "key 'from_col' was not added in param: view"
        assert "num_row" in view, "key 'num_row' was not added in param: view"
        assert "num_col" in view, "key 'num_col' was not added in param: view"

        params = self.common_request_params(self.session_id)

        commands = ["dimension", "fact", "view"]

        for index, item in enumerate(commands):
            try:
                command = {
                    "plm_type_code": self.olap_command_codes[item]["id"],
                    "state": self.olap_command_codes["dimension"]["state"]["list_rq"]
                }
            except KeyError as e:
                logging.exception("EXCEPTION!!! No such command/state in server_codes.json: %s", e)
                logging.info("APPLICATION STOPPED")
                if self.jupiter:
                    return "EXCEPTION!!! No such command/state in server_codes.json: %s" % e
                raise
            if command["plm_type_code"] == 506:
                command.update(view)
            query = {
                "uuid": multisphere_module_id,
                "command": command
            }
            params["queries"].append(query)
            params["queries"][index]["command"] = command

        return params
