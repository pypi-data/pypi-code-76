import re

directRules = {
    "naniplay": (re.compile(r"https://(?:www\.)?naniplay(?:\.nanime\.(?:in|biz)|\.com)/file/[^>]+"), "_fembed"),
    "layarkacaxxi": (re.compile(r"https://layarkacaxxi\.icu/f/[^>]+"), "_fembed"),
    "zippyshare": (re.compile(r"https://www\d+\.zippyshare\.com/v/[^/]+/file\.html"), "_zippyshare"),
    "mediafire": (re.compile(r"https://(?:www\.)?mediafire\.com/file/[^>]+"), "_mediafire"),
    "linkpoi": (re.compile(r"https://linkpoi\.me/[^>]+"), "_linkpoi"),
    "uservideo": (re.compile(r"https://uservideo\.xyz/file/[^>]+"), "_linkpoi"),
    "ouo": (re.compile(r'https://ouo\.io/[^>]+'), None)
}

allDirectRules = re.compile(
    r"|".join(v.pattern for v, _ in directRules.values()))
