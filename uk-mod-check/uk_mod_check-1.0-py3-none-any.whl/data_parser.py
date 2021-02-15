import enum
import dataclasses
import typing


class ModMode(enum.Enum):
    Mod10 = 1
    Mod11 = 2
    DblAl = 3

    @classmethod
    def from_txt(cls, name: str):
        if name == "MOD10":
            return cls.Mod10
        elif name == "MOD11":
            return cls.Mod11
        elif name == "DBLAL":
            return cls.DblAl

@dataclasses.dataclass
class Weights:
    u: int
    v: int
    w: int
    x: int
    y: int
    z: int
    a: int
    b: int
    c: int
    d: int
    e: int
    f: int
    g: int
    h: int

    @classmethod
    def from_parts(cls, parts: typing.List[str]):
        return cls(
            u=int(parts[0]),
            v=int(parts[1]),
            w=int(parts[2]),
            x=int(parts[3]),
            y=int(parts[4]),
            z=int(parts[5]),
            a=int(parts[6]),
            b=int(parts[7]),
            c=int(parts[8]),
            d=int(parts[9]),
            e=int(parts[10]),
            f=int(parts[11]),
            g=int(parts[12]),
            h=int(parts[13]),
        )

@dataclasses.dataclass
class ModRule:
    start_code: int
    end_code: int
    mod_mode: ModMode
    weights: Weights
    exception: typing.Optional[int]

    @classmethod
    def from_line(cls, line: str):
        parts = line.split()
        if len(parts) not in (17, 18):
            raise ValueError(f"Invalid record: {line}")
        try:
            start_code = int(parts[0])
            end_code = int(parts[1])
        except ValueError:
            raise ValueError(f"Invalid record: {line}")
        mod_mode = ModMode.from_txt(parts[2])
        if mod_mode is None:
            raise ValueError(f"Invalid record: {line}")
        try:
            weights = Weights.from_parts(parts[3:17])
        except ValueError:
            raise ValueError(f"Invalid record: {line}")
        if len(parts) == 18:
            try:
                exception = int(parts[17])
            except ValueError:
                raise ValueError(f"Invalid record: {line}")
        else:
            exception = None

        return cls(
            start_code=start_code,
            end_code=end_code,
            mod_mode=mod_mode,
            weights=weights,
            exception=exception
        )

@dataclasses.dataclass
class ModRules:
    rules: typing.List[ModRule]

    @classmethod
    def from_file(cls, file_path):
        rules = []
        with open(file_path, "r") as f:
            for line in f.readlines():
                rules.append(ModRule.from_line(line))

        return cls(
            rules=rules
        )

    def find_rule(self, sort_code: int):
        found_rules = []
        for rule in self.rules:
            if rule.start_code <= sort_code <= rule.end_code:
                found_rules.append(rule)
        return found_rules


@dataclasses.dataclass
class CodeSubstitution:
    orig_code: int
    new_code: int

    @classmethod
    def from_line(cls, line: str):
        parts = line.split()
        if len(parts) != 2:
            raise ValueError(f"Invalid record: {line}")
        try:
            orig_code = int(parts[0])
            new_code = int(parts[1])
        except ValueError:
            raise ValueError(f"Invalid record: {line}")

        return cls(
            orig_code=orig_code,
            new_code=new_code
        )

@dataclasses.dataclass
class CodeSubstitutions:
    rules: typing.List[CodeSubstitution]

    @classmethod
    def from_file(cls, file_path):
        rules = []
        with open(file_path, "r") as f:
            for line in f.readlines():
                rules.append(CodeSubstitution.from_line(line))

        return cls(
            rules=rules
        )

    def find_substitution(self, sort_code: int):
        for rule in self.rules:
            if rule.orig_code == sort_code:
                return rule.new_code