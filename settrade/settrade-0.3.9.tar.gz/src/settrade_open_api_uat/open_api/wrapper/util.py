def send_python_error(err):
    return {
        "success": False,
        "data": {},
        "message": str(err),
        "status_code": 500,
    }
