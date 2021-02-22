class Config(object):
    RULES = {
        "tmall": r"detail\.tmall\.com\/item\.htm\S*[\&|\?]id=(\d+)",
        "taobao": r"item\.taobao\.com\/item\.htm\S*[\&|\?]id=(\d+)",
        "suning": r"product\.suning\.com\S*\/(\d+)\.html",
        "jd": r"item\.jd\.com\/(\d+)\.html",
        "amazon": r"amazon\.\S*\/dp\/(\w+)",
    }

