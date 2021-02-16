import nox

nox.options.sessions = ["test"]


@nox.session
def test(session):
    session.install("-e", ".[testing]")
    session.run("pytest")


@nox.session
def pack(session):
    session.install("build")
    session.run("python", "-m", "build", ".")