from random import randrange
from currency_converter import CurrencyConverter
from .Game import Game


class CurrencyRouletteGame(Game):

    def __init__(self, difficulty):
        self.difficulty = difficulty
        self.rand_number = randrange(1, 101)

    def get_money_interval(self):
        c = CurrencyConverter()
        total_converted_cash = c.convert(self.rand_number, 'USD', 'ILS')
        min_interval = total_converted_cash - (5 - self.difficulty)
        max_interval = total_converted_cash + (5 - self.difficulty)

        return min_interval, max_interval

    def get_guess_from_user(self):
        print(f"Can you guess whats the conversion rate of ${self.rand_number}?")
        user_conversation_guess = input("Enter Guess: ")
        return int(user_conversation_guess)

    def play(self):
        user_conversation_guess = self.get_guess_from_user()
        min_interval, max_interval = self.get_money_interval()

        return max_interval >= user_conversation_guess >= min_interval
