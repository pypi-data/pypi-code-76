from flask_cors import CORS


def error_handler(app, simple_cors: bool = True):
    if simple_cors:
        CORS(app, supports_credentials=True)

    @app.errorhandler(400)
    def handle_400_error(error):
        return '请求参数错误', 400, []

    @app.errorhandler(403)
    def handle_403_error(error):
        return '资源不可用', 403, []

    @app.errorhandler(404)
    def handle_404_error(error):
        return '资源不存在', 404, []

    @app.errorhandler(406)
    def handle_406_error(error):
        return '不支持所需表示', 406, []

    @app.errorhandler(409)
    def handle_409_error(error):
        return '发生冲突', 409, []

    @app.errorhandler(412)
    def handle_412_error(error):
        return '前置条件失败', 412, []

    @app.errorhandler(415)
    def handle_415_error(error):
        return '不支持收到的表示', 415, []

    @app.errorhandler(500)
    def handle_500_error(error):
        return '服务内部错误', 500, []

    @app.errorhandler(503)
    def handle_503_error(error):
        return '服务无法处理请求', 503, []

    @app.errorhandler(504)
    def handle_504_error(error):
        return '服务网关超时', 504, []
