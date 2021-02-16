from flask import request
from .argument import ListArgument


class QueryStringParser:
    """ A class to parse the query string arguments"""
    @staticmethod
    def parse_args(qs_args_def):
        """ Parse the query string """
        qs_args_dict = QueryStringParser.args_def_to_args_dict(qs_args_def)
        parsed_args = dict()
        passed_args = request.values.to_dict(flat=False)
        
        # Iterate over all passed args
        for arg in passed_args:

            # Unexpected arg
            if arg not in qs_args_dict:
                parsed_args[arg] = QueryStringParser.parse_list(passed_args[arg], int)                

            # Expected list and the passed is list
            elif qs_args_dict[arg]['type'] is list:
                parsed_args[arg] = QueryStringParser.parse_list(passed_args[arg], qs_args_dict[arg]['list_item_type'])

            else:
                # Expected nmmber or string but the passed is list
                if len(passed_args[arg]) > 1:
                    parsed_args[arg] = passed_args[arg]
                    continue
                
                # Expected nmmber (float or int) and the passed is nmmber
                if qs_args_dict[arg]['type'] in [int, float]:
                    parsed_args[arg] = QueryStringParser.parse_number(passed_args[arg][0])

                else:
                    # Expected string and the passed is string
                    parsed_args[arg] = passed_args[arg][0]

        return parsed_args

    @staticmethod
    def args_def_to_args_dict(args_def):
        """ Convert list of arguments to Flask request parser """
        args_attr = dict()
        for arg in args_def:
            args_attr.update({arg.name: dict()})

            if isinstance(arg, ListArgument):
                args_attr[arg.name].update({
                    'type': list,
                    'list_item_type': arg.arg_obj.arg_type
                    })
            else:
                args_attr[arg.name].update({'type': arg.arg_type})

        return args_attr
      
    @staticmethod          
    def parse_list(arg_value, item_type):
        parsed_arg = arg_value
        if item_type in [int, float]:
            for i in range(len(parsed_arg)):
                parsed_arg[i] = QueryStringParser.parse_number(parsed_arg[i])

        return parsed_arg

    @staticmethod
    def parse_number(arg_value):
        try:
            if '.' in arg_value:
                return float(arg_value)

            else:
                return int(arg_value)

        except:
            return arg_value