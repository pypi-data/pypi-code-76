"""
Generate test data for file output
"""
from tests.config import INPUT_DATA_DIR, DATA_NAME, JSON_PATH, YAML_PATH, TOML_PATH
from tests.fixtures.model import get_model_object

if __name__ == "__main__":
    conf = get_model_object()
    conf.to_json(out_path=JSON_PATH, json_kwargs=dict(indent=2))
    conf.to_yaml(out_path=YAML_PATH)
    conf.to_toml(out_path=TOML_PATH)
