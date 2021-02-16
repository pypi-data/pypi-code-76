from .argument import  IterableArgumentValidator, FileArgument


class ArgumentsStatus:
    def __init__(self, args_dict_name, args_def):
        if not IterableArgumentValidator.in_collection(args_dict_name, ['body', 'query_string']):
            raise Exception('args_dict_name should be body or query_string')

        self.args_dict_name = args_dict_name
        self.args_def = args_def
        self.args_names = [arg.name for arg in self.args_def]
        self.invalid_args = False
        self.extra_args = list()
        self.validation_report = dict()
        self.help_report = dict()

    def args_help(self):
        self.help_report.update({self.args_dict_name: dict()})
        for arg in self.args_def:
            arg.arg_help()
            self.help_report[self.args_dict_name].update(arg.help_report)

    def create_final_report(self):
        if self.invalid_args:
            self.update_validation_report({'extra_arguments': list(self.extra_args)})

    def assert_args(self, args_vals_):
        self.validation_report['wrong_arguments'] = dict()
        args_vals = args_vals_ if args_vals_ else dict()
        self.check_extra_args(args_vals)
        for arg in self.args_def:
            
            if isinstance(arg, FileArgument):
                arg.assert_arg()

            else:
                arg.assert_arg(args_vals)

            if arg.invalid:
                self.update_validation_report(arg.validation_report, 'wrong_arguments')


            
        self.create_final_report()

    def check_extra_args(self, args_vals):
        self.extra_args = set(args_vals) - set(self.args_names)
        if len(self.extra_args):
            self.set_invalid_args()


    def update_validation_report(self, validation_report_update, key=None):
        self.set_invalid_args()
        if key:
            self.validation_report[key].update(validation_report_update)

        else:
            self.validation_report.update(validation_report_update)

    def set_invalid_args(self):
        self.invalid_args = True

    def __repr__(self):
        if self.invalid_args:
            return f'The arguments are invalid\nReport:\n{self.validation_report}'
        else:
            return 'The arguments are valid'