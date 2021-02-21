
class Source:
    Actions = {'.c': 'c', '.cpp': 'cpp', '.s': 's'}

    def __init__(self, path, root):
        self.input = root / path
        self.name = path
        self.output = path + ".o"
        self.action = self.Actions.get(self.input.suffix, None)

    def __str__(self):
        return "{} {}:{}:{}".format(self.action, self.output, self.name, self.input)

