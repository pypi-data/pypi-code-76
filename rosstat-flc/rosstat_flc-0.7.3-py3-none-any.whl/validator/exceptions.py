class ValidationError(Exception):
    pass


# Format Exceptions


class FormatError(ValidationError):
    pass


class NotNumericValue(FormatError):
    msg = 'Значение не является числом'


class InvalidNumFormat(FormatError):
    msg = 'Число не соответствует формату'


class InvalidStrLength(FormatError):
    msg = 'Длина строки больше допустимого'


class OutOfDict(FormatError):
    msg = 'Значение не существует в справочнике'


class OutOfRange(FormatError):
    msg = 'Значение не входит в диапазон допустимых'


class OutOfList(FormatError):
    msg = 'Значение не входит в список допустимых'


class OutOfAdditionDict(FormatError):
    msg = 'Значение не существует в справочнике приложении'


class OutOfAdditionDictCoord(FormatError):
    msg = 'Недопустимое значение'


# Control Exceptions


class ControlError(ValidationError):
    pass


class PeriodCheckFail(ControlError):
    pass


class ConditionCheckFail(ControlError):
    pass


class RuleCheckFail(ControlError):
    def __init__(self, failed_controls):
        self.msg = failed_controls


class ConditionExprError(ControlError):
    msg = 'Ошибка разбора условия контроля'


class RuleExprError(ControlError):
    msg = 'Ошибка разбора правила контроля'


class PeriodExprError(ControlError):
    msg = 'Ошибка разбора формулы проверки периодичности'


class PrevPeriodNotImpl(ControlError):
    msg = 'Проверка со значениями из прошлого периода не реализована'
