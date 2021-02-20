from dataclasses import dataclass


class Status:
    """Утвержденные стандарт используемых статусов в Компании"""

    NEW = 'NEW'  # Активное. требует изменения на INPR
    IN_PROCESS = 'INPR'  # Активное. требует изменения на: FAIL или SCS
    SUCCESS = 'SCS'  # Активное. блокирует создание нового события
    FAILURE = 'FAIL'  # Активное. блокирует создание нового события
    ERROR = 'ERROR'  # Активное. Последнее событие завершилось ситемной ошибкой, бизнес-результат не известен
    CANCEL = 'CANCEL'  # Не активно. Отменяет предыдущий статус. В comment пишется предыдущий статус
    STATUS_CHOICES = {
        (NEW, 'Новый'),
        (IN_PROCESS, 'В процессе'),
        (SUCCESS, 'Успех'),
        (FAILURE, 'Неудача'),
        (ERROR, 'Системная ошибка'),
        (CANCEL, 'Статус отменен')
    }


class Country:
    """Страны присутствия Компании"""

    RUSSIA = 'RU'
    KAZAKHSTAN = 'KZ'
    COUNTRY_CHOICES = [
        (RUSSIA, 'Россия'),
        (KAZAKHSTAN, 'Казахстан'),
    ]


class Loan:
    """Виды займов"""

    PAYDAY_LOAN = 'PDL'
    INSTALLMENT_LOAN = 'IL'
    LOAN_CHOICES = [
        (PAYDAY_LOAN, 'Payday loan'),
        (INSTALLMENT_LOAN, 'Installment loan')
    ]


class Document:
    PASSPORT = 'PP'
    DRIVING_LICENCE = 'DL'
    SNILS = 'SNILS'
    TAX_ID = 'TAX_ID'
    DOCUMENT_CHOICES = [
        (PASSPORT, 'Паспорт'),
        (DRIVING_LICENCE, 'Выдительские права'),
        (SNILS, 'СНИЛС'),
        (TAX_ID, 'ИНН'),
    ]


class Months:
    """Месяцы года"""
    RUSSIA_MONTHS_CHOICES = {
        1: 'Январь', 2: 'Февраль', 3: 'Март', 4: 'Апрель',
        5: 'Май', 6: 'Июнь', 7: 'Июль', 8: 'Август',
        9: 'Сентябрь', 10: 'Октябрь', 11: 'Ноябрь', 12: 'Декабрь'
    }


@dataclass
class Result(Status):
    """Формат ответа адапетров"""

    status: str
    comment: any

    def __init__(self, status, comment=None):
        assert status in [
            self.NEW,
            self.IN_PROCESS,
            self.SUCCESS,
            self.FAILURE,
            self.ERROR,
            self.CANCEL
        ], 'Wrong status'
        self.status = status
        self.comment = comment
