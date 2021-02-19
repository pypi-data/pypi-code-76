from pathlib import Path

TEST_DIR = Path(__file__).parent
INPUT_DATA_DIR = TEST_DIR / 'input_data'
GENERATED_DATA_DIR = TEST_DIR / 'generated_data'

DATA_NAME = 'data'
JSON_PATH = INPUT_DATA_DIR / (DATA_NAME + '.json')
YAML_PATH = INPUT_DATA_DIR / (DATA_NAME + '.yaml')
TOML_PATH = INPUT_DATA_DIR / (DATA_NAME + '.toml')
ENV_PATH = GENERATED_DATA_DIR / '.env'
CUSTOM_CONFIG_OUT_PATH = GENERATED_DATA_DIR / 'config'

if not INPUT_DATA_DIR.exists():
    INPUT_DATA_DIR.mkdir()
if not GENERATED_DATA_DIR.exists():
    GENERATED_DATA_DIR.mkdir()