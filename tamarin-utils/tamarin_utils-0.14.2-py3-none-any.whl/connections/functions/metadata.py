def get_metadata(locale, user=None, request_data=None):
    if user is None:
        user = {}
    return {
        "locale": locale,
        "user": {
            "id": user.get("id", None),
            "username": user.get("username", None)
        },
        'request_data': request_data if request_data else {},
        "transaction": []
    }
