from metafunctions import node
import sys
import inspect 
import dis
from collections import defaultdict
import types



def get_python_file_path():
    #Sub-optimal way to get current working script (NOT superfunctions, the one that imported superfunctions) 
    #because it might not work in some instances, see this comment:
    # https://stackoverflow.com/a/35514032
    script_name_that_was_invoked_from_command_line = sys.argv[0]
    return script_name_that_was_invoked_from_command_line

def get_python_file_contents(filepath):
    f = open(filepath, 'r')
    python_text = f.read()
    f.close()
    return python_text

def get_list_of_imported_modules():
    file_path = get_python_file_path()
    python_file_contents = get_python_file_contents(file_path) 
    instructions = dis.get_instructions(python_file_contents)
    imports = [__ for __ in instructions if 'IMPORT' in __.opname]
    import_dict = defaultdict(list)
    for instr in imports:
        import_dict[instr.opname].append(instr.argval)
    list_of_imported_modules = import_dict.get('IMPORT_NAME')

    return list_of_imported_modules

def get_list_of_imported_functions():
    '''
    file_path = get_python_file_path()
    python_file_contents = get_python_file_contents(file_path) 
    instructions = dis.get_instructions(python_file_contents)
    imports = [__ for __ in instructions if 'IMPORT' in __.opname]
    import_dict = defaultdict(list)
    for instr in imports:
        import_dict[instr.opname].append(instr.argval)
    list_of_imported_functions = import_dict.get('IMPORT_FROM')
    '''
    list_of_imported_functions = []
    for key, value in locals().items():
        #print(key, value)
        if callable(value) and value.__module__ == __name__:
            list_of_imported_functions.append(key)

    return list_of_imported_functions

#print(get_list_of_imported_functions())



def is_string(thing):
    if isinstance(thing, str):

        return True
    else:
 
        return False

def convert_module_string_to_module(module_name):
    try:
        if is_string(module_name):
            module = sys.modules[module_name]
            return module
        else:
            return
    except KeyError:
        pass



#print([str(m) for m in sys.modules])
def decorate_module(module, decorator):
    module = convert_module_string_to_module(module)
    for name, member in inspect.getmembers(module):
        if inspect.getmodule(member) == module and callable(member):
            if member == decorate_module or member == decorator:
                continue
            module.__dict__[name] = decorator(member)

def get_all_classes_of_module(module):
    list_of_classes = []
    for name, obj in inspect.getmembers(module):
        if inspect.isclass(obj):
            list_of_classes.append(obj)
    return list_of_classes

def decorate_all_methods_in_module(module, decorator):
    module = convert_module_string_to_module(module)
    types_of_functions = [types.FunctionType, 
    types.BuiltinFunctionType, types.BuiltinMethodType,
    types.MethodType,
    types.MethodDescriptorType, types.ClassMethodDescriptorType,
    types.DynamicClassAttribute]

    list_of_classes = get_all_classes_of_module(module)
    for class_ in list_of_classes:
        list_of_names_and_functions = inspect.getmembers(class_)
        for name, obj in list_of_names_and_functions:
            if not name.startswith('__') and not name.endswith('__'):
                list_of_checks_to_see_if_function = []
                for type_of_function in types_of_functions:
                    list_of_checks_to_see_if_function.append(isinstance(obj, type_of_function))
                if any(list_of_checks_to_see_if_function):
                    #if name == 'sin':
                        #print('Decorating sin')
                    #if name == 'tan':
                        #print('decorating tan')
                    #Should module be class_ instead?
                    try:

                        setattr(class_, name, decorator(obj))
                        
                    except TypeError:
                        pass
                    #setattr(module, name, decorator(obj))
        #print('Skipped:', skipping)


def decorate_all_functions_in_module(module, decorator):
    module = convert_module_string_to_module(module)
    types_of_functions = [types.FunctionType, 
    types.BuiltinFunctionType, types.BuiltinMethodType,
    types.MethodType,
    types.MethodDescriptorType, types.ClassMethodDescriptorType,
    types.DynamicClassAttribute]

    for name in dir(module):
        if not name.startswith('__') and not name.endswith('__'):

            obj = getattr(module, name)
            list_of_checks_to_see_if_function = []
            for type_of_function in types_of_functions:
                list_of_checks_to_see_if_function.append(isinstance(obj, type_of_function))
            if any(list_of_checks_to_see_if_function):
                try:
                    setattr(module, name, decorator(obj))
                except:
                    pass
                

def decorate_all_modules():
    list_of_imported_modules = get_list_of_imported_modules()
    for module_name in list_of_imported_modules:
        if module_name != 'decorate_module' and module_name != 'superfunctions' and module_name != 'metafunctions':
            if not module_name.startswith('__') and not module_name.endswith('__'):
                decorate_all_functions_in_module(module_name, node)
                decorate_all_methods_in_module(module_name, node)
                
