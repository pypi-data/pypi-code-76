class Config(object):
    RULES = {
        "tmall": r"detail\.tmall\.com\/item\.htm\S*[\&|\?]id=(\w+)",
        "taobao": r"item\.taobao\.com\/item\.htm\S*[\&|\?]id=(\w+)",
        "suning": r"product\.suning\.com\S*\/(\w+)\.html",
        "jd": r"item\.jd\.com\/(\w+)\.html",
        "amazon": r"amazon\.co\.uk\/\S*\/dp\/(\w+)",
    }

# https://list.jd.com/list.html?cat=13765,15155,15179
# 