#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
Используемые переменные класса BusinessLogic:
# язык интерфейса. Задается при авторизации. Возможно задать значения: "ru", "en", "de" или "fr"
self.language = "ru"

# базовый URL для работы
self.url = url

# словарь команд и состояний server-codes.json
self.server_codes

# id сессии
self.session_id

# uuid, который возвращается после авторизации
self.authorization_uuid

# список слоев сессии
self.layers_list

# id мультисферы
self.cube_id

# используемый id слоя
self.active_layer_id

# данные мультисферы в формате словаря {"dimensions": "", "facts": "", "data": ""}
self.multisphere_data

# для хранения названия мультисферы
self.cube_name = ""

# если запускается скрипт из Jupiter Notebook. По умолчанию = False
self.jupiter = False

# значение присвается в случае аварийного завершения работы
# может быть удобно при работе в Jupiter Notebook
self.current_exception = None

# общее количество строк текущей рабочей области
self.total_row = 0

# для измерения вреимени работы функций бизнес-логики
self.func_timing = 0

# записать имя функции для избежания конфликтов с декоратором
self.func_name = ""


:param login: логин пользователя Полиматика
:param url: URL стенда Полиматика
:param password: (необязательный) пароль пользователя Полиматика
:param session_id: (необязательный) id сессии
:param authorization_id: (необязательный) id авторизации
:param timeout: таймауты. по умолчанию = 60.0
:param jupiter: (bool) если запускается скрипт из Jupiter Notebook. По умолчанию = False
"""

__name__ = "BusinessLogic"
