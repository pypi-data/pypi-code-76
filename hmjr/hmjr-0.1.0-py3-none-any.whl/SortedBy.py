from functools import cmp_to_key

class By:
    def header():
        return lambda a: a["header"]
    def date():
        return cmp_to_key(lambda a, b: -1 if len(a["dates"]) < 1 else 1 if len(b["dates"]) < 1 else 1 if a["minDate"]["year"] < b["minDate"]["year"] else -1 if a["minDate"]["year"] > b["maxDate"]["year"] else 1 if a["minDate"]["month"] < b["minDate"]["month"] else -1 if a["minDate"]["month"] > b["maxDate"]["month"] else 1 if a["minDate"]["day"] < b["maxDate"]["day"] else -1)

