# /usr/bin/python3
# -*- coding: utf-8 -*-
""" Модуль авторизации в Полиматике """
import requests
import time
import json
from typing import Tuple, Dict


class Authorization:
    """ Предоставляет возможность авторизации в Полиматике """

    def login(self, user_name: str, url: str, server_codes: Dict, password: str = None, language: str = None) -> Tuple:
        """
        Авторизация (парольная/беспарольная).
        :param user_name: имя пользователя
        :param password: пароль
        :param url: базовый URL стенда
        :param server_codes: значение файла "server_codes.json" (хранит коды команд и их состояний)
        :param language: "en" / "ru" / "de" / "fr"
        :return: (Tuple) session_id, uuid/manager_id, func_timing
        """
        start_time = time.time()

        # для авторизации с паролем
        session = ""

        auth_manager_command = server_codes.get("manager", {}).get("command", {}).get("authenticate", {})
        auth_command = auth_manager_command.get("id")
        auth_check = auth_manager_command.get("state", {}).get("check")
        auth_login = auth_manager_command.get("state", {}).get("login")
        language = server_codes.get("locale", {}).get(language)

        # для авторизации без пароля
        if password is None:
            # формирование id сессии
            url = url + "/login"
            payload = {"login": user_name}
            r = requests.get(url=url, params=payload)
            try:
                response = r.json()
            except json.decoder.JSONDecodeError:
                message = "Host {} not supporting non-password authorization. Please, specify the password!".format(
                    url
                )
                raise ValueError({'message': message})
            if len(r.history) > 0:
                for resp in r.history:
                    session = resp.cookies.get("session")
            else:
                session = response.get("session")

        # формирование command
        command = {"plm_type_code": auth_command}
        if password is None:
            # для авторизации без пароля добавить в command состояние check
            command.update({"state": auth_check})
        else:
            # для авторизации с паролем добавить в command следующие параметры
            command.update({"state": auth_login, "login": user_name, "passwd": password, "locale": language})

        # формирование params
        params = {
            "state": 0,
            "session": session,
            "queries": [
                # query1, query2, ..., queryN will be appended in this list
            ]
        }
        query = {"uuid": "00000000-00000000-00000000-00000000", "command": command}
        params["queries"].append(query)

        # отправляем запрос аутентификации на заданный URL
        r = requests.request(method="POST", url=url, json=params, timeout=60.0)

        # проверки
        session_id, uuid = self._authorization_checks(params, r.json(), r.status_code)

        end_time = time.time()
        func_timing = '{:s} func exec time: {:.2f} sec'.format("login", (end_time - start_time))
        return session_id, uuid, func_timing

    def _get_command(self, data: Dict) -> Dict:
        """
        Возвращает команду запроса/ответа.
        """
        queries = next(iter(data.get("queries")))
        return queries.get("command")

    def _authorization_checks(self, request: Dict, response: Dict, response_code: int) -> Tuple:
        """
        Проверка успешности авторизации. Возвращает идентификатор сессии и manager uuid.
        :param request: (Dict) запрос
        :param response: (Dict) ответ
        :param response_code: (int) код ответа
        :return: (Tuple) идентификатор сессии, uuid
        """
        # получаем команды и коды запроса/ответа
        request_command = self._get_command(request)
        request_code = request_command.get("plm_type_code")
        resp_command = self._get_command(response)
        resp_code = resp_command.get("plm_type_code")

        # проверки полученных кодов
        assert "error" not in resp_command, resp_command.get("error")
        assert response_code == 200, "Response code != 200"
        assert request_code == resp_code, "plm_type_code in request (%s) != plm_type_code (%s) in response!" % \
                                        (request_code, resp_code)

        # извлекаем идентификаторы
        session_id = resp_command.get("session_id")
        uuid = resp_command.get("manager_uuid")

        # проверки идентификаторов
        assert session_id != "", "session_id == empty string"
        assert session_id is not None, "session_id is None!"
        assert uuid != "", "manager_id == empty string"
        assert uuid is not None, "manager_id is None!"

        return session_id, uuid
