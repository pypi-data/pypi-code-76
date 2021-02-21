# This is for reference purposes
"""Handles dice rolling in a better way than the dice library

    Classes:
        Roll

    Methods:
        roll
        total_roll
"""
import re
import dice
import logging

logger = logging.getLogger('dice.prisu')


class Roll():
    """Class that handles dice rolls using the rand function and regular expressions

        ...

        Attributes
        ----------
        string : str
            String to be processed

    """
    diceparse = re.compile(r"(\d*d\d*)[xr^hHvlLoOmMaefts]?")
    mathparse = re.compile(r"([+\-*/]\d*\.*\d*)(?!\d*d\d*)")

    def __init__(self, string: str):
        logger.info("Roll Created!")
        self.string = string
        logger.info("Roll string" + str(self.string))
        self.dicestring = self.diceparse.search(string)
        mathstring = self.mathparse.findall(string)
        tempstring = ""
        for m in mathstring:
            tempstring = tempstring + str(m)
        self.mathstring = tempstring


def roll(string: str):
    """
    Wrapper around the dice library

    """
    inlet = Roll(string)
    if not inlet.dicestring:
        outlet = eval(inlet.string)
    else:
        roll = dice.roll(inlet.dicestring.group())
        try:
            string = inlet.diceparse.sub(str(roll), inlet.string)
            outlet = eval(string)
        except TypeError:
            return "This needs a T"
    return outlet


def total_roll(string: str):
    """Same as roll() but for total rolls

        ...

        Parameters
        ----------
        String (str): string to be processed

    """
    inlet = Roll(string)
    if not inlet.dicestring:
        outlet = eval(inlet.string)
    else:
        roll = dice.roll(inlet.dicestring.group() + "t")
        try:
            string = inlet.diceparse.sub(str(roll), inlet.string)
            outlet = eval(string)
        except TypeError:
            return "This needs a T"
    return outlet
