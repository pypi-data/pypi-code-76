import os
from pathlib import Path
import subprocess as subp
from hashlib import sha224
from typing import Iterable, Union
import semver
from .makru import panic


def exprog(args, cwd=None, env=None):
    env = env if env else os.environ
    cwd = cwd if cwd else os.getcwd()
    return subp.Popen(
        args,
        cwd=cwd,
        env=env,
        stdout=subp.PIPE,
        stderr=subp.PIPE,
        encoding="utf-8",
        universal_newlines=True,
    )


def shell(args, cwd=None, env=None, printf=lambda x: print(x, end=""), non_zero_to_fail: bool=False, dryrun: bool=False):
    printf("$ {}\n".format(" ".join(args) if not isinstance(args, str) else args))
    if not dryrun:
        with exprog(args, cwd=cwd, env=env) as p:
            while p.poll() == None:
                printf(p.stdout.read(1))
            if p.stdout.readable():
                printf(p.stdout.read())
            if p.returncode != 0:
                printf(p.stderr.read())
            code = p.returncode
            if non_zero_to_fail and code != 0:
                panic("failed: sub-process exited with {}".format(code))
            return code


def choose_file(path_templates, name):
    """
    return the first exists path, if not one exists, return None
    ````
    choose_file(["/bin/?", "/usr/local/?"], "sh")
    ````
    """
    for p in map(lambda pt: pt.replace("?", name), path_templates):
        path = Path(p)
        if path.exists():
            return str(path)
    return None


def get_file_hash(path, update, block_size=65536):
    """
    Read blocks from file of the `path` and call `update` once a block.
    `block_size` is the size of one block, is 65535 bytes (a.k.a. 64 kilobytes).
    """
    with open(path, "rb") as f:
        fblk = f.read(block_size)
        while len(fblk) > 0:
            update(fblk)
            fblk = f.read(block_size)


def get_file_hash_sha224(path, block_size=65536):
    """
    Get the sha224 hash of file of the `path`.
    Return `str`
    """
    obj = sha224()
    get_file_hash(path, obj.update, block_size)
    return obj.hexdigest()


def check_binary(name, PATH=None):
    """
    check if the given name exists in PATHs, if exists, return the first path found, else return None.
    ````
    if check_binary("clang"):
        print("Clang mounted!")

    if not check_binary("some-tool", PATH=".:./tools/"):
        print("Could not found the tool needed for compiling")
    ````
    """
    PATH = PATH if PATH else os.environ.get("PATH", "")
    pathes = map(lambda x: os.path.join(x, "?"), PATH.split(":"))
    return choose_file(pathes, name)


def create_makru(*args):
    """
    create a makru instance to deal with another makru project. this function doesn't have path expanding, so the '.' means CWD, not the folder contains makru config file.
    ````
    projectb = create_makru("-F{}".format("./projectb"))
    projectb.action("test")
    ````
    """
    from .makru import Makru

    return Makru(list(args))


def run_makru(*args):
    """
    it looks like run the makru CLI directly.
    """
    makru_instance = create_makru(**args)
    makru_instance.main()


def compare_version(v1, v2):
    """
    This function is a warpper of semver.VersionInfo.compare().
    Return `int`. The return value is negative if v1 < v2, zero if v1 == v2 and strictly positive if v1 > v2.
    """
    return semver.VersionInfo.parse(v1).compare(v2)


def match_version(v1, cond):
    """
    This function is a warpper of semver.VersionInfo.match().
    `cond` is a `str` prefixed with one of > (greater than), < (less than), >= (not less than), <= (not greater than), == (equal), != (not equal).
    Return `bool`.
    """
    return semver.VersionInfo.parse(v1).match(cond)


def is_semver(ver):
    """
    This function is a warpper of semver.VersionInfo.isvalid().
    Return `bool`.
    """
    return semver.VersionInfo.isvalid(ver)


def is_prerelease(ver):
    """
    Return `True` if `ver` contains "prerelease" field (e.g. "pre.2" or "beta.1"), otherwise return `False`.
    """
    return semver.VersionInfo.parse(ver).prerelease != None


def pick_latest_release(vers: Iterable[str]) -> Union[str, None]:
    """
    Return the most recent released version from `vers`. The "released version" means that it does not contains prerelease field.
    Return `str`, or `None` if `vers` is empty.
    """
    iterator_vers = iter(vers)
    latest = next(iterator_vers, None)
    for v in iterator_vers:
        if (not is_prerelease(v)) and (compare_version(latest, v) < 0):
            latest = v
    return latest


def pick_max_version(vers: Iterable[str]) -> Union[str, None]:
    """
    Return the max version from `vers`.
    Return `str`, or `None` if `vers` is empty.
    """
    iterator_vers = iter(vers)
    latest = next(iterator_vers, None)
    for v in iterator_vers:
        if compare_version(latest, v) <= 0:
            latest = v
    return latest
