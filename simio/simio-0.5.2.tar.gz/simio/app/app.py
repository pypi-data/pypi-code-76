from asyncio import AbstractEventLoop
from typing import Callable, Type, Any, Awaitable, Iterator

from aiohttp import web
from aiohttp.web_runner import BaseSite, TCPSite


class Application:
    """
    Abstraction for simio's application
    """

    def __init__(
        self, app_runner: web.AppRunner, loop: AbstractEventLoop,
    ):
        """
        You can modify aiohttp's AppRunner with app_runner_config
        app_runner_config is passing to AppRunner constructor

        aiohttp_site_cls is aiohttp's site class that will start app
        Read aiohttp docs for more info

        Also custom event loop can be chosen. Pass it in builder.
        """
        self._loop = loop
        self._runner = app_runner

    @property
    def app(self):
        return self._runner.app

    @property
    def runner(self):
        return self._runner

    def run(
        self,
        run_forever: bool = True,
        log_func: Callable[..., None] = print,
        site_cls: Type[BaseSite] = TCPSite,
        **site_kwargs,
    ):
        """
        Runs aiohttp's application

        All BaseSites's parameters can be passed in kwargs
        such as host, port and other

        log_func is function that will print info about app start

        If run_forever is true, then this method will block execution
        """
        self._loop.run_until_complete(self._runner.setup())
        site = site_cls(runner=self._runner, **site_kwargs)
        self._loop.run_until_complete(site.start())

        log_func(f"======== Running on {site.name} ========\n(Press CTRL+C to quit)")
        if run_forever:
            self._loop.run_forever()

    def add_startup(self, *startup_funcs: Callable[[Any], Awaitable]):
        self.app.on_startup.append(*startup_funcs)

    def add_cleanup(self, *cleanup_funcs: Callable[[Any], Awaitable]):
        self.app.on_cleanup.append(*cleanup_funcs)

    def add_shutdown(self, *shutdown_funcs: Callable[[Any], Awaitable]):
        self.app.on_shutdown.append(*shutdown_funcs)

    def __getitem__(self, key: str) -> Any:
        return self.app[key]

    def __setitem__(self, key: str, value: Any) -> None:
        self.app[key] = value

    def __delitem__(self, key: str) -> None:
        del self.app[key]

    def __len__(self) -> int:
        return len(self.app)

    def __iter__(self) -> Iterator[str]:
        return iter(self.app)
