import os
import sys
from pathlib import Path
from typing import Callable, List, Optional, Sequence, Tuple

import pytest
from _pytest.monkeypatch import MonkeyPatch  # noqa # cannot import from tox.pytest yet
from _pytest.tmpdir import TempPathFactory
from pytest_mock import MockerFixture
from virtualenv import cli_run

from tox.config.cli.parser import Parsed
from tox.config.loader.api import Override
from tox.config.main import Config
from tox.run import make_config
from tox.tox_env.python.api import PythonInfo, VersionInfo
from tox.tox_env.python.virtual_env.api import VirtualEnv

pytest_plugins = "tox.pytest"
HERE = Path(__file__).absolute().parent


@pytest.fixture(scope="session")
def value_error() -> Callable[[str], str]:
    def _fmt(msg: str) -> str:
        return f'ValueError("{msg}"{"," if sys.version_info < (3, 7) else ""})'

    return _fmt


if sys.version_info >= (3, 8):  # pragma: no cover (py38+)
    from typing import Protocol
else:  # pragma: no cover (<py38)
    from typing_extensions import Protocol  # noqa


class ToxIniCreator(Protocol):
    def __call__(self, conf: str, override: Optional[Sequence[Override]] = None) -> Config:  # noqa: U100
        ...


@pytest.fixture()
def tox_ini_conf(tmp_path: Path, monkeypatch: MonkeyPatch) -> ToxIniCreator:
    def func(conf: str, override: Optional[Sequence[Override]] = None) -> Config:
        dest = tmp_path / "c"
        dest.mkdir()
        config_file = dest / "tox.ini"
        config_file.write_bytes(conf.encode("utf-8"))
        with monkeypatch.context() as context:
            context.chdir(tmp_path)
        return make_config(
            Parsed(work_dir=dest, override=override or [], config_file=config_file, root_dir=None),
            pos_args=[],
        )

    return func


@pytest.fixture(scope="session")
def demo_pkg_setuptools() -> Path:
    return HERE / "demo_pkg_setuptools"


@pytest.fixture(scope="session")
def demo_pkg_inline() -> Path:
    return HERE / "demo_pkg_inline"


@pytest.fixture()
def patch_prev_py(mocker: MockerFixture) -> Callable[[bool], Tuple[str, str]]:
    def _func(has_prev: bool) -> Tuple[str, str]:
        ver = sys.version_info[0:2]
        prev_ver = "".join(str(i) for i in (ver[0], ver[1] - 1))
        prev_py = f"py{prev_ver}"
        impl = sys.implementation.name.lower()

        def get_python(self: VirtualEnv, base_python: List[str]) -> Optional[PythonInfo]:  # noqa
            if base_python[0] == "py31" or (base_python[0] == prev_py and not has_prev):
                return None
            raw = list(sys.version_info)
            if base_python[0] == prev_py:
                raw[1] -= 1  # type: ignore[operator]
            ver_info = VersionInfo(*raw)  # type: ignore[arg-type]
            return PythonInfo(
                executable=Path(sys.executable),
                implementation=impl,
                version_info=ver_info,
                version="",
                is_64=True,
                platform=sys.platform,
                extra_version_info=None,
            )

        mocker.patch.object(VirtualEnv, "_get_python", get_python)
        return prev_ver, impl

    return _func


@pytest.fixture(scope="session", autouse=True)
def _do_not_share_virtualenv_for_parallel_runs(tmp_path_factory: TempPathFactory, worker_id: str) -> None:
    # virtualenv uses locks to manage access to its cache, when running with xdist this may throw off test timings
    if worker_id != "master":  # pragma: no branch
        temp_app_data = str(tmp_path_factory.mktemp(f"virtualenv-app-{worker_id}"))  # pragma: no cover
        os.environ["VIRTUALENV_APP_DATA"] = temp_app_data  # pragma: no cover
        seed_env_folder = str(tmp_path_factory.mktemp(f"seed-cache-{worker_id}"))  # pragma: no cover
        args = [seed_env_folder, "--without-pip", "--activators", ""]  # pragma: no cover
        cli_run(args, setup_logging=False)  # pragma: no cover
