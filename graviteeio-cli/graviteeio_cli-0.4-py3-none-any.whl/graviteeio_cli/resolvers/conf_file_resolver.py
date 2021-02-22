import logging
import os
import enum

from jinja2 import (Environment, FileSystemLoader, TemplateNotFound)

from graviteeio_cli.exeptions import GraviteeioError
from graviteeio_cli.extensions.jinja_filters import filter_loader
from graviteeio_cli.commands.apim.apis.utils import update_dic_with_set
from graviteeio_cli.core.file_format import File_Format_Enum
from graviteeio_cli.resolvers.conf_resolver import CONFIG_FORMATS, ConfigResolver

from graviteeio_cli import environments as env
from . import init_templates as init_tpl

logger = logging.getLogger("class-config__file_resolver")


class Config_Type(enum.Enum):
    API = {
        "conf_file_name": env.API_CONFIG_FILE_NAME,
        "init_config": init_tpl.templates_api
    }

    APP = {
        "conf_file_name": env.APP_CONFIG_FILE_NAME,
        "init_config": init_tpl.templates_app
    }

    def __init__(self, values):
        self.conf_file_name = values['conf_file_name']
        self.init_config = values['init_config']


class ConfigFileResolver(ConfigResolver):

    def _load_template(self, config_type: Config_Type):
        full_conf_file_name = None

        conf_file_name = config_type.conf_file_name
        conf_file_path = f"{self.folders['templates_folder']}/{conf_file_name}"
        # root_template_path_file = self.files["root_template_path_file"]

        for (data_format, extention) in ((data_format, extention) for data_format in CONFIG_FORMATS for extention in data_format.extentions):
            if not full_conf_file_name and os.path.exists(conf_file_path.format(extention)):
                self.config_format = data_format
                full_conf_file_name = conf_file_name.format(extention)

            if full_conf_file_name:
                break

        if not full_conf_file_name:
            raise GraviteeioError("Missing file {} or {}".format(
                conf_file_name.format(".yml"),
                conf_file_name.format(".json"))
            )

        self.templates[config_type.name] = self._get_template(full_conf_file_name, self.folders["templates_folder"])

    def _get_template(self, full_config_file_name, templates_folder):
        j2_env = Environment(loader=FileSystemLoader(templates_folder), trim_blocks=False, autoescape=False)
        filter_loader(j2_env)

        try:
            template = j2_env.get_template(full_config_file_name)
        except TemplateNotFound:
            raise GraviteeioError("Template not found, try to load {}".format(full_config_file_name))

        return template

    def _validate_folder(self):
        for key in self.folders:
            if not os.path.exists(self.folders[key]):
                raise GraviteeioError(f"Missing folder {self.folders[key]}")

    def _get_values_file(self, resources_folder, file_path):
        values_file_path = None
        values_file_format: File_Format_Enum = None

        if not file_path or len(file_path) == 0:
            partial_path = '{}/{}'.format(
                resources_folder,
                env.GIO_VALUE_FILE_NAME
            )

            for (data_format, extention) in ((data_format, extention) for data_format in CONFIG_FORMATS for extention in data_format.extentions):
                file = partial_path.format(extention)
                if not values_file_path and os.path.exists(file):
                    values_file_format = data_format
                    values_file_path = file

                if values_file_path:
                    break

            if not values_file_path:
                raise GraviteeioError("Missing file {} or {}".format(
                    env.GIO_VALUE_FILE_NAME.format(".yml"),
                    env.GIO_VALUE_FILE_NAME.format(".json"))
                )
        else:
            if os.path.exists(file_path):
                filename, file_extension = os.path.splitext(file_path)

                values_file_path = file_path
                values_file_format = File_Format_Enum.find(file_extension)
            else:
                raise GraviteeioError(f"Not file found [{file_path}]")

        return {"path": values_file_path, "format": values_file_format}

    def _read_file(self, file, format: File_Format_Enum):
        content_file = None
        try:
            with open(file, 'r') as f:
                # api_value_string = f.read()
                content_file = f.read()
        except OSError:
            raise GraviteeioError("Cannot open file {}".format(file))

        return format.load(content_file)

    def _get_vars(self, value_file_path, value_file_format: File_Format_Enum):
        vars: dict = {}

        vars["Values"] = self._read_file(value_file_path, value_file_format)

        settings_folder = self.folders["settings_folder"]
        for file in os.listdir(settings_folder):
            if not file.startswith(('_', ".")):
                try:
                    with open("/".join([settings_folder, file]), 'r') as f:
                        config_string = f.read()
                except OSError:
                    raise GraviteeioError("Cannot open {}".format(file))

                filename, file_extension = os.path.splitext(file)
                file_format = File_Format_Enum.find(file_extension)

                if file_format:
                    vars[filename] = file_format.load(config_string)

        return vars

    def generate_init(self, config_type: Config_Type, format=File_Format_Enum.YAML, config_values=None, debug=False):
        for key in self.folders:
            if debug:
                print("mkdir {}".format(self.folders[key]))
            else:
                try:
                    os.mkdir(self.folders[key])
                except OSError:
                    print("Creation folder [%s] failed" % self.folders[key])
                else:
                    print("Successfully created directory %s " % self.folders[key])

        conf_file_path = f"{self.folders['templates_folder']}/{config_type.conf_file_name}"

        if not config_values:
            tpl = config_type.init_config[format.name.lower()]["template"]
            values = config_type.init_config[format.name.lower()]["value_file"]
        else:
            tpl = format.dump(config_values)
            values = ""

        write_files = {
            conf_file_path.format(format.extention): tpl,
        }

        setting_files = config_type.init_config[format.name.lower()]["setting_files"]
        for file, tpl_value in setting_files.items():
            path = "{}/{}".format(self.folders["settings_folder"], file.format(format.extention))
            write_files[path] = tpl_value

        for key in write_files:
            if debug:
                print("write file {}".format(key))
            else:
                try:
                    with open(key, 'x') as f:
                        f.write(write_files[key])
                except OSError:
                    print("Creation of the file %s failed" % key)
                else:
                    print("Successfully created file %s " % key)

        # write values file
        values_file_path = self.values_file["path"].format(format.extention)
        if os.path.exists(values_file_path):
            values = '\n' + values
        try:
            with open(values_file_path, 'a') as f:
                f.write(values)
        except OSError:
            print("Creation of the file %s failed" % key)
        else:
            print("Successfully created file %s " % key)


    # def _api_def_to_template(self, api_def, format):
    #     values = {}

    #     values["version"] = api_def["version"]
    #     values["name"] = api_def["name"]
    #     values["description"] = api_def["description"]

    #     api_def["version"] = "{{ Values.version}}"
    #     api_def["name"] = "{{ Values.name}}"
    #     api_def["description"] = "{{ Values.description}}"

    #     write_files = {
    #         self.files["root_template_path_file"].format(format.extentions[0]): format.dump(api_def),
    #         self.files["value_file"].format(format.extentions[0]): format.dump(values),
    #         "{}/{}".format(self.folders["settings_folder"], "Http{}".format(format.extentions[0])): ""
    #     }

    #     return write_files