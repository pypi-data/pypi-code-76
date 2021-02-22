from random import randrange
from time import sleep
from subprocess import *
from .Game import Game
import os


class MemoryGame(Game):

    def __init__(self, difficulty):
        self.difficulty = difficulty


    def generate_sequence(self):

        list_of_nums = []
        for number in range(0,self.difficulty):

            list_of_nums.append(randrange(1,102))

        return list_of_nums


    def get_list_from_user(self):

        user_list = [int(x) for x in input(f"Please enter a size of {self.difficulty} list of numbers: ").split()]

        return user_list

    def is_list_equal(self):

        computer_list = self.generate_sequence()
        print(computer_list)
        sleep(0.7)

        if os.name == 'nt':
            run(["cls"],shell=True)
        else:
            run("clear")

        user_list = self.get_list_from_user()

        return set(computer_list) == set(user_list)

    def play(self):




       return self.is_list_equal()





