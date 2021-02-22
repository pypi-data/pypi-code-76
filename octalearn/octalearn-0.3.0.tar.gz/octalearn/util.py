import os


def is_pymodule(path_to_module):
    path_to_module_init = os.path.append(path_to_module, '__init__.py')

    return (
            os.path.isdir(path_to_module)
        and os.path.isfile(path_to_module_init)
    )


def package_from_path(path_to_package):
    if is_pymodule(path_to_package):
        package_name = os.path.basename(path_to_package)
        package_path = os.path.dirname(path_to_package)

        return (package_name, package_path)

    return ('', '')
