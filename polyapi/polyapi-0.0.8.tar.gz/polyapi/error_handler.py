# /usr/bin/python3
# -*- coding: utf-8 -*-
""" Модуль обработки ошибок из ответа """
import re
import requests
import datetime
from typing import Dict, Tuple


def request_asserts(response: Dict, r: requests.models.Response) -> bool:
    """
    Проверка ответов сервера
    :param response: (dict) ответ сервера, r.json()
    :param r: <class 'requests.models.Response'>
    :return: True / False
    """
    # парсинг ответа
    resp_queries = response.get("queries")
    resp_error = response.get("error")
    resp_err_code = resp_error.get("code")
    resp_queries = next(iter(resp_queries))  # [0] element in vector
    resp_command = resp_queries.get("command")
    resp_command_err = resp_command.get("error")

    assert len(resp_queries) > 0, resp_error
    assert resp_command, resp_command_err
    assert r.status_code == 200, "Response code != 200"
    assert resp_err_code == 0, "error code in response != 0. Err code: %s" % resp_err_code
    if "error" in resp_command:
        resp_command_err_code = resp_command_err.get("code")
        resp_command_err_message = resp_command_err.get("message")

        assert resp_command_err_code == 0, "ERROR in response: %s" % resp_command_err_message

    if ("error" in resp_command) and ("status" in resp_command):
        resp_command_status = resp_command.get("status")
        resp_command_status_code = resp_command_status.get("code")
        resp_command_status_message = resp_command_status.get("message")

        assert resp_command_status_code == 0, \
            "ERROR in response: %s" % resp_command_status_message

    if ("error" in resp_command) and ("datasources" in resp_command):
        resp_command_datasources = resp_command.get("datasources")
        resp_command_datasources = next(iter(resp_command_datasources))  # [0] element in vector
        datasources_status = resp_command_datasources.get("status")
        datasources_status_code = datasources_status.get("code")
        resp_command_status_message = datasources_status.get("message")

        assert datasources_status_code == 0, "ERROR in response: %s" % resp_command_status_message

    return True


