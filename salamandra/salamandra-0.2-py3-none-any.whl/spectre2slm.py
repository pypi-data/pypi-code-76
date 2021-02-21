from salamandra.lexer import Lexer
import re
from .net import Net
from .inout import Inout
from .component import Component


def get_spectre_tokens():
    # return tokens for Lexer to run with this
    spectre_tokens = {
        'root': [
            (r'\s*(//|\*).*?\n\s*', None),  # //...\n , *...\n
            (r'\s*subckt\s+([\w!]+|\\\S+ )\s+([\S\s]*?[^\\]\n)\s*(parameters\s+[\S\s]*?[^\\]\n)?([\S\s]*?)ends\s+\1\s*', 'subckt'),
            # groups: 0.name(=\1), 1.nodes, 2.parameters(?), 3. subckt body
            # Example:
            # subckt SubcircuitName [(] node1 ... nodeN [)]
            #       [ parameters name1=value1 ... [nameN=valueN]]
            #       instance, model, ic, or nodeset statements—or
            #       further subcircuit definitions
            # ends [SubcircuitName]
            (r'\s*(model|global|include)\s+[\S\s]*?([^\\]\n|\Z)\s*', None),  # model...\n or EOF(\Z)
            (r'\s*simulator\s+lang\s*=\s*spectre\s*', None),  # simulator lang = spectre
            (r'\s*([\w!]+|\\\S+ )(\s+[\S\s]*?)?\s+([\w!]+|\\\S+ )(\s+(?:[\w!]+|\\\S+ )\s*=\s*[\w+\-.]+\s+[\S\s]*?[^\\])?\s*(?:\n|\Z)\s*', 'instance'),
            # instance or analysis, groups: 0.name, 1.nodes, 2.master/analysis_type, 3.parameters(?)
            # Example:
            # name [(]node1 ... nodeN[)] master [[param1=value1] ...[paramN=valueN]]
            # Name [(]node1 ... nodeN[)] Analysis_Type [[param1=value1] ...[paramN=valueN]]
        ],
    }
    return spectre_tokens


def spectre2slm_file(fname, top_cell_name='spectre2slm_cell', is_std_cell=False):
    with open(fname, 'rt') as fh:
        text = fh.read()
    return spectre2slm(text, top_cell_name, is_std_cell)


def spectre2slm(text, top_cell_name='spectre2slm_cell', is_std_cell=False):
    """Parse a text buffer of spectre code
    Args:
      text (str): Source code to parse
      top_cell_name (str): name of top cell component
      is_std_cell (bool): is STD cell (takes only I/O ports)
    Returns:
      top cell component
    """

    spectre_tokens_ = get_spectre_tokens()  # get local spectre tokens
    lex = Lexer(spectre_tokens_)
    analysis_type = ['pxf','xf','sp','tran','tdr','noise','pnoise','dc','ac','pz','envlp','pac','pdisto','pnoise','pss',
                     'sens','fourier','dcmatch','stb','sweep','montecarlo']
    comp = None
    text_instances = []
    text_subckts =[]

    for pos, action, groups in lex.run(text):  # run lexer and search for match
        if action == 'subckt':
            dev_name, pins, params, subckt_body = groups
            comp = Component(dev_name)
            if pins:
                for pin in re.findall(r'([\w!\[\]]+|\\\S* (?:\[\d+\])?)', pins):  # add all pins: A,A[0],\A,\A [0]
                    comp.add_pin(Inout(pin))
            if params:  # add parameters
                for p in re.findall(r'\s*([\w!]+|\\\S+ )\s*=\s*([\w+\-.]+)', params):
                    comp.set_spice_param(p[0], p[1])

            # save subckt content to look inside later
            if subckt_body:
                text_subckts.append((dev_name, subckt_body))

        elif action == 'instance':
            if groups[2] in analysis_type:  # Analysis Statement - skip
                continue
            text_instances.append(groups)  # save to look inside later

    if text_instances:
        if top_cell_name in Component.all_components():
            comp = Component.get_component_by_name(top_cell_name)
        else:
            comp = Component(top_cell_name)
        if is_std_cell:
            comp.set_is_physical(True)

    # instances connectivity part
    for groups in text_instances:
        inst_name, nets, dev_name, params = groups
        dev = Component.get_component_by_name(dev_name)
        comp.add_subcomponent(dev, inst_name)

        nets = re.findall(r'\s*([\w!\[\]]+|\\\S* (?:\[\d+\])?)', nets)
        for net, pin in zip(nets, dev.get_pins_ordered()):
            if net in ['0', '1']:
                net = "1'b0" if net == '0' else "1'b1"
            elif net not in comp.net_names():
                comp.add_net(Net(net))
            comp.connect(net, inst_name+'.'+pin.get_object_name())  # connect net to pin of instance
        if params:
            for p in re.findall(r'\s*([\w!]+|\\\S+ )\s*=\s*([\w+\-.]+)', params):  # add parameters
                if p[1] in comp.get_spice_params():  # check if value is a parameter of comp
                    p = p[0], comp.get_spice_param(p[1])  # update parameter with his actual value
                dev.set_spice_param(p[0], p[1])

    # read subckt body content
    for dev_name, subckt_body in text_subckts:
        spectre2slm(subckt_body, top_cell_name=dev_name)

    return comp
