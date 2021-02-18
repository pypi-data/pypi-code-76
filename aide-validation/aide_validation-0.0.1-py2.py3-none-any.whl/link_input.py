"""GUI to display validation results.
Created on September 18, 2020

@author: jcs528@cornell.edu
"""

from tkinter import Tk, Button, Label, Entry
from aide_validation.validator import Validator


class ValidationGUI(object):
    def __init__(self, root):
        self.root = root
        self.e = Entry(root, width=50)
        self.e.pack()

        urlButton = Button(root, text="Validate OnShape Url", command=self.urlClick)
        urlButton.pack()

        exitButton = Button(root, text="Exit AIDE Validation", command=self.exitClick)
        exitButton.pack()

        self.validator = Validator()
        self.urlLabel = None

    def urlClick(self):
        url = self.e.get()
        message = self.validator.validate(url)
        if self.urlLabel is None:
            self.urlLabel = Label(root, text=message)
            self.urlLabel.pack()
        else:
            self.urlLabel["text"] = message

    def exitClick(self):
        self.root.destroy()


if __name__ == "__main__":
    root = Tk()
    gui = ValidationGUI(root)
    root.mainloop()
