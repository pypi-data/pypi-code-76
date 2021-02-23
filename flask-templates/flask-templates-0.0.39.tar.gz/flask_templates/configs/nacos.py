from ..configs import BEFORE_CONFIG

# nacos服务
NACOS_CONFIG = BEFORE_CONFIG.get('nacos', {})


def config_fix():
    global NACOS_CONFIG
    NACOS_CONFIG = BEFORE_CONFIG.get('nacos', {})
