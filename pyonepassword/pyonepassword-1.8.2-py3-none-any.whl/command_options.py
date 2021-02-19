from dataclasses import dataclass


@dataclass
class AbstractCommandOptions:
    _flags = {}

    def to_argv(self):
        if not self._flags:
            raise NotImplementedError("Must extend and set _flags dict")
        argv = []
        for flag, attr in self._flags.items():
            arg = getattr(self, attr)
            if isinstance(arg, bool):
                if arg is True:
                    argv.extend([flag])
            else:
                argv.extend([flag, arg])
        return argv


@dataclass
class GlobalOptions(AbstractCommandOptions):
    shorthand: str
    token: str
    _flags = {"--session": "token",
              "--account": "shorthand"}


class GetItemOptions(AbstractCommandOptions):
    pass


@dataclass
class GetDocumentOptions(AbstractCommandOptions):
    include_trash: bool
    output: str
    vault: str
    _flags = {"--include-trash": "include_trash",
              "--output": "output",
              "--vault": "vault"}
