import re
import logging
import random
import math
logger = logging.getLogger('snakeeyes.elements')

"""Handles the Grammar of the document"""


class DiceString(object):
    """
        Generates the dice string to put through the system

        Attributes
        ----------
        parsestring : Pattern
            Regex pattern to detect the various attributes of a dice roll

        quantity : int
            Number of times die must be rolled

        sides : int
            Number of sides a die has

    """
    parsestring = re.compile(r"(?P<quantity>\d*(?=d\d*))d(?P<sides>\d*)")
    sides = 0
    quantity = 0

    def __init__(self, string):
        logger.debug("Initating DiceString")
        self.__dice = self.parsestring.search(string)
        try:
            self.quantity = int(self.__dice.group("quantity"))
            self.sides = int(self.__dice.group("sides"))
            logger.debug("Sides: " + str(self.sides) +
                         "Quantity: " + str(self.quantity))
        except (ValueError, AttributeError):
            pass

    def __bool__(self):
        if self.quantity != 0 and self.sides != 0:
            return True
        else:
            return False


class Die(object):
    """Class that handles dice rolls using the rand function and regular expressions

    Attributes
    ----------
    string : str
        String to be processed
    dice : DiceString
        Processed dicestring
    """
    opparse = re.compile(r"(?P<operator>[^\dd\(\)])(?P<operand>\d*)")

    def __init__(self, string: str):
        self.string = string
        logger.debug("String: " + self.string)
        self.dice = DiceString(string)
        self.oplist = self.opparse.findall(string)
        self.operators = self.oplist

        logger.debug(str(self.operators))

    def __bool__(self):
        if bool(self.dice):
            return True
        else:
            return False


class Operator():
    """
    Handles creating operators for use in rolls

    ...

    Attributes
    ----------
    char : str
        character for operand
    regex : str
        raw string, by default just detects the character

    Functions
    -------
    parse - Take the string and show that its there
    evaluate - Blank method where the operator is processed

    """
    priority = 0
    char = r""
    regex = rf"(?P<operator>[{char}])"

    @classmethod
    def parse(cls, string):
        """
        Take a string and output its operator and operands
        """
        compiled = re.compile(cls.regex)
        return compiled.search(string).groupdict()

    @classmethod
    def evaluate(cls, dice):
        pass


class LeftHandOperator(Operator):
    """
    Operators that act on the object to the left, using the object on the right, inherits from Operator

    Attributes
    ----------
    operand : str
        The arguments taken by the operator

    """
    char = Operator.char
    operand = r"\d*"
    regex = rf"(?P<operator>[{char}])(?P<operand>{operand})"

    @classmethod
    def parse(cls, string):
        compiled = re.compile(cls.regex)
        return compiled.search(string).groupdict()


class Successes(LeftHandOperator):

    """
    Takes an operand and calculates how many successes there have been
    """
    priority = 7
    char = r"\>"

    @classmethod
    def evaluate(cls, results, operand, die):
        dice_list = []
        logger.debug("Evaluating successes!")
        for d in results:
            if d > int(operand):
                dice_list.append((d, True))
            else:
                dice_list.append((d, False))

        return dice_list


class Exploding(LeftHandOperator):
    priority = 1
    char = r"x"

    @classmethod
    def evaluate(cls, results, operand: int, die: Die):
        eval_results = results
        logger.debug("Evaluating Exploding!")
        for d in results:
            logger.debug("D is: " + str(d))
            r = d
            logger.debug("Operand:" + str(operand))
            while r >= operand:
                logger.debug("Exploded!")
                temp_roll = math.ceil(random.random() * die.dice.sides)
                r = temp_roll
                logger.debug(" R is " + str(r))
                eval_results.append(temp_roll)
                if r >= operand:
                    break
        logger.debug("Exploded dice:" + str(eval_results))
        return eval_results
