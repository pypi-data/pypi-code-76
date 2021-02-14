# Classes pertaining to the card deck
# Armaan Bhojwani 2021


class Card:
    """Class containing the card information."""

    def __init__(self, inp):
        self.starred = False
        self.side = 0
        self.front = ""
        self.back = ""
        if len(inp) >= 1:
            self.front = inp[0]
        if len(inp) >= 2:
            self.back = inp[1]

    def __str__(self):
        return f"{self.front}, {self.back}"

    def unStar(self):
        self.starred = False

    def star(self):
        self.starred = True

    def toggleStar(self):
        if self.starred:
            self.starred = False
        else:
            self.starred = True

    def printStar(self):
        if self.starred:
            return "★ Starred ★"
        else:
            return "Not starred"

    def get(self, smart=True):
        if self.side == 1 and smart:
            return (self.back, self.front)
        else:
            return (self.front, self.back)

    def flip(self):
        if self.side == 0:
            self.side = 1
        else:
            self.side = 0

    def get_reverse(self):
        if self.side == 0:
            return 1
        else:
            return 0


class Status:
    """Keeps track of where in the deck the user is"""

    def __init__(self):
        self.index = 0
        self.side = 0

    def forward(self, stack):
        if self.index != len(stack):
            self.index += 1

    def back(self):
        if not self.index < 1:
            self.index -= 1

    def get_reverse(self):
        if self.side == 0:
            return 1
        else:
            return 0
