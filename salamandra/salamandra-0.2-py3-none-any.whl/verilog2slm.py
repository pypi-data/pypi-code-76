from salamandra.lexer import Lexer
import sys, os
sys.path.append(os.path.abspath('..'))
import re
from .net import Net
from .bus import Bus
from .input import Input
from .output import Output
from .inout import Inout
from .component import Component


def get_verilog_tokens(is_std_cell=False):
    # return tokens for lexer to run with this
    verilog_tokens = {
        'root': [
            (r'\s*module\s+([\w$]+|\\\S+ )\s*(?:\((?:[\w$]+|\\\S+ |,|\s*)*\))?\s*;\s*', 'module', 'module'),
            (r'\s*/\*.*?\*/\s*', None),
            (r'//#+(.*)\n', 'metacomment'),
            (r'\s*//.*\n', None),
            (r'`.*\n', None),
            (r'\s*\(\s*\*[\s\S]*?\*\s*\)\s*', None),  # (*...*)
        ],
        'module': [
            (r'\s*\(\s*\*[\s\S]*?\*\s*\)\s*', None),  # (*...*)
            (r'\s*//.*\n', None),  # //...
            (r'\s*assign\s+', 'assign_start', 'assignments'),  # assign
            (r'\s*else\s+if\s+\([\S\s]*?\)\s[\S\s]*?;\s*', 'check'),  # else if (...) ...;
            (r'\s*function\s+[\S\s]*?endfunction\s*', None),  # function ... endfunction
            (r'\s*(input|inout|output)(\s+signed)?(?:\s+\[\s*(\d+)\s*:\s*0\s*\])?\s+([\w$]+|\\\S+ )\s*;\s*', 'module_port'),
            # (input) (signed)? [(31):0]? (A);
            (r'\s*(input|inout|output)(\s+signed)?(?:\s+\[\s*(\d+)\s*:\s*0\s*\])?\s+([\w$]+|\\\S+ )\s*,\s*', 'module_port',
             'port_cont'),
            # (input) (signed)? [(31):0]? (A),
            (r'\s*wire(\s+signed)?(?:\s+\[\s*(\d+)\s*:\s*0\s*\])?\s+([\w$]+|\\\S+ )\s*;\s*', 'module_wire'),
            # wire (signed)? [(31):0]? (A);
            (r'\s*((?:\w+|\\\S+)\s+(?:[\w$]+|\\\S+ )\s*\([\S\s]*?\)\s*;\s*)', 'instance'),
            # (\mux$ i_mux(...);)
            (r'/\*.*?\*/', None),
            (r'//#\s*{{(.*)}}\n', 'section_meta'),
            (r'\s*endmodule\s*', 'end_module', '#pop'),
        ],
        'port_cont': [
            (r'\s*(signed)?\s*(?:\[\s*(\d+)\s*:\s*0\s*\])?\s*([\w$]+|\\\S+ )\s*,?\s*', 'port_cont'),
            # (signed)? [(31):0]? (A),?
            (r'\s*,\s*', None),  # ,
            (r'\s*;\s*', None, '#pop'),  # ;
            (r'//.*\n', None),
            (r'\s*/\*.*?\*/\s*', None),
        ],
        'instance_ports': [
            # connect one thing
            (r'\s*\.([\w$]+|\\\S+ )\s*\(\s*{?\s*}?\s*\)\s*,?\s*', 'empty_pin'),  # .I(),? {}? -> I
            (r'\s*\.([\w$]+|\\\S+ )\s*\(\s*{?\s*(\d+)\'([bodhBODH])([a-fA-F0-9x]+)\s*}?\s*\)\s*,?\s*', 'connect_gnets'),
            # .I(2'b01),? {}? -> I,2,b,01/xx
            (r'\s*\.([\w$]+|\\\S+ )\s*\(\s*{?\s*([\w$]+|\\\S+ )\s*(?:\[\s*(\d+)\s*:?\s*(\d+)?\s*\])?\s*}?\s*\)\s*,?\s*',
             'connect'),
            # .I(A[2:0]) # .I(B),? # .I(A[2]),? {}? -> I,A,2?,0?
            (r'\s*\.([\w$]+|\\\S+ )\s*\(\s*{?\s*{\s*(\d+)\s*{\s*([\w$]+|\\\S+ )\s*}\s*}\s*}?\s*\)\s*,?\s*', 'connect_concat'),
            # .I({2{A}}) {}? -> I,2,A

            # connect many things
            (r'\s*\.([\w$]+|\\\S+ )\s*\(\s*{\s*(\d+)\'([bodhBODH])([a-fA-F0-9x]+)\s*,\s*', 'connect_many_gnets', 'bus_cont'),
            # .I({2'b01, -> I,2,b,01
            (r'\s*\.([\w$]+|\\\S+ )\s*\(\s*{\s*([\w$]+|\\\S+ )\s*(?:\[\s*(\d+)\s*:?\s*(\d+)?\s*\])?\s*,\s*', 'connect_many',
             'bus_cont'),
            # .I({A, # .I({A[2:0], # .I({A[2], -> I,A,2?,0?
            (r'\s*\.([\w$]+|\\\S+ )\s*\(\s*{s*{\s*(\d+)\s*{\s*([\w$]+|\\\S+ )\s*}\s*}\s*,\s*', 'connect_many_concat',
             'bus_cont'),  # .I({2{A}}, -> I,2,A

            (r'\s*,\s*', None),  # ,
            (r'\s*\)\s*;\s*', 'end_port', '#pop'),  # );
            (r'//.*\n', None),
            (r'\s*/\*.*?\*/\s*', None),
        ],
        'bus_cont': [
            (r'\s*(\d+)\'([bodhBODH])([a-fA-F0-9x]+)\s*,?\s*', 'connect_many_gnets_cont'),  # 2'b01,? -> 2,b,01
            (r'\s*([\w$]+|\\\S+ )\s*(?:\[\s*(\d+)\s*:?\s*(\d+)?\s*\])?\s*,?\s*', 'connect_many_cont'),
            # A,? # A[31:0],? # A[31],? -> A,2?,0?
            (r'\s*{\s*(\d+)\s*{\s*([\w$]+|\\\S+ )\s*}\s*}\s*,?\s*', 'connect_many_concat_cont',),
            # {2{A}},? -> 2,A

            (r'\s*,\s*', None),  # ,
            (r'\s*}\s*\)\s*', 'end_bus', '#pop'),  # })
            (r'//.*\n', None),
            (r'\s*/\*.*?\*/\s*', None),
        ],
        'assignments': [
            (r'\s*{?\s*(\d+)\'([bodhBODH])([a-fA-F0-9x]+)\s*,?\s*}?\s*', 'assign_cont_gnet'),
            # 1'b0 / 13'h0 {}? ,? -> size,radix,val
            (r'\s*{?\s*{\s*(\d+)\s*{\s*([\w$]+|\\\S+ )\s*}\s*}\s*,?\s*}?\s*', 'assign_cont_concat',),
            # {2{A}}  {}? ,?  -> 2,A
            (r'\s*{?\s*([\w$]+|\\\S+ )\s*(?:\[\s*(\d+)\s*:?\s*(\d+)?\s*\])?\s*,?\s*}?\s*', 'assign_cont_net'),
            # A\A[12]\A[12:0] {}? ,? -> A,12?,0?
            (r'\s*}\s*', None),
            (r'\s*,\s*', None),
            (r'\s*=\s*', 'assign_eq'),
            (r'\s*;\s*', 'assign_finish', '#pop'),
            (r'//.*\n', None),
            (r'\s*/\*.*?\*/\s*', None),
            (r'[\S\s]*?;\s*', 'assign_break', '#pop'),  # not regular assign !danger!
        ],
    }
    if is_std_cell is True:
        verilog_tokens['module'][2] = (r'\s*((assign)|(else\s+if))\s+[\S\s]*?;\s*', None)  # assign/else if ... ; #?|(if)
        del verilog_tokens['module'][3]  # remove assign/else if
        del verilog_tokens['module'][6:8]  # remove wire and instances
    return verilog_tokens


