from flask_templates import FlaskTemplate
from flask_templates.common.logger import logger
from flask_templates.common.class_holder import ClassHolder
from flask_templates.nacosinstance import NacosClient
from flask_templates.configs import BASE_CONFIG

FlaskTemplate.fresh_scope()
ClassHolder().put(NacosClient(only_reader=True))



def sum(a,b):
    logger.info(BASE_CONFIG.get("db-master-port"))
    return a+b