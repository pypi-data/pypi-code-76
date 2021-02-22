from .Helper_funcs import HelperFuncs
from .GuessGame import GuessGame
from .MemoryGame import MemoryGame
from .CurrencyRouletteGame import CurrencyRouletteGame


class Live():





    def welcome(self, name):
        print()
        print(f"Hello {name} and welcome to the world of Games(WoG).")
        print(f"Here you can find many cool games to play.")
        return ""

    def load_game(self):

        helper_fuc = HelperFuncs()

        print()
        print("Please choose a game to play:")
        print("1. Memory Game - a sequence of numbers will appear for 1 second and you have to guess it back")
        print("2. Guess Game - guess a number and see if you chose like the computer")
        print("3. Currency Roulette - try and guess the value of a random amount of USD in ILS")

        game_number = helper_fuc.input_int_validation("please choose a number between 1 and 3: ",1,3)


        if int(game_number) == 1:

            game_difficulty = helper_fuc.input_int_validation("Please choose game difficulty from 1 to 5: ",1,5)

            ins_memory_game = MemoryGame(int(game_difficulty))
            return ins_memory_game.play()


        elif int(game_number) == 2:

            game_difficulty = helper_fuc.input_int_validation("Please choose game difficulty from 1 to 5: ",1,5)

            ins_guess_game = GuessGame(int(game_difficulty))
            return ins_guess_game.play()

        elif int(game_number) == 3:

            game_difficulty = helper_fuc.input_int_validation("Please choose game difficulty from 1 to 5: ",1,5)

            ins_currency_game = CurrencyRouletteGame(int(game_difficulty))
            return ins_currency_game.play()