def checks(self, func_name, *args):
    """
    Проверки
    :param self: экземпляр класса BusinessLogic
    :param func_name: название функции
    :param args: прочие параметры
    :return:
    """
    if func_name == "rename_group":
        group_uuid = args[0]
        group_name = args[1]
        if not group_uuid:
            raise ValueError("No such group: %s " % group_name)
        return True
    if func_name == "move_dimension":
        if self.multisphere_module_id == "":
            raise ValueError("First create cube and get data from it!")
        position = args[0]
        if position == "left":
            return 1
        elif position == "up":
            return 2
        elif position == "out":
            return 0
        raise ValueError('Position "{}" does not exist! Position can only be "up", "left" or "out"!'.format(position))
    elif func_name == "polymatica_health_check_multisphere_updates":
        cubes_list = args[0]
        cube_name = args[1]
        for cube in cubes_list:
            if cube["name"] == cube_name:
                return True
        raise ValueError("No such cube in cubes list: %s" % cube_name)
    elif func_name == "get_measure_name":
        if self.multisphere_module_id == "":
            raise ValueError("First create cube and get data from it!")
        return True
    elif func_name == "rename_dimension":
        dim_name = args[0]
        if not isinstance(dim_name, str):
            raise ValueError('Dimension copy name [%s] is not valid. It should have "string" type' % dim_name)
        return True
    elif func_name == "select_all_dims":
        left_dims = args[0]
        if not left_dims:
            raise ValueError("Left dimension required")
        return True
    elif func_name == "get_dim_name":
        if self.multisphere_module_id == "":
            raise ValueError("First create cube and get data from it!")
        return True
    elif func_name == "set_measure_visibility":
        is_visible = args[0]
        if not isinstance(is_visible, bool):
            raise ValueError("is_visible param can only be boolean: True / False")
        return True
    elif func_name == "sort_measure":
        is_visible = args[0]
        if is_visible not in ("ascending", "descending"):
            raise ValueError("sort_type can only equals 'ascending' OR 'descending'!")
        return True
    elif func_name == "unfold_all_dims":
        position = args[0]
        if position == "left":
            return 1
        elif position == "up":
            return 2
        raise ValueError("Position %s does not exist! position can only be 'up' or 'left'!" % position)
    elif func_name == "set_width_columns":
        measures, measures_list = args[0], args[1]
        if len(measures) != len(measures_list):
            raise ValueError("Количество колонок (параметр measures) должно совпадать с количеством фактов!")
        return True
    elif func_name == "put_dim_filter":
        filter_name, start_date, end_date, months, week_days = args[0], args[1], args[2], args[3], args[4]
        if (filter_name is None) and (start_date is None and end_date is None):
            raise ValueError("If you don't filter one value by param filter_name,"
                             " please assign value to args start_date AND end_date!")
        elif (filter_name is not None) and (start_date is not None and end_date is not None):
            raise ValueError("Please, fill in arg filter_name for filtering one value OR:\n"
                             "args start_date AND end_date for filtering date interval!")

        # список для заполнения данными
        dates_list = []

        # Заполнение списка dates_list в зависимости от содержания параметров filter_name, start_date, end_date
        # заполнить список для недельного интервала
        if (filter_name is None) and (start_date is not None and end_date is not None):
            if (start_date in week_days) and (end_date in week_days):
                start_ind = week_days.index(start_date)
                end_ind = week_days.index(end_date)
                if start_ind > end_ind:
                    raise ValueError("Start week day can not be more than the end week day!")
                dates_list = week_days[start_ind:end_ind + 1]
            # заполнить список для месячного интервала
            elif (start_date in months) and (end_date in months):
                start_ind = months.index(start_date)
                end_ind = months.index(end_date)
                if start_ind > end_ind:
                    raise ValueError("Start month can not be more than the end month!")
                dates_list = months[start_ind:end_ind + 1]
            # Заполнение списка с интервалом числовых дат
            elif isinstance(start_date, int) and isinstance(end_date, int):
                if start_date > end_date:
                    raise ValueError("Start date can not be more than the end date!")
                end_date += 1
                dates_list = [str(x) for x in range(start_date, end_date)]  # list with dates to filter
            # заполнение списка в формате ЧЧ.ММ.ГГГГ, ЧЧ:ММ:СС
            elif (re.search(r'(\d+.\d+.\d+, \d+:\d+:\d+)', start_date) is not None) and \
                    (re.search(r'(\d+.\d+.\d+, \d+:\d+:\d+)', end_date) is not None):
                start = datetime.datetime.strptime(start_date, "%d.%m.%Y, %H:%M:%S")
                end = datetime.datetime.strptime(end_date, "%d.%m.%Y, %H:%M:%S")
                if start > end:
                    raise ValueError("Start date can not be more than the end date!")
                step = datetime.timedelta(days=1)
                while start <= end:
                    date = start.strftime("%d.%m.%Y, %H:%M:%S")
                    dates_list.append(date)
                    start += step
            # заполнение списка в формате ГГГГ-ММ-ДД ЧЧ:ММ:СС
            elif (re.search(r'(\d+-\d+-\d+ \d+:\d+:\d+)', start_date) is not None) and \
                    (re.search(r'(\d+-\d+-\d+ \d+:\d+:\d+)', end_date) is not None):
                start = datetime.datetime.strptime(start_date, "%Y-%m-%d %H:%M:%S")
                end = datetime.datetime.strptime(end_date, "%Y-%m-%d %H:%M:%S")
                if start > end:
                    raise ValueError("Start date can not be more than the end date!")
                step = datetime.timedelta(days=1)
                while start <= end:
                    date = start.strftime("%Y-%m-%d %H:%M:%S")
                    dates_list.append(date)
                    start += step
            # заполнение списка в формате ГГГГ-ММ-ЧЧ
            elif (re.search(r'(\d+-\d+-\d+)', start_date) is not None) and \
                    (re.search(r'(\d+-\d+-\d+)', end_date) is not None):
                start = datetime.datetime.strptime(start_date, "%Y-%m-%d")
                end = datetime.datetime.strptime(end_date, "%Y-%m-%d")
                if start > end:
                    raise ValueError("Start date can not be more than the end date!")
                step = datetime.timedelta(days=1)
                while start <= end:
                    date = start.strftime("%Y-%m-%d")
                    dates_list.append(date)
                    start += step
            # заполнение списка в формате ЧЧ.ММ.ГГГГ
            elif (re.search(r'(\d+.\d+.\d+, \d+:\d+:\d+)', start_date) is None) and \
                    (re.search(r'(\d+.\d+.\d+)', start_date) is not None) and \
                    (re.search(r'(\d+.\d+.\d+)', end_date) is not None):
                start = datetime.datetime.strptime(start_date, "%d.%m.%Y")
                end = datetime.datetime.strptime(end_date, "%d.%m.%Y")
                if start > end:
                    raise ValueError("Start date can not be more than the end date!")
                step = datetime.timedelta(days=1)
                while start <= end:
                    date = start.strftime("%d.%m.%Y")
                    dates_list.append(date)
                    start += step
            else:
                raise ValueError("Unknown date format!")
        return dates_list
    elif func_name == "export":
        file_format = args[0]
        if file_format not in ["csv", "xls", "json"]:
            raise ValueError("Wrong file format: %s" % file_format)
        return True
    elif func_name == "run_scenario":
        scenario_id, scenario_name = args[0], args[1]
        if (scenario_id is None) and (scenario_name is None):
            raise ValueError("Нужно ввести либо uuid, либо название сценария!")
        return True
    elif func_name == "set_measure_precision":
        measure_names, precision = args[0], args[1]
        if len(measure_names) != len(precision):
            raise ValueError("Длина списка с названиями фактов (%s) != длине списка с размерностями (%s)!" %
                             (len(measure_names), len(precision)))
        return True
    elif func_name == "create_sphere":
        if len(args) == 1:
            i = args[0]
            # проверка есть ли в названиях размерностей и фактов метка порядка байтов U + FEFF Byte Order МАРК (BOM)
            if "\ufeff" in i["name"]:
                raise ValueError("Измените кодировку исходного файла на UTF-8 без BOM!")
            if "\ufeff" in i["db_field"]:
                raise ValueError("Измените кодировку исходного файла на UTF-8 без BOM!")
            return True

        update_params, updates, file_type, sql_params, user_interval, interval, period, week, time_zones, source_name,\
            cube_name = args[0], args[1], args[2], args[3], args[4], args[5], args[6], args[7], args[8], args[9],\
            args[10]

        # проверка, что создается мультисфера с уникальным названием
        if "not found" not in self.get_cube_without_creating_module(cube_name):
            raise ValueError("Multisphere %s already exists!" % cube_name)

        if len(cube_name) < 5:
            raise ValueError("Название мультисферы должно состоять из 5 и более символов!")

        # проверка заданного вида обновления
        if update_params["type"] not in updates:
            raise ValueError("Обновление '%s' не существует!" % update_params["type"])

        # проверка корректности параметров в словаре sql_params
        if (file_type != "excel") and (file_type != "csv"):
            if sql_params is None:
                raise ValueError("If your sourse is sql: fill in param sql_params!\n\n"
                                 "In other cases: it is wrong param file_type: %s\n\nIt can be only:\n"
                                 "excel OR csv" % file_type)
            if ("server" not in sql_params) or ("login" not in sql_params) or ("passwd" not in sql_params) \
                    or ("sql_query" not in sql_params):
                raise ValueError(
                    "Please check the following params names in sql_params:\n-server\n-login\n-passwd\n-sql_query")

        if user_interval not in interval:
            raise ValueError("No such interval: %s" % user_interval)

        # проверка длины и отствия пробелов в имени источника
        if len(source_name) < 5:
            raise ValueError("Имя источника должно состоять из 5 и более символов!")
        if " " in source_name:
            raise ValueError("Знак <ПРОБЕЛ> не должен быть в Имени источника!")

        if update_params["type"] != "ручное":
            # проверка корректности введенной часовой зоны
            if update_params["schedule"]["time_zone"] not in time_zones:
                raise ValueError("Time zone %s does not exist!" % update_params["schedule"]["time_zone"])
            # проверка периода, дня недели:
            if update_params["schedule"]["type"] not in period:
                raise ValueError("Нет периода: %s !" % update_params["schedule"]["type"])
            if "week_day" in update_params["schedule"]:
                if update_params["schedule"]["week_day"] not in week:
                    raise ValueError("Неверный день недели: %s !" % update_params["schedule"]["week_day"])
            if "day" in update_params["schedule"]:
                if update_params["schedule"]["day"] > 31:
                    raise ValueError("Неверный день месяца: %s !" % update_params["schedule"]["day"])
        return True
    elif func_name == "execute_olap_command":
        if self.multisphere_module_id == "":
            raise ValueError("First create cube and get data from it!")
        return True
    elif func_name == 'load_sphere_chunk':
        units = args[0]
        is_int = False
        error_msg = 'Param "units" must be a positive integer number!'
        try:
            is_int = int(units) == float(units)
        except ValueError:
            raise ValueError(error_msg)
        if not is_int or int(units) <= 0:
            raise ValueError(error_msg)
    else:
        raise ValueError("No function to check: %s" % func_name)
