class Template:
    def __init__(self):
        pass

    def __call__(self, file):
        with open(file) as f:
            return f.read()
