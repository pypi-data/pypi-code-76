import jinja2

env = jinja2.Environment(
    loader=jinja2.PackageLoader("wgmgr", "templates"),
    lstrip_blocks=True,
    trim_blocks=True,
)


def load_template(name: str) -> jinja2.Template:
    return env.get_template(name)
