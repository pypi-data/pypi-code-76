import json
from typing import Any, Optional


class ExcValues:
    def __init__(self, *args, **kwargs):
        self.args = args
        self.kwargs = kwargs
        self.__dict__.update(**kwargs)

    def __getattr__(self, name) -> Any:
        try:
            return self.kwargs[name]
        except KeyError:
            raise AttributeError(
                f"No exception value {name}: {json.dumps(self.kwargs, indent=2)}"
            )


class CertDumperError(Exception):
    msg: str

    def __init__(
        self,
        *args,
        detail: Optional[str] = None,
        **kw
    ):
        super(CertDumperError, self).__init__(
            self.msg.format(*args, **kw) + (f": {detail}" if detail else '')
        )

        self.detail = detail
        self.values = ExcValues(*args, **kw)


class NoProject(CertDumperError):
    msg = "Cannot find project config file: {config_file} from {work_dir}"


class InvalidAcmeJson(CertDumperError):
    msg = "Cannot parse ACME file: {}\ncontent: '{}'"
