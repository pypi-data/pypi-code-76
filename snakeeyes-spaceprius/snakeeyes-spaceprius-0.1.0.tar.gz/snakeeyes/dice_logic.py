"""
Handles the actual logic of dice rolls

Classes
-------
Roll

Functions
---------
roll
"""
import math
import random
import re
import logging
from .elements import Die, Exploding, Successes

import ast, operator

binOps = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.Mod: operator.mod
}

def arithmeticEval (s):
    node = ast.parse(s, mode='eval')

    def _eval(node):
        if isinstance(node, ast.Expression):
            return _eval(node.body)
        elif isinstance(node, ast.Str):
            return node.s
        elif isinstance(node, ast.Num):
            return node.n
        elif isinstance(node, ast.BinOp):
            return binOps[type(node.op)](_eval(node.left), _eval(node.right))
        else:
            raise Exception('Unsupported type {}'.format(node))

    return _eval(node.body)
logger = logging.getLogger('snakeeyes.dicelogic')


op_dict = {
    ">": Successes,
    "x": Exploding,
}


def roll(die: Die):
    """
    Takes Die object and returns a tuple containing a list of results, and a total of of all rolls.

    Parameters
    ----------

    die : elements.Die
    """
    if die:
        dice_array = []
        for i in range(die.dice.quantity):
            dice_array.append(math.ceil(random.random() * die.dice.sides))
        dice_total = 0
        for r in dice_array:
            dice_total += r
        return (dice_array, dice_total)
    else:
        return False


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
    die : elements.Die
        Dice roll using string input
    results : list of int
        List of results from dice rolled
    total : int
        The total of all dice rolled

    Methods
    -------
    op_collection(die)
        Return operator class list
    op_evaluate(ops)
        Return the final result of all operators

    """

    dice_regex = re.compile(r"\d*d\d*(?:[^d\d\(\)+\-\*/]\d*)*")
    math_regex = re.compile(r"[\(\)+*-\/\d]+")

    def op_collection(self, die: Die):
        """
        Take die object and return list of operator classes.

        Parameters
        ----------
        die : elements.Die

        Returns
        -------
        ops : list of (elements.operator, int)
        """
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
        """Take results and operators and return a final result."""
        ops = sorted(ops, key=lambda op: op[0].priority)
        last_output = self.results
        for o in ops:
            last_output = o[0].evaluate(last_output, o[1], self.die)
        return last_output

    def __init__(self, string: str):
        self.string = string
        try:
            logger.debug("Trying!")
            self.die = Die(self.string)
            if self.die.dice:
                logger.debug("Dice detected")
                r = roll(self.die)
                self.results = r[0]
                if self.results: 
                    logger.debug("Results detected")
                    self.total = r[1]
                    self.result_string = self.dice_regex.sub(
                        f"{self.total}", string)
                    logger.debug("Result String first: %s", self.result_string)
                    op_queue = self.op_collection(self.die)
                    if op_queue:
                        logger.debug("Operator!")
                        self.operator = True
                        self.results = self.op_evaluate(op_queue)
                        self.total = 0
                        try:
                            for i in self.results:
                                self.total += i
                            self.final = self.total
                            self.result_string = self.dice_regex.sub(
                            f"{self.total}", string)
                        except TypeError:
                            pass
                    if self.result_string:
                        self.final = arithmeticEval(self.result_string)
            else:
                logger.debug("Result path:")
                self.final = arithmeticEval(self.result_string)
                logger.debug("Final: %s", self.final)
        except AttributeError:
            logger.debug("Exception result string: %s", self.string)
            self.final = arithmeticEval(self.string)
            logger.debug("Final: %s", self.final)