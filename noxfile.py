import nox

# Exclude black from the sessions run by default
nox.options.sessions = "lint", "tests"

locations = "src", "tests", "noxfile.py"
python_versions = ["3.10"]


@nox.session(python=python_versions)
def tests(session):
    args = session.posargs or ["--cov", "-m", "not e2e"]
    session.run("poetry", "install", external=True)
    session.run("pytest", *args)


@nox.session(python=python_versions)
def lint(session):
    args = session.posargs or locations
    session.install(
        "flake8",
        "flake8-bandit",
        "flake8-black",
        "flake8-bugbear",
        "flake8-import-order",
    )
    session.run("flake8", *args)


@nox.session(python=python_versions)
def black(session):
    args = session.posargs or locations
    session.install("black")
    session.run("black", *args)
