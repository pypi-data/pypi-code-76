from ..configs import BASE_CONFIG

# web服务
WEB_CONFIG = BASE_CONFIG.get('web', {})
# template config
TEMPLATE_CONFIG = BASE_CONFIG.get('flask_template', {})
# 日志
LOG_CONFIG = TEMPLATE_CONFIG.get('log', {})
# requester
REQUESTER_CONFIG = TEMPLATE_CONFIG.get('requester', {})
# celery
CELERY_CONFIG = BASE_CONFIG.get('celery', {})
# 数据库
DB_CONFIG = TEMPLATE_CONFIG.get('db', {})
# mysql
MYSQL_CONFIG = DB_CONFIG.get('mysql', {})
# USE_SLAVE_CONFIG = DB_CONFIG.get('use_slave')
# SLAVE_MYSQL_CONFIG = DB_CONFIG.get('slave_mysql')
# redis
REDIS_CONFIG = DB_CONFIG.get('redis', {})


def config_fix():
    global TEMPLATE_CONFIG, LOG_CONFIG, WEB_CONFIG, DB_CONFIG, MYSQL_CONFIG, REDIS_CONFIG, REQUESTER_CONFIG,CELERY_CONFIG
    TEMPLATE_CONFIG = BASE_CONFIG.get('flask_template', {})
    LOG_CONFIG = TEMPLATE_CONFIG.get('log', {})
    REQUESTER_CONFIG = TEMPLATE_CONFIG.get('requester', {})
    DB_CONFIG = TEMPLATE_CONFIG.get('db', {})
    MYSQL_CONFIG = DB_CONFIG.get('mysql', {})
    REDIS_CONFIG = DB_CONFIG.get('redis', {})
    WEB_CONFIG = BASE_CONFIG.get('web', {})
    CELERY_CONFIG = BASE_CONFIG.get('celery', {})
