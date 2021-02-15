#
# Copyright (c) 2020, Grigoriy Kramarenko
# All rights reserved.
# This file is distributed under the same license as the current project.
#
from types import GeneratorType
from hashlib import sha256
from importlib import import_module
from unidecode import unidecode


def import_string(dotted_path):
    """
    Import a dotted module path and return the attribute/class designated by the
    last name in the path. Raise ImportError if the import failed.
    """
    try:
        module_path, class_name = dotted_path.rsplit('.', 1)
    except ValueError as e:
        raise ImportError(
            "%s doesn't look like a module path." % dotted_path
        ) from e

    module = import_module(module_path)

    try:
        return getattr(module, class_name)
    except AttributeError as e:
        raise ImportError(
            'Module "%s" does not define a "%s" attribute/class' % (
                module_path, class_name)
        ) from e


def to_flat_list(data, skip=None, prebool=None, sort=False):
    """
    Преобразовывает многоуровневый объект в [отсортированный] плоский список.
    """
    result = []
    if skip is None:
        skip = ()
    if prebool is None:
        prebool = int

    def collect(item, prefix=''):
        if isinstance(item, dict):
            for key, value in item.items():
                if key in skip:
                    continue
                # Recursive collection for internal values.
                collect(value, prefix='%s%s:' % (prefix, key))
        elif isinstance(item, (list, tuple, range, GeneratorType)):
            for key, value in enumerate(item):
                # Recursive collection for internal values.
                collect(value, prefix='%s%d:' % (prefix, key))
        else:
            if isinstance(item, bool):
                value = prebool(item)
            else:
                value = item
            result.append('%s%s' % (prefix, str(value)))

    collect(data)
    if sort:
        result.sort()
    return result


def to_unique_string(data, skip=None, prebool=None, separator=';'):
    """
    Преобразовывает многоуровневый объект в уникальную строку.
    """
    if data is None:
        return ''
    elif isinstance(data, str):
        return data
    flat_list = to_flat_list(data, skip=skip, prebool=prebool, sort=True)
    return separator.join(flat_list)


def make_checksum(data, *args, **kwargs):
    uniq = to_unique_string(data, *args, **kwargs)
    return sha256(uniq.encode('utf-8')).hexdigest()


def prepare_dialog_name(s):
    """
    Преобразовывает имена разных алфавитов в латинницу и удаляет/заменяет
    лишние символы.
    """
    return unidecode(s).replace(' ', '_').replace('-', '_').replace("'", "")


def levenshtein_distance(text_1, text_2):
    """Алгоритм вычисления дистанции Левенштейна между двумя текстами."""

    length_1, length_2 = len(text_1), len(text_2)
    # Первым должен быть указан наименьший текст.
    if length_1 > length_2:
        text_1, text_2 = text_2, text_1
        length_1, length_2 = length_2, length_1

    current = range(length_1 + 1)
    for i in range(1, length_2 + 1):
        previous, current = current, [i] + [0] * length_1
        for j in range(1, length_1 + 1):
            add = previous[j] + 1
            delete = current[j - 1] + 1
            change = previous[j - 1]
            if text_1[j - 1] != text_2[i - 1]:
                change += 1
            current[j] = min(add, delete, change)
    return current[length_1]
