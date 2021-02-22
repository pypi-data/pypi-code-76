from random import randrange
from .Game import Game
from .Helper_funcs import HelperFuncs



class GuessGame(Game):

    def __init__(self,difficulty):
        self.difficulty = difficulty

    def generate_number(self):
        self.secret_number = randrange(1, self.difficulty + 1)


    def get_guess_from_user(self):

        helper_fuc = HelperFuncs()
        user_number = helper_fuc.input_int_validation(f"Please enter a number between 1 and {self.difficulty} : ",1,self.difficulty)

        return int(user_number)

    def compare_results(self):
        return self.get_guess_from_user() == self.secret_number

    def play(self):
        self.generate_number()
        return self.compare_results()
