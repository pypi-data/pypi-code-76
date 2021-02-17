import os_xml_handler.xml_handler as xh
from os_android_app_automation.bp import _res as res
from os_android_app_version_changer import version_changer
from os_android_app_version_changer.objs.VersionProperties import VersionProperties
from os_file_stream_handler import  file_stream_handler as fsh


# will set the dependencies of the project to be as the user required
def set_dependencies(project_build_gradle, dependencies_nodes):
    dependencies_str = ''
    for dependency_node in dependencies_nodes:
        dependencies_str += xh.get_text_from_node(dependency_node)

    input_build_gradle_lines = fsh.read_text_file(project_build_gradle)
    output_build_gradle_lines = []
    for line in input_build_gradle_lines:
        output_build_gradle_lines.append(line)
        if 'dependencies' in line:
            output_build_gradle_lines.append(dependencies_str)
            output_build_gradle_lines.append('\n}')
            break
    fsh.write_file(project_build_gradle, output_build_gradle_lines)


# will set the versions of the project to be as the user required
def set_versions(project_path, logger, version_name, version_code):
    version_name = _fix_version_value(logger, res.VERSION_NAME, version_name)
    version_code = _fix_version_value(logger, res.VERSION_CODE, version_code)
    version_properties = VersionProperties(version_code, version_name)
    version_changer.change_version(project_path, version_properties)


# will fix the version value to be as the VersionProperties require
def _fix_version_value(logger, version_type, version_value):
    if version_value is None or version_value == res.TAG_VERSION_KEEP:
        logger.info(f'{version_type} is None: keeping the same properties')
        return VersionProperties.KEEP_OLD_VERSION
    elif version_value == res.TAG_VERSION_RAISE:
        logger.info(f'Raising {version_type} by 1')
        return VersionProperties.RAISE_VERSION_BY_ONE
    return version_value
