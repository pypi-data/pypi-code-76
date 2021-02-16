from collections.abc import Iterable
import copy

class FunctionArgsAssertion:
    """ This class has some function to assert the functions inputs """

    @staticmethod
    def assert_number(num):
        if not (isinstance(num, int) or isinstance(num, float)):
            raise Exception('The passed value should be a number (int or float)')

    @staticmethod
    def assert_number_type(num_typ):
        if num_typ not in [int, float]:
            raise Exception('The selected type should be int or float but you have passed {}'.format(num_typ.__name__))

    @staticmethod
    def assert_range(req_range):
        if type(req_range) is not list or len(req_range) != 2:
            raise Exception('req_range should be a list of two elements')

        try:
            FunctionArgsAssertion.assert_number(req_range[0])
            FunctionArgsAssertion.assert_number(req_range[1])
        except:
            raise Exception('Both items in the req_range should be numbers or can be converted into numbers')

        if req_range[-1] < req_range[0]:
            raise Exception('The first number in range should be smaller or equal to the second number')

    @staticmethod
    def assert_type(req_type):
        if type(req_type) is not type:
            raise Exception('arg_type should be from the type "type" like int,str, ...')

    @staticmethod
    def assert_iterable(req_collection):
        if not isinstance(req_collection, Iterable):
            raise Exception('req_collection should be an iterable object like list, dict, ...')

    @staticmethod
    def assert_list_set_tuple(req_collection):
        if type(req_collection) not in [list, set, tuple]:
            raise Exception('req_collection should be a list, a tuble or, a set')


class ComparisonOperator:
    """ A class to implement the comparison operators as functions """
    comparison_operators = {
        'greater_than': lambda x, y: x > y,
        'greater_than_or_equal_to': lambda x, y: x >= y,
        'less_than': lambda x, y: x < y,
        'less_than_or_equal_to': lambda x, y: x <= y,
        'equal_to': lambda x, y: x == y,
        'not_equal_to': lambda x, y: x != y,
    }

    def __init__(self, operator_name, operand):
        self.operator_name = operator_name
        self.operand = operand

    def compare(self, arg_val):
        if self.operator_name not in ComparisonOperator.comparison_operators:
            raise Exception(f'operator_name should be one of the following values {self.comparison_operators.keys()}')

        operator = ComparisonOperator.comparison_operators[self.operator_name]
        return True if operator(arg_val, self.operand) else False

    def __str__(self):
        return f'{self.operator_name.replace("_", " ")} {self.operand}'


# Prototype class for ComparisonOperator class (using prototype design pattern)
class OperatorPrototype:
    # Create all possible operator objects
    greater_than_operator = ComparisonOperator('greater_than', 0)
    greater_than_or_equal_to_operator = ComparisonOperator('greater_than_or_equal_to', 0)
    less_than_operator = ComparisonOperator('less_than', 0)
    less_than_or_equal_to_operator = ComparisonOperator('less_than_or_equal_to', 0)
    equal_to_operator = ComparisonOperator('equal_to', 0)
    not_equal_to_operator = ComparisonOperator('not_equal_to', 0)

    @staticmethod
    def __new_operator(operator_object, operand):
        new_operator_object = copy.deepcopy(operator_object)
        new_operator_object.operand = operand
        return new_operator_object

    @staticmethod
    def create_greater_than_operator(operand):
        return OperatorPrototype.__new_operator(
            OperatorPrototype.greater_than_operator, operand)

    @staticmethod
    def create_greater_than_or_equal_to_operator(operand):
        return OperatorPrototype.__new_operator(
            OperatorPrototype.greater_than_or_equal_to_operator, operand)

    @staticmethod
    def create_less_than_operator(operand):
        return OperatorPrototype.__new_operator(
            OperatorPrototype.less_than_operator, operand)

    @staticmethod
    def create_less_than_or_equal_to_operator(operand):
        return OperatorPrototype.__new_operator(
            OperatorPrototype.less_than_or_equal_to_operator, operand)

    @staticmethod
    def create_equal_to_operator(operand):
        return OperatorPrototype.__new_operator(
            OperatorPrototype.equal_to_operator, operand)

    @staticmethod
    def create_not_equal_to_operator(operand):
        return OperatorPrototype.__new_operator(
            OperatorPrototype.not_equal_to_operator, operand)

