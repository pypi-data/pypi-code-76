
from dataclasses import dataclass
import io
import json

from typing import IO, Any, Dict, List, Optional, Union

def _quote(s: str):
    '''Return original string 's' as-is if it's something that doesn't
    need to be enclosed in string literals in a Dockerfile.
    Otherwise add quotes.

    Examples:
        "Firstname Lastname <email@example.org>"
        -> use quotes

        mypage:v1.0
        -> no need for quotes
    '''
    # TODO review what type of quoting is really required
    if ' ' in s:
        return f'"{s}"'
    return s

def shellify(cmds: List[str]):
    cstrs = []
    for c in cmds:
        cs = [c.lstrip() for c in c.split('\n')]
        cstrs.append(' \\\n    '.join(cs))
    cstr = ' \\\n && '.join(cstrs)
    return cstr

class BaseInstruction:
    def output(self, fp: IO[str]):
        raise NotImplemented

@dataclass
class From(BaseInstruction):
    image_tag: str
    platform: Optional[str]
    def write(self, fp: IO[str]):
        parts = ['FROM']
        if self.platform is not None:
            parts.append(f'--platform={self.platform}')
        parts.append(self.image_tag)
        # TODO 'as'
        fp.write(' '.join(parts) + '\n')

@dataclass
class Label(BaseInstruction):
    metadata_kv: Dict[str, Any]
    def write(self, fp: IO[str]):
        kvs = [f'{k}={_quote(v)}' for k,v in self.metadata_kv.items()]
        fp.write(f'LABEL {" ".join(kvs)}\n')

@dataclass
class Env(BaseInstruction):
    env_kv: Dict[str, Any]
    def write(self, fp: IO[str]):
        kvs = [f'{k}={_quote(v)}' for k,v in self.env_kv.items()]
        fp.write(f'ENV {" ".join(kvs)}\n')

@dataclass
class Run(BaseInstruction):
    commands: Union[str, List[str]]
    def write(self, fp: IO[str]):
        if isinstance(self.commands, list):
            fp.write(f'RUN {json.dumps(self.commands)}\n')
        else:
            fp.write(f'RUN {self.commands}\n')

@dataclass
class Copy(BaseInstruction):
    source: Union[str, List[str]]
    dest: str
    chown: Optional[str]
    def write(self, fp: IO[str]):
        chown = f'--chown={self.chown} ' if self.chown is not None else ''
        if isinstance(self.source, list):
            fp.write(f'COPY {chown}{" ".join(_quote(s) for s in self.source)} {_quote(self.dest)}\n')
        else:
            fp.write(f'COPY {chown}{_quote(self.source)} {_quote(self.dest)}\n')

@dataclass
class Workdir(BaseInstruction):
    workdir: str
    def write(self, fp: IO[str]):
        fp.write(f'WORKDIR {_quote(self.workdir)}\n')

class Gen:
    def __init__(self):
        self._instrs = []

    def from_(self, image_tag: str, platform: Optional[str] = None):
        '''The FROM instruction initializes a new build stage and sets the
        Base Image for subsequent instructions. As such, a valid Dockerfile
        must start with a FROM instruction
        '''
        self._instrs.append(From(image_tag, platform))

    def label(self, **args):
        self._instrs.append(Label(dict(**args)))

    def env(self, **args):
        self._instrs.append(Env(dict(**args)))

    def run(self, commands: Union[List[str], str], shell=True):
        if not shell:
            # RUN 'exec' form requires a list
            assert isinstance(commands, list)
            self._instrs.append(Run(commands))
        else:
            if isinstance(commands, list):
                self._instrs.append(Run(shellify(commands)))
            else:
                assert isinstance(commands, str)
                self._instrs.append(Run(commands))

    def run_exec(self, command: List[str]):
        '''RUN command but use an explicit list to perform an exec invocation without shell'''
        raise NotImplemented

    def copy(self, source: Union[List[str], str], dest: str, chown: Optional[str] = None):
        self._instrs.append(Copy(source, dest, chown))

    def workdir(self, workdir: str):
        self._instrs.append(Workdir(workdir))

    def write(self, fp: IO[str]):
        for instr in self._instrs:
            instr.write(fp)
