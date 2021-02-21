from . import BonnibelError

class ProjectNotFound(BonnibelError):
    def __str__(self):
        return f"No project file '{Project.filename}' found."

class OutputNotFound(BonnibelError):
    def __init__(self, path):
        self.path = path
    def __str__(self):
        return f"{self.path} is not a valid bonnibel directory."


class BuildContext:
    __filename = ".bonnibel.ctx"

    @classmethod
    def load(cls, output):
        saved = output / cls.__filename
        if saved.is_file():
            import pickle
            return pickle.load(open(saved, "rb"))

        raise OutputNotFound(output)

    @classmethod
    def find(cls, output):
        import pathlib
        from .project import Project

        path = pathlib.Path.cwd()

        while True:
            project = path / Project.filename

            if project.is_file():
                return cls(path, path / output)

            if len(path.parents) == 0:
                raise ProjectNotFound()

            path = path.parent

    def __init__(self, root, output):
        self.root = root
        self.output = output
        self.project = None
        self.modules = {}
        self.variables = {}
        self.generator = None

    def initialize(self, config, generator, variables):
        from pathlib import Path

        self.config = config
        self.generator = Path(generator).resolve()
        self.variables = {}
        for var in variables:
            if '=' in var:
                parts = var.split('=', 1)
                self.variables[parts[0]] = parts[1]
            else:
                self.variables[var] = True

    def update(self):
        from .project import Project
        from .module import Module

        self.project = Project(self.root, self.config)
        self.modules = {mod.name : mod for mod in
            map(lambda x: Module(x, self.root),
                self.root.glob(f"**/{Module.filename}"))}

        Module.update(self.modules)
        self.save()

    def save(self):
        import pickle
        self.output.mkdir(exist_ok=True)
        pickle.dump(self, open(self.output / self.__filename, "wb"))

    def exec_ninja(self, *args):
        import ninja
        ninja._program('ninja', ['-v', '-C', str(self.output)] + list(*args))
