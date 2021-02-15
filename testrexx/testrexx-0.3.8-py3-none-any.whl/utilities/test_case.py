from .background_colors import BG

class TestCase:

    def __init__(self, test_id, description):
        self.test_id = test_id
        self.description = description
        self.passed = False
        self.raw_test_result = ''

    def __doc__(self):
        return f'{self.test_id} - {self.description}'

    def display_test_results(self, verbose=False):
        self.__set_result_character()
        result_string = f'{self.result_char} {self.__doc__()}'
        suffix = f'\n  ├⎯⎯⎯⎯ {self.raw_test_result}\n'
        if verbose or not self.passed:
            result_string += suffix
        print(result_string)

    def __set_result_character(self):
        if self.passed:
            self.result_char = f'{BG.OKGREEN}✓{BG.ENDC}'
        else:
            self.result_char = f'{BG.FAIL}X{BG.ENDC}'