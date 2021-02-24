"""
shirkhan 专用 hasklib 库，sk 来自 shir-s, khan ->k
使用sk前缀是因为hashlib和系统hashlib模块名冲突
"""
import hashlib


def md5(text: str, encoding="utf-8"):
    return hashlib.md5(text.encode(encoding)).hexdigest()


if __name__ == '__main__':
    pass
    text = "abc"
    print(md5(text))
