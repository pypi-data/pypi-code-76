"""Handles the actual logic of dice rolls"""
import math
import random
import re
import logging

from .elements import Die, Exploding, Operator, Successes

logging.getLogger('snakeeyes.dicelogic')

op_dict = {
    ">": Successes,
    "x": Exploding,
}


class Roll():
    """A class which takes a string and outputs a dice roll

    Parameters
    ----------
    string : str
        The input string

    Attributes
    ----------
    dicer_regex : str
        Regex showing how to extract just the dice string from an object
    op_dict : dict
        dictionary containing the characters of an operator, and the assosciated class
    die : Die
        Dice roll using string input
    results : list
        List of results from dice rolled
    total : int
        The total of all dice rolled

    Methods
    -------
    roll
    """

    dice_regex = re.compile(r"\d*d\d*(?:[^d\d\(\)+\-\*/]\d*)*")
    math_regex = re.compile(r"[\(\)+*-\/\d]+")

    def roll(self, die: Die):
        """Takes Die object and returns a tuple containing a list of results, and a total of of all rolls."""
        dice_array = []
        for i in range(die.dice.quantity):
            dice_array.append(math.ceil(random.random() * die.dice.sides))
        dice_total = 0
        for r in dice_array:
            dice_total += r
        return (dice_array, dice_total)

    def op_collection(self, die: Die):
        """Take die object and return list of operator classes"""
        ops = []
        for o in die.operators:
            try:
                operator = op_dict[o[0]]
                op = (operator, int(o[1]))
                ops.append(op)
            except KeyError:
                continue
            return ops

    def op_evaluate(self, ops: list[tuple]):
        """Take results and operators and return a final result"""
        ops = sorted(ops, key=lambda op: op[0].priority)
        last_output = self.results
        for o in ops:
            last_output = o[0].evaluate(last_output, o[1], self.die)
        return last_output

    def __init__(self, string: str):
        self.string = string
        try:
            self.die = Die(self.string)
            if self.die:
                roll = self.roll(self.die)
                self.results = roll[0]
                self.total = roll[1]
                self.result_string = self.dice_regex.sub(
                    f"{self.total}", string)
                op_queue = self.op_collection(self.die)
                if op_queue:
                    self.operator = True
                    self.final = self.op_evaluate(op_queue)
                else:
                    self.result_string = self.math_regex.search(
                        self.string).group
                    self.final = self.result_string
        except AttributeError:
            self.result_string = self.math_regex.search(self.string).group
            self.final = eval(self.result_string)
