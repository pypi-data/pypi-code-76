from flask_templates.common.utils import module_import

module_import("nacos", sdk_name='nacos-sdk-python')

import nacos
import datetime
import yaml
from flask_templates.common.requester import ServiceRegisterCenter
from flask_templates.configs import BASE_CONFIG, config_update,config_replace
from flask_templates.configs.template import WEB_CONFIG
from flask_templates.configs.nacos import NACOS_CONFIG
from flask_templates.common.utils import read_yaml
from flask_templates.common.logger import logger
from flask_apscheduler import APScheduler

NAMESPACE = ""

# Set the following values if authentication mode is enabled on the server
USERNAME = None
PASSWORD = None


class NacosClient(ServiceRegisterCenter):

    def __init__(self, app=None, only_reader=False):
        self.app = app
        self.config = NACOS_CONFIG
        self.discovery_config = self.config.get('discovery', {})
        self.config_config = self.config.get('config', {})
        self.only_reader = only_reader or self.discovery_config.get("only_reader")
        self.pyctuator = None

        self.client = nacos.NacosClient(self.server_addr, namespace=NAMESPACE, username=USERNAME, password=PASSWORD)
        if self.config_enable:
            config_update(BASE_CONFIG, setting=self.get_config())
            config_replace(BASE_CONFIG)
        if self.discovery_enable and not self.only_reader:
            self.scheduler = getattr(self.app,"apscheduler") if self.app and getattr(self.app,"apscheduler",None) else APScheduler()
            self.__register(app=self.app)


    @property
    def server_addr(self):
        return self.config.get("server-addr")

    @property
    def discovery_enable(self):
        return self.discovery_config.get("enable", False)

    @property
    def config_enable(self):
        return self.config_config.get("enable", False)

    def get_config(self):
        config = {}
        if self.config_enable:
            default_data_id = "{}-{}.{}".format(WEB_CONFIG.get('service_name'), BASE_CONFIG.get("env", "dev"),
                                                self.config_config.get("file-extension", "yaml"))
            default_group = self.config_config.get("group", "default")
            config_str = self.client.get_config(data_id=default_data_id, group=default_group, timeout=None,
                                                no_snapshot=None)
            if config_str:
                config.update(yaml.safe_load(config_str))
            else:
                logger.warn("data-id {} does't has any content".format(default_data_id))
            extension_configs = self.config_config.get("extension-configs", [])
            for item in extension_configs:
                config_str = self.client.get_config(data_id=item['data-id'], group=item.get('group', default_group),
                                                    timeout=None,
                                                    no_snapshot=None)
                if config_str:
                    config.update(yaml.safe_load(config_str))
                else:
                    logger.warn("data-id {} does't has any content".format(item['data-id']))
        return config

    def __register(self, app=None):
        if app and self.discovery_config.get("boot_admin", False):
            module_import("pyctuator")
            from pyctuator.pyctuator import Pyctuator
            self.pyctuator = Pyctuator(
                app,
                WEB_CONFIG.get('service_name'),
                app_url="http://wealthwechat.dsjcj.cc",
                pyctuator_endpoint_url="http://wealthwechat.dsjcj.cc/pyctuator",
                # registration_url="http://wealth.afa.ai:10008/admin/instances"
                registration_url=None
            )
        self.client.add_naming_instance(service_name=WEB_CONFIG.get('service_name'), ip=WEB_CONFIG.get("service_ip"),
                                        port=WEB_CONFIG.get('service_port'), weight=1,
                                        cluster_name="DEFAULT",
                                        metadata={"preserved.register.source": "FLASK",
                                                  "management.context-path": "pyctuator"},
                                        enable=True, healthy=True,
                                        group_name=self.discovery_config.get("group", "default"))

    def nacos_heartbeat_func(self):
        self.client.send_heartbeat(WEB_CONFIG.get('service_name'), ip=WEB_CONFIG.get("service_ip"),
                                   port=WEB_CONFIG.get('service_port'),
                                   weight=1,
                                   cluster_name="DEFAULT",
                                   metadata={"preserved.register.source": "FLASK",
                                             "management.context-path": "pyctuator"},
                                   ephemeral=True, group_name=self.discovery_config.get("group", "default"))
        # print(".")

    def start_heartbeat(self, app=None, seconds=15):
        if self.discovery_enable and not self.only_reader:
            if self.discovery_config.get("boot_admin", False) and not self.pyctuator:
                module_import("pyctuator")
                from pyctuator.pyctuator import Pyctuator
                self.pyctuator = Pyctuator(
                    app,
                    WEB_CONFIG.get('service_name'),
                    app_url="http://wealthwechat.dsjcj.cc",
                    pyctuator_endpoint_url="http://wealthwechat.dsjcj.cc/pyctuator",
                    # registration_url="http://wealth.afa.ai:10008/admin/instances"
                    registration_url=None
                )
            self.scheduler.add_job(func=self.nacos_heartbeat_func, id='nacos_heartbeat', trigger='interval',
                                   seconds=seconds,
                                   replace_existing=True, start_date=datetime.datetime.now())
            if not self.scheduler.running:
                app.config['SCHEDULER_API_ENABLED'] = True
                self.scheduler.init_app(app=app if app else self.app)
                self.scheduler.start()

    def stop_heartbeat(self):
        if self.discovery_enable and not self.only_reader:
            self.scheduler.remove_all_jobs()
            self.scheduler.shutdown()

    def get_servers(self, service_name):
        return [(x['ip'], x['port']) for x in
                self.client.list_naming_instance(service_name,
                                                 group_name=self.discovery_config.get("group", "default"),
                                                 healthy_only=True)['hosts']]


if __name__ == '__main__':
    import time
    from flask_templates import FlaskTemplate

    client = NacosClient(FlaskTemplate().app)
    client.start_heartbeat()
    print(client.get_servers(WEB_CONFIG.get('service_name')))
    while True:
        time.sleep(1)
