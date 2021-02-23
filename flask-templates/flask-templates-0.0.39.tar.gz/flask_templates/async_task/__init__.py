from celery import Celery
from flask_templates.configs import config_update, BEFORE_CONFIG, template
from importlib import import_module
"""
run 'celery -A flask_templates.async_task.cele worker -l INFO  -P gevent  -c 10' in windows
monitor 'celery flower --broker=redis://r2.dsjcj.cc:10168/2'
"""

if template.CELERY_CONFIG.pop("enable",False):
    cele = Celery(__name__, broker=template.CELERY_CONFIG['broker_url'])
    cele.conf.update(template.CELERY_CONFIG)
else:
    cele = Celery()

@cele.task
def async_tasker(func,*args,**kwargs):
    module,func = func.rsplit(".", maxsplit=1)
    func_m = import_module(module)
    return getattr(func_m,func)(*args,**kwargs)

if __name__ == '__main__':
    pass