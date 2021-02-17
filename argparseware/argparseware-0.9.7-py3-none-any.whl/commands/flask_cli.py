import abc
import typing
import sys
import json
import argparse
from flask import url_for
from flask import Flask
from werkzeug.routing import Rule
from werkzeug.exceptions import InternalServerError

from argparseware.utils import parse_inline_options
from . import Command
from . import CommandsMiddleware


class CommandError(RuntimeError):
    """
    Raised when a command throws an error.
    """


class ICommandParser(metaclass=abc.ABCMeta):
    """
    This abstract class can be implemented to parse routes into commands.
    """

    @classmethod
    def get_url(cls, app: Flask, rule: Rule, args: dict) -> str:
        """
        Build the URL for a specific set of arguments.
        """
        server_name = app.config.get('SERVER_NAME')
        app.config['SERVER_NAME'] = '.'

        try:
            with app.app_context():
                url = url_for(rule.endpoint, **args)
                return url[8:]
        finally:
            app.config['SERVER_NAME'] = server_name

    @classmethod
    def parse_docstring(cls, func: typing.Callable) -> None:
        pass

    @classmethod
    def get_endpoints(cls, app: Flask) -> typing.Tuple[Rule, typing.Callable]:
        """
        Parse the endpoints from a given application.
        """
        results = []
        for rule in app.url_map.iter_rules():
            func = app.view_functions[rule.endpoint]  # func
            item = (rule, func)
            results.append(item)

        return results

    @abc.abstractmethod
    def parse(self, rule: Rule, func: typing.Callable) -> typing.List[typing.Tuple[str, str]]:
        """
        Parse a rule into a list of command name and HTTP method pairs.
        """


class RouteCommandParser(ICommandParser):
    """
    This parser generates commands based on the route path.
    """

    # The method to command mapping
    METHOD_MAP = {
        'get': 'get',
        'post': 'create',
        'put': 'set',
        'patch': 'update',
        'delete': 'delete',
    }

    def __init__(self, *, use_method: bool = False, fold: bool = True) -> None:
        """
        When *use_method* is enabled, the request method (e.g.: POST) is used as the command name.
        Otherwise, it is mapped to a friendly name (e.g.: create).

        If *fold* is enabled, instances of rules that only have a single method will not add an
        additional level (e.g.: `app route get` would become `app route`).
        """
        self.use_method = use_method
        self.fold = fold

    def parse(self, rule: Rule, func: typing.Callable) -> typing.List[typing.Tuple[str, str]]:
        """
        Parse a rule into a list of command name and HTTP method pairs.
        """
        parts = []
        for part in rule.rule.strip('/').split('/'):
            if part[0] == '<' and part[-1] == '>':
                pass
            else:
                parts.append(part)
        prefix = ' '.join(parts)

        results = []
        methods = [x for x in rule.methods if x.lower() in self.METHOD_MAP]
        for method in methods:
            method = method.lower()
            suffix = method.lower() if self.use_method else self.METHOD_MAP[method]
            name = prefix if len(methods) == 1 and self.fold \
                else '{} {}'.format(prefix, suffix)

            item = (name, method.upper())
            results.append(item)

        return results


class FlaskCommandsMiddleware(CommandsMiddleware):
    """
    This middleware transforms Flask applications into command line applications.
    """

    def __init__(self, app: Flask, parser: ICommandParser = None, *,
                 params: typing.List[str] = ('-D', '--data'),
                 request_builder: typing.Callable[[dict], str] = json.dumps,
                 content_type: str = None, **kwargs) -> None:
        """
        The *app* argument is the Flask application to use. The *parser* arguments is the
        route parser to use (defaults to `RouteCommandParser`).

        The *params* argument sets the arguments to use when specifying query string or request
        body parameters.

        The *request_builder* argument is a callable that transforms the request body parameters
        into actual request body.

        The *content_type* argument defines the content type to use when using POST, PUT,
        PATCH and DELETE requests. It can sometimes be automatically detected from the
        *request_builder* argument.

        The *kwargs* argument are passed to the parent `CommandsMiddleware`.
        """
        super().__init__(**kwargs)
        self.app = app
        self.parser = parser or RouteCommandParser()
        self.params = list(params)
        self.request_builder = request_builder
        self.content_type = content_type
        self.dest = None

    def command_handler(self, rule: Rule, method: str, body_params=None):
        """
        Handle a dispatched command.
        """
        def error_handler(_):
            """ Handles exceptions thrown by the target. """
            raise CommandError()

        def handler(args):
            """ Dispatches the request and handle the response. """
            url = self.parser.get_url(self.app, rule, args.__dict__)
            client = self.app.test_client()
            self.app.errorhandler(InternalServerError)(error_handler)

            with self.app.app_context():
                func = getattr(client, method.lower())
                response = func(url)
                if response.json:
                    content = response.json
                else:
                    try:
                        content = response.data.decode('utf-8')
                    except AttributeError:
                        content = None

                if response.status_code >= 400:
                    raise CommandError(content)

                if isinstance(content, (list, dict)):
                    print(json.dumps(content, indent=2))
                else:
                    print(content)

        return handler

    def configure(self, parser: argparse.ArgumentParser) -> argparse.ArgumentParser:
        """
        Configure the middleware arguments.
        """
        self.commands = []

        endpoints = self.parser.get_endpoints(self.app)
        for rule, func in endpoints:
            items = self.parser.parse(rule, func)

            types = typing.get_type_hints(func)
            defaults = typing._get_defaults(func)  # pylint:disable=protected-access
            defaults.update(rule.defaults or {})

            for name, method in items:
                is_leaf = len([x for x, _ in items if x.startswith('{} '.format(name))]) == 0
                command = Command(name, self.command_handler(rule, method))

                if self.params and is_leaf:
                    arg = command.add_argument(*self.params, action='append',
                                               help='additional request parameters in format KEY=VALUE')
                    # self.dest = arg.dest

                for arg in rule.arguments:
                    default = defaults.get(arg)
                    data_type = types.get(arg, str)
                    command.add_argument('--{}'.format(arg), type=data_type, default=default,
                                         required=default is None)
                self.commands.append(command)

        return super().configure(parser)

    def run(self, args: argparse.Namespace) -> None:
        """
        Run the middleware.
        """
        if self.dest:
            params = getattr(args, self.dest)
            params = parse_inline_options(params)

        print(params)

        try:
            super().run(args)
        except CommandError as ex:
            msg = str(ex)
            if msg:
                print(msg)
            sys.exit(1)
