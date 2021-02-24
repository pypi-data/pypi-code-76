
# import dxclient
# from . import __config
"""
Tests:

Инициализация
    1. Создан ли дефолтный глобальный класс без sdk_key при инициализации? +
    2. Включены ли логи +
    3. Включен ли уровень логов INFO -
    4. url api == 'api.deploy-x.com

Установка конфига как класса Config()
    1. С валидным ключом
    2. С нулевым ключом
    3. С другим типом ключа

Установка конфига как словарь
    1. С валидным ключом
    2. С нулевым ключом
    3. С другим типом ключа

Установка просто ключа
    1. С валидным ключом
    2. С нулевым ключом
    3. С другим типом ключа
"""
# ==============================================================
from . import *

@pytest.fixture(scope='class')
def config_instance():
    return dxclient.config.Config()

@pytest.fixture(scope='class')
def client_instance():
    config = dxclient.config.Config()
    return dxclient.client.DXClient(config)

    
@pytest.mark.usefixtures('config_instance', 'client_instance')
class TestDxclientInitialization:

    def test_is_config_instance_created(self, config_instance):
        assert isinstance(config_instance, config.Config) == True
        assert config_instance.sdk_key == None

    def test_logging_is_working(self):    
        if logging.getLogger():
            assert True
        else:
            assert False
    
    # def test_logging_lever(self):
    #     assert logging.getLogger().level == 40

    
