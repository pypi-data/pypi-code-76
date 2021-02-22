import re

directRules = {
  "_fembed": re.compile(r"https://(?:www\.naniplay\.com|layarkacaxxi.icu)/f/[^>]+"),
  "_zippyshare": re.compile(r"https://www\d+\.zippyshare\.com/v/[^/]+/file\.html"),
  "_mediafire": re.compile(r"https://(?:www\.)?mediafire\.com/file/[^>]+"),
  "_linkpoi": re.compile(r"https://linkpoi\.me/[^>]+"),
  "_ouo": re.compile(r'https://ouo\.io/[^>]+'),
  "_uservideo": re.compile(r"https://uservideo\.xyz/file/[^>]+")
}

allDirectRules = re.compile(r"|".join(v.pattern for v in directRules.values()))
