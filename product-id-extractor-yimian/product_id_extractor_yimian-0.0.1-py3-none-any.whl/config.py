class Config(object):
    RULES = {
        "tmall_taobao": r"id=\w+",
        "jd_suning": r"[^/]*\.html",
        "amazon": r"dp/\w+",
    }