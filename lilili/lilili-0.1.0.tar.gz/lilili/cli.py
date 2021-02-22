from cleo import Application, Command

from . import __title__, __version__
from .db.defs import Domain, Session
from .db.helpers import query_library_by_name
from .search import Search
from .server import webapp
from .utils import output


class SearchCommand(Command):
    """
    Search library information.

    search
        {input : input file path}
        {--domain=? : pypi, rubygems or npm}
        {--json : output in JSON format}
        {--yaml : output in YAML format}
    """

    def handle(self):
        input_file_path = self.argument("input")
        if self.option("domain"):
            domain = Domain(self.option("domain"))
        else:
            domain = None

        s = Search(input_file_path, domain=domain)
        progress = self.progress_bar(s.size)
        progress.set_format(
            " %current%/%max% [%bar%] %percent:3s%% %elapsed:6s%/%estimated:-6s%"
        )
        libraries = []
        for library in s.search_libraries():
            libraries.append(library)
            progress.advance()
        progress.finish()

        output(self.option("json"), self.option("yaml"), libraries)


class QueryCommand(Command):
    """
    Query library in database.

    query
        {name : library's name}
        {--json : output in JSON format}
        {--yaml : output in YAML format}
    """

    def handle(self):
        name = self.argument("name")
        session = Session()
        libraries = query_library_by_name(session, name)
        session.close()
        output(self.option("json"), self.option("yaml"), libraries)


class LoadCommand(Command):
    """
    Load libraries from file.

    load
        {input : input file path}
    """

    def handle(self):
        input_file_path = self.argument("input")
        print("input_file_path = " + input_file_path)
        raise NotImplementedError


class ServeCommand(Command):
    """
    Start up an HTTP server.

    serve
        {--host=? : host name}
        {--port=? : port number}
    """

    def handle(self):
        kwargs = {}
        if self.option("host"):
            kwargs["host"] = self.option("host")
        if self.option("port"):
            kwargs["port"] = self.option("port")
        kwargs["debug"] = True
        webapp.run(**kwargs)


def main():
    cliapp = Application(name=__title__, version=__version__, complete=True)
    cliapp.add(SearchCommand())
    cliapp.add(QueryCommand())
    cliapp.add(LoadCommand())
    cliapp.add(ServeCommand())
    cliapp.run()
