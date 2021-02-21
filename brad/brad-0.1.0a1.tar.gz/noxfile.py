import nox

# don't run format session by default
nox.options.sessions = ["lint", "test"]

SOURCES = ["src", "tests", "noxfile.py"]


@nox.session()
def lint(session):
    """Lint all source code"""
    session.install("black", "flake8", "isort", "mypy")
    session.run("black", "--check", *SOURCES)
    session.run("flake8", *SOURCES)
    session.run("isort", "--check", *SOURCES)
    session.run("mypy", *SOURCES)


@nox.session(python=["3.7", "3.8", "3.9"])
def test(session):
    """Run tests"""
    session.install(".")
    session.install("pytest", "pytest-cov")
    session.run("pytest")


@nox.session(name="format")
def format_(session):
    """Format all source code"""
    session.install("black", "isort")
    session.run("black", *SOURCES)
    session.run("isort", *SOURCES)


@nox.session()
def build(session):
    """Build package"""
    session.install(".", "build")
    session.run(
        "python", "-m", "build", "--sdist", "--wheel", "--outdir", "dist/"
    )
