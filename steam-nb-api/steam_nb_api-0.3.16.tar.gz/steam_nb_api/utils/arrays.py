from py4j.java_gateway import launch_gateway, java_import, JavaGateway, JavaObject, GatewayParameters, Py4JNetworkError

def create_hyper_line_array(gateway, args):
    HyperLine = gateway.jvm.model.geometry.basic.HyperLine
    if type(args) is tuple:
        hl_array = gateway.new_array(HyperLine, len(args))
        for i in range(len(args)):
            hl_array[i] = args[i]
    else:
        hl_array = gateway.new_array(HyperLine, 1)
        hl_array[0] = args
    return hl_array

def create_element_array(gateway, args):
    Element = gateway.jvm.model.geometry.Element
    if type(args) is tuple:
        el_array = gateway.new_array(Element, len(args))
        for i in range(len(args)):
            el_array[i] = args[i]
    else:
        el_array = gateway.new_array(Element, 1)
        el_array[0] = args
    return el_array

def create_string_array(gateway, args):
    if any(var_type is type(args) for var_type in [tuple, list]):
        el_array = gateway.new_array(gateway.jvm.String, len(args))
        for i in range(len(args)):
            el_array[i] = args[i]
    else:
        el_array = gateway.new_array(gateway.jvm.String, 1)
        el_array[0] = args
    return el_array

def create_double_array(gateway, args):
    if type(args) is tuple:
        el_array = gateway.new_array(gateway.jvm.double, len(args))
        for i in range(len(args)):
            el_array[i] = args[i]
    else:
        el_array = gateway.new_array(gateway.jvm.double, 1)
        el_array[0] = args
    return el_array

def create_int_array(gateway, args):
    if type(args) is tuple:
        el_array = gateway.new_array(gateway.jvm.int, len(args))
        for i in range(len(args)):
            el_array[i] = args[i]
    else:
        el_array = gateway.new_array(gateway.jvm.int, 1)
        el_array[0] = args
    return el_array

def create_domain_array(gateway, args):
    Domain = gateway.jvm.model.domains.Domain
    if type(args) is tuple:
        el_array = gateway.new_array(Domain, len(args))
        for i in range(len(args)):
            el_array[i] = args[i]
    else:
        el_array = gateway.new_array(Domain, 1)
        el_array[0] = args
    return el_array

def create_area_array(gateway, args):
    Area = gateway.jvm.model.geometry.basic.Area
    if type(args) is tuple:
        el_array = gateway.new_array(Area, len(args))
        for i in range(len(args)):
            el_array[i] = args[i]
    else:
        el_array = gateway.new_array(Area, 1)
        el_array[0] = args
    return el_array

def convert_list_to_double_array(gateway, arg):
    el_array = gateway.new_array(gateway.jvm.Double, len(arg))
    for i in range(len(arg)):
        el_array[i] = float(arg[i])
    return el_array

def convert_list_to_string_array(gateway, arg):
    el_array = gateway.new_array(gateway.jvm.String, len(arg))
    for i in range(len(arg)):
        el_array[i] = arg[i]
    return el_array

def create_winding_array(gateway, args):
    Winding = gateway.jvm.model.geometry.coil.Winding
    if type(args) is tuple:
        el_array = gateway.new_array(Winding, len(args))
        for i in range(len(args)):
            el_array[i] = args[i]
    else:
        el_array = gateway.new_array(Winding, 1)
        el_array[0] = args
    return el_array

def create_pole_array(gateway, args):
    Pole = gateway.jvm.model.geometry.coil.Pole
    if type(args) is tuple:
        el_array = gateway.new_array(Pole, len(args))
        for i in range(len(args)):
            el_array[i] = args[i]
    else:
        el_array = gateway.new_array(Pole, 1)
        el_array[0] = args
    return el_array

def parse_java_array(java_array):
    rows = len(java_array)
    cols = len(java_array[0])
    
    array = [[0 for x in range(rows)] for y in range(cols)] 
    
    for i in range(rows):
        for j in range(cols):
            array[i][j] = java_array[i][j]
    return array

def create_double_2D_array(gateway, input_array):
    output_array = gateway.new_array(gateway.jvm.Double, len(input_array), len(input_array[0]))
    for r in range(len(input_array)):
        for c in range(len(input_array[r])):
            output_array[r][c] = input_array[r][c]
    return output_array

def create_unboxed_double_2D_array(gateway, input_array):
    output_array = gateway.new_array(gateway.jvm.double, len(input_array), len(input_array[0]))
    for r in range(len(input_array)):
        for c in range(len(input_array[r])):
            output_array[r][c] = input_array[r][c]
    return output_array