"""Easily create `boto3` assume role sessions with automatic credential refreshing.

Examples
--------
A minimum example to assume a role:

.. code-block:: python

    import boto3
    from boto3_assume import assume_role

    assume_session = assume_role(
        source_session=boto3.Session(), # You must pass in a boto3 session that automatically refreshes!
        assume_role_kwargs={
            "RoleArn": "arn:aws:iam::123412341234:role/my_role",
            "RoleSessionName": "my-role-session"
        }
    )
"""

__version__ = "0.2.0"
__all__ = [
    "assume_role_session",
    "assume_role",
    "Boto3AssumeError",
    "ForbiddenKWArgError",
    "MissingKWArgError"
]

from boto3_assume.core import assume_role_session, assume_role
from boto3_assume.exceptions import Boto3AssumeError, ForbiddenKWArgError, MissingKWArgError

try:
    from boto3_assume.aio_core import assume_role_aio_session
    __all__.append("assume_role_aio_session")
except ModuleNotFoundError as error: # pragma: no cover
    pass
