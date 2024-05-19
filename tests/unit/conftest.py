
import os

from moto import mock_aws
from moto.server import ThreadedMotoServer
import pytest


@pytest.fixture(scope="session")
def moto_creds() -> None:
    cred_env_vars = [
        "AWS_ACCESS_KEY_ID",
        "AWS_SECRET_ACCESS_KEY",
        "AWS_SECURITY_TOKEN",
        "AWS_SESSION_TOKEN"
    ]
    aws_creds = {}
    for env_var in cred_env_vars:
        aws_creds[env_var] = os.environ.get(env_var, None)
        os.environ[env_var] = "testing"

    yield

    for cred in aws_creds:
        if aws_creds[cred] is None:
            os.environ.pop(cred)
        else:
            os.environ[cred] = aws_creds[cred]


@pytest.fixture(scope="function")
def sts_moto(moto_creds: None) -> None:
    with mock_aws():
        yield 


@pytest.fixture(scope="function")
def moto_server(moto_creds: None) -> str:
    server = ThreadedMotoServer()
    server.start()

    yield "http://localhost:5000"

    server.stop()


@pytest.fixture(scope="function")
def role_arn() -> str:
    return "arn:aws:iam::123412341234:role/my_role"


@pytest.fixture(scope="function")
def session_name() -> str:
    return "tester-session"


@pytest.fixture(scope="function")
def sts_arn() -> str:
    return "arn:aws:sts::123412341234:assumed-role/my_role/tester-session"

