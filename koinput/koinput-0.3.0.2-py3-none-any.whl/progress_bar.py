import sys
import ctypes
import math


# TODO: сделать отдельный стиль для текста и прогресс бара
# TODO: сделать стили сегментов прогресс бара
# TODO: если текст стиль или прогресс бар стиль не ноне консоль стиль не ноне всегда


class ProgressBar:
    max_value = 100
    counter = False
    string = "[########################################] @@@%"
    progressbar_symbol = "#"
    percent_symbol = "@"
    counter_separator = '/'

    @staticmethod
    def show(value, text=None):

        # Проверка существования processed_string
        try:
            str(ProgressBar.processed_string)
        except Exception:
            ProgressBar.processed_string = None

        # Проверка значений вводимых данных
        if type(ProgressBar.counter) != bool:
            raise ValueError('ProgressBar.counter must be bool')
        if type(ProgressBar.counter_separator) != str:
            raise ValueError('ProgressBar.counter_separator must be str')

        if ProgressBar.counter:  # если counter true то только int для value и max_value
            if type(value) != int and type(value) != float:
                raise ValueError('If ProgressBar.counter = True, then value must be int.')
            if type(ProgressBar.max_value) != int and type(ProgressBar.max_value) != float:
                raise ValueError('If ProgressBar.counter = True, then ProgressBar.max_value must be int.')
        else:
            if type(value) != int and type(value) != float:
                raise ValueError('value must be int or float')
            if type(ProgressBar.max_value) != int and type(ProgressBar.max_value) != float:
                raise ValueError('ProgressBar.max_value must be int or float')

        if type(ProgressBar.string) != str:
            raise ValueError('ProgressBar.string must be str')
        if type(ProgressBar.progressbar_symbol) != str:
            raise ValueError('ProgressBar.progressbar_symbol must be one element str')
        if type(ProgressBar.percent_symbol) != str:
            raise ValueError('ProgressBar.percent_symbol must be one element str')
        if len(ProgressBar.progressbar_symbol) != 1:
            raise ValueError('ProgressBar.progressbar_symbol must be one element str')
        if len(ProgressBar.percent_symbol) != 1:
            raise ValueError('ProgressBar.percent_symbol must be one element str')

        if value > ProgressBar.max_value:
            raise ValueError('value must be less than ProgressBar.max_value')

        # обработка изменения string
        if ProgressBar.string != ProgressBar.processed_string:

            # поиск прогресс бара
            symbol_was_found = False
            i = 0
            while i < len(ProgressBar.string):
                if ProgressBar.string[i] == ProgressBar.progressbar_symbol:
                    symbol_was_found = True
                    ProgressBar.progressbar_start = i
                    try:  # TODO: избавиться от этой херни
                        while ProgressBar.string[i] == ProgressBar.progressbar_symbol:
                            i += 1
                    except IndexError:
                        pass
                    ProgressBar.progressbar_length = i - ProgressBar.progressbar_start
                    break
                i += 1
            if not symbol_was_found:
                raise ValueError('ProgressBar.progressbar_symbol was not found in ProgressBar.string')

            # поиск процентов
            symbol_was_found = False
            i = 0
            while i < len(ProgressBar.string):
                if ProgressBar.string[i] == ProgressBar.percent_symbol:
                    symbol_was_found = True
                    ProgressBar.percent_start = i
                    try:
                        while ProgressBar.string[i] == ProgressBar.percent_symbol:
                            i += 1
                    except IndexError:
                        pass
                    ProgressBar.percent_length = i - ProgressBar.percent_start
                    if ProgressBar.percent_length < 2:
                        ProgressBar.percent_length = 2
                    break
                i += 1
            if not symbol_was_found:
                raise ValueError('ProgressBar.percent_symbol was not found in ProgressBar.string')

            ProgressBar.processed_string = ProgressBar.string
            # Очистка string
            ProgressBar.cleared_string = ProgressBar.string.replace(ProgressBar.progressbar_symbol, '')
            ProgressBar.cleared_string = ProgressBar.cleared_string.replace(ProgressBar.percent_symbol, '')
            # массив id символ старт
            ProgressBar.symbols_ids = sorted([id(ProgressBar.progressbar_start),
                                              id(ProgressBar.percent_start)],
                                             key=lambda x: ctypes.cast(x, ctypes.py_object).value)

        # изменение выходного string
        string = ProgressBar.cleared_string
        for operation_id in ProgressBar.symbols_ids:

            # ProgressBar.progressbar_start
            if operation_id == id(ProgressBar.progressbar_start):
                progressbar = ''
                percent = value / ProgressBar.max_value
                progressbar += '█' * math.floor(percent * ProgressBar.progressbar_length)
                if percent * ProgressBar.progressbar_length - math.floor(
                        percent * ProgressBar.progressbar_length) > 7 / 8:
                    progressbar += '▉'
                elif percent * ProgressBar.progressbar_length - math.floor(
                        percent * ProgressBar.progressbar_length) > 6 / 8:
                    progressbar += '▊'
                elif percent * ProgressBar.progressbar_length - math.floor(
                        percent * ProgressBar.progressbar_length) > 5 / 8:
                    progressbar += '▋'
                elif percent * ProgressBar.progressbar_length - math.floor(
                        percent * ProgressBar.progressbar_length) > 4 / 8:
                    progressbar += '▌'
                elif percent * ProgressBar.progressbar_length - math.floor(
                        percent * ProgressBar.progressbar_length) > 3 / 8:
                    progressbar += '▍'
                elif percent * ProgressBar.progressbar_length - math.floor(
                        percent * ProgressBar.progressbar_length) > 2 / 8:
                    progressbar += '▎'
                elif percent * ProgressBar.progressbar_length - math.floor(
                        percent * ProgressBar.progressbar_length) > 1 / 8:
                    progressbar += '▏'
                progressbar = progressbar + ' ' * (ProgressBar.progressbar_length - len(progressbar))
                string = string[0:ProgressBar.progressbar_start] + progressbar + string[ProgressBar.progressbar_start:]

            # ProgressBar.percent_start
            elif operation_id == id(ProgressBar.percent_start):
                if not ProgressBar.counter:
                    percent = value / ProgressBar.max_value * 100
                    if ProgressBar.percent_length != 2:
                        percent = str(float(round(percent * 10 ** (ProgressBar.percent_length - 2))) /
                                      10 ** (ProgressBar.percent_length - 2))
                    else:
                        percent = str(int(round(percent)))
                    string = string[0:ProgressBar.percent_start] + percent + string[ProgressBar.percent_start:]
                else:
                    string = string[0:ProgressBar.percent_start] + str(value) + ProgressBar.counter_separator + \
                             str(ProgressBar.max_value) + string[ProgressBar.percent_start:]

        # вывод
        text_string = ''
        if text is not None:
            text_string = text + ' ' * (len(string) - len(text) + 2) + '\n'

        sys.stdout.write(text_string + string + '\r')
        if value == ProgressBar.max_value:
            sys.stdout.write('\n')
