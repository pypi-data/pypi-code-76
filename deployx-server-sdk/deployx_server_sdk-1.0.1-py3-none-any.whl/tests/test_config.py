from . import *

@pytest.fixture()
def ready_config():
    # need every time create new object of Config class with blank sdk_key
    config = dxclient.config.Config()
    return config

# test configs
class TestSetSdkKeyFunction:
    
    def test_init_config(self, ready_config):
        assert ready_config.sdk_key == None
        assert ready_config.offline == False
        # assert ready_config.api_url == 'api.deploy-x.com'

    # test set_sdk_key() function
    def test_install_valid_sdk_key(self, ready_config):
        ready_config.set_sdk_key('4bd7c57120acf64056da4847c64c60c5d1536e9f948c6b3c9d4d37e6804eb2ee')
        assert ready_config.sdk_key == '4bd7c57120acf64056da4847c64c60c5d1536e9f948c6b3c9d4d37e6804eb2ee'

    def test_install_wrong_sdk_key(self, ready_config):
        with pytest.raises(AttributeError) as e: 
            ready_config.set_sdk_key(1212123)

    def test_install_blank_sdk_key(self, ready_config):
        with pytest.raises(TypeError) as e:
            ready_config.set_sdk_key()


def get_config_objects():
    """ return attrs for parametrize in functions """
    i_config = config.Config(sdk_key='QWERTTYU')
    return [
        (i_config, 'QWERTTYU'), 
        ({'sdk_key': '3e2269e0666dfb82ff059438586f585e21c6b158d55c17c0a3fc7f5dbc74e018',}, '3e2269e0666dfb82ff059438586f585e21c6b158d55c17c0a3fc7f5dbc74e018')
    ]

def get_blank_objects():
    """ return attrs for parametrize in functions """
    i_config = config.Config(sdk_key='')
    return [
        (i_config, None), 
        ({'sdk_key': '',}, None)
    ]

def get_nonexistent_params():
    """ return try to install nonexistent params into config """
    i_config = config.Config(sdk_key='test_sdk_key')
    nonexist_params = {
        'at1': '123',
        'at2': '123'
    }
    i_config.set_config(nonexist_params)
    return [
        (i_config, None), 
        ({ 'sdk_key': 'test_sdk_key', 'at1': '123' }, None)
    ]

def get_unavailable_attrs():
    """ return try to install unavailable params into config """
    i_config = config.Config(sdk_key='test_sdk_key')
    nonexist_params = {
        'api_url': '228',
        'api_port': '1337',
        'sdk_key': 'test_sdk_key'
    }
    i_config.set_config(nonexist_params)
    return [
        (i_config, None), 
        (nonexist_params, None)
    ]

class TestSetConfigFunctionDict:

    @pytest.mark.parametrize("config, expected", get_config_objects())
    def test_set_valid_dict_config(self, config, expected, ready_config):
        ready_config.set_config(config)
        assert ready_config.sdk_key == expected
        # assert ready_config.username == "captainkryuk"
    
    @pytest.mark.parametrize("config, expected", get_blank_objects())
    def test_set_blank_sdk_key(self, config, expected, ready_config):
        """ test with blank sdk_key """
        ready_config.set_config(config) 
        assert ready_config.sdk_key == expected

    @pytest.mark.parametrize("config, expected", get_nonexistent_params())
    def test_nonexistent_attrs_config(self, config, expected, ready_config):
        """ Test with nonexist attributes """
        ready_config.set_config(config)
        assert ready_config.sdk_key == 'test_sdk_key'
        assert hasattr(ready_config, 'at1') == False
    
    @pytest.mark.parametrize("config, expected", get_unavailable_attrs())
    def test_unavailable_attrs(self, config, expected, ready_config):
        """ Test with unavailable params. They are exist in class, but they can't be changed """
        ready_config.set_config(config)
        assert ready_config.api_url == '127.0.0.1'
        assert ready_config.sdk_key == 'test_sdk_key'


