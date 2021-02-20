from flask import current_app


class EnvHelper:
    """
    环境变量工具
    """
    @classmethod
    def env(cls):
        return current_app.config['ENV']

    @classmethod
    def is_dev(cls):
        return cls.env() == "dev"

    @classmethod
    def is_test(cls):
        return cls.env() == "testing"

    @classmethod
    def is_prod(cls):
        return cls.env() == "production"

    @classmethod
    def is_for_test(cls):
        """
        是否是用于测试, 包含 dev test
        :return:
        """
        return not cls.is_prod()

    @classmethod
    def is_postman(cls, ua):
        return cls.is_for_test() and 'PostmanRuntime' in ua
