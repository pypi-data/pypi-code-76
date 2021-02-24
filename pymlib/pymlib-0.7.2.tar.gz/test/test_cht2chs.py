# coding: utf-8

"""
繁体转简体中文
"""

import mlib.utils

if __name__ == "__main__":
    src = "圖案, 大麥"
    dst = mlib.utils.cht_to_chs(src)
    print(src, dst)