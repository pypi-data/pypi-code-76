import environ


@environ.config(prefix="")
class Config:
    @environ.config
    class Paths:
        templates = environ.var(".sigla/templates")
        snapshots = environ.var(".sigla/snapshots")
        definitions = environ.var(".sigla/definitions")
        filters = environ.var(".sigla/filters.py")

    path = environ.group(Paths)


config = environ.to_config(Config)
