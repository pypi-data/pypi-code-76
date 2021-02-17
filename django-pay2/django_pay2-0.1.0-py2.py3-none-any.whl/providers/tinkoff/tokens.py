import hashlib


def build_token(data, password):
    prep_data = {k: v for k, v in data.items() if k not in ["Receipt", "Data", "Token"]}
    prep_data["Password"] = password
    sorted_data = {k: prep_data[k] for k in sorted(prep_data.keys())}
    hash_str = "".join(_to_json_str(v) for v in sorted_data.values())
    hash_obj = hashlib.sha256(hash_str.encode("utf-8"))
    return hash_obj.hexdigest()


def _to_json_str(value):
    if isinstance(value, bool):
        return _bool_to_str(value)
    return str(value)


def _bool_to_str(a_bool):
    return str(a_bool).lower()
