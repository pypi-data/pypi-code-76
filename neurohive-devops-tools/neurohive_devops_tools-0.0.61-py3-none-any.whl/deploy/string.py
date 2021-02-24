from hashlib import md5
import re


def slugify(original: str):
    filtered = "".join(list(map(lambda c: c if c.isalnum() else '-', original)))
    filtered = re.sub(r'[\-]+', '-', filtered)
    str_chunk = filtered[:26]
    # костыль для совместимости с баш версией. можно убрать, после передеплоя всех окружений
    original += '\n'
    str_md5 = md5(original.encode()).hexdigest()[:5]
    return  f'{str_chunk}-{str_md5}'
