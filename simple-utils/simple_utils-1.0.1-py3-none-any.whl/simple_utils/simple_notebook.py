from . import simple_structure
import argparse

def is_notebook():
    try:
        get_ipython()
        return True
    except NameError:
        return False

def parse_arguments(param={}, description=""):
    namespace = {}

    default_args = {
        "help": "",
        "required": True
    }
    
    for name, user_args in param.items():
        if not isinstance(user_args, dict):
            param[name] = {
                "default":user_args
            }

    if not is_notebook():
        parser = argparse.ArgumentParser(description=description)

        for name, user_args in param.items():
            args = default_args.copy()
            args.update(user_args)
            print(args)

            parser.add_argument(f"--{name}", **args)

        namespace = parser.parse_args()

    else:
        for name, user_args in param.items():
            namespace[name] = user_args["default"]
            
        namespace = simple_structure.dotdict(namespace)

    return namespace
