import tempfile
import typing as T

import nox
from nox.sessions import Session

# Exclude black from the sessions run by default
nox.options.sessions = "lint", "tests", "mypy", "pytype"

package = "hypermodern_python"
locations = "src", "tests", "noxfile.py"
python_versions = ["3.10"]


def install_with_constraints(
    session: Session, group: str, *args: str, **kwargs: T.Any
) -> None:
    """Install packages constrained by Poetry's lock file.

    This function is a wrapper for nox.sessions.Session.install. It
    invokes pip to install packages inside of the session's virtualenv.
    Additionally, pip is passed a constraints file generated from
    Poetry's lock file, to ensure that the packages are pinned to the
    versions specified in poetry.lock. This allows you to manage the
    packages as Poetry development dependencies.

    Arguments:
        session: The Session object.
        args: Command-line arguments for pip.
        kwargs: Additional keyword arguments for Session.install.
    """
    with tempfile.NamedTemporaryFile() as requirements:
        session.run(
            "poetry",
            "export",
            "--with",
            group,
            "--format=constraints.txt",
            "--without-hashes",
            f"--output={requirements.name}",
            external=True,
        )
        session.install(f"--constraint={requirements.name}", *args, **kwargs)


@nox.session(python=python_versions)
def tests(session: Session) -> None:
    args = session.posargs or ["--cov", "-m", "not e2e"]
    session.run("poetry", "install", "--only", "main", external=True)
    install_with_constraints(
        session, "test", "coverage", "pytest", "pytest-cov", "pytest-mock"
    )
    session.run("pytest", *args)


@nox.session(python=python_versions)
def lint(session: Session) -> None:
    args = session.posargs or locations
    install_with_constraints(
        session,
        "lint",
        "flake8",
        "flake8-annotations",
        "flake8-bandit",
        "flake8-black",
        "flake8-bugbear",
        "flake8-import-order",
    )
    session.run("flake8", *args)


@nox.session(python=python_versions)
def black(session: Session) -> None:
    args = session.posargs or locations
    install_with_constraints(session, "lint", "black")
    session.run("black", *args)


@nox.session(python=python_versions)
def mypy(session: Session) -> None:
    args = session.posargs or locations
    install_with_constraints(session, "typing", "mypy", "click")
    session.run("mypy", "--install-types", "--non-interactive", *args)
    session.run("mypy", *args)


@nox.session(python=python_versions)
def pytype(session: Session) -> None:
    """Type-check using pytype."""
    args = session.posargs or ["--disable=import-error", *locations]
    install_with_constraints(session, "typing", "pytype")
    session.run("pytype", *args)