def verilog2slm_file(fname, is_std_cell=False, implicit_wire=False, verbose=False):
    '''Parse a named Verilog file

    Args:
      fname (str): File to parse.
      is_std_cell (bool): is STD cell (takes only I/O ports)
      implicit_wire (bool): add implicit wires
      verbose (bool): print warnings if exist
    Returns:
      List of parsed objects.
    '''
    if not is_verilog(fname):
        raise Exception(fname + ' is not a verilog file')
    # with open(fname, 'rb') as fh:
    #     text_ba = bytearray(fh.read())
    #     for i in range(len(text_ba)):
    #         if text_ba[i] is 0x80:
    #             text_ba[i] = 92
    #     text = text_ba.decode()
    with open(fname, 'rt') as fh:
        text = fh.read()

    return verilog2slm(text, is_std_cell, implicit_wire, verbose)


def verilog2slm(text, is_std_cell=False, implicit_wire=False, verbose=False):
    '''Parse a text buffer of Verilog code

    Args:
      text (str): Source code to parse
      is_std_cell (bool): is STD cell (takes only I/O ports)
      implicit_wire (bool): add implicit wires
      verbose (bool): print warnings if exist
    Returns:
      List of components objects.
    '''
    verilog_tokens_ = get_verilog_tokens(is_std_cell)  # get local verilog tokens
    lex = Lexer(verilog_tokens_)
    radix2bits = {'b': 2, 'o': 8, 'd': 10, 'h': 16}
    comp = None
    comps = []
    components = []
    text_subcomps = ''
    bus_cont = {}
    assign_dict = {}
    last_port_mode = None

    for pos, action, groups in lex.run(text):  # run lexer and search for match
        if action == 'module':  # initiate Component
            module_name = groups[0]
            if module_name in Component.all_components():
                if verbose:
                    print('Warning: component ' + module_name + ' already exist')
                comp = None
            else:
                comp = Component(module_name)
                if is_std_cell:
                    comp.set_is_physical(True)
            text_subcomps = ''

        elif comp is None:
            continue

        elif action in ['module_port', 'port_cont']:  # adding pin/pinbus
            if action == 'module_port':
                p_mode, signed, bus_msb, p_name = groups
            else:
                signed, bus_msb, p_name = groups
                p_mode = last_port_mode

            last_port_mode = p_mode
            if p_mode == 'input':
                p_type = Input
            elif p_mode == 'output':
                p_type = Output
            elif p_mode == 'inout':
                p_type = Inout

            if bus_msb is None:
                comp.add_pin(p_type(p_name))
            else:
                signed = False if signed is None else True
                comp.add_pinbus(Bus(p_type, p_name, int(bus_msb)+1, signed=signed))

        elif action == 'module_wire':  # adding net/netbus
            signed, bus_msb, n_name = groups
            if n_name in comp.net_names() or n_name in comp.netbus_names():  # in case its pin(pin_adds_net)
                continue
            if bus_msb is None:
                comp.add_net(Net(n_name))
            else:
                signed = False if signed is None else True
                comp.add_netbus(Bus(Net, n_name, int(bus_msb)+1, signed=signed))

        elif action == 'assign_start':  # adding assignment - start
            assign_dict = {'state': 'l', 'l_count': 0, 'r_count': 0, 'l_cases': [], 'r_cases': []}
            assign_pos = pos[0]

        # adding assignment - continue, divide to cases and save for later
        elif action in ['assign_cont_net', 'assign_cont_gnet', 'assign_cont_concat']:
            state = assign_dict['state']
            assign_dict[state+'_cases'].append((action[12:],) + groups)
            assign_dict[state+'_count'] += 1

        elif action == 'assign_eq':  # adding assignment - continue, read "=", so change state to right
            assign_dict['state'] = 'r'

        elif action == 'assign_break':  # can't understand assign command
            assign_command = re.match(r'\s*(assign[\S\s]*?;)', text[assign_pos:]).groups()[0]
            if verbose:
                print('Warning: skipped assign command "{}"'.format(assign_command))

        elif action == 'assign_finish':  # adding assignment - end, read ";", now can handle all the connectivity
            assign_dict['l_nets'] = []
            assign_dict['r_nets'] = []
            for s in ['l', 'r']:  # handle each case for itself and after that connect_nets
                for i in range(assign_dict[s+'_count']):  # loop over num of cases in the present state(left or right)
                    case = assign_dict[s+'_cases'][i][0]
                    if case == 'net':
                        _, net_name, msb, lsb = assign_dict[s+'_cases'][i]  # A,msb?,lsb?
                        if msb is None:
                            # check if net_name is bus
                            if net_name in comp.net_names():
                                assign_dict[s+'_nets'].append(comp.get_net(net_name))
                                is_bus = False
                            elif net_name in comp.netbus_names():
                                msb = comp.get_netbus(net_name).msb()
                                lsb = comp.get_netbus(net_name).lsb()
                                is_bus = True
                            else:
                                raise Exception('cannot find net [' + net_name + '] in component')
                        else:
                            lsb = msb if lsb is None else lsb
                            is_bus = True

                        if is_bus is True:
                            for bit in range(int(msb), int(lsb) - 1, -1):
                                assign_dict[s+'_nets'].append(comp.get_net('{0}[{1}]'.format(net_name, bit)))

                    elif case == 'gnet':
                        _, size, radix, value = assign_dict[s+'_cases'][i]  # 2,b,01/xx
                        if 'x' in value:
                            value_bin = value
                        else:
                            value_dec = int(value, radix2bits[radix.lower()])  # convert value to decimal
                            value_bin = bin(value_dec)[2:].zfill(int(size))  # convert value to binary padded to size

                        for bit in range(int(size)):
                            assign_dict[s+'_nets'].append(comp.get_net("1'b{}".format(value_bin[bit])))

                    elif case == 'concat':
                        _, num, net_name = assign_dict[s+'_cases'][i]  # 2,A
                        net = comp.get_net(net_name)
                        for j in range(int(num)):
                            assign_dict[s+'_nets'].append(net)

            # after we interpreted all the cases we can connect them
            if len(assign_dict['l_nets']) != len(assign_dict['r_nets']):
                raise Exception('cant do assign between two different sizes')
            for i in range(len(assign_dict['l_nets'])):
                comp.connect_nets(assign_dict['r_nets'][i], assign_dict['l_nets'][i])

        elif action == 'instance':  # save all instance connectivity for later
            text_subcomps += '\n'+groups[0]

        elif action == 'end_module':  # read "endmodule"
            comps.append((comp, text_subcomps))

    # instances connectivity part
    for comp, text_subcomps in comps:
        if text_subcomps:
            last_inst = None
            verilog_tokens_['module'][-4] = (r'\s*([\w$]+|\\\S+ )\s*([\w$]+|\\\S+ )\s*\(\s*', 'instance_start', 'instance_ports')  # to handle instances
            verilog_tokens_['module'][-1] = (r'\s*endmodule\s*', None)  # dont do #pop
            lex = Lexer(verilog_tokens_)
            for pos, action, groups in lex.run(text_subcomps, start='module'):  # run lexer and search for match
                if action == 'instance_start':  # adding new subcomponent
                    inst, inst_name = groups  # nand i_nand
                    if inst not in Component.all_components():
                        raise Exception('instance ' + inst + ' should be implemented in verilog file')
                        # sub = Component(inst)
                    else:
                        sub = Component.get_component_by_name(inst)
                    comp.add_subcomponent(sub, inst_name)
                    last_inst = inst_name
                    last_sub = sub

                elif action == 'empty_pin':
                    pass

                elif action == 'connect_gnets':
                    sub_pin, size, radix, value = groups  # I,2,b,01/xx
                    if 'x' in value:
                        value_bin = value
                    else:
                        value_dec = int(value, radix2bits[radix.lower()])  # convert value to decimal
                        value_bin = bin(value_dec)[2:].zfill(int(size))  # convert value to binary padded to size

                    if size == '1':  # not bus
                        comp.connect("1'b{}".format(value_bin), last_inst + '.' + sub_pin)
                    else:  # bus
                        for bit in range(int(size)):  # connect lsb to lsb and so on
                            comp.connect("1'b{}".format(value_bin[::-1][bit]), '{0}.{1}[{2}]'.format(last_inst, sub_pin, bit))

                elif action == 'connect':  # connect net/bus to pin/bus
                    sub_pin, net_name, msb, lsb = groups  # I,A,2?,0?
                    if msb is None:
                        # check if net_name is bus
                        if net_name in comp.net_names():  # net2pin
                            comp.connect(net_name, last_inst + '.' + sub_pin)
                            is_bus = False
                        elif net_name in comp.netbus_names():  # netbus2pinbus
                            msb = comp.get_netbus(net_name).msb()
                            lsb = comp.get_netbus(net_name).lsb()
                            is_bus = True
                        else:
                            raise Exception('cannot find net [' + net_name + '] in component')
                    else:
                        lsb = msb if lsb is None else lsb
                        if msb == lsb and sub_pin in last_sub.pin_names():  # in case were bus#1 to pin(not bus)
                            comp.connect('{}[{}]'.format(net_name, msb), last_inst + '.' + sub_pin)
                            is_bus = False
                        else:
                            is_bus = True

                    if is_bus is True:  # connect netbus to pinbus
                        for i, bit in enumerate(range(int(lsb), int(msb) + 1)):
                            comp.connect('{0}[{1}]'.format(net_name, bit),
                                         '{0}.{1}[{2}]'.format(last_inst, sub_pin, i))

                elif action == 'connect_concat':
                    sub_pin, num, net_name = groups  # I,2,A
                    for i in range(int(num)):
                        comp.connect(net_name, '{0}.{1}[{2}]'.format(last_inst, sub_pin, i))

                elif action in ['connect_many', 'connect_many_gnets', 'connect_many_concat']:  # save connectivity for later
                    bus_cont['count_cases'] = 1
                    bus_cont['sub_pin'] = groups[0]
                    bus_cont['nets2sub'] = [(action,) + groups[1:]]

                elif action in ['connect_many_cont', 'connect_many_gnets_cont', 'connect_many_concat_cont']:  # save connectivity for later
                    bus_cont['count_cases'] += 1
                    bus_cont['nets2sub'].append((action[:-5],) + groups)

                elif action == 'end_bus':  # connect all connectivity above to pinbus
                    pin_counter = 0
                    for d in range(bus_cont['count_cases']-1, -1, -1):  # from lsb to msb
                        if bus_cont['nets2sub'][d][0] == 'connect_many':  # connect net/bus to pin/bus
                            _, net_name, msb, lsb = bus_cont['nets2sub'][d]  # _,A,2,1?
                            if msb is None:
                                # check if net_name is bus
                                if net_name in comp.net_names():  # net2pinbus
                                    comp.connect(net_name, '{0}.{1}[{2}]'
                                                 .format(last_inst, bus_cont['sub_pin'], pin_counter))
                                    pin_counter += 1
                                    is_bus = False
                                elif net_name in comp.netbus_names():  # netbus2pinbus
                                    msb = comp.get_netbus(net_name).msb()
                                    lsb = comp.get_netbus(net_name).lsb()
                                    is_bus = True
                                elif implicit_wire is True:
                                    comp.add_net(Net(net_name))
                                    comp.connect(net_name, '{0}.{1}[{2}]'
                                                 .format(last_inst, bus_cont['sub_pin'], pin_counter))
                                    pin_counter += 1
                                    is_bus = False
                                else:
                                    raise Exception('cannot find net [' + net_name + '] in component')

                            else:
                                lsb = msb if lsb is None else lsb
                                is_bus = True

                            if is_bus is True:  # connect netbus to pinbus
                                p_c = pin_counter
                                for i, bit in enumerate(range(int(lsb), int(msb) + 1)):
                                    comp.connect('{0}[{1}]'.format(net_name, bit),
                                                 '{0}.{1}[{2}]'.format(last_inst, bus_cont['sub_pin'], i + p_c))
                                    pin_counter += 1

                        elif bus_cont['nets2sub'][d][0] == 'connect_many_gnets':
                            _, size, radix, value = bus_cont['nets2sub'][d]  # _,2,b,01/xx
                            if 'x' in value:
                                value_bin = value
                            else:
                                value_dec = int(value, radix2bits[radix.lower()])  # convert value to decimal
                                value_bin = bin(value_dec)[2:].zfill(int(size))  # convert value to binary padded to size

                            if size == '1':  # not bus
                                comp.connect("1'b{}".format(value_bin), '{0}.{1}[{2}]'
                                             .format(last_inst, bus_cont['sub_pin'], pin_counter))
                                pin_counter += 1
                            else:  # bus
                                p_c = pin_counter
                                for bit in range(int(size)):  # connect lsb to lsb and so on
                                    comp.connect("1'b{}".format(value_bin[::-1][bit]),
                                                 '{0}.{1}[{2}]'.format(last_inst, bus_cont['sub_pin'], bit + p_c))
                                    pin_counter += 1

                        elif bus_cont['nets2sub'][d][0] == 'connect_many_concat':
                            _, num, net_name = bus_cont['nets2sub'][d]  # _,2,A
                            p_c = pin_counter
                            for i in range(int(num)):
                                comp.connect(net_name, '{0}.{1}[{2}]'.format(last_inst, bus_cont['sub_pin'], i + p_c))
                                pin_counter += 1

        components.append(comp)
    return components


def is_verilog(fname):
    return os.path.splitext(fname)[1].lower() in ('.vlog', '.v')
