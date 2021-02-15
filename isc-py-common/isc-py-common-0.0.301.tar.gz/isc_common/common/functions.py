import logging
import re

from django.db import connection

from isc_common.number import ToStr

logger = logging.getLogger(__name__)


def uncapitalize(str):
    return str[0:1].lower() + str[1:]


def dbl_qutes_str(str):
    return f'"{str}"'


def qutes_str(str):
    return f"'{str}'"


def delete_dbl_spaces(value):
    if value is None:
        return value

    if not isinstance(value, str):
        return ToStr(value)

    value = value.replace('\\n', ' ')
    return re.sub('\s+', ' ', value).strip()


def null2blanck(str):
    return '' if str == 'null' else str


def ExecuteStoredProc(storedProcName, parametrs):
    c = connection.cursor()
    try:
        # c.execute("BEGIN")
        res = c.callproc(storedProcName, parametrs)
        results, = c.fetchone()
        # c.execute("COMMIT")
        return results
    except Exception as ex:
        logger.error(ex)
        raise ex
    finally:
        c.close()


def ExecuteStoredProcRows(storedProcName, parametrs):
    c = connection.cursor()
    try:
        # c.execute("BEGIN")
        res = c.callproc(storedProcName, parametrs)
        results = c.fetchall()
        # c.execute("COMMIT")
        return results
    except Exception as ex:
        logger.error(ex)
        raise ex
    finally:
        c.close()


class Common:
    @classmethod
    def get_size_file_str(cls, value):
        if value == 0:
            return ""

        if value > 0 and value <= 1024:
            return f'{value} Байт'

        if value > 1024 and value <= 1024 * 1024:
            return f'{round(value / 1024, 2)} КБайт'

        if value > 1024 * 1024 and value <= 1024 * 1024 * 1024:
            return f'{round(value / 1024 / 1024, 2)} МБайт'

        if value > 1024 * 1024 * 1024:
            return f'{round(value / 1024 / 1024 / 1024, 2)}  ГБайт'
        return value

    @classmethod
    def arraund_error(error):
        str = '!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!'
        return f'\n{str}\n{error}\n{str}'
