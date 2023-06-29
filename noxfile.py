
import sys

import nox

nox.options.sessions = [
    "unit-tests-py"
]

@nox.session(name="publish-package")
def publish_package(session: nox.Session):
    """Build a new src dist and wheel, then publish to PYPI.
    """
    dev_venv_setup(session=session)
    session.run(
        "rm", "-rf", "./build/", "./dist/",
        external=True
    )
    session.run("python", "-m", "build", "--sdist", "--wheel")
    session.run("twine", "upload", "dist/*", "--repository", "boto3-assume")


@nox.session(name="unit-tests")
def unit_tests_current_python(session: nox.Session):
    """Run the unit tests in the current venv and generate html coverage report at ./htmlcov/index.html
    """
    if "--no-venv" not in sys.argv:
        dev_venv_setup(session=session)

    session.run("coverage", "erase")
    session.run("pytest", "-vvv", "--cov=src/boto3_assume", "--cov-report", "html", "tests/unit")


@nox.session(
    name="unit-tests-py",
    python=[
        "3.8",
        "3.9",
        "3.10",
        "3.11"
    ]
)
def unit_tests(session: nox.Session):
    """Run tests with all supported python version and generate missing coverage report in terminal.
    """
    dev_venv_setup(session=session)
    session.run("coverage", "erase")
    session.run("pytest", "-vvv", "--cov=src/boto3_assume", "--cov-report", "term-missing", "tests/unit")


@nox.session(name="dev-venv")
def dev_venv_setup(session: nox.Session):
    session.install("-U", "pip", "build")
    session.install("-e", ".[dev,all]")

