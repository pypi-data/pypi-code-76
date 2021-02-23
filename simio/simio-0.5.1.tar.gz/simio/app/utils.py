import pkgutil
from importlib import import_module


def initialize_all_modules(init_module_name: str):
    """
    Runs all modules to execute decorators and register routes
    """
    init_module = import_module(init_module_name)
    for _, module_name, is_package in pkgutil.iter_modules(init_module.__path__):
        absolute_module_name = f"{init_module_name}.{module_name}"

        import_module(absolute_module_name)

        if is_package:
            initialize_all_modules(absolute_module_name)
